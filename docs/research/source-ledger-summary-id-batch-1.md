# Ringkasan Source Ledger — Batch 1 (S001–S013)

> Ringkasan berbahasa Indonesia untuk sumber S001–S013. Urutan bidang setiap sumber mengikuti: Judul; Penulis; Jurnal/Konferensi; URL; Permasalahan; Kontribusi; Metode/solusi; Hasil utama; Batasan; Relevansi dengan penelitian ini.

## S001

- **Judul:** YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection.
- **Penulis:** Sudip Chakrabarty.
- **Jurnal/Konferensi:** arXiv preprint/analisis sekunder, 2026; bukan peer-reviewed.
- **URL:** https://arxiv.org/abs/2601.12882 ; DOI 10.48550/arXiv.2601.12882.
- **Permasalahan:** YOLO tradisional masih bergantung pada Non-Maximum Suppression (NMS) yang menambah latensi, sensitif terhadap hiperparameter, dan dapat menimbulkan gap saat ekspor/deployment real-time.
- **Kontribusi:** Mengulas posisi YOLO26 sebagai kandidat detector end-to-end/NMS-free terbaru dan merangkum klaim teknis yang beredar tentang YOLO26.
- **Metode/solusi:** Analisis sekunder atas dokumentasi/benchmark publik Ultralytics; membahas NMS-free framework, MuSGD, Small-Target-Aware Label Assignment (STAL), ProgLoss, YOLOE-26, serta isu export/deployment.
- **Hasil utama:** Sumber ini aman dipakai untuk menyatakan bahwa YOLO26 diposisikan sebagai detector real-time NMS-free dengan orientasi edge, tetapi bukan bukti eksperimental primer untuk people counting.
- **Batasan:** Preprint dan analisis sekunder; bukan paper resmi Ultralytics dan bukan peer-reviewed. Evaluasi yang dibahas berpusat pada COCO/deteksi objek, bukan MOT, line/ROI counting, HOTA/IDF1, atau error counting.
- **Relevansi dengan penelitian ini:** Berguna sebagai konteks implementasi detector terbaru, tetapi klaim akademik utama tentang NMS-free real-time detection perlu ditopang oleh sumber peer-reviewed seperti YOLOv10 dan RT-DETR.

## S002

- **Judul:** Ultralytics YOLO26 Documentation.
- **Penulis:** Ultralytics.
- **Jurnal/Konferensi:** Dokumentasi vendor/software resmi, 2026; bukan paper akademik.
- **URL:** https://docs.ultralytics.com/models/yolo26.
- **Permasalahan:** Dokumentasi memosisikan YOLO26 untuk kebutuhan object detection real-time pada edge/low-power devices, dengan fokus pada pengurangan kompleksitas NMS, latensi, dan kompatibilitas ekspor.
- **Kontribusi:** Menyediakan sumber primer vendor tentang fitur implementasi YOLO26, variasi model, task yang didukung, format output, benchmark COCO, dan contoh penggunaan Python/CLI.
- **Metode/solusi:** YOLO26 dijelaskan sebagai model native end-to-end/NMS-free dengan one-to-one head untuk inference dan one-to-many head tradisional yang masih memakai NMS; fitur lain mencakup ProgLoss, STAL, MuSGD, DFL removal, segmentation/pose/OBB support, dan YOLOE-26.
- **Hasil utama:** Dokumentasi melaporkan metrik COCO seperti mAPval 50–95, mAPval 50–95(e2e), CPU ONNX speed, T4 TensorRT10 speed, parameter, dan FLOPs untuk YOLO26n/s/m/l/x. Contoh klaim vendor: YOLO26n 40.9 mAPval, 40.1 e2e, 38.9 ms CPU ONNX, 1.7 ms T4 TensorRT10; YOLO26x 57.5 mAPval, 56.9 e2e, 525.8 ms CPU ONNX, 11.8 ms T4 TensorRT10.
- **Batasan:** Dokumentasi vendor; Ultralytics menyatakan belum ada formal research paper untuk YOLO26. Angka COCO tidak membuktikan akurasi people counting, ID persistence, double-counting prevention, atau performa pada CCTV lokal.
- **Relevansi dengan penelitian ini:** Dipakai untuk justifikasi feasibility/prototipe YOLO26, bukan anchor SOTA akademik. Penting untuk merancang eksperimen detector yang kelak diintegrasikan dengan tracker dan counting logic.

