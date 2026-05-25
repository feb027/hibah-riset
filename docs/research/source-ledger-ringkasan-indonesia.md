# Source Ledger Ringkasan Bahasa Indonesia

> Ringkasan ini dibuat dari `docs/research/source-ledger.md`, `references/references.bib`, dokumen yang diunduh ke `docs/research/papers/`, dan hasil ekstraksi teks di `docs/research/paper-text/`.
>
> Format setiap sumber mengikuti permintaan: **Judul, Penulis, Jurnal/Konferensi, URL, Permasalahan, Kontribusi, Metode/solusi, Hasil utama, Batasan, Relevansi dengan penelitian ini**.
>
> Catatan: tidak semua sumber adalah paper akademik. `S002` dan `S035` adalah dokumentasi vendor; beberapa paper berbayar/terblokir PDF-nya disimpan sebagai HTML/Firecrawl/query extraction dan diberi catatan pada bagian batasan.

## Daftar sumber

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

## S027

**Judul:** Deep learning for crowd counting in complex environments: challenges and novel trends

**Penulis:** Heba F. Elsepae; Heba M. El-Hoseny; Ehab K. I. Hamad; El-Sayed M. El-Rabaie

**Jurnal/Konferensi:** *Discover Computing* 29, artikel 101 (2026), artikel ulasan peer-reviewed Springer Nature

**URL:** https://doi.org/10.1007/s10791-026-09928-8

**Permasalahan:** Penghitungan kerumunan pada lingkungan kompleks masih sulit karena oklusi, kepadatan tidak merata, perubahan perspektif, pencahayaan rendah, cuaca buruk, latar belakang berantakan, dan perbedaan domain.

**Kontribusi:** Menyajikan ulasan mutakhir tentang metode, dataset, metrik, tantangan, dan tren deep learning untuk crowd counting; membedakan pendekatan detection-based, regression/density-map, heatmap, dan tracking-by-detection.

**Metode/solusi:** Ulasan naratif dengan proses seleksi terstruktur dari basis data ilmiah; membahas CNN, multi-scale/multi-column networks, attention, transformer, GAN/U-Net, fuzzy preprocessing, curriculum/adaptive learning, lightweight models, dan tracking-by-detection.

**Hasil utama:** Mengidentifikasi bahwa detection-based counting memberi lokalisasi individual tetapi lemah pada kerumunan padat, sedangkan density/heatmap lebih cocok untuk kepadatan tinggi tetapi tidak mempertahankan ID, arah, atau event line-crossing. Metrik umum yang dirangkum meliputi MAE, MSE/RMSE, SSIM, dan PSNR.

**Batasan:** Ini sumber ulasan, bukan eksperimen model baru; angka benchmark yang disebut berasal dari paper primer lain. Fokus utamanya density/count estimation sehingga klaim tentang ID persistence atau logika ROI perlu didukung sumber MOT/deployment lain.

**Relevansi dengan penelitian ini:** Berguna untuk framing gap antara density-map crowd counting dan people counting berbasis deteksi-pelacakan-ROI, serta untuk menjelaskan tantangan oklusi, variasi skala, pencahayaan, dan kebutuhan model ringan pada skenario nyata.

## S028

**Judul:** Crowd counting at the edge using weighted knowledge distillation

**Penulis:** Muhammad Asif Khan; Hamid Menouar; Ridha Hamila; Adnan Abu-Dayya

**Jurnal/Konferensi:** *Scientific Reports* 15, artikel 11932 (2025), peer-reviewed journal article

**URL:** https://doi.org/10.1038/s41598-025-90750-5

**Permasalahan:** Model crowd counting akurat sering berukuran besar dan mahal secara komputasi, sedangkan edge device seperti drone/Jetson membutuhkan inferensi cepat, hemat daya, dan tetap cukup akurat pada adegan kompleks.

**Kontribusi:** Mengusulkan weighted knowledge distillation untuk meningkatkan model crowd-counting ringan dengan mentransfer pengetahuan dari teacher model yang lebih besar ke student model yang kecil.

