# Review Naskah JESTEC — "Pengembangan Model Rekognisi Objek untuk Real-Time People Counting System Berbasis Deep Learning"
**Artefak yang direview:** `docs/_extracted/manuscript-v1.pdf` (15 hlm, dibuat dari Word 2026-09-12 19:31)
**Pembanding ground-truth:** `docs/journal/*.md` (draft Sep-10), `docs/reports/*.md` (laporan eksperimen), `references/references.bib`, `docs/research/source-ledger.md`, template resmi JESTEC
**Tanggal review:** 12 September 2026

---

## VERDICT: **TIDAK LAYAK SUBMIT — MAJOR REVISION** (setara *Reject – Resubmit*)

Alasan tunggal yang sudah cukup untuk desk-reject: **naskah masih memuat isi template asing di tiga tempat terpenting (Abstract, Keywords, Appendix A), Conclusions kosong, dan tidak ada daftar References.** Bahasa naskah juga Bahasa Indonesia, sedangkan JESTEC mewajibkan **English (UK)**.

Skor indikatif (bukan skor resmi jurnal):

| Aspek | Bobot | Skor | Catatan |
|---|---|---|---|
| Kepatuhan template & kelengkapan | 25 | 4/25 | Abstract/Keywords/Appendix template, Conclusions kosong, tak ada References |
| Kebahasaan & presentasi | 15 | 4/15 | Bahasa Indonesia, typo massal, desimal koma, "Gambar" vs "Fig." |
| Metodologi & definisi metrik | 20 | 11/20 | Metrik hitung tidak didefinisikan; GT hitung tak dijelaskan |
| Validitas hasil & konsistensi angka | 20 | 13/20 | Angka lolos lacak-balik ke repo, tapi ada 3 kontradiksi internal |
| Related work, gap, kontribusi | 10 | 6/10 | Gap jelas; kontribusi/rumusan masalah hilang saat pemadatan |
| Integritas sitasi | 10 | 2/10 | 30+ sitasi in-text, 0 entri bibliografi, 3 gaya tercampur |
| **Total** | 100 | **40/100** | |

**Catatan penting yang saya maklumi (sesuai permintaan):** judul belum final, sitasi belum dikonversi, placeholder screenshot dashboard. Itu tiga hal ini **tidak** saya hitung sebagai kesalahan konseptual — hanya dicatat posisinya di daftar kerja (R3/R4/R9).

---

## A. RUSAK — blocker, tidak bisa disubmit sebelum ini beres

**R1. Abstract masih abstract proyektil/SOMChE.**
Isi Abstract saat ini: *"An investigation has been made to predict the effects of forebody and afterbody shapes on the aerodynamic characteristics of several projectile bodies at supersonic speeds…"* — 100% isi template, nol kaitan dengan people counting. Ini hal pertama yang dibaca editor.
→ **Solusi:** tulis abstract 100–200 kata (batas JESTEC) English (UK), struktur: (1) masalah 1 kalimat, (2) pendekatan RANCAGE 1–2 kalimat, (3) hasil berangka: YOLO26s mAP@0.5:0.95 0,4974; DiffMOT HOTA 44,37 di MOT20; galat hitung 16,71% (Deep-OC-SORT) vs 101,99% (naive); 24,61 ms/frame = 40,6 FPS, (4) 1 kalimat kontribusi. Jangan tulis "Penelitian ini bertujuan untuk…" pembuka generik.

**R2. Keywords masih keywords template.**
*"Aerodynamics, Forebody and afterbody, Next keyword, Projectile, Supersonic speed."* → JESTEC: ≤5 kata kunci, **urut alfabetis**. Usulan: `Crowd counting, Multi-object tracking, NMS-free detector, Real-time video analytics, Trajectory-based counting`.

**R3. Bagian 5 Conclusions kosong.** Halaman 14 hanya memuat judul "5. Conclusions" tanpa satu paragraf pun.
→ **Solusi:** 4–6 poin: (a) temuan arsitektur (kapasitas model > perbedaan arsitektur pada tier nano), (b) NMS-free menghemat post-processing, bukan akurasi, (c) asosiasi identitas, bukan kualitas kotak, yang menentukan akurasi hitung, (d) state machine menekan over-count dengan biaya 0,4% latensi, (e) pipeline lolos anggaran 33,3 ms di GPU dan batas perangkat pada jalur Deep-OC-SORT di edge, (f) arah lanjutan. Tanpa angka baru yang belum muncul di Bagian 4.

**R4. Tidak ada daftar References sama sekali.**
Naskah memuat ~30 item sitasi in-text, nol entri bibliografi. `references/references.bib` punya 50 entri (kode S001–S049) — bahan bakunya ada, hanya belum disusun.
→ **Solusi:** susun References **dinomori urut kemunculan** (aturan JESTEC), format contoh dari template resmi:
`Cao, J.; Pang, J.; Weng, X.; Khirodkar, R.; and Kitani, K. (2023). Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), Vancouver, Canada, 1456-1466.`
Perhatikan: inisial dipisah titik, **"; and"** sebelum penulis terakhir, tidak ada "et al." di daftar pustaka.

