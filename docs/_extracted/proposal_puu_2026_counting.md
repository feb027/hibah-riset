# Extracted text: Proposal PUU 2026 - Counting(2).pdf

- Source: `/home/aqua/hibah-riset/docs/Proposal PUU 2026 - Counting(2).pdf`
- Extracted: 2026-05-24T18:28:31.468972Z
- Pages: 11
- Characters: 29650
- Metadata: `{"format": "PDF 1.7", "title": "PUU 2026", "author": "informatika;Desti Karmini Nurdatillah;Febnawan Fatur Rochman", "keywords": "Riset", "creator": "Microsoft® Word for Microsoft 365", "producer": "Microsoft® Word for Microsoft 365", "creationDate": "D:20260525011611+07'00'", "modDate": "D:20260525011611+07'00'"}`


## Page 1

Isian Substansi Proposal 
PENELITIAN KOMPETITIF UNIVERSITAS SILIWANGI TAHUN 2026 
SKEMA PENELITIAN UNGGULAN UNSIL (PUU) 
Petunjuk : Pengusul hanya diperkenankan mengisi di tempat yang telah 
disediakan dan tidak diperkenankan melakukan modifikasi template atau 
menghapus bagian template.  
 
A. JUDUL 
Tuliskan judul usulan penelitian maksimal 20 kata 
 
Pengembangan Model Rekognisi Objek untuk Real-Time People Counting System Berbasis Deep 
Learning 
 
B. RINGKASAN 
Isian ringkasan penelitian tidak lebih dari 300 kata yang berisi urgensi, tujuan, metode, dan 
luaran yang ditargetkan 
 
Dalam pengelolaan ruang publik modern, kebutuhan terhadap sistem pemantauan jumlah individu 
secara akurat dan real-time semakin penting, khususnya pada area dengan mobilitas tinggi seperti 
stasiun transportasi, pusat perbelanjaan, fasilitas pendidikan, dan berbagai layanan publik. Metode 
konvensional yang mengandalkan pengamatan manual melalui kamera pengawas atau perhitungan 
langsung oleh petugas memiliki berbagai keterbatasan, seperti ketergantungan pada tenaga manusia, 
akurasi yang rendah, serta kesulitan beradaptasi dengan kondisi lingkungan dinamis seperti 
kepadatan tinggi, variasi pencahayaan, dan pergerakan objek yang kompleks. Kondisi tersebut dapat 
menyebabkan kesalahan penghitungan yang berdampak pada kurang optimalnya pengelolaan 
kapasitas ruang, sistem keamanan, maupun manajemen kerumunan.  
 
Perkembangan teknologi computer vision berbasis deep learning membuka peluang untuk 
mengembangkan sistem penghitungan manusia secara otomatis dan real-time dari aliran video 
pengawasan. Penelitian ini bertujuan mengembangkan model rekognisi objek dan sistem 
penghitungan jumlah orang secara real-time dengan mengintegrasikan arsitektur deteksi objek 
YOLO26 dan algoritma pelacakan multi-objek berbasis DiffMOT. Integrasi ini dirancang untuk 
meningkatkan akurasi deteksi serta konsistensi identitas objek dalam kondisi kerumunan padat, 
oklusi ekstrem, dan pergerakan manusia yang tidak linier. 
 
Tahapan penelitian diawali dengan pengumpulan dataset kerumunan dari sumber publik seperti 
MOT20 dan DanceTrack, yang dilanjutkan dengan proses preprocessing serta augmentasi data. 
Selanjutnya, dilakukan pengembangan model deteksi berbasis YOLO26 dan implementasi sistem 
pelacakan adaptif menggunakan DiffMOT, dengan dukungan OC-SORT sebagai alternatif pada 
perangkat berspesifikasi terbatas. Sistem juga dilengkapi modul advanced counting logic yang 
memanfaatkan Region of Interest (RoI) Polygon, analisis lintasan zona, serta mekanisme ID State 
Memory untuk mencegah penghitungan ganda akibat gangguan deteksi atau oklusi. Luaran yang 
ditargetkan adalah prototype sistem real-time people counting berbasis deep learning, publikasi 
ilmiah pada jurnal internasional bereputasi, serta pendaftaran hak cipta perangkat lunak dari sistem 
yang dikembangkan. Tingkat Kesiapterapan Teknologi (TKT) ditargetkan berada pada level 3–4 
melalui validasi awal menggunakan rekaman video lingkungan publik yang merepresentasikan 
kondisi nyata.


## Page 2

C. KATA KUNCI 
Isian maksimal 5 kata kunci yang dipisahkan dengan tanda titik koma (;) 
 
Crowd Management; DiffMOT; Multi-Object Tracking; Real-Time People Counting; YOLO26 
 
