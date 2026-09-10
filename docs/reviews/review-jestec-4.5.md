LAYAK DENGAN REVISI MINOR

Review subbab 4.5 End-to-End Performance (docs/journal/4.5-end-to-end-performance.md)
Sumber resmi: docs/reports/laporan-skenario-d-realtime.md (Laporan Skenario D, 16 Agustus 2026)
Reviewer: agen review akademik (netral, bukan penulis draft). Review ini tidak mengubah draft.

====================================================================
1. KESESUAIAN DATA TERHADAP SUMBER (Tabel 10, Tabel 11, prosa persentil)
====================================================================

Tabel 10 (draft baris 9-15) vs Skenario D Tabel A (baris 27-34): SEMUA SEL COCOK.
- Preprocessing 0,85 ms / 3,5% ✓; Deteksi YOLO26 14,20 ms / 57,7% ✓; Tracker & Re-ID
  Deep-OC-SORT (crop Re-ID + VDC + ACM) 9,45 ms / 38,4% ✓; PeopleCounter 0,11 ms / 0,4% ✓;
  Total 24,61 ms ✓; Throughput 40,6 FPS ✓. Komponen dan label identik dengan sumber.

Tabel 11 (draft baris 23-27) vs Skenario D Tabel B (baris 40-43): SEMUA SEL COCOK.
- OC-SORT edge: 1,32 / 28,42 / 2,67 / 0,16 / 32,57 / 30,7 FPS ✓
- Deep-OC-SORT edge: 1,38 / 41,68 / 39,76 / 0,18 / 83,01 / 12,0 FPS ✓
- Baris ketiga (RTX 4090, sel kosong, total 24,61 / 40,6 FPS) adalah agregasi sah dari
  Tabel A sumber; penulisan sel "—" jujur karena breakdown GPU memang berasal dari tabel lain.

Prosa persentil (draft baris 31) vs Tabel distribusi sumber (baris 51-55):
- P95 32,10 ms ✓ dan P99 36,40 ms ✓ (Deep-OC-SORT RTX 4090) — dikutip akurat.
- P90 29,50 ms sumber TIDAK dikutip di draft. Bukan kesalahan (lihat Saran S4).

TEMUAN F1 — WAJIB. Draft baris 31: "Lonjakan latensi hanya terjadi pada *frame* dengan
lebih dari 50 orang sekaligus". Sumber baris 59: "Lonjakan latensi **maksimum** hanya
terjadi pada frame dengan lebih dari 50 orang sekaligus". Draft menggugurkan kata
"maksimum", sehingga klaim meluas dari "lonjakan puncak" menjadi "semua lonjakan".
Data sumber tidak mendukung klaim yang meluas: P99 = 36,40 ms berarti ±1% frame
melampaui anggaran, dan sumber hanya mengaitkan kondisi >50 orang dengan lonjakan
maksimum. Pulihkan kualifikasi "maksimum" (atau "paling ekstrem").

TEMUAN F2 — WAJIB. Draft baris 31: "Pada kondisi ekstrem tersebut *throughput* sesaat
turun di bawah 30 FPS, tetapi kembali normal begitu kerumunan mencair." Kalimat ini
TIDAK ADA di sumber. Sebagian dapat diturunkan (frame latensi maksimum 42,10 ms
berarti 1000/42,10 ≈ 23,8 FPS pada frame tersebut), tetapi (a) draft tidak menyajikan
perhitungan itu, (b) "sesaat turun di bawah 30 FPS" sebagai pernyataan umum tentang
seluruh frame padat tidak didukung data, dan (c) "kembali normal begitu kerumunan
mencair" adalah narasi yang murni dikarang. Hapus kalimat, atau dasarkan eksplisit
pada angka sumber (mis. "frame dengan latensi maksimum 42,10 ms setara ±23,8 FPS").

====================================================================
2. VERIFIKASI ARITMETIKA
====================================================================

Tidak ditemukan masalah. Semua angka dihitung ulang:
- Proporsi Tabel 10: 0,85/24,61 = 3,45% → 3,5% ✓; 14,20/24,61 = 57,70% ✓;
  9,45/24,61 = 38,40% ✓; 0,11/24,61 = 0,45% → 0,4% ✓ (mengikuti sumber; jumlah
  kolom tetap 100,0%). Sums komponen = 24,61 ms tepat.
