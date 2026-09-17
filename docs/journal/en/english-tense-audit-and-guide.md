# Audit Bahasa Inggris + Panduan Tense — Naskah JESTEC (RANCAGE)

**Tanggal kerja:** 17 September 2026
**Masukan yang diaudit:** *"saya baca sekilas. bahasa inggris dibuat lebih precise. masih tampak translate-an dari bhs indo ke inggris. prompt nya: selain meminta mem-formalkan bahasa inggris untuk penulisan jurnal, tambahkan pemilihan tenses nya. latar belakang, tujuan, dan kesimpulan pakai simple tense. metodologi, hasil temuan menggunakan past tense."*
**Objek:** `docs/journal/en/jestec-manuscript-en.md` (sumber) dan eksportnya `JESTEC ENGLISH PEOPLE COUNTING.docx`.
**Status:** audit + daftar perbaikan siap-terap. Belum ada naskah yang diubah.

---

## 0. Diagnosis: keluhan itu sebenarnya tentang tiga hal, bukan satu

| # | Yang dirasakan reviewer | Yang sebenarnya terjadi di naskah |
| --- | --- | --- |
| A | "masih tampak translate-an" | Sisa bahasa Indonesia dan format angka Indonesia masih hidup **di dalam tabel** docx yang diekspor (4 header + 107 sel angka berkoma). Prosa sudah Inggris, tabel belum. |
| B | "bahasa inggris dibuat lebih precise" | Beberapa klaim hasil studi lain ditulis seolah fakta universal (`reaches over 700 FPS`, `needs 16.4 s`) tanpa penanda atribusi dan tanpa perangkat/acuan. Juga beberapa kalimat hasil yang menjanjikan lebih dari yang didukung desain (`guarantees one count per identity`). |
| C | "tambahkan pemilihan tenses" | §3 Method adalah tempat terparah: dalam satu subbagian ada `Four trackers were chosen` (past) berdampingan dengan `All models are fine-tuned` (present) untuk pekerjaan yang sama. §4 Results juga banyak present (`gives`, `is the lightest`, `shows up`). Pembaca merasa acak karena memang acak. |

Intinya: reviewer tidak salah. Yang ia sebut "translate-an" sebagian besar = tense yang tidak konsisten + sisa tabel Indonesia, bukan gramatikal.

---

## 1. Aturan tense yang dipakai mulai sekarang

### 1.1 Prinsip tunggal (bukan daftar hafalan)

Tense menandai **status klaim**, bukan waktu:

- **Past tense** = kejadian spesifik yang sudah selesai dan terikat waktu: eksperimen yang dijalankan, angka yang diukur, apa yang penulis lakukan.
- **Present tense** = pernyataan yang berlaku umum/sekarang: fakta bidang ilmu, definisi, deskripsi arsitektur sistem sebagai artefak, makna temuan, batasan, arah kerja berikutnya.

Satu kalimat boleh mengandung keduanya, dan itu benar: `Because no enzymatic activity was detected [past] in the absence of magnesium, our results indicate [present] that magnesium is required [present]` (AJE, 2015).

### 1.2 Peta per bagian

| Bagian | Tense | Yang masuk present | Yang masuk past |
| --- | --- | --- | --- |
| Title | present (bila berupa kalimat) | kesimpulan yang didukung naskah | — |
| Abstract | campuran | latar belakang, tujuan, kesimpulan | metode, hasil |
| **1. Introduction** | **present** | fakta umum, urgensi, rumusan masalah, tujuan ("this study develops…"), peta struktur naskah | studi spesifik terdahulu sebagai peristiwa ("Smith et al. sampled…") |
| **2. Related Works** | campuran terkendali | fakta desain yang sudah mapan (mekanisme YOLOv10, definisi HOTA), klaim yang sudah mapan di bidang | apa yang **diukur/dilaporkan** studi tertentu (angka HOTA/AP/FPS) |
| **3. Method** | **past** | peta bagian, definisi persamaan/simbol, fakta mekanisme metode pihak ketiga | semua yang kita lakukan: memilih, fine-tune, menyatukan parameter, mengevaluasi, mengukur |
| **4. Results** | **past** | rujukan `Fig. 2 shows` / `Table 5 shows`, fakta umum tentang dataset, interpretasi satu kalimat | semua temuan dan angka penelitian ini |
| **4.6 Discussion** | **present** | interpretasi, implikasi, batasan | kalimat yang **mengulang** angka hasil tertentu |
| **5. Conclusions** | present untuk makna, past untuk laporan | makna temuan, kontribusi, arah kerja berikutnya | kalimat "apa yang dikerjakan/ditemukan" |

### 1.3 Empat pengecualian yang **tetap present** di dalam Method/Results

Ini yang sering bikin orang mengubah semua kalimat jadi past lalu hasilnya makin aneh. Jangan diubah:

1. **Peta bagian dan rujukan gambar/tabel** — `This section describes…`, `Table 1 shows…`, `Fig. 4(a) shows…`. Naskah masih ada di depan pembaca.
2. **Definisi matematis** — `The two segments intersect when…`, `D > 0 indicates the IN direction`. Definisi tidak pernah "terjadi".
3. **Mekanisme metode pihak ketiga** — `YOLOv10 aligns the one-to-many and one-to-one processes…`, `OC-SORT uses an observation-centric mechanism…`. Ini fakta desain, bukan tindakan kita. (Kalau yang dilaporkan adalah *hasil* metode itu, balik ke past: `was reported to reach 54.4 AP`.)
4. **Klaim umum tentang dataset** — `MOT20 is dense: an average of 179 detections per frame`. Ini properti dataset, bukan temuan kita.

### 1.4 Rekonsiliasi dengan instruksi reviewer

