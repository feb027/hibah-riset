"""Deep-OC-SORT Tracker (Maggiolino et al., 2023).

Implementasi mandiri (self-contained) dari Deep-OC-SORT:
- Observation-Centric Kalman Filter dengan momentum kecepatan dan arah (VDC).
- Dynamic Appearance Cost Matrix (ACM) berbasis Deep Learning visual embedding.
- Adaptive Weighting (AW) berbasis margin kemiripan.
- Two-stage association: Round 1 (Motion + Appearance) + Round 2 (OCR recovery).
- EMA Appearance update per tracklet.

Didesain fleksibel: dapat menerima embedder ONNX (DirectML/CPU) atau PyTorch
tanpa memerlukan dependensi CUDA khusus (torchreid/fastreid C++ build).
"""
import numpy as np
from filterpy.kalman import KalmanFilter
from scipy.optimize import linear_sum_assignment


def iou_batch(bboxes1, bboxes2):
    """Computes IoU matrix (N, M) between bboxes1 (N, 4) and bboxes2 (M, 4) in xyxy format."""
    b2 = np.expand_dims(bboxes2, 0)
    b1 = np.expand_dims(bboxes1, 1)

    xx1 = np.maximum(b1[..., 0], b2[..., 0])
    yy1 = np.maximum(b1[..., 1], b2[..., 1])
    xx2 = np.minimum(b1[..., 2], b2[..., 2])
    yy2 = np.minimum(b1[..., 3], b2[..., 3])
    w = np.maximum(0.0, xx2 - xx1)
    h = np.maximum(0.0, yy2 - yy1)
    wh = w * h
    area1 = (b1[..., 2] - b1[..., 0]) * (b1[..., 3] - b1[..., 1])
    area2 = (b2[..., 2] - b2[..., 0]) * (b2[..., 3] - b2[..., 1])
    union = area1 + area2 - wh
    return np.where(union > 0, wh / np.maximum(union, 1e-9), 0.0)


def speed_direction_batch(dets, tracks):
    """Menghitung arah kecepatan antara deteksi saat ini dan observasi tracklet sebelumnya."""
    tracks = tracks[..., np.newaxis]
    CX1 = (dets[:, 0] + dets[:, 2]) / 2.0
    CY1 = (dets[:, 1] + dets[:, 3]) / 2.0
    CX2 = (tracks[:, 0] + tracks[:, 2]) / 2.0
    CY2 = (tracks[:, 1] + tracks[:, 3]) / 2.0
    dx = CX1 - CX2
    dy = CY1 - CY2
    norm = np.sqrt(dx**2 + dy**2) + 1e-6
    return dy / norm, dx / norm  # (num_track, num_det)


def compute_aw_matrix(emb_cost, w_assoc_emb=0.5, max_diff=0.5):
    """Adaptive Weighting (AW) Deep-OC-SORT: meningkatkan bobot penampilan jika terdapat margin tinggi."""
    w_emb = np.full_like(emb_cost, w_assoc_emb, dtype=np.float32)
    w_bonus = np.zeros_like(emb_cost, dtype=np.float32)

    if emb_cost.shape[1] >= 2:
        for idx in range(emb_cost.shape[0]):
            inds = np.argsort(-emb_cost[idx])
            row_weight = min(float(emb_cost[idx, inds[0]] - emb_cost[idx, inds[1]]), max_diff)
            w_bonus[idx] += row_weight / 2.0

    if emb_cost.shape[0] >= 2:
        for idj in range(emb_cost.shape[1]):
            inds = np.argsort(-emb_cost[:, idj])
            col_weight = min(float(emb_cost[inds[0], idj] - emb_cost[inds[1], idj]), max_diff)
            w_bonus[:, idj] += col_weight / 2.0

    return w_emb + w_bonus


def linear_assignment(cost_matrix):
    r, c = linear_sum_assignment(cost_matrix)
    return np.array(list(zip(r, c)), dtype=int) if len(r) > 0 else np.empty((0, 2), dtype=int)


