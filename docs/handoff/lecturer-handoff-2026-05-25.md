# Handoff Diskusi Dosen — Hibah Riset PUU People Counting

> Tanggal kesiapan: 25 Mei 2026 WIB  
> Repo: `feb027/hibah-riset`  
> Fokus tugas minggu ini: pendalaman SOTA, penyusunan **PEKERJAAN TERKAIT**, dan penajaman **PENDAHULUAN**.

## Ringkasan status

| Area | Status |
|---|---|
| Source ledger SOTA | Siap — 38 sumber terpetakan (`A-main`: 24, `B-support`: 11, `C-caution`: 3) |
| Full-text notes prioritas | Siap — 12 note prioritas sumber-spesifik termasuk YOLO26 caution notes, plus 1 bridge Bahasa Indonesia |
| `PEKERJAAN TERKAIT` | Siap diskusi — reviewer patch verdict `READY_FOR_NEXT_PHASE` |
| `PENDAHULUAN` | Siap diskusi — reviewer patch verdict `READY_FOR_NEXT_PHASE`; ±839 kata di luar heading/source ID |
| Citation integrity | Lulus — semua source ID yang dikutip di dua draft ada di `references/references.bib` |
| Validator | `python3 scripts/validate_research_artifacts.py` → `VALIDATION PASSED` |

## File yang perlu dibuka saat diskusi

1. Draft bersih gabungan:
   - `docs/handoff/draft-sections-clean.md`
2. Draft terpisah:
   - `docs/drafts/pendahuluan.md`
   - `docs/drafts/pekerjaan-terkait.md`
3. Evidence/citation control:
   - `docs/research/source-ledger.md`
   - `docs/research/evidence-matrix.md`
   - `docs/research/fulltext-notes/00-phase2-5-indonesian-brief.md`
   - `references/references.bib`
4. Review gate:
   - `docs/reviews/review-pekerjaan-terkait-patch.md`
   - `docs/reviews/review-pendahuluan-patch.md`

## Inti argumen yang dibawa ke dosen

1. **Masalah utama**  
   Real-time people counting pada ruang publik tidak cukup diselesaikan oleh deteksi manusia per-frame karena oklusi, small/partial body, perubahan pencahayaan, gerak non-linear, missed detection, identity switch, dan double-counting.

2. **Pemisahan pendekatan**  
   Literatur dipisahkan menjadi dua jalur:
   - *density-map crowd counting*: kuat untuk estimasi total kerumunan, tetapi tidak memberi ID/arah/state memory;
   - *detection-tracking-counting*: sesuai untuk target proposal karena membutuhkan ID persistence, lintasan, RoI/line/zone, dan anti-double-counting.

3. **Posisi detector**  
   YOLO26 dipakai sebagai kandidat implementasi terbaru, tetapi tidak dijadikan anchor akademik tunggal. Argumen ilmiah NMS-free/end-to-end detection ditopang oleh YOLOv10, RT-DETR, D-FINE, DEIM, dan RF-DETR.

4. **Posisi tracker**  
   DiffMOT diposisikan sebagai tracker utama untuk non-linear motion, sedangkan OC-SORT/SORT-family diposisikan sebagai fallback efisien saat constraint perangkat/latency dominan.

5. **Gap aman**  
   Bukan klaim kekosongan total, melainkan: integrasi eksplisit detector real-time, MOT robust, fallback ringan, dan counting logic berbasis RoI/zone/ID memory masih perlu diperdalam dan divalidasi untuk skenario ruang publik.

## Rumusan gap singkat untuk disampaikan lisan

> Studi terbaru sudah kuat pada detector real-time, MOT, density-based crowd counting, dan edge optimization. Namun, untuk public-space people counting, masih diperlukan pipeline yang mengintegrasikan detector cepat, tracker robust terhadap oklusi dan gerak non-linear, fallback ringan, serta counting logic berbasis zona dan memori identitas agar hitungan tidak ganda dan tetap real-time.

## Pertanyaan penelitian versi diskusi

1. Bagaimana merancang pipeline real-time people counting yang menggabungkan detector NMS-free/real-time dengan tracker yang mampu menjaga identitas pada kondisi padat, oklusi, dan gerak non-linear?
2. Bagaimana memadukan DiffMOT sebagai tracker utama dengan OC-SORT/SORT-family sebagai fallback efisien tanpa mengabaikan konsistensi ID dan akurasi hitung?
3. Bagaimana merancang RoI polygon, zone-to-zone trajectory validation, dan ID state memory agar hitungan tidak ganda ketika terjadi oklusi, missed detection, atau fragmentasi lintasan?

## Risiko/catatan yang perlu jujur ke dosen

| Risiko | Dampak | Mitigasi yang sudah disiapkan |
|---|---|---|
| YOLO26 masih vendor/preprint | Tidak aman dijadikan novelty akademik tunggal | Jadikan kandidat implementasi; anchor akademik ke YOLOv10/RT-DETR/D-FINE/DEIM/RF-DETR |
| Beberapa sumber people-counting/tracking berasal dari MDPI | Perlu cek preferensi dosen/jurnal target | Sandingkan dengan CVPR/NeurIPS/AAAI/Springer/Nature/IEEE sources |
| Dataset publik belum tentu punya label counting berbasis zona | Evaluasi counting bisa tidak langsung tersedia dari MOT20/DanceTrack/CrowdHuman | Tambahkan validasi rekaman ruang publik atau anotasi zona/line untuk skenario target |
| DiffMOT berpotensi lebih berat secara komputasi | Risiko latency saat real-time | Gunakan OC-SORT/SORT-family sebagai fallback; ukur FPS/latency sejak awal |
| Source ID internal belum format IEEE final | Belum siap tempel ke proposal final tanpa formatting | Konversi `[S###]` ke nomor IEEE setelah dosen menyetujui isi/substansi |

## Agenda diskusi offline yang disarankan

1. Setujui dulu **posisi novelty**: integrasi pipeline + counting logic, bukan klaim YOLO26 paling baru.
2. Putuskan apakah YOLO26 tetap menjadi detector utama atau dibuat opsi eksperimen bersama YOLOv10/RT-DETR-style baseline.
3. Putuskan sumber mana yang wajib dipertahankan jika dosen meminta venue non-MDPI lebih dominan.
4. Tetapkan skenario validasi lokal: CCTV kampus/ruang publik, video publik, atau simulasi awal.
5. Tentukan format final: tetap source-ID internal untuk draft tim, atau mulai konversi ke IEEE numerik.
6. Tentukan pembagian kerja mahasiswa: citation formatting, dataset/prototype exploration, atau diagram metode.

## Checklist sebelum dikirim ke dosen

- [x] Draft Pendahuluan di bawah 1000 kata.
- [x] Pendahuluan memuat konteks, masalah, SOTA, gap, RQ, tujuan, kontribusi, dan roadmap 5 tahun.
- [x] Pekerjaan Terkait tematik, bukan katalog paper.
- [x] YOLO26 tidak overclaim sebagai peer-reviewed anchor.
- [x] Density-map counting tidak dicampur dengan trajectory/ID-based counting.
- [x] Semua citation ID di dua draft tersedia di `references/references.bib`.
- [x] Reviewer patch untuk kedua draft memberi verdict `READY_FOR_NEXT_PHASE`.
- [ ] Konversi source ID `[S###]` ke format IEEE final setelah arahan dosen.
- [ ] Rapikan metadata bibliografi final/DOI jika sudah masuk tahap submission.