**Metode/solusi:** Menggunakan paradigma density-map crowd counting: anotasi titik/kepala dikonversi menjadi density map, prediksi dihitung dengan menjumlahkan density map. Teacher CSRNet/CSRNet_lite mentransfer pengetahuan ke student MCNN, DroneNet, dan LCDnet melalui loss distilasi berbobot.

**Hasil utama:** Evaluasi pada beberapa dataset menunjukkan KD menurunkan MAE pada berbagai student model, terutama ketika label terbatas. Paper juga melaporkan ukuran model, parameter, GMACs, dan waktu inferensi pada server, Jetson Xavier, dan Jetson Nano; contoh kompleksitas: LCDnet 0,05M parameter dan 0,21 MB.

**Batasan:** Density-map counting, bukan sistem deteksi-pelacakan-ID; tidak menyediakan line-crossing, arah masuk/keluar, atau pencegahan double counting. Penulis juga mengecualikan dataset yang terlalu padat karena student model sangat dangkal.

**Relevansi dengan penelitian ini:** Mendukung bagian edge deployment dan trade-off akurasi–komputasi, sekaligus menjadi pembanding bahwa model density-map ringan belum menyelesaikan kebutuhan ROI/trajectory-based people counting.

## S029

**Judul:** Deep learning in crowd counting: A survey

**Penulis:** Lijia Deng; Qinghua Zhou; Shuihua Wang; Juan Manuel Górriz; Yudong Zhang

**Jurnal/Konferensi:** *CAAI Transactions on Intelligence Technology* 9(5), 1043–1077 (2024; metadata BibTeX mencatat 2023 online/awal)

**URL:** https://doi.org/10.1049/cit2.12241

**Permasalahan:** Perkembangan crowd counting berbasis deep learning tersebar luas, sementara tantangan kepadatan tinggi, skenario dunia nyata, dan pemrosesan real-time masih belum tuntas.

**Kontribusi:** Mengusulkan taksonomi dataset tiga tingkat, memperkenalkan indeks kejelasan dataset Average Pixel Occupied by each Object (APO), mengklasifikasikan 36 dataset, dan meninjau lebih dari 110 algoritma.

**Metode/solusi:** Survei metode deep learning dari sudut pandang data: jaringan multi-scale, single-column, multi-column, multi-task, attention-based, weakly supervised, serta organisasi dataset berdasarkan skala dan kejelasan.

**Hasil utama:** Memberikan peta taxonomy dataset, metrik, dan evolusi algoritma; menegaskan oklusi, variasi skala, iluminasi, skenario real-world, dan real-time processing sebagai tantangan berulang. Ekstraksi lokal berupa metadata dan ringkasan query, bukan full text lengkap.

**Batasan:** Sumber ulasan dan tidak mengusulkan pipeline implementatif; pembahasannya luas sehingga detail ROI/ID/line-crossing tidak menjadi fokus.

**Relevansi dengan penelitian ini:** Berguna untuk menyusun latar belakang crowd-counting, pemilihan dataset/metrik seperti MAE/RMSE, dan membedakan density/count estimation dari people counting berbasis pelacakan.

## S030

**Judul:** Federated Learning for Crowd Counting in Smart Surveillance Systems

**Penulis:** Yiran Pang; Zhen Ni; Xiangnan Zhong

**Jurnal/Konferensi:** *IEEE Internet of Things Journal* 11(3), 5200–5209 (2024)

**URL:** https://doi.org/10.1109/JIOT.2023.3305933

**Permasalahan:** Pelatihan crowd-counting terpusat pada data video pengawasan menimbulkan risiko privasi, kebutuhan transmisi data mentah, dan biaya komunikasi dalam sistem smart surveillance/IoT.

**Kontribusi:** Mengembangkan kerangka horizontal federated learning (HFL) untuk melatih model crowd counting tanpa mengakses data privat pada perangkat lokal, serta menyediakan benchmark Federated Crowd Counting.

**Metode/solusi:** Model dilatih melalui agregasi model antarklien; paper merancang empat strategi partisi non-IID—feature-skew, quantity-skew, scene-skew, dan time-skew—serta menggunakan efficient fully convolutional network (e-FCN) yang ringan/communication-friendly.

