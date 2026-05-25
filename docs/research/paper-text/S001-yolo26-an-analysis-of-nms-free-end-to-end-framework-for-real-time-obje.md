---
source_id: S001
title: YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection
source_url: https://arxiv.org/pdf/2601.12882
source_file: docs/research/papers/S001-yolo26-an-analysis-of-nms-free-end-to-end-framework-for-real-time-obje.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S001-yolo26-an-analysis-of-nms-free-end-to-end-framework-for-real-time-obje.pdf
## PDF metadata
- format: PDF 1.7
- title: YOLO26: An Analysis of NMS-Free End to End Framework for Real-Time Object Detection
- author: Sudip Chakrabarty
- creator: arXiv GenPDF (tex2pdf:d72aa01)
- producer: pikepdf 8.15.1


## Page 1

YOLO26: AN ANALYSIS OF NMS-FREE END TO END
FRAMEWORK FOR REAL-TIME OBJECT DETECTION
Sudip Chakrabarty
School of Computer Engineering, KIIT University
sudipchakrabarty6@gmail.com
ABSTRACT
The “You Only Look Once” (YOLO) framework has long served as a standard for
real-time object detection, though traditional iterations have utilized Non-Maximum
Suppression (NMS) post-processing, which introduces specific latency and hyper-
parameter variables. This paper presents a comprehensive architectural analysis
of YOLO26, a model that shifts toward a native end-to-end learning strategy by
eliminating NMS. This study examines the core mechanisms driving this frame-
work: the MuSGD optimizer for backbone stabilization, Small-Target-Aware Label
Assignment (STAL), and ProgLoss for dynamic supervision. To contextualize its per-
formance, this article reviews exhaustive benchmark data from the COCO val2017
leaderboard. This evaluation provides an objective comparison of YOLO26 across
various model scales (Nano to Extra-Large) against both prior CNN lineages and
contemporary Transformer-based architectures (e.g., RT-DETR, DEIM, RF-DETR),
detailing the observed speed-accuracy trade-offs and parameter requirements without
asserting a singular optimal model. Additionally, the analysis covers the framework’s
unified multi-task capabilities, including the YOLOE-26 open-vocabulary module
for promptable detection. Ultimately, this paper serves to document how decoupling
representation learning from heuristic post-processing impacts the "Export Gap" and
deterministic latency in modern edge-based computer vision deployments.
Keywords: YOLO26, End-to-End Object Detection, NMS-Free, MuSGD, ProgLoss,
YOLOE-26, Open-Vocabulary Detection, Real-Time Computer Vision.
1
Introduction
Computer vision has evolved rapidly from basic image processing techniques such as edge detection
and morphological filtering into a domain dominated by deep learning. At the forefront of this
evolution is Object Detection, the fundamental task of identifying and localizing instances of
semantic objects within a digital image [1, 2]. Unlike simple classification, which assigns a single
label to an image, object detection requires the simultaneous prediction of class labels and geometric
bounding boxes. This capability is the cornerstone of modern automation, underpinning critical
This article presents a secondary analytical review of YOLO26 based exclusively on publicly available documen-
tation, benchmarks, and technical descriptions released by Ultralytics. For official documentation of YOLO26, visit:
https://docs.ultralytics.com/models/yolo26/
arXiv:2601.12882v2  [cs.CV]  18 Mar 2026


## Page 2

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
applications ranging from autonomous driving and robotic navigation to medical image analysis and
real-time surveillance [3]. As the demand for real-time analysis has grown, the field has shifted away
from computationally heavy two-stage detectors (like Faster R-CNN) toward efficient one-stage
architectures that prioritize inference speed without compromising accuracy [4, 5].
1.1
The Ultralytics Legacy
In this landscape, Ultralytics has emerged as the defining force in real-time detection. Beginning
with the standardization of the YOLO (You Only Look Once) architecture, Ultralytics has consis-
tently pushed the boundaries of efficiency. Their iterative releases—most notably YOLOv5 [6]
and YOLOv8 [7] —stablished a new industry standard by combining Cross-Stage Partial (CSP)
backbones with user-friendly deployment pipelines. These models successfully democratized AI,
allowing complex detection tasks to run on edge devices with limited computational resources.
However, even these state-of-the-art models largely relied on Non-Maximum Suppression (NMS)
post-processing, a sequential step that introduces latency variability in dense scenes.
1.2
YOLO26: Redefining Real-Time Edge Inference
Released in January 2026, YOLO26 establishes a new milestone in the history of real-time object
detection. To quantify this leap, the Ultralytics team has released official benchmarks comparing
YOLO26 against a comprehensive suite of predecessors (YOLOv5 [6] through YOLO11 [8, 9]) and
competitive architectures such as RTMDet [10], DAMO-YOLO [11], and PP-YOLOE+ [12].
Figure 1: Speed-Accuracy Trade-off on COCO val2017. The chart plots the Mean Average Precision
(mAP 50-95) against inference latency (ms/img) on an NVIDIA T4 GPU (TensorRT10, FP16). The
deep blue curve represents YOLO26, which forms a new Pareto front, consistently outperforming
prior YOLO iterations (v5–v11) and state-of-the-art competitors by achieving higher accuracy at
equivalent or lower latency.
2


## Page 3

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Figure 2: Comparative Pareto frontier of YOLO26 against advanced end-to-end architectures on an
NVIDIA T4 GPU (TensorRT10, FP16). YOLO26 strictly dominates recent competitors including
YOLOv10 and the entire RT-DETR lineage (v2, v3, and v4) across all model scales.
1.2.1
Analysis of Reported Performance
As illustrated in the official benchmark data (Figures 1 and 2) [13], the performance landscape is
definitively dominated by the YOLO26 family.
• Absolute Pareto Dominance: The reported metrics show that the YOLO26 curve resides
strictly above and to the left of all other models. Figure 1 demonstrates its superiority over
the legacy CNN-based YOLO lineage. More importantly, Figure 2 provides critical evidence
that YOLO26 also outperforms state-of-the-art transformer-based detectors (including the
latest RT-DETRv4 iterations). This proves that NMS-free CNN architectures can surpass
heavy attention-based mechanisms in both speed and spatial reasoning.
• Nano to Extra-Large Scaling: The Ultralytics benchmarks highlight dominance across all
model scales [8]. The highly constrained nano variant (26n) is shown to achieve > 40 mAP
at a negligible latency of ≈1.5 ms. At the high end, the extra-large model (26x) pushes the
accuracy boundary to ≈57.5 mAP while maintaining real-time performance (≈11.5 ms),
surpassing both YOLO11x [8] and massive DETR equivalents.
This empirical evidence provided by the developers confirms that the removal of NMS and the
adoption of the end-to-end architecture have effectively unlocked raw throughput gains, cementing
YOLO26’s status as the fastest and most accurate detector currently documented.
1.3
Contributions of This Article
This study provides a comprehensive analysis of the YOLO26 architecture, evaluating its impact
on the current state of real-time object detection. The primary contributions of this article are
summarized as follows:
3


## Page 4

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
• Architectural Deconstruction: This article presents a detailed breakdown of the Native
End-to-End NMS-Free architecture, explaining the mathematical mechanisms that allow for
the removal of non-differentiable post-processing.
• Training Dynamics Analysis: Novel optimization strategies—specifically MuSGD, STAL,
and ProgLoss—are reviewed to elucidate how they enable stable convergence for lightweight,
end-to-end backbones.
• Comprehensive Benchmarking: An exhaustive comparative study of YOLO26 is pro-
vided, evaluating its performance not only against prior YOLO lineages (v1–v13) but also
against contemporary State-of-the-Art Transformer architectures (e.g., RT-DETR, DEIM,
RF-DETR) to highlight its dominant speed-accuracy Pareto front.
• Multi-Task & Open-Vocabulary Evaluation: The article analyzes the framework’s unified
multi-task extensions, specifically detailing the structural modifications of the YOLOE-26
open-vocabulary module and its capacity for zero-overhead promptable detection.
• Impact Assessment: The implications of resolving the "Export Gap" are discussed, pro-
viding an analysis of how deterministic latency and direct regression benefit safety-critical
edge AI applications.
1.4
Organization of the Paper
The remainder of this article is structured as follows: Section 2 traces the historical evolution of
the YOLO lineage, setting the context for the current architectural shift. Section 3 dissects the
core innovations of YOLO26, including the NMS-Free pipeline, the DFL-free decoupled head,
and the MuSGD training dynamics. Section 4 details the model’s unified multi-task capabilities,
covering detection, segmentation, and pose estimation. Section 5 presents the official performance
benchmarks, featuring a comprehensive State-of-the-Art (SOTA) analysis. Section 6 analyzes the
critical "Export Gap" challenge and how the architecture achieves deterministic latency on edge
hardware. Section 7 proposes future avenues for research, such as inherent explainability and
spatiotemporal perception. Finally, Section 8 summarizes the contributions and potential impact of
this work.
2
The Evolution of YOLO
The YOLO (You Only Look Once) family has undergone a decade of rapid architectural evolution,
transitioning from rigid grid-based detection to flexible, multi-task intelligence [14, 15]. This
progression can be categorized into three distinct eras: the Foundational Era (v1–v3), the Community
Expansion Era (v4–v7), and the Modern Unified Era (v8–26). Each era is defined by a shift in how
spatial features are extracted and how the final predictions are supervised.
2.1
The Foundational Era (2015–2018)
The original YOLOv1 [16] revolutionized object detection by reframing it as a single regression
problem, sacrificing some localization accuracy for real-time speed. Subsequent iterations intro-
duced anchor boxes in YOLOv2 [17] for improved recall and multi-scale feature pyramids in
YOLOv3 [18] to address the "small object problem," establishing the Darknet backbone as an
industry standard. This era was characterized by the transition from fully connected layers to
4


