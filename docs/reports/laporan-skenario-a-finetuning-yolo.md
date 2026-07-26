# Laporan Skenario A: Fine-Tuning dan Evaluasi Komparatif Empat Arsitektur YOLO pada Dataset CrowdHuman

*Disusun menggunakan standar penulisan akademik untuk justifikasi metodologi eksperimen.*

---

## 1. Pendahuluan

Laporan ini mendokumentasikan pelaksanaan penuh **Skenario A (Evaluasi Detector)** sebagaimana dirancang dalam `docs/drafts/usulan-pendekatan.md` dan dirinci sebagai S1 dalam `docs/drafts/bab3_revisi_skenario_eksperimen.md`. Empat arsitektur YOLO telah di-*fine-tune* pada dataset CrowdHuman menggunakan workstation RTX 4090, kemudian dievaluasi pada tiga dimensi: akurasi deteksi, latensi *post-processing*, dan penskalaan resolusi masukan.

Tujuan skenario ini bukan menentukan "model terbaik" secara umum, melainkan menjawab satu pertanyaan spesifik yang menopang rancangan sistem: **apakah arsitektur *NMS-free* memberikan keuntungan nyata untuk *people counting* di kerumunan padat, dan apakah keuntungan itu cukup besar untuk membenarkan pemilihannya?**

Perlu ditegaskan sejak awal bahwa deteksi bukanlah *counting*. CrowdHuman berupa citra statis tanpa identitas temporal, sehingga hasil laporan ini membatasi diri pada kualitas detektor sebagai lapisan kedua dari pipeline lima lapis. Akurasi hitungan akhir baru dapat dinilai setelah Skenario B (tracker) dan Skenario C (counting logic) diintegrasikan.

---

## 2. Metodologi

### 2.1 Dataset dan Protokol Anotasi

Dataset yang digunakan adalah **CrowdHuman** (Shao et al., 2018) [S038], dengan pembagian standar: ±15.000 citra latih dan **4.370 citra validasi**. Seluruh evaluasi dalam laporan ini dilakukan pada *validation set*, yang memuat **103.115 kotak beranotasi bertag `person`**.

Konversi anotasi dari format `.odgt` ke format YOLO dilakukan dengan keputusan protokol berikut, yang perlu dinyatakan eksplisit karena memengaruhi keterbandingan angka:

1. **Kotak yang dipakai adalah `fbox` (*full-body box*)**, bukan `vbox` (*visible-body*). CrowdHuman menyediakan keduanya; literatur pembanding tidak selalu menggunakan protokol yang sama, sehingga nilai mAP absolut dalam laporan ini **tidak dapat dibandingkan langsung** dengan paper yang memakai *visible-body*.
2. **Anotasi `fbox` bersifat amodal** — digambar sampai bagian tubuh yang tertutup atau berada di luar bingkai. Audit menggunakan `scripts/data_prep/check_label_quality.py` menunjukkan **14,92%** kotak menembus tepi citra. Kotak-kotak ini ditulis apa adanya tanpa pemotongan.
3. **Kotak bertanda `extra.ignore == 1` (3,52%) tetap disertakan sebagai label positif.** Protokol CrowdHuman resmi memperlakukannya sebagai *ignore region*. Konsekuensinya, nilai mAP yang dilaporkan bersifat **pesimistis** dibanding protokol resmi: model dihukum karena gagal mendeteksi objek yang oleh datasetnya sendiri dinyatakan ambigu.
4. **Kotak yang titik tengahnya jatuh di luar bingkai (1,97%)** mengalami distorsi geometri ringan akibat pemotongan per-komponen. Proporsinya kecil dan dampaknya identik pada seluruh model.

Poin 1–4 berlaku **seragam untuk keempat model**. Karena itu, meskipun nilai absolutnya tidak sebanding dengan literatur, **perbandingan antar model dalam laporan ini tetap sah** — inilah yang menjadi objek penelitian.

### 2.2 Konfigurasi Pelatihan

Seluruh model dilatih dengan hyperparameter identik untuk menjamin perbandingan yang setara (*apples-to-apples*):

