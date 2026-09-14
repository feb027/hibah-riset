#!/usr/bin/env python3
"""Cetak parameter dan GFLOPs model hasil fine-tuning sendiri (bukan angka tabel vendor).

Alasan script ini ada: angka params/GFLOPs pada Tabel 7 paper YOLO26 adalah untuk model
rilis yang sudah difusi (Conv+BatchNorm digabung, cabang one-to-many dilepas). Model yang
kita fine-tune adalah arsitektur pelatihan penuh, dan bila jumlah kelasnya berbeda dari
COCO 80 kelas, jumlah parameternya ikut berbeda. Jadi angka yang benar untuk Tabel 1
adalah yang dicetak dari bobot kita sendiri, seperti yang diminta pembimbing.

Jalankan di mesin yang menyimpan folder runs/detect (bobot best.pt):
    python3 scripts/journal/report_model_stats.py
Hasilnya berupa potongan tabel markdown siap tempel.
"""
from __future__ import annotations

import re
from pathlib import Path

RUNS = Path("runs/detect")
# nama folder run -> label di naskah
RUNS_MAP = {
    "yolo_crowdhuman": "YOLO26n",
    "yolo_crowdhuman_small": "YOLO26s",
    "yolo10_crowdhuman": "YOLOv10n",
    "yolo11_crowdhuman": "YOLOv11n",
}


def main() -> None:
    try:
        from ultralytics import YOLO
    except ImportError:
        raise SystemExit("ultralytics belum terpasang: pip install ultralytics")

    rows = []
    for folder, label in RUNS_MAP.items():
        weights = RUNS / folder / "weights" / "best.pt"
        if not weights.is_file():
            print(f"[SKIP] {label}: {weights} tidak ada")
            continue

        model = YOLO(str(weights))
        # info() mencetak ringkasan; ambil angkanya dari layer agar bisa dipakai di tabel
        model.info(verbose=False)
        n_params = sum(p.numel() for p in model.model.parameters())
        n_layers = len(list(model.model.modules()))
        # GFLOPs pada resolusi 640 (nilai tercetak info() mengikuti imgsz model)
        gflops = getattr(model.model, "gflops", None)
        if callable(gflops):  # beberapa versi menyimpan callable
            gflops = gflops(640)
        nc = getattr(model.model, "nc", None)

        rows.append({
            "label": label,
            "params": n_params / 1e6,
            "gflops": float(gflops) if gflops else float("nan"),
            "nc": nc,
            "layers": n_layers,
        })
        print(f"{label}: {n_params/1e6:.2f} juta parameter, {gflops} GFLOPs, nc={nc}")

    if not rows:
        raise SystemExit("tidak ada bobot best.pt yang ditemukan; cek folder runs/detect")

    print("\n| Arsitektur | Params (juta) | FLOPs (G) |")
    print("|---|---|---|")
    for r in rows:
        print(f"| {r['label']} | {r['params']:.2f} | {r['gflops']:.2f} |")

    ncs = {r["nc"] for r in rows}
    print(f"\njumlah kelas pada bobot fine-tune: {ncs}")
    if ncs == {1}:
        print("Catatan untuk naskah: bobot dilatih dengan satu kelas (person), sehingga jumlah "
              "parameter head berbeda dari angka COCO 80 kelas pada paper vendor. Pakai angka "
              "di tabel atas untuk Tabel 1, bukan angka paper.")
    else:
        print("Catatan: jumlah kelas bukan 1; periksa kembali konfigurasi dataset sebelum "
              "menyimpulkan perbedaan parameter terhadap paper vendor.")


if __name__ == "__main__":
    main()
