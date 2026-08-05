# S014 — LightTrack-ReID: catatan implementasi detail (from paper fulltext)

> Sumber: Khan SBJ, Zhang P, Kamal MM, Saudagar AKJ (2026). *LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking.* PLoS ONE 21(3):e0342246. doi:10.1371/journal.pone.0342246
> PDF: `docs/research/papers/S014-lighttrack-reid-....pdf` | HTML cache: `~/.hermes/cache/web/journals.plos.org-e7cde34ada.md`
> Tujuan: resep implementasi setia + konflik/kekosongan yang harus kita putuskan sendiri saat reimplementasi (no code publish → reimplement).

## Angka klaim (buat konteks, BUKAN target reproduksi — protokol beda)
- MOT17 **test** (private det, YOLOX): HOTA 66.92, MOTA 82.81, IDF1 82.52, IDSW 992.
- MOT20 **test**: HOTA 66.6, MOTA 79.1, IDF1 82.2, IDSW 753.
- Asosiasi: ~0.6 GFLOPs/frame (LAE ~0.5 + TBSS ~0.1). Detektor YOLOX-S ~26.8 GFLOPs = dominan. Full pipeline ~30 FPS di GTX 1080 (8GB), i7-6700.
- Training: MOT17+MOT20, 20 epoch, ~10 jam di GTX 1080.
- ⚠️ Angka test pakai public MOT benchmark + YOLOX + full train. Protokol KITA beda (YOLO26, leave-one-out) → kita lapor perbandingan relatif, bukan banding ke tabel paper.

## Arsitektur & rumus (persis dari paper)
- Deteksi `Dt = {(bt,i, ct,i)}`, box xywh + confidence. Tracklet punya history deteksi + fitur. SimilarityModel → cost matrix → Hungarian.
- Cost: `C_ij = 1 − [w_t·s_ij + (1−w_t)·IoU(bt,i, bt−1,j)]`  (Eq 10)
- Occlusion weight global per-frame: `w_t = σ(N_occ_t / N_t)`  — N_occ = deteksi yang IoU overlap > 0.5 dgn deteksi lain; N_t = total deteksi. **(GLOBAL — satu skalar per frame.)**
- TBSS input: `x_ij = [bt,i, bt−1,j, IoU, at,i, at−1,j] ∈ R^73` = 4+4+1+32+32. (Eq 5)
- TBSS: `Linear → Transformer(1 layer, 4 head) → Linear → σ` (Eq 6). d_model TIDAK disebt di paper → kita tentukan (default 64; tunable).
- LAE: `at,i = Pool(Conv(MobileNetV3(It,i))) ∈ R^32` (Eq 2,3). MobileNetV3-Small. Dimensi 16/32/64 diuji → 32 terbaik.
- CMOH: buffer `M_t,j = {a_{t-k,j}}`, K=10 (Eq 7). Context feature `a_ctx = mean(M)` (Eq 8). Untuk tracklet occluded/nggak ada match: sim pakai `[bt,i, bt−1,j, IoU, at,i, a_ctx_t,j]` (Eq 9) — mean embedding buffer, bukan embedding terakhir.
- Training: triplet + BCE. `L = L_triplet + L_BCE` (Eq 13). `L_triplet = max(||a_a−a_p||² − ||a_a−a_n||² + m, 0)`, m=1.0 (Eq 11). BCE for s_ij (Eq 12).

## Training (persis)
- Data: MOT17 + MOT20. APS ~135,000 samples. Split 80/20 train/val (dalam set training; formal val set TIDAK ada).
- `MAX_PAIRS_PER_FRAME = 50` (Eq 1). Positif = pasangan (i,j) dengan GT id sama; negatif = beda id; diambel max 50/frame.
- 20 epoch, Adam lr=0.001. Crop 224×224, normalisasi [0,1]. Augmentasi: random flip 50%, crop 10% padding, color jitter 0.2.
- Hyperparams m=1.0, K=10 di-tune di MOT17 val (half-split).
- FLTC: cache satu tensor per frame `Γ_t = (B_t, I_t, G_t)` — `I_t` = kumpulan crop **224×224** dari semua deteksi frame itu (BUKAN frame utuh). Kurangi I/O dari ~100rb pair-tensor jadi ~2rb frame-tensor; loading 2-5 mnt (uncached) / <30 detik (cached), speedup 3-5×. Biaya ~0.001 GFLOPs/tensor. **Simpan kumpulan crop per frame, bukan frame setengah-res (plan sebelumnya keliru — koreksi).**
- Implementasi asli: Python 3.8, PyTorch 1.9.1, CUDA 10.2, OpenCV 4.5.3, NumPy 1.19.5, TrackEval. Detektor YOLOX pretrained (dari ByteTrack).

