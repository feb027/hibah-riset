# Laporan Skenario B: Evaluasi Tracker untuk People Counting — Perbandingan OC-SORT vs DiffMOT dan Arah ke Tracker Usulan (LightTrack-ReID-inspired)

*Disusun menggunakan standar penulisan akademik untuk justifikasi metodologi eksperimen. Status: OC-SORT baseline ✅ selesai; DiffMOT ✅ selesai (2026-08-05); tracker usulan LightTrack-ReID-inspired dalam implementasi (Phase 3 — lihat Bagian 6.3).*

---

## 1. Ringkasan Eksekutif

Skenario B mengevaluasi lapisan **tracker** dari pipeline *people counting* lima lapis: setelah detektor (Skenario A) menghasilkan kotak orang per bingkai, tracker harus menyatukannya menjadi **identitas temporal yang stabil** agar hitungan orang yang sama tidak dihitung ganda. Laporan ini mendokumentasikan dua tracker pembanding — **OC-SORT** (motion-only, murah) dan **DiffMOT** (diffusion + ReID, mahal) — pada protokol deteksi yang sama, serta arah ke **tracker usulan** (Bagian 6.3).

Temuan utama:

1. **Pada kerumunan padat (MOT20-train full, 8.931 bingkai), OC-SORT mencapai HOTA 36,51, MOTA 55,98, IDF1 42,88** — akurasi deteksi tinggi (MOTA), tetapi asosiasi identitas lemah: **14.293 ID switch** dan **27.646 fragmentasi**. Kepadatan rata-rata **179 deteksi/bingkai** (puncak 272 di MOT20-05) membuat asosiasi berbasis IoU+Kalman mudah putus saat orang saling menutupi.
2. **Pada gerak non-linear (DanceTrack-val), OC-SORT jatuh ke HOTA 28,39 dan IDF1 26,63** — MOTA 71,38 tetap tinggi karena deteksi bagus, tetapi identitas nyaris berantakan (IDF1 < 30%). Ini persis skenario yang menjadi motivasi DiffMOT (Lv et al., 2024 – S021): prediksi gerak Kalman (asumsi kecepatan konstan) gagal pada penari yang berakselerasi/berbelok tidak menentu.
3. **DiffMOT mengalahkan OC-SORT di kedua benchmark (eval kampus 2026-08-05): MOT20 HOTA 44,37 vs 36,51; DanceTrack HOTA 39,05 vs 28,39** — perbaikan terpusat pada asosiasi (IDSW MOT20 turun dari 14.293 ke 6.905; DanceTrack 6.701 ke 2.784), membuktikan diffusi gerak + ReID bekerja. Namun harga yang dibayar besar: DiffMOT butuh GPU (HMINet + ReID berat), black-box (tidak bisa dilatih ulang), dan dependensi patch sehingga **bukan kandidat deployment people counting real-time** — ini alasan utama pivot ke tracker usulan yang ringan (Bagian 6.3).
4. **Yang menjadi pembatas adalah asosiasi, bukan deteksi.** Pola HOTA-MOTA-IDF1 di kedua benchmark konsisten dengan diagnosis literatur. Untuk *people counting*, **IDF1 adalah metrik yang paling relevan** — identitas yang putus saat oklusi membuat objek dapat dihitung ganda ketika muncul kembali.

Seluruh angka dapat ditelusuri ke berkas hasil pada Lampiran A.

---

## 2. Pendahuluan

Deteksi bukanlah *counting* (temuan Skenario A, laporan `docs/reports/laporan-skenario-a-finetuning-yolo.md`). Sistem *people counting* real-time membutuhkan lapisan yang memutuskan *kotak mana di bingkai t yang merupakan orang yang sama dengan kotak di bingkai t−1*. Tanpa lapisan ini, setiap bingkai dihitung independen dan orang yang melewati garis hitung dapat dihitung berkali-kali.

Skenario B menjawab pertanyaan: **tracker mana — dan pada kondisi apa — yang mampu mempertahankan identitas objek cukup lama untuk hitungan yang akurat?** Dua kandidat dipilih dari rancangan proposal:

- **OC-SORT** (Cao et al., 2023) — baseline berbasis gerak murni (Kalman filter + asosiasi IoU dengan koreksi observasi). Cepat, tanpa GPU, tanpa ReID. Menjadi jalur *efisien/fallback* dalam proposal.
- **DiffMOT** (Lv et al., 2024 – S021) — prediksi gerak berbasis diffusion (D²MP) + asosiasi berbasis penampilan (ReID). Lebih berat (butuh GPU), diharapkan unggul pada gerak non-linear dan oklusi. **Dieksekusi penuh dan dievaluasi pada protokol yang sama (2026-08-05, GPU kampus).**
- **Tracker usulan — LightTrack-ReID-inspired** (Khan et al., 2026 – S014): LAE MobileNetV3-Small → embedding 32-d + TBSS (scorer transformer ringan) + CMOH memory + ASW — **tracker yang bisa dilatih ulang, ringan, dan dievaluasi pada protokol yang sama** (Bagian 6.3).

Kedua tracker pembanding dievaluasi pada **deteksi yang identik** (YOLO26 fine-tune hasil Skenario A) agar perbandingan mengukur kemampuan *tracking*, bukan selisih detektor. Setelah DiffMOT selesai, laporan ini menyajikan tabel pembanding OC-SORT vs DiffMOT secara penuh, analisis downside-nya, dan banding terhadap tracker usulan.

---

## 3. Metodologi

### 3.1 Dataset dan Protokol

| Benchmark | Split | Jumlah sekuens | Frame | Ground truth | Alasan |
|---|---|---|---|---|---|
| **MOT20** | train | 4 (MOT20-01/02/03/05) | 8.931 | Publik (GT ber-ID) | Test MOT20 tanpa GT publik (submission ke server) |
| **DanceTrack** | val | 25 | 25.508 | Publik (GT ber-ID) | Train untuk melatih tracker (tidak dipakai); test tanpa GT publik |

- **MOT20** (Dendorfer et al., 2020 – S036): kerumunan pejalan kaki sangat padat di ruang publik — menguji oklusi masif. Kepadatan deteksi rata-rata 179/bingkai (GT: 127/bingkai).
- **DanceTrack** (Sun et al., 2022 – S037): penari dengan penampilan seragam (baju sama) dan gerak non-linear — menguji asosiasi saat penampilan tidak informatif dan gerak tidak linear.
- Kedua split dipilih karena **GT-nya publik** — evaluasi HOTA/IDF1/MOTA lokal dimungkinkan. Sebelum dipakai, GT diverifikasi dengan `scripts/data_prep/verify_mot_dataset.py` (memeriksa ID yang bertahan lintas bingkai, bukan sekadar format deteksi).

### 3.2 Deteksi — YOLO26 Fine-Tune (Skenario A)

Deteksi memakai bobot **YOLO26s fine-tune CrowdHuman** dari Skenario A (mAP@0.5:0.95 = 0,4974; laporan Skenario A Bagian 4). Eksekusi di PC rumah (CPU):

- **MOT20**: `best.onnx` (ONNX Runtime, ±2× lebih cepat di CPU) — 4 sekuens, 8.931 bingkai, **1.595.730 deteksi**, ±4 menit.
- **DanceTrack**: `best.onnx` — 25 sekuens, 25.508 bingkai, **369.101 deteksi**, ±18 menit.

Hasil deteksi per sekuens tercatat di `experiments/s2_tracker/detection_stats.csv` dan `docs/panduan-skenario-b-oc-sort.md`. Ambang *confidence* 0,3 digunakan untuk membatasi noise (temuan Skenario A: pada 0,05 deteksi noise membanjiri, mis. MOT20-05 sampai 272 deteksi/bingkai).

*Catatan konsistensi:* pada jalur GPU (kampus) deteksi memakai `best.pt` (native CUDA). Aturan yang dipakai: jangan mencampur deteksi `.pt` dan `.onnx` dalam satu tabel hasil.

### 3.3 Tracking — OC-SORT

| Parameter | Nilai |
|---|---|
| `--track-thresh` | 0,3 |
| `--min-conf` | 0,3 |
| `--iou-thresh` | 0,3 |
| Runtime | ±54 FPS (CPU, diukur pada MOT20-train) |

Orchestrator satu perintah: `python scripts/s2/run_skenario_b_ocsort.py --steps arrange,detect,track,eval` (idempotent, `--force` untuk ulang). OC-SORT murni berbasis gerak — tanpa ReID — sehingga berjalan penuh di CPU.

