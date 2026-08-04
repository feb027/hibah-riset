#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnosa kualitas video demo: bandingkan hasil tracking vs GT (IoU, ukuran, cakupan). Tanpa numpy."""
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load_mot(path):
    d = {}
    for line in Path(path).read_text().splitlines():
        p = line.split(',')
        if len(p) < 8:
            continue
        f, tid = int(float(p[0])), int(float(p[1]))
        x, y, w, h = float(p[2]), float(p[3]), float(p[4]), float(p[5])
        d.setdefault(f, []).append((tid, x, y, w, h))
    return d

def iou(a, b):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    iw, ih = max(0, ix1 - ix0), max(0, iy1 - iy0)
    inter = iw * ih
    if inter == 0:
        return 0.0
    return inter / ((ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - inter)

def median(vals):
    return statistics.median(vals) if vals else 0.0

for seq in ['MOT20-01', 'MOT20-02']:
    gt = load_mot(ROOT / f'data/s2/mot20_hf/train/{seq}/gt/gt.txt')
    tr = load_mot(ROOT / f'experiments/s2_tracker/ocsort_results/mot20/{seq}.txt')
    gf, tf = set(gt), set(tr)
    print(f'=== {seq} === GT frames {min(gf)}..{max(gf)} ({len(gf)}) | track frames {min(tf)}..{max(tf)} ({len(tf)})')
    frames = sorted(gf)
    step = max(1, len(frames) // 6)
    for f in frames[::step]:
        g = [b[1:] for b in gt[f]]
        t = [b[1:] for b in tr.get(f, [])]
        if not g or not t:
            print(f'  frame {f}: GT={len(g)} track={len(t)} (skip)')
            continue
        best = []
        for bx, by, bw, bh in t:
            bb = (bx, by, bx + bw, by + bh)
            m = max(iou(bb, (gx, gy, gx + gw, gy + gh)) for gx, gy, gw, gh in g)
            best.append(m)
        frac = sum(1 for v in best if v > 0.5) / len(best)
        gsizes = [gw * gh for gx, gy, gw, gh in g]
        tsizes = [bw * bh for bx, by, bw, bh in t]
        print(f'  frame {f}: GT={len(g)} track={len(t)} | median best-IoU={median(best):.2f} '
              f'frac>0.5={frac:.0%} | GT med={median(gsizes):.0f}px2 track med={median(tsizes):.0f}px2')
