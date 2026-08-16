"""LightTrack-ReID-inspired — Phase 1: skeleton tracker (tanpa learning).

Baseline paper = Kalman + IoU + Hungarian + confidence filter + EMA smoothing
(TAHPA OCM/ORU seperti OC-SORT). Kalman via filterpy, Hungarian via scipy.

State Kalman: XYAH (x,y,aspect-ratio,height) + velocity, 8-d (pola SORT/OC_SORT).
Output: format MOT [frame,id,x,y,w,h,conf,-1,-1,-1].
"""
from __future__ import annotations

import numpy as np
from collections import deque
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


def _asw_weight(det_xyxy):
    """ASW (paper Eq 10): w_t = sigmoid(N_occ/N_t), GLOBAL per frame.

    det_xyxy: (N,4) deteksi setelah conf-filter. N_occ = jumlah deteksi yang
    IoU > 0.5 dgn deteksi lain (potensi oklusi); N_t = total. Frame ramai ->
    w_t tinggi -> asosiasi lebih percaya penampilan daripada geometri.
    N=0/1 -> w_t = sigmoid(0) = 0.5 (netral, sama dgn appearance_w default).
    """
    n = len(det_xyxy)
    if n < 2:
        return 0.5
    iou_mat = _iou(det_xyxy, det_xyxy)
    np.fill_diagonal(iou_mat, 0.0)  # jangan hitung diri sendiri
    n_occ = int(np.sum(np.any(iou_mat > 0.5, axis=1)))
    return float(1.0 / (1.0 + np.exp(-n_occ / max(1, n))))


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
    # filterpy kf.x berbentuk KOLOM: bisa (8,1), x[:4] -> (4,1), atau sudah (4,).
    # Flatten dulu supaya tahan numpy 1.x (float() array 1-elemen cuma warning)
    # DAN numpy 2.x (jadi error: "only 0-dimensional arrays can be converted").
    x, y, a, h = (float(v) for v in np.asarray(xyah, dtype=float).reshape(-1)[:4])
    w = a * h
    return np.array([x - w / 2, y - h / 2, w, h])