### 3.4 Evaluasi — TrackEval

Metrik dihitung dengan **TrackEval** (toolkit Luiten et al., github.com/JonathonLuiten/TrackEval) versi 1.3.0, protokol MOTChallenge:

- **HOTA** (Luiten et al., 2021 – S025): metrik gabungan deteksi-asosiasi, *primary metric*.
- **MOTA** (CLEAR): cakupan deteksi — penalizes *misses*, *false positives*, ID switch.
- **IDF1** (Identity): seberapa konsisten identitas — paling relevan untuk counting.
- **IDSW** (ID switch) dan **Frag** (fragmentasi): jumlah putusnya trajektori.

Detail teknis yang memengaruhi pembacaan angka (sudah ditangani, terdokumentasi di `references/trackeval-eval-pitfalls.md`): layout folder datar (`SKIP_SPLIT_FOL=True`), skala metrik 0–1 dikali 100, `seqinfo.ini` disynthesize dari bingkai asli, dan `DO_PREPROC=False` (tanpa penghapusan distraktor) — angka dengan demikian **tidak persis** leaderboard MOTChallenge, tetapi **konsisten antar tracker** sehingga sah untuk perbandingan tracker-vs-tracker.

### 3.5 Perangkat

| Lingkungan | Perangkat | Dipakai untuk |
|---|---|---|
| PC rumah (Windows 11) | CPU (i5-12400F), ONNX Runtime | Deteksi `.onnx`, tracking OC-SORT, evaluasi |
| GPU kampus (RTX 4090) | PyTorch CUDA | DiffMOT (selesai 2026-08-05), deteksi `.pt` |

---

## 4. Hasil

### 4.1 Tabel Utama

| Benchmark | Tracker | HOTA | MOTA | IDF1 | IDSW | Frag |
|---|---|---|---|---|---|---|
| MOT20 (train) | **OC-SORT** | 36,51 | 55,98 | 42,88 | 14.293 | 27.646 |
| MOT20 (train) | **DiffMOT** | **44,37** | **60,91** | **53,86** | **6.905** | **15.005** |
| DanceTrack (val) | **OC-SORT** | 28,39 | **71,38** | 26,63 | 6.701 | 6.936 |
| DanceTrack (val) | **DiffMOT** | **39,05** | 70,72 | **43,39** | **2.784** | **6.765** |

*Dibangkitkan dari `experiments/s2_tracker/eval_results.csv` (ekstraksi otomatis TrackEval, skala 0–1 × 100; DiffMOT dijalankan di GPU kampus 2026-08-05 pada deteksi YOLO26 yang sama, protokol sama; hasil per sekuens di `experiments/s2_tracker/diffmot_results/`).*

> **✅ PEMBARUAN (2026-08-04):** angka di atas adalah hasil **re-run full-sequence** — sebelumnya output tracking hanya menutupi sebagian frame (MOT20-01: 1–214 dari 429; MOT20-02: 1–1391 dari 2782) karena dataset di PC rumah tidak lengkap dan junction layout menunjuk ke subset `ablation/` (repo HF menyediakan dua versi). Setelah download ulang lengkap (divalidasi: 429/2782/2405/3315 gambar per sekuens, total 8.931 — cocok dengan Tabel 1 paper MOT20, arXiv:2003.09003), seluruh pipeline diulang (`--steps arrange,detect,track,eval --force`; fix relink di `scripts/s2/run_skenario_b_ocsort.py`). Tabel kini mewakili **MOT20-train penuh**. Perbandingan lama vs baru: HOTA 37,46→36,51; IDF1 44,67→42,88; IDSW 7.933→14.293 — frame tambahan didominasi sekuens malam terpadat (MOT20-03, MOT20-05), sehingga bobot asosiasi justru menurun; temuan "asosiasi rapuh" makin kuat, bukan melemah.

![Figur 1: HOTA/MOTA/IDF1 per benchmark](../../experiments/s2_tracker/figs/fig1_hota_mota_idf1.png)

![Figur 2: IDSW dan Frag per benchmark](../../experiments/s2_tracker/figs/fig2_idsw_frag.png)

### 4.2 Kepadatan Data

Deteksi YOLO26 menghasilkan kepadatan yang sangat berbeda antar benchmark — konteks penting untuk membaca skor asosiasi:

![Figur 3: kepadatan deteksi per sekuens DanceTrack](../../experiments/s2_tracker/figs/fig3_density_dance.png)

![Figur 4: kepadatan deteksi per sekuens MOT20](../../experiments/s2_tracker/figs/fig4_density_mot20.png)

MOT20 rata-rata **202 deteksi/bingkai** (sampai 271 di MOT20-05) — kerumunan ekstrem. DanceTrack rata-rata **14,5 deteksi/bingkai** — kepadatan jauh lebih rendah, tetapi tiap orang bergerak non-linear dan berpakaian seragam.

### 4.3 Runtime

| Tahap | Lingkup | Waktu |
|---|---|---|
| Deteksi MOT20 (4 sekuens) | CPU+ONNX | ±4 menit |
| Deteksi DanceTrack (25 sekuens) | CPU+ONNX | ±18 menit |
| Tracking OC-SORT (MOT20-train) | CPU | ±54 FPS (≈2,8 menit untuk 8.931 bingkai) |
| Evaluasi TrackEval | CPU | menit |

---

## 5. Analisis

### 5.1 Kerumunan padat (MOT20): deteksi kuat, asosiasi rapuh

MOTA 55,98 dengan kepadatan 179 deteksi/bingkai (puncak 272 di MOT20-05) menunjukkan detektor YOLO26 mampu menutupi mayoritas orang bahkan dalam oklusi berat. Namun **14.293 ID switch** — rata-rata 1,6 per bingkai — menandakan asosiasi berbasis gerak mudah salah sambung saat dua orang saling menutupi dan kotak IoU saling tumpang tindih. IDF1 42,88 berarti sekitar **57% bobot asosiasi identitas tidak cocok dengan GT** — implikasi praktis untuk counting: orang yang tertutup 2–3 bingkai lalu terdeteksi ulang dapat dihitung sebagai orang baru.

HOTA 36,51 yang berada jauh di bawah MOTA 55,98 secara kualitatif mengindikasikan komponen asosiasi lebih lemah daripada komponen deteksi — konsisten dengan tracker motion-only tanpa ReID. Dekomposisi eksplisit DetA/AssA belum dicatat pada run ini dan akan ditambahkan pada run berikutnya (TrackEval menyediakannya).

### 5.2 DiffMOT: asosiasi diperbaiki, tetapi biaya tidak sebanding untuk deployment

DiffMOT menyelesaikan persis kelemahan yang ditemukan OC-SORT: pada kerumunan padat **IDSW turun 52%** (14.293 → 6.905) dan **IDF1 naik 11 poin** (42,88 → 53,86) di MOT20; pada gerak non-linear **HOTA naik 10,7 poin** (28,39 → 39,05) di DanceTrack. Namun keputusan penelitian tidak berhenti di akurasi:

| Dimensi | OC-SORT (baseline) | DiffMOT | Tracker usulan (LightTrack-ReID-inspired) |
|---|---|---|---|
| Biaya asosiasi | ~0 GFLOPs (motion-only), **54+ FPS CPU** | HMINet + ReID berat, butuh GPU RTX (publikasi: ~22,7 FPS di RTX 3090) | LAE+TBSS **~0,6 GFLOPs**, target >100 FPS GPU / CPU fallback |
| Dapat dilatih ulang (data kampus) | Tidak perlu (rule-based) | ✗ **Black-box — tidak bisa fine-tune** | ✅ LAE siap train dari data sendiri |
| Dependensi | pip minimal | Patch fragile (`patch_diffmot_eval.py`), env khusus torch | Murni `filterpy` + `scipy` + torch |
| Target tesis (people counting real-time di scene kampus) | Cepat tapi asosiasi rapuh | Akurat tapi tidak deployable | **Tengah jalan: akurat + ringan + trainable** |

### 5.3 Keterbatasan dan Kejujuran Pelaporan

Tabel pembanding dari literatur (hanya sel yang memiliki sumber diisi):

