# Review JESTEC — Subbab 4.2 Multi-Object Tracking Results

LAYAK DENGAN REVISI MINOR

Reviewer: prompt reviewer subbab tracker (JESTEC)
Draft: docs/journal/4.2-mot-results.md
Sumber: docs/reports/laporan-skenario-b-tracker.md; experiments/s2_tracker/trackeval_trackers/{mot20,dance}/{deepocsort,ocsort,diffmot,lighttrack}/pedestrian_summary.txt
Tanggal: 2026-09-10

Metode: draft dan kedua sumber dibaca penuh; setiap sel Tabel 5 dicocokkan ke pedestrian_summary.txt per tracker (kolom file: HOTA=1, MOTA=13, IDF1=31, IDSW=24, Frag=29) dan ke Bag. 4.1 laporan B untuk OC-SORT/DiffMOT; seluruh klaim kualitatif dihitung ulang dari angka sumber; empat kode S### dicek ke references/references.bib; subbab 4.1 dibaca untuk konsistensi istilah.

Hasil fact-check: 39 dari 40 sel Tabel 5 terverifikasi. SATU sel salah kolom (IDSW DanceTrack Deep-OC-SORT) — lihat Perbaikan Wajib 1. Dua catatan lain: inkonsistensi angka kepadatan MOT20 antar dokumen sumber (draft berada di sisi yang benar) dan satu kalimat keputusan yang menggantung — lihat Perbaikan Wajib 2–3.

## 1. FACTUALITY — 1 kesalahan angka + 2 catatan perbaikan

### 1a. Tabel 5 vs pedestrian_summary.txt (perbandingan koma desimal → titik)

Baris OC-SORT dan DiffMOT (draft baris 11, 13, 15, 17) cocok sel per sel dengan laporan B Bag. 4.1 DAN dengan file summary: MOT20 OC-SORT 36,512/55,98/42,878/14.293/27.646; DiffMOT 44,373/60,913/53,857/6.905/15.005; DanceTrack OC-SORT 28,39/71,38/26,63/6.701/6.936; DiffMOT 39,053/70,721/43,386/2.784/6.765. Pembulatan dua desimal semua benar (36,512→36,51; 55,98→55,98; 60,913→60,91; 53,857→53,86; 39,053→39,05; 70,721→70,72; 43,386→43,39; 42,878→42,88; 26,63→26,63).

Baris Deep-OC-SORT dan LightTrack tidak ada di laporan B — diverifikasi langsung ke file summary:

- MOT20 Deep-OC-SORT (draft baris 12) ↔ mot20/deepocsort/pedestrian_summary.txt baris 2: HOTA 36.123→36,12 ✓; MOTA 54.7→54,70 ✓; IDF1 42.158→42,16 ✓; IDSW 11751→11.751 ✓; Frag 29729→29.729 ✓. Kelima sel cocok.
- DanceTrack Deep-OC-SORT (draft baris 16): HOTA 28.908→28,91 ✓; MOTA 70.047→70,05 ✓; IDF1 27.377→27,38 ✓; Frag 8053→8.053 ✓ — tetapi **IDSW draft 1.984 TIDAK cocok**. Kolom IDSW (kolom 24) di file adalah **5948**; angka 1.984 adalah kolom `IDs` (jumlah trajektori unik, kolom 39). Kesalahan kolom, bukan pembulatan. Dampaknya besar: dengan IDSW sebenarnya 5.948, Deep-OC-SORT hanya menurunkan IDSW DanceTrack 11% dari 6.701 (bukan 70%), dan DiffMOT (2.784) jauh lebih baik dari Deep-OC-SORT pada metrik ini. Perbaikan Wajib 1.
- MOT20 LightTrack (draft baris 14) ↔ mot20/lighttrack/pedestrian_summary.txt: HOTA 32.917→32,92 ✓; MOTA 37.999→38,00 ✓; IDF1 34.693→34,69 ✓; IDSW 13121→13.121 ✓; Frag 8863→8.863 ✓. Cocok semua.
- DanceTrack LightTrack (draft baris 18): HOTA 22.531→22,53 ✓; MOTA 32.718→32,72 ✓; IDF1 18.911→18,91 ✓; IDSW 6697→6.697 ✓; Frag 4405→4.405 ✓. Cocok semua.

