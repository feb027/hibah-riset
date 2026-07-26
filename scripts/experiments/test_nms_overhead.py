"""Ukur latensi inference dan post-processing (NMS) per arsitektur detektor.

Ini eksperimen inti Skenario A: apakah arsitektur NMS-free benar-benar memangkas
biaya post-processing dibanding arsitektur yang masih memakai NMS.

Tiga hal yang dijaga di sini karena menentukan sah-tidaknya angka yang keluar:

1. Gambar uji dipilih berdasarkan kepadatan anotasi, bukan urutan filesystem.
   Biaya NMS naik seiring jumlah kandidat box, jadi gambar sepi akan
   mengecilkan efek yang justru ingin diukur. Pemilihannya deterministik
   supaya angka bisa direproduksi di mesin lain.

2. Semua model dibatasi ke kelas person. Model pra-latih COCO mengenali 80
   kelas sedangkan model hasil fine-tune hanya satu, dan selisih itu sendiri
   sudah mengubah beban NMS.

3. Sifat NMS-free dibaca dari katalog detektor, bukan ditebak dari potongan
   nama file. Untuk checkpoint hasil training, arsitekturnya ditelusuri lewat
   args.yaml. Sifat itu dicetak apa adanya sebagai fakta arsitektur, tanpa
   label menghakimi seperti "cepat"/"lambat" - justru itu yang diukur.

Contoh:
    python scripts/experiments/test_nms_overhead.py
    python scripts/experiments/test_nms_overhead.py --weights yolo11n.pt yolov10n.pt --images 10
"""
from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from src.detector import describe_weights  # noqa: E402
from src.utils.crowdhuman import densest_images  # noqa: E402

DEFAULT_ODGT = "data/raw/crowdhuman/extracted/annotation_val.odgt"
DEFAULT_IMAGES_DIR = "data/processed/crowdhuman/images/val"
DEFAULT_OUTPUT_CSV = "experiments/nms_overhead_results.csv"

# Dipakai kalau tidak ada checkpoint hasil training yang ditemukan.
FALLBACK_WEIGHTS = ["yolo11n.pt", "yolov10n.pt", "yolo26n.pt"]


def discover_weights():
    """Cari checkpoint hasil training di runs/detect, urut nama supaya stabil."""
    found = sorted(str(p) for p in Path("runs/detect").glob("*/weight*/best.pt"))
    return found or FALLBACK_WEIGHTS


def benchmark(model, image_paths, iters):
    from ultralytics import YOLO  # noqa: F401  (diimpor di main, dipakai lewat `model`)

    inference_ms, postprocess_ms, detections = [], [], []

    # Warmup: alokasi CUDA dan kompilasi kernel tidak boleh masuk hitungan.
    for _ in range(5):
        model(image_paths[0], classes=[0], verbose=False)

    for img_path in image_paths:
        for _ in range(iters):
            results = model(img_path, classes=[0], verbose=False)
            speed = results[0].speed
            inference_ms.append(speed["inference"])
            postprocess_ms.append(speed["postprocess"])
            detections.append(len(results[0].boxes))

    return inference_ms, postprocess_ms, detections


def mean_sd(values):
    if len(values) < 2:
        return (values[0] if values else 0.0), 0.0
    return statistics.mean(values), statistics.stdev(values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", nargs="+", default=None, help="Daftar bobot model (default: hasil training di runs/detect)")
    parser.add_argument("--odgt", default=DEFAULT_ODGT, help="Anotasi .odgt untuk memilih gambar terpadat")
    parser.add_argument("--images-dir", default=DEFAULT_IMAGES_DIR, help="Folder gambar validasi")
    parser.add_argument("--images", type=int, default=5, help="Jumlah gambar terpadat yang dipakai")
    parser.add_argument("--iters", type=int, default=20, help="Pengulangan per gambar")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_CSV, help="File CSV hasil")
    args = parser.parse_args()

    from ultralytics import YOLO

    weights_list = args.weights or discover_weights()
    selected = densest_images(args.odgt, args.images_dir, n=args.images)
    image_paths = [str(p) for p, _ in selected]

    print("\nGambar uji terpilih (paling padat, urutan deterministik):")
    for path, count in selected:
        print(f"  {path.name}  -  {count} orang beranotasi")
    print(f"\n{len(weights_list)} model x {args.images} gambar x {args.iters} iterasi\n")

    rows = []
    for weights in weights_list:
        meta = describe_weights(weights)
        print(f"--- {weights}")

        model = YOLO(weights)
        inference_ms, postprocess_ms, detections = benchmark(model, image_paths, args.iters)

        inf_mean, inf_sd = mean_sd(inference_ms)
        post_mean, post_sd = mean_sd(postprocess_ms)
        total = inf_mean + post_mean

        rows.append(
            {
                "weights": weights,
                "arsitektur": meta["alias"],
                "source_id": meta["source_id"] or "-",
                "nms_free": {True: "ya", False: "tidak", None: "?"}[meta["nms_free"]],
                "inference_ms": round(inf_mean, 3),
                "inference_sd": round(inf_sd, 3),
                "postprocess_ms": round(post_mean, 3),
                "postprocess_sd": round(post_sd, 3),
                "postprocess_pct": round(100.0 * post_mean / total, 2) if total else 0.0,
                "deteksi_rata2": round(statistics.mean(detections), 1),
            }
        )

    header = f"{'Arsitektur':<12} | {'NMS-free':<8} | {'Inference (ms)':<18} | {'Post-process (ms)':<20} | {'Post %':<7} | {'Deteksi'}"
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for r in rows:
        inf = f"{r['inference_ms']:.2f} +/- {r['inference_sd']:.2f}"
        post = f"{r['postprocess_ms']:.2f} +/- {r['postprocess_sd']:.2f}"
        print(
            f"{r['arsitektur']:<12} | {r['nms_free']:<8} | {inf:<18} | {post:<20} | "
            f"{r['postprocess_pct']:<7.1f} | {r['deteksi_rata2']}"
        )
    print("-" * len(header))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nTersimpan ke {out_path}")
    print(
        "\nCatatan pembacaan: kolom 'Post-process' adalah biaya yang dihapus arsitektur\n"
        "NMS-free. Bandingkan model dalam tier yang sama saja (nano lawan nano),\n"
        "karena antar-tier selisihnya didominasi ukuran model, bukan arsitektur.\n"
        "Simpangan baku disertakan supaya selisih yang lebih kecil dari noise\n"
        "pengukuran tidak dilaporkan sebagai temuan."
    )


if __name__ == "__main__":
    main()
