# Review Phase 4 — Draft PENDAHULUAN

**Artifact:** `docs/drafts/pendahuluan.md`  
**Tanggal review:** 25 Mei 2026 WIB  
**Verdict: READY_FOR_PATCH**

## Ringkasan keputusan

Draft `PENDAHULUAN` sudah jauh lebih tajam daripada pendahuluan proposal awal. Alurnya sudah mengikuti kebutuhan utama: urgensi ruang publik, masalah teknis video/CCTV, pemisahan jalur *density-map crowd counting* vs *detection-tracking-counting*, posisi detector real-time/NMS-free, MOT, gap integrasi, pertanyaan penelitian, tujuan, ruang lingkup evaluasi, dan kontribusi. Draft juga berhasil membersihkan artefak ekstraksi Word yang muncul pada proposal awal seperti `Formatted`, `Field Code Changed`, dan duplikasi sitasi.

Namun, draft belum saya nyatakan siap fase berikut tanpa patch karena ada dua isu finalisasi yang perlu dibereskan: (1) panjang isi sekitar **1065 kata** sehingga berisiko melewati batas **1000 kata** bila naskah ini dipakai untuk bagian Pendahuluan proposal PUU, dan (2) paragraf akhir memakai format *outline makalah*, sedangkan template proposal PUU meminta peta jalan/roadmap setidaknya 5 tahun. Jika target dokumen adalah artikel/paper, paragraf outline dapat dipertahankan; jika targetnya proposal PUU, paragraf itu harus diganti atau dipadatkan menjadi roadmap singkat.

## Hasil pemeriksaan wajib

| Aspek | Hasil review |
|---|---|
| Factuality | Lulus dengan catatan minor. Tidak ditemukan klaim hasil eksperimen internal atau angka performa yang tidak didukung. Klaim masih bersifat latar, gap, rancangan, dan rencana evaluasi. |
| Freshness per 25 Mei 2026 WIB | Lulus. Draft memanfaatkan sumber 2024–2026 untuk detector, MOT, people counting, edge, dan review crowd counting, serta tetap memakai sumber lama hanya untuk metrik/dataset kanonik. |
| Citation integrity | Lulus. Semua citation ID yang muncul di draft (`S001`–`S038` subset sebanyak 30 ID) tersedia di `references/references.bib`. `python3 scripts/validate_research_artifacts.py` juga menghasilkan `VALIDATION PASSED`. |
| Indonesian academic tone | Lulus. Bahasa akademik-natural, jauh lebih bersih daripada proposal awal, dan tidak terasa sebagai daftar paper mekanis. Beberapa istilah Inggris teknis masih wajar karena domain computer vision/MOT. |
| Anti-AI wording | Lulus. Tidak ada frasa bombastis seperti “secara absolut”, “mengeliminasi”, atau “terbukti unggul” yang sebelumnya berisiko overclaim. |
| Alignment to lecturer guide | Hampir lulus. Struktur pendahuluan sudah memenuhi konteks, masalah, gap, pertanyaan penelitian, tujuan/lingkup, dan kontribusi. Isu tersisa adalah batas 1000 kata dan kebutuhan roadmap bila mengikuti template proposal PUU. |
| YOLO26 caution | Lulus. YOLO26 diposisikan sebagai kandidat implementasi/vendor-preprint, bukan dasar akademik tunggal. Anchor akademik diarahkan ke YOLOv10/RT-DETR dan detector 2025–2026 lain. |
| Density-map vs tracking-counting separation | Lulus. Paragraf line 7 membedakan density-map crowd counting dari detection-tracking-counting secara eksplisit dan tidak memakai density-map sebagai bukti ID/arah lintasan. |
| Unsupported result claims | Lulus. Draft tidak mengklaim sistem usulan sudah mencapai akurasi, FPS, HOTA/IDF1, atau counting error tertentu. |
| Word extraction artifacts | Lulus. Tidak ditemukan `Formatted`, `Field Code Changed`, `{Formatting Citation}`, atau duplikasi sitasi numerik dari ekstraksi proposal. |

## Catatan berdasarkan lokasi draft

