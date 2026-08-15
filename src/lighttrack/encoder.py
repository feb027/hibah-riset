"""LightTrack-ReID-inspired (Phase 2) — LAE encoder: MobileNetV3-Small -> 32-d embedding.

Jalur inference untuk bagaimana sebuah crop orang (kotak deteksi) diubah menjadi
vektor penampilan (appearance) 32-d yang L2-normalised, bisa digunakan nantinya di
Phase 3 oleh TBSS agar ID orang tetap nempel walau objek saling menutupi.

Modul ini TORCH-ONLY dan berdiri sendiri: tracker CPU Phase 1 (tracker.py) TIDAK
mengimpornya, jadi mode USE_REID=false tetap jalan tanpa torch.

Kontrak:
    model = LAE('cpu' | 'cuda')
    emb = model.embed_frame(bgr_frame, boxes_tlwh)   # (N, 32) numpy, L2-normalised
    :returns: dua crop orang sama punya cosine lebih besar dari dua crop orang
              berbeda. Verifikasi LANGSUNG via demo()/self-test di bawah.
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.models as tv_models

# py3.8 env kampus: TIDAK pakai list[int]/X | None (PEP 585/604).

EMBEDED_DIM = 32          # dimensi vektor output
CROP_SIZE = 224           # input LAE
FC_IN = 576               # channel fitur akhir MobileNetV3-Small
_IMAGENET_MEAN = (0.485, 0.456, 0.406)
_IMAGENET_STD = (0.229, 0.224, 0.225)


def _load_backbone():
    """MobileNetV3-Small pretrained, kompatibel torchvision 0.13-0.15+."""
    # torchvision >=0.13: weights=; <0.13: pretrained=
    try:
        from torchvision.models import MobileNet_V3_Small_Weights as W
        return torchvision.models.mobilenet_v3_small(weights=W.DEFAULT)
    except Exception:  # pragma: no cover - fallback API lama
        return torchvision.models.mobilenet_v3_small(pretrained=True)


class LAE(nn.Module):
    """LAE (light appearance extractor): backbone -> AvgPool -> Linear(576->32) -> L2-norm."""

    def __init__(self):
        super().__init__()
        self.backbone = _load_backbone()
        self.backbone.classifier = nn.Identity()   # buang head klasifikasi ImageNet
        self.fc = nn.Linear(FC_IN, EMBEDED_DIM, bias=False)

    def forward(self, x):
        # x: (N,3,CROP_SIZE,CROP_SIZE) float, ter-normalisasi ImageNet (RGB).
        f = self.backbone(x)                       # (N, 576, 1, 1) setelah avgpool internal
        e = self.fc(f.reshape(f.shape[0], -1))     # (N, 32)
        return F.normalize(e, p=2, dim=1)


class EmbeddingComputer:
    """Jalur inference: crop deteksi -> 224 -> normalize -> LAE -> (N,32)."""

    def __init__(self, model=None, device=None, size=CROP_SIZE, max_side=0):
        self.device = device or (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
        self.model = model or LAE()
        self.model.to(self.device).eval()
        self.size = size
        self._mean = torch.tensor(_IMAGENET_MEAN, dtype=torch.float32)
        self._std = torch.tensor(_IMAGENET_STD, dtype=torch.float32)

    def embed_frame(self, frame_bgr, boxes_tlwh):
        """frame_bgr: numpy (H,W,3) uint8 BGR; boxes_tlwh: iterable (x,y,w,h). -> (N,32) numpy.

        Crop+resize+normalize di-GPU sekaligus (batch). Resize BOX (= area averaging,
        setara cv2 INTER_AREA yang dipakai train) supaya numerik konsisten train↔inference.
        """
        if len(boxes_tlwh) == 0:
            return np.zeros((0, EMBEDED_DIM), dtype=np.float32)
        x = self._crop_batch_torch(frame_bgr, np.asarray(boxes_tlwh, dtype=float))
        with torch.inference_mode():
            e = self.model(x).cpu().numpy()
        return e.astype(np.float32)

    def _crop_batch_torch(self, frame_bgr, boxes_tlwh):
        """Semua crop diresize ke (size,size) di GPU.

        Frame dikonversi sekali ke float RGB dinormalisasi (H,W,3) di device; tiap box
        di-slice view lalu resize via F.interpolate(mode='area') = area averaging,
        setara cv2 INTER_AREA yang dipakai train. Border behavior sama persis dgn
        jalur cv2 (clamp ke frame, tanpa pad). Opsional: nggak ada.
        """
        rgb = torch.from_numpy(frame_bgr[..., ::-1].astype(np.float32) / np.float32(255.0))
        rgb = (rgb - self._mean) / self._std    # (H,W,3) float32, masih di CPU
        # pindah ke device; slicing per box = view, tidak menyalin frame
        rgb = rgb.to(self.device)
        hh, ww = frame_bgr.shape[:2]
        outs = []
        for x, y, w, h in boxes_tlwh:
            x0 = int(round(x)); y0 = int(round(y))
            x1 = min(ww, x0 + max(1, int(round(w)))); y1 = min(hh, y0 + max(1, int(round(h))))
            x0 = max(0, x0); y0 = max(0, y0)
            if x1 <= x0 or y1 <= y0:
                continue
            c = rgb[y0:y1, x0:x1].permute(2, 0, 1).unsqueeze(0)   # (1,3,h,w) [H,W] urut benar
            c = c.contiguous()
            outs.append(F.interpolate(c, size=(self.size, self.size), mode="area"))
        if not outs:
            return torch.zeros((0, 3, self.size, self.size), device=self.device)
        return torch.cat(outs, dim=0)


def _demo():
    """Self-check: embedding crop SAMA orang > cosine crop BEDA orang."""
    try:
        torch.manual_seed(0)
        emb = EmbeddingComputer()
    except Exception as e:  # pragma: no cover
        print(f"SKIP: model tidak bisa dimuat di mesin ini ({e!r})")
        return
    import cv2
    # 3 bingkai tiruan: 2 berisi satu orang (kemeja merata), 1 berisi orang lain.
    def make(img_bgr, x, y, w, h):
        box = [[x, y, w, h]]
        return emb.embed_frame(img_bgr, box)[0]
    oranye = np.full((180, 320, 3), 0, np.uint8)
    biru = np.full((180, 320, 3), 0, np.uint8)
    oranye[:, :, ...] = [0, 90, 170]      # BGR oranye
    biru[:, :, ...] = [170, 0, 0]          # BGR biru
    e_sama = make(oranye, 40, 40, 80, 120)
    e_sama2 = make(oranye, 140, 30, 80, 120)   # crop sama, bergeser/tumpang tindih
    e_beda = make(biru, 40, 40, 80, 120)

    from numpy.linalg import norm
    sim_same = float(np.dot(e_sama, e_sama2) / (norm(e_sama) * norm(e_sama2)))
    sim_diff = float(np.dot(e_sama, e_beda) / (norm(e_sama) * norm(e_beda)))
    print(f"cosine same-person={sim_same:.3f} diff-person={sim_diff:.3f}")
    assert sim_same > sim_diff, f"kemiripan salah: sama {sim_same} <= beda {sim_diff}"
    assert e_sama.shape == (EMBEDED_DIM,), e_sama.shape
    # L2-norm output == 1
    assert abs(norm(e_sama) - 1.0) < 1e-3
    print("demo OK")


if __name__ == "__main__":
    _demo()