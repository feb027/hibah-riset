#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render video demo Skenario B: deteksi (Skenario A, YOLO26 fine-tune) + tracking OC-SORT.

Cara pakai:
    python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450 --fps 30
    python scripts/s2/render_demo_video.py --seq MOT20-01

Frame diunduh sekali dari HF (Lekim89/MOT20, CDN — Xet di-disable agar tidak kena kuota API),
hasil tracking dibaca dari experiments/s2_tracker/ocsort_results/mot20/<seq>.txt.
Tidak butuh numpy/cv2: menggambar dengan Pillow, encode dengan binary ffmpeg (imageio-ffmpeg).
"""
import argparse
import colorsys
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "s2"
EXP = ROOT / "experiments" / "s2_tracker"
OUT = EXP / "demo"

SEQ_META = {
    "MOT20-01": (214, "Kerumunan jarang, gerak linier"),
    "MOT20-02": (1391, "Kerumunan padat, banyak oklusi"),
    "MOT20-03": (1202, "Kerumunan padat, oklusi berat"),
    "MOT20-05": (1657, "Kepadatan ekstrem, oklusi masif"),
}


def id_color(tid: int):
    """Warna stabil per ID track (HSV -> RGB 0-255)."""
    h = (tid * 0.618033988749895) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.85, 0.95)
    return int(r * 255), int(g * 255), int(b * 255)


def load_tracks(path: Path):
    """MOT format: frame,id,x,y,w,h,conf,-1,-1,-1 (frame 1-based)."""
    tracks = defaultdict(list)
    for line in path.read_text().splitlines():
        p = line.strip().split(",")
        if len(p) < 7:
            continue
        frame, tid, x, y, w, h = (float(p[i]) for i in range(6))
        tracks[int(frame)].append((int(tid), x, y, w, h))
    return tracks


def ffmpeg_writer(path: Path, w: int, h: int, fps: int):
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg = "ffmpeg"
    cmd = [
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-movflags", "+faststart",
        str(path),
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True, choices=list(SEQ_META))
    ap.add_argument("--start", type=int, default=1, help="frame awal (1-based)")
    ap.add_argument("--end", type=int, default=0, help="frame akhir (0 = sampai habis)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--max-w", type=int, default=960)
    args = ap.parse_args()

    total = SEQ_META[args.seq][0]
    end = args.end or total
    assert 1 <= args.start <= end <= total, f"range frame salah ({args.start}..{end} / {total})"

    OUT.mkdir(parents=True, exist_ok=True)

    # 1) frame dari HF (sekali; resume otomatis)
    from huggingface_hub import snapshot_download
    img_dir = DATA / "mot20_hf" / "train" / args.seq / "img1"
    if not any(img_dir.glob("*.jpg")):
        print(f"[1/4] unduh frame {args.seq} dari HF ...")
        snapshot_download(
            repo_id="Lekim89/MOT20", repo_type="dataset",
            allow_patterns=[f"train/{args.seq}/*"],
            local_dir=str(DATA / "mot20_hf"),
        )
    frames = sorted(img_dir.glob("*.jpg"))
    if len(frames) < end:
        print(f"!! frame tersedia {len(frames)} < {end}; pakai {len(frames)}")
        end = len(frames)

    # 2) hasil tracking
    print("[2/4] baca hasil tracking OC-SORT ...")
    tracks = load_tracks(EXP / "ocsort_results" / "mot20" / f"{args.seq}.txt")

    # 3) render
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 13)
    except Exception:
        font = font_small = None

    print(f"[3/4] render frame {args.start}..{end} ...")
    sample = Image.open(frames[args.start - 1])
    scale = args.max_w / sample.width
    H = int(sample.height * scale)
    W = args.max_w
    out_mp4 = OUT / f"{args.seq}_f{args.start}-{end}_tracked.mp4"
    proc = ffmpeg_writer(out_mp4, W, H, args.fps)

    for i in range(args.start, end + 1):
        im = Image.open(frames[i - 1]).convert("RGB").resize((W, H))
        d = ImageDraw.Draw(im)
        active = tracks.get(i, [])
        for tid, x, y, w, h in active:
            x0, y0 = int(x * scale), int(y * scale)
            x1, y1 = int((x + w) * scale), int((y + h) * scale)
            c = id_color(tid)
            d.rectangle([x0, y0, x1, y1], outline=c, width=2)
            d.text((x0, max(0, y0 - 18)), f"#{tid}", fill=c, font=font_small)
        # header: counting (jumlah ID aktif) — relevan untuk people counting
        d.rectangle([0, 0, W, 34], fill=(0, 0, 0))
        d.text((10, 6), f"{args.seq} | OC-SORT | count: {len(active)}", fill=(255, 255, 255), font=font)
        proc.stdin.write(im.tobytes())
        if i % 60 == 0:
            print(f"   frame {i}/{end}")

    proc.stdin.close()
    proc.wait()
    print(f"[4/4] selesai: {out_mp4}")
    print(f"      ({end - args.start + 1} frame @ {args.fps} fps = {(end - args.start + 1)/args.fps:.1f} dtk)")


if __name__ == "__main__":
    sys.exit(main())