Bold kolom (DiffMOT penuh di MOT20; OC-SORT MOTA + DiffMOT HOTA/IDF1/IDSW di DanceTrack) konsisten dengan nilai tertinggi per kolom per benchmark. Setelah IDSW DanceTrack Deep-OC-SORT dikoreksi ke 5.948, bold DiffMOT 2.784 pada baris 17 tetap benar (2.784 < 5.948).

### 1b. Klaim kualitatif — aritmetika diverifikasi

- "IDSW turun 52% menjadi 6.905" (baris 22): (14.293−6.905)/14.293 = 51,69% → 52% ✓.
- "IDF1 naik 10,98 poin menjadi 53,86": 53,857−42,878 = 10,979 ✓.
- "HOTA naik 10,66 poin menjadi 39,05": 39,053−28,39 = 10,663 ✓.
- "IDF1 naik 16,76 poin menjadi 43,39": 43,386−26,63 = 16,756 ✓.
- "HOTA MOT20 36,12 vs 36,51" (baris 22): cocok sumber ✓; draft tidak menyimpulkan Deep-OC-SORT lebih akurat — benar.
- "IDSW dari 6.701 menjadi 1.984 pada DanceTrack" (baris 22): 6.701 cocok, tetapi 1.984 mewarisi kesalahan kolom yang sama → harus 5.948 (Perbaikan Wajib 1).
- "menurunkan IDSW dari 14.293 menjadi 11.751 pada MOT20" (baris 22): cocok ✓ (17,8% turun).
- "179 kotak per frame dengan puncak 272" (baris 20): 1.595.730/8.931 = 178,67 ≈ 179 ✓; puncak 272 cocok laporan B (Bag. 1 dan 5.1). Namun laporan B Bag. 4.2 menulis rata-rata **202** deteksi/bingkai (puncak 271, MOT20-05) — angka lain di dokumen sumber yang sama. detection_stats.csv mengonfirmasi 178,7 dengan puncak MOT20-05 = 274,2, jadi draft konsisten dengan file data mentah; laporan B internalnya sendiri tidak konsisten (179 vs 202, 272 vs 271 vs 274). Draft berada di sisi yang benar, tetapi inkonsistensi sumber perlu dibersihkan (Perbaikan Wajib 2).
- "hampir separuh bobot identitas tidak cocok" (baris 20): IDF1 42,88 → 57,1% tidak cocok — "hampir separuh" agak menghaluskan; laporan B menulis "sekitar 57% bobot tidak cocok". Saran 1.
- "22,7 FPS pada RTX 3090" (baris 24): cocok laporan B (Bag. 5.2/6.2) ✓, dengan atribusi "publikasinya melaporkan" tepat (angka publikasi pada deteksi YOLOX, bukan hasil ukur sendiri).
- Konteks DanceTrack "25 sekuens, 25.508 frame" dan MOT20 "4 sekuens, 8.931 frame" (baris 3): cocok laporan B Bag. 3.1 ✓.

## 2. CITATION INTEGRITY — tidak ditemukan masalah

- S024 Cao et al. 2023, OC-SORT (draft baris 3) ↔ bib baris 181 @inproceedings{S024}, CVPR 2023, arXiv 2203.14360 ✓.
- S049 Maggiolino et al. 2024, Deep-OC-SORT (baris 3) ↔ bib baris 365 @article{S049}, IEEE TIP 2024, arXiv 2306.04946 ✓. Atribusi "menambahkan Re-ID adaptif" sesuai judul paper ("Adaptive Re-Identification").
- S021 Lv et al. 2024, DiffMOT (baris 3) ↔ bib baris 168 @inproceedings{S021}, CVPR 2024, arXiv 2403.02075 ✓. Atribusi "berbasis diffusion dan Re-ID" sesuai.
- S050 Khan et al. 2026, LightTrack-ReID (baris 3) ↔ bib baris 378 @article{S050}, PLOS ONE 21(3), e0342246 ✓.