Instruksi reviewer — *"latar belakang, tujuan, dan kesimpulan pakai simple tense; metodologi, hasil temuan menggunakan past tense"* — **konsisten** dengan konvensi di §1.2, dengan dua catatan yang perlu disampaikan balik supaya tidak jadi salah paham:

1. **"Hasil temuan pakai past"** juga berlaku untuk **temuan studi lain** di Related Works (`was reported to reach HOTA 62.3`), bukan hanya temuan kita. Ini yang membuat naskah terasa lebih precise: angka pinjaman jadi punya atribusi.
2. **Kesimpulan** tidak bisa 100% present. Kalimat yang melaporkan kembali hasil tetap past (`the counting logic added only 0.11 ms`); yang present adalah kalimat maknanya (`ID stability and trajectory validation therefore matter…`). Kalau penguji tetap minta seluruh §5 present, konversinya ada di §4.6 di bawah — tapi saya tidak menyarankan, karena `suppresses the error to 13.08%` terbaca sebagai hukum umum, bukan hasil satu konfigurasi.

### 1.5 Aturan presisi (bagian "lebih precise")

Satu baris per aturan, semuanya bisa dicek:

1. **Setiap angka pinjaman wajib punya penanda atribusi** — `was reported to reach`, `reported`, atau satuan acuan (nama dataset, perangkat). Angka tanpa acuan adalah klaim universal palsu.
2. **Hindari kata kerja absolut** untuk hasil satu konfigurasi: `guarantees`, `proves`, `always`. Ganti dengan batas yang benar-benar diuji (`allows at most one count per identity within each cooldown window`).
3. **Kata yang menggantikan istilah bidang harus dikembalikan** — `connected components` → `coupled components`; `follow how objects move` → `track how objects move`.
4. **Kolokasi verba+benda** — `conducted a study`, `drew a comparison`, `yielded a result`, `raised a concern`. Bukan `made an analysis`.
5. **Angka dan satuan konsisten**: desimal titik, pemisah ribuan koma (JESTEC), satuan SI, dan tidak mencampur `%` dengan proporsi di satu kolom.

---

## 2. Dasar aturan: sumber terverifikasi

Aturan di §1 tidak saya karang. Yang diverifikasi:

| Sumber | Jenis bukti | Yang diambil |
| --- | --- | --- |
| **JESTEC — "Submit a paper"**, Taylor's University. https://jestec.taylors.edu.my/submit%20a%20paper.htm | Pedoman jurnal (diakses 17 Sep 2026) | Menetapkan **English (UK)**, 10–15 hlm, struktur bagian, `Fig./Table/Eq.`, AI declaration. **JESTEC tidak menetapkan aturan tense.** Jadi konvensi tense di §1 berasal dari pedoman penulisan ilmiah, bukan house style JESTEC — penting agar tidak salah diklaim ke reviewer. |
| **AJE — "Verb Tense in Scientific Manuscripts"** (2015). https://files-aje-com.s3.amazonaws.com/www/row/_assets/docs/AJE-Choosing-the-Right-Verb-Tense-for-Your-Scientific-Manuscript-2015.pdf | Pedoman penyuntingan naskah, dipakai luas | Peta tense per bagian (Methods past; Results past; Abstract campuran) + kalimat contoh campuran past/present yang saya kutip di §1.1 |
| **EASE Guidelines for Authors and Translators** (2017/2018), EASE. https://urologyjournal.ru/apps/ur_en/assets/uploads/ease-guidelines-2017-english.pdf | Pedoman editor jurnal Eropa | "Past tense untuk bagaimana studi dilakukan dan apa yang ditemukan; present untuk pernyataan umum, interpretasi, dan isi tabel/gambar." Juga panduan Abstract 5-elemen (BACKGROUND/OBJECTIVES/METHODS/RESULTS/CONCLUSIONS). |
| **CASRAI — "Verb Tense Conventions in Research Papers"**, diperbarui 23 Agustus 2026. https://casrai.org/guides/verb-tense-conventions-in-research-papers | Panduan penulisan ilmiah, mengacu APA Publication Manual 7th ed. dan ICMJE | Perumusan "tense menandai status klaim"; Results **past tanpa pengecualian kecuali rujukan tabel/gambar**; Literature review = past/present perfect/present sesuai kematangan klaim |
| **Brandeis University Writing Program — "Verb Tenses: Science"**. https://www.brandeis.edu/writing-program/resources/students/handouts/verb-tenses-science-handout.pdf | Handout penulisan akademik | "Jangan pakai present untuk melaporkan penelitian orang lain"; present untuk ide yang masih benar sampai sekarang |
| **Academic Phrasebank**, University of Manchester. https://www.phrasebank.manchester.ac.uk/ (PDF 2016: https://wetenschappelijkschrijven.nl/wp-content/uploads/2023/02/Academic-Phrases-Manchester-Universiy.pdf) | Bank frasa, korpus 100 disertasi pascasarjana + artikel | Sumber frasa pengganti yang **bukan** AI-slop, per fungsi retoris (Introducing work, Describing methods, Reporting results, Writing conclusions) |

**Bukti peer-reviewed bahwa ini konvensi lintas disiplin (bukan selera satu penguji):**

| Studi | Temuan yang relevan | Identifier |
| --- | --- | --- |
| Salager-Meyer, F. *A text-type and move analysis study of verb tense and modality distribution in medical English abstracts*. English for Specific Purposes, 1992 | Studi klasik distribusi tense per *move* pada abstrak | doi:10.1016/s0889-4906(05)80002-x |
| Hardjanto, T. D. *Rhetorical Patterns, Verb Tense, and Voice in Cross-Disciplinary Research Article Abstract*, 2017 | 40 abstrak, 4 bidang: present aktif dominan di Move 1 (latar) & Move 4 (evaluasi); **past pasif dominan di Move 2 (prosedur)**; past aktif di Move 3 (hasil) | doi:10.22146/jh.v28i1.11410 |
| *Analyses of Move Structure and Verb Tense of Research Article Abstracts in Applied Linguistics*, 2011 | 90 abstrak: present di move 1–2 & 5; **past di move 3–4 (metode & hasil)** | doi:10.5539/ijel.v1n2p27 |
| *The distribution of verb tenses and modals in journal articles' abstracts*, 2017 | 100 abstrak, 4 rumpun ilmu: mayoritas **present simple + past simple**, sedikit present perfect | doi:10.2989/16073614.2017.1373366 |

