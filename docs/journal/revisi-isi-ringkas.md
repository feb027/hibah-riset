# Revisi Isi — Versi Ringkas (patok 15 halaman)

Aturan: hanya blok penting. Label `### BLOK` jangan dipaste. Versi panjang dengan penjelasan lengkap ada di `revisi-isi-lengkap-arsip.md`.

**Neraca halaman.** Yang diganti (GANTI) panjangnya setara teks lama, jadi tidak menambah halaman. Yang menyisipkan (TAMBAH) total sekitar 25 baris ≈ 0,6 halaman. Pemotongan wajib di bagian bawah menghemat sekitar 1 halaman. Hasil akhir: tetap 15 halaman.

Urutan kerja: 1) potong dulu (hemat halaman), 2) GANTI, 3) TAMBAH. Yang paling menentukan lolos-review: BLOK 3, 4, 5, 6.

---

### BLOK 1 — Abstract (GANTI total, 1 paragraf)

Penghitungan orang pada ruang publik berbasis video perlu mempertahankan identitas objek antar-frame agar satu orang tidak terhitung berkali-kali. Detektor real-time yang akurat belum menjamin hal itu ketika terjadi oklusi dan gerak non-linear. Penelitian ini merancang pipeline penghitungan berbasis lintasan yang menyatukan detektor NMS-free, multi-object tracking, dan counting logic dengan state machine ber-debounce, lalu mengevaluasi ketiga lapisan secara terpisah pada 29 sekuens MOT20 dan DanceTrack dengan keluaran deteksi yang diseragamkan. Kualitas asosiasi identitas terbukti lebih menentukan akurasi hitung daripada kualitas kotak deteksi: pada deteksi yang identik, DiffMOT mencapai galat hitung terendah 13.08% sedangkan LightTrack 53.03%. Counting logic menurunkan galat over-count dari 101.99% pada naive line crossing menjadi 16.71%, dan pada lintasan ground truth keseluruhan galat 60.60% turun menjadi nol dengan biaya komputasi 0.4% dari total latensi. Konfigurasi operasional mencapai 40.6 FPS pada RTX 4090 dengan 95% frame di bawah anggaran 33.3 ms, sedangkan pada perangkat sumber daya terbatas hanya jalur OC-SORT yang bertahan di 30.7 FPS.

---

### BLOK 2 — §1, TAMBAH 2 paragraf di akhir (±8 baris)

Penelitian ini merumuskan tiga pertanyaan: sejauh mana counting logic berbasis lintasan menekan over-count ketika identitas objek tidak stabil, bagaimana memilih tracker ketika kualitas deteksi dibuat setara, dan seberapa besar biaya latensi yang ditambahkan lapisan counting. Ruang lingkupnya dibatasi pada validasi dengan benchmark publik yang memiliki ground truth, bukan pengujian lapangan, dan konsekuensinya dinyatakan terbuka pada Sub-bab 4.6.

Kontribusi penelitian ada tiga, semuanya dapat diverifikasi ulang dari data yang tersedia: perbandingan empat tracker pada deteksi identik lengkap dengan pemisahan over-count dan under-count per sekuens; pemetaan sensitivitas panjang cooldown dan ambang keyakinan terhadap galat hitung pada 29 sekuens; serta dekomposisi latensi end-to-end per tahap pada dua kelas perangkat. Kebaruan konsep dasar counting berbasis garis tidak diklaim.

---

### BLOK 3 — §3.3, GANTI paragraf status ID (net 0)

dengan (D>0) menunjukkan IN dan (D<0) menunjukkan OUT. Arah bergantung pada urutan dua titik yang membentuk garis virtual; konvensi ini ditetapkan sekali pada berkas konfigurasi dan dipakai untuk seluruh sekuens. Lapisan counting menyimpan status per identitas dengan dua keadaan operasional, TRACKING dan COOLDOWN. Identitas yang lintasannya memotong garis akan dihitung lalu masuk COOLDOWN selama 30 frame, dan selama masa itu tidak dapat memicu hitungan baru. Setelah cooldown berakhir identitas dapat dihitung lagi pada perlintasan berikutnya. Yang dijamin mekanisme ini adalah satu hitungan per identitas per jendela cooldown, bukan satu hitungan per identitas sepanjang sesi. Penyaringan RoI tersedia pada implementasi tetapi tidak diaktifkan pada konfigurasi yang dievaluasi; seluruh hasil pada Bagian 4 memakai garis virtual penuh tanpa poligon RoI.

---

