# Skenario B: Evaluasi Tracker dan Arah Tracker Usulan

Bahan presentasi, 11 Agustus 2026.

Pesan inti satu kalimat: yang membatasi kualitas counting adalah asosiasi identitas antar frame, bukan deteksi, dan jawabannya adalah tracker ringan dengan ReID yang bisa dilatih ulang.

---

## 1. Kenapa Perlu Tracker

Deteksi cuma memberi kotak per frame. Tanpa tracker, orang yang tertutup sebentar lalu muncul lagi dihitung dua kali.

Pertanyaan skenario B: tracker mana yang mampu menjaga identitas cukup lama untuk counting yang akurat?

Dua pembanding diuji pada deteksi YOLO26 yang sama persis (hasil Skenario A), memakai TrackEval di MOT20-train (4 sekuens, 8.931 frame, kerumunan sangat padat) dan DanceTrack-val (25 sekuens, 25.508 frame, gerak non-linear, penampilan seragam). Karena deteksi bukan deteksi resmi MOTChallenge, angka tidak dibandingkan 1:1 ke leaderboard; perbandingan yang sah antar tracker pada deteksi yang sama.

## 2. Data Hasil: OC-SORT vs DiffMOT

| Benchmark | Tracker | HOTA | MOTA | IDF1 | IDSW | Frag |
|---|---|---|---|---|---|---|
| MOT20 (train) | OC-SORT | 36,51 | 55,98 | 42,88 | 14.293 | 27.646 |
| MOT20 (train) | DiffMOT | 44,37 | 60,91 | 53,86 | 6.905 | 15.005 |
| DanceTrack (val) | OC-SORT | 28,39 | 71,38 | 26,63 | 6.701 | 6.936 |
| DanceTrack (val) | DiffMOT | 39,05 | 70,72 | 43,39 | 2.784 | 6.765 |

Selisihnya:

| Metrik | Selisih DiffMOT vs OC-SORT |
|---|---|
| MOT20 HOTA | +7,86 |
| MOT20 IDF1 | +10,98 |
| MOT20 IDSW | −7.388 (turun 52%) |
| DanceTrack HOTA | +10,66 |
| DanceTrack IDF1 | +16,76 |
| DanceTrack IDSW | −3.917 (turun 58%) |

Yang penting dibaca:

- OC-SORT: deteksi kuat (MOTA 55,98 di kepadatan 179 deteksi/frame, puncak 272), tapi asosiasi putus-putus: 14.293 ID switch di MOT20, IDF1 cuma 26,63 di DanceTrack.
- DiffMOT: ID switch turun 52 sampai 58 persen, IDF1 naik 11 sampai 17 poin. ReID plus memori memang diperlukan.
- Untuk counting, IDF1 dan IDSW paling relevan: identitas putus saat oklusi = orang dihitung ganda saat muncul lagi.

## 3. Kenapa Tidak Memakai DiffMOT

| Dimensi | OC-SORT | DiffMOT |
|---|---|---|
| Biaya asosiasi | hampir nol, 54+ FPS di CPU | berat, butuh GPU, 20 sampai 25 FPS di RTX 4090 (demo: sekitar 20 FPS) |
| Bisa dilatih ulang | tidak perlu | tidak, black box |
| Dependensi | pip minimal | patch lokal + env khusus |

Target pipeline: minimal 30 FPS (anggaran 33 sampai 40 ms per frame). DiffMOT sudah melewati anggaran pada tahap tracking saja, sebelum detektor dihitung. Publikasi DiffMOT sendiri menyebut 22,7 FPS di RTX 3090.

Kesimpulan: arah riset butuh ReID plus memori, tapi arsitekturnya harus ringan dan trainable. DiffMOT tetap dipakai sebagai pembanding kualitas.

## 4. Paper Acuan: LightTrack-ReID

Khan dkk. (2026, S014), PLOS ONE 21(3), e0342246. Peer-reviewed. Tidak ada kode resmi, reimplementasi menjadi kontribusi mandiri.

Singkatan yang dipakai sistem:

| Singkatan | Kepanjangan | Arti singkat |
|---|---|---|
| LAE | Lightweight Appearance Encoder | Sidik jari penampilan, vektor 32 angka per orang |
| TBSS | Transformer-Based Similarity Scoring | Penilai kemiripan posisi + penampilan, skor 0 sampai 1 |
| CMOH | Context Memory for Occlusion Handling | Memori 10 embedding terakhir, untuk yang tertutup sebentar |
| ASW | Adaptive Similarity Weighting | Bagi porsi antara posisi dan penampilan sesuai keramaian frame |
| APS | Adaptive Pair Sampling | Cara memilih pasangan latih, maksimal 50 per frame |

Angka di paper (konteks, bukan target reproduksi):

| Metrik | Nilai paper |
|---|---|
| MOT17 test | HOTA 66,92, IDF1 82,52 |
| MOT20 test | HOTA 66,6, IDF1 82,2 |
| Kecepatan | sekitar 30 FPS di GTX 1080 |
| Biaya asosiasi | sekitar 0,6 GFLOPs/frame |
| Training | MOT17 + MOT20, 20 epoch, sekitar 10 jam di GTX 1080 |

## 5. Pola Ablasi Paper (Data Asli, val split paper)

| Konfigurasi | HOTA (MOT17) | HOTA (MOT20) | IDSW (MOT17) | Bacaannya |
|---|---|---|---|---|
| Baseline (Kalman + IoU + EMA) | 66,13 | 56,17 | 227 | titik awal |
| +LAE | 70,88 | 60,38 | 168 | kenaikan terbesar, penampilan sinyal utama |
| +LAE +TBSS | 73,38 | 63,94 | 138 | menambah stabil di atas LAE |
| +LAE +TBSS +CMOH | 74,88 | 65,74 | 80 | paling memangkas pergantian identitas |
| +LAE +TBSS +CMOH +ASW | 75,63 | 66,70 | 79 | tambahan tipis |

