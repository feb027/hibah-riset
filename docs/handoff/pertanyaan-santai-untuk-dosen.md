# Pertanyaan Santai untuk Diskusi Dosen

> Konteks: dosen kemungkinan belum terlalu mengikuti detail teknis riset ini. Jadi jangan langsung tanya teknis seperti “YOLO26 gimana?” atau “DiffMOT oke tidak?”. Mulai dari menjelaskan dulu **kenapa riset ini arahnya begitu**, baru minta saran.

## Pola ngobrol yang disarankan

Gunakan pola ini:

1. Jelaskan konteks singkat.
2. Jelaskan masalah yang kami lihat.
3. Jelaskan arah solusi yang kami susun.
4. Baru minta saran dosen.

Format sederhananya:

> “Bu/Pak, kami coba baca ulang proposal dan update SOTA-nya. Dari situ kami melihat masalahnya bukan cuma mendeteksi orang, tapi menjaga agar orang yang sama tidak dihitung dua kali saat bergerak, tertutup, atau keluar-masuk zona. Karena itu kami coba arahkan risetnya ke integrasi detector, tracker, dan counting logic. Menurut Bu/Pak, framing seperti ini sudah masuk akal belum?”

---

# Script pembuka 1 menit

Kalau mau mulai diskusi, bisa pakai ini:

> “Bu/Pak, jadi kami coba dalami lagi proposal counting yang kemarin lolos. Awalnya proposal banyak menekankan YOLO26 dan DiffMOT. Setelah kami baca SOTA terbaru, kami lihat masalah people counting di ruang publik itu bukan cuma model deteksi yang cepat, tapi juga bagaimana sistem menjaga identitas orang antar-frame, terutama kalau ada oklusi, orang berdekatan, atau geraknya tidak lurus. Kalau ID-nya hilang atau tertukar, hasil hitung bisa dobel atau malah tidak kehitung.”

Lanjutkan:

> “Karena itu, kami coba posisikan risetnya sebagai pipeline: YOLO26 untuk deteksi real-time, DiffMOT untuk tracking gerak non-linear, OC-SORT sebagai fallback yang lebih ringan, lalu counting logic berbasis RoI, zona, dan ID memory supaya hitungannya lebih stabil. Tapi kami ingin minta arahan Bu/Pak, apakah framing ini sudah pas untuk arah hibah ini, atau perlu disederhanakan/digeser fokusnya?”

---

# Versi pembuka yang lebih pendek

Kalau waktunya sempit:

> “Bu/Pak, kami sudah update SOTA dan coba rapihkan gap-nya. Intinya kami melihat riset ini sebaiknya tidak hanya dibingkai sebagai ‘pakai YOLO26’, tapi sebagai integrasi detector, tracker, dan counting logic supaya hasil hitung orang lebih stabil di kondisi oklusi dan ramai. Kami ingin minta saran, apakah arah framing ini sudah tepat?”

---

# Pertanyaan utama yang paling penting

## 1. Minta validasi arah riset

- “Bu/Pak, dari penjelasan tadi, apakah arah risetnya sudah pas kalau kami bingkai sebagai integrasi detector, tracking, dan counting logic?”
- “Apakah gap seperti ini cukup kuat, atau menurut Bu/Pak masih terlalu teknis?”
- “Kalau Bu/Pak melihat proposal awal, bagian mana yang paling sebaiknya kami jadikan fokus utama?”
- “Menurut Bu/Pak, riset ini lebih baik ditekankan sebagai riset model, sistem, atau aplikasi/prototipe?”

## 2. Minta saran soal kontribusi

- “Kalau kontribusinya harus dibuat lebih jelas, sebaiknya kami tekankan di bagian mana: detector, tracking, atau logika hitung?”
- “Apakah cukup kalau kontribusinya berupa pipeline yang menggabungkan beberapa metode, atau harus ada modifikasi metode tertentu?”
- “Kalau tidak sampai membuat algoritma baru, apakah integrasi sistem + evaluasi pada skenario ruang publik masih cukup layak untuk hibah ini?”
- “Menurut Bu/Pak, novelty yang aman untuk ditulis itu apa?”

