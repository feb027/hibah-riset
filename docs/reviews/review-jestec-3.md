LAYAK DENGAN REVISI MINOR

Review Bab 3 Method (docs/journal/3-method.md) — reviewer: Hermes (subagent aktar hibah-riset), 10 Sep 2026.
Basis verifikasi: docs/drafts/usulan-pendekatan.md, docs/drafts/bab3_revisi_skenario_eksperimen.md, kode (src/detector.py, src/pipeline.py, core/counting/counter.py, core/counting/models.py, core/counting/detector.py, src/deepocsort/tracker.py, scripts/s3/eval_counting.py, scripts/s2/run_*_mot.py, experiments/s3_counting/*.csv, experiments/s4_realtime/*.csv), docs/journal/4.1–4.6, references/references.bib, docs/reports/laporan-skenario-a-finetuning-yolo.md.

Baca file ini di GitHub (rendered), bukan editor mentah.

═══════════════════════════════════════════
A. FAKTUALITAS vs SUMBER & KODE
═══════════════════════════════════════════

A1. [WAJIB] Rata-rata orang per citra CrowdHuman tidak konsisten dengan angka pada kalimat yang sama.
  Lokasi: 3.4, par. 1 — "…4.370 citra validasi dengan 103.115 kotak anotasi *full-body* (rata-rata 22,8 orang per citra)".
  Fakta: 103.115 / 4.370 = 23,6 (bukan 22,8). Angka 22,8 hanya cocok bila dibagi target pasca-ignore 99.481 (99.481/4.370 = 22,8) — basis yang berbeda dari yang dikutip. Angka level dataset di makalah CrowdHuman (dan di usulan-pendekatan.md §Rencana Data) adalah 22,6. Jangan biarkan dua angka bertentangan dalam satu kalimat.
  Fix: cari `(rata-rata 22,8 orang per citra)` → ganti `(rata-rata 23,6 kotak per citra pada split validasi)` — atau kutip 22,6 sebagai angka dataset-level dengan menyebut basisnya. Pilih satu, jangan campur.

A2. Arsitektur lima lapis — TERVERIFIKASI. Urutan dan penamaan identik dengan usulan-pendekatan.md §Arsitektur Sistem (input+preprocessing → deteksi → tracking → counting logic → output+logging) dan dengan alur pipeline di kode (src/pipeline.py → PeopleDetector → DeepOCSortTracker → PeopleCounter).

A3. Dataset + split + jumlah frame — TERVERIFIKASI.
  - MOT20-train 4 sekuens / 8.931 frame: konsisten dengan 4.2 dan konvensi MOTChallenge (total benchmark 8 sekuens menurut usulan; Bab 3 benar memakai split train ber-GT).
  - DanceTrack-val 25 sekuens / 25.508 frame: konsisten dengan 4.2.
  - CrowdHuman 15.000 train / 4.370 val: konsisten dengan 4.1 dan laporan skenario A (kecuali A1 di atas).

A4. Konfigurasi pelatihan — TERVERIFIKASI. "100 epoch, batch size 32, resolusi 640×640, satu kelas, optimizer bawaan, satu seed" cocok dengan tabel konfigurasi laporan-skenario-a (Epoch 100, Batch 32, 640×640, Seed 0, Kelas 1, optimizer `auto`) dan notebooks training (epochs=100).

A5. Konvensi format MOT — TERVERIFIKASI. "indeks frame, ID, kotak pembatas, confidence" sesuai output scripts/s2/run_*_mot.py: "format TrackEval: frame,id,x,y,w,h,conf".

A6. State machine — TERVERIFIKASI. Deskripsi 3.3 (status per ID, debounce cooldown, lintasan harus memotong garis antar frame berurutan, hitungan masuk/keluar) sesuai core/counting/counter.py (`TrackState`, `cooldown_threshold=30`, `LineCrossDetector.check_crossing`, `count_in/count_out`) dan core/counting/models.py. Ground truth hitung dari counter pada lintasan GT terkonfirmasi di scripts/s3/eval_counting.py (baris "Ground truth track" Tabel 6).

A7. Metrik per lapisan — TERVERIFIKASI. mAP + MR⁻² protokol resmi CrowdHuman (4.1 ✓); HOTA/IDF1/MOTA/IDSW/Frag via TrackEval 1.3.0 (4.2 ✓, penulisan skrip output format TrackEval ✓); MAE/galat/RMSE interval + over/under-count (4.3–4.4 ✓, kolom CSV counting_metrics.csv ✓); P90/P95/P99 + pemanasan (warmup) terukur (4.5 ✓, kolom p90/p95/p99 di experiments/s4_realtime/latency_distribution_*.csv ✓, flag --warmup di scripts/experiments ✓); perangkat GPU RTX 4090 + CPU + ONNX Runtime ✓ (Tabel 4, Tabel 11).

═══════════════════════════════════════════
B. CITATION INTEGRITY
═══════════════════════════════════════════

Tidak ditemukan masalah. Ke-12 kode sitasi ada di references/references.bib dengan atribusi benar:
  S002 Ultralytics YOLO26 docs (2026) ✓ · S003 Wang et al. 2024 YOLOv10 ✓ · S004 Zhao et al. 2024 RT-DETR ✓ · S021 Lv et al. 2024 DiffMOT ✓ · S024 Cao et al. 2023 OC-SORT ✓ · S049 Maggiolino et al. 2024 Deep-OC-SORT ✓ · S038 Shao et al. 2018 CrowdHuman ✓ · S036 Dendorfer et al. 2020 MOT20 ✓ · S037 Sun et al. 2022 DanceTrack ✓ · S025 Luiten et al. 2021 HOTA ✓ · S026 Ristani et al. 2016 IDF1 ✓ · S048 Dollár et al. 2012 MR⁻² ✓.
Pemisahan peran S002 (vendor, kandidat implementasi) vs S003/S004 (peer-reviewed, jangkar akademik NMS-free) di 3.2 sudah jujur dan sesuai source-ledger.

═══════════════════════════════════════════
C. OVERCLAIM
═══════════════════════════════════════════

C1. [WAJIB] "Zona" diklaim sebagai komponen sistem padahal tidak diimplementasikan dan tidak dievaluasi.
  Lokasi: 3.1 — "zona yang didefinisikan eksplisit pada koordinat *frame*" dan "mencatat hitungan masuk-keluar per zona".
  Fakta: implementasi hanya RoI poligon + garis hitung (core/counting: `Line`, `Polygon`, `LineCrossDetector`, `PolygonDetector`); tidak ada transisi zona di kode, dan Bab 4 tidak mengevaluasi hitungan per zona. Usulan memang merencanakan zona, tapi jurnal ini tidak mewujudkannya — Bab 3 tidak boleh mengklaimnya.
  Fix: cari `serta zona yang didefinisikan eksplisit pada koordinat *frame*` → `serta *region of interest* poligon pada koordinat *frame*` (RoI sudah disebut sebelumnya, jadi cukup hapus "zona"); cari `hitungan masuk-keluar per zona` → `hitungan masuk-keluar`.

C2. Angka performa tidak menyelundup ke Bab 3 — BERSIH. 3.3 merujuk studi sensitivitas subbab 4.4 tanpa memunculkan satu pun angka hasil; satu-satunya angka di Bab 3 adalah statistik dataset (sah). Framing YOLO26 sebagai "kandidat implementasi, bukan jangkar kebaruan" sudah defensif dengan benar.

C3. [SARAN] 3.3 — "kemunculan kembali tidak langsung dihitung sebagai orang baru bila lintasannya masih ambigu": mekanisme ini hidup di lapisan tracker (max_age=30, asosiasi ulang OCR round-2 di src/deepocsort/tracker.py), bukan di counter (counter hanya mencegat ID yang sama via cooldown). Satu klausa penjelas bahwa retensi identitas saat oklusi dikerjakan lapisan tracking menghindari kesan mekanisme tunggal di counter.

═══════════════════════════════════════════
D. KONSISTENSI DENGAN BAB 4
═══════════════════════════════════════════

D1. [WAJIB] Jumlah tracker meleset: 3.2 menyebut TIGA, 4.2/4.3 mengevaluasi EMPAT.
  Lokasi: 3.2 — "Tiga *tracker* dipbandingkan dengan keluaran deteksi yang identik".
  Fakta: 4.2 membandingkan OC-SORT, Deep-OC-SORT, DiffMOT, **plus reimplementasi LightTrack-ReID (Khan et al., 2026 – S014)**; LightTrack juga masuk Tabel 6 dan 7 di 4.3. Tracker keempat tidak pernah diperkenalkan di Bab 3.
  Fix: cari `Tiga *tracker* dipbandingkan dengan keluaran deteksi yang identik` → `Empat *tracker* dipbandingkan dengan keluaran deteksi yang identik`, lalu tambah satu klausa: `…dan reimplementasi LightTrack-ReID (Khan et al., 2026 – S014) sebagai pembanding eksplorasi ringan.` (urutan bebas; S014 sudah ada di references.bib).

D2. [WAJIB] Set detektor eksperimen tidak diintroduksi; 3.4 membaca seperti satu model.
  Lokasi: 3.4 — "Pelatihan deteksi memakai konfigurasi seragam: 100 *epoch*, …" dan 3.2 yang hanya menama-nama YOLO26.
  Fakta: 4.1 melakukan fine-tune dan membandingkan EMPAT detektor (YOLO26n, YOLO26s, YOLOv10n, YOLOv11n). Pembaca Bab 3 tidak tahu model mana yang dilatih; "konfigurasi seragam" jadi menggantung. RT-DETR di 3.2 berstatus jangkar akademik dan memang tidak dievaluasi — itu sah, asalkan set eksperimen disebut eksplisit.
  Fix: tambah satu kalimat di 3.4 sebelum kalimat konfigurasi, mis.: `Empat detektor di-*fine-tune* dengan konfigurasi identik: YOLO26n, YOLO26s, YOLOv10n, dan YOLOv11n, semua dari bobot awal pra-latih COCO.` — sesuaikan dengan kalimat "konfigurasi seragam" yang ada.

D3. [WAJIB] Analisis galat "ukuran objek" dijanjikan, tidak pernah dikirim.
  Lokasi: 3.4 — "tambahan pula analisis galat terstratifikasi menurut pemotongan bingkai, oklusi, dan ukuran objek".
  Fakta: 4.1 mengirim stratifikasi pemotongan bingkai (15,3% menembus tepi) dan oklusi (rasio biaya 1,86–2,50×), tapi tidak ada analisis per ukuran objek di Bab 4 mana pun.
  Fix (pilih satu): hapus `, dan ukuran objek` di 3.4 — ATAU tambahkan stratifikasi ukuran di 4.1. Termurah dan jujur: hapus.

D4. Arah sebaliknya (metrik di Bab 4 tanpa pengantar di Bab 3): HOTA/IDF1/MOTA/IDSW/Frag, mAP/MR⁻², MAE/galat/RMSE, over/under-count, FPS/latensi/P90-95-99 — semua diintroduksi 3.4 ✓. Dua metrik turunan muncul di Bab 4 tanpa nama di Bab 3: "Bias (prediksi − GT)" (Tabel 8) dan "Recall maksimum" (Tabel 2). Keduanya turunan langsung metrik yang sudah diintroduksi — [SARAN] tidak wajib; kalau mau rapat, tambah kata "bias" di daftar metrik hitung 3.4.

D5. Janji → pengiriman lintas subbab sudah beres: 3.2→3.4 (rincian pelatihan) ✓, 3.3→4.4 (studi sensitivitas cooldown + conf) ✓, 3.4→4.1/4.2 (protokol resmi, TrackEval) ✓, ground-truth counter → baris GT di Tabel 6 ✓. Konfigurasi operasional CD=30/conf=0,30 di 4.4–4.5 konsisten dengan 3.3 yang menyerahkan penetapan nilainya ke studi sensitivitas.

═══════════════════════════════════════════
E. GAYA BAHASA
═══════════════════════════════════════════

E1. [WAJIB] Typo prefiks: "dipbandingkan".
  Lokasi: 3.2 — "Tiga *tracker* dipbandingkan dengan keluaran deteksi yang identik".
  Fix: cari `dipbandingkan` → `dibandingkan`.

E2. [SARAN] Frasa ambigu: "pemisahan arah *over-count* dan *under-count*" (3.4) — "arah" bisa terbaca sebagai direction (masuk/keluar) atau sebagai penjelas over/under. Usulan memisahkan direction accuracy DARI over/under-count. Rapikan menjadi: `pemisahan *over-count* dan *under-count*` (direction memang tidak diukur di Bab 4).

E3. [SARAN] Repetisi pola "bersifat X" tiga kali dalam dua subbab: "bersifat sengaja" (3.1), "bersifat replaceable" (3.1), "bersifat praktis" (3.2). Satu-duanya cukup diganti kata kerja biasa (mis. "Pemisahan lima lapis ini disengaja", "tracker dapat ditukar").

E4. [SARAN] "pelaporan persentil dengan pemanasan terukur" (3.4) — "pemanasan terukur" tidak idiomatik; maksudnya warmup terdokumentasi sebelum pengukuran. Ganti: `pelaporan persentil setelah *warmup* terdokumentasi`.

E5. Di luar itu BAGUS: kalimat spesifik, hedging jujur ("menyebut", "kandidat implementasi"), tidak ada tricolon dekoratif, tidak ada kalimat penutup rangkuman berulang, transisi antarparagraf fungsional. Nada anti-AI aman.

═══════════════════════════════════════════
F. KELAYAKAN JURNAL
═══════════════════════════════════════════

F1. [SARAN] Bab 3 tidak punya satu pun gambar/tabel. Untuk standar JESTEC, method section lazimnya menyertakan (a) diagram arsitektur pipeline (versi final dari diagram mermaid di usulan-pendekatan.md) dan (b) tabel parameter (tracker: det_thresh 0,30, max_age 30, min_hits 3; counter: cooldown 30; detektor: conf 0,30 — nilai operasional baru muncul di 4.4–4.5). Nilai tracker parameters (min_hits/max_age/det_thresh) tidak tertulis di Bab 3 maupun Bab 4 — ini gap reproduksi paling nyata.

F2. Struktur subbab 3.1–3.4 sesuai template JESTEC ✓, alur logis arsitektur→komponen→dataset/metrik ✓, level detail definisi metrik dengan sitasi kanonik ✓.

═══════════════════════════════════════════
PERBAIKAN WAJIB (urut nomor, semua cari → ganti)
═══════════════════════════════════════════

1. [A1 — fakta] 3.4: `rata-rata 22,8 orang per citra` → `rata-rata 23,6 kotak per citra pada split validasi` (atau kutip 22,6 dengan basis dataset-level; pilih satu basis).
2. [C1 — overclaim] 3.1: hapus klaim "zona": `serta zona yang didefinisikan eksplisit pada koordinat *frame*` → `serta *region of interest* poligon pada koordinat *frame*`; `hitungan masuk-keluar per zona` → `hitungan masuk-keluar`.
3. [D1 — konsistensi] 3.2: `Tiga *tracker* dipbandingkan` → `Empat *tracker* dibandingkan` + tambah klausa pengantar LightTrack-ReID (S014) sebagai pembanding eksplorasi.
4. [D2 — konsistensi] 3.4: tambah satu kalimat yang menama-kan empat detektor yang di-fine-tune (YOLO26n, YOLO26s, YOLOv10n, YOLOv11n) sebelum "konfigurasi seragam".
5. [D3 — konsistensi] 3.4: hapus `, dan ukuran objek` dari daftar stratifikasi galat (atau tambahkan analisisnya di 4.1).
6. [E1 — typo] 3.2: `dipbandingkan` → `dibandingkan` (tercakup juga di butir 3).

═══════════════════════════════════════════
SARAN (opsional, tidak memblokir)
═══════════════════════════════════════════

1. [C3] 3.3: satu klausa bahwa retensi identitas saat oklusi dikerjakan lapisan tracking (max_age + re-associasi), bukan counter.
2. [E2] 3.4: `pemisahan arah *over-count* dan *under-count*` → `pemisahan *over-count* dan *under-count*`.
3. [E3] Kurangi repetisi "bersifat X" (3×).
4. [E4] 3.4: `dengan pemanasan terukur` → `setelah *warmup* terdokumentasi`.
5. [F1] Tambahkan diagram arsitektur + tabel parameter (termasuk parameter tracker yang sampai hari ini tidak tertulis di Bab 3/4).
6. [D4] Opsional: sebut "bias" di daftar metrik hitung 3.4 agar Tabel 8 punya pengantar.