class LightTrackTracker:
    """Skeleton: Kalman predict → cost (IoU, atau LAE+TBSS bila appearance ada) → Hungarian → update. EMA pada output box.

    appearance (optional): objek dengan dua metode:
        embed(frame_bgr, dets_tlwh) -> (N,32) embedding L2-normalized numpy
        score(W, H, track_tlwh, det_tlwh, e_track, e_det) -> (M,N) skor [0,1]
    Tanpa appearance tracker murni IoU (Phase 1/Phase 2 behavior identik).

    CMOH (paper Eq 7-9): tiap tracklet simpan buffer K=10 embedding TERAKHIR.
    Saat tracklet tidak mendapat match (age > 0, kemungkinan oklusi), embedding
    yang dikirim ke TBSS = RATA-RATA buffer (a_ctx). Dot(a_ctx, e_det) = rata-rata
    cosine K pasangan terakhir, jadi sinyal tetap di [-1,1] tanpa normalisasi ulang.
    """

    def __init__(self, min_conf=0.3, iou_thresh=0.3, min_hits=3, max_age=30, ema_alpha=0.9,
                 appearance=None, appearance_w=0.5, score_min=0.3, cmoh_k=10, emit_age=5,
                 asw=False):
        self.min_conf = min_conf
        self.iou_thresh = iou_thresh
        self.min_hits = min_hits
        self.max_age = max_age
        self.ema_alpha = ema_alpha
        self.appearance = appearance
        # ponytail: w statis 0.5 (blend IoU & skor), ASW adaptif fase berikutnya.
        self.appearance_w = appearance_w
        self.score_min = score_min
        self.cmoh_k = cmoh_k
        # ASW (paper Eq 10): w_t = sigmoid(N_occ/N_t) — GLOBAL per frame.
        # N_occ = deteksi yang overlap IoU > 0.5 dgn deteksi lain; N_t = total det.
        # Frame ramai (banyak overlap) -> w_t tinggi -> lebih percaya penampilan.
        self.asw = asw
        # emit_age: track gap DI-SEMBUNYIKAN (tidak di-emit) setelah usia ini,
        # tapi tetap hidup untuk matching (OCM). max_age=umur match, emit_age=umur
        # output — memisahkan keduanya mencegah box hantu = FP (MOTA). 
        self.emit_age = emit_age
        self.next_id = 1
        self.tracks = {}  # id -> dict(kf, age, hits, ema_box(1x4 tlwh), emb_buf(deque[K]))

    def _track_emb(self, tr):
        """Embedding tracklet utk TBSS: CMOH a_ctx (mean buffer) saat age>0, else embedding terakhir."""
        buf = tr["emb_buf"]
        if len(buf) == 0:
            return None
        if tr["age"] > 0 and len(buf) > 1:
            return np.mean(np.stack(buf), axis=0)
        return buf[-1]

    def update(self, dets_tlwh, scores, frame_bgr=None):
        """dets_tlwh: (N,4) tlwh; scores: (N,). frame_bgr wajib bila appearance aktif.
        Return list of (tlwh, id)."""
        conf = scores >= self.min_conf
        dets_tlwh = np.asarray(dets_tlwh, dtype=float)[conf]
        n_dets = len(dets_tlwh)
        preds = {}
        for tid, tr in self.tracks.items():
            tr["age"] += 1
            if tr["age"] <= 1:
                # OCM-light: Kalman predict HANYA utk track yang aktif (baru match
                # frame lalu, atau 1 frame masuk gap). Track gap lebih lama DI-FREEZE
                # di posisi terakhir yang ke-match — tanpa freeze, prediksi drift
                # terus dan max_age panjang malah nyasar ke deteksi orang lain
                # (sweep max_age=90/150 → MOTA negatif, IDSW naik).
                tr["kf"].predict()
            preds[tid] = tr["kf"].xyah
        e_det = np.zeros((0, 32), dtype=np.float32)  # hanya dipakai bila appearance aktif
        H = W = 0  # diisi bila appearance aktif (dipakai score() di blok matching)
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
        # ASW: bobot blend per-frame dari tingkat overlap deteksi (paper Eq 10).
        # w_t = sigmoid(N_occ/N_t); N_occ = deteksi dgn IoU > 0.5 thd deteksi lain.
        w_t = self.appearance_w if not self.asw else _asw_weight(det_xyxy)
        matched = set()
        if ious.size:
            if self.appearance is not None:
                embs = [self._track_emb(self.tracks[tid]) for tid in preds]
                clean = [e for e in embs if e is not None]
                if len(clean) != len(embs):
                    raise RuntimeError("tracklet tanpa emb_buf saat appearance aktif")
                e_track = np.stack(clean)
                sims = self.appearance.score(W, H, pred_tlwh, dets_tlwh, e_track, e_det)
                gate_mat = w_t * sims + (1 - w_t) * ious
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
                    tr["emb_buf"].append(e_det[j])   # CMOH: simpan K embedding terakhir (deque auto-evict)
                matched.add(j)
        # deteksi baru
        for j in range(n_dets):
            if j in matched:
                continue
            tid = self.next_id
            self.next_id += 1
            self.tracks[tid] = dict(kf=_KalmanBox(dets_tlwh[j]), age=0, hits=1,
                                    ema_box=None,
                                    emb_buf=deque([e_det[j]], maxlen=self.cmoh_k)
                                    if self.appearance is not None else deque(maxlen=self.cmoh_k))
        # keluarkan track mati
        dead = [tid for tid, tr in self.tracks.items() if tr["age"] > self.max_age]
        for tid in dead:
            del self.tracks[tid]
        out = []
        for tid, tr in self.tracks.items():
            if tr["hits"] < self.min_hits:
                continue
            if tr["age"] > self.emit_age:
                # OCM + emit-gap: track tetep dipakai untuk matching, tapi box
                # hantu (gap > emit_age) tidak di-emit -> bukan FP di TrackEval.
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
    # semua box output harus 1-D (4,) — regresi bentuk (4,1)/(M,4,1) dari filterpy
    for box, tid in list(out1a) + list(out2a) + list(out1i) + list(out2i):
        assert box.shape == (4,), f"box shape {box.shape}"

    # ---- CMOH: B tertutup 1 frame (oklusi), muncul lagi — ID harus tetap ----
    cmoh_tr = LightTrackTracker(min_hits=1, appearance=FakeAppearance())
    o1 = cmoh_tr.update(np.array([[10., 10., 20., 50.], [300., 10., 20., 50.]]),
                        np.array([0.9, 0.9]), frame_bgr=zero)
    cmoh_tr.update(np.array([[11., 10., 20., 50.], [301., 10., 20., 50.]]),
                   np.array([0.9, 0.9]), frame_bgr=zero)
    cmoh_tr.update(np.array([[12., 10., 20., 50.]]), np.array([0.9]), frame_bgr=zero)  # B tertutup
    o4 = cmoh_tr.update(np.array([[13., 10., 20., 50.], [302., 10., 20., 50.]]),
                        np.array([0.9, 0.9]), frame_bgr=zero)
    assert id_at(o4, 302, 10) == id_at(o1, 300, 10), "CMOH: ID B harus bertahan setelah oklusi 1 frame"
    for tid, tr in cmoh_tr.tracks.items():
        assert len(tr["emb_buf"]) <= cmoh_tr.cmoh_k, f"buffer melebihi K={cmoh_tr.cmoh_k}"

    # ---- OCM-light: oklusi 4 frame -> posisi track DI-FREEZE (no drift), ID tetap ----
    occ_tr = LightTrackTracker(min_hits=1, appearance=FakeAppearance(), max_age=10)
    oc1 = occ_tr.update(np.array([[10., 10., 20., 50.], [300., 10., 20., 50.]]),
                        np.array([0.9, 0.9]), frame_bgr=zero)
    for t in range(4):  # B hilang 4 frame, A jalan sendiri; tidak ada deteksi B
        occ_tr.update(np.array([[10. + t, 10., 20., 50.]]), np.array([0.9]), frame_bgr=zero)
    # cek B DI-FREEZE: posisi prediksi tidak melebar drastis dari posisi oklusi
    tb = occ_tr.tracks[id_at(oc1, 300, 10)]
    frozen = _xyah_to_tlwh(tb["kf"].xyah)
    assert abs(frozen[0] - 301.0) < 30.0, f"OCM-freeze gagal: B drift ke x={frozen[0]:.1f}"
    oc6 = occ_tr.update(np.array([[10., 10., 20., 50.], [302., 10., 20., 50.]]),
                        np.array([0.9, 0.9]), frame_bgr=zero)
    assert id_at(oc6, 302, 10) == id_at(oc1, 300, 10), "OCM: ID B harus bertahan setelah oklusi 4 frame"
    # ---- ASW: w_t naik saat frame penuh overlap, netral saat sepi ----
    assert abs(_asw_weight(np.zeros((0, 4))) - 0.5) < 1e-9
    sep = np.array([[10., 10., 40., 100.], [300., 10., 40., 100.], [600., 10., 40., 100.]])
    occ = np.array([[10., 10., 40., 100.], [15., 15., 40., 100.], [20., 20., 40., 100.]])
    w_sep = _asw_weight(sep)
    w_occ = _asw_weight(occ)
    assert w_occ > w_sep > 0.5 - 1e-9, f"ASW salah: w_sep={w_sep:.3f} w_occ={w_occ:.3f}"
    print("demo OK (ioU-only + appearance + CMOH + OCM-light + ASW)")


if __name__ == "__main__":
    _demo()