Tiga studi korpus terakhir mengukur naskah nyata dan hasilnya persis pola yang diminta reviewer. Ini amunisi kalau pola tense naskah dipertanyakan.

> Catatan disiplin sumber: DOI di atas diambil dari metadata penelusuran (bukan dibaca penuh). Sebelum masuk ke daftar pustaka naskah, venue/volume/halaman tiap entri wajib diverifikasi ulang — aturan proyek: jangan mengarang sitasi.

---

## 3. Referensi korpus untuk phrasing — paper yang dibaca sebagai acuan gaya

Ini bagian yang diminta: *"mungkin dari paper lain yang bisa dijadikan referensi untuk translate-an ini"*. Dua kelompok, fungsinya berbeda.

### 3.1 Acuan register jurnal tujuan (cara JESTEC menulis)

| Paper | Venue | Yang diambil |
| --- | --- | --- |
| *Durian detection and counting system using deep learning*, A. H. A. Azizi dkk., hlm. 2470–2477 | **JESTEC** Vol. 18 Issue 5, https://jestec.taylors.edu.my/V18Issue5.htm | Satu-satunya paper JESTEC yang saya temukan dengan kombinasi deteksi + counting. Acuan register: bagaimana jurnal ini menulis abstrak, jumlah, dan klaim performa. |

Cara pakai: baca 1 paper JESTEC sejenis, catat 10 pola kalimat yang menyebut angka hasil dan rujukan tabel. Naskah kita harus berbunyi seperti itu.

### 3.2 Acuan istilah dan cara melaporkan angka (paper asli tiap metode)

Naskah kita mengutip metode ini, jadi kalimat kita harus memakai kata kerja dan penamaan yang sama dengan penulis aslinya. Ini yang menghilangkan kesan "translate-an": istilah berpindah utuh, bukan diterjemahkan ulang.

| Paper asli | Yang diambil | Identifier di naskah |
| --- | --- | --- |
| Cao dkk. *Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking* | Penamaan `ORU`, `OCM`, `OCR`, `observation-centric` — jangan diparafrase jadi "re-update, momentum, recovery" saja tanpa akronim | [4] |
| Lv dkk. *DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction* | Cara menyebut prediction non-linear & pelaporan FPS dengan perangkat | [7] |
| Maggiolino dkk. *Deep OC-SORT: Multi-Pedestrian Tracking by Adaptive Re-Identification* | Penamaan *appearance embedding* + *exponential moving average* | [8] |
| Dendorfer dkk. *MOT20: A benchmark for multi object tracking in crowded scenes* | Cara mendeskripsikan kepadatan (`detections per frame`) | [10] |
| Sun dkk. *DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion* | Alasan dataset diadakan — dipakai untuk paragraf dataset | [11] |
| Ristani dkk. *Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking* | Definisi resmi IDF1 dan cara melafalkannya | [28] |

Cara pakai (murah dan berdampak): untuk **setiap** angka hasil dari studi lain yang muncul di Related Works, buka abstract paper aslinya, lalu tiru struktur kalimat pelaporannya. Contoh arah: DiffMOT melaporkan `22.7 FPS on an NVIDIA RTX 3090`; kalimat kita harus menyebut perangkat itu dengan tense past + penanda atribusi, bukan `reaches`.

---

## 4. Audit naskah — daftar perubahan siap-terap

Rujukan `L…` = nomor baris di `docs/journal/en/jestec-manuscript-en.md` (350 baris).

### 4.1 Abstract (L11)

| # | Sebelum | Sesudah | Dasar |
| --- | --- | --- | --- |
| 1 | `Evaluation uses CrowdHuman for detection and MOT20 together with DanceTrack, covering 29 sequences, for tracking and counting.` | `Evaluation used CrowdHuman for detection and MOT20 together with DanceTrack, covering 29 sequences, for tracking and counting.` | Abstrak: metode → past |
| 2 | `YOLO26s reaches mAP@0.5:0.95 of 0.4974` | `YOLO26s reached mAP@0.5:0.95 of 0.4974` | hasil → past |
| 3 | `DiffMOT gives the strongest association` | `DiffMOT gave the strongest association` | hasil → past |
| 4 | `Deep-OC-SORT is selected as the main tracker because it balances accuracy against computational cost` | `Deep-OC-SORT was selected as the main tracker because it balanced accuracy against computational cost` | keputusan yang diambil → past |
| 5 | `a state machine with cooldown lowers the error from 88.7–155.1% … to 13.08–16.71%` | `… lowered the error from …` | hasil → past |
| — | `Trajectory validation and identity state memory therefore matter…` | *tetap* | kesimpulan → present (§1.2) |

### 4.2 Introduction (L19–L31) — sudah present, hanya presisi

