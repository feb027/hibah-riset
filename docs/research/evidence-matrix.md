# Evidence Matrix — Mapping Sources to Claims

> Phase 1 update: 25 Mei 2026 WIB. Matrix ini mengikat klaim yang boleh dipakai di draft dengan sumber dan batasannya.

| Claim/gap | Supporting sources | Counterpoints/limitations | Draft target |
|---|---|---|---|
| Real-time people counting di ruang publik tidak cukup diselesaikan dengan deteksi frame-level; sistem perlu menggabungkan deteksi, tracking identitas, dan counting logic agar tidak double-counting. | S010, S011, S035, S024, S025, S026 | S035 vendor docs; S010/S011 application-specific. Perlu tulis sebagai kebutuhan arsitektur, bukan bukti bahwa sistem usulan sudah unggul. | Pendahuluan + Related Work counting logic |
| NMS-free/end-to-end detector relevan untuk menurunkan latency karena mengurangi post-processing, tetapi YOLO26 belum punya anchor peer-reviewed yang kuat. | S001, S002, S003, S004, S005, S006, S007, S008 | YOLO26: preprint/vendor. Maka naskah harus menyebut YOLO26 sebagai kandidat implementasi terbaru, dengan justifikasi akademik dari YOLOv10/RT-DETR/D-FINE/DEIM/RF-DETR. | Detector subsection + novelty positioning |
| Tantangan utama people counting dari CCTV adalah kepadatan tinggi, oklusi, small/partial body, pencahayaan, variasi perspektif, dan non-linear motion. | S011, S018, S019, S021, S027, S029, S036, S038 | Crowd counting review biasanya density-map; jangan samakan langsung dengan line/zone counting berbasis ID. | Pendahuluan problem paragraph + Related Work taxonomy |
| SORT/Kalman-family tracker efisien namun rawan identity switch ketika deteksi hilang/occlusion/non-linear motion; OC-SORT memperbaiki sebagian lewat observation-centric update dan tetap berguna sebagai fallback ringan. | S024, S023, S020, S025, S026 | Jangan strawman: OC-SORT adalah baseline kuat, bukan “metode lama yang buruk”. Posisikan sebagai fallback/komparator efisien. | Tracker subsection |
| Diffusion-based MOT menjanjikan untuk prediksi motion non-linear dan pemulihan lintasan, tetapi dapat menambah kompleksitas komputasi. | S021, S022, S033, S013, S014 | Perlu pisahkan DiffMOT/DiffusionTrack untuk tracking dari CrowdDiff untuk density estimation. Klaim real-time perlu mengikuti angka paper, bukan asumsi. | Tracker subsection + gap synthesis |
| 2024–2026 SOTA MOT bergerak ke track-centric, ID-centric, transformer/graph, confidence-aware, dan occlusion-aware association. | S013, S014, S015, S016, S017, S018, S020, S023 | Sebagian metode general MOT, tidak semua dense-crowd-specific. Harus jelaskan relevansinya terhadap ID persistence/counting. | Related Work modern MOT subsection |
| People counting punya dua jalur besar: density-map crowd counting dan detection-tracking-counting. Proposal harus menegaskan memilih jalur kedua karena targetnya real-time people counting berbasis lintasan/ID. | S027, S028, S029, S031, S032, S033, S010, S011, S035 | Density-map methods kuat untuk estimasi kerumunan padat, tetapi tidak selalu memberi ID/arah lintasan. | Counting subsection + gap |
| Edge/real-time deployment memerlukan kompromi accuracy-latency, model compression, export/runtime optimization, dan fallback ringan. | S009, S010, S028, S031, S032, S002, S035 | Jangan klaim deploy edge sudah selesai; ini baru desain kebutuhan dan evaluasi yang akan dilakukan. | Pendahuluan contribution + method scope |
| Dataset dan metrik harus mengukur bukan hanya deteksi, tetapi juga asosiasi identitas dan kecepatan. | S036, S037, S038, S025, S026 | Dataset standar tidak semuanya sesuai domain lokal; perlu rencana validasi rekaman publik/lokal untuk TKT. | Evaluation paragraph + Related Work dataset/metric |
| Gap riset yang aman: banyak studi kuat pada satu komponen (detector, tracker, density counting, atau edge compression), tetapi masih diperlukan rancangan pipeline yang menggabungkan detector real-time, tracker non-linear/occlusion-aware, fallback ringan, dan counting logic berbasis zona/ID untuk public-space people counting. | S003–S011, S013–S026, S027–S038 | Hindari klaim “belum ada sama sekali”. Formulasi: “masih terbatas/masih membutuhkan integrasi dan validasi pada skenario X”. | Gap synthesis + research questions |

## Draftable research questions after Phase 1

1. Bagaimana merancang pipeline people counting real-time yang menggabungkan detector NMS-free/real-time dengan tracker occlusion-aware agar tetap stabil pada kondisi padat dan non-linear motion?
2. Bagaimana memadukan DiffMOT sebagai tracker utama dan OC-SORT/Hybrid-SORT-family sebagai fallback efisien tanpa mengorbankan konsistensi ID dan akurasi hitung?
3. Bagaimana merancang RoI/zone-to-zone/ID state memory agar penghitungan tidak ganda ketika terjadi occlusion, missed detection, dan track fragmentation?
4. Bagaimana mengevaluasi sistem secara seimbang menggunakan metrik deteksi, asosiasi identitas, counting error, dan latency/FPS?

## Current blockers before writing final draft

- Perlu membaca full text minimal sumber utama S003, S004, S010, S011, S018, S021, S024, S025, S027, S028.
- Perlu putuskan apakah MDPI acceptable untuk dosen/tim. Jika tidak, gunakan MDPI sebagai pendukung dan anchor ke IEEE/CVF/Springer/Elsevier/Nature.
- Perlu format sitasi final IEEE/BibTeX dan cek semua DOI/URL satu per satu sebelum naskah final.