## Page 5

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
fully convolutional architectures, setting the precedent for global context reasoning in single-stage
detectors.
2.2
The Community Expansion Era (2020–2022)
This period saw a diversification of the YOLO lineage, led by YOLOv4 [19] and YOLOv5 [6], which
introduced CSP (Cross-Stage Partial) connections and advanced "Bag-of-Freebies" augmentation
techniques. This era marked the transition to production-ready frameworks, with variants like
YOLOv6 [20] and YOLOv7 [21] introducing re-parameterization and E-ELAN architectures to
maximize hardware-specific compute utilization. By integrating mosaic augmentation and genetic
anchor optimization, these models bridged the gap between academic research and industrial-scale
deployment across diverse hardware targets.
2.3
The Modern Unified Era (2023–Present)
Starting with YOLOv8 [22], the focus shifted toward anchor-free, decoupled heads. This architec-
tural modularity was further refined in YOLOv9 [23] through Programmable Gradient Information
(PGI) and in YOLOv10 [24], which introduced consistent dual-label assignment for NMS-free
training. The lineage continued with YOLO11 [8, 25], optimizing the C3k2 backbone for multi-task
efficiency, and YOLOv12 [26], which integrated Area Attention (A2) to provide transformer-level
context at CNN speeds. Most recently, YOLOv13 [27] utilized hypergraph spatial modeling to
improve relational reasoning in complex scenes. This transition reflects a broader movement toward
eliminating manual heuristics in favor of end-to-end differentiable pipelines, paving the way for the
edge-optimized strategies seen in the latest iterations.
A critical challenge identified in this era is the "Export Gap"—the performance drop observed
when moving a model from a GPU-training environment to edge-inference hardware (NPUs/CPUs).
Complex operators like Distribution Focal Loss (DFL) used in versions v8 through v13 [22, 24, 27],
while accurate, often create latency bottlenecks on integer-arithmetic hardware.
YOLO26 [13] represents the culmination of this lineage, departing from the complexity-heavy trends
of v12 and v13 to prioritize edge-device latency. By removing the computational burden of DFL
and adopting a native one-to-one prediction head, YOLO26 achieves deterministic inference times,
rendering it highly effective for real-time deployment on low-power devices. These architectural
shifts are summarized in Table 1.
3
Architecture and Methodology of YOLO26
The architectural philosophy of YOLO26 diverts from the recent trend of increasing parameter
complexity (as seen in v10 and v11)[8] to focus on computational density and deterministic latency.
This is achieved by restructuring the inference pipeline to remove heuristic bottlenecks and adopting
optimization strategies traditionally reserved for LLMs, such as MuSGD.
3.1
Native End-to-End NMS-Free Architecture
Traditional object detectors rely on Non-Maximum Suppression (NMS) as a distinct post-processing
step to filter redundant bounding boxes. NMS functions by iteratively selecting the proposal with the
5


## Page 6

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Table 1: Source-Safe Architectural Evolution of the YOLO Family (v1–26)
Model
Backbone
Neck Head
Task(s)
Anc-
hors Loss
Post-
Proc.
Key Innovations & Contributions
YOLOv1
(2015)
Darknet-24
None Coupled
Object Detection No
SSE (Sum)
NMS
Unified single-stage regression framework
enabling real-time object detection.
YOLOv2
(2016)
Darknet-19
Pass-
thro-
ugh
Coupled
Object Detection Yes
Sum-Squared
Error (SSE)
NMS
Introduced anchor boxes, batch normalization,
and the passthrough layer for improved recall and
small-object detection.
YOLOv3
(2018)
Darknet-53
Multi-
Scale Coupled
Object Detection Yes
BCE + SSE
NMS
Multi-scale feature prediction strategy for
enhanced small-object localization.
YOLOv4
(2020)
CSPDarknet53 PAN
Coupled
Object Detection Yes
CIoU + BCE
NMS
CSP-integrated augmentation for optimal
speed–accuracy trade-off.
YOLOv5
(2020)
CSPDarknet
PAN
Coupled
Object Detection Yes
GIoU/CIoU +
BCE
NMS
PyTorch-based modular design with automatic
anchor optimization for easy deployment.
YOLOv6
(2022)
EfficientRep
PAN
Decoupled Object Detection Yes
SIoU / Varifo-
cal
NMS
Re-parameterized convolution for
high-throughput industrial inference efficiency.
YOLOv7
(2022)
E-ELAN
CSP-
PAN
Lead
+
Auxiliary
Object Detection Yes
CIoU + BCE
NMS
Introduced E-ELAN, deep supervision and OTA
assignment for better accuracy and efficiency.
YOLOv8
(2023)
C2f
PAN
Decoupled Obj. Det., Seg.,
Pose Est.
No
BCE + CIoU +
DFL
NMS
Anchor-free decoupled head enabling a unified
multi-task detection framework.
YOLOv9
(2024)
GELAN
PAN
Decoupled Object Detection No
BCE + CIoU +
DFL
NMS
Programmable Gradient Information & GELAN
to overcome info. bottleneck in deep networks.
YOLOv10
(2024)
GELAN
PAN
Decoupled Object Detection No
BCE + CIoU +
DFL
NMS-
Free
NMS-free inference via Dual-Label Assignment;
integrates Partial Self-Attention into GELAN.
YOLOv11
(2024)
C3k2
PAN
Decoupled Obj. Det., Seg.,
Pose Est.
No
BCE + CIoU +
DFL
NMS
C2PSA-based feature refinement; still uses
standard NMS for post-processing.
YOLOv12
(2025)
Flash
Back-
bone + Area
Attention
PAN
Decoupled Object Detection,
Segmentation
No
BCE + CIoU +
DFL
NMS
Uses Area Attention (A2) for long-range
dependency capture while keeping computation
efficient; improves multi-task performance.
YOLOv13
(2025)
Hyper-Net
PAN
Decoupled
Object Detection,
Segmentation,
Pose Estimation
No
BCE + CIoU +
DFL
NMS
Third-party release by iMoonLab; Hypergraph
spatial modeling for relational reasoning and
complex scene understanding.
YOLO26
(2026)
CSP-Muon
(Edge-
Optimized
CNN)
PAN
Decoupled
(1-to-1)
Object Detection,
Segmentation,
Pose Estimation,
OBB
No
STAL
+
ProgLoss
NMS-
Free
Edge-optimized, DFL-free learning with
one-to-one label assignment; native NMS-free
head for low-latency deployment; optimized for
CPU and Edge exportability.
6


