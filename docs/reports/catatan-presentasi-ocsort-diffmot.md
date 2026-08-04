# Catatan Presentasi — OC-SORT & DiffMOT (Skenario B)

*Tanggal: 2026-08-04. Tujuan: bahan penjelasan untuk presentasi progres — dari dasar (biar presenter
paham betul) sampai perbandingan dua tracker. Sumber: fulltext-notes S024 (OC-SORT, CVPR 2023) dan
S021 (DiffMOT, CVPR 2024) + hasil eksperimen kita.*

---

## 1. Konteks: dari deteksi ke tracking

Pipeline sistem kita punya 3 tahap:

```
deteksi (YOLO26)  →  tracking (OC-SORT / DiffMOT)  →  counting (Skenario C)
"ada orang di sini"   "orang yang sama ini tadi di sana"   "berapa yang lewat garis"
```

- **Deteksi** menjawab: di frame ini, di mana kotak orangnya? Tapi kotak di frame 1 dan frame 2
  belum tahu mana yang orang yang sama.
- **Tracking** menjawab: kotak-kotak antar-frame itu disambungkan menjadi **identitas (ID) yang
  stabil**. Inilah yang membuat counting masuk akal — tanpa ID stabil, orang yang sama bisa dihitung
  dua kali (double-count) atau terlewat.
- **Counting** (Skenario C) memakai ID stabil itu untuk menghitung perlintasan garis.

> Analogi: deteksi itu "foto per detik", tracking itu "menyatukan foto-foto menjadi satu cerita
> per orang". Kalau ceritanya salah sambung (ID berubah), laporan jumlah orangnya ikut salah.

## 2. Fondasi: SORT — tracker klasik (2016)

SORT (Simple Online and Realtime Tracking) adalah pola dasar semua tracker berbasis deteksi modern:

1. **Prediksi**: filter Kalman memperkirakan posisi berikutnya tiap objek (asumsi: gerak
   ~kecepatan konstan/linear).
2. **Asosiasi**: kotak hasil deteksi dicocokkan dengan prediksi memakai kemiripan **IoU**
   (tumpang-tindih kotak) + algoritma Hungarian (pencocokan optimal).
3. **Update**: yang cocok dipakai mengoreksi prediksi; yang tidak cocok → track baru / track mati.

Kelebihan: sangat cepat, online, tanpa model penampilan. Kelemahan: rapuh terhadap dua hal yang
justru dominan di kerumunan publik — **oklusi** dan **gerak non-linear**.

## 3. Kenapa SORT gagal (masalah yang dijawab OC-SORT)

Filter Kalman mengasumsikan gerak hampir linear. Dua musuh:

1. **Oklusi** — orang ketutupan objek lain beberapa frame → tidak ada pengamatan → Kalman melakukan
   "update kosong" dan mempercayai perkiraannya sendiri → **error menumpuk** setiap frame tanpa
   koreksi.
2. **Gerak non-linear** — belok tiba-tiba, berhenti, saling papasan → asumsi kecepatan konstan
   meleset jauh dari kenyataan.

Saat keduanya terjadi bersamaan, track salah sambung: orang yang sama diberi ID baru (ID switch),
atau track mati-hidup berkali-kali. Paper OC-SORT (Cao dkk., CVPR 2023) menyebut tiga kelemahan
SORT: sensitif terhadap noise estimasi, error membesar selama periode tanpa pengamatan, dan desain
yang *estimation-centric* — memperpanjang track memakai perkiraan, bukan fakta.

## 4. OC-SORT — ide inti dan 3 modul

**Ide inti**: pindah dari *estimation-centric* ke *observation-centric* — setiap kali objek muncul
kembali, kesalahan Kalman yang menumpuk **dikoreksi memakai pengamatan (deteksi) nyata**, bukan
diteruskan sebagai perkiraan.

> Analogi presentasi: SORT seperti orang menutup mata dan meneruskan langkah dari perhitungan
> sendiri; OC-SORT setiap beberapa langkah **membuka mata** dan menyesuaikan langkah dengan
> kenyataan.

Tiga modul (hafalkan urutan ini):

**a. ORU — Observation-Centric Re-Update**
Track hilang (oklusi) lalu muncul lagi. OC-SORT tidak langsung meneruskan; ia **menelusuri balik
interval kehilangan**, membuat lintasan virtual antara pengamatan terakhir dan pengamatan yang
membangunkannya kembali, lalu **menjalankan ulang prediksi/update** pada periode itu untuk
mengoreksi parameter Kalman. Efek: error tidak dibawa-bawa ke depan.

