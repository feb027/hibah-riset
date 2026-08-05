# Rencana Implementasi — Tracker Versi Kita: LightTrack-ReID-inspired (Skenario B, Phase 11)

> **Status:** USULAN — belum implementasi. Workflow: konsep → approval → implement.
> **Referensi utama:** PLOS ONE 2026 — *LightTrack-ReID: A Real-time Multi-Object Tracker...* (fulltext di `docs/research/papers/`, catatan di `docs/research/fulltext-notes/`).
> **Posisi di tesis:** pelengkap Skenario B. OC-SORT = baseline ringan (selesai), DiffMOT = pembanding berat GPU (hasil mentah ada, eval menyusul), tracker ini = **proposed method** (ringan, bisa dilatih ulang ke data sendiri).

## Hasil eval DiffMOT vs OC-SORT (protokol sama, YOLO26, TrackEval) — 2026-08-05

| Benchmark | Tracker | HOTA | MOTA | IDF1 | IDSW ↓ | Frag ↓ |
|---|---|---|---|---|---|---|
| MOT20-train | OC-SORT | 36.51 | 55.98 | 42.88 | 14293 | 27646 |
| MOT20-train | **DiffMOT** | **44.37** | **60.91** | **53.86** | **6905** | 15005 |
| DanceTrack-val | OC-SORT | 28.39 | 71.38 | 26.63 | 6701 | 6936 |
| DanceTrack-val | **DiffMOT** | **39.05** | 70.72 | **43.39** | **2784** | 6765 |

DiffMOT menang di semua metrik utama (kecuali MOTA DanceTrack tipis). IDSW DiffMOT ~setengah OC-SORT di kedua benchmark. Implikasi: **DiffMOT secara akurasi jelas baseline terbaik**; kelemahannya bukan akurasi melainkan (1) biaya inference GPU (HMINet+OSNet jauh lebih berat dari LAE+TBSS), (2) black-box — tidak bisa dilatih ulang ke scene kampus, (3) dependensi patch fragile (`patch_diffmot_eval.py`). Tracker versi kita = kandidat menyamai/melampaui akurasi DiffMOT dengan biaya jauh lebih rendah + bisa train ulang.

## Goal

Membangun tracker multi-object *ringan* berbasis ReID-transformer (terinspirasi LightTrack-ReID) untuk people counting realtime:
- Tracking stage GPU: **target >100 FPS di RTX 4090** (paper: ~30 FPS di GTX 1080).
- Bisa dilatih ulang dari data sendiri (MOT20-train + opsional data kampus) → bukan black-box.
- Dievaluasi di **protokol yang sama** dengan OC-SORT & DiffMOT (deteksi YOLO26 sama, TrackEval sama) → perbandingan sah.
- Kontribusi "versi kita" vs paper: **ASW lokal per-track** + **memory dua tingkat (2-tier)** — dua kelemahan yang diakui paper sebagai future work.

## Keputusan desain (sudah disepakati)

1. **Deteksi = YOLO26 fine-tune Skenario A (sama untuk semua tracker).** Deteksi sudah ada di `data/s2/*/det_mot/` → dipakai ulang untuk training crops DAN eval. Aturan emas: deteksi identik.
2. **Protokol eval = MOT20-train (leave-one-out 4 fold) + DanceTrack-val (zero-shot).** Train/test leakage dicegah: model untuk fold-i tidak pernah melihat sekuens fold-i. DanceTrack = tes generalisasi domain (model hanya dilatih MOT20). DiffMOT sudah dieval di protokol ini — lihat tabel di atas.
3. **CMC di-skip** (kamera statis untuk people counting; paper pakai CMC untuk kamera bergerak).
4. **Mode CPU:** flag `USE_REID=false` → cost = 1 − IoU (fallback geometris murni, setara SORT). Mode GPU: LAE+TBSS aktif. Ini menjaga narasi deployment (CPU/edge tetap bisa jalan, GPU dapat akurasi).
5. **Reuse** Kalman + Hungarian dari `external/OC_SORT` (filterpy, sudah terpasang) — jangan tulis ulang.

## Arsitektur (ringkas, detail formula di paper §method)