## S003

- **Judul:** YOLOv10: Real-Time End-to-End Object Detection.
- **Penulis:** Ao Wang, Hui Chen, Lihao Liu, Kai Chen, Zijia Lin, Jungong Han, Guiguang Ding.
- **Jurnal/Konferensi:** NeurIPS 2024; arXiv full text.
- **URL:** https://arxiv.org/abs/2405.14458 ; https://neurips.cc/virtual/2024/poster/93301.
- **Permasalahan:** YOLO dengan one-to-many label assignment menghasilkan banyak prediksi positif per objek sehingga membutuhkan NMS; NMS menambah latensi, sensitif terhadap threshold, dan menghambat deployment end-to-end.
- **Kontribusi:** Memberikan anchor peer-reviewed bahwa YOLO-style detector dapat dibuat real-time dan NMS-free melalui desain training dan arsitektur yang konsisten.
- **Metode/solusi:** Consistent dual assignments: one-to-many head memberi supervisi kaya saat training, one-to-one head dipakai saat inference tanpa NMS. Arsitektur diperbaiki melalui lightweight classification head, spatial-channel decoupled downsampling, rank-guided compact blocks, large-kernel depthwise convolution, dan Partial Self-Attention.
- **Hasil utama:** Paper melaporkan peningkatan trade-off COCO AP-latency. Contoh: YOLOv10-S 46.3 AP, 7.2M parameter, 21.6 GFLOPs, 2.49 ms latency; YOLOv10-X 54.4 AP, 29.5M parameter, 160.4 GFLOPs, 10.70 ms latency pada benchmark T4 TensorRT FP16. YOLOv10-S dilaporkan 1.8× lebih cepat dari RT-DETR-R18 pada AP serupa.
- **Batasan:** Evaluasi berfokus pada COCO object detection dan T4 TensorRT FP16; tidak mengevaluasi people counting, MOT, ROI/line crossing, CCTV lokal, atau edge rendah seperti Jetson Nano. Paper juga mencatat gap AP NMS-free untuk model kecil.
- **Relevansi dengan penelitian ini:** Menjadi bukti akademik utama untuk tren detector end-to-end/NMS-free. Namun, penelitian people counting tetap memerlukan tracker dan counting logic agar tidak berhenti pada deteksi frame tunggal.

## S004

- **Judul:** DETRs Beat YOLOs on Real-time Object Detection / RT-DETR.
- **Penulis:** Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang, Yi Liu, Jie Chen.
- **Jurnal/Konferensi:** IEEE/CVF CVPR 2024.
- **URL:** https://openaccess.thecvf.com/content/CVPR2024/html/Zhao_DETRs_Beat_YOLOs_on_Real-time_Object_Detection_CVPR_2024_paper.html ; arXiv http://arxiv.org/abs/2304.08069.
- **Permasalahan:** DETR bersifat end-to-end dan tidak memerlukan NMS, tetapi DETR klasik mahal secara komputasi; sebaliknya YOLO cepat tetapi NMS dapat memengaruhi latensi dan akurasi.
- **Kontribusi:** Menunjukkan bahwa DETR-style detector dapat dibuat real-time dan kompetitif melalui desain encoder/decoder efisien dan benchmark end-to-end yang memasukkan biaya NMS pada YOLO.
- **Metode/solusi:** RT-DETR memakai backbone, efficient hybrid encoder, decoder transformer, auxiliary heads, Attention-based Intra-scale Feature Interaction pada fitur level tinggi, CNN-based Cross-scale Feature Fusion, uncertainty-minimal query selection, dan jumlah decoder layer yang dapat disesuaikan saat inference.
- **Hasil utama:** RT-DETR-R50 dilaporkan mencapai 53.1 AP dan 108 FPS; RT-DETR-R101 54.3 AP dan 74 FPS pada COCO val2017/T4 TensorRT FP16. Paper juga menunjukkan waktu NMS bergantung pada confidence/IoU threshold dan dapat memengaruhi hasil.
- **Batasan:** Small-object performance masih disebut sebagai kelemahan relatif. Sumber ini tidak menguji tracking, identity continuity, double counting, atau deployment pada perangkat low-end; hasil COCO tidak langsung berlaku untuk CCTV crowd counting.
- **Relevansi dengan penelitian ini:** Mendukung argumen bahwa pengurangan NMS dan end-to-end inference relevan untuk sistem real-time, tetapi perlu digabungkan dengan MOT dan counting rule agar sesuai dengan target people counting.

