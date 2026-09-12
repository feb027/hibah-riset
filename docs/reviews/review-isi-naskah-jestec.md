# Review ISI Naskah JESTEC — People Counting (RANCAGE)
**Fokus review: isi/konten ilmiah saja.** Format, bahasa, typo, template, metadata, penomoran sitasi, dan daftar gambar **tidak** dinilai di dokumen ini (sudah ditangani di `review-jestec-manuscript-full.md`). Bahasa Indonesia dianggap wajar karena akan diterjemahkan.
**Dibaca:** `manuscript-v1.pdf` + `docs/journal/*.md` + `docs/reports/*.md` + kode `core/counting/{counter,detector,models}.py`
**Tanggal:** 12 September 2026

---

## VERDICT (isi): **MAJOR REVISION — 52/100**

Argumen inti naskah berdiri dan angkanya nyata. Yang membuatnya belum layak adalah **metrik hitung tidak didefinisikan**, **janji uji di Method yang tidak dilaporkan di Results**, **ablation yang tidak mengisolasi mekanisme**, dan **satu klaim Method yang tidak sesuai dengan kode aktual**.

| Aspek isi | Bobot | Skor |
|---|---|---|
| Metodologi & definisi metrik | 20 | 11 |
| Validitas hasil & ketegasan statistik | 20 | 10 |
| Konsistensi klaim ↔ bukti (termasuk kode) | 20 | 9 |
| Kebaruan & positioning | 15 | 6 |
| Related work & ketajaman gap | 10 | 7 |
| Discussion & limitasi | 15 | 9 |
| **Total** | 100 | **52** |

---

## A. RUSAK — blocker konten

**K1. Metrik hitung tidak pernah didefinisikan. Ini yang paling pertama ditembak reviewer.**
§4.3 melaporkan "galat 13,08% / 16,71% / 22,38% / 53,03%" dan "MAE 4,41 / 6,34 / 8,37 / …" tanpa pernah menjelaskan: rumus galatnya apa (MAPE agregat? rata-rata galat per sekuens?), GT hitung diperoleh dari mana, dan di mana garis virtual diletakkan.
Padahal jawabannya ada di repo, `docs/journal/3-method.md`: *"ground truth hitung diturunkan dengan menjalankan counter yang sama pada lintasan ground truth"* dan *"MAE, galat relatif, RMSE per interval, serta pemisahan over-count dan under-count"*. **Kalimat ini hilang saat versi Word disusun.**
→ **Solusi:** pindahkan definisi itu ke §3.4 + tulis rumus eksplisit. Lalu tambahkan satu kalimat yang justru memperkuat posisi Anda: metrik ini mengukur **sensitivitas counting logic terhadap galat tracking**, bukan akurasi absolut terhadap jumlah orang sebenarnya di lapangan. Menyatakan ini sendiri lebih baik daripada dituduh reviewer.
→ Sekalian deklarasikan konvensi tanda: arah IN/OUT bergantung pada urutan dua titik yang mendefinisikan garis virtual (`A = virtual_line.start`, `B = virtual_line.end`, cross product `(B−A) × (D−C) > 0` → IN). Tanpa ini, hasil tidak bisa direplikasi.

**K2. Tiga janji di Method yang tidak ada di Results.**
| Dijanjikan di §3.4 | Ada di §4? |
|---|---|
| S1 membandingkan konfigurasi **zero-shot vs fine-tuned** | ❌ nol angka |
| S4 mengukur **P90, P95, P99 tail latency** | ❌ hanya menyebut "Gambar 8" |
| S4 mengukur **perangkat edge AMD RX 6600 (DirectML)** | ❌ nol angka |
Padahal datanya lengkap di `docs/reports/laporan-skenario-d-realtime.md`: `P90 29,50 / P95 32,10 / P99 36,40 ms` (RTX 4090), `OC-SORT edge total 32,57 ms = 30,7 FPS` vs `Deep-OC-SORT edge 83,01 ms = 12,0 FPS`.
→ **Solusi:** tambahkan tabel tail-latency + tabel edge. Klaim §4.6 *"pada perangkat edge, OC-SORT lebih sesuai"* sekarang menggantung tanpa bukti. Dan hasil edge-nya sendiri menarik: Deep-OC-SORT **gagal** real-time di edge (12 FPS) — tulis apa adanya, itu temuan, bukan kelemahan yang disimpan.

