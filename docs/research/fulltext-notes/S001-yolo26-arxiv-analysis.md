# Full-Text Note — S001 YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection

## Source identity

- Source ID: S001
- Title: YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection
- Authors: Sudip Chakrabarty
- Year/version: 2026; arXiv ID 2601.12882
- URL/DOI/arXiv: https://arxiv.org/abs/2601.12882 ; DOI 10.48550/arXiv.2601.12882
- Access date: 2026-05-24 UTC / 2026-05-25 WIB project cutoff
- Venue/source type: arXiv preprint / secondary analytical review.
- Indexed/peer-reviewed status: not peer-reviewed; the abstract explicitly states the article is a secondary analytical review based on publicly available Ultralytics documentation, benchmarks, and technical descriptions.

## Why this source matters

Sumber ini penting karena proposal menyebut YOLO26 sebagai kandidat detector terbaru, sehingga perlu ada catatan khusus agar pembahasan tidak hanya bergantung pada YOLOv10/RT-DETR. Namun, posisinya harus hati-hati: S001 bukan paper resmi Ultralytics dan bukan venue peer-reviewed. Fungsinya adalah menangkap bagaimana YOLO26 diposisikan dalam literatur/preprint terbaru: NMS-free, edge deployment, MuSGD, STAL, ProgLoss, YOLOE-26, dan isu export gap.

## Problem addressed

- S001 membahas keterbatasan YOLO tradisional yang masih memakai Non-Maximum Suppression (NMS) sebagai post-processing, terutama latency, sensitivitas hyperparameter, dan export/deployment gap.
- Paper ini menempatkan YOLO26 sebagai evolusi menuju native end-to-end detector yang memisahkan representasi model dari heuristik post-processing.
- Paper juga membahas kebutuhan real-time object detection untuk edge-based computer vision deployment.

## Method summary

- S001 bukan paper metode primer yang memperkenalkan YOLO26 dari tim Ultralytics; ia adalah analisis sekunder.
- Mekanisme yang dibahas: NMS-free end-to-end framework, MuSGD optimizer, Small-Target-Aware Label Assignment (STAL), ProgLoss, dan YOLOE-26 open-vocabulary module.
- S001 mengaitkan YOLO26 dengan tren one-to-one/end-to-end prediction yang sebelumnya menjadi fondasi akademik pada YOLOv10 dan RT-DETR-family detectors.
- Analisisnya memakai dokumentasi publik Ultralytics dan benchmark COCO val2017 yang tersedia secara publik.

## Dataset / evaluation protocol

- Dataset utama yang dibahas: COCO val2017 benchmark.
- Perbandingan diklaim mencakup skala model YOLO26 dari Nano sampai Extra-Large dan pembanding seperti prior YOLO lineages serta Transformer-based detectors, misalnya RT-DETR, DEIM, dan RF-DETR.
- Hardware/protocol yang muncul dalam ekstraksi: NVIDIA T4 GPU, TensorRT10, FP16 untuk plot speed-accuracy trade-off.
- People counting, MOT, RoI/line crossing, public-space CCTV lokal, dan counting-error evaluation: tidak dievaluasi langsung dalam sumber ini.

## Metrics reported

- Object-detection benchmark metrics: mAP 50-95 / COCO-style accuracy, latency ms/image, parameter count, dan speed-accuracy trade-off.
- Paper membahas deterministic latency dan export gap.
- Tidak melaporkan HOTA, IDF1, MOTA, counting MAE, crossing accuracy, ID switch pada people counting, atau FPS pipeline lengkap detector+tracker+counter.

## Findings safe to cite

- S001 aman dipakai untuk menyatakan bahwa ada preprint 2026 yang menganalisis YOLO26 sebagai model NMS-free/end-to-end untuk real-time object detection.
- S001 aman dipakai untuk mencatat bahwa klaim YOLO26 yang beredar berfokus pada penghapusan NMS, deployment edge, MuSGD, STAL, ProgLoss, dan open-vocabulary YOLOE-26.
- S001 aman dipakai sebagai bukti konteks terbaru bahwa YOLO26 sedang diposisikan sebagai kandidat detector mutakhir, tetapi bukan sebagai bukti akademik utama.
- S001 memperkuat alasan mengapa pembahasan detector perlu menautkan YOLO26 ke anchor peer-reviewed seperti YOLOv10/RT-DETR, bukan berdiri sendiri.

## Limitations stated by authors

- Abstract menyatakan artikel ini adalah secondary analytical review berbasis dokumentasi, benchmark, dan deskripsi teknis publik dari Ultralytics.
- Sumber ini tidak mengklaim sebagai paper resmi Ultralytics.
- Tidak ada validasi independen berbasis eksperimen penulis terhadap pipeline people counting.

## Limitations inferred for this project

- Tidak boleh dipakai sebagai anchor novelty akademik utama karena statusnya arXiv/preprint dan sekunder.
- Tidak membuktikan YOLO26 meningkatkan akurasi people counting, mengurangi double-counting, atau memperbaiki ID switch.
- Benchmark COCO detector tidak otomatis berlaku untuk CCTV ruang publik, kerumunan padat, small/partial body, oklusi, atau pipeline DiffMOT/OC-SORT.
- Angka speed/accuracy harus dikutip sebagai klaim dari sumber/benchmark publik, bukan hasil riset internal tim.

## Exact claims allowed in draft

- “YOLO26 dapat diposisikan sebagai kandidat implementasi detector terbaru karena dokumentasi dan preprint 2026 menekankan rancangan end-to-end/NMS-free untuk real-time object detection.”
- “Karena bukti akademik YOLO26 masih terbatas pada dokumentasi vendor dan preprint/analisis sekunder, klaim ilmiah utama tentang tren NMS-free sebaiknya tetap ditopang oleh YOLOv10 dan RT-DETR.”
- “S001 menunjukkan bahwa diskusi YOLO26 berkisar pada NMS-free inference, MuSGD, STAL, ProgLoss, edge deployment, dan export gap.”

## Claims NOT allowed

- Jangan menulis bahwa YOLO26 sudah peer-reviewed atau terindeks.
- Jangan menulis bahwa YOLO26 terbukti terbaik untuk people counting.
- Jangan menulis bahwa YOLO26 mengurangi double-counting, ID switch, atau error line-crossing tanpa eksperimen pipeline.
- Jangan memakai angka benchmark S001 sebagai hasil eksperimen internal.
- Jangan menjadikan S001 satu-satunya bukti novelty proposal.

## Mapped sections

- Detector / NMS-free real-time detection.
- Deployment/edge context.
- Gap synthesis: YOLO26 sebagai kandidat implementasi, bukan anchor akademik utama.

## Notes for citation auditor

- BibTeX key exists as `S001` in `references/references.bib`.
- Mark as `C-caution` in final prose.
- If cited, add wording such as “preprint/analisis sekunder” or keep it in implementation-context sentence.
