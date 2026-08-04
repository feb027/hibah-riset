# Phase 10 — Skenario C: Evaluasi Counting Logic terintegrasi Tracker

*Tanggal: 2026-08-04. Status: KONSEP (belum dieksekusi). Basis: hasil Skenario B full-sequence sudah valid.*

## 1. Tujuan

Membuktikan logika hitung (*counting logic*) bekerja pada **output tracking nyata** — bukan lagi data
sintetik — dan mengukur akurasinya secara kuantitatif. Sesuai arah proposal (YOLO26 + tracker +
*advanced counting logic*):

1. Validasi State Machine + debouncing (`core/counting/`) pada trajectory OC-SORT hasil Skenario B.
2. Kuantifikasi akurasi counting: **MAE, error %**, over/under-count per arah (IN/OUT).
3. **Dekomposisi sumber error counting**: deteksi vs tracking vs logika hitung (dengan counterfactual GT-track).
4. Fondasi **tracker-agnostic** — pipeline counting membaca file track format MOT, sehingga saat
   DiffMOT selesai (GPU kampus) tinggal tukar path, tanpa ubah kode counting.

## 2. Status saat ini (fakta dari repo)

| Komponen | Status | Lokasi |
|---|---|---|
| `PeopleCounter` (state machine, cooldown=30) | Ada, API siap | `core/counting/counter.py` |
| `LineCrossDetector`, `PolygonDetector` | Ada | `core/counting/detector.py` |
| Uji logika hitung | **HANYA data sintetik** (3 orang + jitter) → naive 11 vs state machine 4 | `scripts/experiments/ablation_counting_logic.py` |
| Track OC-SORT MOT20 (full, 8.931 frame) | Ada | `experiments/s2_tracker/ocsort_results/mot20/*.txt` |
| Track OC-SORT DanceTrack (25.508 frame) | Ada | `experiments/s2_tracker/ocsort_results/dancetrack/*.txt` |
| GT MOT20 (9 kolom, class 1=pedestrian, vis) | Ada | `data/s2/mot20_hf/train/*/gt/gt.txt` |
| GT DanceTrack (8 kolom) | Ada (PC rumah) | layout DanceTrack |

Catatan penting: hasil "11 vs 4" di `experiments/ablation_counting.png` adalah bukti konsep pada
lintasan buatan, **belum pernah diuji pada trajectory tracker sungguhan** — klaim "-60% over-counting"
di `presentasi_progres_counting.md` belum terverifikasi di data real.

## 3. Data & GT

- **Input track**: `ocsort_results/{mot20,dancetrack}/<seq>.txt` — format MOT `frame,id,x,y,w,h,1,-1,-1,-1`.
- **GT**: MOT20 `gt.txt` 9 kolom (frame,id,bb,mark,class,vis); DanceTrack 8 kolom.
- **Filtering GT wajib**: hanya `class==1` (pedestrian); distraktor (`class==2`, e.g. kursi roda di
  MOT20) diabaikan. `vis<1` (teroklusi) dicatat proporsinya sebagai keterbatasan, tidak dibuang dulu.
- **Count GT** diturunkan dengan menjalankan *counter yang sama* pada **trajectory GT** (ID stabil →
  cooldown nyaris tak berpengaruh) → ini "true count" per arah per interval.

## 4. Desain eksperimen

### 4.1 Konfigurasi (wajib dicatat, reproducible)
- **Garis virtual per sekuens**: tetap, posisi ditentukan sekali per sekuens lalu di-freeze
  (default: vertikal di 1/3 lebar frame; alternatif horizontal untuk MOT20-03/05 yang kamera
  miring). Disimpan `scripts/counting/configs/<seq>.yaml` — angka absolut bergantung posisi garis,
  jadi **komparasi A vs B hanya sah pada garis yang sama**.
- **Interval evaluasi**: per sekuens + sub-interval 300 frame (melihat dinamika error sepanjang video).

