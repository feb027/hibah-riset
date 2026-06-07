# TARGET PROGRESS SELASA — ARSITEKTUR SISTEM, DATA EKSPERIMEN, DAN TAHAPAN PENGEMBANGAN

Dokumen ini disusun sebagai bahan tambahan untuk target progress Selasa. Fokusnya adalah menjawab tiga permintaan utama: deskripsi arsitektur sistem yang diusulkan, data eksperimen yang digunakan beserta statistik dan *preprocessing*, serta tahapan pengembangan atau eksperimen. Bagian ini masih berada pada tahap rancangan metodologi, sehingga tidak menyajikan klaim hasil eksperimen numerik yang belum dijalankan.

## 1. Deskripsi Arsitektur Sistem yang Diusulkan

Penelitian ini mengusulkan arsitektur *real-time people counting* berbasis video dengan pendekatan *detection-tracking-counting*. Pendekatan ini dipilih karena kebutuhan menghitung orang pada ruang publik tidak cukup diselesaikan dengan deteksi manusia pada tiap frame. Sistem perlu mempertahankan identitas objek antar-frame, membaca arah lintasan, lalu memutuskan kapan sebuah lintasan layak dihitung sebagai event masuk atau keluar. Diaz-Santos dkk. (2025 – S010) memperlihatkan bahwa analisis arus penumpang berbasis video dapat dibangun dari integrasi deteksi, tracking, dan counting pada perangkat tepi. Nurseitov dkk. (2026 – S011) juga menunjukkan bahwa sistem *people counting* untuk lingkungan urban perlu menggabungkan deteksi, pelacakan, dan pencatatan event agar keluaran tidak hanya berupa jumlah objek sesaat.

Arsitektur sistem terdiri atas enam komponen utama, yaitu input video, *preprocessing*, deteksi manusia, pelacakan multi-objek, *counting logic*, serta keluaran dan evaluasi. Gambar 1 merangkum alur sistem dari video masukan sampai keluaran hitungan dan log evaluasi.

[Sisipkan Gambar 1 di sini: `docs/diagrams/revisi-no3-architecture.png`]

**Gambar 1. Arsitektur sistem *real-time people counting* yang diusulkan.**

Pada tahap input, sistem menerima video dari CCTV atau rekaman ruang publik dengan sudut kamera tetap. Video kemudian dipecah menjadi frame berurutan. Pada tahap *preprocessing*, frame disiapkan agar konsisten untuk deteksi dan tracking. Proses ini mencakup penyesuaian resolusi, *frame sampling*, penetapan RoI, pembuatan garis virtual, dan penentuan zona asal-tujuan. RoI dan garis virtual diperlukan karena target penelitian bukan hanya mendeteksi manusia, tetapi menghitung event lintasan berdasarkan area yang relevan.

Tahap deteksi manusia menggunakan detector real-time sebagai penghasil *bounding box* dan *confidence score*. YOLO26 diposisikan sebagai salah satu kandidat implementasi terbaru karena Chakrabarty (2026 – S001) membahas pergeseran YOLO26 menuju kerangka NMS-free dan end-to-end untuk mengurangi ketergantungan pada *post-processing* NMS. Namun, YOLO26 tidak dijadikan satu-satunya dasar akademik karena sumber tersebut masih berupa preprint analitis dan dokumentasi teknis. Dasar akademik untuk arah NMS-free/end-to-end diperkuat oleh YOLOv10 dari Wang dkk. (2024 – S003), yang menekankan deteksi real-time end-to-end, serta RT-DETR dari Zhao dkk. (2024 – S004), yang menunjukkan bahwa detector end-to-end berbasis transformer dapat bersaing pada kebutuhan real-time.

Output detector diteruskan ke modul *multi-object tracking* (MOT). DiffMOT dirancang sebagai tracker utama karena Lv dkk. (2024 – S021) mengusulkan prediksi gerak non-linear berbasis difusi dan melaporkan kemampuan real-time pada konteks MOT. Komponen ini relevan untuk skenario ruang publik yang memiliki oklusi, perubahan arah, dan lintasan saling berdekatan. OC-SORT digunakan sebagai baseline sekaligus *fallback* efisien karena Cao dkk. (2023 – S024) menunjukkan bahwa pendekatan *observation-centric* dapat memperbaiki akumulasi error saat oklusi dan tetap berjalan ringan. Kombinasi DiffMOT dan OC-SORT memungkinkan penelitian membandingkan jalur yang lebih robust terhadap gerak non-linear dengan jalur yang lebih ringan secara komputasi.

