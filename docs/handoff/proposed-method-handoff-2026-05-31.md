# Handoff Diskusi — Proposed Method

**Tanggal:** 31 Mei 2026  
**Status:** `READY_FOR_DISCUSSION` berdasarkan `docs/reviews/review-usulan-pendekatan.md`.

## File yang dibuka saat diskusi

1. `docs/drafts/usulan-pendekatan.md` — draft utama Proposed Method.
2. `docs/outlines/usulan-pendekatan-outline.md` — outline kerja dan anti-overclaim rules.
3. `docs/plans/2026-05-31-phase6-proposed-method.md` — pre-plan fase Proposed Method.
4. `docs/diagrams/proposed-method-architecture.mmd` — diagram arsitektur sistem.
5. `docs/reviews/review-usulan-pendekatan.md` — hasil review; verdict `READY_FOR_DISCUSSION`.

6. `docs/diagrams/proposed-method-architecture-gpt-image-2.png` — diagram visual hasil image generation untuk bahan presentasi/diskusi.

## Inti yang perlu disampaikan ke dosen

Bagian Proposed Method belum mengklaim eksperimen. Isinya adalah rancangan metodologi dan arsitektur sistem untuk *real-time people counting* berbasis pipeline **detection-tracking-counting**.

Alur yang diusulkan:

1. Input video CCTV/rekaman ruang publik.
2. Preprocessing: frame sampling, resize, timestamp, anotasi RoI/line/zone.
3. Detector manusia: YOLO26 sebagai kandidat implementasi; YOLOv10/RT-DETR sebagai anchor/baseline akademik untuk arah NMS-free/end-to-end.
4. Tracker: DiffMOT sebagai jalur robust untuk gerak non-linear; OC-SORT/SORT-family sebagai fallback efisien.
5. Counting logic: RoI polygon, line/zone crossing, trajectory validation, ID state memory, cooldown/debouncing, dan reactivation handling.
6. Output: hitungan masuk/keluar/per zona, log event per ID, overlay visual, FPS/latency, dan error analysis.

## Batasan aman

- Belum ada training/inference eksperimen aktual.
- Belum ada klaim bahwa YOLO26/DiffMOT/OC-SORT sudah unggul pada data target.
- Dataset publik diposisikan sesuai fungsi:
  - CrowdHuman: deteksi manusia pada crowd.
  - MOT20/DanceTrack: tracking dan asosiasi ID.
  - Data target/lokal: counting berbasis RoI/line/zone.
- DeepStream/NVIDIA `[S035]` hanya referensi teknis RoI/line analytics, bukan bukti SOTA akademik.

## Pertanyaan diskusi untuk dosen

1. Apakah struktur Proposed Method sudah cukup sesuai arahan paper: arsitektur → data/preprocessing → tahapan → skenario eksperimen → evaluasi?
2. Apakah YOLO26 tetap diposisikan sebagai kandidat implementasi utama, atau sebaiknya ditulis sebagai salah satu kandidat bersama YOLOv10/RT-DETR?
3. Apakah DiffMOT perlu dipertahankan sebagai tracker utama, atau dibuat dua jalur sejajar dengan OC-SORT sejak awal?
4. Untuk data target, apakah boleh memakai rekaman kampus/ruang publik internal, atau sebaiknya mulai dari dataset/video publik dulu?
5. Apakah dosen ingin ada pseudocode counting logic pada draft berikutnya?
6. Apakah diagram arsitektur saat ini sudah cukup, atau perlu dibuat versi gambar final untuk paper?

## Next action setelah diskusi

- Jika dosen setuju struktur: rapikan menjadi versi paper-ready dan konversi diagram ke gambar final.
- Jika dosen minta detail teknis: tambahkan pseudocode counting logic dan tabel konfigurasi skenario eksperimen.
- Jika dosen minta fokus data: buat protokol anotasi RoI/line/zone dan template ground truth counting.
- Jika dosen minta mulai prototype: baru masuk fase eksperimen/integrasi kode secara bertahap.