**R5. Tiga gaya sitasi tercampur, tidak satu pun sesuai JESTEC.**
Yang ada di naskah sekarang: `(Cao et al., 2023)` · `[Jinkun Cao]` · `[Ao Wang 2024]` · `[nurseitov]` · `[dendorfer]` · `[shao 2018]` · `[sun 2022]` · `[Surantha 2025]` dan `[Surantha, 2025]` untuk sumber yang sama · `[Maggiolino]` dan `[Maggiolino et al., 2023]` untuk sumber yang sama.
→ **Solusi:** ganti **semua** jadi angka kurung siku urut kemunculan: `[1]`, `[2]`, `[3]`, … (JESTEC: *References numbered by first appearance*). Sekalian: `nurseitov` → `Nurseitov` (huruf kapital), dan satu sumber = satu nomor, jangan dua gaya.
Temuan tambahan: `Ultratics, 2026` dan `Chakrabarty, 2026` dipakai di Related Works tapi belum ada entri bib-nya → cek `references.bib` sebelum menomori.

**R6. Bahasa naskah Indonesia; JESTEC mewajibkan English (UK).**
Ini bukan soal selera: halaman *Submit a paper* JESTEC menyatakan `Language: English (UK)`. Naskah saat ini Bahasa Indonesia dengan heading Inggris → campur. Tambahan: heading Indonesia/Inggris juga campur di dalamnya (`4.1.1 Akurasi Deteksi` vs `4.1.2 Efisiensi Komputasi` di bawah `4.1. Object Detection Results`).
→ **Solusi:** putuskan dulu venue. Kalau tetap JESTEC: terjemahkan penuh + konsisten UK (`model`→tak berubah; `behavior`→`behaviour`; `generalization`→`generalisation`). Kalau targetnya laporan hibah berbahasa Indonesia, jangan pakai template JESTEC — pakai template laporan kampus, supaya "tidak sesuai template" tidak menjadi temuan.

**R7. Sisa template masih hidup di badan naskah.**
Header halaman ganjil: `A. B. One and X. Y. Two`. Footer: `This is the Template You Use to Format and Prepare Your Manuscript`. Halaman 15: `Appendix A / Computer Programme / A.1 Introduction / A.2 Programme Structure… / Fig. A-1. Main flow chart of the computer programme` — semuanya isi template proyektil (Fortran-77).
→ **Solusi:** hapus header/footer template; ganti Appendix A dengan listing ringkas `src/pipeline.py` + `src/web/core/pipeline.py` (bagian inti state machine + CCW) **atau** hapus Appendix sepenuhnya (JESTEC: *Appendix (if any)*).

**R8. Gambar tidak ada di naskah, dan rujukan gambar timpang.**
- `Fig. 1. Arsitektur Sistem RANCAGE` disebut di §3.1 tapi gambarnya tidak ada — halaman 10 dan 12 kosong.
- §4.1 tidak pernah merujuk Gambar apa pun, padahal repo punya `fig1_pr_curve.png` dan `fig2_f1_curve.png` yang sudah diberi caption di `docs/journal/4.1-object-detection-results.md`.
- §4.2 merujuk `Gambar 4`, §4.3 `gambar 6`, §4.4 `Gambar 6` dan `Gambar 7`, §4.5 `Gambar 8` — tanpa satu gambar maupun caption. Nomor 1, 2, 3, 5 tidak pernah muncul di naskah.
- Istilah campur: `Fig 1` vs `Gambar 4` (JESTEC: `Fig. 1`, atau `Figure 1` di awal kalimat; caption **di bawah** gambar; tabel caption **di atas**).
→ **Solusi:** ambil 9 file di `experiments/journal_figs/` (`fig1_pr_curve`, `fig2_f1_curve`, `fig9_tracking_metrics`→jadi Fig. 3, `fig10_demo_qualitative`→Fig. 4, `fig5_counting_error`→Fig. 5, `fig6_cooldown_sensitivity`→Fig. 6, `fig7_conf_sensitivity`→Fig. 7, `fig8_latency_breakdown`→Fig. 8, dan `fig9_web_dashboard` untuk dashboard), tempel semua, seragamkan penomoran `Fig. 1`–`Fig. 9`, dan samakan rujukan di teks.

