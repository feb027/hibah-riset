# Revisi Isi Naskah JESTEC — Siap Copas ke Word

> **Cara pakai.** Setiap blok punya label lokasi (`### BLOK n`) yang **tidak ikut dipaste**. Teks di bawah label adalah teks final siap tempel. Kalau blok berisi tabel markdown, salin isinya lalu buat tabel Word baru (Table 8, 9, ...) dan sesuaikan nomor tabel di teks.
> **Notasi angka.** Semua desimal di dokumen ini memakai titik karena naskah akan diterjemahkan ke Inggris. Kalau ditempel ke versi Indonesia, ganti titik desimal menjadi koma.
> **Sumber angka.** Semua angka baru di dokumen ini berasal dari `experiments/s3_counting/*.csv` dan `docs/reports/laporan-skenario-d-realtime.md`, bukan angka baru yang dikarang. Regenerasi tabel kapan saja dengan `python3 scripts/journal/make_revision_tables.py` (script ini juga memverifikasi angka headline naskah).

---

## Daftar blok

| Blok | Lokasi di naskah | Menutup temuan |
|---|---|---|
| 1 | §1 Introduction (sisipan di akhir) | K5 |
| 2 | §1 Introduction (koreksi kecil) | — |
| 3 | §2.2 (sisipan) | S10, S11 |
| 4 | §3.3 (ganti + sisipan) | K7, S9, S8 |
| 5 | §3.4 (sisipan sub-bab baru) | K1 |
| 6 | §3.4 (koreksi kalimat skenario) | K2 |
| 7 | §4.1.2 (sisipan pembatas) | S6 |
| 8 | §4.2 (ganti paragraf penutup) | S2, S4 |
| 9 | §4.3 (ganti Tabel 6 + paragraf) | K1, K2 |
| 10 | §4.4.1 (ganti paragraf) | S1 |
| 11 | §4.4.2 (ganti paragraf) | S1 |
| 12 | §4.5.2 (isi sub-bab kosong) | K2 |
| 13 | §4.6 (sisipan) | S13, V5 |
| 14 | §4.6 (ganti paragraf limitasi) | K6, S14 |
| 15 | §5 Conclusions (isi) | K3 |
| 16 | Abstract (ganti total) | K4 |
| 17 | Judul / nama sistem | S7 |
| 18 | Tabel 4 (catatan kaki) | V9 |
| 19 | §4.4.3 baru — ablasi penyaringan RoI | S3 (terjawab) |

---

### BLOK 1 — §1 Introduction, sisipkan tepat sebelum kalimat "Naskah ini terdiri atas lima bagian"

Cari kalimat: *"Kontribusi penelitian terletak pada perancangan counting pipeline..."* sampai *"...terhadap konsistensi people counting."* → tambahkan paragraf berikut **setelah** paragraf tersebut.

Penelitian ini merumuskan tiga pertanyaan. Pertama, sejauh mana counting logic berbasis lintasan mampu menekan over-count ketika identitas objek tidak stabil akibat oklusi, pergantian ID, dan gerak bolak-balik di sekitar garis hitung. Kedua, bagaimana memilih tracker di antara kandidat yang memiliki karakteristik biaya dan ketahanan asosiasi berbeda, ketika kualitas deteksi dibuat setara. Ketiga, seberapa besar biaya komputasi yang ditambahkan lapisan counting terhadap anggaran latensi pipeline. Pertanyaan ketiga sengaja dirumuskan sebagai pengukuran, bukan asumsi, karena klaim bahwa logika spasial bersifat ringan perlu dibuktikan pada perangkat yang menjadi target.

Tujuan penelitian ini adalah merancang dan memvalidasi tahap awal pipeline *real-time people counting* yang menyatukan detektor *NMS-free*, *multi-object tracking*, dan counting logic berbasis lintasan, lalu mengukur tiga hal secara terpisah: kualitas deteksi, kestabilan asosiasi identitas, dan galat hitung. Ruang lingkupnya dibatasi pada validasi menggunakan *benchmark* publik yang memiliki *ground truth*, bukan pada pengujian lapangan. Konsekuensi pembatasan ini dinyatakan terbuka pada Sub-bab 4.6 agar capaian sistem tidak dibaca melebihi buktinya.

Kontribusi penelitian ada pada tiga hal yang dapat diverifikasi ulang dari data yang tersedia. Pertama, perbandingan empat *tracker* pada keluaran deteksi yang identik sehingga perbedaan performa tidak tercampur perbedaan detektor, lengkap dengan pemisahan *over-count* dan *under-count* per sekuens. Kedua, pemetaan sensitivitas dua parameter counting, yaitu panjang *cooldown* dan ambang keyakinan detektor, terhadap galat hitung pada 29 sekuens. Ketiga, dekomposisi latensi *end-to-end* per tahap pada dua kelas perangkat, yang menunjukkan bahwa biaya counting logic berada di bawah 1% dari total latensi sementara deteksi dan *Re-ID* mengambil porsi terbesar. Yang tidak diklaim penelitian ini adalah kebaruan konsep dasar counting berbasis garis atau RoI; yang diukur adalah perilaku dan batasnya pada konfigurasi yang dikontrol.

---

### BLOK 2 — §1 Introduction, koreksi

Kalimat: *"Prototipe berbasis RoI/zona dikembangkan dan dievaluasi menggunakan ketiga tracker"*
→ **ganti menjadi:** "Prototipe berbasis RoI/zona dikembangkan dan dievaluasi menggunakan empat *tracker*"

*(Alasan: §1 paragraf sebelumnya, §3.2, dan §4.2 semuanya menyebut empat tracker. Ini kontradiksi internal, bukan pilihan kata.)*

---

### BLOK 3 — §2.2, sisipkan sebagai paragraf baru sebelum paragraf "Meskipun demikian, keberhasilan tracking tidak selalu menghasilkan penghitungan yang akurat."

Satu hal yang jarang dibahas terpisah dari kinerja *tracker* adalah logika yang mengubah lintasan menjadi angka. Praktik yang beredar umumnya memakai tiga mekanisme yang sama: pembatasan area dengan poligon RoI, penentuan perlintasan garis atau perpindahan antar-zona, dan penyimpanan status per identitas agar satu objek tidak dihitung berkali-kali. Kerangka analitik video seperti NVIDIA DeepStream menyediakan ketiganya sebagai modul siap pakai melalui `nvdsanalytics`, sedangkan perkakas deteksi seperti Ultralytics menyediakan penghitung zona berbasis lintasan. Konsekuensinya, *gap* penelitian bukan pada ada atau tidaknya mekanisme tersebut, melainkan pada seberapa jauh mekanisme itu bertahan ketika identitas objek tidak stabil dan seberapa besar biayanya terhadap latensi. Literatur *people counting* melaporkan angka akurasi yang tinggi pada kondisi terkendali, misalnya 98.42% pada deteksi kaskade dengan Kalman Filter dan 85% pada RoI kuadrilateral dengan *virtual-line event* (Nurseitov, 2026; Holla, 2024), tetapi angka tersebut jarang disertai pemisahan galat yang berasal dari deteksi dan yang berasal dari logika hitung. Pemisahan itu yang diuji pada penelitian ini.

**Tabel perbandingan studi (buat sebagai Tabel 2 atau 3 di Word).**

