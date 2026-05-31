# Progress Log — Hibah Riset PUU 2026

## 2026-05-25 WIB — Phase 0 setup

- [x] Verified current local date: 25 Mei 2026 WIB.
- [x] Located source PDFs in `docs/`.
- [x] Extracted proposal and lecturer guide into `docs/_extracted/`.
- [x] Created project brief, pre-plan, source ledger, draft/review structure, and validation script.
- [x] Create/push GitHub repo: https://github.com/feb027/hibah-riset
- [ ] Phase 1 SOTA source ledger.

## 2026-05-25 WIB — Phase 1 source discovery started

- [x] Collected indexed/credible source candidates for detector/YOLO26/NMS-free/edge.
- [x] Collected indexed/credible source candidates for MOT/dense crowd/occlusion/DiffMOT/OC-SORT.
- [x] Collected indexed/credible source candidates for people counting/ROI/datasets/metrics.
- [x] Updated `docs/research/source-ledger.md` with 38 source entries.
- [x] Updated `docs/research/evidence-matrix.md` with draftable claims, limits, and blockers.
- [x] Run reviewer pass on source ledger before Phase 2 outline finalization: `docs/reviews/review-source-ledger.md` verdict `READY_FOR_OUTLINE`.

## 2026-05-25 WIB — Phase 2 related-work outline

- [x] Rewrote `docs/outlines/pekerjaan-terkait-outline.md` into a full thematic outline.
- [x] Added source-to-section map and anti-overclaim rules for Phase 3 writer.
- [x] Run reviewer pass on Phase 2 outline: `docs/reviews/review-pekerjaan-terkait-outline.md` verdict `READY_FOR_DRAFT`.

## 2026-05-25 WIB — Phase 0.5 infrastructure hardening

- [x] Added bibliography infrastructure under `references/`.
- [x] Generated starter `references/references.bib` from DOI/arXiv metadata where possible.
- [x] Added source ID mapping in `references/source-id-map.md`.
- [x] Added full-text reading note templates under `docs/research/fulltext-notes/`.
- [x] Improved prompts for researcher, full-text reader, writers, reviewer, citation auditor, and final verifier.
- [x] Upgraded `scripts/validate_research_artifacts.py` into a stronger quality gate.
- [x] Updated README, AGENTS, and pre-plan with evidence-gate rules.

## 2026-05-25 WIB — Phase 2.5 full-text notes

- [x] Filled full-text notes for detector sources: S003 YOLOv10 and S004 RT-DETR.
- [x] Filled full-text notes for people-counting/crowd-counting sources: S010, S011, S027, S028.
- [x] Filled full-text notes for MOT/metric sources: S018, S021, S024, S025.
- [x] Added Phase 2.5 review: `docs/reviews/review-fulltext-notes.md` verdict `READY_FOR_DRAFT`.
- [x] Strengthened validator to reject priority full-text notes that still contain template markers or missing required sections.


## 2026-05-25 WIB — Phase 2.5 correction: Indonesian bridge + YOLO26 caution notes

- [x] Added YOLO26 caution full-text notes: `S001-yolo26-arxiv-analysis.md` and `S002-yolo26-ultralytics-docs.md`.
- [x] Added `docs/research/fulltext-notes/00-phase2-5-indonesian-brief.md` for Bahasa Indonesia writer handoff.
- [x] Updated full-text reader prompt and README to require Bahasa Indonesia note content while preserving validator headings.
- [x] Updated Phase 2.5 review and validator to include S001/S002 as priority caution notes.


## 2026-05-25 WIB — Phase 3 PEKERJAAN TERKAIT draft

- [x] Drafted `docs/drafts/pekerjaan-terkait.md` in Bahasa Indonesia academic style.
- [x] Used thematic structure from Phase 2 outline: domain counting, detector, MOT, DiffMOT, counting logic, evaluation, and gap synthesis.
- [x] Preserved YOLO26 caution positioning: candidate implementation/context, not peer-reviewed novelty anchor.
- [x] Reviewer pass wrote `docs/reviews/review-pekerjaan-terkait.md` with verdict `READY_FOR_PATCH`.
- [x] Patched citation blocker by adding BibTeX entries for S006, S015, S016, and S017.
- [x] Patched YOLO26 wording in the gap synthesis.
- [x] Patch verification wrote `docs/reviews/review-pekerjaan-terkait-patch.md` with verdict `READY_FOR_NEXT_PHASE`.
- [x] Strengthened validator to catch draft citations missing from `references/references.bib` and require Phase 3 review gates.


## 2026-05-25 WIB — Phase 4 PENDAHULUAN draft

