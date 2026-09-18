# Riset Text-to-Speech untuk Video Penelitian PUU 2026

Disusun 18 September 2026. Semua harga, versi, dan ketersediaan diverifikasi pada tanggal tersebut.

---

## 0. Kebutuhan dan Besaran yang Harus Dipenuhi

Video contoh yang diberikan adalah video luaran hibah PUU 2025, *Sistem Cerdas Pengenalan dan Perhitungan Objek Ikan secara Realtime Berbasis Optimasi YoloV11*. Transkrip otomatis video itu memperlihatkan pola yang penting: narasi Bahasa Indonesia formal, satu suara tunggal sepanjang video, dengan musik latar. Transkripnya juga memperlihatkan masalah pelafalan yang khas: "Yolo V11" dieja huruf per huruf, "conveyor" menjadi "convior", "occlusion" menjadi "oclusion", "Siliwangi" menjadi "liwangi", dan "artificial intelligence" menjadi "artifisial inteligi".

Itu bukan masalah modelnya bagus atau tidak, melainkan masalah model TTS mana pun yang tidak mengenal istilah teknis. Bagian 5 di bawah membahas cara menanganinya.

Untuk durasi 4–5 menit, narasi formal Bahasa Indonesia pada tempo presentasi berada di kisaran 130–150 kata per menit. Artinya kebutuhan teksnya sekitar **600–750 kata, atau ±4.000–5.000 karakter** termasuk spasi. Angka ini yang membuat hampir semua kuota gratis di bawah cukup untuk satu video, bahkan beberapa kali revisi.

Persyaratan yang dipakai untuk menyaring kandidat: dukungan Bahasa Indonesia asli, bisa dipakai gratis, bisa dijalankan sendiri di RTX 4090 kampus, dan lisensinya tidak menghalangi pemakaian pada luaran penelitian.

---

## 1. Rekomendasi

### 1.1 Pilihan utama: VoxCPM2

**OpenBMB/VoxCPM2**, dirilis April 2026, lisensi **Apache-2.0** untuk kode dan bobot. Ini pilihan terkuat untuk kasus ini dan jaraknya cukup jauh dari kandidat lain.

| Aspek | Nilai |
| :--- | :--- |
| Parameter | 2B, backbone MiniCPM-4 |
| Bahasa | 30, **termasuk Indonesia**, tanpa perlu penanda bahasa |
| Keluaran audio | 48 kHz (masukan referensi 16 kHz di-*upscale* internal) |
| Fitur | *Voice Design* (buat suara baru dari deskripsi teks), *Controllable Cloning*, *Ultimate Cloning* |
| RTF di RTX 4090 | ~0,3 (klaim vendor); ~0,13 dengan Nano-vLLM |
| VRAM | ~8 GB menurut tabel resmi repo; terukur 5,76 GB puncak pada benchmark independen |
| Lisensi | Apache-2.0, bebas komersial |

Bukti independen yang paling relevan datang dari repositori `paksopi/Text-to-Speech-Analysis` (Juli 2026, MIT). Repositori itu membandingkan **10 model TTS pada perangkat yang sama** (RTX 3050 Laptop, 6 GB VRAM) dengan kalimat uji yang sama, lalu menilainya dengan empat metrik objektif, bukan klaim pemasaran. Hasilnya:

- Dari 10 model yang diuji, **hanya VoxCPM2 dan Piper yang punya dukungan Bahasa Indonesia**, dan hanya VoxCPM2 yang juga mendukung Melayu.
- WER (kata yang dihasilkan dibanding teks yang diminta, diukur lewat transkripsi Whisper) untuk VoxCPM2 adalah **0,0000 pada keenam generasi EN/BM/ID**.
- Kemiripan suara pada mode kloning: 0,94 untuk sesama bahasa, 0,85 lintas bahasa.
- Model lain terhenti di Inggris saja, atau Inggris+Tionghoa: XTTSv2 (17 bahasa, tanpa Indonesia), StyleTTS2, Parler-TTS, ChatTTS, F5-TTS.

