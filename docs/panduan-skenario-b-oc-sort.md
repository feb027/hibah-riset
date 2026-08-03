# Panduan Skenario B — Jalur OC-SORT (PC Rumah, CPU-only)

*Tanggal: 2026-08-02. Berlaku untuk PC rumah **Windows 11** i5-12400F / 16 GB / RX6600
(GPU AMD tidak dipakai — semua langkah CPU). Jangan jalankan beban berat ini di VPS
(4 vCPU QEMU, 7,3 GB RAM).*

## 0. Tujuan

Dapat angka evaluasi tracker OC-SORT pada MOT20-train + DanceTrack-val:
**HOTA, IDF1, MOTA, IDSW, Frag** — dengan deteksi dari bobot YOLO fine-tune Skenario A.
Ini progres nyata Skenario B (jalur baseline). DiffMOT (jalur DL utama) tetap butuh GPU
(Colab / 4090 kampus) — panduan terpisah (notebook `40–50_s2_*`).

## 1. Prasyarat (PC rumah, Windows 11)

- Python 3.10–3.12 dari python.org — centang **"Add python.exe to PATH"** saat install.
- Git for Windows (`winget install Git.Git` atau git-scm.com).
- Disk kosong ±25 GB.
- Bobot Skenario A: `best.pt` (yolo26n/yolov10n/yolov11n) — **download dari Colab/GPU server
  dulu**, taruh di `data/s2/weights/`.
- Repo: `git clone https://github.com/feb027/hibah-riset && cd hibah-riset` (atau `git pull`).
- Semua perintah di bawah dijalankan di **PowerShell** (bukan cmd).

## 2. Setup environment (sekali)

```powershell
cd hibah-riset
python -m venv .venv-s2
.\.venv-s2\Scripts\Activate.ps1

# torch CPU dulu (hindari wheel CUDA ~2 GB)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt trackeval huggingface_hub
```

Verifikasi:
```powershell
python -c "import torch, ultralytics, trackeval; print(torch.__version__, ultralytics.__version__)"
```

## 3. Download data

### Opsi A — Hugging Face (disarankan, tanpa kredensial)

```powershell
.\.venv-s2\Scripts\Activate.ps1

# MOT20 (mirror lengkap, ada gt.txt ber-track-ID)
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Lekim89/MOT20', repo_type='dataset', local_dir='data/s2/mot20_hf')"

# DanceTrack (resmi, cc-by-4.0; unduh tanpa split test)
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='noahcao/dancetrack', repo_type='dataset', local_dir='data/s2/dancetrack_hf', ignore_patterns=['test/*'])"
```

Estimasi: MOT20 ±5 GB, DanceTrack ±12 GB (tanpa test). Waktu tergantung koneksi.
MOT20 butuh `~/.kaggle/kaggle.json`? Tidak — opsi A ini bebas kredensial.

### Opsi B — Kaggle (hanya jika punya kaggle.json)

```powershell
pip install kaggle
kaggle datasets download -d ismailelbouknify/mot-20 -p data/s2/mot20_raw
Expand-Archive -Path data/s2/mot20_raw/mot-20.zip -DestinationPath data/s2/mot20_raw/extracted
```

⚠️ Mirror Kaggle **sering kehilangan track ID** (jadi dataset deteksi). Apapun sumbernya,
langkah `arrange` menjalankan `verify_mot_dataset.py` — kalau gagal, ganti sumber (HF/resmi
motchallenge.net) lalu ulangi.

## 4. Jalankan

```powershell
.\.venv-s2\Scripts\Activate.ps1
python scripts/s2/run_skenario_b_ocsort.py --steps arrange,detect,track,eval
```

Apa yang terjadi per langkah:

| Langkah | Isi | Estimasi (i5-12400F) |
|---|---|---|
| `arrange` | susun sekuens ke `data/s2/{mot20,train|dancetrack,val}` + seqinfo.ini + verify | 1–2 mnt |
| `detect` | YOLO fine-tune (CPU) atas ±35k frame → `det_mot/` + `detections/` | 15–25 mnt |
| `track` | OC-SORT (asosiasi 700 FPS CPU) → `experiments/s2_tracker/ocsort_results/` | 2–5 mnt |
| `eval` | TrackEval → `experiments/s2_tracker/eval_results.csv` | 2–5 mnt |

Perintah berguna lain:
```powershell
# unduh data juga (satu perintah penuh; butuh bandwidth besar)
python scripts/s2/run_skenario_b_ocsort.py --steps data,arrange,detect,track,eval

# ulangi hanya deteksi (mis. ganti bobot)
python scripts/s2/run_skenario_b_ocsort.py --steps detect --force --weights data/s2/weights/best_yolo26n.pt

# evaluasi ulang saja (deteksi & tracking sudah ada)
python scripts/s2/run_skenario_b_ocsort.py --steps eval

# selaraskan param OC-SORT (min-conf = buang deteksi ber-score rendah)
python scripts/s2/run_skenario_b_ocsort.py --steps track --track-thresh 0.4 --min-conf 0.4 --iou-thresh 0.3
```

Semua langkah idempotent: output yang sudah ada dilewati; `--force` untuk mengulang.

## 5. Hasil

- `experiments/s2_tracker/eval_results.csv` — tabel metrik per dataset:
  `dataset, tracker, cls, HOTA, MOTA, IDF1, IDSW, Frag`.
- `experiments/s2_tracker/detection_stats.csv` — statistik deteksi per sekuens.
- `experiments/s2_tracker/ocsort_results/{mot20,dancetrack}/*.txt` — hasil track format MOT.

Catatan jujur untuk laporan: `DO_PREPROC=False` (tanpa penghapusan distractor) → angka tidak
persis sama dengan leaderboard MOTChallenge, tapi konsisten → valid untuk perbandingan tracker.

## 6. Troubleshooting

| Masalah | Solusi |
|---|---|
| `verify_mot_dataset.py` gagal | Mirror tanpa track ID — ganti sumber: HF `Lekim89/MOT20` / resmi `motchallenge.net` |
| MemoryError saat deteksi | Turunkan `--imgsz 480` atau `--conf 0.1` |
| `torch` wheel besar | Sudah dicegah: install dari index CPU (langkah 2) |
| `cython-bbox` gagal build | Tidak dipakai jalur OC-SORT (hanya DiffMOT) — abaikan |
| `pip` tidak dikenali | Pakai `py -m pip ...` atau pastikan python.exe di PATH |
| Activate.ps1 diblokir eksekusi | PowerShell: `Set-ExecutionPolicy -Scope Process Bypass` lalu ulangi |
| Ingin lebih cepat | Export bobot ke ONNX (`yolo export model=... format=onnx`) + `--conf` naik; deteksi CPU bisa ~2× lebih cepat |

## 7. Setelah ini

1. Salin `eval_results.csv` ke repo (sudah di `experiments/s2_tracker/`, committed).
2. Tulis `docs/reports/laporan-skenario-b-tracker.md` (pola: laporan-skenario-a).
3. DiffMOT: butuh GPU — jalankan notebook `40–50_s2_*` di Colab (T4) atau 4090 kampus
   (setup ±15 mnt, run ±2–3 jam). Setelah itu tabel B lengkap (2 tracker × 2 dataset).
4. Skenario C (counting logic) & prototype: CPU-friendly, bisa jalan di PC rumah.

## 8. Referensi

- Plan: `docs/plans/2026-08-02-phase9-skenario-b-tracker.md`
- Script: `scripts/s2/run_skenario_b_ocsort.py`, `scripts/s2/run_ocsort_mot.py`
- Dataset: MOT20 [S036], DanceTrack [S037]; OC-SORT [S024]; TrackEval (JonathonLuiten)