**R9. Placeholder yang belum selesai (dimaklumi, tapi harus dicatat posisinya).**
`: (tambahkan screenshot dashboard)` **di dalam sel Tabel 6**, dan `**[Gambar 9]**` di `docs/journal/4.3` — belum jadi gambar. Judul masih ganda: judul Indonesia + `RANCAGE: REAL-TIME ADAPTIVE NEURAL COUNTING WITH ASSOCIATIVE GROUP ESTIMATION`.
→ **Solusi:** ambil screenshot sesuai panduan di `docs/journal/4.3-people-counting-results.md` (jalankan `python -m src.web.server --source <video>`, simpan `experiments/journal_figs/fig9_web_dashboard.png`), hapus blok placeholder dari sel tabel, dan pilih **satu** judul (sarankan judul Inggris informatif; akronim RANCAGE boleh jadi sub-judul atau disebut sekali di Abstract).

**R10. Nomenclature dan Declaration of Generative AI tidak ada.**
JESTEC mensyaratkan (a) `Nomenclature` **sebelum** References, alfabetis, mencakup semua simbol/singkatan/subskrip-superskrip beserta satuan SI; (b) sejak **1 Mei 2026**, `Declaration of Generative AI in Scientific Writing` tepat **sebelum** References.
→ **Solusi:** buat Nomenclature memuat minimal: `CCW`, `CD` (cooldown, frame), `FPS`, `GT`, `HOTA`, `IDF1`, `IDSW`, `IoU`, `MAE`, `mAP`, `MOTA`, `MR⁻²`, `NMS`, `Re-ID`, `RoI`, `tlwh`, dan simbol `D` (arah perlintasan), `N`, `p1/p2`, `q1/q2`, `v_line`, `v_move`. Untuk deklarasi AI: nyatakan penggunaan alat AI **hanya** untuk perbaikan bahasa, bukan analisis. Ini bukan formalitas — JESTEC menyatakan naskah tanpa deklarasi ini akan dikembalikan.

---

## B. REVISI — wajib diperbaiki, tapi tidak mematikan

**V1. Metrik hitung tidak didefinisikan di naskah (temuan paling serius dari sisi metodologi).**
§4.3 melaporkan "galat rata-rata 13,08% / 16,71% / 53,03%" tanpa pernah menjelaskan: (a) rumusnya apa (MAPE agregat? per-sekuens lalu dirata-rata? selisih total?), (b) **bagaimana ground truth hitung diperoleh**, (c) di mana garis virtual diletakkan dan mengapa di situ, (d) apakah satu garis atau beberapa.
Padahal jawabannya sudah ada di repo, di `docs/journal/3-method.md`: *"ground truth hitung diturunkan dengan menjalankan counter yang sama pada lintasan ground truth"* dan *"Kualitas hitungan dinilai dari MAE, galat relatif, RMSE per interval, serta pemisahan over-count dan under-count"*. Kalimat ini **hilang** saat penyusunan Word.
→ **Solusi:** pindahkan kalimat definisi itu ke §3.4 (atau sub-bab metodologi baru "Counting Metrics"), sertakan rumus galat relatif dan penjelasan bahwa GT hitung bukan anotasi manusia melainkan hasil counter pada lintasan GT — sekaligus sebutkan konsekuensinya: metrik ini mengukur *sensitivitas counter terhadap galat tracking*, bukan akurasi absolut terhadap jumlah orang sebenarnya di lapangan.

**V2. Janji di Method yang tidak muncul di Results.**
- §3.4: *"S1 mengevaluasi… perbandingan antara konfigurasi zero-shot dan fine-tuned"* → **tidak ada satu angka pun** di §4.1.
- §3.4: *"S4 mengevaluasi… tail latency pada persentil P90, P95, dan P99 serta perangkat edge AMD RX 6600 dengan DirectML"* → §4.5.2 hanya menunjuk "Gambar 8" tanpa angka. Padahal `docs/reports/laporan-skenario-d-realtime.md` punya lengkap: `P90 29,50 / P95 32,10 / P99 36,40 ms` (RTX 4090), dan jalur edge `OC-SORT total 32,57 ms = 30,7 FPS` vs `Deep-OC-SORT total 83,01 ms = 12,0 FPS`.
→ **Solusi:** tambahkan Tabel tail-latency dan Tabel edge. Klaim §4.6 *"pada perangkat edge, OC-SORT lebih sesuai untuk mempertahankan real-time"* sekarang tidak berdiri di atas apa pun; dengan tabel itu, klaimnya jadi kuat (dan sekaligus jujur: Deep-OC-SORT **gagal** real-time di edge, 12 FPS — ini temuan yang layak ditulis, bukan disembunyikan).

