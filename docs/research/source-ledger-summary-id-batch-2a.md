# Ringkasan Source Ledger S014–S020

## S014

- **Judul:** LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking.
- **Penulis:** Said Baz Jahfar Khan; Peng Zhang; Mian Muhammad Kamal; Abdul Khader Jilani Saudagar.
- **Jurnal/Konferensi:** PLOS One, 21(3), e0342246, 2026.
- **URL:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0342246 ; DOI: 10.1371/journal.pone.0342246
- **Permasalahan:** Pelacakan multi-objek real-time masih rentan terhadap oklusi, fragmentasi lintasan, dan identity switch, terutama ketika komputasi terbatas.
- **Kontribusi:** Mengusulkan LightTrack-ReID sebagai kerangka MOT ringan dan tahan oklusi yang menggabungkan ReID ringkas, penilaian kemiripan berbasis transformer, memori konteks, dan pembobotan kemiripan adaptif.
- **Metode/solusi:** Menggunakan YOLOX-S untuk deteksi, Lightweight Appearance Encoder berbasis MobileNetV3-Small untuk fitur ReID 32 dimensi, Transformer-Based Similarity Scoring, Context Memory for Occlusion Handling, Adaptive Similarity Weighting, Kalman/Hungarian matching, serta pelatihan dengan triplet loss dan binary cross-entropy.
- **Hasil utama:** Penulis melaporkan kinerja kuat pada MOT17 dan MOT20, termasuk HOTA 66.92/66.6 dan IDF1 82.52/82.2; modul asosiasi sekitar 0.6 GFLOPs dan sistem penuh sekitar 30 FPS pada GTX1080 dalam konfigurasi yang dilaporkan.
- **Batasan:** ASW memakai bobot oklusi global sehingga dapat melewatkan variasi lokal; CMOH dibatasi buffer K=10 dan kurang kuat untuk oklusi panjang/berulang; encoder yang dilatih pada MOT17/MOT20 berisiko kurang general pada domain baru dengan pencahayaan atau gerak kamera berbeda.
- **Relevansi dengan penelitian ini:** Mendukung rancangan tracker ringan untuk people counting real-time, khususnya kebutuhan menjaga ID saat oklusi agar logika hitung berbasis lintasan tidak mudah ganda atau hilang.

## S015

- **Judul:** Focusing on Tracks for Online Multi-Object Tracking.
- **Penulis:** Kyujin Shim; Kangwook Ko; Yujin Yang; Changick Kim.
- **Jurnal/Konferensi:** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2025.
- **URL:** https://openaccess.thecvf.com/content/CVPR2025/html/Shim_Focusing_on_Tracks_for_Online_Multi-Object_Tracking_CVPR_2025_paper.html
- **Permasalahan:** Banyak tracker online masih mengandalkan optimasi global dan asosiasi multi-tahap yang kurang optimal untuk memanfaatkan deteksi low-confidence atau deteksi yang terhapus NMS, terutama saat oklusi.
- **Kontribusi:** Memperkenalkan TrackTrack, tracker online yang berfokus pada perspektif track melalui Track-Perspective-Based Association (TPA) dan Track-Aware Initialization (TAI).
- **Metode/solusi:** TPA melakukan asosiasi bersama satu tahap terhadap deteksi high-confidence, low-confidence, dan high-confidence yang terhapus NMS, lalu memilih pasangan minimum dari perspektif track; TAI menekan inisialisasi track palsu dengan mempertimbangkan overlap terhadap track aktif dan deteksi yang lebih meyakinkan.
- **Hasil utama:** Pada eksperimen MOT17, MOT20, dan DanceTrack, TrackTrack dilaporkan konsisten mengungguli tracker pembanding pada metrik utama; penulis juga menunjukkan peningkatan HOTA/AssA dalam ablation dan laju asosiasi yang tetap tinggi.
- **Batasan:** Evaluasi tidak secara khusus ditujukan untuk sistem people counting; pipeline tetap bergantung pada kualitas detektor dan fitur ReID; eksperimen komputasi menggunakan GPU desktop, bukan perangkat edge rendah daya.
- **Relevansi dengan penelitian ini:** Relevan untuk merancang asosiasi track yang lebih stabil di antrean/kerumunan, termasuk pemanfaatan deteksi lemah agar orang yang tertutup sebagian tidak langsung hilang dari hitungan.

## S016

