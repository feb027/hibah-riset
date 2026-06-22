# S1 — Detector Smoke Test (Tier 1)

Status: **draft code** (akan menjadi `smoke_passed` setelah run pertama di Colab).

## Tujuan

Membuktikan pipeline deteksi orang bisa dijalankan end-to-end pada GPU Colab
sebelum masuk ke evaluasi kuantitatif S1 (CrowdHuman), S2 (MOT20/DanceTrack),
S3 (counting logic), S4 (end-to-end) sesuai `docs/revisions/progress-selasa-arsitektur-data-tahapan-copy-to-word.md`.

## Sumber sitasi

| Kode | Peran | Status |
|---|---|---|
| S001 | YOLO26 (kandidat) | caution — preprint |
| S002 | Ultralytics YOLO26 docs | caution — vendor |
| S003 | YOLOv10 (anchor) | A-main — NeurIPS 2024 |
| S004 | RT-DETR (alternatif) | A-main — CVPR 2024 |

Lihat `src/detector.py::DETECTOR_CATALOGUE` untuk daftar lengkap + pemetaan
sumber. Jangan klaim kontribusi baru untuk detector — yang dievaluasi adalah
**kematangan pipeline**, bukan model.

## Cara menjalankan (di Colab, BUKAN di VPS / lokal)

1. Buka `notebooks/01_smoke_test_detector.ipynb` di Google Colab.
2. Runtime → Change runtime type → **T4 GPU**.
3. Jalankan semua cell secara berurutan.
4. Hasil tersimpan di `OUTPUT_ROOT` (default `/content/hibah-riset-smoke`).

Jika ingin simpan permanen ke Drive, uncomment cell mounting Drive di langkah 0.

## Cara menjalankan via CLI (jika sudah punya model + video lokal)

> **Tidak disarankan** di laptop tanpa GPU. Pakai Colab.

```bash
python -m pip install -r requirements.txt
python scripts/smoke_test_detector.py \
    --video path/to/crowd.mp4 \
    --out experiments/s1_detector_smoke \
    --detector yolov10s \
    --max-frames 200 \
    --device cuda:0
```

## Yang TIDAK boleh dilakukan

- Training / fine-tuning model (bukan Tier 1).
- Klaim `mAP`, `HOTA`, atau angka SOTA lainnya (butuh labelled eval set).
- Klaim "real-time" tanpa mengukur latency di hardware target.
- Klaim "YOLO26 paling baru / paling bagus" — di paper kita pegang S001/S002
  sebagai kandidat implementasi, bukan bukti SOTA akademik.
- Menjalankan di VPS tanpa GPU — tidak akan selesai tepat waktu.

## Hasil yang diharapkan

| Artefak | Format | Catatan |
|---|---|---|
| `annotated_<detector>.mp4` | video | BBox + label "person 0.87" + overlay count |
| `per_frame_<detector>.csv` | CSV | frame_index, person_count, latency_ms, fps_instant |
| `summary_<detector>.json` | JSON | FPS avg, latency p50/p95, mean person count |
| `diagnostic_<detector>.png` | PNG | Plot count + latency per frame |

## Setelah lulus

1. Salin `outputs/` ke `experiments/s1_detector_smoke/` di repo lokal.
2. Update `docs/PROGRESS.md` dengan ringkasan run (tanggal, detector, FPS).
3. Commit + push.
4. Ajukan ke reviewer (strict mode → `docs/reviews/review-s1-smoke.md`).

Lihat eksperimen card lengkap di `docs/experiments/s1-detector-smoke-test.md`.
