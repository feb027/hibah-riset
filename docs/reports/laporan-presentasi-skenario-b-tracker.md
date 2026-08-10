# Laporan Presentasi: Dari DiffMOT ke Tracker Usulan LightTrack-ReID-inspired

**Konteks:** Skenario B — evaluasi dan pemilihan lapisan *tracker* untuk sistem *people counting* real-time.
**Disusun:** 11 Agustus 2026 (bahan presentasi kemajuan riset).

---

## 1. Konteks Singkat: Mengapa Tracker Diperlukan

Deteksi tidak sama dengan *counting*. Detektor (YOLO26 fine-tune, Skenario A) menghasilkan kotak orang per bingkai, tetapi tidak tahu apakah kotak di bingkai *t* adalah orang yang sama dengan kotak di bingkai *t−1*. Tanpa lapisan **tracker** yang menjaga identitas temporal, orang yang melewati garis hitung dapat dihitung berkali-kali — terutama saat tertutup objek lain (oklusi) lalu muncul kembali.

Skenario B menjawab: **tracker mana, pada kondisi apa, yang mampu menjaga identitas cukup lama untuk counting yang akurat?** Dua kandidat dievaluasi pada protokol yang sama, lalu diputuskan arah pengembangan:

- **OC-SORT** (Cao et al., 2023) — berbasis gerak murni (Kalman + IoU), cepat, tanpa GPU. Jalur efisien/fallback.
- **DiffMOT** (Lv et al., 2024 – S021) — prediksi gerak diffusion + ReID, butuh GPU. Dipilih dari proposal sebagai kandidat akurasi tertinggi.
- **Tracker usulan** — LightTrack-ReID-inspired (Khan et al., 2026 – S014): ringan, dapat dilatih ulang, target real-time.

**Protokol (kejujuran eksperimen):** kedua tracker memakai **deteksi YOLO26 yang identik** (hasil Skenario A), dievaluasi dengan TrackEval pada benchmark MOT20-train (4 sekuens, 8.931 bingkai, GT publik) dan DanceTrack-val (25 sekuens, 25.508 bingkai, GT publik), `DO_PREPROC=False`. Karena deteksi bukan deteksi resmi MOTChallenge, angka **tidak sebanding 1:1 dengan leaderboard**; perbandingan yang sah adalah antar-tracker pada deteksi yang sama.

---

## 2. Hasil DiffMOT (Evaluasi Selesai, 5 Agustus 2026)

DiffMOT v1.0 dijalankan penuh di GPU kampus (RTX 4090) pada deteksi YOLO26 yang sama dengan OC-SORT. Hasil TrackEval:

| Benchmark | Tracker | HOTA | MOTA | IDF1 | IDSW | Frag |
|---|---|---|---|---|---|---|
| MOT20 (train) | OC-SORT | 36,51 | 55,98 | 42,88 | 14.293 | 27.646 |
| MOT20 (train) | **DiffMOT** | **44,37** | **60,91** | **53,86** | **6.905** | **15.005** |
| DanceTrack (val) | OC-SORT | 28,39 | 71,38 | 26,63 | 6.701 | 6.936 |
| DanceTrack (val) | **DiffMOT** | **39,05** | 70,72 | **43,39** | **2.784** | **6.765** |

Pembacaan:

| Metrik | OC-SORT | DiffMOT | Δ |
|---|---|---|---|
| MOT20 HOTA | 36,51 | **44,37** | +7,86 |
| MOT20 IDF1 | 42,88 | **53,86** | +10,98 |
| MOT20 IDSW | 14.293 | **6.905** | **−7.388 (−52%)** |
| DanceTrack HOTA | 28,39 | **39,05** | +10,66 |
| DanceTrack IDF1 | 26,63 | **43,39** | +16,76 |
| DanceTrack IDSW | 6.701 | **2.784** | **−3.917 (−58%)** |

**Temuan kunci:**

1. **Masalah sesungguhnya adalah asosiasi, bukan deteksi.** OC-SORT mencapai MOTA 55,98 pada kepadatan rata-rata 179 deteksi/bingkai (GT 127; puncak 272 di MOT20-05) — deteksi kuat — tetapi **14.293 ID switch** (±1,6 per bingkai): identitas sering putus saat oklusi. IDF1 42,88 berarti ±57% bobot asosiasi tidak cocok dengan GT. Untuk counting, inilah masalah utama: orang yang tertutup 2–3 bingkai lalu terdeteksi ulang dihitung sebagai orang baru.
2. **OC-SORT gagal pada gerak non-linear.** Di DanceTrack (penari seragam, gerak berakselerasi) HOTA jatuh ke 28,39 dan IDF1 ke 26,63 — asumsi kalman kecepatan konstan runtuh. Ini persis skenario motivasi DiffMOT.
3. **DiffMOT memperbaiki asosiasi secara drastis**: IDSW turun >50% di kedua benchmark, IDF1 naik 11–17 poin, HOTA naik 8–11 poin. Prediksi diffusion + ReID terbukti bekerja.

