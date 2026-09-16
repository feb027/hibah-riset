# Catatan Riset — HKI Program Komputer (Sep 2026)

Catatan di balik `hki-rancage.md`. Isinya tiga hal: syarat administratif pencatatan hak cipta program
komputer, cara membuat diagram yang rapi, dan aturan penulisan bahasa Indonesia supaya tidak terbaca sebagai
tulisan model. Semua sumber ada di bagian akhir, diakses 16 September 2026.

---

## 1. Syarat dan batasan pencatatan hak cipta program komputer

Dasar hukum: UU Nomor 28 Tahun 2014 tentang Hak Cipta, Peraturan Pemerintah Nomor 16 Tahun 2020 tentang
Pencatatan Ciptaan dan Produk Hak Terkait, serta Peraturan Pemerintah Nomor 45 Tahun 2024 untuk tarif PNBP.

Yang perlu dipegang:

- **Program Komputer masuk ciptaan yang dilindungi**, tercantum eksplisit di Pasal 40 ayat (1) huruf s UU 28/2014.
  Definisinya di Pasal 1 angka 9: seperangkat instruksi yang diekspresikan dalam bentuk bahasa, kode, skema, atau
  bentuk apapun yang ditujukan agar komputer bekerja melakukan fungsi tertentu.
- **Pelindungan timbul otomatis**, bukan karena pencatatan (sistem deklaratif). Pencatatan hanya berfungsi sebagai
  bukti awal kepemilikan bila terjadi sengketa. Konsekuensinya, yang dinilai petugas dan calon pemohon banding
  adalah kejelasan deskripsi, bukan ada atau tidaknya pencatatan.
- **Masa pelindungan 50 tahun** sejak pertama kali diumumkan (Pasal 59 ayat (1) huruf e).
- **Yang dilindungi adalah ekspresi, bukan fungsi atau ide.** Ini titik paling sering salah. Uraian ciptaan yang
  isinya cuma kegunaan produk ("aplikasi untuk menghitung orang") lemah sebagai deskripsi ciptaan, karena fungsi
  tidak dilindungi hak cipta. Uraian yang kuat menerangkan bagaimana program itu dibentuk dan dirakit: modul,
  berkas, struktur data, alur pemrosesan, parameter, dan format keluaran. Karena itu bagian KODE PROGRAM dan
  penamaan berkas di dokumen ini bukan hiasan, melainkan bagian dari pemenuhan syarat substantif.
- **Judul ciptaan jangan generik.** Judul seperti "Aplikasi Kasir" atau "Sistem Informasi" menyulitkan petugas
  mengidentifikasi keunikan karya. Nama RANCAGE dengan perluasan singkatannya lebih aman.
- **Nama pencipta harus persis sama dengan KTP**, termasuk gelar dan ejaan. Beda satu huruf bisa memicu permintaan
  perbaikan.
- **Tanggal penciptaan tidak boleh melewati tanggal pengajuan permohonan.**
- **Dokumen yang dilampirkan** (Pasal 6 PP 16/2020): fotokopi identitas pemohon, contoh ciptaan atau penggantinya,
  surat pernyataan kepemilikan ciptaan, surat pengalihan hak bila hak ekonomi dialihkan, surat persetujuan tertulis
  bila pemohon lebih dari satu, surat kuasa bila diwakilkan, dan bukti pembayaran biaya.
- **Contoh ciptaan untuk program komputer berupa source code** dan manual penggunaan program. Praktik yang lazim
  diunggah berupa potongan kode bagian awal dan bagian akhir, ditambah tangkapan layar antarmuka. Berkasnya
  dikirim dalam format PDF atau satu arsip terkompresi yang memuat juga README ringkas.
- **Tarif PNBP** mengikuti PP 45/2024. Angka yang beredar di berbagai panduan tidak seragam (Rp200.000 untuk
  perorangan dan UMKM; kisaran Rp300.000 sampai Rp400.000 untuk badan usaha), dan PP 30 Tahun 2026 yang
  menggratiskan pencatatan hanya berlaku untuk karya lagu dan musik. Program komputer tetap berbayar, jadi
  pastikan angka terbaru saat pembayaran di SIMPAKI.
- **Alur pendaftaran**: akun di laman hakcipta.dgip.go.id, pilih jenis ciptaan Program Komputer, isi data pencipta
  dan pemegang hak, unggah dokumen dan contoh ciptaan, bayar PNBP, lalu unduh Surat Pencatatan Ciptaan secara
  elektronik. Sistem POP HC (Persetujuan Otomatis Pencatatan Hak Cipta) mempercepat prosesnya.