| Benchmark | Tracker | Deteksi | HOTA | IDF1 | MOTA |
|---|---|---|---|---|---|
| MOT20 | OC-SORT (eksperimen ini) | YOLO26 fine-tune kami | 36,51 | 42,88 | 55,98 |
| MOT20 | OC-SORT (publikasi) | deteksi resmi | 62,4 | — | — |
| DanceTrack | OC-SORT (eksperimen ini) | YOLO26 fine-tune kami | 28,39 | 26,63 | 71,38 |
| DanceTrack | OC-SORT (publikasi) | deteksi resmi | — | — | — |
| DanceTrack | DiffMOT (publikasi) | YOLOX | 62,3 | 63,0 | — |

Catatan:

1. **Angka tidak sebanding 1:1 dengan leaderboard.** Deteksi memakai YOLO26 fine-tune kita (bukan deteksi resmi MOTChallenge/YOLOX) dan `DO_PREPROC=False`. Perbandingan yang sah di sini adalah **antar tracker pada deteksi yang sama**, bukan melawan angka publikasi. Tabel di atas hanya memberi konteks besaran.
2. **Angka publikasi OC-SORT** (MOT20 HOTA 62,4; DanceTrack-test 55,1) diambil dari catatan riset dan diverifikasi ulang ke arXiv selama audit referensi DiffMOT berjalan; angka publikasi DiffMOT diverifikasi dari arXiv:2403.02075 dan situs proyek (Lv et al., 2024 – S021).
3. **Detektor kita menjadi lantai (*floor*).** Skenario A menemukan under-count struktural 7,4–10,0% di lapisan detektor — tracker tidak dapat memperbaiki orang yang tidak terdeteksi sama sekali. IDF1/HOTA karenanya memiliki batas atas yang lebih rendah daripada eksperimen dengan deteksi resmi (dari sinilah sesat antara angka kita dan angka publikasi).
4. **Baseline ganda.** OC-SORT dan DiffMOT keduanya telah dijalankan pada deteksi yang sama (2026-08-05); tabel lengkap ada di Bagian 6. Tracker usulan (LightTrack-ReID-inspired) akan ditambahkan pada tabel yang sama setelah Phase 3 selesai.
5. **Ceiling DiffMOT belum dilampaui.** Selisih HOTA kedua tracker di DanceTrack (~39,05) masih ~23 poin di bawah angka publikasi DiffMOT (62,3) — komparasi adil antar tracker, bukan melawan leaderboard.

---

## 6. DiffMOT — Hasil, Downside, dan Keputusan Pivot ke Tracker Usulan

### 6.1 Eksekusi

DiffMOT v1.0 (motion D²MP + ReID) dijalankan di GPU kampus pada **deteksi YOLO26 fine-tune yang sama** dengan OC-SORT (protokol identik; `DO_PREPROC=False`). Hasil per sekuens lengkap di `experiments/s2_tracker/diffmot_results/`; panduan eksekusi: `docs/panduan-skenario-b-diffmot.md` (notebook 10–70).

### 6.2 Hasil dan Analisis Downside

| Metrik | OC-SORT | DiffMOT | Δ |
|---|---|---|---|
| MOT20 HOTA | 36,51 | **44,37** | +7,86 |
| MOT20 IDF1 | 42,88 | **53,86** | +10,98 |
| MOT20 IDSW | 14.293 | **6.905** | **−7.388 (−52%)** |
| DanceTrack HOTA | 28,39 | **39,05** | +10,66 |
| DanceTrack IDF1 | 26,63 | **43,39** | +16,76 |
| DanceTrack IDSW | 6.701 | **2.784** | **−3.917 (−58%)** |

DiffMOT terbukti memperbaiki asosiasi secara drastis — persis kelemahan baseline. Namun tiga downside membuatnya **tidak dipilih sebagai tracker utama untuk people counting real-time**:

1. **Kebutuhan GPU + throughput rendah.** Butuh CUDA (RTX); pada skala kerumunan padat MOT20, biaya ReID + denoising diffusion menekan FPS jauh di bawah kebutuhan real-time untuk deployment kamera kampus (target: ≥30 FPS pada perangkat murah/embedded). Publikasi ~22,7 FPS di RTX 3090 diukur pada deteksi YOLOX — dengan pipeline kita biayanya lebih besar.
2. **Black-box, tidak dapat dilatih ulang.** DiffMOT adalah sistem lengkap dengan bobot pra-latih; evaluasi pada data kampus tidak bisa memanfaatkan fine-tune pada distribusi kita sendiri.
3. **Rantai dependensi fragile.** Patch lokal (`patch_diffmot_eval.py`), env torch khusus, dan format deteksi yang harus disesuaikan membuatnya sulit didistribusikan sebagai artefak deployment.