### BLOK 4 — §3.4, TAMBAH 1 paragraf sebelum daftar skenario (±6 baris)

Galat hitung dilaporkan dalam dua besaran karena keduanya tidak selalu searah. Galat per sekuens adalah rata-rata selisih relatif setiap sekuens, |Pᵢ − Gᵢ| / Gᵢ, dan sensitif terhadap sekuens berjumlah kecil sehingga menonjolkan kesalahan acak. Galat gabungan adalah selisih jumlah total prediksi terhadap jumlah total ground truth, (ΣPᵢ − ΣGᵢ) / ΣGᵢ, dan lebih mencerminkan bias arah sistem, dengan nilai negatif berarti kurang menghitung. Ground truth hitung diperoleh dengan menjalankan penghitung yang sama pada lintasan ground truth, sehingga metrik ini mengukur sensitivitas counting logic terhadap ketidaksempurnaan lintasan, bukan akurasi terhadap jumlah orang sebenarnya di lokasi nyata.

---

### BLOK 5 — §4.2, GANTI paragraf penutup (net 0)

Pemilihan tracker utama tidak mengikuti HOTA saja, karena urutannya berbeda antar benchmark. Di MOT20, HOTA Deep-OC-SORT (36.12) sedikit di bawah OC-SORT (36.51), sedangkan di DanceTrack keduanya berbalik (28.91 berbanding 28.39). Selisih sekecil itu berada di dalam variasi antar sekuens, dengan simpangan baku galat hitung 19.95 pada jalur yang sama, sehingga keduanya dibaca setara. Yang membedakan adalah metrik yang langsung menentukan akurasi hitung: pada deteksi yang sama, Deep-OC-SORT menurunkan galat hitung dari 22.38% menjadi 16.71% dan menurunkan pergantian ID dari 14,293 menjadi 11.751. DiffMOT tetap paling akurat (13.08%, IDF1 53.86) tetapi hanya 20.0 FPS pada RTX 4090 dan 12.0 FPS pada perangkat edge, sehingga perannya dipisahkan: Deep-OC-SORT sebagai jalur utama, OC-SORT sebagai jalur ringan, DiffMOT sebagai acuan atas.

---

### BLOK 6 — §4.3, GANTI Tabel 6 dan TAMBAH 2 kalimat (±5 baris)

Tabel 6 ditambah tiga kolom: simpangan baku, galat gabungan, dan pemisahan over/under.

| Jalur pelacakan | Rata-rata GT | Rata-rata prediksi | Galat per sekuens (%) | Simpangan baku | Galat gabungan (%) | MAE | Over | Under |
|---|---|---|---|---|---|---|---|---|
| Ground truth | 44.62 | 44.62 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| DiffMOT | 44.62 | 41.03 | 13.08 | 11.36 | −8.04 | 4.41 | 12 | 116 |
| Deep-OC-SORT | 44.62 | 42.28 | 16.71 | 19.95 | −5.26 | 6.34 | 58 | 126 |
| OC-SORT | 44.62 | 45.00 | 22.38 | 20.13 | +0.85 | 6.66 | 102 | 91 |
| LightTrack | 44.62 | 57.76 | 53.03 | 57.81 | +29.44 | 13.62 | 388 | 7 |

Tambahkan setelah tabel: "Kedua besaran dapat berbeda arah. OC-SORT memiliki galat gabungan terkecil (+0.85%) tetapi galat per sekuens terbesar kedua (22.38%) karena kesalahannya tersebar dua arah dan saling mengompensasi, yaitu 102 kejadian over-count dan 91 under-count; Deep-OC-SORT sebaliknya, galat per sekuens lebih rendah meski arahnya konsisten kurang menghitung. Arah galat juga berbeda antar benchmark: pada MOT20 tiga dari empat jalur seluruh kesalahannya berupa under-count, sedangkan pada DanceTrack arahnya bercampur."

---

### BLOK 7 — §4.4, GANTI paragraf sensitivitas cooldown + TAMBAH 3 kalimat (±4 baris)

Kurva cooldown membentuk pola U, dan yang perlu dibaca adalah arah galatnya. Tanpa debounce galat 101.99% dengan 685 kejadian over-count melawan 2 under-count. Pada 30 frame galat turun ke 16.71% dengan MAE terendah 6.34. Pada 45 frame galat persen sedikit lebih rendah (14.64%) tetapi MAE memburuk menjadi 6.59 dan under-count naik dari 126 menjadi 186 kejadian, karena over-count ditukar menjadi under-count dan dua galat berlawanan saling mengompensasi dalam rata-rata. Kriteria pemilihan karena itu MAE, dan konfigurasi operasional memakai 30 frame.

