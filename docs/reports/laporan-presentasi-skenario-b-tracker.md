# Laporan Kemajuan Skenario B: Evaluasi Tracker dan Arah Tracker Usulan

Bahan presentasi, 11 Agustus 2026.

Skenario B adalah tahap pemilihan lapisan tracker pada sistem people counting. Ceritanya begini: deteksi saja tidak cukup untuk menghitung orang. Detektor seperti YOLO26 hanya memberi kotak di tiap frame, tapi tidak tahu apakah kotak di frame berikutnya masih orang yang sama. Kalau tidak ada tracker, orang yang tertutup objek lain lalu muncul lagi bisa dihitung dua kali. Skenario B menguji dua tracker pembanding pada deteksi yang identik, lalu memutuskan arah pengembangan selanjutnya.

---

## 1. Konteks dan Protokol

Dua tracker diuji: OC-SORT yang hanya memakai gerak (murah, tanpa GPU), dan DiffMOT yang memakai prediksi gerak berbasis diffusion plus ReID (mahal, butuh GPU). Keduanya memakai deteksi YOLO26 fine-tune yang sama persis, supaya perbandingannya mengukur kualitas tracking, bukan perbedaan detektor.

Datanya: MOT20-train (4 sekuens, 8.931 frame) untuk kerumunan sangat padat, dan DanceTrack-val (25 sekuens, 25.508 frame) untuk gerak non-linear dengan penampilan seragam. Metrik dihitung dengan TrackEval: HOTA, MOTA, IDF1, dan jumlah ID switch (IDSW). Satu catatan penting: karena deteksi yang dipakai bukan deteksi resmi MOTChallenge, angka hasil kita tidak bisa dibandingkan 1:1 dengan leaderboard. Perbandingan yang sah adalah antar tracker pada deteksi yang sama.

## 2. Hasil DiffMOT

| Benchmark | Tracker | HOTA | MOTA | IDF1 | IDSW | Frag |
|---|---|---|---|---|---|---|
| MOT20 (train) | OC-SORT | 36,51 | 55,98 | 42,88 | 14.293 | 27.646 |
| MOT20 (train) | DiffMOT | 44,37 | 60,91 | 53,86 | 6.905 | 15.005 |
| DanceTrack (val) | OC-SORT | 28,39 | 71,38 | 26,63 | 6.701 | 6.936 |
| DanceTrack (val) | DiffMOT | 39,05 | 70,72 | 43,39 | 2.784 | 6.765 |

Selisih antar keduanya bisa dilihat lebih jelas begini:

| Metrik | OC-SORT | DiffMOT | Perubahan |
|---|---|---|---|
| MOT20 HOTA | 36,51 | 44,37 | +7,86 |
| MOT20 IDF1 | 42,88 | 53,86 | +10,98 |
| MOT20 IDSW | 14.293 | 6.905 | −7.388 (turun 52%) |
| DanceTrack HOTA | 28,39 | 39,05 | +10,66 |
| DanceTrack IDF1 | 26,63 | 43,39 | +16,76 |
| DanceTrack IDSW | 6.701 | 2.784 | −3.917 (turun 58%) |

Dua temuan penting dari angka ini.

Pertama, masalah yang dihadapi sistem kita memang di asosiasi identitas, bukan deteksi. OC-SORT di MOT20 tetap mencapai MOTA 55,98 (deteksi kuat) tapi mencatat 14.293 ID switch, rata-rata 1,6 kali per frame. Kepadatan di benchmark ini tinggi, sekitar 179 deteksi per frame dari GT 127, dengan puncak 272 di satu sekuens. Saat orang saling menutupi, pencocokan berbasis IoU mudah salah sambung, identitas putus, dan orang muncul kembali dihitung sebagai orang baru. IDF1 42,88 artinya sekitar 57 persen bobot asosiasi tidak cocok dengan ground truth.

Kedua, DiffMOT memang memperbaiki asosiasi secara nyata. ID switch turun lebih dari setengah di kedua benchmark, IDF1 naik 11 sampai 17 poin, HOTA naik 8 sampai 11 poin. Ini bukti eksperimental bahwa penambahan informasi penampilan (ReID) dan prediksi gerak yang lebih baik memperbaiki hal yang selama ini lemah.

## 3. Kenapa Pivot dari DiffMOT

Akurasi bukan satu-satunya kriteria, dan DiffMOT punya tiga masalah untuk sistem people counting real-time di kampus.