**Hasil utama:** HFL dengan e-FCN dilaporkan kompetitif terhadap model yang lebih kompleks pada beberapa dataset dunia nyata, termasuk crowd surveillance, ShanghaiTech Part B, WorldExpo’10, FDST, CityUHK-X, UCSD, dan MALL. Full text lokal hanya berisi landing page; ringkasan detail diambil dari abstrak/metadata resmi, sehingga tidak dicantumkan angka metrik spesifik.

**Batasan:** Tidak secara langsung membahas tracker, ID persistence, line crossing, atau ROI counting; evaluasinya masih dalam konteks density/count estimation dan simulasi skenario FL non-IID.

**Relevansi dengan penelitian ini:** Mendukung argumen privasi dan deployment terdistribusi untuk smart surveillance; dapat dipakai sebagai konteks bahwa desain people-counting publik perlu mempertimbangkan data governance selain akurasi model.

## S031

**Judul:** TinyCount: an efficient crowd counting network for intelligent surveillance

**Penulis:** Hyeonbeen Lee; Jangho Lee

**Jurnal/Konferensi:** *Journal of Real-Time Image Processing* 21, artikel 153 (2024)

**URL:** https://doi.org/10.1007/s11554-024-01531-8

**Permasalahan:** Crowd-counting untuk intelligent CCTV/edge device membutuhkan performa robust, parameter sedikit, dan waktu respons cepat; banyak model akurat sulit ditanamkan pada perangkat terbatas.

**Kontribusi:** Mengusulkan TinyCount, jaringan crowd counting ringan dengan sekitar 60 ribu parameter untuk aplikasi intelligent surveillance.

**Metode/solusi:** TinyCount berupa fully convolutional network yang terdiri dari Feature Extract Module (FEM), Scale Perception Module (SPM), dan Upsampling Module (UM); memanfaatkan gagasan MobileNetV2, dilated convolution, transposed convolution, dan SE block.

**Hasil utama:** Abstrak melaporkan performa kompetitif pada tiga dataset crowd-counting representatif dengan parameter sekitar 3,33 sampai 271 kali lebih sedikit dibanding metode lain, serta evaluasi pada Raspberry Pi 4, NVIDIA Jetson Nano, dan NVIDIA Jetson AGX Xavier. Full text lokal adalah preview Springer, sehingga angka MAE/FPS spesifik tidak tersedia.

**Batasan:** Tetap density/count estimation berbasis citra, tidak mempertahankan ID individu atau event crossing. Akses lokal tidak memuat tabel hasil lengkap.

**Relevansi dengan penelitian ini:** Memberi bukti pendukung untuk kebutuhan model ringan pada perangkat edge dan intelligent CCTV, tetapi perlu dipasangkan dengan sumber tracker/ROI untuk sistem people counting berbasis lintasan.

## S032

**Judul:** Efficient crowd density estimation with edge intelligence via structural reparameterization and knowledge transfer

**Penulis:** Chenxi Lin; Xiaojian Hu

**Jurnal/Konferensi:** *Applied Soft Computing* 154, artikel 111366 (2024)

**URL:** https://doi.org/10.1016/j.asoc.2024.111366

**Permasalahan:** Estimasi kepadatan kerumunan real-time penting untuk keselamatan publik dan manajemen aliran massa, tetapi banyak model masih memakai backbone/modul berat yang sulit dijalankan pada edge device.

**Kontribusi:** Mengusulkan Repmobilenet, jaringan konvolusional multi-branch ringan untuk crowd counting edge, dengan structural reparameterization dan multi-layer knowledge distillation.

**Metode/solusi:** Menggunakan depthwise separable convolution untuk fitur multi-skala, dilated convolution untuk memperluas receptive field, structural reparameterization agar model training multi-branch berubah menjadi inference single-branch, dan teacher-student knowledge transfer untuk menjaga akurasi.

**Hasil utama:** Ringkasan ekstraksi menyebut performa counting sebanding dengan metode state-of-the-art sambil mempertahankan ukuran model dan latensi rendah, termasuk demonstrasi pada Jetson Nano. Full text tidak tersedia lokal, sehingga angka metrik spesifik tidak dicantumkan.

