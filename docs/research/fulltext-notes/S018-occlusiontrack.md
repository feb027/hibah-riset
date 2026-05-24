# Full-Text Note — S018 OcclusionTrack: Multi-Object Tracking in Dense Scenes

## Source identity

- Source ID: S018
- Title: OcclusionTrack: Multi-Object Tracking in Dense Scenes
- Authors: Yuzhi Chen, Fanqin Meng, Ziqiu Chen
- URL/DOI/arXiv: https://www.mdpi.com/2076-3417/15/24/13030 ; DOI: 10.3390/app152413030
- Access date: 25 May 2026 WIB
- Venue/source type: Applied Sciences, 2025, 15(24), article 13030; open-access journal article; published 10 December 2025
- Indexed/peer-reviewed status: Peer-reviewed MDPI journal article according to the publisher page; use as MDPI/source-ledger `A-main` with the project caveat that lecturer acceptance of MDPI should be checked.

## Why this source matters

OcclusionTrack is directly relevant to the proposal's MOT component because it targets dense-scene occlusion, a core failure case for public-space people counting. It gives concrete mechanisms for partial occlusion, camera motion, association ambiguity, and complete-occlusion recovery inside a tracking-by-detection pipeline. It is useful evidence for explaining why counting based only on detector boxes is fragile when IDs are lost, reactivated, or switched.

## Problem addressed

- The paper addresses multi-object tracking in dense scenes where frequent occlusion degrades detection boxes, makes IoU association ambiguous, and causes complete track loss.
- It identifies four practical TBD failure modes: partial occlusion degrading detection quality, camera motion shifting coordinates across frames, overlapping boxes causing association ambiguity, and complete occlusion causing Kalman-filter state/parameter error accumulation.
- The target use case is pedestrian MOT on standard benchmarks, not a counting system.

## Method summary

- Overall paradigm: tracking-by-detection, using ByteTrack as baseline and YOLOX detections.
- The tracker uses only IoU distance for association, with high-score and low-score detections similar to ByteTrack, but adds four modules:
  1. **Confidence-Based Kalman Filter (CBKF):** dynamically scales Kalman measurement noise using detection confidence, `R(conf)=R*exp(-beta*(conf-c0))`. High-confidence detections are trusted more; low-confidence detections are trusted less.
  2. **Camera Motion Compensation (CMC):** estimates inter-frame global motion with sparse optical flow/keypoints and RANSAC affine transformation, then transforms predicted states/covariances so IoU matching is performed in the current-frame coordinate system.
  3. **Depth–Cascade-Matching (DCM):** calculates pseudo-depth from bounding-box geometry, splits detections and tracks into depth levels, and runs Hungarian/IoU matching by depth level to reduce ambiguous matches among overlapping objects.
  4. **CMC-detection-based Re-activate:** when a lost trajectory is rematched, it applies accumulated CMC, interpolates virtual detection boxes and confidence scores between the last matched detection and new detection, and reruns CBKF over the lost interval to correct accumulated state error.
- Pipeline details: detect boxes and confidence scores; split high/low detections; estimate CMC; predict tracks; run DCM on high detections, then low detections; update active tracks with CBKF or re-activate lost tracks; remove tracks after `max age`.

## Dataset / evaluation protocol

- Benchmarks: MOT17, MOT20, and DanceTrack.
- MOT17 and MOT20: tracking performed on test sets and submitted to MOTChallenge for metrics; training sets split in half to form validation sets for component ablations following ByteTrack-style validation.
- DanceTrack: 100 sequences total, with 40 train, 20 validation, and 40 test sequences; test metrics require submission to the official website.
- Detector/protocol: comparison experiments use the pre-trained YOLOX detector from ByteTrack with the same weights and NMS threshold; different detector quality is also tested in ablation.
- Hardware reported: NVIDIA GeForce RTX3060 GPU for experiments.

## Metrics reported

- CLEAR/MOT metrics: MOTA, ID Switch, FP, FN.
- Identity/association metrics: IDF1 and, for DanceTrack, AssA.
- Balanced tracking metric: HOTA; DetA also reported for DanceTrack.
- Runtime: FPS is reported in test-set comparison tables.
- Key reported test values:
  - MOT17 private detector: OCCTrack HOTA 64.9, MOTA 80.9, IDF1 79.7, ID Switch 1269, FPS 12.5.
  - MOT20 private detector: OCCTrack HOTA 63.2, MOTA 76.9, IDF1 77.5, ID Switch 916, FPS 8.5.
  - DanceTrack private detector: OCCTrack HOTA 57.5, MOTA 91.4, IDF1 58.4, AssA 40.9, DetA 81.0.

