# Ringkasan Source Ledger S021–S026

## S021

- **Judul:** DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction
- **Penulis:** Weiyi Lv, Yuhang Huang, Ning Zhang, Ruei-Sung Lin, Mei Han, Dan Zeng
- **Jurnal/Konferensi:** IEEE/CVF CVPR 2024, peer-reviewed conference paper
- **URL:** https://openaccess.thecvf.com/content/CVPR2024/html/Lv_DiffMOT_A_Real-time_Diffusion-based_Multiple_Object_Tracker_with_Non-linear_Prediction_CVPR_2024_paper.html ; arXiv: 2403.02075
- **Permasalahan:** Banyak tracker berbasis tracking-by-detection masih mengandalkan prediksi gerak linear/Kalman filter, sehingga rentan pada gerak non-linear, akselerasi/deselerasi, oklusi, dan fragmentasi identitas.
- **Kontribusi:** Mengusulkan DiffMOT dengan D2MP (Decoupled Diffusion-based Motion Predictor) untuk prediksi gerak non-linear secara real-time dalam kerangka tracking-by-detection.
- **Metode/solusi:** Deteksi menggunakan YOLOX, prediksi gerak diganti dengan model difusi yang dikondisikan oleh riwayat bounding box dan gerak objek, lalu asosiasi dilakukan mirip ByteTrack dengan pemanfaatan deteksi skor tinggi/rendah, IoU, ReID, dan Hungarian matching.
- **Hasil utama:** Dilaporkan unggul/kompetitif pada DanceTrack dan SportsMOT untuk skenario gerak non-linear; pada DanceTrack dengan YOLOX-X penulis melaporkan HOTA 62.3, IDF1 63.0, dan 22.7 FPS, sedangkan YOLOX-S memberi trade-off lebih cepat dengan akurasi lebih rendah.
- **Batasan:** Tetap bergantung pada kualitas detektor; kecepatan real-time dilaporkan pada GPU RTX 3090 dan belum otomatis berlaku untuk edge device; tidak mencakup logika counting berbasis RoI/garis/zona.
- **Relevansi dengan penelitian ini:** Menjadi sumber inti untuk tracker utama berbasis DiffMOT pada people counting real-time, terutama untuk mengurangi ID switch akibat gerak non-linear sebelum tahap logika penghitungan.

## S022

- **Judul:** DiffusionTrack: Diffusion Model for Multi-Object Tracking
- **Penulis:** Run Luo, Zikai Song, Lintao Ma, Jinlin Wei, Wei Yang, Min Yang
- **Jurnal/Konferensi:** Proceedings of the AAAI Conference on Artificial Intelligence, AAAI 2024, 38(5), 3991–3999
- **URL:** https://ojs.aaai.org/index.php/AAAI/article/view/28192 ; DOI: 10.1609/aaai.v38i5.28192
- **Permasalahan:** Pendekatan TBD dan JDT masih menghadapi inkonsistensi global/lokal, kompromi antara robustnes dan kompleksitas model, serta kurang fleksibel untuk variasi adegan dalam video yang sama.
- **Kontribusi:** Memformulasikan deteksi dan asosiasi objek secara bersama sebagai proses difusi denoising dari paired noise boxes ke paired object/ground-truth boxes.
- **Metode/solusi:** Menggunakan backbone YOLOX untuk mengekstraksi fitur dua frame berurutan, diffusion head dengan spatial-temporal fusion dan association score head untuk memprediksi kelas, bounding box, dan skor asosiasi; inferensi dapat memakai one-step atau multi-step denoising dengan jumlah proposal/sampling yang dapat diatur.
- **Hasil utama:** Eksperimen pada MOT17, MOT20, dan DanceTrack menunjukkan kinerja kompetitif; penulis melaporkan DiffusionTrack sebagai state-of-the-art di antara metode one-stage pada MOT17/MOT20 dan HOTA 52.4 pada DanceTrack dalam protokol yang digunakan.
- **Batasan:** Desain difusi menambah biaya komputasi; peningkatan jumlah proposal atau sampling steps menaikkan akurasi tetapi menambah latensi; pelatihan dilaporkan memerlukan 8 GPU RTX 3090 sekitar 30 jam; metode ini tidak langsung menyelesaikan counting.
- **Relevansi dengan penelitian ini:** Menjadi pembanding penting bagi DiffMOT karena sama-sama memakai paradigma difusi untuk MOT, tetapi dengan fokus pada formulasi deteksi-asosiasi end-to-end, bukan prediksi gerak non-linear khusus.