**Batasan:** Paradigma density estimation, bukan pelacakan trajectory/ID atau line/zone counting. Bukti lokal berbasis query extraction dan preview, bukan full text lengkap.

**Relevansi dengan penelitian ini:** Relevan untuk diskusi efisiensi edge, latency, dan trade-off akurasi–kecepatan; menjadi pembanding bagi pendekatan deteksi-pelacakan yang perlu real-time.

## S033

**Judul:** CrowdDiff: Multi-Hypothesis Crowd Density Estimation using Diffusion Models

**Penulis:** Yasiru Ranasinghe; Nithin Gopalakrishnan Nair; Wele Gedara Chaminda Bandara; Vishal M. Patel

**Jurnal/Konferensi:** IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2024

**URL:** https://arxiv.org/abs/2303.12790 ; https://doi.org/10.1109/CVPR52733.2024.01217

**Permasalahan:** Density-map crowd counting dengan Gaussian kernel lebar dapat menumpuk noise latar dan kehilangan density pada area padat; kernel sempit sulit dipelajari oleh regresi density konvensional.

**Kontribusi:** Memformulasikan generasi density map sebagai proses denoising diffusion, menggunakan narrow Gaussian kernel, auxiliary regression branch saat training, dan multi-hypothesis/fusion dari beberapa realisasi density map.

**Metode/solusi:** Conditional diffusion model menghasilkan density map dari citra kerumunan; peta hasil ditreshold menjadi crowd maps, beberapa realisasi digabungkan, dan branch regresi hanya dipakai saat training untuk memperbaiki pembelajaran fitur.

**Hasil utama:** Dievaluasi pada JHU-Crowd++, ShanghaiTech A/B, UCF-CC-50, UCF-QNRF, dan NWPU-Crowd dengan MAE/MSE; paper melaporkan hasil state-of-the-art, misalnya CrowdDiff MAE 47,3 pada JHU-Crowd++, 47,4 pada ShanghaiTech A, 5,7 pada ShanghaiTech B, 160,8 pada UCF-CC-50, 68,9 pada UCF-QNRF, dan 57,8 pada NWPU-Crowd.

**Batasan:** Model diffusion cenderung berat untuk inferensi real-time/edge; output tetap density/count map, bukan ID, trajectory, atau crossing event.

**Relevansi dengan penelitian ini:** Berguna sebagai pembanding SOTA density-map/diffusion counting dan untuk memperjelas gap bahwa akurasi density tinggi belum langsung memenuhi kebutuhan people counting berbasis lintasan dan ROI.

## S034

**Judul:** High-accuracy occupancy counting at crowded entrances for smart buildings

**Penulis:** Kailai Sun; Xinwei Wang; Tian Xing; Shaobo Liu; Qianchuan Zhao

**Jurnal/Konferensi:** *Energy and Buildings* 319, artikel 114509 (2024)

**URL:** https://doi.org/10.1016/j.enbuild.2024.114509

**Permasalahan:** Occupancy counting di pintu masuk ramai sulit karena oklusi, kedatangan/kepergian simultan, dan akumulasi kesalahan hitung; kesalahan ini dapat mengganggu kontrol bangunan berbasis okupansi.

**Kontribusi:** Mengusulkan metode occupancy tracking berbasis deep learning untuk entrance ramai, membuat/menandai dataset occupancy tracking, menggabungkan informasi multi-kamera, dan mengaitkannya dengan occupant-centric control.

**Metode/solusi:** Fokus pada head tracking untuk mengurangi efek oklusi; melatih model MOT, menerapkan logika trajectory/counting, melakukan fusi dua kamera, dan memakai informasi arrival/departure/increment untuk kontrol energi.

**Hasil utama:** Ringkasan ekstraksi melaporkan akurasi occupancy counting sekitar 98,1% dengan dua kamera pengawasan nyata, MOTA 80,4% dan 69,9% untuk dua kamera, peningkatan 7,7% atas metode pembanding, serta potensi penghematan energi ruang 17–25%.

**Batasan:** Dataset dan validasi berasal dari rentang scene terbatas; full text lokal tidak tersedia, sehingga detail eksperimen hanya bersumber dari query extraction/preview.

