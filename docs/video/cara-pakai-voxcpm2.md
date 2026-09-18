# Cara Pakai: Render Narasi Video dengan VoxCPM2

Panduan langkah demi langkah. Tiga jalur, pilih satu. Siapkan dulu bahannya, karena ketiga jalur memakai bahan yang sama.

---

## 0. Siapkan Dua File Naskah

Buat folder `video-puu/` di Google Drive berisi dua file. Keduanya punya **jumlah paragraf yang sama persis**, hanya isinya berbeda.

**`naskah-asli.txt`** — naskah normal, untuk subtitle. Paragraf dipisah satu baris kosong:

```
Pengelolaan ruang publik modern memerlukan informasi mengenai jumlah dan
pergerakan orang yang dapat diperoleh secara cepat dan akurat.

Sistem ini diberi nama RANCAGE, singkatan dari Real-Time Adaptive Neural
Counting with Associative Group Estimation.
```

**`naskah-tts.txt`** — versi yang dibaca mesin, untuk disintesis. Sudah ditulis ulang secara fonetis memakai tabel di `docs/video/riset-tts-video-penelitian.md` bagian 6:

```
Pengelolaan ruang publik modern memerlukan informasi mengenai jumlah dan
pergerakan orang yang dapat diperoleh secara cepat dan akurat.

Sistem ini diberi nama Rancage.
```

Bedanya cuma di istilah teknis. Kalimat biasa tidak perlu diubah. Kalau ada istilah Inggris yang terdengar aneh saat keluar, baru tulis ulang secara fonetis mengikuti ejaan Indonesia.

Cek dulu panjangnya. Target 4–5 menit berarti 600–750 kata:

```bash
wc -w naskah-asli.txt
```

---

## 1. Jalur A — Google Colab (paling praktis, tanpa pasang apa pun)

Buka `colab.research.google.com` → *New notebook* → *Runtime* → *Change runtime type*.

Di dialog itu isi begini:

| Kolom | Nilai |
| :--- | :--- |
| *Runtime type* | Python 3 |
| *Hardware accelerator* | **T4 GPU** |
| *Runtime version* | **Latest (recommended)** |

T4 punya 16 GB VRAM, cukup untuk kebutuhan VoxCPM2 sekitar 8 GB. Kalau akunmu menawarkan **L4 GPU** atau **A100 GPU**, ambil itu, hasilnya lebih cepat. Jangan pilih opsi TPU: VoxCPM2 memakai CUDA, bukan TPU.

*Runtime version* dibiarkan di **Latest**. Versi terbaru saat ini adalah 2026.07 dengan Python 3.12.13, dan itu sudah masuk syarat VoxCPM. Pinning ke 2026.07 hanya perlu kalau suatu saat Latest berpindah ke Python 3.13, karena VoxCPM menolak versi 3.13 ke atas.

### Sel 1 — sambungkan Drive dan pasang VoxCPM

```python
from google.colab import drive
drive.mount('/content/drive')
!pip install -q voxcpm soundfile
```

Pemasangan ini tidak cepat. `voxcpm` menarik `modelscope`, `datasets`, `funasr`, `gradio`, dan `matplotlib` sekaligus, jadi sediakan beberapa menit. Selama prosesnya jalan dan tidak berhenti dengan `ERROR: Could not find a version`, biarkan saja. Baris peringatan `pip's dependency resolver` di akhir bukan tanda gagal; penjelasannya ada di tabel bagian 5.

### Sel 2 — ambil skrip render

```python
!wget -q -O /content/render_narasi.py \
 https://raw.githubusercontent.com/feb027/hibah-riset/main/scripts/video/render_narasi.py
!python /content/render_narasi.py --help | head -20
```

Kalau sel ini menampilkan bantuan pemakaian, skripnya siap.

### Sel 3 — cek rencana tanpa memuat model

```python
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" --dry-run
```

Lihat daftar paragraf dan perkiraan durasinya. Kalau jumlah paragrafnya sudah benar, lanjut.

