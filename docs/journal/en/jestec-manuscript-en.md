# RANCAGE: Real-Time Adaptive Neural Counting with Associative Group Estimation

> **Source**: translation of `JESTEC Pengembangan Model Rekognisi Objek untuk Real-Time People Counting System Berbasis Deep Learning.docx` (Indonesian master, frozen).
> **Target venue rules applied**: JESTEC — English (UK), 10–15 pages, references numbered by first appearance, `Fig. 1` caption below, `Table 1` caption above, `Eq. (1)`.
> **Not yet done here (do before submission)**: reference entries reformatted to JESTEC style; AI-use declaration inserted immediately before References; 3 equations re-inserted with the Word Equation Editor (marked below); Nomenclature checked against final symbol list.

---

## Abstract

Managing public spaces such as railway stations, campuses and shopping centres requires accurate, real-time information on how many people are present, both for capacity planning and for safety. Manual monitoring struggles to stay consistent as the number of objects grows. Video-based people counting systems are usually assessed on detection performance or on the quality of tracker association, while the contribution of those two components to the final count has rarely been evaluated in an integrated way. This study develops and validates RANCAGE, a real-time people counting pipeline that combines an NMS-free detector (YOLO26), four multi-object tracker variants (OC-SORT, Deep-OC-SORT, DiffMOT and LightTrack-ReID), and trajectory-based counting logic built on polygon RoIs and an ID state machine. Evaluation uses CrowdHuman for detection and MOT20 together with DanceTrack, covering 29 sequences, for tracking and counting. YOLO26s reaches mAP@0.5:0.95 of 0.4974, the best detection performance among the four architectures tested. In tracking, DiffMOT gives the strongest association, with HOTA 44.37/39.05 and IDF1 53.86/43.39 on MOT20/DanceTrack, while Deep-OC-SORT is selected as the main tracker because it balances accuracy against computational cost. At the counting layer, a state machine with cooldown lowers the error from 88.7–155.1% under naive line crossing to 13.08–16.71% on the two best tracker paths, at an added latency of only 0.11 ms within a 24.61 ms end-to-end total, equivalent to 40.6 FPS on an RTX 4090. Trajectory validation and identity state memory therefore matter for counting accuracy without costing real-time feasibility. The study claims no novelty in the basic concept of line/RoI counting; it measures how far that concept holds within a controlled experimental configuration.

**Keywords:** Multi-object tracking, Occlusion handling, People counting, Trajectory validation, YOLO

---

## 1. Introduction

Managing public spaces now depends on information that is fast, accurate and refreshed in real time [1]. Such information underpins capacity management, safety and data-driven decisions. Manual monitoring through surveillance cameras in places like railway stations, campuses or shopping centres has limits. It leans entirely on an operator, which makes consistency hard to hold once the number of objects grows. Work on people counting and smart surveillance shows the requirement is not merely to detect that a person appears in a frame; the system must also preserve identity and follow how objects move between frames so that inflow and outflow can be recovered consistently [2].

Part of the difficulty is that the visual characteristics of public spaces keep changing. Cameras sit far away, bodies appear small or only partly visible, lighting shifts, and people stand close together. A system that only detects people within a single frame can therefore produce inconsistent counts: the same person is detected again after occlusion, IDs are swapped when two paths run near each other, and objects move back and forth around the counting line. The crowd counting and MOT literature confirms that occlusion, perspective variation, non-linear motion, missed detections and identity switches directly affect the reliability of video-based systems [3][4].

Current studies show people counting developing along several paradigms with distinct characteristics. Density-map crowd counting is useful for estimating total crowd size, but it does not always provide the identity, trajectory direction or object state memory needed to count entries and exits per zone [5][6]. The detection-tracking-counting approach, by contrast, detects individuals, maintains identity across frames, and then counts against a region of interest (RoI), a line or a zone [2]. Because this study focuses on counting from individual trajectories, the detection-tracking-counting approach is adopted, with detection, tracking and counting logic treated as connected components.

Even though real-time detectors keep improving, gains on benchmark metrics such as mAP, HOTA and IDF1 do not necessarily translate into accurate counts under real conditions when counting logic is developed separately from detection and tracking. The consistency of the count is worth evaluating from the earliest prototype stage, before the system moves further towards deployment. Against that need, this study develops RANCAGE (Real-Time Adaptive Neural Counting with Associative Group Estimation), a real-time people counting pipeline that integrates object detection, MOT and trajectory-based counting logic. The system uses a YOLO-based detector with YOLO26 as the implementation candidate, and evaluates four trackers: OC-SORT [4], DiffMOT [7], Deep-OC-SORT [8] and LightTrack [9].

Three problems are addressed here: the ability of trajectory-based counting to suppress over-counting caused by unstable identity; the choice of the most suitable tracker under equivalent detection conditions; and the contribution of counting logic to pipeline latency. On that basis, the study develops and validates a real-time people counting pipeline that integrates an NMS-free detector, MOT and trajectory-based counting logic on public benchmarks with ground truth.

