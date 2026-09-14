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

import contextlib
import io
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

        # Angka diambil dari keluaran model.info() karena atribut .gflops tidak selalu terisi
        # dan nilainya berbeda antar versi ultralytics.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            model.info()
        info = buf.getvalue()
        print(info.strip())

        m_params = re.search(r"([\d,]+)\s+parameters", info)
        m_gflops = re.search(r"([\d.]+)\s+GFLOPs", info)
        n_params = int(m_params.group(1).replace(",", "")) if m_params else sum(
            p.numel() for p in model.model.parameters())
        gflops = float(m_gflops.group(1)) if m_gflops else float("nan")
        nc = getattr(model.model, "nc", None)

        rows.append({
            "label": label,
            "params": n_params / 1e6,
            "gflops": gflops,
            "nc": nc,
        })
        print(f"--> {label}: {n_params/1e6:.2f} juta parameter, {gflops} GFLOPs, nc={nc}\n")

    if not rows:
        raise SystemExit("tidak ada bobot best.pt yang ditemukan; cek folder runs/detect")

    print("\n| Arsitektur | Params (juta) | FLOPs (G) |")
    print("|---|---|---|")
    for r in rows:
        g = "n/a" if r["gflops"] != r["gflops"] else f"{r['gflops']:.2f}"
        print(f"| {r['label']} | {r['params']:.2f} | {g} |")

    ncs = {r["nc"] for r in rows}
    print(f"\njumlah kelas pada bobot fine-tune: {ncs}")
    if ncs == {1}:
        print("Catatan untuk naskah: bobot dilatih dengan satu kelas (person), sehingga jumlah "
              "parameter head berbeda dari angka COCO 80 kelas pada paper vendor. Pakai angka "
              "di tabel atas untuk Tabel 1, bukan angka paper.")
    if any(r["gflops"] != r["gflops"] for r in rows):
        print("\nFLOPs belum terbaca dari info(). Jalankan sekali lagi dengan "
              "`model.info(verbose=True)` atau pakai ultralytics.utils.torch_utils.get_flops, "
              "lalu salin angka GFLOPs yang tercetak di atas.")


if __name__ == "__main__":
    main()
