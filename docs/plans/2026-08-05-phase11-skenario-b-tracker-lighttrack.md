# Rencana Implementasi — Tracker Versi Kita: LightTrack-ReID-inspired (Skenario B, Phase 11)

> **Status:** USULAN — belum implementasi. Workflow: konsep → approval → implement.
> **Referensi utama:** PLOS ONE 2026 — *LightTrack-ReID* (fulltext di `docs/research/papers/S014-*.pdf`, catatan detail implementasi di `docs/research/fulltext-notes/S014-lighttrack-reid.md` — WAJIB dibaca sebelum implement; isinya resep rumus, tabel ablasi, dan daftar celah yang harus kita putuskan sendiri).
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
- **Target akurasi eksplisit:** melampaui DiffMOT pada protokol sama (HOTA 44.37 MOT20-train / 39.05 DanceTrack-val) dengan biaya asosiasi ~0.6 GFLOPs (LAE+TBSS) vs ReID OSNet DiffMOT ≳ 5 GFLOPs. Kalau hanya menyamai, argumen tesis tetap kuat (biaya <1/10 + bisa train ulang).
- Kontribusi "versi kita" vs paper: **ASW lokal per-track** + **memory hierarkis (2-tier)** + **fine-tune domain kampus** — ketiganya persis future work yang diakui paper (ASW global, CMOH K=10 gagal long-term, encoder kurang generalisasi).

## Kelayakan (bisa kita lakukan? — dicek 2026-08-05)

**Ya.** Hasil verifikasi:

1. **Tidak ada kode publik** (paper 2026-03-25, 0 sitasi; semua hit web = mirror paper/Pubmed/ResearchGate). Implementasi = dari nol, tapi **semua modul terspesifikasi lengkap** (rumus + hiperparameter eksak di `docs/research/fulltext-notes/S014-lighttrack-reid.md`) — tidak ada "infer dari abtraksi".
2. **Semua dependency sudah ada di env kampus** (jupyterhub-env, py3.8, torch 2.0.1+cu118): torchvision 0.15 (→ `mobilenet_v3_small` ada), filterpy (dep OC_SORT, jalan), scipy (Hungarian), numpy/opencv, TrackEval (sudah dipakai). **Tidak ada dependency baru** kecuali pretrained MobileNetV3-Small (~10 MB, download 1×, internet kampus tersedia).
3. **Komponen non-torch cuma 3:** Kalman (filterpy), Hungarian (scipy), format MOT (sudah berpola di `run_ocsort_mot.py`). Tidak ada bagian eksotis.
4. **Data:** kampus sudah punya MOT20-train 4 sekuens + DanceTrack-val (dipakai eval DiffMOT). PC rumah cuma MOT20-01/02 (dev + smoke test saja). MOT17-train sedang di-download user → pindah via WinSCP.
5. **Compute:** RTX 4090 24 GB. Estimasi paper (GTX 1080, 10 jam/20 ep) → ~3 jam/fold → 4 fold ± 12 jam (semalam) + ~6 jam ablasi fold-1.
6. **Risiko nyata bukan "bisa/tidak" tapi:** (a) waktu training, (b) pola ablasi mungkin tidak persis seperti paper (lapor relatif, bukan absolut), (c) satu API torchvision (`mobilenet_v3_small` weights) perlu dicek sekali di kampus — sudah masuk cek `--steps doctor`.

## Keputusan desain (sudah disepakati)

1. **Deteksi = YOLO26 fine-tune Skenario A (sama untuk semua tracker).** Deteksi sudah ada di `data/s2/*/det_mot/` → dipakai ulang untuk training crops DAN eval. Aturan emas: deteksi identik.
2. **Protokol eval = MOT20-train (leave-one-out 4 fold) + DanceTrack-val (zero-shot).** Train/test leakage dicegah: model untuk fold-i tidak pernah melihat sekuens fold-i. DanceTrack = tes generalisasi domain (model hanya dilatih MOT20). DiffMOT sudah dieval di protokol ini — lihat tabel di atas.
3. **CMC di-skip** (kamera statis untuk people counting; paper pakai CMC untuk kamera bergerak).
4. **Mode CPU:** flag `USE_REID=false` → cost = 1 − IoU (fallback geometris murni, setara SORT). Mode GPU: LAE+TBSS aktif. Ini menjaga narasi deployment (CPU/edge tetap bisa jalan, GPU dapat akurasi).
5. **Reuse** Kalman + Hungarian via `filterpy.KalmanFilter` + `scipy.optimize.linear_sum_assignment` (dua-duanya sudah terpasang di env kampus sebagai dependency OC_SORT) — JANGAN import internal `external/OC_SORT` (repo itu di-clone on demand, fragile; pakai library langsung).

