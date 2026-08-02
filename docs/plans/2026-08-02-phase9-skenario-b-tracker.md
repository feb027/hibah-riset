# Phase 9 — Skenario B: Evaluasi Tracker (DiffMOT vs OC-SORT)

*Tanggal: 2026-08-02. Status: PLAN + SCAFFOLD (belum dieksekusi di GPU).*

## 1. Tujuan

Menilai stabilitas identitas tracker pada kerumunan padat, oklusi, dan gerak non-linear,
sesuai `docs/drafts/bab3_revisi_skenario_eksperimen.md` §S2:

- **Tracker**: DiffMOT (jalur robust, fokus utama — judul berbasis deep learning) vs OC-SORT (baseline efisien).
- **Data**: MOT20-train (4 sekuens, kepadatan ekstrem) + DanceTrack-val (25 sekuens, appearance seragam + gerak non-linear).
- **Metrik**: HOTA, IDF1, MOTA, ID switch, fragmentasi, runtime tracker.
- **Kesetaraan**: kedua tracker diberi deteksi yang SAMA (aturan emas perbandingan).

## 2. Ringkasan riset (fakta terverifikasi, 2026-08-02)

### 2.1 Download dataset

| Dataset | Sumber | Ukuran | Catatan verifikasi |
|---|---|---|---|
| MOT20 | Kaggle `ismailelbouknify/mot-20` (isi BELUM terverifikasi), HF `Lekim89/MOT20`, resmi `motchallenge.net/data/MOT20` (registrasi) | ±5 GB | **Wajib** `scripts/data_prep/verify_mot_dataset.py` — banyak mirror Kaggle kehilangan track ID (jadi dataset deteksi, tak bisa hitung HOTA/IDF1) |
| DanceTrack | HF `noahcao/dancetrack` (resmi; Google Drive deprecated) | 17,7 GB total; unduh tanpa `test/*` | cc-by-4.0; val = 25 sekuens dengan GT publik |

Keputusan: coba Kaggle dulu (ingatan user benar, dataset-nya ada), fallback berantai HF → resmi.
`verify_mot_dataset.py` sudah ada dan memang dibuat untuk jebakan mirror ini (cek kolom ID bertahan antar frame).

### 2.2 DiffMOT (`Kroery/DiffMOT`, CVPR2024, MIT) — fokus utama

- **Env**: python 3.9, `torch==2.0.1 torchvision==0.15.2` **WAJIB dari index CUDA**
  (`--index-url https://download.pytorch.org/whl/cu118`) — wheel PyPI 2.0.1 RUSAK
  (kehilangan dependensi nvidia → `libnvrtc.so not found`). RTX 4090 (sm_89) didukung cu118.
- **Deps**: `einops easydict tensorboardX tqdm lap cython-bbox fvcore opencv-python scipy numpy pyyaml argparse`
  + 3 external `setup.py develop`: YOLOX, deep-person-reid, fast_reid. `cython-bbox` rawan gagal
  compile di GCC baru → fallback build dari source.
- **Bobot rilis v1.0** (path relatif ke `external/diffmot/`):
  - Motion D²MP: `MOT_epoch800.pt` (MOT17+MOT20 sekaligus) → rename `mot_epoch800.pt`,
    `DanceTrack_epoch800.pt` → rename `dancetrack_epoch800.pt`
  - ReID (FastReID): `mot20_sbs_S50.pth`, `dance_sbs_S50.pth` → `external/weights/`
  - Checkpoint motion dimuat dari `./experiments/{eval_expname}/{dataset}_epoch{epoch}.pt`
    (`dataset` = arg `--dataset`: `mot` / `dancetrack`).
- **Format deteksi**: `det_dir/{seq}/{frame}.txt` per frame, tiap baris 6 kolom CSV;
  **kolom 1 dibuang kode** (`np.loadtxt(...).reshape(-1,6)[:,1:6]`) → tersisa `x,y,w,h,score` (tlwh).
  Nama file di-sort; gambar di-match **per indeks** (`imgs[i]`) → padding nol konsisten.