**K3. Bagian 5 Conclusions kosong.** Bukan soal format — naskah tanpa kesimpulan tidak punya jawaban atas pertanyaan yang diajukan di Introduction. Tulis 4–6 poin yang menjawab langsung: apakah counting logic menyelesaikan masalah double-counting (ya, dengan batas), apakah tracker terbaik = tracker terpilih (tidak, dan itu keputusan desain), apakah sistem memenuhi anggaran 33,3 ms (ya di GPU, tidak dengan Deep-OC-SORT di edge).

**K4. Abstract tidak memuat isi penelitian.** Yang ada di Abstract adalah abstrak template tentang bentuk proyektil supersonik. Isinya nol percent tentang naskah ini. → Tulis ulang: masalah, pendekatan, 3–4 angka kunci, kontribusi.

**K5. Rumusan masalah, tujuan, dan kontribusi tidak ada.** Introduction langsung melompat dari masalah ke "penelitian ini mengembangkan RANCAGE". Draft repo (`docs/handoff/draft-sections-clean.md`) punya tiga pertanyaan penelitian + tujuan + ruang lingkup (TKT 3–4) — **hilang saat pemadatan**. Akibatnya reviewer tidak punya patokan untuk menilai apakah naskah menjawab apa yang dijanjikan.
→ **Solusi:** kembalikan 3 pertanyaan penelitian + 1 paragraf kontribusi yang spesifik: (i) ablasi counting logic vs naive pada deteksi identik, (ii) peta trade-off cooldown/threshold antara over-count dan under-count, (iii) dekomposisi latensi lintas perangkat. Jangan tulis kontribusi generik "integrasi deteksi-tracking-counting" — DeepStream `nvdsanalytics` sudah melakukan itu sejak lama, dan reviewer akan menyebutnya.

**K6. Klaim "akurasi hitung" ditarik lebih jauh dari yang dibuktikan (validitas eksternal).**
Naskah menguji di MOT20 (kerumunan padat, dalam ruangan) dan DanceTrack (gerak non-linear, penampilan seragam), memakai garis hitung yang diletakkan penulis sendiri, dengan GT yang dihasilkan counter itu sendiri. Yang **tidak** diuji: pintu masuk/keluar ruang publik nyata, arah arus berarah, kerumunan berdiri dekat garis, kamera miring/perspektif jauh, dan fps selain benchmark. §4.6 mengakui "satu seed" dan "deteksi offline", tapi **tidak** mengakui bahwa tidak ada satu pun uji pada skenario target (stasiun/kampus/pusat perbelanjaan — yang justru disebut di Introduction sebagai motif).
→ **Solusi:** tambahkan satu sub-bab limitasi eksplisit: *"validasi ini mengukur konsistensi counting logic terhadap galat tracking pada benchmark tracking publik; belum ada validasi pada rekaman ruang publik dengan definisi masuk/keluar yang sebenarnya."* Lalu turunkan judul/sub-klaim dari "sistem people counting" ke "pipeline counting yang divalidasi pada benchmark tracking" selama uji domain target belum ada. Ini yang membedakan naskah yang jujur dari yang di-reject karena overclaim.

**K7. FACT-CHECK KODE: satu klaim Method tidak sesuai implementasi.**
§3.3 menulis: *"Setiap ID mengikuti status UNSEEN, TRACKING, COUNTED_IN/COUNTED_OUT, COOLDOWN, EXPIRED. … sedangkan ID yang tidak lagi diperbarui akan dihapus."*
Di `core/counting/models.py` + `core/counting/counter.py`:
- Enum memang punya enam state, tetapi **hanya `TRACKING` dan `COOLDOWN` yang pernah di-assign**. `UNSEEN`, `COUNTED_IN`, `COUNTED_OUT`, `EXPIRED` **tidak pernah dipakai di satu baris pun**.
- **Tidak ada mekanisme penghapusan/expiry.** `self._tracks` tidak pernah dipangkas (`last_updated` ada di dataclass tapi tidak pernah di-update). Jadi klaim "ID yang tidak lagi diperbarui akan dihapus" **tidak benar** — dalam sesi panjang dictionary ID tumbuh tanpa batas.
- Perilaku sebenarnya adalah **debounce berbasis waktu per-ID**, bukan state identitas "sekali seumur sesi": setelah 30 frame, ID yang sama boleh dihitung lagi kalau melintas lagi. Ada test yang justru mengunci perilaku ini: `tests/counting/test_counter.py` berakhir dengan `assert counter.count_in == 2` untuk ID yang sama.
→ **Solusi:** (a) perbaiki §3.3 agar menggambarkan implementasi aktual (state machine TRACKING ⇄ COOLDOWN dengan debounce 30 frame; struktur state lain disiapkan untuk pengembangan lanjut); (b) kalau memang ingin state identity-based, implementasikan dulu (set COUNTED_* + pruning) baru tulis; (c) hilangkan/kuatkan klaim implikasi "satu orang hanya terhitung sekali" — yang benar: **satu orang hanya bisa terhitung sekali per jendela cooldown**. Ini juga menjelaskan mengapa optimum CD bergantung dataset, dan justru memperkuat analisis Anda di §4.4.