The contribution lies in the design of a counting pipeline that combines trajectory and identity information with spatial rules and object state memory. The pipeline is evaluated by comparing four trackers on identical detector output, by a sensitivity analysis of cooldown and confidence against counting error on MOT20 [10] and DanceTrack [11], and by an end-to-end latency decomposition across two device classes. The study does not claim novelty in the basic concept of line/RoI counting; it focuses on measuring effectiveness, and the limits of that effectiveness, in a controlled configuration.

The manuscript has five sections. Section 1 covers the introduction and research objectives. Section 2 reviews related work on people counting, detection, tracking and counting logic. Section 3 describes the methods together with the evaluation scenarios. Section 4 presents the experimental results and discussion, and Section 5 gives the conclusions and directions for further work.

## 2. Related Works

The evolution of YOLO shows gains in efficiency, inference speed and ease of deployment [12], with a trend towards NMS-free detectors that reduce post-processing cost. YOLOv10 introduces consistent dual assignments, aligning the one-to-many and one-to-one processes so inference can run on a single head without NMS [13]. Beyond the YOLO line, transformer-based architectures have appeared, including RT-DETR [14] and RF-DETR [15], along with derivatives such as D-FINE [16] and DEIM [17] that push design efficiency further. These transformer architectures generally carry higher computational complexity than YOLO, because their encoder-decoder structure and attention mechanism are heavier than a single-stage convolutional backbone. In metric terms, YOLOv10 [13] is reported to reach 54.4 AP at 10.70 ms latency, while RT-DETR [14] reaches 53.1 AP at 108 FPS; RF-DETR [15], D-FINE [16] and DEIM [17] report improved accuracy-latency efficiency within the transformer line.

Benchmark accuracy such as COCO AP, FLOPs and latency does not yet capture counting accuracy under occlusion or missed detection [2]. On edge devices, evaluation also needs to account for power and RAM: YOLOv7 on a Raspberry Pi 4B needs 16.4 s per inference, whereas YOLOv7-tiny INT8 on a Jetson Orin Nano needs only 0.008 s at mAP 0.936 [18]. LCDnet, with 0.05M parameters, also holds its accuracy on a Jetson Nano through distillation from CSRNet [19]. The feasibility of real-time detection, in other words, cannot be judged from benchmark accuracy alone; target-device efficiency counts as well.

People counting in public spaces needs real-time information on count, flow, density and individual movement. A quadrilateral RoI with virtual-line events and persistent IDs reaches 85% counting accuracy, while cascaded detection with a Kalman filter reaches up to 98.42% under challenging visual conditions [2][20]. Passenger flow work based on YOLO and edge AI likewise shows that directional line crossing requires per-ID position history across frames [21]. Approaches to people counting divide into density-map crowd counting and detection-tracking-counting: density maps work well in dense crowds but preserve neither identity nor trajectory direction [5][6], whereas detection-tracking-counting maintains IDs across frames and counts individuals relative to a line or zone [2]. The second approach matches the cross-zone movement and ID state memory required here.

MOT links detections across frames, so a failure to hold identity can produce double counting, lost counts or wrong direction [2]. OC-SORT improves on SORT through ORU, OCM and OCR and reaches over 700 FPS [4], while DiffMOT targets non-linear motion and reaches HOTA 62.3 / IDF1 63.0 at 22.7 FPS on DanceTrack with an RTX 3090 [7]. DiffMOT operates at the level of identity, unlike CrowdDiff, which applies diffusion to density maps without individual identity [22]. Even so, 22.7 FPS on an RTX 3090 does not guarantee edge performance, so fallbacks such as OC-SORT remain relevant. As a hybrid, Deep-OC-SORT extends OC-SORT with a deep-learning appearance embedding updated by exponential moving average [8], so association draws on motion information and on visual similarity between detections; it keeps the efficiency of OC-SORT while improving identity consistency without the complexity of a diffusion model.

The 2024–2026 trend moves towards confidence-aware and occlusion-aware association, as shown by Sentinel [23], LightTrack-ReID [9], TrackTrack [24], MOTIP [25], OcclusionTrack [3] and DragonTrack [26]. Tracking evaluation uses datasets such as MOT20, DanceTrack and CrowdHuman, with HOTA and IDF1 as metrics: MOT20 provides high-density sequences [10], DanceTrack stresses association under diverse motion and uniform appearance [11], and CrowdHuman provides roughly 470 thousand human instances annotated with full-body, visible-region and head boxes [27]. HOTA balances detection quality against identity association, while IDF1 measures identity consistency through bipartite matching [28].

Successful tracking does not always produce accurate counting, however. ID stability and per-ID position history affect counting accuracy [2][21], yet earlier studies do not detail how trajectory validation is designed. Counting logic therefore needs to be an explicit component, through polygon RoIs/zones, line crossing, transition validation and ID state memory, to reduce double counting in an end-to-end system.

