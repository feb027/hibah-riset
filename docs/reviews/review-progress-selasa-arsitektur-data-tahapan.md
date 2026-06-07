# Strict Review — Progress Selasa: Arsitektur, Data, dan Tahapan

## Verdict

`READY_WITH_MINOR_REVISIONS_BEFORE_WORD_COPY`

Artifact sudah menjawab tiga arahan utama dosen: arsitektur/formalisme sistem, data eksperimen beserta statistik dan preprocessing, serta tahapan pengembangan/eksperimen. Secara umum naskah hati-hati karena menyatakan bahwa bagian ini masih berupa rancangan metodologi dan tidak mengklaim hasil eksperimen numerik. Namun, sebelum dipindahkan ke Word atau digabungkan ke draft paper, masih ada beberapa perbaikan ketat terkait konsistensi bibliografi, keterlacakan angka dataset, dan pembersihan unsur instruksional.

## Ruang Lingkup Review

File yang direview:

- `docs/revisions/progress-selasa-arsitektur-data-tahapan-copy-to-word.md`

Bukti lokal yang digunakan:

- `docs/research/source-ledger.md`
- `docs/research/evidence-matrix.md`
- `docs/_extracted/Status_Indeksasi_Referensi.txt`
- `references/references.bib`

## Temuan Utama

### 1. Kesesuaian dengan arahan dosen

Status: **terpenuhi dengan catatan minor**.

- Bagian 1 sudah menjelaskan arsitektur `input video → preprocessing → detector → tracker → counting logic → output/evaluasi` dan menambahkan formalisme ID state memory serta algoritma prosedural.
- Bagian 2 dan 3 sudah memisahkan fungsi data deteksi, tracking, dan video target untuk validasi counting end-to-end. Ini selaras dengan evidence matrix yang menekankan bahwa dataset standar tidak otomatis memvalidasi people counting berbasis event.
- Bagian 4 dan 5 sudah merinci tahapan eksperimen S1–S4 sehingga tidak hanya berupa daftar model.
- Catatan batasan di Bagian 7 penting dan perlu dipertahankan karena mencegah overclaim hasil sebelum eksperimen dijalankan.

Catatan: untuk kebutuhan Word final, placeholder gambar pada baris 11 dan 96 harus dihapus setelah gambar benar-benar disisipkan. Jangan biarkan teks `[Sisipkan Gambar ...]` ikut masuk ke naskah final.

### 2. Factuality dan sumber bukti

Status: **cukup kuat, tetapi ada risiko keterlacakan angka dataset**.

- Klaim arsitektur detection-tracking-counting didukung oleh S010, S011, dan S035 sesuai source ledger dan evidence matrix. Draft juga sudah benar membatasi S035 sebagai dokumentasi teknis, bukan bukti akademik utama.
- Posisi YOLO26 sudah aman: S001 disebut sebagai preprint/konteks implementasi, sedangkan argumen akademik ditopang oleh YOLOv10/RT-DETR melalui S003 dan S004.
- Posisi DiffMOT dan OC-SORT sudah proporsional: DiffMOT sebagai tracker utama yang akan diuji, OC-SORT sebagai baseline/fallback efisien. Ini konsisten dengan source ledger S021 dan S024.
- Klaim bahwa CrowdHuman, MOT20, dan DanceTrack tidak otomatis memvalidasi counting end-to-end sudah tepat dan sesuai evidence matrix.

Masalah yang perlu diperbaiki:

1. **Angka statistik dataset tertentu belum seluruhnya terlacak ke empat file bukti utama.** Contoh: baris 61 memuat `15.000 citra`, `339.565 anotasi person`, dan `99.227 ignore region`; baris 62 memuat `8.931 frame`, `2.215 track`, dan `1.134.614 bounding box`; baris 63 memuat `990 instance`, `105 ribu frame`, dan `877 ribu bounding box`. Beberapa angka umum seperti `470 ribu instance`, `22,6 orang per gambar`, dan `246 pedestrian per frame` tercermin dalam source ledger/ringkasan sumber, tetapi statistik rinci yang disebut sebagai “dokumen kerja penelitian ini” perlu diberi sumber eksplisit atau dipindahkan ke lampiran data internal. Untuk draft akademik, frasa “dokumen kerja penelitian ini” terlalu longgar jika tidak ada dokumen bernomor/berjudul yang bisa dirujuk.
2. **Klaim “terbaru” pada YOLO26 sebaiknya dilembutkan menjadi “salah satu kandidat implementasi terbaru”** agar tidak menjadi klaim absolut yang sulit dipertahankan pada tanggal submit.
3. **Status indeksasi tidak boleh menjadi klaim yang terlalu besar.** Draft sudah berhati-hati, tetapi frasa “peer-reviewed utama mencakup S003, S004, S021, S024, S025, S026, dan S037” perlu dipastikan selaras dengan versi bibliografi final karena beberapa entry BibTeX saat ini masih berbentuk arXiv, bukan entry proceedings.

### 3. Integritas sitasi dan S-code citation style

Status: **format S-code naskah baik; metadata bibliografi perlu dirapikan**.

Yang sudah baik:

- Tidak ditemukan sitasi numerik gaya angka-bersiku pada draft.
- Sitasi naratif menggunakan pola penulis-tahun-kode, misalnya `Diaz-Santos dkk. (2025 – S010)` dan `Lv dkk. (2024 – S021)`. Ini sesuai kebutuhan S-code citation style.
- Tidak ada tumpukan sitasi panjang di akhir paragraf. Klaim utama umumnya ditempelkan pada kalimat yang relevan.
- S-code yang digunakan dalam draft ditemukan di `source-ledger.md` dan `references.bib`: S001, S003, S004, S010, S011, S021, S024, S025, S026, S035, S036, S037, S038. S002 juga ada di `references.bib` meskipun hanya disebut dalam catatan status, bukan sebagai sitasi utama.