**Konsekuensi untuk dokumen ini**: struktur mengikuti contoh yang diberikan (DAFTAR ISI, PENDAHULUAN, METODE,
KODE PROGRAM, DAFTAR PUSTAKA), tetapi isi PENDAHULUAN diarahkan ke karakteristik program, bukan hanya manfaatnya.
Cover dibuat manual sesuai permintaan.

---

## 2. Membuat diagram tahapan penelitian dan arsitektur

### Pilihan alat

| Pendekatan | Untuk apa | Catatan |
| --- | --- | --- |
| Mermaid (teks) | diagram alur dan arsitektur, versi awal | bisa di-render langsung di GitHub dan Markdown; sintaksnya teks sehingga bisa diedit dan dilacak Git |
| draw.io / diagrams.net | hasil akhir untuk cetak | impor kode Mermaid lalu rapikan manual; punya bentuk standar ANSI/ISO |
| Figma, Lucidchart, Canva, Visio | diagram yang butuh tata letak bebas | berlebihan untuk diagram alur riset |

Kesimpulan riset: **Mermaid untuk menyusun, draw.io untuk memoles**. Itu pola yang dipakai pada penelitian
pengembangan di jurnal HEXAGON (lihat sumber), dan alasannya praktis. Mermaid menghemat waktu menggambar, tetapi
tata letaknya otomatis sehingga belum tentu sesuai standar. draw.io memakai bentuk simbol yang benar dan jalur
ortogonal. Kedua berkas `.mmd` di folder ini disiapkan untuk alur kerja tersebut.

### Prosedur yang dipakai

1. Tulis kode Mermaid di berkas `.mmd`.
2. Render dengan mermaid-cli untuk uji cepat: `npx -y @mermaid-js/mermaid-cli@11 -p pptr.json -b white -s 3 -i in.mmd -o out.png`.
   Pada Ubuntu 23.10 ke atas, Chromium perlu berkas konfigurasi puppeteer berisi `"args": ["--no-sandbox"]`,
   kalau tidak proses gagal dengan pesan *No usable sandbox*.
3. Untuk hasil cetak, buka draw.io, pilih Arrange, Insert, Advanced, Mermaid, tempel kode dari berkas `.mmd`.
4. Rapikan di draw.io: `Ctrl+A` lalu set waypoints ke orthogonal, samakan ukuran kotak, ubah kotak Mulai dan
   Selesai menjadi terminator (opsi rounded), dan ganti garis yang bertumpuk dengan konektor bulat.

### Aturan bentuk simbol

- Oval atau kapsul (terminator) untuk Mulai dan Selesai.
- Persegi panjang untuk proses atau tindakan.
- Jajar genjang untuk masukan dan keluaran data.
- Belah ketupat untuk keputusan yang bercabang.
- Segi enam untuk tahap khusus seperti varian model, dipakai pada diagram tahapan di dokumen ini.
- Alur dibaca dari atas ke bawah, teks di dalam simbol berupa kata kerja operasional yang pendek.
  Penjelasan panjang ditaruh di paragraf bawah gambar, bukan di dalam kotak.

### Catatan hasil render

Kedua diagram sudah di-render dan diperiksa secara visual. Diagram tahapan berbentuk empat band horizontal
berwarna sesuai contoh yang diberikan, dengan kolom fase di sisi kanan. Diagram arsitektur berbentuk alur
vertikal dengan satu percabangan simetris. Kalau kolom fase ingin dipindah ke kiri seperti contoh, geser saja
di draw.io; posisi itu ditentukan mesin tata letak Mermaid, bukan oleh kode.

---

## 3. Gaya penulisan bahasa Indonesia untuk dokumen HKI

### Prinsip akademik yang dipakai

- Bahasa Indonesia baku, lugas, dan langsung ke persoalan. Kalimat efektif, hindari berbelit.
- Objektif: klaim didukung data atau pustaka, bukan pendapat pribadi.
- Konsisten pada istilah, format sitasi, penomoran tabel dan gambar, dari awal sampai akhir.
- Hindari kata ganti orang pertama dan kedua. Pakai bentuk impersonal atau kata "penulis" bila perlu.
- Tidak memakai singkatan yang belum dijelaskan pada kemunculan pertamanya.