## S005

- **Judul:** D-FINE: Redefine Regression Task in DETRs as Fine-grained Distribution Refinement.
- **Penulis:** Yansong Peng, Hebei Li, Peixi Wu, Yueyi Zhang, Xiaoyan Sun, Feng Wu.
- **Jurnal/Konferensi:** ICLR 2025; arXiv 2410.13842.
- **URL:** https://openreview.net/forum?id=MFZjrTFE7h ; https://arxiv.org/abs/2410.13842.
- **Permasalahan:** DETR real-time masih dibatasi oleh regresi bounding box koordinat tetap yang kurang memodelkan ketidakpastian lokalisasi, optimisasi yang sulit, dan kebutuhan distilasi/efisiensi tanpa menambah biaya besar.
- **Kontribusi:** Mengusulkan detector real-time DETR-family yang memperbaiki presisi lokalisasi dan trade-off akurasi-latensi melalui reformulasi regresi sebagai refinement distribusi halus.
- **Metode/solusi:** Fine-grained Distribution Refinement (FDR) mengubah regresi box menjadi refinement distribusi probabilitas per sisi box secara iteratif; Global Optimal Localization Self-Distillation (GO-LSD) mentransfer pengetahuan lokalisasi dari layer lebih dalam ke layer dangkal; komponen mahal pada real-time DETR juga diringankan.
- **Hasil utama:** Pada COCO, D-FINE-L/X dilaporkan mencapai 54.0%/55.8% AP pada 124/78 FPS di NVIDIA T4. Dengan pretraining Objects365, D-FINE-L/X dilaporkan mencapai 57.1%/59.3% AP. Metode juga dilaporkan meningkatkan berbagai model DETR hingga 5.3 AP dengan tambahan parameter/biaya training kecil.
- **Batasan:** Fokus pada object detection COCO/Objects365 dan benchmark GPU; bukan people counting, bukan MOT, dan tidak mengevaluasi counting error atau ID switch. Performa edge riil perlu diuji ulang.
- **Relevansi dengan penelitian ini:** Menjadi pembanding detector real-time terbaru untuk sisi akurasi-latensi; berguna saat memilih baseline selain YOLO, tetapi perlu pipeline tracker-counter untuk menjawab masalah counting.

## S006

- **Judul:** DEIM: DETR with Improved Matching for Fast Convergence.
- **Penulis:** Shihua Huang, Zhichao Lu, Xiaodong Cun, Yongjun Yu, Xiao Zhou, Xi Shen.
- **Jurnal/Konferensi:** IEEE/CVF CVPR 2025.
- **URL:** https://cvpr.thecvf.com/virtual/2025/poster/32773 ; https://openaccess.thecvf.com/content/CVPR2025/papers/Huang_DEIM_DETR_with_Improved_Matching_for_Fast_Convergence_CVPR_2025_paper.pdf.
- **Permasalahan:** One-to-one matching pada DETR memungkinkan end-to-end/NMS-free detection, tetapi supervisi positifnya sparse dan banyak match berkualitas rendah, sehingga konvergensi lambat terutama untuk real-time detector.
- **Kontribusi:** Mengusulkan framework training yang mempercepat konvergensi real-time DETR dan meningkatkan performa tanpa mengorbankan prinsip one-to-one matching.
- **Metode/solusi:** Dense O2O meningkatkan jumlah target/positif per image melalui augmentasi seperti mosaic/mixup sambil mempertahankan one-to-one matching; Matchability-Aware Loss (MAL) mengoptimalkan match pada berbagai kualitas, termasuk low-quality matches yang kurang tertangani oleh Varifocal Loss.
- **Hasil utama:** Integrasi DEIM dengan RT-DETR dan D-FINE dilaporkan meningkatkan performa sekaligus mengurangi waktu training 50%. DEIM-RT-DETRv2-R50 mencapai 53.2% AP dalam satu hari training pada NVIDIA 4090. DEIM-D-FINE-L/X mencapai 54.7%/56.5% AP pada 124/78 FPS di NVIDIA T4 tanpa data tambahan.
- **Batasan:** Lebih merupakan framework training detector daripada pipeline people counting. Evaluasi utama COCO dan GPU; tidak menguji tracking, occlusion recovery dalam video, counting events, atau perangkat edge target.
- **Relevansi dengan penelitian ini:** Relevan untuk diskusi detector NMS-free pada dense/small-object supervision; dapat menjadi rujukan jika riset ingin melatih/menyesuaikan detector untuk kondisi kerumunan, tetapi tetap perlu evaluasi tracker dan counting.

