# USULAN PENDEKATAN (PROPOSED METHOD)

Catatan format sitasi: angka dalam kurung siku `[n]` dipakai untuk penanda sitasi di naskah Word. Nama penulis, tahun, dan kode sumber `Sxxx` dipertahankan pada daftar rujukan ringkas di akhir agar tetap cocok dengan `Status_Indeksasi_Referensi.pdf`.


Penelitian ini termasuk dalam kategori *applied research* di bidang *computer science* karena berfokus pada perancangan dan pengujian awal sistem *real-time people counting* berbasis video. Pendekatan yang digunakan adalah *detection-tracking-counting*, yaitu mendeteksi manusia pada setiap frame, mempertahankan identitas objek antar-frame melalui *multi-object tracking* (MOT), kemudian menghitung peristiwa masuk-keluar atau perpindahan zona berdasarkan lintasan objek. Rancangan ini dipilih karena kebutuhan *people counting* pada ruang publik tidak cukup diselesaikan dengan deteksi per-frame atau estimasi kepadatan saja. Diaz-Santos dkk. (2025 – S010) menunjukkan bahwa analisis arus penumpang berbasis video membutuhkan deteksi dan pemrosesan tepi secara real-time [1]. Nurseitov dkk. (2026 – S011) menekankan bahwa *people counting* di lingkungan urban perlu menggabungkan deteksi dan pelacakan agar lintasan objek dapat dipertahankan [2]. Sun dkk. (2024 – S034) juga memperlihatkan bahwa *occupancy counting* pada pintu masuk padat memerlukan mekanisme yang dapat mengurangi kesalahan hitung pada arus manusia yang saling berdekatan [3].

Secara umum, bagian ini disusun menjadi enam bagian utama, yaitu: (1) rancangan eksperimen, (2) arsitektur sistem yang diusulkan, (3) data eksperimen dan *preprocessing*, (4) tahapan pengembangan sistem, (5) rencana diskusi hasil, serta (6) rencana evaluasi sistem dan ancaman terhadap validitas. Pada tahap penulisan ini, eksperimen belum dijalankan sehingga bagian ini belum menyajikan hasil numerik. Penjelasan diarahkan pada rencana metodologi, rancangan arsitektur, skenario eksperimen, dan cara evaluasi yang akan digunakan pada tahap penelitian berikutnya.

### 3.1 Rancangan Eksperimen

Rancangan eksperimen disusun dengan mengadaptasi prinsip perencanaan eksperimen perangkat lunak dari Wohlin dkk. (2012), yaitu mendefinisikan tujuan, objek studi, domain, fokus, pertanyaan evaluasi, dan variabel yang diukur sebelum eksperimen dijalankan [16]. Adaptasi ini diperlukan agar eksperimen tidak hanya berupa uji coba model, tetapi memiliki struktur yang jelas untuk menjawab masalah penelitian: apakah integrasi detector, tracker, dan *counting logic* dapat menghasilkan sistem *people counting* yang akurat dan tetap layak dijalankan secara *real-time*.

**Tabel 1. Rancangan Eksperimen Penelitian**