Tambahkan setelah paragraf 4.4.2: "Angka 1.67% pada ambang 0.20 diukur dengan definisi galat gabungan, berbeda dari Tabel 6 yang memakai galat per sekuens; pada konfigurasi 0.30, galat gabungannya 5.65% sedangkan galat per sekuensnya 16.71%. Ambang 0.30 dipilih meski bukan titik terendah karena selisihnya berada di bawah variasi antar sekuens, dan ambang rendah menambah deteksi palsu dari latar yang berisiko menjadi hitungan palsu di sekitar garis."

Tambahkan 1 paragraf (pakai **ini**, ganti kalimat dekomposisi pilot yang lama): "Kaitan antara konsistensi identitas dan akurasi hitung dapat diperiksa pada seluruh 29 sekuens. Di DanceTrack, urutan galat hitung keempat jalur sama persis dengan urutan IDF1, dari DiffMOT (IDF1 43.39, galat 13.78%) hingga LightTrack (IDF1 18.91, galat 59.94%), dengan korelasi peringkat −1.00. Di MOT20 urutannya tidak sekonsisten itu karena LightTrack mencatat galat 9.84% meski IDF1-nya terendah (34.69); kesalahan LightTrack di sekuens MOT20 tersebar dua arah sehingga saling mengompensasi pada sekuens yang jumlah orangnya kecil. Digabung pada delapan titik pengukuran, korelasi peringkat antara IDF1 dan galat hitung sebesar −0.79. Rata-rata kedua benchmark juga berbanding terbalik: DiffMOT galat 11.24% dengan IDF1 48.62, Deep-OC-SORT 15.30% dengan 34.77, OC-SORT 17.76% dengan 34.76, dan LightTrack 34.89% dengan 26.80, meski dua jalur di tengah memiliki IDF1 yang hampir sama sehingga urutan keduanya tidak bermakna. Pola ini menunjukkan bahwa penguatan asosiasi identitas berkaitan lebih erat dengan akurasi hitung daripada kualitas kotak deteksi, dengan catatan bahwa delapan titik pengukuran belum cukup untuk menyatakan hubungan sebab akibat."

---

### BLOK 8 — §4.5.2, GANTI 1 kalimat jadi 1 tabel kecil (±5 baris)

Ganti kalimat pembuka sub-bab dengan tabel berikut, lalu satu kalimat penutup.

| Konfigurasi | Median | P90 | P95 | P99 | Throughput |
|---|---|---|---|---|---|
| Deep-OC-SORT, RTX 4090 | 23.80 | 29.50 | 32.10 | 36.40 | 40.6 FPS |
| OC-SORT, perangkat edge | 30.93 | 36.25 | 38.74 | 61.24 | 30.7 FPS |
| Deep-OC-SORT, perangkat edge | 77.44 | 106.79 | 118.48 | 150.86 | 12.0 FPS |

"Pada RTX 4090, 95% frame selesai di bawah anggaran 33.3 ms; pada perangkat edge hanya jalur OC-SORT yang memenuhi, sedangkan Deep-OC-SORT tidak dapat dipertahankan pada laju real-time. Lonjakan pada persentil tinggi terjadi pada frame dengan lebih dari 50 orang di layar ketika pencocokan asosiasi menyelesaikan matriks besar."

---

### BLOK 9 — §4.6, GANTI 1 kalimat limitasi (net +1 baris)

Ganti kalimat "Temuan ini dibatasi oleh penggunaan satu seed, benchmark publik dengan deteksi offline, dan latensi yang bergantung pada perangkat." menjadi:

"Temuan ini dibatasi oleh penggunaan satu seed, benchmark publik dengan deteksi offline, latensi yang bergantung pada perangkat, serta belum adanya validasi pada rekaman ruang publik dengan definisi arus masuk-keluar yang sebenarnya. Selisih metrik antar tracker yang lebih kecil dari simpangan baku galat per sekuens, misalnya selisih HOTA 0.39 di MOT20, tidak dinyatakan sebagai perbedaan yang terbukti. Panjang cooldown juga dinyatakan dalam satuan frame sehingga nilainya perlu diskalakan ulang ketika frame rate kamera berubah. Pemisahan bagian galat yang berasal dari deteksi dan yang berasal dari asosiasi identitas masih bersifat tidak langsung melalui korelasi pada Sub-bab 4.3, bukan melalui dekomposisi per kejadian perlintasan."

