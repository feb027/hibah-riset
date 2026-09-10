LAYAK DENGAN REVISI MINOR

Reviewer: agen reviewer akademik (netral, bukan penulis draft) — JESTEC-style, Bab 4 subbab 4.4
Sumber rujukan: laporan-sensitivitas-parameter.md (utama), experiments/s3_counting/sensitivity_cooldown.csv + sensitivity_confidence.csv (verifikasi data mentah), 4.2-mot-results.md, 4.3-people-counting-results.md, 4.5-end-to-end-performance.md (konsistensi antar-subbab).

Ringkasan verdict: seluruh sel Tabel 8 (10 baris × 3 kolom angka) dan Tabel 9 (10 baris × 3 kolom angka) terverifikasi cocok persis dengan laporan sumber dan CSV mentah, termasuk tanda desimal koma dan kolom perilaku/catatan. Masalahnya seluruhnya pada kalimat interpretasi: klaim tren "monoton" kontradiktif dengan tabel yang dicetak dua baris di atasnya, klaim titik lintas-nol bias salah rentang, klaim "empat tracker" tidak konsisten dengan framing subbab 4.3 sendiri, dan klaim penutup "titik optimal" tidak terjamah oleh data subbab ini. Semua dapat diperbaiki dengan mengedit kalimat, bukan data.

---

## 1. Akurasi angka (Tabel 8 dan Tabel 9 vs sumber)

TIDAK DITEMUKAN MASALAH pada angka. Verifikasi sel-per-sel terhadap Tabel bagian 2 dan 3 laporan sumber serta CSV mentah:

- Tabel 8 — ke-10 baris (CD 0, 5, 10, 15, 20, 30, 45, 60, 90, 120) kolom MAE (23,69 … 9,45), Galat % (101,99 … 23,96), Bias (+23,55 … −8,41) cocok semua dengan sensitivity_cooldown.csv jalur deepocsort dan identik dengan laporan sumber. Kolom Perilaku menyalin karakteristik sumber dengan penerjemahan wajar.
- Tabel 9 — ke-10 baris (conf 0,10–0,60) kolom MAE (2,46 … 11,34), Galat % (5,50 … 25,43), FPS (39,2 … 43,0) cocok semua dengan sensitivity_confidence.csv dan laporan sumber.
- Konversi "20–30 frame ≈ 0,7–1,0 detik pada video 30 FPS" benar (20/30 ≈ 0,67).
- Rentang throughput "39,2–43,0 FPS" dan "di atas 40 FPS pada 0,25–0,30" benar (40,4 dan 40,8).

## 2. Klaim aritmetika dan logika tren

Empat masalah:

- [W1] Kutipan (baris 24): "Galat turun monoton hingga mencapai titik terendah 16,71% pada *cooldown* 30 *frame*".
  Kontradiktif dengan Tabel 8 sendiri (baris 18–19): galat CD=45 adalah 14,64%, LEBIH RENDAH 2,07 poin persentase (12,4% relatif) dari CD=30 yang 16,71%. Penurunan monoton berlaku hingga CD=45, bukan 30; titik terendah galat ada di CD=45, dan itu pula yang dilabeli "Under-count ringan" di tabel. Yang benar hanya klaim MAE: MAE terendah memang 6,34 di CD=30 (CD=45: 6,59). Draft menggabungkan dua metrik berbeda menjadi satu klaim. Sumber pun keliru di ringkasan eksekutifnya ("Galat terendah 16,71%") sementara tabelnya sendiri menunjukkan 14,64% — draft mewarisi kesalahan sumber tanpa cek silang. Perbaiki menjadi: MAE terendah di CD=30, galat terendah di CD=45, keduanya di piringan lebar 20–45. Penanda tebal "**Galat terendah**" pada baris CD=30 di Tabel 8 juga menyesatkan dan perlu dipindah/di-disambiguasi.
- [W2] Kutipan (baris 24): "Rentang 20–30 *frame* … merupakan titik seimbang: bias melintasi nol di daerah ini".
  Data menunjukkan lintas-nol terjadi antara CD=15 (+1,17) dan CD=20 (−0,17), yaitu rentang 15–20, bukan 20–30. Pada rentang 20–30 bias sudah negatif di kedua ujung (−0,17 dan −2,34). Sumber sendiri hanya mengklaim "Bias −0,17 s.d. −2,34" untuk CD 20–30 (tanpa klaim lintas-nol) dan melabel CD=20 "Zero Bias". Rumusan "melintasi nol di daerah ini" keliru rentang; transisi over→under terjadi di 15–20.
