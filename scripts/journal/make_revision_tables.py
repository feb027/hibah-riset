#!/usr/bin/env python3
"""Regenerasi tabel revisi naskah JESTEC dari CSV eksperimen.

Menghasilkan tabel markdown untuk Bab 4 (akurasi hitung, ablasi, sensitivitas,
dekomposisi galat) langsung dari hasil eksperimen, agar angka di naskah tidak
salah salin. Jalankan: python3 scripts/journal/make_revision_tables.py

Sumber (jangan diubah, read-only):
  experiments/s3_counting/counting_metrics.csv     per-sekuens, State Machine (CD=30) + GroundTruth
  experiments/s3_counting/counting_ablation.csv    per-sekuens, Model A naive vs CD 15/30/60
  experiments/s3_counting/sensitivity_cooldown.csv kurva cooldown agregat
  experiments/s3_counting/sensitivity_confidence.csv kurva confidence agregat
  experiments/s4_realtime/ (latensi) -> lihat docs/reports/laporan-skenario-d-realtime.md
"""
from __future__ import annotations

import csv
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S3 = ROOT / "experiments" / "s3_counting"

TRACKER_LABEL = {
    "ocsort": "OC-SORT",
    "deepocsort": "Deep-OC-SORT",
    "diffmot": "DiffMOT",
    "lighttrack": "LightTrack",
    "ground_truth": "Ground truth",
    "GroundTruth": "Ground truth",
}
TRACKER_ORDER = ["diffmot", "deepocsort", "ocsort", "lighttrack"]


def rows(name: str) -> list[dict[str, str]]:
    with open(S3 / name, newline="") as fh:
        return list(csv.DictReader(fh))


def f(x: str) -> float:
    return float(x)


