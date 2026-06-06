# Review Keras Revisi No. 3 — Usulan Pendekatan

## Verdict

`READY_FOR_MANUAL_REWRITE_AND_WORD_ASSEMBLY`

File copy-ready:

- `docs/revisions/revisi-no3-usulan-pendekatan-copy-to-word.md`

Gambar pendukung:

- `docs/diagrams/revisi-no3-architecture.png`
- `docs/diagrams/revisi-no3-research-workflow.png`
- `docs/diagrams/revisi-no3-id-state-memory.png`

## Komentar dosen yang ditangani

| Komentar | Status | Tindak lanjut |
|---|---|---|
| DL54 — tambahkan bagian rancangan eksperimen | Selesai | Ditambahkan subbagian `3.1 Rancangan Eksperimen` dan Tabel 1 berisi tujuan, objek studi, domain, fokus, pertanyaan evaluasi, dan variabel. |
| DL56 — buat gambar arsitektur + penjelasan detail | Selesai | Ditambahkan Gambar 1 dan paragraf penjelas. |
| DL57 — cantumkan sitasi referensi yang menginspirasi tahapan | Selesai | Setiap tahap memuat sitasi sumber relevan: detector, tracker, dataset, metric, counting logic. |
| DL58 — evaluasi disesuaikan dengan rancangan eksperimen awal | Selesai | Bagian evaluasi disusun ulang agar mengikuti S1–S4 dari Tabel 3. |
| Placeholder Gambar 2 | Selesai | Ditambahkan diagram `Research Workflow`. |
| Placeholder Gambar 3 | Selesai | Ditambahkan diagram `ID State Memory`. |

## Catatan keras

1. **Draft lama terlalu berisiko karena beberapa detail terlalu spesifik padahal eksperimen belum dilakukan.** Contoh: batch size 64, klaim STAL/ProgLoss akan memitigasi objek kecil, dan prediksi keunggulan DiffMOT/OC-SORT. Di file revisi, bagian itu dibuat sebagai rencana evaluasi, bukan hasil/dugaan yang seolah pasti.

2. **Jangan menulis YOLO26 seolah sudah peer-reviewed.** YOLO26 tetap aman sebagai kandidat implementasi/prototipe, tetapi argumen akademik NMS-free harus ditopang YOLOv10 dan RT-DETR.

3. **Jangan menyamakan dataset tracking dengan dataset counting.** MOT20/DanceTrack bagus untuk tracking, tetapi tidak otomatis menyediakan ground truth line/zone counting. Revisi sudah memisahkan fungsi dataset: deteksi, tracking, counting target.

4. **Gambar generated harus tetap dicek manusia sebelum ditempel ke Word.** Tiga gambar yang dipakai sudah lolos cek visual dasar. Satu gambar hasil generate awal untuk workflow ditolak karena typo dan tidak dipakai.

5. **Karena dosen eksplisit melarang AI, file ini tidak boleh diperlakukan sebagai final mentah tanpa pemahaman.** Gunakan sebagai bahan kerja: baca, pahami, ubah gaya kalimat sesuai cara bicaramu/tim, lalu baru tempel ke Word. Kalau dosen tanya, kamu harus bisa menjelaskan setiap tabel, gambar, dan alasan pemilihan metrik.

## Checklist sebelum ditempel ke Word

- [ ] Hapus/konversi format Markdown ke format Word normal.
- [ ] Sisipkan tiga gambar PNG secara manual.
- [ ] Pastikan caption gambar mengikuti urutan final di Word.
- [ ] Tambahkan referensi Wohlin dkk. (2012) ke daftar pustaka jika subbagian rancangan eksperimen dipakai.
- [ ] Sinkronkan nomor tabel/gambar dengan bagian teman yang mengerjakan No. 2.
- [ ] Pastikan sitasi `[S###]` dikonversi ke format sitasi yang dipakai paper final.
- [ ] Baca keras-keras minimal sekali; potong kalimat yang terdengar terlalu mesin atau terlalu panjang.