**Relevansi dengan penelitian ini:** Sangat relevan untuk people counting berbasis tracking pada pintu/entrance, terutama logika trajectory, head tracking saat oklusi, fusi kamera, dan evaluasi occupancy count.

## S035

**Judul:** Gst-nvdsanalytics — NVIDIA DeepStream documentation

**Penulis:** NVIDIA

**Jurnal/Konferensi:** Dokumentasi vendor NVIDIA DeepStream SDK 9.0; bukan paper akademik

**URL:** https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_plugin_gst-nvdsanalytics.html

**Permasalahan:** Implementasi people-counting real-time membutuhkan modul analitik praktis untuk ROI filtering, overcrowding detection, direction detection, dan line crossing di atas metadata detector/tracker.

**Kontribusi:** Mendokumentasikan plugin Gst-nvdsanalytics yang menambahkan metadata analitik level-frame dan level-objek pada pipeline DeepStream.

**Metode/solusi:** Plugin membaca metadata dari nvinfer/nvtracker; ROI filtering dapat bekerja dari output detector, sedangkan direction detection dan line crossing memerlukan tracker-id karena butuh riwayat/keadaan objek. Perhitungan memakai koordinat bottom-center bounding box dan aturan dikonfigurasi lewat file konfigurasi per stream/fitur.

**Hasil utama:** Dokumentasi menjelaskan fitur praktis: total objek dalam ROI per frame, status overcrowding berdasarkan threshold, arah objek berdasarkan riwayat posisi, serta cumulative/per-frame line-crossing count. Tidak ada hasil eksperimen akademik karena ini dokumentasi vendor.

**Batasan:** Tidak boleh dipakai sebagai bukti SOTA ilmiah; performa bergantung pada kualitas detector, tracker, konfigurasi aturan, dan kalibrasi ROI/line. Dokumentasi menjelaskan mekanisme implementasi, bukan validasi ilmiah.

**Relevansi dengan penelitian ini:** Sangat berguna untuk merancang logika counting berbasis ROI/line crossing dan menegaskan bahwa direction/line analytics membutuhkan ID tracker—tepat untuk bagian implementasi/deployment, bukan klaim kebaruan akademik.

## S036

**Judul:** MOT20: A benchmark for multi object tracking in crowded scenes

**Penulis:** Patrick Dendorfer; Hamid Rezatofighi; Anton Milan; Javen Shi; Daniel Cremers; Ian Reid; Stefan Roth; Konrad Schindler; Laura Leal-Taixé

**Jurnal/Konferensi:** MOTChallenge/arXiv benchmark; pertama dipresentasikan pada 4th BMTT MOT Challenge Workshop di CVPR 2019; arXiv 2020

**URL:** https://arxiv.org/abs/2003.09003 ; https://motchallenge.net/data/MOT20/

**Permasalahan:** Benchmark MOT sebelumnya kurang menekan pelacak pada skenario pedestrian sangat padat; evaluasi tracking butuh data dan protokol standar untuk oklusi/densitas tinggi.

**Kontribusi:** Memperkenalkan MOT20, benchmark multi-object tracking untuk adegan sangat ramai dengan 8 sekuens dari 3 scene, anotasi bounding box/ID, public detections, dan protokol evaluasi MOTChallenge.

**Metode/solusi:** Menyediakan train/test split, anotasi pedestrian serta kelas distractor/static/occluder, format data standar, dan evaluasi berbasis MOTA/MOTP/ID switch/fragmentation serta deteksi publik Faster R-CNN.

**Hasil utama:** Dataset mencakup 1.652.040 anotasi pedestrian dan total 2.102.385 anotasi semua kelas; kepadatan dapat mencapai 246 pedestrian per frame. MOT20 memberi benchmark yang jauh lebih padat dibanding rilis MOT awal dan menekan kemampuan tracking pada oklusi tinggi.

**Batasan:** Benchmark tracking, bukan dataset counting khusus; jumlah scene terbatas dan gerak pedestrian relatif reguler dibanding dataset seperti DanceTrack. Tidak langsung mengukur akurasi hitung ROI/line.

