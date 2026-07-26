# Laporan Skenario A: Fine-Tuning dan Evaluasi Komparatif Empat Arsitektur YOLO pada Dataset CrowdHuman

*Disusun menggunakan standar penulisan akademik untuk justifikasi metodologi eksperimen.*

---

## 1. Ringkasan Eksekutif

Empat arsitektur YOLO telah di-*fine-tune* pada dataset CrowdHuman dan dievaluasi pada tiga dimensi: akurasi deteksi (dua protokol evaluasi), latensi (dua kelas perangkat), dan penskalaan resolusi. Lima temuan utama:

1. **Pada akurasi, ketiga arsitektur tier nano setara.** Rentang mAP@0.5:0.95 hanya 0,0058 — di bawah ambang yang dapat dibedakan dari variasi acak. Argumen pemilihan detektor karena itu tidak dapat berdiri di atas akurasi agregat.
2. **Arsitektur *NMS-free* memangkas latensi *post-processing* 2,9×** dengan pemisahan distribusi yang utuh, dan biayanya **datar** terhadap kepadatan kerumunan.
3. **Peringkat kecepatan terbalik antara GPU dan CPU.** Di RTX 4090 dengan PyTorch, YOLO26n paling lambat di tier nano. Di CPU dengan ONNX, YOLO26n justru **tercepat** — 27% di atas YOLOv11n. Klaim YOLO26 memang seluruhnya tentang CPU/edge, sehingga benchmark GPU adalah lingkungan yang keliru untuk menilainya.
4. **Arsitektur *NMS-free* memiliki batas atas recall lebih tinggi** (0,9124–0,9146) daripada arsitektur ber-NMS (0,9000), konsisten pada dua kali pengukuran. Ini argumen *NMS-free* berbasis **akurasi**, bukan sekadar latensi.
5. **Terdapat lantai *under-count* struktural sebesar 7,4–10,0%** yang terkunci di lapisan detektor dan tidak dapat diperbaiki oleh *tracker* maupun *counting logic* di hilirnya.

Seluruh angka dapat ditelusuri ke berkas hasil yang tercantum pada Lampiran.

---

## 2. Pendahuluan

Laporan ini mendokumentasikan pelaksanaan penuh **Skenario A (Evaluasi Detector)** sebagaimana dirancang dalam `docs/drafts/usulan-pendekatan.md` dan dirinci sebagai S1 dalam `docs/drafts/bab3_revisi_skenario_eksperimen.md`.

Tujuan skenario ini bukan menentukan "model terbaik" secara umum, melainkan menjawab satu pertanyaan yang menopang rancangan sistem: **apakah arsitektur *NMS-free* memberikan keuntungan nyata untuk *people counting* di kerumunan padat, dan apakah keuntungan itu cukup besar untuk membenarkan pemilihannya?**

Perlu ditegaskan sejak awal bahwa deteksi bukanlah *counting*. CrowdHuman berupa citra statis tanpa identitas temporal, sehingga laporan ini membatasi diri pada kualitas detektor sebagai lapisan kedua dari pipeline lima lapis. Akurasi hitungan akhir baru dapat dinilai setelah Skenario B (tracker) dan Skenario C (counting logic) terintegrasi.

---

## 3. Metodologi

### 3.1 Dataset dan Protokol Anotasi

Dataset yang digunakan adalah **CrowdHuman** (Shao et al., 2018) [S038], dengan pembagian standar: ±15.000 citra latih dan **4.370 citra validasi**. Seluruh evaluasi dilakukan pada *validation set*, yang memuat **103.115 kotak beranotasi bertag `person`**.

Audit anotasi dijalankan menggunakan `scripts/data_prep/check_label_quality.py` dengan hasil berikut:

| Aspek | Jumlah | Proporsi |
|---|---|---|
| Total kotak `person` | 103.115 | 100% |
| Menembus tepi citra (anotasi amodal) | 15.383 | 14,92% |
| Bertanda `extra.ignore == 1` | 3.634 | 3,52% |
| Titik tengah di luar bingkai | 2.033 | 1,97% |

Keputusan protokol yang diambil, beserta konsekuensinya:

1. **Kotak yang dipakai adalah `fbox` (*full-body box*)**, bukan `vbox` (*visible-body*). Literatur pembanding tidak selalu memakai protokol sama, sehingga nilai absolut **tidak dapat dibandingkan langsung** dengan paper yang memakai *visible-body*.
2. **Anotasi `fbox` bersifat amodal** — digambar sampai bagian tubuh yang tertutup atau di luar bingkai. Kotak-kotak ini ditulis apa adanya tanpa pemotongan.
3. **Kotak `ignore` disertakan sebagai label positif pada pelatihan**, tetapi **dikecualikan pada evaluasi protokol resmi** (Bagian 6). Dampak kuantitatif koreksi ini terukur dan dilaporkan, bukan diasumsikan.
4. **Kotak yang titik tengahnya jatuh di luar bingkai (1,97%)** mengalami distorsi geometri ringan akibat pemotongan per-komponen. Proporsinya kecil dan dampaknya identik pada seluruh model.

