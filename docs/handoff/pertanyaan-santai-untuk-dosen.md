# Pertanyaan Santai untuk Diskusi Dosen

> Tujuan file ini: pegangan ngomong saat diskusi offline supaya pertanyaannya natural, tidak terlalu akademis, tapi tetap mengarah ke keputusan penting.

## Pembuka santai

- “Bu/Pak, kemarin kami coba rapihin bagian SOTA, pekerjaan terkait, sama pendahuluannya. Boleh kami minta arahan, kira-kira arah gap yang kami tarik ini sudah pas belum?”
- “Kami coba posisikan risetnya bukan sekadar pakai YOLO26, tapi integrasi detector, tracker, sama counting logic. Menurut Bu/Pak, framing seperti ini sudah aman belum?”
- “Kalau dari draft ini, bagian mana yang menurut Bu/Pak paling perlu dipertajam sebelum lanjut ke metode/prototipe?”

## Pertanyaan soal fokus riset

1. “Menurut Bu/Pak, fokus utama riset ini sebaiknya lebih ditekankan ke **model deteksinya**, **tracking-nya**, atau **counting logic-nya**?”
2. “Kalau harus dibuat lebih sederhana, bagian mana yang sebaiknya jadi inti kontribusi utama?”
3. “Apakah gap ‘integrasi detector real-time + tracker robust + counting logic berbasis zona’ sudah cukup kuat untuk dibawa sebagai posisi penelitian?”
4. “Apakah perlu tetap membawa istilah *smart surveillance/crowd management*, atau cukup fokus ke *real-time people counting* saja?”
5. “Untuk ruang publik target, sebaiknya kami bayangkan skenario seperti CCTV kampus, stasiun, pintu masuk gedung, atau tempat lain?”

## Pertanyaan soal YOLO26

6. “Karena YOLO26 masih banyak berbasis dokumentasi vendor dan preprint, apakah aman kalau kami posisikan hanya sebagai kandidat implementasi, bukan dasar novelty utama?”
7. “Apakah Bu/Pak ingin YOLO26 tetap jadi detector utama, atau sebaiknya kami siapkan pembanding seperti YOLOv10/RT-DETR juga?”
8. “Kalau nanti reviewer/dosen lain mempertanyakan YOLO26 karena masih baru, apakah strategi kami yang menjadikan YOLOv10 dan RT-DETR sebagai dasar akademik sudah cukup aman?”
9. “Apakah istilah NMS-free perlu dijelaskan lebih sederhana di proposal, atau cukup disebut sebagai bagian dari efisiensi detector?”

## Pertanyaan soal DiffMOT dan OC-SORT

10. “Untuk tracking, apakah DiffMOT sebaiknya diposisikan sebagai metode utama karena gerak non-linear, lalu OC-SORT sebagai fallback ringan?”
11. “Kalau DiffMOT ternyata berat saat prototipe, apakah sejak awal perlu kami tulis bahwa OC-SORT/SORT-family menjadi baseline atau backup?”
12. “Apakah perlu membandingkan DiffMOT dengan tracker lain juga, atau cukup dengan OC-SORT dulu supaya scope tidak melebar?”
13. “Menurut Bu/Pak, fokus evaluasi tracker nanti lebih penting ke IDF1/HOTA, atau langsung ke error hitung orang?”

## Pertanyaan soal counting logic

14. “Untuk counting logic, apakah konsep RoI polygon, zone-to-zone trajectory, dan ID state memory sudah masuk akal untuk dijadikan kontribusi sistem?”
15. “Kalau orang hanya mondar-mandir di area kamera, apakah sistem harus menghitung hanya saat benar-benar pindah zona?”
16. “Apakah perlu dari awal kami definisikan skenario masuk-keluar, misalnya zona A ke zona B baru dihitung?”
17. “Untuk menghindari double-counting, apakah ID memory cukup dijelaskan secara konsep dulu, atau perlu langsung dibuat diagram alurnya?”

## Pertanyaan soal dataset dan validasi

