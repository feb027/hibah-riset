# Prompt Image Generator untuk Diagram HKI

Catatan riset dan kumpulan prompt untuk membuat diagram HKI memakai generator gambar AI. Diriset
16 September 2026. **Diagram Mermaid yang sekarang tetap dipakai**; berkas ini alternatif, bukan pengganti.

---

## 0. Ringkasan temuan, baca ini dulu

Untuk membuat **diagram kotak dan panah**, generator gambar AI adalah alat yang lebih lemah daripada Mermaid
atau draw.io, bukan lebih kuat. Tiga alasan yang bisa diperiksa, bukan opini:

1. **Hasilnya raster dan tidak bisa diedit.** Salah satu label, regenerasi ulang. Mermaid diperbaiki dengan
   mengubah satu kata di berkas teks.
2. **Teks kecil masih jadi titik lemah.** GPT-image-2 memimpin dengan akurasi karakter sekitar 99 persen,
   Nano Banana Pro sekitar 95 persen namun turun ke 80 sampai 85 persen pada teks kecil. Nama diri dan istilah
   teknis adalah tempat kesalahannya muncul, misalnya `Elasticsearch` menjadi `Elasticseach`. Diagram HKI ini
   penuh nama teknis (Deep-OC-SORT, DiffMOT, LightTrack-ReID, YOLO26, HOTA, IDF1) dan itu justru kelas teks
   yang paling rawan.
3. **Ada jejak provenance yang tidak bisa dihapus.** Google membubuhkan watermark SynthID ke dalam piksel, dan
   OpenAI serta Google menandatangani berkas dengan C2PA Content Credentials. SynthID bertahan melewati
   pemotongan, kompresi, tangkapan layar, dan penempelan ke Word. Artinya gambar hasil generator bisa
   dibuktikan sebagai keluaran AI, bukan sekadar diduga.

Poin ketiga yang paling perlu dipertimbangkan, karena dua konteks berbeda memakainya dengan cara berbeda.

**Untuk jurnal.** Beberapa penerbit mengizinkan gambar AI untuk diagram penjelas asalkan diungkap di caption,
tetapi ada yang melarangnya sama sekali. Tabel lengkapnya ada di bagian 2.

**Untuk HKI.** Ini yang jarang dibahas. Pencatatan hak cipta adalah klaim kepemilikan atas ekspresi yang
dihasilkan pencipta. Kalau diagram di dokumen ciptaan adalah keluaran model, bagian itu bukan ekspresi pencipta
secara langsung, dan kalau nanti ada sengketa, gambar berwatermark SynthID adalah bukti yang merugikan pemohon
sendiri. Diagram Mermaid juga bukan gambar tangan, tetapi kodenya ditulis sendiri dan hasil visualnya ditentukan
oleh keputusan pencipta, jadi posisinya lebih kuat.

Kesimpulan praktis: pakai generator gambar untuk **mencari komposisi dan gaya**, lalu gambar versi finalnya
kembali di Mermaid atau draw.io. Kalau tetap mau memakai hasil generator apa adanya, pakai prompt di bagian 4
dan jalankan pemeriksaan di bagian 6.

---

## 1. Rasio aspek dan lebar cetak

Diagram HKI sekarang: arsitektur 2,21, peta metode 1,76, tahapan 1,32.

| Diagram | Rasio target | Rasio siap pakai |
| --- | --- | --- |
| Arsitektur sistem | 2,21 | `21:9` atau `2:1` |
| Peta metode deteksi dan tracking | 1,76 | `16:9` |
| Tahapan penelitian | 1,32 | `4:3` atau `3:2` |

Resolusi: pada lebar teks A4 sekitar 16 cm atau 6,3 inci, keluaran 2048 piksel setara 325 DPI dan itu cukup
untuk dokumen Word. Kalau mau aman untuk kebutuhan line art 1200 DPI, hanya Nano Banana Pro yang menyediakan
4K native. Model lain perlu upscale atau digambar ulang sebagai vektor.