Poin 1–4 berlaku **seragam untuk keempat model**. Karena itu, meskipun nilai absolut tidak sebanding dengan literatur, **perbandingan antar model tetap sah** — dan perbandingan itulah objek penelitian.

### 3.2 Konfigurasi Pelatihan

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

Kesetaraan konfigurasi diverifikasi dari berkas `args.yaml` masing-masing run, bukan diasumsikan.

### 3.3 Perangkat dan Runtime

| Lingkungan | Perangkat | Runtime | Dipakai untuk |
|---|---|---|---|
| Server GPU | NVIDIA RTX 4090 | PyTorch | Pelatihan, evaluasi akurasi, latensi GPU, penskalaan resolusi |
| Edge CPU | CPU workstation kampus | PyTorch dan ONNX Runtime | Latensi CPU, uji klaim edge |

---

## 4. Hasil Pelatihan

### 4.1 Tabel Utama

| Arsitektur | Sumber | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | Waktu latih |
|---|---|---|---|---|---|---|
| **YOLO26s** | S001/S002 | **0,8480** | **0,7455** | **0,8266** | **0,4974** | 4,89 jam |
| YOLOv10n | S003 | 0,8212 | 0,6892 | 0,7826 | 0,4521 | 5,91 jam |
| YOLO26n | S001/S002 | 0,8230 | 0,6888 | 0,7814 | 0,4497 | 2,27 jam |
| YOLOv11n | — | 0,8352 | 0,6965 | 0,7855 | 0,4463 | 1,94 jam |

*Dibangkitkan otomatis oleh `scripts/experiments/summarize_training_runs.py` untuk menghindari kesalahan salin manual. Sumber: `runs/detect/*/results.csv`.*

### 4.2 Cara Membaca Metrik Ini

Arti operasional tiap kolom dalam konteks *people counting*:

- **Precision (0,82–0,85)** — dari setiap 100 kotak yang dilaporkan sebagai "orang", sekitar 82–85 memang benar. Sisanya *false positive*, yang bila bertahan beberapa frame dapat memicu **hitungan berlebih**.
- **Recall (0,69–0,75)** — dari setiap 100 orang yang benar-benar ada, model menemukan 69–75. Sisanya terlewat, menyebabkan **hitungan kurang**. Ini metrik paling kritis bagi penelitian ini.
- **mAP@0.5** — ambang tumpang tindih longgar (50%); mengukur "apakah orangnya ketemu".
- **mAP@0.5:0.95** — ambang ketat (50–95%); mengukur "apakah kotaknya rapat". Menjadi tolok ukur utama karena kotak yang meleset menyulitkan *tracker* mempertahankan identitas antar-frame.

**Recall konsisten lebih rendah daripada precision di semua model.** Ini pola khas deteksi kerumunan padat: model cenderung melewatkan orang yang tertutup ketimbang mengarang deteksi. Untuk *people counting*, artinya sistem punya **kecenderungan sistemik ke arah *under-count***.

### 4.3 Dinamika Konvergensi

Perkembangan mAP@0.5:0.95 sepanjang pelatihan:

| Arsitektur | Ep 1 | Ep 10 | Ep 25 | Ep 50 | Ep 75 | Ep 100 | Capai 99% nilai akhir |
|---|---|---|---|---|---|---|---|
| YOLOv10n | 0,2811 | 0,3847 | 0,4232 | 0,4446 | 0,4510 | 0,4521 | epoch **55** |
| YOLOv11n | 0,3023 | 0,3896 | 0,4247 | 0,4408 | 0,4452 | 0,4463 | epoch **55** |
| YOLO26n | 0,2875 | 0,3847 | 0,4168 | 0,4432 | 0,4486 | 0,4497 | epoch **55** |
| YOLO26s | 0,4112 | 0,4340 | 0,4738 | 0,4954 | 0,4976 | 0,4974 | epoch **44** |

**Keempat model mencapai 99% performa akhirnya pada epoch 44–55.** Tambahan dari epoch 50 ke 100 hanya **0,0019–0,0075 mAP** — di bawah ambang kebermaknaan. Sekitar **setengah anggaran komputasi (±7 jam GPU) tidak membeli peningkatan apa pun**. Untuk pelatihan berikutnya, 60 epoch memadai.

![Kurva pelatihan YOLO26s](../../runs/detect/yolo26s_crowdhuman/results.png)

---

## 5. Analisis Kurva Diagnostik

### 5.1 Kurva F1-Confidence

![Kurva F1 YOLO26s](../../runs/detect/yolo26s_crowdhuman/BoxF1_curve.png)

