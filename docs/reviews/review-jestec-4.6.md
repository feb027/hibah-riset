# Review JESTEC — Subbab 4.6 Discussion (penutup Bab 4)

LAYAK DENGAN REVISI MINOR

File direview: docs/journal/4.6-discussion.md (11 baris)
Sumber verifikasi: docs/journal/4.1–4.5, docs/reports/laporan-skenario-a/b/c/d, laporan-sensitivitas-parameter.md
Tanggal review: 10 September 2026

---

## 1. FACTUALITY

Setiap angka utama di 4.6 terlacak ke subbab sumbernya:

- "lantai *under-count* struktural 7,4–10,0%" (4.6 baris 5) ✓ = 4.1 baris 33 (recall maksimum 0,9000–0,9262) dan laporan-skenario-a baris 15, 486.
- "mAP yang tidak dapat dibedakan dari variasi acak" (baris 5) ✓ = 4.1 baris 9 (rentang 0,0058, satu seed).
- "*NMS-free* hanya terukur pada latensi *post-processing* yang datar terhadap kepadatan" (baris 5) ✓ = 4.1 baris 39 (0,164–0,170 ms vs 0,491 ms; biaya datar).
- "HOTA yang konsisten jauh di bawah MOTA pada kedua benchmark" (baris 7) ✓ = Tabel 5 (MOT20: 36,51/36,12/44,37 vs 55,98/54,70/60,91; DanceTrack: 28,39/28,91/39,05 vs 71,38/70,05/70,72).
- "*state machine* menghilangkan galat *over-count* ... (0,4% dari anggaran latensi)" (baris 9) ✓ angkanya = Tabel 10 (0,11 ms, 0,4%), tetapi label "anggaran latensi" keliru — lihat temuan F3.
- "24,61 ms per *frame* ... 95% *frame* di bawah anggaran" (baris 11) ✓ = 4.5 baris 17, 31.
- Ablasi *naive* (baris 9) ✓ = Tabel 7 (88,7–155,1%) dan Tabel 8 (101,99% pada CD=0), tetapi redaksinya menundanya — lihat temuan F2.

Temuan:

**F1 (WAJIB).** Baris 5: "Yang membedakan justru kapasitas model dan kualitas perangkat pelatihannya." — "kualitas perangkat pelatihan" tidak didukung 4.1. Subbab 4.1 mengatribusikan lompatan kinerja pada kapasitas model saja (baris 20: "Lompatan kinerja justru terjadi antar tingkat kapasitas model"; n→s, recall +5,7 poin) dan menyatakan eksplisit bahwa selisih latensi antar arsitektur pada GPU TIDAK ditafsirkan karena dominasi *overhead kernel* (baris 50). Tidak ada pengukuran yang mengisolasi "kualitas perangkat pelatihan". Hapus klausul itu atau ganti dengan atribusi yang memang ada di 4.1.

**F2 (WAJIB).** Baris 9: "galat *over-count* yang mencapai dua digit pada model *naive*" — menyamarkan besaran. Tabel 7: 88,7–155,1%; Tabel 8 (jalur utama Deep-OC-SORT): 101,99%. "Dua digit" secara teknis benar tetapi membayangkan galat ~10–99%, padahal *naive* menghitung hampir dua kali lipat GT. Sebut angkanya (mis. "mencapai 88,7–155,1% bergantung jalur tracker, atau 101,99% pada jalur utama").

**F3 (WAJIB).** Baris 9: "biaya komputasi yang tidak berarti (0,4% dari anggaran latensi pada subbab 4.5)" — salah label. 0,4% adalah proporsi terhadap total latensi pipeline terukur (0,11 ms dari 24,61 ms, Tabel 10), bukan terhadap anggaran 33,3 ms (yang menghasilkan 0,33%). Ganti menjadi "0,4% dari total latensi *end-to-end*". Kata "tidak berarti" juga ambigu dalam bahasa Indonesia (bisa terbaca "meaningless"); "abaikan terhadap total" lebih tepat — 4.5 sendiri memakai "dapat diabaikan" (baris 17).

Selain F1–F3: tidak ditemukan masalah. Semua angka lain konsisten dengan sumbernya; tidak ada angka yang dikarang.

## 2. LOGIKA SINTESIS

