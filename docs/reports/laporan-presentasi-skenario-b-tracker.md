# Skenario B: Evaluasi Tracker dan Arah Tracker Usulan

Bahan presentasi, 11 Agustus 2026.

Pesan inti satu kalimat: yang membatasi kualitas counting adalah asosiasi identitas antar frame, bukan deteksi, dan jawabannya adalah tracker ringan dengan ReID yang bisa dilatih ulang.

---

## 1. Kenapa Perlu Tracker

Deteksi cuma memberi kotak per frame. Tanpa tracker, orang yang tertutup sebentar lalu muncul lagi dihitung dua kali.

Pertanyaan skenario B: tracker mana yang mampu menjaga identitas cukup lama untuk counting yang akurat?

Dua pembanding diuji pada deteksi YOLO26 yang sama persis (hasil Skenario A, fine-tune CrowdHuman, mAP@0.5:0.95 = 0,4974), memakai TrackEval di MOT20-train (4 sekuens, 8.931 frame, kerumunan sangat padat) dan DanceTrack-val (25 sekuens, 25.508 frame, gerak non-linear, penampilan seragam). Karena deteksi bukan deteksi resmi MOTChallenge, angka tidak dibandingkan 1:1 ke leaderboard; perbandingan yang sah antar tracker pada deteksi yang sama.

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

Status implementasi tracker usulan:

| Fase | Komponen | Status | Hasil |
|---|---|---|---|
| Phase 1 | Skeleton asosiasi (Kalman + IoU + Hungarian + EMA) | selesai | 3.211 frame smoke-test, 614 FPS di CPU |
| Phase 2 | LAE encoder (MobileNetV3-Small, 32-d) | selesai, diverifikasi GPU kampus | cosine orang yang sama 0,772 vs orang beda 0,746 (sebelum dilatih, margin kecil +0,027; justru alasan training) |
| Phase 3 v1 | Training fold-1 (LAE + TBSS) | selesai | LAE bagus; TBSS tak terukur (bug validasi, bagian 7) |
| Phase 3 v2 | Perbaikan TBSS (MLP 6-d, optimizer pisah, BCE berbobot) | ✅ selesai (14 Agustus) | BCEacc val 0,92-0,98 (best.pt 0,978 di ep15), TBSS terukur valid pertama kali |
| Evaluasi TrackEval | HOTA/IDF1 tracker usulan | ✅ evaluasi pertama selesai (14 Agustus) | MOT20 HOTA 32,92 / IDF1 34,69; DanceTrack HOTA 22,53 / IDF1 18,91; masih di bawah OC-SORT, tuning lanjut |

## 7. Hasil Training Fold-1 (v1) dan Perbaikan v2

Sebelum full run, ada mini-run (1 sekuens, 60 frame, 1 epoch): BCEacc 0,908 dan margin cosine +0,775, bukti pipeline training jalan dan sinyal penampilan mulai terpisah. Catatan: sampel validasinya hanya 10 frame, bukan bukti final.

Data run asli (20 epoch, MOT17 + MOT20, 4090):

| Metrik | Epoch 1 | Epoch 20 | Artinya |
|---|---|---|---|
| Loss total | 0,139 | 0,054 | turun mulus |
| Loss triplet | 0,070 | 0,021 | embedding belajar memisahkan penampilan |
| cos_same | 0,93 | 0,98 | potongan orang yang sama makin mirip |
| BCEacc (TBSS) | sekitar 0,50 | 0,494 sampai 0,505 | tidak belajar, lempar koin |

Bacaannya: LAE berhasil. Untuk TBSS, ada temuan penting 14 Agustus 2026: angka BCEacc validasi yang datar 0,5 selama ini TIDAK valid karena bug konstruksi fitur di validasi. Pasangan negatif di validasi salah memberi input: kotak yang dibandingkan sama dengan kotaknya sendiri sehingga IoU selalu 1,0, padahal di data latih IoU-nya dihitung dengan kotak anchor yang benar. Akibatnya pasangan negatif di validasi tampak seperti pasangan positif sempurna dan akurasi validasi macet di 0,5 apa pun yang dipelajari model. Artinya TBSS sebenarnya tidak pernah terukur dengan benar, dan skor validasi lama tidak bisa dipakai sebagai bukti TBSS gagal. Bug sudah diperbaiki (sisi kotak anchor dipakai konsisten di training, validasi, dan histogram) dan training dilanjutkan dari checkpoint yang ada.