## 3. Minta saran soal YOLO26

Jelaskan dulu:

> “Untuk YOLO26, kami menemukan sumbernya masih banyak dari dokumentasi vendor dan preprint. Jadi kami tidak berani menjadikannya satu-satunya dasar akademik. Kami posisikan YOLO26 sebagai kandidat implementasi terbaru. Supaya argumen akademiknya tetap kuat, kami topang dari YOLOv10 dan RT-DETR, karena dua paper itu sudah lebih kuat secara akademik untuk menjelaskan arah detector real-time yang end-to-end dan NMS-free.”

Kalau dosen belum familiar, jelaskan dengan bahasa santai:

> “Sederhananya, NMS itu proses tambahan setelah model mendeteksi objek, untuk memilih bounding box mana yang dianggap paling benar kalau ada banyak box yang tumpang tindih. Masalahnya, proses tambahan ini bisa menambah latency dan butuh threshold. Nah, arah NMS-free itu mencoba membuat detector lebih end-to-end, jadi hasil deteksi tidak terlalu bergantung pada post-processing tambahan.”

Penjelasan YOLOv10:

> “YOLOv10 penting karena dia masih satu keluarga YOLO, tapi sudah membawa ide real-time end-to-end object detection. Jadi kalau YOLO26 ditanya dasarnya apa, kami bisa bilang arah NMS-free di keluarga YOLO sudah punya pijakan akademik dari YOLOv10, bukan cuma dari dokumentasi YOLO26.”

Penjelasan RT-DETR:

> “RT-DETR penting karena dia menunjukkan pendekatan DETR/transformer juga bisa real-time dan end-to-end tanpa NMS. Jadi RT-DETR memperkuat bahwa tren detector modern memang mengarah ke end-to-end/NMS-free, bukan hanya klaim dari YOLO26.”

Kalimat aman kalau dosen tanya “kenapa pakai YOLOv10 dan RT-DETR sebagai penopang?”:

> “Karena YOLOv10 dan RT-DETR lebih kuat untuk argumen akademiknya, Bu/Pak. YOLOv10 menunjukkan keluarga YOLO bisa diarahkan ke end-to-end/NMS-free, sedangkan RT-DETR menunjukkan detector transformer juga bisa real-time tanpa NMS. Jadi keduanya kami pakai untuk membuktikan bahwa arah NMS-free detector itu memang tren SOTA, sementara YOLO26 kami pakai sebagai kandidat implementasi terbaru.”

Lalu tanya:

- “Menurut Bu/Pak, penjelasan seperti ini sudah cukup aman untuk membedakan YOLO26 sebagai kandidat implementasi dan YOLOv10/RT-DETR sebagai dasar akademik?”
- “Apakah YOLO26 tetap perlu dipakai sebagai model utama karena sudah ada di proposal, atau boleh kami siapkan baseline pembanding seperti YOLOv10/RT-DETR?”
- “Kalau nanti ada yang mempertanyakan YOLO26 karena belum kuat secara paper, apakah strategi menjawab dengan YOLOv10 dan RT-DETR ini sudah tepat?”
- “Apakah perlu kami ubah narasinya supaya YOLO26 tidak terlihat sebagai satu-satunya novelty?”

## 4. Minta saran soal DiffMOT dan OC-SORT

Jelaskan dulu:

> “Untuk tracking, kami melihat DiffMOT cocok karena menangani gerak non-linear. Tapi karena diffusion bisa lebih berat, kami juga menaruh OC-SORT sebagai fallback yang lebih ringan.”

Lalu tanya:

- “Menurut Bu/Pak, pembagian DiffMOT sebagai tracker utama dan OC-SORT sebagai fallback ini masuk akal?”
- “Apakah perlu sejak awal kami tulis bahwa OC-SORT adalah backup kalau DiffMOT terlalu berat?”
- “Kalau scope-nya mau dijaga, cukup bandingkan DiffMOT dan OC-SORT dulu, atau perlu tracker lain juga?”
- “Dari sisi riset, apakah tracking ini perlu jadi fokus besar, atau cukup sebagai komponen sistem?”