Tahap berikutnya adalah *counting logic*. Modul ini tidak menghitung jumlah *bounding box* per frame secara langsung. Sistem hanya mencatat event ketika lintasan objek memenuhi syarat arah, melewati garis atau batas RoI, dan belum pernah dihitung pada transisi yang sama. Dokumentasi NVIDIA DeepStream (2026 – S035) menunjukkan bahwa analitik berbasis RoI, direction detection, dan line crossing membutuhkan tracker ID karena riwayat posisi diperlukan untuk menentukan arah dan crossing. Rujukan ini digunakan sebagai bukti teknis implementasi, sedangkan bukti akademik kebutuhan deteksi-tracking-counting tetap ditopang oleh Diaz-Santos dkk. (2025 – S010) dan Nurseitov dkk. (2026 – S011).

Formalisme sederhana untuk modul counting dinyatakan sebagai berikut. Setiap lintasan objek ke-`i` direpresentasikan sebagai `T_i = {(b_t, z_t, s_t)}`, dengan `b_t` sebagai *bounding box* pada frame ke-`t`, `z_t` sebagai status zona atau RoI, dan `s_t` sebagai status ID dalam memori. Event counting dinyatakan valid jika `T_i` mengalami transisi zona sesuai arah yang ditentukan, melewati garis atau batas RoI, serta `s_t` belum berada pada status `counted` atau `cooldown`. Setelah event tersimpan, status track masuk ke `counted` lalu `cooldown` agar objek yang sama tidak dihitung berulang saat bergerak di sekitar garis.

Secara prosedural, logika tersebut dapat ditulis sebagai algoritma berikut.

```text
Algoritma 1. Validasi event counting berbasis ID state memory
Input  : frame video, hasil deteksi manusia, hasil tracking ID, RoI, garis virtual, zona arah
Output : event log masuk-keluar dan jumlah per zona

1. Untuk setiap frame t:
2.   Jalankan detector untuk memperoleh bounding box manusia.
3.   Kirim bounding box ke tracker untuk memperoleh track ID.
4.   Untuk setiap track T_i:
5.      Hitung posisi objek terhadap RoI, garis virtual, dan zona.
6.      Perbarui status s_t pada ID state memory.
7.      Jika track berpindah zona sesuai arah dan melewati garis virtual:
8.          Jika status track bukan counted dan bukan cooldown:
9.              Catat event masuk/keluar ke event log.
10.             Ubah status track menjadi counted lalu cooldown.
11.     Jika track hilang sementara:
12.         Simpan status lost track selama masih dalam batas buffer.
13.     Jika track pulih dengan lintasan yang konsisten:
14.         Lanjutkan status track sebelumnya.
15.     Jika track hilang terlalu lama:
16.         Ubah status menjadi expired.
17. Kembalikan jumlah event, log ID, dan metrik evaluasi.
```

Formalisme tersebut tidak dimaksudkan sebagai teorema matematis baru. Fungsinya adalah memperjelas aturan keputusan agar penelitian dapat membedakan kesalahan yang berasal dari detector, tracker, RoI, atau state memory. Dengan demikian, kontribusi arsitektur berada pada integrasi komponen dan mekanisme validasi event, bukan klaim bahwa detector atau tracker yang digunakan selalu lebih unggul dari semua metode lain.

## 2. Data Eksperimen dan Data yang Digunakan

Data eksperimen dirancang sebagai kombinasi dataset standar komunitas dan video target. Dataset standar digunakan agar komponen deteksi dan tracking dapat diuji pada benchmark yang dikenal komunitas computer vision. Video target tetap diperlukan karena dataset deteksi atau tracking tidak selalu menyediakan label event masuk-keluar berbasis RoI atau garis virtual. Pemisahan ini penting agar penelitian tidak menyamakan benchmark deteksi/tracking dengan validasi end-to-end people counting.

**Tabel 1. Rencana data eksperimen dan fungsi tiap data**