| No. | Unsur | Deskripsi |
|---|---|---|
| 1 | Tujuan | Mengembangkan rancangan sistem *real-time people counting* berbasis *deep learning* yang mengintegrasikan detector manusia, MOT, dan *counting logic* berbasis RoI/zone/ID memory. Tujuan kedua adalah menyiapkan skenario evaluasi untuk menilai akurasi deteksi, stabilitas pelacakan, akurasi hitung, dan kelayakan *real-time*. |
| 2 | Objek studi | Pipeline *people counting* berbasis video yang terdiri dari komponen deteksi manusia, pelacakan multi-objek, validasi lintasan, memori status ID, dan keluaran hitungan masuk-keluar/per zona. |
| 3 | Domain | *Smart surveillance* dan pengelolaan ruang publik, misalnya pintu masuk gedung, koridor layanan, area kampus, halte/stasiun, atau area pengawasan dengan arus manusia dinamis. |
| 4 | Fokus | Fokus pertama adalah integrasi detector real-time/NMS-free dengan tracker yang mampu menjaga identitas pada kondisi oklusi dan gerak non-linear. Fokus kedua adalah perancangan *counting logic* agar sistem tidak menghitung objek yang sama berulang kali. Fokus ketiga adalah pengukuran performa agar pipeline tetap memungkinkan digunakan pada skenario *real-time*. |
| 5 | Pertanyaan evaluasi | PE1: Bagaimana kualitas deteksi manusia pada kondisi crowd dan oklusi? PE2: Bagaimana stabilitas ID yang dihasilkan DiffMOT dan OC-SORT pada video padat atau gerak kompleks? PE3: Seberapa besar pengaruh RoI/zone/ID memory terhadap *counting error*? PE4: Apakah pipeline masih memenuhi kebutuhan FPS dan latency yang realistis? |
| 6 | Variabel | Variabel data: jenis dataset, kepadatan, oklusi, pencahayaan, dan karakter gerak. Variabel model: detector, tracker, threshold, resolusi, dan FPS sampling. Variabel pengukuran: mAP/precision/recall, HOTA, IDF1, MOTA, ID switch, *counting error*, FPS, latency, dan penggunaan sumber daya. |

Rancangan eksperimen tersebut menempatkan sistem yang diusulkan sebagai pipeline terpadu, bukan sekadar kumpulan model. Komponen detector akan diuji untuk memastikan manusia dapat ditemukan pada frame video; komponen tracker akan diuji untuk memastikan identitas objek tetap stabil; sedangkan *counting logic* akan diuji untuk memastikan lintasan objek diterjemahkan menjadi event hitung yang benar. Dengan demikian, eksperimen yang direncanakan tidak berhenti pada akurasi deteksi, tetapi juga menilai akurasi hitung dan kelayakan sistem secara end-to-end.

### 3.2 Arsitektur Sistem yang Diusulkan

Arsitektur sistem yang diusulkan terdiri dari enam komponen utama: input video, *preprocessing*, deteksi manusia, pelacakan multi-objek, *counting logic*, serta keluaran dan evaluasi. Gambar 1 memperlihatkan alur sistem dari video masukan sampai keluaran hitungan dan log evaluasi.

[Sisipkan Gambar 1 di sini: `docs/diagrams/revisi-no3-architecture-gpt-image-2.png`]

**Gambar 1. Arsitektur sistem real-time people counting yang diusulkan.**

Pada Gambar 1, video dari CCTV atau rekaman ruang publik diproses menjadi frame berurutan. Tahap *preprocessing* mencakup penyesuaian ukuran frame, *frame sampling*, penentuan RoI, dan anotasi zona atau garis virtual. Setelah itu, detector manusia menghasilkan *bounding box* dan *confidence score* untuk objek manusia. YOLO26 diposisikan sebagai kandidat implementasi karena analisis Chakrabarty (2026 – S001) menekankan rancangan NMS-free pada deteksi real-time [4]. Dokumentasi Ultralytics (2026 – S002) melengkapi rujukan tersebut dari sisi orientasi implementasi dan *edge deployment* [5]. Namun, keduanya tetap ditempatkan sebagai rujukan implementasi awal, bukan satu-satunya dasar akademik. Untuk argumen ilmiah mengenai detector NMS-free/end-to-end, YOLOv10 dari Wang dkk. (2024 – S003) digunakan sebagai rujukan tren deteksi real-time tanpa NMS [6]. RT-DETR dari Zhao dkk. (2024 – S004) digunakan sebagai rujukan detector end-to-end berbasis transformer yang relevan dengan kebutuhan real-time [7].

Output detector diteruskan ke modul MOT. DiffMOT dirancang sebagai tracker utama karena Lv dkk. (2024 – S021) memodelkan prediksi gerak non-linear pada MOT sehingga relevan untuk skenario oklusi atau perubahan arah mendadak [8]. OC-SORT digunakan sebagai baseline dan *fallback* efisien karena Cao dkk. (2023 – S024) menunjukkan bahwa pendekatan *observation-centric* dapat membantu menjaga lintasan dengan beban komputasi lebih ringan [9]. Strategi dua jalur ini diperlukan karena tracker yang lebih robust belum tentu paling cepat, sedangkan tracker yang ringan belum tentu cukup stabil pada kondisi padat.

