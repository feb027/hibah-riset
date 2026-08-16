#!/usr/bin/env python3
"""Orchestrator Evaluasi Skenario C: Counting Logic, State Machine, dan Dekomposisi Galat.

Mengevaluasi akurasi perhitungan perlintasan garis virtual (People Counting) pada trajectory
Ground Truth (GT) dan hasil pelacakan (OC-SORT, Deep-OC-SORT, DiffMOT, LightTrack).

Metrik yang dihitung:
- Ground Truth Event Count (IN, OUT, TOTAL)
- Predicted Count (IN, OUT, TOTAL)
- MAE (Mean Absolute Error) & RMSE
- Error Percentage (|Pred - GT| / GT * 100)
- Studi Ablasi: Naive Line Crossing vs State Machine Debouncing (Cooldown=15, 30, 60)

Output disimpan ke:
- experiments/s3_counting/counting_metrics.csv
- experiments/s3_counting/counting_ablation.csv
- experiments/s3_counting/counting_series.csv
"""
from __future__ import annotations

import argparse
import configparser
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from core.counting.counter import PeopleCounter  # noqa: E402
from core.counting.detector import LineCrossDetector, PolygonDetector  # noqa: E402
from core.counting.models import Line, Point, Polygon  # noqa: E402


class NaiveCounter:
    """Model A: Naive Line Crossing tanpa State Machine dan tanpa Cooldown (Baseline rentan Over-Count)."""

    def __init__(self, virtual_line: Line, roi: Polygon = None) -> None:
        self.virtual_line = virtual_line
        self.roi = roi
        self.count_in = 0
        self.count_out = 0
        self._last_points: dict[int, Point] = {}

    def update(self, track_id: int, current_centroid: Point) -> None:
        if self.roi is not None and not PolygonDetector.is_inside(self.roi, current_centroid):
            return

        if track_id in self._last_points:
            prev = self._last_points[track_id]
            trajectory = Line(start=prev, end=current_centroid)
            intersects, direction = LineCrossDetector.check_crossing(self.virtual_line, trajectory)
            if intersects:
                if direction == "IN":
                    self.count_in += 1
                elif direction == "OUT":
                    self.count_out += 1

        self._last_points[track_id] = current_centroid


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir", type=Path, default=Path(ROOT) / "data" / "s2")
    p.add_argument("--exp-dir", type=Path, default=Path(ROOT) / "experiments" / "s2_tracker")
    p.add_argument("--out-dir", type=Path, default=Path(ROOT) / "experiments" / "s3_counting")
    p.add_argument("--dataset", default="mot20", choices=["mot20", "dancetrack", "all"])
    p.add_argument("--line-pos", type=float, default=0.33,
                   help="Posisi garis virtual sebagai fraksi lebar frame (default: 0.33 / 1/3 frame)")
    p.add_argument("--interval-len", type=int, default=300,
                   help="Panjang interval frame untuk perhitungan dinamika RMSE (default: 300 frame)")
    return p.parse_args()


def load_gt_tracks(gt_file: Path) -> dict[int, list[tuple[int, float, float]]]:
    """Memuat ground truth track format MOT. Filter hanya pedestrian (class == 1)."""
    data = np.loadtxt(gt_file, delimiter=",", dtype=float)
    if data.ndim == 1:
        data = data.reshape(1, -1)

    # Kolom MOT20 GT: frame, id, bb_left, bb_top, bb_width, bb_height, mark, class, vis
    if data.shape[1] >= 8:
        # Filter class 1 (pedestrian)
        data = data[data[:, 7] == 1]

    frame_dict: dict[int, list[tuple[int, float, float]]] = {}
    for row in data:
        frame_idx = int(row[0])
        tid = int(row[1])
        x, y, w, h = row[2:6]
        # Gunakan bottom-center atau center sebagai titik perlintasan pejalan kaki
        cx = x + w / 2.0
        cy = y + h / 2.0
        if frame_idx not in frame_dict:
            frame_dict[frame_idx] = []
        frame_dict[frame_idx].append((tid, cx, cy))

    return frame_dict


def load_pred_tracks(pred_file: Path) -> dict[int, list[tuple[int, float, float]]]:
    """Memuat hasil prediksi tracker format MOT: frame, id, x, y, w, h, conf, -1, -1, -1."""
    if not pred_file.is_file():
        return {}

    data = np.loadtxt(pred_file, delimiter=",", dtype=float)
    if data.size == 0:
        return {}
    if data.ndim == 1:
        data = data.reshape(1, -1)

    frame_dict: dict[int, list[tuple[int, float, float]]] = {}
    for row in data:
        frame_idx = int(row[0])
        tid = int(row[1])
        x, y, w, h = row[2:6]
        cx = x + w / 2.0
        cy = y + h / 2.0
        if frame_idx not in frame_dict:
            frame_dict[frame_idx] = []
        frame_dict[frame_idx].append((tid, cx, cy))

    return frame_dict