1. **Line 3–5 — urgensi dan masalah teknis:** sudah lebih kuat daripada proposal awal karena tidak hanya menyebut “penghitungan real-time”, tetapi menghubungkannya dengan arus, arah, oklusi, *missed detection*, *identity switch*, dan *double-counting*. Klaim ini sesuai dengan evidence matrix dan sumber `S010`, `S011`, `S018`, `S021`, `S024`, `S027`, `S036`, `S038`.
2. **Line 7 — pemisahan paradigma counting:** ini salah satu bagian terkuat. Draft tidak mencampuradukkan *density-map crowd counting* dengan trajectory/ID counting. Formulasi sudah aman: density-map kuat untuk estimasi total kerumunan, tetapi tidak selalu menyediakan identitas, arah lintasan, atau state memory.
3. **Line 9 — detector dan YOLO26:** wording sudah hati-hati. YOLO26 tidak dijual sebagai “terbukti paling unggul”; ia disebut kandidat implementasi berbasis dokumentasi/preprint, sedangkan argumen ilmiah NMS-free ditopang `S003`/`S004`. Ini memperbaiki overclaim pada proposal awal.
4. **Line 11–13 — MOT dan gap:** gap integrasi sudah masuk akal dan tidak menyatakan “belum ada sama sekali”. Draft menempatkan OC-SORT sebagai fallback efisien, bukan metode buruk, dan DiffMOT sebagai kandidat untuk gerak non-linear tanpa mengklaim menyelesaikan counting sendirian.
5. **Line 15 — pertanyaan penelitian:** tiga pertanyaan sudah relevan dan sinkron dengan gap. Pertanyaan evaluasi tidak dibuat sebagai RQ tersendiri, tetapi sudah muncul di ruang lingkup line 17; ini masih dapat diterima. Jika ingin lebih lengkap, patch dapat menambahkan frasa singkat pada RQ atau tujuan tentang evaluasi multi-metrik.
6. **Line 17 — tujuan dan ruang lingkup:** cukup jelas: YOLO26, DiffMOT, OC-SORT, RoI/zona/ID memory, dataset publik, validasi rekaman ruang publik, HOTA/IDF1, FPS/latency, dan counting error. Ini lebih realistis daripada proposal awal karena tidak menjanjikan performa absolut.
7. **Line 19 — kontribusi:** kontribusi dirumuskan sebagai rancangan integratif, bukan klaim hasil. Ini aman untuk tahap pendahuluan.
8. **Line 21 — alur makalah:** cocok untuk format artikel ilmiah, tetapi kurang cocok bila draft ini akan menggantikan bagian Pendahuluan proposal PUU yang secara eksplisit meminta roadmap 5 tahun. Ini perlu keputusan target dokumen.

## Blocker patch sebelum dinyatakan siap

1. **Panjang melebihi batas proposal.**  
   - Lokasi: seluruh `docs/drafts/pendahuluan.md`.  
   - Hasil hitung kasar setelah menghapus heading dan citation ID: sekitar **1065 kata**. Template proposal pada `docs/_extracted/proposal_puu_2026_counting.md` line 68–72 menyatakan Pendahuluan tidak lebih dari 1000 kata.  
   - Patch yang disarankan: pangkas sekitar 80–120 kata, terutama dari paragraf detector/tracker yang agak padat atau dari paragraf kontribusi/outline.

2. **Paragraf akhir belum selaras jika targetnya proposal PUU.**  
   - Lokasi: `docs/drafts/pendahuluan.md` line 21.  
   - Masalah: paragraf ini menyatakan “Makalah ini disusun...” dan memberi outline bagian paper. Template proposal PUU meminta pendahuluan memuat roadmap penelitian setidaknya 5 tahun.  
   - Patch yang disarankan: jika targetnya proposal, ganti paragraf outline dengan roadmap singkat 5 tahun yang tetap hemat kata; jika targetnya artikel, pertahankan outline tetapi pastikan dokumen lain tidak mengharuskan roadmap.

## Minor non-blocking

- Citation style masih memakai ID internal `[S###]`. Ini boleh untuk draft riset, tetapi final proposal/artikel perlu dikonversi ke format sitasi numerik IEEE sesuai template.
- Sumber MDPI cukup banyak untuk people-counting terapan (`S010`, `S011`, `S018`), tetapi draft sudah menyeimbangkannya dengan CVPR/NeurIPS/Springer/Nature/Elsevier. Pada final submission, tetap pastikan dosen tidak keberatan dengan porsi MDPI.
- Kalimat line 9 yang menyebut D-FINE, DEIM, dan RF-DETR sudah cukup umum. Jangan menambah klaim rinci tentang performa ketiganya tanpa full-text note/detail validasi tambahan.

## Keputusan akhir

**READY_FOR_PATCH** — secara substansi sudah kuat, faktual, dan lebih tajam daripada proposal awal; patch yang dibutuhkan bersifat finalisasi: pangkas di bawah 1000 kata bila mengikuti template proposal PUU, dan sesuaikan paragraf akhir antara outline makalah atau roadmap 5 tahun sesuai target dokumen.