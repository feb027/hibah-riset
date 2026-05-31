# Phase 6 Pre-Plan — Usulan Pendekatan / Proposed Method

**Tanggal kerja:** 31 Mei 2026 UTC.  
**Konteks tugas dosen:** minggu ini/pekan depan fokus pada bagian **USULAN PENDEKATAN (PROPOSED METHOD)**. Belum masuk eksperimen aktual. Deliverable hanya berupa rencana metodologi, rencana arsitektur sistem, rencana skenario eksperimen, dan penjelasan detailnya.

## 1. Batasan scope

### In scope

1. Menurunkan gap dari `PENDAHULUAN` dan `PEKERJAAN TERKAIT` menjadi rancangan metode.
2. Menulis rancangan **arsitektur sistem** untuk pipeline real-time people counting.
3. Menjelaskan **tahapan metodologi** dari input video sampai output hitungan.
4. Menyusun **rencana data dan preprocessing** tanpa mengklaim eksperimen sudah dilakukan.
5. Menyusun **rencana skenario eksperimen/evaluasi** untuk tahap berikutnya.
6. Menentukan metrik yang akan digunakan: detection, tracking, counting, dan real-time performance.
7. Menulis ancaman validitas awal agar rancangan terlihat jujur dan siap didiskusikan dengan dosen.

### Out of scope sekarang

1. Tidak menjalankan training/inference eksperimen.
2. Tidak mengklaim hasil metrik baru.
3. Tidak membuat tabel hasil seolah-olah sudah ada.
4. Tidak menetapkan YOLO26 sebagai novelty akademik tunggal.
5. Tidak mengubah `PENDAHULUAN`/`PEKERJAAN TERKAIT` kecuali diperlukan sinkronisasi minor setelah review.

## 2. Acuan dari file dosen

Dari `docs/F-Paper Penelitian.pdf`, bagian **USULAN PENDEKATAN (PROPOSED METHOD)** meminta:

- bagian awal mendeskripsikan arsitektur sistem yang diusulkan;
- bagian selanjutnya menjelaskan penerapan/eksperimen, mencakup:
  - data eksperimen atau data penelitian, sumber data, statistik data, penggunaan data, dan preprocessing;
  - tahapan pengembangan atau eksperimen, tujuan, prosedur, narasi, algoritma, atau diagram alir;
  - diskusi hasil jika sudah ada;
- bagian akhir mendeskripsikan evaluasi sistem, cara mengukur kinerja, validasi/pengujian, dan ancaman validitas.

Karena instruksi dosen terbaru menyatakan **belum ke eksperimen**, maka bagian “diskusi hasil” diganti menjadi **rencana analisis hasil yang akan dilakukan** dan seluruh kalimat hasil ditulis sebagai rencana, bukan klaim temuan.

## 3. Rancangan struktur deliverable

Target file utama: `docs/drafts/usulan-pendekatan.md`.

Struktur:

1. **Gambaran umum pendekatan**
   - Ringkasan pipeline: video → preprocessing → detector → tracker → counting logic → dashboard/log evaluasi.
   - Posisi kontribusi: integrasi detector real-time, tracker robust, fallback ringan, dan counting logic berbasis RoI/zone/ID memory.

2. **Arsitektur sistem yang diusulkan**
   - Lapisan input dan preprocessing.
   - Lapisan deteksi manusia: YOLO26 sebagai kandidat implementasi, YOLOv10/RT-DETR sebagai anchor/baseline akademik bila eksperimen dilakukan.
   - Lapisan tracking: DiffMOT sebagai tracker utama; OC-SORT/SORT-family sebagai fallback efisien.
   - Lapisan counting: RoI polygon, line/zone crossing, trajectory validation, ID state memory, debouncing/cooldown, dan reactivation handling.
   - Lapisan keluaran: total masuk/keluar/per zona, log per ID, FPS/latency, dan error analysis.

3. **Rencana data dan preprocessing**
   - Dataset publik untuk komponen: CrowdHuman/deteksi, MOT20 & DanceTrack/tracking.
   - Data validasi target: rekaman ruang publik/kampus atau video CCTV publik yang sesuai etika/izin.
   - Preprocessing: resize, frame sampling, anonymization bila perlu, RoI annotation, line/zone annotation, dan ground truth counting manual.

4. **Tahapan metodologi**
   - Studi data dan definisi skenario.
   - Implementasi detector.
   - Integrasi tracker.
   - Perancangan counting logic.
   - Logging dan evaluasi.
   - Analisis error dan iterasi.

5. **Rencana skenario eksperimen**
   - Skenario A: evaluasi detector.
   - Skenario B: evaluasi tracker.
   - Skenario C: evaluasi counting logic dan ablation.
   - Skenario D: evaluasi real-time/edge readiness.
   - Skenario E: uji domain ruang publik/rekaman lokal.

6. **Rencana metrik evaluasi**
   - Detector: AP/mAP, precision/recall, latency detector.
   - Tracker: HOTA, IDF1, MOTA, ID switches, fragmentasi track.
   - Counting: MAE/MAPE/counting error, over-count, under-count, direction accuracy.
   - Real-time: FPS, end-to-end latency, CPU/GPU/memory utilization.

7. **Ancaman validitas dan mitigasi awal**
   - Internal, construct, conclusion, external validity.

## 4. Agent workflow

1. Writer membuat `docs/drafts/usulan-pendekatan.md` berdasarkan outline dan dokumen sebelumnya.
2. Reviewer menulis `docs/reviews/review-usulan-pendekatan.md` tanpa mengubah draft.
3. Patch langsung jika reviewer menemukan blocker.
4. Patch-review atau final verifier menulis `docs/reviews/review-usulan-pendekatan-final.md`.
5. Update validator agar draft proposed method wajib ada dan tidak mengandung klaim eksperimen palsu.
6. Commit + push.

## 5. Acceptance criteria

- [ ] `docs/drafts/usulan-pendekatan.md` ada dan membahas arsitektur, metodologi, rencana data, rencana skenario eksperimen, metrik, dan validitas.
- [ ] Tidak ada klaim hasil eksperimen aktual.
- [ ] Diagram arsitektur tersedia minimal sebagai Mermaid/Markdown.
- [ ] Review gate menyatakan `READY_FOR_DISCUSSION` atau `READY_FOR_PATCH` lalu dipatch sampai final.
- [ ] `scripts/validate_research_artifacts.py` pass.
- [ ] Commit dan push ke `main`.