| Data | Statistik dan karakteristik | Penggunaan dalam eksperimen | Bukti sumber |
|---|---|---|---|
| CrowdHuman | Dataset deteksi manusia pada kondisi kerumunan dan oklusi. Shao dkk. (2018 – S038) melaporkan sekitar 470 ribu instance manusia dari subset train dan validation, dengan rata-rata sekitar 22,6 orang per gambar. Teks penuh S038 juga mencatat split training 15.000 citra, 339.565 anotasi person, 99.227 ignore region, dan rata-rata 22,64 person per citra. | Menguji kemampuan detector manusia pada kondisi crowded, partial body, dan oklusi. Data ini tidak digunakan langsung untuk event counting karena berupa citra dan tidak memiliki lintasan temporal. | Shao dkk. (2018 – S038). |
| MOT20 | Benchmark MOT untuk skenario sangat padat. Dendorfer dkk. (2020 – S036) menjelaskan MOT20 sebagai benchmark 8 sequence dari 3 scene dengan kepadatan yang dapat mencapai 246 pedestrian per frame. Tabel statistik S036 mencatat 4 sequence training dan 4 sequence testing; data training berisi 8.931 frame, 2.215 track, dan 1.134.614 bounding box. | Menguji kualitas tracking pada crowd, ID switch, fragmentasi lintasan, dan robustness tracker. MOT20 dipakai untuk stress test tracker, bukan sebagai pengganti video counting lokal. | Dendorfer dkk. (2020 – S036). |
| DanceTrack | Dataset MOT dengan 100 video, 40 video training, 25 video validation, 35 video testing, 990 instance unik, 105.855 frame, dan sekitar 877 ribu bounding box. Sun dkk. (2022 – S037) menekankan bahwa DanceTrack memiliki penampilan objek yang relatif seragam dan gerak yang beragam. | Menguji tracker pada kondisi asosiasi identitas yang sulit, khususnya saat appearance cue tidak cukup membedakan objek. Domainnya tidak sama dengan CCTV ruang publik, sehingga digunakan sebagai stress test gerak dan asosiasi, bukan sebagai bukti domain akhir. | Sun dkk. (2022 – S037). |
| Video target ruang publik | Rekaman CCTV atau video publik dengan kamera tetap. Statistik yang wajib dicatat setelah data diperoleh meliputi jumlah video, durasi, FPS, resolusi, jumlah event manual, tingkat kepadatan, kondisi pencahayaan, bentuk RoI, dan arah garis virtual. | Validasi end-to-end untuk counting logic, direction accuracy, over-count, under-count, dan latency pipeline. Data ini menjadi bagian terpenting untuk menilai apakah sistem benar-benar sesuai dengan kebutuhan aplikasi ruang publik. | Diaz-Santos dkk. (2025 – S010) dan Nurseitov dkk. (2026 – S011) digunakan sebagai rujukan desain sistem video counting. |

CrowdHuman digunakan karena masalah deteksi manusia pada kerumunan masih kuat dipengaruhi oklusi dan tubuh yang terlihat sebagian. Shao dkk. (2018 – S038) secara eksplisit merancang dataset tersebut untuk mengevaluasi deteksi manusia di lingkungan crowded. Oleh karena itu, CrowdHuman sesuai untuk menguji detector, tetapi tidak boleh digunakan untuk menyimpulkan akurasi counting event.

MOT20 digunakan karena penelitian ini membutuhkan pengujian tracker pada kepadatan tinggi. Dendorfer dkk. (2020 – S036) menjelaskan MOT20 sebagai benchmark untuk tracking pada scene sangat padat, termasuk situasi indoor, outdoor, siang, dan malam. Data ini cocok untuk membaca ID switch dan fragmentasi track, tetapi belum cukup untuk menguji aturan masuk-keluar berbasis garis virtual.

DanceTrack digunakan untuk menguji ketahanan tracker saat penampilan objek mirip dan geraknya beragam. Sun dkk. (2022 – S037) menunjukkan bahwa banyak tracker mengalami penurunan performa pada DanceTrack karena bottleneck utamanya berada pada asosiasi identitas, bukan hanya deteksi. Hal ini relevan dengan people counting karena kesalahan ID dapat menyebabkan double-counting atau missed-counting.

Video target ruang publik tetap wajib disiapkan karena validasi counting membutuhkan ground truth event. Pada video target, anotasi tidak cukup berupa bounding box; anotasi perlu mencatat event masuk, event keluar, arah crossing, ID orang jika memungkinkan, timestamp, dan zona. Tanpa ground truth event manual, hasil sistem hanya dapat dievaluasi sebagai deteksi atau tracking, belum sebagai people counting end-to-end.

## 3. Preprocessing Data

Preprocessing dilakukan berbeda sesuai fungsi data. Pada CrowdHuman, preprocessing diarahkan pada penyelarasan format anotasi, pemilihan kategori manusia, normalisasi resolusi, serta konversi label ke format yang kompatibel dengan detector. Karena CrowdHuman berisi citra, unit evaluasinya adalah gambar atau batch gambar, bukan video temporal.

