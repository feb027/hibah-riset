# Review Naskah Video PUU 2026 dan Dasar Penulisan Ulang

Disusun 18 September 2026. Mengaudit `naskah-asli.txt` dan `naskah-tts.txt` (v1, 15 paragraf) terhadap `docs/laporan-kemajuan/bab-hasil-pelaksanaan-penelitian.md`, `docs/journal/en/jestec-manuscript-en.md`, dan template A4 Laporan Kemajuan PUU. Naskah pengganti ada di `naskah-asli-v2.txt` dan `naskah-tts-v2.txt` (16 paragraf).

---

## 1. Putusan singkat

**Kerangkanya sudah bagus, isinya belum boleh dipakai apa adanya.**

Yang sudah benar dan tidak perlu diubah: aturan dua berkas, jumlah paragraf dan kalimat yang identik, nol digit di versi TTS, nol em dash/titik koma/tanda kurung di kedua berkas, kalimat terpanjang 19 kata, enumerasi eksplisit alih-alih daftar berderet, render per paragraf, dan penguncian suara lewat audio acuan. Semua itu sesuai praktik terbaik yang ditemukan di riset bagian 3, dan sudah terverifikasi mesin.

Yang salah: tiga cacat fakta dan lima kekosongan isi. Dua di antaranya akan langsung terlihat oleh dosen yang membaca laporan kemajuannya.

---

## 2. Hasil audit

### 2.1 RUSAK — harus diperbaiki

| # | Lokasi | Masalah | Bukti |
| :--- | :--- | :--- | :--- |
| R1 | `naskah-asli.txt:17` | "Deep-OC-SORT ... masih bisa berjalan pada perangkat tanpa kartu grafis" | Bertentangan dengan Tabel 12 laporan: Deep-OC-SORT pada perangkat edge hanya **12,0 FPS**, gagal ambang 30 FPS. Yang lolos di edge adalah **OC-SORT, 30,7 FPS**. Laporan menyatakan pilihannya bersyarat perangkat, justru salah satu temuan utamanya |
| R2 | `naskah-asli.txt:15` | Pelacak terbaik tidak pernah disebut namanya, hanya "pelacak berbasis diffusion", sementara Deep-OC-SORT disebut | Pendengar tidak bisa memetakan angka HOTA 44,37 ke nama tracker mana pun. Paper JESTEC menulisnya eksplisit: DiffMOT |
| R3 | `naskah-asli.txt:11` | "YOLO26 varian small" | Nama modelnya YOLO26s. "varian small" tidak dipakai di laporan maupun paper, dan tidak bisa dicari pembaca |

### 2.2 REVISI — kekosongan isi

| # | Kekosongan | Alasan |
| :--- | :--- | :--- |
| V1 | Status luaran tidak disebut sama sekali | Template A4 bagian **H. STATUS LUARAN PENELITIAN** adalah butir yang dinilai pada laporan kemajuan. Video yang tidak menyebut JESTEC dan HKI melewatkan pertanyaan pertama penilai |
| V2 | Singkatan RANCAGE tidak pernah dijabarkan | Nama sistem adalah judul penelitian. Video yang tidak menjabarkannya membuang satu-satunya kesempatan menjelaskan arti namanya |
| V3 | Temuan objek terpotong tepi bingkai tidak ada di video | Ada di laporan (§3.1) dan di paper §4.1.2, dan ini satu-satunya temuan yang langsung berbentuk instruksi desain: garis hitung dijauhkan dari tepi bingkai. Recall kelompok ini turun 20–21 poin |
| V4 | Versi TTS menyisakan kosakata yang tidak dikonversi | "varian smol" (bukan kata apa pun) dan "dataset" yang justru ada di tabel istilah sendiri sebagai "de-ta-set" |
| V5 | Tidak ada atribusi institusi di penutup | Video kegiatan UNSIL umumnya menutup dengan unit pengembang. Nol biaya, menaikkan kelengkapan |

