"""LightTrack-ReID-inspired (Phase 3) — training LAE + TBSS (loss = triplet + BCE).

Melatih dua modul sekaligus (kode paper Eq 13: L = L_triplet + L_BCE):
  - LAE  (encoder.py)  : backbone MobileNetV3-Small -> 32-d embedding (fine-tuned)
  - TBSS (scorer.py)   : similarity score s in [0,1] utk pasangan deteksi-tracklet

Data: FLTCCache + APSSampler (dataset.py). Tiap langkah = satu frame:
  - triplet loss dipakai di embedding LAE    (a = anchor, p = positif, n = negatif)
  - BCE loss dipakai di skor TBSS            (x = [b_a,b_p,IoU,e_a,e_p] -> 1,
                                              x = [b_a,b_n,IoU,e_a,e_n] -> 0)

Normalisasi: ImageNet (konsisten dengan encoder inference Phase 2).
Augmentasi (paper): flip 50%, crop padding 10%, color jitter 0.2.
Keputusan konsep: d_model=64, batch 64, ImageNet.

py3.8-friendly, TORCH-ONLY. Simpan ckpt {out}/last.pt (tiap epoch) +
{out}/best.pt (BCEacc val terbaik, ala YOLO).
    {"lae": LAE.state_dict(), "tbss": TBSS.state_dict(), "epoch": k, "loss": ..}

Dipakai:
    python train.py --seq-dirs data/s2/mot17_hf/train/MOT17-02:data/s2/mot20_hf/train/MOT20-01
        [--out out/phase3 --epochs 20 --batch 64 --lr 1e-3 --max-frames 0]
    --max-frames>0 = mini-run (uji pipa dulu, 1-3 epoch, 1 sekuens), lalu full.
"""
import argparse
import sys
import json
import os
import subprocess
import time

import numpy as np
import torch
import torch.nn as nn

from encoder import LAE, _IMAGENET_MEAN, _IMAGENET_STD
from scorer import SimilarityModel
from dataset import FLTCCache, APSSampler, CROP


# ---------------------------------------------------------------- augment/norm
def _to_xyxy(boxes, W, H):
    """(B,4) tlwh -> (B,4) xyxy ternormalisasi [0,1] (clamp ke frame asli W,H).

    Normalisasi penting: TBSS mencampur bbox + IoU(0..1) + embedding L2-norm (v1
    73-d / v2 6-d); koordinat piksel mentah (0..1920) akan mendominasi Linear.
    Wajib direplikasi identik di inference (Phase 4 tracker).
    """
    x, y, w, h = boxes.T
    x1 = torch.clamp(x, 0, W)
    y1 = torch.clamp(y, 0, H)
    x2 = torch.clamp(x + w, 0, W)
    y2 = torch.clamp(y + h, 0, H)
    return torch.stack([x1 / W, y1 / H, x2 / W, y2 / H], dim=1)


def _iou(a, b):
    """a,b: (B,4) xyxy -> (B,) IoU per pair."""
    x1 = torch.max(a[:, 0], b[:, 0]); y1 = torch.max(a[:, 1], b[:, 1])
    x2 = torch.min(a[:, 2], b[:, 2]); y2 = torch.min(a[:, 3], b[:, 3])
    inter = torch.clamp(x2 - x1, 0) * torch.clamp(y2 - y1, 0)
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    return inter / (area_a + area_b - inter + 1e-9)


def _augment(crops, rng):
    """crops: torch (B,3,CROP,CROP) float [0,1] -> augmented (B,3,CROP,CROP)."""
    B = crops.shape[0]
    # flip horizontal 50%
    flip = torch.rand(B, device=crops.device) < 0.5
    crops[flip] = torch.flip(crops[flip], dims=[3])
    # crop padding 10% -> offset random, krop balik ke 224
    pad = int(round(CROP * 0.1))
    pad_t = torch.nn.functional.pad(crops, (pad, pad, pad, pad), mode="replicate")
    offx = [rng.randint(0, 2 * pad + 1) for _ in range(B)]
    offy = [rng.randint(0, 2 * pad + 1) for _ in range(B)]
    out = torch.stack([pad_t[i, :, offy[i]:offy[i] + CROP, offx[i]:offx[i] + CROP]
                       for i in range(B)])
    # color jitter 0.2 (brightness/contrast/saturation)
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
    rgb = crop_uint8_bgr[..., ::-1].copy()          # BGR -> RGB
    t = torch.from_numpy(rgb).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    return t.to(device)


