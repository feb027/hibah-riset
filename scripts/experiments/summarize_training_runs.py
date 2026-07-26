"""Rangkum seluruh run training di runs/detect/ menjadi satu tabel komparasi.

Membaca baris epoch terakhir dari setiap results.csv dan mencetaknya sebagai
tabel Markdown yang siap ditempel ke naskah Skenario A. Tujuannya menghindari
salah salin angka secara manual ke tabel paper.

Contoh:
    python scripts/experiments/summarize_training_runs.py
    python scripts/experiments/summarize_training_runs.py --runs-dir runs/detect --out docs/reports/tabel-skenario-a.md
"""

import argparse
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from src.detector import describe_weights  # noqa: E402

METRICS = [
    ("metrics/precision(B)", "Precision"),
    ("metrics/recall(B)", "Recall"),
    ("metrics/mAP50(B)", "mAP50"),
    ("metrics/mAP50-95(B)", "mAP50-95"),
]


def read_final_row(results_csv):
    with open(results_csv, newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-1] if rows else None


def collect(runs_dir):
    summaries = []
    for results_csv in sorted(Path(runs_dir).glob("*/results.csv")):
        row = read_final_row(results_csv)
        if row is None:
            print(f"[lewat] {results_csv} kosong")
            continue

        # Arsitektur ditelusuri lewat args.yaml, bukan ditebak dari nama folder,
        # supaya run yang salah beri nama tetap terbaca apa adanya.
        checkpoint = next(results_csv.parent.glob("weight*/best.pt"), None)
        meta = describe_weights(checkpoint) if checkpoint else {"alias": "?", "source_id": None}

        summaries.append(
            {
                "run": results_csv.parent.name,
                "arsitektur": meta["alias"],
                "source_id": meta["source_id"] or "-",
                "epochs": int(float(row["epoch"])),
                "hours": float(row["time"]) / 3600.0,
                **{label: float(row[key]) for key, label in METRICS},
            }
        )
    return summaries


def render(summaries):
    summaries = sorted(summaries, key=lambda s: s["mAP50-95"], reverse=True)

    lines = [
        "| Run | Arsitektur | Sumber | Epoch | " + " | ".join(label for _, label in METRICS) + " | Waktu (jam) |",
        "|---|---|---|---|" + "---|" * (len(METRICS) + 1),
    ]
    for s in summaries:
        cells = " | ".join(f"{s[label]:.4f}" for _, label in METRICS)
        lines.append(
            f"| {s['run']} | {s['arsitektur']} | {s['source_id']} | {s['epochs']} | "
            f"{cells} | {s['hours']:.2f} |"
        )

    if len(summaries) > 1:
        best, worst = summaries[0], summaries[-1]
        spread = best["mAP50-95"] - worst["mAP50-95"]
        lines += [
            "",
            f"Rentang mAP50-95 antar run: {spread:.4f} "
            f"({worst['run']} -> {best['run']}).",
            "",
            "> Catatan: setiap angka berasal dari satu run dengan satu seed. Selisih "
            "di bawah ~0,01 mAP tidak dapat dibedakan dari variasi acak dan tidak "
            "boleh ditulis sebagai keunggulan salah satu model.",
            "> Kolom waktu adalah durasi training, bukan kecepatan inferensi. Jangan "
            "dipakai untuk klaim kecepatan; GPU dapat terbagi dengan run lain.",
        ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", default="runs/detect", help="Folder berisi hasil training")
    parser.add_argument("--out", default=None, help="Tulis tabel ke file Markdown")
    args = parser.parse_args()

    summaries = collect(args.runs_dir)
    if not summaries:
        raise SystemExit(f"Tidak ada results.csv di bawah {args.runs_dir}")

    table = render(summaries)
    print()
    print(table)
    print()

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(table + "\n", encoding="utf-8")
        print(f"Tersimpan ke {out_path}")


if __name__ == "__main__":
    main()


