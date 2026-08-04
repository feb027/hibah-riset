# Brutal Review — Laporan Skenario B: Baseline OC-SORT (draft 1)

*Reviewer: strict mode (lecturer-style). Target: `docs/reports/laporan-skenario-b-tracker.md`.*
*Dibaca: 2026-08-03. Fokus: factuality, freshness, gap logic, citation integrity, tone, anti-AI, alignment.*

---

## Verdict: BELUM LAYAK final — perlu patch (item 1–4 wajib, 5–7 disarankan)

Angka-angka inti valid dan dapat ditelusuri ke artifacts (`eval_results.csv`, `detection_stats.csv`). Masalahnya di konvensi sitasi, tiga klaim yang melampaui data yang diukur, dan satu tabel pembanding yang seharusnya ada.

---

## 1. [WAJIB] Konvensi sitasi melanggar aturan repo

Laporan Skenario A memakai `[S038]`-style; memory & AGENTS.md menetapkan **S-code** (`(Author, Tahun – Sxxx)`), bukan `[1]`. Draft memakai `[1]`–`[7]`.

- DiffMOT → **S021** (terdaftar di source-ledger)
- HOTA → **S025**
- MOT20 → **S036**
- DanceTrack → **S037**
- OC-SORT → tidak ada S-ID → tulis `(Cao et al., 2023)` polos
- TrackEval/Ultralytics → rujukan vendor/toolkit, tulis deskriptif

**Fix:** ganti seluruh rujukan numerik di teks dengan S-code; daftar pustaka ditata ulang mengikuti.

## 2. [WAJIB] Klaim "AssA jauh lebih lemah daripada DetA" tanpa pengukuran

Draft Bagian 5.1: *"HOTA 37,46 relatif terhadap MOTA 56,13 mengindikasikan komponen asosiasi (AssA) yang jauh lebih lemah daripada komponen deteksi (DetA)"* — **DetA dan AssA tidak pernah dicatat** dalam run kita (`eval_results.csv` hanya memuat HOTA/MOTA/IDF1/IDSW/Frag). Ini inferensi yang sah secara kualitatif, tetapi diformulasikan seolah terukur.

**Fix:** nyatakan sebagai inferensi kualitatif + komitmen mencatat DetA/AssA pada run berikutnya (TrackEval memang menyediakannya).

## 3. [WAJIB] Interpretasi IDF1 berlebihan

*"IDF1 44,67 berarti hampir separuh lintasan memiliki identitas yang tidak konsisten"* — keliru. IDF1 = rasio pasangan identitas yang cocok dengan GT; bukan proporsi lintasan "rusak".

**Fix:** reformulasi: *"sekitar 55% bobot asosiasi identitas tidak cocok dengan GT — implikasi praktis: objek yang identitasnya putus dapat dihitung ganda"*.

## 4. [WAJIB] Perlu tabel komparasi referensi

Pembaca tidak bisa menilai 37,46/28,39 tanpa konteks. Tambahkan tabel (Bagian 4 atau 5.3) dengan caveat eksplisit:

| Benchmark | Tracker | Deteksi | HOTA | IDF1 | MOTA |
|---|---|---|---|---|---|
| MOT20 | OC-SORT (kami) | YOLO26 kita | 37,46 | 44,67 | 56,13 |
| MOT20 | OC-SORT (publikasi) | resmi | 62,4 | — | — |
| DanceTrack | OC-SORT (kami) | YOLO26 kita | 28,39 | 26,63 | 71,38 |
| DanceTrack | OC-SORT (publikasi) | resmi | — | — | — |
| DanceTrack | DiffMOT (publikasi) | YOLOX | 62,3 | 63,0 | — |

Hanya isi sel yang punya sumber; sel kosong = jangan mengarang. Caveat wajib: deteksi berbeda ⇒ tidak sebanding langsung; tabel hanya konteks.

## 5. [DISARANKAN] Angka publikasi OC-SORT perlu sumber

"OC-SORT publikasi melaporkan MOT20 HOTA 62,4 dan DanceTrack-test 55,1" — bersumber dari catatan riset (`references/tracker-evaluation-scenario-b.md`), bukan diverifikasi ulang ke arXiv saat penulisan. Periksa ulang atau tandai "dari catatan riset".

## 6. [DISARANKAN] Video belum ada saat review

Bagian 7 merujuk `demo/*.mp4` yang saat review belum di-render. Verifikasi file + durasi sebelum finalisasi; kalau render gagal, jangan klaim "tersedia".

## 7. [DISARANKAN] Kecil

- "IDF1 paling relevan untuk counting" — kuatkan 1 kalimat alasannya (double-counting saat garis hitung).
- Bagian 5.2 "MOTA 71,38 (tertinggi)" — tertinggi relatif ke MOT20-nya sendiri; perjelas.
- Ringkasan eksekutif item 3: sebutkan angka AssA/DetA belum diukur (konsisten dgn item 2).
- Hindari "Penting:" di awal kalimat (nada template); ganti langsung.

---

## Catatan audit (valid)

- 202 det/frame (MOT20) dan 14,5 det/frame (DanceTrack) sesuai `detection_stats.csv` + log run. ✓
- 7.933 IDSW / 4.464 frame = 1,78 ≈ "1,8 per bingkai". ✓
- MOT20-05 271 det/frame = 449.452/1.657. ✓
- Runtime: 4.464/54,3 FPS ≈ 1,4 menit. ✓
- Sitat DiffMOT (CVPR 2024, pp. 19321–19330, arXiv:2403.02075; DanceTrack HOTA 62,3/IDF1 63,0/AssA 47,2) diverifikasi ke sumber. ✓
- Status DiffMOT (belum dieksekusi + kendala + roadmap) jujur dan sesuai fakta sesi. ✓