## S023

- **Judul:** Hybrid-SORT: Weak Cues Matter for Online Multi-Object Tracking
- **Penulis:** Mingzhan Yang, Guangxin Han, Bin Yan, Wenhua Zhang, Jinqing Qi, Huchuan Lu, Dong Wang
- **Jurnal/Konferensi:** Proceedings of the AAAI Conference on Artificial Intelligence, AAAI 2024, 38(7), 6504–6512
- **URL:** https://ojs.aaai.org/index.php/AAAI/article/view/28471 ; DOI: 10.1609/aaai.v38i7.28471
- **Permasalahan:** Isyarat kuat seperti lokasi spasial dan appearance dapat menjadi ambigu ketika terjadi oklusi berat dan clustering, sehingga asosiasi objek sering keliru.
- **Kontribusi:** Menunjukkan bahwa weak cues—confidence state, height state, dan velocity direction—dapat melengkapi strong cues tanpa meninggalkan karakteristik Simple, Online, and Real-Time dari keluarga SORT.
- **Metode/solusi:** Memperkenalkan Tracklet Confidence Modeling (TCM), Height Modulated IoU (HMIoU), dan Robust Observation-Centric Momentum (ROCM), serta menerapkannya secara plug-and-play/training-free pada beberapa tracker seperti SORT, DeepSORT, MOTDT, ByteTrack, dan OC-SORT.
- **Hasil utama:** Pada DanceTrack, Hybrid-SORT meningkatkan performa dibanding OC-SORT dengan input asosiasi yang sama; tabel paper melaporkan HOTA 62.2 dan IDF1 63.0 untuk Hybrid-SORT, serta HOTA 65.7 dengan varian ReID. Peningkatan juga dilaporkan pada MOT17 dan MOT20 dengan tambahan komputasi kecil.
- **Batasan:** Desain cue masih heuristik dan bergantung pada kualitas deteksi; manfaat pada MOT17/MOT20 lebih terbatas karena dataset cenderung lebih linear/saturasi; penambahan ReID meningkatkan akurasi tetapi menurunkan kecepatan menuju near real-time.
- **Relevansi dengan penelitian ini:** Cocok sebagai baseline/alternatif ringan untuk pipeline YOLO + tracker, terutama ketika penelitian perlu membandingkan DiffMOT dengan metode SORT-family yang efisien pada oklusi dan crowd clustering.

## S024

- **Judul:** Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking
- **Penulis:** Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani
- **Jurnal/Konferensi:** IEEE/CVF CVPR 2023, peer-reviewed conference paper
- **URL:** https://openaccess.thecvf.com/content/CVPR2023/html/Cao_Observation-Centric_SORT_Rethinking_SORT_for_Robust_Multi-Object_Tracking_CVPR_2023_paper.html ; arXiv: 2203.14360
- **Permasalahan:** SORT/Kalman filter mengalami akumulasi error saat objek tidak teramati karena oklusi, terutama jika oklusi berbarengan dengan gerak non-linear.
- **Kontribusi:** Menggeser desain SORT dari estimation-centric menjadi observation-centric agar observasi detektor dapat memperbaiki error prediksi setelah track hilang dan muncul kembali.
- **Metode/solusi:** Menambahkan Observation-centric Re-Update (ORU), Observation-Centric Momentum (OCM), dan Observation-Centric Recovery (OCR) untuk memperbaiki parameter Kalman, menjaga konsistensi arah gerak, dan mencoba asosiasi kedua pada track/deteksi yang belum cocok.
- **Hasil utama:** Dilaporkan kuat pada MOT17, MOT20, DanceTrack, dan KITTI; paper melaporkan kecepatan tracking sangat tinggi ketika deteksi sudah tersedia (sekitar 700+ FPS/793 FPS pada CPU), sehingga cocok sebagai tracker ringan.
- **Batasan:** Kecepatan tersebut hanya untuk tahap tracking dengan deteksi off-the-shelf, bukan end-to-end detector+tracker; asosiasi IoU-only dapat lemah pada objek cepat atau frame rate rendah; tidak menyediakan modul people counting.
- **Relevansi dengan penelitian ini:** Menjadi baseline/fallback penting untuk membandingkan DiffMOT dengan tracker ringan yang mudah diintegrasikan pada sistem people counting real-time.

