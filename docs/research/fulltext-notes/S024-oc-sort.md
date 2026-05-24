# Full-Text Note — S024 Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking

## Source identity

- Source ID: S024
- Title: Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking
- Authors: Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani
- URL/DOI/arXiv: https://openaccess.thecvf.com/content/CVPR2023/html/Cao_Observation-Centric_SORT_Rethinking_SORT_for_Robust_Multi-Object_Tracking_CVPR_2023_paper.html ; arXiv: 2203.14360
- Access date: 25 May 2026 WIB
- Venue/source type: IEEE/CVF CVPR 2023 conference paper, pp. 9686–9696; open-access CVF paper and arXiv open version
- Indexed/peer-reviewed status: Peer-reviewed IEEE/CVF CVPR paper; source-ledger `B-support` canonical OC-SORT baseline.

## Why this source matters

OC-SORT is a canonical lightweight MOT baseline for the proposal because it remains simple, online, and real-time while explicitly addressing occlusion and non-linear motion failure cases in SORT/Kalman tracking. It supports the planned fallback/benchmark role beside DiffMOT: DiffMOT can be positioned for non-linear motion robustness, while OC-SORT can be positioned as an efficient SORT-family comparator or fallback. It also gives safe language for explaining why identity switches occur when occlusion and motion-model error accumulate.

## Problem addressed

- SORT and many Kalman-filter MOT methods assume approximately linear/constant-velocity object motion.
- When objects are occluded, no detector observation is available for Kalman update; SORT performs a dummy update and trusts the prior estimate, so state error accumulates over time.
- The paper argues that most motion-model tracking errors occur when occlusion and non-linear motion occur together.
- The authors identify three SORT limitations: sensitivity to state-estimation noise, temporal error magnification during unobserved periods, and an estimation-centric design that extends tracks using estimates rather than observations.

## Method summary

- OC-SORT keeps the SORT philosophy: simple, online, and real-time tracking from off-the-shelf detections.
- Core idea: move from an estimation-centric to an observation-centric design, using detector observations to correct accumulated Kalman-filter errors.
- Main modules:
  1. **Observation-centric Re-Update (ORU):** triggered when a lost track is re-associated. It backchecks the lost interval, generates a virtual trajectory between the last observation before loss and the new observation that reactivates the track, then reruns predict/re-update over the lost period to correct Kalman parameters.
  2. **Observation-Centric Momentum (OCM):** adds a motion-direction consistency term to the association cost, computed from observations rather than noisy state estimates. The cost combines negative IoU and a weighted velocity-consistency term.
  3. **Observation-Centric Recovery (OCR):** a heuristic second association attempt between the last observation of unmatched tracks and unmatched detections, useful for short occlusion or stopping cases.
- Implementation details verified from the paper: for MOT17/MOT20/DanceTrack, detections use publicly available YOLOX weights by ByteTrack; ORU uses constant-velocity virtual trajectory; OCM uses observations three time steps apart (`Delta t=3`) and weight `lambda=0.2`; detection confidence threshold is 0.4 for MOT20 and 0.6 for other datasets; IoU association threshold is 0.3.

## Dataset / evaluation protocol

- Datasets: MOT17, MOT20, KITTI, DanceTrack, and CroHD in the appendix.
- MOT17/MOT20/DanceTrack: use public YOLOX detections from ByteTrack for fair comparison in the shared-detection blocks; tables also discuss private-detection test settings.
- KITTI: uses detections from PermaTrack's public release.
- DanceTrack is emphasized because it has highly non-linear human motion, similar appearance, severe occlusion, and frequent crossovers.
- Reported runtime: 793 FPS on an Intel i9-9980XE CPU @ 3.00 GHz, given off-the-shelf detections; abstract states 700+ FPS on a single CPU.

## Metrics reported

- HOTA is the main metric because it balances detection and association.
- AssA and IDF1 are emphasized for association performance.
- MOTA, FP, FN, ID switches, and fragmentations are also reported, but the paper warns that MOTA is highly related to detection performance and fair mainly when methods share detections.
- Key reported values:
  - MOT17 test with private detections: OC-SORT HOTA 63.2, MOTA 78.0, IDF1 77.5, IDs 1950, Frag 2040, AssA 63.2.
  - MOT20 test with private detections: OC-SORT HOTA 62.1, MOTA 75.5, IDF1 75.9, IDs 913, Frag 1198, AssA 62.0.
  - DanceTrack test: OC-SORT HOTA 54.6, DetA 80.4, AssA 40.2, MOTA 89.6, IDF1 54.6; with linear interpolation, HOTA 55.1 and IDF1 54.9.
  - KITTI test: OC-SORT improves pedestrian tracking over PermaTrack in the paper's table, but car tracking exposes a limitation of IoU-only association when motion is fast/low frame-rate.