Catatan penting soal angka di atas: itu n=1 per kondisi, jadi sah untuk melihat jarak besar antar model, tidak sah untuk meranking selisih kecil. Repositori itu sendiri menyatakannya demikian.

**Keterbatasan yang perlu diketahui sebelum dipakai.** Dokumentasi VoxCPM2 mengakui stabilnya menurun pada teks panjang, sehingga narasi 5 menit harus dipotong per paragraf lalu disambung. `torch.compile` juga **tidak membantu** untuk pemakaian sekali-sekali: benchmark komunitas mengukur mode *compiled* justru 10–20 kali lebih lambat daripada *eager* karena grafnya dikompilasi ulang untuk setiap bentuk masukan baru. Untuk keperluan video ini, jalankan apa adanya tanpa `optimize=True`.

Satu keterbatasan lagi yang paling mudah menjebak, dan tertulis di halaman *A Voice Chef's Guide*: **hasil *Voice Design* dari teks tidak konsisten antar pemanggilan.** Kalimat aslinya, *"Because of the model's creative nature, every generation can still have subtle, unique variations, a bit like hiring a new voice actor each time."* Usage Guide malah menyatakannya lebih tegas: *"If you do not provide a reference audio, VoxCPM generates a random voice each time."* Artinya, membuat 15 paragraf dengan satu deskripsi suara yang sama tetap menghasilkan 15 suara yang berbeda-beda. Yang mengunci suara adalah **kloning dari berkas audio acuan**, bukan deskripsi teks dan bukan *seed*. Alur yang benar adalah membuat satu paragraf contoh, memilih hasil terbaik, lalu menjadikan berkas itu acuan `reference_wav_path` untuk seluruh paragraf sisanya.

Satu hal kecil yang menentukan berhasil atau tidaknya deskripsi suara: **instruksinya hanya dipahami dalam Bahasa Inggris dan Bahasa Mandarin.** Usage Guide menuliskan, *"Chinese and English are both supported in the instruction."* Deskripsi berbahasa Indonesia dilewati begitu saja dan model kembali ke suara acak. Jadi tulis `(a young male narrator, calm and clear, brisk pace)`, bukan `(Pria muda, suara tenang, tempo agak cepat)`. Isi teks yang akan diucapkan tetap Bahasa Indonesia; hanya instruksi di dalam tanda kurung yang harus Bahasa Inggris.

Rinciannya ada di `docs/video/cara-pakai-voxcpm2.md` Sel 4 dan 5.

Perintah pemakaiannya:

```bash
pip install voxcpm soundfile
```

```python
from voxcpm import VoxCPM
import torch
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False)

torch.manual_seed(42)
wav = model.generate(
    text="Pengelolaan ruang publik menuntut informasi jumlah orang yang cepat dan akurat.",
    cfg_value=2.0,
    inference_timesteps=10,
)
sf.write("narasi_01.wav", wav, model.tts_model.sample_rate)
```

Untuk membuat suara tanpa merekam siapa pun, pakai *Voice Design* dengan deskripsi di dalam tanda kurung di awal teks. Pakai ini untuk membuat **satu** paragraf acuan saja, bukan untuk seluruh naskah:

```python
wav = model.generate(
    text="(a young male narrator, calm and clear, brisk pace)Selamat pagi, semuanya.",
    cfg_value=2.0,
    inference_timesteps=10,
)
```

**Konsekuensi praktis untuk video ini:** narasi 5 menit cukup dihasilkan sekali, dan penyesuaian tempo bisa dilakukan di editor video tanpa perlu membuat ulang. RTF 0,3 pada 4090 berarti audio 5 menit selesai dalam sekitar 1,5 menit proses, ditambah waktu pemuatan model.

### 1.2 Kalau tidak mau pasang apa pun: Google Cloud Text-to-Speech, Chirp 3 HD

Ini jalur tercepat dan tetap gratis untuk kebutuhan satu video.

