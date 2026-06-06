# Ekstraksi Komentar Dosen — Fokus Revisi No. 3

Sumber PDF: `docs/260602 Paper Hibah-People-Counting-revisi-dari-dosen.pdf`

## Komentar yang relevan dengan No. 3 / Proposed Method

### DL54

> Tambahkan bagian “rancangan eksperimen” ini.
>
> Kemudian menguraikan tahapan penelitian secara visual/gambar yang jelas + termasuk paragraf penjelasannya + jangan lupa mencantumkan semua sitasi referensi yang diadopsi dan/atau menginspirasi dalam menyusun semua tahapan penelitian tersebut.

Tindak lanjut:

- Menambahkan subbagian `3.1 Rancangan Eksperimen`.
- Menambahkan Tabel 1 rancangan eksperimen.
- Menambahkan Gambar 2 tahapan pengembangan/evaluasi.
- Menambahkan sitasi pada tahapan detector, tracker, counting, dataset, dan metrik.

### DL55

> Contoh detail nya ini. Silahkan disesuaikan dengan kebutuhan penelitian ini ya.

Tindak lanjut:

- Struktur contoh Wohlin tidak disalin mentah.
- Elemen eksperimen disesuaikan dengan domain people counting: tujuan, objek studi, domain, fokus, pertanyaan evaluasi, dan variabel.

### DL56

> Buat gambar arsitektur nya + penjelasan dari gambar tersebut secara detail. Silahkan lihat contoh-contoh gambar arsitektur pada paper-paper yang terbit di jurnal bereputasi.

Tindak lanjut:

- Menambahkan Gambar 1 arsitektur sistem.
- Menulis penjelasan detail alur input video → preprocessing → detector → tracker → counting logic → output/evaluation.

### DL57

> Cantumkan semua sitasi referensi yang diadopsi dan/atau menginspirasi dalam menyusun semua tahapan pengembangan tersebut.

Tindak lanjut:

- Detector: S001, S002, S003, S004.
- Tracker: S021, S024.
- Counting logic: S010, S011, S034, S035.
- Dataset: S036, S037, S038.
- Metrik: S025, S026.
- Rancangan eksperimen: Wohlin dkk. (2012), perlu ditambahkan ke daftar pustaka final jika dipakai.

### DL58

> Disesuaikan lagi dengan rekomendasi rancangan eksperimen di awal pembahasan bagian paper ini ya.

Tindak lanjut:

- Bagian evaluasi disusun ulang mengikuti skenario S1–S4: deteksi, tracking, counting logic, dan end-to-end/real-time.
- Ancaman validitas disambungkan dengan rancangan eksperimen, bukan berdiri sendiri.
