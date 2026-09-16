#!/usr/bin/env python3
"""Compose the four CrowdHuman confusion matrices into one 2x2 figure.

One figure slot in the HKI document, all four fine-tuned architectures visible.
Panel order follows the manuscript's detection table: nano tier (YOLO26n,
YOLOv10n, YOLOv11n) then the small tier anchor (YOLO26s) in the reading order
YOLO26n / YOLO26s on top, YOLOv10n / YOLOv11n below.

Run from the repo root:  python3 scripts/make_confusion_matrix_grid.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "experiments", "journal_figs", "fig_confusion_matrix_grid.png")

PANELS = [
    ("yolo26n_crowdhuman", "YOLO26n"),
    ("yolo26s_crowdhuman", "YOLO26s"),
    ("yolo10_crowdhuman", "YOLOv10n"),
    ("yolo11_crowdhuman", "YOLOv11n"),
]

CELL = 1200          # panel width in the composed figure
PAD = 16             # white gap between panels
BANNER = 64          # height of the label strip above each panel


def font(size):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main() -> int:
    tiles = []
    for folder, label in PANELS:
        src = os.path.join(REPO, "runs", "detect", folder, "confusion_matrix.png")
        if not os.path.exists(src):
            print(f"missing: {src}", file=sys.stderr)
            return 1
        im = Image.open(src).convert("RGB")
        # crop the ultralytics title strip off the top so our own label is the only one
        top = int(im.height * 0.08)
        im = im.crop((0, top, im.width, im.height))
        ratio = CELL / im.width
        im = im.resize((CELL, int(im.height * ratio)), Image.LANCZOS)

        tile = Image.new("RGB", (CELL, BANNER + im.height), "white")
        tile.paste(im, (0, BANNER))
        d = ImageDraw.Draw(tile)
        f = font(34)
        tw = d.textlength(label, font=f)
        d.text(((CELL - tw) / 2, 14), label, fill="black", font=f)
        tiles.append(tile)

    w = CELL * 2 + PAD
    h = max(t.height for t in tiles[:2]) + max(t.height for t in tiles[2:]) + PAD
    canvas = Image.new("RGB", (w, h), "white")
    canvas.paste(tiles[0], (0, 0))
    canvas.paste(tiles[1], (CELL + PAD, 0))
    canvas.paste(tiles[2], (0, tiles[0].height + PAD))
    canvas.paste(tiles[3], (CELL + PAD, tiles[0].height + PAD))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas.save(OUT)
    print(f"{OUT}  {canvas.width}x{canvas.height} ratio={canvas.width / canvas.height:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
