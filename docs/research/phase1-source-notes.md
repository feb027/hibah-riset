# Phase 1 Source Notes — Indexed/Credible Source Strategy

Tanggal kerja: 25 Mei 2026 WIB.

## Prinsip pemilihan sumber

Karena user meminta “kalau bisa yang terindeks”, strategi sumber untuk draft adalah:

1. **Utama:** peer-reviewed proceedings/journals dari IEEE/CVF, NeurIPS, ICLR, AAAI, Springer, Elsevier, Nature Portfolio, Wiley/IET, PLOS, dan jurnal peer-reviewed lain.
2. **Pendukung teknis:** arXiv hanya jika paper baru belum punya versi proceeding/jurnal atau sebagai akses PDF dari paper yang sudah accepted.
3. **Vendor docs:** hanya untuk implementasi/feasibility, misalnya Ultralytics YOLO26 dan NVIDIA DeepStream; tidak dipakai sebagai bukti akademik utama.
4. **Benchmark/dataset/metric klasik:** boleh lebih tua dari 2024 bila memang standar komunitas, misalnya MOT20, DanceTrack, CrowdHuman, HOTA, IDF1.

## Hasil awal

- Total sumber di ledger: 38.
- Sumber utama/peer-reviewed 2024–2026: mayoritas sudah memenuhi target awal.
- Sumber yang perlu hati-hati: YOLO26 karena saat ini anchor utamanya vendor + arXiv/preprint; novelty akademik perlu ditopang oleh YOLOv10, RT-DETR, D-FINE, DEIM, RF-DETR.

## Rekomendasi untuk PEKERJAAN TERKAIT

Urutan penulisan yang paling aman:

1. Mulai dari domain people/crowd counting dan tantangan dunia nyata.
2. Bedakan density-map counting vs detection-tracking-counting.
3. Bahas real-time detector dan NMS-free trend.
4. Bahas MOT dense crowd/occlusion dan identitas.
5. Bahas counting logic berbasis RoI/line/zone/ID memory.
6. Tutup dengan gap integrasi pipeline dan validasi real-time.