def associate_deep_ocsort(detections, trackers, det_embs, trk_embs, iou_threshold,
                          velocities, previous_obs, vdc_weight=0.2, w_assoc_emb=0.5,
                          aw_off=False, aw_param=0.5):
    """Tahap asosiasi gabungan: IoU + Velocity Direction Cost (VDC) + Appearance Cost (ACM)."""
    if len(trackers) == 0 or len(detections) == 0:
        return (
            np.empty((0, 2), dtype=int),
            np.arange(len(detections)),
            np.arange(len(trackers)),
        )

    # 1. Velocity Direction Consistency (VDC)
    Y, X = speed_direction_batch(detections, previous_obs)
    inertia_Y, inertia_X = velocities[:, 0], velocities[:, 1]
    inertia_Y = np.repeat(inertia_Y[:, np.newaxis], Y.shape[1], axis=1)
    inertia_X = np.repeat(inertia_X[:, np.newaxis], X.shape[1], axis=1)
    diff_angle_cos = np.clip(inertia_X * X + inertia_Y * Y, -1.0, 1.0)
    diff_angle = (np.pi / 2.0 - np.abs(np.arccos(diff_angle_cos))) / np.pi

    valid_mask = np.ones(previous_obs.shape[0], dtype=np.float32)
    valid_mask[np.where(previous_obs[:, 4] < 0)] = 0.0
    valid_mask = np.repeat(valid_mask[:, np.newaxis], X.shape[1], axis=1)

    scores = np.repeat(detections[:, -1][:, np.newaxis], trackers.shape[0], axis=1)
    angle_diff_cost = (valid_mask * diff_angle).T * vdc_weight * scores

    # 2. IoU Matrix
    iou_matrix = iou_batch(detections, trackers)

    # 3. Dynamic Appearance Cost (ACM)
    if det_embs is not None and trk_embs is not None and len(det_embs) > 0 and len(trk_embs) > 0:
        emb_cost = np.clip(det_embs @ trk_embs.T, 0.0, 1.0)
        if not aw_off:
            w_mat = compute_aw_matrix(emb_cost, w_assoc_emb, aw_param)
            emb_cost *= w_mat
        else:
            emb_cost *= w_assoc_emb
    else:
        emb_cost = np.zeros_like(iou_matrix)

    # Combined Cost Matrix
    final_cost = -(iou_matrix + angle_diff_cost + emb_cost)
    matched_indices = linear_assignment(final_cost)

    unmatched_detections = []
    for d in range(len(detections)):
        if d not in matched_indices[:, 0]:
            unmatched_detections.append(d)

    unmatched_trackers = []
    for t in range(len(trackers)):
        if t not in matched_indices[:, 1]:
            unmatched_trackers.append(t)

    # Filter out matched with low IoU
    matches = []
    for m in matched_indices:
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        else:
            matches.append(m.reshape(1, 2))

    matches_arr = np.concatenate(matches, axis=0) if len(matches) > 0 else np.empty((0, 2), dtype=int)
    unmatched_dets_arr = np.unique(unmatched_detections).astype(int) if len(unmatched_detections) > 0 else np.empty(0, dtype=int)
    unmatched_trks_arr = np.unique(unmatched_trackers).astype(int) if len(unmatched_trackers) > 0 else np.empty(0, dtype=int)
    return matches_arr, unmatched_dets_arr, unmatched_trks_arr