Kurva ini menjawab pertanyaan praktis: **pada ambang *confidence* berapa model harus dioperasikan?** Ambang terlalu rendah menghasilkan banyak *false positive*; terlalu tinggi membuat banyak orang terlewat. Puncak kurva adalah titik seimbangnya.

| Arsitektur | F1 puncak | Ambang optimal |
|---|---|---|
| YOLOv10n | 0,75 | 0,283 |
| YOLO26n | 0,75 | 0,289 |
| YOLOv11n | 0,76 | 0,349 |
| **YOLO26s** | **0,79** | 0,348 |

**Ambang optimal berbeda antar arsitektur.** Nilai bawaan Ultralytics (0,25) mendekati optimal untuk model *NMS-free* (0,283–0,289), tetapi terlalu rendah untuk YOLOv11n dan YOLO26s (0,348–0,349).

Temuan ini menjelaskan anomali pada pengujian latensi: YOLOv11n melaporkan 197 deteksi per citra sementara YOLOv10n hanya 153, padahal mAP keduanya setara. Penyebabnya bukan kepekaan lebih tinggi, melainkan **YOLOv11n diuji di bawah ambang optimalnya** sehingga mengeluarkan banyak deteksi berkualitas rendah. Pelajarannya: **jumlah deteksi mentah bukan ukuran akurasi**, dan setiap model wajib disetel ambangnya sendiri sebelum masuk pipeline.

### 5.2 Kurva Precision-Recall

![Kurva PR YOLO26s](../../runs/detect/yolo26s_crowdhuman/BoxPR_curve.png)

Bentuk kurva lebih informatif daripada satu angka:

- **Wilayah datar (recall 0 sampai ±0,6):** presisi bertahan di atas 0,95. Model sangat andal untuk orang yang terlihat jelas.
- **Lutut kurva (recall ±0,75–0,85):** presisi turun tajam. Di sinilah orang yang saling menutupi.
- **Dinding vertikal (recall ±0,90–0,93):** presisi jatuh ke nol. **Ini batas atas recall** — berapa pun ambang diturunkan, sisa orang tersebut tidak pernah terdeteksi.

Nilai eksak batas atas recall dihitung pada Bagian 6.

### 5.3 Confusion Matrix

![Confusion Matrix YOLO26s](../../runs/detect/yolo26s_crowdhuman/confusion_matrix.png)

Untuk YOLO26s: **97.662 terdeteksi benar**, **5.453 terlewat**, dan **641.871 tercatat sebagai *false positive***.

Angka *false positive* yang tampak dramatis itu **bukan cacat model dan perlu dibaca dengan hati-hati**. Ultralytics membangun matriks ini pada ambang *confidence* sangat rendah (0,001) agar perhitungan mAP mencakup seluruh kurva. Pada ambang serendah itu model memang mengeluarkan ratusan kotak spekulatif per citra yang tidak akan dipakai dalam operasi nyata. Nilai *false positive* di sini **sepenuhnya bergantung pada ambang** dan tidak bermakna tanpa menyebutkan ambangnya.

Yang bermakna adalah kolom pertama: **5.453 dari 103.115 orang (5,3%) tidak terdeteksi bahkan pada ambang 0,001**.

---

## 6. Evaluasi Protokol CrowdHuman

Evaluasi Ultralytics pada Bagian 4 memakai protokol yang memasukkan region `ignore` sebagai target wajib. Bagian ini mengulang evaluasi dengan **protokol CrowdHuman resmi**, di mana region `ignore` diperlakukan netral: tidak wajib dideteksi, dan deteksi yang jatuh di atasnya tidak dihitung sebagai *false positive*.

Perbedaan ini penting dan bukan sekadar menghapus kotak dari ground truth — kalau hanya dihapus, deteksi di region itu justru **berbalik menjadi *false positive*** dan model dihukum dua kali. Implementasi ada di `src/eval_mr2.py`, dijalankan lewat `scripts/experiments/eval_crowdhuman_protocol.py`.

### 6.1 Hasil

Dijalankan pada seluruh 4.370 citra validasi, dengan **99.481 kotak target** setelah 3.634 kotak `ignore` dipindahkan ke status netral.

| Arsitektur | MR⁻² | AP@0.5 | **Recall maks** | AP@0.5 protokol lama | Selisih |
|---|---|---|---|---|---|
| **YOLO26s** | **0,7574** | **0,8283** | **0,9262** | 0,8167 | +0,0116 |
| YOLOv10n | 0,7764 | 0,7898 | **0,9146** | 0,7766 | +0,0133 |
| YOLOv11n | 0,7778 | 0,7882 | **0,9000** | 0,7742 | +0,0140 |
| YOLO26n | 0,7792 | 0,7881 | **0,9124** | 0,7750 | +0,0132 |

*Sumber: `experiments/crowdhuman_protocol_results.csv`. MR⁻² semakin kecil semakin baik — kebalikan dari mAP.*