**V3. Tiga kontradiksi angka yang akan langsung ditembak reviewer.**
- §4.3.1: Deep-OC-SORT galat **16,71%** (§4.3.2 menempelkan 16,71% ke `CD=30`) — tetapi §4.4.1: **"galat persentase terendah 14,64% pada CD=45"** dan "MAE terendah 6,34 pada CD=30". Mana yang jadi konfigurasi operasional? Kalau CD=45 lebih akurat dari CD=30, mengapa memilih CD=30?
- §4.4.2: **"galat terendah 1,67% pada threshold 0,20"** — angka ini satu orde lebih baik dari 13–16% di §4.3 dan tidak pernah dijelaskan basisnya (subset sekuens berbeda? lintasan GT?). Reviewer akan menganggap ini angka salah tempat.
- §4.2: LightTrack `Frag` 8.863 **lebih rendah** dari OC-SORT 27.646, padahal HOTA-nya jauh lebih rendah (22,53 vs 36,51) dan IDSW-nya setara. Ini butuh satu kalimat penjelasan, kalau tidak terbaca seperti tabel yang tidak konsisten.
→ **Solusi:** (a) tambahkan satu paragraf "pemilihan konfigurasi operasional" yang menjustifikasi CD=30 (MAE terendah + bias mendekati nol) **dan** menyebut 14,64% di CD=45 sebagai konsekuensi bias under-count (−4,38) yang tidak diinginkan; (b) pada §4.4.2, tulis basis perhitungan 1,67% secara eksplisit; (c) beri satu kalimat tentang fragmentasi LightTrack.

**V4. Kontradiksi jumlah tracker.**
Introduction hal. 3: *"dievaluasi menggunakan ketiga tracker"* → padahal §1 hal. 2 dan §3.2/§4.2 menyebut **empat** tracker (OC-SORT, DiffMOT, Deep-OC-SORT, LightTrack).
→ **Solusi:** seragamkan jadi empat di seluruh naskah.

**V5. §3.1 vs §4.2 soal arsitektur.**
§3.1: *"Hasil deteksi kemudian diteruskan ke **dua jalur tracking**, yaitu Deep-OC-SORT sebagai jalur utama… serta OC-SORT sebagai jalur ringan"* — tetapi §3.2 dan §4.2 mengevaluasi **empat** tracker, dan DiffMOT malah jadi yang terbaik di MOT20 lalu tetap tidak dipilih. Gambar 1 (yang hilang) pasti tidak bisa memuat keduanya sekaligus.
→ **Solusi:** pisahkan "jalur operasional" (Deep-OC-SORT utama + OC-SORT fallback) dari "kandidat yang dievaluasi" (4 tracker). Tulis dua kalimat berbeda untuk dua hal berbeda itu.

**V6. §4.5: "Latensi diukur dalam satuan mikrodetik"** sementara Tabel 7 semuanya **milidetik**.
→ Ganti jadi "milidetik".

**V7. Percepatan di Tabel 4 tidak konsisten dengan latensi di tabel yang sama.**
Tabel 4: YOLO26n `22,48 → 10,28 ms` dengan `2,24×`. 22,48/10,28 = **2,19**, bukan 2,24. Angka 2,24 berasal dari perbandingan *inference-only* (22,48/10,05 — sesuai `docs/reports/laporan-skenario-a` baris 358), sedangkan kolom "ONNX CPU total" sudah memasukkan post-processing.
→ **Solusi:** beri catatan kaki tabel: *"Percepatan dihitung dari latensi inferensi murni (PyTorch 22,48 ms → ONNX 10,05 ms); kolom ONNX CPU total termasuk post-processing 0,233 ms."* Atau ubah kolom jadi inference-only.

**V8. Konfound pengukuran GPU hilang — ini yang akan dipakai reviewer untuk menyerang klaim NMS-free.**
Laporan sumber eksplisit menyatakan: pengukuran GPU berada di rezim yang didominasi *overhead* peluncuran kernel (`YOLO26s` ~3,8× FLOPs `YOLO26n` tapi hanya 5,5% lebih lambat), dan **pada CPU + PyTorch justru YOLOv11n yang tercepat (21,14 ms), YOLO26n hanya tercepat pada kombinasi CPU + ONNX**. Naskah §4.1.2 menulis *"Keunggulan arsitektur NMS-free terukur pada latensi post-processing, bukan pada akurasi"* tanpa peringatan konfound ini, dan §4.1.1 menyimpulkan *"kapasitas model lebih berpengaruh dibandingkan perbedaan arsitektur"* tanpa menyebut bahwa kesimpulan itu hanya berlaku di jalur ONNX.
→ **Solusi:** tambahkan satu kalimat pembatas: *"Peringkat latensi bergantung pada kombinasi perangkat dan runtime: pada CPU dengan PyTorch, YOLOv11n justru tercepat; keunggulan YOLO26n terikat pada jalur ONNX Runtime."* Ini memperkuat, bukan melemahkan, naskah — karena menunjukkan penulis memahami kondisi pengukurannya.

**V9. Dua set angka CPU yang berbeda dari sumber yang sama tidak dijelaskan.**
`docs/reports/laporan-skenario-a` memuat dua tabel CPU: satu memberi YOLO26n ONNX **10,05 + 0,233 = 10,28 ms**, tabel lain **9,95 ms** (dan PyTorch 22,48 vs 23,06). Naskah memakai yang pertama tanpa menyebut variasi antar-run.
→ **Solusi:** sebutkan run/tanggal pengukuran dan variasi antar-run (mis. "±3% pada tiga pengulangan"), atau sajikan median.