**b. OCM — Observation-Centric Momentum**
Konsistensi arah gerak ditambahkan ke biaya asosiasi. Bedanya dengan versi klasik: **arah dihitung
dari pengamatan nyata** (posisi deteksi beberapa frame terakhir), bukan dari estimasi Kalman yang
berisik. Pada implementasi paper: dihitung dari pengamatan berselang `Delta t = 3` frame, bobot
`lambda = 0.2`. Paling terasa manfaatnya di gerak rumit (DanceTrack).

**c. OCR — Observation-Centric Recovery**
**Kesempatan kedua**: deteksi yang belum tersambung di asosiasi utama dicocokkan sekali lagi dengan
track yang baru saja hilang. Menolong untuk oklusi singkat dan kasus orang berhenti/diam.

**Alur per frame (yang kita jalankan):**
```
deteksi YOLO26 → filter conf (≥0.3) → tracker.update_public(boxes)
   ├─ Kalman predict
   ├─ asosiasi IoU + Hungarian (dengan biaya OCM)
   ├─ OCR untuk yang belum cocok
   └─ ORU saat track lama re-activated
→ keluaran: [x1,y1,x2,y2,id]
```
Parameter yang kita pakai (identik run Skenario B): `track-thresh 0.3, min-conf 0.3, iou 0.3,
delta-t 3, min-hits 3, max-age 30, inertia 0.2`.

**Kenapa tanpa ReID (Re-Identification)?** OC-SORT murni geometri (IoU + momentum) — tidak
mempelajari penampilan orang. Inilah alasan ia **ringan** (paper: 793 FPS *tracking stage* di CPU;
di data kita ±54 FPS) dan bisa jalan di CPU. Sekaligus batasnya: saat penampilan mirip dan gerak
sulit, asosiasi geometri saja lemah.

## 5. Metrik MOT — cara baca hasil kita

| Metrik | Arti singkat | Hasil kita (MOT20-train, deteksi YOLO26 sendiri) |
|---|---|---|
| **HOTA** (0–100) | keseimbangan akurasi deteksi × asosiasi; metrik utama | **36,51** |
| **MOTA** (0–100) | FP + FN + ID switch dibagi jumlah GT | **55,98** |
| **IDF1** (0–100) | seberapa benar ID dipertahankan | **42,88** |
| **IDSW** | jumlah kali ID berganti | **14.293** (±1,6/frame) |

- MOT20-train: 4 sekuens, **8.931 frame**, kepadatan ekstrem (rata-rata 179 deteksi/frame, puncak
  272). IDSW tinggi di sini = "asosiasi rapuh di kerumunan" — temuan utama laporan B.
- DanceTrack-val: **HOTA 28,39 · MOTA 71,38 · IDF1 26,63** — penampilan seragam + gerak non-linear
  membuat asosiasi geometri murni paling lemah. **Inilah bukti celah risetnya.**

> ⚠️ Konteks jujur (wajib disampaikan): angka ini memakai **deteksi kita sendiri** (YOLO26
> fine-tune CrowdHuman), bukan deteksi publik YOLOX seperti di paper OC-SORT. Maka **tidak boleh
> dibandingkan 1:1 dengan leaderboard**. Yang valid: perbandingan relatif antar tracker pada
> deteksi yang sama — itulah protokol "deteksi sama" (aturan emas) di Skenario B, dan DiffMOT
> nanti juga akan dijalankan dengan deteksi kita.

## 6. DiffMOT — apa bedanya (CVPR 2024)

DiffMOT tetap *tracking-by-detection* (deteksi + prediksi + asosiasi), tapi mengganti **prediktor
gerak**:

- **Kalman (OC-SORT)** = asumsi linear, satu perkiraan titik.
- **D²MP (DiffMOT)** = model difusi yang **belajar distribusi gerak nyata** dari data.

**Cara kerja D²MP (Decoupled Diffusion-based Motion Predictor):**
1. Gerak didefinisikan sebagai **perubahan kotak** antar frame: `(Δpusat_x, Δpusat_y, Δlebar,
   Δtinggi)`.
