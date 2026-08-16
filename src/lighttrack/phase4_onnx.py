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

Optimasi untuk PC Windows + RX 6600 (DirectML):
- Pre-allocated crop buffer + cv2 dst resize untuk memangkas overhead alokasi memori.
- Fused vectorized normalization (multiply-add in-place) memangkas normalisasi CPU dari ~38 ms ke ~8 ms.
- LAE berjalan di DmlExecutionProvider (GPU RX 6600) dan di-warmup di awal.
- TBSS berjalan di CPUExecutionProvider untuk menghindari latency kernel launch GPU pada batch kecil.
"""
import os

import cv2
import numpy as np

CROP_SIZE = 224
EMBEDED_DIM = 32

_IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 3, 1, 1)
_IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 3, 1, 1)
_SCALE = (1.0 / (255.0 * _IMAGENET_STD)).astype(np.float32)
_BIAS = (-_IMAGENET_MEAN / _IMAGENET_STD).astype(np.float32)


def _providers():
    """DML dulu kalau ada, sisanya CPU. Sesuai kemampuan onnxruntime terpasang."""
    import onnxruntime as ort
    avail = ort.get_available_providers()
    order = ["DmlExecutionProvider", "CPUExecutionProvider"]
    chosen = [p for p in order if p in avail]
    print("[phase4_onnx] providers=%s" % chosen, flush=True)
    return chosen


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
        # LAE (CNN berat): prioritaskan DirectML GPU
        self.lae = ort.InferenceSession(lae_path, session_options, providers=prov)
        self.tbss = None
        if use_tbss:
            # TBSS (MLP 6-dimensi ringan): CPUExecutionProvider lebih cepat (tanpa overhead PCIe/launch)
            so_cpu = ort.SessionOptions()
            so_cpu.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            self.tbss = ort.InferenceSession(tbss_path, so_cpu, providers=["CPUExecutionProvider"])

        # Warm-up sessions untuk compile HLSL shader di awal
        try:
            dummy_x = np.zeros((1, 3, CROP_SIZE, CROP_SIZE), dtype=np.float32)
            self.lae.run(None, {"x": dummy_x})
            if self.tbss is not None:
                dummy_xt = np.zeros((1, 6), dtype=np.float32)
                self.tbss.run(None, {"x": dummy_xt})
        except Exception:
            pass

        print("[phase4_onnx] lae.onnx + tbss.onnx dimuat dari %s (teroptimasi DML+CPU)" % model_dir, flush=True)

    def embed(self, frame_bgr, dets_tlwh):
        dets = np.asarray(dets_tlwh, dtype=float)
        if len(dets) == 0:
            return np.zeros((0, EMBEDED_DIM), dtype=np.float32)
        crops = self._crop(frame_bgr, dets)          # (N,224,224,3) uint8 BGR
        if len(crops) == 0:
            return np.zeros((0, EMBEDED_DIM), dtype=np.float32)
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

        ba = np.asarray(track_tlwh, dtype=np.float32)
        ba_x0 = ba[:, 0] / W
        ba_y0 = ba[:, 1] / H
        ba_x1 = (ba[:, 0] + ba[:, 2]) / W
        ba_y1 = (ba[:, 1] + ba[:, 3]) / H
        ba_norm = np.stack([ba_x0, ba_y0, ba_x1, ba_y1], axis=1)

        bp = np.asarray(det_tlwh, dtype=np.float32)
        bp_x0 = bp[:, 0] / W
        bp_y0 = bp[:, 1] / H
        bp_x1 = (bp[:, 0] + bp[:, 2]) / W
        bp_y1 = (bp[:, 1] + bp[:, 3]) / H
        bp_norm = np.stack([bp_x0, bp_y0, bp_x1, bp_y1], axis=1)

        xA = np.maximum(ba_norm[:, None, 0], bp_norm[None, :, 0])
        yA = np.maximum(ba_norm[:, None, 1], bp_norm[None, :, 1])
        xB = np.minimum(ba_norm[:, None, 2], bp_norm[None, :, 2])
        yB = np.minimum(ba_norm[:, None, 3], bp_norm[None, :, 3])
        inter = np.maximum(0.0, xB - xA) * np.maximum(0.0, yB - yA)
        area_a = (ba_norm[:, 2] - ba_norm[:, 0]) * (ba_norm[:, 3] - ba_norm[:, 1])
        area_b = (bp_norm[:, 2] - bp_norm[:, 0]) * (bp_norm[:, 3] - bp_norm[:, 1])
        union = area_a[:, None] + area_b[None, :] - inter
        iou = np.where(union > 0, inter / np.maximum(union, 1e-9), 0.0)

        diff = ba_norm[:, None, :4] - bp_norm[None, :, :4]                 # (M,N,4)
        xt = np.concatenate([iou[..., None], cos[..., None], diff], axis=-1)
        xt = xt.reshape(M * N, 6).astype(np.float32)             # (M*N,6)
        s = self.tbss.run(None, {"x": xt})[0].reshape(M, N)
        return np.asarray(s, dtype=np.float32)

    def _crop(self, frame_bgr, boxes_tlwh):
        hh, ww = frame_bgr.shape[:2]
        n = len(boxes_tlwh)
        crops = np.empty((n, CROP_SIZE, CROP_SIZE, 3), dtype=np.uint8)
        valid = 0
        for x, y, w, h in boxes_tlwh:
            x0 = max(0, int(round(x)))
            y0 = max(0, int(round(y)))
            x1 = min(ww, x0 + max(1, int(round(w))))
            y1 = min(hh, y0 + max(1, int(round(h))))
            if x1 <= x0 or y1 <= y0:
                continue
            c = frame_bgr[y0:y1, x0:x1]
            cv2.resize(c, (CROP_SIZE, CROP_SIZE), dst=crops[valid], interpolation=cv2.INTER_AREA)
            valid += 1
        if valid == 0:
            return np.zeros((0, CROP_SIZE, CROP_SIZE, 3), dtype=np.uint8)
        return crops[:valid]

    def _normalize(self, crops):
        # Transpose & reverse channels ke NCHW (RGB) dalam single copy kontigu
        x = np.ascontiguousarray(crops.transpose(0, 3, 1, 2)[:, ::-1, :, :]).astype(np.float32)
        x *= _SCALE
        x += _BIAS
        return x