**V10. Kontribusi dan rumusan masalah hilang dari Introduction.**
Draft repo (`docs/handoff/draft-sections-clean.md`) memuat **tiga pertanyaan penelitian**, tujuan eksplisit, ruang lingkup (TKT 3–4), dan roadmap lima tahun. Versi Word hanya menyisakan satu paragraf kontribusi generik. Editor JESTEC membaca latar → gap → **kontribusi** → roadmap; sekarang mata rantainya putus di kontribusi.
→ **Solusi:** tambahkan 1 paragraf rumusan masalah (3 pertanyaan, 1 kalimat masing-masing) + 1 paragraf kontribusi yang menyebut hal yang **spesifik**: (i) ablasi eksplisit counting logic vs naive line crossing pada deteksi identik, (ii) analisis sensitivitas cooldown & confidence threshold yang memetakan trade-off over/under-count, (iii) dekomposisi latensi end-to-end lintas perangkat.

**V11. Tidak ada pembandingan angka dengan SOTA people counting yang dikutip sendiri.**
§2.2 mengutip akurasi 85% (RoI quadrilateral) dan 98,42% (kaskade + Kalman Filter), lalu keduanya tidak pernah muncul lagi. Reviewer *people counting* akan menganggap ini celah wajib: kalau ada angka literatur, tabel hasil harus menempatkan 13,08–16,71% di sebelahnya, dengan penjelasan mengapa domain/metriknya tidak apple-to-apple.
→ **Solusi:** tambahkan Tabel perbandingan di akhir §2.2 atau awal §4.3: kolom `Studi | Pendekatan | Dataset | Metrik | Hasil | Batasan`. Lalu satu paragraf di §4.6 yang menjelaskan mengapa angka tidak bisa dibandingkan langsung (bentuk dataset, definisi metrik, garis hitung).

**V12. Typo dan kesalahan mekanis (semuanya di naskah, bukan preferensi).**
`berkaitn` · `mempertahakan` · `peningkata performa` · `dakam validasi` · `dikembangkansecara` · `anatara efisiensi` · `Propors` (kolom tabel terpotong dari "Proporsi") · `LightTra ck` · `Cooldown pen dek` · `3.Method` (tanpa spasi) · `4.Results and Discussion` (tanpa spasi) · `Tracker yang dibandingkan pada deteksi identik, yaitu OC-SORT, … , dibandingkan menggunakan…` (kata "dibandingkan" dua kali dalam satu kalimat) · `FPS.Berdasarkan` (tanpa spasi) · `69.905` vs `6.905` konsistensi pemisah ribuan · `Gambar` vs `Fig.` · `(N) frame (default 30)` — tanda kurung mengelilingi variabel tunggal tanpa alasan.
→ **Solusi:** jalankan pemeriksaan ejaan sekali penuh setelah semua revisi isi selesai. Jangan lakukan dua kali.

**V13. Notasi angka tidak sesuai naskah Inggris.**
`0,4974` · `0,8480` · `88,7–155,1%` (desimal koma) bercampur dengan `54.4 AP` · `10.70 ms` · `53.1 AP` · `98.42%` (desimal titik) di §2.1, dan pemisah ribuan bergaya Indonesia `6.905` / `14.293` berdampingan dengan desimal koma.
→ **Solusi:** dalam naskah Inggris: desimal titik (`0.4974`), pemisah ribuan koma (`6,905`) atau spasi tipis. Seragamkan keduanya sekaligus.

**V14. Tabel 6 dan Tabel 5 caption salah.**
`Table 6. Latensi pada CPU dengan ONNX Runtime` — itu caption Tabel 4, tersalin ke tabel ablasi counting. `Table 5. Hasil TrackEval pada deteksi YOLO26 yang sama` — teksnya bilang YOLO26**s**.
→ **Solusi:** `Table 6. Ablasi counting logic: naive line crossing vs state machine.` dan `Table 5. Hasil TrackEval pada deteksi YOLO26s yang sama.`

**V15. Klaim "DiffMOT … bersifat black-box" tidak akurat.** DiffMOT adalah metode open-source (kode tersedia), bukan model tertutup. Reviewer yang tahu bidangnya akan menandai ini.
→ **Solusi:** ganti dengan alasan yang benar: *"membutuhkan GPU, bergantung pada komponen diffusion dan Re-ID yang menambah dependensi serta latensi, serta tidak dapat berjalan pada perangkat sumber daya terbatas (12,0 FPS pada RX 6600)."*

