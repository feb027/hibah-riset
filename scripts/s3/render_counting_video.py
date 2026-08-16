#!/usr/bin/env python3
"""Render Video Demonstrasi Skenario C: Visualisasi People Counting & Line Crossing.

Menggambar perlintasan garis virtual pada video, lintasan gerak centroid pejalan kaki,
dan dashboard hitungan live IN / OUT / TOTAL.

Contoh penggunaan:
    python scripts/s3/render_counting_video.py --seq MOT20-02 --tracker deepocsort --start 1 --end 450
    python scripts/s3/render_counting_video.py --seq MOT20-01 --tracker ocsort
"""
from __future__ import annotations

import argparse
import colorsys
import os
import sys
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.counting.counter import PeopleCounter  # noqa: E402
from core.counting.models import Line, Point  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seq", default="MOT20-02", help="Nama sekuens (mis. MOT20-01, MOT20-02)")
    p.add_argument("--tracker", default="deepocsort", choices=["deepocsort", "ocsort", "diffmot", "lighttrack", "gt"])
    p.add_argument("--line-pos", type=float, default=0.33, help="Posisi garis virtual (0..1)")
    p.add_argument("--start", type=int, default=1, help="Frame awal")
    p.add_argument("--end", type=int, default=450, help="Frame akhir (0 = semua frame)")
    p.add_argument("--out-dir", type=Path, default=ROOT / "experiments" / "s3_counting" / "demo")
    return p.parse_args()


def id_color(tid: int):
    h = (tid * 0.618033988749895) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.9, 0.95)
    return int(b * 255), int(g * 255), int(r * 255)  # BGR format


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Cari folder frame gambar
    img_dir = ROOT / "data" / "s2" / "mot20" / "train" / args.seq / "img1"
    if not img_dir.is_dir():
        sys.exit(f"Folder gambar tidak ditemukan di: {img_dir}")

    frame_files = sorted(img_dir.glob("*.jpg"))
    if not frame_files:
        sys.exit(f"Tidak ada file .jpg di {img_dir}")

    # 2. Cari file track
    if args.tracker == "gt":
        track_file = ROOT / "data" / "s2" / "mot20" / "train" / args.seq / "gt" / "gt.txt"
    else:
        track_file = ROOT / "experiments" / "s2_tracker" / f"{args.tracker}_results" / "mot20" / f"{args.seq}.txt"

    if not track_file.is_file():
        sys.exit(f"File track tidak ditemukan di: {track_file}")

    print(f"Memuat frame dari: {img_dir}")
    print(f"Memuat track dari: {track_file}")

    # Baca track
    tracks_by_frame = defaultdict(list)
    for line in track_file.read_text().splitlines():
        parts = line.strip().split(",")
        if len(parts) >= 6:
            f = int(parts[0])
            tid = int(parts[1])
            x, y, w, h = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            tracks_by_frame[f].append((tid, x, y, w, h))

    # Baca dimensi frame pertama
    first_img = cv2.imread(str(frame_files[0]))
    h_img, w_img = first_img.shape[:2]

    # Inisialisasi Garis Virtual & PeopleCounter
    line_x = int(w_img * args.line_pos)
    virtual_line = Line(start=Point(line_x, 0), end=Point(line_x, h_img))
    counter = PeopleCounter(virtual_line=virtual_line, cooldown_threshold=30)

    # Inisialisasi Video Writer
    end_frame = min(args.end if args.end > 0 else len(frame_files), len(frame_files))
    out_path = args.out_dir / f"{args.seq}_{args.tracker}_counting.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 25
    writer = cv2.VideoWriter(str(out_path), fourcc, fps, (w_img, h_img))

    print(f"Rendering frame {args.start} sampai {end_frame}...")

    recent_crossings = []  # Menyimpan timestamp event perlintasan untuk efek visual flash

    for f_idx in range(args.start, end_frame + 1):
        if f_idx - 1 >= len(frame_files):
            break

        img = cv2.imread(str(frame_files[f_idx - 1]))
        if img is None:
            continue

        prev_in = counter.count_in
        prev_out = counter.count_out

        # Update counter untuk semua track di frame ini
        frame_tracks = tracks_by_frame.get(f_idx, [])
        for tid, x, y, w, h in frame_tracks:
            cx = x + w / 2.0
            cy = y + h / 2.0
            counter.update(tid, Point(cx, cy))

            # Gambar box & titik centroid
            color = id_color(tid)
            cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
            cv2.circle(img, (int(cx), int(cy)), 4, color, -1)
            cv2.putText(img, f"ID:{tid}", (int(x), max(15, int(y) - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        # Cek apakah ada perlintasan baru
        if counter.count_in > prev_in:
            recent_crossings.append((f_idx, "IN", (0, 255, 0)))
        if counter.count_out > prev_out:
            recent_crossings.append((f_idx, "OUT", (0, 165, 255)))

        # Bersihkan crossing tua (> 25 frame)
        recent_crossings = [c for c in recent_crossings if f_idx - c[0] <= 25]

        # 1. Gambar Garis Virtual
        line_color = (0, 255, 255) if not recent_crossings else (0, 255, 0)
        cv2.line(img, (line_x, 0), (line_x, h_img), line_color, 3)
        cv2.putText(img, "VIRTUAL COUNTING LINE", (line_x + 10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, line_color, 2, cv2.LINE_AA)

        # 2. Gambar Dashboard Header
        # Semi-transparent background banner
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w_img, 70), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)

        # Teks Dashboard
        cv2.putText(img, f"SKENARIO C: REAL-TIME COUNTING | TRACKER: {args.tracker.upper()}",
                    (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)

        stat_text = f"IN: {counter.count_in}   |   OUT: {counter.count_out}   |   TOTAL: {counter.count_in + counter.count_out}"
        cv2.putText(img, stat_text, (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

        frame_text = f"Frame: {f_idx}/{end_frame}"
        cv2.putText(img, frame_text, (w_img - 200, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        writer.write(img)

    writer.release()
    print(f"[SELESAI] Video berhasil dirender ke: {out_path}")
    print(f"Hasil Akhir: IN={counter.count_in}, OUT={counter.count_out}, TOTAL={counter.count_in + counter.count_out}")


if __name__ == "__main__":
    main()
