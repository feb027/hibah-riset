"""LightTrack appearance via ONNX Runtime — tanpa torch di runtime.

Pengganti drop-in untuk `TbssAppearance` (phase4.py) pada mesin tanpa torch-GPU
(Windows + RX6600: torch-CUDA tidak ada, ROCm tidak ada di Windows). Deteksi YOLO
juga sudah lewat onnx, jadi seluruh pipeline realtime tidak menyentuh torch.

Kontrak identik dengan phase4.py:
    embed(frame_bgr, dets_tlwh) -> (N,32) float32 L2-unit
    score(W, H, track_tlwh, det_tlwh, e_track, e_det) -> (M,N) [0,1]

File model dibutuhkan:
    lae.onnx  : (N,3,224,224) float32 normalize ImageNet (RGB) -> (N,32) L2-norm
    tbss.onnx : (B,6) [iou,cos,dx_c,dy_c,dw,dh] -> (B,1)

Crop+resize memakai cv2 INTER_AREA (sama persis dengan training dataset.py:126),
fallback numerik yang konsisten. Catatan ceiling: loop cv2 per box berjalan di CPU
(~25 ms di frame padat) — jalan, tapi bukan 49 FPS kampus. Upgrade path bila perlu:
resize di-GPU via DML tidak tersedia untuk loop dinamis; cukup render offline.

Provider: DmlExecutionProvider (RX6600/RDNA2) kalau onnxruntime-directml terpasang,
jatuh ke CPUExecutionProvider kalau tidak.
"""
import os

import cv2
import numpy as np

_IMAGENET_MEAN = (0.485, 0.456, 0.406)
_IMAGENET_STD = (0.229, 0.224, 0.225)
CROP_SIZE = 224
EMBEDED_DIM = 32


def _providers():
    """DML dulu kalau ada, sisanya CPU. Sesuai kemampuan onnxruntime terpasang."""
    import onnxruntime as ort
    avail = ort.get_available_providers()
    order = ["DmlExecutionProvider", "CPUExecutionProvider"]
    chosen = [p for p in order if p in avail]
    print("[phase4_onnx] providers=%s" % chosen, flush=True)
    return chosen


def _to_xyxy_np(tlwh, W, H):
    """Normalisasi box tlwh -> xyxy di [0,1]. Meniru train._to_xyxy (numpy)."""
    x = np.asarray(tlwh, dtype=float)
    x0 = x[:, 0] / W
    y0 = x[:, 1] / H
    x1 = (x[:, 0] + x[:, 2]) / W
    y1 = (x[:, 1] + x[:, 3]) / H
    return np.stack([x0, y0, x1, y1], axis=1)


def _iou_mn_np(ba, bd):
    """IoU matriks (M,N) dari box xyxy normalisasi. Meniru phase4._iou_mn (numpy)."""
    x1 = np.maximum(ba[:, None, 0], bd[None, :, 0])
    y1 = np.maximum(ba[:, None, 1], bd[None, :, 1])
    x2 = np.minimum(ba[:, None, 2], bd[None, :, 2])
    y2 = np.minimum(ba[:, None, 3], bd[None, :, 3])
    inter = np.clip(x2 - x1, 0.0, None) * np.clip(y2 - y1, 0.0, None)
    area_a = (ba[:, 2] - ba[:, 0]) * (ba[:, 3] - ba[:, 1])
    area_b = (bd[:, 2] - bd[:, 0]) * (bd[:, 3] - bd[:, 1])
    union = area_a[:, None] + area_b[None, :] - inter
    return np.where(union > 0, inter / (union + 1e-9), 0.0)


class TbssAppearanceOnnx:
    """Appearance LAE+TBSS via onnxruntime. Kontrak sama dgn TbssAppearance."""

    def __init__(self, model_dir, use_tbss=True, session_options=None):
        import onnxruntime as ort
        if session_options is None:
            session_options = ort.SessionOptions()
            session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        lae_path = os.path.join(model_dir, "lae.onnx")
        tbss_path = os.path.join(model_dir, "tbss.onnx")
        for f in (lae_path, tbss_path):
            if not os.path.exists(f):
                raise FileNotFoundError("model onnx tidak ada: %s" % f)
        prov = _providers()
        self.lae = ort.InferenceSession(lae_path, session_options, providers=prov)
        self.tbss = None
        if use_tbss:
            self.tbss = ort.InferenceSession(tbss_path, session_options, providers=prov)
        print("[phase4_onnx] lae.onnx + tbss.onnx dimuat dari %s" % model_dir, flush=True)

    def embed(self, frame_bgr, dets_tlwh):
        dets = np.asarray(dets_tlwh, dtype=float)
        if len(dets) == 0:
            return np.zeros((0, EMBEDED_DIM), dtype=np.float32)
        crops = self._crop(frame_bgr, dets)          # (N,224,224,3) uint8 BGR
        x = self._normalize(crops)                   # (N,3,224,224) float32 RGB
        e = self.lae.run(None, {"x": x})[0]
        # LAE output sudah L2-normalized (F.normalize di graph); jaga numerik lama
        return np.asarray(e, dtype=np.float32)

    def score(self, W, H, track_tlwh, det_tlwh, e_track, e_det):
        M, N = len(track_tlwh), len(det_tlwh)
        if M == 0 or N == 0:
            return np.zeros((M, N), dtype=np.float32)
        ea = np.asarray(e_track, dtype=np.float32)
        ed = np.asarray(e_det, dtype=np.float32)
        cos = (ea[:, None, :] * ed[None, :, :]).sum(-1)          # (M,N)
        if self.tbss is None:
            return np.clip(cos, 0.0, 1.0).astype(np.float32)
        ba = _to_xyxy_np(np.asarray(track_tlwh, dtype=float), W, H)
        bp = _to_xyxy_np(np.asarray(det_tlwh, dtype=float), W, H)
        iou = _iou_mn_np(ba, bp)                                 # (M,N)
        diff = ba[:, None, :4] - bp[None, :, :4]                 # (M,N,4)
        xt = np.concatenate([iou[..., None], cos[..., None], diff], axis=-1)
        xt = xt.reshape(M * N, 6).astype(np.float32)             # (M*N,6)
        s = self.tbss.run(None, {"x": xt})[0].reshape(M, N)
        return np.asarray(s, dtype=np.float32)

    def _crop(self, frame_bgr, boxes_tlwh):
        hh, ww = frame_bgr.shape[:2]
        outs = []
        for x, y, w, h in boxes_tlwh:
            x0 = max(0, int(round(x)))
            y0 = max(0, int(round(y)))
            x1 = min(ww, x0 + max(1, int(round(w))))
            y1 = min(hh, y0 + max(1, int(round(h))))
            if x1 <= x0 or y1 <= y0:
                continue
            c = frame_bgr[y0:y1, x0:x1]
            outs.append(cv2.resize(c, (CROP_SIZE, CROP_SIZE), interpolation=cv2.INTER_AREA))
        if not outs:
            return np.zeros((0, CROP_SIZE, CROP_SIZE, 3), dtype=np.uint8)
        return np.stack(outs)

    def _normalize(self, crops):
        rgb = crops[..., ::-1].astype(np.float32) / np.float32(255.0)   # (N,H,W,3) RGB
        rgb = (rgb - np.array(_IMAGENET_MEAN, dtype=np.float32)) \
            / np.array(_IMAGENET_STD, dtype=np.float32)
        return rgb.transpose(0, 3, 1, 2).astype(np.float32)
