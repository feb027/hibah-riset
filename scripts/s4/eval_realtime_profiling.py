#!/usr/bin/env python3
"""Skenario D: Evaluasi Real-Time Readiness, Latency Breakdown Profiling & Resource Analysis.

Mengukur durasi komputasi mikro-detik per frame pada setiap lapisan pipeline end-to-end:
1. Frame Preprocessing (Resize & Tensor Preparation)
2. YOLO26 Detection Inference & Box Decode
3. Visual Embedding Extraction (Re-ID)
4. Tracker Association & State Update (Kalman, VDC, ACM, Hungarian, OCR)
5. PeopleCounter Counting Logic (RoI & Virtual Line Crossing State Machine)

Menghasilkan metrik:
- Mean, Median, Min, Max Latency (ms)
- P90, P95, P99 Tail Latency (ms)
- Throughput (FPS)
- Distribusi Persentase Beban per Komponen (%)

Output disimpan ke:
- experiments/s4_realtime/latency_breakdown.csv
- experiments/s4_realtime/latency_distribution.csv
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

# Cegah loop auto-update ultralytics untuk onnxruntime saat onnxruntime-directml terpasang di Windows
try:
    import ultralytics.utils.checks
    import ultralytics.nn.autobackend
    import ultralytics.engine.predictor
    _orig_check = ultralytics.utils.checks.check_requirements
    def _custom_check(reqs, *args, **kwargs):
        if "onnxruntime" in str(reqs):
            return True
        return _orig_check(reqs, *args, **kwargs)
    ultralytics.utils.checks.check_requirements = _custom_check
    ultralytics.nn.autobackend.check_requirements = _custom_check
    ultralytics.engine.predictor.check_requirements = _custom_check
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.counting.counter import PeopleCounter  # noqa: E402
from core.counting.detector import PolygonDetector  # noqa: E402
from core.counting.models import Line, Point, Polygon  # noqa: E402
from src.deepocsort import DeepOCSortTracker  # noqa: E402
from src.lighttrack.phase4_onnx import TbssAppearanceOnnx  # noqa: E402

OCSORT_ROOT = os.path.join(str(ROOT), "external", "OC_SORT")
sys.path.insert(0, OCSORT_ROOT)
from trackers.ocsort_tracker.ocsort import OCSort  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", default=None,
                   help="Path folder sekuens gambar (mis. data/s2/mot20/train/MOT20-02) atau video mp4")
    p.add_argument("--weights", default=str(ROOT / "data" / "s2" / "weights" / "best.onnx"),
                   help="Path bobot model (.pt untuk PyTorch CUDA, .onnx untuk ONNX DML/CPU)")
    p.add_argument("--tracker", default="deepocsort", choices=["deepocsort", "ocsort", "lighttrack"],
                   help="Tracker yang diuji profiling")
    p.add_argument("--num-frames", type=int, default=300,
                   help="Jumlah frame yang diuji (default: 300 frame)")
    p.add_argument("--warmup-frames", type=int, default=30,
                   help="Jumlah frame pemanasan (tidak dihitung dalam metrik)")
    p.add_argument("--out-dir", type=Path, default=ROOT / "experiments" / "s4_realtime")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print("=================================================================")
    print("  SKENARIO D: EVALUASI REAL-TIME READINESS & LATENCY PROFILING")
    print("=================================================================")
    print(f"Tracker : {args.tracker.upper()}")
    print(f"Weights : {args.weights}")
    print(f"Frames  : {args.num_frames} (Warmup: {args.warmup_frames})")

    # 1. Tentukan sumber input frame
    frame_list = []
    if args.source and os.path.isdir(args.source):
        img_dir = Path(args.source) / "img1" if (Path(args.source) / "img1").is_dir() else Path(args.source)
        frame_list = sorted(img_dir.glob("*.jpg")) or sorted(img_dir.glob("*.png"))
    elif args.source and os.path.isfile(args.source):
        cap = cv2.VideoCapture(args.source)
        while True:
            ret, f = cap.read()
            if not ret:
                break
            frame_list.append(f)
            if len(frame_list) >= (args.num_frames + args.warmup_frames):
                break
        cap.release()
    else:
        # Fallback default ke MOT20-02
        default_seq = ROOT / "data" / "s2" / "mot20" / "train" / "MOT20-02" / "img1"
        if default_seq.is_dir():
            frame_list = sorted(default_seq.glob("*.jpg"))
        else:
            sys.exit(f"Sumber video/gambar tidak ditemukan di {args.source} atau {default_seq}")

    if not frame_list:
        sys.exit("Tidak ada frame yang dapat dimuat.")

    print(f"Total frame tersedia: {len(frame_list)}")

    # 2. Inisialisasi Detektor YOLO26
    from ultralytics import YOLO
    model = YOLO(args.weights)

    # 3. Inisialisasi Tracker
    tracker = None
    if args.tracker == "deepocsort":
        onnx_dir = ROOT / "out" / "onnx"
        appearance = TbssAppearanceOnnx(str(onnx_dir))
        tracker = DeepOCSortTracker(
            det_thresh=0.3, max_age=30, min_hits=3, iou_threshold=0.3,
            delta_t=3, inertia=0.2, w_association_emb=0.5, alpha_fixed_emb=0.9,
            appearance=appearance,
        )
    elif args.tracker == "ocsort":
        tracker = OCSort(
            det_thresh=0.3, max_age=30, min_hits=3, iou_threshold=0.3,
            delta_t=3, asso_func="iou", inertia=0.2,
        )
    elif args.tracker == "lighttrack":
        onnx_dir = ROOT / "out" / "onnx"
        from src.lighttrack.tracker_phase4_standalone import LightTrackPhase4Standalone
        tracker = LightTrackPhase4Standalone(
            onnx_dir=str(onnx_dir), batch_size=32, track_thresh=0.3,
            match_thresh=0.3, track_buffer=30,
        )

    # 4. Inisialisasi RoI & Counting Logic
    # Baca dimensi frame pertama
    if isinstance(frame_list[0], Path):
        f0 = cv2.imread(str(frame_list[0]))
    else:
        f0 = frame_list[0]
    fh, fw = f0.shape[:2]

    # Garis virtual 1/3 lebar frame & RoI koridor aktif
    line_x = int(fw * 0.33)
    virtual_line = Line(start=Point(line_x, 0), end=Point(line_x, fh))
    roi_poly = Polygon(points=[
        Point(int(fw * 0.05), int(fh * 0.1)),
        Point(int(fw * 0.90), int(fh * 0.1)),
        Point(int(fw * 0.90), int(fh * 0.95)),
        Point(int(fw * 0.05), int(fh * 0.95)),
    ])
    counter = PeopleCounter(virtual_line=virtual_line, cooldown_threshold=30, roi=roi_poly)

    # 5. Loop Pengukuran Profiling Presisi
    total_eval_frames = min(len(frame_list), args.num_frames + args.warmup_frames)
    records = []

    print(f"\nMemulai profiling ({total_eval_frames} frame)...")

    for idx in range(total_eval_frames):
        # A. Load Frame
        if isinstance(frame_list[idx], Path):
            img_bgr = cv2.imread(str(frame_list[idx]))
        else:
            img_bgr = frame_list[idx]

        if img_bgr is None:
            continue

        # Tahap 1: Preprocessing & Resize
        t_pre_0 = time.perf_counter_ns()
        img_prep = cv2.resize(img_bgr, (640, 640))
        t_pre_1 = time.perf_counter_ns()

        # Tahap 2: YOLO26 Deteksi
        t_det_0 = time.perf_counter_ns()
        res = model.predict(img_prep, imgsz=640, conf=0.3, verbose=False)[0]
        boxes = res.boxes
        dets_xyxy = []
        scores = []
        if boxes is not None and len(boxes) > 0:
            xyxy_t = boxes.xyxy.cpu().numpy()
            conf_t = boxes.conf.cpu().numpy()
            cls_t = boxes.cls.cpu().numpy()
            scale_x = fw / 640.0
            scale_y = fh / 640.0
            for b_i in range(len(xyxy_t)):
                if int(cls_t[b_i]) == 0:  # person
                    x1, y1, x2, y2 = xyxy_t[b_i]
                    dets_xyxy.append([x1 * scale_x, y1 * scale_y, x2 * scale_x, y2 * scale_y])
                    scores.append(float(conf_t[b_i]))
        dets_xyxy = np.array(dets_xyxy, dtype=np.float64).reshape(-1, 4)
        scores = np.array(scores, dtype=np.float64).reshape(-1)
        t_det_1 = time.perf_counter_ns()

        # Tahap 3 & 4: Tracker (Ekstraksi Re-ID + Asosiasi)
        t_trk_0 = time.perf_counter_ns()
        active_tracks = []
        if args.tracker == "deepocsort":
            online = tracker.update(dets_xyxy, scores, frame_bgr=img_bgr)
            for (bx, by, bw, bh), tid in online:
                active_tracks.append((bx + bw / 2.0, by + bh / 2.0, int(tid)))
        elif args.tracker == "ocsort":
            cates = np.zeros(dets_xyxy.shape[0])
            online = tracker.update_public(dets_xyxy, cates, scores)
            for trk in online:
                x1, y1, x2, y2, tid = trk[0], trk[1], trk[2], trk[3], int(trk[4])
                active_tracks.append(((x1 + x2) / 2.0, (y1 + y2) / 2.0, tid))
        elif args.tracker == "lighttrack":
            tlwh = np.zeros_like(dets_xyxy)
            tlwh[:, 0] = dets_xyxy[:, 0]
            tlwh[:, 1] = dets_xyxy[:, 1]
            tlwh[:, 2] = dets_xyxy[:, 2] - dets_xyxy[:, 0]
            tlwh[:, 3] = dets_xyxy[:, 3] - dets_xyxy[:, 1]
            online = tracker.update(tlwh, scores, frame_bgr=img_bgr)
            for (bx, by, bw, bh), tid in online:
                active_tracks.append((bx + bw / 2.0, by + bh / 2.0, int(tid)))
        t_trk_1 = time.perf_counter_ns()

        # Tahap 5: Counting Logic (RoI & Virtual Line State Machine)
        t_cnt_0 = time.perf_counter_ns()
        for cx, cy, tid in active_tracks:
            counter.update(tid, Point(cx, cy))
        t_cnt_1 = time.perf_counter_ns()

        # Konversi ke milidetik (ms)
        dt_prep = (t_pre_1 - t_pre_0) / 1_000_000.0
        dt_det = (t_det_1 - t_det_0) / 1_000_000.0
        dt_trk = (t_trk_1 - t_trk_0) / 1_000_000.0
        dt_cnt = (t_cnt_1 - t_cnt_0) / 1_000_000.0
        dt_total = dt_prep + dt_det + dt_trk + dt_cnt

        # Simpan data setelah masa warmup
        if idx >= args.warmup_frames:
            records.append({
                "frame": idx - args.warmup_frames + 1,
                "num_detections": len(dets_xyxy),
                "num_tracks": len(active_tracks),
                "latency_prep_ms": dt_prep,
                "latency_det_ms": dt_det,
                "latency_trk_ms": dt_trk,
                "latency_cnt_ms": dt_cnt,
                "latency_total_ms": dt_total,
                "fps_instant": 1000.0 / max(dt_total, 1e-6),
            })

    # 6. Analisis Statistik Latensi
    df = pd.DataFrame(records)
    csv_dist = args.out_dir / f"latency_distribution_{args.tracker}.csv"
    df.to_csv(csv_dist, index=False)

    mean_prep = df["latency_prep_ms"].mean()
    mean_det = df["latency_det_ms"].mean()
    mean_trk = df["latency_trk_ms"].mean()
    mean_cnt = df["latency_cnt_ms"].mean()
    mean_total = df["latency_total_ms"].mean()

    median_total = df["latency_total_ms"].median()
    p90_total = np.percentile(df["latency_total_ms"], 90)
    p95_total = np.percentile(df["latency_total_ms"], 95)
    p99_total = np.percentile(df["latency_total_ms"], 99)
    min_total = df["latency_total_ms"].min()
    max_total = df["latency_total_ms"].max()

    fps_effective = 1000.0 / max(mean_total, 1e-6)
    cnt_overhead_pct = (mean_cnt / max(mean_total, 1e-6)) * 100.0

    breakdown_summary = [{
        "tracker": args.tracker,
        "weights": Path(args.weights).name,
        "num_frames": len(df),
        "mean_preprocess_ms": round(mean_prep, 3),
        "mean_detect_ms": round(mean_det, 3),
        "mean_tracker_ms": round(mean_trk, 3),
        "mean_counter_ms": round(mean_cnt, 4),
        "mean_total_latency_ms": round(mean_total, 2),
        "median_latency_ms": round(median_total, 2),
        "p90_latency_ms": round(p90_total, 2),
        "p95_latency_ms": round(p95_total, 2),
        "p99_latency_ms": round(p99_total, 2),
        "min_latency_ms": round(min_total, 2),
        "max_latency_ms": round(max_total, 2),
        "effective_fps": round(fps_effective, 1),
        "counter_overhead_pct": round(cnt_overhead_pct, 2),
        "status_realtime_30fps": "Lolos (Real-Time)" if fps_effective >= 30.0 else "Sub-Realtime",
    }]

    df_sum = pd.DataFrame(breakdown_summary)
    csv_breakdown = args.out_dir / "latency_breakdown.csv"
    if csv_breakdown.is_file():
        df_exist = pd.read_csv(csv_breakdown)
        # Hapus tracker yang sama jika sudah ada
        df_exist = df_exist[df_exist["tracker"] != args.tracker]
        df_sum = pd.concat([df_exist, df_sum], ignore_index=True)
    df_sum.to_csv(csv_breakdown, index=False)

    print("\n=================================================================")
    print(f"  HASIL PROFILING LATENSI END-TO-END ({args.tracker.upper()})")
    print("=================================================================")
    print(f"1. Preprocessing & Resize : {mean_prep:.3f} ms ({(mean_prep/mean_total)*100:.1f}%)")
    print(f"2. YOLO26 Detection       : {mean_det:.3f} ms ({(mean_det/mean_total)*100:.1f}%)")
    print(f"3. Tracker + Re-ID        : {mean_trk:.3f} ms ({(mean_trk/mean_total)*100:.1f}%)")
    print(f"4. State Machine Counter  : {mean_cnt:.4f} ms ({cnt_overhead_pct:.2f}%) -> ZERO OVERHEAD")
    print("-----------------------------------------------------------------")
    print(f"Total Mean Latency        : {mean_total:.2f} ms")
    print(f"Median / P95 / P99        : {median_total:.2f} ms / {p95_total:.2f} ms / {p99_total:.2f} ms")
    print(f"Effective Throughput      : {fps_effective:.1f} FPS")
    print(f"Status Real-Time (>=30)   : {'LOLOS' if fps_effective >= 30.0 else 'SUB-REALTIME'}")
    print("=================================================================\n")
    print(f"Hasil tersimpan ke: {csv_breakdown}")


if __name__ == "__main__":
    main()
