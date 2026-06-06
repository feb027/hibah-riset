# Independent Strict Review — Revisi No. 3 Usulan Pendekatan

## Verdict

`READY_FOR_PATCH`

Artifact belum aman untuk langsung ditempel ke Word sebagai naskah final. Substansi revisi sudah jauh lebih baik dan sudah menjawab inti komentar dosen, tetapi masih ada beberapa risiko copy-to-Word, integrasi gambar/caption, dan ketajaman metodologis yang perlu dibereskan sebelum dipakai sebagai versi final.

## Ruang Lingkup Review

File yang direview:

- `docs/revisions/revisi-no3-usulan-pendekatan-copy-to-word.md`

Konteks pembanding:

- `docs/revisions/revisi-no3-komentar-dosen.md`
- `docs/revisions/revisi-no3-review-dan-catatan.md`
- `docs/_extracted/revisi-dosen-260602/full_text.txt`
- `docs/drafts/usulan-pendekatan.md`
- `references/references.bib`

Pengecekan teknis yang dilakukan:

- Semua sitasi `[S###]` yang muncul di artifact ada di `references/references.bib`.
- Referensi Wohlin 2012 sudah ada di BibTeX.
- Tiga path gambar yang dirujuk artifact ada di `docs/diagrams/`.
- Ukuran gambar terdeteksi 1536×1024 px untuk ketiga file.

## Penilaian terhadap Komentar Dosen

| Komentar dosen | Status review | Catatan ketat |
|---|---|---|
| DL54 — tambah rancangan eksperimen | Hampir terpenuhi | Ada subbagian 3.1 dan Tabel 1. Namun unsur eksperimen masih cukup umum; belum ada rancangan jumlah/jenis scene, level kepadatan, unit eksperimen, jumlah replikasi, atau definisi batas real-time. Untuk proposal awal masih dapat diterima, tetapi belum kuat sebagai desain eksperimen lengkap. |
| DL56 — gambar arsitektur + penjelasan detail | Terpenuhi secara struktur | Gambar 1 ada dan dijelaskan. Risiko tetap ada pada keterbacaan/akurasi teks di gambar generated image; perlu cek manual/OCR sebelum dimasukkan ke Word. |
| DL57 — sitasi tahapan yang diadopsi/menginspirasi | Mayoritas terpenuhi | Tahap detector, tracker, counting, dataset, dan metrik sudah diberi sitasi. Namun klaim metodologis ID state memory/counting logic masih lebih banyak ditopang referensi teknis DeepStream dan sumber people/occupancy counting umum, bukan paper khusus state-machine counting. |
| DL58 — evaluasi diselaraskan dengan rancangan eksperimen | Terpenuhi secara garis besar | Skenario S1–S4 sinkron dengan Tabel 1 dan metrik di 3.8. Masih perlu menambahkan definisi operasional metrik counting dan threshold real-time agar evaluasi tidak terlalu deklaratif. |

## Temuan Utama

### 1. Masalah terbesar: belum benar-benar aman untuk copy-to-Word langsung

Artifact masih memuat elemen non-naskah dan format Markdown:

- Judul meta `# Revisi No. 3 — USULAN PENDEKATAN (PROPOSED METHOD)`.
- Blockquote penjelasan file pada baris awal.
- Tabel masih dalam sintaks Markdown.
- Gambar masih berupa path relatif Markdown.
- Caption gambar muncul dua kali secara praktis: alt text gambar dan caption tebal setelah gambar.
- Sitasi masih memakai format internal `[S###]`, bukan gaya sitasi final paper.

Jika pengguna menyalin mentah ke Word, hasilnya akan tampak seperti bahan kerja, bukan naskah akademik. Ini cukup untuk membuat verdict menjadi `READY_FOR_PATCH`, bukan `READY_FOR_WORD_COPY`.

### 2. Rancangan eksperimen sudah ada, tetapi masih terlalu high-level

Tabel 1 sudah menjawab permintaan dosen secara formal, tetapi masih lemah sebagai rancangan eksperimen yang dapat langsung dieksekusi. Yang belum jelas:

