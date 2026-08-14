"""Phase 4 - sambungkan LAE + TBSS ke asosiasi tracker (gelar penampilan).

Memakai fungsi dari train.py (_to_xyxy/_cuda_available) yang SAMA agar normalisasi
box input TBSS identik antara training dan inference. IoU dihitung ulang di sini
dengan rumus yang sama persis (_iou train), bentuk matriks (M,N) karena inference
membandingkan M tracklet vs N deteksi.

Kontrak objek appearance untuk LightTrackTracker:
    embed(frame_bgr, dets_tlwh) -> (N,32) embedding L2-unit numpy
    score(W, H, track_tlwh, det_tlwh, e_track, e_det) -> (M,N) skor [0,1]
"""
import os
import sys

import numpy as np
import torch

_LT_DIR = os.path.dirname(os.path.abspath(__file__))
if _LT_DIR not in sys.path:
    sys.path.insert(0, _LT_DIR)

from train import _to_xyxy, _cuda_available  # noqa: E402
from encoder import EmbeddingComputer  # noqa: E402
from scorer import SimilarityModel  # noqa: E402


def _iou_mn(ba, bd):
    """IoU matriks (M,N) antar dua set box xyxy NORMALISASI [0,1].

    Rumus sama dengan _iou di train.py (pairwise), di sini bentuk matriks.
    IoU invariant terhadap normalisasi, jadi nilai identik dgn IoU box mentah.
    """
    x1 = torch.maximum(ba[:, None, 0], bd[None, :, 0])
    y1 = torch.maximum(ba[:, None, 1], bd[None, :, 1])
    x2 = torch.minimum(ba[:, None, 2], bd[None, :, 2])
    y2 = torch.minimum(ba[:, None, 3], bd[None, :, 3])
    inter = torch.clamp(x2 - x1, min=0.0) * torch.clamp(y2 - y1, min=0.0)
    area_a = (ba[:, 2] - ba[:, 0]) * (ba[:, 3] - ba[:, 1])   # (M,1)
    area_b = (bd[:, 2] - bd[:, 0]) * (bd[:, 3] - bd[:, 1])   # (N,1)
    union = area_a[:, None] + area_b[None, :] - inter
    return torch.where(union > 0, inter / (union + 1e-9), torch.zeros_like(inter))


class TbssAppearance:
    """LAE (embedding) + TBSS v2 (input 6-d: IoU, cosine, bbox-diff) untuk tracker.

    use_tbss=False = mode LAE-only (ablasi "+LAE" paper): sim = cosine murni,
    tidak memuat/memakai TBSS — dipakai untuk ckpt yang TBSS-nya tidak relevan
    (mis. v1 yang scorer-nya gagal) atau untuk titik ablas.
    """

    def __init__(self, ckpt, device=None, use_tbss=True):
        # GPU COMPUTE EXCLUSIVE kampus: probe aman via subprocess (sama seperti train.py)
        self.device = torch.device(device or ("cuda" if _cuda_available() else "cpu"))
        self.emb = EmbeddingComputer(device=self.device)
        ck = torch.load(ckpt, map_location=self.device, weights_only=False)
        self.emb.model.load_state_dict(ck["lae"])
        self.tbss = None
        if use_tbss:
            self.tbss = SimilarityModel().to(self.device).eval()
            self.tbss.load_state_dict(ck["tbss"])
            mode = "LAE+TBSS"
        else:
            mode = "LAE-only"
        print(f"[phase4] ckpt={ckpt} cmode={mode} epoch={ck.get('epoch')} "
              f"best_acc={ck.get('best_acc')} device={self.device}", flush=True)

    def embed(self, frame_bgr, dets_tlwh):
        return self.emb.embed_frame(frame_bgr, np.asarray(dets_tlwh, dtype=float))

    def score(self, W, H, track_tlwh, det_tlwh, e_track, e_det):
        """(M,N) skor [0,1]. TBSS: fitur identik _tbss_x train [IoU, cos, b_a-b_p].
        LAE-only: cosine murni (clipped [0,1])."""
        M, N = len(track_tlwh), len(det_tlwh)
        if M == 0 or N == 0:
            return np.zeros((M, N), dtype=np.float32)
        ea = torch.tensor(e_track, dtype=torch.float32, device=self.device)
        ed_ = torch.tensor(e_det, dtype=torch.float32, device=self.device)
        cos = (ea[:, None, :] * ed_[None, :, :]).sum(-1)     # (M,N) cosine embedding L2-unit
        if self.tbss is None:
            return np.clip(cos.cpu().numpy(), 0.0, 1.0).astype(np.float32)
        b_t = torch.tensor(np.asarray(track_tlwh, dtype=np.float64)).float().to(self.device)
        b_d = torch.tensor(np.asarray(det_tlwh, dtype=np.float64)).float().to(self.device)
        ba = _to_xyxy(b_t, W, H)                       # tracklet -> "anchor" (b_a)
        bp = _to_xyxy(b_d, W, H)                       # deteksi -> "positive" (b_p)
        iou = _iou_mn(ba, bp)                          # (M,N)
        diff = ba[:, None, :4] - bp[None, :, :4]             # (M,N,4) bbox-diff, [-1,1]
        x = torch.cat([iou.unsqueeze(-1), cos.unsqueeze(-1), diff], dim=-1).reshape(M * N, 6)
        with torch.inference_mode():
            s = self.tbss(x).reshape(M, N).cpu().numpy()
        return s.astype(np.float32)