Perbaikan v2 yang sudah dikerjakan sebelumnya juga tetap: TBSS diganti transformer 73 dimensi (attention-nya tidak efektif) menjadi MLP ringan input 6 angka (IoU, cosine, selisih box), optimizer TBSS dipisah, BCE diberi bobot, checkpoint ala YOLO (last/best.pt). Status: training v2 sedang berjalan; setelah fix ini, BCEacc validasi berikutnya adalah angka yang pertama kali valid.

Catatan jujur untuk presentasi: angka HOTA/IDF1 tracker usulan belum ada. Yang terbukti baru encoder penampilan berfungsi baik.

## 8. Status dan Langkah Berikutnya

- Baseline OC-SORT: selesai. DiffMOT: selesai. Tracker usulan: integrasi pertama selesai, tuning berjalan.
- Evaluasi pertama tracker usulan (LAE+TBSS, ckpt best.pt BCEacc 0,978, 14 Agustus 2026), protokol sama:

| Tracker | MOT20 HOTA | MOT20 IDF1 | DanceTrack HOTA | DanceTrack IDF1 |
|---|---|---|---|---|
| OC-SORT (baseline) | 36,51 | 42,88 | 28,39 | 26,63 |
| DiffMOT | 44,37 | 53,86 | 39,05 | 43,39 |
| Tracker usulan (LAE+TBSS, OCM, ma90_ea5, sm0.3_aw0.5) | **37,67** | 43,54 | 28,43 | 28,71 |
| Ablasi LAE-only | 12,01 | 10,17 | 19,61 | 18,69 |

Bacaannya: pipeline end-to-end sudah bekerja, dengan OCM + tuning gate berhasil menembus baseline OC-SORT (37,67 vs 36,51 HOTA MOT20, +1,16) sambil IDF1 naik (43,54 vs 42,88). DiffMOT tetap unggul jauh (44,37), posisi jujur untuk presentasi: tracker usulan menang tipis atas OC-SORT, kalah telak dari DiffMOT — alasan pivot ke LightTrack-ReID (S014). Ablasi LAE-only menunjukkan penampilan tanpa geometri justru merusak asosiasi, konsisten dengan pelajaran paper (LAE menambah di atas baseline IoU, bukan menggantikan).

### 8.1 Hasil akhir (16 Agustus 2026) — gate sweep + ASW

Sweep terakhir di atas OCM `ma90_ea5` dengan ckpt v2 `best.pt` (BCEacc 0,978):

| Konfigurasi | MOT20 HOTA | MOT20 MOTA | MOT20 IDF1 | DanceTrack HOTA | Bacaannya |
|---|---|---|---|---|---|
| sm0.3 aw0.5 (default, best) | **37,67** | 54,94 | **43,54** | 28,43 | tetap terbaik MOT20 |
| sm0.2 aw0.5 | 37,15 | 54,99 | 43,02 | **29,31** | DT terbaik, MOT20 turun |
| sm0.3 aw0.7 | 37,19 | 54,93 | 42,99 | 27,64 | tidak mengungguli |
| + ASW (Eq 10 paper) | 37,59 | 54,96 | 43,51 | 27,65 | negatif: tidak ada gain |

Keputusan: konfigurasi final = **sm0.3, appearance-w 0.5, ma90, ea5** — angka 37,67 HOTA MOT20 / 28,43 DanceTrack. ASW (bobot adaptif paper Eq 10) **tidak terbukti** di protokol kita (37,59 < 37,67; selisih ±0,1 di bawah noise run), dicatat sebagai hasil ablasi negatif — tidak dipakai. Gate `sm0.2` menarik untuk DanceTrack (29,31) tapi mengorbankan 0,52 HOTA MOT20, tidak diambil karena prioritas laporan adalah MOT20 (domain people counting padat).

- Hasil lengkap per-sekuens: `experiments/s2_final/{sm0.3_aw0.5,asw,sm0.2_aw0.5,sm0.3_aw0.7}/eval_results.csv`

- Status tuning tracker usulan: **selesai** (sweep gate + ASW dieksekusi 16 Agustus 2026, hasil di 8.1). Selanjutnya di kampus hanya bila ada GPU luang: konfirmasi per-sekuens (MOT17 test) atau uji cepat pada video real people-counting.

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
