LAYAK DENGAN REVISI MINOR

Reviewer: agen reviewer akademik (netral, bukan penulis draft) — JESTEC-style, Bab 4 subbab 4.3
Sumber rujukan: laporan-skenario-c-counting.md (utama), 4.2-mot-results.md, laporan-skenario-b-tracker.md (konteks), laporan-sensitivitas-parameter.md + 4.4-ablation-system-analysis.md (rekonsiliasi), experiments/s3_counting/*.csv (verifikasi data mentah), references/references.bib.

Ringkasan verdict: seluruh angka pada Tabel 6 dan Tabel 7 terverifikasi benar terhadap data mentah (termasuk tanda desimal koma), arah perbandingan antar-tracker benar, dan keputusan Deep-OC-SORT sebagai tracker utama konsisten dengan laporan Skenario C dan subbab 4.2. Revisi yang diminta bersifat kalimat-interpretasi, bukan data: tiga klaim kausal/kuantitatif pada paragraf interpretasi tidak didukung (dua di antaranya kontradiktif dengan data di subbab 4.4 sendiri).

---

## 1. Akurasi angka (Tabel 6 dan Tabel 7 vs sumber)

TIDAK DITEMUKAN MASALAH pada angka. Verifikasi terhadap counting_metrics.csv (29 sekuens per tracker) dan sensitivity_cooldown.csv:

- Tabel 6 baris per baris — Rata-rata GT 44,62; DiffMOT 41,03 / MAE 4,41 / 13,08% / RMSE 3,25; Deep-OC-SORT 42,28 / 6,34 / 16,71% / 4,16; OC-SORT 45,00 / 6,66 / 22,38% / 4,31; LightTrack 57,76 / 13,62 / 53,03% / 9,57. Semua cocok persis (dua desimal, koma) dengan CSV dan Tabel bagian 2 laporan C.
- Throughput 40,6 FPS untuk Deep-OC-SORT cocok dengan laporan C; draft tidak menyalin throughput tracker lain (aman, karena pembanding FPS antar-tracker ada di ranah 4.2/4.5).
- Tabel 7 — 16,71% (CD=30) dan 27,13% (CD=15) cocok dengan sensitivity_cooldown.csv jalur deepocsort (6,34/16,71 dan 7,52/27,13) serta identik dengan Tabel 8 di subbab 4.4.
- Rata-rata prediksi 57,76 untuk LightTrack dan karakterisasi *over-count* kuat benar: bias agregat +13,14 orang, 25 dari 29 sekuens lebih hitung.

Satu catatan verifikasi (bukan kesalahan draft): angka "+17% s.d. +58%" untuk model naive di Tabel 7 berasal dari laporan C tetapi tidak dapat direproduksi dari data — lihat temuan W2 di bawah. Ini masalah klaim, bukan salah salin.

## 2. Klaim aritmetika dan logika

Tiga masalah:

- [W1] Kutipan (baris 17, 4.3.1): "*state machine* pada lintasan *ground truth* menghasilkan galat nol, sehingga seluruh galat pada baris-baris lainnya berasal dari ketidaksempurnaan deteksi dan pelacakan di hulunya."
  Bagian pertama benar (CSV: baris GroundTruth MAE/Err/RMSE = 0,00 pada CD=30), tetapi kesimpulan "seluruh galat … dari hulu" adalah klaim kausal 100% yang kontradiktif dengan data sistem sendiri: pada jalur *ground truth* sekalipun, logika hitung menghasilkan galat pada nilai *cooldown* lain — 60,60% pada CD=0, 12,88% pada CD=15, dan *under-count* 7,63–28,70% pada CD=45–120 (sensitivity_cooldown.csv, tracker ground_truth; dicerminkan sebagai Tabel 8 di subbab 4.4). Artinya konfigurasi logika hitung tetap menyumbang galat pada lintasan tracker; yang dapat diklaim adalah (a) pada CD=30 *state machine* tidak menambah galat pada lintasan ideal, dan (b) relatif terhadap *naive*, galat turun dominan karena koreksi logika hitung (101,99% → 16,71% pada Deep-OC-SORT). Rumusan sekarang berisiko dibantah reviewer yang membaca 4.4.
- [W2] Kutipan (baris 25, Tabel 7): "Naive (tanpa debounce) … +17% s.d. +58%".
  Tidak terverifikasi terhadap data mana pun. counting_ablation.csv (Model_A_Naive, 29 sekuens per tracker) menunjukkan rentang galat per sekuens 3,55–592,86% (Deep-OC-SORT) dan rata-rata 88,66% (DiffMOT), 101,99% (Deep-OC-SORT), 120,40% (OC-SORT), 155,12% (LightTrack). Angka "+17% s.d. +58%" tidak cocok dengan rentang maupun rata-rata, dan kontradiktif dengan subbab 4.4 yang menyebut galat *naive* 101,99%. Kemungkinan angka laporan C yang usang/salah — draft menyalinnya tanpa cek. Ganti dengan angka dari CSV atau samakan dengan 4.4.
- [W3] Kutipan (baris 29, 4.3.2): "*State machine* menghilangkan seluruh *over-count* palsu tersebut dengan mengingat status setiap ID sehingga satu orang hanya terhitung sekali."
  Overclaim. Pada jalur tracker dengan CD=30, *over-count* per sekuens masih terjadi (Deep-OC-SORT: lebih hitung di 16 dari 29 sekuens; bias agregat −2,34 hanya berarti rata-ratanya negatif), dan pada CD=15 galat masih 47,74% dengan bias +7,31. Yang didukung data: *state machine* menghilangkan *over-count* akibat getaran pada lintasan ideal (GT+CD30 = galat nol) dan menekan galat *naive* 101,99% → 16,71%. Kata "seluruh" perlu dihapus atau dicakupkan ke mekanisme getaran pada lintasan ideal.

Klaim lain pada kategori ini bersih:
- Galat nol pada GT track: benar (terverifikasi CSV).
- Arah *over/under-count*: LightTrack *over-count* kuat (benar); Deep-OC-SORT "cenderung kurang hitung" benar secara bias rata-rata (−2,34) — lihat saran S2 untuk kualifikasi; draft tidak mengklaim arah untuk OC-SORT (tepat, karena hampir imbang: bias +0,38).

## 3. Interpretasi dan overclaim

- [S1] Kutipan (baris 17): "peringkat akurasi hitungan mengikuti kualitas asosiasi tracker".
  Benar untuk dua kutub yang dikutip eksplisit (DiffMOT IDF1 tertinggi → galat terendah; LightTrack IDF1 terendah → galat terbesar), tetapi tidak monoton di pasangan tengah: pada MOT20 IDF1 OC-SORT (42,88) justru di atas Deep-OC-SORT (42,16), sementara galat hitung OC-SORT jauh lebih buruk (22,38% vs 16,71). Saran: kualifikasi klaim agar tidak terbaca sebagai hubungan monoton penuh untuk keempat tracker.
- Dekomposisi galat: laporan C berjudul "…dan Dekomposisi Galat" tetapi tidak menyajikan tabel dekomposisi eksplisit deteksi-vs-tracking-vs-counting; draft tidak menyalin komponen yang memang tidak ada — keputusan yang tepat, jangan mengarang. Namun klaim kesimpulan laporan C ("Dekomposisi Galat Hitung … tuntas dilaksanakan") membuat draft kehilangan pijakan: tanpa dekomposisi, draft hanya bisa mengklaim secara agregat, dan di sinilah klaim W1 menjadi rapuh. Nilai reviewer: bukan blokir untuk 4.3; jika reviewer jurnal menuntut dekomposisi, bahan mentahnya tersedia di counting_ablation.csv (jalur GT vs jalur tracker per model hitung).
- [S4] Rekonsiliasi dengan 4.1 opsional: 4.1 menetapkan "lantai *under-count*" 7,4–10,0% dan menyatakan target 4.3 memperhitungkannya; galat sistem 13,08–16,71% memang konsisten di atas lantai itu, tetapi 4.3 tidak menutup lingkaran tersebut. Satu klausa cukup, bukan wajib.
- Klaim "melebihi 85%"? Tidak ada di draft — benar, draft tidak mengklaim akurasi ≥85% di mana pun. Aman.

## 4. Sitasi

TIDAK DITEMUKAN MASALAH. Subbab 4.3 tidak memuat sitasi maupun kode S### — konsisten dengan pembagian kerja antar-subbab (metodologi dan sitasi tracker/detektor ditanggung 4.1/4.2: S024, S049, S021, S014 terverifikasi ada di references/references.bib). Tidak ada kebutuhan sitasi baru: MOT20/DanceTrack, TrackEval, dan keempat tracker sudah disitasi di 4.2; CD/*state machine* adalah kontribusi internal yang dibahas 4.4.

## 5. Gaya bahasa (Indonesia akademik-natural, anti-AI)

Secara umum bersih: kalimat padat, faktual, tidak ada tricolon berlebihan, tidak ada paragraf penutup rangkuman berulang (penutup 4.3.2 justru mengarahkan ke 4.4 — baik). Dua catatan ringan:

- [S5] Pola pembuka enumeratif berulang lintas subbab: 4.2 "Dua konsekuensi ditarik dari tabel ini" vs 4.3 "Dua hal terbaca langsung dari Tabel 6". Sendiri tidak masalah; berdampingan dalam dua subbab berurutan mulai terasa templat. Variasikan salah satunya.
- Kutipan (baris 27, Tabel 7): "*State machine* (CD=15) … Optimal untuk pejalan cepat" — lihat S3; selain salah nuansa, "optimal" di posisi ini adalah label promosi, bukan gaya akademik.

## 6. Kelayakan jurnal (alur, tabel, konsistensi antar-subbab)

- Konsistensi keputusan tracker utama: KONSISTEN. Laporan C menetapkan Deep-OC-SORT "TRACKER UTAMA" (40,6 FPS, galat 16,71%); draft 4.2 menutup dengan keputusan yang sama; 4.3 Tabel 6 memakai Peran "Tracker utama" dan menunda rincian biaya ke 4.5 — alur antar-subbab rapi tanpa repetisi berlebihan.
- [S3] Tabel 7: kolom "Galat rata-rata" mencampur satuan — baris *naive* berisi rentang ("+17% s.d. +58%"), baris lain titik tunggal; dan tabel tidak menyebut pada jalur tracker mana ablasi dijalankan (data: Deep-OC-SORT; DiffMOT CD15 justru 15,42%). Tambahkan di keterangan tabel: "(Deep-OC-SORT, 29 sekuens)" dan samakan satuan.
- [S3b] Label "Perilaku" baris CD=15 "Optimal untuk pejalan cepat" menyesatkan: CD=15 galatnya 27,13%, lebih buruk dari CD=30 (16,71%); perilaku CD=15 adalah *over-count* ringan (bias +1,17), dan "pejalan cepat" adalah konteks penggunaan, bukan perilaku terukur. Ganti, misalnya, "*Over-count* ringan; cocok untuk arus cepat".
- Istilah: "lantai *under-count*" dari 4.1 tidak dipakai di 4.3 (tidak wajib); IDF1, *throughput*, *cooldown*, *over-count/under-count* konsisten dengan 4.2/4.4. Angka 29 sekuens konsisten. Tanda desimal koma konsisten di seluruh draft.
- Logika alur 4.3.1 → 4.3.2 → rujukan 4.4/4.5 benar dan tidak melompat.

---

## PERBAIKAN WAJIB

1. [W1] Baris 17 (4.3.1): lunakkan klaim kausal "seluruh galat pada baris-baris lainnya berasal dari ketidaksempurnaan deteksi dan pelacakan di hulunya". Rumusan yang didukung data: *state machine* pada CD=30 tidak menambah galat pada lintasan *ground truth*; pada lintasan tracker, galat didominasi ketidaksempurnaan hulu, tetapi kontribusi logika hitung pada nilai *cooldown* lain tetap ada (jalur GT: 60,60% pada CD=0; *under-count* hingga 28,70% pada CD=120 — lihat 4.4).
2. [W2] Baris 25 (Tabel 7): angka "+17% s.d. +58%" tidak dapat direproduksi dari experiments/s3_counting/counting_ablation.csv (rentang per sekuens 3,55–592,86%; rata-rata 88,66–155,12% per tracker) dan kontradiktif dengan 4.4 (101,99%). Ganti dengan angka terverifikasi, misalnya rentang rata-rata antar-tracker 88,66–155,12%, atau rujuk angka 101,99% yang sama dengan 4.4.
3. [W3] Baris 29 (4.3.2): hapus/cakupkan kata "seluruh" pada "menghilangkan seluruh *over-count* palsu" — pada jalur tracker, *over-count* per sekuens masih terjadi pada CD=30 dan CD=15. Klaim aman: menghilangkan *over-count* akibat getaran pada lintasan ideal dan menekan galat *naive* 101,99% → 16,71%.

## SARAN

1. [S1] Baris 17: kualifikasi "peringkat akurasi hitungan mengikuti kualitas asosiasi tracker" — hubungan tegas pada dua kutub (DiffMOT, LightTrack), tidak monoton di pasangan OC-SORT vs Deep-OC-SORT (IDF1 MOT20 42,88 vs 42,16, galat 22,38% vs 16,71%).
2. [S2] Baris 17: "prediksi yang cenderung kurang hitung" untuk Deep-OC-SORT — tambah kualifikasi "secara rata-rata" (bias −2,34), karena 16 dari 29 sekuens justru lebih hitung.
3. [S3] Tabel 7: sebutkan jalur tracker di keterangan ("Deep-OC-SORT, 29 sekuens"), samakan satuan kolom galat, dan ganti label "Optimal untuk pejalan cepat" menjadi deskripsi perilaku (mis. "*Over-count* ringan; cocok untuk arus cepat").
4. [S4] Opsional: satu klausa rekonsiliasi dengan lantai *under-count* 4.1 (galat sistem 13,08–16,71% berada di atas lantai 7,4–10,0% dari deteksi) untuk menutup alur antar-subbab.
5. [S5] Variasikan pola pembuka "Dua hal terbaca…" (4.3) yang berdampingan dengan "Dua konsekuensi ditarik…" (4.2).