18. “Untuk dataset awal, apakah cukup pakai MOT20, DanceTrack, dan CrowdHuman, atau perlu cari dataset people counting yang punya label keluar-masuk?”
19. “Kalau dataset publik tidak punya label zona/counting, apakah boleh kami buat validasi kecil dari video sendiri atau CCTV publik?”
20. “Untuk validasi lokal, apakah memungkinkan pakai rekaman area kampus atau harus pakai data publik saja?”
21. “Nanti ground truth counting sebaiknya dibuat manual per video, per zona, atau cukup sampling beberapa skenario dulu?”
22. “Kalau target TKT 3–4, seberapa jauh prototipe harus berjalan? Cukup demo video offline, atau harus real-time dari kamera?”

## Pertanyaan soal evaluasi

23. “Metrik evaluasi yang paling penting menurut Bu/Pak apa: FPS, HOTA/IDF1, counting error, atau semuanya tetap perlu?”
24. “Kalau sistem deteksinya bagus tapi counting error masih tinggi, apakah itu tetap dianggap masalah utama yang perlu dianalisis?”
25. “Apakah perlu sejak awal menulis bahwa evaluasi akan dipisah: detector, tracker, counting, dan real-time performance?”
26. “Untuk klaim real-time, kira-kira target minimal FPS-nya perlu ditentukan sekarang atau nanti setelah eksperimen awal?”

## Pertanyaan soal sumber dan sitasi

27. “Di source ledger kami ada beberapa paper MDPI yang relevan. Apakah Bu/Pak nyaman memakai MDPI sebagai pendukung, asal anchor utamanya tetap CVPR/NeurIPS/IEEE/Springer/Nature?”
28. “Untuk final nanti, apakah sitasi sebaiknya langsung IEEE numerik, atau source ID internal dulu tidak apa-apa selama diskusi?”
29. “Apakah ada jurnal atau konferensi tertentu yang Bu/Pak ingin kami jadikan acuan gaya penulisan dan daftar pustaka?”
30. “Kalau ada sumber yang menurut Bu/Pak kurang kuat, bagian mana yang sebaiknya kami ganti dengan paper yang lebih bereputasi?”

## Pertanyaan soal draft Pendahuluan dan Pekerjaan Terkait

31. “Apakah alur pendahuluan dari urgensi → masalah teknis → SOTA → gap → tujuan sudah enak dibaca?”
32. “Apakah bagian pekerjaan terkait sudah cukup tematik, atau masih terlalu panjang/teknis?”
33. “Bagian mana yang sebaiknya kami ringkas supaya draft lebih nyaman dibaca dosen/reviewer?”
34. “Apakah istilah teknis seperti NMS-free, ID switch, HOTA, dan DiffMOT perlu dijelaskan lebih awam?”
35. “Apakah roadmap 5 tahun di pendahuluan sudah sesuai dengan arah kelompok riset AI Siliwangi?”

## Pertanyaan soal langkah berikutnya

36. “Setelah ini, sebaiknya kami lanjut ke perapian sitasi dulu, atau mulai eksplorasi prototipe kecil?”
37. “Untuk tugas mahasiswa minggu depan, lebih baik dibagi ke citation formatting, dataset/prototype, atau diagram metode?”
38. “Apakah perlu kami buat diagram pipeline baru berdasarkan SOTA yang sudah diperbarui?”
39. “Kalau harus demo awal, bagian mana yang paling realistis: YOLO detector dulu, tracking dulu, atau counting logic sederhana dulu?”
40. “Apa keputusan paling penting yang harus kami bawa pulang dari diskusi minggu depan?”

## Versi paling singkat kalau waktu diskusi terbatas

Kalau waktunya sempit, cukup tanya ini:

1. “Bu/Pak, framing gap integrasi detector + tracker + counting logic ini sudah pas belum?”
2. “YOLO26 aman tidak kalau kami posisikan sebagai kandidat implementasi, bukan novelty utama?”
3. “DiffMOT utama dan OC-SORT fallback, apakah strategi ini masuk akal?”
4. “Dataset dan validasinya sebaiknya pakai publik saja, atau perlu video lokal juga?”
5. “Next step kami sebaiknya rapihin sitasi dulu atau mulai prototipe kecil?”

## Kalimat penutup santai

- “Oke Bu/Pak, berarti setelah ini kami fokus ke bagian yang Ibu/Bapak arahkan dulu, nanti kami update draft dan source-nya.”
- “Kalau begitu kami akan rapikan bagian gap, sitasi, dan rencana validasi sesuai masukan hari ini.”
- “Siap Bu/Pak, nanti kami lanjutkan ke prototipe kecil sambil tetap jaga framing akademiknya.”