Setelah track ID diperoleh, modul *counting logic* mengevaluasi lintasan terhadap RoI polygon, garis virtual, dan transisi zona. Sistem tidak langsung menghitung jumlah *bounding box* pada frame, tetapi menunggu event lintasan yang valid. ID state memory digunakan untuk menyimpan status setiap objek, misalnya belum terlihat, kandidat, berada di RoI, melewati garis, sudah dihitung, *cooldown*, atau kedaluwarsa. Prinsip ini diadaptasi dari kebutuhan praktis *line crossing*, *direction detection*, dan ketergantungan pada tracker ID dalam sistem analitik video yang dijelaskan pada dokumentasi NVIDIA DeepStream (2026 – S035) [10]. Rujukan tersebut diposisikan sebagai referensi teknis, bukan bukti akademik utama. Secara akademik, kebutuhan penggabungan tracking dan counting diperkuat oleh studi Diaz-Santos dkk. (2025 – S010) tentang analisis arus penumpang real-time [1], Nurseitov dkk. (2026 – S011) tentang *people counting* dan tracking urban [2], serta Sun dkk. (2024 – S034) tentang *occupancy counting* pada pintu masuk padat [3].

Keluaran sistem berupa jumlah orang masuk, keluar, total per zona, *event log* per ID, visualisasi overlay, serta metrik evaluasi seperti FPS, latency, *counting error*, dan kesalahan asosiasi identitas. Log ini penting karena kesalahan hitung dapat berasal dari beberapa sumber berbeda: detector gagal menemukan objek, tracker mengganti ID, lintasan terfragmentasi, atau aturan zona tidak tepat.

### 3.3 Data Eksperimen dan Preprocessing

Data eksperimen direncanakan menggunakan kombinasi dataset publik dan video target. Dataset publik digunakan untuk menguji komponen deteksi dan tracking secara lebih objektif, sedangkan video target digunakan untuk memvalidasi *counting logic* pada konteks ruang publik yang mendekati kebutuhan aplikasi. Pemisahan ini penting karena dataset deteksi atau tracking tidak selalu menyediakan label event counting berbasis RoI atau garis virtual.

**Tabel 2. Rencana Data Eksperimen**

| Data | Karakteristik Utama | Penggunaan dalam Eksperimen | Sitasi |
|---|---|---|---|
| CrowdHuman | Dataset deteksi manusia pada kondisi crowd dan oklusi; menyediakan anotasi manusia pada citra padat. | Menguji atau menyesuaikan kemampuan detector manusia pada kondisi objek saling menutupi. Tidak digunakan langsung untuk event counting karena tidak memiliki lintasan temporal. | Shao dkk. (2018 – S038) [11] |
| MOT20 | Benchmark MOT untuk skenario pedestrian padat dan oklusi berat. | Menguji kualitas pelacakan, ID switch, fragmentasi track, dan robustness tracker pada crowd. | Dendorfer dkk. (2020 – S036) [12] |
| DanceTrack | Dataset MOT dengan gerak beragam dan penampilan objek relatif seragam. | Menguji tracker pada gerak non-linear dan kondisi asosiasi identitas yang sulit. | Sun dkk. (2022 – S037) [13] |
| Video target ruang publik | Rekaman CCTV atau video publik dengan sudut kamera tetap, variasi kepadatan, pencahayaan, dan arah arus. | Validasi pipeline end-to-end, terutama RoI/line/zone counting dan *counting error*. | Diaz-Santos dkk. (2025 – S010) [1]; Nurseitov dkk. (2026 – S011) [2]; Sun dkk. (2024 – S034) [3] |