| # | Sebelum | Sesudah | Alasan |
| --- | --- | --- | --- |
| 6 | `It leans entirely on an operator, which makes consistency hard to hold once the number of objects grows.` | `It depends entirely on an operator, so consistency becomes difficult to maintain as the number of objects grows.` | `lean on` + `hard to hold` = register percakapan |
| 7 | `preserve identity and follow how objects move between frames so that inflow and outflow can be recovered consistently` | `preserve identity and track how objects move between frames so that inflow and outflow are counted consistently` | `recover a count` bukan kolokasi bidang; `follow` → `track` |
| 8 | `Current studies show people counting developing along several paradigms with distinct characteristics.` | `Work on people counting currently follows several paradigms with distinct characteristics.` | `show X developing` bukan konstruksi Inggris alami (calque dari `menunjukkan … berkembang`) |
| 9 | `with detection, tracking and counting logic treated as connected components` | `… treated as coupled components` | `connected components` = istilah khusus (graf); maksudnya digabung |

### 4.3 Related Works (L35–L45) — angka pinjaman → past + atribusi

| # | Sebelum | Sesudah |
| --- | --- | --- |
| 10 | `YOLOv10 [13] is reported to reach 54.4 AP at 10.70 ms latency, while RT-DETR [14] reaches 53.1 AP at 108 FPS; RF-DETR [15], D-FINE [16] and DEIM [17] report improved accuracy-latency efficiency` | `YOLOv10 [13] was reported to reach 54.4 AP at 10.70 ms latency, while RT-DETR [14] reached 53.1 AP at 108 FPS; RF-DETR [15], D-FINE [16] and DEIM [17] reported improved accuracy-latency efficiency` |
| 11 | `YOLOv7 on a Raspberry Pi 4B needs 16.4 s per inference, whereas YOLOv7-tiny INT8 on a Jetson Orin Nano needs only 0.008 s at mAP 0.936 [18]. LCDnet, with 0.05M parameters, also holds its accuracy on a Jetson Nano through distillation from CSRNet [19].` | `YOLOv7 on a Raspberry Pi 4B needed 16.4 s per inference, whereas YOLOv7-tiny INT8 on a Jetson Orin Nano needed only 0.008 s at mAP 0.936 [18]. LCDnet, with 0.05M parameters, also held its accuracy on a Jetson Nano through distillation from CSRNet [19].` |
| 12 | `A quadrilateral RoI with virtual-line events and persistent IDs reaches 85% counting accuracy, while cascaded detection with a Kalman filter reaches up to 98.42% … [2][20]` | `… reached 85% counting accuracy, while cascaded detection with a Kalman filter reached up to 98.42% …` |
| 13 | `Passenger flow work based on YOLO and edge AI likewise shows that directional line crossing requires per-ID position history across frames [21].` | `… likewise showed that directional line crossing requires per-ID position history across frames [21].` |
| 14 | `OC-SORT improves on SORT through ORU, OCM and OCR and reaches over 700 FPS [4], while DiffMOT targets non-linear motion and reaches HOTA 62.3 / IDF1 63.0 at 22.7 FPS on DanceTrack with an RTX 3090 [7].` | `OC-SORT improves on SORT through ORU, OCM and OCR and was reported to reach above 700 FPS [4], while DiffMOT targets non-linear motion and was reported to reach HOTA 62.3/IDF1 63.0 at 22.7 FPS on DanceTrack with an RTX 3090 [7].` |

Catatan presisi untuk #14: `reaches over 700 FPS` menyembunyikan perangkat dan protokol. `was reported to` + menyebut perangkat adalah batas minimum yang jujur tanpa membuka papernya. Kalau paper [4] dibuka, ganti dengan angka dan perangkat persisnya.

### 4.4 Method (L49–L89) — sumber masalah utama

