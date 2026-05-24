# Full-Text Note — S003 YOLOv10: Real-Time End-to-End Object Detection

## Source identity

- Source ID: S003
- Title: YOLOv10: Real-Time End-to-End Object Detection
- Authors: Ao Wang, Hui Chen, Lihao Liu, Kai Chen, Zijia Lin, Jungong Han, Guiguang Ding
- Year/version: 2024; arXiv v2 dated 30 Oct 2024; NeurIPS 2024 poster page lists the paper as a 2024 poster.
- URL/DOI/arXiv: https://arxiv.org/abs/2405.14458 ; https://arxiv.org/pdf/2405.14458 ; https://neurips.cc/virtual/2024/poster/93301
- Access date: 2026-05-24 UTC
- Venue/source type: 38th Conference on Neural Information Processing Systems (NeurIPS 2024); arXiv full text and official NeurIPS poster page.
- Indexed/peer-reviewed status: accepted peer-reviewed NeurIPS 2024 paper per official NeurIPS page; arXiv is the full-text source used for detailed extraction.

## Why this source matters

YOLOv10 is the main peer-reviewed anchor for the proposal's detector discussion because it explicitly targets real-time, end-to-end, NMS-free YOLO-style detection. The paper connects the latency problem of NMS post-processing with architectural redundancy in YOLO detectors, then proposes training and model-design changes to improve the accuracy-latency trade-off. It is therefore safer than YOLO26 vendor/preprint material for claims about the academic trend toward NMS-free/end-to-end real-time detectors.

## Problem addressed

- The paper states that common YOLO detectors use one-to-many label assignment during training, which creates multiple positive predictions per object and makes NMS necessary at inference.
- It argues that NMS slows inference, introduces sensitivity to NMS hyperparameters, and prevents optimal end-to-end deployment.
- It also states that YOLO component design has not been comprehensively inspected from both efficiency and accuracy perspectives, leaving computational redundancy and suboptimal parameter utilization.
- Target problem: improve YOLO's performance-efficiency boundary by addressing both post-processing and model architecture.

## Method summary

- **Consistent dual assignments for NMS-free training:** YOLOv10 adds a one-to-one head alongside the original one-to-many head during training. The one-to-many branch provides richer supervision, while the one-to-one branch is used at inference; the one-to-many head is discarded at inference, so no extra inference cost is added.
- **Consistent matching metric:** the paper aligns the one-to-one and one-to-many branches by using a consistent metric `m = s · p^alpha · IoU(b_hat, b)^beta`, with the one-to-one metric proportional to the one-to-many metric. This is intended to reduce the supervision gap between heads and avoid extra hyperparameter tuning.
- **Efficiency-driven architecture design:** the model uses a lightweight classification head, spatial-channel decoupled downsampling, and rank-guided compact block allocation using Compact Inverted Blocks (CIB) to reduce parameters, FLOPs, and latency.
- **Accuracy-driven architecture design:** the model adds large-kernel depthwise convolution in selected deep stages of small variants and a Partial Self-Attention (PSA) module placed at low resolution to improve global representation with limited overhead.
- **Model family:** YOLOv10-N/S/M/B/L/X variants; YOLOv10-B is derived by increasing the width scale factor of YOLOv10-M.

## Dataset / evaluation protocol

- Main benchmark: MS COCO object detection.
- Training: all YOLOv10 models are trained from scratch; appendix states 500 epochs with SGD, momentum 0.937, weight decay `5e-4`, linear learning-rate decay, and common YOLO-style augmentations including Mosaic, Mixup, and copy-paste.
- Hardware for training: appendix states all models are trained on 8 NVIDIA 3090 GPUs.
- Latency benchmark: T4 GPU with TensorRT FP16, following RT-DETR; end-to-end latency is measured on COCO val set with batch size 1. For YOLO baselines with NMS, TensorRT `efficientNMSPlugin` is appended and average latency is reported across all images; I/O overhead is omitted.
- Comparators include YOLOv6-v3.0, Gold-YOLO, YOLOv8, YOLOv9, YOLO-MS, RT-DETR, and additional lightweight detectors in the appendix.
- People-counting, MOT, ROI/line-crossing, and edge-device evaluation: not evaluated in this source.

## Metrics reported

- Detection accuracy: standard COCO AP, plus appendix reports AP50, AP75, AP for small/medium/large objects.
- Efficiency: number of parameters, FLOPs, end-to-end latency in ms, and forward-only latency (`Latencyf`) for some comparisons.
- Ablations: AP and latency for NMS-free training, model-design components, matching metric variants, large-kernel convolution, PSA, and training cost.
- No tracking metrics (HOTA, IDF1, MOTA), counting error, or deployment resource metrics beyond latency/parameters/FLOPs are reported.