- [W3] Kutipan (baris 24): "Pola yang sama berlaku konsisten pada empat tracker yang diuji."
  Dua masalah. (a) Data (sensitivity_cooldown.csv) memuat 3 jalur tracker (deepocsort, ocsort, diffmot) + jalur ground_truth. Subbab 4.3 sendiri konsisten memperlakukan GT sebagai "referensi", bukan tracker (Tabel 6: GT = baris Referensi terpisah dari "Empat tracker"). Menyebutnya "empat tracker" kontradiktif dengan framing internal makalah. (b) "Konsisten" hanya benar secara kualitatif (bentuk V over→under di semua jalur); secara kuantitatif tidak sama: galat terendah DiffMOT di CD=30 (13,08%), Deep-OC-SORT di CD=45 (14,64%), OC-SORT di CD=60 (14,39%); posisi lintas-nol bias juga beda (DiffMOT/GT ~15–20, Deep-OC ~15–20, OC-SORT ~30–45, bias +0,38 masih positif di CD=30). Klaim perlu dikualifikasi: pola V konsisten, lokasi optimum bervariasi 20–60 frame.
- [W4] Klaim arah galat dua sisi ambang conf (baris 43): BENAR — Tabel 9 menunjukkan bentuk V (5,50% → 1,67% di 0,20 → 25,43% di 0,60) dengan mekanisme FP di bawah dan FN di atas; tidak ditemukan masalah pada klaim ini.

## 3. Konsistensi antar-subbab

- [W5] Kutipan (baris 45): "*cooldown* 20–30 *frame* dan *confidence* 0,25–0,30 adalah konfigurasi yang dipakai oleh pengukuran *end-to-end* pada subbab 4.5, sehingga angka pada subbab tersebut merupakan performa sistem pada titik optimalnya, bukan pada setelan acak."
  Tidak sah dari sumber, tiga lapis. (a) Subbab 4.5 tidak menyebut setelan confidence mana pun; klaim "0,25–0,30 dipakai di 4.5" tidak dapat diverifikasi pembaca dari teks 4.5 (setelan deployment 0,30 hanya ada di laporan sensitivitas). (b) "Titik optimal" kontradiktif dengan temuan subbab ini sendiri: Tabel 9 menempatkan galat terendah di conf 0,20 (1,67%), bukan 0,25–0,30 (5,26–5,65%); 0,25–0,30 adalah pilihan trade-off deployment, bukan optimum akurasi. Demikian pula CD=30 optimum MAE tetapi bukan optimum galat (W1). (c) Konfigurasi 4.5 adalah CD=30 (Tabel 7 di 4.3) — titik atas rentang 20–30, bukan rentangnya. Rumuskan ulang: 4.5 mengukur pada konfigurasioperasi (CD=30, conf 0,30) yang berada di dalam piringan stabil hasil studi sensitivitas — klaim yang jujur dan tetap kuat.
- Penandaan model "YOLO26-S" (baris 3, 28) tidak konsisten dengan "YOLO26s" di subbab 4.1, 4.2, dan 4.3 (Tabel 6: jalur "YOLO26-S + Deep-OC-SORT" tidak pernah muncul; 4.3 memakai "YOLO26s"). Samakan kapitalisasi.
- Catatan kecil lintas-subbab (bukan kesalahan 4.4): throughput 40,6 FPS (Tabel 6 di 4.3, Tabel 10/11 di 4.5) vs 40,8 FPS pada Tabel 9 conf 0,30 — dua pengukuran berbeda pada setelan nominal sama; siapkan satu kalimat penjelasan bila reviewer jurnal menanyakannya.

## 4. Sitasi

TIDAK DITEMUKAN MASALAH. Subbab ini memang tidak memuat sitasi baru — sesuai kebijakan pembagian sitasi per-subbab (semua rujukan metode/perangkat telah diperkenalkan di 4.1–4.3). Tidak ada nomor ledger S0xx yang bocor ke teks. Konsisten.

## 5. Gaya bahasa (pola tulisan AI)

