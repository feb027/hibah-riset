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

### Sel 4 — render

```python
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --voice-desc "(Pria muda, suara tenang dan jelas, tempo sedang, gaya narasi dokumenter)" \
  --seed 42
```

Unduhan model pertama kali makan waktu beberapa menit. Setelah itu tiap paragraf sekitar 5–15 detik pada T4.

**Hasilnya langsung masuk Google Drive.** Jadi kalau sesi Colab putus di tengah, tinggal jalankan ulang Sel 1, 2, dan 4 — paragraf yang sudah jadi akan dilewati otomatis dan proses lanjut dari yang belum.

### Ganti warna suara

Coba beberapa deskripsi di *Voice Design*, lalu pilih satu dan pakai deskripsi itu untuk semua paragraf:

- `(Wanita muda, suara hangat, tempo tenang)`
- `(Pria dewasa, suara berat dan mantap, tempo lambat, gaya berita)`
- `(Suara netral, jelas, tempo sedang, tanpa emosi berlebih)`

Yang penting deskripsi dan `--seed` harus sama persis di seluruh paragraf, supaya warnanya konsisten. Kalau ada satu paragraf yang hasilnya kurang enak, render ulang paragraf itu saja:

```python
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --voice-desc "(Pria muda, suara tenang dan jelas, tempo sedang, gaya narasi dokumenter)" \
  --seed 42 --start 4 --force
```

`--start 4` artinya mulai dari paragraf keempat, dan `--force` menimpanya.

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
| Sebutir kata terucap salah | Perbaiki di `naskah-tts.txt` saja, lalu render ulang paragraf itu dengan `--start N --force`. Naskah asli tidak perlu disentuh. |
| `edge-tts` mengembalikan 403 | Versi lama. `pipx upgrade edge-tts`. |
| Semua paragraf terdengar seperti orang berbeda | `--voice-desc` atau `--seed` berubah antar render. Pakai nilai yang sama persis. |
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

# final dengan VoxCPM2
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --voice-desc "(Pria muda, suara tenang, tempo sedang)" --seed 42

# render ulang satu paragraf
python scripts/video/render_narasi.py naskah-tts.txt --out out \
  --voice-desc "(...)" --seed 42 --start 4 --force
```
