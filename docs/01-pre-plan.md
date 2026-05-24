# Pre-Plan — SOTA, Pekerjaan Terkait, dan Pendahuluan PUU 2026

> For Hermes/Codex/subagents: jalankan fase berurutan. Jangan masuk fase penulisan final sebelum gate sumber dan evidence matrix lolos.

**Goal:** menghasilkan draft akademik **PEKERJAAN TERKAIT** dan **PENDAHULUAN** yang lebih tajam dari proposal lolos, berbasis SOTA terbaru sampai 25 Mei 2026 WIB.

**Architecture:** pekerjaan dibagi menjadi pipeline riset → evidence matrix → outline → writer → reviewer → patch → final verifier. Repo menyimpan semua bukti, draft, dan review agar bisa dilanjutkan sampai fase prototipe nanti.

**Tech stack / tools:** local PDF extraction (PyMuPDF), web/arXiv/Semantic Scholar/Firecrawl/Exa search, GitHub via `gh`, Markdown artifacts, deterministic validation script.

---

## Scope minggu ini

### In scope

- Audit proposal lolos dan panduan paper dosen.
- Kumpulkan dan validasi SOTA terbaru untuk:
  1. real-time object detection / YOLO26 / NMS-free detection,
  2. dense-scene multi-object tracking,
  3. DiffMOT/diffusion-based tracking,
  4. OC-SORT/ByteTrack/SORT-family baseline,
  5. people counting / crowd counting berbasis CCTV/video,
  6. datasets: CrowdHuman, MOT20, DanceTrack, RHC/people-counting datasets,
  7. metrics: HOTA, MOTA, IDF1, FPS/latency,
  8. edge/real-time deployment constraints.
- Draft `docs/drafts/pekerjaan-terkait.md`.
- Draft `docs/drafts/pendahuluan.md`.
- Review brutal dan final verifier.

### Out of scope sekarang

- Training model, prototipe inference, dashboard, deployment, atau eksperimen GPU.
- Klaim hasil eksperimen internal yang belum dilakukan.
- Submit jurnal/format final ACM lengkap.

---

## Acceptance criteria

- [ ] Source ledger berisi minimal 20 sumber kandidat, dengan minimal 15 sumber kuat yang layak disitasi.
- [ ] Minimal 70% sumber utama berasal dari 2024–2026; sumber klasik boleh untuk dataset/metric/metode dasar.
- [ ] Setiap klaim utama dalam draft punya sumber yang jelas.
- [ ] Related work dikelompokkan tematik, bukan daftar paper satu-per-satu.
- [ ] Gap riset eksplisit dan nyambung ke proposal YOLO26 + DiffMOT/OC-SORT + counting logic.
- [ ] Pendahuluan mengikuti panduan dosen: konteks → masalah → pendekatan eksisting → gap → rumusan masalah/tujuan/lingkup → kontribusi/outline.
- [ ] Tidak ada sitasi rusak seperti `{Formatting Citation}` atau duplikasi daftar pustaka mentah.
- [ ] Reviewer menulis file review dan final verifier menyatakan READY atau menyebut blocker spesifik.

---

## Phase 0 — Repo and document orientation

**Objective:** membuat dasar repo dan memahami sumber awal.

**Files:**
- Read: `docs/Proposal PUU 2026 - Counting(2).pdf`
- Read: `docs/F-Paper Penelitian.pdf`
- Create: `docs/_extracted/*.md`
- Create: `docs/00-project-brief.md`
- Create: `docs/01-pre-plan.md`
- Create: `AGENTS.md`

**Verification:**
- `docs/_extracted/manifest.json` ada dan mencatat jumlah halaman/karakter.
- `git status --short` bersih setelah commit fase.

---

## Phase 1 — SOTA discovery and source ledger

**Objective:** mengumpulkan sumber primer dan kandidat terbaru.

**Search protocol:**
- Query exact untuk YOLO26/arXiv 2601.12882 dan dokumentasi vendor Ultralytics.
- Query MOT 2025/2026: dense scenes, occlusion, transformer MOT, end-to-end MOT, diffusion-based tracker.
- Query people counting/crowd counting 2025/2026: CCTV, real-time, edge, region-of-interest, trajectory/counting logic.
- Query dataset/metrics: MOT20, DanceTrack, CrowdHuman, HOTA, MOTA, IDF1.
- Untuk GitHub repo resmi, gunakan `gh` CLI saja.

**Files:**
- Modify: `docs/research/source-ledger.md`
- Create: `docs/research/evidence-matrix.md`
- Optional: `references/references.bib`