def _tbss_x(box_a, box_p, iou, ea, ep):
    # v2 — input ringkas 6-d (fix collapse):
    #   [IoU(1), cos(e_a,e_p)(1), bbox-diff termormalisasi(4)]
    # bukan concat bbox/embedding 73-d (embedding unit-vector bikin sinyal
    # informasi tenggelam). Skala seluruh fitur di [-1,1] utk input MLP TBSS.
    cos = (ea * ep).sum(dim=1, keepdim=True)          # embedding L2-unit -> cosine
    bd = box_a - box_p                                 # (B,4) diff, sudah [0,1]^4
    return torch.cat([iou, cos, bd], dim=1)            # (B,6)


# ---------------------------------------------------------------- resource stats
def _cuda_available(timeout=10):
    """torch.cuda.is_available() bisa HANG selamanya di GPU COMPUTE EXCLUSIVE
    (JupyterHub kampus) tanpa MPS server -> probe di proses terpisah + timeout.
    Return True cuma kalau CUDA benar2 siap; selain itu False (cpu, aman)."""
    import subprocess
    code = "import torch; print(torch.cuda.is_available())"
    try:
        r = subprocess.run([sys.executable, "-c", code],
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() == "True"
    except Exception:
        return False


def _proc_stat():
    """(/proc/stat cpu line, /proc/meminfo dict) utk CPU% & RAM usage (Linux/stdlib)."""
    with open("/proc/stat") as f:
        cpu = f.readline().split()[1:]           # user nice system idle iowait irq ...
    with open("/proc/meminfo") as f:
        mem = {l.split(":")[0]: int(l.split()[1]) for l in f
               if l.split(":")[0] in ("MemTotal", "MemAvailable")}
    return [int(x) for x in cpu], mem


def cpu_percent():
    """CPU usage % antar dua panggilan (delta idle/total /proc/stat)."""
    def load():
        with open("/proc/stat") as f:
            p = [int(x) for x in f.readline().split()[1:]]
        return sum(p), p[3] + p[4]               # total, idle+iowait
    a1, idle1 = load()
    time.sleep(0.2)
    a2, idle2 = load()
    d = a2 - a1
    return 0.0 if d <= 0 else max(0.0, 100.0 * (1 - (idle2 - idle1) / d))


def res_stats(device):
    """dict statistik: CPU%, RAM (total/avail), GPU (VRAM alloc/total, util% via nvidia-smi kalau ada)."""
    s = {}
    _, mem = _proc_stat()
    s["cpu_percent"] = round(cpu_percent(), 1)
    s["ram_total_gb"] = round(mem["MemTotal"] / 1e6, 2)
    s["ram_avail_gb"] = round(mem["MemAvailable"] / 1e6, 2)
    if device.type == "cuda":
        try:
            s["gpu_vram_alloc_gb"] = round(torch.cuda.memory_allocated(device) / 1e9, 2)
            s["gpu_vram_total_gb"] = round(torch.cuda.get_device_properties(device).total_memory / 1e9, 2)
            util = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                capture_output=True, text=True)
            s["gpu_util_percent"] = float(util.stdout.strip().split("\n")[0]) if util.returncode == 0 else None
        except Exception:
            pass
    return s


