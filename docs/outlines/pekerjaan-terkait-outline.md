# Outline Final Phase 2 — PEKERJAAN TERKAIT

> Status: **READY FOR PHASE 3 DRAFTING** setelah reviewer pass.  
> Tanggal: 25 Mei 2026 WIB.  
> Basis: `docs/research/source-ledger.md`, `docs/research/evidence-matrix.md`, dan panduan dosen pada `docs/_extracted/f_paper_penelitian.md`.

## Tujuan bagian PEKERJAAN TERKAIT

Bagian ini tidak boleh menjadi daftar paper. Fungsi utamanya adalah:

1. mengelompokkan penelitian terdahulu berdasarkan kelas persoalan/metode;
2. menjelaskan capaian utama tiap kelompok studi;
3. menilai keterbatasan faktualnya;
4. menunjukkan gap yang mengarah secara logis ke proposal: **detector real-time/NMS-free + tracker occlusion-aware/non-linear + fallback ringan + advanced counting logic berbasis RoI/zone/ID memory**.

## Posisi argumen utama

Argumen related work yang akan dibangun:

> Studi terbaru telah maju pada tiga jalur utama—deteksi objek real-time, multi-object tracking pada skenario padat, dan crowd/people counting. Namun banyak pendekatan masih kuat pada salah satu komponen saja: detector cepat, tracker robust, density-counting, atau edge compression. Untuk target real-time people counting di ruang publik, masih diperlukan integrasi pipeline yang menjaga kecepatan deteksi, konsistensi identitas saat oklusi/pergerakan non-linear, serta validasi hitung berbasis lintasan/zona agar mengurangi double-counting.

Formulasi gap aman: **“masih terbatas / masih membutuhkan integrasi dan validasi”**, bukan “belum ada penelitian sama sekali”.

---

# Struktur Outline

## 1. People counting dalam konteks ruang publik dan smart surveillance

### Fungsi paragraf

Membuka related work dari domain masalah, bukan langsung dari YOLO. Jelaskan bahwa people counting dipakai untuk manajemen kapasitas, keselamatan, transportasi, smart building, dan smart surveillance. Masalahnya makin sulit ketika kamera menghadapi kepadatan tinggi, pencahayaan berubah, perspektif jauh, oklusi, dan pergerakan tidak linier.

### Isi yang harus ditulis

- Definisikan real-time people counting sebagai proses menghitung orang dari aliran video, bukan sekadar deteksi satu frame.
- Jelaskan dua rumpun pendekatan:
  1. **density-map crowd counting**: memperkirakan jumlah kerumunan dari peta kepadatan;
  2. **detection-tracking-counting**: mendeteksi individu, mempertahankan ID/lintasan, lalu menghitung berdasarkan RoI/line/zone.
- Tegaskan proposal ini berada pada rumpun kedua karena targetnya menghitung orang secara real-time dengan arah/lintasan/ID persistence.

### Sumber utama

- S011 — Vision-Based People Counting and Tracking for Urban Environments, 2026.
- S027 — Deep learning for crowd counting in complex environments, 2026.
- S029 — Deep learning in crowd counting: A survey, 2024.
- S030 — Federated Learning for Crowd Counting in Smart Surveillance Systems, 2024.
- S010 — Real-Time Passenger Flow Analysis in Tram Stations using YOLO and Edge AI, 2025.
- S034 — High-accuracy occupancy counting at crowded entrances, 2024.

### Kelebihan studi terdahulu yang perlu disebut

- Survey dan studi aplikasi menunjukkan people counting relevan untuk surveillance, transportasi, smart building, dan manajemen fasilitas.
- Studi edge/passenger flow membuktikan feasibility YOLO-based counting pada perangkat terbatas.
- Studi occupancy counting memperlihatkan kebutuhan akurasi di area masuk/keluar yang padat.

### Keterbatasan/gap yang perlu ditarik

- Density-map counting kuat untuk estimasi jumlah total, tetapi tidak selalu memberi ID, arah lintasan, atau pencegahan double-counting.
- Studi aplikasi biasanya domain-specific; belum otomatis cukup untuk generalisasi ke ruang publik lain.
- Counting yang membutuhkan arah/keluar-masuk perlu dukungan tracker dan counting logic, bukan detector saja.