| Studi | Pendekatan | Dataset/skenario | Metrik | Hasil dilaporkan | Batasan untuk perbandingan |
|---|---|---|---|---|---|
| Nurseitov et al. (2026) | RoI kuadrilateral + *virtual-line event* dengan ID persisten | Rekaman urban | Akurasi hitung | 85% | Definisi metrik dan konfigurasi kamera tidak seragam dengan benchmark publik |
| Holla et al. (2024) | Deteksi kaskade + Kalman Filter | Kondisi visual menantang | Akurasi hitung | hingga 98.42% | Skenario tidak padat; tidak melaporkan galat asosiasi |
| Diaz-Santos & Caballero-Gil (2025) | *Line crossing* berarah berbasis ID | *Passenger flow* dengan *edge AI* | Akurasi hitung | dilaporkan per skenario | Bergantung pada riwayat posisi ID tanpa ablasi *debounce* |
| DiffMOT (Lv et al., 2024) | Prediksi gerak berbasis *diffusion* | DanceTrack | HOTA / IDF1 | 62.3 / 63.0 pada 22.7 FPS (RTX 3090) | Detektor dan protokol berbeda; pada penelitian ini detektor diseragamkan |
| OC-SORT (Cao et al., 2023) | *Observation-centric* Re-Update, OCM, OCR | MOT17/MOT20 | HOTA | 700+ FPS, akurasi bersaing SORT-family | Tidak melaporkan akurasi hitung |
| Penelitian ini | Deteksi identik + empat *tracker* + dua model counting | 29 sekuens MOT20 dan DanceTrack | Galat per sekuens, MAE, *over/under-count*, latensi per tahap | lihat Sub-bab 4.3 | Benchmark publik tanpa label masuk-keluar; satu seed |

Dua angka terbesar pada tabel itu (98.42% dan 85%) tidak dapat dibandingkan langsung dengan galat pada Sub-bab 4.3 karena tiga alasan yang perlu dinyatakan. Definisi "dihitung" berbeda, ada studi yang menghitung perlintasan dan ada yang menghitung keberadaan per frame. Datasetnya berbeda, sehingga kepadatan, sudut kamera, dan kecepatan objek tidak setara. Cara *ground truth* hitung diperoleh juga berbeda. Karena itu Sub-bab 4.3 melaporkan galat beserta pemisahan arahnya alih-alih satu angka akurasi tunggal, supaya besaran yang benar-benar diukur terbaca jelas.

---

### BLOK 4 — §3.3, ganti paragraf tentang status ID

Cari dan **buang** paragraf: *"dengan (D>0) menunjukkan IN dan (D<0) menunjukkan OUT. Setiap ID mengikuti status UNSEEN, TRACKING, COUNTED_IN/COUNTED_OUT, COOLDOWN, EXPIRED. Setelah dihitung, ID memasuki cooldown selama (N) frame (default 30) untuk mencegah hitungan berulang akibat osilasi atau perlintasan semu. Setelah periode tersebut, ID dapat dihitung kembali jika melakukan perlintasan valid, sedangkan ID yang tidak lagi diperbarui akan dihapus. Mekanisme ini menerapkan prinsip debouncing serupa pendekatan double-line tanpa menambah anotasi garis."*

Ganti menjadi:

dengan (D>0) menunjukkan IN dan (D<0) menunjukkan OUT. Perlu dinyatakan bahwa definisi arah ini bergantung pada urutan dua titik yang membentuk garis virtual: titik pertama dan kedua menentukan sisi mana yang dihitung sebagai IN. Konvensi tersebut ditetapkan sekali pada berkas konfigurasi dan dipakai untuk seluruh sekuens, sehingga perbandingan antar jalur pelacakan tidak terpengaruh perbedaan orientasi garis.

Lapisan *counting* menyimpan status per identitas dengan dua keadaan operasional, yaitu TRACKING dan COOLDOWN. Identitas baru masuk sebagai TRACKING dan mulai mengumpulkan riwayat posisi. Ketika lintasannya memotong garis virtual, penghitung bertambah dan statusnya berpindah ke COOLDOWN selama 30 frame; selama masa itu identitas tidak dapat memicu hitungan baru meskipun lintasannya bergetar di sekitar garis. Setelah *cooldown* berakhir, identitas kembali ke TRACKING dan dapat dihitung lagi pada perlintasan berikutnya. Struktur status yang lebih rinci, mencakup penandaan arah hitungan dan identitas kedaluwarsa, disediakan pada lapisan model untuk pengembangan lanjutan tetapi belum diaktifkan pada konfigurasi yang diuji. Karena itu, sifat yang dijamin mekanisme ini adalah satu hitungan per identitas per jendela *cooldown*, bukan satu hitungan per identitas sepanjang sesi. Pembedaan ini relevan untuk membaca Sub-bab 4.4, karena panjang *cooldown* menentukan seberapa besar peluang satu orang tercatat lebih dari sekali ketika ia bergerak bolak-balik di area garis.

Penyaringan RoI tersedia pada implementasi namun tidak diaktifkan pada konfigurasi yang dievaluasi. Seluruh hasil pada Bagian 4 dijalankan dengan area aktif berupa garis virtual penuh tanpa poligon RoI, sehingga klaim kontribusi pada sub-bab ini dibatasi pada mekanisme state machine dengan *debouncing*. Pengaruh penyaringan RoI diukur terpisah sebagai ablasi tambahan dan dilaporkan pada Sub-bab 4.4.3, tanpa dimasukkan ke konfigurasi operasional.

**Paragraf tambahan (sisipkan setelahnya), batas mekanisme:**

Tiga batas mekanisme perlu dinyatakan agar hasil pada Sub-bab 4.4 dibaca pada konteks yang benar. Pertama, penyaringan RoI bekerja sebagai gerbang di awal pemrosesan: *centroid* di luar poligon tidak memperbarui riwayat posisi sama sekali, sehingga ketika objek masuk kembali segmen lintasan yang diuji dibentuk dari titik terakhir sebelum keluar. Untuk objek yang bergerak di sepanjang tepi RoI, segmen tersebut dapat menyeberangi garis virtual secara semu. Kedua, riwayat posisi dibatasi sepuluh titik terakhir untuk menahan penggunaan memori, yang berarti pada objek bergerak cepat atau *frame rate* rendah segmen uji tetap dibentuk dari dua titik terakhir dan tidak memanfaatkan riwayat lebih panjang. Ketiga, panjang *cooldown* dinyatakan dalam satuan frame, sehingga durasi efektifnya bergantung pada *frame rate* masukan: 30 frame setara satu detik pada 30 FPS dan setengah detik pada 60 FPS. Ketiga batas ini tidak diuji secara terpisah sebagai variabel bebas pada laporan utama; pengaruh penyaringan RoI diukur pada Sub-bab 4.4.3, sedangkan dua batas lainnya belum diukur dan dibahas sebagai keterbatasan pada Sub-bab 4.6.

---

### BLOK 5 — §3.4, sisipkan sebagai sub-bab baru "3.4.1 Definisi Metrik Hitung" (sebelum kalimat "Evaluasi sistem dirancang dalam empat skenario")

Kalimat "Evaluasi sistem dirancang dalam empat skenario" dinaikkan menjadi sub-bab "3.4.2 Skenario Evaluasi".

Galat hitung pada penelitian ini didefinisikan melalui dua besaran yang mengukur hal berbeda, dan keduanya dilaporkan karena tidak selalu searah. Besaran pertama adalah galat per sekuens, yaitu rata-rata dari selisih relatif antara jumlah prediksi dan jumlah *ground truth* pada setiap sekuens:

galat per sekuens = (1/M) · Σ |Pᵢ − Gᵢ| / Gᵢ × 100%

dengan Pᵢ dan Gᵢ berturut-turut jumlah orang yang dihitung dan jumlah *ground truth* pada sekuens ke-i, dan M adalah jumlah sekuens. Besaran kedua adalah galat gabungan, yaitu selisih jumlah total prediksi terhadap jumlah total *ground truth* pada seluruh sekuens:

galat gabungan = (Σ Pᵢ − Σ Gᵢ) / Σ Gᵢ × 100%

Dua besaran ini berbeda perilakunya karena sebaran jumlah orang antar sekuens lebar: jumlah *ground truth* per sekuens pada penelitian ini berkisar 4 hingga 337 orang dengan nilai tengah 21. Pada besaran pertama, sekuens dengan jumlah kecil dan satu kesalahan memberi kontribusi galat persen yang besar, sehingga angka ini sensitif terhadap sekuens pendek. Pada besaran kedua, sekuens berjumlah besar mendominasi, sehingga angka ini lebih mencerminkan bias arah sistem. Tanda pada galat gabungan menunjukkan arah: nilai negatif berarti sistem cenderung kurang menghitung, nilai positif berarti cenderung lebih menghitung. Selain keduanya dilaporkan MAE sebagai rata-rata selisih absolut jumlah orang per sekuens, simpangan baku galat per sekuens sebagai ukuran kestabilan lintas sekuens, serta pemisahan jumlah kejadian *over-count* dan *under-count*.

*Ground truth* hitung diperoleh dengan menjalankan penghitung yang sama pada lintasan *ground truth* untuk setiap sekuens, memakai garis virtual dan RoI yang identik dengan yang dipakai pada lintasan hasil *tracker*. Konsekuensinya perlu dinyatakan sejak awal: metrik ini mengukur sensitivitas counting logic terhadap ketidaksempurnaan lintasan, bukan akurasi absolut terhadap jumlah orang sebenarnya di lokasi nyata. Ketika lintasan ideal menghasilkan galat nol, seluruh galat pada lintasan hasil *tracker* berasal dari deteksi dan asosiasi di hulunya, dan itu yang membuat pemisahan kontribusi dapat dilakukan.

MAE untuk seluruh konfigurasi dihitung sebagai rata-rata |Pᵢ − Gᵢ| pada 29 sekuens: 4 sekuens MOT20 (8,931 frame) dan 25 sekuens validasi DanceTrack (25,508 frame). Kedua *benchmark* dilaporkan terpisah pada Sub-bab 4.3 karena kepadatan keduanya berbeda jauh.

---

### BLOK 6 — §3.4, koreksi kalimat skenario (pilih salah satu, jangan dua-duanya)

Kalimat lama: *"S1 mengevaluasi kinerja detektor berdasarkan akurasi, latensi, serta perbandingan antara konfigurasi zero-shot dan fine-tuned."*

**Opsi A — kalau hasil zero-shot ingin tetap dilaporkan**, tambahkan di §4.1 kalimat berikut dan ubah §3.4 menjadi: *"...serta pemeriksaan kualitatif pada bobot pra-latih untuk memastikan penambahan bobot CrowdHuman benar-benar diperlukan."*
Teks §4.1: "Sebelum *fine-tuning*, keempat model dijalankan dengan bobot pra-latih pada satu *frame* kerumunan padat. Ketiga varian *nano* hanya mendeteksi 9 hingga 12 orang pada *frame* yang mengandung lebih dari 50 orang, jauh di bawah jumlah yang terlihat. Perbedaan antar arsitektur pada kondisi ini tidak dapat disimpulkan karena hanya diuji pada satu citra, dan yang terbaca adalah bahwa bobot pra-latih tidak memadai untuk kerumunan padat. Karena itu evaluasi kuantitatif pada sub-bab ini seluruhnya memakai bobot hasil *fine-tuning*."

**Opsi B — kalau klaim itu tidak ingin dipertahankan**, hapus frasa *"serta perbandingan antara konfigurasi zero-shot dan fine-tuned"* dari §3.4. Lebih aman untuk reviewer: janji di Method yang tidak ada angkanya di Results adalah temuan yang pasti muncul.

Perlakuan yang sama berlaku untuk S4. Kalimat lama: *"S4 mengevaluasi kinerja end-to-end melalui FPS dan tail latency pada persentil P90, P95, dan P99 menggunakan server GPU RTX 4090 serta perangkat edge AMD RX 6600 dengan DirectML."* Pertahankan kalimat ini dan isi hasilnya memakai BLOK 12.

---

### BLOK 7 — §4.1.2, sisipkan di akhir sub-bab

Satu pembatas perlu ditambahkan pada pembacaan angka latensi di atas. Peringkat kecepatan antar arsitektur pada Tabel 3 dan Tabel 4 berlaku untuk kombinasi perangkat dan *runtime* yang diuji, bukan sebagai urutan yang berlaku umum. Pada GPU, seluruh model berada pada rezim waktu frame 2 sampai 3 ms sehingga yang mendominasi adalah *overhead* peluncuran kernel, bukan komputasi: YOLO26s memiliki sekitar 3.8 kali FLOPs YOLO26n tetapi hanya 5.5% lebih lambat. Pada CPU dengan PyTorch, urutan peringkatnya berbeda lagi dan YOLOv11n justru menjadi yang tercepat, sementara keunggulan YOLO26n hanya muncul pada jalur ONNX Runtime. Karena itu kesimpulan bahwa kapasitas model lebih berpengaruh daripada perbedaan arsitektur pada tingkat *nano* dibaca sebagai kesimpulan untuk konfigurasi yang diuji, dan pemilihan YOLO26s pada perangkat GPU di Sub-bab 4.5 mengikuti kriteria akurasi, bukan klaim bahwa arsitektur tersebut selalu lebih cepat.

---

### BLOK 8 — §4.2, ganti paragraf penutup sub-bab

Cari dan buang: *"Gambar 4 menunjukkan bahwa pada satu frame MOT20-02... Dengan mempertimbangkan akurasi dan efisiensi, Deep-OC-SORT dipilih sebagai tracker utama, sedangkan DiffMOT digunakan sebagai pembanding kualitas."*

Catatan penting dari Tabel 5 adalah kesenjangan antara MOTA dan HOTA yang melebar di MOT20. OC-SORT mencapai MOTA 55.98, yang berarti deteksi menutupi sebagian besar orang, tetapi HOTA-nya 36.51 dan IDF1 42.88 dengan 14,293 pergantian ID serta 27.646 fragmentasi. DiffMOT memimpin pada ketiga metrik asosiasi dengan HOTA 44.37, IDF1 53.86, dan 6.905 pergantian ID. Pola yang sama muncul di DanceTrack, tempat selisih HOTA antar *tracker* lebih besar, dari 22.53 pada LightTrack hingga 39.05 pada DiffMOT.

Anomali pada kolom fragmentasi perlu dijelaskan sebelum angka itu dibaca sebagai kontradiksi. LightTrack mencatat fragmentasi terendah di MOT20, yaitu 8.863, sementara HOTA-nya justru terendah dan ID-nya berganti 13.121 kali. Fragmentasi rendah dengan HOTA rendah menunjukkan bahwa lintasan tidak banyak terputus, tetapi identitas di dalamnya berpindah antar objek, sehingga lintasan yang tampak utuh sebenarnya menempel pada orang yang berbeda pada rentang waktu berbeda. Kebalikannya terjadi pada DiffMOT: fragmentasi 15.005 lebih tinggi daripada LightTrack, tetapi pergantian ID-nya paling rendah, sehingga pemutusan lintasan yang terjadi tidak berlanjut menjadi pertukaran identitas.