## 3. Method

This section describes the design of RANCAGE, a real-time people counting pipeline that integrates object detection, MOT and trajectory-based counting logic into one end-to-end architecture. The design is presented from the overall system architecture, through the configuration of the detection and tracking components and the trajectory-based counting mechanism, to the datasets and evaluation scenarios used. Each stage is built so that it can be tested in isolation or end-to-end, which makes the effect of each component on counting accuracy and latency measurable under controlled conditions.

### 3.1 System Architecture

RANCAGE has five main processing stages, as shown in Fig. 1. Video is processed by YOLO26 with an NMS-free head to produce bounding boxes and confidence scores [13]. The detection output is then passed to two tracking paths: Deep-OC-SORT as the main path, combining Kalman observation-centric estimation with deep-feature re-identification, and OC-SORT as a lightweight path for constrained resources [4]. The tracklets are evaluated by the counting logic, which uses polygon RoIs and virtual lines to validate the direction of movement. ID State Memory holds the status of every identity so that double counting from occlusion or back-and-forth movement is prevented [21].

**Fig. 1.** RANCAGE system architecture.

### 3.2 Object Detection and Multi-Object Tracking

The detection component uses the Ultralytics YOLO family, comparing NMS-free architectures (YOLOv10 and YOLO26) against an NMS-based architecture (YOLOv11). All models are fine-tuned on CrowdHuman [27] using amodal fbox annotations. In YOLOv10 the consistent dual label assignment aligns the one-to-many and one-to-one processes, so inference runs on a single head without NMS [13]. To keep the comparison consistent, all trackers are evaluated on the same YOLO26 detection output.

Four trackers were chosen to represent different tracking characteristics. OC-SORT uses an observation-centric mechanism to improve robustness against occlusion through Re-Update, Momentum and Recovery, with a lightweight geometric approach [4]. DiffMOT uses a diffusion-based motion predictor for non-linear movement patterns and includes appearance-based Re-ID, at a higher GPU cost [7]. Deep-OC-SORT combines observation-centric motion estimation with a deep-learning appearance embedding updated by exponential moving average, so association draws on motion information and visual similarity together [8]. LightTrack-ReID is designed as a lightweight approach, with a MobileNetV3-Small appearance encoder, transformer-based similarity scoring, feature memory for occlusion, and adaptive IoU-appearance weighting [9].

Every tracker outputs in tlwh format with a standardised track_id, so counting logic does not depend on a particular implementation. Key parameters, including threshold, IoU, min-hits and max-age, were unified for the experiment. Because the original publications used different detectors and protocols, all trackers here run on YOLO26 detection to give a more controlled comparison; the absolute results in Section 4 therefore do not directly represent the figures reported in the original studies.

### 3.3 Trajectory-Based Counting

The counting component of RANCAGE evaluates the trajectory of each ID against the RoI and virtual lines, rather than counting objects per frame. The approach adopts the virtual-line RoI concept used in people counting [29]. Two models are compared. Model A (naive line crossing) records an object when its trajectory crosses the virtual line with no state memory, which leaves it vulnerable to spatial jitter and tracking noise that can cause double counting or missed counts [30]. Model B addresses this through RoI validation, crossing detection and an ID state machine. Only centroids inside the RoI polygon are processed. A crossing is determined from the trajectory segment between the last two points, *p*<sub>1</sub> = (*x*<sub>1</sub>, *y*<sub>1</sub>) and *p*<sub>2</sub> = (*x*<sub>2</sub>, *y*<sub>2</sub>), against the virtual line segment *q*<sub>1</sub> = (*x*<sub>q1</sub>, *y*<sub>q1</sub>) and *q*<sub>2</sub> = (*x*<sub>q2</sub>, *y*<sub>q2</sub>). Intersection is tested with the counterclockwise (CCW) test for line segments [31]:

<!-- Eq. (1): reproduce with Word Equation Editor (OMML extracted from master docx) -->
Eq. (1)  *CCW*(*A*, *B*, *C*) = (*B*<sub>x</sub> − *A*<sub>x</sub>)(*C*<sub>y</sub> − *A*<sub>y</sub>) − (*B*<sub>y</sub> − *A*<sub>y</sub>)(*C*<sub>x</sub> − *A*<sub>x</sub>)

The two segments intersect when the CCW values show a sign change on each segment. Crossing direction is determined with the cross product:

<!-- Eq. (2): reproduce with Word Equation Editor -->
Eq. (2)  *D* = *v*<sub>line,x</sub> · *v*<sub>move,y</sub> − *v*<sub>line,y</sub> · *v*<sub>move,x</sub>

*D* > 0 indicates the IN direction and *D* < 0 the OUT direction. Direction depends on the order of the two points defining the virtual line, which is fixed once in the configuration file and applied consistently across all sequences. The counting layer tracks the status of each identity through two operational states, TRACKING and COOLDOWN. When a trajectory crosses the virtual line, the system emits a count and puts that identity into COOLDOWN for 30 frames, during which it cannot trigger another count. Once the cooldown ends, the identity can be counted again on the next crossing. The mechanism therefore guarantees one count per identity within each cooldown window, not one count for the whole session. Although RoI filtering is available in the implementation, it was not enabled in the experimental configuration.