```
deteksi YOLO26 → filter conf (≥0.3, sama dgn OC-SORT) → tracker.update(boxes)
  ├─ Kalman predict (XYAH, reuse OC_SORT)
  ├─ LAE   : MobileNetV3-Small → head → embedding a ∈ R^32 (L2-normalized)
  ├─ TBSS  : 1-layer transformer, 4 heads. Input x = [b_t, b_{t-1}, IoU, a_t, a_{t-1}] ∈ R^73 → skor s ∈ [0,1]
  ├─ CMOH  : buffer K=10 embedding terakhir per track; saat track hilang → pakai mean konteks
  ├─ ASW   : bobot oklusi w = σ(N_occ/N)  →  cost = 1 − [w·s + (1−w)·IoU]   (MODIFIKASI: w per-track, bukan global)
  └─ Hungarian → update Kalman / track baru / track mati
keluaran: [frame,id,x1,y1,w,h,conf,-1,-1,-1] (format MOT, langsung TrackEval)
```

Komponen biaya (paper): LAE ~0.5 GFLOPs + TBSS ~0.1 GFLOPs → jauh lebih ringan dari DiffMOT (HMINet + OSNet ReID). Ini argumen utama "lebih ideal dari DiffMOT".

## Struktur file

```
src/lighttrack/                # package tracker kita (baru)
  __init__.py
  encoder.py                   # LAE: MobileNetV3-Small (torchvision) + head 32-d
  scorer.py                    # TBSS: 1-layer transformer scorer (input 73-d → s)
  memory.py                    # CMOH: buffer K=10 + mean kontekstual
  tracker.py                   # update loop: Kalman + asosiasi + manajemen track
  dataset.py                   # FLTC (cache tensor frame) + APS (sampling pasangan)
  train.py                     # training LAE+TBSS (triplet + BCE)
  configs/lighttrack_mot20.yaml
scripts/s2/
  run_skenario_b_lighttrack.py # orkestrator: prepare → train → track → eval → laporan
  (eval: reuse step_eval run_skenario_b_ocsort.py dengan --tracker lighttrack)
experiments/s2_tracker/
  lt_models/                   # checkpoint per fold + ablasi
  lighttrack_results/{mot20,dancetrack}/
  trackeval_trackers/{mot20,dance}/lighttrack/
docs/
  panduan-skenario-b-lighttrack.md
```

## Resep training (dari paper, disesuaikan data kita)

| Parameter | Nilai | Catatan |
|---|---|---|
| Data training | MOT17-train + MOT20-train 3-of-4 sekuens per fold (~14k frame) | MOT17 nambah keragaman penampilan; tanpa risiko leakage (eval tetap MOT20 leave-one-out) |
| Pasangan/frame | max 50 (APS) | positif = pasangan track GT ID sama antar frame; negatif = beda ID, seimbang |
| Embedding | 32-d, L2-norm | triplet margin m=1.0 |
| Loss | L = L_triplet + BCE(s, y) | s dari TBSS, y = label pasangan |
| Optimizer | Adam, lr=0.001 | 20 epoch, 80/20 split dalam fold |
| Input | crop 224×224 | augmentasi: flip 50%, crop 10%, color jitter 0.2 |
| FLTC | cache tensor frame 0.5×, LRU cap ~2048 frame | ponytail: LRU cap; naikkan bila cache miss dominan |
| GPU | RTX 4090 kampus (kernel jupyterhub-env, py3.8, torch 2.0.1+cu118) | per fold ~2-3 jam → 4 fold ± 12 jam (semalam) |

## Tahapan

### Phase 1 — Skeleton tracker (tanpa learning)
- Tulis `tracker.py` pakai Kalman+Hungarian dari OC_SORT; asosiasi IoU murni.
- **Verifikasi:** jalankan di MOT20-train → HOTA harus mendekati OC-SORT tanpa OCM/ORU (angka validasi pipeline, bukan target akhir). TrackEval via `run_skenario_b_ocsort.py --steps eval --tracker lighttrack`.

### Phase 2 — LAE encoder + jalur inference
- `encoder.py`: MobileNetV3-Small pretrained (torchvision `mobilenet_v3_small(pretrained=True)`; torch 2.0.1 → API `weights=` atau `pretrained=` sesuai versi torchvision) → GlobalAvgPool → Linear(576→32) → L2-norm.
- Crop pipeline dari deteksi (crop → resize 224 → normalize ImageNet).
- **Verifikasi:** embedding dua crop orang sama lebih dekat (cosine) daripada beda orang — smoke test 10 frame MOT20-01.