---

## B. REVISI — isi

**S1. Tiga titik optimum, tanpa kriteria keputusan yang diformalkan.** §4.4.1: MAE terendah 6,34 pada CD=30, galat persentase terendah 14,64% pada CD=45. §4.4.2: galat terendah 1,67% pada conf 0,20. §4.3.1 memakai 16,71% (CD=30). Jadi ada **empat angka** berbeda untuk konfigurasi yang berbeda-beda, dan naskah tidak pernah menyatakan objective function pemilihannya.
→ **Solusi:** satu paragraf "kriteria pemilihan konfigurasi operasional": MAE dipilih sebagai kriteria utama (bukan galat persentase) karena galat persentase membaik di CD=45 akibat **bias under-count −4,38** yang saling mengompensasi dengan over-count di sekuens lain — kompensasi dua galat berlawanan bukan akurasi. Itu argumen kuat dan sudah setengah ada di `docs/journal/4.4`; tinggal dikembalikan ke naskah. Sertakan juga basis perhitungan angka 1,67%.

**S2. Pemilihan Deep-OC-SORT tidak konsisten dengan data tracking-nya sendiri — ini pertanyaan reviewer nomor satu.**
Di MOT20: OC-SORT HOTA **36,51** > Deep-OC-SORT **36,12**. Di DanceTrack: Deep-OC-SORT 28,91 > OC-SORT 28,39 (selisih 0,52). Di edge: Deep-OC-SORT **12,0 FPS**, OC-SORT **30,7 FPS**. Artinya, pada benchmark terpadat, metode yang dipilih sebagai tracker utama **kalah HOTA** dari baseline yang justru paling ringan, dan di perangkat terbatas ia gagal real-time.
→ **Solusi:** jangan sembunyikan. Tulis argumen pemilihannya secara terbuka dan berlapis: Deep-OC-SORT menang konsistensi identitas (IDSW 11.751 vs 14.293; IDF1 unggul di DanceTrack) dan galat hitungnya lebih rendah (16,71% vs 22,38%) **pada deteksi yang sama** — jadi untuk tujuan counting ia menang meski HOTA-nya kalah tipis. Tambahkan juga: selisih HOTA 0,39 di MOT20 berada di dalam variasi antar-run, sehingga dua tracker ini praktis setara di MOT20 (lihat S5). Rumusan jujur semacam ini menaikkan kredibilitas, bukan menurunkan.

**S3. Ablasi tidak mengisolasi mekanisme, dan baseline-nya strawman.**
Model B = RoI polygon **+** deteksi perpotongan segmen **+** state machine, digabung jadi satu. Tidak ada varian yang menguji peran RoI sendirian, atau intersection sendirian. Padahal §2.3 dan §3.3 menyebut "validasi RoI" sebagai salah satu kontribusi — dan kontribusi itu **tidak diukur**.
Lebih jauh: Model A ("naive line crossing") tidak punya memori status sama sekali. Pembanding yang adil untuk klaim kebaruan adalah **debounce/double-line standar** — praktik yang sudah default di tool komersial (RoI + line crossing + ID state, mis. DeepStream `nvdsanalytics`, Ultralytics solutions). Melawan baseline tanpa memori membuat lompatan 101,99% → 16,71% terdengar lebih besar dari kebaruannya.
→ **Solusi:** tambahkan baris ablasi: (a) RoI saja, (b) intersection saja, (c) cooldown saja, (d) lengkap. Dan tambahkan satu paragraf yang mengakui bahwa double-line/debounce adalah praktik umum, lalu nyatakan yang membedakan naskah ini: **perbandingan kuantitatif antara naive vs state machine pada deteksi identik di 29 sekuens, plus peta sensitivitas cooldown lintas tracker** — bukan pada konsep dasarnya, tapi pada pengukurannya.