### 3.4 Dataset, Experimental Setup and Evaluation Metrics

Three public datasets are used, according to the characteristics and purpose of each evaluation. CrowdHuman evaluates human detection on static images without temporal identity information [27]. MOT20 evaluates tracking and counting under high-density crowd conditions [10], while DanceTrack [11] tests tracker robustness to non-linear movement and to objects with relatively uniform appearance.

Counting error is reported with two metrics, because the two can disagree. Per-sequence error is the mean relative difference over sequences, as in Eq. (3), which makes it more sensitive to sequences with few objects and lets it reflect error variation between individual sequences. Aggregate error uses the difference between total predictions and total ground truth, as in Eq. (4), which better captures the overall bias of the system; a negative value indicates under-counting. The counting ground truth is obtained by applying the same counting logic to the ground-truth trajectories. These metrics therefore measure the sensitivity of the counting logic to imperfect trajectories, not the true number of people at the site.

<!-- Eq. (3) and Eq. (4): reproduce with Word Equation Editor -->
Eq. (3)  (*P*<sub>i</sub> − *G*<sub>i</sub>) / *G*<sub>i</sub>
Eq. (4)  (Σ*P*<sub>i</sub> − Σ*G*<sub>i</sub>) / Σ*G*<sub>i</sub>

The system evaluation has four main scenarios (S). S1 evaluates detector performance in terms of accuracy and latency, and compares zero-shot against fine-tuned configurations. S2 compares trackers using the TrackEval framework with HOTA, IDF1, MOTA and ID switch on identical detection output. S3 evaluates the effect of the counting logic by comparing Model A and Model B, and by a sensitivity analysis of cooldown and confidence threshold. S4 evaluates end-to-end performance through FPS and tail latency at P90, P95 and P99 on an RTX 4090 server GPU and an AMD RX 6600 edge device with DirectML. The system counts as meeting real-time requirements when it sustains at least 30 FPS.

## 4. Results and Discussion

### 4.1 Object Detection Results

Four detection models — YOLO26n, YOLO26s, YOLOv10n and YOLOv11n — were fine-tuned on CrowdHuman with identical training settings. Evaluation used the 4,370-image validation set with 103,115 full-body annotation boxes. CrowdHuman carries no temporal information, so this section concentrates on detection performance.

#### 4.1.1 Detection accuracy

Table 1 shows the fine-tuning results for the four architectures by model tier. In the nano tier, YOLOv11n leads marginally on mAP@0.5 (0.7855 against 0.7814) but trails YOLO26n on mAP@0.5:0.95 (0.4463 against 0.4497). YOLO26n is also the lightest in that tier, at 2.50 million parameters and 5.8 GFLOPs, against 2.59 million and 6.4 G for YOLOv11n and 2.71 million and 8.4 G for YOLOv10n. YOLO26s sits in the tier above, with 9.95 million parameters and 22.5 GFLOPs, and is reported as the extended configuration when accuracy is the priority.

YOLO26s was set as the operational configuration on GPU hardware, while YOLO26n is reserved for resource-constrained devices. YOLOv10n and YOLOv11n were not carried forward because they offer no equivalent scale path, and YOLOv11s was not fine-tuned here, so the s-tier comparison uses the vendor benchmark (48.6 against 47.0 AP).

**Table 1.** Fine-tuning results of four YOLO architectures

| Architecture | Tier | NMS-free | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | Params (million) | FLOPs (G) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| YOLO26n | n | yes | 0.8230 | 0.6888 | 0.7814 | 0.4497 | 2.50 | 5.8 |
| YOLOv10n | n | yes | 0.8212 | 0.6892 | 0.7826 | 0.4521 | 2.71 | 8.4 |
| YOLOv11n | n | no | 0.8352 | 0.6965 | 0.7855 | 0.4463 | 2.59 | 6.4 |
| YOLO26s | s | yes | 0.8480 | 0.7455 | 0.8266 | 0.4974 | 9.95 | 22.5 |

Under the official CrowdHuman protocol shown in Table 2, YOLO26s again gives the best results, with MR⁻² 0.7574 and maximum recall 0.9262. That recall ceiling shows some objects remain undetected, which can produce an under-count the tracker cannot correct. Objects cut by the frame edge also show a larger drop in recall and AP than intact objects. These findings support placing the RoI and counting line away from the frame edge.

**Table 2.** Evaluation under the official CrowdHuman protocol

| Architecture | MR⁻² | AP@0.5 | Maximum recall |
| --- | --- | --- | --- |
| YOLO26n | 0.7792 | 0.7881 | 0.9124 |
| YOLO26s | 0.7574 | 0.8283 | 0.9262 |
| YOLOv10n | 0.7764 | 0.7898 | 0.9146 |
| YOLOv11n | 0.7778 | 0.7882 | 0.9000 |

