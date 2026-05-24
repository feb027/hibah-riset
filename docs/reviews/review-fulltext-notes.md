# Review — Phase 2.5 Full-Text Notes

Date: 2026-05-25 WIB
Reviewer: Hermes main verification pass after full-text-reader subagents
Artifact scope: `docs/research/fulltext-notes/S003`, `S004`, `S010`, `S011`, `S018`, `S021`, `S024`, `S025`, `S027`, `S028`

## Verdict

**READY_FOR_DRAFT**

No blocker remains for starting Phase 3 draft of `PEKERJAAN TERKAIT`, provided the writer uses these notes as evidence boundaries and does not cite performance/method claims outside the allowed-claims sections.

## Completeness check

| Source | Note file | Required sections | TODO/template residue | Draft readiness |
|---|---|---:|---:|---|
| S003 | `S003-yolov10.md` | complete | none | ready |
| S004 | `S004-rt-detr.md` | complete | none | ready |
| S010 | `S010-passenger-flow-yolo-edge.md` | complete | none | ready |
| S011 | `S011-vision-people-counting-tracking.md` | complete | none | ready |
| S018 | `S018-occlusiontrack.md` | complete | none | ready |
| S021 | `S021-diffmot.md` | complete | none | ready |
| S024 | `S024-oc-sort.md` | complete | none | ready |
| S025 | `S025-hota.md` | complete | none | ready |
| S027 | `S027-crowd-counting-complex-review.md` | complete | none | ready |
| S028 | `S028-edge-crowd-counting-kd.md` | complete | none | ready |

## Evidence quality check

- Detector notes S003/S004 correctly limit claims to object detection, end-to-end/NMS-free design, latency/accuracy framing, and COCO-style detector evaluation. They do **not** claim people-counting, tracking, line-crossing, or double-counting performance.
- Counting notes S010/S011/S027/S028 correctly distinguish detection-tracking-counting from density-map crowd counting.
- MOT notes S018/S021/S024 correctly separate dense-scene occlusion, non-linear motion prediction, and lightweight fallback/baseline roles.
- Metric note S025 correctly positions HOTA as an evaluation metric, not a tracking/counting method.
- Each note contains `Exact claims allowed in draft` and `Claims NOT allowed`, which is sufficient for Phase 3 writer guardrails.

## Citation integrity check

- All ten priority source IDs exist in `docs/research/source-ledger.md`.
- All ten priority source IDs exist as BibTeX keys in `references/references.bib`.
- Notes are aligned with `docs/research/evidence-matrix.md` blocker row: full-text notes now exist for S003, S004, S010, S011, S018, S021, S024, S025, S027, and S028.

## Remaining risks / writer cautions

1. **S003/S004 bibliography metadata:** `references.bib` currently keeps source-ID keys; citation auditor should later decide whether final bibliography needs formal NeurIPS/CVPR proceedings metadata instead of arXiv-oriented metadata.
2. **MDPI acceptability:** S010, S011, and S018 are useful but may need support from CVF/Springer/Nature/IEEE sources if the lecturer is strict about MDPI.
3. **Performance claims:** numeric metrics from notes can be cited only with dataset/protocol context; do not compare numbers across papers as if they used identical conditions.
4. **Density-map vs ID-based counting:** S027/S028 support crowd-counting background and edge constraints, but they must not be used as proof of line/zone crossing or identity-persistence counting.
5. **YOLO26 positioning:** still use YOLO26 as candidate/latest implementation context only; anchor academic detector claims on S003/S004/S005/S006/S007.

## Decision

Phase 2.5 is complete. Proceed to Phase 3 with the writer prompt `prompts/writer-pekerjaan-terkait.md` and the outline `docs/outlines/pekerjaan-terkait-outline.md`.
