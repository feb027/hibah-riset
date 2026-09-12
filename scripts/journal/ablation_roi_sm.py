#!/usr/bin/env python3
"""Ablasi faktorial RoI x state machine pada sekuens yang tersedia lokal.

Melengkapi `scripts/s3/eval_counting.py` yang hanya memvariasikan panjang cooldown dan
menjalankan seluruh konfigurasi TANPA RoI (`roi=None`). Di sini setiap jalur tracker
di-replay pada enam konfigurasi counting:

    A1  naive line crossing, tanpa RoI            (baseline laporan lama)
    A2  naive line crossing + RoI inset 5%        (kontribusi RoI saja)
    A3  naive line crossing + RoI inset 10%
    B1  state machine CD=30, tanpa RoI            (kontrol, sama dengan laporan lama)
    B2  state machine CD=30 + RoI inset 5%        (Model B penuh)
    B3  state machine CD=30 + RoI inset 10%

Referensi ground truth memakai protokol yang sama dengan laporan lama: PeopleCounter CD=30
tanpa RoI pada lintasan ground truth. RoI inset m% = persegi penuh frame dikurangi margin m
pada tiap sisi; garis hitung vertikal pada x = 0.33 lebar frame.

Hanya memakai pustaka standar (numpy tidak dipakai agar script dapat dijalankan pada mesin
tanpa AVX2). Script mereproduksi angka laporan lama pada konfigurasi B1 sebagai cek silang.

Jalankan: python3 scripts/journal/ablation_roi_sm.py
Keluaran: experiments/s3_counting/counting_ablation_roi.csv + tabel markdown ke stdout.
"""
from __future__ import annotations

import configparser
import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.counting.counter import PeopleCounter  # noqa: E402
from core.counting.models import Line, Point, Polygon  # noqa: E402

LINE_FRAC = 0.33
TRACKERS = ["ocsort", "deepocsort", "diffmot", "lighttrack"]
LABEL = {"ocsort": "OC-SORT", "deepocsort": "Deep-OC-SORT", "diffmot": "DiffMOT", "lighttrack": "LightTrack"}
CONFIGS = [
    ("A1_naive_no_roi", "Naive, tanpa RoI", None),
    ("A2_naive_roi05", "Naive + RoI 5%", 0.05),
    ("A3_naive_roi10", "Naive + RoI 10%", 0.10),
    ("B1_sm30_no_roi", "State machine, tanpa RoI", None),
    ("B2_sm30_roi05", "State machine + RoI 5%", 0.05),
    ("B3_sm30_roi10", "State machine + RoI 10%", 0.10),
]


class NaiveCounter:
    """Model A lokal: perlintasan garis murni, tanpa state dan tanpa cooldown.

    Perilaku penyaringan RoI disamakan dengan PeopleCounter (early return tanpa memperbarui
    riwayat posisi) agar perbandingan faktorial tetap adil.
    """

    def __init__(self, virtual_line: Line, roi: Polygon | None = None) -> None:
        self.virtual_line = virtual_line
        self.roi = roi
        self.count_in = 0
        self.count_out = 0
        self._last: dict[int, Point] = {}

    def update(self, track_id: int, current: Point) -> None:
        from core.counting.detector import LineCrossDetector, PolygonDetector
        if self.roi is not None and not PolygonDetector.is_inside(self.roi, current):
            return
        prev = self._last.get(track_id)
        if prev is not None:
            hit, direction = LineCrossDetector.check_crossing(self.virtual_line, Line(start=prev, end=current))
            if hit:
                if direction == "IN":
                    self.count_in += 1
                else:
                    self.count_out += 1
        self._last[track_id] = current


def make_roi(w: int, h: int, margin: float) -> Polygon:
    return Polygon([Point(w * margin, h * margin), Point(w * (1 - margin), h * margin),
                    Point(w * (1 - margin), h * (1 - margin)), Point(w * margin, h * (1 - margin))])


def load_mot(path: Path, gt: bool) -> dict[int, list[tuple[int, float, float]]]:
    """Muat berkas format MOT; untuk GT, saring hanya kelas pejalan kaki (kolom 8 == 1)."""
    frames: dict[int, list[tuple[int, float, float]]] = defaultdict(list)
    if not path.is_file():
        return frames
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 6:
                continue
            try:
                vals = [float(v) for v in row[:10]]
            except ValueError:
                continue
            if gt and len(vals) >= 8 and vals[7] != 1:
                continue
            frame, tid, x, y, w, h = vals[:6]
            frames[int(frame)].append((int(tid), x + w / 2.0, y + h / 2.0))
    return frames


def seq_dimensions(seq_dir: Path) -> tuple[int, int, int]:
    ini = seq_dir / "seqinfo.ini"
    if ini.is_file():
        cp = configparser.ConfigParser()
        cp.read(ini)
        if "Sequence" in cp:
            return (int(cp["Sequence"].get("imWidth", 1920)), int(cp["Sequence"].get("imHeight", 1080)),
                    int(cp["Sequence"].get("seqLength", 1000)))
    return 1920, 1080, 1000


def replay(counter, frames: dict[int, list[tuple[int, float, float]]], max_frame: int) -> tuple[int, int]:
    for f in range(1, max_frame + 1):
        for tid, cx, cy in frames.get(f, ()):
            counter.update(tid, Point(cx, cy))
    return counter.count_in, counter.count_out