#### 4.1.2 Computational efficiency

The advantage of the NMS-free architectures shows up in post-processing latency rather than in accuracy. On the RTX 4090 the NMS-free models need 0.164–0.170 ms of post-processing, below the 0.491 ms of YOLOv11n, as Table 3 shows.

**Table 3.** Inference and post-processing latency on the RTX 4090

| Architecture | Inference (ms) | Post-processing (ms) | Post-processing share |
| --- | --- | --- | --- |
| YOLO26n | 2.554 | 0.164 | 6.0% |
| YOLO26s | 2.695 | 0.170 | 6.0% |
| YOLOv10n | 2.129 | 0.167 | 7.3% |
| YOLOv11n | 2.142 | 0.491 | 18.7% |

On CPU with ONNX Runtime, shown in Table 4, YOLO26n is the fastest model at 10.28 ms, equivalent to 97 FPS. ONNX export yields a 1.73–2.38× speed-up with no measurable change in accuracy, and every model exceeds 30 FPS.

**Table 4.** Latency on CPU with ONNX Runtime

| Architecture | PyTorch CPU (ms) | ONNX CPU total (ms) | Speed-up | Equivalent FPS |
| --- | --- | --- | --- | --- |
| YOLO26n | 22.48 | 10.28 | 2.24× | 97 |
| YOLO26s | 54.50 | 23.15 | 2.38× | 43 |
| YOLOv10n | 25.13 | 12.13 | 2.11× | 82 |
| YOLOv11n | 22.98 | 14.05 | 1.73× | 71 |

On that basis, YOLO26s is chosen when a GPU is available, because it gives the best accuracy, while YOLO26n is used where compute is limited. The remaining tests turn to how well the trackers preserve object identity across frames.

### 4.2 Multi-Object Tracking Results

This section evaluates the tracking layer that links detection boxes across frames into temporal identities. The trackers compared on identical detection — OC-SORT, Deep-OC-SORT, DiffMOT and LightTrack — all run on the same YOLO26s output. Evaluation used TrackEval on MOT20-train and DanceTrack-val. MOT20 is dense: an average of 179 detections per frame, peaking at 272. Under those conditions DiffMOT gives the best results, with HOTA 44.37, MOTA 60.91 and IDF1 53.86, and the lowest IDSW at 6,905. OC-SORT, by contrast, has MOTA 55.98 but produces 14,293 IDSW and 27,646 fragmentations. The results in Table 5 show that high detection accuracy does not guarantee stable identity under occlusion.

**Table 5.** TrackEval results on identical YOLO26 detection

| Benchmark | Tracker | HOTA | MOTA | IDF1 | IDSW | Frag |
| --- | --- | --- | --- | --- | --- | --- |
| MOT20 | OC-SORT | 36.51 | 55.98 | 42.88 | 14,293 | 27,646 |
| MOT20 | Deep-OC-SORT | 36.12 | 54.70 | 42.16 | 11,751 | 29,729 |
| MOT20 | DiffMOT | 44.37 | 60.91 | 53.86 | 6,905 | 15,005 |
| MOT20 | LightTrack | 32.92 | 38.00 | 34.69 | 13,121 | 8,863 |
| DanceTrack | OC-SORT | 28.39 | 71.38 | 26.63 | 6,701 | 6,936 |
| DanceTrack | Deep-OC-SORT | 28.91 | 70.05 | 27.38 | 5,948 | 8,053 |
| DanceTrack | DiffMOT | 39.05 | 70.72 | 43.39 | 2,784 | 6,765 |
| DanceTrack | LightTrack | 22.53 | 32.72 | 18.91 | 6,697 | 4,405 |

Fig. 2 shows that on a single MOT20-02 frame both OC-SORT and DiffMOT track 38 people, while ground truth records 59. The gap falls mainly in the dense crowd area, which means tracker differences are better judged from ID stability over time than from one frame.

Fig. 2. MOT20-02 frame with tracking results for (a) OC-SORT, (b) Deep-OC-SORT, (c) DiffMOT, (d) LightTrack and (e) ground truth.

Taken together, association is what matters under occlusion and non-linear motion. DiffMOT performs best but needs a GPU, behaves as a black box, and carries heavier dependency requirements. Weighing accuracy against efficiency, Deep-OC-SORT is selected as the main tracker, with DiffMOT kept as a quality reference.

### 4.3 People Counting Results

Two approaches are compared across the 29 combined sequences from MOT20-train (4 sequences) and DanceTrack-val (25 sequences): naive line crossing without state memory, and a state machine with debouncing. For reference, the state machine was also tested on ground-truth trajectories.

#### 4.3.1 Aggregate counting accuracy