**V16. Tabel 6 memuat kalimat di dalam sel angka.** Sel "Galat rata-rata" berisi `Galat rata-rata 88,7–155,1% bergantung jalur tracker` — bukan angka, dan judul kolomnya terulang di dalam selnya sendiri.
→ **Solusi:** isi sel dengan rentang saja (`88.7–155.1`), dan pindahkan penjelasan "bergantung jalur tracker" ke catatan bawah tabel.

**V17. Blok sitasi bergerombol.** §2.2: `[Hyun-SungYang][Said Baz Jahfar Khan][Kyujin Shim][Ruopeng Gao][Yuzhi Chen][Bishoy Galoaa]` (6 sumber, satu tembakan). §2.3: `[Ao Wang, 2024], [Yian Zhao]`.
→ **Solusi:** satu metode, satu kalimat, satu nomor. Mis. *"Sentinel [x] dan LightTrack-ReID [y] menempatkan confidence dan oklusi sebagai sinyal asosiasi utama, sedangkan DragonTrack [z] memakai graf-transformer untuk skenario padat dan OcclusionTrack [w] menambahkan depth-cascade matching."* JESTEC menghargai kalimat berisi, bukan penumpukan rujukan.

**V18. Etika, privasi, dan lisensi dataset tidak disinggung sama sekali.** Topik ini *people counting* dengan pelacakan identitas persisten di ruang publik; editor dan reviewer etika akan menanyakannya.
→ **Solusi:** tambahkan 2–3 kalimat di §3.4 atau §4.6: data yang dipakai hanya benchmark publik dengan lisensi riset (MOT20, DanceTrack, CrowdHuman), tidak ada perekaman orang nyata, tidak ada identifikasi biometrik, dan ID bersifat *session-scoped* serta tidak disimpan antar-sesi.

**V19. Metadata PDF membocorkan jejak template asing.**
Metadata file: `title: FORMAT INSTRUCTIONS FOR SOMChE 2004 PAPERS`, `author: Universiti Teknologi PETRONAS`. Untuk naskah *blind review*, ini bukan hanya ceroboh — ini sinyal bahwa dokumen dibangun dari template lain tanpa dibersihkan.
→ **Solusi:** di Word → *File → Info → Properties*: set Title = judul naskah, Author = (kosongkan), Comments = (kosongkan); lalu *Inspect Document → Remove All* sebelum export PDF.

**V20. Standar deviasi / sebaran antar-sekuens tidak dilaporkan.** Semua galat disajikan sebagai satu angka agregat dari 29 sekuens. Satu seed, satu angka rata-rata.
→ **Solusi:** tambahkan kolom std atau IQR per jalur tracker di Tabel 6 (datanya ada di `laporan-skenario-c-counting.md`), dan turunkan klaim "terbaik" menjadi "terendah pada konfigurasi yang diuji" selama masih satu seed. Ini biaya kecil yang mematikan serangan reviewer `"single seed, no error bars"`.

---

## C. BAGUS — jangan diubah

1. **Struktur skenario S1–S4 → hasil per sub-bab.** Pemetaan bersih dan mudah diikuti reviewer; setiap klaim bisa dilacak ke satu sub-bab.
2. **Tracker dievaluasi pada deteksi yang identik.** Ini praktik terbaik dan membedakan naskah ini dari banyak paper orang-counting yang membandingkan tracker memakai detektor aslinya masing-masing. Pertahankan kalimat §3.2 tentang hal ini — itu kekuatan metodologis utama.
3. **Ablasi state machine vs naive line crossing.** 101,99% → 16,71% (dan 88,7–155,1% antar jalur) adalah hasil yang berbicara sendiri. Ini kontribusi terkuat naskah dan alasannya sudah ditulis dengan benar.
4. **Dekomposisi latensi + penetapan anggaran 33,3 ms secara eksplisit.** Reviewer menyukai target yang dideklarasikan lalu diuji, bukan diuji lalu dijustifikasi.
5. **Kejujuran metodologis yang sudah ada**: §3.2 menyatakan hasil absolut tidak merepresentasikan capaian paper asli karena detektor berbeda; §4.6 menyebut limitasi single-seed dan deteksi offline. Jangan dihapus saat edit.
6. **Angka lolos lacak-balik.** Semua angka yang saya uji (0,4974; 103.115; 44,37; 6.905; 14.293; 27.646; 53,03; 57,76; 6,34; 1,67; 40,6; 24,61; 14,20; 9,45; 0,11; 0,85; 2,554/2,695/2,129/2,142; 0,164/0,170/0,167/0,491; 10,28; 23,15) ada di laporan eksperimen repo. Nol angka karangan. Ini kondisi terbaik yang bisa diharapkan sebelum review.

---

## D. Hasil fact-check

**TERVERIFIKASI terhadap repo (angkanya nyata, ada di `docs/reports/`):**

