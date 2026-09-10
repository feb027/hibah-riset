# Review JESTEC — Final Verifier 4.5 + 4.6 (verifikasi perbaikan wajib)

LAYAK

File diverifikasi: docs/journal/4.5-end-to-end-performance.md, docs/journal/4.6-discussion.md
Review rujukan: docs/reviews/review-jestec-4.5.md, docs/reviews/review-jestec-4.6.md
Sumber data: docs/reports/laporan-skenario-d-realtime.md, docs/journal/4.1-object-detection-results.md (ditunjang 4.2–4.4)
Tanggal verifikasi: 10 September 2026

---

## 1. STATUS PERBAIKAN WAJIB

### Review 4.5 (3 wajib)

**F1 — TERAPAN.** Kualifikasi "maksimum" pada klaim lonjakan latensi telah dipulihkan.
Bukti (4.5 baris 31): "Lonjakan latensi maksimum, yang melampaui anggaran hingga 42,10 ms
per *frame* (setara sekitar 23,8 FPS pada *frame* tersebut), hanya terjadi pada *frame*
dengan lebih dari 50 orang sekaligus". Sesuai sumber baris 59: "Lonjakan latensi
**maksimum** hanya terjadi pada frame dengan lebih dari 50 orang sekaligus".

**F2 — TERAPAN.** Kalimat tidak didukung "throughput sesaat turun di bawah 30 FPS, tetapi
kembali normal begitu kerumunan mencair" sudah dihapus dan diganti versi berbasis angka
sumber. Bukti (4.5 baris 31): "melampaui anggaran hingga 42,10 ms per *frame* (setara
sekitar 23,8 FPS pada *frame* tersebut)" — persis opsi sah yang diresepkan reviewer
(1000/42,10 ≈ 23,8 FPS; Max Latency 42,10 ms pada tabel distribusi sumber). Frasa
"kembali normal begitu kerumunan mencair" tidak ada lagi (grep: nihil).

**F3 — TERAPAN.** Klausa konfigurasi pengukuran ditambahkan di paragraf pembuka 4.5.
Bukti (4.5 baris 3): "Pengukuran dilakukan pada konfigurasi operasional hasil subbab 4.4
(*cooldown* 30 *frame*, *confidence* 0,30)". Janji penutup 4.4 baris 45 ("Subbab 4.5
mengukur performa *end-to-end* pada konfigurasi operasional *cooldown* 30 *frame* dan
*confidence* 0,30") kini terpenuhi. Bonus: reviewer 4.5 juga minta konteks densitas MOT20
(S1, saran) — draft menambahkan klausa "jauh lebih jarang daripada kepadatan rata-rata
MOT20-*train* pada subbab 4.2 karena pengukuran ini berfokus pada satu sekuens dan
menghitung orang, bukan kotak deteksi" (baris 3), menutup celah 179 kotak vs 34–38 orang.

### Review 4.6 (5 wajib)

**F1 — TERAPAN.** "dan kualitas perangkat pelatihannya" sudah dihapus; atribusi kini sah.
Bukti (4.6 baris 5): "Yang membedakan tingkat akurasi justru kapasitas model." — sejalan
dengan 4.1 baris 20 ("Lompatan kinerja justru terjadi antar tingkat kapasitas model").
Frasa "kualitas perangkat pelatihan" tidak ada lagi (grep: nihil).

**F2 — TERAPAN.** "dua digit" diganti angka riil. Bukti (4.6 baris 9): "galat *over-count*
model *naive* yang mencapai 88,7–155,1% bergantung jalur tracker (101,99% pada jalur
utama)". 88,7–155,1% = Tabel 7 (4.3 baris 25); 101,99% = Tabel 8 baris CD=0 (4.4 baris 13);
"jalur utama" = Deep-OC-SORT, tracker utama (4.2 baris 24).