Tesis "setiap lapisan punya pembatas sendiri" akurat dan terpetakan benar: deteksi → lantai struktural + truncasi tepi (4.1); pelacakan → asosiasi/identitas (4.2); logika hitung → *cooldown* vs kepadatan (4.3, 4.4); sistem → latensi perangkat (4.5). Runtunan "pembatas berpindah" antar paragraf tetap jujur karena paragraf deteksi sudah menyatakan lantainya terkunci di lapisan itu.

Temuan:

**F4 (WAJIB).** Baris 7: "penambahan mekanisme Re-ID terbukti lebih berpengaruh pada akurasi hitungan daripada peningkatan kualitas kotak itu sendiri." — atribusi melenceng dari bukti. Data 4.2 justru menunjukkan Re-ID murni (Deep-OC-SORT) hampir tidak mengubah akurasi agregat (HOTA 36,12 vs 36,51; IDF1 42,16 vs 42,88 pada MOT20) dan 4.2 menilai efeknya "berbeda jauh antar benchmark". Lonjakan IDF1/galat datang dari DiffMOT, yang merupakan paket *diffusion* + Re-ID, bukan penambahan Re-ID semata. 4.3 sendiri berhati-hati: "peringkat akurasi hitungan mengikuti kualitas asosiasi tracker". Perketat 4.6 ke klaim yang dibuktikan: kualitas asosiasi/identitas (bukan "mekanisme Re-ID") yang lebih menentukan; kalau ingin menyebut Re-ID, atribusikan ke mekanisme DiffMOT secara eksplisit.

**S1 (SARAN).** Baris 5: "pilihan arsitektur tidak mengubah akurasi" — pada klausul pertama ini tidak berskop, padahal Tabel 1 memuat YOLO26s yang akurasinya jelas di atas tier nano. Kalimat berikutnya sudah menyebut "ketiga model tingkat nano"; pindahkan skop itu ke klausul pertama ("pada tingkat nano, pilihan arsitektur tidak mengubah akurasi") agar tidak terbaca menyangkal tabelnya sendiri.

**S2 (SARAN).** Baris 7: klaim "galat hitung mengikuti peringkat IDF1 dan bukan MOTA" — diskriminasi ini bersih di DanceTrack (MOTA memeringkat OC-SORT teratas, tetapi galatnya ke-3; urutan IDF1 = urutan galat) dan pada kutub DiffMOT/LightTrack. Namun pada MOT20 peringkat tengah terbalik terhadap keduanya: IDF1 OC-SORT 42,88 > Deep-OC-SORT 42,16, sedangkan galat 22,38% > 16,71% (urutan galat justru memihak Deep-OC-SORT). Klaim tetap bisa dipertahankan lewat IDF1 agregat lintas benchmark (34,77 vs 34,76 — seri), tetapi tulisan sebaiknya memakai rumusan 4.3 ("kualitas asosiasi") atau menandai bahwa kesesuaian peringkat paling tegas pada DanceTrack.

## 3. OVERCLAIM

Tidak ditemukan masalah. Discussion tidak mengklaim generalisasi ke dataset/deployment di luar bukti: tidak ada penamaan MOT20/DanceTrack/CrowdHuman sebagai bukti universal, tidak ada klaim kebaruan yang tidak ditunjukkan Bab 4, dan klaim penutup dibatasi pada "konfigurasi operasional yang tepat". Interpretasi MR⁻²/pembanding eksternal tidak diulang di 4.6 (aman).

## 4. KONSISTENSI

- Konfigurasi operasional CD=30 / conf 0,30: 4.6 tidak menyebut nilainya, tetapi juga tidak ada yang bertentangan dengan 4.4–4.5. Konsisten secara pasif.
- Keputusan tracker: 4.6 tidak menyebut Deep-OC-SORT/OC-SORT sama sekali, padahal keputusan bersyarat perangkat (server GPU = Deep-OC-SORT; *edge* = OC-SORT pada 30,7 FPS) adalah salah satu kesimpulan 4.2/4.5 yang paling actionable dan justru layak disintesis di Discussion.

**S3 (SARAN).** Kalimat penutup menyebut "konfigurasi operasional yang tepat" tanpa pernah menamakannya — rujukan menggantung secara konseptual. Namakan eksplisit: *cooldown* 30 *frame*, *confidence* 0,30, Deep-OC-SORT pada GPU / OC-SORT pada *edge*. Ini menutup loop ke 4.4–4.5 dan membuat kalimat maksim di akhir berpijak pada keputusan konkret.