## S007

- **Judul:** RF-DETR: Neural Architecture Search for Real-Time Detection Transformers.
- **Penulis:** Isaac Robinson, Peter Robicheaux, Matvei Popov, Deva Ramanan, Neehar Peri.
- **Jurnal/Konferensi:** ICLR 2026; arXiv 2511.09554.
- **URL:** https://openreview.net/forum?id=qHm5GePxTh ; https://arxiv.org/abs/2511.09554.
- **Permasalahan:** Specialist detector real-time sering overfit pada COCO dan sulit menggeneralisasi ke dataset nyata; sementara fine-tuned vision-language detector berat untuk real-time.
- **Kontribusi:** Mengusulkan RF-DETR sebagai detector transformer ringan dengan weight-sharing Neural Architecture Search (NAS) untuk menemukan Pareto accuracy-latency pada dataset target tanpa melatih ulang setiap konfigurasi.
- **Metode/solusi:** Memodernisasi DETR dengan backbone ViT/DINOv2, scheduler-free training, weight-sharing NAS, serta pencarian konfigurasi resolusi, patch size, jumlah decoder layer, jumlah query, dan window attention. Paper juga menstandardisasi evaluasi latensi untuk mengurangi variasi akibat power throttling GPU.
- **Hasil utama:** RF-DETR nano dilaporkan mencapai 48.0 AP di COCO dan mengungguli D-FINE nano sebesar 5.3 AP pada latensi serupa. RF-DETR 2x-large diklaim sebagai real-time detector pertama yang melampaui 60 AP di COCO; pada RF100-VL, RF-DETR 2x-large mengungguli GroundingDINO tiny 1.2 AP sambil berjalan 20× lebih cepat.
- **Batasan:** Sangat baru; detail implementasi/benchmark perlu diaudit saat versi final dipakai. Fokus pada object detection/segmentation, bukan people counting, MOT, atau counting logic. NAS dan pretraining besar mungkin tidak langsung cocok untuk perangkat edge terbatas.
- **Relevansi dengan penelitian ini:** Berguna sebagai pembanding detector 2026 pada frontier akurasi-latensi dan sebagai pengingat bahwa generalisasi ke data nyata harus dievaluasi, bukan hanya COCO.

## S008

- **Judul:** A Decade of You Only Look Once (YOLO) for Object Detection: A Review.
- **Penulis:** Leo Thomas Ramos, Angel D. Sappa.
- **Jurnal/Konferensi:** IEEE Access, 2025, vol. 13, pp. 192747–192794.
- **URL:** https://ieeexplore.ieee.org/document/11237046 ; DOI 10.1109/ACCESS.2025.3630988 ; arXiv https://arxiv.org/abs/2504.18586.
- **Permasalahan:** Evolusi YOLO selama satu dekade menghasilkan banyak varian, arsitektur, dan aplikasi sehingga perlu tinjauan sistematis untuk memahami tren, evaluasi, etika, dan arah pengembangan.
- **Kontribusi:** Menyediakan review teknis YOLO dari YOLOv1 sampai YOLOv13, termasuk tren arsitektur, skalabilitas modular, adaptasi lintas domain, praktik evaluasi, isu etika, dan arah masa depan.
- **Metode/solusi:** Tinjauan literatur dan analisis teknis terhadap keluarga YOLO serta area aplikasinya; bukan eksperimen pipeline baru.
- **Hasil utama:** Menegaskan posisi YOLO sebagai keluarga detector real-time yang berpengaruh dan terus berevolusi dari detector sederhana menjadi ekosistem arsitektur yang efisien, modular, dan adaptif. Tidak ada metrik eksperimen baru yang perlu diperlakukan sebagai hasil people-counting.
- **Batasan:** File lokal untuk S008 hanya berupa HTML IEEE yang sangat parsial; ringkasan ini dibantu metadata/abstrak arXiv. Karena merupakan review, sumber ini tidak membuktikan performa detector tertentu pada CCTV lokal, tracking, atau counting.
- **Relevansi dengan penelitian ini:** Cocok untuk latar belakang evolusi YOLO dan framing detector real-time; tidak cukup untuk klaim spesifik YOLO26, DiffMOT, atau counting accuracy.