- **Kuota gratis Chirp 3: HD adalah 0–1 juta karakter per bulan.** Narasi 5 menit hanya memakai ±5.000 karakter, sekitar 0,5% dari kuota.
- **`id-ID` termasuk locale yang didukung Chirp 3: HD** (daftar locale pada catatan rilis Google Cloud mencantumkan `id-ID` bersama `hi-IN`, `it-IT`, `ja-JP`, dan lainnya).
- Setelah kuota habis, tarifnya US$30 per 1 juta karakter, jadi bahkan kelebihan kuota pun tidak relevan untuk skala ini.
- Kuota gratis untuk WaveNet dan Standard malah 0–4 juta karakter, tetapi kualitasnya satu generasi di bawah Chirp 3 HD.
- Gemini-TTS tidak punya kuota gratis dan tagihannya berbasis token audio.

Catatan operasional: layanan ini mewajibkan pengaktifan penagihan pada proyek Google Cloud, jadi kartu tetap harus terdaftar meskipun pemakaiannya di bawah kuota gratis.

### 1.3 Pelengkap untuk cek cepat: edge-tts

`rany2/edge-tts` memakai layanan TTS bawaan Microsoft Edge lewat Python, tanpa kunci API dan tanpa biaya. Suara Indonesia yang tersedia adalah `id-ID-GadisNeural` dan `id-ID-ArdiNeural`.

Dua alasan kenapa ini **bukan** pilihan utama untuk video institusi:

1. Ini bukan API resmi. Layanan itu bisa dan sudah beberapa kali memblokir klien dengan galat `403 WSServerHandshakeError`, terakhir diperbaiki pada versi 7.2.7 lewat pembaruan token `Sec-MS-GEC`. Artinya, kalau `pip` di mesin kampus memasang versi lama, hasilnya galat, bukan suara.
2. Pakai layanan tidak resmi untuk luaran penelitian yang dipublikasikan itu berisiko dari sisi ketentuan layanan.

Tetap berguna untuk membuat *draft* narasi cepat sebelum masuk ke model yang sebenarnya.

```bash
pipx install edge-tts
edge-tts --voice id-ID-ArdiNeural --rate=+0% \
  --text "Pengelolaan ruang publik menuntut informasi jumlah orang yang cepat." \
  --write-media draft.mp3
```

### 1.4 Model ringan untuk CPU atau kartu 8 GB

Kalau 4090 tidak bisa dipakai dan harus jalan di PC rumah:

| Model | Ukuran | Kecepatan | Kualitas | Catatan |
| :--- | :--- | :--- | :--- | :--- |
| Piper (dan turunannya, NusaVoice) | puluhan MB | 0,3 detik per kalimat, CPU | Cukup, agak datar | Satu-satunya selain VoxCPM2 yang mendukung Indonesia di benchmark 10 model |
| MMS-TTS `ind` (Meta, VITS) | 36M param, 0,47 GB | Cepat di CPU | Datar, jelas, tanpa kloning | WER 0,0000 pada benchmark |
| Pocket TTS Indonesian | 438 MB (varian 6 lapis) | 2,23× realtime di CPU | Terbatas | WER median 12,50%, kemiripan suara 0,938 |
| F5-TTS-INDO-FINETUNE-V2 | — | GPU | Bagus untuk kloning | Lisensi **CC-BY-NC-4.0**, tidak untuk pemakaian komersial |

Pocket TTS Indonesian pantas dibahas lebih detail karena sekilas cocok: dibangun di atas `kyutai/pocket-tts`, dilatih pada 502 jam data LEMAS, dan berjalan di CPU tanpa GPU. Masalahnya ada di kualitas sumber. Datanya berasal dari audio 16 kHz, sedangkan arsitektur Mimi berjalan pada 24 kHz, sehingga tidak ada energi di atas 8 kHz untuk dipelajari. UTMOS-nya 2,68, sedangkan model Inggris Pocket TTS mencapai 4,36. Penulis model card-nya sendiri menulis harapan realistisnya: "sekitar kualitas panggilan telepon atau video YouTube, bukan rekaman studio". Ditambah lagi angka harus ditulis sebagai kata (`lima belas`, bukan `15`) dan tanda seru tidak ada dalam kosakata. Untuk narasi video penelitian, itu terlalu banyak kompromi.

---

## 2. Tabel Keputusan Ringkas