### Sel 4 — tentukan suara acuan (sekali saja)

**Jangan langsung render 15 paragraf.** Dua hal dari dokumentasi resmi yang harus dipegang di sini:

1. **Tanpa audio referensi, VoxCPM menghasilkan suara acak setiap kali.** Usage Guide menuliskannya apa adanya: *"If you do not provide a reference audio, VoxCPM generates a random voice each time."* Itu sebabnya paragraf 1 dan 2 kamu terdengar seperti dua orang berbeda.
2. **Deskripsi suara hanya dipahami dalam Bahasa Inggris atau Bahasa Mandarin.** Kalimat aslinya: *"Chinese and English are both supported in the instruction."* Deskripsi berbahasa Indonesia diabaikan begitu saja, dan model jatuh ke suara acak. Ini penyebab suara pria yang kamu minta keluar sebagai suara perempuan.

Jalan keluarnya: buat **satu** paragraf contoh dengan deskripsi **berbahasa Inggris**, dengarkan, kalau bagus simpan filenya sebagai acuan, lalu semua paragraf lain mengkloning file itu.

```python
!cd /content && mkdir -p acuan && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out acuan --only 1 \
  --voice-desc "(a middle-aged male narrator with a warm, slightly husky low register and audible breath, measured pace, as if explaining the work to one colleague in a quiet room)" \
  --steps 25 --cfg 1.7
```

Dengarkan `acuan/narasi_01.wav`. Dokumentasi menyarankan mencoba 1–3 kali untuk mendapat suara yang diinginkan. Bahan deskripsinya, semua dalam Bahasa Inggris:

| Bagian | Contoh |
| :--- | :--- |
| Identitas | `a young male narrator`, `a middle-aged male broadcaster`, `an elderly woman` |
| Tekstur | `low register`, `slightly husky`, `breathy`, `warm and magnetic` |
| Tempo dan gaya | `measured pace`, `unhurried`, `dry and matter-of-fact` |
| Situasi | `as if explaining to one colleague`, `speaking to one listener in a quiet room` |
| Emosi | `neutral, no strong emotion`, `warm`, `composed` |

Baris **tekstur** dan **situasi** adalah dua baris yang paling menentukan hasilnya. Deskripsi tanpa keduanya, misalnya `calm and clear` saja, menghasilkan suara bawaan model, dan suara bawaan itulah yang terdengar seperti AI. Pembahasan lengkapnya di bagian 6.

Kalau temponya terlalu lambat, tukar `measured pace` jadi `brisk pace` atau tambahkan `faster pace`. Kalau terasa datar, tambahkan `warm` atau `husky`.

### Sel 5 — render semua paragraf dengan suara terkunci

```python
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --reference-wav "/content/acuan/narasi_01.wav"
```

Sejak titik ini, timbre suara diambil dari `narasi_01.wav`, bukan dari deskripsi teks. Semua 15 paragraf akan terdengar sebagai orang yang sama.

Dua hal yang berubah setelah ini:

- **`--seed` tidak lagi perlu dipikirkan.** Yang mengunci suara adalah berkas acuan, bukan angka acak.
- **Kontrol tempo masih bisa.** Tambahkan `--voice-desc "(brisk pace)"` di samping `--reference-wav`. Ini mengubah gaya, bukan timbre, jadi suara tetap konsisten dengan acuan. Ingat, deskripsi harus Bahasa Inggris.

### Sel 6 — render ulang satu paragraf saja

Perbaiki paragraf itu di `naskah-tts.txt`, unggah ulang, lalu:

```python
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --reference-wav "/content/acuan/narasi_01.wav" \
  --only 4 --force
```

`--only 4` artinya render paragraf keempat saja, dan `--force` menimpanya.

Jangan tertukar: `--only N` me-render satu paragraf saja, sedangkan `--start N` me-render dari paragraf N sampai paragraf terakhir.

### Mode ketiga: kloning hi-fi, kalau masih kurang mirip

