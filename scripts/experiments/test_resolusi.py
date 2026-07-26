"""Uji penskalaan resolusi input: FPS dan jumlah deteksi dari 256 sampai 640.

Tujuannya menemukan titik trade-off antara kecepatan dan kemampuan menangkap
orang berukuran kecil di kerumunan, sebagai bahan keputusan deployment di
Skenario D.

Beberapa hal yang dijaga supaya angkanya sah:

- Pengukuran dirata-ratakan atas beberapa gambar terpadat, bukan satu gambar
  yang kebetulan muncul pertama dari filesystem. Jumlah deteksi pada satu
  gambar tunggal terlalu bergantung pada isi gambar itu.
- Semua model dibatasi ke kelas person supaya beban post-processing sebanding
  antara model pra-latih COCO dan model hasil fine-tune.
- Label grafik diambil dari katalog detektor, jadi tidak ada daftar label
  paralel yang harus disinkronkan manual setiap kali daftar model berubah.

Contoh:
    python scripts/experiments/test_resolusi.py
    python scripts/experiments/test_resolusi.py --weights yolo11n.pt yolov10n.pt
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.detector import describe_weights  # noqa: E402
from src.utils.crowdhuman import densest_images  # noqa: E402

DEFAULT_ODGT = "data/raw/crowdhuman/extracted/annotation_val.odgt"
DEFAULT_IMAGES_DIR = "data/processed/crowdhuman/images/val"
RESOLUTIONS = [256, 320, 416, 480, 512, 640]
FALLBACK_WEIGHTS = ["yolov10n.pt", "yolo11n.pt", "yolo26n.pt"]


def discover_weights():
    found = sorted(str(p) for p in Path("runs/detect").glob("*/weight*/best.pt"))
    return found or FALLBACK_WEIGHTS


def measure(model, image_paths, res, iters):
    """Rata-rata FPS end-to-end dan jumlah deteksi pada satu resolusi."""
    total_ms = 0.0
    total_det = 0
    n = 0

    for img_path in image_paths:
        for _ in range(iters):
            results = model(img_path, imgsz=res, classes=[0], conf=0.25, verbose=False)
            speed = results[0].speed
            total_ms += speed["preprocess"] + speed["inference"] + speed["postprocess"]
            total_det += len(results[0].boxes)
            n += 1

    avg_ms = total_ms / n
    return 1000.0 / avg_ms, total_det / n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", nargs="+", default=None)
    parser.add_argument("--odgt", default=DEFAULT_ODGT)
    parser.add_argument("--images-dir", default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--images", type=int, default=5, help="Jumlah gambar terpadat")
    parser.add_argument("--iters", type=int, default=5, help="Pengulangan per gambar per resolusi")
    parser.add_argument("--plot", default="experiments/resolusi_scaling.png")
    parser.add_argument("--out", default="experiments/resolusi_scaling_results.csv")
    args = parser.parse_args()

    from ultralytics import YOLO

    weights_list = args.weights or discover_weights()
    selected = densest_images(args.odgt, args.images_dir, n=args.images)
    image_paths = [str(p) for p, _ in selected]

    print("\nGambar uji terpilih (paling padat, urutan deterministik):")
    for path, count in selected:
        print(f"  {path.name}  -  {count} orang beranotasi")
    print()

    series = []
    rows = []
    for weights in weights_list:
        label = describe_weights(weights)["alias"]
        print(f"--- {label}  ({weights})")

        model = YOLO(weights)
        for _ in range(3):
            model(image_paths[0], imgsz=640, classes=[0], verbose=False)

        fps_points, det_points = [], []
        for res in RESOLUTIONS:
            fps, det = measure(model, image_paths, res, args.iters)
            fps_points.append(fps)
            det_points.append(det)
            print(f"    {res}x{res}  ->  {fps:6.1f} FPS  |  {det:5.1f} deteksi/gambar")
            rows.append(
                {
                    "model": label,
                    "weights": weights,
                    "resolusi": res,
                    "fps": round(fps, 2),
                    "deteksi_rata2": round(det, 2),
                }
            )

        series.append((label, fps_points, det_points))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    markers = ["o", "s", "^", "D", "v", "P"]

    ax1.set_title("Kecepatan Pemrosesan (FPS) vs Resolusi", fontweight="bold")
    ax1.set_xlabel("Resolusi input (piksel)")
    ax1.set_ylabel("FPS (lebih tinggi lebih cepat)")
    ax2.set_title("Kemampuan Deteksi vs Resolusi", fontweight="bold")
    ax2.set_xlabel("Resolusi input (piksel)")
    ax2.set_ylabel(f"Deteksi per gambar (rata-rata {args.images} gambar)")

    for i, (label, fps_points, det_points) in enumerate(series):
        marker = markers[i % len(markers)]
        ax1.plot(RESOLUTIONS, fps_points, marker=marker, linewidth=2, label=label)
        ax2.plot(RESOLUTIONS, det_points, marker=marker, linewidth=2, label=label)

    ax1.axhline(y=30, color="red", linestyle="--", alpha=0.5, label="Batas real-time (30 FPS)")
    for ax in (ax1, ax2):
        ax.grid(True, alpha=0.4, linestyle="--")
        ax.legend()

    plt.tight_layout()
    Path(args.plot).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.plot, dpi=300, bbox_inches="tight")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nGrafik : {args.plot}")
    print(f"Data   : {out_path}")
    print(
        "\nCatatan pembacaan: 'deteksi per gambar' bukan akurasi. Deteksi yang lebih\n"
        "banyak bisa berarti lebih sedikit orang terlewat, bisa juga berarti lebih\n"
        "banyak false positive. Untuk menilai akurasi, pakai mAP/recall dari\n"
        "summarize_training_runs.py, bukan grafik ini."
    )


if __name__ == "__main__":
    main()