The results in Fig. 3 show that the state machine adds no error on ideal trajectories, giving 0 error on ground-truth tracks. On tracker output, DiffMOT gives the lowest error at 13.08%, followed by Deep-OC-SORT at 16.71%, OC-SORT at 22.38% and LightTrack at 53.03%. The pattern follows association quality. LightTrack also shows the largest over-count, averaging 57.76 predictions against a GT of 44.62. Deep-OC-SORT tends to count lower but holds 40.6 FPS throughput, which is why it is chosen as the main tracker. The 13.08–16.71% error on the two best paths also includes detection limits, with 7.4–10.0% of objects left undetected.

**Fig. 3.** MAE and mean counting error per tracking path across 29 sequences.

#### 4.3.2 Ablation of the state machine against naive line crossing

Table 6 shows naive line crossing producing 88.7–155.1% error from position jitter around the line, people stopping near the line, and ID switches that trigger repeated events. The state machine with cooldown suppresses that over-counting by holding the status of each ID.

**Table 6.** Counting logic ablation (mean across sequences)

| Model | Characteristic | Mean error | Behaviour |
| --- | --- | --- | --- |
| Naive (no debounce) | Pure line crossing | Mean error 88.7–155.1% depending on tracker path | Severe over-count |
| State machine (CD = 30) | Per-ID state + cooldown | 16.71% | Stable |
| State machine (CD = 15) | Short cooldown | 27.13% | Better suited to fast pedestrian flow |

### 4.4 Ablation and System Analysis

This section tests the sensitivity of two main parameters, debounce cooldown length and confidence threshold, against counting accuracy. The test uses the YOLO26s + Deep-OC-SORT + state machine configuration on the 29 benchmark sequences, and the results set the operational configuration for the end-to-end evaluation.

Fig. 4(a) shows a U-shaped pattern in MAE and counting error against cooldown length. Without debounce (naive), the error reaches 101.99% from false crossings around the counting line. Error falls to the lowest MAE of 6.34 at CD = 30 and the lowest percentage error of 14.64% at CD = 45, then rises again when the cooldown is too long and some trajectories go uncounted. Other trackers show the same pattern with a different optimum.

Fig. 4(b) shows the trade-off between false positives and false negatives against confidence threshold. At low thresholds the error is driven by background noise detections, while thresholds above 0.40 increase under-counting because low-confidence objects go undetected. The lowest error, 1.67%, occurs at a threshold of 0.20, while the 0.25–0.30 range gives more stable performance with throughput above 40 FPS. Threshold changes affect throughput only slightly, from 39.2 to 43.0 FPS. On the basis of both analyses, the end-to-end evaluation uses a cooldown of 30 frames and a confidence threshold of 0.30.

**Fig. 4.** Cooldown sensitivity: (a) MAE and counting error against cooldown length; (b) counting error and throughput against detector confidence threshold.

### 4.5 End-to-End Performance

This section integrates every pipeline stage — detection, Re-ID feature extraction, tracker association and counting logic — to assess readiness for real-time operation. The reference is 30 FPS with a latency budget of 33.3 ms per frame. The test uses the operational configuration from Section 4.4 (cooldown 30 frames, confidence 0.30) on MOT20-02, where density sits at around 34–38 people per frame. Latency is measured in microseconds for each computation stage.

#### 4.5.1 Latency decomposition on the target device

Table 7 shows an end-to-end latency of 24.61 ms, about 40.6 FPS, which stays inside the 33.3 ms budget. The largest contributor is YOLO26 detection at 14.20 ms (57.7%), followed by tracking and Re-ID at 9.45 ms (38.4%). Preprocessing and counting logic need only 0.85 ms and 0.11 ms. Computational cost is therefore dominated by detection and tracking, while RoI-based counting logic adds comparatively little latency.

**Table 7.** Pipeline latency breakdown on the RTX 4090

| Pipeline layer | Component | Latency (ms) | Proportion |
| --- | --- | --- | --- |
| Preprocessing | capture, resize 640×640, tensor format | 0.85 | 3.5% |
| Object detection | YOLO26 inference (NMS-free) | 14.20 | 57.7% |
| Tracker & Re-ID | Deep-OC-SORT (crop Re-ID + VDC + ACM) | 9.45 | 38.4% |
| Counting logic | PeopleCounter (state machine + RoI) | 0.11 | 0.4% |
| Total | End-to-end pipeline | 24.61 | 100% |

#### 4.5.2 Performance on resource-constrained devices and latency stability

Fig. 5 compares performance across devices and shows the pipeline latency distribution. The results bring out the difference in throughput and computational load between the edge configuration and the RTX 4090, and show the latency stability against the 33.3 ms real-time target.

**Fig. 5.** End-to-end latency decomposition per device.

### 4.6 Discussion

The evaluation shows that each pipeline layer has a different limiting factor. In detection, model capacity matters more for accuracy than architectural differences, while the NMS-free design mainly improves post-processing efficiency. Detection also leaves a structural under-count of 7.4–10.0%, mostly for objects cut at the frame edge. In tracking, HOTA falling below MOTA shows that identity consistency remains the main obstacle, and strengthening association proved more influential for counting accuracy than improving detection box quality.