**Validasi silang implementasi.** Tiga pemeriksaan independen konsisten, sehingga angka di atas dapat dipercaya:

- AP@0.5 hasil implementasi sendiri berselisih hanya ±0,005 dari mAP@0.5 Ultralytics pada keempat model, meskipun dihitung oleh kode yang sepenuhnya terpisah.
- Jumlah target 99.481 = 103.115 − 3.634, persis sesuai hasil audit anotasi pada Bagian 3.1.
- Kepadatan 99.481 ÷ 4.370 = **22,8 orang per citra**, cocok dengan angka 22,6 yang didokumentasikan CrowdHuman.

Metrik juga diuji terhadap kasus sintetis: detektor sempurna menghasilkan MR⁻² 0,0; satu *false positive* berskor tinggi menaikkannya ke 0,01; *false positive* yang sama di dalam region `ignore` mengembalikannya ke 0,0; dan MR⁻² naik monoton (0 / 0,25 / 0,50 / 0,75) seiring bertambahnya target yang terlewat.

### 6.2 Dampak Koreksi Protokol

Koreksi penanganan region `ignore` menaikkan AP@0.5 sebesar **+0,0116 sampai +0,0140**, dan batas atas recall sebesar **+0,0083 sampai +0,0115**.

Besarnya moderat. **Angka pada Bagian 4 karena itu tetap sahih**, hanya bersifat sedikit pesimistis. Nilai praktis dari pengukuran ini adalah metodologis: proporsi distorsinya kini **terukur, bukan diperkirakan**, sehingga dapat dinyatakan sebagai satu kalimat batasan yang tertopang data.

Perlu dicatat bahwa **koreksi terbesar dialami YOLOv11n** (+0,0140 AP, +0,0115 recall). Ini konsisten dengan mekanisme NMS yang paling dirugikan di region kerumunan ambigu, dan menghubungkan Bagian 6.2 dengan temuan pada Bagian 6.3.

### 6.3 Temuan: Batas Atas Recall Arsitektur NMS-Free Lebih Tinggi

| Arsitektur | Sifat | Recall maks |
|---|---|---|
| YOLO26s | NMS-free | 0,9262 |
| YOLOv10n | NMS-free | 0,9146 |
| YOLO26n | NMS-free | 0,9124 |
| **YOLOv11n** | **ber-NMS** | **0,9000** |

Pada tier nano, kedua arsitektur *NMS-free* mencapai 0,9124–0,9146 sedangkan arsitektur ber-NMS hanya 0,9000 — **selisih 1,2–1,5 poin**. Pola ini muncul **konsisten pada dua kali pengukuran independen**: pada subset 200 citra tercatat 0,9019 lawan 0,9129–0,9137, dan pada 4.370 citra penuh 0,9000 lawan 0,9124–0,9146.

Penjelasan mekanismenya langsung: **NMS tidak dapat membedakan "dua kotak untuk satu orang" dari "dua orang yang saling menutupi".** Di kerumunan padat, penyaringan berbasis tumpang tindih itu menghapus deteksi yang sebenarnya sah. Arsitektur *NMS-free* tidak memiliki tahap tersebut sehingga tidak kehilangan deteksi karenanya.

**Signifikansi temuan ini besar untuk penelitian.** Sebelumnya, argumen pemilihan arsitektur *NMS-free* hanya bertumpu pada latensi *post-processing*, yang secara absolut kecil (0,33 ms). Temuan ini memberi **argumen kedua yang berbasis akurasi**, dan menyentuh metrik yang paling menentukan bagi *people counting*: recall, sumber langsung *under-count*.

Batasan yang wajib disertakan: selisih 1,2–1,5 poin berasal dari satu *run* per model. Konsistensinya pada dua ukuran sampel memperkuat dugaan, tetapi konfirmasi statistik memerlukan pengulangan dengan beberapa *seed*.

### 6.4 Membaca Nilai MR⁻²

MR⁻² keempat model berada pada **0,757–0,779**. Angka ini tinggi dan menuntut penjelasan yang jujur.

MR⁻² merata-ratakan *miss rate* secara logaritmik pada sembilan titik FPPI (*false positive per image*) antara 0,01 dan 1,0. Nilai 0,78 berarti: **apabila sistem dibatasi maksimal satu alarm palsu per citra, model melewatkan sekitar 78% orang.** Tuntutan itu sangat berat pada CrowdHuman, yang memuat 22,8 orang per citra — menemukan sebagian besar dari mereka sambil hanya boleh keliru sekali per gambar.

Sebagai pembanding, baseline pada paper CrowdHuman asli mencapai MR⁻² sekitar 0,50, tetapi memakai ResNet-50 FPN dua tahap dengan puluhan juta parameter dan resolusi masukan lebih besar. Model dalam penelitian ini berukuran **2,4–9,5 juta parameter**, satu tahap, resolusi 640.

