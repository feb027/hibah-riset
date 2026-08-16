"""Verifikasi TbssAppearanceOnnx vs TbssAppearance (torch) pada data nyata.

Membandingkan output embed() dan score() kedua jalur pada frame MOT20 asli dengan
deteksi sintetik. Kalau adapter ONNX bug (normalisasi, IoU, urutan fitur TBSS),
cosine embed turun jauh / skor TBSS meleset > 1e-3.

Cara pakai (kampus, butuh torch + onnxruntime):
    python scripts/s2/verify_onnx_adapter.py \
        --ckpt out/phase3_fold1_v2/best.pt --onnx-dir out/onnx \
        --img-dir data/s2/mot20/train/MOT20-02/img1 \
        --frames 3 --dets 25

Ambruk indicator: LAE cosine < 0.99 (embed beda) atau TBSS max-diff > 1e-3 (skor beda).
"""
import argparse
import glob
import os
import random
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", required=True)
    p.add_argument("--onnx-dir", required=True)
    p.add_argument("--img-dir", required=True, help="folder img1 MOT20 (mis. .../MOT20-02/img1)")
    p.add_argument("--frames", type=int, default=3)
    p.add_argument("--dets", type=int, default=25, help="jumlah deteksi sintetik per frame")
    return p.parse_args()


def main():
    import cv2
    import numpy as np

    from src.lighttrack.phase4 import TbssAppearance
    from src.lighttrack.phase4_onnx import TbssAppearanceOnnx

    args = parse_args()
    torch_app = TbssAppearance(args.ckpt)
    onnx_app = TbssAppearanceOnnx(args.onnx_dir)

    imgs = sorted(glob.glob(os.path.join(args.img_dir, "*.jpg")))
    if len(imgs) == 0:
        sys.exit("tidak ada frame di %s" % args.img_dir)
    step = max(1, len(imgs) // args.frames)
    frames = imgs[::step][:args.frames]
    print("frame sample: %d (dari %d)" % (len(frames), len(imgs)))

    rng = random.Random(42)
    cos_all, diff_all, score_diff_all = [], [], []
    for fp in frames:
        frame = cv2.imread(fp)
        h, w = frame.shape[:2]
        dets = []
        for _ in range(args.dets):
            bw = rng.randint(30, 200); bh = rng.randint(60, 300)
            x = rng.randint(0, max(1, w - bw)); y = rng.randint(0, max(1, h - bh))
            dets.append([x, y, bw, bh])
        e_t = torch_app.embed(frame, dets)
        e_o = onnx_app.embed(frame, dets)
        cos = float(np.mean(np.sum(e_t * e_o, axis=1)))          # L2-unit -> cosine
        cos_all.append(cos)
        # skor: track sintetik = 10 deteksi pertama, det = semuanya
        tr = dets[:max(1, len(dets) // 4)]
        s_t = torch_app.score(w, h, tr, dets, e_t[:len(tr)], e_t)
        s_o = onnx_app.score(w, h, tr, dets, e_o[:len(tr)], e_o)
        d = float(np.abs(s_t - s_o).max())
        diff_all.append(np.abs(e_t - e_o).max())
        score_diff_all.append(d)
        print("  %-30s cos=%.4f | emb_maxdiff=%.2e | tbss_maxdiff=%.2e"
              % (os.path.basename(fp), cos, diff_all[-1], d))

    print()
    print("RINGKASAN: embed cos min=%.4f (harus > 0.99) | tbss maxdiff maks=%.2e (harus < 1e-3)"
          % (min(cos_all), max(score_diff_all)))
    assert min(cos_all) > 0.99, "embedding ONNX menyimpang dari torch"
    assert max(score_diff_all) < 1e-3, "skor TBSS ONNX menyimpang dari torch"
    print("OK: adapter ONNX konsisten dengan torch.")


if __name__ == "__main__":
    main()