**F3 — TERAPAN.** Label 0,4% dikoreksi. Bukti (4.6 baris 9): "dengan biaya komputasi yang
dapat diabaikan — 0,4% dari total latensi *end-to-end*". Sesuai resep reviewer; 0,4% =
0,11 ms / 24,61 ms (Tabel 10), bukan terhadap anggaran 33,3 ms. "Tidak berarti" diganti
"dapat diabaikan", konsisten dengan diksi 4.5 baris 17.

**F4 — TERAPAN.** Atribusi baris 7 diperbaiki: bukan lagi "penambahan mekanisme Re-ID",
melainkan kualitas asosiasi, dengan DiffMOT dinisbatkan eksplisit sebagai paket
diffusion + Re-ID. Bukti (4.6 baris 7): "Karena galat hitung pada subbab 4.3 mengikuti
kualitas asosiasi tracker, penguatan asosiasi identitas terbukti lebih berpengaruh pada
akurasi hitungan daripada peningkatan kualitas kotak itu sendiri. Paket DiffMOT — prediksi
gerak *diffusion* yang dipadukan Re-ID — mencapai galat hitung terendah ... Re-ID semata
pada Deep-OC-SORT hampir tidak mengubah akurasi agregat dan lebih berperan menekan ID
switch." Semua sesuai bukti 4.2 (HOTA 36,12 vs 36,51; IDF1 42,16 vs 42,88) dan rumusan
hati-hati 4.3 baris 17. Klaim lama "penambahan mekanisme Re-ID terbukti lebih berpengaruh"
sudah tidak ada.

**F5 — TERAPAN.** Batasan eksplisit ditambahkan sebagai paragraf penutup. Bukti (4.6
baris 13): "setiap model dilatih satu kali dengan satu *seed* sehingga kesetaraan akurasi
tingkat nano adalah klaim di dalam derau pengukuran; evaluasi dilakukan pada benchmark
publik dengan deteksi *offline*, bukan pada *deployment* lapangan; dan angka latensi
bersifat spesifik perangkat." Ketiga batasan yang diminta (satu seed; benchmark publik
bukan deployment; latensi spesifik perangkat) hadir. Keputusan tracker bersyarat perangkat
yang menempel pada batasan ketiga dinyatakan di baris 11: "server GPU memakai Deep-OC-SORT
demi akurasi, sedangkan perangkat *edge* memakai OC-SORT yang masih lolos ambang 30 FPS."

Total: 3/3 wajib 4.5 TERAPAN + 5/5 wajib 4.6 TERAPAN (8/8).

---

## 2. TINJAUAN ULANG: KLAIM BARU TANPA DUKUNGAN

Tidak ditemukan. Setiap angka di hasil editan terlacak ke sumber:

- 24,61 ms / 40,6 FPS / 33,3 ms / 35% → Tabel A sumber Skenario D (baris 33-34).
- 42,10 ms → Max Latency Deep-OC-SORT RTX 4090 (baris 55); 23,8 FPS = 1000/42,10 (aritmetika
  disetujui reviewer 4.5 F2).
- Persentil 29,50 / 32,10 / 36,40 ms → tabel distribusi sumber baris 55.
- 30,7 FPS (OC-SORT edge) dan 12,0 FPS (Deep-OC-SORT edge) → Tabel B sumber baris 42-43.
- 7,4–10,0% → 4.1 baris 33 (recall maksimum 0,9000–0,9262).
- 88,7–155,1% → Tabel 7 (4.3 baris 25); 101,99% → Tabel 8 CD=0 (4.4 baris 13).
- 0,4% → Tabel 10 (0,11 ms dari 24,61 ms).
- MOT20-02 "34–38 orang per *frame*" → sumber Skenario D baris 23; kalimat penjelas
  densitas baru konsisten dengan 4.2 baris 20 (179 kotak/frame pada MOT20-*train* 4 sekuens).