2. Prediksi gerak diperlakukan sebagai masalah **generatif denoising**: dari noise, model
   merekonstruksi gerak yang paling mungkin, **dikondisikan pada riwayat gerak objek** (5 frame
   terakhir, `n=5`) yang diekstrak jaringan self-attention (HMINet).
3. **Decoupled diffusion** memecah proses noise menjadi dua sub-proses sehingga cukup **satu
   langkah sampling** → tetap cepat (bukan diffusion lambat seperti di gambar).

> Analogi presentasi: OC-SORT menebak "orang ini akan lurus terus" (garis). DiffMOT belajar dari
> ribuan contoh gerak orang sungguhan — belok, berhenti, zig-zag — lalu "menggambar ulang" gerak
> yang paling masuk akal dari noise, seperti AI yang mengingat pola gerak manusia.

**Asosiasi DiffMOT** bergaya ByteTrack: deteksi skor tinggi dicocokkan dulu (biaya = jarak ReID +
IoU), deteksi skor rendah menyusul (biaya IoU). Jadi DiffMOT **memakai ReID** — mahal secara
komputasi tapi kuat saat penampilan bisa dibedakan.

**Angka paper (RTX 3090, deteksi YOLOX):**
| Dataset | HOTA | IDF1 | FPS |
|---|---|---|---|
| DanceTrack (YOLOX-X) | 62,3 | 63,0 | 22,7 |
| DanceTrack (YOLOX-S) | 53,3 | — | 30,3 |
| SportsMOT (train-only) | 72,1 | 72,8 | — |
| MOT17 (private det) | 64,5 | 79,3 | — |

> ⚠️ Konteks: 22,7 FPS itu di **GPU RTX 3090** — bukan bukti bisa realtime di CPU/edge. Dan angka
> itu pakai deteksi YOLOX, jadi lagi-lagi tidak bisa dibandingkan langsung dengan hasil kita.

## 7. Perbandingan langsung: OC-SORT vs DiffMOT

| Aspek | OC-SORT (CVPR 2023) | DiffMOT (CVPR 2024) |
|---|---|---|
| Prediksi gerak | Kalman, asumsi linear | D²MP difusi, belajar non-linear |
| Asosiasi | IoU + momentum (OCM) | IoU + **ReID** (gaya ByteTrack) |
| Komputasi | Ringan: 793 FPS (tracking, CPU, paper); ±54 FPS di data kita | Berat: 22,7 FPS (GPU 3090, paper) |
| Kuat di | Oklusi singkat, murah, real-time CPU | Gerak non-linear, papasan, DanceTrack |
| Lemah di | Gerak non-linear + penampilan seragam (DanceTrack IDF1 26,6 di kita) | Butuh GPU; kompleksitas; dependensi ReID |
| Peran di proposal | **Baseline efisien** / fallback (CPU, edge) | **Fokus utama robust** (GPU) |
| Status kita | ✅ SELESAI (angka valid) | ⏳ menyusul (GPU kampus) |

**Satu kalimat pembeda untuk slide:**
> OC-SORT = pelacak murah yang mengoreksi kesalahannya memakai pengamatan (bagus untuk oklusi
> singkat dan CPU). DiffMOT = pelacak yang *belajar memprediksi gerak non-linear* dengan model
> difusi + ReID (lebih akurat di gerak rumit, tapi butuh GPU). Bukan pengganti — dua-duanya
> dipertahankan sebagai **perbandingan adil pada deteksi yang sama**.

## 8. Kenapa dua-duanya? (logika eksperimen Skenario B)

- Aturan emas MOT: membandingkan tracker hanya sah bila **deteksi identik**. Kita sudah punya hasil
  OC-SORT dengan deteksi YOLO26 kita; DiffMOT nanti dijalankan dengan deteksi yang sama.
- Tujuan bukan "siapa menang", tapi **memetakan trade-off**: kapan tracker ringan cukup (murah,
  CPU), kapan perlu tracker berat (kerumunan dengan gerak sulit) — ini langsung menentukan arsitektur
  deployment di Skenario D (CPU/edge vs GPU).
- Hipotesis yang diuji: pada sekuens gerak non-linear (DanceTrack), DiffMOT seharusnya mengurangi
  ID switch → **counting lebih akurat** (Skenario C akan membuktikannya dengan metrik count).

## 9. Narasi saat demo video diputar