| Parameter | Nilai |
|---|---|
| Epoch | 100 |
| Batch size | 32 |
| Resolusi masukan | 640 × 640 |
| Optimizer | `auto` (Ultralytics) |
| Seed | 0 |
| AMP (mixed precision) | aktif |
| Kelas | 1 (`person`) |
| Bobot awal | pra-latih COCO |

Kesetaraan konfigurasi ini diverifikasi dari berkas `args.yaml` masing-masing run, bukan diasumsikan.

### 2.3 Perangkat

Pelatihan dan pengukuran latensi dijalankan pada workstation **NVIDIA RTX 4090**. Batasan penting: seluruh pengukuran kecepatan dalam laporan ini berasal dari lingkungan GPU kelas server dengan runtime PyTorch tanpa *export*. Implikasinya dibahas pada Bagian 7.

---

## 3. Hasil Pelatihan

### 3.1 Tabel Utama

| Arsitektur | Sumber | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | Waktu latih |
|---|---|---|---|---|---|---|
| **YOLO26s** | S001/S002 | **0,8480** | **0,7455** | **0,8266** | **0,4974** | 4,89 jam |
| YOLOv10n | S003 | 0,8212 | 0,6892 | 0,7826 | 0,4521 | 5,91 jam |
| YOLO26n | S001/S002 | 0,8230 | 0,6888 | 0,7814 | 0,4497 | 2,27 jam |
| YOLOv11n | — | 0,8352 | 0,6965 | 0,7855 | 0,4463 | 1,94 jam |

*Tabel dibangkitkan otomatis oleh `scripts/experiments/summarize_training_runs.py` untuk menghindari kesalahan salin manual.*

### 3.2 Cara Membaca Metrik Ini

Karena laporan ini akan dibaca lintas latar belakang, berikut arti operasional tiap kolom dalam konteks *people counting*:

- **Precision (0,82–0,85)** — dari setiap 100 kotak yang dilaporkan model sebagai "orang", sekitar 82–85 memang benar orang. Sisanya *false positive*. Dalam sistem hitung, *false positive* yang bertahan beberapa frame dapat memicu **hitungan berlebih (*over-count*)**.
- **Recall (0,69–0,75)** — dari setiap 100 orang yang benar-benar ada, model menemukan 69–75. Sisanya terlewat. Ini penyebab langsung **hitungan kurang (*under-count*)**, dan merupakan metrik paling kritis bagi penelitian ini.
- **mAP@0.5** — rata-rata presisi ketika kotak dianggap benar apabila tumpang tindihnya dengan anotasi mencapai 50%. Ambang yang longgar; mengukur "apakah orangnya ketemu".
- **mAP@0.5:0.95** — rata-rata pada ambang tumpang tindih 50% sampai 95%. Ambang yang ketat; mengukur "apakah kotaknya rapat dan presisi". Metrik ini yang menjadi tolok ukur utama karena kotak yang meleset menyulitkan *tracker* mempertahankan identitas antar-frame.

Perhatikan bahwa **recall lebih rendah daripada precision di semua model**. Ini pola khas deteksi pada kerumunan padat: model cenderung "berhati-hati" dan melewatkan orang yang tertutup, ketimbang mengarang deteksi. Untuk *people counting*, ini berarti kecenderungan sistemik ke arah *under-count*, bukan *over-count* — informasi yang berguna saat merancang kompensasi di lapisan *counting logic*.

### 3.3 Dinamika Konvergensi

Perkembangan mAP@0.5:0.95 sepanjang pelatihan:

| Arsitektur | Epoch 1 | Epoch 10 | Epoch 25 | Epoch 50 | Epoch 75 | Epoch 100 | Capai 99% nilai akhir |
|---|---|---|---|---|---|---|---|
| YOLOv10n | 0,2811 | 0,3847 | 0,4232 | 0,4446 | 0,4510 | 0,4521 | epoch **55** |
| YOLOv11n | 0,3023 | 0,3896 | 0,4247 | 0,4408 | 0,4452 | 0,4463 | epoch **55** |
| YOLO26n | 0,2875 | 0,3847 | 0,4168 | 0,4432 | 0,4486 | 0,4497 | epoch **55** |
| YOLO26s | 0,4112 | 0,4340 | 0,4738 | 0,4954 | 0,4976 | 0,4974 | epoch **44** |

