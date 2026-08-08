"""LightTrack-ReID-inspired (Phase 3) — TBSS: compact similarity scorer (v2).

v2 (fix TBSS collapse, fold-1 baseline BCEacc~0.5):
  - Input RINGKAS 6-d, bukan 73-d: [IoU(1), cos(e_a,e_p)(1), bbox-diff(4)].
    Alasan: 64/73 dim input lama adalah embedding L2-normalized -> informasi
    utama (cosinus) tenggelam oleh dimensi; di 6-d sinyal diskriminatif
    (cos + IoU + geometri) langsung terlihat dan berskala [0,1]/[-1,1].
  - "Transformer"-nya diganti MLP 2-layer + LayerNorm. Di arsitektur lama
    TransformerEncoderLayer dipakai dengan S=1 token -> attention adalah
    no-op (satu token tidak punya siapa-siapa utk di-attend), jadi kapasitas
    model nyatanya cuma proyeksi+FFN. MLP eksplisit memberi kapasitas yang
    sama tanpa overhead yang menyesatkan.
  - Output: sigmoid -> s in [0,1] (kontrak sama dgn v1).

Input (B,6):
    x = [iou, cos, dx_c, dy_c, dw, dh]   (bbox termormalisasi [0,1] utk dx/dw)

Kontrak:
    model = SimilarityModel(d_model=64)
    s = model(x)   # x (B,6) float -> (B,1) float [0,1]
"""
import torch
import torch.nn as nn


class SimilarityModel(nn.Module):
    """TBSS scorer v2: MLP 2-layer + GELU + LayerNorm -> sigmoid."""

    def __init__(self, in_dim=6, d_model=64):
        super().__init__()
        # FFN 2 layer (opsi perbaikan dari hasil diagnosa collapse).
        self.net = nn.Sequential(
            nn.Linear(in_dim, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, 1),
        )

    def forward(self, x):
        # x: (B, in_dim) -> (B, 1)
        return torch.sigmoid(self.net(x))


def _demo():
    torch.manual_seed(0)
    m = SimilarityModel().eval()
    x = torch.randn(4, 6)
    with torch.inference_mode():
        s = m(x)
    assert s.shape == (4, 1), s.shape
    assert bool((s >= 0.0).all() and (s <= 1.0).all()), s
    # input makin mirip (embed cos=+1, IoU=1, bbox diff=0) -> skor naik
    x_pair = torch.tensor([[1.0, 1.0, 0.0, 0.0, 0.0, 0.0]])       # identik
    x_far = torch.tensor([[0.0, -1.0, 0.5, 0.5, 0.5, 0.5]])        # jauh
    s_pair, s_far = m(x_pair), m(x_far)
    assert float(s_pair) > float(s_far), (s_pair, s_far)
    print("demo OK", {"shape": tuple(s.shape), "s_pair": round(float(s_pair), 3),
                      "s_far": round(float(s_far), 3)})


if __name__ == "__main__":
    _demo()