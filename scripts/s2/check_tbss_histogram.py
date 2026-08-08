"""Diagnostik TBSS (Phase 3) — histogram skor s_ap (sama) vs s_an (beda).

Membedakan dua dugaan saat BCEacc val mentok ~0.5:
  1) TBSS collapse  -> histogram s_ap dan s_an tumpang tindih di ~0.5
  2) bug threshold  -> histogram terpisah, tapi akumulasi acc salah

Cara pakai (kampus, kernel jupyterhub-env, sama seperti train):
    python scripts/s2/check_tbss_histogram.py \
        --ckpt out/phase3_fold1_v2/best.pt \
        --seq-dirs data/s2/mot17_hf/train/MOT17-02:data/s2/mot20_hf/train/MOT20-01

Replikasi persis logika val notebook 35 (batch-64 GPU, cap MAX_VAL_PAIRS,
split holdout RandomState(seed) advancing) supaya angkanya sebanding dgn
bce_acc yang dilaporkan. Tanpa augment, tanpa grad.

Output: statistik + histogram ASCII tiap kelas + verdict singkat.
"""
import argparse
import os
import sys

import numpy as np
import torch

# train.py memakai import datar ("from encoder import ...") -> harus lewat sys.path
# langsung ke folder src/lighttrack, bukan lewat package src.lighttrack.*
_LT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "src", "lighttrack")
sys.path.insert(0, os.path.normpath(_LT_DIR))
from train import _to_xyxy, _iou, _tbss_x, _normalize, _crop_to_tensor  # noqa: E402
from encoder import LAE  # noqa: E402
from scorer import SimilarityModel  # noqa: E402
from dataset import FLTCCache, APSSampler  # noqa: E402

BINS = 10


