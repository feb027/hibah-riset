# Storyboard Narasi Video PUU 2026 — versi supervisor (v3)

Disusun 18 September 2026. Naskah narasi diambil dari storyboard bertimecode yang diberikan dosen pembimbing, lalu dipecah menjadi 9 paragraf tanpa mengubah isinya. Berkas yang dipakai untuk render: `naskah-asli-v3.txt` (subtitle) dan `naskah-tts-v3.txt` (sintesis).

Sumber angka: `docs/laporan-kemajuan/bab-hasil-pelaksanaan-penelitian.md`. Tidak ada klaim baru di luar laporan dan paper JESTEC.

---

## Ringkasan

| Blok | Target timecode | Target kata | Kata aktual | Paragraf |
| :--- | :--- | :---: | :---: | :---: |
| Opening | 00:00–00:25 | 58 | 71 | 1 |
| Pengenalan RANCAGE | 00:25–00:55 | 70 | 73 | 2 |
| Tujuan Penelitian | 00:55–01:30 | 82 | 53 | 3 |
| Metodologi | 01:30–02:15 | 105 | 116 | 4 |
| Hasil Utama | 02:15–03:10 | 128 | 118 | 5 |
| Real-Time Performance | 03:10–03:55 | 105 | 103 | 6 |
| Kebaruan dan Kontribusi | 03:55–04:25 | 70 | 59 | 7 |
| Luaran dan Pengembangan | 04:25–04:50 | 58 | 80 | 8 |
| Closing | 04:50–05:00 | 23 | 20 | 9 |
| **Total** | **5 menit** | **699** | **693** | **9** |

693 kata pada 140 kata per menit = **4 menit 57 detik**, masuk ke target 4:30–5:00. Verifikasi mesin: 9 paragraf, 48 kalimat identik di kedua berkas, nol digit di berkas TTS, nol em dash / titik koma / tanda kurung / tanda hubung, kalimat terpanjang 24 kata.

---

## Catatan penyuntingan yang dilakukan

Naskah dosen dipakai apa adanya. Tiga hal dikerjakan agar memenuhi aturan TTS, dan semuanya bisa dibatalkan kalau tidak disetujui.

### 1. Kalimat panjang dipecah

Kalimat di atas 25 kata tidak bisa dibaca TTS tanpa kehilangan jeda. Yang dipecah:

| Blok | Kalimat asli dosen | Hasil |
| :--- | :--- | :--- |
| Opening | "…informasi mengenai jumlah serta arus pergerakan orang menjadi penting untuk mendukung pemantauan dan pengambilan keputusan berbasis data." | jadi dua kalimat |
| Pengenalan | "Sistem dirancang tidak hanya untuk mendeteksi keberadaan orang, tetapi juga mempertahankan identitas…" | jadi dua kalimat |
| Metodologi | "Tahapan penelitian dimulai dari … di-fine-tune menggunakan dataset CrowdHuman." | jadi dua kalimat |
| Hasil | "Pada pengujian, state machine … pada konfigurasi tracker dengan kinerja terbaik." | jadi dua kalimat |
| Real-Time | "Sebanyak 95 persen frame … acuan untuk mencapai minimal 30 frame per detik." | jadi dua kalimat |
| Kebaruan | "Kontribusi penelitian ini tidak terletak pada … tetapi pada evaluasi kuantitatif…" | jadi dua kalimat |
| Luaran | "…dua luaran utama, yaitu publikasi … serta Hak Cipta…", "Pengujian langsung menggunakan CCTV…" | jadi tiga kalimat |
| Closing | tanda pisah pada "RANCAGE — mengubah…" | dihapus |

### 2. Kata dipertegas tanpa mengubah isi

- "mempertahankan identitas" tetap; ditambah "Kontribusinya terletak pada…" agar kalimat kedua punya subjek.
- "Pendekatan ini diharapkan dapat menghasilkan" jadi "Pendekatan ini diharapkan menghasilkan".

### 3. Tujuh kalimat ditambahkan, semua dari laporan

Naskah dosen berisi 551 kata, sedangkan timecode-nya sendiri menjumlah 5 menit. Selisih itu diisi dengan angka yang sudah ada di laporan kemajuan, bukan klaim baru.