**Temuan operasional:** keempat model mencapai 99% performa akhirnya pada **epoch 44–55**. Tambahan dari epoch 50 ke epoch 100 hanya **0,0019–0,0075 mAP** — di bawah ambang kebermaknaan. Artinya sekitar **setengah anggaran komputasi (±7 jam GPU) tidak membeli peningkatan apa pun**. Untuk pelatihan berikutnya, 60 epoch sudah memadai, dan penghematan itu lebih baik dialihkan untuk menjalankan beberapa *seed* (lihat Bagian 7).

Grafik lengkap kurva pelatihan tersedia pada `runs/detect/<nama_run>/results.png`.

---

## 4. Analisis Kurva Diagnostik

### 4.1 Kurva F1-Confidence

![Kurva F1 YOLO26s](../../runs/detect/yolo26s_crowdhuman/BoxF1_curve.png)

Kurva ini menjawab pertanyaan praktis: **pada ambang *confidence* berapa model harus dioperasikan?** Sumbu horizontal adalah ambang, sumbu vertikal adalah F1 (rata-rata harmonik precision dan recall). Ambang terlalu rendah menghasilkan banyak *false positive*; terlalu tinggi membuat banyak orang terlewat. Puncak kurva adalah titik seimbangnya.

| Arsitektur | F1 puncak | Ambang optimal |
|---|---|---|
| YOLOv10n | 0,75 | 0,283 |
| YOLO26n | 0,75 | 0,289 |
| YOLOv11n | 0,76 | 0,349 |
| **YOLO26s** | **0,79** | 0,348 |

**Temuan penting:** ambang optimal **berbeda antar arsitektur**. Nilai bawaan Ultralytics (0,25) kebetulan mendekati optimal untuk model *NMS-free* (0,283–0,289), tetapi terlalu rendah untuk YOLOv11n dan YOLO26s (0,348–0,349).

Temuan ini sekaligus menjelaskan anomali pada pengujian latensi: YOLOv11n melaporkan 197 deteksi per citra sementara YOLOv10n hanya 153, padahal mAP keduanya setara. Penyebabnya bukan kepekaan yang lebih tinggi, melainkan **YOLOv11n diuji pada titik operasi di bawah ambang optimalnya**, sehingga mengeluarkan banyak deteksi berkualitas rendah. Pelajarannya: **jumlah deteksi mentah bukan ukuran akurasi**, dan setiap model wajib disetel ambangnya sendiri sebelum masuk pipeline.

### 4.2 Kurva Precision-Recall

![Kurva PR YOLO26s](../../runs/detect/yolo26s_crowdhuman/BoxPR_curve.png)

Kurva PR memetakan pertukaran antara ketelitian dan kelengkapan pada seluruh rentang ambang. Luas di bawah kurva adalah mAP@0.5. Bentuknya jauh lebih informatif daripada satu angka:

- **Wilayah datar (recall 0 sampai ±0,6):** presisi bertahan di atas 0,95. Model sangat andal untuk orang yang terlihat jelas.
- **Lutut kurva (recall ±0,75–0,85):** presisi mulai turun tajam. Di sinilah letak orang yang saling menutupi.
- **Dinding vertikal (recall ±0,92–0,93):** presisi jatuh ke nol. **Ini batas atas recall** — berapa pun ambang diturunkan, sisa orang tersebut tidak pernah terdeteksi.

Batas atas recall: **±0,93 untuk YOLO26s**, **±0,92 untuk YOLOv10n**. Artinya sekitar **7–8% orang beranotasi tidak dapat ditemukan oleh detektor pada kondisi apa pun**.

Angka ini penting karena menetapkan **lantai *under-count* struktural bagi seluruh sistem**. Sebaik apa pun *tracker* dan *counting logic* yang dibangun nanti, mereka tidak dapat menghitung orang yang tidak pernah terlihat oleh detektor.

### 4.3 Confusion Matrix

![Confusion Matrix YOLO26s](../../runs/detect/yolo26s_crowdhuman/confusion_matrix.png)