Catatan tentang Google Flow: Flow adalah studio kreatif untuk video dan gambar, dan model bawaannya Nano Banana
Pro. Karena orientasinya pembuatan video dan adegan, pemakaian Flow untuk diagram akan cenderung dibawa ke arah
sinematik. Kalau tujuannya diagram statis, permukaan yang lebih langsung adalah aplikasi Gemini atau Google AI
Studio dengan model Nano Banana Pro dipilih eksplisit.

---

## 2. Kebijakan penerbit untuk gambar hasil AI

Diringkas dari kebijakan resmi per September 2026.

| Penerbit | Gambar penjelas (diagram, flowchart) | Gambar data | Posisi |
| --- | --- | --- | --- |
| Elsevier | Diizinkan | Dilarang untuk citra data | Ungkap di caption tiap gambar: nama alat, versi, cara pakai. Graphical abstract harus alat khusus, bukan generator umum |
| Springer Nature | Diizinkan bila berasal dari bahan yang bisa diverifikasi | Tidak dianggap sah | Gambar AI tanpa masukan yang bisa diverifikasi disebut opaque dan tidak diizinkan |
| Science (keluarga) | Tidak diizinkan | Tidak diizinkan | Penggunaan gambar AI yang tidak diungkap dianggap misconduct; ada penyaringan Proofig sejak 2024 |
| IEEE | Diungkap di acknowledgments | Fabrikasi gambar = pelanggaran integritas | Penulis bertanggung jawab 100 persen |
| MDPI | Diungkap | Diungkap | Penulis bertanggung jawab penuh atas konten berbantuan AI |
| JAMA Network | Diungkap | Diungkap | Sebut alat, versi, produsen |

Tiga hal yang disepakati semua penerbit: pengungkapan terbuka, akuntabilitas tetap di manusia, dan pemeriksaan
tambahan untuk gambar yang bisa disalahartikan sebagai data primer.

Konsekuensi untuk dokumen HKI ini: semua diagram di sini adalah diagram penjelas dan tidak ada yang menyajikan
data eksperimen. Grafik hasil pelatihan dan grafik perbandingan tracker tetap harus berasal dari data, bukan
dari generator.

---

## 3. Yang masih terbaca sebagai AI pada tahun 2026

Riset deteksi bergeser. Dua hal yang dulu jadi penanda utama sudah tidak berlaku: tangan dan teks pendek kini
dirender hampir sempurna oleh model teratas, jadi keduanya bukan bukti apa-apa lagi. Yang masih bekerja ada di
lapisan berbeda.

### Lapisan provenance, diperiksa lebih dulu

| Cara | Alat | Catatan |
| --- | --- | --- |
| Watermark SynthID | Aplikasi Gemini, unggah gambar lalu tanya apakah dibuat Google AI | Hanya menandai keluaran Google. Hasil "tidak ditemukan" bukan berarti bersih |
| Content Credentials | verify.contentauthenticity.org atau ekstensi browser C2PA | Metadata bisa hilang saat platform mengunggah ulang |
| Detektor | Minimal dua alat, misalnya Hive dan Illuminarty | Akurasi bersih sekitar 85 sampai 94 persen. Anggap skor sebagai petunjuk, bukan putusan |

### Lapisan tanda visual, untuk diagram secara khusus

Tanda fisika seperti arah bayangan dan pantulan tidak relevan untuk diagram garis. Yang relevan justru ini:

1. **Tidak mau menyisakan ruang kosong.** Ini penanda nomor satu untuk gambar gaya slide dan infografis. Model
   mengisi ruang sisa dengan hiasan: ikon kecil, garis aksen, pola latar. Diagram yang baik justru punya banyak
   ruang kosong.
2. **Palet pelangi.** Kotak berwarna-warni tanpa alasan semantik. Diagram akademik biasanya satu warna aksen
   ditambah abu-abu.
