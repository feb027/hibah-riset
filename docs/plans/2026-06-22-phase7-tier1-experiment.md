# Phase 7 — Tier 1 Detector Smoke Test

> **Tanggal mulai**: 22 Juni 2026
> **Status**: kode scaffold + notebook siap; **belum dieksekusi** di Colab.
> **Outcome gate**: smoke test jalan tanpa error; FPS rata-rata > 5 fps
> pada Colab T4 dengan max_frames=200.

## Latar belakang eskalasi scope

Sebelum Phase 7, AGENTS.md eksplisit menulis
*"Out of scope sekarang: training, prototipe inference, eksperimen GPU"*.
Pada 22 Juni 2026, dosen meminta agar mahasiswa **menyiapkan dataset dan
mencoba eksperimen**. Artinya eskalasi dari fase kepustakaan ke fase
implementasi terbatas. Phase 7 menjawab eskalasi tersebut dengan Tier 1
yang konservatif: inference-only, smoke test, no training.

## Tujuan Tier 1

1. Membuktikan pipeline deteksi orang (detector → output → visualisasi)
   bisa dijalankan pada GPU Colab.
2. Memetakan `DETECTOR_CATALOGUE` ke source-ledger (S003/S004/S001/S002).
3. Menghasilkan artefak yang bisa di-commit ke repo (annotated video, CSV,
   JSON, plot diagnostik) **tanpa** klaim akurasi SOTA.

## Komponen yang dibuat

- `src/detector.py` — wrapper PeopleDetector + `DETECTOR_CATALOGUE`.
- `src/pipeline.py` — `run_smoke_test()` end-to-end + CLI.
- `src/eval_detection.py` — agregasi statistik per frame.
- `src/utils/video_io.py` — probe video, iter frames, draw boxes, tulis video.
- `notebooks/01_smoke_test_detector.ipynb` — Colab-ready.
- `configs/s1_detector_smoke.yaml` — konfigurasi eksperimen.
- `experiments/s1_detector_smoke/README.md` — eksperimen card singkat.
- `scripts/smoke_test_detector.py` — entry point CLI lokal.
- `scripts/download_mot17_mini.py` + `scripts/download_mall_dataset.py` —
  helper untuk Tier 2.
- `data/README.md`, `models/README.md` — dokumentasi dataset + model.
- `.gitignore` — di-update untuk ignore `data/`, `models/`, `*.pt`,
  `*.onnx`, `experiments/*/runs/`.

## Batasan Tier 1 (CRITICAL)

- **No training**, **no fine-tuning**, **no mAP/HOTA/MOTA**.
- Sample video = CC0 pendek atau synthetic (bukan CrowdHuman/MOT20).
- "Real-time" TIDAK boleh diklaim tanpa latency diukur di hardware target.
- YOLO26 (S001/S002) tetap berstatus caution. Eksperimen aktual pakai
  YOLOv10 (S003) sebagai anchor dan YOLOv11n sebagai baseline Ultralytics.

## Acceptance criteria

- [x] Scaffold repo terbentuk (`src/`, `configs/`, `data/`, `notebooks/`,
      `experiments/`, `models/`).
- [x] `src/detector.py` punya `DETECTOR_CATALOGUE` dengan pemetaan
      sumber S001/S002/S003/S004.
- [x] Notebook Colab bisa clone repo + install deps + jalankan smoke test.
- [x] Validator riset masih PASS (`VALIDATION PASSED`).
- [ ] **Smoke test dieksekusi di Colab** (bukan oleh agent — oleh user).
- [ ] Hasil run di-commit ke `experiments/s1_detector_smoke/` (CSV, JSON, MP4).
- [ ] Reviewer pass menulis `docs/reviews/review-s1-smoke.md`.

## Out of scope Tier 1

- Training detector baru.
- Integrasi tracker (OC-SORT, DiffMOT) → Tier 2.
- Counting logic end-to-end → Tier 3.
- CrowdHuman / MOT20 / DanceTrack full eval → Tier 2/3.
- Diffusi MOT (S021) — butuh verifikasi implementasi publik dulu.

## Risiko

| Risiko | Mitigasi |
|---|---|
| URL video sample mati | Notebook auto-generate synthetic fallback |
| Pretrained `.pt` gagal di-download | Tergantung Ultralytics cache; retry |
| Colab T4 disconnect sebelum selesai | `max_frames` dibatasi 200; simpan CSV ke Drive |
| User menjalankan di VPS tanpa GPU | README eksperimen tegaskan "di Colab, bukan VPS" |
| Klaim overclaim angka FPS ke dosen | Hard rule: hanya fps_avg, p50, p95 dari run aktual |