Dua frasa diidentifikasi; keseluruhan subbab relatif bersih dan padat:

- Baris 45: "Temuan kedua studi ini bersifat saling melengkapi" — frasa jembatan template yang tidak membawa informasi; dua studi parameter sederhana tidak perlu dipersonifikasikan "saling melengkapi". Hapus, langsung ke isi.
- Baris 45: "bukan pada setelan acak" — kontras retoris defensif khas tulisan AI; setelah W5 diperbaiki, frasa ini redundan terhadap klaim yang benar.
- Baris 24: "transisi dari *over-counting* ke *under-counting* yang saling meniadakan" — "saling meniadakan" mengambang; yang dimaksud adalah dua galat arah berlawanan yang saling mengompensasi di sekitar optimum. Katakan eksplisit atau hapus.
- Tidak ditemukan tricolon berlebihan atau transisi kaku berulang; variasi panjang kalimat wajar.

## 6. Kelayakan jurnal (alur, tabel, logika pembacaan tren)

- Struktur 4.4.1 → 4.4.2 → jembatan ke 4.5 logis dan selesai; pembacaan "dua hiperparameter, dua studi, satu kesimpulan operasional" jelas.
- Tabel rapi: perataan kolom konsisten, desimal koma seragam, kolom kualitatif (Perilaku/Catatan) informatif, caption mencakup jalur dan cakupan 29 sekuens. Satu kelemahan: tebal pada baris CD=30 ("Galat terendah", W1) membimbing pembaca ke kesimpulan yang salah — penanda visual harus mengikuti data.
- Tabel 8 hanya menyajikan Deep-OC-SORT sementara klaim generalisasi ada di kalimat (W3); untuk jurnal, pertimbangkan tabel ringkas lintas-tracker (atau appendix) agar klaim pola-V terdata — bukan klaim 9 kata tanpa bukti tampil.
- Logika tren dua sisi pada Tabel 9 sudah diajarkan dengan baik ke pembaca (mekanisme FP/FN di tiap kutub).

---

## PERBAIKAN WAJIB

1. (W1) Ganti klaim "galat turun monoton … titik terendah 16,71% pada cooldown 30": galat terendah adalah 14,64% pada CD=45 (16,71% di CD=30 lebih tinggi 2,07 pp); penurunan monoton berlaku hingga CD=45. Pertahankan klaim MAE terendah di CD=30 sebagai klaim terpisah. Perbaiki juga penanda tebal dan label "Galat terendah" di Tabel 8.
2. (W2) Ganti "bias melintasi nol di daerah ini [20–30]": lintas-nol terjadi pada rentang 15–20 (dari +1,17 ke −0,17); pada 20–30 bias sudah negatif.
3. (W3) Kualifikasi "pola yang sama berlaku konsisten pada empat tracker": (a) sebut "tiga tracker + lintasan ground truth" agar konsisten dengan 4.3; (b) batasi klaim konsistensi pada bentuk-V kualitatif — galat terendah bervariasi (DiffMOT CD=30, Deep-OC CD=45, OC-SORT CD=60).
4. (W5) Rumus ulang kalimat penutup: 4.5 mengukur pada konfigurasi operasional CD=30 dan conf 0,30 yang berada di dalam piringan stabil hasil studi ini — hapus klaim "titik optimal" (galat terendah conf ada di 0,20; galat terendah CD ada di 45) dan klaim setelan conf yang tidak terverifikasi di teks 4.5.
5. Samakan penulisan "YOLO26-S" → "YOLO26s" (baris 3 dan 28) dengan subbab lain.

## SARAN

1. Hapus frasa pengisi "Temuan kedua studi ini bersifat saling melengkapi" dan "bukan pada setelan acak" (baris 45).
2. Ganti "yang saling meniadakan" (baris 24) dengan rumusan kompensasi galat dua arah di sekitar optimum.
3. Tambahkan bukti tampil untuk klaim lintas-tracker (tabel ringkas 3 tracker + GT dari sensitivity_cooldown.csv) atau nyatakan eksplisit bahwa datanya ada di berkas eksperimen.
4. Siapkan catatan rekonsiliasi throughput 40,6 vs 40,8 FPS (setelan nominal sama, pengukuran berbeda) untuk 4.3/4.5.