def find_sequences() -> list[tuple[str, Path, str]]:
    """Kumpulkan sekuens yang tersedia lokal, satu entri per nama sekuens (dedup)."""
    found: dict[str, tuple[str, Path, str]] = {}
    for ds, split, roots in (("mot20", "train", ["mot20", "mot20_hf"]), ("dancetrack", "val", ["dancetrack"])):
        for root in roots:
            base = ROOT / "data" / "s2" / root / split
            if not base.is_dir():
                continue
            for p in sorted(base.iterdir()):
                if p.is_dir() and (p / "gt" / "gt.txt").is_file() and p.name not in found:
                    found[p.name] = (p.name, p, ds)
    return list(found.values())


def main() -> None:
    seqs = find_sequences()
    if not seqs:
        sys.exit("tidak ada sekuens dengan ground truth di data/s2")
    print(f"sekuens ditemukan: {len(seqs)} -> {[s[0] for s in seqs]}\n")

    rows: list[dict] = []
    for seq, sdir, ds in seqs:
        w, h, seq_len = seq_dimensions(sdir)
        line = Line(start=Point(int(w * LINE_FRAC), 0), end=Point(int(w * LINE_FRAC), h))
        gt_frames = load_mot(sdir / "gt" / "gt.txt", gt=True)
        max_frame = max(max(gt_frames, default=1), seq_len)
        gt_in, gt_out = replay(PeopleCounter(virtual_line=line, cooldown_threshold=30), gt_frames, max_frame)
        gt_tot = gt_in + gt_out
        if gt_tot == 0:
            continue

        for trk in TRACKERS:
            trk_file = ROOT / "experiments" / "s2_tracker" / f"{trk}_results" / ds / f"{seq}.txt"
            pred = load_mot(trk_file, gt=False)
            if not pred:
                print(f"  [SKIP] {trk}: {trk_file} kosong/tidak ada")
                continue
            for key, label, margin in CONFIGS:
                roi = make_roi(w, h, margin) if margin else None
                counter = (NaiveCounter(line, roi) if key.startswith("A")
                           else PeopleCounter(virtual_line=line, cooldown_threshold=30, roi=roi))
                p_in, p_out = replay(counter, pred, max_frame)
                tot = p_in + p_out
                rows.append({"seq": seq, "tracker": trk, "config": key, "GT_TOTAL": gt_tot, "Pred_TOTAL": tot,
                             "MAE": abs(tot - gt_tot), "Error_Pct": round(abs(tot - gt_tot) / gt_tot * 100.0, 2),
                             "Over_Count": max(0, tot - gt_tot), "Under_Count": max(0, gt_tot - tot)})
        print(f"[{seq}] GT={gt_tot} selesai")

    if not rows:
        sys.exit("tidak ada hasil; cek path experiments/s2_tracker")

    out = ROOT / "experiments" / "s3_counting" / "counting_ablation_roi.csv"
    with open(out, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)
    print(f"\n[SUKSES] tersimpan: {out}  ({len(rows)} baris)")

    # cek silang: B1 harus mereproduksi laporan lama untuk sekuens yang tersedia
    old_path = ROOT / "experiments" / "s3_counting" / "counting_ablation.csv"
    if old_path.is_file():
        old = {f"{r['seq']}|{r['tracker']}": float(r["Error_Pct"]) for r in csv.DictReader(open(old_path))
               if r["model"] == "Model_B_CD30_Default"}
        new = {f"{r['seq']}|{r['tracker']}": r["Error_Pct"] for r in rows if r["config"] == "B1_sm30_no_roi"}
        checked = [k for k in new if k in old]
        bad = [k for k in checked if abs(new[k] - old[k]) > 0.011]
        assert not bad, f"B1 tidak mereproduksi laporan lama pada: {bad[:5]}"
        print(f"verifikasi OK: B1 identik dengan laporan lama pada {len(checked)} baris\n")

    def aggregate(subset: list[dict]) -> tuple[float, float, float, int, int]:
        sgt = sum(r["GT_TOTAL"] for r in subset)
        spr = sum(r["Pred_TOTAL"] for r in subset)
        return (st.mean([r["Error_Pct"] for r in subset]), 100 * (spr - sgt) / sgt,
                st.mean([r["MAE"] for r in subset]),
                sum(r["Over_Count"] for r in subset), sum(r["Under_Count"] for r in subset))

    g: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        g[(r["tracker"], r["config"])].append(r)
    print("| Jalur pelacakan | Konfigurasi | Galat per sekuens (%) | Galat gabungan (%) | MAE | Over-count | Under-count |")
    print("|---|---|---|---|---|---|---|")
    for trk in TRACKERS:
        for key, label, _ in CONFIGS:
            rs = g[(trk, key)]
            if not rs:
                continue
            e, pooled, mae, ov, un = aggregate(rs)
            print(f"| {LABEL[trk]} | {label} | {e:.2f} | {pooled:+.2f} | {mae:.2f} | {ov} | {un} |")

    print(f"\n=== agregat seluruh jalur ({len(rows)} baris) ===")
    print("| Konfigurasi | Galat per sekuens (%) | Galat gabungan (%) | MAE | Over-count | Under-count |")
    print("|---|---|---|---|---|---|")
    for key, label, _ in CONFIGS:
        e, pooled, mae, ov, un = aggregate([r for r in rows if r["config"] == key])
        print(f"| {label} | {e:.2f} | {pooled:+.2f} | {mae:.2f} | {ov} | {un} |")


if __name__ == "__main__":
    main()
