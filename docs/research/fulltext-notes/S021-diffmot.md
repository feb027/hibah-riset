# Full-Text Note — S021 DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction

## Source identity

- Source ID: S021
- Title: DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction
- Authors: Weiyi Lv, Yuhang Huang, Ning Zhang, Ruei-Sung Lin, Mei Han, Dan Zeng
- URL/DOI/arXiv: https://openaccess.thecvf.com/content/CVPR2024/html/Lv_DiffMOT_A_Real-time_Diffusion-based_Multiple_Object_Tracker_with_Non-linear_Prediction_CVPR_2024_paper.html ; arXiv: 2403.02075
- Access date: 25 May 2026 WIB
- Venue/source type: IEEE/CVF CVPR 2024 conference paper, pp. 19321–19330; open-access CVF paper and arXiv open version
- Indexed/peer-reviewed status: Peer-reviewed IEEE/CVF CVPR paper; source-ledger `A-main`.

## Why this source matters

DiffMOT is the central source for the proposal's tracker novelty because it explicitly targets non-linear motion prediction in MOT. It is especially relevant for dense public-space people counting where abrupt direction changes, acceleration/deceleration, and trajectory fragmentation can create ID switches and double-counting. It also provides measured speed/accuracy trade-offs, so claims about "real-time diffusion MOT" can be grounded in reported FPS rather than assumed.

## Problem addressed

- Tracking-by-detection trackers commonly use Kalman-filter motion prediction, which assumes constant velocity/linear motion.
- The paper argues that this is often adequate for pedestrian-dominant datasets such as MOT17/20 but fails in scenes with non-linear and diverse motion, such as DanceTrack and SportsMOT.
- The goal is to obtain accurate non-linear motion prediction while preserving real-time tracking speed.

## Method summary

- DiffMOT follows a tracking-by-detection framework with three parts: detection, motion prediction, and association.
- Detection: uses YOLOX as detector.
- Motion prediction: replaces the usual Kalman-filter predictor with **D2MP (Decoupled Diffusion-based Motion Predictor)**.
  - Object motion is defined as the difference between current and previous bounding boxes: changes in center position, width, and height.
  - D2MP treats motion prediction as a generative denoising problem conditioned on historical object motion.
  - The conditioned input contains the previous `n` frames of box and motion information; the paper sets `n=5` in the main implementation.
  - The historical motion information network (HMINet) uses multi-head self-attention layers to extract condition embeddings, then fuses the condition with noisy motion features.
  - The decoupled diffusion design splits the data-to-noise process into data-to-zero and zero-to-noise sub-processes and enables one-step sampling for faster inference.
- Association: similar to ByteTrack, with high-score detections matched first and low-score detections matched later using the Hungarian algorithm. Matching costs include ReID feature distance and IoU for high-scoring boxes; low-scoring boxes use IoU cost. The paper also adopts dynamic appearance and adaptive weighting techniques from prior work.

## Dataset / evaluation protocol

- Main non-linear motion benchmarks: DanceTrack and SportsMOT.
- Additional pedestrian-dominant benchmark: MOT17 under a private-detector protocol.
- DanceTrack: used to test diverse/non-linear dance motion and weak appearance distinction.
- SportsMOT: includes soccer, basketball, and volleyball sequences with extensive acceleration/deceleration; 45 training, 45 validation, and 150 test sequences are described.
- MOT17: used to show performance remains satisfactory in conventional pedestrian-dominant tracking.
- Implementation details verified from the full text: historical window `n=5`; high detection threshold `tau_high=0.6`; low detection threshold `tau_low=0.4`; D2MP uses one-step sampling; runtime reported on an RTX 3090 machine.

## Metrics reported

- HOTA, AssA, DetA from Higher Order Tracking Accuracy family.
- IDF1 for identity/association performance.
- MOTA from CLEAR metrics.
- FPS for speed.
- Key reported values:
  - DanceTrack test with YOLOX-X: HOTA 62.3, IDF1 63.0, AssA 47.2, MOTA 92.8, DetA 82.5, 22.7 FPS.
  - DanceTrack detector trade-off: YOLOX-S reaches 30.3 FPS with HOTA 53.3; YOLOX-X reaches HOTA 62.3 with 22.7 FPS.
  - SportsMOT test, train-only detector setup: HOTA 72.1, IDF1 72.8, AssA 60.5, MOTA 94.5, DetA 86.0.
  - SportsMOT test, detector trained on train+validation following MixSORT convention: HOTA 76.2, IDF1 76.1, AssA 65.1, MOTA 97.1, DetA 89.3.
  - MOT17 test under private detector with same YOLOX detector: HOTA 64.5, IDF1 79.3, AssA 64.6, MOTA 79.8, DetA 64.7.