def get_seq_dimensions(seq_dir: Path) -> tuple[int, int, int]:
    """Membaca lebar, tinggi, dan total frame dari seqinfo.ini."""
    ini_path = seq_dir / "seqinfo.ini"
    if ini_path.is_file():
        cp = configparser.ConfigParser()
        cp.read(ini_path)
        if "Sequence" in cp:
            w = int(cp["Sequence"].get("imWidth", 1920))
            h = int(cp["Sequence"].get("imHeight", 1080))
            n = int(cp["Sequence"].get("seqLength", 1000))
            return w, h, n
    return 1920, 1080, 1000


def evaluate_sequence(
    seq_name: str,
    seq_dir: Path,
    tracker_files: dict[str, Path],
    line_frac: float = 0.33,
    interval_len: int = 300,
) -> tuple[list[dict], list[dict], list[dict]]:
    """Evaluasi counting untuk satu sekuens."""
    w, h, max_frame = get_seq_dimensions(seq_dir)
    line_x = int(w * line_frac)
    virtual_line = Line(start=Point(line_x, 0), end=Point(line_x, h))

    gt_file = seq_dir / "gt" / "gt.txt"
    if not gt_file.is_file():
        print(f"  [SKIP] GT tidak ditemukan untuk {seq_name}")
        return [], [], []

    gt_frames = load_gt_tracks(gt_file)
    actual_max_frame = max(max(gt_frames.keys(), default=1), max_frame)

    # 1. Jalankan Ground Truth Counting sebagai true reference
    gt_counter = PeopleCounter(virtual_line=virtual_line, cooldown_threshold=30)
    gt_series = []
    for f in range(1, actual_max_frame + 1):
        if f in gt_frames:
            for tid, cx, cy in gt_frames[f]:
                gt_counter.update(tid, Point(cx, cy))
        gt_series.append((f, gt_counter.count_in, gt_counter.count_out, gt_counter.count_in + gt_counter.count_out))

    gt_in = gt_counter.count_in
    gt_out = gt_counter.count_out
    gt_tot = gt_in + gt_out

    metrics_rows = []
    ablation_rows = []
    series_rows = []

    # Catat GT series
    for f, cin, cout, ctot in gt_series:
        series_rows.append({
            "seq": seq_name, "tracker": "GroundTruth", "model": "GT",
            "frame": f, "count_in": cin, "count_out": cout, "count_total": ctot
        })

    # Catat baris GT di metrics
    metrics_rows.append({
        "seq": seq_name, "tracker": "GroundTruth", "model": "Ideal (GT-Track)",
        "GT_IN": gt_in, "GT_OUT": gt_out, "GT_TOTAL": gt_tot,
        "Pred_IN": gt_in, "Pred_OUT": gt_out, "Pred_TOTAL": gt_tot,
        "MAE": 0.0, "MAE_IN": 0.0, "MAE_OUT": 0.0,
        "Error_Pct": 0.0, "RMSE_Interval": 0.0,
        "Over_Count": 0, "Under_Count": 0
    })

    # Model konfigurasi yang diuji
    counter_configs = [
        ("Model_A_Naive", lambda: NaiveCounter(virtual_line)),
        ("Model_B_CD15", lambda: PeopleCounter(virtual_line, cooldown_threshold=15)),
        ("Model_B_CD30_Default", lambda: PeopleCounter(virtual_line, cooldown_threshold=30)),
        ("Model_B_CD60", lambda: PeopleCounter(virtual_line, cooldown_threshold=60)),
    ]

    for trk_name, trk_path in tracker_files.items():
        if not trk_path.is_file():
            continue

        pred_frames = load_pred_tracks(trk_path)
        if not pred_frames:
            continue

        for model_name, counter_fn in counter_configs:
            counter = counter_fn()
            cur_series = []

            # Replay per frame
            for f in range(1, actual_max_frame + 1):
                if f in pred_frames:
                    for tid, cx, cy in pred_frames[f]:
                        counter.update(tid, Point(cx, cy))
                cur_series.append((f, counter.count_in, counter.count_out, counter.count_in + counter.count_out))

            pred_in = counter.count_in
            pred_out = counter.count_out
            pred_tot = pred_in + pred_out

            mae_tot = abs(pred_tot - gt_tot)
            mae_in = abs(pred_in - gt_in)
            mae_out = abs(pred_out - gt_out)
            err_pct = (mae_tot / max(1, gt_tot)) * 100.0
            over_count = max(0, pred_tot - gt_tot)
            under_count = max(0, gt_tot - pred_tot)

            # Hitung RMSE antar sub-interval (misal per 300 frame)
            n_intervals = max(1, actual_max_frame // interval_len)
            interval_diffs = []
            for i in range(n_intervals):
                f_end = min((i + 1) * interval_len, actual_max_frame) - 1
                diff_i = cur_series[f_end][3] - gt_series[f_end][3]
                interval_diffs.append(diff_i ** 2)
            rmse = float(np.sqrt(np.mean(interval_diffs))) if interval_diffs else float(mae_tot)

            # Simpan ringkasan untuk default model (State Machine CD=30) di metrics_rows
            if model_name == "Model_B_CD30_Default":
                metrics_rows.append({
                    "seq": seq_name, "tracker": trk_name, "model": "State Machine (CD=30)",
                    "GT_IN": gt_in, "GT_OUT": gt_out, "GT_TOTAL": gt_tot,
                    "Pred_IN": pred_in, "Pred_OUT": pred_out, "Pred_TOTAL": pred_tot,
                    "MAE": mae_tot, "MAE_IN": mae_in, "MAE_OUT": mae_out,
                    "Error_Pct": round(err_pct, 2),
                    "RMSE_Interval": round(rmse, 2),
                    "Over_Count": over_count, "Under_Count": under_count
                })

            # Simpan seluruh variasi di ablation_rows
            ablation_rows.append({
                "seq": seq_name, "tracker": trk_name, "model": model_name,
                "GT_TOTAL": gt_tot, "Pred_TOTAL": pred_tot,
                "MAE": mae_tot, "Error_Pct": round(err_pct, 2),
                "RMSE": round(rmse, 2), "Over_Count": over_count, "Under_Count": under_count
            })

            # Simpan kurva series
            for f, cin, cout, ctot in cur_series:
                series_rows.append({
                    "seq": seq_name, "tracker": trk_name, "model": model_name,
                    "frame": f, "count_in": cin, "count_out": cout, "count_total": ctot
                })

    return metrics_rows, ablation_rows, series_rows


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print("=================================================================")
    print("  SKENARIO C: EVALUASI COUNTING LOGIC & DEKOMPOSISI GALAT HITUNG")
    print("=================================================================")
    print(f"Data Dir: {args.data_dir}")
    print(f"Exp Dir : {args.exp_dir}")
    print(f"Out Dir : {args.out_dir}")
    print(f"Virtual Line Fraction: {args.line_pos} (Vertikal)")

    all_metrics = []
    all_ablation = []
    all_series = []

    # Daftar dataset yang diuji
    datasets_to_run = []
    if args.dataset in ("mot20", "all"):
        datasets_to_run.append(("mot20", args.data_dir / "mot20" / "train"))
    if args.dataset in ("dancetrack", "all"):
        datasets_to_run.append(("dancetrack", args.data_dir / "dancetrack" / "val"))

    trackers = ["ocsort", "deepocsort", "diffmot", "lighttrack"]

    for ds_name, ds_path in datasets_to_run:
        if not ds_path.is_dir():
            print(f"\n[SKIP] Dataset folder {ds_path} tidak ditemukan.")
            continue

        print(f"\n--- Memproses Dataset: {ds_name.upper()} ---")
        seq_dirs = sorted([p for p in ds_path.iterdir() if p.is_dir() and not p.name.endswith(".bad-old")])

        for sdir in seq_dirs:
            seq_name = sdir.name
            print(f"[{ds_name}/{seq_name}] Mengevaluasi perlintasan garis...")

            trk_files = {}
            for t in trackers:
                # Cek file track di experiments/s2_tracker/{t}_results/{ds_name}/{seq_name}.txt
                tf = args.exp_dir / f"{t}_results" / ds_name / f"{seq_name}.txt"
                if tf.is_file():
                    trk_files[t] = tf

            m_rows, a_rows, s_rows = evaluate_sequence(
                seq_name=seq_name,
                seq_dir=sdir,
                tracker_files=trk_files,
                line_frac=args.line_pos,
                interval_len=args.interval_len,
            )

            all_metrics.extend(m_rows)
            all_ablation.extend(a_rows)
            all_series.extend(s_rows)

    if all_metrics:
        df_metrics = pd.DataFrame(all_metrics)
        csv_metrics = args.out_dir / "counting_metrics.csv"
        df_metrics.to_csv(csv_metrics, index=False)
        print(f"\n[SUKSES] Metrics counting tersimpan ke: {csv_metrics}")

    if all_ablation:
        df_ablation = pd.DataFrame(all_ablation)
        csv_ablation = args.out_dir / "counting_ablation.csv"
        df_ablation.to_csv(csv_ablation, index=False)
        print(f"[SUKSES] Ablation counting tersimpan ke: {csv_ablation}")

    if all_series:
        df_series = pd.DataFrame(all_series)
        csv_series = args.out_dir / "counting_series.csv"
        df_series.to_csv(csv_series, index=False)
        print(f"[SUKSES] Series frame counting tersimpan ke: {csv_series}")

    # Cetak ringkasan tabel komparasi utama
    if all_metrics:
        print("\n=================================================================")
        print("  RINGKASAN AKURASI COUNTING (STATE MACHINE CD=30) PER TRACKER")
        print("=================================================================")
        df_m = pd.DataFrame(all_metrics)
        # Filter ringkasan agregat
        summary = df_m.groupby("tracker")[["GT_TOTAL", "Pred_TOTAL", "MAE", "Error_Pct", "RMSE_Interval"]].mean()
        print(summary.round(2).to_string())
        print("=================================================================\n")


if __name__ == "__main__":
    main()
