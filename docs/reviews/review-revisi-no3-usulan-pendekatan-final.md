# Final Strict Review — Revisi No. 3 Usulan Pendekatan

## Verdict

`READY_FOR_WORD_COPY`

Artifact revisi No. 3 sudah cukup aman untuk **manual Word assembly**. Blocker utama dari review sebelumnya sudah diperbaiki pada level yang diperlukan: header/meta awal sudah dibersihkan, substansi rancangan eksperimen diperkuat, definisi evaluasi counting/real-time sudah ditambahkan, kriteria video target sudah lebih eksplisit, dan path gambar yang dirujuk tersedia. Masih ada pekerjaan teknis saat perakitan Word, tetapi itu bersifat formatting/manual assembly, bukan blocker isi draft.

## Ruang Lingkup Review

File utama:

- `docs/revisions/revisi-no3-usulan-pendekatan-copy-to-word.md`

Konteks pembanding:

- `docs/revisions/revisi-no3-komentar-dosen.md`
- `docs/reviews/review-revisi-no3-usulan-pendekatan.md`

Pengecekan teknis yang dilakukan:

- Semua sitasi internal yang muncul di artifact (`S001`, `S002`, `S003`, `S004`, `S010`, `S011`, `S021`, `S024`, `S025`, `S026`, `S034`, `S035`, `S036`, `S037`, `S038`) ditemukan di `references/references.bib`.
- Referensi Wohlin / *Experimentation in Software Engineering* ditemukan di `references/references.bib`.
- Tiga path gambar yang dirujuk artifact ada di `docs/diagrams/`.
- Ketiga gambar berukuran 1536×1024 px.
- Artifact tidak lagi memuat header meta “Revisi No. 3” atau blockquote instruksi di awal.

## Status terhadap Blocker Review Sebelumnya

| Blocker review sebelumnya | Status final | Catatan |
|---|---|---|
| Header meta dan blockquote instruksi di awal file | **Fixed** | File sekarang langsung masuk ke judul bagian `USULAN PENDEKATAN (PROPOSED METHOD)`. |
| Rancangan eksperimen terlalu high-level | **Fixed enough** | Tabel rancangan eksperimen, skenario S1–S4, unit evaluasi, karakteristik video/scene, dan variabel pengukuran sudah lebih jelas untuk proposal metodologi. |
| Definisi operasional metrik counting belum ada | **Fixed** | Bagian 3.8 sudah mendefinisikan absolute counting error, MAE, MAPE, over-count, under-count, direction accuracy, FPS, dan latency end-to-end. |
| Data target terlalu abstrak | **Fixed enough** | Artifact sudah menyebut karakteristik minimal video/scene: posisi kamera, durasi, FPS sumber, pencahayaan, kepadatan, jumlah event manual, dan bentuk RoI/line/zone. |
| Risiko overclaim / fake-result wording | **Fixed enough** | Teks konsisten menyatakan eksperimen belum dijalankan dan tidak menyajikan hasil numerik. YOLO26, DiffMOT, OC-SORT, dan ID state memory diposisikan sebagai rancangan/kandidat yang akan diuji, bukan sebagai hasil terbukti. |
| Sitasi internal perlu integrasi | **Not a content blocker** | Semua S-ID tersedia di BibTeX. Pada Word final, `[S###]` tetap harus dikonversi ke gaya sitasi paper, tetapi ini pekerjaan perakitan sitasi, bukan blocker draft metodologi. |
| Gambar masih perlu integrasi manual | **Not a content blocker** | Path gambar valid. Pada Word final, gambar perlu disisipkan manual dan placeholder path tidak boleh ikut menjadi isi naskah final. |
| Markdown table masih perlu konversi | **Not a content blocker** | Tabel masih dalam sintaks Markdown, tetapi struktur tabel sudah jelas untuk dikonversi ke tabel Word. |

## Status terhadap Komentar Dosen

| Komentar dosen | Status final | Catatan |
|---|---|---|
| DL54 — Tambahkan rancangan eksperimen dan tahapan penelitian visual beserta penjelasan serta sitasi | **Terpenuhi** | Subbagian 3.1, Tabel 1, Gambar 2, narasi tahapan, dataset, model, metrik, dan sitasi sudah tersedia. |
| DL55 — Sesuaikan contoh detail rancangan eksperimen dengan kebutuhan penelitian | **Terpenuhi** | Unsur eksperimen disesuaikan dengan domain people counting: tujuan, objek studi, domain, fokus, pertanyaan evaluasi, dan variabel. |
| DL56 — Buat gambar arsitektur dan penjelasan detail | **Terpenuhi** | Gambar 1 dirujuk dan alur input video → preprocessing → detector → tracker → counting logic → output/evaluasi dijelaskan. |
| DL57 — Cantumkan semua sitasi referensi yang diadopsi/menginspirasi tahapan pengembangan | **Terpenuhi cukup** | Detector, tracker, counting logic, dataset, metrik, dan eksperimen sudah diberi rujukan. Status YOLO26 dan DeepStream sudah diposisikan hati-hati. |
| DL58 — Selaraskan evaluasi dengan rancangan eksperimen | **Terpenuhi** | Skenario S1–S4 sudah selaras dengan Tabel 1 dan bagian 3.8. |

## Catatan Final untuk Manual Word Assembly

Hal-hal berikut masih wajib dilakukan saat menyusun dokumen Word, tetapi tidak mengubah verdict:

1. Konversi tabel Markdown menjadi tabel Word normal.
2. Sisipkan tiga gambar secara manual dari path berikut:
   - `docs/diagrams/revisi-no3-architecture-gpt-image-2.png`
   - `docs/diagrams/revisi-no3-research-workflow-gpt-image-2.png`
   - `docs/diagrams/revisi-no3-id-state-memory-gpt-image-2.png`
3. Hapus teks placeholder `[Sisipkan Gambar ...]` setelah gambar benar-benar dimasukkan ke Word.
4. Gunakan satu caption resmi per gambar sesuai teks artifact.
5. Konversi `[S###]` dan sitasi naratif Wohlin dkk. ke format sitasi final yang konsisten dengan paper.
6. Cek visual gambar secara manual di Word: keterbacaan teks, konsistensi istilah, arah panah, dan ukuran setelah diperkecil.

## Kesimpulan

Revisi patched No. 3 sudah memenuhi arahan utama dosen dan sudah memperbaiki blocker substansi dari review sebelumnya. Sisa pekerjaan adalah formatting, penyisipan gambar, dan konversi sitasi pada tahap manual Word assembly.

Verdict akhir: `READY_FOR_WORD_COPY`.