## S009

- **Judul:** Key Considerations for Real-Time Object Recognition on Edge Computing Devices.
- **Penulis:** Nico Surantha, Nana Sutisna.
- **Jurnal/Konferensi:** Applied Sciences, 2025, 15(13), Article 7533.
- **URL:** https://www.mdpi.com/2076-3417/15/13/7533 ; DOI 10.3390/app15137533.
- **Permasalahan:** Implementasi object recognition real-time pada edge menghadapi keterbatasan komputasi, memori, baterai, panas, latensi, keamanan, privasi, interoperabilitas, dan kebutuhan metrik yang tidak hanya akurasi.
- **Kontribusi:** Mereview pertimbangan utama edge AI untuk object recognition dan memberi studi kasus inspeksi kabel listrik real-time dengan YOLO/Tiny YOLO pada Raspberry Pi dan Jetson.
- **Metode/solusi:** Membahas pemilihan device (GPU/TPU/FPGA/Raspberry Pi/Jetson), framework edge (TensorFlow Lite, TensorRT, ONNX, OpenVINO, Vitis AI), model ringan, kompresi/kuantisasi/pruning/distillation, hardware optimization, cross-layer optimization, serta metrik Edge-AI Deployment Score (EADS).
- **Hasil utama:** Studi kasus menunjukkan pemilihan model, kuantisasi, framework, dan hardware sangat memengaruhi real-time performance. Contoh: YOLOv7 pada Raspberry Pi 4B memerlukan 16.4 s inference; YOLOv7 FP16 dengan TensorRT pada Jetson Nano 0.33 s; YOLOv7-tiny FP16 pada Jetson Nano 0.06 s; YOLOv7-tiny INT8 pada Jetson Orin Nano 0.008 s dan mAP 0.936. EADS menggabungkan akurasi, inference time, resource utilization, dan power consumption.
- **Batasan:** Review luas dan studi kasusnya power-line inspection, bukan people counting. Data mentah tersedia atas permintaan. Klaim deployment perlu divalidasi pada pipeline detector+tracker+counter target.
- **Relevansi dengan penelitian ini:** Menjadi dasar untuk merancang eksperimen edge: jangan hanya mengukur mAP, tetapi juga FPS/latensi, memori, daya, framework optimisasi, dan trade-off akurasi-performa pada perangkat target.

## S010

