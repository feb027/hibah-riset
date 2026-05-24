# Full-Text Note — S011 Vision-Based People Counting and Tracking for Urban Environments

## Source identity

- Source ID: S011
- Title: Vision-Based People Counting and Tracking for Urban Environments
- Authors: Daniyar Nurseitov; Kairat Bostanbekov; Nazgul Toiganbayeva; Aidana Zhalgas; Didar Yedilkhan; Beibut Amirgaliyev
- URL/DOI/arXiv: https://doi.org/10.3390/jimaging12010027 ; official MDPI URL: https://www.mdpi.com/2313-433X/12/1/27
- Access date: 2026-05-25 WIB
- Venue/source type: *Journal of Imaging* 2026, 12(1), Article 27; MDPI journal article; open access.
- Indexed/peer-reviewed status: Peer-reviewed journal article per source ledger; full text read from official MDPI HTML/PDF landing page.
- Citation key in `references/references.bib`: `S011`.

## Why this source matters

This paper is a recent, directly relevant example of a **detection-tracking-counting** pipeline for public-transport/urban environments. It explicitly combines YOLOv8 detection/segmentation, modified DeepSORT tracking, ROI/virtual-line event logic, and event-log generation. It is particularly useful for the proposal’s claim that people counting in transport/public spaces requires tracking and counting rules, not just single-frame detection.

## Problem addressed

The authors address automatic passenger detection, tracking, and entry/exit counting under real-world urban transport conditions, including occlusion, unstable lighting, varying camera views, and privacy requirements. The research question is how detection and tracking algorithms can be optimized to ensure accurate passenger counting in crowded and dynamic public-transport scenarios.

## Method summary

- Approach type: **detection-tracking-counting**, not density-map crowd counting.
- Detection/segmentation: YOLOv8, including person-class detection and segmentation masks, with COCO pre-training and retraining/adaptation on the authors’ transport dataset.
- Tracking: a modified DeepSORT pipeline, supplemented by depth information and an adaptive bilinear filter according to the results section.
- Counting logic: persistent IDs are maintained and per-ID histories are updated relative to virtual lines defining a quadrilateral ROI. The system counts IN/OUT events after complete intersection/crossing of the area and writes annotated videos/event logs.
- Sensors/data modalities: RGB, stereo, IR/depth, RGB-D/LiDAR; depth cues are used for occlusion handling and spatial separation, while RGB data are used for main YOLO training.
- Ethics/privacy: the dataset includes only images where faces are not recognizable; the paper states local/edge processing is used to reduce privacy risks.

## Dataset / evaluation protocol

- Core labeled dataset: 4047 images with 8918 annotated “Person” objects.
- Split: 3293 images / 7322 objects for training and 754 images / 1596 objects for testing; approximately 81/19% by images and 82/18% by annotations.
- Data collection: frames from surveillance cameras inside city buses; additional university corridor data recorded using depth/stereo cameras connected to Jetson Nano; MaixSense A075V and 3D Stereo VR USB camera streams were collected in 10-minute intervals across daytime hours.
- Training: YOLOv8 trained/retrained for 200 epochs; the paper notes signs of overfitting after about the 150th epoch.
- Counting evaluation: a pre-recorded 3-hour video with various movement scenarios; manual actual IN/OUT events compared with algorithm predictions.
- Data availability: data are available on request from the corresponding author; not a fully open public benchmark.

## Metrics reported

- Detection/segmentation metrics in official table: Precision, Recall, mAP@50, mAP@50–95 for bounding boxes and masks.
  - Bounding box: Precision 0.91971; Recall 0.86848; mAP@50 0.93335; mAP@50–95 0.74044.
  - Mask: Precision 0.93538; Recall 0.8526; mAP@50 0.93295; mAP@50–95 0.67564.
- Confusion matrix: person class correctly classified in 92% of cases; 8% assigned to background; background recognized with 100% accuracy.
- Counting accuracy: 140 correct events out of 164 total events = 85%; specifically 70/80 actual inputs and 70/84 outputs correctly identified.
- Additional comparison metrics discussed: Accuracy, MAE, RMSE, X-Accuracy for related occupancy/counting studies; MOTA and IDF1 appear in a comparative table for SORT/DeepSORT/FairMOT, not as the paper’s own tracking benchmark.
- Runtime/deployment: tests on Jetson Nano and NVIDIA RTX5000 with and without TensorRT optimization; exact FPS values should be taken only from Figure 14 if manually verified, not inferred from prose.

