# Rangkuman Skenario B: Perjalanan Pemilihan dan Pengembangan Tracker

Disusun 16 Agustus 2026. Dokumen ini merangkum Skenario B dari awal sampai akhir: mengapa tracker diuji, apa hasil tiap pilihan, dan ke mana riset berakhir. Ditulis ringkas, angka adalah hasil pengukuran nyata dengan deteksi YOLO26 yang sama (Skenario A, fine-tune CrowdHuman, mAP@0.5:0.95 = 0,4974) dan metrik TrackEval. Perbandingan antar tracker sah digunakan, angka tidak dibandingkan 1:1 ke leaderboard resmi karena deteksi bukan deteksi resmi.

---

## 1. Masalahnya

Deteksi memberi kotak per frame, tapi tidak tahu apakah orang di frame ini sama dengan orang di frame sebelumnya. Akibatnya, orang yang tertutup sebentar lalu muncul lagi bisa dihitung dua kali. Skenario B menjawab: tracker mana yang menjaga identitas cukup lama untuk counting yang akurat?

Dua benchmark dipakai:

| Benchmark | Isi | Karakter |
|---|---|---|
| MOT20-train | 4 sekuens, 8.931 frame | kerumunan sangat padat (rata-rata 179 deteksi per frame, puncak 272) |
| DanceTrack-val | 25 sekuens, 25.508 frame | gerak non-linear (menari), penampilan seragam, sulit dibedakan dari penampilan |

Metrik yang paling relevan untuk counting: IDF1 (seberapa konsisten identitas dipertahankan) dan IDSW (berapa kali identitas pindah/salah). Identitas putus saat oklusi berarti orang dihitung ganda saat muncul lagi.

## 2. Pilihan Pertama: OC-SORT (Baseline)

OC-SORT dipilih sebagai baseline karena murah: biaya asosiasi hampir nol, bisa jalan 54+ FPS di CPU, dan tidak butuh pelatihan. Ini penting karena pada awalnya komputasi terbatas (PC rumah tanpa GPU yang bisa dipakai untuk hal ini).

Hasil OC-SORT:

| Benchmark | HOTA | MOTA | IDF1 | IDSW | Frag |
|---|---|---|---|---|---|
| MOT20 | 36,51 | 55,98 | 42,88 | 14.293 | 27.646 |
| DanceTrack | 28,39 | 71,38 | 26,63 | 6.701 | 6.936 |

Bacaannya: deteksi kuat (MOTA tinggi), tapi asosiasi putus-putus. ID switch 14.293 di MOT20 dan IDF1 hanya 26,63 di DanceTrack. Untuk counting, ini masalah: identitas mudah pindah saat sesama orang saling menutupi. OC-SORT sebagus apa pun murni mengandalkan posisi benda, bukan siapa orangnya.

## 3. Pembanding: DiffMOT (Kualitas Tinggi, Terbukti)

DiffMOT adalah tracker berbasis deep learning yang menggabungkan deteksi, ReID, dan memori, diterbitkan di CVPR 2024 (Lv dkk., S021). Hasilnya jauh lebih baik:

| Benchmark | HOTA | MOTA | IDF1 | IDSW | Frag |
|---|---|---|---|---|---|
| MOT20 | 44,37 | 60,91 | 53,86 | 6.905 | 15.005 |
| DanceTrack | 39,05 | 70,72 | 43,39 | 2.784 | 6.765 |

Selisihnya terhadap OC-SORT:

| Metrik | Selisih |
|---|---|
| MOT20 HOTA | +7,86 |
| MOT20 IDF1 | +10,98 |
| MOT20 IDSW | turun 52 persen |
| DanceTrack HOTA | +10,66 |
| DanceTrack IDF1 | +16,76 |
| DanceTrack IDSW | turun 58 persen |

Kesimpulan yang sah: ReID plus memori memang diperlukan untuk menjaga identitas di adegan padat. DiffMOT membuktikan arahnya benar.

## 4. Kenapa DiffMOT Tidak Dipakai

Hasilnya bagus, tapi ada tiga masalah praktis:

| Dimensi | OC-SORT | DiffMOT |
|---|---|---|
| Biaya asosiasi | hampir nol, 54+ FPS di CPU | berat, butuh GPU, 20 sampai 25 FPS di RTX 4090 |
| Bisa dilatih ulang | tidak perlu | tidak, black box |
| Dependensi | pip minimal | patch lokal + env khusus |

Target pipeline kita minimal 30 FPS (anggaran 33 sampai 40 ms per frame). DiffMOT sudah melewati anggaran pada tahap tracking saja, sebelum detektor dihitung. Publikasi DiffMOT sendiri menyebut 22,7 FPS di RTX 3090. Selain itu, DiffMOT tidak bisa dilatih ulang untuk domain kampus kita. Jadi arah riset harus memakai ReID plus memori, tapi arsitekturnya ringan dan bisa dilatih. DiffMOT tetap dipakai sebagai pembanding kualitas.

## 5. Pivot: LightTrack-ReID (Khan dkk., 2026, S014)