**Selisih itu adalah harga yang dibayar untuk memilih model kelas edge, dan justru mendukung framing penelitian ini**: sistem dirancang berjalan tanpa GPU mahal, dan Bagian 7.2 menunjukkan pilihan itu memang membuahkan kelayakan CPU. Nilai MR⁻² tidak boleh dituliskan tanpa menyertakan ukuran model dan tujuan deployment-nya.

---

## 7. Hasil Pengukuran Latensi

### 7.1 Overhead Post-Processing di GPU

Pengukuran memakai lima citra terpadat dari *validation set*, dipilih deterministik berdasarkan kepadatan anotasi, 20 iterasi per citra, pemanasan 10 putaran penuh, seluruh model dibatasi ke kelas `person`.

| Arsitektur | NMS-free | Inference p50/p95 (ms) | Post-process p50/p95 (ms) | Total p50 | Porsi post |
|---|---|---|---|---|---|
| **YOLOv10n** | ya | **2,129** / 2,454 | **0,167** / 0,205 | **2,296** | 7,3% |
| YOLOv11n | tidak | 2,142 / 2,470 | 0,491 / 0,552 | 2,633 | 18,7% |
| YOLO26n | ya | 2,554 / 2,964 | 0,164 / 0,201 | 2,718 | 6,0% |
| YOLO26s | ya | 2,695 / 3,044 | 0,170 / 0,203 | 2,865 | 6,0% |

*Sumber: `experiments/nms_overhead_results.csv`. Latensi dilaporkan sebagai persentil karena distribusinya menjulur ke kanan sehingga rata-rata mudah terseret sedikit iterasi lambat.*

**Temuan 1 — pemangkasan post-processing terbukti meyakinkan.** Model *NMS-free* membutuhkan 0,164–0,170 ms; model ber-NMS 0,491 ms, atau **2,9 kali lipat**. Pemisahan distribusinya sempurna: p50 model ber-NMS (0,491) masih lebih dari dua kali p95 model *NMS-free* (0,205). Tidak ada tumpang tindih.

**Temuan 2 — biaya post-processing NMS-free bersifat datar.** YOLO26s menghasilkan 199 deteksi dan YOLO26n 167 deteksi, namun keduanya membayar 0,164–0,170 ms. Tanpa NMS, biaya *post-processing* **tidak tumbuh mengikuti kepadatan kerumunan**. Bagi sistem *real-time* di ruang publik, sifat ini bernilai lebih tinggi daripada rata-ratanya: latensi tetap dapat diprediksi justru ketika kerumunan memuncak — saat sistem paling tidak boleh gagal.

**Temuan 3 — di GPU, keunggulan itu tidak otomatis menjadi keuntungan bersih.** YOLO26n membutuhkan *inference* 2,554 ms, sekitar **20% lebih lambat** daripada YOLOv10n dan YOLOv11n pada tier sama. Selisih ini nyata: p95 YOLOv10n (2,454) masih di bawah p50 YOLO26n (2,554). Akibatnya:

- **YOLOv10n lawan YOLOv11n:** *inference* imbang, hemat 0,33 ms di *post-processing* → unggul 13% total. Keunggulan *NMS-free* terwujud.
- **YOLO26n lawan YOLOv11n:** rugi 0,41 ms di *inference*, hemat 0,33 ms di *post-processing* → **imbang**. Keunggulan *NMS-free*-nya habis termakan.

### 7.2 Latensi CPU dan Dampak Export ONNX

| Arsitektur | PyTorch CPU p50 | **ONNX CPU p50** | Percepatan | Post-proc ONNX | Total ONNX | Setara FPS | Berkas ONNX |
|---|---|---|---|---|---|---|---|
| **YOLO26n** | 22,48 | **10,05** | 2,24× | 0,233 | **10,28 ms** | **97** | 9,8 MB |
| YOLOv10n | 25,13 | 11,93 | 2,11× | 0,204 | 12,13 ms | 82 | 9,3 MB |
| YOLOv11n | 22,98 | 13,26 | 1,73× | 0,788 | 14,05 ms | 71 | 10,6 MB |
| YOLO26s | 54,50 | 22,91 | 2,38× | 0,235 | 23,15 ms | 43 | 38,2 MB |

*Sumber: `experiments/cpu_onnx_results.csv`.*

**Temuan 4 — peringkat kecepatan terbalik antara GPU dan CPU.**

| Peringkat | Di GPU (PyTorch) | Di CPU (ONNX) |
|---|---|---|
| 1 | YOLOv10n (2,296 ms) | **YOLO26n (10,28 ms)** |
| 2 | YOLOv11n (2,633 ms) | YOLOv10n (12,13 ms) |
| 3 | YOLO26n (2,718 ms) | YOLOv11n (14,05 ms) |
| 4 | YOLO26s (2,865 ms) | YOLO26s (23,15 ms) |