Kalau hasil kloning referensi masih terasa belum pas, VoxCPM2 punya mode paling ketat: audio acuan **beserta transkrip persisnya**. Model melanjutkan langsung dari rekaman itu sehingga timbre, ritme, dan gaya ikut terbawa.

```python
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --reference-wav "/content/acuan/narasi_01.wav" \
  --prompt-wav "/content/acuan/narasi_01.wav" \
  --prompt-text "Setiap hari, stasiun kereta, kampus, dan pusat perbelanjaan dipenuhi orang yang bergerak masuk dan keluar. Pengelola tempat itu perlu tahu berapa banyak orang yang ada di dalam, dan perlu tahu sekarang juga. Angka itu dipakai untuk mengatur kapasitas, menjaga keamanan, dan mengambil keputusan."
```

`--prompt-text` harus transkrip **kata per kata** dari audio acuan, tanpa dikoreksi. Kalau diisi sembarangan, hasilnya rusak.

Satu batasan mode ini: **kontrol instruksi hanya diabaikan pada mode hi-fi**, seperti dikonfirmasi pengelola VoxCPM2 di issue #210. Model meniru persis tempo dan gaya audio acuan, tanpa memedulikan instruksi. Karena itu skrip menolak kombinasi `--voice-desc` dengan `--prompt-wav`, supaya tidak ada ilusi bahwa instruksinya bekerja.

Di luar mode hi-fi, alias pada `--reference-wav` saja, instruksi gaya justru **didukung** dan itu tertulis di Usage Guide: timbre diambil dari berkas acuan, sedangkan tag di dalam tanda kurung mengubah gaya. Jadi `--reference-wav acuan.wav --voice-desc "(brisk pace)"` sah dan memang bekerja.

Konsekuensinya praktis: **kalau ingin suara hi-fi yang lebih cepat, audio acuannya harus sudah lebih cepat.** Bikin acuan dengan deskripsi `brisk pace` atau `faster pace`, simpan hasil itu, baru pakai sebagai `--prompt-wav`. Pengguna lain di issue yang sama menempuh jalan ini setelah melaporkan hasil hi-fi terlalu lambat untuk voiceover.

### Tidak ada opsi "render sekaligus"

Dua alasan kenapa narasi dipecah per paragraf:

1. **Batas keras 8192 token** pada VoxCPM2, dengan audio maksimum sekitar 3 menit per pemanggilan. Satu paragraf di berkas ini saja memakai ratusan token, jadi 16 paragraf jauh melewatinya. (VoxCPM 1.x batasnya 4096; angka itu yang sering tersalin dari panduan lama.)
2. **Dokumentasi mengakui ketidakstabilan pada teks panjang.** Peramban CLI resmi VoxCPM2 sendiri, `voxcpm batch`, juga memecah masukan baris per baris, bukan sekali jalan.

Setelah suara terkunci lewat berkas acuan, pemecahan ini tidak lagi merugikan konsistensi. Yang tersisa hanya pekerjaan menyambung 15 potongan di editor.

---

## 2. Jalur B — RTX 4090 Kampus

Samakan saja dengan Colab, hanya tanpa Drive.

```bash
pip install voxcpm soundfile
mkdir -p ~/video-puu/out
cd ~/video-puu
python /path/ke/hibah-riset/scripts/video/render_narasi.py naskah-tts.txt \
  --out out \
  --voice-desc "(a young male narrator, calm and clear, brisk pace, documentary style)" \
  --seed 42
```

Pada 4090, RTF sekitar 0,3 berarti narasi 5 menit selesai dalam sekitar 1,5 menit setelah model termuat.

**Jangan aktifkan `torch.compile` atau `optimize=True`.** Untuk pemakaian sekali-sekali, itu justru 10–20 kali lebih lambat.

Kalau ingin antarmuka web alih-alih baris perintah, repo VoxCPM punya `app.py`:

```bash
git clone https://github.com/OpenBMB/VoxCPM && cd VoxCPM
python app.py --port 8808
```

