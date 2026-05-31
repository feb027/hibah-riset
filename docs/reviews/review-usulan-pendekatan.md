# Review — Draft USULAN PENDEKATAN

**Artifact:** `docs/drafts/usulan-pendekatan.md`  
**Panduan reviewer:** `prompts/reviewer-usulan-pendekatan.md`  
**Tanggal review:** 31 May 2026 WIB

## Ringkasan keputusan

Draft `USULAN PENDEKATAN` sudah layak dibawa ke diskusi. Isi bagian ini konsisten dengan instruksi dosen terbaru: belum menyajikan eksperimen aktual, melainkan rencana metodologi, arsitektur sistem, skenario eksperimen, metrik evaluasi, dan ancaman validitas. Tidak ditemukan klaim hasil palsu atau klaim performa baru yang seolah-olah sudah diuji.

Secara substansi, draft sudah menghubungkan gap dari `PENDAHULUAN` dan `PEKERJAAN TERKAIT` ke rancangan pipeline *detection-tracking-counting*: YOLO26 sebagai kandidat implementasi yang diperlakukan hati-hati, YOLOv10/RT-DETR sebagai anchor akademik untuk detector NMS-free/end-to-end, DiffMOT sebagai tracker utama, OC-SORT/SORT-family sebagai baseline/fallback, serta *counting logic* berbasis RoI, garis/zona, memori status ID, dan *debouncing*.

## Hasil pemeriksaan terhadap kriteria

| Kriteria | Status | Catatan |
|---|---|---|
| Alignment dengan `F-Paper Penelitian.pdf` bagian Proposed Method | Lulus | Draft memuat arsitektur sistem, data/preprocessing, tahapan pengembangan/eksperimen, skenario eksperimen, metrik evaluasi, dan ancaman validitas. Bagian diskusi hasil aktual memang belum ada, tetapi ini sesuai instruksi fase saat ini bahwa eksperimen belum dilakukan. |
| Alignment dengan instruksi dosen terbaru | Lulus | Baris/paragraf awal menegaskan bahwa belum ada eksperimen aktual dan seluruh isi adalah rencana. Bahasa “direncanakan”, “akan”, dan “rancangan” konsisten digunakan. |
| Konsistensi dengan `PENDAHULUAN` dan `PEKERJAAN TERKAIT` | Lulus | Gap integrasi detector real-time, robust MOT, fallback efisien, dan counting logic berbasis zona diteruskan dengan koheren ke metodologi. Peran CrowdHuman, MOT20, DanceTrack, dan validasi domain target juga selaras dengan bagian sebelumnya. |
| Tidak ada klaim hasil palsu | Lulus | Tidak ada tabel hasil, angka performa model usulan, atau kesimpulan empiris yang diklaim sudah diperoleh. Statistik dataset dipakai sebagai konteks rencana data, bukan sebagai hasil penelitian. |
| Arsitektur eksplisit | Lulus | Input, preprocessing, detector, tracker, counting logic, output/logging, dan evaluasi dijelaskan jelas serta diperkuat diagram alir Mermaid. |
| Metodologi executable | Lulus | Tahapan metodologi cukup operasional: definisi scene/RoI/zone, persiapan data/anotasi, integrasi detector, integrasi tracker, counting logic, logging/evaluasi, dan analisis error. Draft tidak terlalu abstrak. |
| Skenario eksperimen jelas dan terukur | Lulus | Skenario A–E memiliki tujuan, rancangan evaluasi, dan keluaran yang direncanakan. Skenario mencakup detector, tracker, counting logic, real-time readiness, dan validasi domain target. |
| Metrik lengkap | Lulus | Mencakup AP/mAP, precision/recall, FP/FN, latency detector; HOTA, IDF1, MOTA, ID switch, fragmentasi; MAE/MAPE, over-count, under-count, direction accuracy; FPS, latency end-to-end/p95, CPU/GPU/memori, dan metrik edge tambahan bila tersedia. |
| Threats to validity | Lulus | Sudah mencakup validitas internal, konstruk, kesimpulan, eksternal, implementasi/reproduksibilitas, serta etika/privasi. Mitigasinya relevan dan tidak berlebihan. |
| Keamanan penggunaan source ID | Lulus | Source ID digunakan sesuai peran: YOLO26 `[S001]`, `[S002]` tetap diposisikan sebagai preprint/vendor; DeepStream `[S035]` sebagai referensi teknis; dataset/metrik lama dipakai sebagai benchmark/metrik, bukan novelty. |
| Citation integrity teknis | Lulus | Pemeriksaan otomatis menemukan 24 source ID pada draft; semuanya tersedia di `docs/research/source-ledger.md` dan `references/references.bib`. `python3 scripts/validate_research_artifacts.py` juga lulus. |
| Nada akademik Indonesia dan anti-AI wording | Lulus | Bahasa akademik-natural, tidak berupa template generik. Struktur panjang tetapi masih fungsional untuk bagian metode. |

## Catatan minor non-blocking

1. **Panjang bagian metode cukup besar.** Untuk versi final paper, beberapa detail operasional dapat dipadatkan bila ada batas halaman. Namun untuk draft diskusi, kelengkapan ini justru membantu dosen mengevaluasi rancangan.
2. **Diagram sudah membantu, tetapi versi final sebaiknya dicek render-nya.** Mermaid sudah jelas di Markdown; jika akan dipindahkan ke format paper, perlu dibuat gambar/diagram final yang terbaca.
3. **Algoritma counting logic dapat ditambahkan pada tahap patch berikutnya jika diminta dosen.** Saat ini aturan state memory dan debouncing sudah dijelaskan naratif; pseudocode akan memperkuat replikasi, tetapi belum menjadi blocker.
4. **Skenario E bergantung pada izin/data target.** Draft sudah menulis mitigasi dan pembatasan klaim dengan benar; pada tahap eksperimen nanti perlu memastikan protokol data/privasi benar-benar tersedia.

## Kesimpulan review

Tidak ada blocker yang mengharuskan patch sebelum diskusi. Draft sudah memenuhi fungsi bagian `USULAN PENDEKATAN` untuk fase pra-eksperimen: arsitektur eksplisit, metodologi dapat dieksekusi, evaluasi terukur, tidak mengklaim hasil yang belum ada, dan konsisten dengan konteks riset sebelumnya.

VERDICT: READY_FOR_DISCUSSION