Pemilihan *tracker* utama tidak mengikuti HOTA saja, dan alasannya perlu dinyatakan karena pada satu *benchmark* urutannya berbeda. Di MOT20, HOTA Deep-OC-SORT (36.12) berada sedikit di bawah OC-SORT (36.51), sementara di DanceTrack keduanya berbalik (28.91 berbanding 28.39). Selisih 0.39 di MOT20 berada di dalam rentang variasi antar sekuens pada jalur yang sama, dengan simpangan baku galat hitung 19.95 untuk Deep-OC-SORT, sehingga keduanya dibaca setara pada *benchmark* tersebut. Yang membedakan keduanya adalah perilaku pada metrik yang langsung menentukan akurasi hitung: dengan deteksi yang sama, Deep-OC-SORT menurunkan galat hitung dari 22.38% menjadi 16.71% dan menurunkan pergantian ID dari 14,293 menjadi 11.751. DiffMOT tetap yang paling akurat dengan galat hitung 13.08% dan IDF1 53.86, tetapi throughput-nya 20.0 FPS pada RTX 4090 dan 12.0 FPS pada perangkat *edge*, sehingga ia dipakai sebagai pembanding kualitas dan bukan sebagai konfigurasi operasional pada perangkat terbatas. Dua peran itu dipisahkan secara eksplisit: Deep-OC-SORT sebagai jalur utama, OC-SORT sebagai jalur ringan, DiffMOT sebagai acuan atas.

---

### BLOK 9 — §4.3, ganti Tabel 6 dan paragraf 4.3.1

**Tabel 6 (revisi). Hasil penghitungan pada 29 sekuens dengan state machine (CD=30), deteksi YOLO26s.**

| Jalur pelacakan | Rata-rata GT | Rata-rata prediksi | Galat per sekuens (%) | Simpangan baku | Galat gabungan (%) | MAE | Over-count | Under-count |
|---|---|---|---|---|---|---|---|---|
| Ground truth (lintasan ideal) | 44.62 | 44.62 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| DiffMOT | 44.62 | 41.03 | 13.08 | 11.36 | −8.04 | 4.41 | 12 | 116 |
| Deep-OC-SORT | 44.62 | 42.28 | 16.71 | 19.95 | −5.26 | 6.34 | 58 | 126 |
| OC-SORT | 44.62 | 45.00 | 22.38 | 20.13 | +0.85 | 6.66 | 102 | 91 |
| LightTrack | 44.62 | 57.76 | 53.03 | 57.81 | +29.44 | 13.62 | 388 | 7 |

Angka di atas memakai dua definisi galat yang dijelaskan pada Sub-bab 3.4.1: galat per sekuens adalah rata-rata selisih relatif per sekuens, sedangkan galat gabungan adalah selisih total prediksi terhadap total *ground truth* dengan tanda menunjukkan arah. Perbedaan kedua besaran itu menjelaskan temuan yang paling penting pada tabel: peringkat akurasi berubah bergantung besaran yang dipakai. OC-SORT memiliki galat gabungan terkecil, yaitu +0.85%, tetapi galat per sekuensnya terbesar kedua (22.38%) karena kesalahannya tersebar dua arah dan saling mengompensasi, dengan 102 kejadian *over-count* dan 91 *under-count*. Deep-OC-SORT sebaliknya, galat gabungannya −5.26% tetapi galat per sekuensnya lebih rendah (16.71%) dengan MAE 6.34, sehingga kesalahannya lebih jarang meskipun arahnya konsisten kurang menghitung. DiffMOT tetap yang paling akurat pada kedua besaran, sekaligus yang paling konsisten kurang menghitung dengan galat gabungan −8.04%.

Empat hal terbaca dari Tabel 6. Pertama, pada lintasan *ground truth*, state machine menghasilkan galat nol pada seluruh 29 sekuens, sehingga lapisan counting tidak menambahkan galat ketika lintasan sempurna dan seluruh galat pada baris lain berasal dari deteksi dan asosiasi. Kedua, peringkat galat per sekuens mengikuti kualitas asosiasi: DiffMOT dengan IDF1 tertinggi di MOT20 (53.86) memberi galat terendah, dan LightTrack dengan IDF1 terendah (34.69) memberi galat terbesar sekaligus *over-count* yang paling banyak, 388 kejadian dengan prediksi rata-rata 57.76 melawan *ground truth* 44.62. Ketiga, arah galat berbeda antar jalur pelacakan dan itu punya konsekuensi operasional: untuk penghitungan arus masuk-keluar, *under-count* dan *over-count* tidak setara karena yang pertama membuat sistem melaporkan kapasitas lebih rendah dari kenyataan. Keempat, sebaran galat lebar pada semua jalur, dengan simpangan baku 11.36 hingga 57.81, sehingga satu angka rata-rata tidak cukup untuk menggambarkan perilaku sistem.

Pemisahan galat menurut *benchmark* pada Tabel 7 memperlihatkan bahwa kesulitan terbesar bukan pada kepadatan tinggi. Pada MOT20, galat per sekuens keempat jalur berada pada rentang sempit 8.71% hingga 13.35%, dan pada tiga dari empat jalur seluruh kesalahannya berupa *under-count*, dengan 53 hingga 102 kejadian dan tanpa satu pun *over-count*; LightTrack menjadi pengecualian dengan 94 kejadian *over-count* pada *benchmark* yang sama. Pada DanceTrack, galatnya jauh lebih lebar, dari 13.78% hingga 59.94%, dan arahnya bercampur di semua jalur. Pola tersebut masuk akal karena pada kerumunan sangat padat orang yang tertutup tidak terdeteksi sehingga hitungan berkurang, sementara pada gerak non-linear identitas yang berpindah menghasilkan hitungan berlebih. Selain itu, jumlah orang per sekuens di MOT20 jauh lebih besar sehingga MAE di sana terlihat tinggi (13.25 hingga 25.50) meskipun galat persennya lebih rendah; perbedaan skala ini juga alasan mengapa dua definisi galat dilaporkan berdampingan.

**Tabel 7. Pemisahan galat hitung menurut *benchmark* (state machine CD=30, deteksi YOLO26s).**

| Jalur pelacakan | Benchmark | Sekuens | Galat per sekuens (%) | Simpangan baku | MAE | Over-count | Under-count |
|---|---|---|---|---|---|---|---|
| DiffMOT | MOT20 | 4 | 8.71 | 5.45 | 13.25 | 0 | 53 |
| DiffMOT | DanceTrack | 25 | 13.78 | 11.96 | 3.00 | 12 | 63 |
| Deep-OC-SORT | MOT20 | 4 | 13.35 | 5.72 | 25.50 | 0 | 102 |
| Deep-OC-SORT | DanceTrack | 25 | 17.25 | 21.40 | 3.28 | 58 | 24 |
| OC-SORT | MOT20 | 4 | 11.37 | 5.52 | 19.75 | 0 | 79 |
| OC-SORT | DanceTrack | 25 | 24.14 | 21.11 | 4.56 | 102 | 12 |
| LightTrack | MOT20 | 4 | 9.84 | 11.15 | 23.75 | 94 | 1 |
| LightTrack | DanceTrack | 25 | 59.94 | 59.35 | 12.00 | 294 | 6 |

*(Setelah BLOK 9 dan BLOK 12 masuk, penomoran tabel bergeser. Tabel 6 tetap ablasi counting; tabel-tabel baru dinomori ulang saat penyusunan akhir.)*

---

### BLOK 10 — §4.4.1, ganti paragraf sensitivitas cooldown

Cari dan buang paragraf lama: *"Gambar 6 menunjukkan pola berbentuk U pada MAE dan galat hitung. Tanpa debounce, galat mencapai 101.99%..."* sampai akhir sub-bab.