Istilah teknisnya: Kalman = prediktor posisi (asumsi gerak lurus), IoU = seberapa tumpang tindih dua kotak, EMA = penghalus kotak supaya tidak goyang, LAE = sidik jari penampilan, TBSS = penilai kemiripan, CMOH = memori oklusi, ASW = penyeimbang posisi vs penampilan.

Analoginya: Kalman menebak orang ada di mana, IoU melihat kotaknya nyambung atau tidak, LAE mengenali orang dari penampilannya, CMOH mengingat orang yang sempat hilang dari layar, ASW memutuskan kapan lebih percaya mata (penampilan) dan kapan lebih percaya posisi.

## 6. Tracker Usulan (Per Resep Paper)

Komponen: LAE + TBSS + asosiasi inti (Kalman, Hungarian, filter, EMA) + CMOH + ASW. Skor akhir = bobot ASW kali skor TBSS ditambah bobot kebalikannya kali IoU.

Resep training persis paper: MOT17 + MOT20, loss triplet + BCE, Adam lr 0,001, 20 epoch, crop 224, augmentasi flip/crop/jitter, maksimal 50 pasangan per frame. Estimasi 2,5 sampai 5 jam per 20 epoch di RTX 4090.

Protokol evaluasi anti-overclaim: leave-one-out MOT20 4 fold + DanceTrack zero-shot, deteksi YOLO26 identik, hasil dibandingkan relatif ke OC-SORT (36,51) dan DiffMOT (44,37), bukan ke angka paper.

## 7. Hasil Training Fold-1 (v1) dan Perbaikan v2

Data run asli (20 epoch, MOT17 + MOT20, 4090):

| Metrik | Epoch 1 | Epoch 20 | Artinya |
|---|---|---|---|
| Loss total | 0,139 | 0,054 | turun mulus |
| Loss triplet | 0,070 | 0,021 | embedding belajar memisahkan penampilan |
| cos_same | 0,93 | 0,98 | potongan orang yang sama makin mirip |
| BCEacc (TBSS) | sekitar 0,50 | 0,494 sampai 0,505 | tidak belajar, lempar koin |

Bacaannya: LAE berhasil, TBSS tidak. Loss BCE hanya sekitar 0,03, padahal kalau skor benar-benar semua 0,5 loss-nya harusnya sekitar 0,69. Artinya TBSS yakin benar di data latih (kemungkinan jalan pintas geometri), tapi kalah telak di validasi. Ini yang sedang dibedah lewat histogram distribusi skor, begitu GPU kampus aktif.

Perbaikan v2 yang sudah dikerjakan: TBSS diganti transformer 73 dimensi (attention-nya tidak efektif) menjadi MLP ringan input 6 angka (IoU, cosine, selisih box), optimizer TBSS dipisah, BCE diberi bobot, checkpoint ala YOLO (last/best.pt). Status: GPU kampus sedang tidak bisa dipakai, training v2 belum tuntas.

Catatan jujur untuk presentasi: angka HOTA/IDF1 tracker usulan belum ada. Yang terbukti baru encoder penampilan berfungsi baik.

## 8. Status dan Langkah Berikutnya

- Baseline OC-SORT: selesai. DiffMOT: selesai. Tracker usulan: dalam implementasi.
- Begitu GPU kampus aktif: jalankan histogram skor TBSS (5 menit) untuk memastikan akar masalah, lanjutkan training v2, lalu evaluasi TrackEval dan masuk ke tabel pembanding.

---

## Lampiran. Materi Pendukung

- Video demo klip padat MOT20-02 (450 frame, 18 detik): [OC-SORT](experiments/s2_tracker/demo/MOT20-02_f1-450_tracked.mp4) | [DiffMOT](experiments/s2_tracker/demo/MOT20-02_f1-450_tracked_diffmot.mp4) | [Ground truth](experiments/s2_tracker/demo/MOT20-02_f1-450_gt.mp4). Bandingkan langsung di klip yang sama: ID switch jauh lebih jarang saat oklusi pada versi DiffMOT.
- Video demo klip jarang MOT20-01 penuh (429 frame): [OC-SORT](experiments/s2_tracker/demo/MOT20-01_f1-429_tracked.mp4)
- Tabel hasil lengkap: experiments/s2_tracker/eval_results.csv
- Laporan detail Skenario B: docs/reports/laporan-skenario-b-tracker.md
- Catatan implementasi paper S014: docs/research/fulltext-notes/S014-lighttrack-reid.md
- Rencana fase 11: docs/plans/2026-08-05-phase11-skenario-b-tracker-lighttrack.md

## Daftar Pustaka

1. Lv, W., dkk. (2024, S021). DiffMOT. CVPR 2024, 19321-19330. arXiv:2403.02075.
2. Khan, S. B. J., dkk. (2026, S014). LightTrack-ReID. PLOS ONE 21(3), e0342246. DOI 10.1371/journal.pone.0342246.
3. Cao, J., dkk. (2023). OC-SORT. CVPR 2023. arXiv:2203.14360.
4. Luiten, J., dkk. (2021, S025). HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking. IJCV 129(2), 548-578.
5. Dendorfer, P., dkk. (2020, S036). MOT20. ECCV 2020 Workshops. arXiv:2003.09003.
6. Sun, P., dkk. (2022, S037). DanceTrack. CVPR 2022. arXiv:2111.14690.
