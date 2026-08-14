"""LightTrack-ReID-inspired — runner MOT: deteksi format MOT -> hasil tracker.

Phase 1 (tanpa --ckpt): tracker IoU-only (Kalman+Hungarian+EMA), numpy/scipy tanpa torch.
Phase 4 (dengan --ckpt): asosiasi memakai LAE + TBSS (perlu torch; crop dari frame asli).

Input : {det_dir}/{seq}.txt — format deteksi MOT: frame,id,x,y,w,h,conf,cls,-1,-1 (id boleh -1)
Output: {out_dir}/{seq}.txt — format hasil TrackEval: frame,id,x,y,w,h,conf,-1,-1,-1

Contoh:
    # Phase 1 (tanpa torch):
    python scripts/s2/run_lighttrack_mot.py \
        --det-dir data/s2/mot20/det_mot/train \
        --out-dir experiments/s2_tracker/lighttrack_results/mot20

    # Phase 4 (LAE + TBSS dari ckpt training):
    python scripts/s2/run_lighttrack_mot.py \
        --det-dir data/s2/mot20/det_mot/train \
        --out-dir experiments/s2_tracker/lighttrack_results/mot20 \
        --ckpt out/phase3_fold1_v2/best.pt \
        --img-dir data/s2/mot20/train
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

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
    p.add_argument("--ckpt", default=None,
                   help="ckpt .pt (best.pt/last.pt) utk LAE+TBSS — tanpa ini tracker IoU-only")
    p.add_argument("--img-dir", default=None,
                   help="folder berisi {seq}/img1/*.jpg (WAJIB saat --ckpt; crop embedding)")
    p.add_argument("--appearance-w", type=float, default=0.5,
                   help="bobot skor penampilan vs IoU saat --ckpt (1 = murni penampilan)")
    p.add_argument("--score-min", type=float, default=0.3,
                   help="ambang skor gabungan untuk match saat --ckpt")
    p.add_argument("--lae-only", action="store_true",
                   help="pakai LAE murni (sim=cosine, tanpa TBSS) — ablasi '+LAE' paper; "
                        "cocok utk ckpt v1 (TBSS-nya gagal). Padukan --appearance-w 1.0")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    if args.ckpt and not args.img_dir:
        sys.exit("--ckpt butuh --img-dir (folder sekuens berisi {seq}/img1 untuk crop embedding)")
    appearance = None
    if args.ckpt:
        if not os.path.isdir(args.img_dir):
            sys.exit(f"--img-dir tidak ada: {args.img_dir}")
        from src.lighttrack.phase4 import TbssAppearance
        appearance = TbssAppearance(args.ckpt, use_tbss=not args.lae_only)

    seq_files = sorted(f for f in os.listdir(args.det_dir) if f.endswith(".txt"))

    total_time, total_frame = 0.0, 0
    for seq_name in seq_files:
        print(f"[{seq_name}]")
        seq_stem = seq_name[:-4] if seq_name.endswith(".txt") else seq_name
        img_frames = []
        if appearance:
            img_root = Path(args.img_dir) / seq_stem / "img1"
            img_frames = sorted(img_root.glob("*.*"))
            if not img_frames:
                sys.exit(f"tidak ada frame di {img_root} — cek --img-dir/{seq_stem}/img1")
        seq_trks = np.loadtxt(os.path.join(args.det_dir, seq_name), dtype=np.float64,
                              delimiter=",").reshape(-1, 10)
        if seq_trks.shape[0] == 0:
            print("  (kosong, dilewati)"); continue
        tracker = LightTrackTracker(min_conf=args.min_conf, iou_thresh=args.iou_thresh,
                                    min_hits=args.min_hits, max_age=args.max_age,
                                    ema_alpha=args.ema_alpha,
                                    appearance=appearance,
                                    appearance_w=args.appearance_w,
                                    score_min=args.score_min)
        min_frame, max_frame = int(seq_trks[:, 0].min()), int(seq_trks[:, 0].max())
        with open(os.path.join(args.out_dir, f"{seq_name}"), "w") as out_file:
            for frame_ind in range(min_frame, max_frame + 1):
                rows = seq_trks[seq_trks[:, 0] == frame_ind]
                if args.min_conf > 0 and rows.shape[0]:
                    rows = rows[rows[:, 6] >= args.min_conf]
                dets = rows[:, 2:6].copy()          # tlwh
                scores = rows[:, 6]
                frame_bgr = None
                if appearance:
                    idx = frame_ind - 1
                    if idx < 0 or idx >= len(img_frames):
                        sys.exit(f"{seq_stem}: frame {frame_ind} di luar img1 "
                                 f"({len(img_frames)} frame) — data tidak lengkap")
                    import cv2
                    frame_bgr = cv2.imread(str(img_frames[idx]))
                    if frame_bgr is None:
                        sys.exit(f"{seq_stem}: gagal baca {img_frames[idx]}")
                t0 = time.time()
                online = tracker.update(dets, scores, frame_bgr=frame_bgr)
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