**S4. Anomali tabel tidak dijelaskan.** Di MOT20, LightTrack punya fragmenasi **8.863**, lebih rendah dari OC-SORT (27.646) dan DiffMOT (15.005), padahal HOTA-nya terburuk (32,92) dan IDSW tinggi. Tanpa satu kalimat, ini terbaca seperti angka yang tidak konsisten.
→ **Solusi:** jelaskan bahwa fragmentasi rendah dengan HOTA rendah berarti track terpecah sedikit tetapi identitas tidak konsisten — indikasi ID menggantung/berpindah alih-alih memutus track. Idealnya tambahkan kolom atau kalimat dugaan mekanisme.

**S5. Tidak ada ketegasan statistik sama sekali.** Satu seed, satu angka agregat, tanpa standar deviasi, tanpa interval, tanpa uji signifikansi — sementara naskah membuat peringkat antar tracker. Selisih HOTA 0,39 (OC-SORT vs Deep-OC-SORT di MOT20) dan 0,52 (DanceTrack) hampir pasti di dalam noise run.
→ **Solusi:** (a) sajikan std/IQR per sekuens di Tabel 5 dan Tabel 6 (datanya ada di `laporan-skenario-c-counting.md` dan `laporan-skenario-b-tracker.md`); (b) turunkan klaim "terbaik" menjadi "terendah pada konfigurasi yang diuji"; (c) jangan klaim ranking di mana selisihnya lebih kecil dari variasi antar-run. Ini biaya kecil yang mematikan serangan "single seed, no error bars".

**S6. Interpretasi keunggulan NMS-free melewati konfound pengukuran.** §4.1.2 menyimpulkan keunggulan NMS-free terukur pada post-processing dan §4.1.1 menyimpulkan kapasitas model lebih berpengaruh dari arsitektur. Laporan sumber eksplisit memperingatkan: pengukuran GPU didominasi *overhead* peluncuran kernel (YOLO26s ±3,8× FLOPs YOLO26n hanya 5,5% lebih lambat), dan **pada CPU + PyTorch justru YOLOv11n yang tercepat (21,14 ms vs YOLO26n 23,06 ms)** — YOLO26n hanya unggul pada jalur ONNX.
→ **Solusi:** tambahkan satu kalimat pembatas: kesimpulan peringkat latensi berlaku pada kombinasi perangkat **dan** runtime yang diuji. Ini memperkuat kesan penulis memahami kondisi pengukurannya.

**S7. Nama sistem menjanjikan mekanisme yang tidak ada.** "Real-Time **Adaptive** Neural Counting with **Associative Group Estimation**". Saya sudah menyisir seluruh `src/` dan `core/`: **tidak ada satu pun mekanisme adaptif** (cooldown, threshold, dan RoI semuanya nilai tetap dari konfigurasi), dan **tidak ada estimasi grup** (setiap ID dinilai sendiri, tanpa agregasi/grouping).
→ **Solusi:** pilih satu dari dua — (a) ganti nama/singkatan agar sesuai isi (mis. *Robust Line-Crossing Counting with State-Machine Debouncing*), atau (b) implementasikan minimal satu mekanisme adaptif yang benar-benar diukur (mis. cooldown yang menyesuaikan kecepatan pejalan, atau cooldown dalam satuan detik alih-alih frame) dan jadikan itu sebagai kontribusi baru. Opsi (b) sebenarnya menaikkan nilai naskah secara signifikan — dan menjawab S8 sekaligus. Tapi jangan biarkan singkatan menjanjikan hal yang tidak ada; reviewer pertama yang menyadari ini akan kehilangan kepercayaan pada seluruh klaim lain.