- Throughput: 1000/24,61 = 40,63 → 40,6 FPS ✓; 1000/32,57 = 30,70 → 30,7 FPS ✓;
  1000/83,01 = 12,05 → 12,0 FPS ✓. Total baris edge: 32,57 dan 83,00 (sumber
  menulis 83,01; selisih pembulatan 0,01 ms, draft mengikuti sumber — konsisten).
- Cadangan performa: (33,3 − 24,61)/24,61 = 35,3%; draft "sekitar 35%" ✓
  (sumber: "Cadangan Performa +35%").
- Klaim P95: 32,10 ms < 33,3 ms, jadi "95% frame diproses di bawah anggaran 33,3 ms"
  (draft baris 31) SAH. Perlu dicatat P99 = 36,40 ms > 33,3 ms — draft tidak pernah
  mengklaim P99 di bawah anggaran, jadi tidak ada overclaim di sisi ini.
- Klaim zero-overhead counter: 0,11 ms dan 0,4% cocok dengan sumber ("Zero Overhead
  <1%", baris 32, 66-67) dan klaim linearitas O(N) terhadap tracklet aktif sesuai
  sumber baris 67.

====================================================================
3. KONSISTENSI ANTAR-SUBBAB (4.2, 4.3, 4.4)
====================================================================

Keputusan tracker (Deep-OC-SORT di GPU, OC-SORT di edge): SAH dan konsisten.
- Skenario D memang menguji kedua jalur di edge dan menyimpulkan OC-SORT lolos
  (30,7 FPS) sedangkan Deep-OC-SORT tidak (12,0 FPS, baris 42-43).
- 4.2 (baris 24) menetapkan "Deep-OC-SORT dipilih sebagai tracker utama sistem,
  dengan DiffMOT sebagai pembanding kualitas"; 4.3 (baris 17) mengulangi pemilihan
  itu dengan throughput 40,6 FPS — angka yang sama persis dengan Tabel 10 draft 4.5 ✓.
- Prosa 4.5 (baris 29) menjelaskan pemilihan bersyarat perangkat ("server GPU memakai
  Deep-OC-SORT demi akurasi, perangkat *edge* memakai OC-SORT") sehingga tidak
  dipandang kontradiktif dengan status "tracker utama" di 4.2/4.3.

TEMUAN F3 — WAJIB. 4.4 menutup (baris 45): "Subbab 4.5 mengukur performa *end-to-end*
pada konfigurasi operasional *cooldown* 30 *frame* dan *confidence* 0,30". Draft 4.5
TIDAK menyebut setelan ini di mana pun — tidak di intro (baris 3), tidak di 4.5.1,
tidak di 4.5.2. Janji silang-subbab menggantung dan pembaca tidak dapat mengetahui
konfigurasi di balik angka 24,61 ms / 40,6 FPS. Perlu: satu klausa pada paragraf
pembuka 4.5, mis. "Pengukuran dilakukan pada konfigurasi operasional hasil subbab
4.4 (*cooldown* 30 *frame*, *confidence* 0,30)". Perbaikan satu kalimat, tanpa
perubahan data.

TEMUAN S1 — SARAN. Densitas kerumunan berpotensi membingungkan pembaca: 4.2 (baris 20)
menyebut "kepadatan deteksi mencapai rata-rata 179 kotak per *frame*" pada MOT20-*train*
(4 sekuens), sedangkan 4.5 (baris 3) menyebut MOT20-02 memuat "rata-rata 34–38 orang
per *frame*". Keduanya dapat benar (179 = kotak deteksi lintas 4 sekuens termasuk
sekuens terpadat; 34–38 = orang pada MOT20-02 saja), tetapi tanpa konteks pembaca
akan melihat lompatan 5×. Satu klausa penjelas (cakupan sekuens dan definisi kotak
vs orang) menutup celah ini.

====================================================================
4. GAYA BAHASA (ANTI-AI)
====================================================================

Tidak ditemukan masalah berarti. Tidak ada tricolon berlebihan, tidak ada paragraf
penutup rangkuman yang berulang, tidak ada frasa template ("edelweiss", "krusial",
"responsif", "signifikan meningkatkan"). Prosa padat dan sejalan dengan register
subbab 4.1–4.4. Dua catatan kecil:

TEMUAN S2 — SARAN. "cadangan performa sekitar 35% *di atas* ambang *real-time*"
(baris 17) rancu secara semantik: cadangan adalah selisih terhadap ambang, bukan
sesuatu yang berada di atas ambang. Rumaskan "menyisakan cadangan performa ±35%
terhadap anggaran" atau langsung "24,61 ms, 35% di bawah anggaran 33,3 ms".
(Hasil koreksi bersama F2 sebaiknya dikerjakan dalam satu tarikan edit.)

TEMUAN S3 — SARAN. "tetapi kembali normal begitu kerumunan mencair" (baris 31)
adalah sentimen naratif yang tidak berbasis data — selain wajib dikoreksi secara
faktual (F2), penghapusannya sekaligus menghilangkan satu-satunya kalimat bergaya
cerita di subbab ini.

====================================================================
5. KELAYAKAN JURNAL (ALUR, TABEL, ISTILAH)
====================================================================

Alur logis: BAIK. 4.5.1 (budget GPU → lolos) → 4.5.2 (edge → keputusan tracker →
stabilitas persentil) mengikuti pertanyaan kunci Skenario D secara berurutan.
Tabel rapi, jumlah kolom konsisten, angka format Indonesia (koma desimal) seragam.

Istilah: "anggaran latensi" dipakai konsisten di intro dan 4.5.2 (33,3 ms); "throughput"
konsisten dan nilainya menyambung dengan Tabel 6 di 4.3 (40,6 FPS Deep-OC-SORT) ✓.
"Lantai deteksi" dari 4.1/4.3 memang tidak diperlukan di 4.5.

TEMUAN S4 — SARAN (tabel & istilah). (a) Label kolom Tabel 11 "Tracker+Re-ID (ms)"
menyesatkan untuk baris OC-SORT yang tidak memakai Re-ID (2,67 ms adalah pelacakan
murni). Label ini diwarisi dari sumber; pertimbangkan "Tracker (ms)" atau catatan
kaki. (b) "Preproses" (Tabel 11) vs "Preprocessing" (Tabel 10) — samakan salah satu.
(c) P90 = 29,50 ms dari sumber tidak dikutip; satu klausa ("P90 29,50 ms, artinya
90% frame selesai di bawah 29,5 ms") memperkuat argumen stabilitas tanpa menambah
tabel. Bersifat opsional.

====================================================================
RINGKASAN
====================================================================

PERBAIKAN WAJIB (3):
1. F1 — Baris 31: pulihkan kualifikasi "maksimum" pada klaim lonjakan latensi
   (>50 orang) agar setia pada sumber; klaim tanpa kualifikasi tidak didukung data.
2. F2 — Baris 31: hapus atau dasarkan pada data kalimat "throughput sesaat turun di
   bawah 30 FPS, tetapi kembali normal begitu kerumunan mencair" (tidak ada di sumber;
   versi sah: frame latensi maksimum 42,10 ms ≈ 23,8 FPS).
3. F3 — Tambahkan satu klausa konfigurasi pengukuran (cooldown 30 frame, confidence
   0,30) di paragraf pembuka 4.5 agar janji penutup 4.4 (baris 45) terpenuhi.

SARAN (4):
1. S1 — Beri konteks densitas MOT20 (179 kotak/frame di 4.2 vs 34–38 orang/frame
   di 4.5) agar tidak terbaca kontradiksi.
2. S2 — Perbaiki frasa "cadangan performa ... di atas ambang" menjadi relasi
   selisih yang benar.
3. S3 — Terselesaikan oleh penghapusan F2 (kalimat naratif "kerumunan mencair").
4. S4 — Samakan label "Preproses/Preprocessing"; label "Tracker+Re-ID" untuk baris
   OC-SORT; pertimbangkan mengutip P90 29,50 ms.

Tidak ditemukan: fabrikasi angka, sel tabel yang menyimpang dari sumber, kesalahan
aritmetika, pola gaya AI yang berarti, inkonsistensi istilah lintas 4.1–4.4.