Pada MOT20 dan DanceTrack, preprocessing harus menjaga urutan frame dan track ID. File anotasi tidak boleh diperlakukan seperti data deteksi biasa karena evaluasi tracking membutuhkan identitas objek yang konsisten antar-frame. Untuk eksperimen tracker, preprocessing mencakup penyesuaian struktur folder sequence, konversi format anotasi jika diperlukan, dan verifikasi bahwa frame rate serta urutan frame tidak berubah.

Pada video target, preprocessing lebih kompleks karena data harus mendukung counting event. Langkah yang diperlukan meliputi pemotongan scene yang relevan, penetapan RoI polygon, penentuan garis virtual, definisi arah masuk-keluar, anotasi event manual, dan pencatatan kondisi scene. Jika video memuat wajah atau informasi personal, akses data perlu dibatasi dan identitas personal tidak boleh menjadi bagian dari keluaran penelitian. Fokus penelitian adalah jumlah dan lintasan agregat, bukan identifikasi individu.

Tabel 2 merangkum preprocessing yang direncanakan.

**Tabel 2. Rencana preprocessing data**

| Jenis data | Preprocessing utama | Keluaran preprocessing | Risiko yang harus dikontrol |
|---|---|---|---|
| Data deteksi | Resize, normalisasi, konversi anotasi, pemilihan kategori person. | Dataset siap untuk training atau evaluasi detector. | Label tidak konsisten, ignore region terabaikan, objek kecil/teroklusi tidak terwakili. |
| Data tracking | Penjagaan urutan frame, validasi track ID, konversi format MOT, pengecekan FPS. | Sequence siap untuk evaluasi HOTA, IDF1, MOTA, ID switch, dan fragmentasi. | Frame teracak, ID rusak, hasil metrik tidak sah. |
| Video target | Pemilihan scene, RoI polygon, garis virtual, zona arah, anotasi event manual, catatan kondisi video. | Ground truth event counting dan konfigurasi counting logic. | Jumlah event terlalu sedikit, anotasi tidak konsisten, privasi tidak dikontrol. |

## 4. Deskripsi Tahapan Pengembangan atau Eksperimen

Tahapan pengembangan disusun agar setiap komponen diuji sebelum digabungkan menjadi pipeline utuh. Gambar 2 memperlihatkan bagan alir tahapan eksperimen dari rancangan sampai evaluasi.

[Sisipkan Gambar 2 di sini: `docs/diagrams/revisi-no3-research-workflow.png`]

**Gambar 2. Tahapan pengembangan dan evaluasi sistem.**

Tahap pertama adalah perumusan rancangan eksperimen. Pada tahap ini ditentukan tujuan, objek studi, variabel, data, baseline, serta metrik evaluasi. Tujuannya adalah memastikan eksperimen tidak berubah menjadi sekadar mencoba beberapa model tanpa pertanyaan evaluasi yang jelas. Variabel yang dicatat mencakup model detector, tracker, resolusi, FPS sampling, threshold, konfigurasi RoI, panjang buffer track, dan aturan cooldown.

Tahap kedua adalah persiapan data. Dataset publik disiapkan untuk evaluasi komponen, sedangkan video target disiapkan untuk validasi end-to-end. CrowdHuman mendukung evaluasi detector pada oklusi dan kerumunan karena Shao dkk. (2018 – S038) menargetkan human detection pada crowd. MOT20 mendukung evaluasi tracker pada kepadatan tinggi karena Dendorfer dkk. (2020 – S036) merancang benchmark tersebut untuk scene crowded. DanceTrack mendukung evaluasi asosiasi identitas pada gerak kompleks karena Sun dkk. (2022 – S037) merancang dataset dengan appearance yang mirip dan motion yang beragam.

Tahap ketiga adalah penyusunan pipeline model. Detector menghasilkan bounding box manusia pada setiap frame. Tracker mempertahankan ID antar-frame. Counting logic mengevaluasi lintasan terhadap RoI, garis virtual, zona, dan ID state memory. Pada tahap ini, YOLO26 hanya ditempatkan sebagai kandidat implementasi, sedangkan YOLOv10 dan RT-DETR menjadi rujukan akademik untuk detector end-to-end real-time. Wang dkk. (2024 – S003) menjadi dasar untuk arah YOLO end-to-end, sedangkan Zhao dkk. (2024 – S004) menjadi dasar untuk alternatif detector real-time berbasis transformer.