## 5. Minta saran soal counting logic

Jelaskan dulu:

> “Kami juga melihat bahwa tracking bagus belum tentu counting-nya benar. Karena itu kami tambahkan logika RoI, zona, validasi lintasan, dan ID memory supaya orang yang sama tidak dihitung dua kali.”

Lalu tanya:

- “Apakah counting logic seperti RoI, zone-to-zone, dan ID memory ini layak dijadikan bagian kontribusi?”
- “Kalau orang mondar-mandir di area kamera, menurut Bu/Pak sebaiknya dihitung kapan?”
- “Apakah perlu dari awal kami definisikan skenario masuk-keluar, misalnya dari zona A ke zona B baru dihitung?”
- “Apakah bagian counting logic ini perlu dibuat diagram supaya lebih mudah dipahami?”

## 6. Minta saran soal dataset dan validasi

Jelaskan dulu:

> “Untuk data, kami melihat MOT20, DanceTrack, dan CrowdHuman cocok untuk deteksi/tracking, tapi belum tentu punya label counting berbasis zona. Jadi mungkin perlu validasi tambahan dari video lokal atau video publik.”

Lalu tanya:

- “Menurut Bu/Pak, untuk tahap awal cukup pakai dataset publik dulu, atau perlu video lokal juga?”
- “Kalau perlu video lokal, apakah memungkinkan pakai rekaman area kampus atau ruang publik tertentu?”
- “Untuk validasi counting, apakah ground truth-nya cukup dibuat manual di beberapa video dulu?”
- “Kalau targetnya TKT 3–4, apakah demo offline dari video sudah cukup, atau harus real-time dari kamera?”

## 7. Minta saran soal evaluasi

Jelaskan dulu:

> “Kami rencanakan evaluasinya tidak hanya akurasi deteksi, tapi juga ID tracking, error hitung, dan FPS/latency.”

Lalu tanya:

- “Menurut Bu/Pak, metrik mana yang paling penting untuk ditekankan?”
- “Apakah evaluasi perlu dipisah menjadi detector, tracker, counting, dan real-time performance?”
- “Kalau detector bagus tapi counting error masih tinggi, apakah itu justru bisa jadi analisis utama?”
- “Target real-time-nya perlu ditentukan sekarang, atau nanti setelah eksperimen awal?”

## 8. Minta saran soal sumber dan sitasi

Jelaskan dulu:

> “Kami sudah kumpulkan sumber 2024–2026 dan memisahkan mana yang peer-reviewed, mana yang vendor/preprint. Tapi beberapa sumber people counting yang relevan ada dari MDPI, jadi kami sandingkan dengan CVPR/NeurIPS/IEEE/Springer/Nature supaya lebih aman.”

Lalu tanya:

- “Apakah Bu/Pak nyaman kalau MDPI dipakai sebagai pendukung, bukan sumber utama satu-satunya?”
- “Apakah ada venue atau jurnal tertentu yang sebaiknya kami jadikan acuan?”
- “Kalau ada sumber yang kurang kuat, bagian mana yang sebaiknya kami ganti?”
- “Untuk draft tim, apakah boleh pakai source ID dulu, lalu nanti kami konversi ke IEEE setelah arahnya disetujui?”

## 9. Minta saran soal draft

- “Apakah alur pendahuluannya sudah enak: urgensi, masalah teknis, SOTA, gap, tujuan?”
- “Apakah pekerjaan terkaitnya sudah cukup tematik, atau masih terlalu teknis?”
- “Bagian mana yang menurut Bu/Pak perlu dipersingkat?”
- “Apakah istilah seperti NMS-free, ID switch, HOTA, dan DiffMOT perlu dijelaskan lebih awam?”
- “Apakah roadmap 5 tahun sudah sesuai dengan arah kelompok riset?”

## 10. Minta arahan next step

- “Setelah ini, menurut Bu/Pak kami sebaiknya lanjut ke perapian sitasi dulu atau mulai prototipe kecil?”
- “Kalau mulai prototipe, sebaiknya mulai dari detector dulu, tracking dulu, atau counting logic sederhana dulu?”
- “Untuk pembagian kerja mahasiswa, lebih baik fokus ke citation formatting, dataset, diagram metode, atau eksperimen awal?”
- “Apa keputusan utama yang sebaiknya kami bawa pulang dari diskusi ini?”

