"""Benchmark detektor di CPU, membandingkan runtime PyTorch lawan ONNX.

Eksperimen ini menguji dua klaim inti YOLO26 yang belum tersentuh oleh
pengukuran di GPU (lihat docs/reports/laporan-skenario-a-finetuning-yolo.md
Bagian 6.3):

1. "Up to 43% faster CPU inference" - klaim ini spesifik menyebut CPU, dan
   angka rujukan di dokumentasi vendor adalah angka CPU ONNX, bukan PyTorch.
2. "DFL dihapus sehingga export lebih sederhana" - klaim tentang kemudahan
   deployment, yang hanya terlihat kalau proses export benar-benar dijalankan.

Karena itu script ini mencatat bukan hanya latensi, tetapi juga keberhasilan
export, durasinya, dan ukuran berkas ONNX yang dihasilkan. Kegagalan export
adalah hasil eksperimen yang sah dan dilaporkan apa adanya, bukan dianggap
error yang menghentikan pengujian.

Protokol pengukuran (gambar terpadat, pemanasan penuh, statistik p50/p95)
sengaja dibuat identik dengan test_nms_overhead.py agar hasil CPU dapat
disandingkan langsung dengan hasil GPU.

Catatan: di CPU setiap iterasi jauh lebih mahal daripada di GPU, jadi nilai
bawaan --iters dan --warmup dibuat lebih kecil. Naikkan bila waktu memungkinkan.

Contoh:
    python scripts/experiments/test_cpu_onnx.py
    python scripts/experiments/test_cpu_onnx.py --iters 10 --images 3
    python scripts/experiments/test_cpu_onnx.py --skip-export   # pakai .onnx yang sudah ada
"""
from __future__ import annotations

import argparse
import csv
import os
import platform
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from src.detector import describe_weights  # noqa: E402
from src.utils.benchmark import summarize, warmup  # noqa: E402
from src.utils.crowdhuman import densest_images  # noqa: E402

DEFAULT_ODGT = "data/raw/crowdhuman/extracted/annotation_val.odgt"
DEFAULT_IMAGES_DIR = "data/processed/crowdhuman/images/val"
DEFAULT_OUTPUT_CSV = "experiments/cpu_onnx_results.csv"
FALLBACK_WEIGHTS = ["yolo11n.pt", "yolov10n.pt", "yolo26n.pt"]


def discover_weights():
    found = sorted(str(p) for p in Path("runs/detect").glob("*/weight*/best.pt"))
    return found or FALLBACK_WEIGHTS


def export_onnx(weights, imgsz, skip_existing):
    """Export ke ONNX. Mengembalikan (path, detik, ukuran_MB, pesan_error).

    Kegagalan export dikembalikan sebagai pesan, bukan dilempar sebagai
    exception, karena "model X tidak bisa di-export" adalah temuan yang ingin
    dicatat - bukan alasan untuk membatalkan seluruh eksperimen.
    """
    from ultralytics import YOLO

    expected = Path(weights).with_suffix(".onnx")
    if skip_existing and expected.exists():
        return str(expected), 0.0, expected.stat().st_size / 1e6, None

    try:
        start = time.perf_counter()
        produced = YOLO(weights).export(format="onnx", imgsz=imgsz, simplify=True)
        elapsed = time.perf_counter() - start
        path = Path(produced)
        return str(path), elapsed, path.stat().st_size / 1e6, None
    except Exception as exc:  # noqa: BLE001 - pesan apa pun tetap ingin dicatat
        return None, 0.0, 0.0, f"{type(exc).__name__}: {exc}"