**S8. Cooldown dalam satuan frame mengikat sistem ke fps kamera.** CD=30 frame berarti 1 detik pada 30 fps, tapi 0,5 detik pada 60 fps — dan §4.4.1 sendiri menyatakan CD=15 "lebih tepat untuk arus pejalan cepat", artinya nilai optimum bergantung pada kecepatan pejalan. Padahal target deployment justru bisa berjalan 30–97 fps (§4.1.2).
→ **Solusi:** konversi cooldown ke satuan waktu (`cooldown_ms`) atau, lebih baik, nyatakan sebagai rekomendasi: cooldown harus diskalakan `CD_opt = f(fps, kecepatan_pejalan)`. Ini cacat generalisasi yang mudah diperbaiki dan justru bisa jadi kontribusi.

**S9. Dua mode kegagalan mekanisme yang tidak dibahas sama sekali.**
Dari kode `core/counting/counter.py`:
- **RoI early-return:** kalau centroid di luar RoI, objek **tidak di-update sama sekali** (state dan history dibekukan, baris 32–35). Saat objek masuk kembali, segmen lintasan memakai titik terakhir yang sudah tua → segmen panjang menyeberangi garis → **potensi hitungan palsu** untuk orang yang berjalan di sepanjang tepi RoI. Naskah §3.3 menjual RoI sebagai *validator*, padahal di kode RoI juga bisa menjadi *sumber galat*.
- **Riwayat dibatasi 10 titik** (baris 42–45, untuk menahan RAM). Untuk orang yang bergerak cepat atau fps rendah, segmen 2 titik terakhir tetap pendek — tapi interaksi antara batas riwayat dan RoI-freeze tidak pernah diuji.
→ **Solusi:** tambahkan paragraf "batas mekanisme counting" yang menyebut dua hal ini, dan sebutkan cara mitigasinya (mis. reset history saat objek keluar-masuk RoI, atau ROI dijadikan filter output ketimbang early-return). Reviewer akan menghargai; kalau tidak ditulis dan ditemukan sendiri, ini alasan penolakan.

**S10. Counting logic — inti kontribusi — justru bagian yang paling lemah dukungan literaturnya.**
§2.3 dan §3.3 bersandar terutama pada `[Nurseitov]`, `[Diaz-Santos]`, `[McCarthy]`, `[Song 2026]`, dan satu buku geometri 1998 (`O'Rourke`) untuk CCW. Sementara deteksi (YOLO/RT-DETR/D-FINE) dan tracking (OC-SORT/DiffMOT/Deep-OC-SORT/6 metode 2024–2026) mendapat porsi jauh lebih besar. Padahal yang dijual naskah ini adalah lapisan counting.
→ **Solusi:** imbangi — tambahkan sub-bab Related Works khusus counting logic yang memuat: praktik industri (DeepStream `nvdsanalytics`, Ultralytics line-zone counting), studi people counting berbasis garis/zona dengan angka, dan pekerjaan yang membahas *debounce*/hysteresis pada line crossing. Lalu tarik satu paragraf pembeda: apa yang belum ada di literatur (perbandingan terkontrol antara naive vs state machine pada deteksi identik; peta sensitivitas cooldown lintas tracker).

**S11. Tidak ada pembandingan angka dengan literatur yang dikutip sendiri.** §2.2 mengutip akurasi 85% (RoI quadrilateral) dan 98,42% (kaskade + Kalman Filter), lalu keduanya tidak pernah muncul lagi — sementara §4.3 melaporkan galat 13–16%. Reviewer akan menyimpulkan naskah menghindari perbandingan yang tidak menguntungkan.
→ **Solusi:** tambahkan tabel perbandingan (`Studi | Pendekatan | Dataset | Metrik | Hasil | Batasan`) dan satu paragraf yang menjelaskan mengapa angkanya tidak apple-to-apple (dataset berbeda, definisi metrik berbeda, definisi "orang dihitung" berbeda). Ketidakbisaan dibandingkan boleh dijelaskan — diabaikan tidak boleh.

**S12. Justifikasi kenapa benchmark tracking publik sah dipakai mengukur counting belum ada.** MOT20 dan DanceTrack tidak punya label masuk/keluar; CrowdHuman citra statis. Naskah memilihnya tanpa argumen validitas.
→ **Solusi:** satu paragraf: benchmark ini dipakai karena menekan **kegagalan asosiasi** (oklusi padat MOT20; gerak non-linear DanceTrack) yang justru penyebab utama galat counting; counting dievaluasi sebagai *derivatif* dari kualitas asosiasi. Akui batasnya (K6).

