#!/usr/bin/env python3
"""Extract reference-paper figures used by the HKI document.

The HKI manuscript cites the original architecture and pipeline figures of three
trackers it evaluates (OC-SORT, DiffMOT, LightTrack-ReID) plus the MOT20 dataset
overview. Those figures are publisher-copyrighted, so they are NOT committed to
this public repository: this script regenerates them locally from the PDFs in
docs/research/papers/, which ARE tracked.

Output goes to docs/hki/gambar/ (gitignored). Run before assembling the Word file.

Usage:  python3 scripts/extract_hki_reference_figures.py
"""
from __future__ import annotations

import os
import sys

import fitz
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(REPO, "docs", "research", "papers")
OUT = os.path.join(REPO, "docs", "hki", "gambar")

# (output name, source pdf, 1-based page, caption anchor to find the figure above)
JOBS = [
    ("ocsort-fig2-pipeline",
     "S024-observation-centric-sort-rethinking-sort-for-robust-multi-object-track.pdf",
     4, "Figure 2. The pipeline"),
    ("diffmot-fig2-arch",
     "S021-diffmot-a-real-time-diffusion-based-multiple-object-tracker-with-non-l.pdf",
     3, "Figure 2. The overall architecture of DiffMOT"),
    ("lighttrack-fig2-overview",
     "S014-lighttrack-reid-a-lightweight-and-occlusion-robust-framework-for-multi.pdf",
     3, "Fig 2."),
    ("mot20-fig1-overview",
     "S036-mot20-a-benchmark-for-multi-object-tracking-in-crowded-scenes.pdf",
     2, "Fig. 1: An overview"),
]

DPI = 300
MIN_SIDE = 40          # ignore small inline glyphs/decoration rects
TRIM_THRESHOLD = 245   # pixel value above which a region counts as blank


def figure_region(page, caption_bbox):
    """Union of image and vector-drawing rects that sit above the caption."""
    rects = [fitz.Rect(i["bbox"]) for i in page.get_image_info()]
    rects += [fitz.Rect(d["rect"]) for d in page.get_drawings()]
    above = [r for r in rects
             if r.y1 <= caption_bbox.y0 + 2 and r.width > MIN_SIDE and r.height > MIN_SIDE]
    if not above:
        return None
    above.sort(key=lambda r: -r.y1)
    box = above[0]
    for r in above[1:]:
        if r.y0 < box.y1 + 20 and r.y1 > box.y0 - 20:
            box |= r
    return box


def trim(image):
    bbox = image.convert("L").point(lambda v: 0 if v >= TRIM_THRESHOLD else 255).getbbox()
    if not bbox:
        return image
    pad = 8
    return image.crop((max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
                       min(bbox[2] + pad, image.width), min(bbox[3] + pad, image.height)))


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    failures = []
    for name, pdf_name, pno, caption in JOBS:
        path = os.path.join(PAPERS, pdf_name)
        if not os.path.exists(path):
            failures.append(f"{name}: missing {pdf_name}")
            continue
        doc = fitz.open(path)
        page = doc[pno - 1]
        hits = page.search_for(caption[:45])
        if not hits:
            failures.append(f"{name}: caption not found")
            doc.close()
            continue
        region = figure_region(page, hits[0])
        if region is None:
            failures.append(f"{name}: no figure rects above caption")
            doc.close()
            continue
        clip = fitz.Rect(min(region.x0, page.rect.x0 + 18) - 2, max(region.y0, 20) - 2,
                         max(region.x1, page.rect.x1 - 18) + 2, min(region.y1, hits[0].y1) + 4)
        raw = os.path.join(OUT, f".{name}.raw.png")
        page.get_pixmap(clip=clip, dpi=DPI).save(raw)
        image = trim(Image.open(raw).convert("RGB"))
        image.save(os.path.join(OUT, f"{name}.png"))
        os.remove(raw)
        print(f"{name}: {image.width}x{image.height} ratio={image.width / image.height:.2f}")
        doc.close()

    if failures:
        print("FAILURES:", *failures, sep="\n  ", file=sys.stderr)
        return 1
    print(f"done -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
