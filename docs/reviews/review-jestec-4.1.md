LAYAK

Reviewer: prompt reviewer 4.1 (JESTEC)
Draft: docs/journal/4.1-object-detection-results.md
Sumber: docs/reports/laporan-skenario-a-finetuning-yolo.md
Tanggal: 2026-09-09

Metode: kedua file dibaca penuh termasuk seluruh sel tabel; setiap angka dicocokkan ke bagian sumbernya; 7 kode S### dicek ke references.bib (baris 216/226/260/280/292/302/354) dan source-ledger.

Hasil fact-check: SEMUA klaim kuantitatif TERVERIFIKASI ke laporan sumber; tidak ada UNVERIFIED/phantom. Rincian per kategori di bawah.

## 1. FACTUALITY — tidak ditemukan masalah

Semua angka, persentase, dan klaim identik dengan sumber. Yang sudah dicocokkan sel per sel:

- Tabel 1 (draft baris 13–18) ↔ laporan Bag. 4.1: YOLO26n 0,8230/0,6888/0,7814/0,4497; YOLO26s 0,8480/0,7455/0,8266/0,4974; YOLOv10n 0,8212/0,6892/0,7826/0,4521; YOLOv11n 0,8352/0,6965/0,7855/0,4463 — semua cocok, termasuk kolom NMS-free dan pemboldan YOLO26s.
- Tabel 2 (baris 24–31) ↔ laporan Bag. 6.1: MR⁻² 0,7792/0,7574/0,7764/0,7778; AP@0.5 0,7881/0,8283/0,7898/0,7882; recall maks 0,9124/0,9262/0,9146/0,9000; keterangan "4.370 citra, 99.481 target" cocok.
- Tabel 3 (baris 41–48) ↔ laporan Bag. 7.1: inferensi p50 2,554/2,695/2,129/2,142; post-proc 0,164/0,170/0,167/0,491; porsi 6,0%/6,0%/7,3%/18,7% — cocok.
- Tabel 4 (baris 54–61) ↔ laporan Bag. 7.2: PyTorch CPU 22,48/54,50/25,13/22,98; ONNX total 10,28/23,15/12,13/14,05; percepatan 2,24×/2,38×/2,11×/1,73×; FPS 97/43/82/71 — cocok.
- Kalimat kunci: rentang nano 0,4463–0,4521 (Δ0,0058) ↔ Bag. 8.1; kenaikan 26n→26s 0,0477 dan recall +5,7 poin ↔ Bag. 8.2; koreksi protokol +0,0116–0,0140 ↔ Bag. 6.2; MR⁻² 0,757–0,779, baseline 0,50, 2,4–9,5 juta parameter ↔ Bag. 6.4; lantai under-count 7,4–10,0% ↔ ringkasan eksekutif no. 5; 15,3% terpotong tepi, recall −20–21 poin, AP −28–31 poin, rasio 1,86–2,50× ↔ Bag. 6.5.1; 2,9× dan pemisahan distribusi (p50 ber-NMS > 2× p95 NMS-free) ↔ Temuan 1; 199/167 deteksi biaya datar ↔ Temuan 2; 3,8× FLOPs hanya 5,5% lebih lambat ↔ Temuan 3; 27%/18%, 24% vs klaim vendor 43% ↔ Bag. 7.2/7.4; export ONNX 1,73–2,38×, selisih akurasi nol, >30 FPS ↔ Temuan 5–6 dan Bag. 10.1.

Catatan keterlacakan (bukan kesalahan draft): klaim "selisih akurasi antara model PyTorch dan ONNX terukur nol" bersandar pada Bag. 10.1 laporan (uji sudah dijalankan, artefak `experiments/crowdhuman_protocol_onnx.csv`). Batasan no. 4 di laporan yang sama masih bertulis "Akurasi model ONNX belum divalidasi" — teks lama yang sudah tergantikan oleh Bag. 10.1. Sebaiknya laporan sumber membersihkan batasan itu agar tidak membingungkan pemeriksa berikutnya; draft sudah mengikuti versi terbaru yang benar.

## 2. CITATION INTEGRITY — tidak ditemukan masalah

Ketujuh kode yang dikutip ada dan atribusinya benar:

- S038 Shao et al. 2018, CrowdHuman (draft baris 5) ↔ bib @article{S038}; dataset utama, sesuai.
- S048 Dollár et al. 2012, TPAMI (baris 22, sumber metrik MR⁻²) ↔ bib @article{S048}; atribusi metrik tepat.
- S043 Hoiem et al. 2012, ECCV (baris 35, stratifikasi galat truncated) ↔ bib @inproceedings{S043}; tepat.
- S039 Cai et al. 2019 ICLR (ProxylessNAS), S041 Lu et al. 2022 SIGMETRICS (latency monotonicity), S042 Lazarevich et al. 2023 ICCVW (YOLOBench) (baris 52) ↔ ketiganya ada di bib dengan venue/tahun cocok; konteks "peringkat latensi berubah lintas perangkat" sesuai isi sumber di Bag. 7.4.
- S002 Ultralytics 2026 (baris 52, klaim "CPU inference hingga 43% lebih cepat") ↔ bib @misc{S002}; klaim vendor dikutip akurat dan langsung disandingkan dengan hasil ukur sendiri (24%) — pemakaian yang benar untuk sumber C-caution.