Pertama, kecepatannya tidak cukup. Pada video demo klip MOT20-02, pipeline DiffMOT tercatat sekitar 20 FPS di RTX 4090, dan pengukuran tracking-only di benchmark juga berada di kisaran 20 sampai 25 FPS. Target kita minimal 30 FPS (anggaran 33 sampai 40 ms per frame) di perangkat yang lebih murah dari RTX 4090. Publikasi DiffMOT sendiri menyebut 22,7 FPS di RTX 3090 sudah termasuk detektor, jadi dari sisi throughput tracker ini tidak menyisakan ruang untuk detektor.

Kedua, DiffMOT black box. Bobotnya sudah dilatih pengembang, tidak bisa dilatih ulang untuk data kampus yang beda iluminasi dan sudut kamera. Padahal kemampuan fine-tune ke scene sendiri justru salah satu kontribusi riset yang kita incar.

Ketiga, rantai dependensinya rapuh. DiffMOT butuh environment torch khusus, patch lokal untuk memperbaiki beberapa bug runtime, dan format data yang harus disetel persis. Sebagai artefak deployment, ini sulit didistribusikan dan dirawat.

Ringkasnya:

| Dimensi | OC-SORT | DiffMOT | Tracker usulan |
|---|---|---|---|
| Biaya asosiasi | hampir nol, 54+ FPS di CPU | berat, butuh GPU, 20 sampai 25 FPS di RTX 4090 | sekitar 0,6 GFLOPs, target jauh di atas 30 FPS |
| Bisa dilatih ulang | tidak perlu | tidak bisa | bisa, dari data sendiri |
| Dependensi | pip minimal | patch lokal plus env khusus | torch dan modul ringan lain |
| Posisi | cepat tapi asosiasi rapuh | akurat tapi tidak layak deploy | akurat, ringan, bisa dilatih |

Kesimpulan dari tahap ini: arah riset butuh ReID plus memori, tapi arsitekturnya harus ringan dan trainable. DiffMOT tetap dipertahankan sebagai pembanding kualitas kedua pada tabel hasil.

## 4. Paper LightTrack-ReID dan Pola Ablasinya

Pencarian tracker 2025 sampai 2026 menemukan paper yang paling cocok dengan kebutuhan: LightTrack-ReID dari Khan dkk. (2026, S014), terbit di PLOS ONE 21(3), DOI 10.1371/journal.pone.0342246. Paper ini peer-reviewed, melaporkan MOT17 dan MOT20, dan menekankan efisiensi.

Angka di paper (konteks saja, bukan target reproduksi, karena protokol evaluasi mereka berbeda):

| Metrik | Nilai paper |
|---|---|
| MOT17 test | HOTA 66,92, MOTA 82,81, IDF1 82,52 |
| MOT20 test | HOTA 66,6, MOTA 79,1, IDF1 82,2 |
| Kecepatan | sekitar 30 FPS di GTX 1080 |
| Biaya asosiasi | sekitar 0,6 GFLOPs per frame |
| Training | MOT17 plus MOT20, 20 epoch, sekitar 10 jam di GTX 1080 |

Di paper, pengaruh tiap komponen diuji dengan cara ditambahkan satu per satu ke baseline. Baseline-nya detektor YOLOX plus asosiasi sederhana (Kalman, IoU, Hungarian, EMA). Hasilnya (angka MOT17 val):

| Konfigurasi | HOTA MOT17 val | HOTA MOT20 val |
|---|---|---|
| Baseline | 66,13 | 56,17 |
| +LAE | 70,88 | 60,38 |
| +LAE+TBSS | 73,38 | 63,94 |
| +LAE+TBSS+CMOH | 74,88 | 65,74 |
| +LAE+TBSS+CMOH+ASW | 75,63 | 66,70 |

Supaya pembacaannya jelas, berikut maksud tiap komponen dengan bahasa sederhana.

Kalman filter. Prediktor posisi. Dari posisi dan arah gerak di frame sebelumnya, tracker memperkirakan di mana orang itu di frame berikutnya. Asumsinya gerak lurus beraturan, karena itu penari yang berbelok mendadak bisa meleset dari perkiraan.

IoU (Intersection over Union). Ukuran seberapa besar dua kotak saling menutupi. Dua kotak yang tumpang tindih banyak kemungkinan besar orang yang sama. Ini cara paling sederhana mencocokkan deteksi antar frame.

