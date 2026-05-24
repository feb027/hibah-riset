# Agent Instructions — Hibah Riset PUU 2026

## Project scope

Topik: pengembangan model rekognisi objek untuk real-time people counting system berbasis deep learning, dengan arah proposal YOLO26 + DiffMOT/OC-SORT + advanced counting logic.

Target tugas minggu ini:
1. Kajian SOTA mendalam dan terbaru untuk bagian **PEKERJAAN TERKAIT**.
2. Re-formulasi **PENDAHULUAN** dari proposal agar lebih tajam dan sinkron dengan SOTA.

## Hard rules

- Utamakan sumber terbaru sampai tanggal kerja: **25 Mei 2026 WIB**.
- Jangan mengarang sitasi. Setiap klaim SOTA harus punya URL/DOI/arXiv/venue dan tanggal akses.
- Pisahkan bukti peer-reviewed, arXiv/preprint, dokumentasi vendor, blog, dan GitHub.
- GitHub hanya lewat `gh` CLI; jangan scrape github.com.
- Jangan menulis full draft final sebelum source ledger, evidence matrix, bibliography, dan full-text notes prioritas siap.
- Jangan hapus PDF sumber.

## Evidence gates

Before Phase 3 final drafting:
- `docs/research/source-ledger.md` must contain enough indexed/credible sources.
- `docs/research/evidence-matrix.md` must map claims to sources and limitations.
- `references/references.bib` must contain bibliography entries for cited sources.
- Priority sources must have notes under `docs/research/fulltext-notes/` before detailed method/performance claims are used.
- `scripts/validate_research_artifacts.py` must pass.

## Writer strict mode

Writer agent:
- Hanya menulis/memperbarui file target.
- Setelah menulis, baca ulang file target jika memungkinkan.
- Tidak perlu output ringkasan panjang di chat.

## Reviewer strict mode

Reviewer agent:
- Hanya menulis review ke file di `docs/reviews/`.
- Tidak mengubah draft kecuali diminta eksplisit.
- Review wajib cek: factuality, freshness, gap logic, citation integrity, Indonesian academic tone, anti-AI wording, and alignment to lecturer guide.

## Citation policy

For every source candidate capture:
- title
- authors/organization
- year/date
- venue/source type
- URL/DOI/arXiv ID
- access date
- why relevant
- limitation/risk
- mapped section: detector / tracker / people counting / dataset / metric / deployment / gap

## Draft style

- Bahasa Indonesia akademik-natural, tidak template/slop.
- Pekerjaan terkait: kritis, dikelompokkan per tema, menyebut kelebihan/keterbatasan berbasis fakta.
- Pendahuluan: mulai dari urgensi ruang publik, masalah teknis, gap SOTA, rumusan masalah, pendekatan, kontribusi, roadmap singkat bila tetap diminta.