| Blok | Kalimat tambahan | Sumber di laporan |
| :--- | :--- | :--- |
| Opening | "Orang yang sama bisa terhitung dua kali setelah terhalang, identitas dua orang bisa tertukar, dan hitungan palsu bisa muncul di sekitar garis hitung." | §5, mekanisme kegagalan model naive |
| Pengenalan | "Ketiga komponen itu diuji terpisah maupun bersama, sehingga pengaruh setiap lapisan terhadap akurasi hitungan dapat diukur." | §4 paper JESTEC, tiap tahap diuji terpisah atau end-to-end |
| Metodologi | "Seluruh tracker dijalankan pada keluaran deteksi yang identik, supaya perbandingannya adil." | §4, Tabel 6 |
| Metodologi | "Evaluasi pelacakan memakai TrackEval pada 29 sekuens, yaitu empat sekuens MOT20 dan dua puluh lima sekuens DanceTrack." | §4, protokol evaluasi |
| Hasil | "Pada tahap deteksi, YOLO26s mencapai mAP sebesar 0,4974, yang tertinggi di antara empat arsitektur." | §3.1, Tabel 2 |
| Hasil | "Namun, 7,4 sampai 10,0 persen orang tetap tidak terdeteksi pada ambang keyakinan mana pun, dan batas itu terbentuk di lapisan deteksi." | §3.1, Tabel 3 |
| Real-Time | "Pada perangkat tanpa kartu grafis, jalur OC-SORT masih menyentuh 30,7 frame per detik, sedangkan Deep-OC-SORT turun ke 12,0 frame per detik." | §7, Tabel 12 |
| Luaran | "Peta jalan lima tahun mengarah pada penguatan ketahanan model, fitur atensi, pemampatan model, dan penerapan pada infrastruktur kota cerdas." | §Pendahuluan proposal, roadmap 5 tahun |

Kalau dosen ingin naskahnya persis seperti aslinya, hapus delapan kalimat di tabel itu. Sebagai gantinya video akan jatuh ke sekitar 4 menit 0 detik, di bawah timecode yang diminta.

---

## Visual per blok

Tetap sesuai storyboard dosen, dipakai apa adanya di editor.

| Blok | Visual |
| :--- | :--- |
| Opening | Foto/video people counting → bounding box → ID tracking → angka count IN/OUT |
| Pengenalan RANCAGE | Logo/judul RANCAGE → arsitektur sistem secara keseluruhan |
| Tujuan Penelitian | Tiga tujuan muncul satu per satu |
| Metodologi | Dataset → YOLO26 → Deep-OC-SORT/OC-SORT → Counting Logic → Output |
| Hasil Utama | Grafik batang galat: Naive 101,99% → LightTrack 53,03% → OC-SORT 22,38% → Deep-OC-SORT 16,71% → DiffMOT 13,08%, lalu HOTA dan IDF1 |
| Real-Time Performance | Angka besar: 24,61 ms/frame, 40,6 FPS, 0,11 ms counting logic, 95% frame di bawah 33,3 ms |
| Kebaruan dan Kontribusi | Detection → Identity → Trajectory → Counting |
| Luaran dan Pengembangan | Ikon jurnal → HKI → edge device → CCTV |
| Closing | Judul RANCAGE dan identitas program studi |

Catatan untuk editor: grafik batang di blok Hasil Utama menampilkan 101,99% sebagai titik Naive, sedangkan narasinya menyebut rentang 88,7–155,1 persen. Keduanya benar dan berasal dari tabel yang berbeda di laporan, yaitu 101,99% untuk jalur Deep-OC-SORT pada cooldown 0 (§6, Tabel 9) dan rentang 88,7–155,1 persen untuk rata-rata lintas jalur tracker (§5, Tabel 8). Sebaiknya label pada grafik ditulis "Deep-OC-SORT, cooldown 0" supaya tidak terbaca sebagai angka yang bertentangan.

---

## Setelah naskah ini

1. Render dengan `--reference-wav`. Tanpa berkas acuan, tiap paragraf jadi suara berbeda.
2. Urutan render dan pemilihan suara: `cara-pakai-voxcpm2.md`.
3. Subtitle dibuat dari `naskah-asli-v3.txt`, bukan berkas TTS.
4. Keterangan narasi berbantuan AI di deskripsi video.