D. PENDAHULUAN 
Pendahuluan penelitian tidak lebih dari 1000 kata yang memuat, latar belakang, rumusan 
permasalahan yang akan diteliti, pendekatan pemecahan masalah, state-of-the-art dan kebaruan, 
peta jalan (road map) penelitian setidaknya 5 tahun. Sitasi disusun dan ditulis berdasarkan sistem 
nomor sesuai dengan urutan pengutipan. 
 
Kebutuhan terhadap sistem yang efisien dan aman dalam manajemen ruang publik semakin penting, 
khususnya pada area berkepadatan tinggi seperti stasiun transportasi, pusat perbelanjaan, dan fasilitas 
institusi pendidikan [1]{Formatting Citation}. Metode tradisional kesulitan menghitung jumlah 
individu secara akurat ketika dihadapkan pada skenario dunia nyata yang bervariasi. Faktor seperti 
pencahayaan buruk, kerumunan padat, cuaca tidak mendukung, dan variasi sudut pandang dapat 
mengacaukan hasil perhitungan [2][2]. Sistem tradisional rentan terhadap human error, memiliki 
akurasi rendah dalam mendeteksi pergerakan komunal, serta sulit beradaptasi pada kondisi 
lingkungan yang dinamis [3][3]. Pemantauan berbasis visual menawarkan pengawasan lebih 
komprehensif, namun penghitungan manual dari layar CCTV tetap tidak efisien untuk volume massa 
besar. 
Dalam konteks tersebut, sistem computer vision berbasis deep learning menjadi pendekatan paling 
menjanjikan untuk mengotomatisasi deteksi dan penghitungan manusia dari aliran video secara real-
time [3]. Paradigma Tracking-by-Detection (TBD) diakui sebagai metode dominan dalam arsitektur 
Multi-Object Tracking (MOT) [4][4], namun implementasinya di lingkungan publik menghadapi 
tantangan kompleks, meliputi oklusi ekstrem pada kerumunan padat dengan kepadatan lebih dari 200 
pejalan kaki per frame [5][5], variasi skala akibat jarak kamera, serta dinamika pergerakan pejalan 
kaki yang acak dan tidak linier [6][6]. Kondisi tersebut menunjukkan adanya kesenjangan yang belum 
terpecahkan secara optimal, sehingga penelitian ini merumuskan dua pertanyaan utama: (1) 
Bagaimana merancang model deteksi manusia berbasis YOLOv26 yang mampu beroperasi secara 
real-time tanpa NMS (NMS-Free) dengan akurasi tinggi di lingkungan dengan oklusi parah? dan (2) 
Bagaimana mengintegrasikan YOLO26 dengan algoritma pelacakan DiffMOT dan OC-SORT secara 
otomatis untuk menangani pergerakan non-linier guna menghasilkan penghitungan manusia yang 
persisten dan andal? 
Penelitian ini mengusulkan sistem deteksi, pelacakan, dan penghitungan manusia secara real-time 
menggunakan YOLO26 yang diintegrasikan dengan DiffMOT untuk menjawab tantangan oklusi 
ekstrem dan pergerakan non-linier. YOLO26 dipilih karena mengeliminasi Non-Maximum 
Suppression (NMS) melalui penugasan one-to-one label sehingga menghasilkan kecepatan inferensi 
end-to-end optimal pada perangkat edge [7][8]. Fitur Small-Target-Aware Label Assignment (STAL) 
memanfaatkan ambang batas dinamis untuk mengidentifikasi objek manusia berukuran sangat kecil 
dari tangkapan kamera jauh [7][8]. Model dioptimasi melalui fine-tuning menggunakan dataset 
CrowdHuman, MOT20, dan DanceTrack untuk melatih kemampuan generalisasi terhadap oklusi 
parah [8][9]. 
Berbagai literatur terdahulu membuktikan potensi deep learning dalam deteksi dan pelacakan objek. 
Integrasi arsitektur YOLO generasi terbaru dengan algoritma pelacakan menghasilkan sistem 
penghitungan objek real-time dengan akurasi tinggi serta efisiensi komputasi yang baik [9][10]. 
Formatted: Indonesian
Field Code Changed
Formatted: Indonesian
Formatted: Indonesian
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Formatted: Swedish (Sweden)
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)


## Page 3