- [x] Drafted `docs/drafts/pendahuluan.md` in Bahasa Indonesia academic style using Phase 3 `PEKERJAAN TERKAIT` as the SOTA/gap basis.
- [x] Sharpened proposal introduction around urgency, technical problem, SOTA summary, gap, research questions, objectives/scope, contribution, and 5-year roadmap.
- [x] Preserved YOLO26 caution positioning and density-map vs trajectory/ID counting separation.
- [x] Reviewer pass wrote `docs/reviews/review-pendahuluan.md` with verdict `READY_FOR_PATCH`.
- [x] Patched blockers: reduced draft below the PUU 1000-word limit and replaced article-outline ending with a PUU-style five-year roadmap.
- [x] Patch verification wrote `docs/reviews/review-pendahuluan-patch.md` with verdict `READY_FOR_NEXT_PHASE`.
- [x] Strengthened validator to require Phase 4 review gates.


## 2026-05-25 WIB — Phase 5 lecturer handoff package

- [x] Created `docs/handoff/lecturer-handoff-2026-05-25.md` with status, file list, core argument, safe gap, research questions, risks, agenda, and checklist.
- [x] Created `docs/handoff/draft-sections-clean.md` combining copy-ready `PENDAHULUAN` and `PEKERJAAN TERKAIT`.
- [x] Verified source/citation status: 38 mapped sources; all cited `[S###]` IDs in the drafts exist in `references/references.bib`.
- [x] Review gate wrote `docs/reviews/review-handoff-package.md` with verdict `READY_FOR_DELIVERY`.
- [x] Strengthened validator to require Phase 5 handoff artifacts and delivery review.

## Next phase

After lecturer feedback: convert accepted source IDs to IEEE/numeric citations, update bibliography metadata, and refine method/prototype plan based on selected detector/tracker/evaluation decisions.

## 2026-05-25 WIB — Casual lecturer discussion questions

- [x] Added `docs/handoff/pertanyaan-santai-untuk-dosen.md` with non-formal, practical questions for offline lecturer discussion.
- [x] Questions cover focus/novelty, YOLO26, DiffMOT/OC-SORT, counting logic, datasets, evaluation, citations, draft quality, and next steps.

## 2026-05-25 WIB — Casual lecturer questions reframed

- [x] Revised `docs/handoff/pertanyaan-santai-untuk-dosen.md` because lecturers may not be deeply involved in the technical research details.
- [x] Added explanation-first flow: context → problem → proposed direction → ask for advice.
- [x] Added short scripts for explaining why YOLO alone is not enough, why DiffMOT is considered, what the safe novelty is, and what needs validation.

## 2026-05-25 WIB — YOLOv10/RT-DETR casual explanation added

- [x] Expanded `docs/handoff/pertanyaan-santai-untuk-dosen.md` so the YOLO26 section explains NMS, YOLOv10, and RT-DETR in lecturer-friendly language before asking for advice.
- [x] Added ready answers for likely lecturer questions: why YOLOv10/RT-DETR are mentioned and how they differ from YOLO26.

## 2026-05-25 WIB — Indonesian source-ledger paper summaries

- [x] Downloaded/saved available source materials under `docs/research/papers/` and extracted readable text under `docs/research/paper-text/` for all 38 mapped sources.
- [x] Created `docs/research/source-ledger-ringkasan-indonesia.md` with Indonesian summaries for S001–S038 using fields: Judul, Penulis, Jurnal/Konferensi, URL, Permasalahan, Kontribusi, Metode/solusi, Hasil utama, Batasan, Relevansi.
- [x] Used delegated agents for source-summary batches and retained batch outputs as supporting artifacts.
- [x] Added `scripts/download_and_extract_sources.py` for reproducible source download/extraction attempts.

## 2026-05-31 UTC — Phase 6 USULAN PENDEKATAN / Proposed Method

- [x] Extracted the lecturer guide section from `docs/F-Paper Penelitian.pdf` into `docs/_extracted/F-Paper-Penelitian.txt` and used the Proposed Method requirements as the phase gate.
- [x] Created Phase 6 pre-plan: `docs/plans/2026-05-31-phase6-proposed-method.md`.
- [x] Created proposed-method outline: `docs/outlines/usulan-pendekatan-outline.md`.
- [x] Created system architecture diagram source: `docs/diagrams/proposed-method-architecture.mmd`.
- [x] Created writer/reviewer prompts for Proposed Method.
- [x] Drafted `docs/drafts/usulan-pendekatan.md` as a pre-experiment methodology/architecture/scenario plan.
- [x] Reviewer gate wrote `docs/reviews/review-usulan-pendekatan.md` with verdict `READY_FOR_DISCUSSION`.
- [x] Created discussion handoff: `docs/handoff/proposed-method-handoff-2026-05-31.md`.
- [x] Strengthened validator to require Proposed Method artifacts and guard against fake experiment-result claims.
