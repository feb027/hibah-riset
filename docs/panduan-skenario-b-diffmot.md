# Panduan Skenario B — DiffMOT di PC Kampus (tanpa conda)

Target: PC kampus (RTX 4090), Jupyter terisolasi per-user (password), **tanpa conda/venv**.

Semua install memakai python dari env Jupyter yang sudah aktif.

## 1. Setup sekali

```bash
git clone https://github.com/feb027/hibah-riset
cd hibah-riset
python scripts/s2/setup_diffmot_pip.py
```

Script ini menggantikan notebook 10 (setup env + clone + bobot) untuk env pip-only:
- memakai torch yang sudah ada bila CUDA aktif (requirement DiffMOT tidak mengunci torch);
  kalau belum ada CUDA dan python ≤ 3.10 → install torch 2.0.1 dari index cu118
- clone DiffMOT / OC_SORT / TrackEval ke `external/`
- install YOLOX, deep-person-reid, fast_reid (editable) — **wajib walau YOLOX tidak
  dipakai deteksi**: kode DiffMOT mengimpornya saat load
- download 4 bobot rilis v1.0 (mot_epoch800.pt, dancetrack_epoch800.pt,
  mot20_sbs_S50.pth, dance_sbs_S50.pth)

Pitfall: `cython-bbox` rawan gagal build → coba `pip install cython-bbox --no-build-isolation`.

## 2. Data

```bash
export HF_TOKEN=hf_xxx            # token Read gratis — download jauh lebih cepat
python scripts/s2/run_skenario_b_ocsort.py --steps data,arrange
```

- **Dataset TETAP harus ada di kampus** (folder `data/` tidak ikut git) — download di sini
  atau salin dari PC rumah (jalur Tailscale/network).
- Download sudah hemat: MOT20 hanya train (test di-skip), DanceTrack hanya `val.zip`
  (test1/2.zip, train1/2.zip, *.xlsx di-skip).
- `arrange` mengekstrak val.zip, menyusun layout `data/s2/mot20/train` &
  `data/s2/dancetrack/val`, menulis `seqinfo.ini`, dan memverifikasi.

## 3. Deteksi — YOLO26 fine-tune (BUKAN YOLOX)

Taruh bobot Skenario A **`.pt`** (bukan `.onnx`) di `data/s2/weights/best.pt`:

- Deteksi pakai **YOLO26 fine-tune** hasil Skenario A — DiffMOT hanya membaca file
  deteksi (`det_dir`), detektor bawaan YOLOX **tidak dipakai**.
- **`.pt` untuk GPU** (kampus): ultralytics native CUDA, lebih cepat dan sederhana.
  `.onnx` hanya berguna untuk mempercepat CPU (PC rumah).

Lalu jalankan notebook `30_s2_gen_detections.ipynb` (kernel apa pun dari env ini):
menghasilkan **dua format sekaligus** — per-frame untuk DiffMOT
(`detections/{split}/{seq}/{frame:08d}.txt`) dan MOT-format untuk OC-SORT
(`det_mot/{split}/{seq}.txt`). Estimasi GPU: 2–5 menit untuk 4 + 25 sekuens.

## 4. Run DiffMOT

- `40_s2_diffmot_embeddings.ipynb` — patch `diffmot.py` (idempotent) + smoke ReID
- `50_s2_run_diffmot.ipynb` — run MOT20 (~7–10 mnt) & DanceTrack (~15–20 mnt) di 4090
- `70_s2_eval_trackeval.ipynb` — eval HOTA/IDF1/MOTA/IDSW/Frag → bandingkan baseline
  OC-SORT (MOT20: HOTA 37.5 / MOTA 56.1 / IDF1 44.7; DanceTrack: HOTA 28.4 /
  MOTA 71.4 / IDF1 26.6)

## Catatan versi

- torch 2.0.1 wajib dari `--index-url https://download.pytorch.org/whl/cu118`
  (wheel PyPI 2.0.1 rusak: hilang dependensi nvidia).
- DiffMOT dikembangkan dengan torch 2.0.1; torch lebih baru umumnya jalan untuk eval,
  tapi kalau import/forward error, pakai env python 3.9/3.10 + torch 2.0.1.
