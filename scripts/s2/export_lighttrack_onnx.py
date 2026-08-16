"""Export LAE + TBSS dari ckpt .pt ke ONNX (untuk PC tanpa torch-GPU: Windows/RX6600).

Runtime hasil export TIDAK butuh torch: adapter `src/lighttrack/phase4_onnx.py`
memakai onnxruntime (DirectML kalau ada, jatuh ke CPU kalau tidak). Deteksi YOLO
sendiri sudah lewat .onnx (ultralytics).

Cara pakai (butuh torch + onnx + onnxruntime, bisa CPU aja; jalan di kampus):
    python scripts/s2/export_lighttrack_onnx.py --ckpt out/phase3_fold1_v2/best.pt \
        --out-dir out/onnx

Menghasilkan:
    lae.onnx   : (N,3,224,224) float32 ternormalisasi ImageNet (RGB) -> (N,32) L2-norm
    tbss.onnx  : (B,6) float32 [iou,cos,dx_c,dy_c,dw,dh] -> (B,1) [0,1]

Verifikasi numerik otomatis: cosine LAE torch vs ONNX > 0.99, max-abs-diff TBSS < 1e-4.
File ckpt dijamin tidak berubah: export hanya membaca bobot via load_state_dict.

Catatan: ONNX jalankan di-device CPU saat export (tracing tidak butuh GPU);
output "Applied workaround for CuDNN issue" adalah warning tidak berbahaya.
"""
import argparse
import os
import sys

# skrip dijalankan sebagai scripts/s2/export_lighttrack_onnx.py dari repo root:
# sys.path[0] = scripts/s2, jadi tambah root repo agar `src.` bisa di-import
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# butuh torch — skrip ini HANYA dijalankan di mesin yang punya torch (kampus),
# bukan di PC target. Import dibawah untuk menghindari error saat --help.
def run():
    import numpy as np
    import onnx
    import onnxruntime as ort
    import torch

    from torchvision.models import MobileNet_V3_Small_Weights

    from src.lighttrack.encoder import LAE, EMBEDED_DIM, CROP_SIZE
    from src.lighttrack.scorer import SimilarityModel

    def parse_args():
        p = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        p.add_argument("--ckpt", required=True, help="ckpt training (out/phase3_fold1_v2/best.pt)")
        p.add_argument("--out-dir", default="out/onnx", help="folder output")
        return p.parse_args()

    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    ck = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    lae = LAE().eval()
    lae.load_state_dict(ck["lae"])
    tbss = SimilarityModel().eval()
    tbss.load_state_dict(ck["tbss"])
    print("ckpt dimuat: epoch=%s best_acc=%s" % (ck.get("epoch"), ck.get("best_acc")))

    # eager mode ONNX (torch 2.0 kompatibel, tidak butuh dynamo)
    lae_path = os.path.join(args.out_dir, "lae.onnx")
    dummy = torch.randn(1, 3, CROP_SIZE, CROP_SIZE)
    torch.onnx.export(lae, dummy, lae_path,
                      input_names=["x"], output_names=["emb"],
                      dynamic_axes={"x": {0: "N"}, "emb": {0: "N"}},
                      opset_version=13, do_constant_folding=True)
    print("LAE     ->", lae_path)

    tbss_path = os.path.join(args.out_dir, "tbss.onnx")
    dummy_t = torch.randn(1, 6) * 0.1
    torch.onnx.export(tbss, dummy_t, tbss_path,
                      input_names=["x"], output_names=["s"],
                      dynamic_axes={"x": {0: "B"}, "s": {0: "B"}},
                      opset_version=13, do_constant_folding=True)
    print("TBSS    ->", tbss_path)

    # verifikasi numerik vs torch (CPU provider; runtime target boleh DML/CPU)
    sess = ort.InferenceSession(lae_path, providers=["CPUExecutionProvider"])
    ort_tbss = ort.InferenceSession(tbss_path, providers=["CPUExecutionProvider"])

    torch.manual_seed(0)
    for n in (1, 5, 33):
        x = torch.randn(n, 3, CROP_SIZE, CROP_SIZE)
        with torch.inference_mode():
            e_torch = lae(x).numpy()
        e_onnx = sess.run(None, {"x": x.numpy()})[0]
        cos = np.sum(e_torch * e_onnx, axis=1)  # L2-unit, cosine = dot
        assert cos.min() > 0.99, (n, cos)
    print("LAE verifikasi OK: cosine torch-vs-onnx > 0.99 (N=1,5,33)")

    for b in (1, 7, 128):
        xt = torch.randn(b, 6) * 0.2
        with torch.inference_mode():
            s_torch = tbss(xt).numpy().reshape(-1)
        s_onnx = ort_tbss.run(None, {"x": xt.numpy()})[0].reshape(-1)
        assert np.abs(s_torch - s_onnx).max() < 1e-4, (b, np.abs(s_torch - s_onnx).max())
    print("TBSS verifikasi OK: max-abs-diff < 1e-4 (B=1,7,128)")

    for f in (lae_path, tbss_path):
        onnx.checker.check_model(onnx.load(f))
        print("  %s  %d bytes" % (os.path.basename(f), os.path.getsize(f)))
    print("Selesai. Salin dua file .onnx ke PC target (mis. data/s2/weights/).")


if __name__ == "__main__":
    run()
