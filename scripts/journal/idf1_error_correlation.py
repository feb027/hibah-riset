#!/usr/bin/env python3
"""Korelasi peringkat antara konsistensi identitas (IDF1) dan galat hitung.

Dipakai untuk klaim pada Sub-bab 4.3: galat hitung mengikuti kualitas asosiasi. Tidak
memerlukan dataset, hanya dua berkas yang sudah ada di repo:

  experiments/s3_counting/counting_metrics.csv   galat per sekuens (State Machine CD=30)
  docs/reports/laporan-skenario-b-tracker.md     HOTA/MOTA/IDF1/IDSW per benchmark

Jalankan: python3 scripts/journal/idf1_error_correlation.py
"""
from __future__ import annotations

import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# IDF1 dan IDSW per (tracker, benchmark); dikutip dari Tabel 5 laporan Skenario B
IDF1 = {("diffmot", "MOT20"): 53.86, ("deepocsort", "MOT20"): 42.16,
        ("ocsort", "MOT20"): 42.88, ("lighttrack", "MOT20"): 34.69,
        ("diffmot", "DanceTrack"): 43.39, ("deepocsort", "DanceTrack"): 27.38,
        ("ocsort", "DanceTrack"): 26.63, ("lighttrack", "DanceTrack"): 18.91}
IDSW = {("diffmot", "MOT20"): 6905, ("deepocsort", "MOT20"): 11751,
        ("ocsort", "MOT20"): 14293, ("lighttrack", "MOT20"): 13121,
        ("diffmot", "DanceTrack"): 2784, ("deepocsort", "DanceTrack"): 5948,
        ("ocsort", "DanceTrack"): 6701, ("lighttrack", "DanceTrack"): 6697}
TRACKERS = ["diffmot", "deepocsort", "ocsort", "lighttrack"]
LABEL = {"ocsort": "OC-SORT", "deepocsort": "Deep-OC-SORT", "diffmot": "DiffMOT", "lighttrack": "LightTrack"}


def spearman(a: list[float], b: list[float]) -> float:
    def ranks(xs):
        order = sorted(range(len(xs)), key=lambda i: xs[i])
        r = [0] * len(xs)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(len(a)))
    den = (sum((ra[i] - ma) ** 2 for i in range(len(a))) * sum((rb[i] - mb) ** 2 for i in range(len(a)))) ** 0.5
    return num / den


def counting_error() -> dict[tuple[str, str], float]:
    path = ROOT / "experiments" / "s3_counting" / "counting_metrics.csv"
    rows = [r for r in csv.DictReader(open(path)) if r["model"] == "State Machine (CD=30)"]
    g: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in rows:
        bench = "MOT20" if r["seq"].startswith("MOT20") else "DanceTrack"
        g[(r["tracker"], bench)].append(float(r["Error_Pct"]))
    return {k: st.mean(v) for k, v in g.items()}


def main() -> None:
    err = counting_error()
    if not err:
        sys.exit("counting_metrics.csv tidak memuat baris State Machine (CD=30)")

    for bench in ("DanceTrack", "MOT20"):
        keys = sorted((k for k in err if k[1] == bench), key=lambda k: -IDF1[k])
        print(f"--- {bench} ---")
        for k in keys:
            print(f"  {LABEL[k[0]]:13s} IDF1 {IDF1[k]:6.2f}  IDSW {IDSW[k]:6d}  galat {err[k]:6.2f}%")
        rho = spearman([IDF1[k] for k in keys], [err[k] for k in keys])
        print(f"  spearman(IDF1, galat) = {rho:+.3f}  (n={len(keys)})")

    allk = sorted(err)
    rho_idf1 = spearman([IDF1[k] for k in allk], [err[k] for k in allk])
    rho_idsw = spearman([IDSW[k] for k in allk], [err[k] for k in allk])
    print(f"\n8 titik (4 tracker x 2 benchmark): spearman(IDF1, galat) = {rho_idf1:+.3f}, "
          f"spearman(IDSW, galat) = {rho_idsw:+.3f}")

    avg_idf1 = {t: st.mean([IDF1[(t, b)] for b in ("MOT20", "DanceTrack")]) for t in TRACKERS}
    avg_err = {t: st.mean([err[(t, b)] for b in ("MOT20", "DanceTrack")]) for t in TRACKERS}
    print("\nrata-rata dua benchmark:")
    for t in TRACKERS:
        print(f"  {LABEL[t]:13s} IDF1 {avg_idf1[t]:6.2f}  galat {avg_err[t]:6.2f}%")

    # angka yang dikutip di naskah
    assert abs(rho_idf1 - (-0.786)) < 0.005, rho_idf1
    assert abs(err[("diffmot", "DanceTrack")] - 13.78) < 0.01
    assert abs(err[("lighttrack", "DanceTrack")] - 59.94) < 0.01
    assert abs(avg_err["diffmot"] - 11.24) < 0.01 and abs(avg_idf1["diffmot"] - 48.62) < 0.01
    print("\nverifikasi OK: angka korelasi dan rata-rata cocok dengan yang dikutip di naskah")


if __name__ == "__main__":
    main()