Preprocessing dilakukan sesuai kebutuhan tiap jenis data. Pada data deteksi, frame atau citra akan disiapkan dalam format yang kompatibel dengan detector, misalnya normalisasi resolusi dan penyelarasan format anotasi. Pada data tracking, urutan frame dan anotasi track ID dijaga agar metrik HOTA, IDF1, MOTA, ID switch, dan fragmentasi dapat dihitung. Pada data target, preprocessing mencakup penentuan RoI polygon, garis virtual, zona asal-tujuan, timestamp, dan anotasi event counting manual sebagai *ground truth*.

Jika video target memuat wajah, plat nomor, atau informasi personal lain, data perlu dibatasi aksesnya atau dianonimkan sebelum digunakan secara luas. Hal ini penting karena tujuan penelitian adalah mengevaluasi lintasan dan jumlah orang, bukan mengidentifikasi individu tertentu. Dengan demikian, preprocessing tidak hanya menyangkut transformasi teknis frame, tetapi juga pengendalian privasi dan validitas data.

Agar video target dapat dipakai sebagai unit evaluasi, setiap video atau scene perlu dilaporkan karakteristiknya secara eksplisit. Karakteristik minimal yang perlu dicatat meliputi posisi kamera, durasi video, FPS sumber, kondisi pencahayaan, tingkat kepadatan rendah/sedang/tinggi, jumlah event masuk-keluar berdasarkan anotasi manual, serta bentuk RoI/line/zone yang digunakan. Unit evaluasi counting direncanakan berbasis video, zona, interval waktu, dan event crossing sehingga kesalahan hitung dapat ditelusuri ke konteks kejadian tertentu, bukan hanya dilaporkan sebagai total akhir.

### 3.4 Tahapan Pengembangan Sistem

Tahapan pengembangan sistem disusun secara bertahap agar setiap komponen dapat diuji dan dianalisis sebelum diintegrasikan. Gambar 2 memperlihatkan alur umum tahapan penelitian, mulai dari rancangan eksperimen sampai evaluasi dan analisis error.

[Sisipkan Gambar 2 di sini: `docs/diagrams/revisi-no3-research-workflow-gpt-image-2.png`]

**Gambar 2. Tahapan pengembangan dan evaluasi sistem.**

Tahap pertama adalah perumusan rancangan eksperimen. Pada tahap ini ditentukan tujuan, objek studi, domain, pertanyaan evaluasi, variabel yang diukur, serta batasan eksperimen. Kerangka ini mengacu pada prinsip perencanaan eksperimen perangkat lunak dari Wohlin dkk. (2012) agar eksperimen yang dilakukan tidak bersifat acak, tetapi diarahkan untuk menjawab pertanyaan penelitian [16].

Tahap kedua adalah persiapan data. CrowdHuman digunakan untuk kebutuhan deteksi manusia pada crowd karena Shao dkk. (2018 – S038) menyediakan benchmark deteksi manusia pada kondisi padat [11]. MOT20 digunakan untuk pelacakan pada kerumunan padat karena Dendorfer dkk. (2020 – S036) menargetkan evaluasi MOT pada skenario crowd [12]. DanceTrack digunakan untuk gerak non-linear dan asosiasi identitas yang sulit karena Sun dkk. (2022 – S037) merancang dataset dengan penampilan objek relatif seragam dan ragam gerak tinggi [13]. Video target digunakan untuk evaluasi *counting logic* pada konteks ruang publik karena Diaz-Santos dkk. (2025 – S010) menunjukkan kebutuhan analisis arus penumpang berbasis video real-time [1]. Rujukan tersebut dilengkapi oleh Nurseitov dkk. (2026 – S011) untuk konteks *people counting* dan tracking urban [2]. Sun dkk. (2024 – S034) digunakan untuk menguatkan kebutuhan *occupancy counting* pada pintu masuk padat [3]. Pada tahap ini juga dilakukan anotasi RoI, garis virtual, zona, serta ground truth event counting.

