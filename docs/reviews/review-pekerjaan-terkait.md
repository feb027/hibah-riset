# Review Phase 3 — Draft PEKERJAAN TERKAIT

**Artifact:** `docs/drafts/pekerjaan-terkait.md`  
**Tanggal review:** 25 Mei 2026 WIB  
**Verdict: READY_FOR_PATCH**

## Penilaian ringkas

Draft `PEKERJAAN TERKAIT` sudah kuat secara struktur, alur, dan posisi akademik. Naskah tidak berubah menjadi katalog paper; pembahasan disusun tematik dari domain *people counting*, detector real-time/NMS-free, MOT, diffusion-based tracking, counting logic, dataset/metrik, sampai sintesis gap. Secara substansi, draft sudah mengikuti outline Phase 2, evidence matrix, full-text notes prioritas, dan arahan dosen pada `docs/_extracted/f_paper_penelitian.md`.

Namun, draft **belum boleh masuk next phase** karena ada blocker integritas sitasi: beberapa ID yang dikutip di draft belum ada di `references/references.bib`. Ini melanggar aturan proyek bahwa sumber yang dirujuk langsung harus tercatat dalam bibliografi. Perbaikannya kecil dan jelas, sehingga verdict yang tepat adalah **READY_FOR_PATCH**, bukan `READY_FOR_NEXT_PHASE`.

## Kekuatan utama

1. **Tematik, bukan paper-by-paper.** Struktur bagian sudah mengelompokkan studi berdasarkan kelas persoalan/metode: domain counting, detector, MOT, diffusion tracking, counting logic, evaluasi, dan sintesis gap. Ini sesuai panduan dosen bahwa pekerjaan terkait harus mengelompokkan penelitian terdahulu dan menelaah kelebihan/kekurangannya secara kritis.
2. **Gap logic aman dan tidak overclaim.** Draft memakai formulasi “masih perlu integrasi dan validasi”, bukan klaim berbahaya seperti “belum ada penelitian”. Gap detector → tracking → counting logic dijelaskan runut.
3. **YOLO26 ditangani cukup hati-hati.** Draft menempatkan YOLO26 sebagai kandidat implementasi berbasis dokumentasi vendor/preprint, sementara dasar akademik NMS-free/end-to-end tetap ditopang oleh YOLOv10 dan RT-DETR.
4. **Density-map vs trajectory/ID counting dipisahkan jelas.** Draft membedakan density-map crowd counting dari detection-tracking-counting berbasis ID/lintasan/zona, dan menegaskan bahwa proposal berada pada jalur kedua.
5. **Counting logic tidak dianggap tempelan.** Seksi RoI/line/zone/trajectory validation/ID memory berhasil menunjukkan bahwa tracking yang baik belum otomatis menghasilkan counting yang benar.
6. **Nada Bahasa Indonesia akademik cukup natural.** Prosa relatif padat, tidak berlebihan, dan tidak tampak sebagai AI-slop generik. Kelebihan/keterbatasan studi ditulis dengan nada faktual, bukan pujian kosong.
7. **Selaras dengan lecturer guide.** Draft memuat overview penelitian terdahulu, analisis kelebihan/keterbatasan, identifikasi gap, dan kebutuhan solusi pada paragraf akhir.

## Blocker wajib sebelum next phase

### 1. Ada citation keys yang dikutip draft tetapi belum ada di bibliografi

Hasil cek terhadap `docs/drafts/pekerjaan-terkait.md` dan `references/references.bib`:

- Dikutip di draft tetapi **belum ada** di `references/references.bib`:
  - `S006` — dikutip pada seksi detector, baris 17 draft, untuk DEIM/CVPR 2025.
  - `S015` — dikutip pada seksi MOT modern, baris 29 draft, untuk *Focusing on Tracks*.
  - `S016` — dikutip pada seksi MOT modern, baris 29 draft, untuk *Multiple Object Tracking as ID Prediction*.
  - `S017` — dikutip pada seksi MOT modern, baris 29 draft, untuk DragonTrack.