Namun pendekatan konvensional masih memiliki kelemahan berupa kehilangan atau pertukaran ID 
saat objek terhalang sesaat, akibat penggunaan Kalman Filter yang mengasumsikan pergerakan linier 
sehingga kurang adaptif terhadap dinamika kerumunan [9][10]. 
Kebaruan penelitian ini terletak pada integrasi YOLO26 dengan DiffMOT sebagai sistem MOT 
berbasis Generative AI. DiffMOT mengadopsi Diffusion Probabilistic Models untuk memprediksi 
lintasan non-linear pada kerumunan kompleks [10][11], dengan secara bertahap memperbaiki 
prediksi posisi objek dari distribusi acak menjadi lintasan akurat sehingga tangguh terhadap gangguan 
deteksi dan oklusi. Karena arsitektur difusi probabilistik menuntut komputasi besar, penelitian ini 
mengintegrasikan OC-SORT sebagai backup plan. OC-SORT memperbaiki kelemahan asumsi linier 
Kalman Filter melalui modul Observation-centric Re-Update (ORU) dan Observation-Centric 
Momentum (OCM) untuk mengurangi akumulasi eror selama objek tidak terlihat [4][4]. Untuk 
menjamin validitas hasil, sistem menerapkan Advanced Counting Logic yang terdiri dari tiga 
komponen yaitu, Region of Interest (RoI) Polygon sebagai zona deteksi aktif non-linear yang 
menyesuaikan geometri area pemantauan [11][12], Zone-to-Zone Trajectory Analysis untuk 
memvalidasi arah lintasan objek berdasarkan metodologi pemisahan area deteksi [12][13], dan ID 
State Memory untuk penguncian identitas secara permanen selama objek berada dalam frame guna 
mencegah double-counting akibat fluktuasi deteksi [13][14]. 
Secara sistematis, pengembangan sistem dibagi menjadi tiga tahap utama. Pertama, Preprocessing 
dan Augmentasi Data untuk mempersiapkan dataset yang representatif. Kedua, Pelatihan dan Fine-
Tuning YOLO26 beserta algoritma pelacakan dengan mengoptimalkan parameter ProgLoss guna 
meningkatkan akurasi deteksi. Ketiga, evaluasi model menggunakan metrik HOTA untuk mengukur 
keseimbangan antara akurasi deteksi dan asosiasi identitas [14], MOTA dan IDF1 untuk mengukur 
konsistensi identitas [15], serta FPS untuk mengukur kecepatan pemrosesan secara real-time 
[16].Evaluasi Model menggunakan metrik HOTA, MOTA, dan IDF1 untuk mengukur konsistensi 
identitas, serta FPS untuk mengukur kecepatan pemrosesan secara real-time. 
Penelitian ini diharapkan berkontribusi pada pengembangan teknologi smart city dan crowd 
management, khususnya otomasi pengawasan keamanan fasilitas publik. Sistem ini relevan untuk 
memenuhi kebutuhan pemantauan demografis yang dinamis, adaptif, dan berbasis data secara real-
time.  
Roadmap Penelitian 5 Tahun 
a. Tahun 1: Pengembangan arsitektur awal YOLO26 terintegrasi DiffMOT  
b. Tahun 2: Peningkatan ketahanan model terhadap oklusi  parah dan fluktuasi pencahayaan. 
c. Tahun 3: Pengembangan fitur atensi untuk menangkap pola pergerakan kompleks. 
d. Tahun 4: Implementasi kompresi model untuk optimasi kecepatan inferensi pada perangkat 
edge. 
e. Tahun 5: Hilirisasi sistem ke infrastruktur Smart City dan layanan forensik digital. 
Berdasarkan peta jalan kelompok keilmuan Artificial Intelligence Siliwangi (Gambar 1), penelitian 
ini menempati posisi Market Product (MP1: Automation System and Intelligent Software). Pada Basic 
Application, mencakup  BA2 (Computer Vision and Robotics) dan BA14 (Image and Video 
Generation). Pada Applied Application , masuk dalam AA21 (Pattern Recognition in Various 
Domain). Penelitian ini jugaTerakhir, bertumpu pada BK3 (Machine Learning) dengan menggunakan 
arsitektur Deep Learning untuk rekognisi objek real-time. 
Field Code Changed
Formatted: Swedish (Sweden)
Field Code Changed
Formatted: Swedish (Sweden)
Formatted: Indonesian
Field Code Changed
Formatted: Indonesian
Formatted: Indonesian
Field Code Changed
Formatted: Indonesian
Formatted: Indonesian
Field Code Changed
Formatted: Indonesian
Formatted: Indonesian
Field Code Changed
Formatted: Indonesian
Formatted: Indonesian
Formatted: Font: Italic, Indonesian
Formatted: Indonesian
Formatted: Font: Italic, Indonesian
Formatted: Indonesian


## Page 4

Gambar 1. Peta Jalan Kelompok Keilmuan Artificial Intelligence Siliwangi 
Pada setiap lapisan peta jalan telah dilakukan riset sebelumnya dengan beberapa luaran 
publikasi beberapa tahun terakhir sebagai berikut: 
 
