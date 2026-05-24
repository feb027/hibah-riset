# Ringkasan Bahasa Indonesia — Phase 2.5 Full-Text Notes

> Dokumen ini dibuat untuk menjembatani full-text notes yang sebagian besar berbahasa Inggris dengan kebutuhan writer Phase 3 yang harus menulis dalam Bahasa Indonesia akademik-natural. Gunakan ringkasan ini sebagai peta cepat; detail klaim tetap harus dicek di masing-masing note.

## Prinsip umum untuk writer

- Source ledger adalah peta sumber; full-text notes adalah batas klaim yang boleh dipakai.
- YOLO26 (`S001`, `S002`) hanya untuk konteks kandidat implementasi/prototipe, bukan anchor novelty akademik.
- Argumen akademik NMS-free/end-to-end detector harus ditopang terutama oleh `S003` YOLOv10 dan `S004` RT-DETR.
- `S027` dan `S028` membahas crowd counting/density estimation; jangan dipakai untuk membuktikan line-crossing, ID tracking, atau anti-double-counting.
- `S021` adalah anchor DiffMOT; `S024` adalah fallback/baseline OC-SORT; `S025` adalah metrik HOTA.

## Ringkasan per sumber

### S001 — YOLO26 arXiv analysis

- Status: `C-caution`, preprint/analisis sekunder.
- Pakai untuk: konteks terbaru YOLO26, NMS-free, MuSGD, STAL, ProgLoss, YOLOE-26, export gap.
- Jangan pakai untuk: bukti peer-reviewed, klaim people-counting, atau novelty utama.

### S002 — Ultralytics YOLO26 docs

- Status: `C-caution`, vendor docs.
- Pakai untuk: fitur implementasi YOLO26, supported tasks, model files, one-to-one vs one-to-many head, deployment/edge feasibility.
- Jangan pakai untuk: bukti akademik SOTA atau performa people counting.

### S003 — YOLOv10

- Status: `A-main`, NeurIPS 2024.
- Pakai untuk: anchor akademik YOLO-style end-to-end/NMS-free detector.
- Batas: object detection COCO; bukan tracking/counting.

### S004 — RT-DETR

- Status: `A-main`, CVPR 2024.
- Pakai untuk: end-to-end real-time detector tanpa NMS yang kompetitif.
- Batas: object detection; bukan people-counting pipeline.

### S010 — Passenger flow YOLO Edge AI

- Status: `A-main`, applied edge people counting.
- Pakai untuk: contoh people-counting berbasis YOLO + edge/Jetson + passenger-flow scenario.
- Batas: domain spesifik; jangan generalisasi ke semua CCTV/kerumunan.

### S011 — Vision-based people counting and tracking

- Status: `A-main`, 2026 people counting/tracking.
- Pakai untuk: pipeline counting + tracking di urban/passenger environment.
- Batas: cek dataset/generalization; jangan overclaim ke sistem usulan.

### S018 — OcclusionTrack

- Status: `A-main`, dense-scene occlusion MOT.
- Pakai untuk: oklusi padat, confidence Kalman filtering, camera motion compensation, trajectory reactivation.
- Batas: detector-dependent; bukan counting method.

### S021 — DiffMOT

- Status: `A-main`, CVPR 2024.
- Pakai untuk: diffusion-based non-linear motion prediction dalam MOT.
- Batas: kompleksitas model dan tetap bergantung pada kualitas deteksi.

### S024 — OC-SORT

- Status: `B-support`, CVPR 2023 baseline/fallback.
- Pakai untuk: baseline ringan berbasis observation-centric recovery.
- Batas: jangan strawman sebagai metode buruk; posisikan sebagai fallback efisien.

### S025 — HOTA

- Status: `B-support`, metric.
- Pakai untuk: evaluasi MOT yang menyeimbangkan detection, association, dan localization.
- Batas: metrik, bukan metode.

### S027 — Crowd counting complex review

- Status: `A-main`, review 2026.
- Pakai untuk: tantangan crowd counting seperti density, perspective, occlusion, lighting, dan dataset taxonomy.
- Batas: review; banyak bahasan density-map, bukan ID/trajectory counting.

### S028 — Edge crowd counting KD

- Status: `A-main`, Scientific Reports 2025.
- Pakai untuk: edge crowd counting dan knowledge distillation.
- Batas: density-map crowd counting; tidak memberi ID lintasan/arah.

## Formula aman untuk draft

- “YOLO26 diposisikan sebagai kandidat implementasi karena dokumentasi vendor dan preprint 2026 menekankan NMS-free/edge deployment; namun, argumen ilmiah mengenai end-to-end detector tetap ditopang oleh YOLOv10 dan RT-DETR yang telah peer-reviewed.”
- “Studi crowd counting berbasis density map kuat untuk estimasi jumlah pada kerumunan, tetapi tidak selalu menyediakan identitas, arah lintasan, dan state memory yang diperlukan untuk line/zone-based people counting.”
- “MOT modern seperti DiffMOT dan OcclusionTrack menunjukkan perhatian pada non-linear motion dan oklusi, tetapi integrasi dengan counting logic berbasis RoI/ID masih perlu dirancang dan divalidasi pada skenario ruang publik.”