3. **Efek dekoratif.** Bayangan tebal, glow, gradien, bentuk 3D, gaya kaca atau glassmorphism. Semua ini muncul
   otomatis kalau tidak dilarang eksplisit.
4. **Ikon besar yang mengalahkan teks.** Ikon harus jadi penunjuk arah, bukan hierarki utama.
5. **Semua kotak berukuran sama.** Hierarki hilang; kotak yang penting tidak terlihat penting.
6. **Label yang hampir benar.** Bukan ngawur, tapi hampir: satu huruf meleset, tanda hubung bergeser, subscript
   jadi angka biasa. Jenis kesalahan ini paling berbahaya karena lolos pada pembacaan cepat.

---

## 4. Prompt

Alur kerjanya dua langkah. Langkah pertama menyusun struktur memakai model teks, langkah kedua menyuruh model
gambar menggambar berdasarkan struktur itu. Menuang teks mentah langsung ke model gambar menghasilkan diagram
yang isinya kurang dan logikanya campur.

### 4.1 Langkah 1, prompt penyusun struktur

Jalankan di model teks mana pun. Ganti bagian `[DIAGRAM]` dengan isi diagram yang dituju.

```text
You are a technical editor. Turn the material below into a diagram specification that an
illustrator can draw without asking questions.

Constraints:
- Maximum 6 groups. If the material has more, merge the least important ones.
- Maximum 5 nodes per group.
- Every node label is a short noun phrase, maximum 5 words. No sentences.
- Name every arrow and its direction explicitly.
- Fix the reading order: left to right, or top to bottom. State which one.
- Do not add any node, label, or relationship that is not in the material.
- If something in the material is ambiguous, list it under OPEN QUESTIONS instead of
  inventing a plausible answer.

Output format:
1. TITLE: one line, maximum 8 words
2. READING ORDER: left-to-right | top-to-bottom
3. GROUPS: for each group, a group title and its nodes as a numbered list
4. ARROWS: from node -> to node, one per line, with the condition if any
5. OPEN QUESTIONS: anything unresolved

Material:
[DIAGRAM]
```

### 4.2 Langkah 2, prompt penggambar

Blok berikut dipakai untuk ketiga diagram. Bagian yang berubah hanya `[ISI DIAGRAM]` dan `[RASIO]`.

```text
Draw a technical diagram for a printed academic document. It must look like a figure
produced in draw.io or Inkscape by a researcher, not like an infographic.

CONTENT
[ISI DIAGRAM]

READING ORDER
[Left to right / Top to bottom]. The primary path must be obvious within two seconds.

STYLE
- Plain white background, no texture, no paper grain.
- One accent colour (#2874A6) plus neutral grey (#5D6D7E) plus black. Nothing else.
- Flat 1 pt black outlines, 2 px border radius, no drop shadow, no gradient, no glow,
  no 3D, no glassmorphism.
- Typeface: a neutral sans-serif for node labels. Same size for every node at the same
  level of importance. Group titles one step larger.
- Generous whitespace. It is correct for the figure to have large empty areas.
- Grouped nodes sit inside a thin rectangular boundary with the group title in the top
  left corner of that boundary.
- Arrows are straight or orthogonal (right-angled) lines with small solid arrowheads.
  Dashed arrows only for feedback loops, with the loop label on the line.

TEXT RULES
- Render every label exactly as written, letter for letter. Do not translate, do not
  abbreviate, do not correct spelling.
- Keep hyphens, capitalisation, and digits exactly as given.
- No extra text anywhere: no legend that was not requested, no footer, no title unless
  listed, no numbering that was not requested.

HARD BANS
- Do not fill empty space with decoration, icons, patterns, or accent lines.
- Do not make every node the same size; hierarchy must be visible.
- Do not use rainbow colours, gradient fills, or coloured backgrounds per group beyond
  the single accent tint.
- Do not add icons larger than the label text.
- Do not invent nodes, labels, or connections that were not provided.
- Do not draw a legend.

CANVAS
Aspect ratio [RASIO]. High resolution. Clean enough to place at 16 cm wide in a Word
document at 300 DPI.
```