### 2.3 BAGUS — dipertahankan

- Aturan dua berkas dengan batas kalimat identik. Terverifikasi: v1 63/63 kalimat, v2 70/70 kalimat, nol selisih per paragraf.
- Nol digit di berkas TTS, nol em dash / titik koma / tanda kurung di kedua berkas.
- Enumerasi eksplisit ("Pertama... Kedua...") alih-alih daftar berderet koma.
- Penguncian suara lewat berkas audio acuan, bukan deskripsi teks. Ini persis pola yang direkomendasikan dokumentasi VoxCPM2 dan diperkuat temuan drift antar segmen pada riset bagian 3.
- Paragraf 9 versi v1 (alasan tracker terbaik tidak dipakai) adalah keputusan penulisan yang tepat. Dipertahankan, isinya dikoreksi.

---

## 3. Dasar riset untuk penulisan ulang

Semua sumber diverifikasi 18 September 2026.

### 3.1 Struktur naskah video penelitian

| Temuan | Sumber |
| :--- | :--- |
| Segmen baku: *hook* 10–15 dtk (mengapa penting), konteks 20–30 dtk, metode 30–60 dtk, temuan 30–45 dtk, implikasi 15–20 dtk. Tempo 130–150 kata/menit | X-Pilot, *Academic Research Video Production: 2026 Scientist Guide* |
| Busur naratif dengan proporsi: masalah 10%, metode 30%, temuan 40%, implikasi **dan keterbatasan** 20%. Porsi keterbatasan disebut tidak bisa ditawar untuk integritas riset | X-Pilot, *Research Visualization Best Practices* |
| Buka dengan pertanyaan penelitian, bukan dengan institusi; nama dan afiliasi cukup jadi teks di layar | CASRAI, *How to Create a Video Abstract for a Research Paper* |
| Tiga beat tetap yang berulang di panduan semua penerbit: pertanyaan → metode → temuan dan artinya | CASRAI, idem |
| Baca naskah lantang dengan stopwatch sebelum rekaman. Memotong naskah setelah rekaman selalu lebih mahal | CASRAI, idem |
| Struktur hook → masalah → solusi → bukti → analisis → dampak → langkah lanjut | The Online Scientist, *Make your research speak* |

**Konsekuensinya untuk naskah ini.** v1 sudah mengikuti busur itu, dan penutupnya sudah memuat keterbatasan secara tersirat. v2 menambah satu paragraf luaran pada posisi "implikasi dan langkah lanjut", sebelum peta jalan.

### 3.2 Panjang dan tempo

| Temuan | Sumber |
| :--- | :--- |
| Standar industri voice over Indonesia 2,5 kata per detik. Video 3 menit ≈ 420–450 kata; 60 detik ≈ 140–160 kata | Creativism, *Teks Voice Over: 16 Contoh Naskah Siap Pakai* |
| Narasi 140–170 kata/menit untuk bahasa Inggris; satu slide jangan melebihi 25–30 detik | 2Slides, *Panduan Terbaik Video Narasi Slide* |
| Musik latar −28 sampai −32 dB, jeda 200–500 ms antar pergantian topik | 2Slides, idem |

Angka 2,5 kata per detik setara **150 kata per menit**, sedikit di atas rentang 130–150 yang dipakai `riset-tts-video-penelitian.md`. Rentang aman yang dipakai v2: **130–150 kata per menit**, artinya 695 kata ≈ **4,6–5,0 menit**.

Catatan durasi: Panduan Pelaksanaan Penelitian UNSIL Edisi VI mencantumkan **"Video kegiatan 3 menit dimuat di Youtube, Instagram dengan hashtag LP2M-PMP UNSIL"** pada tabel indikator kinerja **pengabdian** sebagai luaran tambahan. Tabel indikator **penelitian** (Tabel 2.3) tidak memuat butir video dan tidak menetapkan durasi. Artinya 3 menit adalah norma institusi pada sisi pengabdian, bukan batas resmi skema PUU. Durasi video luaran 2025 tidak terdokumentasi di repositori ini; yang dipakai sebagai acuan adalah pola narasinya, bukan panjangnya. Kalau dosen memegang angka 3 menit, naskah harus dipotong seperti opsi 1 pada bagian 5.