Paper acuan: Khan dkk. (2026, S014), PLOS ONE 21(3), e0342246, peer-reviewed. Paper ini menawarkan arsitektur yang cocok dengan kebutuhan: ringan (biaya asosiasi sekitar 0,6 GFLOPs per frame), sekitar 30 FPS di GTX 1080, dan bisa dilatih ulang. Karena tidak ada kode resmi, reimplementasi menjadi kontribusi mandiri.

Komponen sistem (dijelaskan singkat):

| Singkatan | Kepanjangan | Arti singkat |
|---|---|---|
| LAE | Lightweight Appearance Encoder | Sidik jari penampilan, vektor 32 angka per orang |
| TBSS | Transformer-Based Similarity Scoring | Penilai kemiripan posisi plus penampilan, skor 0 sampai 1 |
| CMOH | Context Memory for Occlusion Handling | Memori 10 embedding terakhir untuk yang tertutup sebentar |
| ASW | Adaptive Similarity Weighting | Pembagi porsi posisi vs penampilan sesuai keramaian frame |
| APS | Adaptive Pair Sampling | Cara memilih pasangan latih, maksimal 50 per frame |

Pola ablasi paper (konteks, bukan target reproduksi):

| Konfigurasi | HOTA MOT17 | HOTA MOT20 | IDSW MOT17 |
|---|---|---|---|
| Baseline (Kalman + IoU + EMA) | 66,13 | 56,17 | 227 |
| + LAE | 70,88 | 60,38 | 168 |
| + LAE + TBSS | 73,38 | 63,94 | 138 |
| + LAE + TBSS + CMOH | 74,88 | 65,74 | 80 |
| + LAE + TBSS + CMOH + ASW | 75,63 | 66,70 | 79 |

Pelajaran penting dari pola ini: kenaikan terbesar datang dari LAE (penampilan), lalu CMOH paling memangkas pergantian identitas. ASW hanya tambahan tipis.

## 6. Reimplementasi dan Perjalanan Training

Protokol evaluasi dipilih anti-overclaim: leave-one-out MOT20 4 fold plus DanceTrack zero-shot, deteksi YOLO26 identik, hasil dibandingkan relatif ke OC-SORT (36,51) dan DiffMOT (44,37), bukan ke angka paper.

Progres pembangunan:

| Fase | Komponen | Status | Hasil |
|---|---|---|---|
| Phase 1 | Skeleton asosiasi (Kalman + IoU + Hungarian + EMA) | selesai | 3.211 frame smoke-test, 614 FPS di CPU |
| Phase 2 | LAE encoder (MobileNetV3-Small, 32-d) | selesai, diverifikasi GPU | cosine orang sama 0,772 vs orang beda 0,746 sebelum dilatih (margin kecil, alasan training) |
| Phase 3 v1 | Training fold-1 (LAE + TBSS) | selesai | LAE bagus; TBSS tak terukur (bug validasi) |
| Phase 3 v2 | Perbaikan TBSS (MLP 6-d, optimizer pisah, BCE berbobot) | selesai (14 Agustus) | BCEacc validasi 0,92 sampai 0,98, best.pt 0,978 di epoch 15 |
| Evaluasi TrackEval | HOTA/IDF1 tracker usulan | selesai | awalnya 32,92, setelah tuning 37,67 (detail di bagian 7) |

Kendala terbesar selama fase ini: TBSS tampak tidak belajar (BCEacc macet di sekitar 0,5, seperti lempar koin) selama training v1. Setelah ditelusuri 14 Agustus 2026, ternyata bukan model yang gagal, melainkan bug konstruksi fitur di validasi: pasangan negatif di validasi salah diberi input (kotak yang dibandingkan sama dengan kotaknya sendiri sehingga IoU selalu 1,0), membuat pasangan negatif tampak seperti pasangan positif sempurna. TBSS sebenarnya tidak pernah terukur dengan benar. Bug diperbaiki (sisi kotak anchor dipakai konsisten di training, validasi, dan histogram), training dilanjutkan, dan v2 menghasilkan TBSS yang valid pertama kali: BCEacc 0,92 sampai 0,98.

Selain itu, perbaikan v2: TBSS diganti dari transformer 73 dimensi (attention-nya tidak efektif) menjadi MLP ringan input 6 angka (IoU, cosine, selisih box), optimizer TBSS dipisah, BCE diberi bobot, checkpoint ala YOLO (best/last.pt).

## 7. Hasil Akhir Tracker Usulan

Dua tahap evaluasi, protokol sama:

| Tracker | MOT20 HOTA | MOT20 IDF1 | DanceTrack HOTA | DanceTrack IDF1 |
|---|---|---|---|---|
| OC-SORT (baseline) | 36,51 | 42,88 | 28,39 | 26,63 |
| DiffMOT | 44,37 | 53,86 | 39,05 | 43,39 |
| Tracker usulan, evaluasi pertama (14 Agustus, sebelum tuning) | 32,92 | 34,69 | 22,53 | 18,91 |
| Tracker usulan, setelah tuning (OCM, ma90, ea5, sm0.3, aw0.5) | 37,67 | 43,54 | 28,43 | 28,71 |
| Ablasi LAE-only | 12,01 | 10,17 | 19,61 | 18,69 |