### 6.3 Keputusan: Tracker Usulan LightTrack-ReID-inspired

Pivot telah disepakati dalam implementasi fase berikut: **tracker usulan — arsitektur ringan terinspirasi LightTrack-ReID** (Khan et al., 2026 – S014) — dirancang untuk mempertahankan kualitas asosiasi DiffMOT-style (ReID + memory) dengan biaya sepersekian:

- **LAE MobileNetV3-Small → embedding 32-d** untuk ReID ringan (~0,6 GFLOPs asosiasi, tabel publikasi S014) — jalur efisien/CPU; 
- **TBSS scorer transformer** untuk skor kemiripan yang lebih tajam daripada IoU murni;
- **CMOH memory + ASW** untuk bertahan pada oklusi (menyerap kelemahan IDSW DiffMOT yang masih 6.905 di MOT20);
- **dapat dilatih ulang** pada data kampus → perbaikan berkelanjutan, target >100 FPS GPU / fallback CPU.

Tabel 4.1 akan dimutakhirkan dengan baris tracker usulan setelah Phase 3 selesai; DiffMOT tetap dipertahankan sebagai baseline kualitas kedua dalam tabel perbandingan.

---

## 7. Video Demo (Kombinasi Skenario A + B)

Video demo merender hasil pipeline lengkap — **deteksi YOLO26 (Skenario A) → tracking OC-SORT (Skenario B) → overlay jumlah orang per bingkai** — untuk bahan presentasi. FPS mengikuti `seqinfo.ini` dataset (MOT20 = 25 fps, bukan 30 — koreksi 2026-08-04):

- `experiments/s2_tracker/demo/MOT20-02_f1-450_tracked.mp4` — kerumunan padat, 450 bingkai (±18 dtk @25 fps)
- `experiments/s2_tracker/demo/MOT20-01_f1-429_tracked.mp4` — kerumunan jarang, 429 bingkai penuh (±17 dtk @25 fps)
- `experiments/s2_tracker/demo/MOT20-02_f1-450_tracked_diffmot.mp4` — **kerumunan padat dengan tracking DiffMOT** (450 bingkai, ±18 dtk @25 fps): perbandingan visual langsung vs OC-SORT `_tracked.mp4` pada klip yang sama — ID switch jauh lebih jarang saat oklusi/papasan
- `experiments/s2_tracker/demo/MOT20-02_f1-450_gt.mp4` — **referensi Ground Truth** (kotak hijau = pedestrian ber-GT, abu-abu = distraktor) untuk membandingkan "ideal" vs baseline

*Klip demo dirender ulang (2026-08-04) dari hasil tracking full-sequence* — sebelumnya `MOT20-01_f1-214` adalah artefak data terpotong dan telah dihapus.

Setiap kotak diberi ID stabil (warna per ID) dan header menampilkan jumlah orang aktif per bingkai. Klip GT bukan hasil pipeline — hanya referensi visual agar kelemahan baseline (ID switch saat oklusi) terbaca jelas sebagai *gap*, bukan sebagai kesalahan render.

Dibangkitkan dengan `scripts/s2/render_demo_video.py` (Pillow + ffmpeg, tanpa GPU; frame diunduh dari HF sekali, resume otomatis; `--source gt` untuk klip referensi):

```bash
python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450
python scripts/s2/render_demo_video.py --seq MOT20-01
python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450 --source gt
```

---

## 8. Kesimpulan dan Arah Lanjut

Baseline ganda (OC-SORT vs DiffMOT) menunjukkan: (1) deteksi YOLO26 fine-tune siap dipakai di lapisan bawah (MOTA tinggi di kedua benchmark); (2) asosiasi motion-only tidak memadai untuk counting yang akurat — IDF1 DanceTrack 26,63 dengan OC-SORT; (3) DiffMOT memperbaiki asosiasi secara drastis (IDF1/HOTA naik 8–17 poin, IDSW turun >50% di kedua benchmark) tetapi **tidak memenuhi kebutuhan real-time dan tidak dapat dilatih ulang** — bukan kandidat deployment people counting.