## Findings safe to cite

- S011 proposes and evaluates a unified people-counting architecture that integrates YOLOv8 detection/segmentation, modified DeepSORT tracking, virtual-line/ROI counting, and event-log generation.
- The paper’s dataset contains 4047 images and 8918 annotated person objects, collected for urban/public-transport conditions.
- The authors report 92% detection/classification accuracy for the person class and 85% counting accuracy on a 3-hour video, with 140 correct IN/OUT events out of 164.
- The paper identifies common practical gaps: dense crowd/occlusion robustness, lighting and camera-orientation sensitivity, insufficiently diverse datasets, and the need for integrated detection-tracking-counting frameworks suitable for edge/peripheral devices.
- The paper supports the distinction that trajectory/ROI people counting needs persistent IDs and event logic; it is not a density-map MAE/RMSE crowd-estimation paper.

## Limitations stated by authors

- Existing systems and the proposed approach remain challenged by dense crowding/occlusions, undercounting or double-counting, illumination changes, and camera orientation variation.
- The ethical-model discussion notes the current implementation does not yet cover a wide range of environmental conditions or multimodal sensor inputs.
- Future work is planned for more complex/nighttime/crowded scenarios, multicamera integration, and embedded-device adaptation.
- Data are available on request only, limiting direct reproducibility.
- Training shows signs of overfitting after about 150 epochs.

## Limitations inferred for this project

- The dataset is proprietary/on-request and transport-specific, so generalization to other public spaces is not guaranteed.
- Counting accuracy is evaluated on one 3-hour video/event set; broader multi-camera, multi-site validation is still needed.
- The paper reports MOTA/IDF1 for related algorithms in a comparison table, but it does not provide a full MOT benchmark for its own modified DeepSORT system.
- Counting depends on ID stability; the paper itself notes that trajectory-crossing accuracy depends on stable identifiers and reliable tracking.
- Because the method is detection/tracking based, it should not be used as evidence for density-map crowd-counting accuracy on datasets like ShanghaiTech or UCF-QNRF.

## Exact claims allowed in draft

- “Nurseitov et al. (2026) proposed a YOLOv8 + modified DeepSORT pipeline that counts passenger IN/OUT events using persistent IDs and ROI/virtual-line crossing rules.”
- “Their proprietary urban/public-transport dataset contains 4047 images and 8918 annotated person objects, with 3293 images for training and 754 for testing.”
- “The paper reports 85% counting accuracy on a 3-hour video, corresponding to 140 correct events out of 164.”
- “The authors identify occlusion, lighting variation, dataset diversity, and integrated detection-tracking-counting deployment as unresolved challenges.”

## Claims NOT allowed

- Do not claim this is a density-map crowd-counting method.
- Do not claim the reported MOTA/IDF1 values are the authors’ own tracker results; they are comparative values for other methods in the related/comparison table.
- Do not claim the dataset is publicly downloadable; the paper says data are available on request.
- Do not claim the method solves double-counting generally; its accuracy still depends on stable tracking identifiers.
- Do not cite exact FPS from Figure 14 unless separately extracted/verified from the figure or source table.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 1: people counting in public/transport environments.
- Section 3: tracking, occlusion, and identity consistency in crowded scenes.
- Section 5: counting logic based on ROI, line/zone crossing, trajectory validation, and ID memory.
- Section 6: dataset, metrics, and edge/real-time deployment constraints.
- Section 7: gap synthesis for integrating detection, tracking, and counting logic.

## Notes for citation auditor

- Full text was accessible on the official MDPI page on 2026-05-25 WIB.
- `references/references.bib` contains `@article{S011,... DOI={10.3390/jimaging12010027} ...}`.
- Audit risk: MDPI article; support major SOTA claims with additional non-MDPI tracking/counting sources. Use S011 mainly for recent applied detection-tracking-counting evidence and counting-logic framing.