**S13. Discussion tidak menempatkan hasil terhadap literatur.** §4.6 merangkum temuan secara internal (per lapisan) dan bagus di situ, tapi tidak satu kalimat pun berbentuk "temuan kami sejalan/berbeda dengan X". Bagian Discussion tanpa posisi terhadap literatur akan diminta ditulis ulang oleh reviewer.
→ **Solusi:** tambahkan 3 kalimat: (a) temuan bahwa HOTA rendah sementara MOTA tinggi sejalan dengan laporan MOT20 pada umumnya; (b) temuan bahwa kualitas asosiasi lebih menentukan counting daripada kualitas kotak deteksi — hubungkan ke studi people counting berbasis lintasan; (c) keunggulan NMS-free yang hanya muncul di post-processing adalah verifikasi independen, bukan temuan (laporan repo sudah menyebutnya dengan nama teknis *latency monotonicity*).

**S14. Daftar limitasi belum lengkap.** Sudah ada: satu seed, deteksi offline, latensi bergantung perangkat. Belum ada: tidak ada uji domain target, tidak ada uji lintas fps, tidak ada analisis kerumunan ekstrem (P99 spike akibat Hungarian matching pada >50 orang sudah disebut di laporan skenario D, tidak masuk naskah), tidak ada uji privasi/etika untuk klasifikasi orang di ruang publik.

---

## C. BAGUS — jangan diubah

1. **Semua tracker dievaluasi pada deteksi yang identik.** Ini kekuatan metodologis utama naskah. Banyak paper people counting membandingkan tracker memakai detektor aslinya masing-masing, sehingga perbedaannya tidak terkontrol. Pertahankan §3.2 dan tegaskan lagi di §4.2.
2. **Ablasi naive vs state machine memberi hasil yang berbicara sendiri** (88,7–155,1% → 16,71%). Ukuran efeknya besar dan mekanismenya dijelaskan dengan benar (osilasi, orang berhenti dekat garis, ID berganti).
3. **Anggaran real-time dideklarasikan lebih dulu (30 FPS / 33,3 ms), lalu diuji.** Ini urutan yang benar; banyak naskah menguji lalu mencari ambang.
4. **Kejujuran yang sudah ada:** §3.2 menyatakan hasil absolut tidak merepresentasikan capaian paper asli tracker; §4.6 menyebut single seed dan deteksi offline; status YOLO26 sebagai preprint/vendor dinyatakan terbuka. Jangan hilangkan saat penyuntingan.
5. **Semua angka lolos lacak-balik ke repo.** Nol metrik karangan — saya uji 21 angka kunci, semuanya ada di `docs/reports/`.
6. **Gap statement di §2.3 tajam dan spesifik** (bukan "belum ada yang meneliti X"). Kalimat "keberhasilan tracking tidak selalu menghasilkan penghitungan yang akurat" adalah tesis naskah yang bagus.
7. **Analisis per-lapisan di §4.6 masuk akal dan tidak berlebihan** — setiap lapisan punya faktor pembatas yang berbeda, dan itu argumen yang benar.

---

## D. Saran (penguatan, tidak wajib)

1. **Peta sensitivitas lintas tracker diperluas jadi tabel.** §4.4.1 menyebut optimum berbeda per tracker (DiffMOT CD=30, Deep-OC-SORT CD=45, OC-SORT CD=60) — itu temuan menarik yang sekarang hanya jadi satu anak kalimat. Jadikan tabel; nilai tambahnya besar dan datanya sudah ada.
2. **Analisis atribusi galat.** Sekarang klaim "galat 13–16,71% mencakup lantai deteksi 7,4–10,0%" adalah inferensi, bukan pengukuran. Kalau bisa dipisah berapa galat akibat missed detection vs ID switch, naskah naik kelas.
3. **Contoh kasus kualitatif per mode kegagalan** (satu clip ID switch, satu clip orang berhenti di garis, satu clip under-count di tepi bingkai) — jauh lebih persuasif daripada satu angka agregat.
4. **Ablasi resolusi** sudah ada di repo (`experiments/resolusi_scaling_results.csv`: turunkan 640→256 memangkas piksel 6,25× tapi FPS hanya naik 27%, dan **−60% s/d −78% deteksi hilang**) dan belum masuk naskah. Ini argumen kuat bahwa pada GPU sistem tidak compute-bound.
5. **Pernyataan ketersediaan kode** — menaikkan kesan reprodusibel dan melindungi dari permintaan reviewer.