Tahap ketiga adalah penyusunan pipeline model. Detector dipakai untuk menghasilkan *bounding box* manusia. YOLO26 ditempatkan sebagai kandidat implementasi/prototipe berdasarkan analisis NMS-free dari Chakrabarty (2026 – S001) [4]. Dokumentasi Ultralytics (2026 – S002) digunakan sebagai rujukan implementasi teknis untuk kandidat tersebut [5]. YOLOv10 dari Wang dkk. (2024 – S003) menjadi rujukan akademik untuk rancangan detector real-time NMS-free [6]. RT-DETR dari Zhao dkk. (2024 – S004) menjadi rujukan akademik untuk detector end-to-end berbasis transformer [7]. Hasil deteksi kemudian diteruskan ke tracker. DiffMOT digunakan sebagai tracker utama untuk menguji prediksi gerak non-linear berdasarkan Lv dkk. (2024 – S021) [8]. OC-SORT menjadi baseline dan fallback efisien berdasarkan Cao dkk. (2023 – S024) [9].

Tahap keempat adalah pengujian skenario. Pengujian tidak hanya menilai satu model, tetapi memisahkan skenario deteksi, tracking, counting, dan performa real-time. Pemisahan ini penting karena sistem dapat memiliki detector yang baik tetapi tetap menghasilkan hitungan keliru jika tracker mengalami ID switch atau counting logic tidak tepat.

Tahap kelima adalah evaluasi dan analisis error. Hasil pengujian akan dianalisis menggunakan metrik deteksi, metrik MOT, metrik counting, dan metrik real-time. HOTA digunakan untuk menilai keseimbangan kualitas deteksi dan asosiasi sebagaimana dirumuskan oleh Luiten dkk. (2021 – S025) [14]. IDF1 digunakan untuk menilai konsistensi identitas lintasan berdasarkan ukuran evaluasi multi-target tracking dari Ristani dkk. (2016 – S026) [15]. Kesalahan counting akan ditelusuri kembali ke sumbernya: false positive detector, missed detection, ID switch, track fragmentation, kesalahan RoI/line, atau latency.

### 3.5 Rancangan ID State Memory untuk Counting Logic

Akurasi counting tidak hanya bergantung pada detector dan tracker, tetapi juga pada aturan kapan sebuah lintasan dianggap sebagai event yang sah. Oleh karena itu, penelitian ini merancang ID state memory untuk menyimpan status setiap track ID. Mekanisme ini dirancang untuk mengurangi risiko objek yang sama dihitung berulang ketika terjadi oklusi, ID reactivation, atau pergerakan bolak-balik di sekitar garis hitung.

[Sisipkan Gambar 3 di sini: `docs/diagrams/revisi-no3-id-state-memory-gpt-image-2.png`]

**Gambar 3. State machine ID State Memory.**

Pada Gambar 3, setiap objek dimulai dari status *unseen* ketika belum terdeteksi. Ketika detector menemukan kandidat manusia, status berubah menjadi *candidate*. Jika track masuk ke RoI, status menjadi *inside ROI*. Event counting baru dipertimbangkan ketika track benar-benar melewati garis atau berpindah zona sesuai arah yang ditentukan. Setelah event disimpan, status berubah menjadi *counted* lalu masuk ke *cooldown* agar objek yang sama tidak dihitung ulang dalam waktu singkat. Jika track tidak aktif melebihi batas waktu, status berubah menjadi *expired*.

Cabang *lost track* dan *recovered* digunakan untuk menangani oklusi atau fragmentasi lintasan. Jika track hilang sementara, sistem tidak langsung membuat event baru. Apabila track dapat dipulihkan dengan ID atau lintasan yang masih konsisten, status dapat kembali ke proses validasi. Namun, jika track hilang terlalu lama atau lintasan pemulihannya ambigu, sistem lebih aman mengakhiri status sebagai *expired*. Strategi konservatif ini diperlukan karena kesalahan pemulihan ID dapat langsung menyebabkan *double-counting* atau *missed counting*.

### 3.6 Rencana Skenario Eksperimen

Evaluasi sistem dirancang dalam empat skenario utama. Skenario pertama menilai detector, skenario kedua menilai tracker, skenario ketiga menilai *counting logic*, dan skenario keempat menilai pipeline secara end-to-end pada video target. Rancangan ini diselaraskan dengan rancangan eksperimen pada Tabel 1 agar setiap pertanyaan evaluasi memiliki data, metrik, dan keluaran yang jelas.