## Findings safe to cite

- OC-SORT shows that a basic Kalman-filter/SORT framework can be strengthened by correcting accumulated errors with observations after occlusion.
- The authors explicitly connect SORT failures to occlusion plus non-linear motion, which is useful for the proposal's ID-switch/double-counting rationale.
- ORU is shown in ablation to improve HOTA/AssA/IDF1 on MOT17-val and DanceTrack-val; OCM is especially helpful on DanceTrack where motion is complicated and occlusion is heavy.
- OC-SORT is very fast when detections are already provided: 793 FPS on the reported CPU, so it is appropriate as a lightweight fallback/comparator claim.
- The paper positions HOTA as the main metric and AssA/IDF1 as important association metrics, supporting the proposal's multi-metric evaluation plan.

## Limitations stated by authors

- On KITTI car tracking, the default OC-SORT implementation using IoU matching can be weak when objects move fast or frame rate is low, because consecutive-frame box IoU can be very low or zero.
- The authors state that adding other cues or appearance similarity can address this issue, indicating that IoU-only association is not universally sufficient.
- The authors use a shared parameter stack across datasets and note that careful parameter tuning could further boost performance.
- The authors mention adaptive detection thresholds from previous work as potentially useful, but OC-SORT keeps a simple design.
- Some KITTI results use offline head padding post-processing to write back entries from track initialization; this is not the same as a purely online count/event output.

## Limitations inferred for this project

- OC-SORT is a tracker, not a people-counting pipeline; it does not define RoI/line/zone crossing, counting-state memory, or count-error metrics.
- The very high FPS refers to the tracker given detections, not detector+tracker end-to-end runtime.
- It is a strong lightweight fallback but still relies on detector quality and IoU-style spatial association.
- It improves SORT under occlusion/non-linear motion but still uses a constant-velocity virtual trajectory in ORU; do not position it as equivalent to a learned non-linear predictor such as DiffMOT.
- Public-space CCTV with dense crowds may require domain-specific validation beyond MOT17/MOT20/DanceTrack/KITTI.

## Exact claims allowed in draft

- "OC-SORT rethinks SORT from an observation-centric perspective, adding ORU, OCM, and OCR to reduce Kalman-filter error accumulation during occlusion."
- "The CVPR 2023 paper reports 700+ FPS / 793 FPS tracking speed on CPU when off-the-shelf detections are provided, supporting its use as a lightweight fallback or comparator."
- "OC-SORT is a fair baseline for tracking-by-detection systems because it explicitly discusses occlusion, non-linear motion, HOTA, AssA, IDF1, and detector-sharing protocols."
- "For the proposal, OC-SORT can be used as an efficient fallback/benchmark, while DiffMOT is better suited for a non-linear motion emphasis."

## Claims NOT allowed

- Do not claim OC-SORT's FPS includes detector inference.
- Do not claim OC-SORT solves all non-linear motion or dense crowd cases.
- Do not claim it is detector-independent or appearance-independent in all domains; the paper itself notes IoU-only weakness in fast/low-frame-rate settings.
- Do not use OC-SORT results as evidence of people-counting accuracy.
- Do not call it obsolete or weak; the paper is a canonical strong baseline and should be positioned respectfully.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 3: Multi-object tracking pada kerumunan padat, oklusi, dan identity switch.
- Section 4: Diffusion-based MOT dan prediksi lintasan non-linear, as the lightweight fallback/comparator beside DiffMOT.
- Section 5: Counting logic berbasis RoI/line/zone/ID memory, as support that stable IDs are needed before counting.
- Section 6: Dataset, metrik evaluasi, dan constraint real-time/edge, as source for HOTA/AssA/IDF1 and tracker-only FPS caution.

## Notes for citation auditor

- Bibliography key in `references/references.bib`: `S024`.
- Ledger status: `B-support`, canonical OC-SORT baseline, IEEE/CVF CVPR 2023 peer-reviewed.
- Full text accessed via official CVF open-access PDF/HTML and arXiv ID 2203.14360 on 25 May 2026 WIB.
- Any runtime claim must specify "given off-the-shelf detections" or "tracking stage only" to avoid detector-runtime overclaim.
