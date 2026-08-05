"""LightTrack-ReID-inspired — Phase 1: skeleton tracker (tanpa learning).

Baseline paper = Kalman + IoU + Hungarian + confidence filter + EMA smoothing
(TAHPA OCM/ORU seperti OC-SORT). Kalman via filterpy, Hungarian via scipy.

State Kalman: XYAH (x,y,aspect-ratio,height) + velocity, 8-d (pola SORT/OC_SORT).
Output: format MOT [frame,id,x,y,w,h,conf,-1,-1,-1].
"""
from __future__ import annotations

import numpy as np
from filterpy.kalman import KalmanFilter
from scipy.optimize import linear_sum_assignment


def _iou(a_xyxy, b_xyxy):
    """IoU matrix (M,N) antar dua set box xyxy."""
    a = np.asarray(a_xyxy, dtype=float).reshape(-1, 4)
    b = np.asarray(b_xyxy, dtype=float).reshape(-1, 4)
    xA = np.maximum(a[:, None, 0], b[None, :, 0])
    yA = np.maximum(a[:, None, 1], b[None, :, 1])
    xB = np.minimum(a[:, None, 2], b[None, :, 2])
    yB = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.maximum(0.0, xB - xA) * np.maximum(0.0, yB - yA)
    a_area = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    b_area = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    union = a_area[:, None] + b_area[None, :] - inter
    return np.where(union > 0, inter / np.maximum(union, 1e-9), 0.0)


class _KalmanBox:
    """Constant-velocity XYAH Kalman, pola SORT/OC_SORT (filterpy)."""

    def __init__(self, tlwh):
        self.kf = KalmanFilter(dim_x=8, dim_z=4)
        self.kf.F = np.array([
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]])
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0]])
        self.kf.R[2:, 2:] *= 10.
        self.kf.P[4:, 4:] *= 1000.
        self.kf.P *= 10.
        self.kf.Q[-1, -1] *= 0.01
        self.kf.Q[3, 3] *= 0.01
        x, y, w, h = tlwh
        self.kf.x[:4, 0] = np.array([x + w / 2, y + h / 2, w / max(h, 1e-6), h])

    @property
    def xyah(self):
        return self.kf.x[:4].copy()

    def predict(self):
        self.kf.predict()
        return self.xyah

    def update(self, tlwh):
        x, y, w, h = tlwh
        self.kf.update(np.array([x + w / 2, y + h / 2, w / max(h, 1e-6), h]))


def _xyah_to_tlwh(xyah):
    x, y, a, h = xyah
    w = a * h
    return np.array([x - w / 2, y - h / 2, w, h])


class LightTrackTracker:
    """Skeleton: Kalman predict → IoU cost → Hungarian → update. EMA pada output box."""

    def __init__(self, min_conf=0.3, iou_thresh=0.3, min_hits=3, max_age=30, ema_alpha=0.9):
        self.min_conf = min_conf
        self.iou_thresh = iou_thresh
        self.min_hits = min_hits
        self.max_age = max_age
        self.ema_alpha = ema_alpha
        self.next_id = 1
        self.tracks = {}  # id -> dict(kf, age, hits, ema_box(1x4 tlwh))

    def update(self, dets_tlwh, scores):
        """dets_tlwh: (N,4) tlwh; scores: (N,). Return list of (tlwh, id)."""
        conf = scores >= self.min_conf
        dets_tlwh = np.asarray(dets_tlwh, dtype=float)[conf]
        n_dets = len(dets_tlwh)
        preds = {}
        for tid, tr in self.tracks.items():
            tr["age"] += 1
            tr["kf"].predict()
            preds[tid] = tr["kf"].xyah
        # cost matrix: 1 - IoU (predicted xyxy vs det tlwh->xyxy)
        pred_tlwh = np.array([_xyah_to_tlwh(p) for p in preds.values()]) if preds else np.zeros((0, 4))
        pred_xyxy = np.column_stack([pred_tlwh[:, 0], pred_tlwh[:, 1],
                                     pred_tlwh[:, 0] + pred_tlwh[:, 2],
                                     pred_tlwh[:, 1] + pred_tlwh[:, 3]]) if len(pred_tlwh) else np.zeros((0, 4))
        det_xyxy = np.column_stack([dets_tlwh[:, 0], dets_tlwh[:, 1],
                                    dets_tlwh[:, 0] + dets_tlwh[:, 2],
                                    dets_tlwh[:, 1] + dets_tlwh[:, 3]]) if n_dets else np.zeros((0, 4))
        ious = _iou(pred_xyxy, det_xyxy)
        matched = set()
        if ious.size:
            cost = 1.0 - ious
            r, c = linear_sum_assignment(cost)
            for i, j in zip(r, c):
                if ious[i, j] < self.iou_thresh:
                    continue
                tid = list(preds.keys())[i]
                tr = self.tracks[tid]
                tr["kf"].update(dets_tlwh[j])
                tr["age"] = 0
                tr["hits"] += 1
                ema = tr["ema_box"]
                if ema is None:
                    tr["ema_box"] = dets_tlwh[j].copy()
                else:
                    tr["ema_box"] = self.ema_alpha * dets_tlwh[j] + (1 - self.ema_alpha) * ema
                matched.add(j)
        # deteksi baru
        for j in range(n_dets):
            if j in matched:
                continue
            tid = self.next_id
            self.next_id += 1
            self.tracks[tid] = dict(kf=_KalmanBox(dets_tlwh[j]), age=0, hits=1,
                                    ema_box=None)
        # keluarkan track mati
        dead = [tid for tid, tr in self.tracks.items() if tr["age"] > self.max_age]
        for tid in dead:
            del self.tracks[tid]
        out = []
        for tid, tr in self.tracks.items():
            if tr["hits"] < self.min_hits:
                continue
            box = tr["ema_box"] if tr["ema_box"] is not None else _xyah_to_tlwh(tr["kf"].xyah)
            out.append((box, tid))
        return out


def _demo():
    """Self-check: 3 frame deteksi dua orang — dua ID konsisten, output format benar."""
    tr = LightTrackTracker(min_hits=1)
    d = np.array([[10, 10, 20, 50], [100, 100, 20, 50]])
    ids = set()
    for _ in range(3):
        out = tr.update(d, np.array([0.9, 0.9]))
        ids.update(tid for _, tid in out)
    assert len(ids) == 2, f"harusnya 2 track, dapat {len(ids)}"
    # box output harus bentuk tlwh (4,) non-negatif
    for box, tid in tr.update(d, np.array([0.9, 0.9])):
        assert box.shape == (4,) and (box >= 0).all(), box
    # min_conf menolak deteksi lemah: hanya 1 track yang muncul, id=1
    tr2 = LightTrackTracker(min_hits=1, min_conf=0.5)
    out2 = tr2.update(d, np.array([0.1, 0.9]))
    assert len(out2) == 1 and out2[0][1] == 1, out2
    print("demo OK")


if __name__ == "__main__":
    _demo()