| # | Baris | Sebelum | Sesudah |
| --- | --- | --- | --- |
| 15 | L53 | `Video is processed by YOLO26 with an NMS-free head to produce bounding boxes and confidence scores [13]. The detection output is then passed to two tracking paths… The tracklets are evaluated by the counting logic, which uses polygon RoIs and virtual lines to validate the direction of movement. ID State Memory holds the status of every identity so that double counting from occlusion or back-and-forth movement is prevented [21].` | `Video was processed by YOLO26 with an NMS-free head, which produced bounding boxes and confidence scores [13]. The detection output was then passed to two tracking paths… Tracklets were evaluated by the counting logic, which used polygon RoIs and virtual lines to validate the direction of movement. ID State Memory held the status of every identity so that double counting from occlusion or back-and-forth movement was prevented [21].` |
| 16 | L59 | `The detection component uses the Ultralytics YOLO family, comparing NMS-free architectures (YOLOv10 and YOLO26) against an NMS-based architecture (YOLOv11). All models are fine-tuned on CrowdHuman [27] using amodal fbox annotations.` | `The detection component used the Ultralytics YOLO family and compared NMS-free architectures (YOLOv10 and YOLO26) against an NMS-based architecture (YOLOv11). All models were fine-tuned on CrowdHuman [27] using amodal fbox annotations.` |
| 17 | L59 | `To keep the comparison consistent, all trackers are evaluated on the same YOLO26 detection output.` | `… all trackers were evaluated on the same YOLO26 detection output.` |
| 18 | L63 | `Every tracker outputs in tlwh format with a standardised track_id, so counting logic does not depend on a particular implementation.` | `Every tracker output boxes in tlwh format with a standardised track_id, so the counting logic did not depend on a particular implementation.` |
| 19 | L67 | `The counting component of RANCAGE evaluates the trajectory of each ID … The approach adopts the virtual-line RoI concept used in people counting [29].` | `The counting component of RANCAGE evaluated the trajectory of each ID … The approach adopted the virtual-line RoI concept used in people counting [29].` |
| 20 | L67 | `Model A (naive line crossing) records an object when its trajectory crosses the virtual line with no state memory, which leaves it vulnerable to spatial jitter and tracking noise` | `Model A (naive line crossing) recorded an object when its trajectory crossed the virtual line with no state memory, which left it vulnerable to spatial jitter and tracking noise` |
| 21 | L67 | `Only centroids inside the RoI polygon are processed. A crossing is determined from the trajectory segment between the last two points` | `Only centroids inside the RoI polygon were processed. A crossing was determined from the trajectory segment between the last two points` |
| 22 | L67 | `Intersection is tested with the counterclockwise (CCW) test for line segments [31]:` | `Intersection was tested with the counterclockwise (CCW) test for line segments [31]:` |
| 23 | L77 | `The counting layer tracks the status of each identity through two operational states… When a trajectory crosses the virtual line, the system emits a count and puts that identity into COOLDOWN for 30 frames, during which it cannot trigger another count. Once the cooldown ends, the identity can be counted again on the next crossing. The mechanism therefore guarantees one count per identity within each cooldown window, not one count for the whole session. Although RoI filtering is available in the implementation, it was not enabled in the experimental configuration.` | `The counting layer tracked the status of each identity through two operational states… When a trajectory crossed the virtual line, the system emitted a count and put that identity into COOLDOWN for 30 frames, during which it could not trigger another count. Once the cooldown ended, the identity could be counted again on the next crossing. The mechanism therefore allows at most one count per identity within each cooldown window, not one count for the whole session. RoI filtering was available in the implementation but was not enabled in the experimental configuration.` |
| 24 | L81 | `Three public datasets are used… CrowdHuman evaluates… MOT20 evaluates tracking and counting under high-density crowd conditions [10], while DanceTrack [11] tests tracker robustness` | `Three public datasets were used… CrowdHuman evaluated… MOT20 evaluated tracking and counting under high-density crowd conditions [10], while DanceTrack [11] tested tracker robustness` |
| 25 | L89 | `The system evaluation has four main scenarios (S). S1 evaluates … and compares zero-shot against fine-tuned configurations. S2 compares trackers … S3 evaluates the effect of the counting logic by comparing Model A and Model B, and by a sensitivity analysis … S4 evaluates end-to-end performance through FPS and tail latency …` | `The system evaluation comprised four main scenarios (S). S1 evaluated … and compared zero-shot against fine-tuned configurations. S2 compared trackers … S3 evaluated the effect of the counting logic by comparing Model A and Model B and by a sensitivity analysis … S4 evaluated end-to-end performance through FPS and tail latency …` |
| — | L49, L59 | `This section describes the design…`, `In YOLOv10 the consistent dual label assignment aligns the one-to-many and one-to-one processes, so inference runs on a single head without NMS [13].`, `OC-SORT uses an observation-centric mechanism…`, `DiffMOT uses a diffusion-based motion predictor…` | ***tetap present*** — pengecualian §1.3 (peta bagian + mekanisme pihak ketiga). Jangan diubah. |

### 4.5 Results (L95–L226) — temuan → past

