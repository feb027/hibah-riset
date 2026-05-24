# Source Ledger — SOTA People Counting / Detection / MOT

> Status: setup scaffold. Final citations must be validated before draft writing. Access date default for setup leads: 25 Mei 2026 WIB.

| ID | Status | Topic | Source type | Year/date | Title/source | URL/DOI/arXiv | Why relevant | Limit/risk | Mapped section |
|---|---|---|---|---|---|---|---|---|---|
| S001 | lead | YOLO26 / NMS-free detector | arXiv preprint | 2026 | YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection | https://arxiv.org/abs/2601.12882 | Primary candidate for proposal's YOLO26 claims | Need read full paper; verify author/version and benchmark claims | detector |
| S002 | lead | YOLO26 implementation | vendor docs | 2026 | Ultralytics YOLO26 docs | https://docs.ultralytics.com/models/yolo26 | Implementation-facing details for model usage/deployment | Vendor source, not peer-reviewed; do not use as sole evidence for novelty | detector/deployment |
| S003 | lead | dense-scene MOT | journal | 2025 | OcclusionTrack: Multi-Object Tracking in Dense Scenes | https://www.mdpi.com/2076-3417/15/24/13030 | Fresh occlusion-focused MOT source | Need verify method, benchmarks, relevance to people/crowd | tracker/gap |
| S004 | lead | occlusion MOT | journal | 2025 | A two stage multi object tracking algorithm with transformer ... | https://www.nature.com/articles/s41598-025-16389-4 | Fresh transformer/MOT occlusion source | Need extract exact contribution and limitations | tracker |
| S005 | lead | occluded MOT | conference | 2025 | More Than Meets the Eye: Enhancing Multi-Object Tracking Even ... | https://icml.cc/virtual/2025/poster/46062 | Latest occlusion-aware MOT candidate | Need paper/PDF and exact claims | tracker/gap |
| S006 | lead | MOT review | journal/review | 2025 | A Review of Multi-Object Tracking in Recent Times | https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/cvi2.70010 | Helps organize taxonomy for related work | Need access and check coverage | tracker/taxonomy |
| S007 | from proposal | diffusion tracker | CVPR paper | 2024 | DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction | TBD official CVF/arXiv | Core tracker proposed in proposal | Need official URL/BibTeX and limitation analysis | tracker |
| S008 | from proposal | OC-SORT | CVPR paper/GitHub | 2023 | Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking | TBD official CVF/arXiv/GitHub via gh | Baseline/fallback for lighter deployment | Older but still relevant baseline | tracker/deployment |
| S009 | from proposal | dense crowd dataset | benchmark | 2020 | MOT20: A benchmark for multi object tracking in crowded scenes | TBD official/arXiv | Dataset for crowded tracking validation | Older dataset, acceptable benchmark | dataset |
| S010 | from proposal | diverse motion dataset | CVPR paper | 2022 | DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion | TBD official/arXiv | Dataset for diverse/non-linear motion | Older but standard benchmark | dataset |
| S011 | from proposal | MOT metric | journal | 2021 | HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking | TBD DOI/arXiv | Metric for balancing detection and association | Metric source, not SOTA method | metrics |

## Source quality labels

- `accepted`: read and usable as citation.
- `lead`: found but not fully read/validated.
- `reject`: not suitable, with reason.
- `background`: useful for context but not central citation.

## Required fill before Phase 2

- Add at least 9 more sources.
- Convert S001–S011 from `lead/TBD` into accepted/rejected after reading.
- Add a 1–3 sentence evidence note for each accepted source.