Tahap keempat adalah pengujian skenario. Skenario S1 menguji detector menggunakan CrowdHuman dan subset video target jika tersedia. Skenario S2 menguji tracker menggunakan MOT20 dan DanceTrack. Skenario S3 menguji counting logic menggunakan video target yang telah diberi anotasi event manual. Skenario S4 menguji pipeline end-to-end dengan menghitung FPS, latency, akurasi event, dan sumber error.

Tahap kelima adalah evaluasi dan analisis error. Deteksi dievaluasi menggunakan mAP, precision, recall, false positive, false negative, dan latency detector. Tracking dievaluasi menggunakan HOTA, IDF1, MOTA, ID switch, dan fragmentasi. Luiten dkk. (2021 – S025) menjelaskan HOTA sebagai metrik yang menyeimbangkan aspek deteksi, asosiasi, dan lokalisasi dalam evaluasi MOT. Ristani dkk. (2016 – S026) digunakan sebagai dasar untuk evaluasi identitas seperti IDF1 pada multi-target tracking. Counting dievaluasi menggunakan MAE, MAPE bila jumlah event cukup besar, over-count, under-count, direction accuracy, dan absolute counting error.

Tahap keenam adalah analisis validitas. Ancaman validitas internal muncul dari perubahan threshold, resolusi, FPS sampling, parameter tracker, dan aturan cooldown. Ancaman validitas konstruk muncul karena mAP, HOTA, IDF1, FPS, dan counting error mengukur aspek berbeda. Ancaman validitas eksternal muncul karena dataset publik tidak sepenuhnya sama dengan video target ruang publik. Karena itu, kesimpulan akhir harus memisahkan performa detector, performa tracker, performa counting logic, dan kelayakan runtime.

## 5. Rencana Skenario Eksperimen

**Tabel 3. Skenario eksperimen yang direncanakan**

| Skenario | Fokus | Data | Metrik utama | Tujuan evaluasi |
|---|---|---|---|---|
| S1 — Evaluasi detector | Kualitas deteksi manusia dan latency detector. | CrowdHuman, subset MOT20, dan frame dari video target jika tersedia. | mAP, precision, recall, false positive, false negative, latency. | Menilai apakah detector cukup stabil untuk menjadi input tracker pada kondisi crowded dan oklusi. |
| S2 — Evaluasi tracker | Stabilitas ID dan asosiasi lintasan. | MOT20 dan DanceTrack. | HOTA, IDF1, MOTA, ID switch, fragmentasi, FPS tracker. | Membandingkan DiffMOT sebagai jalur robust dengan OC-SORT sebagai baseline atau fallback ringan. |
| S3 — Evaluasi counting logic | Validasi event masuk-keluar berbasis RoI, line, zone, dan ID memory. | Video target dengan anotasi event manual. | MAE, MAPE, absolute counting error, over-count, under-count, direction accuracy. | Menilai apakah ID state memory mengurangi hitung ganda dan event yang hilang. |
| S4 — Evaluasi end-to-end | Kelayakan pipeline lengkap. | Video target ruang publik. | FPS end-to-end, latency rata-rata/p95, penggunaan CPU/GPU/memori, counting error. | Menilai trade-off antara akurasi counting dan kebutuhan real-time. |

Dalam S1, hasil deteksi yang buruk akan berpengaruh langsung terhadap tracker karena tracker hanya dapat mempertahankan objek yang berhasil dideteksi. Dalam S2, tracker diuji pada kondisi yang menekan asosiasi identitas. DiffMOT relevan untuk gerak non-linear berdasarkan Lv dkk. (2024 – S021), sedangkan OC-SORT relevan sebagai baseline ringan berdasarkan Cao dkk. (2023 – S024). Dalam S3, variasi counting logic dapat dibandingkan, misalnya line crossing sederhana, line crossing dengan RoI, transisi zona, dan transisi zona dengan ID state memory. Dalam S4, sistem diuji sebagai satu pipeline agar bottleneck runtime dan sumber counting error dapat dilihat secara menyeluruh.

## 6. Bukti Sitasi dan Status Sumber

Sumber yang digunakan dipisahkan berdasarkan kekuatan bukti. Sumber akademik utama berasal dari paper peer-reviewed atau benchmark komunitas. Sumber teknis seperti dokumentasi vendor hanya digunakan untuk menjelaskan kemungkinan implementasi, bukan untuk membuktikan novelty akademik.

