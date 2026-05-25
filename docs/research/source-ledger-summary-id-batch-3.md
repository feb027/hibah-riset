# Ringkasan Source Ledger — Batch 3 (S027–S038)

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
