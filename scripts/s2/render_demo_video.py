#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render video demo Skenario B: deteksi (Skenario A, YOLO26 fine-tune) + tracking OC-SORT.

Cara pakai:
    python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450        # hasil OC-SORT
    python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450 --source gt   # GT reference

Frame diunduh sekali dari HF (Lekim89/MOT20, CDN — Xet di-disable agar tidak kena kuota API),
hasil tracking dibaca dari experiments/s2_tracker/ocsort_results/mot20/<seq>.txt.
FPS diambil dari seqinfo.ini dataset (MOT20 = 25 fps; DanceTrack = 30 fps) — bukan asumsi.
Tidak butuh numpy/cv2: menggambar dengan Pillow, encode dengan binary ffmpeg (imageio-ffmpeg).
"""
import argparse
import colorsys
import configparser
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

SEQ_DEFAULT_FPS = {
    "MOT20-01": 25, "MOT20-02": 25, "MOT20-03": 25, "MOT20-05": 25,
    "dancetrack": 30,
}


def seq_fps(seq: str, fallback: int) -> int:
    ini = DATA / "mot20_hf" / "train" / seq / "seqinfo.ini"
    try:
        cp = configparser.ConfigParser()
        cp.read(ini)
        return int(cp["Sequence"]["frameRate"])
    except Exception:
        return fallback


def id_color(tid: int):
    """Warna stabil per ID (HSV -> RGB 0-255)."""
    h = (tid * 0.618033988749895) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.85, 0.95)
    return int(r * 255), int(g * 255), int(b * 255)


def load_mot(path: Path):
    """MOT format: frame,id,x,y,w,h,conf,... (frame 1-based). Return {frame: [(id,x,y,w,h,conf)]}."""
    tracks = defaultdict(list)
    for line in path.read_text().splitlines():
        p = line.strip().split(",")
        if len(p) < 7:
            continue
        frame, tid = int(float(p[0])), int(float(p[1]))
        x, y, w, h = (float(p[i]) for i in range(2, 6))
        conf = float(p[6])
        tracks[frame].append((tid, x, y, w, h, conf))
    return tracks


def load_gt(path: Path):
    """MOT GT: frame,id,x,y,w,h,conf,class,visibility. Hanya box trackable (class==1) digambar penuh."""
    tracks = defaultdict(list)
    for line in path.read_text().splitlines():
        p = line.strip().split(",")
        if len(p) < 9:
            continue
        frame, tid = int(float(p[0])), int(float(p[1]))
        x, y, w, h = (float(p[i]) for i in range(2, 6))
        cls = int(float(p[7]))
        tracks[frame].append((tid, x, y, w, h, cls))
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
    ap.add_argument("--seq", required=True, help="nama sekuens, mis. MOT20-02 / dancetrack0004")
    ap.add_argument("--start", type=int, default=1, help="frame awal (1-based)")
    ap.add_argument("--end", type=int, default=0, help="frame akhir (0 = sampai habis)")
    ap.add_argument("--fps", type=int, default=0, help="override fps (default: baca seqinfo)")
    ap.add_argument("--source", choices=["track", "gt"], default="track",
                    help="track = hasil tracker (OC-SORT/DiffMOT); gt = ground truth (referensi)")
    ap.add_argument("--tracker", choices=["ocsort", "diffmot"], default="ocsort",
                    help="hasil tracking mana yang dirender (format MOT di experiments/s2_tracker/<tracker>_results/)")
    ap.add_argument("--max-w", type=int, default=960)
    args = ap.parse_args()

    TRACKER_LABEL = {"ocsort": "OC-SORT", "diffmot": "DiffMOT"}

    is_mot = args.seq.startswith("MOT20")
    fallback_fps = SEQ_DEFAULT_FPS.get("MOT20" if is_mot else "dancetrack", 30)
    fps = args.fps or (seq_fps(args.seq, fallback_fps) if is_mot else fallback_fps)

    if args.source == "track":
        total = len(list((DATA / "mot20_hf" / "train" / args.seq / "img1").glob("*.jpg"))) if is_mot else 0
        if total == 0:
            print("!! frame dataset belum diunduh — jalankan sekali tanpa --source untuk download")
            return 1
        src_path = EXP / f"{args.tracker}_results" / ("mot20" if is_mot else "dancetrack") / f"{args.seq}.txt"
        if not src_path.exists():
            print("!! tidak ada hasil tracking:", src_path)
            return 1
        data = load_mot(src_path)
        label = TRACKER_LABEL[args.tracker]
    else:
        gt_path = DATA / "mot20_hf" / "train" / args.seq / "gt" / "gt.txt"
        total = len(list((DATA / "mot20_hf" / "train" / args.seq / "img1").glob("*.jpg")))
        if not gt_path.exists():
            print("!! tidak ada GT:", gt_path)
            return 1
        data = load_gt(gt_path)
        label = "Ground Truth (referensi)"

    end = args.end or total
    assert 1 <= args.start <= end <= total, f"range frame salah ({args.start}..{end} / {total})"
    OUT.mkdir(parents=True, exist_ok=True)

    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 13)
    except Exception:
        font = font_small = None

    img_dir = DATA / "mot20_hf" / "train" / args.seq / "img1"
    if not any(img_dir.glob("*.jpg")):
        print(f"[1/4] unduh frame {args.seq} dari HF ...")
        try:
            from huggingface_hub import snapshot_download
        except ModuleNotFoundError:
            sys.exit("huggingface_hub tidak ada di venv ini; install: pip install huggingface_hub")
        snapshot_download(
            repo_id="Lekim89/MOT20", repo_type="dataset",
            allow_patterns=[f"train/{args.seq}/*"],
            local_dir=str(DATA / "mot20_hf"),
        )
    frames = sorted(img_dir.glob("*.jpg"))
    if len(frames) < end:
        print(f"!! frame tersedia {len(frames)} < {end}; pakai {len(frames)}")
        end = len(frames)

    from PIL import Image, ImageDraw, ImageFont

    sample = Image.open(frames[args.start - 1])
    scale = args.max_w / sample.width
    H = int(sample.height * scale)
    W = args.max_w
    tag = f"{args.seq}_f{args.start}-{end}_{'gt' if args.source == 'gt' else f'tracked_{args.tracker}'}"
    out_mp4 = OUT / f"{tag}.mp4"
    proc = ffmpeg_writer(out_mp4, W, H, fps)

    print(f"[render] {args.seq} {args.start}..{end} @ {fps} fps, sumber={args.source} -> {out_mp4}")
    for i in range(args.start, end + 1):
        im = Image.open(frames[i - 1]).convert("RGB").resize((W, H))
        d = ImageDraw.Draw(im)
        active = data.get(i, [])
        for tid, x, y, w, h, extra in active:
            x0, y0 = int(x * scale), int(y * scale)
            x1, y1 = int((x + w) * scale), int((y + h) * scale)
            if args.source == "gt":
                if extra == 1:  # class 1 = trackable pedestrian
                    d.rectangle([x0, y0, x1, y1], outline=(60, 179, 60), width=2)
                    d.text((x0, max(0, y0 - 18)), f"GT#{tid}", fill=(60, 179, 60), font=font_small)
                else:  # distractor/ignore
                    d.rectangle([x0, y0, x1, y1], outline=(150, 150, 150), width=1)
            else:
                c = id_color(tid)
                d.rectangle([x0, y0, x1, y1], outline=c, width=2)
                d.text((x0, max(0, y0 - 18)), f"#{tid}", fill=c, font=font_small)
        d.rectangle([0, 0, W, 34], fill=(0, 0, 0))
        d.text((10, 6), f"{args.seq} | {label} | count: {len(active)}", fill=(255, 255, 255), font=font)
        proc.stdin.write(im.tobytes())
        if i % 60 == 0:
            print(f"   frame {i}/{end}")

    proc.stdin.close()
    proc.wait()
    print(f"[4/4] selesai: {out_mp4} ({(end - args.start + 1)} frame @ {fps} fps = "
          f"{(end - args.start + 1) / fps:.1f} dtk)")


if __name__ == "__main__":
    sys.exit(main())