---

## 3. Kenapa Pivot: Tiga Hambatan DiffMOT untuk Deployment

Akurasi bukan satu-satunya kriteria. Untuk people counting real-time di kamera kampus, DiffMOT gagal di tiga dimensi:

**1. Throughput tidak mencukupi, bahkan di GPU kuat.** Keseluruhan pipeline DiffMOT diukur **±20–25 FPS (tracking-only) pada RTX 4090** — pada video demo klip MOT20-02 (450 bingkai) tercatat ±20 FPS. Kebutuhan pipeline real-time adalah **≥30 FPS (≤33–40 ms/bingkai)** pada perangkat murah/embedded. ReID (OSNet) + denoising diffusion + Hungarian membuat DiffMOT sudah melewati anggaran waktu per bingkai **sebelum detektor dihitung**; publikasi sendiri menyebut 22,7 FPS pada RTX 3090 *termasuk* deteksi YOLOX.

**2. Black-box — tidak dapat dilatih ulang.** DiffMOT adalah sistem lengkap dengan bobot pra-latih. Untuk scene kampus (iluminasi, sudut kamera, kepadatan berbeda), kita tidak bisa fine-tune — salah satu kontribusi riset (adaptasi domain) hilang.

**3. Rantai dependensi rapuh.** DiffMOT butuh env torch khusus (cu118), patch lokal `patch_diffmot_eval.py` (5+ bug runtime di-fix manual), format deteksi dan cache embedding yang harus disetel persis. Tidak layak didistribusikan sebagai artefak deployment.

| Dimensi | OC-SORT (baseline) | DiffMOT | Tracker usulan |
|---|---|---|---|
| Biaya asosiasi | ~0 GFLOPs, 54+ FPS CPU | HMINet + ReID berat, **±20–25 FPS di RTX 4090** | LAE+TBSS **~0,6 GFLOPs**, target >100 FPS GPU |
| Dapat dilatih ulang | Tidak perlu | ✗ Black-box | ✅ Dari data sendiri |
| Dependensi | Pip minimal | Patch fragile + env khusus | Torch + filterpy |
| Posisi | Cepat, asosiasi rapuh | Akurat, **tidak deployable** | Akurat + ringan + trainable |

**Kesimpulan:** DiffMOT meninggalkan warisan penting — bukti kuantitatif bahwa **ReID + memory diperlukan** untuk counting yang akurat (IDSW turun 52–58%) — tetapi arsitekturnya tidak bisa menjadi tracker utama. Dicari: tracker dengan kualitas asosiasi gaya DiffMOT, biaya sepersekian, dan bisa dilatih ulang.

---

## 4. Penemuan Paper LightTrack-ReID (Khan et al., 2026 – S014)

Survei lanskap tracker 2025–2026 (setelah eval DiffMOT) menemukan kandidat yang paling pas dengan kebutuhan: **LightTrack-ReID** — peer-reviewed di *PLOS ONE* 21(3):e0342246, DOI 10.1371/journal.pone.0342246 (Khan et al., 2026 – S014).

**Klaim paper (konteks, bukan target reproduksi — protokol beda):**

| Metrik | Nilai paper |
|---|---|
| MOT17 test (YOLOX, protokol resmi) | HOTA 66,92 · MOTA 82,81 · IDF1 82,52 |
| MOT20 test | HOTA 66,6 · MOTA 79,1 · IDF1 82,2 |
| Kecepatan | ±30 FPS di GTX 1080, i7-6700 |
| Biaya asosiasi | ±0,6 GFLOPs/bingkai (LAE ~0,5 + TBSS ~0,1); detektor YOLOX-S ~26,8 GFLOPs = dominan |
| Training | MOT17 + MOT20, 20 epoch, ±10 jam GTX 1080 |

**Mengapa paper ini dipilih (kesesuaian dengan tesis):**