YOLO26n berpindah dari posisi paling lambat di tier nano menjadi **yang tercepat**, unggul 27% atas YOLOv11n dan 18% atas YOLOv10n. Pada lingkungan CPU, penalti *inference* yang muncul di GPU tidak hanya hilang tetapi berbalik menjadi keunggulan, sehingga keuntungan *NMS-free* kini benar-benar terwujud sebagai keuntungan bersih.

Temuan ini menjelaskan mengapa evaluasi di GPU saja menyesatkan untuk menilai YOLO26: seluruh proposisi nilainya memang menyasar CPU dan perangkat edge.

**Temuan 5 — export ONNX memangkas latensi CPU 1,7–2,4× untuk semua arsitektur.** Ini temuan deployment yang berlaku lepas dari pilihan arsitektur, dan berkaitan langsung dengan peta jalan tahun keempat proposal (*optimasi kompresi dan deployment edge*).

**Temuan 6 — deployment CPU tanpa GPU layak.** Keempat model beroperasi di atas 30 FPS pada resolusi penuh 640: 43–97 FPS. Ini bukti kuantitatif pertama bahwa sistem yang diusulkan dapat berjalan tanpa akselerator mahal.

**Klaim vendor yang tidak tereproduksi persis.** Dokumentasi YOLO26 [S002] menyebut "up to 43% faster CPU inference". Terukur **24% lebih cepat** daripada YOLOv11n pada ONNX CPU — arah klaim benar, besarannya lebih kecil. Yang dilaporkan dalam naskah harus angka terukur sendiri, bukan angka vendor.

**Klaim yang tidak terbukti maupun terbantah.** Klaim penghapusan DFL yang mempermudah export tidak dapat dibedakan: keempat model berhasil di-export dalam 0,6–1,0 detik tanpa galat. Tidak ada pembeda karena tidak ada yang bermasalah. Dilaporkan sebagai hasil nol.

### 7.3 Penskalaan Resolusi

![Penskalaan Resolusi](../../experiments/resolusi_scaling.png)

| Arsitektur | FPS @640 | FPS @256 | Deteksi @640 | Deteksi @256 | Deteksi hilang |
|---|---|---|---|---|---|
| YOLOv10n | 287,3 | 364,6 | 153,2 | 33,0 | −78% |
| YOLOv11n | 269,0 | 341,7 | 197,2 | 57,0 | −71% |
| YOLO26n | 254,0 | 320,4 | 167,0 | 41,4 | −75% |
| YOLO26s | 250,7 | 300,4 | 199,0 | 78,6 | −60% |

*Sumber: `experiments/resolusi_scaling_results.csv`.*

**Kurvanya sangat landai.** Menurunkan resolusi dari 640 ke 256 memangkas jumlah piksel 6,25 kali lipat, tetapi FPS hanya naik 27%. GPU **sama sekali tidak *compute-bound***: pada waktu frame 2–3 ms, yang mendominasi adalah *overhead* tetap (*preprocessing*, transfer data, interpreter Python), bukan konvolusinya.

Sebaliknya ongkosnya berat: **tiga perempat deteksi hilang**. Pada GPU ini pertukaran yang buruk tanpa pengecualian.

**Rekomendasi untuk Skenario D: pertahankan resolusi 640 pada lingkungan GPU.** Garis batas 30 FPS pada grafik berada jauh di dasar — seluruh model 8–12 kali lipat di atasnya — sehingga grafik ini tidak dapat dipakai menyimpulkan kelayakan *edge*. Untuk itu, rujuk Bagian 7.2.

---

## 8. Pembahasan

### 8.1 Arsitektur Tidak Menentukan Akurasi Agregat

Pada tier nano, rentang mAP@0.5:0.95 antara ketiga arsitektur hanya **0,0058** (0,4463–0,4521). Dengan satu *run* per model dan satu *seed*, selisih sekecil itu **tidak dapat dibedakan dari variasi acak**. YOLOv11n bahkan sedikit unggul pada precision, recall, dan mAP@0.5, sementara tertinggal pada mAP@0.5:0.95 — pola yang menandakan kotaknya sedikit kurang rapat pada ambang IoU ketat, tetapi seluruhnya masih di dalam derau.

**Kesimpulan yang boleh ditarik: ketiga arsitektur setara pada akurasi agregat.** Yang **tidak** boleh ditarik: bahwa salah satunya lebih unggul.

Namun perlu dibedakan dari Bagian 6.3: **kesetaraan pada mAP agregat tidak berarti kesetaraan pada seluruh aspek.** Batas atas recall menunjukkan perbedaan yang konsisten dan dapat dijelaskan secara mekanis. mAP merata-ratakan banyak hal sekaligus sehingga perbedaan spesifik dapat tersamarkan di dalamnya.

### 8.2 Ukuran Model Jauh Lebih Menentukan