# ---------------------------------------------------------------- training
def train(args):
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if _cuda_available() else "cpu")
    print(f"[train] device={device}")

    lae = LAE().to(device).train()
    tbss = SimilarityModel(d_model=args.d_model).to(device).train()
    # opsi 2 — optimizer pisah per modul (LR sendiri2), cekpt opt
    # state_dict() sama bentuknya: dua param group.
    opt = torch.optim.Adam([
        {"params": lae.parameters(), "lr": args.lr},
        {"params": tbss.parameters(), "lr": args.tbss_lr},
    ])
    m_triplet = args.margin

    caches = [FLTCCache(d) for d in args.seq_dirs.split(":")]
    sampler = APSSampler(window=args.window, max_pairs=args.max_pairs, seed=args.seed)

    # pasangan (cache_idx, frame) -> split train/val per cache (frame antar-cache
    # tidak bisa dicampur: tiap seq mulai dari frame 1 sendiri-sendiri)
    all_pairs = []
    for ci, c in enumerate(caches):
        fr = c.frames()
        if args.max_frames > 0:
            fr = fr[: args.max_frames]
        all_pairs.extend((ci, f) for f in fr)
    val_pairs, train_pairs = [], []
    split_rng = np.random.RandomState(args.seed)   # satu rng, advancing (bukan dibuat ulang tiap frame)
    for ci, f in all_pairs:
        (val_pairs if split_rng.rand() < args.holdout
         else train_pairs).append((ci, f))
    print(f"[train] train_frames={len(train_pairs)} val_frames={len(val_pairs)}")

    os.makedirs(args.out, exist_ok=True)
    logf = open(os.path.join(args.out, "train.log"), "a")
    stats_jsonl = open(os.path.join(args.out, "train_stats.jsonl"), "a")

    start_ep = 0
    best_acc = 0.0
    if args.resume:
        ck = torch.load(args.resume, map_location=device)
        lae.load_state_dict(ck["lae"]); tbss.load_state_dict(ck["tbss"])
        if "opt" in ck:
            opt.load_state_dict(ck["opt"])
        start_ep = int(ck["epoch"])
        best_acc = float(ck.get("best_acc", 0.0))
        print(f"[train] resume dari {args.resume} (lanjut epoch {start_ep+1}, best_acc={best_acc:.3f})")

    # metadata header (sekali, kalau file baru)
    if logf.tell() == 0:
        logf.write(f"# train {time.strftime('%Y-%m-%d %H:%M:%S')} "
                   f"seq_dirs={args.seq_dirs} out={args.out} epochs={args.epochs} "
                   f"batch={args.batch} lr={args.lr} d_model={args.d_model} "
                   f"window={args.window} max_pairs={args.max_pairs} margin={args.margin} "
                   f"holdout={args.holdout} device={device}\n")
        stats_jsonl.write('{"event":"start","time":"%s","device":"%s","epochs":%d,"seq":%d}\n'
                          % (time.strftime("%Y-%m-%d %H:%M:%S"), str(device), args.epochs, len(caches)))

    t_epoch0 = time.time()
    for ep in range(start_ep + 1, args.epochs + 1):
        t_ep = time.time()
        lae.train(); tbss.train()
        tot_l = tot_lt = tot_lb = 0.0
        nb = 0
        rng = np.random.RandomState(args.seed + ep)
        np.random.RandomState(args.seed + ep).shuffle(train_pairs)
        seq_names = [os.path.basename(d) for d in args.seq_dirs.split(":")]
        t_last = time.time()
        for i, (ci, t) in enumerate(train_pairs):
            triplets = sampler.sample(caches[ci], t)
            if not triplets:
                continue
            H, W = caches[ci].frame_size()   # frame asli utk clamp/normalisasi box
            use = triplets[: args.batch]
            # ---- crops (B,3,224,224) float [0,1], augment, normalize
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
            # triplet (m=1.0)
            dpos = ((ea - ep_) ** 2).sum(1)
            dneg = ((ea - en_) ** 2).sum(1)
            L_triplet = torch.clamp(dpos - dneg + m_triplet, min=0.0).mean()
            # BCE (a,p)->1 ; (a,n)->0  -- box TERNORMALISASI [0,1] (skala & IoU & embedding
            #                          sebanding; lihat _to_xyxy doc). WAJIB sama di val & Phase 4.
            b_ap = _to_xyxy(ba, W, H); b_an = _to_xyxy(bn, W, H)
            x_ap = _tbss_x(b_ap, _to_xyxy(bp, W, H), iou_ap, ea, ep_)
            x_an = _tbss_x(b_an, _to_xyxy(bn, W, H), iou_an, ea, en_)
            y = torch.cat([torch.ones(len(use), 1, device=device),
                           torch.zeros(len(use), 1, device=device)])
            # opsi 2 — BCE berbobot: kelas negatif (y=0) lebih penting utk
            # mendorong skor pasangan beda turun (v1 gagal krn s_an nyangkut
            # ~0.95). weight dihitung per-elemen y.
            bce_w = torch.where(y > 0, torch.ones_like(y) * args.bce_pos_w,
                                torch.ones_like(y) * args.bce_neg_w)
            L_bce = nn.functional.binary_cross_entropy(
                torch.cat([tbss(x_ap), tbss(x_an)]), y, weight=bce_w)

            loss = L_triplet + L_bce
            opt.zero_grad(); loss.backward(); opt.step()
            tot_l += loss.item(); tot_lt += L_triplet.item(); tot_lb += L_bce.item(); nb += 1
            # realtime progress 1 baris (overwrite \r) — update tiap >=0.5s, flush
            now = time.time()
            if now - t_last >= 0.5:
                t_last = now
                pct = 100.0 * (i + 1) / len(train_pairs)
                el = now - t_ep
                eta = el / (i + 1) * (len(train_pairs) - i - 1)
                bar = "#" * int(30 * (i + 1) / len(train_pairs))
                sys.stdout.write(
                    f"\r\033[K  ep={ep} [{i+1}/{len(train_pairs)}] {pct:5.1f}% |{bar:<30}| "
                    f"seq={seq_names[ci]} fr={t} L={tot_l/max(1,nb):.4f} "
                    f"el={el:6.0f}s ETA={eta/60:5.1f}m")
                sys.stdout.flush()

        sys.stdout.write("\r\033[K")  # bersihkan baris realtime sebelum summary

        # ---- validation (tanpa augment; tanpa grad)
        lae.eval(); tbss.eval()
        acc_t = acc_d = 0
        cos_same = cos_diff = 0.0
        n_s = n_d = 0
        with torch.inference_mode():
            tv_last = time.time(); vi = 0
            for ci, t in val_pairs:
                vi += 1
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
                # val realtime (1 baris, sama pola dgn train)
                now = time.time()
                if now - tv_last >= 0.5:
                    tv_last = now
                    sys.stdout.write(
                        f"\r\033[K  ep={ep} [val {vi}/{len(val_pairs)}] "
                        f"seq={seq_names[ci]} fr={t} n_s={n_s} n_d={n_d}")
                    sys.stdout.flush()
            sys.stdout.write("\r\033[K")
        acc = (acc_t + acc_d) / max(1, n_s + n_d)
        cos_s = cos_same / max(1, n_s)
        cos_d = cos_diff / max(1, n_d)
        line = (f"ep={ep:2d} L={tot_l/max(1,nb):.4f} Lt={tot_lt/max(1,nb):.4f} "
                f"Lb={tot_lb/max(1,nb):.4f} BCEacc={acc:.3f} "
                f"cos_same={cos_s:.3f} cos_diff={cos_d:.3f} margin={cos_s-cos_d:+.3f}")
        dt_ep = time.time() - t_ep
        dt_avg = (time.time() - t_epoch0) / (ep - start_ep)
        eta = dt_avg * (args.epochs - ep)
        rs = res_stats(device)
        line += (f"  [{dt_ep:.0f}s | rata {dt_avg:.0f}s/ep | ETA {eta/60:.0f}m] "
                 f"CPU {rs.get('cpu_percent')}% RAM {rs.get('ram_avail_gb')}/{rs.get('ram_total_gb')}GB"
                 + (f" GPU util {rs.get('gpu_util_percent')}% VRAM {rs.get('gpu_vram_alloc_gb')}/{rs.get('gpu_vram_total_gb')}GB"
                    if "gpu_vram_alloc_gb" in rs else ""))
        print(line); logf.write(line + "\n"); logf.flush()
        stats_jsonl.write(json.dumps({"event": "epoch", "ep": ep, "loss": tot_l / max(1, nb),
                                      "lt": tot_lt / max(1, nb), "lb": tot_lb / max(1, nb),
                                      "bce_acc": acc, "cos_same": cos_s, "cos_diff": cos_d,
                                      "dt_s": round(dt_ep, 1), "eta_s": round(eta, 1),
                                      "cpu_percent": rs.get("cpu_percent"),
                                      "ram_avail_gb": rs.get("ram_avail_gb"),
                                      "gpu_util_percent": rs.get("gpu_util_percent"),
                                      "gpu_vram_alloc_gb": rs.get("gpu_vram_alloc_gb")}) + "\n")
        stats_jsonl.flush()

        # YOLO-style: last.pt selalu ditimpa tiap epoch; best.pt hanya kalau
        # BCEacc val membaik (bukan loss — loss gak mencerminkan diskriminasi TBSS).
        ck = {"lae": lae.state_dict(), "tbss": tbss.state_dict(),
              "opt": opt.state_dict(),
              "epoch": ep, "loss": tot_l / max(1, nb), "best_acc": best_acc}
        torch.save(ck, os.path.join(args.out, "last.pt"))
        if acc >= best_acc:
            best_acc = acc
            ck["best_acc"] = best_acc
            torch.save(ck, os.path.join(args.out, "best.pt"))

    logf.close(); stats_jsonl.close()
    print(f"[train] selesai. Best BCEacc={best_acc:.3f} -> {args.out}/best.pt; last -> {args.out}/last.pt")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq-dirs", required=True, help="path sekuens dipisah ':'")
    ap.add_argument("--out", default="out/phase3")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--tbss-lr", type=float, default=1e-3,
                    help="LR khusus TBSS (opsi 2: optimizer pisah per modul)")
    ap.add_argument("--bce-pos-w", type=float, default=1.0,
                    help="bobot BCE kelas positif (y=1)")
    ap.add_argument("--bce-neg-w", type=float, default=1.0,
                    help="bobot BCE kelas negatif (y=0) — naikkan utk s_an turun")
    ap.add_argument("--d-model", type=int, default=64)
    ap.add_argument("--window", type=int, default=15)
    ap.add_argument("--max-pairs", type=int, default=50)
    ap.add_argument("--margin", type=float, default=1.0)
    ap.add_argument("--holdout", type=float, default=0.2)
    ap.add_argument("--max-frames", type=int, default=0,
                    help=">0 = mini-run: batasi jumlah frame per seq (uji pipa)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--resume", default=None,
                    help="ckpt .pt (last.pt/best.pt) utk lanjut training (opsional)")
    args = ap.parse_args()
    train(args)


if __name__ == "__main__":
    main()