| Klaim di naskah | Sumber di repo | Status |
|---|---|---|
| 4.370 citra val, 103.115 kotak | `laporan-skenario-a`, `3-method.md` | ✅ |
| mAP@0.5:0.95 YOLO26s 0,4974 | `laporan-skenario-a` | ✅ |
| Tabel 3 (2,554/2,695/2,129/2,142; 0,164/0,170/0,167/0,491) | `laporan-skenario-a` baris 330-333 | ✅ |
| Tabel 4 (22,48/10,28; 54,50/23,15; 25,13/12,13; 22,98/14,05) | `laporan-skenario-a` baris 358-361 | ✅ (tapi lihat V6/V9) |
| HOTA 44,37 / MOTA 60,91 / IDF1 53,86 / IDSW 6.905 (DiffMOT, MOT20) | `laporan-skenario-b-tracker` baris 98 | ✅ |
| 179 deteksi/frame, puncak 272 | `laporan-skenario-b-tracker` | ✅ |
| Galat 13,08 / 16,71 / 53,03%; prediksi 57,76 vs GT 44,62 | `laporan-skenario-c-counting` | ✅ |
| CD=0 → 101,99%; MAE 6,34 @CD=30; 14,64% @CD=45 | `laporan-sensitivitas-parameter` | ✅ |
| 1,67% @conf 0,20; 39,2–43,0 FPS | `laporan-sensitivitas-parameter` | ✅ |
| Latensi 14,20 / 9,45 / 0,11 / 0,85 / total 24,61 ms / 40,6 FPS | `laporan-skenario-d-realtime` | ✅ |
| P95 32,10 ms, 95% frame < 33,3 ms | `laporan-skenario-d-realtime` baris 55-58 | ✅ (tapi tidak muncul di naskah → V2) |

**UNVERIFIED / belum bisa diverifikasi:**
- **`[Ao Wang 2024]` dan `[Yian Zhao]`** dipakai berdampingan sebagai klaim YOLOv10 54,4 AP dan RT-DETR 53,1 AP@108 FPS tanpa entri bib. Sumber ada di ledger (S003/S004) tapi entri bib belum saya cocokkan ke angka spesifiknya. Wajib dicek sebelum menomori.
- **`Chakrabarty, 2026` + `Ultralytics, 2026`** (klaim status YOLO26) — ada di `references.bib` baris 73, tapi tahun/venue harus dipastikan konsisten saat menomori.
- **`Song et al., 2026`**, **`McCarthy et al., 2025`**, **`momand 2025`/`mansouri 2025`**, **`Chen et al., 2025`**, **`Holla et al., 2024`** — dipakai in-text di Introduction dengan huruf kecil/nama tidak lengkap; belum saya buktikan ada di bib. Ini yang paling berisiko jadi **phantom citation**.
- **`O'Rourke, 1998`** (tes CCW) — buku *Computational Geometry in C*, klaim benar secara isi, tapi butuh entri bib.
- **`Dollár et al., 2012`** (MR⁻²) dipakai di `3-method.md` — hanya perlu dipastikan ada entri bila metrik itu dipertahankan di naskah.

**Kesimpulan fact-check:** tidak ada metrik palsu. Yang ada adalah **30+ sitasi tanpa bibliografi**, dan itu masuk kategori FLOOR (integritas sitasi 2/10 → naskah **tidak layak** selama daftar pustaka belum ada).

---

## E. Kepatuhan template JESTEC — checklist cepat

| Persyaratan resmi JESTEC | Status naskah |
|---|---|
| Template Blind Review Word | ⚠️ dipakai, tapi placeholder template masih tersisa (R7) |
| Semua identitas dihapus (nama, afiliasi, acknowledgment, grant) | ✅ di badan naskah — ⚠️ metadata PDF masih berisi author asing (V19) |
| Urutan: Judul → (Authors) → Abstract → Keywords → Introduction → Theory → Methodology → Results → Conclusions → Nomenclature → References → Appendix | ❌ tidak ada Nomenclature, tidak ada References, Appendix berisi template |
| Abstract 100–200 kata | ❌ masih abstract template |
| Keywords ≤5, alfabetis | ❌ masih keywords template |
| Gambar `Fig. 1`, caption di bawah; Tabel `Table 1`, caption di atas; persamaan `Eq. (1)` | ❌ campur `Gambar`/`Fig`, caption gambar tidak ada, persamaan tidak bernomor |
| Simbol miring, satuan SI, semua simbol di Nomenclature | ❌ tidak ada Nomenclature |
| Panjang 10–15 hlm | ✅ 15 hlm (setelah References + Nomenclature masuk akan jadi ~18 → perlu memangkas; lihat S1) |
| Bahasa English (UK) | ❌ Bahasa Indonesia |
| References bernomor urut kemunculan | ❌ tidak ada |
| Declaration of Generative AI (wajib sejak 1 Mei 2026) | ❌ tidak ada |
| Turnitin ≤20% | belum diuji |

---

## F. Saran (penguatan, bukan kewajiban)