### 4.3 Yang berubah per diagram

| Diagram | `[RASIO]` | `[ISI DIAGRAM]` yang dipakai |
| --- | --- | --- |
| Arsitektur sistem | `21:9` | Isi `docs/hki/diagram-arsitektur-sistem.mmd`, bagian setelah kata `flowchart` |
| Peta metode | `16:9` | Isi `docs/hki/diagram-peta-metode-deteksi-tracking.mmd` |
| Tahapan penelitian | `4:3` | Isi `docs/hki/diagram-tahapan-penelitian.mmd` |

Karena kode Mermaid sudah memuat seluruh isi, struktur, dan relasinya, cara paling murah adalah menempelkan
kode Mermaid itu apa adanya ke `[ISI DIAGRAM]`. Model akan membacanya sebagai struktur dan bukan sebagai teks
untuk digambar ulang, sehingga hasilnya lebih setia.

### 4.4 Varian untuk GPT-image-2

Tambahkan baris ini di blok `TEXT RULES`:

```text
- This figure contains dense small labels and hyphenated technical names. Render every
  character at a legible size; if a label cannot fit, widen the node instead of shrinking
  the type.
- Subscripts and hyphenated model names must stay exact: YOLO26, YOLOv10, Deep-OC-SORT,
  LightTrack-ReID, MOT20, DanceTrack, HOTA, IDF1, IDSW, RoI.
```

GPT-image-2 punya keunggulan struktural pada teks kecil, istilah teknis, dan simbol, dan toleransi terhadap
prompt panjang jauh lebih baik. Model ini pilihan utama untuk diagram ini.

### 4.5 Varian untuk Nano Banana Pro atau Flow

Tambahkan baris ini:

```text
- Preserve the layout exactly as specified. Do not recompose, do not reinterpret, do not
  add visual storytelling.
- Keep the composition quiet and editorial. No cinematic lighting, no depth of field,
  no scene-like framing.
```

Nano Banana Pro punya kecenderungan menata ulang komposisi menjadi lebih indah tetapi melepas label opsional,
legenda, dan anotasi angka begitu promptnya panjang. Varian ini menahannya. Kalau mau memakai Flow, ingat bahwa
Flow adalah studio video dan gambar, jadi tambahan baris di atas wajib, bukan pilihan.

Aspek rasio tambahan yang hanya tersedia di Nano Banana 2 dan berguna untuk diagram: `1:4`, `4:1`, `1:8`, `8:1`.
Rasio ekstrem itu pas untuk diagram arsitektur yang memanjang mendatar.

### 4.6 Kalau mau hasil vektor

Recraft V3 mengeluarkan SVG asli, jadi hasilnya bisa diperbesar tanpa pecah dan bisa diedit sebagai vektor.
Harganya, kepatuhan terhadap prompt biasanya di bawah GPT-image-2 untuk diagram padat teks. Alur yang masuk akal:
susun di Recraft untuk dapat SVG, kirim SVG ke Recraft V3, jadikan PNG dan SVG, sisanya tidak diubah.

---

## 5. Urutan pengerjaan yang disarankan

1. Jalankan prompt 4.1 pada kode Mermaid diagram yang dituju.
2. Periksa hasil struktur. Kalau ada `OPEN QUESTIONS`, jawab dulu, jangan diteruskan mentah.
3. Jalankan prompt 4.2 dengan model pilihan. Untuk diagram HKI ini, mulai dari GPT-image-2. Nano Banana Pro
   dipakai kalau komposisi jadinya lebih penting daripada ketepatan label.
4. Periksa hasil dengan daftar di bagian 6. Perbaiki lewat prompt tambahan, jangan lewat alat edit gambar
   kecuali untuk memotong margin.