- **Alur ReID (paling subtle)**: `tracker/embedding.py` cache embedding per sekuens ke
  `{reid_dir}/{seq}_embedding.pkl`. Di `diffmot.py` eval, `cv2.imread` DIKOMENTARI → tanpa cache
  dan tanpa patch, `compute_embedding(img=None,...)` crash. Solusi: **patch 2 baris** —
  aktifkan `img = cv2.imread(im_path)` dan teruskan `img` ke `tracker.update(...)`. Cache
  terisi otomatis saat run pertama (dump_cache per sekuens), run berikutnya reuse.
  Cache harus match deteksi persis (beda jumlah deteksi → RuntimeError; jangan ganti deteksi
  setelah cache dibuat).
- **Config `*_test.yaml` STALE** — semuanya copy-paste path `/mnt/8T/home/estar/...` DanceTrack
  (bahkan `mot17_test.yaml` det_dir-nya DanceTrack). Wajib tulis config sendiri. Threshold:
  MOT20 high 0.4 / low 0.1 / w_assoc_emb 2.2 / aw_param 1.7; DanceTrack 0.6 / 0.4 / 2.2 / 1.7.
- **`data_dir` aman untuk eval**: `DiffMOTDataset.__init__` di-guard `if os.path.isdir(path)` —
  evaluasi tidak butuh `trackers_gt` (produk `*_data_process.py` yang hanya untuk training).
- **Struktur path wajib**: kode melakukan `det_dir.replace('/detections/', '/')` untuk mencari
  gambar → layout harus `{root}/{dataset}/{split}/{seq}/img1/` + `{root}/{dataset}/detections/{split}/{seq}/`.
- **Output**: `{save_dir}/{seq}.txt` format MOT `frame,id,x,y,w,h,1,-1,-1,-1` (via `tracking_utils/io.py`).
- Runtime: 22,7 FPS (YOLOX-X, RTX 3090) → MOT20-train ±8,9k frame ≈ 7–10 mnt, DanceTrack-val ≈ 15–20 mnt di 4090.
- Risiko: 26 open issue; env lama. Mitigasi: install pinned, smoke test (load ReID + 1 sekuens) sebelum run penuh.

### 2.3 OC-SORT (`noahcao/OC_SORT`, CVPR2023)

- `tools/run_ocsort_public.py` **tidak support MOT** (branch cuma kitti/bdd/headtrack, else `assert(0)`).
- Template branch `headtrack`: baca `seq.txt` MOT 10 kolom → dets xywh→xyxy, scores col 6 →
  `tracker.update_public(dets, cates, scores)` → tulis `frame,id,x,y,w,h,1,-1,-1,-1`.
- Solusi: runner sendiri `scripts/s2/run_ocsort_mot.py` (pola sama, tanpa menyentuh repo mereka).
- Murni motion (tanpa ReID) → murah: asosiasi 700 FPS CPU. Param: `track_thresh, iou_thresh,
  delta_t, min_hits, max_age, asso_func, inertia` (default repo: det 0.3, iou 0.3, delta_t 3,
  min_hits 3, inertia 0.2).

### 2.4 TrackEval (`JonathonLuiten/TrackEval`)

- MOT20: `run_mot_challenge.py --BENCHMARK MOT20 --SPLIT_TO_EVAL train` (GT publik di train).
- DanceTrack: script yang sama dengan `--GT_FOLDER <dance>/val --SEQMAP_FILE <seqmap>` —
  seqmap digenerate dinamis dari isi folder val (25 nama sekuens), tidak bergantung file dari repo DanceTrack.
- Format hasil tracker: `frame,id,x,y,w,h,conf,-1,-1,-1`.

## 3. Layout direktori