**Relevansi dengan penelitian ini:** Relevan sebagai dataset evaluasi tracker untuk crowded pedestrian scenes dan untuk menguji robustness deteksi-pelacakan sebelum diterapkan pada people counting real-time.

## S037

**Judul:** DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion

**Penulis:** Peize Sun; Jinkun Cao; Yi Jiang; Zehuan Yuan; Song Bai; Kris Kitani; Ping Luo

**Jurnal/Konferensi:** IEEE/CVF CVPR 2022

**URL:** https://arxiv.org/abs/2111.14690

**Permasalahan:** Banyak tracker modern terlalu mengandalkan appearance/re-ID dan dataset sebelumnya cenderung berisi objek dengan tampilan mudah dibedakan serta gerak relatif linear/reguler.

**Kontribusi:** Memperkenalkan DanceTrack, dataset MOT berskala besar dengan appearance seragam, gerak non-linear/diverse, pose ekstrem, oklusi, dan crossover yang sering.

**Metode/solusi:** Mengumpulkan 100 video tari/olahraga dengan 105.855 frame, membagi 40 train/25 validation/35 test, memberi bounding box dan ID, lalu mengevaluasi tracker SOTA dengan metrik HOTA, DetA, AssA, MOTA, dan IDF1.

**Hasil utama:** Paper menunjukkan penurunan signifikan kualitas association pada DanceTrack dibanding MOT17 meskipun metrik deteksi relatif tinggi; misalnya benchmark menegaskan bottleneck utama adalah association, bukan detection. Analisis juga menunjukkan motion modeling/temporal dynamics penting saat appearance cue lemah.

**Batasan:** Domain video tari tidak sama dengan CCTV ruang publik; dataset menonjolkan gerak kompleks dan appearance seragam, bukan kepadatan ekstrem seperti MOT20.

**Relevansi dengan penelitian ini:** Berguna untuk menguji atau mendiskusikan tracker yang harus tahan terhadap gerak non-linear dan appearance mirip, kondisi yang dapat menyebabkan ID switch dan double counting pada sistem people counting.

## S038

**Judul:** CrowdHuman: A Benchmark for Detecting Human in a Crowd

**Penulis:** Shuai Shao; Zijian Zhao; Boxun Li; Tete Xiao; Gang Yu; Xiangyu Zhang; Jian Sun

**Jurnal/Konferensi:** arXiv/dataset benchmark (2018)

**URL:** https://arxiv.org/abs/1805.00123 ; https://www.crowdhuman.org/

**Permasalahan:** Human detection pada kerumunan masih sulit karena oklusi berat, overlap antar orang, sensitivitas NMS, dan kurangnya dataset yang benar-benar merepresentasikan crowd scene.

**Kontribusi:** Memperkenalkan CrowdHuman, dataset deteksi manusia padat dan beragam dengan anotasi full-body box, visible-region box, dan head box untuk setiap instance.

**Metode/solusi:** Mengumpulkan sekitar 25.000 citra dari pencarian web dengan berbagai aktivitas/kota/viewpoint; split 15.000 train, 4.370 validation, dan 5.000 test; anotasi dilakukan exhaustively dan dicek ulang; evaluasi baseline memakai Faster R-CNN/FPN dan RetinaNet.

**Hasil utama:** Train+validation berisi sekitar 470 ribu human instances, rata-rata 22,6 orang per citra, dan overlap jauh lebih tinggi dari Caltech/CityPersons/COCO; rata-rata 2,40 pasangan orang per citra memiliki IoU > 0,5. Head detection juga dibahas sebagai bagian penting untuk people counting dan tracking.

**Batasan:** Dataset gambar statis untuk deteksi, bukan video tracking; tidak menyediakan ID temporal, trajectory, atau event counting. Tahun 2018 sehingga perlu dipadukan dengan benchmark/arsitektur terbaru.

**Relevansi dengan penelitian ini:** Relevan sebagai dataset pretraining/evaluasi detector manusia pada oklusi tinggi, terutama untuk meningkatkan robust detection/head detection sebelum tahap tracking dan counting.