**S1. Pemangkasan terkendali.** Setelah Nomenclature + References masuk, naskah melewati 15 halaman. Yang paling aman dipotong: tabel Tabel 1 dan Tabel 2 gabung (metrik overlap), dan §2.1 dipendekkan — status YOLO26 sebagai preprint/vendor sudah dinyatakan di Introduction dan §2.1, cukup sekali.
**S2. Tabel perbandingan SOTA** di akhir §2.2 (`Studi | Pendekatan | Dataset | Metrik | Hasil | Batasan`) — ini yang paling sering diminta reviewer di jurnal jenis ini, dan bahannya sudah ada di `docs/research/source-ledger.md`.
**S3. Tabel ringkasan per-skenario** di awal §4 (`Skenario | Konfigurasi | Metrik utama | Hasil | Verdict`), supaya editor bisa menilai kontribusi dari satu tabel.
**S4. Analisis galat kualitatif.** Satu gambar contoh kasus ID switch/gagal hitung + 3 kalimat penyebabnya akan jauh lebih persuasif daripada angka agregat.
**S5. Pernyataan ketersediaan kode.** `Data availability statement` singkat (repo GitHub, atau "kode tersedia atas permintaan") menaikkan kesan reproduktifitas. Sesuai kebiasaan Anda: repo publik tanpa tooling AI/raw data.
**S6. Turunkan klaim "terbaik" selama satu seed.** "DiffMOT memberikan hasil terbaik" → "DiffMOT memberikan galat terendah pada konfigurasi yang diuji (satu seed)". Lebih kuat, bukan lebih lemah.

---

## G. Perbaikan urut prioritas (kerjakan dari atas)

1. Abstract + Keywords diganti (R1, R2).
2. Conclusions ditulis (R3).
3. References disusun dari `references.bib`, dinomori urut kemunculan; semua sitasi in-text dikonversi (R4, R5) — **ini yang menjaga naskah dari tuduhan sitasi fiktif.**
4. Keputusan bahasa: terjemahkan penuh ke English (UK) atau ganti venue (R6).
5. Header/footer/Appendix template dibersihkan; Nomenclature + Declaration AI ditambahkan (R7, R10).
6. Definisi metrik hitung dipindahkan dari `3-method.md` ke naskah (V1).
7. Tabel tail-latency + edge ditambahkan; klaim §4.6 diberi sandaran (V2).
8. Tiga kontradiksi angka diselesaikan (V3).
9. Semua gambar ditempel + caption + penomoran seragam (R8).
10. Typo, notasi desimal, caption tabel, metadata PDF (V12–V19).

---

### Formula cari → ganti yang bisa langsung dipakai (10 teratas)

| # | Cari di naskah | Ganti menjadi |
|---|---|---|
| 1 | Abstract proyektil (paragraf 1–2) | Abstract people counting 100–200 kata (lihat R1) |
| 2 | `Keywords: Aerodynamics, Forebody and afterbody, Next keyword, Projectile, Supersonic speed.` | `Keywords: Crowd counting, Multi-object tracking, NMS-free detector, Real-time video analytics, Trajectory-based counting` |
| 3 | `A. B. One and X. Y. Two` (header) | *(hapus)* |
| 4 | `This is the Template You Use to Format and Prepare Your Manuscript` (footer) | *(hapus)* |
| 5 | `Appendix A` s.d. `Fig. A-1…` (hal. 15) | *(hapus, atau ganti listing pipeline inti)* |
| 6 | `dievaluasi menggunakan ketiga tracker` | `dievaluasi menggunakan empat tracker` |
| 7 | `Latensi diukur dalam satuan mikrodetik untuk setiap tahap komputasi.` | `Latensi diukur dalam milidetik untuk setiap tahap komputasi.` |
| 8 | `Table 6. Latensi pada CPU dengan ONNX Runtime` | `Table 6. Ablasi counting logic: naive line crossing vs state machine.` |
| 9 | `DiffMOT memberikan kinerja terbaik, tetapi membutuhkan GPU, bersifat black-box, dan memiliki kompleksitas dependensi yang lebih tinggi.` | `DiffMOT memberikan galat hitung terendah, tetapi membutuhkan GPU, bergantung pada komponen diffusion dan Re-ID yang menambah latensi, dan tidak dapat mempertahankan real-time pada perangkat sumber daya terbatas (12,0 FPS pada RX 6600).` |
| 10 | `: (tambahkan screenshot dashboard)` (di sel Tabel 6) | *(hapus; sisipkan screenshot sebagai Fig. 9 dengan caption)* |

---

*Catatan review: penuh, tidak ada bagian yang saya baca sekilas. Tiga hal yang saya maklumi sebagai pekerjaan berjalan (judul, sitasi, screenshot dashboard) tetap saya nilai posisinya di atas agar tidak terlupa, tetapi tidak saya jadikan dasar verdict. Verdict murni ditentukan oleh R1, R3, R4, R6, dan V1.*