Masalah yang perlu diperbaiki sebelum final:

1. **Beberapa venue yang diklaim di draft/status belum tercermin dalam `references.bib`.** Contoh: S003 disebut NeurIPS 2024 di draft dan source ledger, tetapi `references.bib` masih berupa entry arXiv; S004 disebut CVPR 2024, tetapi entry BibTeX memakai tahun arXiv 2023; S021 disebut CVPR 2024, tetapi BibTeX masih arXiv; S024 disebut CVPR 2023, tetapi BibTeX masih arXiv 2022; S037 disebut CVPR 2022, tetapi BibTeX masih arXiv 2021. Jika naskah menyebut venue peer-reviewed, bibliografi final harus memakai metadata proceedings yang konsisten.
2. **S025 memiliki potensi inkonsistensi tahun.** Draft menyebut `Luiten dkk. (2021 – S025)` dan status indeksasi menyebut IJCV 2021, sedangkan `references.bib` mencatat year 2020. Pilih satu bentuk sitasi final berdasarkan metadata publikasi resmi yang akan digunakan.
3. **Baris 147 menyebut “dokumen status indeksasi referensi internal”.** Untuk bahan progress internal masih bisa diterima, tetapi bila masuk ke paper atau laporan resmi, ubah menjadi klaim berbasis daftar referensi/bibliografi, bukan merujuk “dokumen internal”.

### 4. Risiko overclaim hasil eksperimen

Status: **aman**.

Draft tidak menyatakan bahwa eksperimen sudah menghasilkan akurasi, FPS, latency, MAE, MAPE, atau angka performa lain. Hampir semua bagian memakai bahasa rencana: “dirancang”, “digunakan untuk”, “wajib dicatat setelah data diperoleh”, “skenario eksperimen yang direncanakan”, dan “akan diuji”. Ini sesuai dengan tahap metodologi.

Catatan ketat: baris 120 menyatakan tujuan S3 adalah “menilai apakah ID state memory mengurangi hitung ganda dan event yang hilang.” Kalimat ini masih aman karena berupa tujuan evaluasi, tetapi saat ditulis di paper hasil nanti jangan berubah menjadi “ID state memory mengurangi...” sebelum eksperimen benar-benar menunjukkan demikian.

### 5. Nada akademik Indonesia dan anti-slop phrasing

Status: **cukup baik, perlu sedikit pemolesan istilah**.

Kekuatan:

- Nada umum akademik, hati-hati, dan tidak terlalu promosi.
- Draft menghindari frasa hiperbolik seperti “sangat revolusioner”, “terbukti unggul”, atau “solusi terbaik”.
- Ada pemisahan jelas antara sumber akademik, preprint, dan dokumentasi vendor.

Perlu pemolesan:

- Beberapa istilah Inggris beruntun dapat dibuat lebih natural dalam Bahasa Indonesia akademik: `pipeline`, `fallback`, `stress test`, `robustness tracker`, `appearance cue`, `missed-counting`, `double-counting`. Jika tetap dipakai, konsistenkan italic atau beri padanan Indonesia pada kemunculan pertama.
- Frasa “Gambar 1 dapat digunakan...” dan “Gambar 2 dapat digunakan...” terasa instruksional/template. Untuk naskah Word, ubah menjadi kalimat deskriptif, misalnya “Gambar 1 merangkum arsitektur sistem yang diusulkan.”
- “Dokumen kerja penelitian ini juga mencatat...” perlu diganti dengan rujukan yang lebih formal atau dihapus jika tidak akan dicantumkan sebagai sumber.

### 6. Struktur dan kelayakan copy-to-Word

Status: **layak setelah pembersihan kecil**.

- Struktur heading sudah jelas dan langsung menjawab target progress.
- Tabel 1–4 informatif, tetapi tabel cukup panjang. Untuk Word, pastikan lebar kolom tidak membuat teks terlalu padat.
- Algoritma 1 sudah membantu formalisme counting logic, tetapi perlu diputuskan apakah akan masuk sebagai blok algoritma formal atau cukup sebagai pseudocode naratif.
- Placeholder gambar harus diganti dengan gambar aktual dan caption tunggal. Jangan sisakan path file di dokumen final kecuali memang diminta sebagai catatan teknis.

## Daftar Revisi Wajib Sebelum Word Final

1. Samakan metadata `references.bib` dengan klaim venue/tahun pada draft untuk S003, S004, S021, S024, S025, dan S037.
2. Tambahkan sumber eksplisit untuk statistik dataset rinci yang saat ini dikaitkan dengan “dokumen kerja penelitian ini”, atau ubah menjadi statistik umum yang sudah jelas didukung oleh S036/S037/S038.
3. Ganti kalimat instruksional placeholder gambar menjadi caption/rujukan gambar final setelah gambar disisipkan.
4. Lembutkan klaim “YOLO26 kandidat implementasi terbaru” menjadi “salah satu kandidat implementasi terbaru”.
5. Hilangkan atau formalkan frasa “dokumen status indeksasi referensi internal” jika bagian tersebut akan masuk ke naskah akademik resmi.
6. Rapikan istilah Inggris agar konsisten dengan gaya akademik Indonesia.

## Kesimpulan

Artifact ini sudah substantif dan tidak memiliki blocker metodologis besar. Ia layak dipakai sebagai bahan progress dosen karena menjawab arsitektur/formalisme, statistik dan preprocessing data, serta tahapan pengembangan/eksperimen. Perbaikan yang masih diperlukan terutama berada pada integritas bibliografi, keterlacakan angka statistik dataset, dan pembersihan format sebelum copy-to-Word.
