"""Pecah kinerja detektor menurut tingkat oklusi dan ukuran objek.

Recall agregat mencampur orang yang berdiri sendirian dengan orang yang hanya
tampak kepalanya, sehingga menyembunyikan justru kondisi yang menjadi pernyataan
masalah inti penelitian ini. Script ini memisahkannya.

Dua pengelompokan:

1. **Tingkat oklusi**, dari rasio luas vbox terhadap fbox. CrowdHuman sudah
   menganotasi keduanya, jadi tingkat oklusi tidak perlu diperkirakan.
   Menjawab: seberapa cepat kinerja detektor runtuh saat orang saling menutupi,
   dan apakah keunggulan recall arsitektur NMS-free (lihat laporan Skenario A
   Bagian 6.3) memang berasal dari kasus tumpang tindih. Kalau selisihnya
   membesar pada kelompok teroklusi berat, penjelasan mekanisnya terdukung;
   kalau rata di semua kelompok, penjelasan itu harus dicabut.

2. **Ukuran objek**, dari tinggi fbox dalam piksel. Untuk pejalan kaki, tinggi
   lebih mewakili jarak ke kamera daripada luas kotak. Menjawab klaim ProgLoss
   /STAL YOLO26 soal objek kecil, sekaligus relevan langsung karena pada kamera
   CCTV ruang publik orang di kejauhan tampak kecil dan paling sering terlewat.

Saat satu kelompok dinilai, kotak di luar kelompok dipindahkan ke status ignore,
bukan dihapus - lihat docstring subset_ground_truth untuk alasannya.

Contoh:
    python scripts/experiments/eval_breakdown.py
    python scripts/experiments/eval_breakdown.py --limit 500
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from src.detector import describe_weights  # noqa: E402
from src.eval_mr2 import (  # noqa: E402
    evaluate_detections,
    load_odgt_ground_truth,
    subset_ground_truth,
)

DEFAULT_ODGT = "data/raw/crowdhuman/extracted/annotation_val.odgt"
DEFAULT_IMAGES_DIR = "data/processed/crowdhuman/images/val"
DEFAULT_OUTPUT_CSV = "experiments/breakdown_results.csv"

# Ambang oklusi mengikuti konvensi umum deteksi pejalan kaki.
OCCLUSION_GROUPS = [
    ("terlihat penuh", "visibility >= 0.65", lambda a: a["visibility"] >= 0.65),
    ("teroklusi sebagian", "0.35 - 0.65", lambda a: (a["visibility"] >= 0.35) & (a["visibility"] < 0.65)),
    ("teroklusi berat", "visibility < 0.35", lambda a: a["visibility"] < 0.35),
]

# Ambang tinggi mengikuti konvensi Caltech (near / medium / far).
SIZE_GROUPS = [
    ("besar (dekat)", "tinggi >= 150 px", lambda a: a["height"] >= 150),
    ("sedang", "50 - 150 px", lambda a: (a["height"] >= 50) & (a["height"] < 150)),
    ("kecil (jauh)", "tinggi < 50 px", lambda a: a["height"] < 50),
]

# Memisahkan pemotongan bingkai dari oklusi. Anotasi fbox bersifat amodal,
# sehingga orang di tepi citra tampak "kurang terlihat" padahal tidak tertutup
# siapa pun. Dimensi ini membuat pengaruh itu terbaca langsung di tabel.
TRUNCATION_GROUPS = [
    ("utuh dalam bingkai", "fbox tidak menembus tepi", lambda a: a["truncated"] < 0.5),
    ("terpotong tepi", "fbox menembus tepi", lambda a: a["truncated"] >= 0.5),
]

# Oklusi murni: hanya orang yang seluruh fbox-nya berada di dalam bingkai,
# sehingga rasio visibility benar-benar mengukur tertutupnya oleh orang lain.
OCCLUSION_CLEAN_GROUPS = [
    (f"{nama} (utuh)", f"{aturan}, tidak terpotong", (lambda fn: lambda a: fn(a) & (a["truncated"] < 0.5))(fn))
    for nama, aturan, fn in OCCLUSION_GROUPS
]


def discover_weights():
    found = sorted(str(p) for p in Path("runs/detect").glob("*/weight*/best.pt"))
    if not found:
        raise FileNotFoundError("Tidak ada checkpoint di runs/detect/*/weight*/best.pt")
    return found


def batch_for(weights, requested):
    """Turunkan batch ke 1 untuk model ONNX ber-bentuk statis.

    Ultralytics meng-export ONNX dengan `dynamic=False` secara bawaan, sehingga
    dimensi batch terkunci di 1 dan pengiriman batch lebih besar ditolak runtime.
    """
    if str(weights).endswith(".onnx") and requested > 1:
        print(f"    (batch diturunkan ke 1: {Path(weights).name} ber-bentuk statis)")
        return 1
    return requested


def predict_all(weights, image_paths, conf, batch, max_det, nms_iou):
    """Inferensi sekali per model; hasilnya dipakai ulang untuk semua kelompok.

    `nms_iou` diteruskan ke predictor. Sebelumnya tidak pernah diteruskan sama
    sekali, sehingga model ber-NMS memakai nilai bawaan Ultralytics (0,7) yang
    tidak pernah ditala untuk anotasi amodal CrowdHuman. Akibatnya perbandingan
    "arsitektur ber-NMS lawan NMS-free" bercampur dengan "hiperparameter tak
    ditala" - menyapu nilai ini memisahkan keduanya.
    """
    from ultralytics import YOLO

    model = YOLO(weights)
    predictions = {}

    for start in range(0, len(image_paths), batch):
        chunk = image_paths[start : start + batch]
        for path, result in zip(
            chunk,
            model([str(p) for p in chunk], conf=conf, max_det=max_det, iou=nms_iou, verbose=False),
        ):
            boxes = result.boxes
            predictions[Path(path).stem] = (
                boxes.xyxy.cpu().numpy() if boxes is not None else np.zeros((0, 4)),
                boxes.conf.cpu().numpy() if boxes is not None else np.zeros(0),
            )
        print(f"\r    {min(start + batch, len(image_paths))}/{len(image_paths)} citra", end="", flush=True)

    print()
    return predictions


def report_distribution(ground_truth, groups, judul):
    """Cetak sebaran target per kelompok agar pembaca tahu bobot tiap baris."""
    total = sum(len(gt["boxes"]) for gt in ground_truth.values())
    print(f"\nSebaran target - {judul} (total {total}):")

    for name, rule, fn in groups:
        n = sum(int(np.count_nonzero(fn(gt["attrs"]))) for gt in ground_truth.values() if len(gt["boxes"]))
        share = 100.0 * n / total if total else 0.0
        print(f"  {name:<20} {rule:<20} {n:>7} ({share:5.1f}%)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", nargs="+", default=None)
    parser.add_argument("--odgt", default=DEFAULT_ODGT)
    parser.add_argument("--images-dir", default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--conf", type=float, default=0.001)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--max-det", type=int, default=300)
    parser.add_argument(
        "--iou", type=float, default=0.5,
        help="Ambang IoU pencocokan deteksi-target. Naikkan ke 0.75 untuk menguji hipotesis "
             "kredit-okluder: dua fbox amodal yang bertindih dengan cakupan c memberi "
             "IoU=c/(2-c), sehingga kelompok teroklusi berat (c>0.65) mendarat di IoU~0.48-0.50, "
             "berimpit dengan ambang 0.5. Bila anomali berat>sebagian runtuh pada 0.75, "
             "penyebabnya memang deteksi atas si penutup yang terkredit ke target.")
    parser.add_argument(
        "--nms-iou", type=float, default=0.7,
        help="Ambang IoU untuk NMS di predictor (bawaan Ultralytics 0.7). Hanya berpengaruh "
             "pada arsitektur ber-NMS.")
    parser.add_argument("--limit", type=int, default=None, help="Batasi jumlah citra (uji cepat)")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    weights_list = args.weights or discover_weights()

    image_paths = sorted(Path(args.images_dir).rglob("*.jpg"))
    if args.limit:
        image_paths = image_paths[: args.limit]
    if not image_paths:
        raise FileNotFoundError(f"Tidak ada .jpg di bawah {args.images_dir}")

    print(f"\nMemuat ground truth dari {args.odgt} ...")
    # images_dir wajib diberikan agar visibility dihitung terhadap bagian fbox
    # yang berada di dalam bingkai - lihat docstring load_odgt_ground_truth.
    ground_truth = load_odgt_ground_truth(
        args.odgt, exclude_ignore_from_gt=True, images_dir=args.images_dir
    )

    report_distribution(ground_truth, OCCLUSION_GROUPS, "tingkat oklusi")
    report_distribution(ground_truth, TRUNCATION_GROUPS, "pemotongan bingkai")
    report_distribution(ground_truth, OCCLUSION_CLEAN_GROUPS, "oklusi murni (tanpa yang terpotong)")
    report_distribution(ground_truth, SIZE_GROUPS, "ukuran objek")

    # Subset dibangun sekali saja, lalu dipakai untuk seluruh model.
    subsets = {
        ("oklusi", name): subset_ground_truth(ground_truth, fn)
        for name, _, fn in OCCLUSION_GROUPS
    }
    for dimensi, groups in [
        ("ukuran", SIZE_GROUPS),
        ("pemotongan", TRUNCATION_GROUPS),
        ("oklusi murni", OCCLUSION_CLEAN_GROUPS),
    ]:
        subsets.update(
            {(dimensi, name): subset_ground_truth(ground_truth, fn) for name, _, fn in groups}
        )

    rows = []
    for weights in weights_list:
        meta = describe_weights(weights)
        print(f"\n--- {meta['alias']}  ({weights})")

        predictions = predict_all(
            weights, image_paths, args.conf, batch_for(weights, args.batch), args.max_det, args.nms_iou
        )

        for (dimensi, kelompok), subset_gt in subsets.items():
            hasil = evaluate_detections(predictions, subset_gt, iou_thr=args.iou)
            rows.append(
                {
                    "arsitektur": meta["alias"],
                    "nms_free": {True: "ya", False: "tidak", None: "?"}[meta["nms_free"]],
                    "dimensi": dimensi,
                    "kelompok": kelompok,
                    "recall_maks": round(hasil["recall_max"], 4),
                    "ap50": round(hasil["ap50"], 4),
                    "mr2": round(hasil["mr2"], 4),
                    "n_gt": hasil["n_gt"],
                    "iou_cocok": args.iou,
                    "nms_iou": args.nms_iou,
                }
            )

    for dimensi, groups in [
        ("oklusi", OCCLUSION_GROUPS),
        ("oklusi murni", OCCLUSION_CLEAN_GROUPS),
        ("pemotongan", TRUNCATION_GROUPS),
        ("ukuran", SIZE_GROUPS),
    ]:
        print(f"\n{'=' * 78}\nRECALL MAKSIMUM menurut {dimensi.upper()}\n{'=' * 78}")

        arsitektur = []
        for r in rows:
            if r["arsitektur"] not in arsitektur:
                arsitektur.append(r["arsitektur"])

        header = f"{'Arsitektur':<12} | {'NMS-free':<9} | " + " | ".join(f"{n:<18}" for n, _, _ in groups)
        print(header)
        print("-" * len(header))

        for arch in arsitektur:
            cells = []
            nms = "?"
            for name, _, _ in groups:
                match = [r for r in rows if r["arsitektur"] == arch and r["dimensi"] == dimensi and r["kelompok"] == name]
                if match:
                    nms = match[0]["nms_free"]
                    cells.append(f"{match[0]['recall_maks']:<18.4f}")
                else:
                    cells.append(f"{'-':<18}")
            print(f"{arch:<12} | {nms:<9} | " + " | ".join(cells))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nTersimpan ke {out_path}  (AP@0.5 dan MR^-2 per kelompok ikut tercatat)")
    print(
        "\nCatatan pembacaan: bandingkan penurunan recall dari kiri ke kanan dalam satu\n"
        "baris untuk melihat seberapa cepat kinerja runtuh, dan bandingkan antar baris\n"
        "pada kolom yang sama untuk melihat arsitektur mana yang lebih tahan. Kelompok\n"
        "dengan jumlah target kecil (lihat sebaran di atas) menghasilkan angka yang\n"
        "goyah - jangan tarik kesimpulan dari kelompok yang isinya sedikit."
    )


if __name__ == "__main__":
    main()