## Arsitektur (ringkas, detail formula di paper §method)

```
deteksi YOLO26 → filter conf (≥0.3, sama dgn OC-SORT) → tracker.update(boxes)
  ├─ Kalman predict (XYAH, reuse OC_SORT)
  ├─ LAE   : MobileNetV3-Small → head → embedding a ∈ R^32 (L2-normalized)
  ├─ TBSS  : 1-layer transformer, 4 heads. Input x = [b_t, b_{t-1}, IoU, a_t, a_{t-1}] ∈ R^73 → skor s ∈ [0,1]
  ├─ CMOH  : buffer K=10 embedding terakhir per track; saat track hilang → pakai mean konteks
  ├─ ASW   : paper w_t = σ(N_occ/N) global per frame (N_occ = deteksi dgn IoU overlap > 0.5 dgn deteksi lain)
  │         →  cost = 1 − [w·s + (1−w)·IoU]   (MODIFIKASI kita: w per-track, bukan global)
  └─ Hungarian → update Kalman / track baru / track mati
keluaran: [frame,id,x1,y1,w,h,conf,-1,-1,-1] (format MOT, langsung TrackEval)
```

Komponen biaya (paper): LAE ~0.5 GFLOPs + TBSS ~0.1 GFLOPs; detektor (YOLOX-S) ~26.8 GFLOPs = dominan → asosiasi cuma <3% tambahan. Jauh lebih ringan dari DiffMOT (HMINet + OSNet ReID). Ini argumen utama "lebih ideal dari DiffMOT". Catatan: torchvision `mobilenet_v3_small` ~0.11 GFLOPs — angka paper 0.5 kemungkinan over-estimate; pakai yang torchvision (lebih hemat).

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
  lt_runs/                     # doctor.txt, run log (runs.yaml), loss, stats per step
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
| FLTC | cache **kumpulan crop 224×224 per frame** (uint8, bukan frame setengah-res), LRU cap ~2048 frame | paper: ~100rb pair-tensor → ~2rb frame-tensor, loading <30 dtk (cached); ponytail: LRU cap, naikkan bila cache miss dominan |
| GPU | RTX 4090 kampus (kernel jupyterhub-env, py3.8, torch 2.0.1+cu118) | paper: MOT17+MOT20 full 20 ep ≈ 10 jam GTX 1080 → di 4090 ~2.5-5 jam utk dua dataset; per fold (MOT17+3/4 MOT20) ~3 jam → 4 fold ± 12 jam (semalam) |

## Tahapan

### Phase 1 — Skeleton tracker (tanpa learning)
- Tulis `tracker.py` pakai Kalman+Hungarian dari OC_SORT **tanpa OCM/ORU** (baseline paper = Kalman + IoU + Hungarian + confidence filtering + **EMA smoothing** box — bukan OC-SORT penuh).
- **Verifikasi:** jalankan di MOT20-train → HOTA di bawah OC-SORT penuh (karena tanpa OCM/ORU; ini angka validasi pipeline, bukan target akhir). TrackEval via `run_skenario_b_ocsort.py --steps eval --tracker lighttrack`.

### Phase 2 — LAE encoder + jalur inference
- `encoder.py`: MobileNetV3-Small pretrained (torchvision `mobilenet_v3_small(pretrained=True)`; torch 2.0.1 → API `weights=` atau `pretrained=` sesuai versi torchvision) → GlobalAvgPool → Linear(576→32) → L2-norm.
- Crop pipeline dari deteksi (crop → resize 224 → normalize ImageNet).
- **Verifikasi:** embedding dua crop orang sama lebih dekat (cosine) daripada beda orang — smoke test 10 frame MOT20-01.

