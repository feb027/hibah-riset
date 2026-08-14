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
    """Skeleton: Kalman predict → cost (IoU, atau LAE+TBSS bila appearance ada) → Hungarian → update. EMA pada output box.

    appearance (optional): objek dengan dua metode:
        embed(frame_bgr, dets_tlwh) -> (N,32) embedding L2-normalized numpy
        score(W, H, track_tlwh, det_tlwh, e_track, e_det) -> (M,N) skor [0,1]
    Tanpa appearance tracker murni IoU (Phase 1/Phase 2 behavior identik).
    """

    def __init__(self, min_conf=0.3, iou_thresh=0.3, min_hits=3, max_age=30, ema_alpha=0.9,
                 appearance=None, appearance_w=0.5, score_min=0.3):
        self.min_conf = min_conf
        self.iou_thresh = iou_thresh
        self.min_hits = min_hits
        self.max_age = max_age
        self.ema_alpha = ema_alpha
        self.appearance = appearance
        # ponytail: w statis 0.5 (blend IoU & skor), ASW adaptif fase berikutnya.
        # Fase berikutnya juga: emb track = mean buffer K (CMOH), sekarang = embedding terakhir.
        self.appearance_w = appearance_w
        self.score_min = score_min
        self.next_id = 1
        self.tracks = {}  # id -> dict(kf, age, hits, ema_box(1x4 tlwh), emb(32,)|None)

    def update(self, dets_tlwh, scores, frame_bgr=None):
        """dets_tlwh: (N,4) tlwh; scores: (N,). frame_bgr wajib bila appearance aktif.
        Return list of (tlwh, id)."""
        conf = scores >= self.min_conf
        dets_tlwh = np.asarray(dets_tlwh, dtype=float)[conf]
        n_dets = len(dets_tlwh)
        preds = {}
        for tid, tr in self.tracks.items():
            tr["age"] += 1
            tr["kf"].predict()
            preds[tid] = tr["kf"].xyah
        e_det = np.zeros((0, 32), dtype=np.float32)  # hanya dipakai bila appearance aktif
        # cost matrix: 1 - (w*sim + (1-w)*IoU)  atau  1 - IoU (appearance=None)
        pred_tlwh = np.array([_xyah_to_tlwh(p) for p in preds.values()]) if preds else np.zeros((0, 4))
        pred_xyxy = np.column_stack([pred_tlwh[:, 0], pred_tlwh[:, 1],
                                     pred_tlwh[:, 0] + pred_tlwh[:, 2],
                                     pred_tlwh[:, 1] + pred_tlwh[:, 3]]) if len(pred_tlwh) else np.zeros((0, 4))
        det_xyxy = np.column_stack([dets_tlwh[:, 0], dets_tlwh[:, 1],
                                    dets_tlwh[:, 0] + dets_tlwh[:, 2],
                                    dets_tlwh[:, 1] + dets_tlwh[:, 3]]) if n_dets else np.zeros((0, 4))
        ious = _iou(pred_xyxy, det_xyxy)
        if self.appearance is not None and frame_bgr is None:
            raise ValueError("appearance aktif tapi frame_bgr tidak diberikan")
        if self.appearance is not None:
            assert frame_bgr is not None  # sudah di-raise di atas
            H, W = frame_bgr.shape[:2]
            e_det = self.appearance.embed(frame_bgr, dets_tlwh) if n_dets else np.zeros((0, 32), dtype=np.float32)
        matched = set()
        if ious.size:
            if self.appearance is not None:
                e_track = np.stack([self.tracks[tid]["emb"] for tid in preds]) if preds \
                    else np.zeros((0, 32), dtype=np.float32)
                sims = self.appearance.score(W, H, pred_tlwh, dets_tlwh, e_track, e_det)
                gate_mat = self.appearance_w * sims + (1 - self.appearance_w) * ious
                cost = 1.0 - gate_mat
            else:
                gate_mat = ious
                cost = 1.0 - ious
            r, c = linear_sum_assignment(cost)
            for i, j in zip(r, c):
                gate = gate_mat[i, j]
                need = (self.score_min if self.appearance is not None else self.iou_thresh)
                if gate < need:
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
                if self.appearance is not None:
                    # ponytail: simpan embedding TERAKHIR; CMOH (mean buffer K) fase berikutnya
                    tr["emb"] = e_det[j]
                matched.add(j)
        # deteksi baru
        for j in range(n_dets):
            if j in matched:
                continue
            tid = self.next_id
            self.next_id += 1
            self.tracks[tid] = dict(kf=_KalmanBox(dets_tlwh[j]), age=0, hits=1,
                                    ema_box=None,
                                    emb=(e_det[j] if self.appearance is not None else None))
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
    """Self-check: jalur IoU-only + jalur appearance (fake numpy) — ID harus stabil saat papasan."""
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

    # ---- jalur appearance: dua objek papasan; IoU menyesatkan, embedding menjaga ID ----
    class FakeAppearance:
        """Embedding dari paritas index (stabil selama urutan deteksi konsisten)."""

        def embed(self, frame_bgr, dets_tlwh):
            n = len(dets_tlwh)
            e = np.zeros((n, 4))
            for i in range(n):
                e[i, i % 2] = 1.0
            return e

        def score(self, W, H, track_tlwh, det_tlwh, e_track, e_det):
            return np.clip(e_track @ e_det.T, 0.0, 1.0)

    def id_at(out, x, y):
        for box, tid in out:
            if abs(box[0] - x) < 2 and abs(box[1] - y) < 2:
                return tid
        return None

    zero = np.zeros((100, 400, 3), dtype=np.uint8)
    f1 = np.array([[10., 10., 20., 50.], [300., 10., 20., 50.]])   # A kiri, B kanan
    f2 = np.array([[290., 10., 20., 50.], [30., 10., 20., 50.]])   # A & B papasan posisi

    app = LightTrackTracker(min_hits=1, appearance=FakeAppearance())
    out1a = app.update(f1, np.array([0.9, 0.9]), frame_bgr=zero)
    out2a = app.update(f2, np.array([0.9, 0.9]), frame_bgr=zero)
    iou_only = LightTrackTracker(min_hits=1)
    out1i = iou_only.update(f1, np.array([0.9, 0.9]))
    out2i = iou_only.update(f2, np.array([0.9, 0.9]))

    # dengan appearance: objek A (awalnya kiri) tetap A walau kotaknya pindah kanan
    assert id_at(out2a, 290, 10) == id_at(out1a, 10, 10), out2a
    # tanpa appearance: A kehilangan ID saat papasan (tertukar/buat track baru)
    assert id_at(out2i, 290, 10) != id_at(out1i, 10, 10), out2i
    print("demo OK (ioU-only + appearance)")


if __name__ == "__main__":
    _demo()