def _ascii_hist(vals, label, lo=0.0, hi=1.0, width=40):
    if len(vals) == 0:
        print(f"{label}: (kosong)")
        return
    counts, edges = np.histogram(vals, bins=BINS, range=(lo, hi))
    mx = max(1, int(counts.max()))
    print(f"{label}  n={len(vals)} mean={vals.mean():.3f} std={vals.std():.3f}")
    for i in range(BINS):
        bar = "#" * int(round(width * counts[i] / mx))
        print(f"  [{edges[i]:.2f}-{edges[i+1]:.2f}) {counts[i]:6d} {bar}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ckpt", required=True, help="best.pt/last.pt hasil train")
    ap.add_argument("--seq-dirs", required=True, help="path sekuens dipisah ':'")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--max-pairs", type=int, default=1200, help="cap triplet val (MAX_VAL_PAIRS)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--holdout", type=float, default=0.2)
    ap.add_argument("--device", default=None)
    args = ap.parse_args()

    device = torch.device(args.device or ("cuda" if torch.cuda.is_available() else "cpu"))
    print(f"[ckpt] {args.ckpt}  device={device}", flush=True)

    ck = torch.load(args.ckpt, map_location=device)
    lae = LAE().to(device).eval()
    tbss = SimilarityModel().to(device).eval()
    lae.load_state_dict(ck["lae"]); tbss.load_state_dict(ck["tbss"])
    print(f"[ckpt] epoch={ck.get('epoch')} loss={ck.get('loss')}", flush=True)

    print("[val] memuat cache & index GT ...", flush=True)
    caches = [FLTCCache(d) for d in args.seq_dirs.split(":")]
    sampler = APSSampler(window=15, max_pairs=50, seed=args.seed)

    all_pairs = [(ci, f) for ci, c in enumerate(caches) for f in c.frames()]
    split_rng = np.random.RandomState(args.seed)   # sama dgn train.py
    val_pairs = [(ci, f) for ci, f in all_pairs if split_rng.rand() < args.holdout]
    print(f"[val] frame={len(val_pairs)} (cap {args.max_pairs} triplet)", flush=True)

    s_ap, s_an, c_ap, c_an = [], [], [], []
    v_n = 0
    with torch.inference_mode():
        for ci, t in val_pairs:
            if v_n >= args.max_pairs:
                break
            use = list(sampler.sample(caches[ci], t))[: args.batch]
            if not use:
                continue
            H, W = caches[ci].frame_size()
            a = torch.cat([_crop_to_tensor(u["a"][0], device) for u in use])
            p = torch.cat([_crop_to_tensor(u["p"][0], device) for u in use])
            n = torch.cat([_crop_to_tensor(u["n"][0], device) for u in use])
            a, p, n = _normalize(a), _normalize(p), _normalize(n)
            ba = torch.tensor([u["a"][1] for u in use], device=device).float()
            bp = torch.tensor([u["p"][1] for u in use], device=device).float()
            bn = torch.tensor([u["n"][1] for u in use], device=device).float()
            ea, ep_, en_ = lae(a), lae(p), lae(n)
            b_ap = _to_xyxy(ba, W, H); b_an = _to_xyxy(bn, W, H)
            iou_ap = _iou(b_ap, _to_xyxy(bp, W, H)).reshape(-1, 1)
            iou_an = _iou(b_an, _to_xyxy(bn, W, H)).reshape(-1, 1)
            s_ap.extend(tbss(_tbss_x(b_ap, _to_xyxy(bp, W, H), iou_ap, ea, ep_))[:, 0].tolist())
            s_an.extend(tbss(_tbss_x(b_an, _to_xyxy(bn, W, H), iou_an, ea, en_))[:, 0].tolist())
            c_ap.extend((ea * ep_).sum(1).tolist())
            c_an.extend((ea * en_).sum(1).tolist())
            v_n += len(use)
            seq = os.path.basename(caches[ci].seq_dir)
            sys.stdout.write(f"\r\033[K  [val] {v_n}/{min(args.max_pairs, len(val_pairs))} tr | {seq} fr={t}")
            sys.stdout.flush()
    sys.stdout.write("\r\033[K")

    s_ap, s_an = np.array(s_ap), np.array(s_an)
    c_ap, c_an = np.array(c_ap), np.array(c_an)
    n = min(len(s_ap), len(s_an))
    s_ap, s_an = s_ap[:n], s_an[:n]

    print(f"\nn={n}  (positif & negatif sama banyak — seimbang seperti train)\n", flush=True)
    _ascii_hist(s_ap, "s_ap (pasangan SAMA)")
    _ascii_hist(s_an, "s_an (pasangan BEDA)")

    acc05 = ((s_ap > 0.5).mean() + (s_an < 0.5).mean()) / 2
    print(f"\nBCEacc @0.5  = {acc05:.3f}   (yang dilaporkan di log)", flush=True)

    # signal: akurasi terbaik atas semua threshold -> skor bawa informasi apa tidak
    thr = np.linspace(0.05, 0.95, 19)
    best = max(((s_ap > t).mean() + (s_an < t).mean()) / 2 for t in thr)
    print(f"BCEacc terbaik (cari threshold) = {best:.3f}")

    sep = float(s_ap.mean() - s_an.mean())
    print(f"mean s_ap={s_ap.mean():.3f}  mean s_an={s_an.mean():.3f}  selisih={sep:+.3f}", flush=True)
    print(f"cosine  same={c_ap.mean():.3f}  diff={c_an.mean():.3f}  margin={c_ap.mean()-c_an.mean():+.3f}",
          flush=True)

    if sep > 0.3 and best > 0.8:
        print("\nVERDICT: skor TERPISAH (s_ap > s_an) tapi BCEacc@0.5 rendah ->", flush=True)
        print("  threshold/akumulasi val bermasalah, bukan model. Cek >0.5 di val.", flush=True)
    elif best > 0.8:
        print("\nVERDICT: ada signal (best acc tinggi) tapi skor tidak terkalibrasi 0.5 ->", flush=True)
        print("  model bisa dipakai asal threshold dicari (lihat best acc).", flush=True)
    else:
        print("\nVERDICT: TBSS COLLAPSE — skor tidak membawa signal (best acc ~0.5).", flush=True)
        print("  Cek jalur training TBSS: input _tbss_x, gradien BCE, LR per-modul.", flush=True)


if __name__ == "__main__":
    main()