**Tabel 3. Rencana Skenario Eksperimen**

| Skenario | Fokus | Data | Metrik Utama | Tujuan Evaluasi |
|---|---|---|---|---|
| S1 — Evaluasi Deteksi | Kualitas deteksi manusia dan latency detector. | CrowdHuman, subset MOT20, dan video target jika tersedia. | mAP, precision, recall, false positive, false negative, latency detector. | Menilai apakah detector cukup baik untuk menjadi input tracker pada kondisi crowd dan oklusi. |
| S2 — Evaluasi Tracking | Kualitas asosiasi identitas dan stabilitas lintasan. | MOT20 dan DanceTrack. | HOTA, IDF1, MOTA, ID switch, fragmentasi track, FPS tracker. | Membandingkan DiffMOT sebagai jalur robust dan OC-SORT sebagai fallback efisien. |
| S3 — Evaluasi Counting Logic | Akurasi hitung berbasis RoI/line/zone dan ID memory. | Video target atau skenario video publik dengan anotasi event counting manual. | MAE, MAPE, over-count, under-count, direction accuracy, counting error rate. | Menilai apakah RoI, transisi zona, dan ID state memory mengurangi hitung ganda atau event yang hilang. |
| S4 — Evaluasi End-to-End dan Real-Time | Kelayakan pipeline lengkap. | Video target ruang publik. | FPS end-to-end, latency rata-rata/p95, penggunaan CPU/GPU/memori, counting error. | Menilai apakah seluruh pipeline dapat berjalan pada batas latency yang realistis dan tetap menghasilkan hitungan yang dapat dipertanggungjawabkan. |

Pada S1, detector akan dievaluasi terutama pada kemampuan mengenali manusia kecil, saling menutupi, atau berada pada kepadatan tinggi. Pada S2, tracker akan dievaluasi berdasarkan kemampuan mempertahankan ID pada kondisi oklusi dan gerak non-linear. Pada S3, eksperimen akan membandingkan beberapa variasi *counting logic*, misalnya line crossing sederhana, line crossing dengan RoI, transisi zona, dan transisi zona dengan ID state memory. Pada S4, seluruh komponen digabungkan untuk melihat performa end-to-end, termasuk sumber error dan bottleneck komputasi.

### 3.7 Rencana Diskusi Hasil

Karena eksperimen belum dijalankan, bagian ini tidak menyatakan hasil aktual. Diskusi hasil yang direncanakan akan diarahkan pada interpretasi tiap skenario. Pada skenario deteksi, hasil akan dianalisis untuk melihat hubungan antara kualitas deteksi, objek kecil, oklusi, dan latency. Jika detector memiliki precision tinggi tetapi recall rendah, sistem mungkin mengurangi false positive tetapi berisiko melewatkan orang yang harus dihitung. Jika recall tinggi tetapi false positive besar, counting logic berisiko menerima event yang tidak valid.

Pada skenario tracking, diskusi akan membandingkan stabilitas DiffMOT dan OC-SORT. DiffMOT diperkirakan relevan pada gerak non-linear karena pendekatan *diffusion-based motion prediction* dari Lv dkk. (2024 – S021), tetapi perlu diuji apakah kompleksitasnya masih sesuai untuk kebutuhan real-time [8]. OC-SORT diperkirakan lebih efisien sebagai fallback berdasarkan pendekatan *observation-centric* dari Cao dkk. (2023 – S024), tetapi perlu diuji apakah stabilitas ID-nya cukup pada kondisi oklusi berat [9]. Diskusi hasil tidak akan hanya melihat nilai HOTA atau IDF1, tetapi juga pola kegagalan seperti ID switch, track fragmentation, dan reactivation yang keliru.