### 4.2 Variabel
| Label | Deskripsi |
|---|---|
| A | Naive: hitung tiap persilangan trajectory–garis (baseline rentan jitter) |
| B | State machine + cooldown 30 (default sekarang) |
| B-10 / B-60 / B-120 | Sensitivitas cooldown (10/60/120 frame) |
| GT-track | Counterfactual: counter dijalankan pada **trajectory GT** → memisahkan kontribusi tracker |

### 4.3 Metrik (custom, didokumentasikan eksplisit)
- `MAE_count = mean(|count_pred - count_GT|)` per arah & total, per interval.
- `err% = MAE / count_GT`; breakdown **over vs under**.
- `RMSE` per interval; agregat dataset tertimbang count GT.
- Analisis korelasi error counting vs IDSW per sekuens (menguji hipotesis: asosiasi rapuh →
  count salah) dan dekomposisi: `err(OC-SORT) = err(GT-track) + err(tracker)`.

## 5. Pipeline (skrip baru, `scripts/counting/`)

1. `configs/<seq>.yaml` — garis + interval.
2. `eval_counting.py` (orchestrator, CLI `--tracker ocsort|gt --seq ... --model A|B|B-60 ...`):
   baca track/GT → replay per frame → counter → simpan count series + metrics.
3. `gt_count.py` — ekstraksi count GT (jalankan counter pada GT trajectory).
4. Output: `experiments/s3_counting/{count_metrics.csv, series/<seq>_<model>.csv, figs/*.png}`.
5. Video overlay counting (reuse gaya `render_demo_video.py`): frame + garis + count header
   (IN/OUT/total) untuk bahan presentasi.
6. **Tracker-agnostic by construction**: input hanya format MOT txt → DiffMOT nanti drop-in.

## 6. Deliverables

- `experiments/s3_counting/` (metrics, series, figur, video demo)
- `docs/reports/laporan-skenario-c-counting.md` (hasil + keterbatasan, format laporan B)
- Review brutal `docs/reviews/` (workflow wajib), PROGRESS.md, commit+push.

## 7. Risiko & keterbatasan (diakui sejak awal)

1. **Posisi garis memengaruhi absolut** — publikasi angka hanya sebagai perbandingan relatif
   antar-model pada garis sama, plus MAE per sekuens.
2. **GT oklusi MOT20** (`vis<1`): orang yang "hilang" saat melintas garis → GT count bisa
   undercount sendiri; dilaporkan sebagai interval error bar, bukan disembunyikan.
3. **Bukan metrik standar MOT** — didefinisikan sendiri; ditulis eksplisit di laporan.
4. Komparasi counting dua tracker (OC-SORT vs DiffMOT) **menyusul** setelah DiffMOT jalan.
5. DanceTrack: beberapa sekuens penampilan identik → GT crossing di garis tertentu jarang;
   agregat 25 sekuens mengurangi noise.

## 8. Urutan kerja

- **C0** — konfigurasi garis + ekstraksi count GT + validasi visual (render GT + garis,
  cek count masuk akal sebelum lanjut).
- **C1** — eval Model A vs B (default) pada semua sekuens OC-SORT → metrik awal.
- **C2** — grid cooldown (10/60/120) + dekomposisi error (GT-track vs OC-SORT-track).
- **C3** — video demo counting + laporan + review + commit.
- *(C4 — ulang dengan DiffMOT track, setelah Skenario B selesai semua.)*

Estimasi: C0–C2 murni CPU di PC rumah (replay logika ringan; 8.931+25.508 frame ≈ menit per
konfigurasi); C3 menambah render video.

## 9. Keputusan yang diminta (sebelum implementasi)

1. **Skenario counting**: mulai dari *line crossing* (pintu masuk/keluar) — atau langsung juga
   *zone counting* (ROI, sudah ada `PolygonDetector`)?
2. **Posisi garis**: default vertikal 1/3 lebar per sekuens — atau mau ditentukan manual dengan
   referensi visual (lebih akurat, sedikit lebih lama)?
3. **Arah**: evaluasi IN/OUT terpisah (cocok narasi "ruang publik: masuk vs keluar") — setuju?