- 4.6 baris 11 menamai konfigurasi "cooldown 30 *frame* dan *confidence* 0,30" → 4.4
  (Tabel 8 CD=30; Tabel 9 conf 0,30 "standar *deployment*") — ini sekaligus memenuhi
  S3 review 4.6 (saran).

Klausa penutup 4.6 "bukan oleh keunggulan satu komponen tunggal" adalah sintesis diskusi,
bukan klaim empiris baru — aman.

---

## 3. TINJAUAN ULANG: POLA TULISAN AI BARU

Tidak ditemukan. Grep frasa slop ("krusial", "signifikan", "menandakan", "mendalam",
"Perlu diingkat", "Secara keseluruhan", tricolon penutup) nihil di kedua draft. Kalimat
naratif "kerumunan mencair" (satu-satunya gaya cerita di 4.5) hilang bersama F2. Pembuka
paralel "Pada ..." di 4.6 masih ada (S4, saran, bukan wajib) — bukan regresi baru; draft
kini memakai pembuka "Hasil *end-to-end* menutup..." dan "Keseluruhan rantai bukti ini..."
sehingga pola "Pada lapisan ..." sudah tidak seragam tiga kali beruntun.

---

## 4. KONSISTENSI ANGKA ANTAR-FILE

| Angka | 4.5 | 4.6 | Sumber | Status |
| :--- | :--- | :--- | :--- | :--- |
| 24,61 ms | baris 15, 17, 27 | baris 11 | Skenario D baris 33, 55 | konsisten |
| 40,6 FPS | baris 17, 27 | (implisit via 4.3 Tabel 6) | sumber baris 34 | konsisten |
| 0,4% | baris 14, 17 | baris 9 | sumber baris 32 | konsisten |
| CD=30 | baris 3 | baris 11 | 4.4 baris 18; Tabel 6 (4.3 baris 7) | konsisten |
| conf 0,30 | baris 3 | baris 11 | 4.4 baris 36, 45 | konsisten |
| 88,7–155,1% | — (tidak disebut) | baris 9 | Tabel 7 (4.3 baris 25) | konsisten |
| 101,99% | — (tidak disebut) | baris 9 | Tabel 8 (4.4 baris 13) | konsisten |
| 7,4–10,0% | — | baris 5 | 4.1 baris 33 | konsisten |
| 42,10 ms / 23,8 FPS | baris 31 | — | sumber baris 55 | konsisten |
| P95 32,10 / P99 36,40 | baris 31 | (via "95% frame di bawah anggaran") | sumber baris 55 | konsisten |
| 30,7 / 12,0 FPS edge | baris 25-26, 29 | baris 11 (30 FPS ambang) | sumber baris 42-43 | konsisten |

Format desimal koma seragam di kedua draft. Tidak ada sel tabel yang berubah dari versi
yang sudah lolos review 4.5 (Tabel 10 dan 11 identik dengan sumber).

---

## 5. CATATAN KECIL (BLOKIR TIDAK ADA; SEMUA OPSIONAL)

1. 4.6 baris 11: "lolos ambang 30 FPS" — OC-SORT edge tercatat 30,7 FPS (Tabel 11 / sumber
   baris 42); pernyataan benar, hanya tidak menyebut angkanya. Bukan masalah.
2. Saran S1/S2 (4.6) dan S4 label tabel (4.5) tetap opsional dan tidak mengurangi kelayakan;
   sebagian sudah ikut terjawab (S3 4.6 terpenuhi oleh baris 11; S1 4.5 terpenuhi oleh
   kalimat densitas baris 3).

---

## VERDICT AKHIR

LAYAK — seluruh perbaikan wajib (F1-F3 review 4.5; F1-F5 review 4.6) terverifikasi
TERAPAN dengan bukti kutipan; tidak ada klaim baru tanpa dukungan; tidak ada pola tulisan
AI baru; angka kunci (24,61 ms / 40,6 FPS / 0,4% / CD=30 / conf 0,30 / 88,7–155,1% /
101,99%) konsisten antar file dan terhadap sumber.
