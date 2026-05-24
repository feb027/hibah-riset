# Full-Text Note — S010 Real-Time Passenger Flow Analysis in Tram Stations Using YOLO-Based Computer Vision and Edge AI on Jetson Nano

## Source identity

- Source ID: S010
- Title: Real-Time Passenger Flow Analysis in Tram Stations Using YOLO-Based Computer Vision and Edge AI on Jetson Nano
- Authors: Sonia Diaz-Santos; Pino Caballero-Gil; Cándido Caballero-Gil
- URL/DOI/arXiv: https://www.mdpi.com/2073-431X/14/11/476 ; DOI: 10.3390/computers14110476
- Access date: 2026-05-25 WIB
- Venue/source type: *Computers* 2025, 14(11), Article 476; MDPI journal article; open access.
- Indexed/peer-reviewed status: Peer-reviewed journal article per source ledger; MDPI open-access article. Full text read from official MDPI HTML/PDF landing page.
- Citation key in `references/references.bib`: `S010`.

## Why this source matters

This is a directly relevant applied people-counting paper because it combines YOLO-based person detection, lightweight tracking, line/ROI crossing logic, and Jetson Nano deployment in a public-transport setting. It is useful for the proposal’s detection-tracking-counting branch, especially for arguing that edge people-counting systems must balance detection accuracy, tracking continuity, and device constraints. It should not be treated as density-map crowd counting: the implementation counts people who cross an area/line with tracked IDs.

## Problem addressed

The paper addresses real-time passenger-flow monitoring at tram stations, where manual counts and older APC sensors are limited under high passenger density and cannot provide rich movement information. The stated applied goal is to detect people, track them across frames, and count entries/exits at a defined tram-station area under Jetson Nano resource constraints.

## Method summary

- Approach type: **detection-tracking-counting**, not density-map crowd counting.
- Detector: YOLO-family models were benchmarked from YOLOv3 through YOLOv11 variants. The final implementation selected YOLOv5s as the best trade-off in the authors’ experiment.
- Hardware/software: NVIDIA Jetson Nano 4 GB; OpenCV, Python, NumPy, Pandas, Ultralytics YOLO; reported JetPack 5.1.2, CUDA 10.2, and TensorRT acceleration for inference experiments.
- Counting logic: people detections are filtered to the COCO “person” class, tracked with IDs, and counted when their centroid crosses a reference line inside a defined ROI. Downward crossing is treated as entry; upward crossing is treated as exit.
- Tracker: the implementation uses a simple Euclidean-distance centroid association module. The paper discusses Kalman filters, Siamese trackers, and DeepSORT as alternatives/future work, but the implemented tracker is the lightweight Euclidean-distance tracker.

## Dataset / evaluation protocol

- Data source: video sequences recorded at Tenerife tram stations in collaboration with Metropolitano de Tenerife, plus additional open-source footage representing similar passenger-flow conditions.
- Ground truth: manual annotation of video frames/events; the paper states two independent annotators labeled entries/exits in the ROI and resolved disagreements by consensus.
- Evaluation setup: multiple YOLO model variants tested under the same conditions. The table reports input size 640 × 640 for model evaluation and Jetson Nano inference conditions; the text also discusses optimized TensorRT and reduced 640 × 480 operational throughput.
- Data availability: data are available on request from the corresponding author; no public benchmark split is provided in the article.

## Metrics reported

- Metrics defined: Precision, Recall, F1-score, Accuracy, IoU; the paper also discusses mAP as localization-oriented context.
- Main quantitative table verified from official HTML table: model, inference time (s), frame detection (objects/frame), and accuracy (real).
- Best reported model in authors’ selection: YOLOv5s with inference time 2.1041 s, frame detection 8.1333 objects/frame, and accuracy 0.9685.
- Other table values useful for context: YOLOv8s accuracy 0.9419 at 2.4481 s; YOLOv10s accuracy 0.9084 at 2.3788 s; YOLOv11s accuracy 0.8708 at 2.0946 s.
- Runtime note: the authors state the 2.1041 s value is a baseline average total processing time per frame including detection and tracking under Jetson Nano conditions, while optimized TensorRT and 640 × 480 operation reaches about 12 FPS.