Dua catatan (bukan kesalahan draft):

1. **S014 dan S050 adalah entri ganda untuk paper yang sama** — keduanya DOI 10.1371/journal.pone.0342246, Khan et al., PLOS ONE 21(3) 2026 — tetapi daftar penulisnya berbeda: S014 "Khan, Said Baz Jahfar; Zhang, Peng; Kamal, Mian Muhammad; Saudagar, Abdul Khader Jilani" (4 penulis), S050 "Khan, Shahriar B. J.; Zhang, Ping; Kamal, Mohd Mudassir; Saudagar, Abdul Khader Jilani; and others" (dengan *et al.* padahal paper ber-4 penulis). Laporan B mengutip S014, draft jurnal mengutip S050. Dirapatkan sebelum submisi (lihat Saran 2).
2. Pola sitasi "Penulis (tahun – S0xx)" sama dengan subbab 4.1; konversi ke gaya JESTEC tetap ditunda sampai submisi, konsisten dengan keputusan review 4.1.

## 3. OVERCLAIM — tidak ditemukan masalah

Rambu-rambu dipatuhi:

- Draft eksplisit "perbandingan yang sah adalah antar tracker, bukan terhadap angka leaderboard yang memakai deteksi resmi" (baris 3) — tepat, sesuai Bag. 5.3 laporan B.
- Deep-OC-SORT dilaporkan netral: "hampir tidak mengubah akurasi agregat... HOTA MOT20 36,12 vs 36,51" (baris 22) — draft justru menunjukkan HOTA sedikit lebih rendah dan TIDAK menyimpulkan Deep-OC-SORT lebih akurat. Keunggulan yang diklaim hanya stabilitas identitas (IDSW), dan itu memang yang bergerak signifikan di sumber. Benar.
- Perbandingan LightTrack dinyatakan "belum direkomendasikan sebagai tracker utama" dengan kualifikasi "pada kondisi saat ini" (baris 22) — tidak melebih-lebihkan.
- Pembatasan sifat DiffMOT (GPU, black-box, patch dependensi) dilaporkan sejajar dengan klaim akurasinya (baris 24) — seimbang, sesuai Bag. 6.2 laporan B.
- Tidak ada perbandingan melawan angka publikasi (OC-SORT HOTA 62,4; DiffMOT 62,3) di draft — rambu laporan B no. 5 dipatuhi.

## 4. GAYA BAHASA — tidak ditemukan masalah

Tidak ada frasa template AI ("penting untuk dicatat", "seiring berkembangnya", "dalam era"), tidak ada tricolon berlebihan, tidak ada transisi kaku berulang. Kalimat panjang tetap terkontrol; istilah teknis konsisten diberi italik; pasangan "Pertama... Kedua" (baris 24) dipakai sekali, tidak berulang. Catatan netral: kalimat pengantar (baris 3) memakai empat klausa relatif berurutan dengan pola serupa ("...yang menghubungkan...", "...yang menambahkan...", "...yang berbasis...", "...sebagai eksplorasi") sehingga sedikit berirama — masih wajar untuk kalimat pengantar empat tracker, tidak perlu diubah.

## 5. KELAYAKAN JURNAL — layak dengan dua titik perhatian