Pada skenario counting, analisis akan berfokus pada sumber *counting error*. Over-count dapat terjadi karena ID switch, track reactivation yang salah, atau objek yang berulang kali bergerak di sekitar garis virtual. Under-count dapat terjadi karena missed detection, track yang hilang sebelum melintasi zona, atau aturan validasi yang terlalu ketat. Dengan memisahkan sumber error, perbaikan sistem dapat diarahkan secara lebih tepat: apakah perlu memperbaiki detector, tracker, RoI, threshold, atau aturan ID state memory.

Pada skenario end-to-end, diskusi hasil akan menghubungkan akurasi hitung dengan kelayakan runtime. Sistem yang akurat tetapi terlalu lambat belum memenuhi tujuan real-time; sebaliknya sistem yang cepat tetapi sering salah hitung juga belum layak digunakan. Oleh karena itu, hasil akan dibahas sebagai trade-off antara akurasi deteksi, konsistensi ID, akurasi counting, dan FPS/latency.

### 3.8 Rencana Evaluasi Sistem dan Ancaman terhadap Validitas

Evaluasi sistem akan menggunakan metrik berbeda untuk setiap komponen. Deteksi dievaluasi menggunakan mAP, precision, recall, false positive, false negative, dan latency detector. Tracking dievaluasi menggunakan HOTA untuk membaca keseimbangan deteksi-asosiasi berdasarkan Luiten dkk. (2021 – S025) [14]. Tracking juga dievaluasi menggunakan IDF1, MOTA, ID switch, dan fragmentasi track berdasarkan kerangka evaluasi multi-target tracking dari Ristani dkk. (2016 – S026) [15]. Counting dievaluasi menggunakan absolute counting error, MAE, MAPE, over-count, under-count, dan direction accuracy. Kelayakan real-time dievaluasi menggunakan FPS end-to-end, latency rata-rata, latency p95, serta penggunaan CPU/GPU/memori.

Definisi operasional metrik counting direncanakan sebagai berikut. Absolute counting error dihitung sebagai selisih absolut antara jumlah event hasil sistem dan jumlah event ground truth manual pada unit evaluasi tertentu. MAE dihitung sebagai rata-rata absolute counting error pada seluruh video, zona, atau interval evaluasi. MAPE hanya digunakan bila jumlah event ground truth cukup besar agar tidak menimbulkan distorsi pada scene dengan jumlah event sangat kecil. Over-count dicatat ketika sistem menghasilkan event tambahan yang tidak ada pada ground truth, sedangkan under-count dicatat ketika event ground truth tidak terdeteksi oleh sistem. Direction accuracy dihitung sebagai proporsi event yang arah masuk/keluarnya sesuai dengan label manual. FPS dan latency dihitung secara end-to-end, yaitu dari preprocessing frame sampai event counting/logging, bukan hanya waktu inferensi detector.

Ancaman validitas internal muncul karena hasil sistem dapat dipengaruhi oleh threshold detector, resolusi input, FPS sampling, parameter tracker, panjang buffer track, dan aturan ID state memory. Mitigasinya adalah mencatat konfigurasi eksperimen secara lengkap dan melakukan ablation agar pengaruh detector, tracker, dan counting logic dapat dipisahkan.

Ancaman validitas konstruk muncul karena metrik yang digunakan mengukur aspek berbeda. mAP tidak sama dengan akurasi counting; HOTA dan IDF1 tidak langsung menjamin jumlah masuk-keluar benar; FPS tinggi tidak menjamin lintasan valid. Karena itu, kesimpulan harus ditarik sesuai metriknya masing-masing. Keberhasilan sistem baru dapat dinilai ketika metrik deteksi, tracking, counting, dan runtime dibaca bersama.

Ancaman validitas kesimpulan muncul jika jumlah video target, variasi scene, atau jumlah event counting terlalu kecil. Mitigasinya adalah melaporkan jumlah video, jumlah event, variasi kepadatan, kondisi pencahayaan, dan karakter kamera secara transparan. Jika data target masih terbatas, hasil hanya boleh dinyatakan sebagai validasi awal, bukan generalisasi untuk semua ruang publik.