5. Kalau hasilnya dipakai: turunkan ke 300 DPI pada lebar 16 cm, dan tulis pengungkapan di caption.

---

## 6. Daftar periksa sebelum dipakai

Ini yang wajib dilakukan, bukan saran.

**Periksa teks, huruf per huruf.** Bandingkan setiap label hasil dengan spesifikasi dari langkah 4.1. Perhatikan
khusus nama berhubung dan bersubscript: Deep-OC-SORT, LightTrack-ReID, YOLO26, YOLOv10, MOT20, DanceTrack.
Satu huruf meleset cukup untuk membatalkan pemakaian.

**Periksa hubungan dan arah.** Setiap panah harus ada di bahan sumber, arahnya benar, dan tidak ada panah
tambahan. Kesalahan paling mahal adalah panah yang tampak masuk akal tetapi tidak ada di sumber.

**Periksa hierarki.** Kotak yang penting harus terlihat penting. Kalau semua sama, prompt perlu ditambah
instruksi hierarki.

**Periksa ruang kosong.** Kalau ada hiasan di area yang seharusnya kosong, itu tanda model mengisi ruang. Ulangi
dengan larangan yang lebih tegas.

**Jalankan pemeriksaan provenance.** Unggah hasilnya ke aplikasi Gemini dan tanyakan apakah dibuat oleh Google
AI. Untuk model lain, buka verify.contentauthenticity.org. Kalau tujuannya jurnal, hasil ini juga yang
dilaporkan di caption.

**Pengungkapan kalau dipakai.** Format yang diterima sebagian besar penerbit, ditaruh di caption gambar:

> Diagram dibuat dengan bantuan [nama model, versi]. Penulis memverifikasi seluruh label, arah panah, dan
> struktur terhadap data dan metode penelitian, dan bertanggung jawab penuh atas isi gambar.

---

## 7. Penilaian jujur

Waktu yang dibutuhkan untuk tiga diagram Mermaid ini: satu render, satu pemeriksaan, selesai. Rasio aspeknya
dikendalikan angka, labelnya dijamin benar karena berasal dari teks, dan hasilnya bisa diubah kapan saja.

Waktu untuk jalur generator gambar: satu prompt penyusun, tiga kali generate, pemeriksaan huruf per huruf pada
puluhan label, kemungkinan dua sampai tiga kali regenerasi, lalu pengungkapan di caption. Kemungkinan hasilnya
lebih menarik secara tampilan, tetapi pada label yang salah, seluruh keunggulan itu hilang dan diagramnya tidak
bisa dipakai.

Jadi jalur generator gambar masuk akal kalau hasilnya dipakai sebagai acuan komposisi, bukan sebagai gambar
akhir. Untuk gambar akhir di dokumen HKI dan naskah jurnal, Mermaid dan draw.io adalah jalur pendek.

## 8. Tiga prompt siap copas

Setiap blok di bawah berdiri sendiri. Tidak perlu langkah penyusun struktur lagi, karena isi, urutan, relasi,
dan warnanya sudah disebut eksplisit. Tempel satu blok, generate.

Semua prompt ini ditulis untuk **GPT-image-2**. Kalau memakai **Nano Banana Pro** atau Flow, tambahkan dua baris
ini di bagian STYLE:

```text
- Preserve the layout exactly as specified. Do not recompose, do not reinterpret, do not add visual storytelling.
- Keep the composition quiet and editorial. No cinematic lighting, no depth of field, no scene-like framing.
```

### 8.1 Diagram arsitektur sistem (rasio 21:9)