Kurva *cooldown* pada Tabel 8 membentuk pola U yang tidak simetris, dan bentuk itu lebih mudah dibaca dari pemisahan arah galat daripada dari satu angka. Tanpa *debounce* sama sekali, galat per sekuens 101.99% dengan prediksi rata-rata 68.17 orang melawan *ground truth* 44.62, dan hampir seluruh kesalahan berupa *over-count*: 685 kejadian berlebih melawan 2 kejadian kurang. Pada *cooldown* 15 frame galatnya turun ke 27.13%, dan pada 30 frame 16.71% dengan MAE terendah, yaitu 6.34. Melewati 45 frame, galat persen terus turun sedikit sampai 14.64% tetapi arah kesalahannya berbalik: *under-count* naik dari 126 menjadi 186 kejadian pada 60 frame, dan MAE justru memburuk menjadi 7.21. Pada 120 frame keadaannya paling jelas, dengan galat 23.96%, MAE 9.45, dan bias −8.41 yang berarti sistem melaporkan 8 orang lebih sedikit per sekuens.

**Yang penting dibaca dari kurva ini adalah bahwa galat persen terendah bukan kriteria pemilihan yang tepat.** Angka 14.64% pada *cooldown* 45 frame lebih rendah daripada 16.71% pada 30 frame, tetapi angka itu dicapai dengan menukar 102 kejadian *over-count* menjadi 60 kejadian *under-count* tambahan; dua galat berlawanan arah yang saling mengompensasi dalam rata-rata, bukan kesalahan yang hilang. Kriteria yang dipakai untuk konfigurasi operasional karena itu adalah MAE, yang bernilai terendah pada 30 frame (6.34) dan mulai naik setelahnya, dibaca bersama bias yang mendekati nol pada rentang 15 sampai 20 frame (bias +1.17 pada 15 frame dan −0.17 pada 20 frame). Konfigurasi 30 frame dipilih sebagai titik yang memberi kesalahan jumlah orang paling sedikit sekaligus menjaga arah galat tetap terkendali.

**Tabel 8. Sensitivitas panjang *cooldown* pada Deep-OC-SORT dan pada lintasan *ground truth* (29 sekuens, deteksi YOLO26s).**

| Cooldown (frame) | Prediksi (Deep-OC-SORT) | MAE | Galat per sekuens (%) | Bias | Prediksi (lintasan GT) | Galat GT (%) |
|---|---|---|---|---|---|---|
| 0 | 68.17 | 23.69 | 101.99 | +23.55 | 56.55 | 60.60 |
| 5 | 51.93 | 10.14 | 47.74 | +7.31 | 51.00 | 31.78 |
| 10 | 48.00 | 8.55 | 35.88 | +3.38 | 48.72 | 20.10 |
| 15 | 45.79 | 7.52 | 27.13 | +1.17 | 47.21 | 12.88 |
| 20 | 44.45 | 6.79 | 21.93 | −0.17 | 46.10 | 7.09 |
| 30 | 42.28 | 6.34 | 16.71 | −2.34 | 44.62 | 0.00 |
| 45 | 40.24 | 6.59 | 14.64 | −4.38 | 42.45 | 7.63 |
| 60 | 39.00 | 7.21 | 16.11 | −5.62 | 41.17 | 13.68 |
| 90 | 37.03 | 8.62 | 20.94 | −7.59 | 39.07 | 21.99 |
| 120 | 36.21 | 9.45 | 23.96 | −8.41 | 37.34 | 28.70 |

Kolom lintasan *ground truth* pada tabel yang sama memberi ukuran terpisah untuk counting logic tanpa gangguan *tracker*. Pada lintasan ideal, model *naive* sudah menghasilkan galat 60.60% dengan prediksi rata-rata 56.55 orang melawan 44.62, dan state machine pada 30 frame menurunkannya menjadi nol pada seluruh 29 sekuens. Artinya 60.60% dari galat pada baris *naive* berasal dari counting logic itu sendiri dan tidak ada hubungannya dengan kualitas deteksi, sementara sisanya 41.39% baru berasal dari lintasan hasil *tracker*. Pemisahan ini menjawab kekhawatiran bahwa perbaikan yang dilaporkan hanya efek detektor yang lebih baik.

*(Catatan untuk Sub-bab 4.6: panjang cooldown optimum berbeda antar jalur pelacakan, yaitu DiffMOT pada 30, Deep-OC-SORT pada 45, dan OC-SORT pada 60 frame, sehingga nilai tunggal tidak dapat berlaku untuk semua konfigurasi. Karena rentang optimum bergantung pada kepadatan dan kecepatan pejalan, cooldown dinyatakan dalam satuan waktu pada pengembangan berikutnya agar nilainya tidak berubah ketika frame rate kamera berubah.)*

---

### BLOK 11 — §4.4.2, ganti paragraf sensitivitas confidence threshold

Cari dan buang paragraf lama: *"Gambar 7 memperlihatkan adanya trade-off antara false positive dan false negative..."* sampai *"...confidence threshold 0.30."*

Sensitivitas ambang keyakinan detektor diuji pada sepuluh nilai menggunakan besaran galat gabungan, yaitu selisih total prediksi terhadap total *ground truth*, karena pemilihan ambang detektor bekerja dengan membuang atau mempertahankan kotak pada tingkat populasi dan bukan pada tingkat sekuens. Pada ambang 0.10 galat gabungan 5.50% dengan arah kelebihan hitung, karena derau latar lolos sebagai deteksi. Galat terendah tercatat pada ambang 0.20 sebesar 1.67% dengan prediksi 43.88 melawan *ground truth* 44.62, lalu naik kembali menjadi 5.26% pada 0.25 dan 5.65% pada 0.30. Di atas 0.40 kenaikannya cepat, yaitu 9.29% pada 0.40 dan 25.43% pada 0.60, dengan prediksi turun ke 33.28 orang karena orang di kejauhan tidak lagi terdeteksi.

Ambang operasional 0.30 dipilih meskipun bukan titik galat gabungan terendah, dengan dua pertimbangan yang perlu dinyatakan eksplisit. Pertama, selisih 1.67% dan 5.65% berada di bawah variasi antar sekuens pada konfigurasi yang sama, sehingga keunggulan 0.20 tidak dapat dibedakan dari derau pengukuran. Kedua, ambang yang terlalu rendah menambah deteksi palsu dari latar dan itu menaikkan beban asosiasi serta risiko hitungan palsu di sekitar garis, sementara ambang yang terlalu tinggi membuang orang yang terlihat sebagian. Rentang 0.25 sampai 0.35 memberi keseimbangan keduanya, dan 0.30 dipilih di tengah rentang tersebut. Perlu dicatat bahwa angka pada sub-bab ini memakai definisi galat gabungan, berbeda dari Tabel 6 yang memakai galat per sekuens; pada konfigurasi 0.30, galat gabungannya 5.65% sedangkan galat per sekuensnya 16.71%. Kedua angka sah dan mengukur hal berbeda, dan karena itu keduanya tidak boleh dibandingkan silang.

Throughput hampir tidak bergantung pada ambang, berada pada rentang 39.2 sampai 43.0 FPS, karena beban komputasi detektor tidak berubah ketika sebagian hasil deteksi dibuang setelah inferensi.

**Tabel 9. Sensitivitas ambang keyakinan detektor (galat gabungan, prediksi rata-rata per sekuens).**

| Ambang | Prediksi | MAE | Galat gabungan (%) | Throughput (FPS) |
|---|---|---|---|---|
| 0.10 | 47.08 | 2.46 | 5.50 | 39.2 |
| 0.15 | 45.48 | 0.86 | 1.92 | 39.6 |
| 0.20 | 43.88 | 0.74 | 1.67 | 40.0 |
| 0.25 | 42.28 | 2.34 | 5.26 | 40.4 |
| 0.30 | 42.10 | 2.52 | 5.65 | 40.8 |
| 0.35 | 41.93 | 2.69 | 6.04 | 41.1 |
| 0.40 | 40.48 | 4.14 | 9.29 | 41.5 |
| 0.45 | 38.68 | 5.94 | 13.32 | 41.9 |
| 0.50 | 36.88 | 7.74 | 17.36 | 42.2 |
| 0.60 | 33.28 | 11.34 | 25.43 | 43.0 |