No. 
Penulis 
Judul 
Tahun 
1 
Aradea, R. Rianto, H. 
Mubarok 
Inference Model for Self-Adaptive IoT Service 
Systems 
2021 
2 
Aradea, R. Rianto, H. 
Mubarok 
Cultivating Service Knowledge Models for IoT-
Based Systems Adaptability 
2022 
3 
Aradea, R. Rianto, H. 
Mubarok, I. Darmawan 
Deep Learning-based Regional Plant Type 
Recommendation 
System 
for 
Enhancing 
Agricultural Productivity 
2023 
4 
Aradea, R. Rianto, H. 
Mubarok, G. F. Nugraha 
Recognition of Organic Waste Objects Based on 
Vision Systems Using Attention Convolutional 
Neural Networks Models 
2024 
5 
G. F. Nugraha, Aradea, 
R. Rianto, R. Mardiati 
Object Detection for the Visually Impaired: A 
Systematic Literature Review 
2024 
6 
Aradea, R. Rianto, N. 
Herlina, I. Hoeronis 
Self-Learning Model for Pattern Recognition in 
Vision System Based on Adaptive Kernel 
2025 
7 
Rianto, V. Purwayoga, 
Aradea, A. A. Mikail, I. 
Yumna 
SOCA-YOLO: Smart Optic with Coordinate 
Attention Model for Vision System-Based Eye 
Disease Detection 
2025 
8 
I. Hoeronis, Aradea, I. 
Darmawan, R. Rianto, 
G. F. Nugraha 
LAYUNG-YOLOv12: Illuminating Corrosion 
Detection in Low-light Environments with 
Dynamic Convolutional Attention 
2026 
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic


## Page 5

Selaras dengan seluruh hasil penelitian tersebut, perlu dilakukannya penelitian terkait penerapan 
computer vision dalam pengenalan dan pelacakan objek secara otomatis diperlukan untuk 
menghasilkan sistem penghitungan jumlah manusia yang presisi dalam konteks manajemen ruang 
publik. 
 
 
E. METODE  
Isian metode atau cara untuk mencapai tujuan yang telah ditetapkan tidak lebih dari 1000 kata. 
Pada bagian metode wajib dilengkapi dengan diagram alir penelitian yang menggambarkan apa 
yang sudah dilaksanakan dan yang akan dikerjakan selama waktu yang diusulkan. Format 
diagram alir dapat berupa file JPG/PNG. Metode penelitian harus memuat sekurang-kurangnya 
prosedur penelitian, hasil yang diharapkan, indikator capaian yang ditargetkan, serta anggota 
tim/mitra yang bertanggung jawab pada setiap tahapan penelitian. Metode penelitian harus 
sejalan dengen Rencana Anggaran Biaya (RAB) 
 
Diagram alir penelitian secara keseluruhan seperti disajikan pada Gambar 2, dan pada setiap tahapan 
penelitian dilengkapi dengan indikator sebagai capaian dari aktivitas penelitian yang dilakukan. 
 
 
Gambar 2. Diagram Alir Penelitian 
 
Proses spesifikasi artifak dilakukan dengan mengikuti cara perancangan yang dilakukan oleh G.Pahl 
dan W.Beitz dalam bukunya yang berjudul Engineering Design : Systematic Approach. Pendekatan 
ini menekankan pada empat fase dalam perancangan produk atau alat  [17][15], seperti terlihat pada 
Gambar 3, yaitu perencanaan dan penjelasan tugas, perancangan konsep produk, perancangan 
bentuk produk, dan perancangan detail produk. 
 
 
Gambar 3. Fase Perancangan Produk 
 
Gambar 4 memperlihatkan arsitektur dan pipeline sistem real-time people counting yang mencakup 
Formatted: Font: Italic


## Page 6

tahapan preprocessing data, deteksi objek, pelacakan multi-objek, logika perhitungan lanjutan, serta 
evaluasi performa model.  
 
Gambar 4. Diagram Alur Pengembangan Sistem Real-Time People Counting 
 