```text
You are drawing one figure for a printed academic paper. Output a single flat vector-style diagram. It must look like it was drawn in draw.io by the author, not like an infographic.

FIGURE: system architecture of a real-time people counting pipeline, arranged as two horizontal rows read left to right.

ROW 1 (three nodes, left to right):
1. "Video masukan" - terminator shape (rounded capsule)
2. "Preprocessing" with second line "resize 640 x 640, format tensor" - rectangle
3. "Deteksi Objek" with second line "YOLO26 head NMS-free" - rectangle, light blue fill #EBF5FB, border #2874A6

ROW 2 (five nodes):
4. "Pelacakan utama" with second line "Deep-OC-SORT" - rectangle, light green fill #EAFAF1, border #1E8449
5. "Pelacakan ringan" with second line "OC-SORT" - rectangle, same light green
6. "Logika Penghitungan" with second line "RoI polygon, garis virtual, validasi arah" - rectangle, light orange fill #FEF5E7, border #D68910
7. "ID State Memory" with second line "TRACKING / COOLDOWN" and third line "cooldown 30 bingkai" - rectangle, same light orange
8. "Keluaran" with second line "video beranotasi, CSV per bingkai, JSON" - terminator shape (rounded capsule)

ARROWS (exactly these, no others):
- 1 -> 2
- 2 -> 3
- one arrow from 3 down into row 2, splitting into two: 3 -> 4 and 3 -> 5
- 4 -> 6
- 5 -> 6
- 6 -> 7
- 7 -> 8
- one dashed arrow from 7 looping back up to 6, with the label "cegah double counting" placed on the dashed line

STYLE
- Plain white background. No texture, no grain, no gradient.
- Flat outlines, 1 pt black, 2 px corner radius on rectangles.
- No drop shadow, no glow, no 3D, no glassmorphism.
- Neutral sans-serif. All node labels the same size. Nothing larger than the labels.
- Nodes 1 and 8 are capsules; every other node is a rectangle.
- Arrowheads small and solid.
- Generous whitespace. Large empty areas are correct and expected.
- The whole figure must read as two clean horizontal rows.

TEXT RULES
- Reproduce every label exactly as written above, letter for letter, including the Indonesian words, hyphens and digits. Do not translate. Do not abbreviate. Do not correct spelling.
- Render "Deep-OC-SORT", "OC-SORT", "YOLO26", "TRACKING / COOLDOWN", "RoI", "CSV", "JSON" exactly.
- No title, no legend, no footer, no page number, no watermark, no signature.

HARD BANS
- Do not fill empty space with decoration, icons, patterns or accent lines.
- Do not add any node, label or arrow that is not listed above.
- Do not use rainbow colours. Only the three tint fills named above plus black text.
- Do not draw a legend or a colour key.

CANVAS: aspect ratio 21:9, high resolution, clean lines suitable for placement at 16 cm width in a Word document.
```

### 8.2 Diagram peta metode deteksi dan tracking (rasio 16:9)

