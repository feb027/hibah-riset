# Naskah Presentasi Lengkap: Laporan Skenario A (Evaluasi YOLO)

*Catatan: Naskah ini diurutkan **persis** mengikuti struktur daftar isi laporan `laporan-skenario-a-finetuning-yolo.md`. Teks yang dicetak miring (**Baca:**) adalah poin dari slide/laporan yang Anda bacakan langsung. Teks reguler (**Jelaskan:**) adalah penjelasan lisan dengan gaya bahasa santai untuk audiens/dosen, lengkap dengan cara membaca tabel/grafik.*

---

## Bab 1 & 2: Ringkasan Eksekutif dan Pendahuluan

**Baca:** *"Laporan ini mendokumentasikan pelaksanaan Skenario A (Evaluasi Detector) pada dataset CrowdHuman. Tujuan utamanya bukan semata mencari model terbaik secara umum, melainkan menguji kelayakan model NMS-Free untuk menghitung orang di kerumunan padat."*

**Jelaskan:**
"Bapak/Ibu, hari ini saya akan mempresentasikan hasil pengujian lapis pertama dari sistem *people counting* kita, yaitu bagian deteksi orang (YOLO). Di bab awal ini, kami tegaskan bahwa kita belum membahas soal pelacakan (*tracking*) atau garis hitung (*counting line*). Yang kita uji murni ketajaman mata si AI ini saat melihat foto kerumunan padat. Mari kita lihat metodologi dan hasil ujinya."

---

## Bab 3: Metodologi

### 3.1 Dataset dan Protokol Anotasi
**Baca:** *"Kami menggunakan dataset CrowdHuman dengan 103.115 anotasi target. Protokol yang digunakan adalah 'fbox' (full-body box) yang bersifat amodal. Kami juga mencatat 1,97% kotak memiliki titik tengah di luar bingkai, dan wilayah 'ignore' ditangani secara spesifik."*

**Jelaskan:**
"Terkait tabel audit dataset di poin ini, ada tiga keputusan penting yang kami ambil:
1.  **Kenapa kami pakai Full-Body Box?** Kami memaksa AI menggambar kotak orang dari kepala sampai kaki, meskipun kakinya ketutupan meja atau orang lain. Tujuannya demi sistem *tracking* nanti. Kalau AI hanya disuruh deteksi bagian tubuh yang kelihatan saja, titik pusat badannya akan melompat-lompat saat dia jalan di belakang rintangan, dan itu merusak akurasi penghitungan.
2.  **Kenapa ada 1,97% titik tengah di luar bingkai?** Ini adalah orang yang berdirinya sangat mepet di ujung kamera, sampai titik pusat badannya ada di luar foto. Ini bisa bikin sistem sedikit distorsi (kebingungan), tapi karena jumlahnya cuma 1,97% (sangat kecil), ini tidak merusak hasil eksperimen.
3.  **Apa itu wilayah Ignore?** Di foto kerumunan, kadang ada kerumunan super padat di kejauhan yang saking buramnya tidak bisa dikotaki satu-satu. Area ini kami biarkan AI tebak saat latihan, tapi saat ujian kami anulir, agar nilai ujian AI benar-benar adil."

### 3.2 Konfigurasi Pelatihan
**Baca:** *"Konfigurasi: Epoch 100, resolusi 640x640, Optimizer 'auto', Seed 0, AMP aktif, dan fokus pada 1 Kelas (Person)."*

**Jelaskan:**
"Terkait tabel konfigurasi ini, kami mengunci pengacakan pelatihan dengan **Seed 0**. Tujuannya agar eksperimen ini 100% *reproducible* (bisa diulang kapanpun dengan hasil sama persis). Kami juga menggunakan **AMP** (*Automatic Mixed Precision*) agar AI belajar lebih ngebut di GPU tanpa jadi bodoh. Dan yang paling penting, memori AI ini kami pangkas agar dia fokus 100% mendeteksi 1 kelas saja, yaitu manusia."

### 3.3 Perangkat dan Runtime
**Baca:** *"Pengujian dilakukan pada Server GPU (RTX 4090) dengan PyTorch, dan CPU Komputer biasa menggunakan ONNX."*