## Ablasi (buat ekspektasi KONTRIBUSI relatif tiap modul)
Protocol paper: baseline = YOLOX + Kalman + cost IoU + Hungarian + confidence filtering + **EMA smoothing**; train-set dibelah dua (train/val first-half/second-half). MOT17 & MOT20 val. → angka absolut TIDAK sebanding dengan protokol kita (YOLO26, leave-one-out); pakai POLA-nya saja.

**Per-komponen (MOT17 val):** baseline 66.13 → +LAE 70.88 (naik paling besar); individual: +TBSS 68.10, +CMOH 68.52, +ASW 67.30. TBSS/ASW sendirian naik tipis; LAE bintangnya.

**Kumulatif (MOT17 val):**
| config | HOTA | MOTA | IDF1 | IDSW |
|---|---|---|---|---|
| Baseline | 66.13 | 74.8 | 77.3 | 227 |
| +LAE | 70.88 | 79.0 | 81.97 | 168 |
| +LAE+TBSS | 73.38 | 81.2 | 84.47 | 138 |
| +LAE+TBSS+CMOH | 74.88 | 82.6 | 86.07 | 80 |
| +LAE+TBSS+CMOH+ASW | 75.63 | 83.2 | 86.63 | 79 |

**Kumulatif (MOT20 val):** baseline 56.17/69.92/73.72/1120 → +LAE 60.38/73.51/77.15/952 → +TBSS 63.94/76.61/80.01/882 → +CMOH 65.74/78.21/81.51/701 → +ASW 66.7/78.9/82.3/701.
→ Pelajaran: LAE = peningkatan terbesar; TBSS menambah stabil di atas LAE; CMOH memangkas IDSW drastis (138→80 / 882→701); ASW cuma increment tipis. Ekspektasi kita sama POLAnya.

## Batasan yang diakui paper (= celah kontribusi kita)
1. **ASW global** — satu w uniform per frame, mengabaikan variasi oklusi lokal. Future: *localized ASW*.
2. **CMOH K=10** — cuma untuk short-term occlusion; GAGAL pada long-term/recurrent occlusion. Future: *hierarchical memory*.
3. **Generalization** — encoder dilatih MOT17/MOT20, kurang generalisasi ke domain baru (iluminasi/kamera beda). Future: *domain-adaptive training*.
→ Ketiga future work ini persis = kontribusi "versi kita": (a) ASW lokal per-track, (b) memory 2-tier (short-term buffer + long-term store), (c) fine-tune data kampus.

## Celah/kekosongan yang harus kita putuskan saat reimplement (paper tdk menyebt)
1. **d_model TBSS** tidak dispesifikkan → pilih default 64 (input cuma 73-d), tunable.
2. **Pembentukan triplet dari pasangan APS** tidak dirinci → pilih: dari tiap positive pair, ambil embedding negatif acak sebagai negative anchor; keras/hard mining opsional.
3. **"Soft IoU"** disebut di prose tapi rumus pakai IoU biasa → pakai IoU biasa (rumus lebih otoritatif). Soft-IoU bisa jadi varian nanti.
4. **GFLOPs LAE "0.5" vs MobileNetV3-Small ~0.11** (torchvision) → mismatch; pakai torchvision `mobilenet_v3_small` langsung (lebih hemat, lebih baik). 0.5 kemungkinan over-estimate/kondisi beda.
5. **Cara sampling negatif di APS** (hard vs random) tidak detail → default random negatif, imbang dgn positif.
6. **Threshold conf** deteksi & aturan terminasi trackline (max age) tidak dirinci → pakai nilai analog OC-SORT (conf 0.3, max age mis. 30) & lapor.
7. **EMA smoothing** ada di baseline ablasi — detail formulanya tidak dirinci → EMA biasa di koordinat box.

## Catatan evaluasi (sejajar proyek kita)
- Semua ablasi pakai half-split train (bukan hold-out val). Protokol kita: leave-one-out MOT20-train 4 fold + DanceTrack zero-shot. Report: mean±std + pola kontribusi modul; JANGAN bandingkan angka absolut ke paper.
- Deteksi harus identik antar tracker (YOLO26) — aturan emas proyek.
- Ukur FPS stage asosiasi terpisah dari pipeline penuh (detektor dominan 26.8 GFLOPs di paper).

## Estimasi training untuk protokol kita
- Paper: MOT17+MOT20 (full) 20 epoch ≈ 10 jam GTX1080. On RTX 4090 ≈ 2-4× lipat → ~2.5-5 jam utk full kedua dataset.
- Per fold leave-one-out (MOT17 + 3/4 MOT20 ≈ ~10 sekuens, mirip scale paper): +3-5 jam/fold di 4090. 4 fold ≈ 12-20 jam → 2 malam.
- Ablasi (fold-1 saja): 5 config × ~4 jam ≈ ~20 jam → 1 malam terpisah.