## Findings safe to cite

- OcclusionTrack integrates CBKF, CMC, DCM, and trajectory reactivation into a unified tracking-by-detection pipeline for dense-scene occlusion.
- The authors report competitive performance on MOT17, MOT20, and DanceTrack while relying on IoU matching rather than a separate appearance/ReID module.
- On MOT17, the authors report +1.8 HOTA, +0.6 MOTA, and +2.4 IDF1 over their ByteTrack baseline using the same YOLOX detector, with ID switches reduced to nearly half of ByteTrack's count.
- On MOT20, the authors report +1.9 HOTA and +2.3 IDF1 over ByteTrack using the same pre-trained YOLOX detector, with ID switches reduced by about 25%.
- On DanceTrack, the authors report +9.8 HOTA, +1.8 MOTA, and +4.5 IDF1 over the baseline with the pre-trained YOLOX detector from OC-SORT.
- The paper explicitly states that detector quality strongly affects tracking-by-detection performance and that stronger detectors improve tracking capability.

## Limitations stated by authors

- **Detector dependence:** TBD trackers depend heavily on detector performance; poor detectors limit OcclusionTrack, and CBKF relies on detection confidence being reasonably calibrated to localization quality.
- **CMC assumptions:** the CMC module uses a global 2D model assuming dominant low-frequency camera motion; effectiveness may decline with dynamic/non-planar backgrounds or high-frequency jitter, and it does not satisfy 3D-scene requirements.
- **Motion-model scope:** the framework retains a linear constant-velocity assumption; performance can decline at extremely low frame rates or with highly non-linear agile motion.
- **Object/domain scope:** the framework is primarily designed and tested on pedestrian tracking; extension to highly deformable objects may require adjustments.
- Future work proposed by the authors: joint detector-tracker optimization, adaptive scene-aware CMC, and deep data-driven motion models replacing the linear Kalman predictor.

## Limitations inferred for this project

- OcclusionTrack supports the MOT/occlusion argument but does not provide people-counting logic, zone/line-crossing logic, or count-error evaluation.
- It is not an edge-deployment proof for the proposed system; reported FPS on MOT17/MOT20 tables is below 30 FPS on the stated RTX3060 setup.
- It uses YOLOX detections, not YOLO26 or the proposed detector stack.
- It is an MDPI Applied Sciences article; if the lecturer is strict about venue hierarchy, pair it with CVPR/Springer anchors such as S021, S024, and S025.
- Because it keeps a linear Kalman prior, it should be positioned as occlusion/camera-motion/association support rather than as the strongest source for non-linear motion prediction.

## Exact claims allowed in draft

- "OcclusionTrack targets dense-scene MOT by integrating confidence-based Kalman updates, camera motion compensation, depth-cascade matching, and trajectory reactivation."
- "In the authors' MOT17/MOT20/DanceTrack experiments, OcclusionTrack reports HOTA/IDF1 improvements over ByteTrack-style baselines under the stated detector protocols."
- "The paper explicitly warns that tracking-by-detection performance remains detector-dependent and that its CMC and linear-motion assumptions limit generalization."
- "For people counting, OcclusionTrack is evidence that occlusion-aware tracking modules can reduce identity instability, but separate counting logic and counting-error evaluation are still required."

## Claims NOT allowed

- Do not claim OcclusionTrack proves the proposed people-counting system is accurate.
- Do not claim it solves all occlusion cases or all non-linear motion; the authors state limits for low frame rate and highly non-linear agile motion.
- Do not claim it is independent of detector quality.
- Do not claim the reported runtime proves real-time edge deployment for the target hardware.
- Do not cite it as a non-MDPI/IEEE/CVF/Springer anchor.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 3: Multi-object tracking pada kerumunan padat, oklusi, dan identity switch.
- Section 5: Counting logic berbasis RoI/line/zone/ID memory, as supporting evidence for why ID persistence matters before counting.
- Section 7: Sintesis gap dan posisi penelitian, as support for occlusion-aware tracking and detector dependence.

## Notes for citation auditor

- Bibliography key in `references/references.bib`: `S018`.
- Ledger status: `A-main`, dense-scene occlusion MOT, MDPI Applied Sciences peer-reviewed.
- Full text accessed from the official MDPI page on 25 May 2026 WIB.
- Safe citation should include DOI `10.3390/app152413030` and avoid overclaiming beyond MOT benchmark evidence.
