# Panduan Skenario B — DiffMOT di PC Kampus (JupyterHub, tanpa conda)

Target: PC kampus (RTX 4090), Jupyter terisolasi per-user (password), **tanpa conda/venv**.
Semua langkah lewat notebook — env = kernel Jupyter yang sudah ada.

## Alur

```
10_s2_setup_env.ipynb        env pip-only + clone DiffMOT/OC_SORT/TrackEval + bobot (sekali)
20_s2_download_data.ipynb    data MOT20-train + DanceTrack val (HF; val.zip di-extract di notebook)
30_s2_gen_detections.ipynb   deteksi YOLO26 fine-tune -> dua format (DiffMOT per-frame + MOT utk OC-SORT)
40_s2_diffmot_embeddings.ipynb  patch diffmot.py + smoke ReID
50_s2_run_diffmot.ipynb      run DiffMOT mot20 (~7-10 mnt) + dance (~15-20 mnt) di 4090
70_s2_eval_trackeval.ipynb   eval HOTA/IDF1/MOTA/IDSW/Frag
```

## 1. Setup (notebook 10)

- Semua `pip install` masuk ke env kernel saat ini — **tidak bikin env terpisah**.
- `torch` yang sudah ada TIDAK ditimpa bila CUDA aktif (requirement DiffMOT tidak mengunci torch).
- Clone DiffMOT / OC_SORT / TrackEval + `git submodule update --init --recursive`.
- Install YOLOX, deep-person-reid, fast_reid (editable) — **wajib walau YOLOX tidak
  dipakai deteksi**: kode DiffMOT mengimpornya saat load.
- Download 4 bobot rilis v1.0 (mot_epoch800.pt, dancetrack_epoch800.pt,
  mot20_sbs_S50.pth, dance_sbs_S50.pth).

Pitfall: `cython-bbox` rawan gagal build → `pip install cython-bbox --no-build-isolation`.
Fallback torch: kalau DiffMOT error saat run, pin `torch==2.0.1` dari index cu118
(python ≤ 3.10; wheel PyPI 2.0.1 rusak).

## 2. Data (notebook 20)

- **Dataset TETAP harus ada di kampus** (folder `data/` tidak ikut git) — download di sini
  atau salin folder `data/s2` dari PC rumah (jalur Tailscale/network).
- Download sudah hemat: MOT20 hanya train (`test/*` di-skip), DanceTrack hanya `val.zip`
  (`test1/2.zip`, `train1/2.zip`, `*.xlsx` di-skip).
- `val.zip` di-extract otomatis di dalam notebook (sel align), lalu ditautkan ke
  `data/s2/dancetrack/val`; seqinfo.ini disynthesize bila hilang; verify WAJIB lulus.
- Untuk download cepat set env `HF_TOKEN` (token Read gratis).

## 3. Deteksi — YOLO26 fine-tune (BUKAN YOLOX)

Taruh bobot Skenario A **`.pt`** (bukan `.onnx`) di `data/s2/weights/best.pt`:

- Deteksi pakai **YOLO26 fine-tune** hasil Skenario A — DiffMOT hanya membaca file
  deteksi (`det_dir`), detektor bawaan YOLOX **tidak dipakai**.
- **`.pt` untuk GPU** (kampus): ultralytics native CUDA. `.onnx` hanya untuk CPU (PC rumah).
- Notebook 30 menghasilkan **dua format sekaligus**: per-frame untuk DiffMOT
  (`detections/{split}/{seq}/{frame:08d}.txt`) dan MOT-format untuk OC-SORT
  (`det_mot/{split}/{seq}.txt`). Estimasi GPU: 2–5 menit untuk 4 + 25 sekuens.

## 4. Hasil & baseline

| benchmark  | tracker | HOTA   | MOTA   | IDF1   | IDSW | Frag  |
|------------|---------|--------|--------|--------|------|-------|
| MOT20      | OC-SORT | 37.46  | 56.13  | 44.67  | 7933 | 15033 |
| DanceTrack | OC-SORT | 28.39  | 71.38  | 26.63  | 6701 | 6936  |

Hasil DiffMOT masuk `experiments/s2_tracker/diffmot_results/` → bandingkan dengan baris OC-SORT.
