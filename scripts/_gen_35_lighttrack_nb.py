#!/usr/bin/env python3
"""Generate notebooks/35_s2_lighttrack_train.ipynb — Phase 3 training LAE+TBSS (Fold-1).
Logika training identik dgn src/lighttrack/train.py (hash-for-hash behavior), hanya
progress diganti tqdm.notebook + live plot. py3.8-friendly. Auto-resume dari epoch
terakhir di OUT (cekpt tiap epoch) — aman kalau PC mati: run ulang cell training.
"""
import json, os

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}

def code(src):
    lines = [l + "\n" for l in src.rstrip("\n").split("\n")]
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": lines}

cells = []

cells.append(md(
"""# Phase 3 — Training LAE + TBSS (LightTrack-ReID-inspired, Fold-1)

Melatih dua modul sekaligus (kode paper Eq 13: `L = L_triplet + L_BCE`):
- **LAE** (encoder.py): MobileNetV3-Small → embedding 32-d (fine-tuned)
- **TBSS** (scorer.py): similarity score `s ∈ [0,1]` utk pasangan deteksi-tracklet

Data: FLTCCache + APSSampler (dataset.py). Normalisasi ImageNet; augment flip 50%,
crop padding 10%, color jitter 0.2. Keputusan konsep: `d_model=64, batch 64, lr 1e-3`.

**Cara pakai (JupyterHub kampus, RTX 4090):**
1. Pastikan kernel = **jupyterhub-env** (Python 3.8, torch 2.0.1+cu118).
2. Buka notebook ini di folder repo (`notebooks/35_...ipynb`), jalankan cell dari atas.
3. Path data RELATIF ke root repo — jalan dari mana pun cwd-nya.
4. **PC mati?** Cekpt disimpan tiap epoch (`out/phase3_fold1/lighttrack_eN.pt`).
   Jalankan ulang cell "Model + auto-resume" dan cell training → lanjut otomatis
   dari epoch terakhir, tanpa kehilangan apa pun.
5. Jangan tutup tab browser selama training — cell training bisa jalan berjam-jam.

Versi script asli (kalau mau dipakai di terminal): `src/lighttrack/train.py`
""" ))

cells.append(code(
"""import os, sys, time, json, glob, subprocess
print("[1/2] import numpy/torch (bisa 10-30 detik pertama) ...", flush=True)
import numpy as np
import torch
import torch.nn as nn

# root repo = parent dari notebooks/ (atau cwd kalau bukan di notebooks/)
if os.path.basename(os.getcwd()) == "notebooks":
    ROOT = os.path.abspath(os.path.join(os.getcwd(), ".."))
else:
    ROOT = os.getcwd()
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "src", "lighttrack"))
print("ROOT =", ROOT)

print("[2/2] import modul lighttrack (encoder/scorer/dataset) ...", flush=True)
from encoder import LAE, _IMAGENET_MEAN, _IMAGENET_STD
from scorer import SimilarityModel
from dataset import FLTCCache, APSSampler, CROP

print("[2/2] selesai. Cek GPU ...", flush=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device =", device, "| torch", torch.__version__)
if device.type == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))
"""))

cells.append(code(
"""# ---------------- helper (IDENTIK dgn train.py, jangan diubah) ----------------
def _to_xyxy(boxes, W, H):
    x, y, w, h = boxes.T
    x1 = torch.clamp(x, 0, W); y1 = torch.clamp(y, 0, H)
    x2 = torch.clamp(x + w, 0, W); y2 = torch.clamp(y + h, 0, H)
    return torch.stack([x1 / W, y1 / H, x2 / W, y2 / H], dim=1)

def _iou(a, b):
    x1 = torch.max(a[:, 0], b[:, 0]); y1 = torch.max(a[:, 1], b[:, 1])
    x2 = torch.min(a[:, 2], b[:, 2]); y2 = torch.min(a[:, 3], b[:, 3])
    inter = torch.clamp(x2 - x1, 0) * torch.clamp(y2 - y1, 0)
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    return inter / (area_a + area_b - inter + 1e-9)

def _augment(crops, rng):
    B = crops.shape[0]
    flip = torch.rand(B, device=crops.device) < 0.5
    crops[flip] = torch.flip(crops[flip], dims=[3])
    pad = int(round(CROP * 0.1))
    pad_t = torch.nn.functional.pad(crops, (pad, pad, pad, pad), mode="replicate")
    offx = [rng.randint(0, 2 * pad + 1) for _ in range(B)]
    offy = [rng.randint(0, 2 * pad + 1) for _ in range(B)]
    out = torch.stack([pad_t[i, :, offy[i]:offy[i] + CROP, offx[i]:offx[i] + CROP]
                       for i in range(B)])
    bf = 1.0 + (torch.rand(B, 1, 1, 1, device=crops.device) - 0.5) * 0.4
    cf = 1.0 + (torch.rand(B, 1, 1, 1, device=crops.device) - 0.5) * 0.4
    sf = 1.0 + (torch.rand(B, 1, 1, 3, device=crops.device) - 0.5) * 0.4
    out = (out * bf * cf).clamp(0, 1)
    return out

def _normalize(crops):
    m = torch.tensor(_IMAGENET_MEAN, device=crops.device).view(1, 3, 1, 1)
    s = torch.tensor(_IMAGENET_STD, device=crops.device).view(1, 3, 1, 1)
    return (crops - m) / s

def _crop_to_tensor(crop_uint8_bgr, device):
    rgb = crop_uint8_bgr[..., ::-1].copy()
    t = torch.from_numpy(rgb).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    return t.to(device)

def _tbss_x(box_a, box_p, iou, ea, ep):
    return torch.cat([box_a, box_p, iou, ea, ep], dim=1)

print("helper OK")
"""))

