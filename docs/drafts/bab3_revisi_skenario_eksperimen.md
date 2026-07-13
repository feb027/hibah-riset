## 3.6 Rencana Skenario Eksperimen

Evaluasi sistem dirancang dalam empat skenario (S) utama. Skenario pertama menilai *detector*, skenario kedua menilai *tracker*, skenario ketiga menilai *counting logic*, dan skenario keempat menilai *pipeline* secara *end-to-end* pada video target. Berdasarkan uji pendahuluan yang telah dilakukan untuk memastikan validitas rancangan, berikut adalah rincian metodologi operasional untuk masing-masing skenario:

### S1: Evaluasi Deteksi (Analisis Latensi dan Baseline YOLO)
*   **Tujuan:** Menilai kinerja detektor pada kondisi kerumunan (*crowd*) dan menganalisis dampak latensi *post-processing* untuk memastikan kelayakan operasional *real-time*.
*   **Data Uji:** Dataset CrowdHuman (*validation set*).
*   **Skenario Pengujian:** Pengujian komparatif kemampuan bawaan (*Zero-Shot*) membandingkan arsitektur YOLO konvensional yang bergantung pada *Non-Maximum Suppression* (YOLO11) dengan arsitektur *NMS-Free* (YOLO10 dan kandidat YOLO26). Eksperimen ini dijalankan pada dua lingkungan komputasi: (1) Server GPU untuk mensimulasikan ketersediaan komputasi tinggi, dan (2) Edge CPU Lokal untuk mensimulasikan sumber daya terbatas. Selain itu, dilakukan pengujian penskalaan resolusi input (256x256 hingga 640x640) untuk mengamati titik *trade-off* performa.
*   **Metrik Utama:** Waktu *inference* murni (ms), latensi *post-processing* (NMS overhead), *Frames Per Second* (FPS), dan deteksi *Ground Truth*.

### S2: Evaluasi Tracking (Stabilitas Asosiasi Identitas)
*   **Tujuan:** Membandingkan kinerja pelacakan dalam menangani fragmentasi lintasan, oklusi, dan gerak *non-linear*.
*   **Data Uji:** Dataset MOT20 dan DanceTrack.
*   **Skenario Pengujian:** Membandingkan DiffMOT sebagai jalur pelacakan yang tangguh (*robust*) terhadap gerak kompleks, melawan OC-SORT sebagai jalur alternatif (*fallback*) yang mengutamakan efisiensi komputasi.
*   **Metrik Utama:** HOTA, IDF1, MOTA, *ID Switch*, dan kecepatan *tracking* (FPS).

### S3: Evaluasi Counting Logic (Ablation Study State Machine & ROI)
*   **Tujuan:** Menilai ketahanan algoritma perhitungan terhadap gangguan pelacakan (*tracker jitter*) dan pergerakan mondar-mandir pejalan kaki di batas area hitung.
*   **Data Uji:** Dataset video standar kerumunan (seperti OpenCV *vtest*).
*   **Skenario Pengujian:** Studi ablasif (*Ablation Study*) yang dirancang dengan menyuntikkan gangguan getaran koordinat *bounding box* (*tracker jitter noise*) untuk mensimulasikan kesalahan *tracker* di dunia nyata. Skenario ini menjalankan dua algoritma secara paralel untuk komparasi: (1) **Model A (Baseline):** *Naive Line Crossing* yang mengandalkan irisan garis murni, dan (2) **Model B (Proposed):** Sistem usulan yang mengintegrasikan *Polygon Region of Interest* (ROI), kalkulasi arah masuk/keluar melalui *2D Cross Product Vector*, serta mekanisme *ID State Machine Debouncing* yang mengatur siklus objek menjadi status `TRACKING`, `COUNTED`, dan masa pendinginan `COOLDOWN` (selama 30 frame).
*   **Metrik Utama:** Tingkat *error* hitungan, kejadian *over-count* (hitung ganda), *under-count* (hitungan terlewat), dan keakuratan arah (*direction accuracy*).

### S4: Evaluasi End-to-End dan Real-Time (Kelayakan Pipeline)
*   **Tujuan:** Menilai kelayakan operasional dan skalabilitas seluruh *pipeline* yang digabungkan (Deteksi, Tracking, dan Counting) dalam bentuk perangkat lunak utuh.
*   **Data Uji:** Rekaman video *real-world* ruang publik lokal (misal: pintu perpustakaan / gerbang kampus).
*   **Skenario Pengujian:** Mengintegrasikan seluruh model ke dalam sebuah aplikasi *Graphical User Interface* (GUI) interaktif. Pada tahap operasional, skenario diuji dengan mendefinisikan *Polygon ROI* adaptif dan garis potong (*virtual line*) secara visual. Sistem diuji kemampuannya untuk mengabaikan objek di luar poligon (*masking*) dan hanya memfokuskan sumber daya komputasi di dalam zona relevan menggunakan model akhir (YOLO26 yang telah di-*fine-tune*).
*   **Metrik Utama:** FPS *end-to-end*, latensi sistem total, penggunaan sumber daya (CPU/GPU), dan *absolute counting error* terhadap perhitungan manual.