| Kandidat | Gratis | Bahasa Indonesia | Kloning suara | Jalan di mana | Lisensi | Putusan |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **VoxCPM2** | Ya (self-host) | Ya, native | Ya | 4090, Colab T4, atau Space resmi; RX 6600 berisiko | Apache-2.0 | **Pakai ini** |
| Google Chirp 3 HD | 1 jt karakter/bln | Ya (`id-ID`) | Fitur terpisah, berbayar | Cloud | Ketentuan vendor | **Cadangan terbaik** |
| edge-tts | Ya | Ya (Gadis, Ardi) | Tidak | Klien mana pun | Tidak resmi | Untuk draft saja |
| Piper / NusaVoice | Ya | Ya | Tidak | CPU | MIT/varies | Kalau tanpa GPU |
| MMS-TTS `ind` | Ya | Ya | Tidak | CPU | CC-BY-NC 4.0 | Sangat ringan, suara datar |
| Pocket TTS Indonesian | Ya | Ya | Ya | CPU | CC-BY-4.0 | Kualitas 16 kHz, jangan untuk final |
| F5-TTS-INDO-V2 | Ya | Ya | Ya | GPU | CC-BY-NC-4.0 | Non-komersial saja |
| Qwen3-TTS | Ya | Tidak (10 bahasa) | Ya | GPU | Apache-2.0 | Ada finetune komunitas 0,9B, kualitas tak terverifikasi |
| Chatterbox Multilingual V3 | Ya | Tidak (ada Melayu, bukan Indonesia) | Ya | GPU | MIT | Gagal syarat bahasa |
| XTTSv2 (Coqui) | Ya | Tidak (17 bahasa, tanpa ID) | Ya | GPU | Coqui CPML | Gagal syarat bahasa |
| ElevenLabs | 10 rb karakter/bln | Ya | Ya | Cloud | Ketentuan vendor | Kualitas terbaik, tapi layanan luar |

Catatan tentang tiga model yang sering muncul di daftar "TTS gratis terbaik": MeloTTS, Fish Speech, dan CosyVoice 2.0 **tidak berhasil dipasang** pada benchmark independen di atas, karena paket PyPI-nya rusak atau tidak lengkap. Jangan masukkan ke rencana sebelum diuji sendiri.

---

## 3. Perangkat: RTX 4090 vs RX 6600

**RTX 4090 (kampus).** VoxCPM2 tercatat ~8 GB VRAM pada tabel resmi repo, dengan pengukuran independen 5,76 GB puncak pada kalimat pendek. Pada 24 GB, jalur ini tidak punya kendala berarti.

**RX 6600 (rumah).** Dua masalah bertumpuk. Pertama, kartu ini berarsitektur `gfx1032` dan **tidak didukung resmi oleh ROCm**. Praktik yang berhasil dipakai banyak orang adalah memaksa ROCm memperlakukannya sebagai arsitektur terdekat yang didukung:

```bash
export HSA_OVERRIDE_GFX_VERSION=10.3.0
```

Dengan nilai itu, RX 6600 dan kartu RDNA 2 di bawah RX 6800 bisa menjalankan ROCm 6.2+. VoxCPM2 sendiri butuh PyTorch ≥2.5 dan CUDA ≥12.0; versi ROCm dari PyTorch tidak selalu setara fiturnya, sehingga jalur ini berstatus "mungkin bisa", bukan "pasti bisa".

Kedua, kapasitas memori. RX 6600 hanya punya 8 GB, sedangkan tabel resmi VoxCPM2 mencantumkan kebutuhan ~8 GB. Model sebesar 2B memang bisa dipaksa muat kalau angkanya ditekan, tetapi 8 GB persis di batas kebutuhan bukan tempat yang nyaman untuk bekerja. Kalau jalur ROCm gagal, jangan buang waktu menambal: pakai bagian 1.4 untuk draft, lalu render final di 4090 kampus atau di Colab.

Satu hal yang perlu diingat: Pocket TTS **tidak mendapat percepatan dari GPU sama sekali**. Penulisnya menguji dan tidak melihat percepatan, karena modelnya kecil dan *batch size*-nya 1. Jadi kalau jatuh ke model ini, GPU tidak menolong.