## Findings safe to cite

- S010 demonstrates a complete **detection-tracking-counting** pipeline for passenger-flow analysis on Jetson Nano in a tram-station use case.
- In the authors’ evaluation, YOLOv5s gave the best reported accuracy/speed trade-off among tested YOLO variants, with reported accuracy 0.9685 and inference time 2.1041 s in the comparison table.
- The system uses ROI/line crossing and object IDs to count entries/exits, which makes it relevant to trajectory/zone-based people counting rather than frame-level detection alone.
- The paper reports feasibility of edge AI for real-time passenger monitoring, but also emphasizes resource constraints and the need to balance FPS, accuracy, and tracking reliability.

## Limitations stated by authors

- Detection accuracy decreases in low-light or night/dim station conditions.
- High-density scenes and simultaneous movement can cause occlusions and misdetections.
- Camera placement, extreme angles, and obstructions strongly affect detection quality.
- The implemented Euclidean-distance tracker is lightweight but may struggle with ID switches when individuals move close together; the authors suggest future comparison with DeepSORT.
- Further optimization with ONNX/TensorRT is discussed as future work; not all proposed optimization routes were implemented in the present study.

## Limitations inferred for this project

- The study is domain-specific to tram stations and public-transport footage; it cannot by itself prove generalization to all public spaces.
- The dataset is not publicly released in the article, so independent reproducibility and benchmark comparison are limited.
- Counting relies on stable detections and simple centroid association; severe occlusion, re-entry, track fragmentation, or ID switches can still create double counts or missed counts.
- The paper reports counting-oriented accuracy but does not provide standard MOT metrics such as HOTA, IDF1, MOTA, or ID switches for the tracker.
- The pipeline is not density-map crowd counting and should not be cited as evidence for density-map MAE/RMSE performance.

## Exact claims allowed in draft

- “Diaz-Santos et al. (2025) implemented a YOLO-based detection, lightweight tracking, and ROI/line-crossing people-counting system for tram-station passenger-flow analysis on Jetson Nano.”
- “In their official table, YOLOv5s was selected as the best trade-off among tested YOLO variants, reporting 0.9685 accuracy and 2.1041 s inference time under the stated Jetson Nano evaluation.”
- “The study supports the need to evaluate both count correctness and edge constraints when designing real-time people-counting systems.”
- “The paper’s own limitations include low-light degradation, high-density occlusion, and sensitivity to camera placement.”

## Claims NOT allowed

- Do not claim this paper proves YOLOv5s is universally best for people counting.
- Do not claim the system uses DeepSORT as the implemented tracker; the implementation uses Euclidean-distance tracking, while DeepSORT is discussed as an alternative/future option.
- Do not cite the 0.9685 value as mAP, HOTA, IDF1, or MOT accuracy; it is the paper’s counting/detection accuracy metric.
- Do not claim robust performance in dense crowds, nighttime scenes, or arbitrary public spaces beyond the tested tram-station conditions.
- Do not use this paper as density-map crowd-counting evidence.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 1: people counting in public/public-transport context.
- Section 5: counting logic based on ROI, line/zone crossing, and ID state.
- Section 6: edge/deployment constraints and runtime/accuracy trade-off.
- Section 7: gap synthesis for detector/tracker/counting integration.

## Notes for citation auditor

- Full text was accessible on the official MDPI page on 2026-05-25 WIB.
- `references/references.bib` contains `@article{S010,... DOI={10.3390/computers14110476} ...}`.
- Audit risk: MDPI source should be paired with non-MDPI anchors for SOTA claims. Use S010 primarily as applied edge/counting evidence, not as a sole SOTA authority.