| # | Baris | Sebelum | Sesudah |
| --- | --- | --- | --- |
| 26 | L99 | `YOLOv11n leads marginally on mAP@0.5 … but trails YOLO26n on mAP@0.5:0.95 … YOLO26n is also the lightest in that tier… YOLO26s sits in the tier above, with 9.95 million parameters and 22.5 GFLOPs, and is reported as the extended configuration when accuracy is the priority.` | `YOLOv11n led marginally on mAP@0.5 … but trailed YOLO26n on mAP@0.5:0.95 … YOLO26n was also the lightest in that tier… YOLO26s sat in the tier above, with 9.95 million parameters and 22.5 GFLOPs, and served as the extended configuration when accuracy was the priority.` |
| 27 | L101 | `because they offer no equivalent scale path … so the s-tier comparison uses the vendor benchmark` | `because they offered no equivalent scale path … so the s-tier comparison used the vendor benchmark` |
| 28 | L112 | `YOLO26s again gives the best results … That recall ceiling shows some objects remain undetected … Objects cut by the frame edge also show a larger drop in recall and AP` | `YOLO26s again gave the best results … That recall ceiling showed that some objects remained undetected … Objects cut by the frame edge also showed a larger drop in recall and AP` |
| — | L112 | `These findings support placing the RoI and counting line away from the frame edge.` | *tetap* — implikasi → present |
| 29 | L125 | `The advantage of the NMS-free architectures shows up in post-processing latency rather than in accuracy. On the RTX 4090 the NMS-free models need 0.164–0.170 ms of post-processing` | `The advantage of the NMS-free architectures showed up in post-processing latency rather than in accuracy. On the RTX 4090 the NMS-free models needed 0.164–0.170 ms of post-processing` |
| 30 | L136 | `YOLO26n is the fastest model at 10.28 ms … ONNX export yields a 1.73–2.38× speed-up with no measurable change in accuracy, and every model exceeds 30 FPS.` | `YOLO26n was the fastest model at 10.28 ms … ONNX export yielded a 1.73–2.38× speed-up with no measurable change in accuracy, and every model exceeded 30 FPS.` |
| 31 | L147 | `YOLO26s is chosen when a GPU is available, because it gives the best accuracy, while YOLO26n is used where compute is limited.` | `YOLO26s was chosen when a GPU was available, because it gave the best accuracy, while YOLO26n was used where compute was limited.` |
| 32 | L151 | `All four trackers run on the same YOLO26s output … DiffMOT gives the best results, with HOTA 44.37 … OC-SORT, by contrast, has MOTA 55.98 but produces 14,293 IDSW … The results in Table 5 show that` | `All four trackers ran on the same YOLO26s output … DiffMOT gave the best results, with HOTA 44.37 … OC-SORT, by contrast, had MOTA 55.98 but produced 14,293 IDSW … The results in Table 5 showed that` |
| 33 | L166 | `both OC-SORT and DiffMOT track 38 people, while ground truth records 59` | `both OC-SORT and DiffMOT tracked 38 people, while ground truth recorded 59` |
| 34 | L170 | `Taken together, association is what matters under occlusion and non-linear motion. DiffMOT performs best but needs a GPU, behaves as a black box, and carries heavier dependency requirements. Weighing accuracy against efficiency, Deep-OC-SORT is selected as the main tracker` | `Association was what mattered under occlusion and non-linear motion. DiffMOT performed best but required a GPU, behaved as a black box, and carried heavier dependency requirements. Weighing accuracy against efficiency, Deep-OC-SORT was selected as the main tracker` |
| 35 | L174 | `Two approaches are compared across the 29 combined sequences` | `Two approaches were compared across the 29 combined sequences` |
| 36 | L178 | `The results in Fig. 3 show that the state machine adds no error on ideal trajectories … DiffMOT gives the lowest error at 13.08% … The pattern follows association quality. LightTrack also shows the largest over-count … Deep-OC-SORT tends to count lower but holds 40.6 FPS throughput, which is why it is chosen as the main tracker. The 13.08–16.71% error … also includes detection limits` | `The results in Fig. 3 showed that the state machine added no error on ideal trajectories … DiffMOT gave the lowest error at 13.08% … The pattern followed association quality. LightTrack also showed the largest over-count … Deep-OC-SORT tended to count lower but held 40.6 FPS throughput, which is why it was chosen as the main tracker. The 13.08–16.71% error … also included detection limits` |
| 37 | L184 | `Table 6 shows naive line crossing producing 88.7–155.1% error … The state machine with cooldown suppresses that over-counting by holding the status of each ID.` | `Table 6 showed naive line crossing producing 88.7–155.1% error … The state machine with cooldown suppressed that over-counting by holding the status of each ID.` |
| 38 | L196 | `This section tests the sensitivity … The test uses the YOLO26s + Deep-OC-SORT + state machine configuration on the 29 benchmark sequences` | `This section tested the sensitivity … The test used the YOLO26s + Deep-OC-SORT + state machine configuration on the 29 benchmark sequences` |
| 39 | L198 | `the error reaches 101.99% … Error falls to the lowest MAE of 6.34 at CD = 30 … then rises again when the cooldown is too long and some trajectories go uncounted. Other trackers show the same pattern` | `the error reached 101.99% … Error fell to the lowest MAE of 6.34 at CD = 30 … then rose again when the cooldown was too long and some trajectories went uncounted. Other trackers showed the same pattern` |
| 40 | L200 | `the error is driven by background noise detections, while thresholds above 0.40 increase under-counting because low-confidence objects go undetected. The lowest error, 1.67%, occurs at a threshold of 0.20, while the 0.25–0.30 range gives more stable performance … Threshold changes affect throughput only slightly … the end-to-end evaluation uses a cooldown of 30 frames` | `the error was driven by background noise detections, while thresholds above 0.40 increased under-counting because low-confidence objects went undetected. The lowest error, 1.67%, occurred at a threshold of 0.20, while the 0.25–0.30 range gave more stable performance … Threshold changes affected throughput only slightly … the end-to-end evaluation used a cooldown of 30 frames` |
| 41 | L206 | `This section integrates every pipeline stage … The reference is 30 FPS with a latency budget of 33.3 ms per frame. The test uses the operational configuration from Section 4.4 … where density sits at around 34–38 people per frame. Latency is measured in microseconds` | `This section integrated every pipeline stage … The reference was 30 FPS with a latency budget of 33.3 ms per frame. The test used the operational configuration from Section 4.4 … where density sat at around 34–38 people per frame. Latency was measured in microseconds` |
| 42 | L210 | `Preprocessing and counting logic need only 0.85 ms and 0.11 ms.` | `Preprocessing and counting logic needed only 0.85 ms and 0.11 ms.` |
| 43 | L224 | `The results bring out the difference in throughput and computational load … and show the latency stability` | `The results brought out the difference in throughput and computational load … and showed the latency stability` |
| — | semua | `Fig. 2 shows`, `Fig. 4(a) shows`, `Table 1 shows`, `Table 7 shows` | ***tetap present*** (§1.3 poin 1) |

### 4.6 Discussion & Conclusions (L230–L240)

| # | Baris | Sebelum | Sesudah | Alasan |
| --- | --- | --- | --- | --- |
| 44 | L232 | `the detection-tracking pipeline moves from 24.50 ms to 24.61 ms end-to-end, a 0.4% increase` | `the detection-tracking pipeline moved from 24.50 ms to 24.61 ms end-to-end, a 0.4% increase` | mengulang angka hasil → past |
| 45 | L232 | `End-to-end, the operational configuration reaches 24.61 ms per frame (40.6 FPS) on the RTX 4090` | `End-to-end, the operational configuration reached 24.61 ms per frame (40.6 FPS) on the RTX 4090` | idem |
| — | L230, L234 | `The evaluation shows that each pipeline layer has a different limiting factor…`, `These findings are limited by…`, `People counting performance is therefore set by…` | ***tetap present*** | interpretasi + batasan (§1.2) |
| — | §5 L238 | `This study developed and validated RANCAGE…` dst. | *tetap past* — laporan hasil. Kalimat makna (`ID stability and trajectory validation therefore matter…`) sudah present. |

**Opsional, hanya kalau penguji tetap minta §5 seluruhnya present** (saya tidak menyarankan): `suppressed the error` → `suppresses the error`, `gave the strongest association` → `gives the strongest association`, `added only 0.11 ms` → `adds only 0.11 ms`. Risikonya: terbaca sebagai klaim umum di luar konfigurasi yang diuji.

### 4.7 Ringkasan jumlah