---

## 4. Jalur Menjalankan: Colab dan Web

Pertanyaan praktisnya: apakah harus memasang sendiri di komputer. Jawabannya tidak.

### 4.1 Lewat web, tanpa memasang apa pun

Ada demo resmi dari OpenBMB: **`openbmb/VoxCPM-Demo`** di Hugging Face Spaces. Space itu berjalan dengan Gradio, berlisensi Apache-2.0, dan statusnya *pinned*, artinya selalu aktif dan tidak perlu menunggu *cold start*. Isinya mencakup VoxCPM2 beserta antarmuka untuk *voice design* dan kloning. Untuk sekadar mencoba dan memilih warna suara, ini jalur tercepat.

Halaman sampel audio resmi juga tersedia di `openbmb.github.io/voxcpm2-demopage` untuk mendengar hasilnya sebelum memutuskan.

Yang perlu diperhatikan: Space publik adalah layanan bersama, jadi ada antrean dan batas durasi per permintaan. Untuk narasi 5 menit yang harus dirender utuh dan konsisten, jangan bergantung pada Space. Pakai Space untuk memilih suara, lalu render final di Colab atau di 4090.

Selain itu ada `voxcpm.app`, yang bukan milik OpenBMB dan memakai sistem kredit evaluasi gratis. Untuk luaran penelitian, pakai yang resmi.

### 4.2 Di Google Colab

Bisa, dan ini jalur gratis paling praktis kalau 4090 kampus sedang dipakai orang lain.

Runtime Colab saat ini memakai **Python 3.12.13** dengan **PyTorch 2.11.0** (runtime 2026.07). Keduanya masuk syarat VoxCPM, yaitu Python ≥3.10 dan <3.13 serta PyTorch ≥2.5. GPU gratisnya, T4 dengan 16 GB VRAM, cukup untuk kebutuhan ~8 GB.

Isi satu sel dengan ini:

```python
!pip install -q voxcpm soundfile

from voxcpm import VoxCPM
import torch
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False)

torch.manual_seed(42)
wav = model.generate(
    text="Pengelolaan ruang publik menuntut informasi jumlah orang yang cepat dan akurat.",
    cfg_value=2.0,
    inference_timesteps=10,
)
sf.write("narasi_01.wav", wav, model.tts_model.sample_rate)
```

Tiga hal yang harus diantisipasi:

1. **Bobot diunduh ulang setiap sesi baru.** Colab gratis tidak menyimpan model antar sesi, jadi setiap kali membuka notebook ada unduhan beberapa GB sebelum bisa bicara. Jangan tutup sesi sebelum semua paragraf selesai dirender.
2. **Sesi gratis bisa terputus.** Render per paragraf, simpan tiap hasil ke Google Drive dengan `from google.colab import drive; drive.mount('/content/drive')`, lalu tulis keluaran ke folder Drive. Kalau sesi mati di tengah, yang sudah jadi tidak hilang.
3. **Kalau `pip install voxcpm` menolak karena versi Python.** Jarang terjadi: metadata paket `voxcpm` 2.0.3 hanya mensyaratkan `>=3.10` tanpa batas atas, dan pemasangan pada Colab Python 3.13 sudah terbukti berhasil. Kalau tetap gagal, pin runtime Colab ke versi 2026.07 lewat *Runtime → Change runtime type → Runtime version*, lalu ulangi.
4. **`optimize` defaultnya aktif.** `VoxCPM.from_pretrained(...)` memakai `optimize=True`, yang menyalakan `torch.compile`. Untuk pemakaian sekali-sekali itu merugikan, karena graf dikompilasi ulang untuk setiap panjang teks baru. Skrip pada repositori ini mematikan opsi itu secara default; pemanggilan manual sebaiknya menulis `optimize=False`.
5. **Tidak ada parameter `seed`.** `generate()` pada `voxcpm` 2.0.3 menerima `text`, `cfg_value`, `inference_timesteps`, `prompt_wav_path`, `reference_wav_path`, dan beberapa opsi panjang keluaran. Untuk hasil yang dapat diulang, atur `torch.manual_seed(42)` sebelum tiap pemanggilan. Contoh README di GitHub menyebut `seed=42`, tetapi versi paket yang terpasang belum menerimanya.