### 3.3 Model TTS: dua temuan operasional baru

| Temuan | Sumber |
| :--- | :--- |
| VoxCPM2 punya mode **Style Control**: audio referensi menentukan *siapa* yang bicara, tag di dalam tanda kurung menentukan *bagaimana* ia bicara, termasuk tempo. Klaim lama di `riset-tts-video-penelitian.md` (berdasarkan issue #210) bahwa instruksi gaya diabaikan pada mode kloning perlu diuji ulang pada 2.0.3 | VoxCPM2 documentation, *Style Control* |
| Batas keras model: **8192 token** dan audio maksimum **3 menit** per pemanggilan. Patch size 4 menurunkan laju token ke 6,25 Hz dan **memperbaiki kestabilan teks panjang** | VoxCPM2 Technical Report, arXiv:2606.06928 |
| Praktik potong yang terbukti: pecah di batas kalimat, gabungkan sampai sekitar **15 detik** per segmen. Tanpa pola jangkar, suara **melayang antar segmen** dan terdengar patah | A. Zhu, *VoxCPM2 is great. Using it directly is not* |
| WER Bahasa Indonesia terukur 1,08–1,36%. Model tidak butuh model khusus Bahasa Indonesia | VoxCPM2 Technical Report, Tabel 6 |

**Konsekuensinya.** Pola jangkar yang sudah dipakai repositori ini (paragraf 1 jadi acuan, sisanya mengkloning berkas itu) tepat, dan riset di atas menjelaskan alasannya: tanpa jangkar, suara melayang. Dua tambahan yang belum dipakai: (a) uji apakah tag gaya di dalam tanda kurung masih berpengaruh saat `reference_wav_path` diisi, karena kalau berpengaruh, tempo tidak perlu dipanggang ke audio acuan; (b) batas 3 menit per pemanggilan sudah aman karena naskah ini dirender per paragraf.

---

## 4. Yang berubah di v2

| Paragraf | v1 | v2 |
| :--- | :--- | :--- |
| 5 | "penelitian ini membangun RANCAGE, sebuah pipeline..." | ditambah penjabaran singkatan |
| 6 | "YOLO26 varian small" | "YOLO26s" |
| 7 | dua temuan deteksi | ditambah temuan objek terpotong tepi bingkai dan implikasi penempatan garis hitung |
| 8 | "pelacak berbasis diffusion" | "DiffMOT, pelacak berbasis difusi" |
| 9 | klaim Deep-OC-SORT jalan di perangkat tanpa GPU | dikoreksi: edge memakai OC-SORT 30 FPS, Deep-OC-SORT hanya 12 FPS di sana |
| 13 | tidak ada | paragraf baru: status luaran JESTEC, HKI, tingkat kesiapan teknologi 3–4 |
| 16 | "Terima kasih." | ditambah atribusi Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi |
| TTS | "varian smol", "dataset" | "Yolo dua puluh enam es", "data set" |

Hasil verifikasi mesin atas v2:

```
paragraf: 16 | kalimat: 70 (berkas asli) = 70 (berkas TTS), sama per paragraf
kata: 695 | durasi 130-150 wpm: 4,63-5,35 menit
maks kata/kalimat: 21 | digit di berkas TTS: 0
em dash / titik koma / tanda kurung: 0 di kedua berkas
--dry-run: 16 berkas rencana render, penomoran benar
```

---

## 5. Yang masih perlu diputuskan

1. **Durasi.** v2 = 695 kata ≈ 4,6–5,0 menit. Kalau dosen menuntut ≤4 menit, yang dipotong lebih dulu: paragraf 14 (peta jalan, 6 kalimat) dipadatkan jadi 3 kalimat, dan baris atribusi institusi dipindah ke teks layar. Itu membawa naskah ke ±630 kata ≈ 4,2 menit tanpa kehilangan satu pun angka hasil.
2. **Uji Style Control.** Render satu paragraf dengan `--reference-wav` **dan** tag `(calm, brisk pace)` di dalam kurung. Kalau tempo ikut berubah, catatan issue #210 di `riset-tts-video-penelitian.md` sudah usang dan perlu dikoreksi.
3. **Uji dengar kata rawan.** Empat kata yang paling berisiko pada naskah ini: `Siliwangi` (pernah jadi "liwangi" pada video 2025), `rikol` (recall), `tre-ker` (tracker), dan `Jes tek`. Dengarkan pada render paragraf 1, 7, 9, dan 13 sebelum render penuh.
4. **Subtitle.** Tetap dari `naskah-asli-v2.txt`, bukan berkas TTS. Keterangan narasi berbantuan AI masuk deskripsi video, bukan narasi.

---

## 6. Rujukan

1. X-Pilot, *Academic Research Video Production: 2026 Scientist Guide*. https://www.x-pilot.ai/blog/academic-research-video-production-guide-2026 — diakses 18 September 2026.
2. X-Pilot, *Research Visualization Best Practices: Papers to Video 2026*. https://www.x-pilot.ai/blog/research-visualization-best-practices-paper-to-video-2026 — diakses 18 September 2026.
3. CASRAI, *How to Create a Video Abstract for a Research Paper*. https://www.casrai.org/guides/how-to-create-a-video-abstract-for-a-research-paper — diakses 18 September 2026.
4. The Online Scientist, *Make your research speak: how to script your infographic, scrollytelling, and animated video*. https://www.theonlinescientist.com/make-your-research-speak-how-to-script-your-infographic-scrollytelling-and-animated-video/ — diakses 18 September 2026.
5. Creativism, *Teks Voice Over: 16 Contoh Naskah Siap Pakai* — standar 2,5 kata per detik narator Indonesia. https://creativism.id/teks-voice-over/ — diakses 18 September 2026.
6. 2Slides, *Panduan Terbaik Video Narasi Slide* — tempo 140–170 wpm, musik −28 sampai −32 dB. https://2slides.com/id/blog/slides-narration-video-best-practices — diakses 18 September 2026.
7. OpenBMB, *VoxCPM 2.0 documentation* — Voice Design, Style Control, isolated reference channel, batas 8192 token. https://voxcpm.readthedocs.io/en/latest/models/voxcpm2.html — diakses 18 September 2026.
8. VoxCPM Team, *VoxCPM2: Tokenizer-Free TTS for Multilingual Speech Generation, Creative Voice Design, and True-to-Life Cloning*, arXiv:2606.06928 — patch size 4, laju 6,25 Hz, kestabilan teks panjang, WER Bahasa Indonesia. https://arxiv.org/html/2606.06928 — diakses 18 September 2026.
9. A. Zhu, *VoxCPM2 is great. Using it directly is not* — pemotongan di batas kalimat, target 15 detik per segmen, drift suara antar segmen tanpa pola jangkar. https://xhinker.medium.com/voxcpm2-is-great-using-it-directly-is-not-974b371b1a64 — diakses 18 September 2026.
10. Universitas Siliwangi, *Panduan Pelaksanaan Penelitian dan Pengabdian kepada Masyarakat Edisi VI*, 2022 — Tabel 2.4 memuat butir "Video kegiatan 3 menit dimuat di Youtube, Instagram dengan hashtag LP2M-PMP UNSIL". https://sejarah.unsil.ac.id/wp-content/uploads/2024/06/PANDUAN-PELAKSANAAN-PENELITIAN-2022-Edisi-VI-20220701_compressed.pdf — diakses 18 September 2026.