**Jelaskan:**
"Tabel perangkat ini krusial karena menjawab janji proposal kami. Kami melatih AI di server GPU mahal, tapi untuk sistem yang menyala di lapangan nanti, kami mengujinya di **CPU biasa** menggunakan format **ONNX**. Format ONNX ini ibarat mengubah file dokumen yang berat menjadi PDF ringan, sehingga AI bisa jalan ngebut di komputer murah."

---

## Bab 4: Hasil Pelatihan

### 4.1 & 4.2 Tabel Utama & Cara Membaca
**Baca:** *"Hasil di Tabel 4.1 menunjukkan Precision berada di kisaran 0,82–0,85, dan Recall di kisaran 0,69–0,75. mAP@0.5 rata-rata 0,78, sedangkan mAP@0.5:0.95 menjadi tolok ukur utama."*

**Jelaskan:**
"Mari kita bedah tabel rapor AI di Bab 4.1 ini angka demi angka:
*   **Precision (85%):** Artinya dari 100 kotak tebakan AI, 85 benar-benar manusia, 15 salah tebak benda mati. Kalau presisi jelek, sistem CCTV kita akan menghitung lebih banyak orang dari aslinya (*over-count*).
*   **Recall (75%):** Artinya dari 100 orang asli di kamera, AI kita hanya berhasil nemu 75 orang. Sisanya terlewat. Karena Recall (75) lebih kecil dari Precision (85), artinya watak dasar AI kita lebih sering kehilangan orang (*under-count*) ketimbang berhalusinasi.
*   **mAP@0.5:** Ini mengukur 'apakah AI ketemu letak orangnya?'. Asal AI berhasil nebak 50% area badan orang, dianggap benar.
*   **mAP@0.5:0.95 (Rapor Utama):** Nah, kalau ini syaratnya jauh lebih sadis. AI tidak cuma harus ketemu orangnya, tapi kotaknya harus **sangat rapat** membungkus tubuh orang tersebut (akurasi 50% sampai 95%). Kenapa harus rapat? Karena kalau kotaknya melenceng/kegedean, sistem *Tracker* di tahap selanjutnya bakal kebingungan ngikutin orang itu bergerak."

### 4.3 Dinamika Konvergensi
**Baca:** *"Tabel konvergensi menunjukkan keempat model mencapai 99% performa akhirnya pada epoch 44–55."*

**Jelaskan:**
"Di tabel konvergensi ini, awalnya kami melatih AI selama 100 putaran (100 *epoch*). Tapi kalau kita perhatikan datanya, di putaran ke 50 saja kepintarannya sudah mentok (stagnan). Kesimpulan efisiensinya: 50 putaran terakhir itu hanya buang-buang listrik dan waktu GPU. Untuk riset ke depannya, kami cukup melatih 60 putaran saja."

---

## Bab 5: Analisis Kurva Diagnostik

### 5.1 Kurva F1-Confidence
**Baca:** *"Kurva F1 menunjukkan ambang confidence optimal untuk YOLO26s adalah 0,348, berbeda dengan model NMS-Free di kisaran 0,28."*

**Jelaskan:**
"Grafik F1 ini sangat berguna. Puncak kurvanya memberi tahu kita angka batas keyakinan (threshold) yang harus dipakai di lapangan nanti. Kalau batasnya kekecilan, AI salah nebak terus. Kalau kebesaran, banyak orang terlewat. Hasilnya terbukti: **kita tidak boleh memakai *settingan* pabrik (0,25)**. AI model YOLO26s butuh disetel di angka 0,348 agar akurat, sedangkan model lainnya di 0,28."

### 5.2 Kurva Precision-Recall
**Baca:** *"Kurva PR menabrak dinding vertikal pada recall 0,90–0,93."*

**Jelaskan:**
"Tolong perhatikan ujung kanan dari grafik Kurva PR ini. Kurvanya tiba-tiba jatuh menukik lurus ke bawah di angka 90-93%. Ini disebut 'batas dinding mentok'. Artinya apa? Artinya sehebat apapun kita ngotak-ngatik programnya, pasti selalu ada **sekitar 7-10% orang yang mustahil untuk dideteksi oleh AI**. Kualitas foto mereka memang terlalu buram atau kepotong untuk bisa dilihat mesin."