## Page 7

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
highest confidence score (Smax) and suppressing all other overlapping boxes (bi) whose Intersection
over Union (IoU) with Smax exceeds a predefined threshold (Nt). This process can be formally
defined as [28]:
si =
(
si,
if IoU(M, bi) < Nt
0,
if IoU(M, bi) ≥Nt
(1)
where M is the current maximum confidence box and si is the updated score. This heuristic is
inherently sequential, creating a latency bottleneck that varies depending on scene density (i.e., the
number of detected objects).
Figure 3: Comparison of Inference Pipelines. (Left) Traditional YOLOv8 pipeline requiring
sequential NMS post-processing. (Right) YOLO26 End-to-End pipeline where the model directly
outputs unique predictions, reducing latency and complexity.
YOLO26 fundamentally alters this pipeline through a Native End-to-End Architecture. By
redesigning the prediction head to support one-to-one label assignment [24], the model learns to
output a single, definitive box per object instance during training. This architectural shift eliminates
the need for Eq. 1 entirely, transforming inference from a multi-stage filtering operation into a
direct, deterministic mapping of input to output (see Fig. 3). The result is a lighter, streamlined
execution graph that is easier to deploy and achieves constant-time latency regardless of object
count [10].
Performance Impact: The removal of the NMS operator yields significant latency reductions,
particularly on non-GPU hardware where sequential operations create bottlenecks. By transitioning
to this end-to-end paradigm, Ultralytics reports that YOLO26 achieves an inference speedup of
approximately 43% on CPU targets compared to standard NMS-based baselines [13]. This
constant-time inference is critical for safety-critical applications, such as autonomous driving or
medical monitoring, where deterministic response times are required regardless of scene complexity.
3.2
Regression-Centric Decoupled Head (DFL-Free)
Recent YOLO iterations (v8–v11 [8]) adopted Distribution Focal Loss (DFL) [29] to model bound-
ing box coordinates as general distributions rather than deterministic values. While DFL improves
7


## Page 8

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
localization accuracy by accounting for uncertainty at object boundaries, it introduces a significant
computational overhead: the necessity of performing Softmax operations over discretized bins for
every coordinate prediction. On specialized edge hardware (NPUs and DSPs), these Softmax layers
are notoriously difficult to quantize and often become the primary latency bottleneck [30].
Quantification of Softmax Overhead: In a DFL-based head, estimating a single coordinate y
requires integrating over a discretized probability distribution (typically 16 bins). This forces the
inference engine to compute a weighted Softmax summation for every bounding box parameter:
ˆyDFL =
n
X
i=0
i · Softmax(wi) =
n
X
i=0
i ·
ewi
Pn
j=0 ewj
(2)
This operation involves repeated exponential (ex) and division calculations, which are computation-
ally expensive on integer-arithmetic edge accelerators [31].
Figure 4: Architectural comparison of the prediction heads. (Left) Traditional Decoupled Head uti-
lizing Distribution Focal Loss (DFL), (Right) YOLO26 Decoupled Head employing the streamlined
Direct Regression strategy, eliminating DFL overhead for optimized edge inference.
YOLO26 reverts to a Direct Regression Strategy, removing this module entirely (see Fig. 4). This
architectural rollback is motivated by the "Export Gap"—the discrepancy between theoretical FLOPs
and actual inference speed on deployed hardware [10]. By eliminating the integral representation of
Eq. 2, the decoding phase is simplified to a direct linear mapping:
ˆyv26 = Freg(x) ∈R
(3)
To maintain high precision without the distributional benefits of DFL, YOLO26 employs a refined
Decoupled Head structure inspired by YOLOX [32]. As illustrated in standard topologies, the head
separates feature extraction into two distinct branches:
Head(x) = {Fcls(x), Freg(x)}
(4)
8


## Page 9

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
where Fcls predicts class probabilities and Freg predicts box regression parameters directly. This
separation ensures that the removal of DFL does not degrade classification performance [32],
while the regression branch is optimized via the new STAL and ProgLoss functions to recover the
localization precision lost by discarding the distributional prior.
3.3
Advanced Training Dynamics: MuSGD, STAL, and ProgLoss
The removal of the Distribution Focal Loss (DFL) module and the transition to an end-to-end
architecture necessitate a more robust training strategy to prevent gradient collapse. YOLO26
addresses this through a triad of optimization and supervision innovations.
3.3.1
MuSGD Optimizer
To ensure convergence stability within the new architecture, Ultralytics reports that YOLO26
introduces MuSGD (Momentum-Unified Stochastic Gradient Descent), a novel hybrid optimizer
that fuses the properties of standard SGD with the Muon optimizer. Explicitly inspired by the
training dynamics of Moonshot AI’s Kimi K2 large language model, MuSGD represents a strategic
transfer of advanced optimization methods from the NLP domain into computer vision [33].
The Muon Component: The core innovation of MuSGD lies in its integration of the Muon
optimizer [34]. Unlike element-wise optimizers (e.g., AdamW), Muon performs matrix orthogo-
nalization, updating the entire weight matrix to be orthogonal to its current state. This maximizes
update efficiency along the most impactful directions while restraining the spectral norm [35].
Mathematical Formulation: MuSGD combines this orthogonal scaling with the stability of
classical SGD. First, we define the standard momentum buffer vt used in Stochastic Gradient
Descent:
vt+1 = β · vt + gt
(5)
where gt is the gradient and β is the momentum coefficient. MuSGD then modifies the final weight
update by injecting the Newton-Schulz orthogonalization into this trajectory:
θt+1 = θt −η · (α · vt+1 + (1 −α) · NewtonSchulz(gt))
(6)
where NewtonSchulz(gt) effectively "whitens" the gradient matrix using an iterative refinement
process [36]. This hybrid approach mitigates the variance of pure SGD while avoiding the instability
of pure orthogonal updates in the early epochs (see Fig. 5). By enabling the simplified end-to-end
backbone to learn robust features without the need for complex warm-up schedules, MuSGD reduces
the total training time required to reach convergence.
3.3.2
Small-Target-Aware Label Assignment (STAL)
To address the "small object vanishing" problem inherent in edge-optimized models [37], YOLO26
implements Small-Target-Aware Label Assignment (STAL). Standard assignment strategies
typically rely on a fixed Intersection-over-Union (IoU) threshold (e.g., τ = 0.5). While effective
for large objects, this rigid threshold is detrimental to small targets (occupying < 1% of the image
9


## Page 10

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Figure 5: Conceptual visualization of the expected optimization dynamics. The MuSGD strategy
(Blue) is designed to mitigate the gradient variance observed in standard SGD (Red), theoretically
allowing for a steeper learning trajectory without warm-up.
area), where even well-centered anchors yield mathematically low IoU scores due to pixel-level
discretization errors and the sensitivity of the IoU metric to small spatial shifts [38].
STAL resolves this by replacing the static threshold with a dynamic variable that adapts to the
object’s scale, drawing inspiration from Task Alignment Learning (TAL) [39]. As defined in Eq. 7,
the matching threshold τ relaxes as the relative object size decreases:
τdynamic = τbase ·

1 −α · e
−
Areaobj
Areaimg

(7)
where α controls the decay rate. For a tiny object, the exponential term approaches 1, significantly
lowering τdynamic and allowing anchors with lower physical overlap to still be assigned as positive
samples. This acts as a "magnifying glass" for supervisory signals, ensuring that tiny or occluded
objects—common in drone imagery and medical scans—receive adequate gradient contribution
[40] (see Fig. 6).
3.3.3
Progressive Loss Balancing (ProgLoss)
To further stabilize the training of the end-to-end architecture, YOLO26 employs ProgLoss, a
dynamic loss weighting strategy. In standard detectors [22, 41], the ratio between classification
loss (Lcls) and bounding box regression loss (Lbox) is typically fixed. However, this static bal-
ance is suboptimal for end-to-end learning, where the network must simultaneously learn feature
discrimination and precise localization without the geometric guidance of anchor priors [42].
ProgLoss addresses this by introducing a time-dependent modulation coefficient (λt). As shown in
Eq. 8 and illustrated in Fig. 7, the total loss evolves across training epochs t.
10


## Page 11

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Figure 6: Mechanism of Small-Target-Aware Label Assignment (STAL). (Left) Standard assignment
ignores the small target because its IoU (0.15) is below the fixed threshold (0.5). (Right) STAL
detects the small area ratio and dynamically lowers the threshold to 0.10, successfully assigning the
anchor as a positive sample for training.
Ltotal(t) = λt · Lcls + (1 −λt) · Lbox
(8)
where λt follows a monotonically decreasing schedule, such as cosine decay [43]. This strategy
ensures a smooth transition between semantic grounding and geometric refinement.
• Early Phase (High λt): As seen in the blue region of Fig. 7, the gradient is initially
dominated by Lcls. This prioritizes the learning of high-level semantic features to stabilize
the backbone and establish object existence [44].
• Late Phase (Low λt): As training progresses (orange region), the focus shifts to Lbox,
allowing the model to fine-tune geometric boundaries. This prevents "easy negatives" from
dominating the gradient in the final stages, ensuring high-precision localization despite the
removal of DFL.
4
Multi-Task Capabilities of YOLO26
YOLO26 functions as a unified model family, providing end-to-end support for a diverse range of
computer vision tasks [13]. Each architectural variant, from Nano (n) to Extra-Large (x), is natively
compatible with specialized prediction heads designed for distinct spatial and semantic reasoning
challenges. As illustrated in Figure 8, the framework moves beyond simple object detection to
facilitate a comprehensive suite of analytical capabilities within a single, optimized inference
pipeline.
11


## Page 12

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Figure 7: Conceptual visualization of the proposed ProgLoss scheduling strategy. The chart
illustrates the intended dynamic balancing, where the classification weight (λt, blue) dominates
the early "Semantic Learning" phase to stabilize training, and the regression weight (orange)
progressively increases to prioritize "Geometric Precision" in the final epochs.
Beyond visual representation, the technical execution of these tasks is governed by specialized
output structures and loss functions tailored for edge efficiency. Table 2 provides a comparative
summary of the head outputs and coordinate formats employed by the YOLO26 family to maintain
architectural consistency across varied domains. This multi-task framework leverages the unified
backbone and the aforementioned ProgLoss scheduling to ensure that the transition from standard
bounding boxes to more complex geometries—such as keypoints and oriented boxes—does not
incur a significant latency penalty.
Table 2: Summary of YOLO26 Multi-Task Support and Task-Specific Head Designs
Task
Head Output
Coordinate Format
Head Mechanism / Objective
Object Detection
Class + Box
(xc, yc, w, h)
NMS-Free Detection, STAL
Loss
Instance Segmentation
Class + Box +
Mask
(xc, yc, w, h) + Maskpix
Prototype
Mask
Head,
ProgLoss
Classification
Class Label
None (Global Label)
Global Pooling, Linear Classifi-
cation Head
Pose Estimation
Class + Box +
Keypoints
(xi, yi, vi)17
i=1
OKS-based Keypoint Optimiza-
tion
Oriented Detection
Class + Rotated
Box
(xc, yc, w, h, θ)
Rotated IoU / Angle-Aware
Loss
Open-Vocabulary
Text + Box
(xc, yc, w, h) + Embedtxt
Vision–Language Embedding
Alignment
12


## Page 13

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Figure 8: Unified multi-task execution in YOLO26, demonstrating (a) Detection, (b) Segmentation,
(c) Classification, (d) Pose Estimation, and (e) Oriented Bounding Box (OBB) detection
4.1
Object Detection
The primary objective of YOLO26 is the identification and localization of discrete object instances
via axis-aligned bounding boxes, as demonstrated in Figure 8(a). While this remains the foundational
task of the YOLO series, YOLO26 optimizes the detection pipeline by leveraging the native end-
to-end architecture discussed in Section 3.1. By utilizing the one-to-one label assignment strategy,
the model achieves a 43% reduction in CPU latency [13], a critical factor for real-time medical
monitoring and edge-tier surveillance. Beyond raw speed, the removal of the non-differentiable
NMS operator ensures that the detection process is fully deterministic. This predictability is vital
for the fidelity of explainability methods, providing a direct, transparent path from pixel input to
final box output.
The detection of minute features is further bolstered by the STAL mechanism described in Eq. 7.
In practical applications, such as the analysis of micro-anomalies in histopathological datasets,
STAL prevents the "vanishing gradient" effect typically associated with small targets. This allows
YOLO26 to maintain high recall for objects occupying less than 1% of the image area, ensuring
that the streamlined, DFL-free regression head remains precise across all object scales.
4.2
Instance Segmentation
Instance segmentation in YOLO26 represents a critical shift from regional localization to pixel-wise
classification, as illustrated in Figure 8(b). By integrating a mask-prediction branch alongside the
13


## Page 14

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
decoupled head, the model facilitates precise shape extraction for individual objects. As summarized
in Table 2, the head output for this task includes both bounding box coordinates and a pixel-level
mask (Maskpix), which is vital for medical diagnostics where the exact area of a pathology provides
more value than a simple coordinate box.
A novel refinement in YOLO26-seg is the use of Boundary-Aware Supervision, supported by
the ProgLoss scheduling in Eq. 8. Because the model is DFL-free, it avoids the discretization
errors that often blur object edges on edge hardware. Instead, the late-stage regression focus of
ProgLoss acts as a "contour polisher," ensuring that the masks remain sharp even for small or
overlapping targets. By leveraging the MuSGD optimizer’s ability to maintain stable spectral norms,
the segmentation branch achieves higher feature resolution with fewer parameters, leading to the
previously noted speedup on CPU and NPU targets. This ensures that high-fidelity segmentation is
no longer restricted to high-end GPUs but is fully exportable to real-time edge environments [13].
4.3
Image Classification
Image classification within the YOLO26 ecosystem represents the most computationally efficient
task, as it bypasses the requirement for spatial regression or mask generation, as shown in Figure
8(c). By analyzing the input holistically, the classification head utilizes Global Average Pooling
(GAP) to condense the high-level feature maps from the backbone into a single vector, which is then
mapped to categorical probabilities [45]. This architecture prioritizes overarching visual patterns
over specific coordinate-based boundaries, as summarized in Table 2.
The YOLO26-cls variant leverages the streamlined CSP-based backbone to achieve minimal infer-
ence latency, making it ideal for the initial categorization of large-scale medical or environmental
datasets where the presence of a pathology or object is the primary metric [13]. Furthermore, the
integration of ProgLoss scheduling (Eq. 8) ensures that the classification head achieves stable
convergence on complex, multi-class datasets. By focusing on semantic grounding during the early
training phase, the model establishes robust global representations that are less sensitive to spatial
noise or object occlusion compared to purely regional detectors [46].
4.4
Pose Estimation
Pose estimation in YOLO26 extends spatial reasoning to the localization of 17 anatomical landmarks,
as visualized in Figure 8(d). This task tracks the orientation and movement of joints by outputting
a triplet format (xi, yi, vi) for each keypoint. The specific anatomical indices for the default
COCO-based mapping [47]. are detailed in Table 3.
Table 3: YOLO26 Default 17-Keypoint Mapping
Idx
Joint
Idx
Joint
Idx
Joint
0
Nose
6
Right Shoulder
12
Right Hip
1
Left Eye
7
Left Elbow
13
Left Knee
2
Right Eye
8
Right Elbow
14
Right Knee
3
Left Ear
9
Left Wrist
15
Left Ankle
4
Right Ear
10
Right Wrist
16
Right Ankle
5
Left Shoulder
11
Left Hip
14


## Page 15

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Accuracy is governed by the Object Keypoint Similarity (OKS), which normalizes Euclidean
distance di against the object scale s and a per-joint falloff constant κi:
OKS =
P
i exp(−d2
i /2s2κ2
i )δ(vi > 0)
P
i δ(vi > 0)
(9)
To maintain precision in the absence of DFL, YOLOv26-pose utilizes Residual Log-Likelihood
Estimation (RLE) [48]. By modeling spatial uncertainty rather than a fixed distribution, RLE
allows the model to reason through occlusions. Combined with the MuSGD optimizer, this ensures
high-fidelity keypoint regression with deterministic latency on edge hardware.
4.5
Oriented Object Detection (OBB)
Oriented Object Detection (OBB) in YOLO26 introduces a rotational parameter (θ) to precisely
localize skewed targets, as illustrated in Figure 8(e). By utilizing the normalized xywhr format
detailed in Table 2, the model eliminates the background noise typical of axis-aligned boxes in
aerial and industrial domains [49]. To resolve boundary discontinuity errors inherent in angular
regression, the architecture employs a specialized Angle Loss that maintains geometric consistency
even for near-square objects [50].
This task leverages the Direct Regression strategy and the MuSGD optimizer to achieve high
angular precision without the computational overhead of distributional focal loss. When deployed
on edge-tier hardware like UAVs, the NMS-free head enables deterministic latency in dense envi-
ronments, such as shipping ports. These optimizations result in a 43% inference speedup compared
to traditional heuristic-based rotational NMS baselines [13], ensuring real-time performance on
resource-constrained devices.
4.6
Open-Vocabulary Detection and Segmentation (YOLOE-26)
YOLOE-26 represents a significant evolution in the lineage by integrating the high-performance
YOLO26 architecture with advanced open-vocabulary capabilities. By aligning visual features with
rich linguistic embeddings, this capability enables the real-time detection and instance segmentation
of arbitrary object classes, effectively removing the historical constraints of fixed-category training
[51]. The framework provides flexible inference options to adapt to dynamic scenarios. As illustrated
conceptually in Figure 9, YOLOE-26 supports three distinct modes: utilizing text prompts to define
targets (e.g., "find the red cup"), employing visual prompts via reference images for one-shot
recognition, or operating in a prompt-free mode for zero-shot inference.
To achieve these flexible multi-modal inputs without bottlenecking real-time edge performance,
YOLOE-26 structurally modifies the standard YOLO backbone and PAN-FPN neck by introducing
three novel modules, detailed in Figure 10:
• Re-parameterizable Region-Text Alignment (RepRTA): Refines text embeddings (e.g.,
from CLIP) via a small auxiliary network to support text-prompted detection.
• Semantic-Activated Visual Prompt Encoder (SAVPE): Encodes semantic and activation
features from a reference image, conditioning the model for one-shot visual prompting.
15


## Page 16

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Figure 9: Conceptual overview of the YOLOE-26 open-vocabulary architecture illustrating multi-
modal input processing for real-time edge detection and segmentation.
• Lazy Region-Prompt Contrast (LRPC): Enables prompt-free zero-shot inference by
performing open-set recognition using internal embeddings trained on massive vocabularies
(e.g., LVIS [52], Objects365 [53]).
Figure 10: Detailed architecture pipeline of YOLOE. The diagram illustrates how the RepRTA,
SAVPE, and LRPC modules interface with the standard feature extraction backbone and NMS-free
decoupled head.
The primary architectural motivation behind this specific pipeline is zero-overhead inference. Post-
training, the parameters of the RepRTA and SAVPE modules can be re-parameterized and folded
directly into a standard YOLO head. As a result, when utilized as a regular closed-set detector,
YOLOE-26 preserves identical FLOPs and latency to standard YOLO26 models.
From a technical perspective, YOLOE-26 continues to leverage the native NMS-free, end-to-end
design of the core backbone. This design eliminates the need for heuristic post-processing steps like
16


## Page 17

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Non-Maximum Suppression (NMS), a paradigm shift popularized by transformer-based detectors
[54]. By building upon this streamlined architecture, the model delivers fast open-world inference
with minimal latency. This combination of deterministic high-speed performance and semantic
flexibility makes YOLOE-26 a powerful solution for edge applications deployed in environments
where the objects of interest represent a broad and evolving vocabulary [13].
5
Official Performance Benchmarks and Analysis
To quantify the impact of the architectural innovations discussed in previous sections, this study
reviews the official performance metrics published by the Ultralytics development team [13].
The following benchmarks evaluate YOLO26 on standard datasets, validating the efficacy of the
NMS-free, end-to-end architecture.
5.1
Object Detection Performance
As detailed in the official YOLO26 documentation, the baseline evaluations were conducted on
the Microsoft COCO val2017 dataset, which includes 80 pretrained classes. The most significant
indicator of YOLO26’s architectural efficiency is its performance on standard object detection tasks.
Table 4 presents the official metrics for the YOLO26 family, ranging from the highly constrained
Nano (n) variant to the Extra-Large (x) model.
Table 4: Official YOLO26 Object Detection Benchmarks on COCO. Hardware speeds represent
CPU (ONNX) and NVIDIA T4 GPU (TensorRT10) environments.
Model
Size (px)
mAPval
50-95
mAPval
e2e
CPU ONNX (ms)
T4 TensorRT (ms)
Params (M)
FLOPs (B)
YOLO26n
640
40.9
40.1
38.9 ± 0.7
1.7 ± 0.0
2.4
5.4
YOLO26s
640
48.6
47.8
87.2 ± 0.9
2.5 ± 0.0
9.5
20.7
YOLO26m
640
53.1
52.5
220.0 ± 1.4
4.7 ± 0.1
20.4
68.2
YOLO26l
640
55.0
54.4
286.2 ± 2.0
6.2 ± 0.2
24.8
86.4
YOLO26x
640
57.5
56.9
525.8 ± 4.0
11.8 ± 0.2
55.7
193.9
*Note: mAPval metrics represent single-model, single-scale evaluation on the COCO val2017 dataset. Parameter
counts and FLOPs denote the fused inference architecture, which merges Conv/BatchNorm layers and removes the
auxiliary one-to-many detection head used during training.
As reported in the official metrics, YOLO26 establishes a strict Pareto dominance across all model
scales. Notably, the mAPval
e2e column confirms that the native end-to-end architecture retains nearly
all the precision of the standard evaluation baseline, while the latency columns demonstrate the
extreme computational efficiency of the framework. The Nano variant (YOLO26n), for instance,
achieves over 40 mAP at a negligible 1.7 ms latency on a T4 GPU, rendering it highly competitive
for real-world edge deployment.
5.2
Instance Segmentation Performance
Beyond standard bounding boxes, the official release includes benchmarks for pixel-level instance
segmentation. Because YOLO26 utilizes a unified, DFL-free backbone across all its tasks, the com-
putational penalty typically associated with adding a mask-prediction branch is heavily mitigated.
Table 5 presents the performance of the -seg models on the COCO dataset.
17


## Page 18

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Table 5: Official YOLO26 Instance Segmentation Benchmarks on COCO.
Model
Size (px)
mAPbox
e2e
mAPmask
e2e
CPU ONNX (ms)
T4 TensorRT (ms)
Params (M)
FLOPs (B)
YOLO26n-seg
640
39.6
33.9
53.3 ± 0.5
2.1 ± 0.0
2.7
9.1
YOLO26s-seg
640
47.3
40.0
118.4 ± 0.9
3.3 ± 0.0
10.4
34.2
YOLO26m-seg
640
52.5
44.1
328.2 ± 2.4
6.7 ± 0.1
23.6
121.5
YOLO26l-seg
640
54.4
45.5
387.0 ± 3.7
8.0 ± 0.1
28.0
139.8
YOLO26x-seg
640
56.5
47.0
787.0 ± 6.8
16.4 ± 0.1
62.8
313.5
The data illustrates that high-fidelity contour extraction is exportable to real-time edge environments.
For example, the YOLO26n-seg model requires only 2.7M parameters—a marginal increase over
the base detection model—yet achieves nearly 34.0 mask mAP with a T4 inference latency of
just 2.1 ms. This validates the efficacy of the ProgLoss "contour polishing" dynamic discussed in
Section 4.
5.3
Image Classification Performance
For image classification, the YOLO26 architecture prioritizes holistic visual reasoning via Global
Average Pooling (GAP). The official benchmarks assess this capability on the ImageNet dataset,
evaluating the model across 1000 pretrained classes at a standard resolution of 224x224 pixels.
Table 6: Official YOLO26 Image Classification Benchmarks on ImageNet.
Model
Size (px)
Acc Top-1
Acc Top-5
CPU ONNX (ms)
T4 TensorRT (ms)
Params (M)
FLOPs (B)
YOLO26n-cls
224
71.4
90.1
5.0 ± 0.3
1.1 ± 0.0
2.8
0.5
YOLO26s-cls
224
76.0
92.9
7.9 ± 0.2
1.3 ± 0.0
6.7
1.6
YOLO26m-cls
224
78.1
94.2
17.2 ± 0.4
2.0 ± 0.0
11.6
4.9
YOLO26l-cls
224
79.0
94.6
23.2 ± 0.3
2.8 ± 0.0
14.1
6.2
YOLO26x-cls
224
79.9
95.0
41.4 ± 0.9
3.8 ± 0.0
29.6
13.6
The YOLO26x-cls model achieves nearly 80.0% Top-1 accuracy while maintaining a sub-4-
millisecond inference speed on a T4 GPU, making it a highly optimal feature extractor for upstream
perception pipelines.
5.4
Pose Estimation Performance
Designated by the -pose suffix (e.g., yolo26n-pose.pt), these variants are explicitly trained on
the COCO keypoints dataset, rendering them highly adaptable for a wide variety of downstream
pose estimation tasks. The official performance metrics for these models are detailed in Table 7,
demonstrating the effectiveness of the NMS-free architecture for precise spatial tracking.
Table 7: Official YOLO26 Pose Estimation Benchmarks on COCO.
Model
Size (px)
mAPpose
50-95(e2e)
mAPpose
50(e2e)
CPU ONNX (ms)
T4 TensorRT (ms)
Params (M)
FLOPs (B)
YOLO26n-pose
640
57.2
83.3
40.3 ± 0.5
1.8 ± 0.0
2.9
7.5
YOLO26s-pose
640
63.0
86.6
85.3 ± 0.9
2.7 ± 0.0
10.4
23.9
YOLO26m-pose
640
68.8
89.6
218.0 ± 1.5
5.0 ± 0.1
21.5
73.1
YOLO26l-pose
640
70.4
90.5
275.4 ± 2.4
6.5 ± 0.1
25.9
91.3
YOLO26x-pose
640
71.6
91.6
565.4 ± 3.0
12.2 ± 0.2
57.6
201.7
18


## Page 19

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
These findings confirm that the removal of Distribution Focal Loss (DFL) does not degrade spatial
keypoint tracking. The YOLO26n-pose model yields an impressive 57.2 mAPpose
50-95(e2e) at 1.8 ms (T4
TensorRT), verifying its suitability for real-time biomechanical analysis on edge devices.
5.5
Oriented Bounding Boxes (OBB) Object Detection Performance
For tasks involving skewed or densely packed targets (e.g., aerial or satellite imagery), the OBB
models are evaluated on the DOTAv1 dataset across 15 pretrained classes. Due to the requirement
for higher spatial fidelity in aerial contexts, these models operate at a larger inference resolution of
1024x1024 pixels.
Table 8: Official YOLO26 Oriented Object Detection Benchmarks on DOTAv1.
Model
Size (px)
mAPtest
50-95(e2e)
mAPtest
50(e2e)
CPU ONNX (ms)
T4 TensorRT (ms)
Params (M)
FLOPs (B)
YOLO26n-obb
1024
52.4
78.9
97.7 ± 0.9
2.8 ± 0.0
2.5
14.0
YOLO26s-obb
1024
54.8
80.9
218.0 ± 1.4
4.9 ± 0.1
9.8
55.1
YOLO26m-obb
1024
55.3
81.0
579.2 ± 3.8
10.2 ± 0.3
21.2
183.3
YOLO26l-obb
1024
56.2
81.6
735.6 ± 3.1
13.0 ± 0.2
25.6
230.0
YOLO26x-obb
1024
56.7
81.7
1485.7 ± 11.5
30.5 ± 0.9
57.6
516.5
Despite the computationally intensive 1024x1024 input resolution, the NMS-free architecture
ensures latency remains strictly bounded. The YOLO26s-obb variant processes these large matrices
in under 5.0 ms on a T4 GPU, effectively resolving the boundary discontinuity errors typically
associated with high-resolution aerial detection.
5.6
Open-Vocabulary Instance Segmentation (YOLOE-26)
To validate the multi-modal capabilities discussed in Section 4.6, the official benchmarks assess
the YOLOE-26 series on open-vocabulary detection and segmentation. These models are evaluated
using a combination of the Objects365v1 [53], GQA [55], and Flickr30k [56] datasets. Table 9
presents the performance metrics utilizing both Text and Visual prompts. The metrics are denoted
in a (Text / Visual) format to illustrate the model’s flexibility across different prompting modalities.
Table 9: Official YOLOE-26 Open-Vocabulary Instance Segmentation Benchmarks. Performance
values are reported as (Text Prompt / Visual Prompt).
Model
Size (px)
mAPminival
50-95(e2e)
mAPminival
50-95
mAPr
mAPc
mAPf
Params (M)
FLOPs (B)
YOLOE-26n-seg
640
23.7 / 20.9
24.7 / 21.9
20.5 / 17.6
24.1 / 22.3
26.1 / 22.4
4.8
6.0
YOLOE-26s-seg
640
29.9 / 27.1
30.8 / 28.6
23.9 / 25.1
29.6 / 27.8
33.0 / 29.9
13.1
21.7
YOLOE-26m-seg
640
35.4 / 31.3
35.4 / 33.9
31.1 / 33.4
34.7 / 34.0
36.9 / 33.8
27.9
70.1
YOLOE-26l-seg
640
36.8 / 33.7
37.8 / 36.3
35.1 / 37.6
37.6 / 36.2
38.5 / 36.1
32.3
88.3
YOLOE-26x-seg
640
39.5 / 36.2
40.6 / 38.5
37.4 / 35.3
40.9 / 38.8
41.0 / 38.8
69.9
196.7
The data reveals the architectural overhead required to align visual features with rich linguistic
embeddings. While the parameter count naturally increases compared to the standard segmentation
models (e.g., YOLOE-26n-seg requires 4.8M parameters versus 2.7M for YOLO26n-seg), the
end-to-end framework efficiently manages this multi-modal complexity. The models maintain
strong recall across rare (mAPr), common (mAPc), and frequent (mAPf) classes, confirming that
19


## Page 20

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
the NMS-free design is highly scalable to open-world, dynamic environments where fixed-category
constraints are removed.
Furthermore, the YOLOE-26 framework offers a "Prompt-Free" (zero-shot) mode, designed for
autonomous environments where external text or visual prompts are unavailable. Table 10 details
the performance of the specialized -pf (prompt-free) variants.
Table 10: YOLOE-26 Prompt-Free (Zero-Shot) Benchmarks on Objects365v1, GQA, and Flickr30k.
Model
Size (px)
mAPminival
50-95(e2e)
mAPminival
50(e2e)
Params (M)
FLOPs (B)
YOLOE-26n-seg-pf
640
16.6
22.7
6.5
15.8
YOLOE-26s-seg-pf
640
21.4
28.6
16.2
35.5
YOLOE-26m-seg-pf
640
25.7
33.6
36.2
122.1
YOLOE-26l-seg-pf
640
27.2
35.4
40.6
140.4
YOLOE-26x-seg-pf
640
29.9
38.7
86.3
314.4
While operating without explicit guidance naturally results in lower overall mAP compared to
prompt-assisted modes, the prompt-free models retain substantial zero-shot detection capabilities.
The corresponding increase in parameter and computational load—for instance, the Nano prompt-
free variant requires 6.5M parameters and 15.8B FLOPs compared to 4.8M and 6.0B for the
prompted version—reflects the heavier internal encoding required to independently reason about
open-world object classes without an external semantic anchor.
5.7
Comprehensive State-of-the-Art Analysis
To establish the efficacy of the YOLO26 architecture, we conduct an exhaustive comparison against
the current State-of-the-Art (SOTA) object detection models. The benchmark data, sourced from
the Roboflow Computer Vision Leaderboard1, evaluates models on the COCO val2017 dataset.
This comparison spans the entire spectrum of model scales, from highly constrained Nano variants
to high-capacity Extra-Large models, incorporating both CNN-based YOLO lineages (v8 through
v13) and recent Transformer-based architectures (RT-DETR, DEIM, RF-DETR).
Table 11: Comprehensive SOTA Object Detection Benchmarks on COCO val2017. Models are grouped by
scale and sorted by mAPval
50-95. All performance metrics (mAP and F1 scores) are reported as percentages (%).
Model
Params (M)
mAPval
50-95
mAPval
50
mAPval
75
F150
F175
License
Large & Extra-Large Models
RF-DETR-XXL
126.9
59.9
78.2
65.4
15.3
12.9
PML-1.0
RF-DETR-XL
126.4
58.5
77.1
63.7
15.0
12.4
PML-1.0
DEIM-D-FINE-X
61.7
56.5
74.0
61.6
5.7
4.8
Apache-2.0
YOLO26x
55.7
56.3
73.4
61.7
14.4
12.5
AGPL-3.0
RF-DETR-L
33.9
56.3
74.8
61.1
15.2
12.6
Apache-2.0
Continued on next page
1Leaderboard: https://leaderboard.roboflow.com/
20


## Page 21

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Table 11 – continued from previous page
Model
Params (M)
mAPval
50-95
mAPval
50
mAPval
75
F150
F175
License
DEIM-RT-DETRv2-X
74.9
55.5
73.5
60.3
5.7
4.7
Apache-2.0
DEIM-D-FINE-L
30.8
54.7
72.4
59.4
5.6
4.7
Apache-2.0
RT-DETRv2-X
92.5
54.3
72.8
58.8
5.6
4.6
Apache-2.0
RT-DETR-R101
92.5
54.3
72.8
58.8
5.6
4.6
Apache-2.0
DEIM-RT-DETRv2-L
42.1
54.3
72.2
58.8
5.7
4.7
Apache-2.0
YOLOv12x
59.1
54.0
70.3
59.0
26.2
22.5
AGPL-3.0
YOLOv13x
64.0
53.7
70.8
58.7
13.8
11.6
AGPL-3.0
YOLOv10x
31.7
53.6
70.3
58.4
22.6
19.4
AGPL-3.0
YOLO11x
56.9
53.6
70.2
58.4
13.9
11.8
AGPL-3.0
YOLO26l
24.8
53.6
70.4
58.6
14.2
12.2
AGPL-3.0
RT-DETRv2-L
50.0
53.4
71.6
57.5
5.6
4.6
Apache-2.0
RT-DETR-R50
50.0
53.1
71.2
57.7
5.5
4.5
Apache-2.0
YOLOv8x
68.2
52.9
69.4
57.7
23.6
20.0
AGPL-3.0
YOLOv12l
26.4
52.6
69.1
57.3
24.4
20.7
AGPL-3.0
RTMDet-x
94.9
52.5
70.1
57.7
5.4
4.5
GPL-3.0
YOLOv10l
25.8
52.3
69.1
57.1
22.6
19.2
AGPL-3.0
YOLOv13l
27.6
52.3
69.7
56.9
13.8
11.5
AGPL-3.0
YOLO11l
25.3
52.2
68.5
56.9
13.7
11.5
AGPL-3.0
YOLOv8l
43.7
51.8
68.3
56.5
22.8
19.3
AGPL-3.0
RTMDet-l
52.3
51.2
68.9
55.8
5.5
4.5
GPL-3.0
Medium Models
RF-DETR-M
33.7
54.8
73.6
59.3
5.7
4.6
Apache-2.0
DEIM-RT-DETRv2-M*
33.0
53.2
71.2
57.8
5.7
4.6
Apache-2.0
DEIM-D-FINE-M
19.2
52.7
70.0
57.3
5.6
4.6
Apache-2.0
YOLO26m
20.4
52.0
69.0
56.8
14.1
12.0
AGPL-3.0
RT-DETRv2-M*
38.4
51.9
69.9
56.5
5.6
4.6
Apache-2.0
YOLOv10b
20.5
51.8
68.6
56.6
22.0
18.6
AGPL-3.0
YOLOv12m
20.2
51.4
68.0
55.8
23.5
19.8
AGPL-3.0
DEIM-RT-DETRv2-M
31.2
50.9
68.6
55.2
5.6
4.6
Apache-2.0
YOLO11m
20.1
50.5
67.1
55.0
13.5
11.3
AGPL-3.0
YOLOv10m
16.5
50.3
67.2
54.9
21.2
17.8
AGPL-3.0
RT-DETRv2-M
33.2
49.9
67.5
54.1
5.5
4.5
Apache-2.0
YOLOv8m
25.9
49.2
65.7
53.6
20.2
16.8
AGPL-3.0
RTMDet-m
24.7
49.0
66.7
53.6
5.5
4.4
GPL-3.0
Small Models
RF-DETR-S
32.1
53.0
72.1
57.3
5.6
4.4
Apache-2.0
DEIM-RT-DETRv2-S
20.0
49.1
66.1
53.3
5.7
4.6
Apache-2.0
DEIM-D-FINE-S
10.2
49.0
65.9
53.1
5.5
4.5
Apache-2.0
RT-DETR-R34
33.2
48.9
66.8
52.7
5.4
4.4
Apache-2.0
RT-DETRv2-S
22.0
48.1
65.1
52.1
5.5
4.5
Apache-2.0
YOLO26s
9.5
47.2
63.5
51.5
13.5
11.1
AGPL-3.0
YOLOv13s
9.0
46.8
63.5
50.6
13.0
10.4
AGPL-3.0
YOLOv12s
9.3
46.7
63.1
50.6
20.7
16.9
AGPL-3.0
Continued on next page
21


## Page 22

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
Table 11 – continued from previous page
Model
Params (M)
mAPval
50-95
mAPval
50
mAPval
75
F150
F175
License
RT-DETR-R18
22.0
46.4
63.7
50.3
5.4
4.3
Apache-2.0
YOLOv10s
8.1
45.7
62.3
49.8
18.6
15.2
AGPL-3.0
YOLO11s
9.4
45.5
62.0
49.3
12.8
10.4
AGPL-3.0
RTMDet-s
8.9
44.4
61.5
48.1
5.0
3.9
GPL-3.0
YOLOv8s
11.2
44.1
60.2
47.7
17.6
14.1
AGPL-3.0
Nano & Tiny Models
DEIM-D-FINE-N
10.2
49.0
65.9
53.1
5.5
4.5
Apache-2.0
RF-DETR-N
30.5
48.4
67.5
51.8
5.2
3.9
Apache-2.0
RTMDet-t
4.9
41.0
57.4
44.3
5.1
3.9
GPL-3.0
YOLOv13n
2.5
40.4
56.2
43.9
12.2
9.4
AGPL-3.0
YOLO26n
2.4
39.9
55.2
43.4
12.2
9.5
AGPL-3.0
YOLOv12n
2.6
39.7
55.0
42.9
16.7
13.1
AGPL-3.0
YOLO11n
2.6
38.6
53.9
42.0
12.1
9.3
AGPL-3.0
YOLOv10n
2.8
38.0
52.9
41.3
15.4
12.1
AGPL-3.0
YOLOv8n
3.2
36.5
51.4
39.8
14.8
11.5
AGPL-3.0
As evidenced by the exhaustive data in Table 11, the YOLO26 architecture establishes a highly
dominant Pareto frontier across all model scales, successfully bridging the gap between lightweight
CNN efficiency and heavy Transformer accuracy. At the high-capacity end, the YOLO26x vari-
ant achieves an exceptional 56.3% mAPval
50-95 with only 55.7M parameters. This firmly eclipses
contemporary heavyweight models such as YOLO11x (53.6% mAP at 56.9M parameters) and
fiercely rivals advanced Transformer architectures like DEIM-D-FINE-X (56.5% mAP at 61.7M
parameters), delivering comparable spatial reasoning without the massive computational overhead
typical of self-attention mechanisms.
Furthermore, this architectural efficiency seamlessly cascades down to the most constrained edge
environments. The YOLO26n model (2.4M parameters) secures 39.9% mAP, outperforming
equivalently scaled variants like YOLOv12n and YOLO11n. Across the entire YOLO26 family, the
robust F150 and F175 scores demonstrate a superior precision-recall balance. This validates the core
premise of the end-to-end, NMS-free design: by eliminating heuristic post-processing, the model
fundamentally reduces false positives and boundary discontinuities, resulting in a sharper, more
reliable perception pipeline.
6
Implications for Edge AI: Bridging the "Export Gap"
A pervasive challenge in the modern era of object detection is the "Export Gap"—the discrepancy
between the theoretical performance observed during GPU training and the actual latency realized on
deployed edge hardware [10]. This section analyzes how YOLO26 addresses this critical bottleneck
through its architectural constraints.
22


## Page 23

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
6.1
The Latency Bottleneck in Traditional Models
Prior State-of-the-Art (SOTA) models, including YOLOv8 through YOLOv13, relied heavily on
Distribution Focal Loss (DFL) to maximize mAP [22, 24, 27]. While mathematically precise, DFL
necessitates complex Softmax operations over discretized bins to calculate final coordinates [29].
On server-grade GPUs, these operations are negligible. However, on integer-arithmetic hardware
(such as NPUs in mobile devices or DSPs in drones), Softmax layers are difficult to quantize and
often become the primary latency bottleneck [30]. Consequently, a model that appears efficient in a
research paper often suffers severe throughput degradation when exported to real-world embedded
systems.
6.2
Deterministic Inference via Direct Regression
YOLO26 resolves this trade-off by reverting to a Direct Regression strategy, explicitly removing
the computational burden of DFL [57]. By decoupling representation learning from complex post-
processing, the architecture ensures that the inference graph consists solely of standard convolutional
and linear operations. This shift guarantees deterministic latency—the inference time remains
constant regardless of scene complexity or object density [10, 57]. This predictability is paramount
for safety-critical edge applications, such as autonomous driving and robotic navigation, where
timing violations can lead to catastrophic failures [57].
7
Future Directions
While YOLO26 establishes a new benchmark for real-time detection, several avenues for exploration
remain to fully bridge the gap between edge efficiency and cognitive intelligence.
Inherent Explainability and Trustworthiness: Currently, the "black box" nature of deep detectors
is addressed via post-hoc methods like Grad-CAM [58] or SHAP [59], which approximate the
model’s decision-making process after inference. A critical future direction is the development of
Inherent Explainability [60], where the detection head outputs not only the bounding box and class
but also a justification map or textual rationale (e.g., "Classified as Tumor due to irregular border
texture"). Embedding interpretability directly into the end-to-end pipeline will be transformative
for safety-critical domains such as medical diagnostics and autonomous defense, ensuring that
high-speed decisions are also transparent and verifiable.
Unified Spatiotemporal Perception: The NMS-free, deterministic nature of YOLO26 makes it
uniquely suited for video analysis. Traditional detectors often suffer from "flicker" in video streams
because NMS arbitrarily selects different boxes across frames. Future iterations could extend the
YOLO26 backbone to handle Spatiotemporal Object Detection natively. By treating time as a third
spatial dimension, the model could perform tracking and action recognition (e.g., "person running")
within the same single-pass forward pass, eliminating the need for separate tracking algorithms like
DeepSORT [61].
Test-Time Adaptation on the Edge: Finally, the static nature of trained models remains a limitation
in dynamic environments. Future work should explore Test-Time Adaptation (TTA) [62], allowing
the model to update its batch normalization statistics or lightweight adapter layers directly on
the edge device. This would enable a drone or medical device to "acclimatize" to new lighting
23


## Page 24

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
conditions or sensor noise profiles in real-time, maintaining peak accuracy without requiring a full
retraining cycle on a server.
8
Conclusion
This study presents a comprehensive analysis of the YOLO26 architecture, which advances the
real-time object detection paradigm by eliminating Non-Maximum Suppression (NMS) in favor of
a native end-to-end learning strategy. Supported by core innovations such as the MuSGD optimizer,
Small-Target-Aware Label Assignment (STAL), and ProgLoss scheduling, this transition success-
fully resolves historical latency bottlenecks. Furthermore, the adoption of a Direct Regression
head effectively closes the "Export Gap," ensuring deterministic latency for resource-constrained
edge devices. As demonstrated by extensive benchmarking against prior YOLO lineages and
contemporary Transformer architectures, YOLO26 establishes a dominant new speed-accuracy
Pareto front. Additionally, the analysis of the YOLOE-26 open-vocabulary module highlights the
framework’s unified capacity for zero-overhead, promptable multi-task detection. Ultimately, by
decoupling representation learning from heuristic post-processing, YOLO26 signals a fundamental
shift toward fully learnable, hardware-aware pipelines, providing a highly reliable blueprint for the
next generation of safety-critical Edge AI applications.
Acknowledgement(s)
The author explicitly acknowledges the use of Artificial Intelligence tools solely for the purpose
of language refinement and grammatical polishing; all scientific concepts, data, and technical
innovations presented herein are the original work of the author. All architectural interpretations
and mathematical formulations are author-derived abstractions intended for conceptual clarity
and do not represent official Ultralytics specifications. Official documentation is available at:
https://docs.ultralytics.com/models/yolo26/.
References
[1] Z. Zou, K. Chen, Z. Shi, Y. Guo, and J. Ye, “Object detection in 20 years: A survey,” Proceedings of the IEEE,
vol. 111, no. 3, pp. 257–276, 2023.
[2] Z.-Q. Zhao, P. Zheng, S.-t. Xu, and X. Wu, “Object detection with deep learning: A review,” IEEE transactions
on neural networks and learning systems, vol. 30, no. 11, pp. 3212–3232, 2019.
[3] L. Jiao, F. Zhang, F. Liu, S. Yang, L. Li, Z. Feng, and R. Qu, “A survey of deep learning-based object detection,”
IEEE access, vol. 7, pp. 128 837–128 868, 2019.
[4] S. Ren, K. He, R. Girshick, and J. Sun, “Faster r-cnn: Towards real-time object detection with region proposal
networks,” in Advances in neural information processing systems (NeurIPS), vol. 28, 2015.
[5] W. Liu, D. Anguelov, D. Erhan, C. Szegedy, S. Reed, C.-Y. Fu, and A. C. Berg, “Ssd: Single shot multibox
detector,” in European conference on computer vision (ECCV).
Springer, 2016, pp. 21–37.
[6] G. Jocher et al., “ultralytics/yolov5: v3.1 - bug fixes and performance improvements,” Oct. 2020. [Online].
Available: https://github.com/ultralytics/yolov5
[7] M. Sohan, T. Sai Ram, and C. V. Rami Reddy, “A review on yolov8 and its advancements,” in International
conference on data intelligence and cognitive informatics.
Springer, 2024, pp. 529–545.
[8] G. Jocher and J. Qiu, “Ultralytics YOLO11,” 2024. [Online]. Available: https://github.com/ultralytics/ultralytics
24


## Page 25

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
[9] S. Chakrabarty, P. Bishwas, S. Chakraborty, and O. Sarker, “Advancing defense and security with deep learning-
based detection and tracking,” in 2025 International Conference on Intelligent Computing and Knowledge
Extraction (ICICKE), 2025, pp. 1–6.
[10] C. Lyu, W. Zhang, H. Huang, Y. Zhou, Y. Wang, Y. Liu, S. Zhang, and K. Chen, “RTMDet: An empirical study of
designing real-time object detectors,” arXiv preprint arXiv:2212.07784, 2022.
[11] X. Xu, Y. Jiang, W. Chen, Y. Huang, Y. Zhang, and X. Sun, “DAMO-YOLO: A report on real-time object detection
design,” arXiv preprint arXiv:2211.15444, 2022.
[12] S. Xu, X. Wang, W. Lv, Q. Chang, C. Cui, K. Deng, G. Wang, Q. Dang, S. Wei, Y. Du et al., “PP-YOLOE: An
evolved version of yolo,” arXiv preprint arXiv:2203.16250, 2022.
[13] G. Jocher and J. Qiu, “Ultralytics yolo26,” 2026. [Online]. Available: https://github.com/ultralytics/ultralytics
[14] M. L. Ali and Z. Zhang, “The yolo framework: A comprehensive review of evolution, applications, and benchmarks
in object detection,” Computers, vol. 13, no. 12, p. 336, 2024.
[15] T. Diwan, G. Anirudh, and J. V. Tembhurne, “Object detection using yolo: challenges, architectural successors,
datasets and applications,” multimedia Tools and Applications, vol. 82, no. 6, pp. 9243–9275, 2023.
[16] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, “You only look once: Unified, real-time object detection,” in
Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 779–788.
[17] J. Redmon and A. Farhadi, “YOLO9000: Better, faster, stronger,” in Proceedings of the IEEE Conference on
Computer Vision and Pattern Recognition (CVPR), 2017, pp. 7263–7271.
[18] J. Redmon and A. Farhadi, “YOLOv3: An incremental improvement,” arXiv preprint arXiv:1804.02767, 2018.
[19] A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, “YOLOv4: Optimal speed and accuracy of object detection,”
arXiv preprint arXiv:2004.10934, 2020.
[20] C. Li, L. Li, H. Jiang et al., “YOLOv6: A single-stage object detector for industrial applications,” arXiv preprint
arXiv:2209.02976, 2022.
[21] C.-Y. Wang, A. Bochkovskiy, and H.-Y. M. Liao, “YOLOv7: Trainable bag-of-freebies sets new state-of-the-art
for real-time object detectors,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
Recognition (CVPR), 2023, pp. 7464–7475.
[22] G. Jocher,
A. Chaurasia,
and J. Qiu,
“Ultralytics YOLOv8,”
2023. [Online]. Available:
https:
//github.com/ultralytics/ultralytics
[23] C.-Y. Wang, H.-Y. M. Liao, and I.-H. Yeh, “YOLOv9: Learning what you want to learn through programmable
gradient information,” arXiv preprint arXiv:2402.13616, 2024.
[24] A. Wang, H. Chen, L. Li, K. Feng, S. Han, and G. Ding, “YOLOv10: Real-time end-to-end object detection,”
arXiv preprint arXiv:2405.14458, 2024.
[25] S. Chakrabarty, R. Chatterjee, S. Chakraborty, S. Roy Shuvo, and R. Chowdhury, “Drones in defense: Real-time
vision-based military target surveillance and tracking,” in 2025 3rd International Conference on Intelligent
Systems, Advanced Computing and Communication (ISACC), 2025, pp. 508–513.
[26] U. R. Team, “YOLOv12: Attention-centric real-time object detection,” arXiv preprint arXiv:2502.12588, 2025,
preprint.
[27] M. Lei, S. Li, Y. Wu, H. Hu, Y. Zhou, X. Zheng, G. Ding, S. Du, Z. Wu, and Y. Gao, “Yolov13: Real-time object
detection with hypergraph-enhanced adaptive visual perception,” arXiv preprint arXiv:2506.17733, 2025.
[28] N. Bodla, B. Singh, R. Chellappa, and L. S. Davis, “Soft-NMS – improving object detection with one line of
code,” in Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2017, pp. 5561–5569.
[29] X. Li, W. Wang, L. Wu, S. Chen, X. Hu, J. Li, J. Tang, and J. Yang, “Generalized Focal Loss: Learning qualified
and distributed bounding boxes for dense object detection,” Advances in Neural Information Processing Systems
(NeurIPS), vol. 33, pp. 21 002–21 012, 2020.
[30] A. Gholami, S. Kim, Z. Dong, Z. Yao, M. W. Mahoney, and K. Keutzer, “A survey of quantization methods for
efficient neural network inference,” arXiv preprint arXiv:2103.13630, 2021.
25


## Page 26

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
[31] H. Sharma, J. Park, D. Mahajan, E. Amaro, J. K. Kim, C. Shao, A. Mishra, and H. Esmaeilzadeh, “Bitfusion:
Bit-level pipelined multiplication and accumulation for efficient deep learning,” in Proceedings of the 45th Annual
International Symposium on Computer Architecture (ISCA), 2018, pp. 444–455.
[32] Z. Ge, S. Liu, F. Wang, Z. Li, and J. Sun, “YOLOX: Exceeding yolo series in 2021,” arXiv preprint
arXiv:2107.08430, 2021.
[33] K. Jordan, “Muon: A new optimizer for rapid convergence in llm training,” GitHub Blog Post, 2024. [Online].
Available: https://github.com/KellerJordan/Muon
[34] J. Liu et al., “Muon is scalable for llm training,” arXiv preprint arXiv:2502.16982, 2025.
[35] K. Jordan et al., “Orthogonal weight updates for spectral norm control in deep learning,” Technical Report, 2024.
[36] N. J. Higham, “Newton’s method for the matrix square root,” Mathematics of Computation, vol. 46, no. 174, pp.
537–549, 1986.
[37] M. Kisantal, Z. Wojna, J. Murawski, J. Naruniec, and K. Cho, “Augmentation for small object detection,” arXiv
preprint arXiv:1902.07296, 2019.
[38] H. Rezatofighi, N. Tchapmi, Q. Shao, S. Savarese, and A. Gheissari, “Generalized intersection over union: A
metric and a loss for bounding box regression,” in Proceedings of the IEEE/CVF Conference on Computer Vision
and Pattern Recognition (CVPR), 2019, pp. 658–666.
[39] C. Feng, Y. Zhong, Y. Gao, G. Gui, M. Tan, J. Zhang, and K. Ma, “Tood: Task-aligned one-stage object detection,”
in Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2021, pp. 3490–3499.
[40] G. Chen, H. Wang, K. Chen, Z. Li, and Z. Yi, “Towards large-scale small object detection: Survey and benchmarks,”
arXiv preprint arXiv:2207.14096, 2022.
[41] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, “Focal loss for dense object detection,” in Proceedings of
the IEEE international conference on computer vision, 2017, pp. 2980–2988.
[42] S. Hossain and D. Lee, “A curriculum learning approach for object detection,” arXiv preprint arXiv:1901.01890,
2019.
[43] I. Loshchilov and F. Hutter, “Sgdr: Stochastic gradient descent with warm restarts,” in International Conference
on Learning Representations (ICLR), 2017.
[44] A. Kendall, Y. Gal, and R. Cipolla, “Multi-task learning using uncertainty to weigh losses for scene geometry and
semantics,” in Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018,
pp. 7482–7491.
[45] M. Lin, Q. Chen, and S. Yan, “Network in network,” arXiv preprint arXiv:1312.4400, 2013.
[46] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE
Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770–778.
[47] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár, and C. L. Zitnick, “Microsoft coco:
Common objects in context,” in Proceedings of the European Conference on Computer Vision (ECCV), 2014, pp.
740–755.
[48] J. Li, S. Bian, Q. Xu, G. Liu, and B. Cheng, “Human pose regression with residual log-likelihood estimation,” in
Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2021, pp. 11 039–11 048.
[49] J. Ding, N. Xue, G.-S. Xia, X. Bai, W. Yang, M. Y. Yang, S. Belongie, J. Luo, M. Datcu, M. Pelillo et al., “Learning
roi transformer for oriented object detection in aerial images,” in Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition (CVPR), 2019, pp. 2849–2858.
[50] X. Yang, J. Yan, Z. Feng, and T. He, “R3det: Refined single-stage detector with feature refinement for rotating
objects,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 35, no. 4, 2021, pp. 3163–3171.
[51] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark
et al., “Learning transferable visual models from natural language supervision,” in International Conference on
Machine Learning (ICML).
PMLR, 2021, pp. 8748–8763.
[52] A. Gupta, P. Dollar, and R. Girshick, “Lvis: A dataset for large vocabulary instance segmentation,” in Proceedings
of the IEEE/CVF conference on computer vision and pattern recognition, 2019, pp. 5356–5364.
26


## Page 27

S. Chakrabarty; YOLO26: An Analysis of NMS-Free Framework for Object Detection
[53] S. Shao, Z. Li, T. Zhang, C. Peng, G. Yu, X. Zhang, J. Li, and J. Sun, “Objects365: A large-scale, high-quality
dataset for object detection,” in Proceedings of the IEEE/CVF international conference on computer vision (ICCV),
2019, pp. 8430–8439.
[54] N. Carion, F. Massa, G. Synnaeve, N. Usunier, A. Kirillov, and S. Zagoruyko, “End-to-end object detection with
transformers,” in Proceedings of the European Conference on Computer Vision (ECCV).
Springer, 2020, pp.
213–229.
[55] D. A. Hudson and C. D. Manning, “Gqa: A new dataset for real-world visual reasoning and compositional
question answering,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition
(CVPR), 2019, pp. 6700–6709.
[56] B. A. Plummer, L. Wang, C. M. Cervantes, J. C. Caicedo, J. Hockenmaier, and S. Lazebnik, “Flickr30k entities:
Collecting bounding boxes and continuous visual features for their image sentences,” in Proceedings of the IEEE
international conference on computer vision (ICCV), 2015, pp. 264–272.
[57] G. Jocher and J. Qiu, “Ultralytics yolov26: Native end-to-end object detection,” Ultralytics Technical Report,
2026. [Online]. Available: https://github.com/ultralytics/ultralytics
[58] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-cam: Visual explanations
from deep networks via gradient-based localization,” in Proceedings of the IEEE International Conference on
Computer Vision (ICCV), 2017, pp. 618–626.
[59] S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” in Advances in Neural
Information Processing Systems (NeurIPS), 2017, pp. 4765–4774.
[60] S. Chakrabarty, P. Bishwas, M. Bandyopadhyay, and J. Sublime, “Can we trust ai with our ears? a cross-domain
comparative analysis of explainability in audio intelligence,” IEEE Access, vol. 13, pp. 179 733–179 758, 2025.
[61] N. Wojke, A. Bewley, and D. Paulus, “Simple online and realtime tracking with a deep association metric,” in
Proceedings of the IEEE International Conference on Image Processing (ICIP), 2017, pp. 3645–3649.
[62] Y. Sun, X. Wang, Z. Liu, J. Miller, A. Efros, and M. Hardt, “Test-time training with self-supervision for
generalization under distribution shifts,” in International Conference on Machine Learning (ICML), 2020, pp.
9329–9339.
27