Sesuai dengan diagram alir penelitian yang disajikan, metodologi ini dibagi menjadi 
beberapa tahapan utama sebagai berikut: 
1. Pengumpulan dan Pembagian Dataset 
Penelitian diawali dengan proses pengumpulan data menggunakan dataset publik yang 
dirancang khusus untuk skenario ruang publik dengan tingkat kepadatan kerumunan yang 
tinggi, yaitu MOT20 dan DanceTrack. Kedua dataset tersebut banyak digunakan dalam 
penelitian pelacakan multi-objek karena mampu merepresentasikan kondisi kerumunan 
yang kompleks. Dataset yang diperoleh kemudian dibagi menjadi tiga bagian utama, yaitu 
Train (data latih), Test (data uji), dan Validation (data validasi). Pembagian ini bertujuan 
untuk memastikan proses pelatihan model dapat dilakukan secara optimal sekaligus 
menjaga objektivitas evaluasi model, sehingga risiko terjadinya overfitting dapat 
diminimalkan. 
2. Tahap 1: Preprocessing & Augmentasi Data 
Sebelum dimasukkan ke dalam model, data mentah harus melalui tahap prapemrosesan 
agar sesuai dengan standar arsitektur algoritma. 
a. Augmentasi Domain 
Diterapkan untuk merepresentasikan kondisi dunia nyata, termasuk penambahan oklusi 
sintetis (objek yang saling menutupi) dan noise visual. 
b. Standarisasi & Anotasi 
Proses penyesuaian format bounding box menggunakan standar YOLO, difokuskan 
secara eksklusif pada kelas biner orang/pejalan kaki. 
c. Penyesuaian Dimensi & Skala 
Meliputi rescaling image (1./255), pengubahan ukuran citra (resize) menjadi 640 pixel 
untuk keseimbangan akurasi dan kecepatan komputasi, serta penetapan batch size ke 
angka 64. 
3. Pengembangan Model Deteksi Utama 
Tahap ini merupakan inti dari pengenalan objek, yang mengandalkan arsitektur 
mutakhir: 
a. Ekstraksi Fitur 
Formatted: Font: Italic
Formatted: Font: Italic


## Page 7

Memanfaatkan Backbone YOLO26 untuk mengekstraksi fitur spasial secara 
mendalam. 
b. Arsitektur Deteksi 
Menggunakan pendekatan NMS-Free End-to-End yang mengeliminasi proses Non-
Maximum Suppression, sehingga memangkas latensi latensi komputasi secara drastis. 
c. Penugasan Label 
Mengimplementasikan fitur Small-Target-Aware (STAL) agar sistem tetap sensitif 
dalam mendeteksi objek manusia berukuran kecil dari tangkapan kamera jarak jauh. 
4. Sistem Pelacakan Multi-Objek (Adaptive Tracking) 
Untuk mengatasi hilangnya identitas objek saat terjadi pergerakan tumpang tindih, 
sistem pelacakan dibagi berdasarkan kapasitas hardware yang digunakan untuk inferensi: 
a. Skenario Server (Hardware Tinggi) 
Menggunakan Tracker Utama DiffMOT yang berbasis generative diffusion untuk 
memprediksi lintasan objek yang tidak linier (non-linear) di kerumunan ekstrem. 
b. Skenario Edge (Hardware Terbatas) 
Jika dideploy pada perangkat dengan komputasi rendah, sistem secara adaptif akan 
menggunakan Tracker Cadangan OC-SORT yang tangguh dalam pemulihan identitas 
saat terjadi oklusi ringan. 
5. Tahap 2: Modul Penghitungan (Counting) 
Setelah objek berhasil dideteksi dan dilacak oleh tracker, aliran data masuk ke tahap 
kalkulasi yang mengimplementasikan logika penghitungan lanjutan: 
a. Kalkulasi Pejalan Kaki Berbasis Spasial-Temporal 
Sistem meninggalkan mekanisme virtual line crossing konvensional dan beralih 
menggunakan Zone-to-Zone Trajectory Analysis untuk memvalidasi arah lintasan 
objek secara utuh. Objek hanya akan dihitung jika transisi pergerakannya terkonfirmasi 
valid melewati zona deteksi aktif non-linear yang telah dipetakan menggunakan Region 
of Interest (RoI) Polygon, sehingga secara efektif mengeliminasi anomali pergerakan 
seperti orang yang hanya mondar-mandir (loitering). 
b. Pemeliharaan Identitas dengan ID State Memory 
Untuk menyelesaikan masalah tumpang tindih ekstrem dan pergantian identitas tak 
terduga, sistem mengimplementasikan ID State Memory. Fitur ini beroperasi dengan 
melakukan penguncian identitas (ID locking) pada objek yang telah divalidasi, 
sehingga secara absolut mencegah terjadinya perhitungan ganda (double-counting) 
meskipun objek tersebut terhalang (oklusi) sesaat dan muncul kembali di dalam frame.. 
c. Update Kapasitas Real-Time 
Mengonversi data lintasan valid menjadi luaran pembaruan kapasitas demografis ruang 
publik secara instan. Hasil kalkulasi ini menjadi basis data presisi yang krusial untuk 
mendukung sistem peringatan dini kapasitas dan manajemen kerumunan cerdas (Smart 
Crowd Management). 
6. Tahap 3: Evaluasi & Validasi Model 
Tahap akhir difokuskan pada pengujian performa sistem secara menyeluruh. Evaluasi 
kuantitatif dilakukan menggunakan metrik pelacakan standar global seperti HOTA (Higher 
Order Tracking Accuracy), MOTA (Multi-Object Tracking Accuracy), IDF1 (konsistensi 
ID), dan FPS (Frames Per Second untuk mengukur kecepatan real-time). Terakhir, validasi 
praktis dilakukan melalui pengujian skenario nyata pada rekaman Closed-Circuit 
Television (CCTV) dinamis di fasilitas publik. 
 
 
F. HASIL YANG DIHARAPKAN  
Jelaskan hasil yang diharapkan dan luaran yang dijanjikan dari penelitian 
 
