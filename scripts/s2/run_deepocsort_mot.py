#!/usr/bin/env python3
"""Run Deep-OC-SORT atas deteksi format MOT (det.txt) untuk evaluasi TrackEval.

Menggunakan DeepOCSortTracker mandiri yang diintegrasikan dengan visual embedder ONNX
(atau PyTorch) untuk mengekstrak Dynamic Appearance Cost Matrix (ACM) dan melakukan
asosiasi berbasis Velocity Direction Consistency (VDC) serta Adaptive Weighting (AW).

Input : {det_dir}/{seq}.txt — format deteksi MOT: frame,id,x,y,w,h,conf,cls,-1,-1
Output: {out_dir}/{seq}.txt — format TrackEval: frame,id,x,y,w,h,conf,-1,-1,-1

Contoh penggunaan:
    python scripts/s2/run_deepocsort_mot.py \
        --det-dir data/s2/mot20/det_mot/train \
        --out-dir experiments/s2_tracker/deepocsort_results/mot20 \
        --img-dir data/s2/mot20/train \
        --onnx-dir out/onnx
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from src.deepocsort.tracker import DeepOCSortTracker  # noqa: E402
from src.lighttrack.phase4_onnx import TbssAppearanceOnnx  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--det-dir", required=True, help="folder berisi {seq}.txt deteksi MOT")
    p.add_argument("--out-dir", required=True, help="folder output hasil tracker untuk TrackEval")
    p.add_argument("--img-dir", required=True, help="folder berisi frame gambar ({seq}/img1/*.jpg)")
    p.add_argument("--onnx-dir", default=os.path.join(ROOT, "out", "onnx"),
                   help="folder berisi lae.onnx + tbss.onnx (default: out/onnx)")
    p.add_argument("--min-conf", type=float, default=0.3, help="ambang batas deteksi")
    p.add_argument("--iou-thresh", type=float, default=0.3)
    p.add_argument("--min-hits", type=int, default=3)
    p.add_argument("--max-age", type=int, default=30)
    p.add_argument("--delta-t", type=int, default=3)
    p.add_argument("--inertia", type=float, default=0.2)
    p.add_argument("--appearance-w", type=float, default=0.5, help="bobot visual appearance cost (w_assoc)")
    p.add_argument("--ema-alpha", type=float, default=0.95, help="bobot EMA appearance embedding")
    p.add_argument("--aw-param", type=float, default=0.5, help="parameter adaptive weighting max diff")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    if not os.path.isdir(args.img_dir):
        sys.exit(f"Folder gambar tidak ditemukan: {args.img_dir}")

    print(f"Memuat visual embedder dari {args.onnx_dir} ...")
    appearance = TbssAppearanceOnnx(args.onnx_dir)

    seq_files = sorted(f for f in os.listdir(args.det_dir) if f.endswith(".txt"))
    total_time, total_frame = 0.0, 0

    for seq_name in seq_files:
        seq_stem = seq_name[:-4] if seq_name.endswith(".txt") else seq_name
        print(f"[{seq_stem}] Memproses tracking ...")

        img_root = Path(args.img_dir) / seq_stem / "img1"
        img_frames = sorted(img_root.glob("*.*"))
        if not img_frames:
            print(f"  (PERINGATAN: tidak ada frame di {img_root}, sekuens dilewati)")
            continue

        seq_path = os.path.join(args.det_dir, seq_name)
        seq_trks = np.loadtxt(seq_path, dtype=np.float64, delimiter=",").reshape(-1, 10)
        if seq_trks.shape[0] == 0:
            print("  (deteksi kosong, dilewati)")
            continue

        tracker = DeepOCSortTracker(
            det_thresh=args.min_conf,
            max_age=args.max_age,
            min_hits=args.min_hits,
            iou_threshold=args.iou_thresh,
            delta_t=args.delta_t,
            inertia=args.inertia,
            w_association_emb=args.appearance_w,
            alpha_fixed_emb=args.ema_alpha,
            aw_param=args.aw_param,
            appearance=appearance,
        )

        min_frame, max_frame = int(seq_trks[:, 0].min()), int(seq_trks[:, 0].max())
        out_path = os.path.join(args.out_dir, seq_name)

        with open(out_path, "w") as out_file:
            for frame_ind in range(min_frame, max_frame + 1):
                rows = seq_trks[seq_trks[:, 0] == frame_ind]
                if args.min_conf > 0 and rows.shape[0]:
                    rows = rows[rows[:, 6] >= args.min_conf]

                # Dets dalam format tlwh -> xyxy
                dets_tlwh = rows[:, 2:6].copy()
                dets_xyxy = dets_tlwh.copy()
                dets_xyxy[:, 2] += dets_xyxy[:, 0]
                dets_xyxy[:, 3] += dets_xyxy[:, 1]
                scores = rows[:, 6]

                idx = frame_ind - 1
                if idx < 0 or idx >= len(img_frames):
                    continue

                frame_bgr = cv2.imread(str(img_frames[idx]))
                if frame_bgr is None:
                    continue

                t0 = time.perf_counter()
                online = tracker.update(dets_xyxy, scores, frame_bgr=frame_bgr)
                t1 = time.perf_counter()

                total_time += (t1 - t0)
                total_frame += 1

                for trk in online:
                    tlwh_box, tid = trk
                    bx, by, bw, bh = tlwh_box
                    out_file.write(
                        f"{frame_ind},{int(tid)},{bx:.2f},{by:.2f},{bw:.2f},{bh:.2f},1,-1,-1,-1\n"
                    )

        print(f"  Selesai {seq_stem}: hasil disimpan ke {out_path}")

    fps = total_frame / max(total_time, 1e-9)
    print(f"\nSemua sekuens selesai! Total frame: {total_frame}, Waktu: {total_time:.2f}s, Rata-rata FPS Tracking: {fps:.1f}")


if __name__ == "__main__":
    main()