def tabel_akurasi_hitung() -> str:
    """Tabel 6 revisi: galat per jalur + sebaran antar-sekuens + pemisahan over/under."""
    data = [r for r in rows("counting_metrics.csv") if r["model"] == "State Machine (CD=30)"]
    g: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in data:
        g[r["tracker"]].append(r)

    out = [
        "| Jalur pelacakan | Rata-rata GT | Rata-rata prediksi | Galat per sekuens (%) | Simpangan baku | Galat gabungan (%) | MAE | Over-count | Under-count |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    # baris referensi: lintasan ground truth, dirata-rata lintas 29 sekuens
    gt = [r for r in rows("counting_metrics.csv") if "GT-Track" in r["model"]]
    out.append(
        f"| Ground truth (lintasan ideal) | {st.mean([f(r['GT_TOTAL']) for r in gt]):.2f} | "
        f"{st.mean([f(r['Pred_TOTAL']) for r in gt]):.2f} | "
        f"{st.mean([f(r['Error_Pct']) for r in gt]):.2f} | 0,00 | 0,00 | "
        f"{st.mean([f(r['MAE']) for r in gt]):.2f} | 0 | 0 |"
    )
    for t in TRACKER_ORDER:
        rs = g[t]
        sgt = sum(int(r["GT_TOTAL"]) for r in rs)
        spr = sum(int(r["Pred_TOTAL"]) for r in rs)
        errs = [f(r["Error_Pct"]) for r in rs]
        out.append(
            f"| {TRACKER_LABEL[t]} | {st.mean([f(r['GT_TOTAL']) for r in rs]):.2f} | "
            f"{st.mean([f(r['Pred_TOTAL']) for r in rs]):.2f} | {st.mean(errs):.2f} | "
            f"{st.stdev(errs):.2f} | {100 * (spr - sgt) / sgt:+.2f} | "
            f"{st.mean([f(r['MAE']) for r in rs]):.2f} | "
            f"{sum(int(r['Over_Count']) for r in rs)} | {sum(int(r['Under_Count']) for r in rs)} |"
        )
    return "\n".join(out)


def tabel_ablasi() -> str:
    """Ablasi cooldown pada 29 sekuens, semua tracker (Model A naive vs CD 15/30/60)."""
    data = rows("counting_ablation.csv")
    g: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for r in data:
        g[(r["tracker"], r["model"])].append(r)
    out = [
        "| Jalur pelacakan | Konfigurasi | Galat per sekuens (%) | Simpangan baku | MAE | Over-count | Under-count |",
        "|---|---|---|---|---|---|---|",
    ]
    order = ["Model_A_Naive", "Model_B_CD15", "Model_B_CD30_Default", "Model_B_CD60"]
    label = {
        "Model_A_Naive": "Naive (tanpa debounce)",
        "Model_B_CD15": "State machine (CD=15)",
        "Model_B_CD30_Default": "State machine (CD=30)",
        "Model_B_CD60": "State machine (CD=60)",
    }
    for t in TRACKER_ORDER:
        for m in order:
            rs = g[(t, m)]
            if not rs:
                continue
            errs = [f(r["Error_Pct"]) for r in rs]
            out.append(
                f"| {TRACKER_LABEL[t]} | {label[m]} | {st.mean(errs):.2f} | {st.stdev(errs):.2f} | "
                f"{st.mean([f(r['MAE']) for r in rs]):.2f} | {sum(int(r['Over_Count']) for r in rs)} | "
                f"{sum(int(r['Under_Count']) for r in rs)} |"
            )
    return "\n".join(out)


def tabel_cooldown() -> str:
    """Kurva cooldown: Deep-OC-SORT dan lintasan ground truth."""
    out = [
        "| Cooldown (frame) | Prediksi (Deep-OC-SORT) | MAE | Galat (%) | Bias | Prediksi (lintasan GT) | Galat GT (%) |",
        "|---|---|---|---|---|---|---|",
    ]
    buckets: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for r in rows("sensitivity_cooldown.csv"):
        buckets[r["tracker"]][r["cooldown_frames"]] = r
    for cd in sorted(buckets["deepocsort"], key=int):
        a = buckets["deepocsort"][cd]
        b = buckets["ground_truth"].get(cd)
        if b is None:
            continue
        out.append(
            f"| {cd} | {f(a['avg_pred']):.2f} | {f(a['mae']):.2f} | {f(a['error_pct']):.2f} | "
            f"{f(a['bias']):+.2f} | {f(b['avg_pred']):.2f} | {f(b['error_pct']):.2f} |"
        )
    return "\n".join(out)


def tabel_confidence() -> str:
    out = [
        "| Confidence threshold | Prediksi | MAE | Galat (%) | Throughput (FPS) |",
        "|---|---|---|---|---|",
    ]
    for r in rows("sensitivity_confidence.csv"):
        out.append(
            f"| {r['conf_threshold']} | {f(r['estimated_pred']):.2f} | {f(r['mae']):.2f} | "
            f"{f(r['error_pct']):.2f} | {f(r['fps_throughput']):.1f} |"
        )
    return "\n".join(out)


def tabel_per_benchmark() -> str:
    """Pemisahan galat MOT20 vs DanceTrack pada konfigurasi operasional."""
    data = [r for r in rows("counting_metrics.csv") if r["model"] == "State Machine (CD=30)"]
    g: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for r in data:
        bench = "MOT20" if r["seq"].startswith("MOT20") else "DanceTrack"
        g[(r["tracker"], bench)].append(r)
    out = [
        "| Jalur pelacakan | Benchmark | Sekuens | Galat per sekuens (%) | Simpangan baku | MAE | Over-count | Under-count |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for t in TRACKER_ORDER:
        for bench in ("MOT20", "DanceTrack"):
            rs = g[(t, bench)]
            errs = [f(r["Error_Pct"]) for r in rs]
            out.append(
                f"| {TRACKER_LABEL[t]} | {bench} | {len(rs)} | {st.mean(errs):.2f} | {st.stdev(errs):.2f} | "
                f"{st.mean([f(r['MAE']) for r in rs]):.2f} | {sum(int(r['Over_Count']) for r in rs)} | "
                f"{sum(int(r['Under_Count']) for r in rs)} |"
            )
    return "\n".join(out)


def verifikasi() -> None:
    """Cek silang: angka headline naskah harus muncul di data."""
    rs = [r for r in rows("counting_metrics.csv") if r["model"] == "State Machine (CD=30)"]
    per: dict[str, list[float]] = defaultdict(list)
    for r in rs:
        per[r["tracker"]].append(f(r["Error_Pct"]))
    headline = {"diffmot": 13.08, "deepocsort": 16.71, "ocsort": 22.38, "lighttrack": 53.03}
    for t, v in headline.items():
        assert abs(st.mean(per[t]) - v) < 0.01, f"{t}: {st.mean(per[t]):.4f} != {v}"
    cd = {r["cooldown_frames"]: r for r in rows("sensitivity_cooldown.csv") if r["tracker"] == "deepocsort"}
    assert abs(f(cd["0"]["error_pct"]) - 101.99) < 0.01
    assert abs(f(cd["30"]["mae"]) - 6.34) < 0.01
    assert abs(f(cd["45"]["error_pct"]) - 14.64) < 0.01
    gtx = {r["cooldown_frames"]: r for r in rows("sensitivity_cooldown.csv") if r["tracker"] == "ground_truth"}
    assert f(gtx["0"]["error_pct"]) == 60.6 and f(gtx["30"]["error_pct"]) == 0.0
    print("verifikasi OK: angka headline naskah cocok dengan CSV eksperimen\n")


if __name__ == "__main__":
    verifikasi()
    for title, fn in [
        ("TABEL 6 (revisi) - akurasi hitung per jalur, sebaran, over/under", tabel_akurasi_hitung),
        ("TABEL ABLASI - naive vs state machine, 4 tracker, 29 sekuens", tabel_ablasi),
        ("TABEL COOLDOWN - kurva U pada Deep-OC-SORT dan lintasan GT", tabel_cooldown),
        ("TABEL CONFIDENCE THRESHOLD", tabel_confidence),
        ("TABEL PER-BENCHMARK - MOT20 vs DanceTrack", tabel_per_benchmark),
    ]:
        print(f"===== {title} =====\n{fn()}\n")