- Berapa jumlah video target minimal.
- Bagaimana pembagian kepadatan rendah/sedang/tinggi.
- Apakah unit eksperimen per video, per scene, per interval waktu, atau per event crossing.
- Apakah setiap konfigurasi akan diuji berulang.
- Apa batas realistis untuk real-time, misalnya minimal FPS atau batas latency p95.
- Apa definisi operasional `counting error rate`, `direction accuracy`, `over-count`, dan `under-count`.

Saran patch: tambahkan satu paragraf singkat setelah Tabel 3 atau di 3.8 yang mendefinisikan unit evaluasi dan batas real-time yang akan dipakai. Jangan menambahkan angka target performa jika belum ada dasar; gunakan formulasi “akan dilaporkan terhadap batas kebutuhan aplikasi/perangkat yang dinyatakan eksplisit”.

### 3. Klaim dan reasoning sudah lebih hati-hati, tetapi beberapa bagian masih terdengar normatif

Artifact berhasil menghindari fake-result wording yang ada di draft lama. Tidak ada klaim numerik hasil eksperimen palsu. Namun beberapa kalimat masih terdengar seperti justifikasi generik/AI-like, misalnya pola berulang:

- “penting karena...”
- “diperlukan karena...”
- “tidak cukup...”
- “dengan demikian...”
- “secara akademik...”

Ini bukan kesalahan fatal, tetapi jika dosen sensitif terhadap tulisan AI, gaya ini perlu dipadatkan dan dibuat lebih natural. Beberapa kalimat dapat digabung atau dibuat lebih spesifik terhadap konteks penelitian.

### 4. Risiko sitasi: lengkap secara ID, tetapi perlu kehati-hatian status sumber

Hasil cek menunjukkan semua S-ID yang dikutip artifact ada di BibTeX:

- `S001 S002 S003 S004 S010 S011 S021 S024 S025 S026 S034 S035 S036 S037 S038`

Tidak ada S-ID hilang di `references.bib`. Wohlin 2012 juga sudah ada.

Namun ada risiko interpretasi:

- `S001` YOLO26 adalah arXiv/preprint dan `S002` dokumentasi vendor; artifact sudah cukup hati-hati memosisikan YOLO26 sebagai kandidat implementasi, bukan dasar novelty tunggal. Ini harus dipertahankan.
- `S035` DeepStream adalah dokumentasi vendor. Artifact sudah menyatakan hanya referensi teknis, bukan bukti akademik utama. Ini juga harus dipertahankan.
- `S003` dan `S004` di BibTeX saat ini tercatat sebagai arXiv. Jangan menulis “peer-reviewed” untuk keduanya kecuali metadata final peer-reviewed sudah diverifikasi.
- Kutipan Wohlin dkk. ditulis naratif, bukan dalam format `[S###]`; saat masuk Word, pastikan format sitasinya konsisten dengan paper final.

### 5. Gambar ada, tetapi risiko integrasi gambar masih tinggi

Tiga gambar yang dirujuk memang ada:

- `docs/diagrams/revisi-no3-architecture.png`
- `docs/diagrams/revisi-no3-research-workflow.png`
- `docs/diagrams/revisi-no3-id-state-memory.png`

Semua berukuran 1536×1024 px. Namun review ini hanya memastikan keberadaan dan ukuran, bukan memvalidasi isi visual per label. Risiko yang harus dicek manual sebelum Word:

- Apakah semua teks di gambar bebas typo.
- Apakah istilah di gambar sama dengan istilah di narasi, misalnya `inside ROI`, `cooldown`, `expired`, `DiffMOT`, `OC-SORT`.
- Apakah arah panah state machine masuk akal dan tidak bertentangan dengan paragraf.
- Apakah resolusi tetap terbaca setelah diperkecil di Word.
- Apakah nama file teknis tidak terlihat di naskah final; nama file tidak masalah secara teknis, tetapi jangan sampai muncul dalam caption atau daftar gambar.
- Caption sebaiknya hanya satu kali dalam Word, bukan alt text Markdown plus caption tebal.