Notebook komunitas juga sudah ada, misalnya `SWAG456/voxcpm2-tools` yang menyertakan `VoxCPM2_Colab_Notebook.ipynb` untuk T4 gratis, dan notebook Gradio dari `TeamAIQ/Colab-notebooks`. Keduanya bukan keluaran resmi OpenBMB, jadi periksa isinya sebelum dipakai dan jangan jalankan sel yang tidak Anda pahami. Perintah `pip install` di atas sudah cukup; notebook komunitas hanya menambah antarmuka.

### 4.3 Web demo lokal, tanpa Colab dan tanpa internet setelah model terunduh

Repo VoxCPM menyertakan antarmuka web sendiri:

```bash
python app.py --port 8808
```

Lalu buka `http://localhost:8808`. Cocok kalau mau mengulang render berkali-kali tanpa mengunggah apa pun ke luar, asalkan 4090 kampus atau mesin dengan GPU yang cocok bisa diakses.

### Ringkasan jalur

| Cara | Perlu pasang | Gratis | Cocok untuk |
| :--- | :---: | :---: | :--- |
| Space `openbmb/VoxCPM-Demo` | Tidak | Ya | Memilih warna suara dan uji cepat |
| Google Colab (T4, 16 GB) | Tidak | Ya | Render narasi final tanpa mengganggu 4090 |
| `app.py` lokal | Ya | Ya | Render berulang, data tidak keluar dari mesin |
| RTX 4090 kampus | Ya | Ya | Jalur tercepat dan paling stabil |

---

## 5. Yang Sebaiknya Dihindari

**Kloning suara orang lain tanpa izin.** Semua model di atas bisa mengkloning suara dari beberapa detik rekaman. Untuk video penelitian yang dipublikasikan, jangan mengkloning suara anggota tim, dosen, atau narator apa pun tanpa izin tertulis. Pakai *Voice Design* VoxCPM2 supaya tidak menyerupai siapa pun, atau rekam sendiri suaranya dan kloning suara sendiri.

**Menandai audio sintetis.** VoxCPM2 dan Chatterbox menyisipkan tanda air pada keluarannya, dan dokumen mereka meminta pengguna menandai konten yang dihasilkan AI. Cantumkan keterangan kecil di deskripsi video.

**Dua kali kompilasi.** Jangan aktifkan `optimize=True` atau `torch.compile` untuk pemakaian sekali-sekali. Terukur 10–20 kali lebih lambat.

**Memasukkan seluruh naskah sekaligus.** Dokumentasi VoxCPM2 mengakui ketidakstabilan pada teks panjang. Potong per paragraf, render terpisah, sambungkan di editor. Ini juga mempermudah revisi kalau ada satu kata yang salah lafal.

---

## 6. Menangani Pelafalan Istilah Teknis

Ini bagian yang membuat hasil akhir terlihat profesional atau tidak, dan model sekelas apa pun tidak akan menyelesaikannya sendiri. Semua TTS membaca teks apa adanya, sedangkan naskah penelitian penuh singkatan yang tidak pernah ada di data pelatihan mana pun.

Karena itu, yang diumpankan ke mesin TTS sebaiknya bukan naskah asli, melainkan versi yang sudah ditulis ulang secara fonetis. Simpan dua versi: naskah asli untuk subtitle, versi fonetis untuk sintesis.