- **Judul:** Real-Time Passenger Flow Analysis in Tram Stations Using YOLO-Based Computer Vision and Edge AI on Jetson Nano.
- **Penulis:** Sonia Diaz-Santos, Pino Caballero-Gil, Cándido Caballero-Gil.
- **Jurnal/Konferensi:** Computers, 2025, 14(11), Article 476.
- **URL:** https://www.mdpi.com/2073-431X/14/11/476 ; DOI 10.3390/computers14110476.
- **Permasalahan:** Pemantauan arus penumpang tram secara manual atau sensor APC lama kurang memadai pada kepadatan tinggi dan tidak memberi informasi pergerakan yang kaya; sistem edge harus tetap real-time pada Jetson Nano.
- **Kontribusi:** Mengimplementasikan pipeline detection-tracking-counting untuk menghitung penumpang masuk/keluar pada stasiun tram dengan YOLO dan edge AI.
- **Metode/solusi:** Membandingkan YOLOv3 hingga YOLOv11; memilih YOLOv5s sebagai trade-off terbaik; deteksi difilter pada class “person”, lalu dilacak dengan asosiasi centroid berbasis jarak Euclidean. Counting dilakukan saat centroid ID melintasi garis referensi dalam ROI: arah turun sebagai masuk, arah naik sebagai keluar.
- **Hasil utama:** YOLOv5s dilaporkan sebagai pilihan terbaik pada evaluasi penulis dengan inference time 2.1041 s, frame detection 8.1333 objek/frame, dan accuracy 0.9685 pada tabel utama. Penulis juga menyatakan optimisasi TensorRT dan operasi 640×480 dapat mencapai sekitar 12 FPS.
- **Batasan:** Domain spesifik stasiun tram; dataset tersedia atas permintaan, bukan benchmark publik. Tracker centroid sederhana rentan ID switch saat orang berdekatan; low-light, occlusion, camera placement, dan high-density scenes menurunkan performa. Tidak melaporkan HOTA/IDF1/MOTA.
- **Relevansi dengan penelitian ini:** Sangat relevan sebagai contoh people counting berbasis deteksi+tracking+ROI/line crossing di edge, sekaligus menunjukkan gap untuk tracker yang lebih robust seperti DiffMOT/OC-SORT dan evaluasi counting yang lebih ketat.

## S011

- **Judul:** Vision-Based People Counting and Tracking for Urban Environments.
- **Penulis:** Daniyar Nurseitov, Kairat Bostanbekov, Nazgul Toiganbayeva, Aidana Zhalgas, Didar Yedilkhan, Beibut Amirgaliyev.
- **Jurnal/Konferensi:** Journal of Imaging, 2026, 12(1), Article 27.
- **URL:** https://doi.org/10.3390/jimaging12010027 ; https://www.mdpi.com/2313-433X/12/1/27.
- **Permasalahan:** Counting penumpang/pejalan di lingkungan urban menghadapi occlusion, pencahayaan tidak stabil, variasi kamera, crowding, kebutuhan privasi, dan ketergantungan pada ID tracking yang stabil.
- **Kontribusi:** Mengusulkan arsitektur terpadu untuk people counting yang menggabungkan YOLOv8 detection/segmentation, modified DeepSORT, ROI/virtual-line event logic, dan event logging.
- **Metode/solusi:** YOLOv8 dilatih/diadaptasi untuk deteksi/segmentasi person; modified DeepSORT ditambah depth information dan adaptive bilinear filter; counting memakai persistent ID dan riwayat lintasan terhadap virtual lines pada ROI quadrilateral untuk menentukan event IN/OUT.
- **Hasil utama:** Dataset berisi 4047 gambar dan 8918 anotasi person; split 3293 gambar/7322 objek untuk training dan 754 gambar/1596 objek untuk testing. Hasil deteksi bbox: precision 0.91971, recall 0.86848, mAP@50 0.93335, mAP@50–95 0.74044. Counting accuracy 85% pada video 3 jam: 140 event benar dari 164.
- **Batasan:** Dataset transport/urban tersedia atas permintaan, bukan benchmark terbuka. Training menunjukkan indikasi overfitting setelah sekitar epoch 150. Evaluasi counting terbatas pada satu video/event set; tidak menyajikan benchmark MOT lengkap untuk sistem modified DeepSORT sendiri.
- **Relevansi dengan penelitian ini:** Menjadi sumber langsung untuk desain detection-tracking-counting, ROI/line crossing, dan isu double counting/ID stability pada lingkungan urban; mendukung perlunya tracker dan counting logic yang lebih kuat.

## S012