- Alur logis baik: pengantar protokol → tabel → pembacaan MOT20 → pembacaan DanceTrack + keputusan → dua konsekuensi + biaya DiffMOT → serah ke 4.3/4.5. Paralel dengan struktur 4.1.
- Konsistensi istilah dengan 4.1 terjaga: "*fine-tune*", "*tracker*", "*frame*", dan klaim "IDF1 metrik paling relevan bagi penghitungan orang" (baris 24) mencerminkan laporan B Bag. 1 no. 4; jembatan penutup 4.1 ("dievaluasi pada subbab 4.2") terpenuhi.
- Dua titik perhatian dalam draft:
  1. Baris 24: kalimat penutup memadatkan dua ide (akurasi dan biaya) lalu menunjuk "pemilihan tracker" tanpa menyebut tracker mana yang dipilih — pembaca jurnal akan bertanya. Satu klausa pengarah cukup; rincian di Perbaikan Wajib 3.
  2. Baris 22 menyebut "dari 6.701 menjadi 1.984 pada DanceTrack" — angka 6.701 (OC-SORT) benar sesuai sumber; yang salah hanya 1.984, warisan kesalahan kolom yang sama dengan Tabel 5 (Perbaikan Wajib 1).
- Tabel 5 rapi; kolom bold konsisten; caption cukup (menyebut deteksi sama dan dua split).
- Penomoran "Tabel 5" menyiratkan tabel 1–4 milik subbab 4.1 — berlanjut dengan benar; renumber saat submisi seperti catatan review 4.1.

## PERBAIKAN WAJIB

1. **IDSW DanceTrack Deep-OC-SORT salah kolom.** Tabel 5 baris 16: `1.984` → `5.948`; dan baris 22: "dari 6.701 menjadi 1.984 pada DanceTrack" → "dari 6.701 menjadi 5.948 pada DanceTrack". Sumber: experiments/s2_tracker/trackeval_trackers/dance/deepocsort/pedestrian_summary.txt baris 2, kolom IDSW = 5948 (angka 1.984 adalah kolom `IDs`, jumlah trajektori unik). Implikasi: klaim "Re-ID adaptifnya bekerja pada stabilitas identitas" tetap berdiri untuk MOT20 (−17,8%), tetapi pada DanceTrack penurunan IDSW hanya ~11% (6.701→5.948), jauh lebih lemah daripada DiffMOT (−58%); kalimat baris 22 perlu memastikan pembaca tidak menanggapinya setara dengan penurunan MOT20.
2. **Jangan warisi inkonsistensi kepadatan dari laporan B tanpa catatan.** Draft baris 20 memakai "179 kotak per frame dengan puncak 272" (sesuai 1.595.730/8.931 dan laporan B Bag. 1/5.1), tetapi laporan B Bag. 4.2 menulis "rata-rata 202 deteksi/bingkai (sampai 271 di MOT20-05)". detection_stats.csv mengonfirmasi versi draft (178,7; puncak MOT20-05 274,2), jadi draft benar — tapi karena sumber formalnya bertentangan sendiri, tambahkan satu footnote/keterangan di draft atau perbaiki laporan B agar angka yang sama tidak beda antar dokumen saat peer-review menelusuri.
3. **Kalimat keputusan baris 24 tergantung.** "Pertimbangan akurasi dan biaya ini yang mendasari pemilihan tracker pada subbab 4.3 dan 4.5" tidak menyebut tracker mana yang akhirnya dipilih. Tambahkan satu klausa (mis. "...mendasari pemilihan OC-SORT sebagai tracker utama...") atau rujuk eksplisit subbab 4.3 tempat keputusan itu dibahas, agar klaim berdiri sendiri di subbab ini.

## SARAN

1. Baris 20 — cari: "hampir separuh bobot identitas tidak cocok" → ganti: "sekitar 57% bobot identitas tidak cocok" (lebih presisi; IDF1 42,88).
2. Rapatkan entri LightTrack: hapus S014 dari references.bib (duplikat S050 — DOI sama), pertahankan S050, dan samakan ejaan nama penulis dengan halaman penerbit PLOS; laporan B juga perlu diperbarui dari S014 → S050 agar satu paper satu kode.
3. Setelah Perbaikan Wajib 1 masuk, bold kolom IDSW DanceTrack tidak berubah (DiffMOT 2.784 tetap terbaik, 2.784 < 5.948) — cukup dicek ulang saat revisi.
4. Saat submisi: konversi "– S0xx" ke gaya sitasi JESTEC dan renumber tabel (lanjutan keputusan review 4.1).