Formatted: Indent: Left:  1,52 cm, First line:  0,59 cm,
Right:  0,24 cm


## Page 8

Temuan utama yang ditargetkan dari penelitian ini adalah terciptanya sebuah prototype sistem 
berbasis computer vision yang mampu melakukan deteksi, pelacakan, dan penghitungan jumlah 
manusia secara otomatis serta real-time dari aliran video pengawasan (CCTV). Model yang 
dikembangkan mengintegrasikan arsitektur YOLO26 sebagai detektor objek real-time dengan 
algoritma pelacakan multi-objek DiffMOT untuk memprediksi lintasan objek dengan pola pergerakan 
non-linear pada kerumunan yang kompleks. Untuk meningkatkan ketahanan sistem terhadap 
gangguan deteksi dan keterbatasan perangkat keras, penelitian ini juga akan mengimplementasikan 
algoritma pelacakan alternatif OC-SORT yang lebih efisien pada perangkat edge. Evaluasi model 
dilakukan menggunakan dataset publik seperti MOT20 dan DanceTrack dengan metrik standar 
pelacakan seperti HOTA, MOTA, IDF1, serta kecepatan pemrosesan (FPS) untuk memastikan 
kemampuan sistem bekerja secara real-time. 
 
Penelitian ini menargetkan luaran berupa publikasi artikel ilmiah pada jurnal internasional bereputasi 
yang terindeks Scopus serta pendaftaran hak cipta program komputer dari sistem real-time people 
counting yang dikembangkan. Luaran tersebut diharapkan dapat memberikan kontribusi terhadap 
pengembangan teknologi smart city dan crowd management, khususnya dalam mendukung sistem 
pemantauan kapasitas ruang publik yang lebih efisien, adaptif, dan berbasis data secara real-time. 
 
 
G. JADWAL PENELITIAN 
Jadwal penelitian disusun berdasarkan pelaksanaan penelitian, harap disesuaikan berdasarkan  
lama tahun pelaksanaan penelitian 
 
No 
Nama Kegiatan 
Bulan 
1 
2 
3 
4 
5 
6 
7 
8 
9 
10 11 12 
1 
Identifikasi Masalah / Prospek 
 
 
 
 
 
 
 
 
 
 
 
 
2 
Melakukan Explorasi & Review 
Literatur / Jurnal 
 
 
 
 
 
 
 
 
 
 
 
 
3 
Kajian Teori dan Survei Pendekatan 
Engineering 
 
 
 
  
 
 
 
 
 
 
 
 
4 
Persoalan Fundamental & Asumsi 
Domain Riset 
 
 
 
 
 
 
 
 
 
 
 
 
5 
Pembuatan dan Pengusulan Proposal 
Penelitian 
 
 
 
 
 
 
 
 
 
 
 
 
6 
Representasi Pola Visi Komputer 
 
 
 
 
 
 
 
 
 
 
 
 
7 
Karakterisasi Struktur Pola Desain 
 
 
 
 
 
 
 
 
 
 
 
 
8 
Perencanaan Meta Model Design 
Pattern 
 
 
 
 
 
 
 
 
 
 
 
 
9 
Pengembangan Model Pengenalan 
berbasis Vision 
 
 
 
 
 
 
 
 
 
 
 
 
10 Pembuatan Laporan Penelitian 
 
 
 
 
 
 
 
 
 
 
 
 
11 Pembuatan Artikel Jurnal Internasional 
Bereputasi 
 
 
 
 
 
 
 
 
 
 
 
 
 
H. DAFTAR PUSTAKA 
Sitasi disusun dan ditulis berdasarkan sistem nomor sesuai dengan urutan pengutipan, mengikuti 
format IEEE. Hanya pustaka yang disitasi, yang dicantumkan dalam Daftar Pustaka. Sumber 
pustaka atau rujukan minimal 15 referensi yang terbit dalam 10 tahun terakhir. 
 
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic
Formatted: Font: Italic


