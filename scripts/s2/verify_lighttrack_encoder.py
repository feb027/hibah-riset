"""Verifikasi LAE (Phase 2) — crop GT MOT20 -> cosine embedding.

Mengecek klaim Phase 2: dua crop orang SAMA (track ID sama, frame beda) harus punya
cosine similarity lebih tinggi daripada dua crop orang BEDA (ID beda, frame sama).
Pakai GT (gt/gt.txt) sehingga label "orang sama/beda" benar secara ground-truth.

Contoh (kampus, kernel jupyterhub-env):
    python scripts/s2/verify_lighttrack_encoder.py --seq-dir data/s2/mot20/train/MOT20-01

Keluar: rata-rata cosine same vs diff; assert same > diff (kalau gagal, exit != 0).
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."))
from src.lighttrack.encoder import EmbeddingComputer  # noqa: E402

MIN_BOX = 10  # buang box GT terlalu kecil (<10 px) supaya crop bermakna


def _ped_rows(gt):
    # gt: frame,id,x,y,w,h,conf,cls,vis,...
    m = (gt[:, 6] == 1) & (gt[:, 7] == 1) & (gt[:, 8] > 0) & (gt[:, 4] >= MIN_BOX) & (gt[:, 5] >= MIN_BOX)
    return gt[m]


def _load_gt(path):
    """Load MOT gt.txt (ragged lines) -> (N,9) array frame,id,x,y,w,h,conf,cls,vis."""
    rows = []
    for line in open(path):
        parts = line.strip().split(",")
        if len(parts) < 9:
            continue  # baris tidak lengkap / kosong
        rows.append([float(p) for p in parts[:9]])
    return np.asarray(rows, dtype=np.float64)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seq-dir", required=True, help="folder seq MOT: berisi img1/ dan gt/gt.txt")
    p.add_argument("--frames", type=int, default=10, help="jumlah frame sampel (paling ramai)")
    p.add_argument("--device", default=None, help="cpu / cuda (default: otomatis)")
    args = p.parse_args()

    gt = _load_gt(os.path.join(args.seq_dir, "gt", "gt.txt"))
    ped = _ped_rows(gt)
    if len(ped) == 0:
        print("Tidak ada baris pedestrian valid di gt.txt"); sys.exit(2)

    # frame dengan pedestrian terbanyak -> sampel
    frames, counts = np.unique(ped[:, 0], return_counts=True)
    order = np.argsort(-counts)[: args.frames]
    sample_frames = frames[order].astype(int)

    # pilih track yang muncul di >= 2 frame sampel
    per_id = {}
    for f in sample_frames:
        rows = ped[ped[:, 0] == f]
        for r in rows:
            tid = int(r[1])
            per_id.setdefault(tid, []).append((int(f), r[2:6]))
    same_ids = [tid for tid, fr in per_id.items() if len(fr) >= 2]
    if len(same_ids) < 2:
        print("Terlalu sedikit track berulang; coba --frames lebih besar"); sys.exit(2)
    same_ids = same_ids[: min(len(same_ids), 40)]

    emb = EmbeddingComputer(device=args.device)

    def crop_emb(f, box):
        img = np.fromfile(os.path.join(args.seq_dir, "img1", f"{f:06d}.jpg"), dtype=np.uint8)
        import cv2
        frame = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return emb.embed_frame(frame, [box])[0]

    def cos(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

    same, diff = [], []
    for tid in same_ids:
        f1, b1 = per_id[tid][0]
        f2, b2 = per_id[tid][1]
        same.append(cos(crop_emb(f1, b1), crop_emb(f2, b2)))
    # pasangan beda: ID pertama vs ID kedua pada frame sampel pertama
    for f in sample_frames:
        rows = ped[ped[:, 0] == f][:2]
        if len(rows) == 2:
            diff.append(cos(crop_emb(int(f), rows[0][2:6]), crop_emb(int(f), rows[1][2:6])))
    mean_same, mean_diff = float(np.mean(same)), float(np.mean(diff))
    print(f"sample_frames={sample_frames.tolist()}")
    print(f"cosine same-person : {mean_same:.3f}  (n={len(same)})")
    print(f"cosine diff-person : {mean_diff:.3f}  (n={len(diff)})")
    print(f"selisih            : {mean_same - mean_diff:+.3f}")
    if len(diff) == 0:
        print("Tidak ada pasangan beda dievaluasi"); sys.exit(2)
    assert mean_same > mean_diff, "GAGAL: embedding tidak membedakan orang"
    print("VERIFIKASI OK")


if __name__ == "__main__":
    main()