### Phase 3 — TBSS scorer + training
- `scorer.py`: Linear(73→d_model) + `nn.TransformerEncoderLayer(d_model, nhead=4)` + Linear → sigmoid. **d_model default 64** (paper tidak menyebut; input cuma 73-d, tunable).
- `dataset.py`: FLTC (cache **kumpulan crop 224×224 uint8 per frame**, LRU cap ~2048 frame) + APS (pasangan max 50/frame dari GT MOT20-train; positif = GT id sama, negatif = beda id, seimbang).
- `train.py`: triplet(m=1.0) + BCE, Adam 1e-3, 20 epoch, 80/20.
- Triplet dibentuk dari pasangan APS: tiap positive pair → anchor/positive; negatif = embedding acak beda id (paper tidak merinci; pilihan kita). 
- **Verifikasi:** loss turun; akurasi BCE val > 90%; 1 fold selesai ≤ 3 jam di 4090.

### Phase 4 — CMOH + ASW lokal
- `memory.py`: buffer K=10 embedding per track (CMOH); saat track tidak dapat match → embedding = **mean buffer** (`a_ctx`), dipakai di input TBSS menggantikan embedding track terakhir. Tier-2: long-term store untuk track yang hilang lama/recurrent (hanya dipakai saat K=10 sudah tidak menutup — **modifikasi kontribusi** "hierarchical memory").
- ASW: paper = σ(N_occ/N) global satu skalar per frame; modifikasi kita = w per-track dari rasio oklusi track tsb (lokal) — **modifikasi kontribusi**.
- **Verifikasi:** IDSW fold-1 turun vs Phase 3 tanpa CMOH.

### Phase 5 — Eval lengkap + ablasi + laporan
- 4 fold leave-one-out MOT20-train (mean ± std) + zero-shot DanceTrack-val.
- Ablasi di fold-1: (a) IoU-only [=Phase 1], (b) +LAE, (c) +TBSS, (d) +CMOH, (e) +ASW-lokal [full] → tabel ala paper.
- **Ekspektasi ablasi (dari paper, MOT17/20 half-split):** LAE = lompatan terbesar; TBSS naik stabil di atas LAE; CMOH memangkas IDSW drastis; ASW cuma increment tipis. ⚠️ Angka absolut paper TIDAK sebanding protokol kita — lapor pola kontribusi relatif + jangan overclaim.
- FPS: ukur **tracking stage terpisah** dari pipeline penuh (detektor dominan, paper: YOLOX-S 26.8 GFLOPs vs asosiasi 0.6); crop diekstrak batch → satu tensor GPU (hindari loop crop CPU jadi bottleneck). Di 4090 (GPU mode) + PC rumah (CPU, kedua mode).
- Update `eval_results.csv` (reuse step_eval `--tracker lighttrack`) + tabel perbandingan OC-SORT/DiffMOT/lighttrack + update laporan Skenario B.

### Phase 6 — (Opsional, kalau waktu cukup) Fine-tune data kampus
- Rekam/ambil scene kampus, label deteksi (atau pseudo-label dari YOLO26), fine-tune LAE 5-10 epoch → ukur IDSW/IDF1 vs model MOT20-only. Ini bagian cerita "domain gap" di tesis.

## Orkestrasi run di kampus — modular, satu script, hasil otomatis terdokumentasi

`scripts/s2/run_skenario_b_lighttrack.py` (mirror pola `run_skenario_b_ocsort.py` — 1 orkestrator, step terpisah, resume aman):