### Output mini-synthesis

Paragraf akhir seksi ini harus menyambungkan ke kebutuhan detector real-time dan tracker: karena target counting berbasis lintasan, sistem perlu mendeteksi manusia dengan cepat dan menjaga identitas objek lintas frame.

---

## 2. Deteksi manusia real-time dan pergeseran menuju end-to-end/NMS-free detector

### Fungsi paragraf

Menjelaskan SOTA detector yang relevan untuk pipeline people counting. Fokusnya bukan membuktikan YOLO26 “paling baru”, tetapi menunjukkan tren akademik bahwa latency dan end-to-end detection penting untuk real-time video.

### Isi yang harus ditulis

- Bahas YOLO sebagai keluarga detector real-time yang banyak digunakan untuk surveillance dan edge vision.
- Jelaskan masalah NMS secara singkat: post-processing dapat menambah latency dan membutuhkan hyperparameter.
- Bahas pergeseran ke end-to-end / NMS-free detection melalui YOLOv10 dan RT-DETR-family.
- Tempatkan YOLO26 sebagai kandidat implementasi terbaru, tetapi klaim akademiknya harus didukung oleh sumber peer-reviewed terdahulu.

### Sumber utama

- S003 — YOLOv10: Real-Time End-to-End Object Detection, NeurIPS 2024.
- S004 — RT-DETR / DETRs Beat YOLOs on Real-time Object Detection, CVPR 2024.
- S005 — D-FINE, ICLR 2025.
- S006 — DEIM, CVPR 2025.
- S007 — RF-DETR, ICLR 2026.
- S008 — A Decade of YOLO review, IEEE Access 2025.
- S001/S002 — YOLO26 arXiv/vendor docs, **caution only**.
- S009 — Edge object recognition constraints, 2025.

### Kelebihan studi terdahulu yang perlu disebut

- YOLO-family menyediakan baseline real-time kuat untuk video analytics.
- YOLOv10 dan RT-DETR-family menguatkan tren NMS-free/end-to-end detection.
- D-FINE/DEIM/RF-DETR menunjukkan SOTA detector makin menyeimbangkan akurasi, latency, dan efisiensi training/inference.

### Keterbatasan/gap yang perlu ditarik

- Detector yang cepat belum menjamin counting akurat jika ID objek sering hilang/tertukar.
- Benchmark detector sering berfokus pada AP/latency, bukan akurasi hitung berbasis lintasan.
- YOLO26 belum boleh dijadikan satu-satunya novelty akademik karena saat ini lebih kuat sebagai sumber vendor/preprint.

### Output mini-synthesis

Akhiri dengan transisi: detector real-time menyelesaikan sebagian masalah latency, tetapi people counting di kerumunan padat tetap membutuhkan MOT untuk menjaga identitas dan lintasan.

---

## 3. Multi-object tracking pada kerumunan padat, oklusi, dan identity switch

### Fungsi paragraf

Membangun latar belakang MOT sebagai komponen kunci untuk detection-tracking-counting. Fokus pada tantangan identity switch, missed detection, track fragmentation, dan oklusi.

### Isi yang harus ditulis

- Jelaskan paradigma tracking-by-detection: detector menghasilkan bounding box, tracker mengasosiasikan objek antar-frame.
- Bahas masalah dense crowd: objek saling menutup, ukuran kecil, appearance mirip, dan lintasan tidak linier.
- Bahas baseline SORT/OC-SORT/SORT-family secara adil: efisien dan kuat sebagai baseline, tetapi tetap punya batas pada oklusi berat/gerak kompleks.
- Masukkan perkembangan 2024–2026: confidence-aware, ID-centric, track-centric, transformer/graph, occlusion-aware.

### Sumber utama

- S024 — OC-SORT, CVPR 2023.
- S023 — Hybrid-SORT, AAAI 2024.
- S020 — BoostTrack, 2024.
- S013 — Sentinel confidence-aware MOT, 2026.
- S014 — LightTrack-ReID, 2026.
- S015 — Focusing on Tracks, CVPR 2025.
- S016 — Multiple Object Tracking as ID Prediction, CVPR 2025.
- S017 — DragonTrack, WACV 2025.
- S018 — OcclusionTrack, 2025.
- S019 — Heavy occlusion dense crowd / head-focused tracking, 2024.