EMA (Exponential Moving Average). Penghalusan koordinat kotak supaya hasil tidak goyang antar frame. Rata-rata bergerak yang memberi bobot lebih ke frame terbaru. Ini merapikan output, bukan pengambil keputusan asosiasi.

LAE. Model kecil berbasis MobileNetV3-Small yang mengubah potongan gambar orang menjadi vektor 32 angka, semacam sidik jari penampilan. Dua potongan orang yang sama akan menghasilkan vektor yang mirip, dua orang berbeda vektornya beda, diukur dengan cosine similarity. Inilah komponen yang pada ablasi paper memberi kenaikan paling besar, artinya penampilan adalah sinyal paling informatif untuk membedakan orang.

TBSS. Penilai kemiripan. Model kecil yang menerima gabungan informasi posisi dan penampilan lalu mengeluarkan skor 0 sampai 1 untuk sepasang deteksi. Dengan IoU saja, orang yang berdiri berdekatan mudah tertukar; TBSS menambahkan informasi penampilan ke keputusan.

CMOH. Memori konteks. Tracker menyimpan 10 embedding terakhir untuk tiap tracklet. Saat orang tertutup dua atau tiga frame lalu muncul lagi, pencocokan memakai rata-rata embedding lama, bukan hanya yang terakhir. Pada ablasi paper, komponen inilah yang paling memangkas ID switch (di MOT17 dari 138 menjadi 80).

ASW. Bobot oklusi adaptif. Satu angka per frame yang menghitung seberapa ramai frame itu. Kalau sedang banyak orang saling menutupi, keputusan lebih mengandalkan penampilan; kalau sepi, lebih mengandalkan posisi.

Kenapa paper ini dipilih. Pertama, paradigma real-time dan deep learning memang di jalur target: biaya asosiasi hanya 0,6 GFLOPs, kecepatan didominasi detektor, bukan tracker. Kedua, ringan dan bisa dilatih ulang di data sendiri, beda dari DiffMOT. Ketiga, pola ablasi selaras dengan kelemahan yang kita ukur: CMOH memangkas ID switch, dan ini justru kelemahan utama baseline kita. Keempat, paper tidak merilis kode, sehingga reimplementasi menjadi kontribusi mandiri, bukan sekadar replikasi.

## 5. Tracker Usulan Menurut Paper

Tracker versi kita disusun mengikuti resep paper, dengan penyesuaian untuk ekosistem proyek (YOLO26, Python 3.8 di kampus).

Komponennya: LAE sebagai encoder penampilan, TBSS sebagai penilai kemiripan, asosiasi inti Kalman plus Hungarian plus filter confidence plus EMA, lalu CMOH dan ASW untuk bertahan saat oklusi. Skor akhir untuk sepasang deteksi-tracklet adalah kombinasi skor TBSS dan IoU: C = 1 dikurangi (w kali s) ditambah ((1 dikurangi w) kali IoU), dengan w bobot oklusi dari ASW.

Resep training mengikuti paper: data MOT17-train plus MOT20-train, loss gabungan triplet dan BCE, Adam dengan learning rate 0,001, 20 epoch, crop 224x224, augmentasi flip, crop padding, dan color jitter, maksimal 50 pasangan per frame. Estimasi waktu 2,5 sampai 5 jam per 20 epoch di RTX 4090.

Protokol evaluasi kita anti-overclaim: leave-one-out pada MOT20-train empat fold, DanceTrack-val sebagai pengujian zero-shot, deteksi YOLO26 identik dengan OC-SORT dan DiffMOT, dan hasil dilaporkan relatif terhadap OC-SORT (36,51 HOTA) dan DiffMOT (44,37 HOTA) di MOT20. Tidak membandingkan angka dengan tabel paper karena protokolnya beda.

## 6. Hasil Training Fase 3 (v1) dan Perbaikan v2

Training pertama kali diuji dengan mini-run: satu sekuens, 60 frame, satu epoch. Hasilnya bagus secara visual, skor kemiripan benar 0,908 dan margin cosine melebar, tapi ini sampel validasi 10 frame yang kecil, bukan bukti final.

Full run fold-1 (20 epoch, MOT17 plus MOT20) hasilnya campuran. Loss total turun mulus dari 0,139 ke 0,054, loss triplet dari 0,070 ke 0,021, dan cosine antar potongan orang yang sama stabil di 0,93 sampai 0,98. Artinya LAE berhasil belajar memisahkan penampilan. Namun skor kemiripan TBSS di validasi tidak menunjukkan pembelajaran sama sekali: BCEacc datar di 0,494 sampai 0,505 sepanjang 20 epoch, tidak jauh dari lempar koin.

