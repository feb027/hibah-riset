# Models

Folder ini **tidak di-track git** (lihat `.gitignore`). Semua bobot model
pretrained di-download otomatis oleh Ultralytics saat pertama kali
dipanggil via `YOLO("yolov10s.pt")` dst.

## Tier 1 — Detector pretrained (otomatis)

| Alias       | File          | Sumber / paper         |
|-------------|---------------|------------------------|
| yolov10n    | yolov10n.pt   | S003 - NeurIPS 2024    |
| yolov10s    | yolov10s.pt   | S003 - NeurIPS 2024    |
| yolov11n    | yolo11n.pt    | Ultralytics 2024 (no S-code) |
| yolo26n     | yolo26n.pt    | S001/S002 - caution    |
| rtdetr-l    | rtdetr-l.pt   | S004 - CVPR 2024       |

Lokasi default unduhan: `~/.config/Ultralytics/` atau `models/weights/`
jika di-set via `YOLO.set_dir(...)`.

## Tier 2 (berikutnya) — Tracker

- **OC-SORT** (S024): https://github.com/noahcao/OC_SORT
  - Implementasi reference. Untuk integrasi via Ultralytics tracker,
    lihat `tracker=oc-sort` di YOLO.predict().
- **BoxMOT** (komunitas): https://github.com/mikel-brostrom/boxmot
  - Banyak tracker (OC-SORT, BoT-SORT, ByteTrack) dalam satu package.
  - License: AGPL — perhatikan implikasi distribusi.

## Tier 3 (jangka panjang) — DiffMOT

- (S021) Diffusion-based tracker. Implementasi publik perlu diverifikasi
  per tanggal akses. **Jangan** klaim DiffMOT jalan sebelum kode & checkpoint
  ada di lokal.

## Larangan

- **Jangan commit** file `.pt`, `.onnx`, `.engine` ke repo.
- **Jangan klaim akurasi SOTA** hanya berdasarkan pretrained COCO.
- **Jangan pakai model tanpa entry di source-ledger.md**.