### Phase 3 — TBSS scorer + training
- `scorer.py`: Linear(73→d_model) + `nn.TransformerEncoderLayer(d_model, nhead=4)` + Linear → sigmoid.
- `dataset.py`: FLTC (cache tensor 0.5× per frame, LRU) + APS (pasangan max 50/frame dari GT MOT20-train).
- `train.py`: triplet(m=1.0) + BCE, Adam 1e-3, 20 epoch, 80/20.
- **Verifikasi:** loss turun; akurasi BCE val > 90%; 1 fold selesai < 3 jam di 4090.

### Phase 4 — CMOH + ASW lokal
- `memory.py`: buffer K=10 embedding per track; saat oklusi (tidak ada match) → embedding = mean buffer.
- ASW: w per-track dari rasio frame oklusi track tsb (bukan σ global satu frame — **modifikasi kontribusi**).
- **Verifikasi:** IDSW fold-1 turun vs Phase 3 tanpa CMOH.

### Phase 5 — Eval lengkap + ablasi + laporan
- 4 fold leave-one-out MOT20-train (mean ± std) + zero-shot DanceTrack-val.
- Ablasi di fold-1: (a) IoU-only [=Phase 1], (b) +LAE, (c) +TBSS, (d) +CMOH, (e) +ASW-lokal [full] → tabel ala paper.
- FPS: tracking stage di 4090 (GPU mode) + PC rumah (CPU, kedua mode).
- Update `eval_results.csv` (reuse step_eval `--tracker lighttrack`) + tabel perbandingan OC-SORT/DiffMOT/lighttrack + update laporan Skenario B.

### Phase 6 — (Opsional, kalau waktu cukup) Fine-tune data kampus
- Rekam/ambil scene kampus, label deteksi (atau pseudo-label dari YOLO26), fine-tune LAE 5-10 epoch → ukur IDSW/IDF1 vs model MOT20-only. Ini bagian cerita "domain gap" di tesis.

## File yang berubah
- Baru: `src/lighttrack/**` (6 file), `scripts/s2/run_skenario_b_lighttrack.py`, `docs/panduan-skenario-b-lighttrack.md`.
- Diubah: `scripts/s2/run_skenario_b_ocsort.py` (sudah: `--tracker` param), `docs/plans/` (ini), `docs/PROGRESS.md`, `docs/reports/laporan-skenario-b-tracker.md`.
- Tidak disentuh: data, deteksi, hasil OC-SORT/DiffMOT, `patch_diffmot_eval.py`.

## Risiko & jebakan
1. **Angka tidak akan menembus paper (66.6 HOTA MOT20-test)** — protokol kita beda (train-protocol + deteksi sendiri). Yang dilaporkan: perbandingan relatif pada protokol sama. Jangan overclaim.
2. **Python 3.8 di kernel kampus** — tanpa `list[str]` dsb (sudah jadi kebiasaan di script s2).
3. **torchvision di jupyterhub-env**: pastikan `mobilenet_v3_small` tersedia (torch 2.0.1 → torchvision 0.15). Kalau API pretrained berubah, sesuaikan.
4. **FLTC VRAM**: cache 0.5× + LRU cap; jangan cache full-res (MOT20 1080p = ~8 MB/frame × 8.9k frame ≫ VRAM).
5. **Leakage**: jangan pernah train di sekuens yang dieval (leave-one-out wajib). DanceTrack-val tidak boleh masuk training kalau mau dipakai zero-shot.
6. **ReID di CPU tidak realtime** — encodernya 0.5 GFLOPs/crop; di scene padat (>30 orang) CPU gagal. Makanya mode `USE_REID=false` sebagai fallback deployment. Sebutkan di laporan (jujur).

## Estimasi
- Development: ~1.5–2 minggu part-time (Phase 1-4).
- Compute kampus: ±12 jam training (4 fold) + ±6 jam ablasi (fold-1) → 2 malam 4090.
- DiffMOT eval (satu perintah, 10 menit): `python scripts/s2/run_skenario_b_ocsort.py --steps eval --tracker diffmot` di kampus.

## Open questions
1. Download MOT17-train (untuk training lebih kaya) atau cukup MOT20-train? (default: cukup — YAGNI)
2. Phase 6 (fine-tune kampus) dijalankan atau tidak? Tergantung jadwal.
3. Tracker versi kita dipakai di demo realtime Skenario C juga, atau OC-SORT tetap untuk demo?
