# Full-Text Note — S004 DETRs Beat YOLOs on Real-time Object Detection / RT-DETR

## Source identity

- Source ID: S004
- Title: DETRs Beat YOLOs on Real-time Object Detection
- Common method name: RT-DETR / Real-Time DEtection TRansformer
- Authors: Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang, Yi Liu, Jie Chen
- Year: 2024 CVPR proceedings; arXiv source is `2304.08069`.
- URL/DOI/arXiv: https://openaccess.thecvf.com/content/CVPR2024/html/Zhao_DETRs_Beat_YOLOs_on_Real-time_Object_Detection_CVPR_2024_paper.html ; PDF: https://openaccess.thecvf.com/content/CVPR2024/papers/Zhao_DETRs_Beat_YOLOs_on_Real-time_Object_Detection_CVPR_2024_paper.pdf ; supplemental: https://openaccess.thecvf.com/content/CVPR2024/supplemental/Zhao_DETRs_Beat_YOLOs_CVPR_2024_supplemental.pdf ; arXiv: http://arxiv.org/abs/2304.08069
- Access date: 2026-05-24 UTC
- Venue/source type: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024, pp. 16965–16974; official CVF Open Access paper and supplement.
- Indexed/peer-reviewed status: peer-reviewed CVPR 2024 paper via official CVF page; final version also available on IEEE Xplore according to CVF notice.

## Why this source matters

RT-DETR is a peer-reviewed CVPR 2024 anchor showing that end-to-end, NMS-free DETR-style detectors can be adapted to real-time object detection. It is important for the proposal because it supports the broader detector trend beyond YOLO: reducing or eliminating NMS and measuring true end-to-end inference speed. The paper also provides a useful contrast to YOLOv10: both address real-time detection, but RT-DETR does so through transformer-based set prediction rather than a YOLO training-head redesign.

## Problem addressed

- The paper states that YOLO detectors are popular for real-time object detection but their speed and accuracy are negatively affected by NMS.
- It argues that NMS slows inference, introduces confidence and IoU threshold hyperparameters, and can make speed/accuracy unstable across scenarios.
- DETR-like end-to-end detectors remove NMS, but prior DETRs have high computational cost and therefore had not fully exploited the speed advantage of NMS-free inference.
- Target problem: build a real-time end-to-end detector that preserves DETR’s NMS-free set prediction while reducing computational cost and improving query quality.

## Method summary

- **RT-DETR architecture:** backbone + efficient hybrid encoder + transformer decoder with auxiliary prediction heads. The last three backbone stages `{S3, S4, S5}` are fed to the encoder, then selected encoder features initialize object queries for the decoder.
- **Efficient hybrid encoder:** decouples intra-scale feature interaction and cross-scale feature fusion. The encoder uses Attention-based Intra-scale Feature Interaction (AIFI), applied only to high-level S5 features, and CNN-based Cross-scale Feature Fusion (CCFF) for multi-scale fusion.
- **Computational motivation:** the paper identifies the multi-scale transformer encoder as a bottleneck; it states that multi-scale feature sequence length makes encoder interaction expensive, and that lower-level feature self-attention is not required for their best trade-off.
- **Uncertainty-minimal query selection:** instead of selecting encoder features only by classification confidence, the method models feature quality as jointly related to classification and localization. It defines uncertainty as the discrepancy between localization and classification distributions and incorporates uncertainty into optimization to provide higher-quality initial decoder queries.
- **Flexible speed tuning:** because RT-DETR uses a multi-layer decoder, the number of decoder layers used at inference can be reduced to trade small AP loss for lower latency without retraining.
- **Scaling:** the supplement describes lighter scaled RT-DETRs using ResNet50/34/18 and scaled encoder/decoder settings for different real-time scenarios.

## Dataset / evaluation protocol

- Main benchmark: COCO train2017 for training and COCO val2017 for validation.
- Supplemental protocol: standard COCO metrics are reported; RT-DETR uses ResNet backbones pretrained on ImageNet. Final reported results use a 6× configuration, while ablations use 1× in parts of the paper.
- Optimizer/training: supplement states AdamW, four NVIDIA Tesla V100 GPUs, batch size 16, EMA decay 0.9999, and augmentations including random color distortion, expand, crop, flip, and resize.
- Large-scale pretraining: supplement reports pretraining on Objects365 for 12 epochs, then fine-tuning on COCO; R18 is fine-tuned for 60 epochs, R50/R101 for 24 epochs.
- End-to-end speed benchmark: COCO val2017, T4 GPU with TensorRT FP16, input size 640×640 for RT-DETR and YOLO detectors; YOLO detector speed uses official pretrained models and includes TensorRT EfficientNMS according to the paper’s proposed end-to-end benchmark; I/O and MemoryCopy are excluded.
- The paper also compares against DETR variants; speed for most non-real-time DETRs is not tested except DINO-Deformable-DETR.
- People-counting, MOT, line-crossing, ROI/zone counting, and local public-space CCTV evaluation: not evaluated.

## Metrics reported