---

## E. Hasil fact-check isi (klaim teknis ↔ kode)

| Klaim di naskah | Verifikasi di kode | Status |
|---|---|---|
| Rumus CCW `(Bx−Ax)(Cy−Ay) − (By−Ay)(Cx−Ax)` | `detector.py:9` — ekspresi identik (perkalian komutatif) | ✅ cocok |
| Arah: `D = v_line,x·v_move,y − v_line,y·v_move,x`, D>0 = IN | `detector.py:47-52` — `(vA_x*vB_y) - (vA_y*vB_x) > 0 → "IN"` | ✅ cocok |
| Perpotongan diuji perubahan tanda pada kedua segmen | `detector.py:29-32` — dua pasang `!=` | ✅ cocok |
| "Hanya centroid di dalam poligon RoI yang diproses" | `counter.py:32-35` — early return | ✅ cocok (tapi lihat S9) |
| Cooldown 30 frame setelah dihitung, default | `counter.py:72` + `models.py:37` + config default 30 | ✅ cocok |
| Kompleksitas O(N) terhadap tracklet aktif | per track O(1), polygon test O(V); total O(N·V) | ⚠️ disederhanakan, sebutkan V |
| "Status UNSEEN, TRACKING, COUNTED_IN/OUT, COOLDOWN, EXPIRED" | `models.py:22-29` enum ada, **tapi hanya TRACKING & COOLDOWN pernah di-assign** | ❌ **tidak sesuai** |
| "ID yang tidak lagi diperbarui akan dihapus" | tidak ada pruning, `last_updated` tidak pernah di-update, `_tracks` tumbuh tanpa batas | ❌ **tidak sesuai** |
| "Mekanisme ini menerapkan prinsip debouncing… tanpa menambah anotasi garis" | `counter.py` — benar, satu garis + cooldown | ✅ cocok |
| Nama "Adaptive" / "Associative Group Estimation" | tidak ada mekanisme adaptif maupun group estimation di `src/`/`core/` | ❌ **tidak didukung** |

**Kesimpulan fact-check isi:** angka eksperimen bersih. Yang bermasalah adalah **deskripsi mekanisme** — dua klaim §3.3 (enam state + penghapusan ID) tidak benar untuk kode saat ini. Ini masuk kategori klaim teknis tak terverifikasi: perbaiki teksnya **atau** perbaiki kodenya, jangan biarkan seperti ini.

---

## F. Delapan pertanyaan yang hampir pasti ditanya reviewer — siapkan jawabannya

1. Bagaimana ground truth hitung diperoleh, dan apa artinya galat 16,71% secara operasional (berapa orang salah dihitung per sekuens)?
2. Mengapa memilih Deep-OC-SORT sebagai tracker utama padahal HOTA-nya di MOT20 lebih rendah dari OC-SORT, dan ia hanya 12 FPS di edge?
3. Kalau counting logic adalah kontribusi utama, mengapa tidak ada ablasi yang memisahkan peran RoI, deteksi perpotongan, dan state machine?
4. Berapa variasi antar-run / standar deviasi angka-angka ini?
5. Mengapa galat di §4.4.2 bisa 1,67% sementara di §4.3 13–16%?
6. Apa yang membedakan state machine ini dari debounce/double-line standar yang sudah tersedia di tool komersial?
7. Bagaimana sistem berperilaku pada fps kamera yang berbeda, dan bagaimana cooldown 30 frame digeneralisasi?
8. Apakah ada validasi pada skenario ruang publik nyata (pintu, stasiun), atau semuanya berbasis benchmark tracking?

Jawaban untuk 1, 2, 5, 6, dan 7 ada bahannya di repo — tinggal dikembalikan ke naskah. Pertanyaan 3, 4, dan 8 adalah yang paling mungkin memicu revisi mayor, jadi prioritaskan menutupnya.

---

## G. Perbaikan isi — cari → ganti