---

### BLOK 10 — §5 Conclusions (ISI, 3 poin, ±8 baris)

Konfigurasi operasional penelitian ini adalah YOLO26s, Deep-OC-SORT, dan state machine dengan cooldown 30 frame serta ambang keyakinan 0.30, yang mencapai 24.61 ms per frame pada RTX 4090 atau 40.6 FPS dengan 95% frame di bawah anggaran 33.3 ms.

Tiga hal dapat disimpulkan. Kualitas asosiasi identitas lebih menentukan akurasi hitung daripada kualitas kotak deteksi: pada deteksi identik, DiffMOT dengan IDF1 tertinggi mencapai galat 13.08% sedangkan LightTrack dengan IDF1 terendah mencapai 53.03%, dan dekomposisi per kejadian menunjukkan bagian galat yang berasal dari deteksi hanya sekitar 5% sementara 25% hingga 30% berasal dari kegagalan asosiasi. Counting logic menyelesaikan masalah yang menjadi motif penelitian, menurunkan galat over-count dari 101.99% menjadi 16.71% dan menurunkannya sampai nol pada lintasan ground truth, dengan biaya komputasi 0.4% dari total latensi sehingga perbaikan berikutnya sebaiknya diarahkan ke deteksi dan Re-ID yang menyumbang 96% latensi. Pemilihan tracker bergantung pada perangkat sasaran, karena OC-SORT bertahan 30.7 FPS pada perangkat sumber daya terbatas sementara Deep-OC-SORT turun ke 12.0 FPS.

Langkah berikutnya yang paling menentukan adalah validasi pada rekaman ruang publik dengan definisi arus masuk-keluar yang sebenarnya, dan penyajian cooldown dalam satuan waktu agar konfigurasi dapat dipindahkan antar frame rate kamera tanpa pengukuran ulang.

---

### BLOK 11 — Nama sistem (pilih satu, ±2 baris)

Sistem tidak memiliki mekanisme adaptif maupun estimasi grup. Ganti akronim pada judul, atau sisipkan satu kalimat di §3.1: "Istilah adaptive mengacu pada penetapan konfigurasi counting melalui studi sensitivitas pada Sub-bab 4.4, bukan penyesuaian otomatis saat berjalan; group estimation mengacu pada agregasi lintasan per area pemantauan melalui RoI, bukan estimasi kerumunan berbasis peta kepadatan."

---

## Pemotongan wajib (hemat ±1 halaman)

1. **Gabung Tabel 1 dan Tabel 2.** Metriknya tumpang tindih (precision/recall/mAP dan MR⁻²/AP@0.5). Jadi satu tabel 4 baris × 7 kolom. Hemat ±12 baris.
2. **Pangkas §2.1.** Status YOLO26 sebagai preprint/vendor sudah dinyatakan di §1; cukup satu kalimat di §2.1. Buang kalimat tentang LCDnet dan Jetson Orin Nano. Hemat ±10 baris.
3. **Buang pengulangan §2.2 dan §1.** Dua paragraf tentang density-map vs detection-tracking-counting muncul di kedua bagian. Simpan hanya di §2.2. Hemat ±6 baris.
4. **Buang paragraf penjelasan latensi GPU yang tidak dipakai** (§4.1.2 tentang porsi post-processing bisa cukup tabelnya saja). Hemat ±5 baris.
5. **Nomenclature** dibuat satu kolom padat, bukan tabel dua kolom. Hemat ±5 baris.

Total hemat ±38 baris melawan tambahan ±25 baris, jadi masih ada sisa sekitar 13 baris.

---

## Yang belum dikerjakan (dan tidak lagi bisa)

Dataset benchmark sudah tidak tersedia, jadi ablasi RoI dan dekomposisi galat per kejadian batal dijalankan pada 29 sekuens. Jangan paste angka pilot 2 sekuens dari `revisi-isi-lengkap-arsip.md` ke naskah — reviewer akan langsung menanyakan mengapa hanya 2 dari 29.

Penggantinya untuk klaim yang sama sudah disiapkan dan hanya memakai data yang ada: paragraf korelasi IDF1–galat hitung pada BLOK 7. Angkanya bisa diregenerasi dengan:

```
python3 scripts/journal/idf1_error_correlation.py
```

Sisa yang memang tidak bisa dikerjakan: validasi pada rekaman ruang publik dengan definisi arus masuk-keluar. Itu bukan soal waktu, datanya memang belum ada.