- **Judul:** Multiple Object Tracking as ID Prediction.
- **Penulis:** Ruopeng Gao; Ji Qi; Limin Wang.
- **Jurnal/Konferensi:** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2025.
- **URL:** https://openaccess.thecvf.com/content/CVPR2025/html/Gao_Multiple_Object_Tracking_as_ID_Prediction_CVPR_2025_paper.html
- **Permasalahan:** Asosiasi MOT berbasis aturan heuristik, ReID, atau matching manual sering memerlukan banyak penyesuaian dan kurang adaptif pada skenario dengan gerak tidak teratur, penampilan mirip, dan oklusi.
- **Kontribusi:** Memformulasikan MOT sebagai tugas in-context ID Prediction dan mengusulkan MOTIP sebagai baseline end-to-end yang sederhana untuk memprediksi label ID deteksi saat ini berdasarkan lintasan historis.
- **Metode/solusi:** Menggunakan Deformable DETR untuk deteksi dan fitur objek, kamus ID learnable sebagai prompt identitas, ID Decoder berbasis transformer, loss gabungan deteksi dan ID, serta augmentasi lintasan berupa random occlusion dan random ID-token switch.
- **Hasil utama:** Penulis melaporkan hasil state-of-the-art pada DanceTrack, SportsMOT, dan BFT; pada DanceTrack tanpa data ekstra, MOTIP dilaporkan mencapai HOTA 69.6 dan IDF1 74.7, serta meningkat dengan data ekstra.
- **Batasan:** Penulis menyatakan desain masih sederhana dan belum mengeksplorasi decoder khusus, cue tambahan seperti motion/depth, atau pemodelan lintasan yang lebih kompleks; kapasitas kamus ID K dapat tidak cukup pada skenario sangat padat.
- **Relevansi dengan penelitian ini:** Memberi perspektif alternatif bahwa stabilitas ID untuk counting dapat dipelajari langsung, bukan hanya diatur lewat heuristik; namun perlu disesuaikan untuk kebutuhan real-time/edge dan area padat.

## S017

- **Judul:** DragonTrack: Transformer-Enhanced Graphical Multi-Person Tracking in Complex Scenarios.
- **Penulis:** Bishoy Galoaa; Somaieh Amraee; Sarah Ostadabbas.
- **Jurnal/Konferensi:** Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2025.
- **URL:** https://openaccess.thecvf.com/content/WACV2025/html/Galoaa_DragonTrack_Transformer-Enhanced_Graphical_Multi-Person_Tracking_in_Complex_Scenarios_WACV_2025_paper.html
- **Permasalahan:** Multi-person tracking sulit mempertahankan identitas saat oklusi, subjek berpenampilan mirip, interaksi kompleks, serta re-entry/exit dalam video.
- **Kontribusi:** Mengusulkan DragonTrack, kerangka end-to-end yang menggabungkan DETR, graph convolutional network, attention, dan learnable Sinkhorn untuk asosiasi multi-person.
- **Metode/solusi:** DETR mengekstraksi bounding box dan fitur; embedding geometris, posisi, dan penampilan diproses melalui MLP dan graph convolutional attention network; matching memakai cosine similarity, learnable Sinkhorn normalization, Hungarian assignment, serta loss gabungan weighted BCE dan contrastive loss.
- **Hasil utama:** Penulis melaporkan kinerja unggul pada MOT17, MOT20, dan DanceTrack; misalnya HOTA 65.3/MOTA 82.0 pada MOT17, HOTA 63.2/IDF1 78.6 pada MOT20, dan HOTA 72.5/MOTA 93.4/IDF1 74.9 pada DanceTrack.
- **Batasan:** Arsitektur berbasis DETR dan GCN relatif berat; penulis menyatakan efisiensi komputasi, validasi pada dataset lebih beragam, dan pelacakan subjek jauh masih menjadi arah perbaikan.
- **Relevansi dengan penelitian ini:** Menjadi bukti bahwa kombinasi fitur spasial, penampilan, dan relasi antar-orang membantu menjaga ID dalam skenario padat; relevan sebagai pembanding tracker kuat, tetapi perlu disederhanakan bila targetnya edge real-time.

## S018

- **Judul:** OcclusionTrack: Multi-Object Tracking in Dense Scenes.
- **Penulis:** Yuzhi Chen; Fanqin Meng; Ziqiu Chen.
- **Jurnal/Konferensi:** Applied Sciences, 15(24), 13030, 2025.
- **URL:** https://www.mdpi.com/2076-3417/15/24/13030 ; DOI: 10.3390/app152413030
- **Permasalahan:** Pada dense-scene MOT, oklusi menurunkan kualitas deteksi, membuat IoU matching ambigu, menyebabkan pergeseran koordinat karena gerak kamera, dan menimbulkan akumulasi error saat track hilang.
- **Kontribusi:** Mengusulkan OcclusionTrack/OCCTrack sebagai pipeline tracking-by-detection yang menambahkan empat modul untuk oklusi dan gerak kamera tanpa ReID terpisah.
- **Metode/solusi:** Mengintegrasikan Confidence-Based Kalman Filter, Camera Motion Compensation, Depth–Cascade-Matching berbasis pseudo-depth, dan CMC-detection-based Re-activate ke baseline ByteTrack/YOLOX; asosiasi tetap memakai IoU dan Hungarian matching pada deteksi high/low score.
- **Hasil utama:** Penulis melaporkan kinerja kompetitif pada MOT17, MOT20, dan DanceTrack; dibanding baseline ByteTrack-style, mereka melaporkan peningkatan HOTA/IDF1 dan penurunan ID switch, termasuk hampir separuh ID switch pada MOT17 dan sekitar 25% pada MOT20.
- **Batasan:** Sangat bergantung pada kualitas dan kalibrasi confidence detektor; CMC memakai asumsi gerak kamera global 2D; model gerak masih constant-velocity linear; terutama diuji pada pedestrian dan belum menjadi evaluasi people-counting.
- **Relevansi dengan penelitian ini:** Sangat relevan untuk gap oklusi pada people counting berbasis deteksi-tracking, karena menunjukkan modul praktis untuk mengurangi ID loss/switch sebelum logika counting diterapkan.

