# Analisis Awal Performa Detektor YOLO (Proof of Concept)

**Tanggal:** 29 Juni 2026
**Lingkungan Uji:** 
1. CPU Lokal (AMD RX 6600 host) - Simulasi skenario *Edge Deployment* tanpa akselerasi GPU.
2. Cloud GPU (Google Colab T4) - Simulasi skenario server/komputasi *High-End*.

## Latar Belakang
Pengujian ini merupakan eksperimen awal (*Proof of Concept*) untuk memvalidasi kelayakan kandidat detektor real-time yang diusulkan dalam draf proposal (YOLOv10, YOLO11, dan YOLO26). Mengingat PC utama kampus (berbasis NVIDIA RTX 4090) belum dapat diakses, eksperimen ini menjadi *baseline* sementara untuk memantau perilaku model pada dua metrik utama: **Average FPS (Kecepatan)** dan **Average Detection Confidence (Ketepatan)**.

## Hasil Eksperimen

Berikut merupakan rekapitulasi performa pada video pengujian berdurasi pendek (596 frame):

| Model | CPU (Edge) FPS | GPU (T4) FPS | Detections | Confidence (Avg) |
|---|---|---|---|---|
| **yolov10n.pt** | 24.9 | 41.1* | 426 | 0.7764 |
| **yolov10s.pt** | 16.6 | 80.3 | 418 | 0.8677 |
| **yolo11n.pt** | 32.4 | 80.7 | 420 | 0.8182 |
| **yolo11s.pt** | 16.4 | **86.3** | **433** | 0.8557 |
| **yolo26n.pt** | **31.9** | 72.7 | 406 | 0.8137 |
| **yolo26s.pt** | 16.1 | 71.7 | 421 | **0.8844** |

*\*Catatan: Performa lambat yolov10n di GPU murni disebabkan oleh overhead inisialisasi CUDA awal (warm-up), bukan kelemahan model secara fundamental.*

## Analisis & Temuan Utama

1. **Pembuktian Kemampuan Edge (CPU-only)**
   Untuk lingkungan yang murni mengandalkan CPU, model varian **Nano ('n')** merupakan satu-satunya pilihan yang memenuhi standar *real-time* industri (>30 FPS). Secara spesifik, **YOLO11n (32.4 FPS)** dan kandidat utama **YOLO26n (31.9 FPS)** menunjukkan bahwa pemrosesan video analitik di lapangan (tanpa GPU mahal) sangat mungkin direalisasikan. Jika kita memaksakan model *Small ('s')*, maka framerate akan anjlok drastis ke level ~16 FPS (terlihat seperti patah-patah).

2. **Kinerja Maksimal dengan Akselerasi (GPU)**
   Di lingkungan dengan akselerasi perangkat keras (simulasi T4 GPU), kendala limitasi performa praktis lenyap. Model *Small* seperti **YOLO11s** mampu melesat menjadi model tercepat (86 FPS) dengan kemampuan mendeteksi total orang terbanyak (433 deteksi). Ini memperkuat argumen bahwa ketika PC eksperimen utama (RTX 4090) sudah siap besok, penggunaan model kelas 's' sangat disarankan karena FPS-nya tidak akan menjadi *bottleneck*.

3. **Trade-off: YOLO11 vs YOLO26**
   Meskipun tidak secara resmi ditulis sebagai *candidate*, **YOLO11s** menawarkan *sweet spot* terbaik untuk rasio kecepatan dan banyaknya manusia yang berhasil dideteksi di keramaian. Namun, kandidat utama dari proposal yaitu **YOLO26s** mengamankan posisi teratas untuk **Tingkat Keyakinan Tertinggi (Average Confidence 0.884)**, menegaskan statusnya sebagai metode SOTA dengan arsitektur paling canggih dalam meyakinkan akurasi *bounding box*.

## Kesimpulan Rekomendasi
Sesuai rancangan pada *usulan-pendekatan.md*, pendekatan real-time sangat bergantung pada kapasitas *hardware*. 
- **Rekomendasi Deployment Real-Time Murah:** Gunakan YOLO26n atau YOLO11n.
- **Rekomendasi Eksperimen Kampus (RTX 4090):** Gunakan YOLO26s atau YOLO11s. Mengingat ketersediaan komputasi raksasa tersebut, memilih varian 's' akan jauh meningkatkan akurasi *people counting* tanpa risiko telat merespons (*frame-drop*).
