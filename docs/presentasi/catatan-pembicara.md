# Catatan Pembicara — Skenario A

Dek: `docs/presentasi/index.html`. Buka di peramban, tekan **F11** untuk layar penuh, navigasi dengan **panah kiri/kanan**.

Slide sengaja tidak memuat kalimat yang akan Anda ucapkan. Yang tertulis di bawah ini adalah bahan bicara, bukan untuk dibaca dari layar.

Target durasi: **10–12 menit**, sekitar 1 menit per slide.

---

## 1 — Judul

> "Saya laporkan hasil Skenario A, yaitu evaluasi detektor. Ini lapisan pertama dari pipeline, dan yang sudah selesai dikerjakan."

Jangan berlama-lama. Langsung lanjut.

---

## 2 — Pertanyaan yang dijawab

> "Proposal kita memilih detektor tanpa NMS. Pertanyaannya: apakah pilihan itu memang menguntungkan untuk menghitung orang di kerumunan."

Kalau dosen belum familier dengan NMS, jelaskan sekali di sini:

> "NMS itu tahap pembersih setelah model mendeteksi. Model biasanya mengeluarkan banyak kotak bertumpuk untuk satu orang, lalu NMS memilih satu dan membuang sisanya. Masalahnya, di kerumunan, dua orang yang berdempetan juga menghasilkan kotak bertumpuk, dan NMS tidak bisa membedakan mana kotak ganda untuk satu orang, mana dua orang berbeda."

**Cukup jelaskan sekali.** Setelah ini pakai istilahnya langsung.

---

## 3 — Cara uji

> "Empat model dilatih dengan pengaturan yang persis sama: data sama, lama pelatihan sama, resolusi sama, seed acak sama. Jadi kalau ada selisih, itu memang karena arsitekturnya, bukan karena setelan yang berbeda."

Kalau ditanya kenapa CrowdHuman: dataset standar untuk deteksi orang di kerumunan, rata-rata 22 orang per gambar.

---

## 4 — Temuan 1: ketiganya setara

> "Ini hasil akurasinya. Tiga model kelas nano praktis sama, selisihnya cuma 0,006. Dengan satu kali latih per model, angka sekecil itu tidak bisa dibedakan dari kebetulan."

**Antisipasi pertanyaan:** *"Kenapa tidak dilatih beberapa kali?"*

> "Betul, itu batasan yang kami sadari. Untuk mengklaim selisih sekecil ini secara statistik memang perlu tiga kali latih per model, sekitar 14 jam GPU. Untuk sekarang kami memilih tidak mengklaim selisihnya sama sekali."

Jawaban ini lebih kuat daripada berkelit.

---

## 5 — Temuan 2: ukuran model yang menentukan

> "Yang benar-benar berpengaruh bukan pilihan arsitektur, tapi ukuran model. Naik satu kelas memberi delapan kali lipat dampaknya dibanding beda arsitektur."

Implikasi praktis kalau ditanya:

> "Artinya keputusan yang penting nanti bukan 'YOLO mana', tapi 'kelas nano atau small', dan itu ditentukan perangkat yang dipakai."

---

## 6 — Temuan 3: tanpa NMS memangkas tahap pembersih

> "Di sini arsitektur tanpa NMS memang menang. Waktu tahap pembersihnya hampir tiga kali lebih hemat. Dan yang lebih penting untuk kita: biayanya tetap datar walau kerumunan makin padat, jadi sistem tidak melambat justru saat ramai."

**Jangan berlebihan.** Kalau ditanya seberapa besar dampaknya:

> "Secara absolut kecil, sekitar 0,33 milidetik. Di GPU tidak terasa. Yang bernilai adalah sifatnya yang stabil, bukan besarnya."

---

## 7 — Temuan 4: CPU cukup

> "Setelah model diekspor ke format ONNX, keempatnya jalan di atas 30 FPS di CPU biasa. Artinya sistem ini tidak wajib pakai GPU mahal."

Ini menyambung ke peta jalan tahun keempat proposal, yaitu deployment edge. Sebut itu.

---

## 8 — Temuan utama: tepi bingkai

**Slide paling penting. Beri jeda di sini.**

> "Ini temuan yang tidak kami duga. Orang yang badannya terpotong tepi bingkai jauh lebih sulit dideteksi daripada orang yang tertutup sesama, dua kali lebih sulit. Padahal selama ini yang selalu dibahas di literatur adalah oklusi."

Kalau ditanya kenapa:

> "Karena anotasi CrowdHuman menggambar kotak badan penuh, termasuk bagian yang di luar layar. Model dituntut menebak posisi bagian tubuh yang sama sekali tidak terlihat. Penjelasan pastinya belum kami uji, itu langkah berikutnya."

**Jangan mengklaim ini temuan baru.** Kalau ditanya:

> "Metodenya sendiri sudah standar sejak 2012, KITTI dan PASCAL VOC sudah memakainya. Yang belum ada pembandingnya adalah angkanya pada CrowdHuman dengan anotasi badan penuh."

---

## 9 — Temuan 5: lantai under-count