In the counting logic, the state machine suppresses over-counting effectively, at an added computational cost of only 0.11 ms per frame: the detection-tracking pipeline moves from 24.50 ms to 24.61 ms end-to-end, a 0.4% increase. Cooldown selection still needs to be matched to object density and movement patterns. End-to-end, the operational configuration reaches 24.61 ms per frame (40.6 FPS) on the RTX 4090, with 95% of frames inside the 33.3 ms budget. On edge devices, OC-SORT is the better fit for holding real time, while Deep-OC-SORT suits GPU hardware when identity consistency is the priority.

These findings are limited by the use of a single seed, by public benchmarks with offline detection, and by device-dependent latency. Overall, people counting performance is determined by how detection, identity, tracking and counting logic align, not by any single component on its own.

## 5. Conclusions

This study developed and validated RANCAGE, a real-time people counting pipeline that integrates detection, multi-object tracking (MOT) and trajectory-based counting in one end-to-end architecture. A state machine with polygon RoI and cooldown suppressed the error of naive line crossing from 88.7–155.1% to 13.08–16.71% on the two best tracker paths. Under identical detection, DiffMOT gave the strongest association, with HOTA 44.37/39.05 and IDF1 53.86/43.39 on MOT20/DanceTrack, while Deep-OC-SORT was selected as the main tracker for its balance of accuracy and efficiency. The counting logic also added only 0.11 ms to the 24.61 ms end-to-end total, or 40.6 FPS on the RTX 4090, with 95% of frames below the 33.3 ms limit.

ID stability and trajectory validation therefore matter for holding counting accuracy without giving up real-time capability. The study claims no novelty in the basic concept of line/RoI counting; it focuses on the quantitative evaluation of how effective that concept is in a controlled configuration. Limitations include the use of offline detection on public benchmarks and a counting ground truth derived from trajectory annotations rather than independent human counts at the site. Further work will deploy RANCAGE on real edge devices such as the Jetson Nano/Orin, using pruning and model quantisation to evaluate the accuracy-latency trade-off under limited resources. Direct testing on CCTV footage with human ground truth, and characterisation of the operational breaking point against object density and extreme visual conditions, are also needed as a basis for more mature deployment readiness.

## Nomenclature

<!-- JESTEC requires this section immediately before References, alphabetical.
     Symbols/abbreviations below are taken from the manuscript body; extend if new ones appear. -->

**Abbreviations**

| Term | Meaning |
| --- | --- |
| ACM | Adaptive Correlation Matrix |
| AP | Average Precision |
| CCW | Counterclockwise |
| COCO | Common Objects in Context |
| FPS | Frames Per Second |
| Frag | Fragmentations |
| GFLOPs | Giga Floating-Point Operations |
| GT | Ground Truth |
| HOTA | Higher Order Tracking Accuracy |
| ID | Identity |
| IDF1 | Identity F1 score |
| IDSW | ID Switches |
| IoU | Intersection over Union |
| MAE | Mean Absolute Error |
| mAP | Mean Average Precision |
| MOT | Multi-Object Tracking |
| MOTA | Multi-Object Tracking Accuracy |
| MR⁻² | Log-Average Miss Rate |
| NMS | Non-Maximum Suppression |
| Re-ID | Re-Identification |
| RoI | Region of Interest |
| VDC | Virtual Detection Confidence |

**Symbols**

| Symbol | Meaning |
| --- | --- |
| *CE* | Counting error |
| *D* | Crossing-direction cross product |
| *CD* | Cooldown length, frames |
| *P*<sub>i</sub> | Predicted count for sequence *i* |
| *G*<sub>i</sub> | Ground-truth count for sequence *i* |
| *p*<sub>1</sub>, *p*<sub>2</sub> | Last two points of the trajectory segment |
| *q*<sub>1</sub>, *q*<sub>2</sub> | Two points defining the virtual line |

## References

*(Carried over unchanged from the Indonesian master. Reference entries still need reformatting to JESTEC style: `Surname, A.B.; and Surname, C.D. (Year). Title. Journal, Vol(Issue), pages.` Several entries are missing venue, volume/pages or year and must be completed before submission.)*

[1] W. Mansouri, M. A. Alohali, H. Alqahtani, and N. Alruwais, "Deep convolutional neural network-based enhanced crowd density monitoring for intelligent urban planning on smart cities," 2025.

[2] D. Nurseitov, K. Bostanbekov, N. Toiganbayeva, A. Zhalgas, and D. Yedilkhan, "Vision-Based People Counting and Tracking for Urban Environments," pp. 1–23, 2026.

[3] Y. Chen, F. Meng, and Z. Chen, "OcclusionTrack: Multi-Object Tracking in Dense Scenes," no. 2, pp. 1–22, 2025.