Ancaman validitas eksternal muncul karena dataset publik tidak sepenuhnya sama dengan CCTV ruang publik lokal. CrowdHuman berfokus pada deteksi manusia dalam citra padat, bukan event counting temporal [11]. MOT20 berfokus pada pelacakan pedestrian padat sehingga cocok untuk menguji tracker, tetapi belum mewakili aturan RoI/line counting lokal [12]. DanceTrack menguji asosiasi identitas pada ragam gerak tinggi, tetapi domain visualnya tetap berbeda dari CCTV ruang publik target [13]. Mitigasinya adalah menggunakan dataset publik untuk menguji komponen, lalu tetap menambahkan video target untuk menguji event counting. Dengan demikian, penelitian dapat membedakan antara performa pada benchmark dan kesesuaian pada domain aplikasi.

Ancaman implementasi muncul karena YOLO26 masih bersumber dari analisis preprint Chakrabarty (2026 – S001), sehingga tidak boleh dijadikan satu-satunya dasar novelty akademik [4]. Dokumentasi vendor Ultralytics (2026 – S002) juga hanya dipakai sebagai rujukan implementasi teknis, bukan publikasi akademik terindeks [5]. Mitigasinya adalah memosisikan YOLO26 sebagai kandidat implementasi. Argumen akademik mengenai detector NMS-free/end-to-end ditopang oleh YOLOv10 dari Wang dkk. (2024 – S003) [6] dan RT-DETR dari Zhao dkk. (2024 – S004) [7]. Dokumentasi DeepStream dari NVIDIA (2026 – S035) juga dipakai hanya sebagai referensi teknis untuk RoI, direction detection, dan line crossing, bukan sebagai bukti akademik utama [10].

Ancaman etika dan privasi muncul karena video ruang publik dapat memuat wajah atau informasi personal. Mitigasi awal mencakup penggunaan data dengan izin yang jelas, pembatasan akses data mentah, anonimisasi bila diperlukan, dan penyimpanan log yang hanya berisi informasi teknis lintasan serta event counting. Evaluasi diarahkan pada perilaku sistem terhadap objek manusia secara agregat, bukan identifikasi individu.

### Daftar Rujukan Ringkas untuk Sitasi Word

Gunakan nomor berikut untuk sitasi di naskah. Kode `Sxxx` dipertahankan agar sumber tetap bisa dicocokkan dengan `Status_Indeksasi_Referensi.pdf` dan `references/references.bib`.

[1] Diaz-Santos, Caballero-Gil, & Caballero-Gil (2025 – S010). *Real-Time Passenger Flow Analysis in Tram Stations Using YOLO-Based Computer Vision and Edge AI on Jetson Nano*.

[2] Nurseitov dkk. (2026 – S011). *Vision-Based People Counting and Tracking for Urban Environments*.

[3] Sun dkk. (2024 – S034). *High-accuracy occupancy counting at crowded entrances for smart buildings*.

[4] Chakrabarty (2026 – S001). *YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection*.

[5] Ultralytics (2026 – S002). *Ultralytics YOLO26 Documentation*.

[6] Wang dkk. (2024 – S003). *YOLOv10: Real-Time End-to-End Object Detection*.

[7] Zhao dkk. (2024 – S004). *DETRs Beat YOLOs on Real-time Object Detection / RT-DETR*.

[8] Lv dkk. (2024 – S021). *DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction*.

[9] Cao dkk. (2023 – S024). *Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking*.

[10] NVIDIA (2026 – S035). *Gst-nvdsanalytics — NVIDIA DeepStream Documentation*.

[11] Shao dkk. (2018 – S038). *CrowdHuman: A Benchmark for Detecting Human in a Crowd*.

[12] Dendorfer dkk. (2020 – S036). *MOT20: A benchmark for multi object tracking in crowded scenes*.

[13] Sun dkk. (2022 – S037). *DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion*.

[14] Luiten dkk. (2021 – S025). *HOTA: A Higher Order Metric for Evaluating Multi-object Tracking*.

[15] Ristani dkk. (2016 – S026). *Performance Measures and a Data Set for Multi-target, Multi-camera Tracking*.

[16] Wohlin dkk. (2012). *Experimentation in Software Engineering*.