```
data/                        (gitignored)
  s2/
    weights/                 best.pt hasil fine-tune Skenario A (di-download dari Colab/GPU server)
    mot20/train/MOT20-{01,02,03,05}/img1/ + gt/ + seqinfo.ini
    mot20/detections/train/MOT20-XX/000001.txt ...
    dancetrack/val/dancetrack00XX/img1/ + gt/ + seqinfo.ini
    dancetrack/detections/val/dancetrack00XX/00000001.txt ...
external/                    (gitignored — clone repo pihak ketiga)
  diffmot/                   Kroery/DiffMOT (+ experiments/ berisi checkpoint, external/weights/)
  OC_SORT/                   noahcao/OC_SORT
  TrackEval/                 JonathonLuiten/TrackEval
experiments/s2_tracker/      (committed — hasil, csv, plot)
scripts/s2/
  run_ocsort_mot.py          runner OC-SORT (det.txt MOT → hasil TrackEval)
  patch_diffmot_eval.py      patch diffmot.py agar mengirim img ke tracker (embedding cache)
notebooks/
  10_s2_setup_env.ipynb      2 conda env: s2-main (ultralytics+TrackEval+OC-SORT), s2-diffmot (py3.9+torch2.0.1 cu118)
  20_s2_download_data.ipynb  MOT20 (Kaggle→HF→resmi + verify) + DanceTrack (HF, tanpa test)
  30_s2_gen_detections.ipynb YOLO fine-tune → deteksi 2 format (DiffMOT per-frame + MOT det.txt) — SATU deteksi utk dua tracker
  40_s2_diffmot_embeddings.ipynb patch + smoke: load ReID weight, forward dummy, validasi CUDA
  50_s2_run_diffmot.ipynb    tulis config, jalankan tracking MOT20 + DanceTrack
  60_s2_run_ocsort.ipynb     jalankan runner OC-SORT
  70_s2_eval_trackeval.ipynb eval HOTA/IDF1/MOTA/IDSW/Frag (MOT20 + DanceTrack), simpan csv
  80_s2_analyze.ipynb        tabel pembanding, plot, bahan laporan
```

## 4. Urutan eksekusi di PC kampus (RTX 4090 / i9-14900K / 32 GB, Jupyter via Tailscale)

1. `10` — env (sekali). Verifikasi `nvidia-smi`, import torch di kedua env, smoke model.
2. `20` — data (sekali, ±15 GB). Verify MOT20 WAJIB lulus.
3. `30` — deteksi dengan bobot fine-tune (butuh `data/s2/weights/*.pt` dari Colab).
4. `40` — patch + smoke ReID DiffMOT (gagal cepat, sebelum buang waktu).
5. `50` + `60` — tracking. **Urutan penting: 50 sebelum 40-jalur-lanjutan; 40 bisa jadi bagian 50.**
6. `70` — eval. `80` — analisis + draft laporan `docs/reports/laporan-skenario-b-*.md`.

Estimasi disk: data ±15 GB + deteksi/embedding ±2 GB. RAM 32 GB cukup (MOT20-04 densitas
246 org/frame tetap OK di 4090).

## 5. Risiko & mitigasi

| Risiko | Mitigasi |
|---|---|
| Kaggle MOT20 tanpa track ID | `verify_mot_dataset.py` wajib; fallback HF `Lekim89/MOT20` → resmi |
| torch 2.0.1 PyPI rusak | install dari index cu118 |
| cython-bbox / fast_reid gagal build | build dari source; smoke test sebelum data besar |
| Embedding cache mismatch | urutan deteksi→embedding→tracking tetap; jangan regenerasi deteksi tanpa hapus cache |
| Config DiffMOT stale | tulis config sendiri (notebook 50) |
| seqinfo.ini hilang di mirror DanceTrack | script 20 cek; synthesize dari dimensi frame jika perlu |
| DiffMOT 26 open issue | install pinned persis; smoke 1 sekuens dulu |

## 6. Yang masih DIVERIFIKASI saat runtime (bukan asumsi)

- Isi Kaggle MOT20 (apakah gt.txt punya ID bertahan) — runtime verify.
- Kehadiran `seqinfo.ini` di mirror DanceTrack HF — script cek + synthesize.
- Build `cython-bbox`/`fast_reid` di GCC mesin kampus — smoke test.
- Akses jaringan kampus ke Kaggle/HF (perlu kaggle.json / HF token bila private).
- Kesesuaian bobot `MOT_epoch800.pt` untuk MOT20 (paper: dilatih MOT17+MOT20 bersamaan — [S021]).

## 7. Referensi

- DiffMOT: Lv et al., CVPR2024, arXiv:2403.02075 — [S021]. Repo: github.com/Kroery/DiffMOT
- OC-SORT: Cao et al., CVPR2023, arXiv:2203.14360 — [S024]. Repo: github.com/noahcao/OC_SORT
- MOT20: Dendorfer et al., 2020 — [S036]. DanceTrack: Sun et al., CVPR2022 — [S037]
- TrackEval: github.com/JonathonLuiten/TrackEval