Buka `http://localhost:8808`.

---

## 3. Jalur C — Draft Cepat Tanpa GPU

Pakai ini untuk menyusun video lebih dulu sambil menunggu GPU kosong. Kualitasnya cukup untuk melihat timing, belum untuk final.

```bash
pipx install edge-tts
python scripts/video/render_narasi.py naskah-tts.txt \
  --engine edge --voice id-ID-ArdiNeural --out out_draft
```

Suara Indonesia yang tersedia: `id-ID-ArdiNeural` (pria), `id-ID-GadisNeural` (wanita). Atur tempo dengan `--rate=-10%` kalau terasa cepat.

Kalau muncul galat `403 Invalid response status`, versi `edge-tts` di mesin terlalu lama. Perbarui: `pipx upgrade edge-tts`.

---

## 4. Setelah Semua Potongan Jadi

1. Periksa durasi total. Enam WAV dari paragraf 700 kata biasanya jatuh di 4,5–5,5 menit. Kalau lewat dari 5 menit, potong kalimat di naskah, bukan mempercepat audio di editor — audio yang dipercepat terdengar tidak wajar.
2. Susun di editor: audio berurutan, musik latar di level sekitar −18 dB supaya tidak menutupi narasi.
3. Subtitle dibuat dari **`naskah-asli.txt`**, bukan versi fonetis. Kalau versi fonetis yang dipakai, subtitle akan menampilkan "Riil Taim Adaptif" alih-alih "Real-Time Adaptive".
4. Tambahkan keterangan kecil di deskripsi video bahwa narasi dihasilkan dengan bantuan AI. VoxCPM2 menyisipkan tanda air pada keluarannya dan dokumentasinya meminta hal ini.

---

## 5. Kalau Ada Masalah