Untuk YOLO26s: **97.662 terdeteksi benar**, **5.453 terlewat** (`person` → `background`), dan **641.871 tercatat sebagai *false positive***.

Angka *false positive* yang tampak dramatis itu **perlu dibaca dengan hati-hati dan bukan merupakan cacat model**. Ultralytics membangun matriks ini pada ambang *confidence* sangat rendah (0,001) agar perhitungan mAP mencakup seluruh rentang kurva. Pada ambang serendah itu, model memang mengeluarkan ratusan kotak spekulatif per citra yang tidak akan pernah dipakai dalam operasi nyata. Nilai FP di sini **sepenuhnya bergantung pada ambang** dan tidak bermakna tanpa menyebutkan ambangnya.

Yang bermakna adalah kolom pertama: **5.453 dari 103.115 orang (5,3%) tidak terdeteksi bahkan pada ambang 0,001**. Angka ini konsisten dengan batas atas recall pada kurva PR, dan menguatkan temuan lantai *under-count* di Bagian 4.2.

Satu kaitan menarik: proporsi orang yang tak terdeteksi (5,3%) berdekatan dengan proporsi kotak bertanda `ignore` (3,52%) yang sengaja tetap disertakan sebagai label positif (Bagian 2.1 poin 3). Sangat mungkin sebagian besar orang "tak terdeteksi" itu justru adalah region ambigu yang oleh protokol resmi CrowdHuman memang tidak wajib dideteksi. **Batas atas recall yang sesungguhnya kemungkinan lebih baik daripada yang tercatat di sini.**

---

## 5. Hasil Pengukuran Latensi

### 5.1 Overhead Post-Processing (NMS)

Pengukuran menggunakan lima citra terpadat dari *validation set*, dipilih secara deterministik berdasarkan kepadatan anotasi, dengan 20 iterasi per citra dan pemanasan 10 putaran penuh. Seluruh model dibatasi ke kelas `person` agar beban *post-processing* sebanding.

| Arsitektur | NMS-free | Inference p50/p95 (ms) | Post-process p50/p95 (ms) | Total p50 (ms) | Porsi post-process |
|---|---|---|---|---|---|
| **YOLOv10n** | ya | **2,129** / 2,454 | **0,167** / 0,205 | **2,296** | 7,3% |
| YOLOv11n | tidak | 2,142 / 2,470 | 0,491 / 0,552 | 2,633 | 18,7% |
| YOLO26n | ya | 2,554 / 2,964 | 0,164 / 0,201 | 2,718 | 6,0% |
| YOLO26s | ya | 2,695 / 3,044 | 0,170 / 0,203 | 2,865 | 6,0% |

Latensi dilaporkan sebagai persentil (p50 = perilaku lazim, p95 = beban puncak), bukan rata-rata, karena distribusi latensi menjulur ke kanan sehingga rata-rata mudah terseret oleh sedikit iterasi lambat.

**Temuan 1 — arsitektur NMS-free memangkas post-processing secara meyakinkan.** Model *NMS-free* membutuhkan 0,164–0,170 ms; model ber-NMS 0,491 ms, atau **2,9 kali lipat**. Pemisahan distribusinya sempurna: p50 model ber-NMS (0,491) masih lebih dari dua kali p95 model *NMS-free* (0,205). Tidak ada tumpang tindih sama sekali.

**Temuan 2 — biaya post-processing NMS-free bersifat datar.** YOLO26s menghasilkan 199 deteksi dan YOLO26n 167 deteksi, namun keduanya membayar 0,164–0,170 ms. Tanpa NMS, biaya *post-processing* **tidak tumbuh mengikuti kepadatan kerumunan**. Bagi sistem *real-time* di ruang publik, sifat ini bernilai lebih tinggi daripada rata-ratanya sendiri: latensi tetap dapat diprediksi justru ketika kerumunan memuncak — yaitu saat sistem paling tidak boleh gagal.

**Temuan 3 — keunggulan NMS-free tidak otomatis menjadi keuntungan bersih.** YOLO26n membutuhkan *inference* 2,554 ms, sekitar **20% lebih lambat** daripada YOLOv10n (2,129 ms) dan YOLOv11n (2,142 ms) pada tier yang sama. Selisih ini nyata, bukan derau: p95 YOLOv10n (2,454) masih berada di bawah p50 YOLO26n (2,554). Akibatnya:

- **YOLOv10n lawan YOLOv11n:** *inference* imbang, YOLOv10n hemat 0,33 ms di *post-processing* → unggul 13% secara total. **Keunggulan NMS-free terwujud.**
- **YOLO26n lawan YOLOv11n:** YOLO26n rugi 0,41 ms di *inference*, hemat 0,33 ms di *post-processing* → **imbang**. **Keunggulan NMS-free-nya habis dimakan biaya inference-nya sendiri.**

### 5.2 Penskalaan Resolusi

![Penskalaan Resolusi RTX 4090](../../experiments/resolusi_scaling.png)

| Arsitektur | FPS @640 | FPS @256 | Deteksi @640 | Deteksi @256 | Deteksi hilang |
|---|---|---|---|---|---|
| YOLOv10n | 287,3 | 364,6 | 153,2 | 33,0 | −78% |
| YOLOv11n | 269,0 | 341,7 | 197,2 | 57,0 | −71% |
| YOLO26n | 254,0 | 320,4 | 167,0 | 41,4 | −75% |
| YOLO26s | 250,7 | 300,4 | 199,0 | 78,6 | −60% |

**Kurvanya sangat landai.** Menurunkan resolusi dari 640 ke 256 memangkas jumlah piksel 6,25 kali lipat, tetapi FPS hanya naik 27%. Ini menunjukkan GPU **sama sekali tidak *compute-bound***: pada waktu frame 2–3 ms, yang mendominasi adalah *overhead* tetap (*preprocessing*, transfer data, interpreter Python), bukan operasi konvolusinya.

Sebaliknya, ongkosnya berat: **tiga perempat deteksi hilang**. Pada RTX 4090 ini pertukaran yang buruk tanpa pengecualian.

**Rekomendasi untuk Skenario D: pertahankan resolusi 640 pada lingkungan GPU.** Menurunkannya hanya membuang kemampuan deteksi tanpa imbalan kecepatan yang berarti.

Perlu dicatat pula bahwa garis batas *real-time* 30 FPS pada grafik berada jauh di dasar — seluruh model beroperasi 8–12 kali lipat di atasnya. **Pada perangkat ini, batas *real-time* bukan kendala sama sekali**, sehingga grafik tersebut tidak dapat dipakai untuk menyimpulkan kelayakan *edge*.

---

## 6. Pembahasan

### 6.1 Arsitektur Tidak Menentukan Akurasi

Pada tier nano, rentang mAP@0.5:0.95 antara ketiga arsitektur hanya **0,0058** (0,4463 sampai 0,4521). Dengan satu *run* per model dan satu *seed*, selisih sekecil itu **tidak dapat dibedakan dari variasi acak**. YOLOv11n bahkan sedikit unggul pada precision, recall, dan mAP@0.5, sementara tertinggal pada mAP@0.5:0.95 — pola yang menandakan kotaknya sedikit kurang rapat pada ambang IoU ketat, tetapi seluruhnya masih di dalam derau.

**Kesimpulan yang boleh ditarik: ketiga arsitektur setara pada akurasi.** Kesimpulan yang **tidak** boleh ditarik: bahwa salah satunya lebih unggul.

Konsekuensi metodologisnya penting: **argumen pemilihan detektor *NMS-free* tidak dapat berdiri di atas akurasi.** Data tidak mendukungnya. Argumen itu hanya dapat berdiri di atas latensi *post-processing*, sebagaimana ditunjukkan Bagian 5.1.

### 6.2 Ukuran Model Jauh Lebih Menentukan

Lompatan dari tier nano ke tier small (YOLO26n 0,4497 → YOLO26s 0,4974) sebesar **0,0477** — sekitar **delapan kali lipat** seluruh rentang antar-arsitektur pada tier yang sama. Peningkatan recall-nya bahkan lebih relevan: dari 0,6888 ke 0,7455, atau **+5,7 poin**, yang berarti sekitar 57 orang tambahan ditemukan dari setiap 1.000 orang.

