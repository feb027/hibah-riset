# Konsep Fase 3 — Latih LAE+TBSS (Jun 2026-08-05)

> **Status: DIAPPROVE & DIIMPLEMENTASI (2026-08-05).** Keputusan user: ImageNet, d_model=64, batch 64, full run fold-1 semalam di kampus.
> Basis: catatan paper `docs/research/fulltext-notes/S014-lighttrack-reid.md` (formula + hyperparams asli) + hasil Fase 1-2 (encoder terverifikasi, margin kecil → training wajib).

## Tujuan
Mengubah LAE dari pretrained-ImageNet (margin +0.027, belum ReID) menjadi ReID terlatih, plus TBSS Transformer peer-scorer. Target degradasi: cosine same-person menembus margin >>, dan saat di-track HOTA/MOTA/IDF1 naik vs Fase 1 (IoU-only) pada protokol sama.

## Yang akan dibuat (3 modul baru; tracker.py Fase 1 TETAP TIDAK disentuh)

1. `src/lighttrack/scorer.py` — TBSS: `Linear(73 → d_model=64) → nn.TransformerEncoderLayer(64, nhead=4) → Linear → sigmoid`. Input x ∈ R^73 = `[b_t(4), b_{t-1}(4), IoU(1), a_t(32), a_{t-1}(32)]` (embedding = output LAE L2-norm). Output s ∈ [0,1].
2. `src/lighttrack/dataset.py` — FLTC + APS:
   - **FLTC**: cache per-frame tensor berisi **kumpulan crop 224×224 uint8** (BUKAN frame half-res — koreksi plan awal) + bbox GT + id. LRU cap ~2048 frame. uint8 = 4× lebih hemat dari float32 → cukup VRAM.
   - **APS**: dibangun dari **GT boxes** (kotak GT = hubungan track/person kotor bebas — suplementer lebih bersih daripada deteksi). Maks **50 pasangan/frame**: jaga sampel positif (id sama antar frame beda frame) seimbang 1:1 dgn negatif (id beda, frame sama). Total diharapkan ~135 ribu pasangan seperti paper.
3. `src/lighttrack/train.py` — pelatihan **LaEA + TBSS CTC tak bersama** gunakan **APS**:
   - loss = **triplet margin m=1.0** (pada embedding) + **BCE**(ŝ, y) (output TBSCS vs label pair).
   - triplet dibentuk: tiap positive pair → anchor + positive (embedding LAE crop); negative = embedding acak beda id dari frame berbeda (paper tak merinci → keputusan kita; hard-mining die-opsi belakangan).
   - **Augmentasi (dari paper): random flip 50 %, crop padding 10%, color jitter 0.2.** Benar: paper pakai; kita pakai di training crops saja — crop yang sama jadi kondisi training SPARSE, augmentasi bikin robust → margin naik.
   - **Adam lr=0.001**, **20 epoch**, **80/20 train/val**. Batch 64.
   - Normalisasi crop IN GAME: paper [0,1]; kita pakai **ImageNet** (konsisten w/ encodering Fase 2 yang sudah terverifikasi — backbone init pretrained ImageNet). Ini deviasi kecil yg bisa ditulis di dokumentasi.
4. **Data training**: **MOT17-train (1 variant/seq, `det/FRCNN`) + MOT20-train** (keputusan lama, momentum OK — MOT17 nambah di di uburrsity, aman vs leave-one-out MOT20). **Setiap fold: sekuens fold-i di-CLIP OUT dari training** (anti-leak) — hanya untuk busycessing MOT20; MOT17 cross full.

## Verifikasi (pass terukur, nggak sekadar "loss turun")

| Check | Target | Alat |
|---|---|---|
| Training loss turun | L_triplet + BCE → konvergen 20 epoch | training log / kurva |
| BCE val accuracy | > 90 % | eval akhir |
| Cosine margin (GT, ulangi Fase 2 terverif) | same-person − diff-person naik jelas vs +0.027 (target ≥ +0.15) | `verify_lighttrack_encoder.py` |
| 1 fold selesai | ≤ 3 jam @ RTX 4090 | wall-time |

*Jika yg dicek TARGET tidak tercapai → bukan PABBU, tapi sinyal konfigurasi (lr/batch/d_model) perlu tuning; berhenti sesuai jangka, tidak overfb.*

## Urutan kerja (tiap langkah berhenti selesai — komit, kirim dari kampus)

1. `scorer.py` + `_demo()` ala Fase 1 (input 73-d → skor [0,1], shape benar, jarak sjauh).
2. `dataset.py` + self-check: FLTC cache ben container benar; APS produce pair; durasi load 1 seq (< 30 dtk cached).
3. `train.py` + run **1 mini-epoch** di kampus (project-BPS backend internal, kasih snark) → log loss 1 baris/10 iter → validasi numerik naik.
4. **Full run fold-1** (MOT20 hold-out) pakai semua data → simpan `lt_trains/sim_fold1.pth` + kur. Backupet hasil verifikasi + hitung backlog ~2,5–5 jam @4090.
5. `run_lighttrack_mot.py` insert memuli LA + TBSC into tracker: fallback CPU tetep IoU-only (`USE_REID=false`) — kompat track.