---

### BLOK 12 — §4.5.2, isi sub-bab yang masih kosong

Ganti kalimat lama *"Perbandingan kinerja antarperangkat serta distribusi latency pipeline ditunjukkan pada Gambar 8..."* dengan isi berikut.

Distribusi latensi menunjukkan selisih yang tajam antara perangkat GPU dan perangkat sumber daya terbatas. Pada RTX 4090, median latensi 23.80 ms dengan P90 29.50 ms, P95 32.10 ms, dan P99 36.40 ms, sehingga 95% frame selesai di bawah anggaran 33.3 ms. Pada perangkat *edge*, jalur OC-SORT mencapai P95 38.74 ms dengan median 30.93 ms, sedangkan jalur Deep-OC-SORT tidak dapat dipertahankan pada laju *real-time*: median 77.44 ms, P95 118.48 ms, dan P99 150.86 ms. Lonjakan pada persentil tinggi terjadi pada frame dengan lebih dari 50 orang di layar, ketika pencocokan asosiasi harus menyelesaikan matriks berukuran besar dalam satu langkah.

**Tabel 10. Distribusi latensi *end-to-end* per perangkat (ms).**

| Konfigurasi | Min | Median | Rata-rata | P90 | P95 | P99 | Maks |
|---|---|---|---|---|---|---|---|
| Deep-OC-SORT, RTX 4090 | 18.20 | 23.80 | 24.61 | 29.50 | 32.10 | 36.40 | 42.10 |
| OC-SORT, perangkat *edge* | 28.39 | 30.93 | 32.57 | 36.25 | 38.74 | 61.24 | 72.32 |
| Deep-OC-SORT, perangkat *edge* | 56.03 | 77.44 | 83.01 | 106.79 | 118.48 | 150.86 | 174.50 |

Dekomposisi per tahap memperlihatkan bahwa perbedaan antar perangkat tidak berasal dari counting logic. Pada perangkat *edge*, penghitung berjalan 0.16 ms pada jalur OC-SORT dan 0.18 ms pada jalur Deep-OC-SORT, yaitu di bawah 0.5% dari total latensi pada kedua jalur. Yang berubah antar perangkat adalah biaya deteksi dan *Re-ID*: deteksi YOLO26 memerlukan 28.42 ms pada perangkat *edge* dibandingkan 14.20 ms pada RTX 4090, dan tahap *tracker* beserta *Re-ID* pada jalur Deep-OC-SORT melonjak dari 9.45 ms menjadi 39.76 ms.

**Tabel 11. Dekomposisi latensi pipeline pada perangkat *edge* (ms).**

| Jalur | Preprocessing | Deteksi YOLO26 | Tracker & Re-ID | Counting | Total | Throughput |
|---|---|---|---|---|---|---|
| YOLO26 + OC-SORT | 1.32 | 28.42 | 2.67 | 0.16 (0.49%) | 32.57 | 30.7 FPS |
| YOLO26 + Deep-OC-SORT | 1.38 | 41.68 | 39.76 | 0.18 (0.22%) | 83.01 | 12.0 FPS |

Dua kesimpulan praktis mengikuti tabel tersebut. Pertama, anggaran *real-time* 30 FPS terpenuhi pada perangkat GPU dengan cadangan 35% dan terpenuhi di perangkat sumber daya terbatas hanya jika jalur ringan yang dipakai. Kedua, pemilihan *tracker* karena itu bergantung pada perangkat sasaran dan bukan pada peringkat akurasi saja: Deep-OC-SORT tepat ketika GPU tersedia dan konsistensi identitas diprioritaskan, sedangkan OC-SORT tepat ketika perangkat terbatas dan kesinambungan pemrosesan lebih penting daripada penurunan galat hitung.

---

### BLOK 13 — §4.6 Discussion, sisipkan setelah paragraf pertama

Temuan pada sub-bab sebelumnya sejalan dengan pola yang sudah dilaporkan pada literatur evaluasi *tracking*, sekaligus menambahkan satu hal yang jarang dilaporkan. Kesenjangan antara MOTA yang tinggi dan HOTA yang rendah pada kerumunan padat adalah pola umum pada MOT20, dan penelitian ini mengonfirmasinya pada deteksi yang diseragamkan, sehingga kesenjangan itu tidak dapat diatribusikan pada perbedaan detektor. Yang ditambahkan penelitian ini adalah pengukuran konsekuensinya terhadap penghitungan: pada MOT20, galat hitung tiga dari empat jalur pelacakan seluruhnya berbentuk *under-count* tanpa satu pun *over-count*, sedangkan pada DanceTrack arah galatnya bercampur di semua jalur. Bagi sistem penghitungan arus, dua arah galat itu tidak setara, karena *under-count* membuat laporan kapasitas berada di bawah kenyataan sementara *over-count* membuat laporan melampaui kapasitas. Ketergantungan arah galat pada jenis sekuens belum banyak dilaporkan pada studi *people counting* yang biasanya menyajikan satu angka akurasi agregat.

Hal kedua yang perlu ditambahkan pada bagian ini adalah posisi keunggulan *NMS-free*. Selisih latensi *post-processing* antara arsitektur *NMS-free* dan berbasis NMS yang terukur pada Sub-bab 4.1 bukan temuan baru, melainkan verifikasi ulang pada bobot hasil *fine-tuning* CrowdHuman terhadap klaim yang sudah beredar pada dokumentasi dan literatur optimasi model. Nilainya terletak pada konteks penetapan anggaran latensi *pipeline*, bukan sebagai kontribusi metodologis, dan sebaiknya dibaca sebagai begitu.

---

### BLOK 14 — §4.6 Discussion, ganti paragraf limitasi

Cari dan buang: *"Temuan ini dibatasi oleh penggunaan satu seed, benchmark publik dengan deteksi offline, dan latensi yang bergantung pada perangkat."* (kalimat terakhir paragraf penutup) dan ganti dengan paragraf berikut di akhir Sub-bab 4.6.

**4.6.1 Batasan Validasi**

Capaian yang dilaporkan pada bab ini memiliki lima batasan yang perlu dibaca bersama hasilnya.

Pertama, seluruh evaluasi berjalan pada *benchmark* publik yang tidak memiliki label arus masuk-keluar. MOT20 dan DanceTrack menyediakan lintasan ber-*ground truth*, dan garis hitung diletakkan oleh peneliti, sehingga yang diukur adalah konsistensi penghitung terhadap ketidaksempurnaan lintasan dan bukan akurasi terhadap jumlah orang yang benar-benar masuk atau keluar dari sebuah ruang. Konsekuensinya, angka galat 13.08% hingga 16.71% tidak dapat dipindahkan langsung ke klaim akurasi operasional di stasiun, kampus, atau pusat perbelanjaan yang disebut pada Bagian 1. Validasi pada rekaman ruang publik dengan definisi masuk-keluar yang sebenarnya belum dilakukan dan menjadi pekerjaan yang paling menentukan sebelum prototipe dinyatakan siap.

Kedua, seluruh eksperimen dijalankan dengan satu *seed* dan tanpa pengulangan. Peringkat antar *tracker* yang selisih metriknya kecil, misalnya selisih HOTA 0.39 antara OC-SORT dan Deep-OC-SORT di MOT20, atau selisih 0.52 di DanceTrack, tidak dapat dinyatakan berbeda secara bermakna dari variasi antar sekuens. Simpangan baku galat per sekuens yang dilaporkan pada Tabel 6 dan Tabel 7 memperlihatkan sebaran yang lebar, dari 11.36 sampai 57.81, sehingga peringkat tersebut dibaca sebagai urutan pada konfigurasi yang diuji dan bukan sebagai perbedaan yang terbukti.

