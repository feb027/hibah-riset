#!/usr/bin/env python3
"""Fig. 4 gabungan: sensitivitas cooldown (a) + sensitivitas confidence (b), satu baris dua panel.

Menggantikan dua figur terpisah supaya hemat tinggi halaman. Font diperbesar karena tiap
panel hanya selebar setengah kolom.

Persiapan data sengaja disalin dari scripts/make_journal_figs.py (Fig 6 dan Fig 7) supaya
skrip generator lama tidak ikut jalan dan menulis ulang figur lain.

Jalankan dengan python yang punya matplotlib, mis.:
    /tmp/plotenv/bin/python scripts/journal/make_combined_fig.py
Keluaran: experiments/journal_figs/fig4ab_cooldown_conf.png
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "experiments" / "s3_counting"
OUT = ROOT / "experiments" / "journal_figs" / "fig4ab_cooldown_conf.png"

TICK, LABEL, LEGEND, ANNOT = 11, 12, 10, 10


def read_csv(path: Path) -> list[dict]:
    return list(csv.DictReader(open(path)))


def panel_a(ax) -> None:
    cd: dict[int, tuple[float, float]] = {}
    for r in read_csv(CSV / "sensitivity_cooldown.csv"):
        if r["tracker"] == "deepocsort":
            cd[int(r["cooldown_frames"])] = (float(r["mae"]), float(r["error_pct"]))
    cds = sorted(cd)

    ax.plot(cds, [cd[c][0] for c in cds], "o-", color="#4472c4", label="MAE (orang)")
    ax.set_xlabel("Cooldown (frame)", fontsize=LABEL)
    ax.set_ylabel("MAE (orang)", color="#4472c4", fontsize=LABEL)
    ax.tick_params(axis="y", labelcolor="#4472c4", labelsize=TICK)
    ax.tick_params(axis="x", labelsize=TICK)
    twin = ax.twinx()
    twin.plot(cds, [cd[c][1] for c in cds], "s--", color="#ed7d31", label="Galat (%)")
    twin.set_ylabel("Galat (%)", color="#ed7d31", fontsize=LABEL)
    twin.tick_params(axis="y", labelcolor="#ed7d31", labelsize=TICK)
    twin.annotate("naive = 101,99%", xy=(0, cd[0][1]), xytext=(12, 86), fontsize=ANNOT, color="#555")
    for a in (ax, twin):
        a.spines[["top"]].set_visible(False)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = twin.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=LEGEND, loc="upper right")


def panel_b(ax) -> None:
    rows = read_csv(CSV / "sensitivity_confidence.csv")
    conf = [float(r["conf_threshold"]) for r in rows]
    err = [float(r["error_pct"]) for r in rows]
    fps = [float(r["fps_throughput"]) for r in rows]

    ax.plot(conf, err, "s-", color="#ed7d31", label="Galat (%)")
    ax.set_xlabel("Confidence threshold", fontsize=LABEL)
    ax.set_ylabel("Galat (%)", color="#ed7d31", fontsize=LABEL)
    ax.tick_params(axis="y", labelcolor="#ed7d31", labelsize=TICK)
    ax.tick_params(axis="x", labelsize=TICK)
    twin = ax.twinx()
    twin.plot(conf, fps, "^--", color="#70ad47", label="Throughput (FPS)")
    twin.set_ylabel("Throughput (FPS)", color="#70ad47", fontsize=LABEL)
    twin.tick_params(axis="y", labelcolor="#70ad47", labelsize=TICK)
    ax.axvspan(0.25, 0.30, alpha=0.15, color="green")
    ax.annotate("rentang operasional", xy=(0.275, 12), ha="center", fontsize=ANNOT, color="#375623")
    for a in (ax, twin):
        a.spines[["top"]].set_visible(False)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = twin.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=LEGEND, loc="upper left")


def main() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4), constrained_layout=True)
    panel_a(axes[0])
    panel_b(axes[1])
    axes[0].set_title("(a)", loc="left", fontsize=13, fontweight="bold")
    axes[1].set_title("(b)", loc="left", fontsize=13, fontweight="bold")
    fig.savefig(OUT, dpi=200)
    print(f"[SUKSES] {OUT} ({OUT.stat().st_size // 1024} KB)")

    # cek: angka pada figur harus sama dengan CSV dan dengan Tabel 8/9 di naskah
    cd = {int(r["cooldown_frames"]): r for r in read_csv(CSV / "sensitivity_cooldown.csv")
          if r["tracker"] == "deepocsort"}
    assert abs(float(cd[30]["mae"]) - 6.34) < 0.01
    assert abs(float(cd[0]["error_pct"]) - 101.99) < 0.01
    conf = {float(r["conf_threshold"]): r for r in read_csv(CSV / "sensitivity_confidence.csv")}
    assert abs(float(conf[0.2]["error_pct"]) - 1.67) < 0.01
    assert abs(float(conf[0.6]["error_pct"]) - 25.43) < 0.01
    print("verifikasi OK: angka pada figur cocok dengan Tabel 8 dan Tabel 9")


if __name__ == "__main__":
    main()
