#!/usr/bin/env python3
"""Compose a 2x2 panel figure from the four CrowdHuman training runs.

Two figures, one slot each in the HKI document:
  --figure training   runs/detect/<run>/results.png              (training curves)
  --figure cm         runs/detect/<run>/confusion_matrix.png     (confusion matrix)

Panel order follows the manuscript's detection table: nano tier first
(YOLO26n, YOLOv10n, YOLOv11n) with the small-tier anchor YOLO26s on top right.

Usage:  python3 scripts/make_model_figures.py            # both figures
        python3 scripts/make_model_figures.py --figure cm
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(REPO, "experiments", "journal_figs")

# (run folder, label shown above the panel, reading order)
PANELS = [
    ("yolo26n_crowdhuman", "YOLO26n", 0),
    ("yolo26s_crowdhuman", "YOLO26s", 1),
    ("yolo10_crowdhuman", "YOLOv10n", 2),
    ("yolo11_crowdhuman", "YOLOv11n", 3),
]

FIGURES = {
    # figure key: (source filename, output filename, cell width, crop top fraction)
    "training": ("results.png", "fig_training_curves_grid.png", 1500, 0.0),
    "cm": ("confusion_matrix.png", "fig_confusion_matrix_grid.png", 1200, 0.08),
}

PAD = 16
BANNER = 64


def font(size):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build(key):
    src_name, out_name, cell, crop_top = FIGURES[key]
    tiles = []
    for folder, label, _ in PANELS:
        src = os.path.join(REPO, "runs", "detect", folder, src_name)
        if not os.path.exists(src):
            print(f"missing source: {src}", file=sys.stderr)
            return None
        im = Image.open(src).convert("RGB")
        if crop_top:
            im = im.crop((0, int(im.height * crop_top), im.width, im.height))
        im = im.resize((cell, round(im.height * cell / im.width)), Image.LANCZOS)

        tile = Image.new("RGB", (cell, BANNER + im.height), "white")
        tile.paste(im, (0, BANNER))
        draw = ImageDraw.Draw(tile)
        f = font(34)
        draw.text(((cell - draw.textlength(label, font=f)) / 2, 14), label, fill="black", font=f)
        tiles.append(tile)

    top_h = max(t.height for t in tiles[:2])
    canvas = Image.new("RGB", (cell * 2 + PAD, top_h * 2 + PAD), "white")
    canvas.paste(tiles[0], (0, 0))
    canvas.paste(tiles[1], (cell + PAD, 0))
    canvas.paste(tiles[2], (0, top_h + PAD))
    canvas.paste(tiles[3], (cell + PAD, top_h + PAD))

    out = os.path.join(OUTDIR, out_name)
    os.makedirs(OUTDIR, exist_ok=True)
    canvas.save(out)
    print(f"{out_name}: {canvas.width}x{canvas.height} ratio={canvas.width / canvas.height:.2f}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--figure", choices=sorted(FIGURES), default=None,
                    help="build one figure; omit to build both")
    args = ap.parse_args()
    keys = [args.figure] if args.figure else sorted(FIGURES)
    for key in keys:
        if not build(key):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
