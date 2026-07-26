"""Komparasi kualitatif deteksi pada gambar kerumunan: simpan overlay per model.

Menghasilkan gambar beranotasi untuk dilihat mata, sebagai pendamping angka mAP.
Berguna untuk melihat pola kegagalan yang tidak tertangkap satu angka agregat:
orang jauh yang terlewat, box ganda pada satu orang, atau kerumunan padat yang
menyatu jadi satu box.

Dua hal yang dijaga:

- Gambar dipilih deterministik berdasarkan kepadatan anotasi, sehingga
  perbandingan antar model dilakukan pada gambar yang sama persis, dan hasilnya
  bisa direproduksi.
- Nama berkas keluaran mencantumkan status model: `zeroshot` untuk bobot
  pra-latih COCO, `finetuned` untuk hasil training CrowdHuman. Keduanya tidak
  boleh tertukar saat dipilih jadi gambar di naskah.

Contoh:
    python scripts/experiments/test_zeroshot.py
    python scripts/experiments/test_zeroshot.py --weights yolo11n.pt --images 5
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import cv2  # noqa: E402

from src.detector import describe_weights  # noqa: E402
from src.utils.crowdhuman import densest_images  # noqa: E402

DEFAULT_ODGT = "data/raw/crowdhuman/extracted/annotation_val.odgt"
DEFAULT_IMAGES_DIR = "data/processed/crowdhuman/images/val"
DEFAULT_OUTPUT_DIR = "experiments/zeroshot"
FALLBACK_WEIGHTS = ["yolov10n.pt", "yolo11n.pt", "yolo26n.pt"]


def discover_weights():
    """Bobot pra-latih plus seluruh checkpoint hasil training yang ditemukan."""
    trained = sorted(str(p) for p in Path("runs/detect").glob("*/weight*/best.pt"))
    return FALLBACK_WEIGHTS + trained


def mode_of(weights):
    """`finetuned` kalau bobot berasal dari folder hasil training, selain itu `zeroshot`."""
    return "finetuned" if "runs" in Path(weights).parts else "zeroshot"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", nargs="+", default=None)
    parser.add_argument("--odgt", default=DEFAULT_ODGT)
    parser.add_argument("--images-dir", default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--images", type=int, default=3, help="Jumlah gambar terpadat")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--out-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    from ultralytics import YOLO

    weights_list = args.weights or discover_weights()
    selected = densest_images(args.odgt, args.images_dir, n=args.images)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\nGambar uji terpilih (paling padat, urutan deterministik):")
    for path, count in selected:
        print(f"  {path.name}  -  {count} orang beranotasi")

    results_table = []
    for weights in weights_list:
        meta = describe_weights(weights)
        mode = mode_of(weights)
        print(f"\n--- {meta['alias']} [{mode}]  ({weights})")

        model = YOLO(weights)
        for img_path, gt_count in selected:
            results = model(str(img_path), classes=[0], conf=args.conf, verbose=False)
            n_detected = len(results[0].boxes)

            out_path = out_dir / f"{img_path.stem}_{meta['alias']}_{mode}.jpg"
            cv2.imwrite(str(out_path), results[0].plot())

            print(f"    {img_path.name}: {n_detected} terdeteksi / {gt_count} beranotasi")
            results_table.append((meta["alias"], mode, img_path.name, n_detected, gt_count))

    print(f"\n{len(results_table)} gambar overlay tersimpan di {out_dir}")
    print(
        "\nCatatan pembacaan: 'terdeteksi vs beranotasi' hanya perbandingan jumlah,\n"
        "bukan pengukuran benar-salah. Jumlah yang pas bisa saja berasal dari satu\n"
        "orang terlewat yang ditutup satu false positive. Gambar ini untuk analisis\n"
        "kualitatif pola kegagalan; angka resminya tetap dari mAP."
    )


if __name__ == "__main__":
    main()