1. **Paradigma real-time + deep learning memang di jalur target**: asosiasi ringan, bukan diffusion. Asosiasi cuma ~0,6 GFLOPs — kecepatan didominasi detektor, bukan tracker.
2. **Ringan dan trainable**: backbone MobileNetV3-Small (32-d embedding) — bisa dilatih ulang di data kampus, beda dari DiffMOT.
3. **Menyerap kelemahan yang ditemukan eksperimen kita**: komponen memory (CMOH) secara ablasi memangkas ID switch drastis (MOT17 val: 138→80; MOT20 val: 882→701) — persis metrik yang rapuh di OC-SORT dan masih tersisa di DiffMOT (6.905 di MOT20).
4. **TIDAK ada kode resmi → reimplementasi = kontribusi riset mandiri**, bukan sekadar replikasi; konsisten dengan kontribusi usulan (tracker versi kita).

**Pola ablasi paper (pembelajaran desain, bukan angka pembanding):**

| Konfigurasi | HOTA (MOT17 val) | HOTA (MOT20 val) | Pembacaan |
|---|---|---|---|
| Baseline (Kalman+IoU+EMA) | 66,13 | 56,17 | — |
| +LAE (ReID embedding) | 70,88 | 60,38 | **Kenaikan terbesar — penampilan adalah sinyal utama** |
| +TBSS (scorer) | 73,38 | 63,94 | Stabil di atas LAE |
| +CMOH (memory oklusi) | 74,88 | 65,74 | **Menggantikan IDSW drastis** |
| +ASW (bobot oklusi) | 75,63 | 66,70 | Increment tipis |

---

## 5. Tracker Usulan Menurut Paper (LightTrack-ReID-inspired)

Arsitektur disusun mengikuti resep paper (S014), disesuaikan dengan ekosistem proyek (YOLO26, python 3.8 di kampus):

**Komponen:**

- **LAE (Lightweight Appearance Embedding)** — MobileNetV3-Small → embedding 32-d L2-normalized. ReID ringan; di inference cosine sebagai sinyal kemiripan penampilan.
- **TBSS (Transformer-Based Similarity Scoring)** — skor kemiripan `s ∈ [0,1]` dari kombinasi bbox, IoU, dan embedding — pengganti IoU murni pada matriks cost asosiasi. Cost: `C = 1 − [w_t·s + (1−w_t)·IoU]` (persamaan 10 paper).
- **Asosiasi inti** — Kalman filter + Hungarian + confidence filter + EMA (baseline yang dipakai ablasi paper).
- **CMOH (Context Memory)** — buffer embedding K=10 agar tracklet yang tertutup singkat tetap bisa dicocokkan saat muncul kembali.
- **ASW (Adaptive Occlusion Weight)** — bobot global per bingkai dari rasio deteksi beroklusi.

**Resep training (persis paper, S014 catatan implementasi):**

- Data: MOT17-train + MOT20-train (APS ±135.000 sampel; split 80/20).
- Loss: `L = L_triplet + L_BCE` — triplet margin 1,0 pada embedding + BCE pada skor TBSS; Adam lr 0,001, 20 epoch.
- Crop 224×224 (ImageNet), augmentasi flip 50% / crop padding 10% / color jitter 0,2; maksimum 50 pasangan per bingkai.
- Estimasi: ±2,5–5 jam/20 epoch di RTX 4090.

**Protokol evaluasi (anti-overclaim):** leave-one-out MOT20-train 4-fold + zero-shot DanceTrack-val, deteksi YOLO26 identik dengan OC-SORT/DiffMOT, TrackEval yang sama. Hasil dilaporkan **relatif terhadap OC-SORT (36,51 HOTA) dan DiffMOT (44,37 HOTA) MOT20** — bukan dibandingkan ke tabel paper (protokol berbeda).

---

## 6. Status Implementasi (Faktual per 10 Agustus 2026)

| Fase | Status | Bukti |
|---|---|---|
| Phase 1 — skeleton tracker | ✅ Selesai | Kalman+IoU+Hungarian+EMA; smoke 3.211 bingkai @ 614 FPS CPU |
| Phase 2 — LAE encoder | ✅ Selesai, verifikasi kampus | MobileNetV3-Small → 32-d; cosine same 0,772 vs diff 0,746 (MOT20-01, GPU) |
| Phase 3 — training (fold-1, batch v1) | ✅ Selesai, **diagnosa** | Loss 0,139→0,054; **LAE sehat** (cos_same 0,93–0,98; Lt 0,070→0,021) — **TBSS BCEacc flat ~0,5** |
| Phase 3 v2 — redesign TBSS | 🔄 Sedang dieksekusi | MLP 6-d input (IoU, cos, geometri bbox), optimizer pisah, BCE berbobot, ckpt last/best.pt; GPU kampus sedang tidak tersedia |
| Evaluasi tracker usulan | ⏳ Belum | Histogram skor TBSS (`check_tbss_histogram.py`) menunggu GPU kampus aktif |

