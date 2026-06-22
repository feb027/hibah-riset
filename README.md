# Hibah Riset PUU 2026 — Real-Time People Counting

Repo kerja riset untuk pendalaman SOTA dan penajaman naskah awal penelitian PUU 2026.

## Fokus minggu ini

1. Membuat bagian **PEKERJAAN TERKAIT** berbasis kajian SOTA yang lebih mendalam dan terbaru.
2. Memformulasikan ulang bagian **PENDAHULUAN** agar gap, urgensi, pertanyaan riset, kontribusi, dan kebaruan lebih tajam.

## Sumber awal

- `docs/Proposal PUU 2026 - Counting(2).pdf` — proposal lolos.
- `docs/F-Paper Penelitian.pdf` — panduan struktur paper dari dosen.
- `docs/_extracted/` — hasil ekstraksi teks PDF untuk audit dan penulisan.

## Workflow singkat

- Semua fase dicatat di `docs/PROGRESS.md`.
- Pre-plan utama ada di `docs/01-pre-plan.md`.
- Ledger sumber SOTA ada di `docs/research/source-ledger.md`.
- Evidence matrix ada di `docs/research/evidence-matrix.md`.
- Bibliography ada di `references/references.bib`.
- Full-text note prioritas ada di `docs/research/fulltext-notes/`.
- Draft final sementara ditulis di `docs/drafts/`.
- Review brutal/validasi ditulis di `docs/reviews/`.

## Validasi

```bash
python3 scripts/validate_research_artifacts.py
```

## Eksperimen (Phase 7 — Tier 1)

Sejak 22 Juni 2026, scope eskalasi ke eksperimen terbatas. Tier 1 = smoke
test inference-only di Colab (bukan training, bukan fine-tuning).

- Plan: `docs/plans/2026-06-22-phase7-tier1-experiment.md`.
- Eksperimen card: `docs/experiments/s1-detector-smoke-test.md` (mirror
  `experiments/s1_detector_smoke/README.md`).
- Notebook Colab: `notebooks/01_smoke_test_detector.ipynb`.
- Source code: `src/detector.py`, `src/pipeline.py`, `src/eval_detection.py`,
  `src/utils/video_io.py`.
- Config: `configs/s1_detector_smoke.yaml`.
- Entry CLI: `scripts/smoke_test_detector.py`.

**Aturan keras**:

- Jangan klaim hasil sebelum run aktual.
- Jangan commit artefak besar (`*.pt`, `*.mp4`, `*.csv` eksperimen) —
  lihat `.gitignore`.
- Detector utama eksperimen = `yolov10s` (S003 NeurIPS 2024). YOLO26
  (S001/S002) berstatus caution di source-ledger.

## Repo layout

```
hibah-riset/
├── AGENTS.md                          # agent operating rules
├── README.md                          # this file
├── requirements.txt                   # pinned deps for Colab / VPS
├── pyproject.toml                     # src/ installable package
├── .gitignore                         # excludes data/, models, runs, *.pt
├── src/                               # importable package
│   ├── detector.py                    # PeopleDetector + DETECTOR_CATALOGUE
│   ├── pipeline.py                    # run_smoke_test + CLI
│   ├── eval_detection.py              # per-frame stats
│   └── utils/video_io.py              # probe, iter, draw, write video
├── configs/                           # experiment configs (YAML)
├── notebooks/                         # Colab-ready Jupyter
├── experiments/                       # per-scenario run folders (gitignored outputs)
├── data/                              # gitignored, dataset land
├── models/                            # gitignored, pretrained weights cache
├── scripts/                           # CLI + download helpers
├── docs/                              # research notes, drafts, plans, reviews
├── prompts/                           # agent prompts (researcher/writer/reviewer)
└── references/                        # bibliography (BibTeX + source-id-map)
```
