"""LightTrack-ReID-inspired (Phase 1) — runner MOT: deteksi format MOT -> hasil tracker.

Input : {det_dir}/{seq}.txt — format deteksi MOT: frame,id,x,y,w,h,conf,cls,-1,-1 (id boleh -1)
Output: {out_dir}/{seq}.txt — format hasil TrackEval: frame,id,x,y,w,h,conf,-1,-1,-1

Contoh:
    python scripts/s2/run_lighttrack_mot.py \
        --det-dir data/s2/mot20/det_mot/train \
        --out-dir experiments/s2_tracker/lighttrack_results/mot20
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."))
from src.lighttrack.tracker import LightTrackTracker  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--det-dir", required=True, help="folder berisi {seq}.txt deteksi MOT")
    p.add_argument("--out-dir", required=True, help="folder hasil tracker")
    p.add_argument("--min-conf", type=float, default=0.3, help="buang deteksi dengan score < ini")
    p.add_argument("--iou-thresh", type=float, default=0.3)
    p.add_argument("--min-hits", type=int, default=3)
    p.add_argument("--max-age", type=int, default=30)
    p.add_argument("--ema-alpha", type=float, default=0.9)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    seq_files = sorted(f for f in os.listdir(args.det_dir) if f.endswith(".txt"))

    total_time, total_frame = 0.0, 0
    for seq_name in seq_files:
        print(f"[{seq_name}]")
        seq_trks = np.loadtxt(os.path.join(args.det_dir, seq_name), dtype=np.float64,
                              delimiter=",").reshape(-1, 10)
        if seq_trks.shape[0] == 0:
            print("  (kosong, dilewati)"); continue
        tracker = LightTrackTracker(min_conf=args.min_conf, iou_thresh=args.iou_thresh,
                                    min_hits=args.min_hits, max_age=args.max_age,
                                    ema_alpha=args.ema_alpha)
        min_frame, max_frame = int(seq_trks[:, 0].min()), int(seq_trks[:, 0].max())
        with open(os.path.join(args.out_dir, f"{seq_name}"), "w") as out_file:
            for frame_ind in range(min_frame, max_frame + 1):
                rows = seq_trks[seq_trks[:, 0] == frame_ind]
                if args.min_conf > 0 and rows.shape[0]:
                    rows = rows[rows[:, 6] >= args.min_conf]
                dets = rows[:, 2:6].copy()          # tlwh
                scores = rows[:, 6]
                t0 = time.time()
                online = tracker.update(dets, scores)
                t1 = time.time()
                total_time += t1 - t0
                total_frame += 1
                for box, tid in online:
                    x, y, w, h = box
                    out_file.write(
                        f"{int(frame_ind)},{int(tid)},{x:.2f},{y:.2f},{w:.2f},{h:.2f},1,-1,-1,-1\n"
                    )
    print(f"\nSelesai. {total_frame} frame, {total_time:.1f}s, "
          f"FPS={total_frame / max(total_time, 1e-9):.1f}")


if __name__ == "__main__":
    main()