## Page 9

[1] 
G. Yigit, “Crowd Detection: Leveraging YOLO for Human Recognition,” Turkish Journal of 
Engineering, vol. 9, no. 3, pp. 571–577, 2025.G. Yigit, “Crowd Detection : Leveraging 
YOLO for Human Recognition,” vol. 9, no. 3, pp. 571–577, 2025. 
[2] 
H. F. Elsepae, H. M. El-hoseny, and E. K. I. Hamad, “Deep learning for crowd counting in 
complex environments : challenges and novel trends,” 2026. 
[3] 
Q. M. B. aljelawy, E. K. Hanoun, and G. M. Ali, “Real-time People Counting with Deep 
Learning: A Solution for Crowd Management,” Al-Mansour Journal, Issue 42, pp. 1–8, 
2025.G. M. Ali, “Real-time People Counting with Deep Learning : A Solution for Crowd 
Management,” vol. 42, pp. 1–8. 
[4] 
Y. Chen, F. Meng, and Z. Chen, “OcclusionTrack : Multi-Object Tracking in Dense Scenes,” 
no. 2, pp. 1–22, 2025. 
[5] 
P. Dendorfer, et al., “MOT20: A benchmark for multi object tracking in crowded scenes,” 
arXiv preprint arXiv:2003.09003, 2020.P. Dendorfer et al., “MOT20 : A benchmark for 
multi object tracking in crowded scenes,” pp. 1–7. 
[6] 
J. Cao, J. Pang, X. Weng, R. Khirodkar, and K. Kitani, “Observation-Centric SORT: 
Rethinking SORT for Robust Multi-Object Tracking,” Proceedings of the IEEE/CVF 
Conference on Computer Vision and Pattern Recognition (CVPR), pp. 9686–9696, 2023.J. 
Cao, J. Pang, X. Weng, R. Khirodkar, and K. Kitani, “Observation-Centric SORT: 
Rethinking SORT for Robust Multi-Object Tracking”. 
[7] 
S. Chakrabarty, “YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time 
Object Detection,” Ultralytics Technical Report, 2026.F. R. For, R. E. A. L. Ime, O. B. D. 
Etection, and S. Chakrabarty, “YOLO26 : A N A NALYSIS OF NMS-F REE E ND TO E 
ND,” 2026. 
[8] 
P. Sun, et al., “DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse 
Motion,” Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern 
Recognition (CVPR), pp. 20993–21002, 2022.P. Sun et al., “DanceTrack : Multi-Object 
Tracking in Uniform Appearance and Diverse Motion,” pp. 20993–21002. 
[9] 
I. Hoeronis, A. Neky, F. Tsani, and R. Naifisurya, “FINDER : Fish Detection and Tracking 
with Enhanced YOLOv11 for Real-Time Counting,” vol. 7, no. 1, pp. 1–19, 2022. 
[10] W. Lv, Y. Huang, N. Zhang, R. S. Lin, M. Han, and D. Zeng, “DiffMOT: A Real-time 
Diffusion-based Multiple Object Tracker with Non-linear Prediction,” Proceedings of the 
IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 19321–
19330, 2024.W. Lv, Y. Huang, N. Zhang, R. L. Mei, and H. Dan, “DiffMOT : A Real-time 
Diffusion-based Multiple Object Tracker with Non-linear Prediction,” pp. 19321–19330. 
[11] B. Pardamean, F. Abid, T. W. Cenggoro, N. Elwirehardja, and H. H. Muljo, “Counting 
people inside a region-of-interest in CCTV footage with deep learning,” pp. 1–21, 2022, doi: 
10.7717/peerj-cs.1067. 
[12] AA. Susanto, “RHC: A Dataset for In-Room and Out-Room Human Counting,” Procedia 
Computer Science, vol. 179, pp. 33–39, 2021, doi: 10.1016/j.procs.2020.12.005.. Susanto, 
“ScienceDirect RHC : A Dataset for In-Room and Out-Room Human Counting RHC : A 
Dataset for In-Room and Out-Room Human Counting,” Procedia Comput. Sci., vol. 179, no. 
Formatted: Space Before:  14 pt, After:  8 pt, Line
spacing:  single


## Page 10