**Kejujuran pelaporan:** **belum ada angka HOTA/IDF1 tracker usulan.** Yang sudah terbukti: pipeline training berjalan (LAE terlatih memisahkan penampilan), sementara komponen skor kemiripan (TBSS) belum menunjukkan pembelajaran di validasi (BCEacc ≈ 0,5 = lempar koin) dan sedang diperbaiki (v2). Temuan diagnosis, dengan cepat: loss BCE total ~0,03 tidak mungkin dari output semua ~0,5 (BCE lempar koin = 0,69) — indikasi awal bukan "collapse mati", melainkan ketidakcocokan train/val yang dibedah lewat histogram skor s_ap vs s_an segera setelah GPU aktif.

**Langkah berikut (tergantung hasil diagnosa):**
1. `scripts/s2/check_tbss_histogram.py` pada `out/phase3_fold1_v2/best.pt` (5 menit) → verdict: threshold/val bermasalah vs collapse asli.
2. Lanjut training fold-1 full (resume `last.pt`), lalu evaluasi TrackEval pada protokol sama.
3. Masuk tabel pembanding Skenario B vs OC-SORT (36,51) dan DiffMOT (44,37).

---

## 7. Kesimpulan

1. **Asosiasi, bukan deteksi, yang menjadi pembatas counting** — OC-SORT: 14.293 IDSW di MOT20, IDF1 26,63 di DanceTrack.
2. **DiffMOT membuktikan ReID + memory diperlukan**: IDSW −52% (MOT20) dan −58% (DanceTrack), HOTA naik 8–11 poin — tetapi ±20–25 FPS di RTX 4090, black-box, dan fragile membuatnya **bukan kandidat deployment**.
3. **Pivot terarah ke LightTrack-ReID (S014)**: peer-reviewed, asosiasi ~0,6 GFLOPs, trainable, ~30 FPS GTX 1080, pattern ablasi (LAE = sinyal terbesar; CMOH = pemangkas ID switch) selaras dengan kelemahan yang diukur pada baseline kita.
4. **Tracker usulan sedang dibangun menurut resep paper**; status jujur: LAE terlatih, TBSS dalam perbaikan (v2), evaluasi penuh menunggu GPU kampus.

---

## Lampiran — Materi Pendukung Presentasi

| Materi | Lokasi |
|---|---|
| Tabel hasil lengkap | `experiments/s2_tracker/eval_results.csv` |
| Video demo klip padat (OC-SORT vs DiffMOT vs GT) | `experiments/s2_tracker/demo/MOT20-02_f1-450_tracked.mp4`, `..._tracked_diffmot.mp4`, `..._gt.mp4` |
| Laporan detail Skenario B | `docs/reports/laporan-skenario-b-tracker.md` |
| Catatan implementasi paper S014 | `docs/research/fulltext-notes/S014-lighttrack-reid.md` |
| Rencana Phase 11 (tracker usulan) | `docs/plans/2026-08-05-phase11-skenario-b-tracker-lighttrack.md` |

## Daftar Pustaka

1. Lv, W., Huang, Y., Zhang, N., Lin, R.-S., Han, M., & Zeng, D. (2024 – S021). *DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction.* CVPR 2024, pp. 19321–19330. arXiv:2403.02075.
2. Khan, S. B. J., Zhang, P., Kamal, M. M., Saudagar, A. K. J., et al. (2026 – S014). *LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking.* PLOS ONE 21(3), e0342246. DOI 10.1371/journal.pone.0342246.
3. Cao, J., Pang, J., Weng, X., Khirodkar, R., & Kitani, K. (2023). *Observation-Centric SORT* (OC-SORT). CVPR 2023. arXiv:2203.14360.
4. Luiten, J., Ošep, A., Dendorfer, P., et al. (2021 – S025). *HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking.* IJCV 129(2), 548–578.
5. Dendorfer, P., et al. (2020 – S036). *MOT20: A benchmark for multi object tracking in crowded scenes.* ECCV 2020 Workshops. arXiv:2003.09003.
6. Sun, P., et al. (2022 – S037). *DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion.* CVPR 2022. arXiv:2111.14690.