**Bagi people counting, recall adalah mata uang yang sesungguhnya.** Orang yang tidak terdeteksi tidak dapat dilacak, dan yang tidak dapat dilacak tidak akan pernah dihitung. Karena itu, apabila anggaran komputasi memungkinkan, **pemilihan tier model memberi dampak jauh lebih besar daripada pemilihan keluarga arsitektur**.

### 6.3 Posisi YOLO26 Berdasarkan Bukti

Menggabungkan Bagian 3.1 dan 5.1, pada perangkat dan runtime yang diuji, **YOLOv10n mengungguli YOLO26n pada seluruh dimensi**: akurasi setara, *post-processing* setara, *inference* 20% lebih cepat.

Namun kesimpulan ini **wajib dibaca bersama batasannya**, dan batasannya besar. Dokumentasi YOLO26 [S002] mengklaim lima keunggulan, dan eksperimen ini hanya menguji satu:

| Klaim YOLO26 [S002] | Diuji? | Keterangan |
|---|---|---|
| Native end-to-end / NMS-free | **Ya** | Terbukti (Bagian 5.1) |
| "Up to 43% faster CPU inference" | Tidak | Pengujian dilakukan di GPU |
| DFL dihapus → export lebih sederhana | Tidak | Runtime PyTorch, tanpa export ONNX/TensorRT |
| ProgLoss + STAL → objek kecil | Tidak | mAP bersifat agregat, tidak dipisah per ukuran objek |
| Optimizer MuSGD | Tidak | Melekat pada proses latih, tidak diukur terpisah |

Seluruh proposisi nilai YOLO26 berpusat pada **CPU, perangkat *edge*, dan kemudahan *export*** — tiga hal yang justru belum tersentuh. Eksperimen ini mengukurnya pada PyTorch mentah di GPU kelas server, yaitu **satu-satunya lingkungan yang tidak diklaim apa pun oleh YOLO26**.

Karena itu perumusan yang jujur adalah: **klaim YOLO26 belum terbantahkan, melainkan belum teruji.** Pengujian yang menentukan adalah benchmark pada CPU dengan model ter-*export* ke ONNX (Bagian 8).

Posisi ini konsisten dengan rambu yang telah ditetapkan sejak awal dalam `docs/research/fulltext-notes/S002-yolo26-ultralytics-docs.md`: YOLO26 diposisikan sebagai **kandidat implementasi/prototipe**, sedangkan argumen ilmiah *NMS-free* ditopang oleh YOLOv10 [S003] dan RT-DETR [S004] yang telah melalui *peer review*. Hasil eksperimen ini justru membuktikan bahwa kehati-hatian tersebut tepat.

### 6.4 Batas Keras Arsitektur: 300 Deteksi

Dokumentasi [S002] menyebut kepala *one-to-one* YOLO26 menghasilkan keluaran `(N, 300, 6)` — maksimum **300 deteksi per citra**. Audit pada *validation set* CrowdHuman menemukan citra terpadat memuat **310 orang**, dan **hanya 1 citra dari 4.370 (0,02%)** yang melampaui batas 300.

Dengan proporsi sekecil itu, batasan ini **tidak berdampak praktis** pada penelitian ini dan tidak menjadi alasan untuk menolak YOLO26. Namun tetap perlu dicatat sebagai batasan arsitektur apabila sistem kelak diterapkan pada skenario kerumunan ekstrem seperti stadion atau konser, di mana kepadatan per bingkai dapat jauh melampaui CrowdHuman.

### 6.5 Implikasi untuk Pipeline Counting

Tiga konsekuensi langsung bagi tahap berikutnya:

1. **Lantai *under-count* sebesar 5–8% sudah terkunci di lapisan detektor** (Bagian 4.2 dan 4.3). Target akurasi hitungan akhir harus ditetapkan dengan memperhitungkan lantai ini, bukan mengasumsikan detektor sempurna.
2. **Ambang *confidence* wajib disetel per model** (Bagian 4.1), bukan memakai nilai bawaan. Untuk YOLO26s gunakan ±0,348; untuk model *NMS-free* nano ±0,285.
3. **Kecenderungan galat sistem bersifat *under-count*, bukan *over-count*** (Bagian 3.2), karena recall konsisten lebih rendah dari precision. Ini berlawanan arah dengan galat yang ditemukan pada Skenario C, di mana *naive line crossing* justru menghasilkan *over-count* ekstrem. Kedua sumber galat bekerja berlawanan arah dan **tidak boleh diasumsikan saling menghapus**; keduanya harus diukur terpisah pada evaluasi *end-to-end*.