| Di naskah | Ditulis untuk TTS | Alasan |
| :--- | :--- | :--- |
| YOLO26 | Yolo dua puluh enam | Menghindari pengejaan huruf dan angka yang salah baca |
| YOLOv11 | Yolo vee sebelas | "v" dibaca "vee", bukan "ve" |
| DiffMOT | Dif Mot | Menghindari "diffmot" jadi satu suku kata aneh |
| OC-SORT | Ok Sort | Sama seperti video 2025, "OC" cenderung dieja |
| Deep-OC-SORT | Dip Ok Sort | "Deep" dibaca "dip", bukan "dep" |
| LightTrack-ReID | Lait Trek Ar I D | "ReID" hampir pasti salah baca |
| HOTA | Hota | Bukan "H-O-T-A" |
| MOTA | Mota | Sama |
| IDF1 | I D F satu | Angka ditulis kata |
| mAP | em A P | Kalau ditulis "mAP" bisa terbaca "map" |
| IoU | ai ou yu | |
| RoI | ar ou ai | Kalau ditulis "RoI" bisa terbaca "roy" |
| CrowdHuman | Kraud Hyuman | |
| MOT20 | Em O Te dua puluh | |
| DanceTrack | Dens Trek | |
| Siliwangi | Siliwangi | Video 2025 salah baca ini jadi "liwangi" |
| RANCAGE | Rancage | Dibaca sebagai satu kata, bukan dieja |
| conveyor | konveyor | Sesuai ejaan Indonesia |
| occlusion | oklusi | Video 2025 memakai "oclusion" |
| real-time | riil taim | |
| dataset | de-ta-set | |
| tracking | tre-king | |
| YOLO26n | Yolo dua puluh enam en | Ditambahkan untuk naskah v3 |
| YOLO26s | Yolo dua puluh enam es | |
| YOLOv10n | Yolo vee sepuluh en | |
| YOLOv11n | Yolo vee sebelas en | |
| Multi-Object Tracking | Multi Objek Tre king | Spasi, bukan tanda hubung |
| TrackEval | Trek Eval | |
| RoI polygon | ar ou ai poligon | |
| ID State Memory | I D steit memori | |
| state machine | steit mesin | |
| cooldown | masa tunggu | Lebih aman dibaca daripada "cooldown" |
| naive line crossing | lain krosing naif | |
| line counting | lain kaunting | |
| counting logic | kaunting logik | |
| end-to-end | end tu end | |
| NVIDIA RTX 4090 | Envidia ar te eks empat ribu sembilan puluh | |
| edge device | perangkat ej | |
| Jetson | Jet son | |
| pruning | pemangkasan | |
| ground truth | graund trut | |
| CCTV | si si ti vi | |
| JESTEC | Jes tek | |
| HKI | ha ka i | Di naskah v3 tertulis "Hak Cipta", jadi tidak dipakai |
| identity switch | pergantian identitas | |
| occlusion | oklusi | |

Dua aturan umum yang berlaku untuk semua model di daftar ini: **tulis angka sebagai kata** (`lima ratus orang`, bukan `500 orang`), dan **hindari singkatan yang tidak diucapkan sebagai kata**.

Tempo narasi juga lebih baik diatur di editor video daripada lewat parameter model, supaya setiap paragraf punya kecepatan yang konsisten.

---

## 7. Rencana Eksekusi

1. **Buat naskah 600–750 kata** terpisah dari bagian laporan, dibagi per paragraf.
2. **Buat versi fonetis** memakai tabel bagian 6.
3. **Pilih warna suara di Space resmi** `openbmb/VoxCPM-Demo`, tanpa memasang apa pun. Simpan deskripsi suara yang terpilih.
4. **Render final**, pilih salah satu jalur: 4090 kampus, Colab T4 (bagian 4.2), atau `app.py` lokal.
   ```bash
   pip install voxcpm soundfile
   ```
   Render per paragraf dengan deskripsi suara dan `seed` yang sama untuk seluruh paragraf, supaya warnanya konsisten. Skrip ini mematikan `torch.compile` secara default (`optimize=False`), karena kompilasi justru memperlambat pemakaian sekali-sekali dan di T4 malah dilewati.
5. **Kalau semua GPU sedang tidak bisa dipakai**, render draft dengan `edge-tts --voice id-ID-ArdiNeural` sambil menyusun video, lalu ganti audio final setelah VoxCPM2 jalan. Timeline tetap sama, hanya audionya yang ditukar di akhir.
6. **Susun di editor**: audio, musik latar dengan level di bawah narasi, subtitle dari naskah asli (bukan versi fonetis), dan keterangan audio dihasilkan AI.

---

## Rujukan

