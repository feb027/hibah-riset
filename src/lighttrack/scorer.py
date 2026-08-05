"""LightTrack-ReID-inspired (Phase 3) — TBSS: Transformer-Based Similarity Scoring.

Menghitung skor kemiripan s ∈ [0,1] antara deteksi (t,i) dan tracklet (t-1,j)
memakai kombinasi bbox, IoU, dan embedding penampilan LAE.

Input vektor 73-d (paper):
    x = [b_t(4), b_{t-1}(4), IoU(1), a_t(32), a_{t-1}(32)]

Arsitektur (paper Eq 6):
    Linear(73 -> d_model) -> TransformerEncoderLayer(d_model, nhead=4) -> Linear -> sigmoid

d_model default 64 — TIDAK disebut paper (input cuma 73-d, kecil sudah cukup);
tunable lewat konstruktor.

Modul TORCH-ONLY pakai tipe py3.8 (tanpa PEP 585: tidak ada list[int]/X | None).
Kontrak:
    model = SimilarityModel(d_model=64)
    s = model(x)              # x (B,73) float -> (B,1) float [0,1]
"""
import torch
import torch.nn as nn


class SimilarityModel(nn.Module):
    """TBSS scorer: 1-layer transformer, 4 heads."""

    def __init__(self, in_dim=73, d_model=64, nhead=4):
        super().__init__()
        self.proj = nn.Linear(in_dim, d_model)
        self.tf = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=False)
        self.head = nn.Linear(d_model, 1)

    def forward(self, x):
        # x: (B, in_dim). TransformerEncoderLayer ekspektasi (S, B, E), S=1 karena
        # tiap sample cuma 1 "token" gabungan bbox+IoU+appearance.
        h = self.proj(x).unsqueeze(0)      # (1, B, d_model)
        h = self.tf(h).squeeze(0)          # (B, d_model)
        return torch.sigmoid(self.head(h))  # (B, 1)


def _demo():
    torch.manual_seed(0)
    m = SimilarityModel().eval()
    x = torch.randn(4, 73)
    with torch.inference_mode():
        s = m(x)
    assert s.shape == (4, 1), s.shape
    assert bool((s >= 0.0).all() and (s <= 1.0).all()), s
    # input makin mirip (vektor sama) -> skor naik (monoton; cek arah mean 2 sampel ekstrim)
    x_same = torch.cat([x[0:1], x[0:1]], dim=1)      # dua deteksi identik
    x_far = torch.cat([torch.zeros(1, 36), torch.ones(1, 37)], dim=1)
    s_same, s_far = m(x_same), m(x_far)
    assert float(s_same) > float(s_far), (s_same, s_far)
    print("demo OK", {"shape": tuple(s.shape), "s_same": round(float(s_same), 3),
                      "s_far": round(float(s_far), 3)})


if __name__ == "__main__":
    _demo()