## 5. GAYA BAHASA

Tidak ada pola AI-slop berat: tidak ada tricolon kosong, tidak ada kalimat penutup yang mengulang pembuka kata per kata, transisi antar paragraf fungsional.

Catatan minor:

**S4 (SARAN).** Tiga paragraf berturut-turut dibuka dengan pola "Pada lapisan ..." (baris 5, 7, 9). Struktur paralel untuk sintesis lapisan adalah pilihan sah, tetasi variasikan minimal satu pembuka agar tidak terbaca template. Juga: baris 3 "membentuk satu kesimpulan yang saling menopang" — gramatika meleset ("satu kesimpulan" tidak mungkin "saling menopang"; yang saling menopang adalah bukti/skenarionya). Perbaiki menjadi mis. "membentuk satu kesimpulan yang ditopang bukti lintas skenario". Kalimat penutup (baris 11) memuat daftar empat butir lalu maksim abstrak; masih bisa diterima karena maksimnya berpijak pada daftar itu, tetapi akan lebih kuat setelah S3 menamai konfigurasinya.

## 6. KELAYAKAN JURNAL

Struktur temuan → implikasi sudah berjalan; runtunan per lapisan mudah diikuti; istilah konsisten ("galat", "lapisan", kotak/*frame* dicetak miring sesuai konvensi bab).

**F5 (WAJIB).** Batasan tidak diucapkan eksplisit. Discussion yang matang menutup dengan batasan; 4.6 hanya menyentuh batasan logika hitung (*cooldown* vs pejalan berdampingan). Batasan yang memang tersedia di subbab sumber dan pantas dinyatakan satu-dua kalimat: (a) satu kali pelatihan per model dengan satu *seed*, sehingga kesetaraan mAP tier nano adalah klaim dalam derau pengukuran (4.1); (b) evaluasi pada benchmark publik dengan deteksi *offline*, bukan *deployment* lapangan; (c) pilihan tracker bergantung perangkat sasaran, sehingga angka latensi 24,61 ms spesifik RTX 4090 (4.5). Tanpa ini, pembaca jurnal berpotensi membaca sintesis sebagai klaim umum.

---

## PERBAIKAN WAJIB

1. **F1** — Hapus "dan kualitas perangkat pelatihannya" (baris 5); atribusi yang sah adalah kapasitas model (4.1 baris 20).
2. **F2** — Ganti "galat *over-count* yang mencapai dua digit" (baris 9) dengan angka riil: 88,7–155,1% (Tabel 7) / 101,99% jalur utama (Tabel 8).
3. **F3** — Ganti "0,4% dari anggaran latensi" (baris 9) menjadi "0,4% dari total latensi *end-to-end*"; pertimbangkan "dapat diabaikan" alih-alih "tidak berarti".
4. **F4** — Perbaiki atribusi baris 7: yang terbukti menentukan adalah kualitas asosiasi/identitas (bukti: DiffMOT), bukan "penambahan mekanisme Re-ID" — Deep-OC-SORT (Re-ID murni) nyaris nol efek agregatnya di 4.2.
5. **F5** — Tambahkan 1–2 kalimat batasan eksplisit: satu *seed* per model, evaluasi benchmark publik (bukan *deployment*), latensi 24,61 ms spesifik perangkat GPU dengan keputusan tracker bersyarat perangkat.

## SARAN

1. **S1** — Skopkan "pilihan arsitektur tidak mengubah akurasi" ke tingkat nano sejak klausul pertama (baris 5).
2. **S2** — Hedging klaim "galat mengikuti IDF1 dan bukan MOTA" (baris 7): tegas di DanceTrack dan kutub DiffMOT/LightTrack; peringkat tengah MOT20 menyimpang — rumusan "kualitas asosiasi" ala 4.3 lebih tahan uji.
3. **S3** — Namakan konfigurasi operasional di kalimat penutup (CD=30, conf 0,30, Deep-OC-SORT GPU / OC-SORT *edge*) agar "konfigurasi operasional yang tepat" tidak menggantung.
4. **S4** — Variasikan satu pembuka paragraf "Pada lapisan ..." dan perbaiki gramatika "satu kesimpulan yang saling menopang" (baris 3).