Catatan minor: S039–S048 belum terdaftar di docs/research/source-ledger.md (ledger berhenti di S038; entri bib baris 253–257 menyebutnya "sumber tambahan Juli 2026"). Kondisi ini memenuhi syarat pemeriksaan (ada di bib), tapi ledger sebaiknya disinkronkan. Catatan verifikasi di akhir laporan sendiri meminta detail S039–S048 diverifikasi ulang sebelum submisi.

## 3. OVERCLAIM — tidak ditemukan masalah

Ketiga rambu dipatuhi persis:

- Kesetaraan tier nano: draft menulis "Rentang sebesar 0,0058, dengan satu kali pelatihan per model dan satu nilai *seed*, tidak dapat dibedakan dari variasi acak" (baris 9) — frasa yang diizinkan, lengkap dengan kondisi satu run/satu seed. Tidak ada klaim keunggulan arsitektur.
- Keunggulan NMS-free: "terukur pada latensi *post-processing*, bukan pada akurasi" (baris 39) — tepat; tidak melebar ke akurasi.
- Selisih inference GPU: "tidak ditafsirkan" (baris 50) — tepat, sesuai Temuan 3 laporan.
- Recall maksimum dipakai hanya untuk lantai under-count (baris 33), bukan sebagai keunggulan akurasi — sesuai peringatan Bag. 6.3 laporan. Klaim vendor YOLO26 dilaporkan sebagai klaim vendor yang diverifikasi arah+besarannya, bukan diadopsi (baris 52).

Satu nuansa (lihat Saran 1): kalimat "Perbandingan yang sah di GPU adalah YOLOv10n terhadap YOLOv11n" (baris 50) menyiratkan satu-satunya; laporan mencantumkan dua perbandingan yang sah (yang kedua: YOLO26n vs YOLOv11n pada post-processing, dengan catatan total end-to-end GPU tidak dapat disimpulkan). Tidak berlebihan, hanya menyempitkan.

## 4. GAYA BAHASA — 2 catatan minor, tidak ada pola tulisan AI

Tidak ditemukan frasa template ("penting untuk dicatat", "seiring berkembangnya"), tricolon berlebihan, transisi kaku berulang, atau pola penutup paragraf yang seragam. Istilah baku dipakai konsisten (*derau*, *galat*, *lantai under-count*).

1. Baris 22: "Nilai ini terasa tinggi dibandingkan baseline" — "terasa" terlalu kolokial untuk naskah jurnal.
2. Baris 20: "Setiap tambahan 1.000 orang pada citra, tingkat *small* menemukan sekitar 57 orang lebih banyak" — "setiap tambahan" mengisyaratkan pertumbuhan kerumunan; maksud sumbernya "per 1.000 orang yang ada".

## 5. KELAYAKAN JURNAL — layak; catatan bukan penghambat

- Alur logis: akurasi (dua protokol, lalu stratifikasi galat) → efisiensi (GPU → CPU/ONNX) → keputusan konfigurasi → serah ke 4.2. Rapi.
- Tabel informatif dan semuanya diperlukan; caption memuat konteks (epoch/resolusi, jumlah target, persentil).
- Konsistensi istilah baik: "lantai *under-count*", "*post-processing*", "*fine-tune*" dipakai konsisten; konvensi mAP@0.5 (eval Ultralytics, Tabel 1) vs AP@0.5 (protokol resmi, Tabel 2) mengikuti sumber.
- Referensi maju ke subbab 4.2, 4.3, 4.4 (baris 5, 33, 63) menunjuk subbab yang belum ada di docs/journal/ — wajar untuk penulisan bertahap, wajib dituntaskan saat subbab tersebut ditulis.
- Penomoran "Tabel 1–4" baru berlaku dalam cakupan subbab; naskah jurnal utuh akan menomori ulang semua tabel lintas bab.
- Kode "– S###" dalam sitasi (mis. "Shao et al., 2018 – S038") adalah penanda internal proyek; saat submisi harus dikonversi ke format sitasi JESTEC dan kodenya dihapus.

## PERBAIKAN WAJIB

Tidak ada.

## SARAN

1. Baris 50 — cari: "Perbandingan yang sah di GPU adalah YOLOv10n terhadap YOLOv11n" → ganti: "Salah satu perbandingan yang sah di GPU adalah YOLOv10n terhadap YOLOv11n" (laporan juga menyatakan YOLO26n vs YOLOv11n sah pada level post-processing).
2. Baris 22 — cari: "Nilai ini terasa tinggi" → ganti: "Nilai ini tergolong tinggi".
3. Baris 20 — cari: "Setiap tambahan 1.000 orang pada citra, tingkat *small* menemukan sekitar 57 orang lebih banyak" → ganti: "Untuk setiap 1.000 orang pada citra, tingkat *small* menemukan sekitar 57 orang lebih banyak".
4. Pertimbangkan satu kalimat pengantar bahwa AP@0.5 pada Tabel 2 adalah metrik yang sama dengan mAP@0.5 pada Tabel 1, hanya dinamai ulang mengikuti implementasi protokol resmi — pembaca jurnal akan bertanya.
5. Sinkronkan source-ledger dengan entri bib S039–S048 (tambahkan baris ledger), dan selesaikan catatan verifikasi laporan untuk detail venue sebelum submisi.
6. Saat submisi: konversi semua "– S###" ke gaya sitasi JESTEC; penomoran tabel akan digeser mengikuti naskah utuh.