Lompatan dari tier nano ke small (YOLO26n 0,4497 → YOLO26s 0,4974) sebesar **0,0477** — sekitar **delapan kali lipat** seluruh rentang antar-arsitektur pada tier sama. Peningkatan recall-nya lebih relevan lagi: 0,6888 → 0,7455, atau **+5,7 poin**, berarti sekitar 57 orang tambahan ditemukan dari setiap 1.000 orang.

**Bagi people counting, recall adalah mata uang yang sesungguhnya.** Orang yang tidak terdeteksi tidak dapat dilacak, dan yang tidak dapat dilacak tidak akan pernah dihitung.

Namun keputusannya tidak sesederhana "pilih yang besar". Bagian 7.2 menunjukkan YOLO26s hanya mencapai 43 FPS di CPU lawan 97 FPS untuk YOLO26n. **Pemilihan tier karena itu adalah keputusan deployment, bukan keputusan akurasi**: bila GPU tersedia gunakan tier small; bila target CPU/edge dengan beban tinggi, tier nano memberi ruang komputasi jauh lebih lapang.

### 8.3 Posisi YOLO26 Berdasarkan Bukti

Menggabungkan seluruh pengukuran, posisi YOLO26 bergantung pada lingkungan deployment:

| Dimensi | YOLO26n lawan pesaing tier nano |
|---|---|
| Akurasi agregat (mAP) | Setara |
| Batas atas recall | Setara dengan YOLOv10n; **unggul 1,2 poin** atas YOLOv11n |
| Post-processing | Setara dengan YOLOv10n; **unggul 2,9×** atas YOLOv11n |
| Inference di GPU (PyTorch) | **Tertinggal ~20%** |
| Inference di CPU (ONNX) | **Unggul 18–27%** |

Dokumentasi YOLO26 [S002] mengajukan lima klaim. Status pengujiannya kini:

| Klaim YOLO26 [S002] | Status | Hasil |
|---|---|---|
| Native end-to-end / NMS-free | **Diuji** | Terbukti (Bagian 7.1) |
| "Up to 43% faster CPU inference" | **Diuji** | Arah benar, besaran 24% (Bagian 7.2) |
| DFL dihapus → export lebih sederhana | **Diuji** | Hasil nol; semua model export mulus |
| ProgLoss + STAL → objek kecil | Belum | mAP masih agregat, belum dipisah per ukuran objek |
| Optimizer MuSGD | Belum | Melekat pada proses latih, tidak dapat diisolasi |

**Kesimpulan yang dapat dipertahankan:** pemilihan YOLO26 sebagai kandidat implementasi **terdukung bukti untuk lingkungan CPU/edge**, yang merupakan target deployment penelitian ini. Untuk lingkungan GPU dengan runtime PyTorch, YOLOv10n merupakan pilihan lebih cepat pada akurasi setara.

Posisi ini konsisten dengan rambu yang ditetapkan sejak awal dalam `docs/research/fulltext-notes/S002-yolo26-ultralytics-docs.md`: YOLO26 sebagai **kandidat implementasi/prototipe**, sedangkan argumen ilmiah *NMS-free* ditopang YOLOv10 [S003] dan RT-DETR [S004] yang telah melalui *peer review*. Hasil eksperimen membuktikan kehati-hatian itu tepat — dan sekaligus menunjukkan pilihan implementasinya dapat dipertahankan.

### 8.4 Batas Keras Arsitektur: 300 Deteksi

Dokumentasi [S002] menyebut kepala *one-to-one* YOLO26 menghasilkan keluaran `(N, 300, 6)` — maksimum **300 deteksi per citra**. Audit menemukan citra terpadat memuat **310 orang**, dan **hanya 1 citra dari 4.370 (0,02%)** melampaui batas 300.

Dengan proporsi sekecil itu, batasan ini **tidak berdampak praktis** pada penelitian ini. Tetap perlu dicatat sebagai batasan arsitektur apabila sistem diterapkan pada skenario kerumunan ekstrem seperti stadion atau konser.

### 8.5 Implikasi untuk Pipeline Counting

Empat konsekuensi langsung bagi tahap berikutnya:

1. **Lantai *under-count* sebesar 7,4–10,0% sudah terkunci di lapisan detektor.** Batas atas recall 0,9000–0,9262 (Bagian 6.1) berarti sebagian orang tidak pernah terlihat oleh detektor pada ambang mana pun. Target akurasi hitungan akhir harus ditetapkan dengan memperhitungkan lantai ini.
2. **Ambang *confidence* wajib disetel per model**, bukan memakai nilai bawaan: ±0,348 untuk YOLO26s, ±0,285 untuk model *NMS-free* tier nano.
3. **Kecenderungan galat detektor bersifat *under-count***, karena recall konsisten lebih rendah dari precision. Ini **berlawanan arah** dengan galat pada Skenario C, di mana *naive line crossing* menghasilkan *over-count* ekstrem. Kedua sumber galat bekerja berlawanan dan **tidak boleh diasumsikan saling menghapus**; keduanya harus diukur terpisah pada evaluasi *end-to-end*.
4. **Pemilihan model untuk Skenario D bergantung perangkat sasaran.** Dengan GPU: YOLO26s untuk akurasi tertinggi. Dengan CPU: YOLO26n memberi 97 FPS, menyisakan anggaran komputasi besar untuk *tracker* dan *counting logic* di hilirnya — pertimbangan penting karena keduanya belum diukur.

