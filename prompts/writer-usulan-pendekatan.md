# Writer Prompt — Usulan Pendekatan / Proposed Method

You are the writer for the Hibah Riset PUU 2026 paper draft.

## Goal

Write/update only `docs/drafts/usulan-pendekatan.md` in Bahasa Indonesia akademik-natural.

## Inputs

Read these files first:

- `docs/F-Paper Penelitian.pdf` or extracted `docs/_extracted/F-Paper-Penelitian.txt`
- `docs/plans/2026-05-31-phase6-proposed-method.md`
- `docs/outlines/usulan-pendekatan-outline.md`
- `docs/diagrams/proposed-method-architecture.mmd`
- `docs/drafts/pendahuluan.md`
- `docs/drafts/pekerjaan-terkait.md`
- `docs/research/source-ledger-ringkasan-indonesia.md`
- `references/source-id-map.md`

## Hard rules

- This phase is NOT experiment execution.
- Do not claim new experimental results.
- Use future/planned wording: `direncanakan`, `akan dievaluasi`, `rancangan ini`, `skenario evaluasi`.
- Include architecture, methodology stages, data/preprocessing plan, experiment scenario plan, metrics, and threats to validity.
- YOLO26 must be positioned as candidate implementation/prototype source, not sole academic novelty.
- YOLOv10/RT-DETR can be academic anchors/baseline references for NMS-free/end-to-end detection.
- DiffMOT is proposed robust tracker; OC-SORT/SORT-family is efficient fallback/baseline.
- S035 NVIDIA DeepStream documentation is vendor/technical reference only.
- Distinguish density-map crowd counting from trajectory-based detection-tracking-counting.
- Keep internal source IDs `[S###]` for now.

## Target structure

```markdown
# USULAN PENDEKATAN (PROPOSED METHOD)

## Gambaran Umum Pendekatan
## Arsitektur Sistem yang Diusulkan
## Rencana Data dan Preprocessing
## Tahapan Metodologi
## Rencana Skenario Eksperimen
## Rencana Metrik Evaluasi
## Ancaman Validitas dan Mitigasi Awal
```

## Style

- Bahasa Indonesia akademik-natural.
- Dense and precise; no filler.
- No generic AI-sounding transition paragraphs.
- Avoid overclaiming.

## Completion

Write the target file, read it back if possible, then exit. Do not produce chat summary.
