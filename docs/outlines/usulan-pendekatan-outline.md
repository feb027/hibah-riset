# Outline Usulan Pendekatan / Proposed Method

> Status: outline kerja untuk Phase 6. Bagian ini belum berisi hasil eksperimen; semua skenario masih berupa rencana metodologi.

## 1. Gambaran umum pendekatan

Fungsi: menjembatani gap dari `PENDAHULUAN` dan `PEKERJAAN TERKAIT` ke rancangan sistem.

Isi wajib:
- masalah yang ditangani: real-time people counting berbasis video pada ruang publik;
- prinsip pendekatan: detection-tracking-counting;
- kontribusi rancangan: detector real-time/NMS-free, tracker robust, fallback ringan, counting logic berbasis RoI/zone/ID memory;
- batasan: belum eksperimen aktual.

Source anchor: S001, S002, S003, S004, S010, S011, S021, S024, S025, S026, S035, S036, S037, S038.

## 2. Arsitektur sistem yang diusulkan

Subbagian:

### 2.1 Input video dan preprocessing
- video CCTV/rekaman ruang publik;
- frame extraction/resizing;
- RoI/zone/line annotation;
- anonymization jika data lokal mengandung wajah/identitas;
- frame timestamp dan metadata kamera.

### 2.2 Deteksi manusia real-time
- YOLO26 sebagai kandidat implementasi/prototipe;
- YOLOv10/RT-DETR sebagai baseline akademik NMS-free/end-to-end;
- output: bounding box manusia, confidence, class label, timestamp.

### 2.3 Multi-object tracking
- DiffMOT sebagai tracker utama untuk motion non-linear;
- OC-SORT/SORT-family sebagai fallback efisien;
- output: track ID, bbox per frame, track confidence/status.

### 2.4 Counting logic
- RoI polygon;
- line crossing / zone-to-zone transition;
- trajectory validation;
- ID state memory: unseen, inside-zone, counted-in, counted-out, expired;
- debouncing/cooldown untuk mencegah hitung ulang;
- handling ID switch/track reactivation secara konservatif.

### 2.5 Output dan logging
- count masuk/keluar/per zona;
- log event per ID;
- visual overlay;
- evaluasi FPS/latency;
- error log untuk analisis.

## 3. Rencana data dan preprocessing

- Data publik:
  - CrowdHuman untuk crowd/person detection.
  - MOT20 untuk dense pedestrian tracking.
  - DanceTrack untuk diverse motion dan uniform appearance.
- Data target/lokal:
  - rekaman ruang publik/kampus jika izin tersedia;
  - alternatif video publik dengan lisensi/akses jelas.
- Ground truth:
  - anotasi bbox/track menggunakan format dataset publik bila tersedia;
  - anotasi counting manual untuk line/zone crossing.

## 4. Tahapan metodologi

1. Definisi skenario dan zona hitung.
2. Persiapan data dan anotasi.
3. Implementasi/integrasi detector.
4. Integrasi tracker utama dan fallback.
5. Perancangan counting logic.
6. Logging evaluasi.
7. Analisis error dan perbaikan rancangan.

## 5. Rencana skenario eksperimen

### Skenario A — Detector
Membandingkan kandidat detector pada data manusia/crowd: akurasi, latency, dan stabilitas deteksi kecil/teroklusi.

### Skenario B — Tracker
Membandingkan DiffMOT dan OC-SORT/SORT-family pada skenario oklusi, gerak non-linear, dan crowd.

### Skenario C — Counting logic
Ablation:
- line crossing sederhana;
- line crossing + RoI;
- RoI + zone transition;
- RoI + zone transition + ID state memory + debouncing.

### Skenario D — Real-time readiness
Mengukur FPS/latency end-to-end, penggunaan CPU/GPU/memori, dan kelayakan konfigurasi untuk perangkat target.

### Skenario E — Domain target
Validasi awal pada video ruang publik/kampus atau video CCTV publik yang paling mirip domain target.

## 6. Metrik evaluasi

- Detector: AP/mAP, precision, recall, false positive/false negative, detector latency.
- Tracker: HOTA, IDF1, MOTA, ID switches, fragmentation.
- Counting: absolute counting error, MAE/MAPE per video/zona, over-count, under-count, direction accuracy.
- Real-time: FPS, end-to-end latency, CPU/GPU/memory utilization.

## 7. Ancaman validitas

- Internal: konfigurasi detector/tracker dapat memengaruhi hasil.
- Construct: AP/MOTA tidak sama dengan akurasi counting.
- Conclusion: jumlah video/skenario kecil dapat membuat kesimpulan lemah.
- External: dataset publik belum tentu merepresentasikan CCTV lokal.

## 8. Anti-overclaim rules

- Jangan menulis “hasil menunjukkan” sebelum eksperimen dilakukan.
- Gunakan “direncanakan”, “akan dievaluasi”, “rancangan ini menempatkan”, “skenario evaluasi disiapkan”.
- YOLO26 = kandidat implementasi, bukan novelty akademik tunggal.
- S035 = referensi teknis/vendor, bukan bukti SOTA akademik.
- Density-map counting dan trajectory-based counting harus tetap dibedakan.