### 5.3 Confusion Matrix
**Baca:** *"Matriks menunjukkan 97.662 deteksi benar, 5.453 terlewat, dan 641.871 false positive pada ambang sangat rendah."*

**Jelaskan:**
"Bapak/Ibu mungkin kaget melihat angka *False Positive* (Background ditebak Orang) mencapai 641 ribu. Tolong diabaikan saja Pak/Bu, karena itu adalah angka artifisial dari software penguji yang memaksa AI menebak serampangan dengan keyakinan nyaris 0 demi menggambar grafik.
Fokus sesungguhnya ada di angka **5.453 (5,3%)** ini. Meskipun AI sudah disuruh nebak ngawur, tetap ada 5,3% orang asli yang dianggap jalanan (Background) oleh AI alias 'buta'. Ini membenarkan teori 'dinding mentok' 10% di Kurva PR tadi."

---

## Bab 6: Evaluasi Protokol CrowdHuman

### 6.1 & 6.2 Dampak Koreksi Protokol
**Baca:** *"Dengan menjadikan wilayah target 'ignore' sebagai netral, seluruh nilai AP mengalami kenaikan rata-rata +0,01."*

**Jelaskan:**
"Di tabel 6.1, nilai akurasi (AP) kita tiba-tiba naik sedikit. Ini karena kita menganulir soal-soal ujian yang jelek (area kerumunan buram). Penilaian jadi lebih adil, dan AI tidak dihukum dua kali karena melewatkan kerumunan buram. Angka akurasi yang naik inilah akurasi yang sesungguhnya."

### 6.3 Mengungkap Ilusi Angka Recall Maksimum
**Baca:** *"Batas atas recall arsitektur NMS-free terlihat unggul (0,91) dari model biasa (0,90), namun ini bukan keunggulan akurasi riil."*

**Jelaskan:**
"Kalau Bapak/Ibu lihat tabel, 'Recall Maksimal' AI generasi baru (NMS-Free) angkanya sedikit lebih tinggi dari AI lama (0,91 vs 0,90). Tapi nyatanya itu hanya **ilusi teknis**. AI generasi baru itu kalau dites dengan angka batas longgar, dia memuntahkan ratusan jawaban bertumpuk (sehingga seolah-olah berhasil mendeteksi banyak orang). Kalau dites dengan batas normal di dunia nyata, akurasi keduanya itu SERI. Kita pilih NMS-Free nanti murni karena dia lebih cepat, bukan lebih akurat."

### 6.4 Membaca Nilai MR⁻²
**Baca:** *"Nilai MR⁻² model kita berada pada 0,757–0,779."*

**Jelaskan:**
"Di tabel ini ada metrik MR⁻². Ini metrik kegagalan. Kenapa angkanya sampai 0,75 (gagal 75%)? Karena tesnya menggunakan simulasi ekstrem: **'Cari 22 orang bertumpuk per gambar, tapi kamu hanya boleh membuat 1 kali alarm palsu (False Positive)'**. 
Ditambah lagi, AI yang kita pakai adalah AI ukuran sangat kecil (Nano) agar bisa jalan di komputer murah, sehingga wajar dia kewalahan dites sekeras ini. Ini adalah harga kompromi antara alat murah vs akurasi absolut."

### 6.5 Analisis Terpisah (Breakdown 3 Kategori)
**Baca:** *"Tabel dan Grafik 6.5 membedah kesulitan deteksi ke dalam 3 sumbu: Pemotongan bingkai, Tingkat Oklusi, dan Ukuran Objek."*

**Jelaskan:**
"Tiga grafik Pie Chart dan tabel breakdown ini merinci kelemahan spesifik AI kita:
1. **Tabel 6.5.1 (Pemotongan):** Orang yang setengah badannya terpotong oleh pinggiran bingkai kamera adalah titik buta terparah AI! Akurasi (AP) anjlok **30 poin** dan Recall anjlok **20 poin**. Ini 2x lipat lebih parah dibanding ketutupan orang lain.
2. **Tabel 6.5.2 (Oklusi):** Orang yang tertutup rapat oleh tubuh orang lain membuat akurasi AI turun sekitar **12-15 poin**. 
3. **Tabel 6.5.3 (Ukuran):** Untuk orang yang posisinya sangat jauh (ukurannya sangat kecil), akurasi AI anjlok **35%**.
4. **Tabel 6.5.4 (Ambang NMS):** Kami juga menguji ulang *settingan* batas NMS ke angka 0,9 untuk memastikan tes kita adil ke model AI lama, dan hasilnya model lama malah makin turun akurasinya. Ini membuktikan *settingan* tes kita sudah 100% adil.