```
# Env & data dicek dulu (1×, sebelum apa pun):
python scripts/s2/run_skenario_b_lighttrack.py --steps doctor
#  → cek: torch+cuda, torchvision mobilenet_v3_small, filterpy, scipy, data MOT20/DanceTrack/MOT17,
#    download pretrained MobileNetV3-Small (sekali), tulis laporan env ke lt_runs/doctor.txt

# Pipeline penuh (4 fold):
python scripts/s2/run_skenario_b_lighttrack.py --steps prepare,train,track,eval,report
#  → 1 perintah, berjalan malam hari di 4090; tiap step resume (output sudah ada → skip, kecuali --force)

# Ablasi fold-1 (setelah pipeline utama jalan):
python scripts/s2/run_skenario_b_lighttrack.py --steps ablation --fold 1
# → 5 config (ioU-only, +LAE, +TBSS, +CMOH, +ASW) → lt_runs/ablation_1.csv + tabel

# Ulang eval saja / satu fold:
python scripts/s2/run_skenario_b_lighttrack.py --steps track,eval --fold 2
```

Setiap step **idempotent** (ada output → skip; `--force` untuk ulang) dan **menulis run log** (timestamp, config, metrik) ke `experiments/s2_tracker/lt_runs/runs.yaml` (append). Artinya progres kampus otomatis tercatat — tinggal `git pull` di rumah untuk lihat.

## Test per fase (WAJIB lolos sebelum lanjut ke fase berikutnya)

| Fase | Perintah test | Lolos bila | Artefak yang dihasilkan |
|---|---|---|---|
| Semua | `--steps doctor` | semua cek PASS (torch/cuda/weights/data ada) | `lt_runs/doctor.txt` |
| 1 Skeleton | `--steps track --fold 1 --model none` di PC rumah (2 sekuens) | TrackEval jalan, HOTA > 0 (validasi pipeline), file output format MOT valid | `lighttrack_results/mot20/MOT20-01.txt` |
| 2 LAE | `--steps test --unit encoder` (smoke 10 frame MOT20-01) | cos(same-person) > cos(different); dim = 32; L2-norm | log + 1 assert |
| 3 TBSS | `--steps train --fold 1` (mini: 1 epoch) lalu `--steps test --unit scorer` | loss turun antar epoch; BCE val > 90% | `lt_models/sim_fold1.pth` + kurva loss |
| 4 CMOH+ASW | `--steps test --unit memory` (unit: celah 20 frame) + `--steps track --fold 1` | ID track **tidak berganti** setelah gap oklusi; IDSW fold-1 turun vs Phase 3 | log unit + `lighttrack_results/...` |
| 5 Eval+ablasi | `--steps eval` + `--steps ablation --fold 1` | 4 fold selesai; CSV 5 config terisi; pola relatif: LAE lompat terbesar, CMOH pangkas IDSW | `eval_results.csv`, `lt_runs/ablation_1.csv` |
| 6 Kampus FT | `--steps train --stage finetune` + `--steps track,eval` | IDF1/IDSW data kampus membaik vs model MOT20-only | `lt_models/ft_kampus.pth` + CSV |

Setiap unit test = **satu assert** (pola ponytail), bukan framework; dijalankan via `--steps test --unit <name>`. Dev/smoke test cukup di PC rumah (2 sekuens); pipeline penuh & training hanya di kampus.

## Artefak & dokumentasi otomatis

```
experiments/s2_tracker/
  lt_models/            # sim_fold{1..4}.pth, ablasi config, ft_kampus.pth
  lighttrack_results/{mot20,dancetrack}/   # output tracker format MOT (masuk TrackEval)
  lt_runs/              # doctor.txt, prepare_{fold}/stats, train_{fold}/loss.png+log,
                        # ablation_{1}/tabel, runs.yaml (run log append otomatis)
  eval_results.csv      # (dipakai bersama OC-SORT/DiffMOT — baris lighttrack di-append)
```

`--steps report` merangkum: metrik 4 fold (mean±std) + DanceTrack + tabel ablasi + FPS tracking → append ke `docs/reports/laporan-skenario-b-tracker.md` + `docs/PROGRESS.md` (pola yang sama seperti OC-SORT/DiffMOT). Dengan begitu kampus tinggal run, hasilnya sudah jadi bahan laporan — nggak ada step manual yang bisa terlewat.

## File yang berubah
- Baru: `src/lighttrack/**` (6 file), `scripts/s2/run_skenario_b_lighttrack.py`, `docs/panduan-skenario-b-lighttrack.md`.
- Diubah: `scripts/s2/run_skenario_b_ocsort.py` (sudah: `--tracker` param), `docs/plans/` (ini), `docs/PROGRESS.md`, `docs/reports/laporan-skenario-b-tracker.md`.
- Tidak disentuh: data, deteksi, hasil OC-SORT/DiffMOT, `patch_diffmot_eval.py`.

