import json, urllib.request

DRAFT = open('docs/journal/4.1-object-detection-results.md').read()
SOURCE = open('docs/reports/laporan-skenario-a-finetuning-yolo.md').read()

prompt = """Kamu adalah reviewer akademik ketat dan netral untuk artikel jurnal JESTEC (Journal of Engineering Science and Technology) yang ditulis dalam Bahasa Indonesia. Topik artikel: real-time people counting berbasis deep learning (YOLO26 + multi-object tracking + counting logic).

Kamu tidak terlibat dalam penulisan draft; tugasmu HANYA menilai.

DI BAWAH INI:
(1) DRAFT yang direview = subbab 4.1 "Object Detection Results" untuk Bab 4 (Results and Discussion).
(2) SUMBER RESMI = laporan eksperimen internal tempat seluruh angka draft berasal.

TUGAS REVIEW - periksa satu per satu:
1. FACTUALITY: setiap angka, persentase, dan klaim di DRAFT harus ada dan konsisten di SUMBER. Periksa seluruh sel tabel. Laporkan setiap ketidakcocokan dengan mengutip potongan bermasalah.
2. CITATION INTEGRITY: sitasi format (Author, Year - S###). Kode yang dipakai: S038 (CrowdHuman, Shao et al. 2018), S048 (Dollar et al. 2012, metrik MR-2), S043 (Hoiem et al. 2012, stratifikasi galat truncated), S039 (Cai et al. 2019, ProxylessNAS), S041 (Lu et al. 2022, latency monotonicity), S042 (Lazarevich et al. 2023, YOLOBench), S002 (dokumentasi vendor Ultralytics YOLO26). Nilai apakah atribusi author-tahun-konteks sudah tepat.
3. OVERCLAIM: draft tidak boleh menarik kesimpulan lebih kuat dari sumbernya. Contoh yang harus dijaga: kesetaraan akurasi tier nano HANYA boleh disimpulkan sebagai "tidak dapat dibedakan dari variasi acak" (satu run, satu seed); klaim NMS-free hanya boleh menyentuh latensi post-processing, bukan akurasi.
4. GAYA BAHASA: Bahasa Indonesia akademik-natural. Tandai pola tulisan AI: frasa template ("penting untuk dicatat", "seiring berkembangnya"), tricolon berlebihan, kalimat pengisi, transisi kaku berulang, paragraf yang selalu diakhiri rangkuman.
5. KELAYAKAN JURNAL: alur logis, tabel informatif dan rapi, transisi antar paragraf wajar, konsistensi istilah.

FORMAT OUTPUT (Bahasa Indonesia):
Baris pertama: verdict salah satu dari: LAYAK / LAYAK DENGAN REVISI MINOR / TIDAK LAYAK
Lalu temuan per kategori (1-5) dengan kutipan potongan bermasalah + lokasinya. Bila tidak ada temuan pada suatu kategori, tulis eksplisit "tidak ditemukan masalah".
Terakhir: daftar "PERBAIKAN WAJIB" (bila ada) dan "SARAN" (bila ada).

=== DRAFT (subbab 4.1) ===
%s

=== SUMBER RESMI (laporan eksperimen Skenario A) ===
%s

Tulis review lengkap sekarang. Hanya output review, tanpa percakapan.""" % (DRAFT, SOURCE)

key = None
for line in open('/home/aqua/.hermes/.env'):
    if line.startswith('OPENROUTER_API_KEY='):
        key = line.split('=', 1)[1].strip()
if not key:
    sys_exit = SystemExit('OPENROUTER_API_KEY tidak ketemu')

models = ['deepseek/deepseek-v4-flash', 'moonshotai/kimi-k3']
out_text, used = None, None
for model in models:
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=json.dumps({'model': model, 'messages': [{'role': 'user', 'content': prompt}],
                         'max_tokens': 8192, 'temperature': 0.2}).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=480) as r:
            out = json.load(r)
        out_text = out['choices'][0]['message']['content']
        used = model
        break
    except Exception as e:
        print(model, 'gagal:', e)

if out_text:
    open('docs/reviews/review-jestec-4.1.md', 'w').write(
        f'# Review JESTEC 4.1 (reviewer netral: {used} via OpenRouter, tanpa konteks penulis)\n\n' + out_text)
    print(out_text[:3000])
    print(f'...[total {len(out_text)} chars — reviewer: {used} — tersimpan di docs/reviews/review-jestec-4.1.md]')
