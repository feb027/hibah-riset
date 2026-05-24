# Review Phase 2 — Outline PEKERJAAN TERKAIT

**Verdict: READY_FOR_DRAFT**

## Penilaian ringkas

Outline Phase 2 sudah layak menjadi dasar Phase 3 drafting. Struktur tidak jatuh menjadi daftar paper, tetapi disusun secara tematik: domain people counting, detector real-time/NMS-free, MOT pada kerumunan padat, diffusion-based MOT, counting logic, dataset/metrik/deployment, lalu sintesis gap. Urutan ini sesuai panduan dosen pada F-Paper: penelitian terdahulu dikelompokkan, dikritisi berdasarkan kelebihan dan keterbatasan, kemudian diarahkan ke gap dan kebutuhan penelitian.

## Kekuatan utama

1. **Tematik, bukan paper-list.** Setiap seksi memiliki fungsi paragraf, isi yang harus ditulis, sumber utama, kelebihan, keterbatasan, dan mini-synthesis. Ini cukup kuat untuk mencegah draft Phase 3 menjadi kumpulan ringkasan satu-paper-satu-paragraf.
2. **Selaras dengan lecturer guide.** Outline sudah memuat overview riset sebelumnya, telaah kritis, gap pengetahuan/masalah, dan kebutuhan solusi. Bagian sintesis gap di akhir juga sudah mengarah ke kontribusi penelitian tanpa melakukan klaim hasil.
3. **Source mapping umumnya benar.** Pemetaan sumber ke seksi konsisten dengan source ledger dan evidence matrix: S003–S008 untuk detector, S013–S024 untuk MOT, S021–S022 untuk diffusion tracking, S027–S033 untuk crowd/density counting, S010/S011/S034/S035 untuk counting logic, serta S025/S026/S036–S038 untuk metrik/dataset.
4. **Gap aman dari overclaim.** Formulasi “masih terbatas/masih perlu integrasi dan validasi” sudah tepat. Outline tidak menyatakan “belum ada penelitian sama sekali”, sehingga risiko factual overclaim rendah.
5. **YOLO26 ditangani hati-hati.** Outline secara eksplisit menempatkan YOLO26 sebagai kandidat implementasi terbaru berbasis arXiv/vendor docs, bukan fondasi novelty akademik. Anchor akademik NMS-free/end-to-end tetap diarahkan ke YOLOv10, RT-DETR, D-FINE, DEIM, RF-DETR, dan review YOLO.
6. **Density-map vs trajectory counting sudah dipisahkan.** Outline membedakan density-map crowd counting dari detection-tracking-counting berbasis ID/lintasan/zona. Pemisahan ini penting karena proposal menargetkan trajectory/ID-based people counting, bukan sekadar estimasi kepadatan.
7. **Siap untuk draft multi-metrik.** Outline sudah mengarahkan evaluasi ke detection, association/identity, counting error, dan FPS/latency. Ini lebih kuat daripada hanya memakai AP detector atau akurasi hitung tunggal.

## Catatan ketat untuk Phase 3 writer

1. Jangan mengubah outline menjadi katalog paper. Setiap paragraf draft harus menutup dengan sintesis atau keterbatasan, bukan hanya “peneliti A melakukan X”.
2. Jangan memakai S001/S002/S035 sebagai bukti SOTA akademik utama. YOLO26 dan DeepStream hanya boleh menjadi konteks teknis/implementasi.
3. Jangan mengutip angka performa, klaim “terbaik”, atau klaim latency spesifik sebelum full text sumber utama diverifikasi.
4. Saat memakai sumber MDPI, sandarkan klaim inti pada anchor non-MDPI bila tersedia, terutama IEEE/CVF, AAAI, NeurIPS/ICLR, Springer, Elsevier, Nature, atau Wiley/IET.
5. Jaga terminologi: density-map counting menghasilkan estimasi jumlah/kepadatan; trajectory-based counting membutuhkan deteksi, ID persistence, validasi lintasan, dan state memory.
6. Gap final harus tetap berbunyi sebagai kebutuhan integrasi dan validasi pada skenario public-space real-time people counting, bukan klaim bahwa semua komponen belum pernah diteliti.

## Blockers

Tidak ada blocker untuk masuk ke Phase 3 drafting.

## Verdict final

**READY_FOR_DRAFT** — outline sudah memenuhi kriteria tematik, sesuai panduan dosen, mapping sumbernya konsisten, gap-nya aman, YOLO26 tidak dioverclaim, dan pemisahan density-map vs trajectory/ID counting sudah jelas. Draft Phase 3 dapat dimulai dengan tetap mengikuti catatan ketat di atas.