cells.append(code(
"""# ---------------- KONFIGURASI (fold-1: MOT17 train + MOT20 train, kecuali MOT20-04) ----------------
SEQ_DIRS = (
    "data/s2/MOT17/train/MOT17-02-DPM:"
    "data/s2/MOT17/train/MOT17-04-DPM:"
    "data/s2/MOT17/train/MOT17-05-DPM:"
    "data/s2/MOT17/train/MOT17-09-DPM:"
    "data/s2/MOT17/train/MOT17-10-DPM:"
    "data/s2/MOT17/train/MOT17-11-DPM:"
    "data/s2/MOT17/train/MOT17-13-DPM:"
    "data/s2/mot20_hf/train/MOT20-02:"
    "data/s2/mot20_hf/train/MOT20-03:"
    "data/s2/mot20_hf/train/MOT20-05"
)
OUT     = "out/phase3_fold1"   # cekpt: {OUT}/lighttrack_eN.pt
EPOCHS  = 20
BATCH   = 64
LR      = 1e-3
D_MODEL = 64
WINDOW  = 15
MAX_PAIRS = 50
MARGIN  = 1.0
HOLDOUT = 0.2
SEED    = 0
print("SEQ_DIRS =", SEQ_DIRS)
"""))

cells.append(code(
"""# ---------------- Bangun cache FLTC + pasangan (ci, frame) + split train/val ----------------
torch.manual_seed(SEED)
seq_dirs = SEQ_DIRS.split(":")
caches = [FLTCCache(d) for d in seq_dirs]
sampler = APSSampler(window=WINDOW, max_pairs=MAX_PAIRS, seed=SEED)

all_pairs = []
for ci, c in enumerate(caches):
    fr = c.frames()
    all_pairs.extend((ci, f) for f in fr)
    print(f"  seq {os.path.basename(seq_dirs[ci]):<14} frames={len(fr)}")

val_pairs, train_pairs = [], []
split_rng = np.random.RandomState(SEED)
for ci, f in all_pairs:
    (val_pairs if split_rng.rand() < HOLDOUT else train_pairs).append((ci, f))
print(f"train_frames={len(train_pairs)} val_frames={len(val_pairs)}")
"""))

cells.append(code(
"""# ---------------- Model + optimizer + AUTO-RESUME ----------------
lae = LAE().to(device).train()
tbss = SimilarityModel(d_model=D_MODEL).to(device).train()
opt = torch.optim.Adam(list(lae.parameters()) + list(tbss.parameters()), lr=LR)

start_ep = 0
os.makedirs(OUT, exist_ok=True)
ckpts = sorted(glob.glob(os.path.join(OUT, "lighttrack_e*.pt")),
               key=lambda p: int(os.path.basename(p).split("_e")[1].split(".")[0]))
if ckpts:
    ck = torch.load(ckpts[-1], map_location=device)
    lae.load_state_dict(ck["lae"]); tbss.load_state_dict(ck["tbss"])
    if "opt" in ck:
        opt.load_state_dict(ck["opt"])
    start_ep = int(ck["epoch"])
    print(f"RESUME dari {ckpts[-1]} -> lanjut epoch {start_ep + 1}")
else:
    print("Mulai dari awal (epoch 1)")
"""))

