#!/usr/bin/env python3
"""Dekomposisi galat hitung: lantai deteksi vs kegagalan asosiasi identitas vs duplikat.

Menjawab pertanyaan reviewer "berapa bagian galat hitung yang berasal dari objek yang
tidak terdeteksi dan berapa yang berasal dari identitas yang berpindah". Caranya: setiap
kejadian perlintasan pada lintasan ground truth diberi sebab, dan setiap kejadian hitung
pada lintasan tracker dicek apakah punya padanan di ground truth.

Definisi (per sekuens, per jalur pelacakan, garis virtual x = 0.33w, cooldown 30 frame):

  Kejadian GT  (gid, frame, arah) -> salah satu dari:
    tercatat          ada kejadian tracker pada jendela +-W frame dengan arah sama yang
                      lintasannya dipadankan ke gid
    gagal deteksi     tidak ada lintasan tracker yang dipadankan ke gid di seluruh jendela
    gagal asosiasi    ada lintasan tracker yang dipadankan ke gid, tetapi tidak menghasilkan
                      kejadian perlintasan (lintasan terputus, identitas berpindah, atau
                      lintasan terdistorsi sehingga tidak memotong garis)

  Kejadian tracker (pid, frame, arah) -> salah satu dari:
    sah               padanan pertama untuk satu kejadian GT
    duplikat          padanan kedua dan seterusnya untuk kejadian GT yang sama
    tanpa padanan     tidak ada kejadian GT yang cocok (lintasan palsu atau identitas baru
                      hasil fragmentasi yang melintas ulang)

Pemadanan identitas: IoU kotak per frame, greedy menurun, ambang 0.30. Satu id tracker
dipetakan ke id GT yang paling sering dipadankan sepanjang hidupnya; jumlah id GT berbeda
yang pernah dipadankan dicatat sebagai indikator pergantian identitas.

Cek otomatis: tercatat + gagal_deteksi + gagal_asosiasi == total kejadian GT, dan
sah + duplikat + tanpa_padanan == total kejadian tracker.

Jalankan: python3 scripts/journal/attribute_counting_error.py
Keluaran: experiments/s3_counting/counting_error_attribution.csv + tabel markdown.
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.counting.counter import PeopleCounter  # noqa: E402
from core.counting.models import Line, Point  # noqa: E402

from ablation_roi_sm import DATA_ROOT, TRACKER_ROOT, find_sequences  # noqa: E402

LINE_FRAC = 0.33
COOLDOWN = 30
WINDOW = 30   # jendela pencocokan kejadian, dalam frame
IOU_MIN = 0.30
TRACKERS = ["ocsort", "deepocsort", "diffmot", "lighttrack"]
LABEL = {"ocsort": "OC-SORT", "deepocsort": "Deep-OC-SORT", "diffmot": "DiffMOT", "lighttrack": "LightTrack"}


def load_mot(path: Path, gt: bool) -> dict[int, list[tuple[int, float, float, float, float, float]]]:
    """frame -> [(id, cx, cy, x, y, w, h)]; untuk GT saring kelas pejalan kaki saja."""
    frames: dict[int, list[tuple]] = defaultdict(list)
    if not path.is_file():
        return frames
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 6:
                continue
            try:
                v = [float(x) for x in row[:10]]
            except ValueError:
                continue
            if gt and len(v) >= 8 and v[7] != 1:
                continue
            f, tid, x, y, w, h = v[:6]
            if w <= 0 or h <= 0:
                continue
            frames[int(f)].append((int(tid), x + w / 2, y + h / 2, x, y, w, h))
    return frames


def iou(a: tuple, b: tuple) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x1, y1 = max(ax, bx), max(ay, by)
    x2, y2 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    if x2 <= x1 or y2 <= y1:
        return 0.0
    inter = (x2 - x1) * (y2 - y1)
    return inter / (aw * ah + bw * bh - inter)


def replay_events(counter, frames: dict[int, list[tuple]], max_frame: int) -> list[tuple[int, int, str]]:
    """Jalankan penghitung dan catat setiap kejadian perlintasan (frame, id, arah)."""
    events = []
    for f in range(1, max_frame + 1):
        for tid, cx, cy, *_ in frames.get(f, ()):
            before = (counter.count_in, counter.count_out)
            counter.update(tid, Point(cx, cy))
            if counter.count_in > before[0]:
                events.append((f, tid, "IN"))
            elif counter.count_out > before[1]:
                events.append((f, tid, "OUT"))
    return events


def frame_matches(gt_frames: dict[int, list[tuple]], pred_frames: dict[int, list[tuple]]) -> dict[int, dict[int, int]]:
    """frame -> {pred_id: gt_id} dari pemadanan IoU greedy menurun."""
    per_frame: dict[int, dict[int, int]] = {}
    for f, preds in pred_frames.items():
        gts = gt_frames.get(f)
        if not gts:
            continue
        pairs = []
        for p in preds:
            pid, pbox = p[0], (p[3], p[4], p[5], p[6])
            for g in gts:
                gid, gbox = g[0], (g[3], g[4], g[5], g[6])
                v = iou(pbox, gbox)
                if v >= IOU_MIN:
                    pairs.append((v, pid, gid))
        pairs.sort(reverse=True)
        used_p, used_g, m = set(), set(), {}
        for v, pid, gid in pairs:
            if pid in used_p or gid in used_g:
                continue
            used_p.add(pid)
            used_g.add(gid)
            m[pid] = gid
        if m:
            per_frame[f] = m
    return per_frame


def attribute(gt_frames, pred_frames, line, max_frame) -> dict:
    gt_events = replay_events(PeopleCounter(virtual_line=line, cooldown_threshold=COOLDOWN), gt_frames, max_frame)
    pred_events = replay_events(PeopleCounter(virtual_line=line, cooldown_threshold=COOLDOWN), pred_frames, max_frame)
    per_frame = frame_matches(gt_frames, pred_frames)

    # id GT yang pernah dipadankan ke tiap id tracker (indikator pergantian identitas)
    votes: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    gt_seen_frames: dict[int, set[int]] = defaultdict(set)
    for f, m in per_frame.items():
        for pid, gid in m.items():
            votes[pid][gid] += 1
            gt_seen_frames[gid].add(f)

    def gid_at(pid: int, frame: int) -> int | None:
        """id GT yang dipadankan ke id tracker ini pada frame kejadian (toleransi +-5 frame)."""
        for f in (frame, frame - 1, frame + 1, frame - 2, frame + 2, frame - 2, frame + 3,
                  frame - 3, frame + 4, frame - 4, frame + 5, frame - 5):
            gid = per_frame.get(f, {}).get(pid)
            if gid is not None:
                return gid
        return None

    # kejadian tracker beserta id GT pada saat perlintasan
    pred_ev = [(j, f, pid, d, gid_at(pid, f)) for j, (f, pid, d) in enumerate(pred_events)]
    gt_by_id: dict[int, list[tuple[int, str]]] = defaultdict(list)
    for f, gid, d in gt_events:
        gt_by_id[gid].append((f, d))

    res = dict(gt_total=len(gt_events), pred_total=len(pred_events), tercatat=0,
               gagal_deteksi=0, gagal_asosiasi=0, sah=0, duplikat=0, tanpa_padanan=0,
               id_switches=sum(1 for v in votes.values() if len(v) > 1), id_tracked=len(votes))

    claimed: set[int] = set()  # index global kejadian tracker yang sudah menjadi padanan sah
    for gid, evs in gt_by_id.items():
        for f, d in evs:
            cand = [j for j, pf, pid, pd, pg in pred_ev
                    if pg == gid and pd == d and abs(pf - f) <= WINDOW and j not in claimed]
            if cand:
                claimed.add(cand[0])
                res["tercatat"] += 1
            elif any(abs(sf - f) <= WINDOW for sf in gt_seen_frames.get(gid, ())):
                res["gagal_asosiasi"] += 1
            else:
                res["gagal_deteksi"] += 1

    for j, f, pid, d, gid in pred_ev:
        if j in claimed:
            res["sah"] += 1
        elif gid is not None and any(pd == d and pf <= f for pf, pd in gt_by_id.get(gid, ())):
            res["duplikat"] += 1
        else:
            res["tanpa_padanan"] += 1

    assert res["tercatat"] + res["gagal_deteksi"] + res["gagal_asosiasi"] == res["gt_total"], res
    assert res["sah"] + res["duplikat"] + res["tanpa_padanan"] == res["pred_total"], res
    return res


def sequences(data_root: Path = DATA_ROOT, tracker_root: Path = TRACKER_ROOT) -> list[tuple[str, Path, str]]:
    """Reuse penemuan sekuens dari ablation_roi_sm (satu tempat, tidak ada tebakan path)."""
    return find_sequences(data_root, tracker_root)


def dimensions(seq_dir: Path) -> tuple[int, int, int]:
    ini = seq_dir / "seqinfo.ini"
    if ini.is_file():
        cp = configparser.ConfigParser()
        cp.read(ini)
        if "Sequence" in cp:
            return (int(cp["Sequence"].get("imWidth", 1920)), int(cp["Sequence"].get("imHeight", 1080)),
                    int(cp["Sequence"].get("seqLength", 1000)))
    return 1920, 1080, 1000


def main() -> None:
    data_root = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_ROOT
    tracker_root = Path(sys.argv[2]) if len(sys.argv) > 2 else TRACKER_ROOT
    rows = []
    for seq, sdir, ds in sequences(data_root, tracker_root):
        w, h, seq_len = dimensions(sdir)
        line = Line(start=Point(int(w * LINE_FRAC), 0), end=Point(int(w * LINE_FRAC), h))
        gt_frames = load_mot(sdir / "gt" / "gt.txt", gt=True)
        max_frame = max(max(gt_frames, default=1), seq_len)
        for trk in TRACKERS:
            pred = load_mot(tracker_root / f"{trk}_results" / ds / f"{seq}.txt", gt=False)
            if not pred:
                continue
            r = attribute(gt_frames, pred, line, max_frame)
            rows.append({"seq": seq, "tracker": trk, **r})
            print(f"[{seq} | {LABEL[trk]}] GT={r['gt_total']} pred={r['pred_total']} "
                  f"tercatat={r['tercatat']} det={r['gagal_deteksi']} asos={r['gagal_asosiasi']} "
                  f"sah={r['sah']} dup={r['duplikat']} tanpa_padanan={r['tanpa_padanan']}")

    if not rows:
        sys.exit("tidak ada baris hasil. Cek pesan [cari] di atas, lalu tunjuk lokasi manual:\n"
                 f"  python3 {Path(__file__).name} <data_root> <tracker_root>")
    out = ROOT / "experiments" / "s3_counting" / "counting_error_attribution.csv"
    with open(out, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)
    print(f"\n[SUKSES] tersimpan: {out} ({len(rows)} baris)\n")

    print("| Jalur pelacakan | Kejadian GT | Tercatat | Gagal deteksi | Gagal asosiasi | Kejadian tracker | Sah | Duplikat | Tanpa padanan |")
    print("|---|---|---|---|---|---|---|---|---|")
    for trk in TRACKERS:
        rs = [r for r in rows if r["tracker"] == trk]
        if not rs:
            continue
        s = {k: sum(r[k] for r in rs) for k in ("gt_total", "tercatat", "gagal_deteksi", "gagal_asosiasi",
                                                "pred_total", "sah", "duplikat", "tanpa_padanan")}
        print(f"| {LABEL[trk]} | {s['gt_total']} | {s['tercatat']} | {s['gagal_deteksi']} | {s['gagal_asosiasi']} | "
              f"{s['pred_total']} | {s['sah']} | {s['duplikat']} | {s['tanpa_padanan']} |")

    print("\npersentase terhadap kejadian GT / kejadian tracker:")
    print("| Jalur pelacakan | Tercatat (%) | Gagal deteksi (%) | Gagal asosiasi (%) | Sah (%) | Duplikat (%) | Tanpa padanan (%) |")
    print("|---|---|---|---|---|---|---|")
    for trk in TRACKERS:
        rs = [r for r in rows if r["tracker"] == trk]
        if not rs:
            continue
        g = sum(r["gt_total"] for r in rs) or 1
        p = sum(r["pred_total"] for r in rs) or 1
        print(f"| {LABEL[trk]} | {100*sum(r['tercatat'] for r in rs)/g:.1f} | "
              f"{100*sum(r['gagal_deteksi'] for r in rs)/g:.1f} | {100*sum(r['gagal_asosiasi'] for r in rs)/g:.1f} | "
              f"{100*sum(r['sah'] for r in rs)/p:.1f} | {100*sum(r['duplikat'] for r in rs)/p:.1f} | "
              f"{100*sum(r['tanpa_padanan'] for r in rs)/p:.1f} |")


if __name__ == "__main__":
    main()