## Risiko & jebakan
1. **Angka tidak akan menembus paper (66.6 HOTA MOT20-test)** — protokol kita beda (train-protocol + deteksi sendiri). Yang dilaporkan: perbandingan relatif pada protokol sama. Jangan overclaim.
2. **Python 3.8 di kernel kampus** — tanpa `list[str]` dsb (sudah jadi kebiasaan di script s2).
3. **torchvision di jupyterhub-env**: pastikan `mobilenet_v3_small` tersedia (torch 2.0.1 → torchvision 0.15). Kalau API pretrained berubah, sesuaikan.
4. **FLTC VRAM**: cache crop 224² uint8 per frame + LRU cap (~2048 frame); jangan cache full-res (MOT20 1080p = ~8 MB/frame × 8.9k frame ≫ VRAM). uint8 = 4× lebih kecil dari float32.
5. **Leakage**: jangan pernah train di sekuens yang dieval (leave-one-out wajib). DanceTrack-val tidak boleh masuk training kalau mau dipakai zero-shot.
6. **ReID di CPU tidak realtime** — encodernya 0.5 GFLOPs/crop; di scene padat (>30 orang) CPU gagal. Makanya mode `USE_REID=false` sebagai fallback deployment. Sebutkan di laporan (jujur).

## Keputusan reimplementasi (kekosongan yang TIDAK dijelaskan paper — diputuskan oleh kita)

| # | Kekosongan paper | Keputusan kita | Alasan |
|---|---|---|---|
| 1 | d_model TBSS tidak disebut | default 64, tunable | input cuma 73-d; kecil sudah cukup |
| 2 | Pembentukan triplet dari pasangan APS tidak dirinci | dari tiap positive pair ambil negatif acak beda id | sederhana, stabil; hard mining opsional belakangan |
| 3 | "Soft IoU" disebut di prose, rumus pakai IoU biasa | pakai IoU biasa | rumus (Eq 5/10) lebih otoritatif; soft-IoU = varian kalau ada waktu |
| 4 | GFLOPs LAE 0.5 vs MobileNetV3-Small ~0.11 (torchvision) | pakai torchvision `mobilenet_v3_small` | lebih hemat, pretrained ImageNet siap pakai |
| 5 | Negatif sampling APS tidak dirinci | acak, seimbang dgn positif, max 50 pasangan/frame | match paper (Eq 1) |
| 6 | Threshold conf & max age track tidak disebut | conf ≥ 0.3, max age analog OC-SORT (lapor) | konsisten dgn pipeline OC-SORT |
| 7 | Formula EMA baseline tidak dirinci | EMA biasa di koordinat box (α=0.9) | cukup untuk smoothing; lapor |

## Estimasi
- Development: ~1.5–2 minggu part-time (Phase 1-4).
- Compute kampus: ±12 jam training (4 fold) + ±6 jam ablasi (fold-1) → 2 malam 4090.
- DiffMOT eval (satu perintah, 10 menit): `python scripts/s2/run_skenario_b_ocsort.py --steps eval --tracker diffmot` di kampus.

## Open questions
1. ~~MOT17 vs MOT20?~~ **Diputuskan: dua-duanya** (MOT17-train + MOT20-train; user download manual, pindah ke kampus via WinSCP). Ambil satu varian detektor per sekuens (gambar & GT identik antar DPM/SDP/FRCNN; yang beda cuma `det/`).
2. Phase 6 (fine-tune kampus) dijalankan atau tidak? Tergantung jadwal — sekarang punya dukungan teoritis (future work #3 paper).
3. Tracker versi kita dipakai di demo realtime Skenario C juga, atau OC-SORT tetap untuk demo? — keputusan di Phase 5 (siapa menang eval).
4. Ablasi penuh (5 config × fold-1) atau subset (mis. tanpa +TBSS individual)? — kalau waktu ketat, subset; pola kontribusi tetap terbaca.
