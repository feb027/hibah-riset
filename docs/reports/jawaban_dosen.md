# Argumen Pertahanan (Defense) untuk Dosen Penguji

Pertanyaan dosen Anda sangat tajam dan sangat khas untuk pengujian riset *Computer Vision*. Inti kekhawatiran beliau adalah **"Sistem Real-Time itu terlalu berat dan mustahil kalau datanya dikirim jarak jauh."**

Kabar baiknya, arsitektur sistem yang kita rancang **sangat bisa menjawab semua kekhawatiran tersebut**. Berikut adalah peluru jawaban elegan dan akademis yang bisa Anda bacakan/tunjukkan kepada beliau:

### 1. Masalah Komputasi Berat & Transfer Data (Poin 1, 2, 3, 7)
**Kekhawatiran:** Mengirim video CCTV secara *real-time* ke server pusat akan memakan *bandwidth* yang sangat besar dan membebani server.
**Jawaban (Solusi):** 
Pendekatan kita menggunakan paradigma **Edge Computing**. Kamera atau Mini-PC di lokasi (Edge) akan memproses videonya di tempat, BUKAN mengirimkan video mentah ke server. Yang dikirimkan ke server/database HANYALAH **data teks metrik** (contoh: `Timestamp: 10:05:01, Lokasi: Gerbang A, IN: 1, OUT: 0`). 
Karena yang dikirim hanya teks (hitungan Kilobyte), masalah transfer data jarak jauh teratasi 100%, sangat ringan, dan *dashboard* pelaporan tetap bisa *real-time*.

### 2. Kecepatan YOLO, FPS, & Frame Processing (Poin 4, 8, 9)
**Kekhawatiran:** Seberapa cepat YOLO memproses? Apakah sanggup memproses semua frame?
**Jawaban (Solusi):**
- **Varian Nano:** Kita menggunakan varian terkecil dari model AI (YOLOv10n / YOLO26-Nano). Varian ini dirancang khusus untuk kecepatan ekstrem, mampu menembus **>100 FPS** di GPU (RTX 4090 kita) dan **>30 FPS** di CPU biasa.
- **Frame Skipping:** CCTV merekam pada 30 Frame-Per-Second (FPS). Otak manusia berjalan sekitar 15-24 FPS. Sistem kita akan menerapkan algoritma *Frame Skipping/Downsampling* untuk hanya memproses **10 hingga 15 frame saja per detik**. Ini akan memangkas beban komputasi hingga 50% tanpa menghilangkan akurasi pelacakan orang berjalan.

### 3. Batasan Domain Terlalu Luas (Poin 5)
**Kekhawatiran:** Jangan terlalu luas lingkupnya.
**Jawaban (Solusi):**
Kami sangat setuju dengan masukan penguji. Untuk tahap purwarupa *(prototype)*, ruang lingkup implementasi *(deployment)* dibatasi secara ketat hanya pada **2 Area Spesifik** (misalnya: Pintu Masuk Utama Perpustakaan dan Gerbang Utama Kampus). 

### 4. Spesifikasi Dataset Primer & Sekunder (Poin 6)
**Kekhawatiran:** Datasetnya dari mana?
**Jawaban (Solusi):**
- **Dataset Sekunder:** Riset ini menggunakan dataset publik terstandarisasi berskala global seperti **CrowdHuman** atau **OpenCV vtest** untuk fase prapelatihan awal *(pre-training)* AI di lab GPU.
- **Dataset Primer:** Kami akan mengumpulkan rekaman CCTV mandiri dari **2 Area kampus** yang telah disepakati untuk proses kalibrasi akhir (Fine-Tuning) dan Validasi *Real-World*.