## Findings safe to cite

- The authors state that DiffMOT introduces a diffusion probabilistic model into MOT to address non-linear motion prediction; phrase this as "to the authors' knowledge" if citing firstness.
- D2MP directly models motion distribution and predicts an individual object's motion conditioned on its historical motion information.
- One-step sampling is a key efficiency design; the authors report 22.7 FPS on DanceTrack with YOLOX-X and 30.3 FPS with YOLOX-S.
- On DanceTrack, DiffMOT reports HOTA 62.3 and IDF1 63.0, outperforming the listed SOTA trackers in the paper's table under the stated protocol.
- On SportsMOT, DiffMOT reports HOTA 72.1 in the train-only detector setup and HOTA 76.2 when detectors are trained on train+validation, outperforming the listed comparison methods in the paper's table.
- On MOT17, DiffMOT is competitive but not the clear top in the table; use it as evidence of transfer to conventional pedestrian tracking, not as a strongest MOT17 claim.
- Ablation on DanceTrack validation shows D2MP outperforming IoU-only, Kalman Filter, LSTM, and Transformer motion models in HOTA/IDF1/AssA under the paper's setup.

## Limitations stated by authors

- No dedicated limitations section was found in the CVPR full text.
- The authors acknowledge the accuracy-speed trade-off across detectors: larger YOLOX variants improve HOTA/IDF1 but reduce FPS, while smaller variants are faster but less accurate.
- The paper frames DiffMOT primarily around non-linear motion; it does not claim to solve all dense-crowd occlusion and counting problems.

## Limitations inferred for this project

- DiffMOT is detection-dependent because it remains a tracking-by-detection method using YOLOX detections.
- Reported real-time speed is measured on an RTX 3090; this does not prove the method will be real-time on edge hardware or the project's target deployment device.
- The strongest evidence is on DanceTrack and SportsMOT non-linear motion; CCTV public-space crowds may involve different camera geometry, occlusion density, and counting-zone requirements.
- DiffMOT does not include RoI/line/zone counting, ID state memory, or count-error metrics.
- Diffusion-based motion prediction adds modeling complexity relative to OC-SORT/SORT-family fallbacks.

## Exact claims allowed in draft

- "DiffMOT is a CVPR 2024 tracking-by-detection method that replaces Kalman-style linear prediction with a decoupled diffusion-based motion predictor for non-linear motion."
- "The authors report HOTA 62.3 and IDF1 63.0 on DanceTrack with YOLOX-X at 22.7 FPS, and show a detector-dependent speed/accuracy trade-off up to 30.3 FPS with YOLOX-S."
- "DiffMOT supports the proposal's need for a tracker robust to non-linear motion, while separate counting logic is still needed for people counting."
- "Use OC-SORT/SORT-family methods as lightweight fallback comparators because DiffMOT's diffusion predictor is more complex and its reported runtime depends on GPU/detector choice."

## Claims NOT allowed

- Do not claim DiffMOT independently solves counting, line crossing, or double-counting.
- Do not claim DiffMOT is detector-independent.
- Do not claim the reported 22.7 FPS guarantees real-time edge deployment.
- Do not claim DiffMOT is best on all MOT datasets; the MOT17 table shows competitive rather than dominant performance.
- Do not generalize DanceTrack/SportsMOT results directly to local CCTV public-space scenes without validation.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 4: Diffusion-based MOT dan prediksi lintasan non-linear.
- Section 3: Multi-object tracking pada kerumunan padat, oklusi, dan identity switch, as evidence about Kalman-filter limits and association metrics.
- Section 7: Sintesis gap dan posisi penelitian, as support for selecting DiffMOT as the main non-linear tracker and requiring a lightweight fallback.

## Notes for citation auditor

- Bibliography key in `references/references.bib`: `S021`.
- Ledger status: `A-main`, IEEE/CVF CVPR 2024 peer-reviewed.
- Full text accessed via official CVF open-access PDF/HTML and arXiv ID 2403.02075 on 25 May 2026 WIB.
- Use exact reported numbers only with dataset/protocol context: DanceTrack/SportsMOT/MOT17, YOLOX detector variant, and FPS hardware where stated.
