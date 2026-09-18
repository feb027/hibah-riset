# Naskah Video Penelitian + Panduan Menulis untuk Model TTS

> **Sudah digantikan.** Berkas ini mendokumentasikan naskah v1, yang tidak lagi dipakai. Naskah yang berlaku sekarang adalah `naskah-asli-v3.txt` dan `naskah-tts-v3.txt`, hasil pecahan dari storyboard bertimecode dosen pembimbing, dan ringkasannya ada di `storyboard-v3.md`. Aturan penulisan di bawah masih berlaku seluruhnya; yang berganti hanya isi naskahnya.

Dua berkas naskah sudah jadi, siap diunggah ke Google Drive:

| Berkas | Isi | Dipakai untuk |
| :--- | :--- | :--- |
| `docs/video/naskah-asli.txt` | Ejaan normal, istilah teknis ditulis apa adanya | **Subtitle** dan naskah yang dibaca dosen |
| `docs/video/naskah-tts.txt` | Versi fonetis, angka dan singkatan ditulis sebagai kata | **Disintesis** oleh VoxCPM2 atau edge-tts |

Keduanya 15 paragraf, panjang 605 dan 662 kata. Perkiraan durasi 4,3–4,7 menit pada tempo 140 kata per menit. Seluruh angka di dalamnya berasal dari bagian *Hasil Pelaksanaan Penelitian* di `docs/laporan-kemajuan/bab-hasil-pelaksanaan-penelitian.md`, jadi tidak ada klaim baru yang tidak tertulis di laporan.

---

## Bagian 1. Panduan Menulis Naskah untuk Model TTS

Panduan ini disusun dari dokumentasi ElevenLabs, panduan penulisan naskah voiceover (YTVoice, Februari 2026), panduan penulisan untuk AI voice (Vois, Desember 2025), catatan model card `pocket-tts-indonesian`, dan dokumentasi VoxCPM2. Semuanya diringkas menjadi aturan yang benar-benar terpakai di naskah ini.

### 1. Tulis untuk telinga, bukan untuk mata

Pembaca bisa mengulang kalimat yang membingungkan. Pendengar tidak. Kalimat yang enak dibaca belum tentu enak didengar, terutama kalimat dengan anak kalimat bertingkat. Satu kalimat, satu ide.

Contoh dari panduan Vois:

> Buruk: "Ketika mempertimbangkan berbagai faktor yang berkontribusi pada efektivitas generasi suara termasuk tetapi tidak terbatas pada pemformatan naskah, pemilihan suara, serta perhatian pada tempo dan penekanan, satu hal yang harus disadari adalah elemen paling dasar tetap kualitas teks sumber itu sendiri."

> Baik: "Banyak faktor memengaruhi hasil generasi suara. Format naskah penting. Pemilihan suara penting. Tempo dan penekanan penting. Tapi fondasinya tetap kualitas teks sumber."

### 2. Jaga kalimat di bawah dua puluh lima kata

Panduan YTVoice menyarankan batas 25 kata; pengalaman praktis justru menaruh titik nyaman di 10–20 kata. Kalimat panjang membuat mesin mempercepat tempo atau kehilangan jeda alami.

Naskah di berkas ini sudah diperiksa: **kalimat terpanjang 19 kata, dari 63 kalimat.** Batas ini membuat mesin selalu punya titik berhenti yang jelas.

### 3. Tanda baca adalah notasi tempo, bukan hiasan

Setiap tanda baca adalah instruksi bagi mesin:

| Tanda | Efek |
| :--- | :--- |
| Koma | Jeda singkat, alur tetap jalan |
| Titik | Berhenti penuh, tempat bernapas |
| Tanda tanya | Intonasi naik secara alami |
| Elipsis | Jeda menggantung, untuk keraguan |
| **Em dash (—)** | **Hindari.** Sebagian besar mesin salah menafsirkannya |

Repositori ini punya kebiasaan memakai em dash di naskah laporan, tapi naskah video harus bersih dari tanda itu. Sudah dicek: **nol em dash, nol titik koma, nol tanda kurung** di kedua berkas.

Tanda hubung juga perlu hati-hati. Catatan `pocket-tts-indonesian` melaporkan tanda hubung pernah keluar sebagai kata baru di tengah frasa, sebelum penormalnya diperbaiki. Untuk naskah ini, tanda hubung hanya dipakai pada kata ulang yang memang baku (`bolak-balik`, `berkali-kali`).

### 4. Angka dan simbol ditulis sebagai kata

Ini aturan yang paling sering diabaikan dan paling sering merusak hasil. Model TTS bekerja paling baik pada teks alfabetis. Digit dan simbol lebih sering salah ucap atau memicu suara hantu, karena satu angka punya beberapa cara pengucapan.

Catatan model card `pocket-tts-indonesian` menyatakannya tegas: angka adalah kosakata di luar cakupan, tulis sebagai kata.

Konsekuensinya, naskah terbagi dua versi:

| Naskah asli | Naskah TTS |
| :--- | :--- |
| mAP@0.5:0.95 sebesar 0,4974 | em A P sebesar nol koma empat sembilan tujuh empat |
| HOTA 44,37 dan IDF1 53,86 | Hota empat puluh empat koma tiga tujuh dan I D F lima puluh tiga koma delapan enam |
| 24,61 milidetik | dua puluh empat koma enam satu milidetik |
| RTX 4090 | ar te eks empat ribu sembilan puluh |

Angka sudah dicek: **nol digit tersisa di `naskah-tts.txt`.**

### 5. Singkatan: jangan berasumsi dieja huruf per huruf

Sebagian singkatan dibaca sebagai kata, sebagian dieja, dan mesin tidak bisa menebak. Panduan Vois menyarankan menulis kepanjangannya pada penyebutan pertama.

Ini juga yang merusak video 2025. Transkrip video itu menunjukkan "YOLO V11" dieja huruf per huruf, "conveyor" menjadi "convior", "occlusion" menjadi "oclusion", dan "Siliwangi" menjadi "liwangi". Semuanya bisa dihindari dengan menulis ulang istilahnya di naskah TTS.

Daftar istilah proyek ini sudah ada di `docs/video/riset-tts-video-penelitian.md` bagian 6, dan semuanya sudah diterapkan di `naskah-tts.txt`.

### 6. Jangan pakai daftar berderet

Daftar yang dipisah koma lalu ditutup "dan" menuntut pendengar mengingat terlalu banyak sekaligus. Repositori ini juga punya bukti langsung: pengujian `pocket-tts-indonesian` melaporkan satu butir daftar hilang saat model membaca enumerasi panjang.

Ganti dengan enumerasi eksplisit. Naskah ini memakainya di beberapa tempat:

> "Pertama, arsitektur NMS-free memangkas waktu post-processing menjadi sepertiga... Kedua, ada batas atas yang tidak bisa dilewati."

Pendengar jadi bisa menghitung, dan kalau ada butir yang hilang, hilangnya satu kalimat utuh, bukan satu kata di tengah daftar.

### 7. Potong per paragraf, jangan kirim seluruh naskah sekaligus

Dokumentasi VoxCPM2 mengakui hasilnya kurang stabil pada teks panjang. Praktik di NVIDIA NeMo dan contoh resmi Inworld sama: pecah di batas alami (paragraf, lalu kalimat), sintesis per potongan, sambung setelahnya.

Karena itu `naskah-tts.txt` memakai baris kosong sebagai pemisah paragraf, dan skrip render memprosesnya satu per satu. Efek sampingnya menguntungkan: kalau satu paragraf jelek, cukup render ulang paragraf itu.

### 8. Uji dulu 200 kata pertama

Panduan YTVoice menyarankan jangan langsung membuat seluruh naskah. Ambil paragraf 1 sampai 3, dengarkan, baru lanjut. Perbaikan yang perlu dilakukan setelah mendengar biasanya tiga hal: kata yang salah ucap, kalimat yang terasa cepat, dan penekanan yang jatuh di tempat salah.

Dengarkan juga sambil membaca naskahnya dengan suara sendiri. Panduan Vois menekankan ini: kalimat yang lidah sendiri tersandung saat dibaca hampir pasti keluar janggal dari mesin.

### Ringkasan aturan terhadap naskah ini

| Aturan | Status di naskah |
| :--- | :--- |
| Kalimat ≤ 25 kata | Maksimum 19 kata |
| Tanpa em dash, titik koma, tanda kurung | 0 kemunculan |
| Angka sebagai kata di versi TTS | 0 digit tersisa |
| Istilah teknis ditulis fonetis di versi TTS | Semua istilah sudah dikonversi |
| Daftar memakai enumerasi eksplisit | Dipakai pada dua blok temuan |
| Dipecah per paragraf | 15 paragraf, satu ide per paragraf |
| Ada versi terpisah untuk subtitle | `naskah-asli.txt` |

---

## Bagian 2. Cara Memakai Kedua Berkas

### Langkah 1. Unggah ke Google Drive

Buat folder `video-puu/` di Google Drive, lalu unggah kedua berkas. Nama berkas tidak perlu diubah.

### Langkah 2. Colab

Runtime: ***Hardware accelerator* = T4 GPU**, ***Runtime version* = Latest**. Kalau tersedia L4 atau A100, pakai itu (lebih cepat). Jangan TPU, karena VoxCPM2 memakai CUDA.