- **Judul:** YOLOv9-Based Human Face Detection and Counting Under Human-Animal Faces, Complex Imaging Environments, and Image Qualities.
- **Penulis:** Sivaranjini Perikamana Narayanan, M. Sabarimalai Manikandan, Linga Reddy Cenkeramaddi.
- **Jurnal/Konferensi:** IEEE Access, 2025, vol. 13, pp. 129600–129637.
- **URL:** https://ieeexplore.ieee.org/document/11087548 ; DOI 10.1109/ACCESS.2025.3591247.
- **Permasalahan:** Deteksi dan counting wajah manusia tetap sulit di bawah variasi warna kulit, ukuran/jumlah wajah, campuran wajah manusia-hewan, brightness/contrast/illumination/glare, blur, low-light, lens flare, noise malam, dan efek pareidolia.
- **Kontribusi:** Mengevaluasi YOLOv9 untuk face detection/counting pada kondisi citra kompleks dan membuat/menambahkan basis data citra dengan berbagai kualitas serta karakteristik yang menantang.
- **Metode/solusi:** YOLOv9 dilatih dan divalidasi pada Wider Face; kemudian diuji pada database tambahan yang mencakup infant faces, faces inside vehicles, animal faces, artificial faces, pareidolia-induced faces, noise, blur, low-light, dan variasi iluminasi. Model juga dideploy pada Raspberry Pi untuk melihat performa real-time.
- **Hasil utama:** Pada Wider Face, model dilaporkan mencapai precision 86%, recall 62.8%, mAP 70.8%, dan inference time 15.2 ms. Untuk counting, dilaporkan MAE 3.36 dan RMSE 22.38; pada infant database tak terlatih dengan noise, MAE 0.53–5.76; pada faces inside vehicles, MAE 0.43–2.87.
- **Batasan:** Sumber lokal hanya HTML IEEE yang parsial; detail tambahan berasal dari halaman/versi author-accepted yang terscrape. Ini face counting, bukan full-body people tracking; tidak menguji ID persistence, line-crossing, atau MOT. Paper mencatat false positive pada animal/pareidolia/artificial faces dan degradasi pada noise/blur.
- **Relevansi dengan penelitian ini:** Berguna untuk membahas robustness detector/counting terhadap low-light, blur, glare, noise, dan false positives, tetapi harus diposisikan sebagai pendukung robustness, bukan bukti utama people-counting berbasis tracking.

## S013

- **Judul:** Sentinel for confidence-aware multi-object tracking.
- **Penulis:** Hyun-Sung Yang, Sung-Wook Park, Chun-Bo Sim, Se-Hoon Jung.
- **Jurnal/Konferensi:** Scientific Reports, 2026, 16, Article 13571.
- **URL:** https://www.nature.com/articles/s41598-026-43938-2 ; DOI 10.1038/s41598-026-43938-2.
- **Permasalahan:** Tracking-by-detection masih menghadapi dilema confidence detector: high-confidence-only meningkatkan presisi tetapi membuang deteksi valid ber-confidence rendah; penggunaan low-confidence tanpa kontrol meningkatkan false positives dan ID switches. Track juga mudah hilang saat occlusion panjang dan terminasi berbasis age terlalu kaku.
- **Kontribusi:** Mengusulkan Sentinel, tracker uncertainty/confidence-aware yang menyesuaikan strategi asosiasi per track dan mempertahankan trajectory berisiko hilang.
- **Metode/solusi:** Confidence Aware Association (CAA) mengklasifikasikan state track menjadi Confident, Critical, dan Uncertain lalu menyesuaikan bobot biaya asosiasi IoU, appearance, arah gerak, dan confidence. Survival Boosting Mechanism (SBM) mengelola survival score berdasarkan posisi terakhir, kecepatan, dan kemungkinan occlusion agar track tidak cepat dihapus.
- **Hasil utama:** Evaluasi pada MOT17, MOT20, dan DanceTrack menunjukkan performa kuat pada HOTA, IDF1, dan AssA; paper menyatakan Sentinel mencapai performa tertinggi pada metrik selain MOTA di MOT17/MOT20 dan tetap kompetitif pada DanceTrack. Sumber tidak perlu dikutip dengan angka spesifik tanpa verifikasi tabel.
- **Batasan:** Ada overhead komputasi moderat dan potensi peningkatan false positives ketika low-confidence detections dimanfaatkan. Tetap bergantung pada kualitas detector/Re-ID dan belum langsung mengevaluasi counting error atau line-crossing accuracy.
- **Relevansi dengan penelitian ini:** Sangat relevan untuk komponen tracker karena people counting berbasis ID membutuhkan asosiasi robust, recovery dari occlusion, dan pengendalian ID switch/double count pada kerumunan.