**Tabel 4. Jejak bukti sitasi untuk bagian ini**

| Kode | Peran dalam dokumen | Status bukti | Alasan digunakan |
|---|---|---|---|
| S001 | Kandidat YOLO26 dan konteks NMS-free terbaru. | Preprint arXiv, bukan peer-reviewed. | Dipakai hati-hati sebagai konteks implementasi YOLO26, bukan anchor utama novelty. |
| S003 | Dasar akademik detector YOLO end-to-end. | NeurIPS 2024. | Menguatkan arah NMS-free/end-to-end detector untuk real-time object detection. |
| S004 | Dasar akademik detector end-to-end berbasis transformer. | CVPR 2024. | Menunjukkan RT-DETR sebagai alternatif real-time tanpa NMS. |
| S010 | Bukti aplikasi passenger-flow counting berbasis YOLO, tracking, dan edge device. | Jurnal Computers 2025. | Relevan untuk arsitektur detection-tracking-counting dan konteks edge. |
| S011 | Bukti people counting dan tracking untuk lingkungan urban. | Journal of Imaging 2026. | Relevan untuk sistem deteksi, tracking, counting, dan event log. |
| S021 | Dasar tracker DiffMOT. | CVPR 2024. | Relevan untuk prediksi gerak non-linear pada MOT. |
| S024 | Dasar OC-SORT sebagai baseline ringan. | CVPR 2023. | Relevan untuk tracking online, oklusi, dan fallback efisien. |
| S025 | Dasar metrik HOTA. | International Journal of Computer Vision 2021. | Relevan karena HOTA menyeimbangkan evaluasi deteksi dan asosiasi. |
| S026 | Dasar evaluasi identitas seperti IDF1. | ECCV Workshop/Springer LNCS 2016. | Relevan untuk evaluasi konsistensi ID pada tracking. |
| S035 | Bukti teknis RoI, direction detection, line crossing. | Dokumentasi NVIDIA DeepStream. | Digunakan hanya untuk menjelaskan implementasi analitik video berbasis tracker ID. |
| S036 | Dataset MOT20. | Benchmark MOTChallenge/arXiv. | Relevan untuk evaluasi dense crowd tracking. |
| S037 | Dataset DanceTrack. | CVPR 2022. | Relevan untuk evaluasi asosiasi identitas pada motion yang beragam. |
| S038 | Dataset CrowdHuman. | Dataset benchmark/arXiv. | Relevan untuk evaluasi deteksi manusia pada crowd dan oklusi. |

Berdasarkan pemeriksaan metadata sumber yang dipakai dalam daftar referensi penelitian, sumber peer-reviewed utama mencakup S003, S004, S021, S024, S025, S026, dan S037 sebagai prosiding atau jurnal bereputasi. S010 dan S011 digunakan sebagai sumber aplikasi terbaru, tetapi tetap perlu dipadukan dengan sumber non-vendor dan benchmark karena keduanya berfokus pada konteks aplikasi tertentu. S001, S002, dan S035 tidak diposisikan sebagai bukti akademik utama karena berupa preprint atau dokumentasi teknis.

## 7. Catatan Batasan yang Perlu Dijaga Saat Dipindahkan ke Draft Paper

Pertama, jangan menyatakan bahwa eksperimen sudah menghasilkan nilai performa tertentu sebelum eksperimen benar-benar dijalankan. Semua metrik dalam dokumen ini masih berupa rencana evaluasi.

Kedua, jangan menyatakan bahwa dataset publik sudah cukup untuk validasi people counting end-to-end. CrowdHuman hanya mendukung deteksi, sedangkan MOT20 dan DanceTrack mendukung tracking. Validasi counting tetap membutuhkan video target dengan ground truth event.

Ketiga, jangan menjadikan YOLO26 sebagai satu-satunya novelty akademik. YOLO26 boleh dipakai sebagai kandidat implementasi, tetapi argumen ilmiah harus tetap ditopang oleh sumber peer-reviewed seperti YOLOv10, RT-DETR, DiffMOT, OC-SORT, HOTA, dan benchmark dataset.

Keempat, jangan menumpuk sitasi di akhir paragraf. Setiap klaim penting perlu ditempelkan pada kalimat yang relevan dengan format penulis, tahun, dan kode sumber.

Kelima, jangan menulis arsitektur seolah-olah seluruh masalah sudah selesai. Bagian ini harus tetap menunjukkan risiko eksperimen, kebutuhan video target, dan rencana analisis error agar terlihat jujur secara akademik.
