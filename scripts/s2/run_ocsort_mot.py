#!/usr/bin/env python3
"""Run OC-SORT atas deteksi format MOT (det.txt) — Skenario B.

Pola mengikuti tools/run_ocsort_public.py branch headtrack dari repo noahcao/OC_SORT
(branch MOT tidak ada di repo; branch ini yang paling dekat dan sudah terbukti).

Input : {det_dir}/{seq}.txt  — format deteksi MOT: frame,id,x,y,w,h,conf,cls,-1,-1 (id boleh -1)
Output: {out_dir}/{seq}.txt  — format hasil TrackEval: frame,id,x,y,w,h,conf,-1,-1,-1

Contoh:
    python scripts/s2/run_ocsort_mot.py \
        --ocsort-root external/OC_SORT \
        --det-dir data/s2/mot20/det_mot/train \
        --out-dir experiments/s2_tracker/ocsort_results/mot20
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ocsort-root", required=True, help="root repo noahcao/OC_SORT")
    p.add_argument("--det-dir", required=True, help="folder berisi {seq}.txt deteksi MOT")
    p.add_argument("--out-dir", required=True, help="folder hasil tracker")
    p.add_argument("--track-thresh", type=float, default=0.3)
    p.add_argument("--iou-thresh", type=float, default=0.3)
    p.add_argument("--delta-t", type=int, default=3)
    p.add_argument("--min-hits", type=int, default=3)
    p.add_argument("--max-age", type=int, default=30)
    p.add_argument("--asso", default="iou", choices=["iou", "giou", "ciou", "diou"])
    p.add_argument("--inertia", type=float, default=0.2)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    sys.path.insert(0, args.ocsort_root)
    from trackers.ocsort_tracker.ocsort import OCSort  # noqa: E402

    os.makedirs(args.out_dir, exist_ok=True)
    seq_files = sorted(f for f in os.listdir(args.det_dir) if f.endswith(".txt"))

    total_time, total_frame = 0.0, 0
    for seq_name in seq_files:
        print(f"[{seq_name}]")
        seq_trks = np.loadtxt(os.path.join(args.det_dir, seq_name), dtype=np.float64, delimiter=",").reshape(-1, 10)
        if seq_trks.shape[0] == 0:
            print("  (kosong, dilewati)"); continue
        tracker = OCSort(
            args.track_thresh,
            max_age=args.max_age,
            min_hits=args.min_hits,
            iou_threshold=args.iou_thresh,
            delta_t=args.delta_t,
            asso_func=args.asso,
            inertia=args.inertia,
        )
        min_frame, max_frame = int(seq_trks[:, 0].min()), int(seq_trks[:, 0].max())
        with open(os.path.join(args.out_dir, f"{seq_name}"), "w") as out_file:
            for frame_ind in range(min_frame, max_frame + 1):
                rows = seq_trks[seq_trks[:, 0] == frame_ind]
                dets = rows[:, 2:6].copy()          # tlwh
                dets[:, 2:] += dets[:, :2]          # -> xyxy (seperti branch headtrack)
                cates = np.zeros(dets.shape[0])
                scores = rows[:, 6]
                t0 = time.time()
                online = tracker.update_public(dets, cates, scores)
                t1 = time.time()
                total_time += t1 - t0
                total_frame += 1
                for trk in online:
                    x1, y1, x2, y2, tid, _cate, lag = trk
                    if frame_ind < 2 * args.min_hits and lag < 0:
                        continue
                    w, h = x2 - x1, y2 - y1
                    out_file.write(
                        f"{int(frame_ind + lag)},{int(tid)},{x1:.2f},{y1:.2f},{w:.2f},{h:.2f},1,-1,-1,-1\n"
                    )
    print(f"\nSelesai. {total_frame} frame, {total_time:.1f}s, FPS={total_frame / max(total_time, 1e-9):.1f}")


if __name__ == "__main__":
    main()
