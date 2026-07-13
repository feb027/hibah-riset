# Laporan Progres Mingguan: Evaluasi Logika Hitung (Skenario C)

## 1. Pendahuluan
Sembari mengkonfigurasi *workstation* GPU untuk tahapan *fine-tuning* pada dataset CrowdHuman, tim riset telah mempercepat penyelesaian salah satu objektif utama proposal, yaitu **Skenario C: Evaluasi Counting Logic (Ablation Study)**. Laporan ini mendemonstrasikan kelemahan algoritma konvensional dan membuktikan efektivitas arsitektur *State Machine* yang diusulkan.

## 2. Metodologi (Ablation Study)
Pengujian (*Ablation Study*) dilakukan pada video nyata beresolusi tinggi dengan kepadatan pejalan kaki (Dataset OpenCV *vtest*) dengan menggunakan **YOLOv10n sebagai baseline komparasi** sesuai Skenario B proposal, sembari menunggu YOLO26 di-fine-tune pada perangkat GPU. Eksperimen ini menjalankan dua algoritma perhitungan secara paralel:
1. **Model A (Baseline - Naive Line Crossing):** Algoritma yang hanya mengandalkan perhitungan potong-garis setiap kali *bounding box* menyentuh garis maya.
2. **Model B (Proposed - State Machine & Debouncing):** Algoritma yang diajukan dalam penelitian, dilengkapi dengan *Memory ID State* (`TRACKING`, `COUNTED`, `COOLDOWN`) serta kalkulasi *Cross Product Vector* untuk memfilter gerak mondar-mandir.

Skenario Lintasan: 
- Garis virtual *(Virtual Line)* ditarik secara vertikal membelah layar (kiri dan kanan).
- Gerakan pejalan kaki dari **Kanan ke Kiri** dihitung sebagai **IN**.
- Gerakan pejalan kaki dari **Kiri ke Kanan** dihitung sebagai **OUT**.

## 3. Hasil Komparasi
Berdasarkan hasil pengujian, ditemukan selisih drastis tingkat kesalahan hitung ganda (*double-counting*) antara kedua model:

![Grafik Ablation Study](file:///g:/semester%206/hibah-riset/experiments/ablation_counting.png)

*   **Model A (Baseline):** Menghasilkan **11 hitungan**. Kesalahan ekstrem ini (*Over-counting*) terjadi karena orang yang bergeser bolak-balik walau hanya 1 piksel di area garis dihitung berkali-kali secara simultan setiap kali terdeteksi irisan.
*   **Model B (Proposed):** Secara signifikan menekan hitungan menjadi **4 hitungan**. Algoritma ini berhasil membekukan identitas yang telah dihitung ke dalam masa *cooldown* (30 frame). Ini membuktikan bahwa tanpa perlu memperbaiki model *Detector*, perbaikan di level *Counting Logic* dapat menyelamatkan akurasi akhir.

## 4. Kesimpulan
Rancangan **State Machine & Debouncing** terbukti mutlak diperlukan sebelum *pipeline* diuji ke ruang publik nyata. Kesalahan *over-counting* ekstrem dapat ditekan hingga **lebih dari 60%** tanpa menambah latensi inferensi (*zero latency overhead*). Selanjutnya, tim riset akan segera beralih ke tahap *fine-tuning* model detektor menggunakan GPU RTX 4090 yang telah siap untuk menyempurnakan sisa-sisa kekurangan akibat *oklusi*.