### Kelebihan studi terdahulu yang perlu disebut

- OC-SORT/Hybrid-SORT/BoostTrack menawarkan efisiensi dan peningkatan asosiasi objek.
- Track-centric dan ID-centric MOT memperkuat fokus pada konsistensi identitas.
- Occlusion-aware dan confidence-aware methods mulai eksplisit menangani skenario dense scene.

### Keterbatasan/gap yang perlu ditarik

- Sebagian metode masih bergantung pada kualitas detector.
- Metode transformer/graph/ReID dapat meningkatkan asosiasi tetapi berpotensi menambah beban komputasi.
- Robust tracking belum otomatis menghasilkan counting logic yang benar jika crossing zone/ID state tidak didefinisikan.

### Output mini-synthesis

Akhiri dengan kebutuhan memilih tracker utama dan fallback: pendekatan kuat perlu menangani non-linear motion, tetapi sistem real-time juga memerlukan alternatif ringan bila biaya komputasi tinggi.

---

## 4. Diffusion-based MOT dan prediksi lintasan non-linear

### Fungsi paragraf

Menjelaskan mengapa proposal memakai DiffMOT, tetapi tetap kritis terhadap trade-off komputasi.

### Isi yang harus ditulis

- Jelaskan bahwa DiffMOT memakai pendekatan diffusion/probabilistic untuk prediksi lintasan non-linear.
- Bandingkan dengan DiffusionTrack sebagai keluarga pendekatan diffusion tracking.
- Kaitkan dengan masalah people counting: non-linear motion dan oklusi menyebabkan ID switch/double-counting bila lintasan tidak dipertahankan.
- Masukkan batasan: diffusion-based tracking berpotensi lebih kompleks sehingga fallback OC-SORT/Hybrid-SORT-family tetap perlu.

### Sumber utama

- S021 — DiffMOT, CVPR 2024.
- S022 — DiffusionTrack, AAAI 2024.
- S033 — CrowdDiff, CVPR 2024, sebagai pembanding diffusion pada density counting, bukan MOT.
- S024 — OC-SORT, CVPR 2023, sebagai fallback ringan.
- S023/S020 — Hybrid-SORT/BoostTrack sebagai pembanding SORT-family modern.

### Kelebihan studi terdahulu yang perlu disebut

- DiffMOT langsung relevan dengan prediksi gerak non-linear.
- DiffusionTrack menunjukkan diffusion model menjadi tren dalam tracking/association.
- CrowdDiff menunjukkan diffusion juga masuk crowd-density estimation, tetapi problemnya berbeda.

### Keterbatasan/gap yang perlu ditarik

- Diffusion model dapat menambah kompleksitas dan runtime.
- Paper diffusion tracking tidak otomatis membahas counting berbasis RoI/zone.
- Karena target sistem real-time, perlu desain fallback dan evaluasi FPS/latency.

### Output mini-synthesis

Paragraf akhir harus memposisikan DiffMOT sebagai tracker utama untuk robustness, sedangkan OC-SORT/SORT-family sebagai fallback efisien pada perangkat terbatas.

---

## 5. Counting logic berbasis RoI, line/zone crossing, trajectory validation, dan ID memory

### Fungsi paragraf

Menutup lubang antara “tracking bagus” dan “counting benar”. Jelaskan bahwa counting membutuhkan aturan spasial-temporal agar tidak menghitung objek dua kali.

### Isi yang harus ditulis

- Jelaskan RoI polygon sebagai area aktif yang membatasi ruang hitung.
- Jelaskan line/zone crossing dan direction detection untuk menghitung masuk/keluar atau perpindahan antar-area.
- Jelaskan trajectory validation agar hitungan hanya terjadi jika lintasan melewati urutan zona yang valid.
- Jelaskan ID state memory untuk mencegah double-counting ketika track sempat hilang lalu muncul kembali.
- Tekankan bahwa sumber teknis/vendor boleh membantu menjelaskan implementasi, tetapi bukti akademik tetap dari people-counting/tracking studies.