## Risiko & celah (jujur)

1. **d_model=64, batch=64, color jitter — tak ada di paper** → tunable, di-TRend dengan ⭐ sebelum eksekusi; impact kerap grid A hipherparam gila — jangan.
2. **Normalisasi [0,1] vs ImageNet** → mengambil ImageNet demi konsistensi backbone; dapat ditunjuk-daftar dalam dokumentasi.
3. **Downtime 2,5–5 jam jadi backlog satu fold** — perlu run mandiri semalam (background adan kampus, jangan blokir hasil lain).
4. **Memos — ~135 rb pasangan APS**: 計算 fine di 4090, tidak perlu colab.

## Oke untuk eksekusi (tanda centang setelah kamu approve)

- [x] Modul scorer/dataset/train dibangun (scorer.py + _demo, dataset.py FLTC/APS + demo OK, train.py; py_compile OK lokal)
- [ ] Self-check + mini-epoch (jalankan di kampus — torch tidak ada di mesin rumah)
- [ ] Full fold-1 run di kampus (backlog semalam)
- [ ] Report + update plan doc / skill

## Yang aku butuh keputusanmu (kalau ada yang masih beda)

1. Normalisasi: **ImageNet (saran) atau [0,1] per paper?** → **KEPUTUSAN: ImageNet** (paper tidak memberi alasan [0,1]; konsistensi backbone pretrained + encoder Phase 2 terverifikasi).
2. d_model=64 & batch 64 **OK?** → **OK**.
3. Fold-1 full run semalam kampus **OK?** → **OK**. Perintah kampus:
   ```bash
   cd /home/if2011/hibah-riset  # atau lokasi repo kampus
   git pull
   # mini-run (uji pipa, 1 sekuens, 1 epoch, 60 frame):
   python src/lighttrack/train.py --seq-dirs data/s2/mot20_hf/train/MOT20-01 --out out/phase3_mini --epochs 1 --max-frames 60
   # full run fold-1 (semua data, 20 epoch) — background semalam:
   nohup python src/lighttrack/train.py \
     --seq-dirs data/s2/mot17_hf/train/MOT17-02:data/s2/mot17_hf/train/MOT17-04:data/s2/mot17_hf/train/MOT17-05:data/s2/mot17_hf/train/MOT17-09:data/s2/mot17_hf/train/MOT17-10:data/s2/mot17_hf/train/MOT17-11:data/s2/mot17_hf/train/MOT17-13:data/s2/mot20_hf/train/MOT20-02:data/s2/mot20_hf/train/MOT20-03:data/s2/mot20_hf/train/MOT20-04:data/s2/mot20_hf/train/MOT20-05 \
     --out out/phase3_fold1 --epochs 20 > out/phase3_fold1.log 2>&1 &
   ```
   *(fold-1 = MOT20-01 sebagai test; MOT17 full + MOT20-02..05 sebagai train. Cek jalur data sebenarnya di kampus: `ls data/s2/`)*

## Operasional pelatihan (add-on commit e55e706) — resume, timing, resource, progress

Semua built-in di `train.py`, tanpa dep baru (stdlib `/proc` + `torch.cuda` + `nvidia-smi`).

- **Resume dari tengah jalan**: tiap epoch simpan `out/<nama>/lighttrack_eN.pt` (state LAE + TBSC + optimizer + epoch). Kalau training terputus (logout/SSH putus/GPU timeout), lanjut tanpa mulai ulang:
  ```bash
  python src/lighttrack/train.py <args-komplit-sama> --resume out/phase3_fold1/lighttrack_e7.pt
  ```
  Log dibuka mode *append* (tidak menimpa) → riwayat lengkap. Pastikan `--seq-dirs`, `--seed`, `--max-frames` dsb **identik** dgn run awal agar split train/val konsisten (split deterministik dari `--seed`).
- **Durasi & ETA per epoch**: baris epoch diakhiri `[NNs | rata MMs/ep | ETA Xm]`.
- **Statistik resource per epoch** (CPU %, RAM avail/total GB, dan jika CUDA: GPU util % + VRAM alloc/total GB). Sumber: `cpu_percent()` dari delta `/proc/stat`, RAM dari `/proc/meminfo`, GPU dari `torch.cuda.memory_allocated` + `nvidia-smi`.
- **Progress intra-epoch**: print `ep=N [k/total] L_running=...` tiap ~10% frame, jadi terlihat jalan nggak (bukan kecewa di akhir).
- **Data terstruktur**: tiap epoch append 1 baris JSON ke `out/<nama>/train_stats.jsonl` (loss, bce_acc, cos, dt_s, eta_s, cpu/ram/gpu). Cocok utk plot kurva / isi dokumen. Header metadata (args + timestamp) ditulis sekali di awal `train.log` & `train_stats.jsonl`.

**Monit-nya (SSH terpisah / terminal lain):**
```bash
tail -f out/phase3_fold1.log                       # baris epoch + progress
tail -f out/phase3_fold1/train_stats.jsonl          # 1 JSON/epoch utk plotting
nvidia-smi                                          # util GPU & VRAM real-time
```