[4] J. Cao, J. Pang, X. Weng, R. Khirodkar, and K. Kitani, "Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking".

[5] L. Deng, Q. Zhou, S. Wang, J. M. Górriz, and Y. Zhang, "Deep learning in crowd counting: A survey," no. February 2023, pp. 1043–1077, 2024, doi: 10.1049/cit2.12241.

[6] H. F. Elsepae, H. M. El-hoseny, and E. K. I. Hamad, "Deep learning for crowd counting in complex environments: challenges and novel trends," 2026.

[7] W. Lv, Y. Huang, N. Zhang, R. L. Mei, and H. Dan, "DiffMOT: A Real-time Diffusion-based Multiple Object Tracker with Non-linear Prediction," pp. 19321–19330.

[8] G. Maggiolino, A. Ahmad, J. Cao, and K. Kitani, "Deep OC-SORT: Multi-Pedestrian Tracking by Adaptive Re-Identification," Carnegie Mellon University.

[9] S. Baz, J. Khan, P. Zhang, and M. M. Kamal, "LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking," 2026, doi: 10.1371/journal.pone.0342246.

[10] P. Dendorfer et al., "MOT20: A benchmark for multi object tracking in crowded scenes," pp. 1–7.

[11] P. Sun et al., "DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion," pp. 20993–21002.

[12] A. D. Sappa, "A Decade of You Only Look Once (YOLO) for Object Detection: A Review," *IEEE Access*, vol. 13, no. November, pp. 192747–192794, 2025, doi: 10.1109/ACCESS.2025.3630988.

[13] A. Wang et al., "YOLOv10: Real-Time End-to-End Object Detection," no. NeurIPS, pp. 1–28, 2024.

[14] Y. Zhao et al., "DETRs Beat YOLOs on Real-time Object Detection," pp. 16965–16974.

[15] F. W. Yansong Peng, Hebei Li, Peixi Wu, Yueyi Zhang, Xiaoyan Sun, "D-FINE: Redefine Regression Task in DETRs as Fine-grained Distribution Refinement," pp. 1–18, 2024.

[16] S. Huang, Z. Lu, and C. Ap, "DEIM: DETR with Improved Matching for Fast Convergence".

[17] N. P. Isaac Robinson, Peter Robicheaux, Matvei Popov, Deva Ramanan, "RF-DETR: Neural Architecture Search for Real-Time Detection Transformers," pp. 1–24, 2026.

[18] N. Surantha and N. Sutisna, "Key Considerations for Real-Time Object Recognition on Edge Computing Devices," pp. 1–26, 2025.

[19] M. A. Khan, H. Menouar, R. Hamila, and A. Abu-dayya, "Crowd counting at the edge using weighted knowledge distillation," pp. 1–16, 2025.

[20] M. R. Holla and D. S. M. Darshan, "Optimizing accuracy and efficiency in real-time people counting with cascaded object detection," *Int. J. Inf. Technol.*, 2024, doi: 10.1007/s41870-024-02153-w.

[21] S. Diaz-santos and P. Caballero-gil, "Real-Time Passenger Flow Analysis in Tram Stations Using YOLO-Based Computer Vision and Edge AI on Jetson Nano," 2025.

[22] Y. Ranasinghe, N. G. Nair, W. Gedara, C. Bandara, and V. M. Patel, "CrowdDiff: Multi-hypothesis Crowd Density Estimation using Diffusion Models".

[23] H. Yang, S. Park, C. Sim, and S. Jung, "Sentinel for confidence-aware multi-object tracking," pp. 1–18, 2026.

[24] K. Shim, K. Ko, Y. Yang, and C. Kim, "Focusing on Tracks for Online Multi-Object Tracking," pp. 11687–11696.

[25] R. Gao and L. Wang, "Multiple Object Tracking as ID Prediction," pp. 27883–27893.

[26] B. Galoaa, S. Amraee, and S. Ostadabbas, "DragonTrack: Transformer-Enhanced Graphical Multi-Person Tracking in Complex Scenarios," pp. 6373–6382.

[27] S. Shao, Z. Zhao, B. Li, T. Xiao, and G. Yu, "CrowdHuman: A Benchmark for Detecting Human in a Crowd," pp. 1–9.

[28] M. Tracking, E. Ristani, F. Solera, R. Zou, R. Cucchiara, and C. Tomasi, "Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking," vol. 1.

[29] C. Mccarthy, H. Ghaderi, F. Martí, P. Jayaraman, and H. Dia, "Video-based automatic people counting for public transport: On-bus versus," *Computers in Industry*, vol. 164, no. September 2024, p. 104195, 2025, doi: 10.1016/j.compind.2024.104195.

[30] L. Song, L. Han, J. Wang, H. Feng, and R. Ji, "Optimization of Indoor Pedestrian Counting Based on Target Detection and Tracking," pp. 1–20, 2026.

[31] J. O'Rourke, *Computational Geometry in C*, 2nd ed. Cambridge University Press, 1998.