| # | Cari di naskah | Ganti/pindahkan menjadi |
|---|---|---|
| 1 | Paragraf §4.3 yang memuat "galat 13,08%…16,71%" tanpa definisi | Tambahkan sebelum tabel: rumus galat, MAE, dan kalimat *"ground truth hitung diturunkan dengan menjalankan counter yang sama pada lintasan ground truth, sehingga metrik mengukur sensitivitas counting logic terhadap galat tracking"* |
| 2 | `Setiap ID mengikuti status UNSEEN, TRACKING, COUNTED_IN/COUNTED_OUT, COOLDOWN, EXPIRED.` | `Setiap ID mengikuti transisi TRACKING dan COOLDOWN; status lain disediakan pada lapisan state untuk pengembangan lanjutan. Setelah dihitung, ID memasuki cooldown selama 30 frame sebelum dapat dihitung kembali.` |
| 3 | `sedangkan ID yang tidak lagi diperbarui akan dihapus` | *(hapus)* — diganti dengan batasan: *"identitas yang tidak lagi terdeteksi tidak dihitung ulang selama berada dalam jendela cooldown"* |
| 4 | `Dengan mempertimbangkan akurasi dan efisiensi, Deep-OC-SORT dipilih sebagai tracker utama` | `Pada deteksi yang sama, Deep-OC-SORT menurunkan galat hitung dari 22,38% (OC-SORT) menjadi 16,71% dan menurunkan ID switch dari 14.293 menjadi 11.751, meskipun HOTA-nya di MOT20 sedikit lebih rendah (36,12 lawan 36,51) dan selisih itu berada dalam variasi antar-run. Untuk tujuan penghitungan berbasis lintasan, konsistensi identitas lebih menentukan, sehingga Deep-OC-SORT dipilih sebagai tracker utama dan OC-SORT dipertahankan sebagai jalur ringan pada perangkat terbatas.` |
| 5 | `Temuan ini dibatasi oleh penggunaan satu seed, benchmark publik dengan deteksi offline, dan latensi yang bergantung pada perangkat.` | `Temuan ini dibatasi oleh penggunaan satu seed, benchmark publik dengan deteksi offline, latensi yang bergantung pada perangkat, serta belum adanya validasi pada rekaman ruang publik dengan definisi arus masuk-keluar yang sebenarnya.` |
| 6 | `Galat 13,08-16,71% pada dua jalur terbaik juga mencakup keterbatasan deteksi, dengan 7,4-10,0% objek yang tidak terdeteksi.` | `Galat 13,08-16,71% pada dua jalur terbaik sebagian berasal dari lantai deteksi 7,4-10,0% objek yang tidak terdeteksi; dekomposisi kuantitatif antara galat akibat missed detection dan galat akibat identity switch belum dipisahkan pada studi ini.` |
| 7 | `Galat terendah sebesar 1,67% diperoleh pada threshold 0,20.` | `Galat terendah sebesar 1,67% diperoleh pada threshold 0,20 pada basis perhitungan yang sama dengan Tabel 6. Namun, konfigurasi operasional memakai 0,30 karena rentang 0,25-0,30 memberi keseimbangan galat dan throughput yang lebih stabil.` |
| 8 | Judul `RANCAGE: REAL-TIME ADAPTIVE NEURAL COUNTING WITH ASSOCIATIVE GROUP ESTIMATION` | Ganti akronim agar sesuai isi, atau tambahkan satu paragraf yang mendefinisikan secara operasional apa yang dimaksud "adaptive" dan "group estimation" di sistem ini |

---

## H. Urutan kerja (isi)

1. K7 — benahi deskripsi state machine + klaim penghapusan ID (paling berisiko: klaim tidak sesuai kode).
2. K1 — definisi metrik hitung dan protokol GT.
3. K2 — tabel tail-latency dan edge.
4. K3 + K4 — Conclusions dan Abstract, setelah isi lain stabil.
5. K5 + K6 — rumusan masalah, kontribusi, dan batasan validitas eksternal.
6. S1 + S2 + S5 — kriteria pemilihan konfigurasi, justifikasi tracker utama, dan sebaran/statistik.
7. S3 — ablasi yang memisahkan mekanisme.
8. S7 + S8 — nama sistem dan cooldown berbasis waktu.
9. S10 + S11 + S13 — literatur counting logic, tabel perbandingan, Discussion berbasis literatur.
10. S9 + S12 + S14 — batas mekanisme, validitas benchmark, limitasi lengkap.

---

*Fokus dokumen ini murni isi. Catatan format dan template sengaja dipisah ke `review-jestec-manuscript-full.md` agar tidak mengaburkan prioritas. Item K1, K2, K6, K7 dan S2 adalah yang paling menentukan hasil review jurnal.*