Semua ID tersebut memang ada di `docs/research/source-ledger.md`, tetapi belum ada sebagai BibTeX key. Karena naskah mengutipnya secara eksplisit, bibliografi harus ditambah atau kutipan harus diganti/dihapus. Ini blocker integritas sitasi.

**Patch minimum:** tambahkan entri BibTeX `S006`, `S015`, `S016`, dan `S017` ke `references/references.bib` berdasarkan ledger, atau revisi draft agar hanya mengutip ID yang sudah tersedia di bibliografi.

## Catatan patch non-blocking tetapi disarankan

1. **Seksi detector, baris 17–19:** klaim D-FINE/DEIM/RF-DETR sudah cukup umum, tetapi karena tidak semua sumber tersebut memiliki full-text notes prioritas, jangan menambah detail performa/angka sebelum full text diverifikasi. Untuk draft saat ini, klaimnya masih aman karena hanya sebagai tren umum.
2. **Seksi sintesis gap, baris 59:** frasa “detector real-time dan NMS-free seperti YOLOv10, RT-DETR, serta kandidat YOLO26 dapat mengurangi bottleneck deteksi” sebaiknya sedikit dipertegas agar S001/S002 tidak tampak menjadi bukti akademik setara dengan S003/S004. Misalnya: YOLOv10/RT-DETR sebagai anchor akademik, sedangkan YOLO26 sebagai kandidat implementasi yang masih berbasis vendor/preprint.
3. **Bibliografi S003/S004/S021/S024:** entri saat ini cenderung arXiv-style, padahal draft memperlakukan beberapa sumber sebagai NeurIPS/CVPR peer-reviewed. Ini bukan blocker untuk draft ID-based citation, tetapi final bibliography nanti sebaiknya memakai metadata proceeding resmi.
4. **Sumber MDPI:** draft sudah menyeimbangkan S010/S011/S018 dengan CVPR/Springer/Nature/IEEE-style anchors. Tetap jaga agar MDPI tidak menjadi satu-satunya penopang klaim SOTA paling penting.

## Hasil pemeriksaan wajib

| Aspek | Penilaian |
|---|---|
| Factuality | Umumnya aman; klaim utama sesuai source ledger, evidence matrix, dan full-text notes prioritas. Tidak ada klaim performa numerik yang tidak diverifikasi. |
| Freshness per 25 Mei 2026 WIB | Baik; draft memakai sumber 2024–2026 untuk detector, MOT, counting, edge, dan dataset/metrik. |
| Citation integrity | **Belum lulus** karena `S006`, `S015`, `S016`, `S017` dikutip tetapi belum ada di `references/references.bib`. |
| Kedalaman SOTA | Cukup untuk Phase 3; meliputi detector, MOT, diffusion, counting logic, edge, dataset, dan metrik. |
| Thematic organization | Lulus; tidak paper-by-paper. |
| Gap logic | Lulus; gap integrasi dirumuskan aman dan tidak mengklaim kekosongan total. |
| YOLO26 caution | Lulus dengan catatan kecil pada sintesis gap agar vendor/preprint tidak tampak setara dengan anchor peer-reviewed. |
| Density-map vs tracking-counting | Lulus; pemisahan eksplisit dan konsisten. |
| Indonesian academic tone | Lulus; prosa natural, kritis, dan cukup ringkas. |
| Anti-AI wording | Lulus; tidak ada frasa template/slop mencolok. |
| Alignment dengan lecturer guide | Lulus; memenuhi overview, kritik, gap, dan kebutuhan solusi. |

## Keputusan

**READY_FOR_PATCH** — draft sudah substantif dan layak dipertahankan, tetapi belum siap masuk fase berikutnya sampai blocker sitasi diperbaiki. Fokus patch cukup jelas: lengkapi bibliografi untuk `S006`, `S015`, `S016`, dan `S017`, lalu pertajam sedikit kalimat YOLO26 pada sintesis gap agar status vendor/preprint tetap eksplisit.