- Accuracy: COCO AP, AP50, AP75, APS, APM, APL.
- Efficiency: FPS with batch size 1 on T4 TensorRT FP16, number of parameters, GFLOPs, latency in ms for ablations.
- NMS analysis: AP and EfficientNMS kernel execution time under different IoU and confidence thresholds.
- Query-selection analysis: proportion of selected features with classification score > 0.5 and both classification/IoU scores > 0.5.
- No tracking metrics (HOTA, IDF1, MOTA), counting error, trajectory consistency, or deployment memory/power metrics are reported.

## Findings safe to cite

- The paper reports that NMS execution time increases when confidence threshold decreases or IoU threshold increases, and that inappropriate thresholds can lead to false positives or false negatives.
- It establishes an end-to-end speed benchmark on COCO val2017 that includes NMS for YOLO detectors, rather than reporting only model-forward speed.
- Main result: RT-DETR-R50 achieves 53.1% AP on COCO val2017 and 108 FPS on T4 GPU; RT-DETR-R101 achieves 54.3% AP and 74 FPS.
- The paper reports that RT-DETR-R50 improves over DINO-Deformable-DETR-R50 by 2.2 AP and by about 21× in FPS (108 FPS vs 5 FPS) under the stated comparison.
- After Objects365 pretraining, RT-DETR-R50/R101 achieves 55.3%/56.2% AP; supplement also reports RT-DETR-R18 improves by 2.7 AP after pretraining/fine-tuning.
- Ablation: the efficient hybrid encoder variant improves the speed-accuracy trade-off; Table 3 reports variant E at 47.9 AP and 9.3 ms latency in the 1× ablation setting.
- Ablation: uncertainty-minimal query selection improves RT-DETR-R50 1× from 47.9 AP to 48.7 AP.
- Decoder tuning: using the 5th decoder layer in a 6-layer RT-DETR-R50 loses only 0.1 AP while reducing latency from 9.3 ms to 8.8 ms in the reported ablation.

## Limitations stated by authors

- The paper includes an explicit “Limitation and Discussion” section.
- Stated limitation: RT-DETR shares a limitation with other DETRs—performance on small objects remains inferior to strong real-time detectors.
- The authors state that RT-DETR-R50 is 0.5 AP lower than the highest small-object AP (`APS`) among L-model real-time detectors, and RT-DETR-R101 is 0.9 AP lower than the highest `APS` among X-model real-time detectors.
- Future direction stated: address the small-object limitation; discussion also suggests distilling lightweight RT-DETR from high-accuracy large DETR models.

## Limitations inferred for this project

- RT-DETR is a detector, not a complete people-counting system; it does not maintain identities, infer trajectories, or implement ROI/zone/line-crossing counting logic.
- Small-object limitation is relevant to CCTV people counting, where people may appear small, partially occluded, or densely packed.
- Reported speed is on T4 GPU with TensorRT FP16 and does not prove performance on low-end edge hardware or CPU.
- COCO object detection metrics do not verify counting accuracy, ID persistence, double-count prevention, or robustness to local public-space video conditions.
- Transformer-based components may still be heavier than lightweight SORT/YOLO-style alternatives on constrained devices; exact cost for the proposed deployment is not verified.

## Exact claims allowed in draft

- “RT-DETR is a CVPR 2024 peer-reviewed example of a real-time, end-to-end, NMS-free object detector.”
- “The RT-DETR paper argues that NMS affects both speed and accuracy in YOLO detectors because NMS time and results depend on confidence and IoU thresholds.”
- “RT-DETR reduces DETR computational cost using an efficient hybrid encoder and improves query initialization with uncertainty-minimal query selection.”
- “RT-DETR reports 53.1 AP / 108 FPS for R50 and 54.3 AP / 74 FPS for R101 on COCO/T4 TensorRT FP16 under its stated benchmark.”
- “For the proposed people-counting research, RT-DETR supports the detector-side feasibility of NMS-free real-time detection, but separate tracking and counting logic remain necessary.”

## Claims NOT allowed

- Do not claim RT-DETR is a people-counting or multi-object tracking method.
- Do not claim RT-DETR solves identity switches, occlusion recovery, or double-counting; these are not evaluated.
- Do not claim RT-DETR is always superior to every YOLO model; the authors themselves state weaker small-object performance than some strong real-time detectors.
- Do not claim the reported FPS applies to Jetson Nano, CPU, mobile, or the project’s target hardware without testing.
- Do not use the Objects365-pretrained AP numbers unless explicitly noting the pretraining/fine-tuning protocol.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 2: “Deteksi manusia real-time dan pergeseran menuju end-to-end/NMS-free detector.”
- Section 6: “Dataset, metrik evaluasi, dan constraint real-time/edge,” for COCO AP/FPS/latency and benchmark protocol discussion.
- Section 7: “Sintesis gap dan posisi penelitian,” as evidence that detector-level real-time advances still need integration with MOT and counting logic.

## Notes for citation auditor

- Citation key in `references/references.bib`: `S004` exists, but appears as an arXiv-style `@article` with year 2023; final bibliography should likely use the CVPR 2024 `@InProceedings{Zhao_2024_CVPR}` entry from the official CVF page if citing the peer-reviewed version.
- Official CVF bibtex lists: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), June 2024, pages 16965–16974.
- Use the CVF HTML/PDF and supplement as primary sources for peer-reviewed extraction; arXiv ID is useful as a secondary identifier.