## S025

- **Judul:** HOTA: A Higher Order Metric for Evaluating Multi-object Tracking
- **Penulis:** Jonathon Luiten, Aljoša Ošep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixé, Bastian Leibe
- **Jurnal/Konferensi:** International Journal of Computer Vision, 129(2), 548–578; Springer IJCV
- **URL:** https://link.springer.com/article/10.1007/s11263-020-01375-2 ; DOI: 10.1007/s11263-020-01375-2
- **Permasalahan:** Evaluasi MOT sulit karena metrik lama cenderung berat sebelah: MOTA sangat dipengaruhi deteksi, sedangkan IDF1 lebih menekankan asosiasi identitas.
- **Kontribusi:** Mengusulkan HOTA sebagai metrik tunggal yang menyeimbangkan detection accuracy, association accuracy, dan localization, sambil tetap dapat diurai menjadi sub-metrik diagnostik.
- **Metode/solusi:** HOTA memakai matching deteksi pada berbagai threshold lokalisasi, menghitung DetA dan AssA, lalu menggunakan hubungan HOTA_alpha = sqrt(DetA_alpha * AssA_alpha); skor akhir dirata-ratakan pada threshold 0.05 hingga 0.95.
- **Hasil utama:** Analisis MOT17 dan studi penilaian manusia menunjukkan HOTA lebih seimbang dibanding MOTA/IDF1; paper juga menunjukkan MOTA berkorelasi kuat dengan DetA, sedangkan IDF1 berkorelasi kuat dengan AssA.
- **Batasan:** HOTA adalah metrik, bukan algoritma; membutuhkan ground-truth track/ID; tidak mengukur akurasi people counting atau line-crossing secara langsung.
- **Relevansi dengan penelitian ini:** Mendukung rencana evaluasi tracker secara multi-metrik sebelum menghitung performa counting, terutama untuk membedakan kegagalan deteksi dan kegagalan asosiasi identitas.

## S026

- **Judul:** Performance Measures and a Data Set for Multi-target, Multi-camera Tracking
- **Penulis:** Ergys Ristani, Francesco Solera, Roger Zou, Rita Cucchiara, Carlo Tomasi
- **Jurnal/Konferensi:** Computer Vision – ECCV 2016 Workshops, LNCS, 17–35; Springer
- **URL:** https://link.springer.com/chapter/10.1007/978-3-319-48881-3_2 ; DOI: 10.1007/978-3-319-48881-3_2
- **Permasalahan:** Metrik event-based seperti CLEAR MOT dan MOTA dapat kurang mencerminkan kualitas pelestarian identitas, khususnya pada pelacakan multi-kamera dengan handover dan fragmentasi.
- **Kontribusi:** Mengusulkan ukuran identitas ID precision (IDP), ID recall (IDR), dan IDF1, serta memperkenalkan dataset DukeMTMC yang besar, teranotasi, dan terkalibrasi untuk MTMC.
- **Metode/solusi:** Membuat truth-to-result matching berbasis bipartite graph/minimum-cost matching antara identitas ground-truth dan identitas hasil tracker, lalu menghitung IDTP, IDFP, IDFN untuk memperoleh IDP, IDR, dan IDF1.
- **Hasil utama:** Dataset DukeMTMC berisi lebih dari 2 juta frame, 8 kamera 1080p 60 fps, 2.834 identitas, dan durasi 85 menit per kamera; paper menunjukkan metrik identitas menangkap kualitas pelestarian identitas yang berbeda dari metrik event-based.
- **Batasan:** Dataset hanya mencakup satu adegan luar ruang dengan kamera tetap, cuaca overcast, dan sebagian besar view disjoint; metrik IDF1 tetap bukan metrik counting dan membutuhkan anotasi identitas.
- **Relevansi dengan penelitian ini:** IDF1 relevan untuk menilai stabilitas identitas tracker agar tidak terjadi double-counting atau missed-counting pada sistem people counting berbasis ID/trajectory.