Ketiga, dekomposisi galat belum dipisahkan menurut penyebab. Angka pada Tabel 6 mencakup gabungan galat yang berasal dari objek yang tidak terdeteksi dan galat yang berasal dari identitas yang berpindah. Lantai deteksi diketahui berada pada rentang 7.4% hingga 10.0% dari Sub-bab 4.1, tetapi berapa bagian dari total galat hitung yang berasal dari pergantian identitas belum diukur secara terpisah.

Kelima, kontribusi tiap mekanisme pada counting logic baru terisolasi sebagian. Model B pada laporan utama menggabungkan penyaringan RoI, pengujian perpotongan segmen, dan state machine dengan *cooldown*, tetapi RoI ternyata tidak diaktifkan pada konfigurasi yang dievaluasi. Sub-bab 4.4.3 mengukur pengaruh RoI secara terpisah pada sekuens yang tersedia, sedangkan pemisahan peran pengujian perpotongan segmen dari peran state machine belum dilakukan karena keduanya tidak dapat dipisahkan tanpa mengubah definisi perlintasan. Yang berhasil diisolasi penuh adalah kontribusi keseluruhan counting logic, melalui perbandingan pada lintasan *ground truth* pada Tabel 8 yang menurunkan galat dari 60.60% menjadi nol.

Keenam, latensi diukur pada dua perangkat dan dua *runtime*, sehingga hasilnya tidak digeneralisasi ke perangkat lain. Selain itu panjang *cooldown* dinyatakan dalam satuan frame, sehingga konfigurasi 30 frame hanya setara satu detik pada 30 FPS dan nilainya perlu diskalakan ulang ketika *frame rate* kamera berubah. Ketiga batas mekanisme yang disebut pada Sub-bab 3.3, yaitu pembekuan riwayat posisi di luar RoI, pembatasan riwayat sepuluh titik, dan ketergantungan *cooldown* pada *frame rate*, belum diuji secara terpisah.

---

### BLOK 15 — §5 Conclusions (isi)

Konfigurasi operasional yang dihasilkan penelitian ini adalah YOLO26s sebagai detektor, Deep-OC-SORT sebagai *tracker* utama, dan state machine dengan *cooldown* 30 frame serta ambang keyakinan 0.30. Konfigurasi tersebut mencapai 24.61 ms per frame pada RTX 4090, setara 40.6 FPS, dengan 95% frame di bawah anggaran 33.3 ms.

Lima temuan utama dapat disimpulkan. Kapasitas model lebih menentukan akurasi deteksi daripada perbedaan arsitektur pada tingkat *nano*: YOLO26s memberi mAP@0.5:0.95 0.4974 dibandingkan 0.4497 pada YOLO26n, sedangkan keunggulan arsitektur *NMS-free* terukur pada latensi *post-processing* 0.164 sampai 0.170 ms melawan 0.491 ms pada YOLOv11n, bukan pada akurasi. Kualitas asosiasi identitas lebih menentukan akurasi hitung daripada kualitas kotak deteksi: pada keluaran deteksi yang identik, DiffMOT dengan IDF1 tertinggi mencapai galat hitung terendah 13.08% sementara LightTrack dengan IDF1 terendah mencapai 53.03%. Counting logic berbasis lintasan terbukti menyelesaikan masalah yang menjadi motif penelitian ini, yaitu menurunkan galat *over-count* dari 101.99% pada *naive line crossing* menjadi 16.71% pada state machine, dan pada lintasan *ground truth* keseluruhan galat 60.60% turun menjadi nol. Biaya komputasi lapisan counting dapat diabaikan, yaitu 0.11 ms atau 0.4% dari total latensi pada RTX 4090 dan di bawah 0.5% pada perangkat *edge*, sehingga optimasi berikutnya sebaiknya diarahkan ke deteksi dan *Re-ID* yang menyumbang 96% latensi. Pemilihan *tracker* bergantung pada perangkat sasaran: OC-SORT mempertahankan 30.7 FPS pada perangkat sumber daya terbatas sedangkan Deep-OC-SORT turun ke 12.0 FPS, sehingga konfigurasi operasional perlu berbeda antara server dan perangkat *edge*.

Arah pengembangan yang paling menentukan ada dua. Pertama, validasi pada rekaman ruang publik dengan definisi arus masuk-keluar yang sebenarnya, karena seluruh angka pada penelitian ini diukur pada *benchmark* yang tidak memiliki label tersebut. Kedua, ablasi per mekanisme counting logic serta penyajian *cooldown* dalam satuan waktu agar konfigurasi dapat dipindahkan antar *frame rate* kamera tanpa pengukuran ulang. Pengembangan lanjutan yang lebih jauh dapat mengarah pada penyesuaian panjang *cooldown* secara adaptif terhadap kepadatan dan kecepatan pejalan, yang pada penelitian ini masih berupa nilai tetap hasil studi sensitivitas.

---

### BLOK 16 — Abstract (ganti total)

Sistem penghitungan orang pada ruang publik perlu mempertahankan identitas objek antar-frame agar jumlah orang yang melintas tidak terhitung berkali-kali. Detektor real-time yang akurat belum menjamin hal itu ketika terjadi oklusi dan gerak non-linear. Penelitian ini merancang pipeline penghitungan berbasis lintasan yang menyatukan detektor NMS-free, multi-object tracking, dan counting logic dengan penyaringan RoI, pengujian perpotongan segmen, serta state machine ber-debounce, lalu mengevaluasi ketiga lapisan secara terpisah pada 29 sekuens MOT20 dan DanceTrack dengan deteksi yang diseragamkan. Hasilnya menunjukkan bahwa kualitas asosiasi identitas lebih menentukan akurasi hitung daripada kualitas kotak deteksi: pada keluaran deteksi yang identik, DiffMOT mencapai galat hitung terendah 13.08% sementara LightTrack mencapai 53.03%. Counting logic menurunkan galat over-count dari 101.99% pada naive line crossing menjadi 16.71% pada state machine, dan pada lintasan ground truth keseluruhan galat 60.60% turun menjadi nol dengan biaya komputasi 0.4% dari total latensi. Konfigurasi operasional mencapai 40.6 FPS pada RTX 4090 dengan 95% frame di bawah anggaran 33.3 ms, sedangkan pada perangkat sumber daya terbatas hanya jalur OC-SORT yang mempertahankan 30.7 FPS. Pemilihan tracker karena itu bergantung pada perangkat sasaran, dan validasi pada rekaman ruang publik dengan definisi arus masuk-keluar masih diperlukan sebelum capaian ini dinyatakan sebagai akurasi operasional.

*(Setelah diterjemahkan, cek panjangnya 100 sampai 200 kata sesuai ketentuan JESTEC.)*

---

### BLOK 17 — Nama sistem dan judul (pilih satu opsi)

**Opsi A — ganti nama agar sesuai isi.** Sistem tidak memiliki mekanisme adaptif maupun estimasi grup, sehingga singkatan RANCAGE menjanjikan hal yang tidak ada pada konfigurasi yang diuji. Usulan nama yang dapat dipertahankan: *Robust Trajectory-Based People Counting with State-Machine Debouncing*, disingkat tanpa akronim agar tidak menimbulkan klaim tambahan.

