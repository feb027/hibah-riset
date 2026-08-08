# Phase 3 — Env training kampus RTX 4090 (jupyterhub-env LAMA bermasalah)

## Kenapa ganti env
- torch 2.0.1+cu118 (CUDA 11.8) di atas driver 580.126/CUDA 13 → wedge GPU:
  - cuDNN conv ~frame 122-130 (fix sementara: disable cudnn)
  - batch_norm saat val pass ~frame 10948 (hang `torch.batch_norm`, 2026-08-08, hang log ada)
- Akar: runtime torch cu118 vs driver CUDA13. Solusi: env torch 2.x + cuDNN 8.9 + TF32.

## Perintah (sekali saja)
conda create -n lt3090 -y python=3.11
conda activate lt3090
package:
  torch 2.3.1+cu118: `pip install torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cu118`
  torch 2.5.1+cu124 (alternatif lebih baru, driver 580 ok): `pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu124`
versi lain: 
  pip install numpy "opencv-python<4.9" tqdm matplotlib
  pip install -e src/lighttrack  # kalau ada (setup.py), atau sys.path cukup

# pastikan kernel pakai env ini di Jupyter: kernel -> Change kernel -> lt309
# verifikasi:
python -c "import torch; print(torch.__version__, torch.version.cuda); print(torch.backends.cudnn.version())"

## Setelah ganti env
- Notebook 35 pakai: TF32 ON, cuDNN tetap aktif, stack-crop tensor (1 from_numpy utk batch).
- Cek hang: 2 epoch dulu. Kalau masih hang --> normal (pindah ke tahap analisis berikutnya).
