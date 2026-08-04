# Panduan Re-run MOT20 Full-Sequence (PC Rumah, Windows 11)

*Tanggal: 2026-08-04. Dipicu temuan 2026-08-04: output tracking MOT20 sebelumnya hanya
menutupi **sebagian frame** sekuens resmi (MOT20-01: 1–214 dari 429; MOT20-02: 1–1391 dari
2782) — angka evaluasi MOT20 di `eval_results.csv` bukan full-sequence dan **belum valid**
untuk dibandingkan dengan literatur. DanceTrack tidak terpengaruh (frame lengkap).*

**Tujuan:** jalankan ulang deteksi → tracking → evaluasi MOT20 atas SEKUENS LENGKAP, lalu
push hasilnya supaya laporan/figur bisa diperbarui.

---

## 0. Prasyarat

- Repo terbaru: `git pull` di `hibah-riset` (pastikan HEAD = `8412a17` atau lebih baru).
- Environment Skenario B sudah ada (`.venv-s2` dari panduan-skenario-b-oc-sort.md).
- Bobot `best.onnx` / `best.pt` Skenario A ada di `data/s2/weights/`.
- Semua perintah di **PowerShell** dengan venv aktif:

```powershell
cd hibah-riset
.\\.venv-s2\\Scripts\\Activate.ps1
```

---

## 1. LANGKAH 0 — Cek integritas data (WAJIB, jangan dilewati)

Penyebab truncation = dataset tidak lengkap saat run sebelumnya (`synth_seqinfo()` memakai
jumlah jpg sebagai `seqLength`, jadi semua tahap ikut terpotong). Cek dulu:

```powershell
$official = @{ "MOT20-01" = 429; "MOT20-02" = 2782; "MOT20-03" = 2405; "MOT20-05" = 3315 }
foreach ($s in $official.Keys) {
  $n = (Get-ChildItem "data\s2\mot20_hf\train\$s\img1\*.jpg").Count
  $ok = if ($n -eq $official[$s]) { "OK" } else { "!! KURANG" }
  "{0,-10} jpg={1,-6} resmi={2,-6} {3}" -f $s, $n, $official[$s], $ok
}
```

**Target: semua sekuens bertanda OK (429 / 2782 / 2405 / 3315).** Sumber angka: Tabel 1 paper
MOT20 (arXiv:2003.09003) dan README mirror `Lekim89/MOT20` — total training = 8.931 frame.

- Kalau semua OK → lanjut ke LANGKAH 1.
- Kalau ada yang KURANG → **jangan lanjut**; perbaiki data dulu (bagian 2), lalu ulangi cek.

> Cek juga file GT lengkap: `data\s2\mot20_hf\train\<seq>\gt\gt.txt` harus punya baris
> dengan frame terakhir = jumlah resmi (429/2782/2650/3327). Mirip pengecekan di atas
> dengan `(Get-Content ...\gt\gt.txt | ForEach-Object { ($_ -split ',')[0] } | Measure-Object -Maximum).Maximum`.

---

## 2. Kalau data kurang — download ulang (sekali)

MOT20 dari HF `Lekim89/MOT20` (mirror lengkap ber-track-ID; CDN, tanpa API rate-limit):

```powershell
$env:HF_HUB_DISABLE_XET = "1"   # hindari Xet API 429 (repo 13k file)
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Lekim89/MOT20', repo_type='dataset', local_dir='data/s2/mot20_hf')"
Remove-Item Env:HF_HUB_DISABLE_XET
```

- Download resume otomatis — kalau terputus, ulangi perintah yang sama.
- Estimasi MOT20 ±5 GB; selesai → ulangi cek LANGKAH 0.

Alternatif (kalau HF macet): unduh zip resmi dari motchallenge.net (MOT20.zip) → ekstrak
ke `data/s2/mot20_raw/` → sesuaikan struktur `train/MOT20-0X/img1` + `gt/gt.txt` — atau
pakai opsi B (Kaggle) di panduan-skenario-b-oc-sort.md, TAPI pastikan track ID ada
(mirror Kaggle sering kehilangan track ID).