```text
You are drawing one figure for a printed academic paper: a taxonomy chart. Output a single flat vector-style diagram. It must look like it was drawn in draw.io by the author, not like an infographic.

FIGURE: a map of object detection and multi-object tracking methods, arranged as FOUR vertical groups side by side, read left to right. There are NO arrows in this figure. Do not draw any arrow.

GROUP 1 - heading "Detektor - Pendekatan Klasik", light red fill #FDF2F0, border #C0392B
- "Background Subtraction" with second line "Otsu, GMM, ViBE"
- "Inter-frame Subtraction"
Both nodes are rounded rectangles, white fill, thin grey border.

GROUP 2 - heading "Tracker - Pendekatan Klasik", light red fill #FDF2F0, border #C0392B
- "Optical Flow"
- "Kalman Filter"
- "Particle Filter"
- "KCF"

GROUP 3 - heading "Detektor - Deep Learning", light blue fill #EEF6FD, border #2874A6
- "R-CNN, Fast R-CNN, Faster R-CNN, Mask R-CNN, SPPNet"
- "SSD"
- "YOLO v3 - v11" with second line "berbasis NMS"
- "YOLO26" with second line "NMS-free" - HIGHLIGHTED: fill #D5F5E3, border #1E8449, 2 px stroke
- "RT-DETR, D-FINE, DEIM, RF-DETR"

GROUP 4 - heading "Tracker - Deep Learning", light blue fill #EEF6FD, border #2874A6
- "SORT, DeepSORT, StrongSORT, BoT-SORT"
- "ByteTrack"
- "OC-SORT" - HIGHLIGHTED: fill #D5F5E3, border #1E8449, 2 px stroke
- "Deep-OC-SORT" - HIGHLIGHTED: fill #D5F5E3, border #1E8449, 2 px stroke
- "DiffMOT" - HIGHLIGHTED: fill #D5F5E3, border #1E8449, 2 px stroke
- "LightTrack-ReID" - HIGHLIGHTED: fill #D5F5E3, border #1E8449, 2 px stroke
- "MOTIP, Sentinel, DragonTrack"

LAYOUT
- Four groups side by side, in the order listed, read left to right.
- Inside each group the nodes stack vertically in the order listed.
- Each group is enclosed by a thin rectangle. The group heading sits inside that rectangle at the top, on one line, top-left.
- Groups 1 and 2 are the left half, groups 3 and 4 the right half.
- The five highlighted nodes are the components actually used in the paper being illustrated.

STYLE
- Plain white background outside the four group rectangles.
- Flat 1 pt outlines, 2 px corner radius on nodes. Nodes are rounded rectangles.
- No drop shadow, no glow, no gradient, no 3D, no glassmorphism.
- Neutral sans-serif, same size for every node label. Group headings one step larger and bold.
- Generous whitespace between groups.

TEXT RULES
- Reproduce every label exactly as written, letter for letter, including hyphens, commas and the mixed Indonesian and English words. Do not translate. Do not correct spelling. Do not reorder the method names inside a label.
- Render "Deep-OC-SORT", "LightTrack-ReID", "YOLO26", "RT-DETR", "D-FINE", "DEIM", "RF-DETR", "BoT-SORT", "MOTIP", "ViBE", "KCF" exactly.
- No title, no legend, no footer, no watermark.

HARD BANS
- Draw NO arrows and no connector lines between or inside groups. This is a classification chart, not a flow.
- Do not add any node, label or group that is not listed above.
- Do not fill empty space with decoration, icons, patterns or accent lines.
- Do not use rainbow colours. Only the fills named above.

CANVAS: aspect ratio 16:9, high resolution, suitable for placement at 16 cm width in a Word document.
```

### 8.3 Diagram tahapan penelitian (rasio 4:3)