---

## 9. Batasan

1. **Satu *run* per model, satu *seed*.** Selisih di bawah ±0,01 mAP tidak dapat dibedakan dari variasi acak. Klaim kesetaraan maupun keunggulan yang tertopang statistik memerlukan minimal tiga *seed* per model.
2. **Protokol anotasi memakai *full-body box* tanpa pemotongan**, sehingga nilai absolut tidak sebanding dengan literatur yang memakai *visible-body*. Perbandingan antar model tetap sah.
3. **MR⁻² tidak sebanding langsung dengan baseline literatur** karena perbedaan kapasitas model (2,4–9,5 juta parameter lawan puluhan juta) dan resolusi masukan.
4. **Akurasi model ONNX belum divalidasi.** Jumlah deteksi YOLO26n turun 6,9% dari PyTorch ke ONNX (179 → 166,7), penurunan terbesar di antara keempat model. Kecepatan ONNX tidak bermakna bila akurasinya ikut turun; mAP versi ONNX perlu diukur.
5. **Waktu pelatihan bukan ukuran kecepatan model.** GPU kemungkinan terbagi antar *run*; angka tersebut hanya informasi anggaran komputasi.
6. **CrowdHuman adalah citra statis.** Tidak ada kesimpulan mengenai stabilitas identitas, *tracking*, maupun akurasi hitungan yang dapat ditarik dari laporan ini.
7. **Evaluasi belum dilakukan pada domain target** (CCTV ruang publik/kampus). Risiko *domain shift* belum terukur.
8. **Kinerja per tingkat oklusi dan per ukuran objek belum dipisah.** Padahal oklusi adalah pernyataan masalah inti proposal, dan objek kecil adalah klaim YOLO26 yang belum teruji.

---

## 10. Langkah Selanjutnya

Diurutkan menurut nilai per satuan usaha:

1. **Validasi akurasi model ONNX** — menutup Batasan 4 memakai perkakas yang sudah ada, tanpa pelatihan ulang.
2. **Pemisahan recall menurut tingkat oklusi** — CrowdHuman menyediakan `vbox` dan `fbox` per orang, sehingga rasio luasnya dapat dipakai sebagai ukuran oklusi. Ini akan mengukur langsung pernyataan masalah inti proposal, dan menguji apakah keunggulan recall *NMS-free* pada Bagian 6.3 memang berasal dari kasus tumpang tindih.
3. **Pemisahan mAP menurut ukuran objek** — menguji klaim ProgLoss/STAL YOLO26 yang tersisa, sekaligus relevan langsung karena orang di kejauhan tampak kecil pada kamera CCTV.
4. **Skenario B — evaluasi tracker.** Belum tersentuh. Lapisan ini yang menentukan stabilitas identitas dan karenanya menentukan galat hitungan.
5. **Kuantisasi INT8 dan pengukuran ulang CPU** — sejalan dengan peta jalan tahun keempat proposal.
6. **Pengulangan tiga *seed*** pada 60 epoch — biaya ±14 jam GPU, prioritas terendah karena pernyataan jujur "selisih di bawah ambang yang dapat dibedakan" sudah dapat ditulis tanpanya.

---

## Lampiran: Artefak dan Keterlacakan

| Artefak | Lokasi |
|---|---|
| Bobot, metrik, dan kurva per run | `runs/detect/{yolo10,yolo11,yolo26n,yolo26s}_crowdhuman/` |
| Tabel komparasi pelatihan | `scripts/experiments/summarize_training_runs.py` |
| Evaluasi protokol CrowdHuman | `experiments/crowdhuman_protocol_results.csv` |
| Latensi NMS di GPU | `experiments/nms_overhead_results.csv` |
| Latensi CPU dan ONNX | `experiments/cpu_onnx_results.csv` |
| Penskalaan resolusi | `experiments/resolusi_scaling_results.csv` |
| Audit kualitas anotasi | `scripts/data_prep/check_label_quality.py` |
| Implementasi MR⁻² | `src/eval_mr2.py` |
| Overlay deteksi kualitatif | `experiments/zeroshot/` |

Seluruh script pengukuran memakai pemilihan citra uji deterministik berbasis kepadatan anotasi, protokol pemanasan bersama (`src/utils/benchmark.py`), dan pelaporan persentil, sehingga hasil antar perangkat dapat disandingkan langsung dan dapat direproduksi pada mesin lain.