---

# Versi super singkat kalau cuma sempat tanya 5 hal

1. “Bu/Pak, framing riset sebagai integrasi detector + tracker + counting logic ini sudah pas belum?”
2. “YOLO26 sebaiknya tetap jadi model utama, atau perlu disiapkan baseline pembanding?”
3. “DiffMOT utama dan OC-SORT fallback, apakah strategi ini masuk akal?”
4. “Validasi cukup pakai dataset publik dulu, atau perlu video lokal juga?”
5. “Next step kami sebaiknya rapihin sitasi dulu atau mulai prototipe kecil?”

---

# Kalau dosen bertanya “kenapa tidak cukup YOLO saja?”

Jawaban santai:

> “Karena YOLO hanya mendeteksi orang per-frame, Bu/Pak. Untuk counting, kita perlu tahu apakah orang di frame sekarang sama dengan orang di frame sebelumnya. Kalau ID-nya hilang atau tertukar saat oklusi, orang yang sama bisa dihitung dua kali. Jadi YOLO perlu digabung dengan tracker dan counting logic.”

# Kalau dosen bertanya “kenapa YOLOv10 dan RT-DETR disebut-sebut?”

Jawaban santai:

> “Karena kami butuh dasar akademik yang lebih kuat untuk menjelaskan arah NMS-free detector. YOLO26 masih baru dan sumbernya banyak dari vendor/preprint. YOLOv10 sudah menunjukkan di keluarga YOLO bahwa deteksi bisa dibuat end-to-end tanpa NMS. RT-DETR juga menunjukkan detector berbasis transformer bisa real-time dan tanpa NMS. Jadi dua itu kami jadikan penopang akademik, sementara YOLO26 tetap kandidat implementasi terbaru.”

# Kalau dosen bertanya “apa bedanya YOLOv10, RT-DETR, dan YOLO26?”

Jawaban santai:

> “YOLOv10 itu penopang akademik dari keluarga YOLO untuk konsep end-to-end/NMS-free. RT-DETR itu penopang akademik dari jalur transformer detector yang juga real-time dan NMS-free. YOLO26 itu yang kami incar sebagai implementasi terbaru, tapi karena status sumbernya belum sekuat YOLOv10/RT-DETR, kami tidak jadikan satu-satunya dasar novelty.”

# Kalau dosen bertanya “kenapa perlu DiffMOT?”

Jawaban santai:

> “Karena gerak orang di kerumunan sering tidak lurus dan bisa saling menutupi. DiffMOT kami lihat relevan untuk prediksi lintasan non-linear. Tapi karena bisa lebih berat, kami tetap siapkan OC-SORT sebagai opsi ringan.”

# Kalau dosen bertanya “apa novelty-nya?”

Jawaban santai:

> “Novelty yang kami tarik bukan sekadar memakai YOLO26, Bu/Pak. Yang kami usulkan adalah integrasi pipeline: detector real-time, tracker untuk menjaga ID saat oklusi/gerak non-linear, fallback ringan, dan counting logic berbasis zona supaya double-counting bisa ditekan.”

# Kalau dosen bertanya “apa yang mau divalidasi?”

Jawaban santai:

> “Kami ingin validasi empat hal: deteksinya cukup baik, tracking ID-nya stabil, error hitungnya rendah, dan FPS/latency-nya masih masuk untuk real-time.”

---

# Kalimat penutup santai

- “Siap Bu/Pak, berarti setelah ini kami rapihkan framing dan fokusnya sesuai arahan.”
- “Oke Bu/Pak, nanti kami update draft, lalu lanjut ke bagian yang paling prioritas dulu.”
- “Siap, jadi kami tidak akan terlalu mengunci di YOLO26 saja, tapi tetap jaga pipeline dan evaluasinya.”
- “Baik Bu/Pak, nanti kami siapkan versi yang lebih rapi untuk sitasi dan metode setelah arah ini disetujui.”
