# Review Phase 1 — Source Ledger dan Evidence Matrix

**Verdict: READY_FOR_OUTLINE**

## Penilaian ringkas

Phase 1 sudah cukup kuat untuk masuk ke Phase 2 related-work outline. Ledger memuat **38 sumber**, dengan komposisi **24 A-main**, **11 B-support**, dan **3 C-caution**. Distribusi kebaruan juga memenuhi kriteria awal: **32/38 sumber (84,2%)** berada pada rentang 2024–2026, dan seluruh **A-main (24/24)** berada pada 2024–2026. Ini melampaui target minimal 20 kandidat, minimal 15 sumber kuat, dan minimal 70% sumber utama terbaru.

## Kekuatan akademik

1. **Cakupan tematik memadai.** Ledger sudah mencakup detector real-time/NMS-free, MOT modern, DiffMOT/diffusion tracking, OC-SORT/SORT-family baseline, people/crowd counting, dataset, metrik, dan constraint edge deployment. Ini sesuai dengan taxonomy Phase 2.
2. **Sumber utama cukup kredibel.** Anchor utama berasal dari venue/penerbit kuat seperti IEEE/CVF, NeurIPS, ICLR, AAAI, Springer, Elsevier, Nature Portfolio, Wiley/IET, IEEE Access, PLOS, serta benchmark komunitas. Catatan ledger juga sudah jujur bahwa pembuktian Scopus/WoS spesifik masih perlu cek manual bila dosen memintanya.
3. **Evidence matrix sudah menahan klaim.** Matrix tidak hanya memasangkan klaim dengan sumber, tetapi juga menulis counterpoint/limitasi. Ini penting agar pekerjaan terkait tidak berubah menjadi daftar paper atau klaim promosi.
4. **Selaras dengan panduan dosen.** Struktur bukti sudah mendukung penulisan kritis: konteks, masalah, pendekatan eksisting, gap, lalu kebutuhan penelitian. Ini sesuai instruksi F-Paper agar pekerjaan terkait mengelompokkan penelitian dan menilai kelebihan/kekurangannya berbasis fakta.

## Risiko dan catatan wajib untuk Phase 2

1. **Risiko YOLO26 masih tinggi.** YOLO26 hanya boleh diposisikan sebagai kandidat implementasi terbaru, bukan fondasi novelty akademik. S001 adalah arXiv/preprint dan S002 adalah vendor docs. Klaim akademik tentang NMS-free/end-to-end detector harus ditopang oleh YOLOv10, RT-DETR, D-FINE, DEIM, RF-DETR, dan review YOLO.
2. **Jangan overclaim gap.** Formulasi aman adalah “integrasi dan validasi pipeline masih terbatas/masih perlu diteliti pada skenario public-space people counting,” bukan “belum ada penelitian.” Ledger sudah benar memberi batasan ini pada evidence matrix.
3. **MDPI perlu dipakai proporsional.** Beberapa sumber sangat relevan tetapi berasal dari MDPI. Tidak perlu dibuang, namun bila dosen sensitif terhadap reputasi jurnal, jadikan MDPI sebagai pendukung dan tetap anchor ke IEEE/CVF, AAAI, Springer, Elsevier, Nature, atau Wiley/IET.
4. **Density-map counting jangan disamakan dengan trajectory/ID counting.** Evidence matrix sudah membedakan dua jalur ini. Outline Phase 2 harus mempertahankan pemisahan tersebut agar gap proposal tetap logis.
5. **Full-text reading belum selesai untuk draft final.** Blocker ini tidak menghalangi outline, tetapi sebelum draft final perlu membaca minimal sumber utama yang sudah ditandai: S003, S004, S010, S011, S018, S021, S024, S025, S027, S028.

## Kesiapan untuk outline

Siap untuk Phase 2 dengan syarat outline memakai urutan tematik, bukan daftar paper: people counting dan tantangan CCTV; pemisahan density-map vs detection-tracking-counting; detector real-time/NMS-free; MOT pada crowd/occlusion/ID switch; DiffMOT dan fallback OC-SORT/SORT-family; counting logic berbasis RoI/zone/ID memory; lalu gap integrasi dan evaluasi real-time.

**Blocker Phase 2:** tidak ada.

**Catatan sebelum draft final:** validasi DOI/URL satu per satu, cek status indeks bila diminta dosen, dan jangan menulis klaim performa numerik sebelum membaca full text sumber utama.