---

## 3. LANGKAH 1 — Re-run full pipeline (--force)

Sekarang susun ulang seqinfo (akan memakai jumlah jpg yang BENAR), deteksi ulang, track
ulang, evaluasi ulang — satu perintah:

```powershell
python scripts/s2/run_skenario_b_ocsort.py --steps arrange,detect,track,eval --force
```

Apa yang terjadi (i5-12400F, CPU):

| Langkah | Isi | Estimasi |
|---|---|---|
| `arrange` | susun ulang sekuens + seqinfo.ini dari frame nyata + verify | 2–5 mnt |
| `detect` | YOLO fine-tune atas ±8.931 frame MOT20 (bukan 4.464) | 20–40 mnt |
| `track` | OC-SORT atas deteksi baru | 3–8 mnt |
| `eval` | TrackEval → `eval_results.csv` baru | 2–5 mnt |

Catatan:
- Gunakan bobot dan parameter yang SAMA dengan run baseline sebelumnya
  (default: `best.onnx`, `--track-thresh 0.3 --min-conf 0.3 --iou-thresh 0.3`) supaya
  perbandingan tracker-vs-tracker tetap sah. Jangan campur `.pt` dengan `.onnx`.
- Kalau ingin melihat setiap langkah berjalan: jalankan per langkah
  (`--steps arrange --force`, lalu `--steps detect --force`, dst) — hasilnya sama.

---

## 4. LANGKAH 2 — Verifikasi hasil (jangan langsung percaya)

1. **Frame count naik** — cek `experiments/s2_tracker/detection_stats.csv`: jumlah frame
   MOT20 total harus ±8.931 (429+2782+2405+3315), bukan 4.464 lagi.
2. **Cakupan track penuh** — baris terakhir `experiments/s2_tracker/ocsort_results/mot20/MOT20-02.txt`
   harus frame ≥ 2782. Di PowerShell:

```powershell
$last = Get-Content experiments\s2_tracker\ocsort_results\mot20\MOT20-02.txt | ForEach-Object { [int]($_ -split ',')[0] } | Measure-Object -Maximum
"frame terakhir MOT20-02: $($last.Maximum) (target: 2782)"
```

3. **Metrik masuk akal** — `experiments/s2_tracker/eval_results.csv` diperbarui. Angka bisa
   berubah (naik atau turun) vs sekuens terpotong — wajar; yang penting sekarang full-sequence.

---

## 5. LANGKAH 3 — Commit & push (biar VPS/kampus sinkron)

```powershell
git add experiments/s2_tracker/eval_results.csv experiments/s2_tracker/detection_stats.csv experiments/s2_tracker/ocsort_results/
git commit -m "perf: rerun MOT20 full-sequence (frame 429/2782/2650/3327) - baseline OC-SORT"
git push
```

Setelah push, beri tahu (chat/session berikutnya): **"rerun MOT20 selesai"** — saya akan
perbarui laporan, figur (density MOT20), dan menghapus warning koreksi dari
`docs/reports/laporan-skenario-b-tracker.md` + `docs/PROGRESS.md`.

---

## 6. Troubleshooting singkat

| Masalah | Solusi |
|---|---|
| `Activate.ps1` diblokir | `Set-ExecutionPolicy -Scope Process Bypass` lalu ulangi |
| `detect` error MemoryError | turunkan `--imgsz 480` (deteksi ulang) |
| Frame count masih pendek setelah download | venv lama? pastikan HF_HUB_DISABLE_XET=1 saat download, lalu cek LANGKAH 0 lagi |
| Ingin lebih cepat | export ONNX (`yolo export model=data/s2/weights/best.pt format=onnx`) + `--imgsz 640` |

---

## 7. Referensi

- Temuan truncation: `docs/reports/laporan-skenario-b-tracker.md` (catatan koreksi 2026-08-04)
- Orchestrator: `scripts/s2/run_skenario_b_ocsort.py` (step `arrange` = `synth_seqinfo()` memakai jumlah jpg nyata)
- Panduan awal: `docs/panduan-skenario-b-oc-sort.md`