cells.append(code(
"""# ---------------- TRAINING (jalankan cell ini; cekpt tiap epoch) ----------------
from tqdm.notebook import tqdm
from IPython.display import clear_output
try:
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except Exception:
    HAVE_PLT = False

logf = open(os.path.join(OUT, "train.log"), "a")
stats_jsonl = open(os.path.join(OUT, "train_stats.jsonl"), "a")
hist = {"ep": [], "loss": [], "lt": [], "lb": [], "bce_acc": [], "margin": [], "dt": []}
seq_names = [os.path.basename(d) for d in seq_dirs]
t_epoch0 = time.time()

for ep in range(start_ep + 1, EPOCHS + 1):
    t_ep = time.time()
    lae.train(); tbss.train()
    tot_l = tot_lt = tot_lb = 0.0
    nb = 0
    rng = np.random.RandomState(SEED + ep)
    np.random.RandomState(SEED + ep).shuffle(train_pairs)

    pbar = tqdm(train_pairs, desc=f"ep{ep}/{EPOCHS} train", unit="fr", leave=False)
    for i, (ci, t) in enumerate(pbar):
        triplets = sampler.sample(caches[ci], t)
        if not triplets:
            continue
        H, W = caches[ci].frame_size()
        use = triplets[:BATCH]
        a = torch.cat([_crop_to_tensor(u["a"][0], device) for u in use])
        p = torch.cat([_crop_to_tensor(u["p"][0], device) for u in use])
        n = torch.cat([_crop_to_tensor(u["n"][0], device) for u in use])
        a, p, n = _normalize(_augment(a, rng)), _normalize(_augment(p, rng)), _normalize(_augment(n, rng))

        ba = torch.tensor([u["a"][1] for u in use], device=device).float()
        bp = torch.tensor([u["p"][1] for u in use], device=device).float()
        bn = torch.tensor([u["n"][1] for u in use], device=device).float()
        iou_ap = _iou(_to_xyxy(ba, W, H), _to_xyxy(bp, W, H)).reshape(-1, 1)
        iou_an = _iou(_to_xyxy(ba, W, H), _to_xyxy(bn, W, H)).reshape(-1, 1)

        ea, ep_, en_ = lae(a), lae(p), lae(n)
        dpos = ((ea - ep_) ** 2).sum(1)
        dneg = ((ea - en_) ** 2).sum(1)
        L_triplet = torch.clamp(dpos - dneg + MARGIN, min=0.0).mean()

        b_ap = _to_xyxy(ba, W, H); b_an = _to_xyxy(bn, W, H)
        x_ap = _tbss_x(b_ap, _to_xyxy(bp, W, H), iou_ap, ea, ep_)
        x_an = _tbss_x(b_an, _to_xyxy(bn, W, H), iou_an, ea, en_)
        y = torch.cat([torch.ones(len(use), 1, device=device),
                       torch.zeros(len(use), 1, device=device)])
        L_bce = nn.functional.binary_cross_entropy(
            torch.cat([tbss(x_ap), tbss(x_an)]), y)

        loss = L_triplet + L_bce
        opt.zero_grad(); loss.backward(); opt.step()
        tot_l += loss.item(); tot_lt += L_triplet.item(); tot_lb += L_bce.item(); nb += 1
        pbar.set_postfix(L=f"{tot_l/max(1,nb):.4f}", seq=seq_names[ci], fr=t)

    # ---- validation (tanpa augment; tanpa grad) ----
    lae.eval(); tbss.eval()
    acc_t = acc_d = 0
    cos_same = cos_diff = 0.0
    n_s = n_d = 0
    vbar = tqdm(val_pairs, desc=f"ep{ep}/{EPOCHS} val  ", unit="fr", leave=False)
    with torch.inference_mode():
        for ci, t in vbar:
            for u in sampler.sample(caches[ci], t):
                H, W = caches[ci].frame_size()
                a = _normalize(_crop_to_tensor(u["a"][0], device))
                p = _normalize(_crop_to_tensor(u["p"][0], device))
                nn_ = _normalize(_crop_to_tensor(u["n"][0], device))
                ea, ep_, en_ = lae(a), lae(p), lae(nn_)
                cos_same += float((ea * ep_).sum()); n_s += 1
                cos_diff += float((ea * en_).sum()); n_d += 1
                ba = torch.tensor([u["a"][1]], device=device).float()
                bp = torch.tensor([u["p"][1]], device=device).float()
                bn = torch.tensor([u["n"][1]], device=device).float()
                b_ap = _to_xyxy(ba, W, H); b_an = _to_xyxy(bn, W, H)
                iou_ap = _iou(b_ap, _to_xyxy(bp, W, H)).reshape(1, 1)
                iou_an = _iou(b_an, _to_xyxy(bn, W, H)).reshape(1, 1)
                s_ap = float(tbss(_tbss_x(b_ap, _to_xyxy(bp, W, H), iou_ap, ea, ep_))[0, 0])
                s_an = float(tbss(_tbss_x(b_an, _to_xyxy(bn, W, H), iou_an, ea, en_))[0, 0])
                acc_t += int(s_ap > 0.5); acc_d += int(s_an < 0.5)
            vbar.set_postfix(seq=seq_names[ci], fr=t, n_s=n_s, n_d=n_d)

    acc = (acc_t + acc_d) / max(1, n_s + n_d)
    cos_s = cos_same / max(1, n_s)
    cos_d = cos_diff / max(1, n_d)
    dt_ep = time.time() - t_ep
    dt_avg = (time.time() - t_epoch0) / (ep - start_ep)
    eta = dt_avg * (EPOCHS - ep)
    line = (f"ep={ep:2d} L={tot_l/max(1,nb):.4f} Lt={tot_lt/max(1,nb):.4f} "
            f"Lb={tot_lb/max(1,nb):.4f} BCEacc={acc:.3f} "
            f"cos_same={cos_s:.3f} cos_diff={cos_d:.3f} margin={cos_s-cos_d:+.3f} "
            f"[{dt_ep:.0f}s | rata {dt_avg:.0f}s/ep | ETA {eta/60:.0f}m]")
    print(line); logf.write(line + "\\n"); logf.flush()
    stats_jsonl.write(json.dumps({"event": "epoch", "ep": ep,
                                  "loss": tot_l / max(1, nb), "lt": tot_lt / max(1, nb),
                                  "lb": tot_lb / max(1, nb), "bce_acc": acc,
                                  "cos_same": cos_s, "cos_diff": cos_d,
                                  "dt_s": round(dt_ep, 1), "eta_s": round(eta, 1)}) + "\\n")
    stats_jsonl.flush()

    torch.save({"lae": lae.state_dict(), "tbss": tbss.state_dict(),
                "opt": opt.state_dict(),
                "epoch": ep, "loss": tot_l / max(1, nb)},
               os.path.join(OUT, f"lighttrack_e{ep}.pt"))

    hist["ep"].append(ep); hist["loss"].append(tot_l / max(1, nb))
    hist["lt"].append(tot_lt / max(1, nb)); hist["lb"].append(tot_lb / max(1, nb))
    hist["bce_acc"].append(acc); hist["margin"].append(cos_s - cos_d)
    hist["dt"].append(dt_ep)

    if HAVE_PLT:
        clear_output(wait=True)
        fig, ax = plt.subplots(1, 3, figsize=(15, 3.5))
        ax[0].plot(hist["ep"], hist["loss"], "-o", label="total")
        ax[0].plot(hist["ep"], hist["lt"], "-o", label="triplet")
        ax[0].plot(hist["ep"], hist["lb"], "-o", label="bce")
        ax[0].set_title("Loss/epoch"); ax[0].legend(); ax[0].grid(alpha=0.3)
        ax[1].plot(hist["ep"], hist["bce_acc"], "-o")
        ax[1].set_title("BCE acc/epoch"); ax[1].grid(alpha=0.3)
        ax[2].plot(hist["ep"], hist["margin"], "-o")
        ax[2].set_title("cos margin/epoch"); ax[2].grid(alpha=0.3)
        plt.tight_layout(); plt.show()
        print(line)

logf.close(); stats_jsonl.close()
print(f"DONE — ckpt terakhir {OUT}/lighttrack_e{EPOCHS}.pt")
"""))

cells.append(code(
"""# ---------------- Ringkasan akhir + kurva ----------------
import matplotlib.pyplot as plt
print("epoch terakhir:", hist["ep"][-1], "| loss:", round(hist["loss"][-1], 4),
      "| BCEacc:", round(hist["bce_acc"][-1], 3),
      "| margin:", round(hist["margin"][-1], 3),
      "| dt_avg:", round(sum(hist["dt"]) / len(hist["dt"]) / 60, 1), "min/epoch")
fig, ax = plt.subplots(1, 2, figsize=(12, 3.5))
ax[0].plot(hist["ep"], hist["loss"], "-o")
ax[0].set_title("Loss"); ax[0].grid(alpha=0.3)
ax[1].plot(hist["ep"], hist["bce_acc"], "-o", label="BCEacc")
ax[1].plot(hist["ep"], hist["margin"], "-o", label="margin")
ax[1].set_title("Val"); ax[1].legend(); ax[1].grid(alpha=0.3)
plt.tight_layout(); plt.show()
"""))

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3 (jupyterhub-env)", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.8"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

path = "notebooks/35_s2_lighttrack_train.ipynb"
with open(path, "w") as f:
    json.dump(nb, f, indent=1)
print("wrote", path, "| cells:", len(cells))