Bacaannya: evaluasi pertama masih kalah dari OC-SORT. Setelah tambahan OCM (memori untuk yang tertutup) dan tuning ambang, tracker usulan menembus baseline: 37,67 vs 36,51 HOTA MOT20, naik +1,16, dan IDF1 naik ke 43,54 vs 42,88. DiffMOT tetap unggul jauh (44,37), posisi yang dicatat jujur: menang tipis atas OC-SORT, kalah dari DiffMOT. Ablasi LAE-only (penampilan tanpa geometri) rusak parah (12,01), konsisten dengan pelajaran paper: penampilan menambah di atas baseline posisi, bukan menggantikannya.

Sweep tambahan untuk memastikan konfigurasi terbaik (16 Agustus 2026):

| Konfigurasi | MOT20 HOTA | MOT20 MOTA | MOT20 IDF1 | DanceTrack HOTA |
|---|---|---|---|---|
| sm0.3 aw0.5 (final) | 37,67 | 54,94 | 43,54 | 28,43 |
| sm0.2 aw0.5 | 37,15 | 54,99 | 43,02 | 29,31 |
| sm0.3 aw0.7 | 37,19 | 54,93 | 42,99 | 27,64 |
| + ASW (Eq 10 paper) | 37,59 | 54,96 | 43,51 | 27,65 |

Keputusan final: sm0.3, appearance-w 0.5, ma90, ea5. ASW tidak terbukti di protokol kita (37,59 lebih rendah dari 37,67; selisih di bawah noise), dicatat sebagai ablasi negatif. Gate sm0.2 menarik untuk DanceTrack (29,31) tapi mengorbankan 0,52 HOTA MOT20, tidak diambil karena prioritas adalah MOT20 (domain people counting padat).

## 8. Optimasi Kecepatan Realtime

Bottleneck realtime ternyata bukan detektor (YOLO26 di RTX 4090 hanya 3 sampai 5 ms per frame), melainkan loop crop dan resize embedding per deteksi yang jalan serial di CPU: sekitar 25 ms per frame di adegan padat. Ini menjelaskan kenapa FPS 4090 nyaris sama dengan GTX 1080 di paper S014. Fix: crop dan resize dipindah ke GPU dengan area averaging (setara interpolasi yang dipakai training, jadi konsisten). Hasilnya diverifikasi dua sisi:

Akurasi tidak berubah (konfigurasi final dijalankan ulang):

| Konfigurasi | MOT20 HOTA | MOT20 MOTA | MOT20 IDF1 | DanceTrack HOTA |
|---|---|---|---|---|
| Baseline (crop CPU) | 37,67 | 54,94 | 43,54 | 28,43 |
| Batch crop GPU | 37,72 | 54,98 | 43,51 | 28,12 |

Selisih dalam noise, malah IDSW MOT20 turun (11.637 menjadi 11.497). Kecepatan realtime demo naik:

| Versi | FPS rata-rata |
|---|---|
| Sebelum (crop CPU) | 31,9 FPS |
| Setelah (batch crop GPU) | 49,3 FPS |

Keduanya sudah di atas target minimal 30 FPS, dan versi after lolos budget dengan lebar (20 ms per frame).

## 9. Ringkasan dan Posisi Jujur

| Tracker | MOT20 HOTA | Kecepatan | Bisa dilatih ulang | Catatan |
|---|---|---|---|---|
| OC-SORT | 36,51 | 54+ FPS CPU | tidak perlu | baseline murah, asosiasi putus di adegan padat |
| DiffMOT | 44,37 | 20 sampai 25 FPS GPU | tidak | kualitas terbaik, tak masuk anggaran realtime |
| Tracker usulan (LAE+TBSS v2) | 37,67 | 49,3 FPS di 4090 | ya | menang tipis atas OC-SORT, kalah dari DiffMOT |

Status: tracker usulan selesai dan stabil. Yang tersedia untuk lanjutan: konfirmasi lintas benchmark lain (MOT17 test) atau uji cepat pada video real people-counting bila GPU kampus luang. Langkah berikutnya yang logis bukan tuning tracker lagi (diminishing returns), melainkan Skenario C: validasi logika counting (line-crossing) dan MAE pada video nyata.

## Sumber

1. Lv, W., dkk. (2024, S021). DiffMOT. CVPR 2024, 19321-19330. arXiv:2403.02075.
2. Khan, S. B. J., dkk. (2026, S014). LightTrack-ReID. PLOS ONE 21(3), e0342246. DOI 10.1371/journal.pone.0342246.
3. Cao, J., dkk. (2023). OC-SORT. CVPR 2023. arXiv:2203.14360.
4. Luiten, J., dkk. (2021, S025). HOTA. IJCV 129(2), 548-578.
5. Dendorfer, P., dkk. (2020, S036). MOT20. ECCV 2020 Workshops. arXiv:2003.09003.
6. Sun, P., dkk. (2022, S037). DanceTrack. CVPR 2022. arXiv:2111.14690.
