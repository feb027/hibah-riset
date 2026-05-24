# Outline — PEKERJAAN TERKAIT

> Draft only after `source-ledger.md` and `evidence-matrix.md` are sufficiently filled.

## 1. Deteksi manusia real-time dan NMS-free detector

- Bahas perkembangan YOLO/real-time detector untuk deteksi manusia pada video.
- Sorot kebutuhan latency rendah untuk CCTV/edge.
- Audit klaim YOLO26 dari sumber primer.

## 2. Multi-object tracking pada kerumunan padat

- Tracking-by-detection sebagai paradigma dominan.
- Tantangan: occlusion, identity switch, small objects, camera angle, non-linear motion.
- Bandingkan SORT/OC-SORT/ByteTrack-family dengan modern tracker.

## 3. Diffusion/transformer/modern MOT untuk lintasan non-linear

- DiffMOT sebagai kandidat inti.
- Sumber 2025/2026 untuk occlusion-aware/transformer/end-to-end MOT.
- Analisis trade-off akurasi vs biaya komputasi.

## 4. People counting berbasis RoI dan trajectory logic

- Bedakan crowd counting density-map vs detection-tracking-counting pipeline.
- Bahas RoI polygon, line/zone crossing, trajectory validation, ID memory.
- Gap: double-counting dan kehilangan ID saat oklusi.

## 5. Dataset, metrik, dan deployment

- Dataset benchmark: CrowdHuman, MOT20, DanceTrack, plus dataset people counting relevan.
- Metrik: HOTA, MOTA, IDF1, FP/FN/ID switches, FPS/latency.
- Deployment edge/real-time: kebutuhan fallback ringan.

## 6. Sintesis gap dan posisi penelitian

- Tunjukkan bahwa studi terdahulu sering kuat di salah satu sisi: deteksi, tracking, atau counting; tetapi integrasi end-to-end untuk counting real-time di kondisi padat masih membutuhkan desain gabungan.
- Posisi penelitian: YOLO26 + DiffMOT + OC-SORT fallback + advanced counting logic.