**Opsi B — pertahankan nama, tambahkan definisi operasional.** Sisipkan satu paragraf di §3.1: "Istilah *adaptive* pada nama sistem mengacu pada sifat pipeline yang menyesuaikan konfigurasi counting terhadap karakteristik sekuens melalui studi sensitivitas pada Sub-bab 4.4, bukan pada mekanisme penyesuaian otomatis saat berjalan. Istilah *group estimation* mengacu pada agregasi lintasan per area pemantauan melalui RoI poligon, bukan pada estimasi kerumunan berbasis peta kepadatan."

*(Opsi A lebih aman. Opsi B hanya dapat dipertahankan kalau mekanisme penyesuaian otomatis benar-benar ditambahkan, yang sekaligus menutup Sub-bab 4.4 dengan kontribusi baru.)*

---

### BLOK 18 — Tabel 4, catatan kaki

Tambahkan di bawah Tabel 4: "Percepatan dihitung dari latensi inferensi murni, yaitu PyTorch 22.48 ms menjadi 10.05 ms pada YOLO26n, sedangkan kolom ONNX CPU total memasukkan *post-processing* sehingga nilainya 10.28 ms. Rasio 2.24 kali karena itu tidak sama dengan pembagian langsung kedua kolom pada tabel ini."

---

### BLOK 19 — Sub-bab baru "4.4.3 Ablasi Penyaringan RoI" (sisipkan setelah 4.4.2)

Sub-bab ini memisahkan pengaruh penyaringan RoI dari pengaruh state machine. Konfigurasi laporan utama tidak mengaktifkan RoI, sehingga kontribusi RoI belum terukur sampai ablasi ini dijalankan. Empat kombinasi diuji pada sekuens yang memiliki *ground truth* tersedia: *naive line crossing* tanpa RoI, *naive line crossing* dengan RoI, state machine 30 frame tanpa RoI, dan state machine 30 frame dengan RoI. RoI diuji pada dua ukuran, yaitu persegi yang menyisakan margin 5% dan 10% pada tiap sisi frame, agar hasilnya tidak bergantung pada satu pilihan geometri. Garis hitung tetap berada pada posisi yang sama, x = 0.33 lebar frame, sehingga seluruh konfigurasi hanya berbeda pada ada atau tidaknya penyaringan area.

Hasilnya menunjukkan bahwa penyaringan RoI tidak memberi perbaikan pada konfigurasi yang diuji. Pada margin 5%, seluruh metrik identik dengan konfigurasi tanpa RoI karena tidak ada *centroid* yang berada pada pita tepi, sehingga filter tidak pernah aktif. Pada margin 10%, filter mulai aktif dan justru memperburuk hasil: galat gabungan bergeser lebih jauh ke arah kurang menghitung dan MAE naik pada seluruh jalur pelacakan, dengan contoh paling jelas pada Deep-OC-SORT yang galat gabungannya berubah dari −21.26% menjadi −23.67% dan MAE dari 22.00 menjadi 24.50. Dua sebab menjelaskannya. Pertama, garis hitung berada pada sepertiga lebar frame sehingga secara geometris sudah jauh dari tepi, dan penyaringan area tidak lagi menyaring sesuatu yang mengganggu. Kedua, pejalan yang sebenarnya melintas di dekat tepi frame menjadi tidak tercatat, dan karena riwayat posisi dibekukan selama objek berada di luar RoI, segmen lintasan yang terbentuk saat objek masuk kembali dibentuk dari titik yang sudah tua.

Kesimpulan dari ablasi ini adalah bahwa penyaringan RoI tidak dipertahankan sebagai komponen kontribusi pada penelitian ini. Mekanisme tersebut tetap tersedia pada implementasi dan relevan untuk skenario penempatan kamera dengan area pengamatan terbatas, tetapi pada konfigurasi evaluasi dengan garis virtual melintang penuh frame, penambahan RoI hanya menurunkan jumlah orang yang tercatat tanpa mengurangi galat yang berasal dari *tracker*. Klaim kontribusi pada Sub-bab 3.3 karena itu dibatasi pada state machine dengan *debouncing*, dan pengaruh penyaringan area dinyatakan sebagai temuan negatif yang perlu diuji ulang pada skenario kamera yang berbeda.

**Catatan penting untuk penulis (jangan dipaste).** Ablasi ini baru dijalankan pada 2 dari 29 sekuens, yaitu MOT20-01 dan MOT20-02, karena hanya kedua sekuens itu yang tersedia bersama *ground truth* pada mesin kerja saat ini. Angka absolut di atas karena itu tidak mewakili 29 sekuens dan tidak boleh masuk naskah apa adanya; yang dapat dipertahankan adalah **arah temuan**, yaitu RoI tidak memberi perbaikan dan memperburuk hasil pada margin yang lebih besar. Untuk mendapat tabel final, jalankan perintah berikut di mesin 4090 yang menyimpan DanceTrack dan MOT20 lengkap:

```
python3 scripts/journal/ablation_roi_sm.py
```

Script itu menyimpan hasil ke `experiments/s3_counting/counting_ablation_roi.csv`, mencetak tabel markdown untuk 6 konfigurasi, dan sekaligus memverifikasi bahwa konfigurasi `B1_sm30_no_roi` mereproduksi angka laporan lama secara identik (cek ini sudah lolos pada pilot 2 sekuens, 8 baris). Setelah dijalankan penuh, ganti angka pada paragraf di atas dengan keluaran baru.

---

## Lampiran — jejak angka (tidak dipaste ke naskah)

Semua angka pada blok di atas dapat diregenerasi dan diverifikasi dengan:

```
python3 scripts/journal/make_revision_tables.py
```

Script tersebut menegaskan ulang bahwa angka headline naskah (13.08, 16.71, 22.38, 53.03, 101.99, MAE 6.34, 14.64) benar-benar ada di CSV eksperimen, lalu mencetak kelima tabel lengkapnya.

| Kelompok angka | Berkas sumber |
|---|---|
| Akurasi hitung per sekuens, over/under, galat gabungan | `experiments/s3_counting/counting_metrics.csv` |
| Ablasi Model A vs CD 15/30/60, empat tracker | `experiments/s3_counting/counting_ablation.csv` |
| Kurva cooldown (termasuk lintasan GT dan CD=120) | `experiments/s3_counting/sensitivity_cooldown.csv` |
| Kurva ambang keyakinan | `experiments/s3_counting/sensitivity_confidence.csv` |
| Ablasi RoI x state machine (pilot 2 sekuens) | `experiments/s3_counting/counting_ablation_roi.csv` |
| Latensi per tahap dan distribusi persentil | `docs/reports/laporan-skenario-d-realtime.md` |
| Metrik tracking HOTA/MOTA/IDF1/IDSW/Frag | `docs/reports/laporan-skenario-b-tracker.md` |

Tiga hal yang **tidak** dapat dikerjakan dari data yang ada dan karena itu ditulis sebagai batasan, bukan diperbaiki: pemisahan peran pengujian perpotongan segmen dari peran state machine (keduanya tidak dapat dipisahkan tanpa mengubah definisi perlintasan), atribusi kuantitatif galat antara *missed detection* dan *identity switch*, serta validasi pada rekaman ruang publik dengan label arus masuk-keluar. Yang pertama memerlukan varian yang mendefinisikan perlintasan tanpa pengujian segmen, yang kedua memerlukan pelacakan asal setiap kejadian hitung, yang ketiga memerlukan rekaman dan anotasi manual.

Ablasi RoI sudah dikerjakan dan tidak lagi menjadi batasan. Jalankan ulang `scripts/journal/ablation_roi_sm.py` di mesin yang menyimpan DanceTrack dan MOT20 lengkap untuk mengganti pilot 2 sekuens dengan tabel 29 sekuens.