1. "Kotak berwarna = ID. Warna stabil = orang yang sama terus dilacak."
2. "Perhatikan saat orang lewat di belakang orang lain: kalau warna berubah, itu ID switch — orang
   yang sama disangka baru. Ini biang double-counting."
3. "Garis kuning + angka IN/OUT = counting logic (Skenario C) yang memakai ID stabil."
4. "HUD FPS = biaya pipeline; terlihat deteksi yang dominan, tracking-nya murah."

## 10. FAQ yang mungkin ditanyakan dosen

**Q: Kenapa tidak DeepSORT saja?**
A: DeepSORT butuh ReID (model penampilan) yang mahal di CPU. OC-SORT membuktikan koreksi berbasis
pengamatan saja sudah jauh lebih tangguh dari SORT — baseline yang fair dan ringan. DiffMOT-lah
yang nanti membawa ReID + prediksi belajar, di jalur GPU.

**Q: Kalau DiffMOT lebih baik, kenapa OC-SORT dulu yang dilaporkan?**
A: Urutan praktis: baseline ringan bisa langsung dieksekusi di CPU rumah tanpa GPU, memberi angka
pembanding sejak awal; DiffMOT butuh environment GPU kampus (lagi disiapkan). Laporan B = baseline
selesai dan valid.

**Q: Kenapa angka kita lebih rendah dari paper OC-SORT?**
A: Karena deteksi berbeda — paper pakai deteksi publik YOLOX, kita pakai YOLO26 fine-tune sendiri.
Bukan perbandingan yang sah; yang sah adalah relatif antar tracker pada deteksi sama (akan
dituntaskan setelah DiffMOT jalan).

**Q: "Real-time" klaim yang mana?**
A: 793 FPS OC-SORT = *tracking stage only* (tanpa deteksi). End-to-end kita di CPU ±20–23 FPS
(YOLO26s) — deteksi adalah bottleneck. DiffMOT 22,7 FPS = GPU 3090 termasuk deteksi YOLOX-X. Kedua
angka punya konteks hardware masing-masing.

**Q: Bagaimana DiffMOT "belajar gerak"?**
A: Dari riwayat 5 frame gerak tiap objek, model difusi (HMINet + one-step sampling) merekonstruksi
distribusi gerak berikutnya — bukan tebak garis lurus, tapi pola gerak yang pernah dilihatnya di
data latih (DanceTrack, SportsMOT).

## 11. Klaim yang BOLEH dan TIDAK BOLEH (safety untuk reviewer)

✅ BOLEH:
- "OC-SORT mereformulasi SORT dari sudut pandang observation-centric dengan ORU, OCM, OCR untuk
  mengurangi akumulasi error Kalman saat oklusi."
- "Paper melaporkan 700+/793 FPS untuk tahap tracking saja di CPU bila deteksi sudah tersedia."
- "DiffMOT mengganti prediksi linear Kalman dengan prediktor gerak difusi ter-dekoupled (D²MP),
  melaporkan HOTA 62,3/IDF1 63,0 di DanceTrack (YOLOX-X, 22,7 FPS, RTX 3090)."
- "Angka kami valid sebagai perbandingan relatif antar tracker pada deteksi yang sama."

❌ TIDAK BOLEH:
- Mengklaim FPS OC-SORT termasuk deteksi.
- Mengklaim OC-SORT/DiffMOT menyelesaikan counting, line crossing, atau double-counting.
- Membandingkan angka kami langsung dengan leaderboard paper (deteksi berbeda).
- Mengklaim 22,7 FPS DiffMOT menjamin realtime di perangkat target.
- Menggeneralisasi hasil DanceTrack/SportsMOT langsung ke CCTV ruang publik tanpa validasi.

## 12. Referensi

- **S024** — Cao, Pang, Weng, Khirodkar, Kitani. *Observation-Centric SORT: Rethinking SORT for
  Robust Multi-Object Tracking*. CVPR 2023, pp. 9686–9696. arXiv:2203.14360.
- **S021** — Lv, Huang, Zhang, Lin, Han, Zeng. *DiffMOT: A Real-time Diffusion-based Multiple
  Object Tracker with Non-linear Prediction*. CVPR 2024, pp. 19321–19330. arXiv:2403.02075.
- Laporan hasil: `docs/reports/laporan-skenario-b-tracker.md`; demo: `experiments/s2_tracker/demo/`.
