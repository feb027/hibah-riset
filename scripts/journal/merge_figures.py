#!/usr/bin/env python3
"""Gabungkan beberapa PNG figur jadi satu panel (a), (b), ... untuk hemat halaman.

Dipakai untuk menggabungkan Fig. 4 (sensitivitas cooldown) dan Fig. 5 (sensitivitas
confidence) menjadi satu figur dua panel agar naskah tetap 15 halaman.

Hanya memakai Pillow (matplotlib tidak tersedia di sebagian mesin; data mentahnya
sudah tidak ada, jadi komposit dari PNG adalah satu-satunya jalur yang jujur).

Jalankan:
    python3 scripts/journal/merge_figures.py (a) (b) --out experiments/journal_figs/gabung.png
Argumen bisa dua berkas atau lebih; label panel mengikuti urutan berkas.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FIGDIR = Path(__file__).resolve().parents[2] / "experiments" / "journal_figs"
GAP = 60          # jarak antar panel, piksel
PAD = 20          # margin di sekeliling kanvas
LABEL_SIZE = 44   # tinggi huruf label panel


def trim_white(im: Image.Image, tol: int = 245) -> Image.Image:
    """Potong border putih supaya panel tidak membawa margin kosong."""
    gray = im.convert("L")
    bbox = gray.point(lambda p: 0 if p > tol else 255).getbbox()
    return im.crop(bbox) if bbox else im


def load_font() -> ImageFont.ImageFont:
    for name in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, LABEL_SIZE)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("images", nargs="+", help="berkas PNG, urut sesuai panel (a), (b), ...")
    p.add_argument("--out", default=str(FIGDIR / "fig_gabung.png"))
    p.add_argument("--gap", type=int, default=GAP)
    p.add_argument("--labels", default="abcdef", help="huruf label panel")
    args = p.parse_args()

    paths = [Path(x) if Path(x).is_file() else FIGDIR / x for x in args.images]
    panels = [trim_white(Image.open(f).convert("RGB")) for f in paths]
    for f, panel in zip(paths, panels):
        print(f"{f.name}: {panel.size} (setelah dipotong)")

    height = max(im.height for im in panels)
    scaled = [im if im.height == height else im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
              for im in panels]

    width = PAD * 2 + sum(im.width for im in scaled) + args.gap * (len(scaled) - 1)
    canvas = Image.new("RGB", (width, height + PAD * 2 + LABEL_SIZE), "white")
    draw = ImageDraw.Draw(canvas)
    font = load_font()

    x = PAD
    for i, im in enumerate(scaled):
        draw.text((x + 4, PAD), f"({args.labels[i]})", fill="black", font=font)
        canvas.paste(im, (x, PAD + LABEL_SIZE))
        x += im.width + args.gap

    out = Path(args.out)
    canvas.save(out, optimize=True)
    print(f"[SUKSES] {out}  {canvas.size}  ({out.stat().st_size // 1024} KB)")
    print(f"Di Word: sisipkan selebar kolom, aspect ratio {canvas.width / canvas.height:.2f}:1 "
          f"-> tinggi sekitar {16 / (canvas.width / canvas.height):.1f} cm pada lebar 16 cm")


if __name__ == "__main__":
    main()