| Gejala | Sebab dan tindakan |
| :--- | :--- |
| Sekumpulan peringatan `Tesla T4 does not support bfloat16 compilation natively, skipping` | **Bukan galat, abaikan.** Model berjalan pada bfloat16, sedangkan T4 arsitektur Turing yang tidak punya tensor core bfloat16. PyTorch melewati tahap kompilasi untuk bagian itu dan jatuh ke jalur biasa. Hasilnya benar, hanya lebih lambat. Percepat dengan `--optimize` tidak dipakai (lihat baris berikutnya). |
| Peringatan `Dynamo detected a call to a functools.lru_cache-wrapped function at 'einops.py'` | **Bukan galat, abaikan.** Ini peringatan `torch.compile` soal fungsi `einops` yang di-cache. Peringatannya sendiri menyebut risikonya hanya potensial dan belum pernah teramati. Kalau mau hilang, jalankan tanpa `--optimize`. |
| `Not enough SMs to use max_autotune_gemm mode` | **Bukan galat.** T4 punya jumlah SM lebih sedikit dari yang dibutuhkan mode autotune. Kompilasi tetap jalan dengan setelan biasa. |
| `pip install voxcpm` gagal, menyebut versi Python | Sangat jarang. Metadata paket `voxcpm` 2.0.3 hanya mensyaratkan `>=3.10`, tanpa batas atas, dan pemasangan di Colab Python 3.13 sudah terbukti berhasil. Kalau tetap gagal, pin runtime: *Runtime → Change runtime type → Runtime version → 2026.07*. |
| `ERROR: pip's dependency resolver ... gcsfs requires fsspec==..., but you have fsspec ...` | **Bukan galat, abaikan saja.** `voxcpm` 2.0.3 mendeklarasikan `modelscope>=1.22.0` dan `datasets<4`, dan keduanya memin `fsspec` ke versi lama sehingga bertabrakan dengan `gcsfs` bawaan Colab. Yang terdampak hanya akses Google Cloud Storage, yang tidak dipakai di alur ini. Pengunduhan model memakai Hugging Face, dan Drive yang sudah termount tidak terpengaruh. Jangan ditambal dengan menaikkan `fsspec`, karena ModelScope akan rusak. |
| Proses berhenti tanpa pesan, Colab memutus sesi | Sesi gratis punya batas waktu. Jalankan ulang Sel 1, 2, 4; hasil sebelumnya dilewati otomatis. |
| Satu paragraf keluar kosong atau terpotong | Dokumentasi VoxCPM2 mengakui ketidakstabilan pada teks panjang. Potong paragraf itu jadi dua, tambahkan baris kosong di `naskah-tts.txt`, render ulang. |
| Sebutir kata terucap salah | Perbaiki di `naskah-tts.txt` saja, lalu render ulang paragraf itu dengan `--only N --force`. Naskah asli tidak perlu disentuh. |
| `edge-tts` mengembalikan 403 | Versi lama. `pipx upgrade edge-tts`. |
| Semua paragraf terdengar seperti orang berbeda | Kamu memakai `--voice-desc` sendirian. Voice Design dari teks memang berganti suara tiap pemanggilan. Pakai `--reference-wav` dengan satu berkas acuan (lihat Sel 4 dan 5). |
| Suara terdengar seperti AI, rata dan tanpa napas | Tiga sebab berurutan: deskripsi suara tanpa tekstur, acuan hasil Voice Design, dan `--steps` masih 10. Ikuti bagian 6. |
| Hasil kloning tidak pernah bernapas, seperti membaca tanpa jeda | Audio acuanmu bersih dari napas. Rekam ulang 20–30 detik dan biarkan napas ikut masuk, lalu jangan di-denoise. Model belajar "tanpa napas" sebagai keadaan normal. |
| Suara tidak sesuai deskripsi, pria diminta keluar perempuan | Deskripsi ditulis dalam Bahasa Indonesia. Instruksi VoxCPM2 hanya mendukung **Bahasa Inggris dan Mandarin**. Tulis ulang dalam Bahasa Inggris, mis. `(a young male narrator, calm and clear, brisk pace)`. |
| Render jalan terus padahal cuma mau satu paragraf | Kamu memakai `--start 1`, yang artinya "dari paragraf 1 sampai habis". Untuk satu paragraf saja pakai `--only 1`. |
| Suara terasa lambat | Tambahkan `brisk pace` atau `faster pace` pada `--voice-desc` di samping `--reference-wav`. Mengubah gaya, bukan timbre. Untuk mode hi-fi, instruksi diabaikan, jadi acuannya sendiri harus sudah lebih cepat. |
| Hasil kloning berbunyi berdengung atau berisik | Turunkan `--cfg` dari 2.0 ke sekitar 1,5–1,6. Dokumentasi menyebut nilai lebih rendah lebih stabil pada masukan sulit. |
| `TypeError: VoxCPM._generate() got an unexpected keyword argument 'seed'` | Versi skrip di Colab masih yang lama. `generate()` pada `voxcpm` 2.0.3 tidak punya parameter `seed`; versi terbaru skrip memakai `torch.manual_seed()`. Ambil ulang: `!wget -q -O /content/render_narasi.py https://raw.githubusercontent.com/feb027/hibah-riset/main/scripts/video/render_narasi.py` |
| Render terasa sangat lambat di Colab | T4 memang jauh lebih lambat dari 4090, dan kompilasi bfloat16 dilewati. Pastikan `--optimize` tidak dipakai. Kalau tersedia L4 atau A100 di dialog runtime, pindah ke sana. |

### Selamat datang di tahap yang benar

Kalau log kamu berisi baris berikut, semuanya sudah berjalan seperti seharusnya:

```
Running on device: cuda, dtype: bfloat16
Loaded VoxCPM2Model
```

Model terunduh 4,35 GB lalu dipulihkan menjadi 4,96 GB di `/root/.cache/huggingface/`. Selepas itu, peringatan apa pun yang muncul berasal dari `torch.compile` dan tidak menghentikan proses. Yang perlu ditunggu adalah baris `narasi_01.wav` mulai muncul di `/content/drive/MyDrive/video-puu/out/`.

