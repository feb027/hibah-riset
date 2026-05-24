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

## Next phase

Phase 4: draft `docs/drafts/pendahuluan.md` after using Phase 3 related work as the SOTA/gap basis.