- Titik edit ber-nomor di audit: **45**. Saat implementasi ditemukan **5 sisa present yang belum masuk daftar**, jadi total yang diterapkan ke naskah: **50 titik edit + 1 catatan kebijakan tense di header**.
- Dari jumlah itu, **46 adalah perubahan tense** (Abstract 5, Related Works 5, Method 14, Results 20, Discussion 2) dan **4 murni presisi** (Introduction: #6–#9).
- **3 edit tense yang sekaligus membawa perbaikan presisi**: #14 (`reaches over 700 FPS` → atribusi + perangkat), #18 (`outputs in tlwh` → `output boxes in tlwh`), #23 (`guarantees` → `allows at most`).
- **5 temuan tambahan saat implementasi** (audit awal luput, ditemukan saat menyisir ulang sisa present di §3–§4):

| Lokasi | Sebelum | Sesudah |
| --- | --- | --- |
| §3.3 | `Two models are compared.` | `Two models were compared.` |
| §3.3 | `Model B addresses this through RoI validation` | `Model B addressed this through RoI validation` |
| §3.3 | `which is fixed once in the configuration file and applied consistently across all sequences` | `which was fixed once in the configuration file and applied consistently across all sequences` |
| §4.1.1 | `while YOLO26n is reserved for resource-constrained devices.` | `while YOLO26n was reserved for resource-constrained devices.` |
| §4.2 | `The gap falls mainly in the dense crowd area` | `The gap fell mainly in the dense crowd area` |

- Semua terletak di satu file: `docs/journal/en/jestec-manuscript-en.md` (350 baris sebelum, 353 sesudah).
- Verifikasi kebocoran angka: 642 angka di naskah sebelum dan sesudah, **tidak ada satu angka pun yang berubah/hilang/bertambah** (2 angka tambahan berasal dari baris catatan kebijakan tense di header).
- Yang **tidak** diubah dan sengaja dibiarkan present: 4 kategori pengecualian §1.3, tersebar di §3 dan §4.

---

## 5. Temuan non-bahasa: sisa Indonesia di dalam docx

Ini bagian yang paling cepat terlihat reviewer, dan paling mudah diperbaiki. Diperiksa langsung dari XML `word/document.xml` eksport:

**Header tabel masih Indonesia (4 sel):**

| Lokasi | Isi sekarang | Ganti jadi |
| --- | --- | --- |
| Tabel 2, kolom 3 | `Recall maksimum` | `Maximum recall` |
| Tabel 3, kolom 4 | `Porsi post-processing` | `Post-processing share` |
| Heading §4.3.2 | `Ablasi State Machine terhadap Naïve Line Crossing` | `Ablation of the state machine against naive line crossing` |
| Tabel 7, baris 2 kolom 1 | `Deteksi objek` | `Object detection` |

**Pemisah angka belum dikonversi (tabel masih memakai konvensi Indonesia):**

- **91 sel** memakai koma desimal (`0,8230`, `0,6888`, `2,50`, `5,8`, …) → harus jadi titik.
- **16 sel** memakai titik pemisah ribuan (`14.293`, `27.646`, `11.751`, …) → harus jadi koma.
- Prosa di docx sudah benar (mis. `mAP@0.5:0.95 of 0.4974`), jadi tabel adalah sisa yang tertinggal saat konversi.

Konsekuensi: naskah saat ini **tidak konsisten** — prosa memakai desimal titik, tabel memakai koma. JESTEC memakai English (UK) dengan desimal titik. Ini wajib beres sebelum kirim.

Catatan: dokumen docx yang dibaca reviewer dengan `jestec-manuscript-en.md` di repo **tidak identik** — prosa sama, tabel tidak. Perbaikan tabel harus diterapkan ke docx yang benar-benar dikirim.

---

## 6. Prompt siap pakai (untuk editor/writer agent)

Tempel apa adanya. Sudah termasuk instruksi tense yang diminta reviewer.

```text
You are editing an English manuscript for submission to JESTEC (Journal of Engineering
Science and Technology, Taylor's University). The text was translated from Indonesian and
still reads like a translation. Your job is language only: do not change claims, numbers,
section order, citations, or table values.

TASK 1 — Tense discipline (apply mechanically, section by section)
The manuscript must use tense to signal claim status, not to vary style. Follow this map
exactly:
  - Abstract: present for background, purpose and conclusion; past for methods and results.
  - Introduction: present for established facts, the research problem and the aim
    ("this study develops..."). Past for a specific prior study reported as an event.
  - Related Works: present for settled design facts and established mechanisms; PAST for
    any number a cited study measured or reported (AP, HOTA, IDF1, FPS, latency, accuracy).
    Every borrowed number must carry an attribution marker: "was reported to reach",
    "reported", or the benchmark/device it was measured on.
  - Method: PAST for everything this study did (chose, fine-tuned, unified, evaluated, set,
    processed, measured). Present only for: (a) the section roadmap and Fig./Table/Equation
    cross-references, (b) mathematical definitions and symbol statements, (c) mechanisms of
    a third-party method being described (e.g. "YOLOv10 aligns ..."), (d) properties of a
    dataset. Do not convert those four categories to past.
  - Results: PAST for every finding of this study, including findings stated confidently.
    Present only for "Table N shows" / "Fig. N shows" and for properties of a dataset.
  - Discussion: present for interpretation, implications and limitations; past when a
    specific numeric result is restated for context.
  - Conclusions: present for the meaning of the findings; past for sentences that report
    what was done or found.
Within a paragraph, the tense must match the role of each sentence, not the sentence before
it. Do not flag mixed tense as an error when each verb matches its role.

TASK 2 — Make the English precise, not merely grammatical
  1. Replace every absolute verb applied to a single experimental configuration
     (guarantees, proves, always, ensures) with the exact limit that was tested.
     Example: "guarantees one count per identity" -> "allows at most one count per identity
     within each cooldown window".
  2. Kill literal translation patterns. Specifically, and only where they occur:
     - "show X developing" -> "follows/consists of X"
     - verbatim Indonesian connectors and comma-chain run-ons -> split into clauses
     - "lean on", "hard to hold" and other conversational register -> formal equivalent
     - field terms must stay as the original authors named them (ORU, OCM, OCR,
       observation-centric, appearance embedding, amodal fbox), never paraphrased.
  3. Restore idiomatic verb+noun collocations: conducted a study, drew a comparison,
     yielded a result, raised a concern. Never "made an analysis".
  4. Articles: Indonesian has none. Every generic or already-mentioned noun needs the/a.
  5. Vary sentence length inside a paragraph; do not produce uniform 20-word sentences.
  6. Do not introduce hedge stacking ("may perhaps suggest"). One calibrated hedge.

FORBIDDEN OUTPUT
  - Do not add new citations, numbers, claims, or sentences of your own.
  - Do not use: Moreover, Furthermore, Additionally, delve, leverage, robust, comprehensive,
    seamless, pivotal, underscore, "it is important to note that", "in order to".
  - Do not use paired em-dashes to frame a list.
  - Do not start a concluding paragraph with "Overall," / "In summary," / "Taken together,".
  - Do not change any value in any table, figure caption, or equation.

DELIVERABLE
  Return the revised text section by section, in the original order. After each section,
  list every sentence you changed with a one-line reason tagged either [tense] or
  [precision]. If you judge a sentence should keep its original tense because it falls under
  one of the four Method/Results exceptions, say so explicitly and leave it alone.
```

---

## 7. Checklist verifikasi sebelum kirim

- [ ] 35 kalimat tense diperbaiki; tidak ada present yang tertinggal di §3 dan §4 untuk tindakan/temuan penelitian ini.
- [ ] 4 kategori pengecualian §1.3 masih present dan tidak ikut dikonversi.
- [ ] Setiap angka pinjaman di §2 punya penanda atribusi.
- [ ] `guarantees` sudah hilang dari §3.3.
- [ ] Tabel docx: 4 header Indonesia → Inggris; 91 koma desimal → titik; 16 titik ribuan → koma.
- [ ] Prosa dan tabel memakai konvensi angka yang sama.
- [ ] Sweep frasa terlarang (§6) bersih.
- [ ] Semua angka hasil di prosa masih sama dengan sebelum edit (ubah tense ≠ ubah angka).
- [ ] Naskah dibaca ulang oleh orang lain selama 10 menit, hanya untuk menjawab: "apakah ada kalimat yang tense-nya berpindah tanpa alasan?"

---

## 8. Sumber (tanggal akses 17 September 2026)

**Pedoman & gaya bahasa**
1. AJE — *Verb Tense in Scientific Manuscripts* (2015). https://files-aje-com.s3.amazonaws.com/www/row/_assets/docs/AJE-Choosing-the-Right-Verb-Tense-for-Your-Scientific-Manuscript-2015.pdf
2. EASE — *Guidelines for Authors and Translators* (2017/2018). https://urologyjournal.ru/apps/ur_en/assets/uploads/ease-guidelines-2017-english.pdf
3. CASRAI — *Verb Tense Conventions in Research Papers*, diperbarui 23 Agustus 2026. https://casrai.org/guides/verb-tense-conventions-in-research-papers
4. Brandeis University Writing Program — *Verb Tenses: Science*. https://www.brandeis.edu/writing-program/resources/students/handouts/verb-tenses-science-handout.pdf
5. University of Manchester — *Academic Phrasebank*. https://www.phrasebank.manchester.ac.uk/
6. JESTEC — *Submit a paper* (Taylor's University). https://jestec.taylors.edu.my/submit%20a%20paper.htm

**Bukti korpus peer-reviewed (distribusi tense)**
7. Salager-Meyer, F. (1992). English for Specific Purposes, 11(2). doi:10.1016/s0889-4906(05)80002-x
8. Hardjanto, T. D. (2017). *Rhetorical Patterns, Verb Tense, and Voice in Cross-Disciplinary Research Article Abstract*. doi:10.22146/jh.v28i1.11410
9. (2011). *Analyses of Move Structure and Verb Tense of Research Article Abstracts in Applied Linguistics*. International Journal of English Linguistics, 1(2). doi:10.5539/ijel.v1n2p27
10. (2017). *The distribution of verb tenses and modals in journal articles' abstracts*. doi:10.2989/16073614.2017.1373366

**Referensi register & istilah**
11. Azizi, A. H. A. dkk. *Durian detection and counting system using deep learning*. JESTEC, 18(5), 2470–2477. https://jestec.taylors.edu.my/V18Issue5.htm

Dokumen pendamping yang sudah ada di repo: `docs/journal/en/english-writing-research-notes.md` (catatan gaya penulisan EN, sebelumnya) dan `docs/journal/en/jestec-manuscript-en.md` (naskah).

---

## 9. Status implementasi

**Sudah dikerjakan (17 Sep 2026):** 50 titik edit diterapkan ke `docs/journal/en/jestec-manuscript-en.md` + 1 baris catatan kebijakan tense di header naskah. Verifikasi: 642 angka di naskah identik sebelum dan sesudah edit — tidak ada angka yang berubah, hilang, atau bertambah.

**Menunggu keputusan:**

1. **Docx** (header tabel + 107 sel angka masih konvensi Indonesia, §5). Docx inilah yang dibaca reviewer, sedangkan repo menyimpan .md — dua-duanya harus disinkronkan. Belum saya sentuh: mengedit prosa docx berisiko merusak field sitasi Mendeley, jadi perlu keputusan apakah (a) perbaiki hanya tabelnya di docx, lalu prosa ditempel ulang dari .md ke template JESTEC, atau (b) saya kerjakan keduanya sekaligus di docx.
2. **Reformat 31 entri referensi ke gaya JESTEC** + AI-use declaration di depan References — masih terbuka dari catatan sebelumnya, dan ini termasuk syarat submission JESTEC.