**Kesimpulan Aplikasi Bab 6:** Nanti saat dipasang di lapangan, **kamera harus ditundukkan** agar orang tidak terlihat terlalu kecil, dan **kami haramkan menaruh garis hitung (counting line) di pinggiran kamera** karena disitulah AI paling buta."

---

## Bab 7: Hasil Pengukuran Latensi (Kecepatan)

### 7.1 & 7.2 Overhead GPU vs CPU + ONNX
**Baca:** *"Model NMS-free memangkas biaya post-processing di GPU sebesar 2,9× lipat. Pada konversi ONNX dan dijalankan di CPU, peringkat latensi berbalik drastis dengan YOLO26n tampil tercepat pada 10,28 ms (97 FPS)."*

**Jelaskan:**
"Bab 7 ini menjawab rasa penasaran soal kecepatan. 
Di tabel 7.1 (GPU), teknologi NMS-Free terbukti membuat proses *post-processing* AI kita **2,9 kali lebih cepat**. Hebatnya lagi, mau kerumunannya sepi atau sepadat apapun, waktu prosesnya (latensinya) tetap datar dan stabil!

Di tabel 7.2 (CPU), perhatikan rankingnya berbalik 180 derajat. Kalau di Server GPU mahal, YOLO model lama (v10n) paling ngebut. TAPI, saat formatnya diubah ke ONNX dan dijalankan di komputer murah (Edge CPU), **YOLO26n mendadak jadi juaranya!** Dia tembus kecepatan **97 FPS** di CPU. Di sisi lain, literatur sains (Tabel 7.4) juga membenarkan bahwa fenomena 'peringkat berubah saat pindah perangkat' (Latency Monotonicity) itu hal yang sangat wajar."

### 7.3 Penskalaan Resolusi
**Baca:** *"Menurunkan resolusi dari 640 ke 256 piksel hanya menaikkan FPS sebesar 27%, namun mengorbankan hingga 78% deteksi."*

**Jelaskan:**
"Kalau ada usulan 'Gimana kalau ukuran gambarnya kita kecilkan biar sistem makin ngebut?' Grafik ini menjawabnya: **TIDAK**. Menurunkan resolusi memang bikin FPS naik 27%, tapi bayarannya mahal banget: **75% orang di layar langsung hilang dari deteksi AI**. Jadi kami putuskan sistem akan mengunci resolusi di angka 640."

---

## Bab 8, 9, 10: Pembahasan, Batasan, dan Langkah Selanjutnya

**Baca:** *"Akurasi di antara model kelas nano praktis setara, ukuran model jauh lebih menentukan. Pilihan jatuh pada YOLO26n untuk target Edge CPU, sedangkan YOLO26s untuk target GPU."*

**Jelaskan:**
"Sebagai kesimpulan presentasi ini: Model mana yang akan kita pakai?
1. Kalau klien butuh akurasi tertinggi dan punya Server GPU, pilih **YOLO26s** (versi Small, recall-nya luar biasa tinggi).
2. TAPI, untuk target riset ini (Sistem Edge CPU yang murah), **Pemenangnya mutlak YOLO26n**. Akurasinya imbang dengan pesaingnya, tapi di CPU dia menang telak soal kecepatan (97 FPS) dan tahan banting melawan kerumunan padat berkat *NMS-Free*.

Selanjutnya (Bab 10), karena kita sudah punya detektor super cepat ini, riset minggu depan akan berfokus membuat otak lapis kedua (Skenario B: Sistem Pelacak / Tracker) agar pergerakan orang-orang ini bisa dihitung lintas *frame*. Demikian Bapak/Ibu, terima kasih."