class KalmanBoxTracker(object):
    """Kalman tracker xyxy dengan observasi trajectory dan EMA embedding."""
    count = 0

    def __init__(self, bbox, delta_t=3, emb=None, alpha=0.95):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([
            [1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
        ])
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ])
        self.kf.R[2:, 2:] *= 10.0
        self.kf.P[4:, 4:] *= 1000.0
        self.kf.P *= 10.0
        self.kf.Q[-1, -1] *= 0.01
        self.kf.Q[4:, 4:] *= 0.01

        # State: [x_center, y_center, area, aspect_ratio]
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        self.kf.x[:4] = np.array([[bbox[0] + w / 2.0], [bbox[1] + h / 2.0], [w * h], [w / max(h, 1e-6)]])

        self.time_since_update = 0
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.hits = 0
        self.hit_streak = 0
        self.age = 0

        self.last_observation = np.array([bbox[0], bbox[1], bbox[2], bbox[3], bbox[4] if len(bbox) > 4 else 1.0])
        self.observations = {self.age: self.last_observation}
        self.velocity = np.array([0.0, 0.0])
        self.delta_t = delta_t

        self.emb = emb
        self.alpha = alpha

    def update(self, bbox):
        if bbox is not None:
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            z = np.array([[bbox[0] + w / 2.0], [bbox[1] + h / 2.0], [w * h], [w / max(h, 1e-6)]])
            self.kf.update(z)

            # Hitung velocity direction
            if len(self.observations) > 0:
                dt = min(self.delta_t, self.age)
                if (self.age - dt) in self.observations:
                    prev = self.observations[self.age - dt]
                    cx_prev = (prev[0] + prev[2]) / 2.0
                    cy_prev = (prev[1] + prev[3]) / 2.0
                    cx_cur = bbox[0] + w / 2.0
                    cy_cur = bbox[1] + h / 2.0
                    dx = cx_cur - cx_prev
                    dy = cy_cur - cy_prev
                    norm = np.sqrt(dx**2 + dy**2) + 1e-6
                    self.velocity = np.array([dy / norm, dx / norm])

            self.time_since_update = 0
            self.hits += 1
            self.hit_streak += 1
            self.last_observation = np.array([bbox[0], bbox[1], bbox[2], bbox[3], bbox[4] if len(bbox) > 4 else 1.0])
            self.observations[self.age] = self.last_observation
        else:
            self.kf.update(None)

    def update_emb(self, emb, alpha=None):
        if emb is not None:
            a = self.alpha if alpha is None else alpha
            if self.emb is None:
                self.emb = emb.copy()
            else:
                self.emb = a * self.emb + (1.0 - a) * emb
                norm = np.linalg.norm(self.emb)
                if norm > 1e-6:
                    self.emb = self.emb / norm

    def predict(self):
        x_flat = np.asarray(self.kf.x).reshape(-1)
        if (x_flat[6] + x_flat[2]) <= 0:
            self.kf.x[6] = 0.0
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        return self.get_state()

    def get_state(self):
        """Mengembalikan kotak estimasi dalam format xyxy."""
        x_flat = np.asarray(self.kf.x).reshape(-1)
        w = np.sqrt(max(0.0, float(x_flat[2] * x_flat[3])))
        h = float(x_flat[2]) / max(w, 1e-6)
        x = float(x_flat[0])
        y = float(x_flat[1])
        return np.array([x - w / 2.0, y - h / 2.0, x + w / 2.0, y + h / 2.0])