## S019

- **Judul:** Handling Heavy Occlusion in Dense Crowd Tracking by Focusing on the Heads.
- **Penulis:** Yu Zhang; Huaming Chen; Zhongzheng Lai; Zao Zhang; Dong Yuan.
- **Jurnal/Konferensi:** AI 2023: Advances in Artificial Intelligence, Springer LNCS / ACM DL page.
- **URL:** https://doi.org/10.1007/978-981-99-8388-9_7
- **Permasalahan:** Pelacakan semua pejalan kaki pada kerumunan padat sulit dilakukan karena tubuh sering tertutup berat, sehingga deteksi full-body dan asosiasi track menjadi tidak andal.
- **Kontribusi:** Mengusulkan pendekatan yang berfokus pada kepala melalui detektor joint head-and-body anchor-free dan pembelajaran relasi kepala-tubuh secara dinamis.
- **Metode/solusi:** Memanfaatkan cue kepala yang lebih sering terlihat saat oklusi berat, menggabungkan informasi kepala dan tubuh, serta tidak bergantung pada rasio statistik kepala-tubuh yang tetap.
- **Hasil utama:** Berdasarkan abstrak/ekstraksi lokal, eksperimen dilaporkan pada MOT20, CrowdHuman, dan HT21 dengan peningkatan recall dan precision untuk pejalan kaki kecil/menengah serta klaim performa kuat pada dataset dense-crowd.
- **Batasan:** Full text tidak tersedia dalam ekstraksi lokal; detail runtime, arsitektur lengkap, dan metrik numerik spesifik tidak dapat diverifikasi dari berkas yang tersedia.
- **Relevansi dengan penelitian ini:** Mendukung argumen bahwa sistem people counting di kerumunan tidak cukup mengandalkan full-body detection; cue kepala/parsial dapat menjadi strategi saat tubuh banyak tertutup.

## S020

- **Judul:** BoostTrack: boosting the similarity measure and detection confidence for improved multiple object tracking.
- **Penulis:** Vukasin D. Stanojevic; Branimir T. Todorovic.
- **Jurnal/Konferensi:** Machine Vision and Applications, 35(3), 2024.
- **URL:** https://link.springer.com/article/10.1007/s00138-024-01531-5 ; DOI: 10.1007/s00138-024-01531-5
- **Permasalahan:** MOT perlu memanfaatkan deteksi low-confidence yang benar tanpa meningkatkan false positive dan harus menghindari identity switch akibat IoU ambigu, terutama pada oklusi dan adegan padat.
- **Kontribusi:** Mengusulkan BoostTrack, tracker tracking-by-detection dengan tambahan plug-and-play ringan untuk boosting confidence deteksi dan boosting similarity matrix dalam asosiasi satu tahap.
- **Metode/solusi:** Mendefinisikan detection-tracklet confidence untuk menskalakan kemiripan, menambahkan boost berbasis IoU, Mahalanobis distance yang dinormalisasi, dan shape similarity; menaikkan confidence deteksi low-score yang kemungkinan objek terlacak atau objek baru/outlier; dapat dikombinasikan dengan CMC, interpolasi, dan appearance similarity sebagai BoostTrack+.
- **Hasil utama:** Penulis melaporkan BoostTrack appearance-free tetap real-time dan kompetitif pada MOT17/MOT20; BoostTrack+ dengan appearance similarity dilaporkan mengungguli solusi benchmark standar dan menjadi online method teratas pada HOTA untuk MOT17/MOT20 dalam protokol private detection.
- **Batasan:** Boosting low-confidence detections dapat memperkenalkan false positive/ID baru; versi BoostTrack+ jauh lebih lambat, terutama pada MOT20; metode tetap bergantung pada detektor, threshold, dan komponen tambahan seperti CMC/interpolasi.
- **Relevansi dengan penelitian ini:** Relevan sebagai baseline/aspek desain untuk tracker people counting karena menunjukkan cara memanfaatkan deteksi lemah secara hati-hati agar orang yang teroklusi tidak terhapus dari lintasan hitung.
