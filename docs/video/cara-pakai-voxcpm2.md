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

**Jangan langsung render 15 paragraf.** Voice Design dari teks tidak menghasilkan suara yang sama antar pemanggilan — dokumentasi resminya sendiri menyebut hasilnya *"a bit like hiring a new voice actor each time"*. Itu sebabnya paragraf 1 dan 2 kamu terdengar seperti dua orang berbeda.

Jalan keluarnya: buat **satu** paragraf contoh, dengarkan, kalau bagus simpan filenya sebagai acuan, lalu semua paragraf lain mengkloning file itu.

```python
!cd /content && mkdir -p acuan && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out acuan --only 1 \
  --voice-desc "(Pria muda, suara tenang dan jelas, tempo agak cepat, gaya narasi dokumenter)"
```

Dengarkan `acuan/narasi_01.wav`. Belum cocok? Ulangi perintah yang sama dengan `--force` dan deskripsi suara yang disesuaikan. Dokumentasi VoxCPM2 menyarankan mencoba 1–3 kali untuk mendapat suara yang diinginkan. Deskripsi yang bisa dipakai:

| Bagian | Contoh |
| :--- | :--- |
| Identitas | `Pria muda`, `Wanita dewasa`, `Narator pria paruh baya` |
| Tekstur | `suara tenang dan jelas`, `suara berat dan mantap` |
| Tempo dan gaya | `tempo agak cepat`, `tempo sedang`, `gaya narasi dokumenter` |
| Emosi | `tanpa emosi berlebih`, `hangat`, `tegas` |

Beberapa variasi yang bisa dicoba:

- `(Wanita muda, suara hangat, tempo sedang, gaya narasi dokumenter)`
- `(Pria dewasa, suara berat dan mantap, tempo sedang, gaya berita)`
- `(Suara netral, jelas, tempo agak cepat, tanpa emosi berlebih)`

Kalau ada yang lambat, tambahkan `tempo agak cepat`. Kalau terlalu datar, tambahkan `hangat` atau `tegas`.

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
- **Kontrol tempo masih bisa.** Tambahkan `--voice-desc "(tempo agak cepat)"` di samping `--reference-wav`. Ini mengubah gaya, bukan timbre, jadi suara tetap konsisten dengan acuan.

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

Satu batasan mode ini: `--voice-desc` tidak bisa dipakai bersamaan, karena dokumentasi VoxCPM2 melarang kontrol instruksi digabung dengan transkrip prompt. Jadi pilih salah satu, kontrol tempo atau kemiripan maksimum.

### Tidak ada opsi "render sekaligus"

Dua alasan kenapa narasi dipecah per paragraf:

1. **Batas keras 4096 token** pada parameter `max_len`. Satu paragraf di berkas ini saja memakai ratusan token, jadi 15 paragraf jauh melewatinya.
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
  --voice-desc "(Pria muda, suara tenang dan jelas, tempo sedang, gaya narasi dokumenter)" \
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
| Render jalan terus padahal cuma mau satu paragraf | Kamu memakai `--start 1`, yang artinya "dari paragraf 1 sampai habis". Untuk satu paragraf saja pakai `--only 1`. |
| Suara terasa lambat | Tambahkan `--voice-desc "(tempo agak cepat)"` di samping `--reference-wav`. Mengubah gaya, bukan timbre. |
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

## Ringkasan Perintah

```bash
# lihat rencana
python scripts/video/render_narasi.py naskah-tts.txt --dry-run

# draft tanpa GPU
python scripts/video/render_narasi.py naskah-tts.txt --engine edge --out out_draft

# LANGKAH 1: buat satu paragraf acuan, ulangi sampai suaranya cocok
python scripts/video/render_narasi.py naskah-tts.txt --out acuan --only 1 \
  --voice-desc "(Pria muda, suara tenang dan jelas, tempo agak cepat)"

# LANGKAH 2: render semua paragraf dengan suara terkunci dari acuan
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --reference-wav acuan/narasi_01.wav

# render ulang satu paragraf
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --reference-wav acuan/narasi_01.wav --only 4 --force

# kloning hi-fi, kalau kloning referensi masih kurang mirip
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --reference-wav acuan/narasi_01.wav --prompt-wav acuan/narasi_01.wav \
  --prompt-text "transkrip kata per kata dari audio acuan"
```

Ringkasnya: `--voice-desc` menentukan suara **sekali** untuk membuat acuan, lalu `--reference-wav` yang mengunci suara itu untuk sisanya. Jangan memakai `--voice-desc` sendirian untuk 15 paragraf, hasilnya akan berganti-ganti suara.
