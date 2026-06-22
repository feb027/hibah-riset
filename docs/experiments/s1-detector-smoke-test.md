# Eksperimen Card — S1 Detector Smoke Test (Tier 1)

Mirror dari `experiments/s1_detector_smoke/README.md` untuk visibilitas
di folder `docs/`.

| Field | Value |
|---|---|
| ID | S1 |
| Tier | 1 (smoke test) |
| Status kode | `draft_code` |
| Tanggal mulai | 2026-06-22 |
| Penanggung jawab | Mahasiswa (eksekusi di Colab) |
| Reviewer | Strict reviewer (post-run) |
| Sumber sitasi | S001, S002, S003, S004 |
| Detektor utama | `yolov10s` (S003) |
| Output utama | annotated video, per-frame CSV, summary JSON |

## Pertanyaan yang dijawab

- Apakah pipeline deteksi orang (input → detector → BBox + count) bisa
  dijalankan end-to-end pada GPU Colab dalam < 5 menit untuk video pendek?
- Berapa FPS rata-rata + p95 latency untuk `yolov10s`, `yolo26n`, dan
  `yolov11n` pada sample video yang sama?

## Pertanyaan yang TIDAK dijawab

- Apakah YOLOv10 lebih akurat dari RT-DETR pada dataset tertentu? (butuh mAP + eval set.)
- Apakah YOLO26 lebih baru dari YOLOv10/11/12? (paper; bukan eksperimen.)
- Bagaimana tracker S2 berperforma? (Tier 2.)
- Bagaimana counting logic S3 berperforma? (Tier 3.)

## Metrik yang dicatat

| Metrik | Unit | Valid untuk klaim? |
|---|---|---|
| `fps_avg` | frames/sec | Hanya sebagai diagnostik runtime, bukan klaim SOTA |
| `latency_p50_ms` | ms | Sama |
| `latency_p95_ms` | ms | Sama |
| `latency_mean_ms` | ms | Sama |
| `mean_persons_per_frame` | float | Diagnostik; bukan akurasi counting |
| `max_persons_in_frame` | int | Diagnostik |
| `total_frames_processed` | int | Diagnostik |

## Metrik yang TIDAK dicatat di Tier 1

- mAP / AP50 / AP75 (butuh COCO-format ground truth)
- precision / recall per class
- HOTA / IDF1 / MOTA (butuh track eval — Tier 2)
- MAE / MAPE / counting error (butuh ground truth event — Tier 3)
- FPS klaim "real-time" tanpa ukur di hardware target

## Cara menjalankan

Lihat `experiments/s1_detector_smoke/README.md` atau langsung buka
`notebooks/01_smoke_test_detector.ipynb` di Colab.

## Setelah run

1. Simpan artefak di `experiments/s1_detector_smoke/` (jangan di-commit
   file besar — lihat `.gitignore`).
2. Isi tabel "Hasil Run" di bawah (oleh mahasiswa).
3. Reviewer strict pass → `docs/reviews/review-s1-smoke.md`.

## Hasil Run (kosong sampai dieksekusi)

| Run ID | Tanggal | Detektor | FPS avg | p50 ms | p95 ms | mean persons | Catatan |
|---|---|---|---|---|---|---|---|
| _-_ | _-_ | _-_ | _-_ | _-_ | _-_ | _-_ | _-_ |