1. OpenBMB, *VoxCPM2: Tokenizer-Free TTS for Multilingual Speech Generation, Creative Voice Design, and True-to-Life Cloning*, Apache-2.0. https://github.com/OpenBMB/VoxCPM — rilis April 2026, diakses 18 September 2026.
2. OpenBMB, *VoxCPM2 Technical Report*, arXiv:2606.06928, 2026.
3. `paksopi/Text-to-Speech-Analysis`, MIT, 2026. Perbandingan 10 model TTS untuk Melayu/Indonesia/Inggris dengan WER, kemiripan suara, VRAM, dan analisis prosodi. https://github.com/paksopi/Text-to-Speech-Analysis — dibuat 2 Juli 2026, diakses 18 September 2026.
4. `anak10thn/pocket-tts-indonesian`, CC-BY-4.0, 2026. https://huggingface.co/anak10thn/pocket-tts-indonesian
5. Kyutai Labs, *Pocket TTS*, 2026. https://kyutai-labs.github.io/pocket-tts/
6. Google Cloud, *Text-to-Speech pricing*, 2026. https://cloud.google.com/text-to-speech/pricing
7. Google Cloud, *Text-to-Speech release notes* dan *Chirp 3: HD voices*, 2026. https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd
8. `rany2/edge-tts`, versi 7.2.7, 2025. https://github.com/rany2/edge-tts
9. Resemble AI, *Chatterbox Multilingual V3*, MIT, 2026. https://github.com/resemble-ai/chatterbox
10. Qwen Team, *Qwen3-TTS Technical Report*, arXiv:2601.15621, Januari 2026.
11. Spheron, *VoxCPM2 VRAM Requirements* (kalkulator VRAM, estimasi 5,0 GB pada FP16 — angka resmi repo menulis ~8 GB, lihat rujukan 1). https://www.spheron.network/tools/gpu-recommender/openbmb/VoxCPM2/
12. RadeonOpenCompute, isu ROCm #1797 dan ROCm/ROCm #5069: penggunaan `HSA_OVERRIDE_GFX_VERSION=10.3.0` pada `gfx1032`. https://github.com/ROCm/ROCm/issues/5069
13. OpenBMB, *VoxCPM Demo*, Hugging Face Spaces (Gradio, Apache-2.0, *pinned*). https://huggingface.co/spaces/openbmb/VoxCPM-Demo — sebutan VoxCPM2 dengan antarmuka *voice design* dan kloning, diakses 18 September 2026.
14. OpenBMB, *VoxCPM2 Demo Page* (sampel audio resmi). https://openbmb.github.io/voxcpm2-demopage/
15. Google Colab, *Past Runtime Versions* dan `googlecolab/backend-info`: runtime 2026.07 memakai Python 3.12.13, numpy 2.0.2, PyTorch 2.11.0. https://research.google.com/colaboratory/runtime-version-faq.html — diakses 18 September 2026.
16. `SWAG456/voxcpm2-tools`, Hugging Face: `VoxCPM2_Colab_Notebook.ipynb` untuk T4 gratis dan skrip inferensi CPU. Bukan keluaran resmi OpenBMB. https://huggingface.co/SWAG456/voxcpm2-tools
17. OpenBMB, *Usage Guide*, VoxCPM 2.0 documentation — tiga mode generasi, *"Chinese and English are both supported in the instruction"*, *"If you do not provide a reference audio, VoxCPM generates a random voice each time"*, penalaan `cfg_value`. https://voxcpm.readthedocs.io/en/latest/usage_guide.html — diakses 18 September 2026.
18. OpenBMB, *A Voice Chef's Guide to VoxCPM2* — contoh kombinasi deskripsi suara dan catatan variasi antar generasi. https://voxcpm.readthedocs.io/en/latest/cookbook.html
19. OpenBMB/VoxCPM, issue #210, *Style control instructions ignored* — kontrol instruksi diabaikan pada mode kloning hi-fi, dikonfirmasi pengelola proyek; jalan keluar untuk tempo adalah audio acuan yang lebih cepat. https://github.com/OpenBMB/VoxCPM/issues/210 — dibuka 8 April 2026, diakses 18 September 2026 melalui `gh issue view 210`.