---

## 6. Supaya Suaranya Tidak Terdengar Seperti AI

Empat tuas, diurutkan dari yang paling berpengaruh. Tiga yang pertama gratis.

### 6.1 Deskripsi `calm and clear` itu deskripsi suara asisten, bukan suara narator

Empat kata sifat yang dipakai sekarang, yaitu `a young male narrator`, `calm and clear`, `brisk pace`, dan `documentary style`, tidak satu pun menyebut tekstur suara. Model tidak punya bahan untuk membedakan hasilnya dari suara bawaannya, dan suara bawaan sebuah model TTS memang yang terdengar seperti AI.

Dokumentasi VoxCPM2 menyebut tiga bahan yang harus ada di `--voice-desc`: **identitas**, **tekstur suara**, dan **situasi**. Contoh resep di dokumentasi resminya jauh lebih spesifik daripada empat kata sifat:

> `A quiet raspy, elderly woman of a low-pitched voice with a distinct, grainy texture and subtle breathy tremors. Delivers a slow tone at a very low volume, perfect for historical narration.`

Terjemahan pola itu untuk video ini, dari yang paling berdampak:

```bash
# 1. paling berpengaruh: tekstur + napas + situasi
--voice-desc "(a middle-aged male narrator with a warm, slightly husky low register and audible breath, measured pace, as if explaining the work to one colleague in a quiet room)"

# 2. tanpa penanda situasi
--voice-desc "(a man in his forties, low-pitched and slightly raspy, unhurried, dry and matter-of-fact)"

# 3. paling dekat ke deskripsi lama, hanya ditambah tekstur
--voice-desc "(calm male narrator, low warm register, quiet and composed, unhurried)"
```

Kata yang dibuang dan alasannya:

| Dibuang | Kenapa |
| :--- | :--- |
| `clear`, `crystal clear` | Mendeskripsikan hasil akhir, bukan suara. Tidak bisa diikuti model |
| `documentary style` | Gaya bawaan semua narator. Nol daya pembeda |
| `professional`, `perfect audio quality` | Deskripsi kualitas rekaman, bukan suara |
| `brisk pace` | Bawaan video ini memang sudah cepat; menyebutnya hanya menambah kerataan |

Tiga kata tekstur yang benar-benar mengubah keluaran: `husky`, `breathy`, `low register`. Satu penanda situasi seperti `explaining to one colleague` membuat tempo tidak rata sendiri, tanpa perlu menyebut tempo.

### 6.2 Akar masalahnya: jangan mengkloning hasil Voice Design

Selama berkas acuan berasal dari deskripsi teks, seluruh 16 paragraf mewarisi suara rata-rata model. Yang mengubah kualitas paling besar bukan deskripsi, melainkan **asal audio acuan**.

Rekam 20–30 detik suara sendiri, baca satu paragraf naskah ini, lalu pakai rekaman itu sebagai acuan untuk semua paragraf. Aturannya:

- 10–30 detik, satu tarikan bicara, jangan dipotong-potong;
- **biarkan napasnya terekam**, jangan dibersihkan;
- tanpa musik, tanpa derau kipas, tanpa `--denoise`;
- nada bicara menjelaskan ke teman, bukan membacakan pengumuman.

Rekaman bersih yang napasnya sudah dibuang mengajarkan model bahwa "tanpa napas" itu keadaan normal. Itulah sumber keluhan suara yang tidak pernah bernapas di tengah paragraf.

```python
# satu rekaman dipakai untuk ke-16 paragraf, tanpa langkah acuan terpisah
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts-v2.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --reference-wav "/content/drive/MyDrive/video-puu/rekaman-saya.wav" \
  --steps 25 --cfg 1.7
```

Kalau memakai suara sendiri, tidak ada urusan izin. Kalau memakai suara orang lain, izin tertulis wajib untuk luaran yang dipublikasikan; keterangan narasi berbantuan AI tetap dicantumkan di deskripsi video.

