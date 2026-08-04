#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figur laporan Skenario B dari artifacts eksperimen (eval_results.csv, detection_stats.csv).

Menghasilkan PNG di experiments/s2_tracker/figs/:
  fig1_hota_mota_idf1.png   bar HOTA/MOTA/IDF1 per benchmark
  fig2_idsw_frag.png        bar IDSW/Frag per benchmark
  fig3_density_dance.png    kepadatan deteksi per sekuens DanceTrack (dets/frame)
  fig4_density_mot20.png    kepadatan deteksi per sekuens MOT20 (dets/frame)
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "s2_tracker"
FIGS = EXP / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

# --- data evaluasi -----------------------------------------------------------
rows = list(csv.DictReader((EXP / "eval_results.csv").open()))
metrics = ["HOTA", "MOTA", "IDF1"]
by_bm = {}
for r in rows:
    by_bm[r["benchmark"]] = {m: float(r[m]) for m in metrics + ["IDSW", "Frag"]}

# --- Fig 1: HOTA / MOTA / IDF1 -------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
bms = ["MOT20", "DanceTrack"]
x = np.arange(len(metrics))
w = 0.35
for j, bm in enumerate(bms):
    vals = [by_bm[bm][m] for m in metrics]
    bars = ax.bar(x + (j - 0.5) * w, vals, w, label=bm, color=["#2c6fbb", "#e07b39"][j])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=12)
ax.set_ylabel("Skor (%)")
ax.set_ylim(0, 85)
ax.set_title("Skenario B — OC-SORT: HOTA / MOTA / IDF1 per benchmark", fontsize=12)
ax.legend(frameon=False)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGS / "fig1_hota_mota_idf1.png")
plt.close(fig)

# --- Fig 2: IDSW / Frag --------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
x = np.arange(2)
for j, bm in enumerate(bms):
    for k, m in enumerate(["IDSW", "Frag"]):
        v = by_bm[bm][m]
        ax.bar(x[j] + (k - 0.5) * w, v, w, label=f"{bm} {m}", color=["#2c6fbb", "#9bb8d8", "#e07b39", "#f0c097"][j * 2 + k])
ax.set_xticks(x)
ax.set_xticklabels(bms)
ax.set_ylabel("Jumlah per seluruh sekuens")
ax.set_title("Skenario B — OC-SORT: ID Switch & Fragmentasi per benchmark", fontsize=12)
ax.legend(frameon=False, ncol=2)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGS / "fig2_idsw_frag.png")
plt.close(fig)

# --- Fig 3: kepadatan deteksi DanceTrack -----------------------------------------
rows = list(csv.DictReader((EXP / "detection_stats.csv").open()))
dance = [r for r in rows if r.get("dataset") == "dancetrack"]
if dance:
    names = [r["sequence"] for r in dance]
    dens = [int(r["dets"]) / max(1, int(r["frames"])) for r in dance]
    order = np.argsort(dens)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    cols = plt.cm.viridis(np.linspace(0.15, 0.9, len(dance)))
    ax.barh([names[i] for i in order], [dens[i] for i in order], color=cols)
    ax.set_xlabel("Deteksi per frame (rata-rata)")
    ax.set_title("Kepadatan deteksi per sekuens — DanceTrack val (deteksi YOLO26 fine-tune)", fontsize=11)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGS / "fig3_density_dance.png")
    plt.close(fig)

# --- Fig 4: kepadatan deteksi MOT20 (dari log run, deteksi .pt GPU) -----------------
mot20 = {
    "MOT20-01": (214, 18839),
    "MOT20-02": (1391, 157368),
    "MOT20-03": (1202, 276114),
    "MOT20-05": (1657, 449452),
}
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
names = list(mot20)
dens = [d / f for f, d in mot20.values()]
bars = ax.bar(names, dens, color="#2c6fbb")
for b, v in zip(bars, dens):
    ax.text(b.get_x() + b.get_width() / 2, v + 5, f"{v:.0f}", ha="center", fontsize=9)
ax.set_ylabel("Deteksi per frame (rata-rata)")
ax.set_title("Kepadatan deteksi per sekuens — MOT20 train (deteksi YOLO26 fine-tune)", fontsize=11)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGS / "fig4_density_mot20.png")
plt.close(fig)

print("figur tersimpan di", FIGS)
for f in sorted(FIGS.glob("*.png")):
    print("  ", f.name)