Kenapa bisa gagal. Ada satu kejanggalan yang menarik. Kalau benar semua skor TBSS di sekitar 0,5, loss BCE-nya harusnya sekitar 0,69. Kenyataannya loss BCE total hanya sekitar 0,03. Artinya di data latih TBSS justru yakin benar, kemungkinan memakai jalan pintas geometri antar kotak, tapi kalah telak di data validasi. Dengan kata lain rangkaian training dan validasi berjalan benar secara kode, tapi ada ketidakcocokan antara perilaku TBSS di data latih dan validasi. Ini yang sedang dibedah lewat histogram distribusi skor pasangan sama-id dan beda-id; butuh GPU, dan tinggal dijalankan begitu GPU kampus aktif.

Perbaikan yang sudah dikerjakan (v2). TBSS diganti dari transformer berdimensi 73 yang attention-nya tidak efektif menjadi MLP ringan dengan input 6 angka (IoU, cosine, selisih box yang dinormalisasi), optimizer untuk TBSS dipisah dari LAE, loss BCE diberi bobot per kelas, dan checkpoint disimpan ala YOLO (last.pt dan best.pt). Status terakhir: GPU kampus sedang tidak bisa dipakai, training v2 belum tuntas.

Satu hal yang harus ditegaskan jujur di presentasi: angka evaluasi dari tracker usulan (HOTA, IDF1) belum ada. Yang sudah terbukti baru sampai encoder penampilan berfungsi baik; komponen penilai kemiripan masih dalam perbaikan.

## 7. Kesimpulan dan Langkah Berikutnya

Tiga kesimpulan dari kemajuan ini. Asosiasi, bukan deteksi, yang membatasi kualitas counting, terlihat dari 14.293 ID switch OC-SORT di MOT20. DiffMOT membuktikan ReID plus memori memang diperlukan, ID switch turun 52 sampai 58 persen, tapi kecepatannya sekitar 20 sampai 25 FPS di RTX 4090, black box, dan fragile, sehingga tidak layak menjadi tracker utama. Maka arahnya ke tracker ringan terinspirasi LightTrack-ReID yang sedang dibangun dan dilatih.

Langkah berikutnya: jalankan histogram skor TBSS begitu GPU kampus aktif untuk memastikan akar masalahnya, lanjutkan training v2 sampai tuntas, lalu evaluasi dengan TrackEval pada protokol yang sama dan masukkan ke tabel pembanding.

---

## Lampiran. Materi Pendukung

| Materi | Lokasi |
|---|---|
| Tabel hasil lengkap | experiments/s2_tracker/eval_results.csv |
| Video demo klip padat, OC-SORT vs DiffMOT vs GT | experiments/s2_tracker/demo/MOT20-02_f1-450_tracked.mp4, ..._tracked_diffmot.mp4, ..._gt.mp4 |
| Laporan detail Skenario B | docs/reports/laporan-skenario-b-tracker.md |
| Catatan implementasi paper S014 | docs/research/fulltext-notes/S014-lighttrack-reid.md |
| Rencana fase 11, tracker usulan | docs/plans/2026-08-05-phase11-skenario-b-tracker-lighttrack.md |

## Daftar Pustaka

1. Lv, W., Huang, Y., Zhang, N., Lin, R.-S., Han, M., & Zeng, D. (2024, S021). DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction. CVPR 2024, 19321-19330. arXiv:2403.02075.
2. Khan, S. B. J., Zhang, P., Kamal, M. M., Saudagar, A. K. J., dkk. (2026, S014). LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking. PLOS ONE 21(3), e0342246. DOI 10.1371/journal.pone.0342246.
3. Cao, J., Pang, J., Weng, X., Khirodkar, R., & Kitani, K. (2023). Observation-Centric SORT (OC-SORT). CVPR 2023. arXiv:2203.14360.
4. Luiten, J., Ošep, A., Dendorfer, P., dkk. (2021, S025). HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking. IJCV 129(2), 548-578.
5. Dendorfer, P., dkk. (2020, S036). MOT20: A benchmark for multi object tracking in crowded scenes. ECCV 2020 Workshops. arXiv:2003.09003.
6. Sun, P., dkk. (2022, S037). DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion. CVPR 2022. arXiv:2111.14690.