class DeepOCSortTracker(object):
    """Deep-OC-SORT: Multi-Object Tracker dengan Re-ID Deep Learning & Koreksi Observasi."""

    def __init__(
        self,
        det_thresh=0.3,
        max_age=30,
        min_hits=3,
        iou_threshold=0.3,
        delta_t=3,
        inertia=0.2,
        w_association_emb=0.5,
        alpha_fixed_emb=0.95,
        aw_param=0.5,
        appearance=None,
    ):
        self.det_thresh = det_thresh
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.delta_t = delta_t
        self.inertia = inertia
        self.w_association_emb = w_association_emb
        self.alpha_fixed_emb = alpha_fixed_emb
        self.aw_param = aw_param
        self.appearance = appearance
        self.trackers = []
        self.frame_count = 0
        KalmanBoxTracker.count = 0

    def update(self, dets_xyxy, scores, frame_bgr=None):
        """Update tracker state per frame.
        
        Args:
            dets_xyxy: (N, 4) numpy array [x1, y1, x2, y2]
            scores: (N,) numpy array confidence scores
            frame_bgr: OpenCV frame BGR untuk ekstraksi visual embedding
        
        Returns:
            List of (tlwh_box, track_id)
        """
        self.frame_count += 1
        dets_xyxy = np.asarray(dets_xyxy, dtype=float).reshape(-1, 4)
        scores = np.asarray(scores, dtype=float).reshape(-1)

        valid_mask = scores >= self.det_thresh
        dets_xyxy = dets_xyxy[valid_mask]
        scores = scores[valid_mask]
        n_dets = len(dets_xyxy)

        if n_dets > 0:
            dets = np.column_stack([dets_xyxy, scores])
        else:
            dets = np.empty((0, 5), dtype=float)

        # 1. Ekstraksi visual embedding (Deep Learning Re-ID)
        dets_embs = None
        if self.appearance is not None and n_dets > 0 and frame_bgr is not None:
            tlwh = np.column_stack([
                dets_xyxy[:, 0],
                dets_xyxy[:, 1],
                dets_xyxy[:, 2] - dets_xyxy[:, 0],
                dets_xyxy[:, 3] - dets_xyxy[:, 1]
            ])
            dets_embs = self.appearance.embed(frame_bgr, tlwh)

        af = self.alpha_fixed_emb
        trust = (scores - self.det_thresh) / max(1.0 - self.det_thresh, 1e-6) if n_dets > 0 else np.array([])
        dets_alpha = af + (1.0 - af) * (1.0 - trust) if n_dets > 0 else np.array([])

        # 2. Kalman Predict
        valid_trackers = []
        valid_trks = []
        valid_embs = []
        for trk in self.trackers:
            pos = trk.predict()
            if not np.any(np.isnan(pos)):
                valid_trackers.append(trk)
                valid_trks.append(pos)
                valid_embs.append(trk.emb if trk.emb is not None else np.zeros(32, dtype=np.float32))

        self.trackers = valid_trackers
        trks = np.array(valid_trks, dtype=float) if len(valid_trks) > 0 else np.empty((0, 4), dtype=float)
        trk_embs = np.array(valid_embs, dtype=np.float32) if len(valid_embs) > 0 else np.empty((0, 32), dtype=np.float32)
        velocities = np.array([trk.velocity for trk in self.trackers], dtype=float) if len(self.trackers) > 0 else np.empty((0, 2))
        last_boxes = np.array([trk.last_observation for trk in self.trackers], dtype=float) if len(self.trackers) > 0 else np.empty((0, 5))

        k_obs = []
        for trk in self.trackers:
            dt = min(self.delta_t, trk.age)
            if (trk.age - dt) in trk.observations:
                k_obs.append(trk.observations[trk.age - dt])
            elif len(trk.observations) > 0:
                max_k = max(trk.observations.keys())
                k_obs.append(trk.observations[max_k])
            else:
                k_obs.append(np.array([-1, -1, -1, -1, -1]))
        previous_obs = np.array(k_obs, dtype=float) if len(k_obs) > 0 else np.empty((0, 5))

        # 3. Round 1 Asosiasi
        matched, unmatched_dets, unmatched_trks = associate_deep_ocsort(
            dets, trks, dets_embs, trk_embs, self.iou_threshold,
            velocities, previous_obs, self.inertia, self.w_association_emb,
            aw_off=False, aw_param=self.aw_param
        )

        for m in matched:
            d_idx, t_idx = m[0], m[1]
            self.trackers[t_idx].update(dets[d_idx])
            if dets_embs is not None:
                self.trackers[t_idx].update_emb(dets_embs[d_idx], alpha=dets_alpha[d_idx])

        # 4. Round 2 OCR (Observation-Centric Recovery)
        if len(unmatched_dets) > 0 and len(unmatched_trks) > 0:
            left_dets = dets[unmatched_dets]
            left_trks = last_boxes[unmatched_trks][:, :4]
            iou_left = iou_batch(left_dets, left_trks)
            if iou_left.size > 0 and iou_left.max() > self.iou_threshold:
                rematched = linear_assignment(-iou_left)
                rem_dets, rem_trks = [], []
                for m in rematched:
                    d_i, t_i = unmatched_dets[m[0]], unmatched_trks[m[1]]
                    if iou_left[m[0], m[1]] >= self.iou_threshold:
                        self.trackers[t_i].update(dets[d_i])
                        if dets_embs is not None:
                            self.trackers[t_i].update_emb(dets_embs[d_i], alpha=dets_alpha[d_i])
                        rem_dets.append(d_i)
                        rem_trks.append(t_i)
                unmatched_dets = np.setdiff1d(unmatched_dets, np.array(rem_dets, dtype=int))
                unmatched_trks = np.setdiff1d(unmatched_trks, np.array(rem_trks, dtype=int))

        for t_idx in unmatched_trks:
            self.trackers[t_idx].update(None)

        # 5. Inisialisasi tracklet baru
        for d_idx in unmatched_dets:
            emb_i = dets_embs[d_idx] if dets_embs is not None else None
            alpha_i = dets_alpha[d_idx] if len(dets_alpha) > d_idx else 0.95
            trk = KalmanBoxTracker(dets[d_idx], delta_t=self.delta_t, emb=emb_i, alpha=alpha_i)
            self.trackers.append(trk)

        # 6. Filter output aktif
        results = []
        i = len(self.trackers)
        for trk in reversed(self.trackers):
            i -= 1
            if trk.time_since_update > self.max_age:
                self.trackers.pop(i)
                continue

            if trk.time_since_update <= 1 and (trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                box_xyxy = trk.last_observation[:4] if trk.time_since_update == 0 else trk.get_state()
                x1, y1, x2, y2 = box_xyxy
                tlwh = np.array([x1, y1, max(0.0, x2 - x1), max(0.0, y2 - y1)])
                results.append((tlwh, trk.id + 1))

        return results
