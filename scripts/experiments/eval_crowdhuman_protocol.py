"""Evaluasi ulang model terlatih dengan protokol CrowdHuman resmi.

Menutup dua batasan yang tercatat di docs/reports/laporan-skenario-a-finetuning-yolo.md:

1. **Region ignore diperlakukan netral.** Pada evaluasi Ultralytics sebelumnya,
   kotak bertanda `extra.ignore == 1` (3,52% dari 103.115 kotak) ikut dihitung
   sebagai target wajib, sehingga model dihukum karena gagal mendeteksi objek
   yang oleh datasetnya sendiri dinyatakan ambigu. Angka mAP sebelumnya
   karenanya bersifat pesimistis.

2. **Metrik MR^-2 dihitung.** Ini metrik konvensional untuk CrowdHuman; tanpa
   itu hasil penelitian tidak punya pembanding di literatur.

Tidak ada pelatihan ulang: script ini hanya menjalankan inferensi pada
validation set memakai checkpoint yang sudah ada. Ground truth dibaca langsung
dari .odgt, jadi label YOLO hasil konversi juga tidak perlu dibuat ulang.

Contoh:
    python scripts/experiments/eval_crowdhuman_protocol.py
    python scripts/experiments/eval_crowdhuman_protocol.py --limit 500   # uji cepat
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
from src.eval_mr2 import evaluate_detections, load_odgt_ground_truth  # noqa: E402

DEFAULT_ODGT = "data/raw/crowdhuman/extracted/annotation_val.odgt"
DEFAULT_IMAGES_DIR = "data/processed/crowdhuman/images/val"
DEFAULT_OUTPUT_CSV = "experiments/crowdhuman_protocol_results.csv"


def discover_weights():
    found = sorted(str(p) for p in Path("runs/detect").glob("*/weight*/best.pt"))
    if not found:
        raise FileNotFoundError("Tidak ada checkpoint di runs/detect/*/weight*/best.pt")
    return found


def batch_for(weights, requested):
    """Turunkan batch ke 1 untuk model ONNX ber-bentuk statis.

    Ultralytics meng-export ONNX dengan `dynamic=False` secara bawaan, sehingga
    dimensi batch terkunci di 1 dan pengiriman batch lebih besar ditolak runtime.

    Model tidak di-export ulang dengan bentuk dinamis secara sengaja: berkas
    ONNX yang divalidasi akurasinya di sini harus persis berkas yang diukur
    kecepatannya pada eksperimen CPU, dan model bentuk dinamis dapat berjalan
    pada kecepatan berbeda.
    """
    if str(weights).endswith(".onnx") and requested > 1:
        print(f"    (batch diturunkan ke 1: {Path(weights).name} ber-bentuk statis)")
        return 1
    return requested


def predict_all(weights, image_paths, conf, batch, max_det):
    """Jalankan inferensi, kembalikan {image_id: (boxes_xyxy, scores)}.

    Ambang confidence sengaja sangat rendah: kurva miss-rate/FPPI membutuhkan
    ekor deteksi berkeyakinan rendah agar titik FPPI tinggi dapat tercapai.
    Memotongnya di 0,25 akan membuat MR^-2 tampak lebih buruk dari seharusnya.

    `max_det` dibiarkan pada 300 untuk seluruh model karena kepala one-to-one
    YOLO26 memang terbatas pada 300 deteksi per citra secara arsitektural.
    Menaikkannya hanya untuk model lain akan membuat perbandingan timpang.
    Nilai 300 sudah lebih dari cukup untuk rentang FPPI 0,01-1,0 yang dipakai
    MR^-2, karena FPPI 1,0 hanya menuntut rata-rata satu false positive per citra.
    """
    from ultralytics import YOLO

    model = YOLO(weights)
    predictions = {}

    for start in range(0, len(image_paths), batch):
        chunk = image_paths[start : start + batch]
        for path, result in zip(
            chunk, model([str(p) for p in chunk], conf=conf, max_det=max_det, verbose=False)
        ):
            boxes = result.boxes
            predictions[Path(path).stem] = (
                boxes.xyxy.cpu().numpy() if boxes is not None else np.zeros((0, 4)),
                boxes.conf.cpu().numpy() if boxes is not None else np.zeros(0),
            )

        done = min(start + batch, len(image_paths))
        print(f"\r    {done}/{len(image_paths)} citra", end="", flush=True)

    print()
    return predictions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", nargs="+", default=None)
    parser.add_argument("--odgt", default=DEFAULT_ODGT)
    parser.add_argument("--images-dir", default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--conf", type=float, default=0.001, help="Ambang confidence minimum")
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--max-det", type=int, default=300, help="Batas deteksi per citra (lihat predict_all)")
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
    gt_strict = load_odgt_ground_truth(args.odgt, exclude_ignore_from_gt=True)
    gt_naive = load_odgt_ground_truth(args.odgt, exclude_ignore_from_gt=False)

    n_strict = sum(len(v["boxes"]) for v in gt_strict.values())
    n_naive = sum(len(v["boxes"]) for v in gt_naive.values())
    print(f"  protokol resmi   : {n_strict} kotak target ({len(gt_strict)} citra)")
    print(f"  tanpa pengecualian: {n_naive} kotak target  <- protokol lama")
    print(f"  selisih          : {n_naive - n_strict} kotak dipindah ke status ignore\n")

    rows = []
    for weights in weights_list:
        meta = describe_weights(weights)
        print(f"--- {meta['alias']}  ({weights})")

        predictions = predict_all(
            weights, image_paths, args.conf, batch_for(weights, args.batch), args.max_det
        )
        strict = evaluate_detections(predictions, gt_strict)
        naive = evaluate_detections(predictions, gt_naive)

        print(
            f"    MR^-2 {strict['mr2']:.4f} | AP@0.5 {strict['ap50']:.4f} | "
            f"recall maks {strict['recall_max']:.4f}"
        )

        rows.append(
            {
                "weights": weights,
                "arsitektur": meta["alias"],
                "source_id": meta["source_id"] or "-",
                "mr2": round(strict["mr2"], 4),
                "ap50": round(strict["ap50"], 4),
                "recall_maks": round(strict["recall_max"], 4),
                "ap50_protokol_lama": round(naive["ap50"], 4),
                "recall_maks_protokol_lama": round(naive["recall_max"], 4),
                "selisih_ap50": round(strict["ap50"] - naive["ap50"], 4),
                "n_gt": strict["n_gt"],
                "n_citra": strict["n_images"],
            }
        )

    rows.sort(key=lambda r: r["mr2"])

    header = (
        f"{'Arsitektur':<12} | {'MR^-2':<8} | {'AP@0.5':<8} | {'Recall maks':<12} | "
        f"{'AP@0.5 lama':<12} | {'Selisih'}"
    )
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r['arsitektur']:<12} | {r['mr2']:<8.4f} | {r['ap50']:<8.4f} | "
            f"{r['recall_maks']:<12.4f} | {r['ap50_protokol_lama']:<12.4f} | {r['selisih_ap50']:+.4f}"
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
        "\nCatatan pembacaan: MR^-2 semakin KECIL semakin baik - kebalikan dari mAP.\n"
        "Kolom 'AP@0.5 lama' memakai protokol sebelumnya (region ignore dihitung\n"
        "sebagai target wajib) dan disertakan agar besarnya dampak koreksi terlihat.\n"
        "AP@0.5 di sini dihitung ulang oleh script ini, jadi angkanya dapat sedikit\n"
        "berbeda dari mAP50 Ultralytics karena beda konvensi interpolasi; yang\n"
        "dibandingkan adalah antar kolom di baris yang sama, bukan lintas alat ukur."
    )


if __name__ == "__main__":
    main()