### Yang harus dihindari supaya tidak terbaca sebagai tulisan model

Riset September 2026 menunjukkan dua hal yang berubah dari tahun sebelumnya. Pertama, GPT-5.1 ke atas sudah
menekan pemakaian em dash, jadi teks tanpa em dash bukan lagi bukti tulisan manusia. Kedua, model terbaru justru
lebih rajin memakai titik dua untuk memperkenalkan ide lanjutan, sekitar empat kali laju manusia, dan titik koma
sekitar tiga kali. Jadi yang perlu dijaga bukan cuma em dash.

Daftar periksa yang saya pakai:

1. **Em dash berpasangan** yang mengapit daftar. Pola `X — a, b, c — adalah ...` adalah sidik jari yang paling
   sering. Ganti dengan koma, tanda kurung, atau susun ulang kalimatnya. Nol em dash di badan dokumen ini.
2. **Titik dua dan titik koma berlebihan.** Sisakan hanya yang memang memperkenalkan rincian.
3. **Pembuka paragraf yang seragam.** Jaga pembuka "Hal ini", "Dalam", "Selain itu", "Dengan" di bawah separuh
   kalimat dalam satu paragraf. Mulai sebagian kalimat dengan kata kerja, angka, nama, atau klausa keterangan.
4. **Panjang kalimat yang seperti metronom.** Jangan tiga kalimat berturut-turut dengan panjang serupa. Campur
   kalimat pendek dan panjang, tetapi jangan bergantian secara mekanis, karena pola jungkat-jungkit pendek-panjang
   juga sudah jadi sidik jari model terbaru.
5. **Busur argumen yang selalu sama.** Pola Pembukaan, Ekspansi, Kontras, Resolusi terdeteksi dalam tiga sampai
   empat kalimat. Pecah di beberapa bagian: buka dari komplikasi, atau akhiri bagian pada fakta konkret.
6. **Paragraf mini berlebihan dan spam poin.** Model terbaru cenderung memecah teks jadi banyak paragraf satu
   sampai dua kalimat. Paragraf yang lebih panjang dan mengalir lebih wajar untuk dokumen resmi.
7. **Kosa kata seragam yang generik.** "Sangat krusial", "mendorong", "menjamin", "seiring berkembangnya",
   "penting untuk dicatat", "dalam konteks ini", "tidak hanya X tetapi juga Y". Diganti dengan istilah bidang
   yang spesifik: HOTA, IDF1, IDSW, fragmentasi, fbox amodal, observation-centric, appearance embedding,
   cooldown debounce, tail latency.
8. **Partikel wacana.** Untuk tingkat formal, hampir nol. Dokumen ini tidak memakainya sama sekali.
9. **Kekayaan kata fungsi.** Variasikan penghubung dan preposisi (serta, dan, namun, sedangkan, sementara itu)
   ketimbang memakai satu kata yang sama sepanjang dokumen.

### Alat anti-AI yang paling kuat: spesifisitas

Bukan penggantian sinonim, bukan pula menambah kalimat retoris. Yang paling ampuh adalah menyebut hal konkret
yang hanya bisa ditulis oleh orang yang mengerjakan proyeknya: nama berkas (`core/counting/counter.py`), nama
kelas (`PeopleCounter`, `LineCrossDetector`), nilai parameter (cooldown 30 bingkai, confidence 0,30, resize
640 x 640), dan angka hasil (24,61 ms, 40,6 FPS, 6.905 IDSW). Data itu tidak mungkin dikarang dan sekaligus
memenuhi syarat HKI soal mendeskripsikan ekspresi program, bukan fungsinya. Karena itu kode dan angka di dokumen
ini dipertahankan apa adanya.

### Plagiarisme

Bentuk yang harus dihindari: plagiasi langsung (salin tempel tanpa tanda kutip), plagiasi parafrase (ganti kata
tetapi struktur dan alur tetap sama), plagiasi daur ulang (memakai tulisan sendiri yang sudah terbit tanpa
menyebutnya), plagiasi mozaik (menyisipkan frasa dari beberapa sumber tanpa kutipan), dan kutipan tidak tepat.

Cara menutupnya:

- Parafrasa benar-benar: gagasan orang lain diungkapkan dengan kalimat sendiri, sumber tetap disebut.
- Setiap kalimat yang memuat angka atau klaim dari penelitian lain diberi nomor rujukan.
- Bagian PENDAHULUAN dan METODE di dokumen ini ditulis dari nol berdasarkan data eksperimen di repositori,
  bukan terjemahan atau salinan dari naskah pihak lain. Paragraf pustaka memakai nomor rujukan ke DAFTAR PUSTAKA
  yang sama dengan naskah jurnal proyek ini.
- Uji kemiripan dijalankan sebelum pengajuan. Bila ada bagian yang menyerupai sumber, kalimatnya disusun ulang
  dari sudut pandang temuan sendiri.

---

## 4. Berkas di folder ini

| Berkas | Isi |
| --- | --- |
| `hki-rancage.md` | Dokumen utama, siap disalin ke Word. Cover dibuat manual. |
| `diagram-arsitektur-sistem.mmd` | Sumber Mermaid Gambar 1. |
| `diagram-tahapan-penelitian.mmd` | Sumber Mermaid Gambar 2. |
| `diagram-arsitektur-sistem.png` | Hasil render skala 3, siap tempel. |
| `diagram-tahapan-penelitian.png` | Hasil render skala 3, siap tempel. |

Gambar 3 sampai Gambar 10 memakai berkas yang sudah ada di repositori, bukan gambar baru. Jalurnya relatif
terhadap `docs/hki/`, jadi bila berkas dipindah, perbaiki jalurnya atau tempel gambarnya langsung ke Word.

---

## Sumber (diakses 16 September 2026)

1. DJKI, Kementerian Hukum RI — "Hak Cipta: Syarat dan Prosedur Permohonan". https://www.dgip.go.id/menu-utama/hak-cipta/syarat-prosedur
2. Peraturan Pemerintah Republik Indonesia Nomor 16 Tahun 2020 tentang Pencatatan Ciptaan dan Produk Hak Terkait. https://www.dgip.go.id/unduhan/download/peraturan-pemerintah-republik-indonesia-nomor-16-tahun-2020-tentang-pencatatan-ciptaan-dan-produk-hak-terkait-34-2020
3. UU Nomor 28 Tahun 2014 tentang Hak Cipta, salinan resmi. https://lpmpp.unsil.ac.id/wp-content/uploads/2025/04/UU-Nomor-28-Tahun-2014.pdf
4. LegalMP — "Cara Daftar Hak Cipta Software ke DJKI: Panduan Lengkapnya". https://legalmp.id/artikel/legalitas/cara-daftar-hak-cipta-software-ke-djki-panduan-lengkapnya
5. LegalMP — "Pendaftaran Hak Cipta Software: Prosedur, Syarat, dan Biayanya". https://legalmp.id/pendaftaran-hak-cipta-software-prosedur-syarat-dan-biayanya/
6. HEXAGON (Jurnal Teknik dan Sains), UTS — "Penerapan ChatGPT dan Draw.io untuk Otomatisasi Flowchart Menggunakan Mermaid Code". https://jurnal.uts.ac.id/index.php/hexagon/article/download/5153/2484
7. Masoem University — "Strategi Menyusun Diagram Alur Penelitian Bab 3 Skripsi". https://masoemuniversity.ac.id/artikel/strategi-menyusun-diagram-alur-penelitian-bab-3-skripsi-agar-metodologi-riset-mudah-dipahami-penguji/
8. Konsep Indonesia — "Membuat Flowchart di Markdown dengan Mermaid". https://konsep.id/membuat-flowchart-di-markdown-dengan-mermaid/
9. repo `adenaufal/anti-slop-writing`, panduan bahasa Indonesia. https://github.com/adenaufal/anti-slop-writing/blob/main/indonesian/AGENTS.md
10. Ruang Jurnal — "Gaya Penulisan Akademik: Pengertian, Ciri-Ciri, dan Cara Menerapkannya". https://ruangjurnal.com/gaya-penulisan-akademik-pengertian-ciri-ciri-dan-cara-menerapkannya/
11. Pedoman Penulisan Karya Ilmiah UIN Sultan Aji Muhammad Idris Samarinda, Bab VI dan Bab VII. https://pasca.uinsi.ac.id/wp-content/uploads/2025/11/PPKI-UINSI-SAMARINDA-2025_compressed.pdf
12. Etika Menulis Akademik di Era Digital, Universitas Jambi. https://repository.unja.ac.id/83062/1/ETIKA%20MENULIS%20AKADEMIK%20DI%20ERA%20DIGITAL.pdf