## Findings safe to cite

- YOLOv10 states that YOLO reliance on NMS post-processing harms end-to-end deployment and inference latency.
- The paper proposes consistent dual assignments so YOLO-style detectors can be trained NMS-free while keeping one-to-many supervision during training and using a one-to-one head at inference.
- The authors report that YOLOv10-S is 1.8× faster than RT-DETR-R18 at similar COCO AP, with 2.8× fewer parameters and FLOPs.
- The authors report that YOLOv10-B has 46% lower latency and 25% fewer parameters than YOLOv9-C at the same performance.
- Table 1 reports YOLOv10 model results on COCO, including YOLOv10-S at 46.3 AP, 7.2M parameters, 21.6 GFLOPs, and 2.49 ms latency; YOLOv10-X at 54.4 AP, 29.5M parameters, 160.4 GFLOPs, and 10.70 ms latency.
- Ablation results state that NMS-free training with consistent dual assignments reduces YOLOv10-S end-to-end latency by 4.63 ms while maintaining 44.3% AP in the ablation setting.
- The paper's claims are about real-time object detection on COCO, not specifically human detection, people counting, or tracking.

## Limitations stated by authors

- The paper does not include a standalone limitations section.
- In the model analysis, the authors state that a performance gap remains between NMS-free training and original one-to-many training with NMS, especially for smaller models; YOLOv10-N has a 1.0% AP gap, while YOLOv10-X shows no gap.
- The authors attribute this gap to limited model capacity and less discriminative features in small models, and state that future work will explore ways to reduce the gap and improve end-to-end performance.
- The authors also note that large-kernel convolution brings no improvement for YOLOv10-M due to its larger inherent receptive field, so it is only used for smaller models.

## Limitations inferred for this project

- COCO AP and latency do not prove people-counting accuracy; a counting system still needs tracking, ID persistence, ROI/zone logic, and count-error evaluation.
- The source does not validate the model on CCTV, dense pedestrian scenes, local public-space videos, MOT20, CrowdHuman, or counting datasets.
- The reported latency is measured on T4 GPU with TensorRT FP16 and may not transfer directly to low-end edge devices such as Jetson Nano or CPU-only deployments.
- NMS-free detection can reduce post-processing latency, but detector quality alone does not prevent double-counting when occlusion, missed detections, or ID switches occur.

## Exact claims allowed in draft

- “YOLOv10 provides a peer-reviewed NeurIPS 2024 example of an end-to-end/NMS-free YOLO-style detector for real-time object detection.”
- “YOLOv10 addresses YOLO NMS latency by combining one-to-many supervision during training with one-to-one inference through consistent dual assignments.”
- “YOLOv10 reports improved COCO accuracy-latency and parameter-efficiency trade-offs over several YOLO and RT-DETR baselines under its stated T4 TensorRT FP16 benchmark.”
- “For people-counting pipelines, YOLOv10 supports the detector-side argument that real-time/NMS-free detection is relevant, but it does not by itself solve tracking or counting.”

## Claims NOT allowed

- Do not claim YOLOv10 is a people-counting method.
- Do not claim YOLOv10 was evaluated on local CCTV, dense-crowd tracking, MOT, or ROI/line-crossing people counting; not verified.
- Do not claim YOLOv10 guarantees better counting accuracy or fewer double counts; not evaluated.
- Do not transfer T4 TensorRT FP16 latency numbers directly to Jetson/CPU/embedded deployments without new experiments.
- Do not claim YOLO26 is peer-reviewed based on this paper; YOLOv10 is a predecessor/academic anchor, not YOLO26.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 2: “Deteksi manusia real-time dan pergeseran menuju end-to-end/NMS-free detector.”
- Section 6: “Dataset, metrik evaluasi, dan constraint real-time/edge,” only for detector metrics/latency context.
- Section 7: “Sintesis gap dan posisi penelitian,” as evidence that detector latency improvements still need integration with tracker and counting logic.

## Notes for citation auditor

- Citation key in `references/references.bib`: `S003` exists, but the entry appears to be arXiv-style; auditor may need to ensure final bibliography reflects NeurIPS 2024 if the manuscript cites the peer-reviewed venue.
- Use the NeurIPS URL for peer-reviewed acceptance and arXiv PDF for full-text method/metric details.
- No DOI was verified from the source text beyond arXiv identifier `2405.14458`; if DOI `10.48550/arXiv.2405.14458` is used, verify formatting during bibliography cleanup.