```python
# Sel 1
from google.colab import drive
drive.mount('/content/drive')
!pip install -q voxcpm soundfile

# Sel 2
!wget -q -O /content/render_narasi.py \
 https://raw.githubusercontent.com/feb027/hibah-riset/main/scripts/video/render_narasi.py

# Sel 3 — cek rencana dulu
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" --dry-run

# Sel 4 — buat satu paragraf acuan, ulangi sampai suaranya cocok
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out acuan --only 1 \
  --voice-desc "(a young male narrator, calm and clear, brisk pace, documentary style)"

# Sel 5 — render semua paragraf dengan suara terkunci dari acuan
!cd /content && python render_narasi.py \
  "/content/drive/MyDrive/video-puu/naskah-tts.txt" \
  --out "/content/drive/MyDrive/video-puu/out" \
  --reference-wav "/content/acuan/narasi_01.wav"
```

Sel 3 akan menampilkan 15 paragraf dan perkiraan 4,7 menit. Kalau jumlahnya bukan 15, berarti berkasnya terunggah tidak lengkap.

Sel 4 wajib dijalankan lebih dulu dan tidak boleh digabung dengan Sel 5. Voice Design dari teks tidak menghasilkan suara yang sama antar pemanggilan, jadi suara harus dikunci lewat berkas audio acuan. Alasan lengkapnya ada di `docs/video/cara-pakai-voxcpm2.md` Sel 4 dan 5.

### Langkah 3. Setelah audio jadi

1. Susun 15 potongan audio berurutan di editor video.
2. Musik latar di level sekitar −18 dB, supaya narasi tetap jelas.
3. **Subtitle dibuat dari `naskah-asli.txt`, bukan yang TTS.** Kalau tertukar, subtitle akan menampilkan "Kraud Hyuman" dan "en em es fri".
4. Tambahkan keterangan bahwa narasi dibuat dengan bantuan AI.

### Kalau ada satu paragraf yang kurang enak

Jangan render semuanya. Perbaiki paragraf itu di `naskah-tts.txt`, unggah ulang, lalu:

```bash
python render_narasi.py naskah-tts.txt --out out \
  --reference-wav acuan/narasi_01.wav --only 7 --force
```

`--only 7` me-render paragraf ke-7 saja, `--force` menimpanya.

---

## Catatan Isi Naskah

Susunan 15 paragraf mengikuti pola video luaran tahun lalu, yang sudah diterima dosen: masalah, mengapa penting, pendekatan, hasil, lalu arah lanjutan.

| Paragraf | Isi |
| :--- | :--- |
| 1 | Urgensi: ruang publik butuh angka jumlah orang secara langsung |
| 2 | Kelemahan pemantauan manual |
| 3 | Kendala teknis kamera pengawas |
| 4 | Tiga kesalahan khas: hitung ganda, ID tertukar, hitungan palsu |
| 5 | Perkenalan RANCAGE dan tiga komponennya |
| 6 | Hasil deteksi: empat arsitektur, mAP terbaik |
| 7 | Dua temuan deteksi: NMS-free dan lantai 7–10 persen |
| 8 | Hasil pelacakan: perbandingan empat pelacak pada deteksi sama |
| 9 | Mengapa Deep-OC-SORT dipakai, bukan yang paling akurat |
| 10 | Hasil logika hitung: 101,99 persen turun ke 16,71 persen |
| 11 | Sensitivitas pengaturan: masa tunggu dan ambang keyakinan |
| 12 | Kelayakan real-time: 24,61 ms, 40,6 FPS, counter 0,4 persen |
| 13 | Peta jalan lima tahun |
| 14 | Kesimpulan |
| 15 | Penutup |

Paragraf 9 sengaja ada. Video penelitian yang hanya menyebut "model terbaik" tanpa menjelaskan mengapa yang terbaik justru tidak dipakai akan memancing pertanyaan dosen. Menyebut alasan biaya komputasi di narasi justru menunjukkan hasilnya dipahami.

## Rujukan Panduan

1. ElevenLabs, *Text to Speech — Best practices*, 2026. https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices.mdx
2. ElevenLabs, *Prompting guide: text normalization* — digit dan simbol lebih sering salah ucap. https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide.mdx
3. YTVoice.app, *How to Write Scripts That Sound Great with AI Voiceover*, Februari 2026, diperbarui April 2026. https://ytvoice.app/blog/how-to-write-scripts-for-ai-voiceover
4. Vois, *Writing Scripts That Sound Natural with AI*, Desember 2025. https://vois.so/blog/scripting-for-ai-voices
5. `anak10thn/pocket-tts-indonesian`, model card: angka di luar kosakata, enumerasi panjang bisa kehilangan satu butir, tanda hubung. https://huggingface.co/anak10thn/pocket-tts-indonesian
6. NVIDIA, *Magpie-TTS Longform Inference*, NeMo Framework User Guide 26.02 — sintesis berjenjang per kalimat. https://docs.nvidia.com/nemo-framework/user-guide/26.02/nemotoolkit/tts/magpietts-longform.html
7. Inworld, *example_tts_long_input.py* — pemotongan bertingkat paragraf, baris, kalimat. https://github.com/inworld-ai/inworld-api-examples
8. OpenBMB, *VoxCPM2* — catatan ketidakstabilan pada teks panjang. https://github.com/OpenBMB/VoxCPM
