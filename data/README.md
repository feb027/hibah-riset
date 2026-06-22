# Datasets

Folder ini **tidak di-track git** (lihat `.gitignore`). Semua dataset diunduh
oleh script yang sesuai dan diletakkan di bawah `data/raw/<nama-dataset>/`.

## Tier 1 (sekarang)

Tidak butuh dataset besar. Pakai:

- **Sample video pendek CC0** (Pexels / Pixabay), diunduh otomatis oleh
  notebook `notebooks/01_smoke_test_detector.ipynb` dari URL publik.
- **Synthetic video** sebagai fallback — dihasilkan oleh notebook jika
  download gagal. Berisi persegi bergerak sebagai pengganti orang. Bukan
  untuk evaluasi, hanya untuk smoke test pipeline.

## Tier 2 (berikutnya)

### MOT17 (mini)
- Sumber: https://motchallenge.net/data/MOT17
- Ukuran: ~1.5 GB (semua sequence). Mini subset: ~150 MB (1 sequence).
- Alasan: benchmark tracking padat, RoI per sequence.
- Script: `python scripts/download_mot17_mini.py --out data/raw/mot17`
- ⚠️ License: research use; hormati terms of use MOTChallenge.
- ⚠️ Perhatian reviewer sebelumnya: angka statistik MOT17/MOT20/DanceTrack
  agar selalu dicocokkan dengan metadata di `docs/research/source-ledger.md`.

### Mall dataset (Chen et al., CVPR 2012)
- Sumber: http://personal.ie.cuhk.edu.hk/~ccloy/downloads_mall_dataset.html
- Ukuran: ~50 MB (frames + count labels).
- Alasan: people counting klasik dengan ground truth count per frame.
- Script: `python scripts/download_mall_dataset.py --out data/raw/mall`
- ⚠️ License: research use; hormati permintaan akses原作者.

### CrowdHuman (untuk S1 evaluator)
- Sumber: https://www.crowdhuman.org/
- Ukuran: ~15 GB (citra + anotasi).
- Alasan: deteksi manusia pada crowd + oklusi (S038).
- ⚠️ Tier 1 tidak butuh CrowdHuman; S1 quant butuh register dulu.

### DanceTrack (untuk S2 tracker)
- Sumber: https://dancetrack.github.io/
- Ukuran: ~10 GB.
- Alasan: tracker robustness pada motion kompleks (S037).
- ⚠️ License: research use; cek terms DanceTrack.

## Catatan penting

1. Folder `data/` adalah `.gitignore` — tidak boleh di-commit.
2. Setelah download, **jangan tulis ulang README dataset ini** dengan angka
   baru tanpa mencocokkan ke `source-ledger.md`. Reviewer akan reject.
3. Untuk klaim "real-time", wajib ukur latency di hardware target (bukan
   laptop dev tanpa GPU).