### Sumber utama

- S011 — Vision-Based People Counting and Tracking, 2026.
- S010 — Passenger Flow YOLO + Edge AI, 2025.
- S034 — Occupancy counting at crowded entrances, 2024.
- S035 — NVIDIA DeepStream nvdsanalytics docs, 2026, **technical reference only**.
- S024/S025/S026 — tracker + metrics supporting ID consistency.

### Kelebihan studi terdahulu yang perlu disebut

- Studi aplikasi menunjukkan counting perlu dikaitkan dengan area/zona dan lingkungan operasional nyata.
- DeepStream-style analytics mendokumentasikan praktik ROI, line crossing, direction detection, dan tracker-ID dependency.
- Metrik IDF1/HOTA membantu menilai apakah tracker cukup stabil sebelum counting.

### Keterbatasan/gap yang perlu ditarik

- Dokumentasi vendor bukan bukti SOTA akademik.
- Sistem counting berbasis line/zone bisa gagal ketika ID switch, missed detection, atau track fragmentation terjadi.
- Masih perlu integrasi eksplisit antara tracker non-linear dan state memory untuk mengurangi double-counting.

### Output mini-synthesis

Akhiri dengan kalimat bahwa people counting yang andal harus dievaluasi tidak hanya dari akurasi deteksi/tracking, tetapi juga dari error hitung dan kestabilan ID pada zona yang relevan.

---

## 6. Dataset, metrik evaluasi, dan constraint real-time/edge

### Fungsi paragraf

Menjelaskan bagaimana studi terdahulu dievaluasi dan bagaimana riset ini akan mengukur keberhasilan secara seimbang.

### Isi yang harus ditulis

- Dataset deteksi/tracking:
  - CrowdHuman untuk human detection pada crowd/occlusion.
  - MOT20 untuk pedestrian tracking crowded scenes.
  - DanceTrack untuk motion diverse dan appearance uniform.
- Metrik tracking:
  - HOTA untuk keseimbangan detection-association.
  - IDF1 untuk konsistensi identitas.
  - MOTA/ID switches sebagai metrik tambahan bila digunakan.
- Metrik deployment:
  - FPS/latency/resource usage.
- Metrik counting:
  - counting error/MAE atau error count per video/zone bila data tersedia.

### Sumber utama

- S036 — MOT20.
- S037 — DanceTrack.
- S038 — CrowdHuman.
- S025 — HOTA.
- S026 — IDF1.
- S009 — edge constraints.
- S010/S028/S031/S032 — edge/counting deployment references.

### Kelebihan studi terdahulu yang perlu disebut

- Dataset standar memungkinkan perbandingan dengan komunitas riset.
- HOTA/IDF1 lebih sesuai untuk tracking-based counting dibanding hanya AP detector.
- Studi edge menunjukkan evaluasi perlu memasukkan latency/resource, bukan hanya akurasi.

### Keterbatasan/gap yang perlu ditarik

- Dataset standar belum tentu merepresentasikan kamera lokal/ruang publik target.
- Dataset tracking tidak selalu punya label counting/zone.
- Validasi TKT awal perlu rekaman atau skenario representatif lokal, bukan hanya benchmark publik.

### Output mini-synthesis

Seksi ini harus menyimpulkan bahwa evaluasi riset perlu multi-metrik: detection, association, count error, dan real-time performance.

---

## 7. Sintesis gap dan posisi penelitian

### Fungsi paragraf

Ini bagian akhir related work. Harus menyatukan semua seksi dan membuka ruang untuk solusi yang ditawarkan penelitian.

### Isi yang harus ditulis

Tuliskan gap secara bertingkat:

1. **Gap detector → counting**: detector real-time/NMS-free menurunkan latency, tetapi belum cukup untuk counting bila ID antar-frame tidak stabil.
2. **Gap tracker → counting**: tracker modern menangani asosiasi/oklusi, tetapi belum otomatis menentukan aturan hitung berbasis RoI/zone/trajectory.
3. **Gap density counting → ID counting**: density-map kuat untuk estimasi jumlah, tetapi tidak memberi arah lintasan/keluar-masuk/ID state.
4. **Gap accuracy → deployability**: metode akurat sering perlu diuji terhadap FPS/latency/resource agar layak real-time.
5. **Gap benchmark → domain target**: benchmark publik perlu dilengkapi validasi rekaman lingkungan publik yang representatif.

### Posisi penelitian yang aman

Penelitian ini diposisikan sebagai upaya merancang pipeline people counting real-time yang mengintegrasikan:

- detector real-time/NMS-free dengan YOLO26 sebagai kandidat implementasi terbaru;
- DiffMOT sebagai tracker utama untuk gerak non-linear dan oklusi;
- OC-SORT/SORT-family sebagai fallback efisien pada perangkat terbatas;
- advanced counting logic berbasis RoI polygon, zone-to-zone trajectory validation, dan ID state memory;
- evaluasi multi-metrik: HOTA, IDF1/MOTA, counting error, dan FPS/latency.

### Rumusan gap final yang boleh dipakai

> Berdasarkan kajian tersebut, penelitian terdahulu telah menunjukkan kemajuan signifikan pada deteksi objek real-time, pelacakan multi-objek, serta crowd/people counting. Namun, integrasi yang secara eksplisit menggabungkan detector real-time, tracker yang adaptif terhadap oklusi dan gerak non-linear, fallback ringan untuk keterbatasan perangkat, serta counting logic berbasis zona dan memori identitas masih perlu diperdalam, terutama untuk skenario public-space people counting yang menuntut akurasi hitung dan pemrosesan real-time secara bersamaan.

---

# Source-to-section map

| Section | Primary sources | Support/caution |
|---|---|---|
| 1. Domain people counting | S011, S027, S029, S030, S010, S034 | S028, S031, S032 |
| 2. Real-time/NMS-free detector | S003, S004, S005, S006, S007, S008 | S001, S002, S009, S012 |
| 3. Dense MOT/occlusion | S013, S014, S015, S016, S017, S018, S020, S023, S024 | S019, S025, S026 |
| 4. Diffusion MOT | S021, S022 | S033, S024, S023, S020 |
| 5. Counting logic | S011, S010, S034 | S035, S024, S025, S026 |
| 6. Dataset/metrics/deployment | S036, S037, S038, S025, S026, S009 | S010, S028, S031, S032 |
| 7. Gap synthesis | S003–S011, S013–S026, S027–S038 | S001, S002, S035 only as caution/context |

---

# Anti-overclaim rules for Phase 3 writer

1. Jangan menulis “belum ada penelitian” kecuali sudah dibuktikan. Gunakan “masih terbatas”, “masih perlu”, atau “belum banyak yang mengintegrasikan secara eksplisit”.
2. Jangan menyebut YOLO26 sebagai paper peer-reviewed. Tulis sebagai kandidat implementasi terbaru berbasis sumber vendor/preprint, sementara dasar akademik NMS-free diambil dari YOLOv10/RT-DETR-family.
3. Jangan menyamakan density-map crowd counting dengan trajectory-based people counting.
4. Jangan klaim sistem usulan lebih akurat sebelum eksperimen dilakukan.
5. Jangan menulis angka performa paper sebelum full text dibaca dan angka diverifikasi.
6. Jangan memakai vendor docs sebagai sitasi utama untuk SOTA akademik.
7. Jika MDPI dipakai, sandingkan dengan anchor non-MDPI dari IEEE/CVF/Springer/Elsevier/Nature/Wiley/IET.

# Phase 3 readiness checklist

- [x] Source ledger memenuhi target jumlah dan kebaruan.
- [x] Reviewer source ledger memberi verdict `READY_FOR_OUTLINE`.
- [x] Outline tematik, bukan paper-by-paper.
- [x] Setiap seksi punya fungsi paragraf, sumber utama, kelebihan, keterbatasan, dan mini-synthesis.
- [x] Gap final sudah aman dari overclaim.
- [ ] Sebelum draft final, baca full text sumber utama: S003, S004, S010, S011, S018, S021, S024, S025, S027, S028.