> "Sekitar 7 sampai 10 persen orang tidak pernah terdeteksi, berapa pun ambang kami turunkan. Artinya dari setiap 100 orang sungguhan, 7 sampai 10 orang lewat dari deteksi. Ini penting karena jadi batas bawah seluruh sistem, tracker dan logika hitung di belakangnya tidak bisa memperbaiki orang yang memang tidak pernah terlihat."

Gunanya: menetapkan target akurasi hitungan yang realistis sejak awal.

---

## 10 — Konsekuensi: geser garis hitung

> "Dari temuan tepi bingkai tadi, ada perbaikan yang bisa langsung dipakai. Di kamera pintu masuk, garis hitung biasanya ditaruh dekat tepi layar, justru di tempat detektor paling buruk. Cukup digeser ke tengah, dan itu tidak butuh model yang lebih besar."

Ini bagian yang paling konkret. Dosen biasanya suka rekomendasi yang bisa langsung dieksekusi.

---

## 11 — Kesimpulan

> "Tiga arsitektur nano setara. Detektor tanpa NMS menang di tahap pembersih, bukan di akurasi. Untuk CPU kampus, YOLO26n paling masuk akal: 97 FPS, ruang leluasa untuk tracker dan penghitungan. Untuk GPU, YOLO26s memberi akurasi tertinggi."

Ini slide jembatan sebelum masuk ke posisi YOLO26. Pakai untuk merangkum sebelum dosen sempat memotong.

---

## 12 — Posisi YOLO26

> "YOLO26 kami uji langsung, bukan sekadar percaya klaim dokumentasi. Tanpa NMS terbukti. Klaim '43 persen lebih cepat di CPU' arahnya benar, tapi kami ukur sendiri 24 persen. Klaim objek kecil lebih baik belum terbukti, selisihnya terlalu kecil, masih di dalam derau."

Tutup dengan:

> "Jadi pilihan YOLO26 sebagai prototipe tertopang bukti untuk perangkat edge, bukan untuk GPU. Itu sesuai target deployment kita."

---

## 13 — Batasan

> "Tiga hal yang belum bisa kami simpulkan."

Sebutkan apa adanya, jangan dilunakkan. Menyebut batasan lebih dulu jauh lebih baik daripada ditemukan penguji.

---

## 14 — Langkah berikutnya

> "Kesimpulannya, detektor bukan penentu utama akurasi hitungan, ketiganya setara. Yang belum diuji sama sekali adalah lapisan pelacakan identitas, dan justru di situ sumber hitung ganda berada. Itu yang kami kerjakan berikutnya."

Kalau ada waktu, tambahkan:

> "Dan lapisan tracking itu juga yang akan menambah komponen deep learning kedua di sistem, lewat DiffMOT."

---

## Slide cadangan

Jangan dibuka kecuali ditanya.

| Slide | Dibuka kalau ditanya |
|---|---|
| C1 — hasil deteksi | "Hasilnya kelihatan seperti apa?" |
| C2 — contoh deteksi kualitatif | "Bisa lihat contoh prediksi per gambar?" |
| C3 — kurva latihan | "Berapa lama dilatih, kapan konvergen?" |
| C4 — resolusi | "Kenapa tidak turunkan resolusi saja biar cepat?" |
| C5 — kurva PR | "Precision-recall-nya bagaimana?" |
| C6 — matriks sesat | "Siapa yang terlewat, false positive-nya?" |

---

## Pertanyaan sulit yang mungkin muncul

**"Deep learning-nya di mana?"**

> "Di lapisan detektor, empat model kami latih ulang pada CrowdHuman, bukan sekadar memakai bobot bawaan. Lapisan tracking akan menambah DiffMOT yang berbasis diffusion model. Logika hitungnya sendiri sengaja dibuat deterministik, supaya kalau ada kesalahan hitung kami bisa menelusuri apakah sumbernya detektor, tracker, atau aturan hitungnya. Kalau lapisan itu ikut jadi jaringan saraf, kesalahan tidak bisa dibongkar lagi."

**"Ini kan cuma pakai model yang sudah ada?"**

> "Betul untuk tahun pertama, dan itu memang sesuai peta jalan di proposal, arsitektur baru dijadwalkan di tahun ketiga. Yang tahun ini kami hasilkan adalah pipeline-nya dan pengetahuan empiris tentang batas kemampuan detektor pada kasus kerumunan."

**"Kenapa YOLO26 kalau ternyata setara?"**

> "Di GPU memang setara, bahkan sedikit lebih lambat. Tapi di CPU dengan ONNX, YOLO26 justru yang tercepat. Dan target deployment kita adalah edge, bukan server GPU. Jadi pilihannya tetap masuk akal, hanya alasannya bukan akurasi, melainkan kecepatan di perangkat sasaran."

**"Angka mAP-nya kok rendah dibanding paper lain?"**

> "Karena dua hal. Pertama, kami pakai anotasi badan penuh, bukan badan terlihat, dua protokol yang angkanya tidak sebanding. Kedua, model kami kelas nano, 2,4 juta parameter, sedangkan baseline di paper CrowdHuman memakai ResNet-50 puluhan juta parameter. Selisih itu harga yang kami bayar untuk bisa jalan di perangkat edge."
