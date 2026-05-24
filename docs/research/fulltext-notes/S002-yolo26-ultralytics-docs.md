# Full-Text Note — S002 Ultralytics YOLO26 Documentation

## Source identity

- Source ID: S002
- Title: Ultralytics YOLO26 Documentation
- Authors/organization: Ultralytics
- Year/version: 2026 documentation; page metadata indicates updated 4 days before scrape on 2026-05-24 UTC.
- URL/DOI/arXiv: https://docs.ultralytics.com/models/yolo26
- Access date: 2026-05-24 UTC / 2026-05-25 WIB project cutoff
- Venue/source type: vendor primary documentation.
- Indexed/peer-reviewed status: not peer-reviewed; official vendor/software documentation.

## Why this source matters

Sumber ini adalah dokumentasi primer YOLO26 dari Ultralytics, sehingga penting untuk memahami fitur implementasi aktual yang mungkin dipakai dalam prototipe: model files, supported tasks, export, one-to-one head, one-to-many head, NMS-free inference, CPU/edge claim, dan benchmark COCO. Namun, karena ini dokumentasi vendor, ia tidak boleh menjadi bukti akademik utama dalam bagian SOTA.

## Problem addressed

- Dokumentasi memosisikan YOLO26 sebagai detector real-time untuk edge dan low-power devices.
- Masalah utama yang ditangani: kompleksitas post-processing NMS, kompatibilitas export/hardware, latency, dan kebutuhan deployment yang lebih sederhana.
- Dokumentasi juga menyoroti kebutuhan small-object recognition, segmentation/pose/OBB task support, dan open-vocabulary YOLOE-26.

## Method summary

- YOLO26 dijelaskan sebagai native end-to-end model yang menghasilkan prediksi langsung tanpa NMS.
- Dokumentasi menyebut DFL removal untuk menyederhanakan export dan kompatibilitas hardware.
- Fitur yang disebut: ProgLoss + STAL untuk peningkatan akurasi/small-object recognition, MuSGD optimizer, semantic segmentation loss, multi-scale proto modules, RLE untuk pose, dan optimized OBB decoding.
- Dual-head architecture:
  - one-to-one head default untuk NMS-free inference dengan output `(N, 300, 6)` dan maksimum 300 deteksi per image;
  - one-to-many head tradisional yang membutuhkan NMS dengan output `(N, nc + 4, 8400)` dan potensi akurasi lebih tinggi dengan biaya post-processing.
- Supported tasks: detection, instance segmentation, semantic segmentation, classification, pose estimation, dan oriented bounding box.

## Dataset / evaluation protocol

- Dokumentasi detection memakai COCO pretrained classes dan tabel performance COCO.
- Tabel detection mencantumkan size 640, mAPval 50-95, mAPval 50-95(e2e), CPU ONNX speed, T4 TensorRT10 speed, params, dan FLOPs.
- Model detection variants: YOLO26n/s/m/l/x.
- People counting, MOT, DiffMOT/OC-SORT, line/zone crossing, dan dataset CCTV lokal: tidak dievaluasi di dokumentasi ini.

## Metrics reported

- Detection: mAPval 50-95 dan mAPval 50-95(e2e).
- Speed: CPU ONNX ms dan T4 TensorRT10 ms.
- Complexity: params (M) dan FLOPs (B).
- Contoh nilai dari dokumentasi detection:
  - YOLO26n: mAPval 50-95 40.9; e2e 40.1; CPU ONNX 38.9 ms; T4 TensorRT10 1.7 ms; 2.4M params; 5.4B FLOPs.
  - YOLO26s: mAPval 48.6; e2e 47.8; CPU ONNX 87.2 ms; T4 TensorRT10 2.5 ms; 9.5M params; 20.7B FLOPs.
  - YOLO26x: mAPval 57.5; e2e 56.9; CPU ONNX 525.8 ms; T4 TensorRT10 11.8 ms; 55.7M params; 193.9B FLOPs.
- Tidak ada HOTA, IDF1, counting error, ID switch, atau full-pipeline FPS.

## Findings safe to cite

- Dokumentasi resmi menyatakan YOLO26 adalah model end-to-end/NMS-free dan dioptimalkan untuk edge/low-power devices.
- Dokumentasi resmi menyebut klaim “up to 43% faster CPU inference” sebagai klaim vendor.
- Dokumentasi resmi menyediakan model files `yolo26n.pt` sampai `yolo26x.pt`, supported tasks, dan contoh penggunaan Python/CLI.
- Dokumentasi resmi menunjukkan ada pilihan one-to-one head untuk NMS-free inference dan one-to-many head yang membutuhkan NMS.
- Dokumentasi aman digunakan untuk menjelaskan feasibility implementasi/prototipe, bukan untuk membuktikan gap akademik.

## Limitations stated by authors

- Bagian “Citations and Acknowledgments” menyatakan Ultralytics belum menerbitkan formal research paper untuk YOLO26 karena model berkembang cepat.
- Dokumentasi menyarankan sitasi software `Ultralytics YOLO26`, bukan paper peer-reviewed.
- DOI YOLO26 disebut pending di dokumentasi.

## Limitations inferred for this project

- Klaim vendor perlu dipisahkan dari klaim akademik; jangan dipakai sebagai anchor SOTA utama.
- Benchmark COCO detection tidak membuktikan akurasi people counting, ID persistence, double-counting prevention, atau performa pada video CCTV lokal.
- Dokumentasi tidak memverifikasi integrasi dengan DiffMOT, OC-SORT, RoI/line crossing, atau ID memory.
- Klaim edge/CPU perlu diuji ulang pada perangkat target jika masuk fase prototipe.

## Exact claims allowed in draft

- “Dokumentasi Ultralytics memosisikan YOLO26 sebagai model end-to-end/NMS-free dengan orientasi deployment edge dan low-power devices.”
- “Dalam naskah akademik, YOLO26 lebih aman diposisikan sebagai kandidat implementasi/prototipe, sedangkan argumen ilmiah NMS-free perlu ditopang paper peer-reviewed seperti YOLOv10 dan RT-DETR.”
- “Dokumentasi YOLO26 menyediakan pilihan one-to-one head untuk NMS-free inference dan one-to-many head yang tetap memakai NMS, sehingga ada kompromi deployment antara kecepatan/sederhana dan akurasi.”

## Claims NOT allowed

- Jangan menulis bahwa dokumentasi vendor membuktikan novelty akademik.
- Jangan menulis bahwa YOLO26 sudah memiliki formal research paper peer-reviewed.
- Jangan menulis bahwa YOLO26 sudah terbukti lebih baik untuk people counting dibanding detector lain tanpa eksperimen pada pipeline counting.
- Jangan memakai angka COCO sebagai klaim performa pada ruang publik/kamera CCTV lokal.
- Jangan mencampur klaim detection dengan klaim tracking/counting.

## Mapped sections

- Detector / NMS-free real-time detection.
- Deployment/edge feasibility.
- Gap synthesis and prototype positioning.

## Notes for citation auditor

- BibTeX key exists as `S002` in `references/references.bib`.
- Final citation should be labelled vendor/software documentation.
- If used in related work, use cautious prose and avoid using S002 as academic proof.