---

## 7. Batasan

Batasan berikut wajib dinyatakan dalam naskah agar temuan tidak digeneralisasi melampaui bukti:

1. **Satu *run* per model, satu *seed*.** Seluruh selisih di bawah ±0,01 mAP tidak dapat dibedakan dari variasi acak. Untuk mengklaim keunggulan atau kesetaraan secara statistik, dibutuhkan minimal tiga *seed* per model. Penghematan dari pemangkasan epoch (Bagian 3.3) cukup untuk membiayai ini.
2. **Protokol anotasi tidak identik dengan protokol CrowdHuman resmi** (Bagian 2.1). Nilai mAP absolut tidak sebanding dengan literatur; perbandingan antar model tetap sah.
3. **Metrik MR⁻² (*log-average miss rate*) belum dihitung**, padahal merupakan metrik konvensional untuk CrowdHuman. Tanpa itu, keterbandingan dengan literatur pedestrian detection terbatas.
4. **Seluruh pengukuran kecepatan berasal dari RTX 4090, runtime PyTorch, tanpa *export***. Angka ini tidak dapat digunakan untuk menyimpulkan kelayakan *edge*.
5. **Waktu pelatihan pada Tabel 3.1 bukan ukuran kecepatan model.** GPU kemungkinan terbagi antar *run*; angka tersebut hanya informasi anggaran komputasi.
6. **CrowdHuman adalah citra statis.** Tidak ada kesimpulan mengenai stabilitas identitas, *tracking*, maupun akurasi hitungan yang dapat ditarik dari laporan ini.
7. **Evaluasi belum dilakukan pada domain target** (CCTV ruang publik/kampus). Terdapat risiko *domain shift* yang belum terukur.

---

## 8. Langkah Selanjutnya

Berdasarkan temuan di atas, prioritas berikutnya tersusun sebagai berikut:

1. **Benchmark CPU + export ONNX** (prioritas tertinggi). Ini satu-satunya pengujian yang dapat memutuskan apakah klaim inti YOLO26 berdiri, sekaligus menghasilkan angka kelayakan *edge* yang sesungguhnya untuk Skenario D. Workstation i5-12400F yang tersedia telah dipakai pada eksperimen pendahuluan, sehingga hasilnya dapat dibandingkan langsung.
2. **Skenario B — evaluasi tracker.** Belum tersentuh sama sekali. Membutuhkan MOT20/DanceTrack serta integrasi OC-SORT sebagai *baseline* dan DiffMOT sebagai jalur *robust*. Lapisan inilah yang menentukan stabilitas identitas, dan karenanya menentukan galat hitungan.
3. **Pengulangan dengan tiga *seed*** pada 60 epoch, untuk mengubah pernyataan "setara" dari pengamatan menjadi klaim yang tertopang statistik.
4. **Perhitungan MR⁻²** pada keempat model agar hasil dapat disandingkan dengan literatur.
5. **Evaluasi ulang dengan *ignore region* dikecualikan** — tidak memerlukan pelatihan ulang, cukup konversi ulang label validasi dan menjalankan `model.val()`, dengan biaya beberapa menit per model.

---

## Lampiran: Artefak yang Dihasilkan

| Artefak | Lokasi |
|---|---|
| Bobot dan metrik per run | `runs/detect/{yolo10,yolo11,yolo26n,yolo26s}_crowdhuman/` |
| Tabel komparasi otomatis | `scripts/experiments/summarize_training_runs.py` |
| Hasil latensi NMS | `experiments/nms_overhead_results.csv` |
| Hasil penskalaan resolusi | `experiments/resolusi_scaling_results.csv` |
| Audit kualitas anotasi | `scripts/data_prep/check_label_quality.py` |
| Overlay deteksi kualitatif | `experiments/zeroshot/` |