### 6. Alignment evaluasi sudah baik, tetapi perlu definisi operasional

Bagian 3.6 dan 3.8 sudah selaras: S1 deteksi, S2 tracking, S3 counting logic, S4 end-to-end/real-time. Ini memperbaiki draft lama yang hanya punya tiga skenario dan kurang sinkron dengan rancangan eksperimen.

Kelemahan yang tersisa:

- MAPE dapat bermasalah bila ground truth event kecil; artifact belum memberi batas pemakaian MAPE.
- `direction accuracy` belum didefinisikan sebagai rasio event arah benar terhadap total event arah berlabel.
- `counting error` muncul sebagai istilah umum, tetapi belum ada rumus atau definisi singkat.
- `latency rata-rata/p95` bagus, tetapi belum jelas apakah dihitung per frame, per event, atau end-to-end pipeline.

Saran patch minimal: tambahkan 3–4 kalimat definisi operasional di 3.8.

### 7. Data target masih terlalu abstrak

Artifact menyebut “video target ruang publik”, “rekaman CCTV”, atau “video publik” dengan cukup hati-hati. Ini aman karena eksperimen belum dilakukan. Namun untuk rancangan eksperimen, bagian ini masih kurang spesifik:

- Belum ada kriteria minimal scene target.
- Belum ada rencana anotasi event counting yang cukup rinci.
- Belum ada pembeda eksplisit antara validasi pada data publik dan validasi domain lokal.

Saran: tambahkan kriteria pemilihan video target tanpa mengklaim data sudah tersedia. Contoh: kamera statis, durasi minimal dilaporkan, jumlah event manual dilaporkan, variasi kepadatan dan pencahayaan dicatat.

## Overclaim / Fake-result Wording Check

Tidak ditemukan hasil numerik palsu atau klaim “model terbukti unggul” pada artifact revisi. Kalimat yang masih perlu dijaga agar tidak berubah menjadi overclaim:

- “DiffMOT dirancang sebagai tracker utama...” aman, selama tetap rencana.
- “OC-SORT digunakan sebagai baseline dan fallback efisien...” aman, tetapi jangan ditulis sebagai pasti lebih cepat pada semua perangkat sebelum diuji.
- “ID state memory ... mencegah objek yang sama dihitung berulang...” sebaiknya ditulis sebagai “dirancang untuk mengurangi/mencegah” karena efektivitasnya belum diuji.
- “pipeline tetap memungkinkan digunakan pada skenario real-time” harus diikuti definisi evaluasi FPS/latency, bukan klaim kelayakan.

## Patch Prioritas Sebelum Word

1. Hapus header meta dan blockquote instruksi di awal file.
2. Konversi semua tabel Markdown menjadi tabel Word normal.
3. Sisipkan gambar secara manual, lalu gunakan satu caption resmi per gambar.
4. Konversi sitasi `[S###]` dan Wohlin 2012 ke format sitasi final paper.
5. Tambahkan definisi operasional ringkas untuk `counting error`, `MAE/MAPE`, `direction accuracy`, dan `latency/FPS end-to-end`.
6. Tambahkan batasan rancangan eksperimen: unit evaluasi, pelaporan jumlah video/event, karakteristik scene, dan konfigurasi perangkat.
7. Cek manual isi gambar generated image untuk typo, panah yang salah, dan konsistensi istilah.
8. Padatkan beberapa kalimat repetitif agar terdengar lebih natural dan tidak terlalu template.

## Kesimpulan Review

Secara substansi, revisi No. 3 sudah menjawab arahan utama dosen: rancangan eksperimen ditambahkan, arsitektur dan tahapan divisualkan, sitasi sumber inspirasi sudah tersedia, dan evaluasi sudah dihubungkan ke skenario eksperimen. Namun artifact belum layak ditempel mentah ke Word karena masih berformat Markdown, masih ada elemen meta, caption/alt-text raw, sitasi internal, dan beberapa definisi evaluasi belum operasional.

Verdict akhir: `READY_FOR_PATCH`.