```text
You are drawing one figure for a printed academic paper: a research stage flowchart, arranged as FOUR horizontal bands stacked top to bottom, each band read left to right.

BAND 1 - heading "1. Arsitektur Sistem, Persiapan Eksperimen, Koleksi Data", light red fill #FDECEA, border #C0392B
- "Mulai" - terminator capsule
- "Perancangan arsitektur," with second line "persiapan perangkat" - rectangle
- "CrowdHuman, MOT20, DanceTrack" - parallelogram (data node)
Arrows inside: Mulai -> Perancangan -> CrowdHuman

BAND 2 - heading "2. Persiapan Data", light orange fill #FEF5E7, border #D68910
- "Anotasi fbox amodal" - rectangle
- "Data Latih" - parallelogram
- "Augmentasi Data" - rectangle
- "Data Validasi" - parallelogram
Arrows inside: Anotasi -> Data Latih -> Augmentasi Data, and Anotasi -> Data Validasi

BAND 3 - heading "3. Pelatihan Model", light green fill #EAFAF1, border #1E8449
- "YOLO26s" - hexagon
- "YOLO26n" - hexagon
No arrows inside this band. Place the two hexagons side by side in the same row.

BAND 4 - heading "4. Evaluasi", light blue fill #EBF5FB, border #2874A6
- "OC-SORT, Deep-OC-SORT, DiffMOT, LightTrack-ReID" - rectangle
- "Logika Penghitungan" with second line "Lintasan" - rectangle
- "Benchmarking FPS" with second line "dan Latensi" - rectangle
- "Selesai" - terminator capsule
Arrows inside: trackers -> Logika -> Benchmarking -> Selesai

ARROWS BETWEEN BANDS (one per boundary, drawn vertically):
- from the last node of band 1 down into the first node of band 2
- from the last nodes of band 2 down into band 3
- from band 3 down into the first node of band 4

STYLE
- Every band is a thin-bordered rectangle with its heading inside, top-left.
- Terminators are capsules, processes are rectangles, data nodes are parallelograms, model nodes are hexagons.
- Plain white background, flat 1 pt outlines, no drop shadow, no glow, no gradient, no 3D.
- Neutral sans-serif, one size for every node label. Band headings one step larger.
- No colour anywhere except the four band fills and their borders named above. Node shapes stay white with a thin grey border.
- The four bands stack with even vertical spacing and all have the same width.

TEXT RULES
- Reproduce every label exactly, including the Indonesian words, the leading numbers and the commas. Do not translate. Do not correct spelling.
- Render "CrowdHuman", "MOT20", "DanceTrack", "YOLO26s", "YOLO26n", "Deep-OC-SORT", "LightTrack-ReID", "DiffMOT", "fbox amodal", "FPS" exactly.
- Keep the heading numbers "1." "2." "3." "4." at the start of each band heading.
- No title, no legend, no sub-caption, no footer, no watermark.

HARD BANS
- Do not add any node, label or arrow that is not listed above.
- Do not fill empty space with decoration, icons, patterns or accent lines.
- Do not draw a legend or a colour key.
- Do not merge the four bands into a single continuous flow.

CANVAS: aspect ratio 4:3, high resolution, suitable for placement at 16 cm width, or 11 cm if it has to shrink, in a Word document.
```

---

## Sumber (diakses 16 September 2026)

1. Google, Introducing Nano Banana Pro (Gemini 3 Pro Image). https://blog.google/innovation-and-ai/products/nano-banana-pro/
2. Google Cloud, Ultimate Prompting Guide for Nano Banana. https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana
3. SciFig, GPT Image 2 vs Nano Banana Pro: 10 Fields Tested. https://scifig.ai/blog/gpt-image-2-vs-nano-banana-pro-disciplines-tested
4. ScholarViz, Best AI Models for Scientific Figures in 2026. https://scholarviz.com/blog/2026-image-generation-model-landscape-for-scientific-figures
5. APIYI, GPT-image-2 vs Nano Banana Pro scientific diagram text rendering test. https://help.apiyi.com/en/gpt-image-2-vs-nano-banana-pro-scientific-diagram-text-rendering-en.html
6. APIYI, Two-step method for AI-generated flowcharts. https://help.apiyi.com/en/ai-text-to-flowchart-llm-image-generation-guide-en.html
7. lihuanyu.com, gpt-image-2 prompts for technical diagrams and infographics. https://www.lihuanyu.com/en/posts/2026/gpt-image-2-technical-diagram-prompts/
8. Gliffy, How to prompt AI for better diagrams. https://www.gliffy.com/blog/prompt-ai-for-better-diagrams
9. Google Flow, AI creative studio for video and images. https://labs.google/fx/tools/flow
10. Fello AI, How to tell if a photo is AI generated, 2026 guide. https://felloai.com/how-to-tell-if-a-photo-is-ai-generated/
11. Endertech, How to tell if an image is AI-generated in 2026. https://endertech.com/blog/6-ways-to-identify-ai-generated-images-with-examples
12. Elsevier, Generative AI policies for journals. https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
13. Springer Nature, AI use in manuscript preparation. https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation
14. CASRAI, Who is accountable when a figure is AI-generated. https://casrai.org/guides/ai-generated-figures-author-accountability