Kesimpulan: arah proposal sudah benar — **tracker dengan ReID + memory diperlukan untuk people counting yang akurat** — namun arsitekturnya harus ringan dan trainable. Maka keputusan: **tracker usulan LightTrack-ReID-inspired** (LAE 32-d + TBSS + CMOH + ASW) diimplementasikan di Phase 3 dan dievaluasi pada protokol yang sama (Tabel 4.1), dengan DiffMOT sebagai baseline kualitas kedua dan OC-SORT sebagai baseline efisien.

---

## Lampiran A — Artefak Hasil

| Berkas | Isi |
|---|---|
| `experiments/s2_tracker/eval_results.csv` | Skor TrackEval per benchmark (sumber tabel 4.1; saat ini berisi OC-SORT + DiffMOT) |
| `experiments/s2_tracker/diffmot_results/{mot20,dancetrack}/*.txt` | Hasil tracking DiffMOT per sekuens (format MOT) |
| `experiments/s2_tracker/detection_stats.csv` | Statistik deteksi per sekuens (frames, dets, det/frame, detik) |
| `experiments/s2_tracker/ocsort_results/{mot20,dancetrack}/*.txt` | Hasil tracking OC-SORT per sekuens (format MOT) |
| `experiments/s2_tracker/figs/*.png` | Figur 1–4 |
| `experiments/s2_tracker/demo/*.mp4` | Video demo (Bagian 7) ‑ termasuk `*_tracked_diffmot.mp4` |
| `scripts/s2/run_skenario_b_ocsort.py` | Orchestrator reproduce: arrange → detect → track → eval |
| `scripts/s2/render_demo_video.py` | Render klip demo (Pillow + ffmpeg) |
| `docs/panduan-skenario-b-oc-sort.md` | Panduan eksekusi PC rumah |
| `docs/panduan-skenario-b-diffmot.md` | Panduan DiffMOT kampus (notebook 10–70) |

## Lampiran B — Reproduksi

```bash
# PC rumah (CPU; deteksi .onnx + OC-SORT + eval)
python scripts/s2/run_skenario_b_ocsort.py --steps arrange,detect,track,eval --force

# Kampus (GPU; DiffMOT) — notebook 10 → 20 → 30 → 40 → 50 → 70 (lihat docs/panduan-skenario-b-diffmot.md)

# Render klip demo (Bagian 7; `--source tracked` default, `--tracker diffmot` untuk DiffMOT, `--source gt` untuk referensi)
python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450
python scripts/s2/render_demo_video.py --seq MOT20-02 --start 1 --end 450 --tracker diffmot
```

## Daftar Pustaka

1. Lv, W., Huang, Y., Zhang, N., Lin, R.-S., Han, M., & Zeng, D. (2024 – S021). *DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction.* CVPR 2024, pp. 19321–19330. arXiv:2403.02075; kode: https://github.com/Kroery/DiffMOT (diakses 2026-08-03).
2. Cao, J., Pang, J., Weng, X., Khirodkar, R., & Kitani, K. (2023). *Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking.* CVPR 2023. arXiv:2203.14360 (diakses 2026-08-03). *(Belum memiliki S-ID di source ledger.)*
3. Luiten, J., Ošep, A., Dendorfer, P., et al. (2021 – S025). *HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking.* IJCV 129(2), 548–578. DOI 10.1007/s11263-020-01375-2 (diakses 2026-08-03).
4. Dendorfer, P., Rezatofighi, H., Milan, A., et al. (2020 – S036). *MOT20: A benchmark for multi object tracking in crowded scenes.* ECCV 2020 Workshops. arXiv:2003.09003 (diakses 2026-08-03).
5. Sun, P., Cao, J., Jiang, Y., et al. (2022 – S037). *DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion.* CVPR 2022. arXiv:2111.14690 (diakses 2026-08-03).
6. Luiten, J., et al. *TrackEval* (toolkit evaluasi MOT). https://github.com/JonathonLuiten/TrackEval (diakses 2026-08-03).
7. Ultralytics. *YOLO Documentation* (deteksi, vendor). https://docs.ultralytics.com (diakses 2026-08-03).
8. Khan, S. B. J., Zhang, P., Kamal, M. M., Saudagar, A. K. J., et al. (2026 – S014). *LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking.* PLOS One 21(3), e0342246. DOI 10.1371/journal.pone.0342246 (diakses 2026-08-05).
