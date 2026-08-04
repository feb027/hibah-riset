#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figur laporan Skenario B — digambar dengan Pillow (tanpa numpy/matplotlib,
agar jalan di VPS tanpa AVX / env minimal). Sumber: artifacts eksperimen.

Output PNG di experiments/s2_tracker/figs/:
  fig1_hota_mota_idf1.png   bar HOTA/MOTA/IDF1 per benchmark
  fig2_idsw_frag.png        bar IDSW/Frag per benchmark
  fig3_density_dance.png    kepadatan deteksi per sekuens DanceTrack (dets/frame)
  fig4_density_mot20.png    kepadatan deteksi per sekuens MOT20 (dets/frame)
"""
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "s2_tracker"
FIGS = EXP / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

try:
    F_TITLE = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    F_LABEL = ImageFont.truetype("DejaVuSans.ttf", 17)
    F_VAL = ImageFont.truetype("DejaVuSans.ttf", 14)
    F_SMALL = ImageFont.truetype("DejaVuSans.ttf", 12)
except Exception:
    F_TITLE = F_LABEL = F_VAL = F_SMALL = None

BLUE = (44, 111, 187)
BLUE_L = (155, 184, 216)
ORANGE = (224, 123, 57)
ORANGE_L = (240, 192, 151)
DARK = (40, 40, 40)
GRID = (210, 210, 210)
WHITE = (255, 255, 255)


def _text_size(d, txt, font):
    if hasattr(d, "textbbox"):
        b = d.textbbox((0, 0), txt, font=font)
        return b[2] - b[0], b[3] - b[1]
    return d.textsize(txt, font=font)


def bar_chart(title, groups, fname, ymax, unit=""):
    """groups: list of dict {label, bars: [(name, value, color)], }"""
    W, H = 1100, 620
    m_l, m_r, m_t, m_b = 90, 30, 70, 70
    cw = W - m_l - m_r
    ch = H - m_t - m_b
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    n_groups = len(groups)
    max_bars = max(len(g["bars"]) for g in groups)
    slot = cw / n_groups
    bw = min(42, slot / (max_bars + 0.8))

    # grid + sumbu
    n_ticks = 4
    for i in range(n_ticks + 1):
        y = m_t + ch - ch * i / n_ticks
        v = ymax * i / n_ticks
        d.line([m_l, y, W - m_r, y], fill=GRID, width=1)
        t = f"{v:.0f}"
        tw, th = _text_size(d, t, F_SMALL)
        d.text((m_l - tw - 8, y - th / 2), t, fill=DARK, font=F_SMALL)
    d.line([m_l, m_t, m_l, m_t + ch], fill=DARK, width=2)
    d.line([m_l, m_t + ch, W - m_r, m_t + ch], fill=DARK, width=2)

    for gi, g in enumerate(groups):
        cx = m_l + slot * gi + slot / 2
        n = len(g["bars"])
        for bi, (name, val, color) in enumerate(g["bars"]):
            x0 = cx - (n * bw + (n - 1) * 6) / 2 + bi * (bw + 6)
            bh = ch * val / ymax
            y0 = m_t + ch - bh
            d.rectangle([x0, y0, x0 + bw, m_t + ch], fill=color)
            vt = f"{val:.1f}"
            vw, vh = _text_size(d, vt, F_VAL)
            d.text((x0 + bw / 2 - vw / 2, y0 - vh - 3), vt, fill=DARK, font=F_VAL)
            if n > 1:
                nw, nh = _text_size(d, name, F_SMALL)
                d.text((x0 + bw / 2 - nw / 2, m_t + ch + 6), name, fill=DARK, font=F_SMALL)
        gl = g["label"]
        gw, gh = _text_size(d, gl, F_LABEL)
        d.text((cx - gw / 2, m_t + ch + (26 if max_bars > 1 else 8)), gl, fill=DARK, font=F_LABEL)

    tw, th = _text_size(d, title, F_TITLE)
    d.text((W / 2 - tw / 2, 18), title, fill=DARK, font=F_TITLE)
    img.save(FIGS / fname)
    print("saved", FIGS / fname)


# --- data -------------------------------------------------------------------
rows = list(csv.DictReader((EXP / "eval_results.csv").open()))
by_bm = {r["benchmark"]: {m: float(r[m]) for m in ["HOTA", "MOTA", "IDF1", "IDSW", "Frag"]} for r in rows}

# Fig 1: HOTA/MOTA/IDF1 per benchmark
groups = []
for bm, c in [("MOT20", BLUE), ("DanceTrack", ORANGE)]:
    groups.append({
        "label": bm,
        "bars": [(m, by_bm[bm][m], c) for m in ["HOTA", "MOTA", "IDF1"]],
    })
bar_chart("Skenario B - OC-SORT: HOTA / MOTA / IDF1 per benchmark", groups, "fig1_hota_mota_idf1.png", ymax=80)

# Fig 2: IDSW/Frag per benchmark
groups = [
    {"label": "MOT20", "bars": [("IDSW", by_bm["MOT20"]["IDSW"], BLUE), ("Frag", by_bm["MOT20"]["Frag"], BLUE_L)]},
    {"label": "DanceTrack", "bars": [("IDSW", by_bm["DanceTrack"]["IDSW"], ORANGE), ("Frag", by_bm["DanceTrack"]["Frag"], ORANGE_L)]},
]
bar_chart("Skenario B - OC-SORT: ID Switch & Fragmentasi per benchmark", groups, "fig2_idsw_frag.png", ymax=16000)

# Fig 3: kepadatan deteksi DanceTrack
drows = [r for r in csv.DictReader((EXP / "detection_stats.csv").open()) if r.get("dataset") == "dancetrack"]
if drows:
    items = sorted(((float(r["dets/frame"]), r["seq"]) for r in drows), reverse=True)
    W, H = 1100, 720
    m_l, m_r, m_t, m_b = 260, 40, 70, 50
    cw = W - m_l - m_r
    ch = H - m_t - m_b
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    ymax = max(v for v, _ in items) * 1.15
    slot = ch / len(items)
    bh = min(16, slot * 0.72)
    for i in range(5):
        x = m_l + cw * i / 4
        d.line([x, m_t, x, m_t + ch], fill=GRID, width=1)
        t = f"{ymax * i / 4:.0f}"
        tw, th = _text_size(d, t, F_SMALL)
        d.text((x - tw / 2, m_t + ch + 6), t, fill=DARK, font=F_SMALL)
    d.line([m_l, m_t, m_l, m_t + ch], fill=DARK, width=2)
    d.line([m_l, m_t + ch, W - m_r, m_t + ch], fill=DARK, width=2)
    for i, (v, name) in enumerate(items):
        y0 = m_t + i * slot
        bw = cw * v / ymax
        d.rectangle([m_l, y0 + (slot - bh) / 2, m_l + bw, y0 + (slot - bh) / 2 + bh], fill=BLUE)
        nw, nh = _text_size(d, name, F_SMALL)
        d.text((m_l - nw - 10, y0 + slot / 2 - nh / 2), name, fill=DARK, font=F_SMALL)
        vt = f"{v:.0f}"
        vw, vh = _text_size(d, vt, F_VAL)
        d.text((m_l + bw + 8, y0 + slot / 2 - vh / 2), vt, fill=DARK, font=F_VAL)
    tw, th = _text_size(d, "Kepadatan deteksi per frame - DanceTrack val (YOLO26 fine-tune)", F_TITLE)
    d.text((W / 2 - tw / 2, 18), "Kepadatan deteksi per frame - DanceTrack val (YOLO26 fine-tune)", fill=DARK, font=F_TITLE)
    img.save(FIGS / "fig3_density_dance.png")
    print("saved", FIGS / "fig3_density_dance.png")

# Fig 4: kepadatan deteksi MOT20
mot20 = [("MOT20-01", 18839, 214), ("MOT20-02", 157368, 1391), ("MOT20-03", 276114, 1202), ("MOT20-05", 449452, 1657)]
dens = [(d / f, n) for n, d, f in mot20]
groups = [{"label": n, "bars": [("", v, BLUE)]} for v, n in dens]
bar_chart("Kepadatan deteksi per frame - MOT20 train (YOLO26 fine-tune)", groups, "fig4_density_mot20.png", ymax=max(v for v, _ in dens) * 1.2)

print("selesai.")