2019, pp. 33–39, 2021, doi: 10.1016/j.procs.2020.12.005. 
[13] P. Somaldo and D. Chahyati, “Comparison of FairMOT-VGG16 and MCMOT 
Implementation for Multi-Object Tracking and Gender Detection on Mall CCTV,” vol. 1, pp. 
49–64, 2021. 
[14] J. Luiten, A. Osep, P. Dendorfer, P. Torr, A. Geiger, L. Leal-Taixé, and B. Leibe, “HOTA: A 
Higher Order Metric for Evaluating Multi-Object Tracking,” International Journal of 
Computer Vision (IJCV), vol. 129, no. 2, pp. 548–578, 2021.J. L. Aljo, D. Philip, T. Andreas, 
L. L. B. Leibe, and A. M. Tracking, “HOTA : A Higher Order Metric for Evaluating Multi-
Object Tracking,” no. August, 2020. 
[15] E. Ristani, F. Solera, R. Zou, R. Cucchiara, and C. Tomasi, “Performance Measures and a 
Data Set for Multi-Target, Multi-Camera Tracking,” European Conference on Computer 
Vision (ECCV), pp. 17–35, 2016.M. Tracking, E. Ristani, F. Solera, R. Zou, R. Cucchiara, 
and C. Tomasi, “Performance Measures and a Data Set for,” vol. 1, no. c. 
[16] J. Alikhanov, D. Obidov, M. Abdurasulov, and H. Kim, “Practical Evaluation Framework for 
Real-Time Multi-Object Tracking : Achieving Optimal and Realistic Performance,” IEEE 
Access, vol. 13, no. February, pp. 34768–34788, 2025, doi: 10.1109/ACCESS.2025.3541177. 
[17] G. Pahl, W. Beitz, J. Feldhusen, and K.-H. Grote, Engineering Design: A Systematic 
Approach. Springer London. doi: 10.1007/978-1-84628-319-2.K.-H. G. Gerhard Pahl, 
Wolfgang Beitz, Jörg Feldhusen, Engineering Design: A Systematic Approach. Springer 
London. doi: https://doi.org/10.1007/978-1-84628-319-2. 
 
 G. Yigit, CCrowd Detection: Leveraging YOLO for Human Recognition,C Turkish Journal of 
Engineering, vol. 9, no. 3, pp. 571–577, 2025. 
[2] 
H. F. Elsepae, H. M. El-hoseny, and E. K. I. Hamad, “Deep learning for crowd counting in 
complex environments : challenges and novel trends,” 2026. 
[3] 
Q. MB aljelawy, E. K. Hanoun, and G. M. Ali, CReal-time People Counting with Deep 
Learning: A Solution for Crowd Management,C Al-Mansour Journal, Issue 42, pp. 1-8, 2025. 
[4] 
Y. Chen, F. Meng, and Z. Chen, “OcclusionTrack : Multi-Object Tracking in Dense Scenes,” 
no. 2, pp. 1–22, 2025. 
[5] 
P. Dendorfer, et al., CMOT20: A benchmark for multi object tracking in crowded scenes,C 
arXiv preprint arXiv:2003.09003, 2020. 
[6] 
J. Cao, et al., CObservation-Centric SORT: Rethinking SORT for Robust Multi-Object 
Tracking,C CVPR, 2023. 
[8] 
S. Chakrabarty, CYOLO26: An Analysis of NMS-Free End to End Framework for Real-Time 
Object DetectionC, 2026. 
[9] 
P. Sun et al., “DanceTrack : Multi-Object Tracking in Uniform Appearance and Diverse 
Motion,” CVPR, pp. 20993–21002, 2022. 
Formatted: Justified, Indent: Left:  0 cm, First line:  0 cm


## Page 11

[10] 
I. Hoeronis, A. Neky, F. Tsani, and R. Naifisurya, “FINDER : Fish Detection and Tracking 
with Enhanced YOLOv11 for Real-Time Counting,” vol. 7, no. 1, pp. 1–19, 2022. 
[11] 
W. Lv, et al., CDiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-
linear Prediction,C CVPR, pp. 19321-19330, 2024. 
[12] 
B. Pardamean, F. Abid, T. W. Cenggoro, N. Elwirehardja, and H. H. Muljo, “Counting people 
inside a region-of-interest in CCTV footage with deep learning,” pp. 1–21, 2022, doi: 10.7717/peerj-
cs.1067. 
[13] 
A. Susanto, CRHC: A Dataset for In-Room and Out-Room Human Counting,C Procedia 
Comput. Sci., vol. 179, pp. 33–39, 2021. 
[14] 
P. Somaldo and D. Chahyati, “Comparison of FairMOT-VGG16 and MCMOT 
Implementation for Multi-Object Tracking and Gender Detection on Mall CCTV,” vol. 1, pp. 49–64, 
2021. 
[15] 
K.-H. G. Gerhard Pahl, Wolfgang Beitz, Jörg Feldhusen, Engineering Design: A Systematic 
Approach. Springer London. doi: https://doi.org/10.1007/978-1-84628-319-2.