**Gate:** lanjut hanya jika minimal 15 sumber layak sudah terisi dan dipetakan ke gap/section.

---

## Phase 2 — Related work outline

**Objective:** membuat kerangka PEKERJAAN TERKAIT berbasis taxonomy.

**Suggested taxonomy:**
1. Deteksi manusia real-time dan pergeseran menuju NMS-free detectors.
2. Multi-object tracking pada kerumunan padat dan masalah identity switch.
3. Diffusion/transformer/modern MOT untuk motion non-linear dan occlusion recovery.
4. People counting berbasis RoI/trajectory dan risiko double-counting.
5. Dataset, metrik, dan constraint deployment real-time.
6. Gap synthesis: mengapa integrasi YOLO26 + DiffMOT + OC-SORT fallback + advanced counting logic masih relevan.

**Files:**
- Create: `docs/outlines/pekerjaan-terkait-outline.md`

**Gate:** reviewer harus menyetujui bahwa outline tidak sekadar listing paper.

---

## Phase 3 — Draft PEKERJAAN TERKAIT

**Objective:** menulis draft related work yang kritis dan berbasis fakta.

**Files:**
- Create/modify: `docs/drafts/pekerjaan-terkait.md`
- Create: `docs/reviews/review-pekerjaan-terkait.md`

**Writer constraints:**
- Bahasa Indonesia akademik-natural.
- Setiap paragraf harus menjawab: kelompok metode apa, capaian apa, keterbatasan apa, implikasinya ke riset ini apa.
- Jangan memakai frasa pujian kosong seperti “sangat baik” tanpa bukti.

**Gate:** review brutal PASS atau semua blocker diperbaiki.

---

## Phase 4 — Draft PENDAHULUAN

**Objective:** menulis ulang pendahuluan setelah related work matang.

**Files:**
- Create/modify: `docs/drafts/pendahuluan.md`
- Create: `docs/reviews/review-pendahuluan.md`

**Structure:**
1. Urgensi manajemen ruang publik dan people counting real-time.
2. Masalah teknis: kepadatan, oklusi, small objects, pencahayaan, non-linear motion, ID switch, double counting.
3. Ringkasan SOTA dan kekurangannya.
4. Gap dan rumusan masalah.
5. Tujuan, lingkup, dan kontribusi usulan.
6. Outline singkat isi makalah/proposal lanjutan.

**Gate:** pendahuluan harus sinkron dengan related work dan tidak mengklaim hasil eksperimen yang belum ada.

---

## Phase 5 — Final verifier and packaging

**Objective:** memastikan draft siap dibawa diskusi offline dengan dosen.

**Files:**
- Create: `docs/reviews/final-verifier.md`
- Modify: `docs/PROGRESS.md`

**Checks:**
- Citation integrity.
- Freshness distribution.
- No unsupported claims.
- No broken markdown links/file references.
- Clear “hal yang perlu dikonfirmasi ke dosen”.

---

## Initial source leads captured during setup

These are leads, not final citations yet:

- YOLO26 arXiv: `https://arxiv.org/abs/2601.12882` — primary source candidate for YOLO26/NMS-free claims.
- Ultralytics YOLO26 docs: `https://docs.ultralytics.com/models/yolo26` — implementation/vendor docs; use carefully, not as peer-reviewed evidence.
- DiffMOT CVPR 2024 — already in proposal; verify official CVF/arXiv.
- OC-SORT CVPR 2023 — baseline/fallback; verify official paper and GitHub via `gh` if needed.
- OcclusionTrack 2025 MDPI: `https://www.mdpi.com/2076-3417/15/24/13030` — dense-scene occlusion lead.
- Nature Scientific Reports 2025 two-stage MOT with transformer: `https://www.nature.com/articles/s41598-025-16389-4` — occlusion/ID switch lead.
- ICML 2025 MOTE: `https://icml.cc/virtual/2025/poster/46062` — occluded MOT lead.
- IET 2025 MOT review: `https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/cvi2.70010` — taxonomy/review lead.

---

## Agent handoff template

```text
You are a research writer/reviewer for /home/aqua/hibah-riset.

Goal:
[one exact file/output]

Inputs:
- docs/00-project-brief.md
- docs/01-pre-plan.md
- docs/_extracted/proposal_puu_2026_counting.md
- docs/_extracted/f_paper_penelitian.md
- docs/research/source-ledger.md
- docs/research/evidence-matrix.md

Constraints:
- Latest cutoff: 25 Mei 2026 WIB.
- No hallucinated citations.
- Writer writes only target file then exits.
- Reviewer writes only review file then exits.

Acceptance:
- [exact checks]
```