### 6.3 Dua parameter yang belum dipakai

Skrip render sudah punya keduanya, tetapi keduanya belum diisi di panduan mana pun.

| Parameter | Bawaan | Untuk natural | Alasan dari dokumentasi |
| :--- | :---: | :---: | :--- |
| `--steps` | 10 | **25** | `inference_timesteps` yang lebih tinggi menaikkan detail dan kenaturalan. Rentang yang dianjurkan 4–30; biaya waktunya linear dan pada 4090 tidak terasa |
| `--cfg` | 2.0 | **1.7** | Rentang 1,0–2,0 disebut lebih rileks dan natural, sedangkan di atas 2,0 menambah risiko derau dan artefak |

Pengaruhnya nyata tetapi tidak sebesar dua tuas di atas. Jangan menaikkan `--steps` melewati 30; hasilnya melandai.

### 6.4 Non-verbal tag, dan kenapa video ini sebaiknya tidak memakainya

Dokumentasi VoxCPM2 menyediakan tag non-verbal di dalam teks, ditulis huruf kecil di dalam kurung siku: `[Uhm]`, `[sigh]`, `[laughing]`. Kalimat dokumentasinya langsung: dipakai untuk membuat hasil tidak terasa mekanis. Aturannya dipakai hemat, jangan menumpuk beberapa tag dalam satu kalimat.

Untuk video laporan resmi, saya tidak akan memakainya sama sekali. Satu `[sigh]` atau `[laughing]` di narasi akademik terbaca sebagai sandiwara dan memancing pertanyaan yang tidak perlu dari penilai. Kalau tetap ingin mencoba, batasi pada satu `[Uhm]` di awal satu paragraf saja, dan dengarkan hasilnya sebelum memutuskan.

### 6.5 Yang tidak perlu diubah

Naskahnya sendiri sudah ditulis untuk telinga: kalimat pendek dengan panjang yang bervariasi, tanpa em dash, angka sebagai kata, enumerasi eksplisit. Kerataan yang kamu dengar datang dari suaranya, bukan dari tulisannya. Membongkar naskah untuk memperbaiki masalah suara hanya memindahkan masalahnya.

---

## Ringkasan Perintah

```bash
# lihat rencana
python scripts/video/render_narasi.py naskah-tts.txt --dry-run

# draft tanpa GPU
python scripts/video/render_narasi.py naskah-tts.txt --engine edge --out out_draft

# LANGKAH 1: buat satu paragraf acuan, ulangi sampai suaranya cocok
python scripts/video/render_narasi.py naskah-tts-v2.txt --out acuan --only 1 \
  --voice-desc "(a middle-aged male narrator with a warm, slightly husky low register and audible breath, measured pace, as if explaining the work to one colleague in a quiet room)" \
  --steps 25 --cfg 1.7

# JALUR LEBIH BAIK: rekam suara sendiri 20-30 detik, pakai sebagai acuan semua paragraf
python scripts/video/render_narasi.py naskah-tts-v2.txt --out out \
  --reference-wav rekaman-saya.wav --steps 25 --cfg 1.7

# LANGKAH 2: render semua paragraf dengan suara terkunci dari acuan
python scripts/video/render_narasi.py naskah-tts-v2.txt --out out \
  --reference-wav acuan/narasi_01.wav --steps 25 --cfg 1.7

# render ulang satu paragraf
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --reference-wav acuan/narasi_01.wav --only 4 --force

# kloning hi-fi, kalau kloning referensi masih kurang mirip
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --reference-wav acuan/narasi_01.wav --prompt-wav acuan/narasi_01.wav \
  --prompt-text "transkrip kata per kata dari audio acuan"
```

Ringkasnya: `--voice-desc` menentukan suara **sekali** untuk membuat acuan, lalu `--reference-wav` yang mengunci suara itu untuk sisanya. Jangan memakai `--voice-desc` sendirian untuk 15 paragraf, hasilnya akan berganti-ganti suara.