def benchmark_cpu(weights, image_paths, iters, warmup_rounds):
    """Ukur latensi di CPU. Mengembalikan (statistik_inference, statistik_post, deteksi)."""
    from ultralytics import YOLO

    model = YOLO(weights)
    warmup(model, image_paths, warmup_rounds, classes=[0], device="cpu")

    inference_ms, postprocess_ms, detections = [], [], []
    for img_path in image_paths:
        for _ in range(iters):
            results = model(img_path, classes=[0], device="cpu", verbose=False)
            speed = results[0].speed
            inference_ms.append(speed["inference"])
            postprocess_ms.append(speed["postprocess"])
            detections.append(len(results[0].boxes))

    return summarize(inference_ms), summarize(postprocess_ms), statistics.mean(detections)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", nargs="+", default=None)
    parser.add_argument("--odgt", default=DEFAULT_ODGT)
    parser.add_argument("--images-dir", default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--images", type=int, default=3, help="Jumlah gambar terpadat")
    parser.add_argument("--iters", type=int, default=10, help="Pengulangan per gambar")
    parser.add_argument("--warmup", type=int, default=3, help="Putaran pemanasan")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--skip-export", action="store_true", help="Pakai .onnx yang sudah ada")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    weights_list = args.weights or discover_weights()
    selected = densest_images(args.odgt, args.images_dir, n=args.images)
    image_paths = [str(p) for p, _ in selected]

    print(f"\nPerangkat : {platform.processor() or platform.machine()}")
    print(f"Core      : {os.cpu_count()} logical")
    print("\nGambar uji terpilih (paling padat, urutan deterministik):")
    for path, count in selected:
        print(f"  {path.name}  -  {count} orang beranotasi")
    print(f"\n{len(weights_list)} model x {args.images} gambar x {args.iters} iterasi\n")

    rows = []
    for weights in weights_list:
        meta = describe_weights(weights)
        print(f"--- {meta['alias']}  ({weights})")

        print("    PyTorch CPU ...", end="", flush=True)
        pt_inf, pt_post, pt_det = benchmark_cpu(weights, image_paths, args.iters, args.warmup)
        print(f" {pt_inf['p50']:.1f} ms")

        print("    export ONNX ...", end="", flush=True)
        onnx_path, export_s, onnx_mb, error = export_onnx(weights, args.imgsz, args.skip_export)
        if error:
            print(f" GAGAL - {error}")
            onnx_inf = onnx_post = None
            onnx_det = 0.0
        else:
            print(f" {export_s:.1f} s, {onnx_mb:.1f} MB")
            print("    ONNX CPU    ...", end="", flush=True)
            onnx_inf, onnx_post, onnx_det = benchmark_cpu(
                onnx_path, image_paths, args.iters, args.warmup
            )
            print(f" {onnx_inf['p50']:.1f} ms")

        speedup = (pt_inf["p50"] / onnx_inf["p50"]) if onnx_inf and onnx_inf["p50"] else 0.0

        rows.append(
            {
                # Path bobot disertakan agar tiap baris tetap dapat diidentifikasi
                # walau arsitekturnya gagal dikenali (mis. args.yaml tidak ada).
                "weights": weights,
                "arsitektur": meta["alias"],
                "source_id": meta["source_id"] or "-",
                "nms_free": {True: "ya", False: "tidak", None: "?"}[meta["nms_free"]],
                "export_ok": "tidak" if error else "ya",
                "export_detik": round(export_s, 1),
                "onnx_mb": round(onnx_mb, 1),
                "pt_inference_p50": round(pt_inf["p50"], 2),
                "pt_inference_p95": round(pt_inf["p95"], 2),
                "pt_postprocess_p50": round(pt_post["p50"], 3),
                "onnx_inference_p50": round(onnx_inf["p50"], 2) if onnx_inf else "",
                "onnx_inference_p95": round(onnx_inf["p95"], 2) if onnx_inf else "",
                "onnx_postprocess_p50": round(onnx_post["p50"], 3) if onnx_post else "",
                "speedup_onnx": round(speedup, 2) if speedup else "",
                "deteksi_pt": round(pt_det, 1),
                "deteksi_onnx": round(onnx_det, 1) if onnx_inf else "",
                "error": error or "",
            }
        )

    header = (
        f"{'Arsitektur':<12} | {'NMS-free':<8} | {'PyTorch p50':<12} | {'ONNX p50':<10} | "
        f"{'Speedup':<8} | {'Export':<8} | {'ONNX MB'}"
    )
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for r in rows:
        onnx_cell = f"{r['onnx_inference_p50']} ms" if r["onnx_inference_p50"] != "" else "gagal"
        speed_cell = f"{r['speedup_onnx']}x" if r["speedup_onnx"] != "" else "-"
        print(
            f"{r['arsitektur']:<12} | {r['nms_free']:<8} | {r['pt_inference_p50']:<9} ms | "
            f"{onnx_cell:<10} | {speed_cell:<8} | {r['export_ok']:<8} | {r['onnx_mb']}"
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
        "\nCatatan pembacaan: bandingkan kolom PyTorch dan ONNX dalam satu baris untuk\n"
        "melihat manfaat export, dan bandingkan antar baris untuk melihat selisih\n"
        "arsitektur. Klaim vendor '43% faster CPU inference' merujuk angka CPU ONNX,\n"
        "sehingga yang relevan menguji klaim itu adalah kolom ONNX, bukan PyTorch.\n"
        "Kolom Export dan ONNX MB menguji klaim terpisah soal kemudahan deployment;\n"
        "export yang gagal dicatat apa adanya sebagai hasil, bukan disembunyikan.\n"
        "Latensi CPU sangat bergantung jumlah core dan beban lain di mesin - catat\n"
        "spesifikasi perangkat saat melaporkan angka ini."
    )


if __name__ == "__main__":
    main()
