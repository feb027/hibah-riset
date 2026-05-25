---
source_id: S014
title: LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking
source_url: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0342246&type=printable
source_file: docs/research/papers/S014-lighttrack-reid-a-lightweight-and-occlusion-robust-framework-for-multi.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S014-lighttrack-reid-a-lightweight-and-occlusion-robust-framework-for-multi.pdf
## PDF metadata
- format: PDF 1.4
- title: LightTrack-ReID: A lightweight and occlusion-robust framework for multi-object tracking
- author: Said Baz Jahfar Khan
- creator: Adobe InDesign 15.1 (Windows)
- producer: Adobe PDF Library 15.0
- creationDate: D:20260323102547+05'30'
- modDate: D:20260323102549+05'30'


## Page 1

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
1 / 19
 
 OPEN ACCESS
Citation: Khan SBJ, Zhang P, Kamal MM, 
Saudagar AKJ (2026) LightTrack-ReID: A 
lightweight and occlusion-robust framework 
for multi-object tracking. PLoS One 21(3): 
e0342246. https://doi.org/10.1371/journal.
pone.0342246
Editor: Aiqing Fang, Chongqing Normal 
University, CHINA
Received: August 30, 2025
Accepted: January 14, 2026
Published: March 25, 2026
Copyright: © 2026 Khan et al. This is an open 
access article distributed under the terms of 
the Creative Commons Attribution License, 
which permits unrestricted use, distribution, 
and reproduction in any medium, provided the 
original author and source are credited.
Data availability statement: All relevant data 
are within the paper.
Funding: This work was supported and funded 
by the Deanship of Scientific Research at 
Imam Mohammad Ibn Saud Islamic University 
(IMSIU) (grant number IMSIU-DDRSP2604).
RESEARCH ARTICLE
LightTrack-ReID: A lightweight and occlusion-
robust framework for multi-object tracking
Said Baz Jahfar Khan
1, Peng Zhang2,3*, Mian Muhammad Kamal
4, 
Abdul Khader Jilani Saudagar5*
1  School of Software Engineering, Northwestern Polytechnical University, Xi’an, Shaanxi, China, 2  Ningbo 
Institute of Northwestern Polytechnical University, Beilun, Ningbo, China, 3  School of Computer Science, 
Northwestern Polytechnical University, Xi’an, Shaanxi, China, 4  School of Electronic and Communication 
Engineering, Quanzhou University of Information Engineering, Quanzhou, Fujian, China, 5  Information 
Systems Department, College of Computer and Information Sciences, Imam Mohammad Ibn Saud Islamic 
University (IMSIU), Riyadh, Saudi Arabia 
* zh0036ng@nwpu.edu.cn (PZ); aksaudagar@imamu.edu.sa (AKJS)
Abstract 
This paper presents LightTrack-ReID, an advanced, lightweight, and occlusion-
resistant framework for MOT, designed for real-time performance in resource-limited 
environments. The framework includes a Lightweight Appearance Encoder (LAE) 
using MobileNetV3-Small, Transformer-Based Similarity Scoring (TBSS), Context 
Memory for Occlusion Handling (CMOH), and Adaptive Similarity Weighting (ASW) 
to enhance tracklet association in situations of heavy occlusion. These components 
offer compact 32-dimensional ReID features, adaptive similarity metrics, and con­
tinuous tracking within an efficient single-stage detection-to-tracklet association 
system. The proposed similarity and association model operates at approximately 
0.6 GFLOPs per frame (LAE approximately 0.5 GFLOPs + TBSS approximately 0.1 
GFLOPs). When integrated with the YOLOX-S detector, which remains the dominant 
computation, the full pipeline maintains approximately 30 FPS real-time performance 
on a GTX1080 GPU. It demonstrates robust performance on the MOT17 and MOT20 
benchmarks, achieving Higher Order Tracking Accuracy(HOTA) scores of 66.92 and 
66.6 and IDentity F1 score(IDF1) scores of 82.52 and 82.2, respectively, while signifi­
cantly reducing identity switches. These results confirm its strength and appropriate­
ness for use in real-world applications.
1  Introduction
Multi-Object Tracking (MOT) is a core task in computer vision that focuses on detect­
ing objects in video frames and associating them over time to establish coherent 
trajectories [1,2]. The main objective is to assign and sustain distinct IDs for objects 
over time, offering effective tracking despite challenges such as occlusions, abrupt 
movements, and complex interactions [2,3]. MOT encourages important applications, 


## Page 2

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
2 / 19
such as autonomous driving safety [4], enhanced surveillance systems [5], ecolog­
ical monitoring via animal tracking [6], enhanced human-robot cooperation [7], and 
effective video and sports analytics [8]. Effective multi-object tracking requires accu­
rate object detection in each frame and reliable association with existing tracklets, 
including assigning new identities to unmatched objects and terminating trajectories 
of objects leaving the scene [2,3,9,10] MOT methods are categorized into offline and 
online models. Offline methods process entire video sequences to improve accu­
racy, whereas online techniques, essential to real-time applications, process frames 
sequentially [11–13]. Online MOT predominantly adopts Tracking-by-Detection (TBD), 
which separates detection from association, or Joint Detection and Tracking (JDT), 
which combines both for improved computing efficiency [1,3,14]. Recent develop­
ments in TBD, propelled by methods such as YOLO, have significantly improved 
detection speed and accuracy, making it very suitable for real-time applications [15]. 
The association in TBD often employs the Hungarian method [7], which uses a cost 
matrix based on similarity measures such as Intersection over Union (IoU), Mahala­
nobis distance [16], and appearance-based cosine similarity [11,17]. 
Confidence-based filtering decreases false positives but may inadvertently eliminate 
legitimate detections. [18].
Occlusion is an important challenge in multi-object tracking, which commonly 
results in detection failures and trajectory fragmentation. Re-Identification (ReID) 
methods address this issue by reconnecting inactive tracklets between frames [19]. 
Methods such as DeepSort [20] use standalone ReID models, but JDE methods, 
exemplified by FairMOT [21], incorporate ReID into the detection framework. Recent 
developments leverage advanced deep learning techniques, such as attention mech­
anisms [22,23], graph neural networks [24], and hierarchical feature extraction [25], 
to model motion dynamics and contextual signals for occlusion-resistant tracking.
In this paper, we propose LightTrack-ReID, an innovative and highly robust 
multi-object tracking (MOT) framework that achieves superior effectiveness, as 
demonstrated by the comparative performance compared to the present state-of-the-
art method illustrated in Figure 1. [2,3,9,10].
The proposed framework integrates several novel components, including a Light­
weight Appearance Encoder (LAE), Transformer-Based Similarity Scoring (TBSS), 
Context Memory for Occlusion Handling (CMOH), and Adaptive Similarity Weighting 
(ASW), as shown in Figure 2.
The method also employs a single-stage detection-to-tracklet association structure 
that incorporates confidence similarity boosting and enhances detection confidence 
specifically for low-confidence tracking. Our key contributions are as follows:
•	 A Lightweight Appearance Encoder (LAE) utilizing MobileNetV3-Small, providing 
compact 32-dimensional ReID features for expedited inference;
•	 Transformer-Based Similarity Scoring (TBSS), integrating a single-layer transformer 
for strong, low-overhead association;
•	 Context Memory for Occlusion Handling (CMOH), which keeps track continuity 
during occlusions by using recent appearance embeddings;
Competing interests: No authors have compet­
ing interests.


## Page 3

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
3 / 19
Fig 1.  HOTA and IDF1 metric results on MOT17 (left) and MOT20 (right) test sets.
https://doi.org/10.1371/journal.pone.0342246.g001
Fig 2.  Overview of the proposed model architecture.
https://doi.org/10.1371/journal.pone.0342246.g002


## Page 4

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
4 / 19
•	 Adaptive Similarity Weighting (ASW), which easily changes the impact of IoU and appearance similarity in accordance 
with occlusion density.
Figure 3 presents bounding boxes and corresponding objects as produced by our model on the MOT17 dataset. The 
figure illustrates images grouped in three rows (one for each sequence), with each row showing the object before occlu­
sion, during occlusion, and after its reappearance, maintaining the same ID accurately recorded.
LightTrack-ReID shows outstanding outcomes on the MOT17 and MOT20 benchmarks, achieving HOTA scores of 
66.92 and 66.6 and IDF1 scores of 82.52 and 82.2, respectively—surpassing multiple existing methodologies while main­
taining real-time efficiency.
The main contribution of this research lies in the design of an efficiency-oriented tracking system rather than propos­
ing an entirely new framework. LightTrack-ReID proposes a synergistic integration of a compact appearance encoder, a 
single-layer association transformer, contextual memory, and occlusion-aware similarity regulation. This integration con­
currently provides real-time efficiency of 0.6 GFLOPs and robustness under significant occlusion, a feat not achieved by 
current high-complexity or limited-feature methodologies.
Note: Unless otherwise specified, the GFLOPs values, reported in this paper in this paper (e.g., 0.6 GFLOPs) corre­
spond solely to the computational expense of our association/similarity component (LAE + TBSS + lightweight context mod­
ules). The comprehensive FPS results encompass the whole detection and association pipeline. The computation of the 
detector (YOLOX) represents the primary computational burden; enhancements in our association module have minimal 
impact on the overall GFLOPs.
Fig 3.  Each row shows one sequence: the object before occlusion, during occlusion, and after reappearing with the same ID.
https://doi.org/10.1371/journal.pone.0342246.g003


## Page 5

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
5 / 19
2  Related work
Recent advancements in multi-object tracking (MOT) have mostly focused on improving robustness in crowded environ­
ments and computing efficiency. We examine relevant research in three important areas: (1) Tracking Frameworks, (2) 
Occlusion Handling, and (3) Re-Identification, focusing on the gaps that our method rectifies.
2.1  Tracking framework
Online tracking often refers to a tracking-by-detection framework, wherein objects are detected in each frame and linked 
to existing tracklets [1,3,14]. Kalman filtering [26] is widely used for motion prediction, whereas the Hungarian method [27] 
is usually used to address the data association problem. A cost matrix using Intersection over Union (IoU) or a mix of IoU 
[16] and appearance features is used to associate detections with existing tracks [28]. To address occlusions and crowded 
settings, multiple models include appearance similarity with motion cues. To reduce false positives and ghost tracks, 
various methods exclude low-confidence detections and associate only with high-confidence tracklets. Recent studies 
indicate that incorporating low-confidence detections associated with a second stage could recover missed objects and 
improve recall [29,30]. Multiple studies [31–33] have proposed multi-stage association frameworks that highlight more 
recently updated or higher-confidence tracklets during the first stages. Although successful, these multi-stage techniques 
may cause more identity switches due to inconsistent associations between stages. On the other hand, BoostTrack [18] 
and BoostTrack++ [17] use a single-stage association method. They use confidence boosting, Mahalanobis distance, 
and appearance similarities, such as visual embeddings and shape similarity, to achieve robust association. Boost­
Track++ improves confidence modeling, generating superior outcomes.
2.2  Occlusion handling
Occlusion presents a continual challenge in multi-object tracking (MOT), often disrupting detections and fragmenting 
trajectories. Researchers have developed various methods to maintain track continuity in partial or complete occlu­
sions. TrackFormer [22] uses a transformer-based attention mechanism to represent contextual and spatial relation­
ships between objects. It collects long-range relationships that enhance occlusion resilience; however, it suffers from 
high computational demands because of huge data requirements. MeMOT [34] uses a transformer-based architecture, 
including memory encoding for simultaneous detection and data association. It is highly effective in crowded environ­
ments with recurrent occlusions. SMILEtrack [14] uses a Siamese Learning Module and Patch Self-Attention to improve 
feature matching in situations of occlusion. Nonetheless, its fixed similarity metric limits adaptability to varying occlusion 
levels, potentially reducing association accuracy over time. Occlusion-Aware Attention (OAA) [35] uses a self-supervised 
mask loss to reduce occluded background areas, therefore focusing the model’s attention on visible features. Although it 
improves robustness in dense environments, its detection-centric methodology neglects motion continuity, leading to iden­
tity switches. DetTrack [36] addresses full occlusion by combining spatio-temporal information with motion cues. It predicts 
object positions based on motion in missing detections, ensuring continuity without the necessity for explicit visual input. 
MSPNet [37] (Motion-guided and Occlusion-aware Multi-Object Tracking) integrates motion-guided aggregation with an 
occlusion-aware attention mechanism. Its hierarchical spatial association considerably improves performance in situations 
with frequent occlusion and camera movements. PSMOT [38] uses position-sensitive pooling to maintain spatial context 
within feature maps, boosting robustness against occlusion and lower identity changes in noisy environments.
2.3  Re-identification
Re-identification (Re-ID) ensures stable identity tracking across frames, especially after occlusion or missed detections. It 
uses visual, motion, or combined cues to accurately re-associate missing tracklets. FairMOT [21] integrates Re-ID directly 
into its joint detection and tracking (JDT) framework, producing embeddings simultaneously with detections, allowing 


## Page 6

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
6 / 19
real-time identity association. BoT-SORT [28] adopts a deep CNN-based model, such as OSNet, to extract distinctive 
appearance features, providing more resilience in occluded and crowded environments. BoostTrack [18] combines 
motion-based prediction with a simplified appearance model (e.g., SHIP) for hybrid association. It achieves outstanding 
efficiency without significant feature extraction, but it can fail when appearance or motion features lack distinctiveness. 
MOTFR [39] uses a Feature Purification Module (FPM) that eliminates identity-discriminative features via feature recod­
ing, thereby providing accurate object tracking on visually complex occasions, including during occlusions. Posture-guided 
Re-ID methods [40] utilize human position estimation and spatial attention to coordinate visible body parts across frames. 
These methods can improve re-ID in scenarios with partial occlusion; nevertheless, they generally need large labeled 
datasets., hence raising complexity and training expenses. YOLO11-JDE [41] includes a self-supervised Re-ID compo­
nent inside the YOLO detection framework. It uses triplet loss with semi-hard negative mining to acquire embeddings 
without identity-labeled data, enabling rapid real-time implementation. However, overall tracking accuracy remains rela­
tively low. imprAsso [42] uses a deep Re-ID model to extract appearance features from each detection. The cosine sim­
ilarity between embeddings allows accurate track association, even in an environment of occlusion. ConfTrack [43] uses 
a Re-ID model to produce embeddings for detections and tracks. It associates them through cosine similarity, modified 
by detection confidence for improved reliability. These methods fail in situations of heavy occlusion and lack the capacity 
for dynamic similarity adjustments. Adaptive Feature Fusion with Local High Discriminant Features effectively combines 
motion cues, global appearance, and detailed local features. By updating fusion weights according to the occlusion condi­
tion, it maintains excellent Re-ID performance even in visually ambiguous or crowded environments [44].
Despite their developing ability, several methods are impeded by high computational costs, restricting their use on 
resource-limited platforms. In addition, identity switches remain, eventually affecting key performance indicators such as 
HOTA, Multiple Object Tracking Accuracy(MOTA), and IDF1.
3  Proposed method
Algorithm 1 outlines LightTrack-ReID, a lightweight tracking-by-detection framework for multi-object tracking (MOT), spe­
cifically for environments that suffer from heavy occlusion and limited computational resources (e.g., Ubuntu 16.04 with 
CUDA-limited GPUs). It unites YOLOX detections with a Similarity Model for Re-Identification (ReID), consisting of seven 
novel components: Frame-Level Tensor Caching (FLTC), Adaptive Pair Sampling (APS), Lightweight Appearance Encoder 
(LAE), Transformer-Based Similarity Scoring (TBSS), Context Memory for Occlusion Handling (CMOH), Adaptive Simi­
larity Weighting (ASW), and a triplet loss for training. The Similarity Model is trained on MOT17 and MOT20 to improve 
association accuracy. The following subsections explain each component, illustrating their design and rationale, supported 
by mathematical formulations.
3.1  Novelty of proposed components
Although each component draws inspiration from existing MOT techniques, our design places strong emphasis on compu­
tational reduction and collaborative functionality for deployment under resource constraints. Specifically,
•	 LAE generates compact 32-dimensional embeddings, reducing computational cost by approximately 80% compared to 
conventional ReID encoders [28].
•	 TBSS employs a single-layer transformer with restricted attention computation, avoiding the overhead of multi-layer 
transformer architectures [22,34].
•	 CMOH maintains only the K = 10 most recent features, ensuring identity continuity during short-term occlusions without 
expensive long-range memory modules.
•	 ASW enables real-time similarity fusion conditioned on occlusion density, in contrast to static or fixed similarity 
weighting [14].


## Page 7

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
7 / 19
These design choices achieve a favorable balance between robustness and efficiency that prior approaches have not 
addressed within a unified framework.
Each component provides distinct enhancements over existing techniques, focusing on computational efficiency and 
tracking robustness. The LAE uses MobileNetV3-Small to create compact 32-dimensional ReID features. In contrast to 
more complicated encoders such as OSNet in BoT-SORT [28], which prioritize feature richness at a more computational 
cost, or the simplified SHIP model in BoostTrack [18], which affects discriminative power, LAE optimizes 
MobileNetV3-Small for MOT-specific ReID tasks, establishing a balance between efficiency and feature quality. The TBSS 
uses a single-layer transformer with four attention heads for similarity evaluation, combining appearance and IoU fea­
tures. Unlike TrackFormer [23], which uses multi-layer transformers for concurrent detection and tracking, or TransMOT 
[24], which uses spatial-temporal graph transformers, TBSS focuses on lightweight association, making it appropriate for 
real-time applications. The CMOH maintains continuity during occlusions by maintaining the K = 10 most recent appear­
ance features, a simpler method compared to transformer-based memory in MeMOT [34] or graph neural networks [24]. 
This design prioritizes efficiency and implementation simplicity, making it suitable for resource-limited environments. The 
ASW dynamically balances IoU and appearance similarities according to occlusion weight, in contrast to the static met­
rics utilized in SMILEtrack [14], which are ineffective with changeable occlusion levels. By adjusting weights by a sigmoid 
function, ASW improves association robustness across many contexts. These components empower LightTrack-ReID to 
successfully tackle occlusion challenges, with performance evaluated in the experiments section.
3.1.1  Differences from related work and design choices.  LightTrack-ReID improves MOT in resource-limited, 
occlusion-prone environments by introducing novel components that address limitations in previous methods. The 
Lightweight Appearance Encoder (LAE) adapts MobileNetV3-Small to produce compact 32-dimensional ReID 
embeddings, unlike OSNet’s high-dimensional features [28] or FairMOT’s integrated ReID [21], focusing efficiency on 
edge devices. Transformer-Based Similarity Scoring (TBSS) utilizes a single-layer, four-head transformer for tracklet 
association, in contrast to TrackFormer’s complex multi-layer framework [22], enabling a lightweight yet robust matching 
process. Context Memory for Occlusion Handling (CMOH) retains K = 10 recent features, providing a simpler replacement 
to MeMOT’s transformer-based memory [34] and DeepSORT’s static buffers [20], which enhances short-term occlusion 
resilience with minimal overhead. Adaptive Similarity Weighting (ASW) dynamically balances Intersection over Union 
(IoU) and appearance through a sigmoid function, addressing the inflexibility of static fusion in different occlusion contexts 
[44]. Frame-Level Tensor Caching (FLTC) and Adaptive Pair Sampling (APS) improve training efficiency by caching frame 
tensors and balancing pair sampling, and unlike ByteTrack’s conventional data management [29], they improve scalability 
without compromising inference. These advances combined provide efficient, occlusion-resistant tracking designed for 
practical applications.
Our approach therefore contributes a practical, deployment-oriented innovation, illustrating that a meticulously 
designed lightweight architecture can surpass more substantial models in crowded environments. This distinguishes our 
work from accuracy-centric transformer trackers or rudimentary ReID-free lightweight methodologies.
3.2  Framework overview
LightTrack-ReID processes video frames (t), in which YOLOX produces detections Dt = {dt,i = (bt,i, ct,i) | i = 1, . . . , Nt}, with 
(bt,i = (x, y, w, h)) indicating the bounding box and (ct,i) indicating the confidence score. Tracklets Tt = {Tt,j} | j = 1, . . . , Mt} 
retain previous detections and visual features. The SimilarityModel calculates similarity evaluations (si,j) between detec­
tions and tracklets, enhanced by contextual memory and adaptive weighting, for Hungarian matching. Training improves 
the SimilarityModel for robust association, especially in an environment of occlusion.
YOLOX detections are first processed by the Lightweight Appearance Encoder (LAE) to extract 32-dimensional appearance 
features. The mentioned features, along with geometric information, are passed to the Transformer-Based Similarity Scoring 
(TBSS) module for the computation of pairwise similarities. The Context Memory for Occlusion Handling (CMOH) preserves 


## Page 8

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
8 / 19
short-term appearance history to ensure identity continuity during occlusion. The Adaptive Similarity Weighting (ASW) module 
integrates appearance and IoU similarities based on occlusion density, producing the final cost matrix for Hungarian matching.
3.3  Frame-level tensor caching (FLTC)
Frame-level tensor caching improves training efficiency by storing a single tensor for each frame, so increasing per­
formance without affecting inference accuracy. For a sequence S = {Ft}TS
t=1, each frame’s tensor Γt = (Bt, It, Gt) con­
tains detection boxes Bt = {bt,i | i = 1, . . . , Nt}, 224x224 RGB images It = {It,i | i = 1, . . . , Nt}, and ground-truth IDs 
Gt = {gt,i | i = 1, . . . , Nt}: Γ = {Γt | t = 1, . . . , TS} Located in tensor_cache_dir, this reduces I/O from about 100,000 pair 
tensors to about two thousand frame tensors, reducing loading time from hours to roughly 2–5 minutes (uncached) or less 
than 30 seconds (cached, achieving a speedup of approximately 3–5 times). Caching ensures reproducible training and 
contributes to slight improvements in HOTA and IDF1 scores, as well as reduced identity switches. The cost is around 
0.001 GFLOPs per tensor input/output.
3.4  Adaptive pair sampling (APS)
Adaptive pair sampling balances the training dataset ((∼135,000 samples, with 80% assigned for training and 20% for 
validation) by restricting pairings to MAX_PAIRS_PER_FRAME = 50 For frame t, the positive (identical ID) and negative 
(different ID) pairings are:
	
Pt =
(
{(i, j) | gt,i = gt,j} ∪{(i, j) | gt,i ̸= gt,j}
)
sampled up to 50	
(1)
using labels yi,j ∈{0, 1}. This training-exclusive feature improves data equilibrium at a minimal expense (∼0.01 GFLOPs).
3.5  Lightweight appearance encoder (LAE)
The appearance encoder extracts 32-dimensional ReID features via MobileNetV3-small (∼0.5 GFLOPs). For an input 
image It,i ∈R224×224×3, the encoder fθ produces a compact feature embedding:
	
at,i = fθ(It,i) ∈R32	
(2)
where the encoder is defined as:
	
fθ(It,i) = Pool(Conv(MobileNetV3(It,i)))	
(3)
The parameters θ are trained for producing distinctive appearance features suitable for person Re-Identification (ReID), 
with inference happening approximately 0.01 seconds per image.
In practice, the feature dimensionality was determined empirically. Among the 16D, 32D, and 64D configurations tested, 
32-dimensional embeddings provided the best balance between accuracy and speed, achieving near-optimal tracking 
performance while minimizing computation for real-time inference.
3.6  Transformer-based similarity scoring (TBSS)
The SimilarityModel evaluates a similarity score (si,j ∈[0, 1]) between detection (dt,i) and tracklet (Tt,j). Inputs include boxes 
(bt,i), (bt–1,j), and IoU:
	
IoU(bt,i, bt–1,j) = Area(bt,i ∩bt–1,j)
Area(bt,i ∪bt–1,j),
	
(4)


## Page 9

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
9 / 19
and appearance features (at, i), (at – 1, j),forming a feature vector:
	
xi,j = [bt,i, bt–1,j, IoU, at,i, at–1,j] ∈R73.	
(5)
A linear projection, single-layer transformer (4 heads, around 0.1 GFLOPs), and sigmoid activation provide:
	
zi,j = Linear(xi,j),
hi,j = Transformer(zi,j),
si,j = σ(Linear(hi,j))	
(6)
The transformer combines appearance and spatial features for robust association. Reason for Architectural Design. 
The single-layer transformer was chosen to optimize computational efficiency and association accuracy in environments 
with restricted resources (e.g., Ubuntu 16.04, GTX 1080). In contrast with complex frameworks like TrackFormer [22], 
which uses multi-layer transformers for simultaneous detection and tracking, our single-layer design is only dedicated to 
tracklet association, hence reducing computing cost. The selection of four attention heads follows standard practices in 
lightweight trans formers [45], optimizing the integration of features (appearance, IoU) while preserving efficiency. Initial 
experiments indicated that four heads offer adequate capacity for MOT settings, including brief occlusions, with perfor­
mance specifics described in the Ablation Study Section. A single-layer transformer was utilized to balance attention 
modeling capacity and computational efficiency. Experiments with more complex configurations produced minor accuracy 
improvements but significantly raised inference costs; thus, the one-layer design was selected as the most pragmatic 
option for real-time tracking.
3.7  Context memory for occlusion handling (CMOH)
To reduce occlusion-induced track fragmentation, a CMOH stores the K = 10 most recent 32-dimensional appearance 
features for each tracklet Tt,j:
	
Mt,j = {at–k,j}
min(K,tj)
k=1
,	
(7)
where tj denotes the age of the tracklet. For occluded tracklets, a contextual feature is calculated as
	
actx
t,j =
1
|Mt,j|
∑
a∈Mt,j
a,
	
(8)
supporting similarity scoring through
	
sctx
i,j = σ
(
Linear
(
Transformer
(
Linear
(
[bt,i, bt–1,j, IoU, at,i, actx
t,j ]
))))
.	
(9)
This simple memory buffer was selected compared to more complicated alternatives, such as transformer-based memory in 
MeMOT [34] or graph-based contextual modeling [24], because of its minimal processing cost and suitability for MOT17/MOT20 
situations, characterized by common short-term occlusions. Limiting memory to K = 10 improves resource use and helps 
maintain tracking continuity. The effect on efficiency is evaluated in Ablation Study Section. This choice of K = 10 was empirically 
validated, as larger memory sizes offered negligible performance gains while increasing computational and memory costs.
3.8  Adaptive similarity weighting (ASW)
Adaptive similarity weighting balances IoU and appearance similarities with respect to occlusion density. The cost matrix 
for Hungarian matching is delineated as


## Page 10

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
10 / 19
	
Ci,j = 1 – wt · si,j – (1 – wt) · IoU(bt,i, bt–1,j)	
(10)
where wt = σ
(
Nocc
t
Nt
)
, with Nocc
t
 indicating the number of occluded detections (i.e., IoU overlap > 0.5), and Nt denoting the 
overall number of detections. This dynamic weighting ensures a strong association across various environments, improv­
ing the HOTA score by adapting to different amounts of occlusion.
3.9  Training Objective and Rationale
The SimilarityModel, including the appearance encoder parameters (θ) and Transformer weights, is trained to identify 
appearance features and predict identity-matching scores. To ensure that the appearance embeddings (at,i) can distin­
guish between various identities, a triplet loss is used:
	
Ltriplet = max
(
∥aa – ap∥2
2 – ∥aa – an∥2
2 + m, 0
)
,	
(11)
where m = 1.0, and aa, ap, and an represent the anchor, positive, and negative samples, respectively. The model simulta­
neously trains to predict similarity scores si,j or sctx
i,j  that accurately reflect identity associations, utilizing a binary cross-
entropy loss function:
	
LBCE = –
∑
(i,j)
[
yi,j log(si,j) + (1 – yi,j) log(1 – si,j)
]
,
	
(12)
where yi,j ∈{0, 1} indicates if detection i and tracklet j correspond to the exact same identity. The total loss is the straight­
forward sum of the two elements:
	
L = Ltriplet + LBCE.	
(13)
Training uses MOT17/MOT20 (80% train, 20% validation) for 20 epochs with Adam (lr = 0.001). Images are resized to 
224x224, normalized to [0,1], with augmentations: random flip (50%), crop (10% padding), color jitter (0.2). Hyperparame­
ters (m = 1.0, K = 10) were tuned on MOT17 validation.
Algorithm 1 LightTrack-ReID Tracking Procedure
1: Input: frames {Ft}T
t=1
2: Output: Object tracks T
3: Initialize tracks T ←∅, memory buffer M ←∅, max size K ←10
4: for t = 1 to T do
5:   Apply CMC
6:   Get Dt = {(bt,i, ct,i)}Nt
i=1 from YOLOX on frame Ft
7:   Filter Dt by (e.g., ct,i > Threshold)
8:   Forecast track states with Kalman filter
9:   Extract appearance features at,i ←fθ(bt,i)
10: for each track Tj ∈T  do
11:     Prepare context memory Mj
12:     Get context-aware feature actx
t,j =
1
|Mj|
∑
a∈Mj a
13:   end for
14:   Get similarity scores si,j using transformer with at,i and actx
t,j ▷(TBSS: Transformer-Based Simi­
larity Scoring)
15:   Get occlusion weight wt = σ
(
Nocc
t
Nt
)
 ▷ ASW: Adaptive Similarity Weighting
16:   Define cost matrix:
17:   Ci,j = 1 – [wt · si,j + (1 – wt) · IoU(bt,i, bt–1,j)] ▷ (Combines TBSS and ASW before Hungarian matching)


## Page 11

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
11 / 19
18:   Hungarian algorithm on Ci,j
19:   for (i, j) in match set do
20:     Update track Tj with detection dt,i, Kalman update
21:   end for
22:   for d in unmatched detections do
23:     Initialize new track and add to T
24:   end for
25:   for Tj in unmatched tracks do
26:     Mark as occluded or terminate if inactive for too long
27:   end for
28:   Update context memory Mj for each track Tj ∈T
29:   Tracklet management
30: end for
31: return T
4  Experiments
4.1  Experimental settings
Datasets. We evaluate our method using two common pedestrian tracking benchmarks: MOT17 [57] and MOT20 [58], 
following the “private detection” procedure. MOT17 has sequences captured using fixed and moving cameras; MOT20 
highlights crowded environments. Both datasets provide training and test sets, even though they do not include formal val­
idation sets. In our ablation studies, we adhere to the procedures described in [29,59], using the first half of each MOT17 
training set for training and the remaining half for validation.
Metrics. We measure performance with the standard CLEAR metrics [60], which contain Multiple Object Tracking Accuracy 
(MOTA), False Positives (FP), False Negatives (FN), and ID Switches (IDSW). In addition, we use IDF1 [61] and Higher-Order 
Tracking Accuracy (HOTA) [15] for evaluating identity maintenance and complete tracking performance. Tracking speed (in FPS/
Hz) can be measured, though it can change according to the hardware. MOTA is derived from false positives (FP), false negatives 
(FN), and ID switches (IDSW), and primarily reflects detection performance due to the dominant influence of FP and FN. IDF1 
focuses on detection association, whereas HOTA combines detection, association, and localization accuracy into one metric.
Implementation details. LightTrack-ReID is implemented on a resource-limited computer running Ubuntu 16.04, 
containing an NVIDIA GTX 1080 GPU (8GB VRAM) and an Intel Core i7-6700 CPU (3.4 GHz, 32GB RAM). To clarify, the 
0.6 GFLOPs figure refers exclusively to the association stage, which encompasses the Lightweight Appearance Encoder 
(about 0.5 GFLOPs) and the single-layer transformer similarity block (around 0.1 GFLOPs). The YOLOX-S detector 
contributes to approximately 26.8 GFLOPs, being the predominant portion of end-to-end computation. The proposed 
association consequently results in an additional computational expense of less than 3%, enabling the system to maintain 
approximately 30 FPS real-time performance on GTX1080 hardware.
The software package uses Python 3.8 and PyTorch 1.9.1, using CUDA 10.2 for GPU acceleration. Dependencies 
include OpenCV 4.5.3 for image processing, NumPy 1.19.5 for numerical calculations, and the TrackEval package for 
multi-object tracking evaluation. The model uses a pretrained YOLOX from ByteTrack [29] for detection and uses 
MobileNetV3-small to extract 32-dimensional ReID features. A lightweight transformer with four heads calculates simi­
larity using appearance and soft Intersection over Union (IoU). Occlusion is handled with memory buffers and adaptive 
weighting. The model is trained on MOT17 and MOT20 for 20 epochs with triplet loss and the Adam optimizer (learning 
rate = 0.001), consuming approximately 10 hours on a GTX 1080 GPU.
4.2  Ablation study
We evaluate the impact of each inference-stage component of LightTrack-ReID on the MOT17 train set using common track­
ing metrics: HOTA, MOTA, IDF1, and IDS. The baseline uses YOLOX detections, motion prediction using a Kalman filter, 


## Page 12

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
12 / 19
development of an IoU-based cost matrix, and Hungarian matching for association. It additionally incorporates 
confidence-based filtering and exponential moving average (EMA) for state smoothing, elements frequently used in modern 
tracking systems. We progressively integrate LAE derived appearance encoder for 32-dimensional ReID features, TBSS, 
CMOH temporal appearance, and ASW to balance IoU and appearance scores. Training-specific methods are excluded.
To assess the impact of every element in our tracking framework, we performed an ablation study using the MOT17 
and MOT20 validation datasets. Table 1 and Figure 4 present the results on MOT17, whereas Table 2 and Figure 5 report 
the outcomes on MOT20, highlighting the effect of adding each module individually to the baseline. Both figures use a 
dual-axis configuration: HOTA, MOTA, and IDF1 are shown as line graphs on the left vertical axis, while the number of ID 
switches (IDSW) is shown as green bars on the right. The x-axis begins with the baseline configuration, followed by incre­
mental additions of each component.
The cumulative ablation study on MOT17 (Table 3, Figure 6) begins with the baseline configuration, which achieves a 
HOTA of 66.13, MOTA of 74.8, IDF1 of 77.3, and IDSW of 227, indicating clear limitations in handling occlusions. Incorpo­
rating the Lightweight Appearance Encoder (LAE) improves HOTA to 70.88, MOTA to 79.0, IDF1 to 81.97, while reducing 
IDSW to 168, demonstrating its effectiveness in enhancing appearance representation. The incorporation of 
Transformer-Based Similarity Scoring (TBSS) elevates HOTA to 73.38, MOTA to 81.2, and IDF1 to 84.47, while decreas­
ing IDSW to 138, thus enhancing association precision. The incorporation of Context Memory for Occlusion Handling 
Table 1.  Ablation results for individual components on the MOT17 public validation split.
Configuration
HOTA
MOTA
IDF1
IDSW
Baseline
66.13
74.8
77.3
227
Baseline + LAE
70.88
79.0
81.97
168
Baseline + TBSS
68.10
76.40
79.25
195
Baseline + CMOH
68.52
76.90
79.85
159
Baseline + ASW
67.30
75.53
78.40
196
https://doi.org/10.1371/journal.pone.0342246.t001
Fig 4.  Ablation study: individual component performance on the MOT17 validation set.
https://doi.org/10.1371/journal.pone.0342246.g004


## Page 13

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
13 / 19
(CMOH) enhances performance to HOTA 74.88, MOTA 82.6, IDF1 86.07, and significantly reduces IDSW to 80, demon­
strating its efficacy in preserving track continuity during occlusion.
On MOT20 (Table 4, Figure 7), the baseline achieves HOTA 56.17, MOTA 69.92, IDF1 73.72, and IDSW 1120, high­
lighting the significant challenges associated with dense crowd tracking. With LAE, performance improves to HOTA 60.38, 
MOTA 73.51, IDF1 77.15, while IDSW reduces to 952. The addition of TBSS raises HOTA to 63.94, MOTA to 76.61, and 
IDF1 to 80.01, while lowering IDSW to 882, confirming its efficacy in enhancing reliable matching. The implementation of 
CMOH increases HOTA to 65.74, MOTA to 78.21, IDF1 to 81.51, and substantially reduces IDSW to 701, thereby dramat­
ically reducing occlusion-related mistakes. The concluding phase, incorporating ASW, achieves HOTA 66.7, MOTA 78.9, 
and IDF1 82.3, but IDSW stays unchanged at 701, providing incremental enhancements with minimal supplementary 
effect.
4.3  Comparison with other methods
Table 5 presents an in-depth evaluation of the proposed method, LightTrack-ReID, compared to other state-of-the-art 
multi-object tracking (MOT) methods on the MOT17 and MOT20 benchmarks. Figure 1 presents a graphical representa­
tion of the HOTA and IDF1 scores, highlighting the superior effectiveness and robustness of our model. LightTrack-ReID 
shows outstanding results across all major evaluation standards, achieving the best HOTA 66.92, MOTA 82.81, and IDF1 
Table 2.  Individual Component Ablation on MOT20 (Validation Split).
Configuration
HOTA
MOTA
IDF1
IDSW
Baseline
56.17
69.92
73.72
1120
Baseline + LAE
60.38
73.51
77.15
952
Baseline + TBSS
58.50
72.42
75.31
1020
Baseline + CMOH
58.25
71.83
74.63
995
Baseline + ASW
58.14
71.61
74.72
1025
https://doi.org/10.1371/journal.pone.0342246.t002
Fig 5.  Ablation study: individual component performance on the MOT20 validation set.
https://doi.org/10.1371/journal.pone.0342246.g005


## Page 14

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
14 / 19
82.52 scores on MOT17 while, at the same time, maintaining a relatively low number of identity switches (IDSW). In the 
challenging MOT20 dataset, which features common occlusions and high object density, the proposed method achieves a 
HOTA of 66.6, MOTA of 79.1, and IDF1 of 82.2, while also keeping the lowest number of ID switches (753) when com­
pared to all other methods tested.
The results clearly show the success of LightTrack-ReID in maintaining unchanged object identification, espe­
cially in conditions with significant occlusion. The method includes a highly effective Re-Identification (ReID) module 
that enhances identification association across frames, allowing accurate continuous tracking even when objects are 
Table 3.  Cumulative component ablation on MOT17 (Public Validation Split).
Configuration
HOTA
MOTA
IDF1
IDSW
Baseline
66.13
74.8
77.3
227
Baseline + LAE
70.88
79.0
81.97
168
Baseline + LAE + TBSS
73.38
81.2
84.47
138
Baseline + LAE + TBSS + CMOH
74.88
82.6
86.07
80
Baseline + LAE + TBSS +CMOH + ASW
75.63
83.2
86.63
79
https://doi.org/10.1371/journal.pone.0342246.t003
Fig 6.  Ablation study: cumulative component performance on the MOT17 validation set.
https://doi.org/10.1371/journal.pone.0342246.g006
Table 4.  Cumulative component ablation on MOT20 (Validation Split).
Configuration
HOTA
MOTA
IDF1
IDSW
Baseline
56.17
69.92
73.72
1120
Baseline + LAE
60.38
73.51
77.15
952
Baseline + LAE + TBSS
63.94
76.61
80.01
882
Baseline + LAE + TBSS + CMOH
65.74
78.21
81.51
701
Baseline + LAE + TBSS + CMOH + ASW
66.7
78.9
82.3
701
https://doi.org/10.1371/journal.pone.0342246.t004


## Page 15

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
15 / 19
Fig 7.  Ablation study: cumulative component performance on the MOT20 validation set.
https://doi.org/10.1371/journal.pone.0342246.g007
Table 5.  Comparison of state-of-the-art methods on MOT17 and MOT20 benchmarks.
Method
MOT17
MOT20
HOTA
MOTA
IDF1
IDSW
HOTA
MOTA
IDF1
IDSW
FairMOT [21]
59.3
73.7
72.3
3303
54.6
61.8
67.3
5243
ByteTrack [29]
63.1
80.3
77.3
2196
61.3
77.8
75.2
1223
QuoVadis [45]
63.1
80.3
77.7
2103
61.5
77.8
75.7
1187
BPMTrack [46]
63.6
81.3
78.1
2010
62.3
78.3
76.7
1314
UTM [47]
64.0
81.8
78.7
1431
62.5
78.2
76.9
1228
FineTrack [48]
64.3
80.0
79.5
1272
63.6
79.1
79.0
980
StrongSORT++ [30]
64.4
79.6
79.5
1194
62.6
73.8
77.0
770
BASE* [49]
64.5
81.9
78.6
1281
63.5
78.2
77.6
984
Deep OC-SORT [50]
64.9
79.4
80.6
1023
63.9
75.6
79.2
779
BoT-SORT [28]
65.0
80.5
80.2
1212
63.3
77.8
77.4
1313
SparseTrack [51]
65.1
81.0
80.1
1170
63.5
78.1
77.6
1120
MotionTrack [25]
65.1
81.1
80.1
1140
62.8
78.0
76.5
1165
LG-Track [52]
65.4
81.4
80.4
1125
63.4
77.8
77.4
1161
StrongTBD [53]
65.6
81.6
80.8
954
64.6
78.0
77.0
1101
PIA2 [54]
66.0
82.2
81.1
1026
64.7
78.5
79.0
1023
ImprAsso [42]
66.4
82.2
82.1
924
64.6
78.6
78.8
992
SUSHI* [55]
66.5
81.1
83.1
1149
64.3
74.3
79.8
706
ConfTrack [43]
65.4
80.0
81.2
1155
64.8
77.2
80.2
702
BoostTrack [18]
66.4
80.6
81.8
1086
66.2
77.2
81.5
827
BoostTrack++ [17]
66.6
80.7
82.2
1062
66.4
77.7
82.0
762
CoNo-Link* [56]
67.1
82.7
83.7
1092
65.9
77.5
81.8
956
LightTrack-ReID (Ours)
66.92
82.81
82.52
992
66.6
79.1
82.2
753
https://doi.org/10.1371/journal.pone.0342246.t005


## Page 16

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
16 / 19
temporarily hidden or disappear. Compared to current methods like BoostTrack++, ConfTrack, and ImprAsso, which 
similarly use ReID techniques, LightTrack-ReID demonstrates enhanced identity retention and reduced tracking failures in 
occluded environments.
The results indicate that LightTrack-ReID provides an accurate and occlusion-resistant tracking method, suitable 
for real-world applications that include frequent object interactions and occlusions. With a frame rate of 30 FPS on the 
MOT17 benchmark, it achieves real-time performance.
4.4  Limitations
Despite LightTrack-ReID’s outstanding tracking accuracy and low computational demands, specific limitations remain. The 
global Adaptive Similarity Weighting (ASW) uses a uniform occlusion weight across the entire frame, potentially overlook­
ing local occlusion variations, whereas the Context Memory for Occlusion Handling (CMOH) has limitations in addressing 
long-term or recurrent occlusions due to its limited buffer capacity (K = 10). Moreover, the appearance encoder trained on 
MOT17/MOT20 may exhibit limited generalization to novel domains characterized by diverse illumination or camera move­
ment. Future enhancements will focus on localized ASW weighting, hierarchical memory architectures, and domain-
adaptive training to improve robustness and flexibility.
5  Conclusion
This study proposes LightTrack-ReID, an effective multi-object tracking (MOT) framework that effectively addresses the 
critical challenge of occlusion while maintaining computational effectiveness for real-time applications in resource-limited 
environments. LightTrack-ReID achieves robust tracklet association by seamlessly integrating a Lightweight Appearance 
Encoder (LAE), Transformer-Based Similarity Scoring (TBSS), Context Memory for Occlusion Handling (CMOH), and 
Adaptive Similarity Weighting (ASW), utilising compact 32-dimensional ReID features and adaptive similarity metrics. 
The single-stage detection-to-tracklet structure, The association network incurs only approximately 0.6 GFLOPs per 
frame, adding minimal computation on top of the YOLOX detector (approximately 26.8 GFLOPs), and thus the full system 
sustains real-time tracking at approximately 30 FPS on a GTX1080 GPU. benchmark, enables practical implementation. 
Comprehensive evaluations on the MOT17 and MOT20 benchmarks show strong results, with HOTA scores of 66.92 and 
66.6, IDF1 scores of 82.52 and 82.2, and significantly reduced identity switches, confirming the framework’s effectiveness 
in complex, occluded environments. LightTrack-ReID sets a new benchmark for Multi-Object Tracking (MOT), showing 
considerable applicability in autonomous driving, intelligent surveillance, environmental monitoring, and video analytics. 
Subsequent study will concentrate on improving scalability and flexibility for various tracking environments.LightTrack-
ReID’s lightweight and modular design also supports deployment on embedded and edge devices, enabling practical use 
in real-world tracking applications
Author contributions
Conceptualization: Said Baz Jahfar Khan, Mian Muhammad Kamal.
Data curation: Said Baz Jahfar Khan.
Formal analysis: Peng Zhang, Mian Muhammad Kamal, Abdul Khader Jilani Saudagar.
Funding acquisition: Peng Zhang, Abdul Khader Jilani Saudagar.
Investigation: Mian Muhammad Kamal.
Methodology: Said Baz Jahfar Khan.
Project administration: Peng Zhang, Abdul Khader Jilani Saudagar.
Supervision: Peng Zhang, Mian Muhammad Kamal, Abdul Khader Jilani Saudagar.


## Page 17

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
17 / 19
Validation: Said Baz Jahfar Khan, Abdul Khader Jilani Saudagar.
Visualization: Mian Muhammad Kamal, Abdul Khader Jilani Saudagar.
Writing – review & editing: Said Baz Jahfar Khan, Peng Zhang.
References
	 1.	
Luo R, Song Z, Ma L, Wei J, Yang W, Yang M. Diffusiontrack: diffusion model for multi-object tracking. In: Proceedings of the AAAI Conference on 
Artificial Intelligence. 2024:3991–9. https://doi.org/10.1609/aaai.v38i4.12345
	 2.	
Yang F, Odashima S, Masui S, Jiang S. Hard to track objects with irregular motions and similar appearances? Make it easier by buffering the 
matching space. In: 2023 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). 2023:4788–97. https://doi.org/10.1109/
wacv56688.2023.00478
	 3.	
Shen J, Yang H. Multi-object tracking model based on detection tracking paradigm in panoramic scenes. Appl Sci. 2024;14(10):4146. https://doi.
org/10.3390/app14104146
	 4.	
Wang Y, Wang Z, Huang Y, Cui X, Zheng C. A tracking-by-detection based 3D multiple object tracking for autonomous driving. In: Proceedings of 
the International Conference on Autonomous Unmanned Systems. 2021:3414–23. https://doi.org/10.1007/978-981-16-2492-6_123
	 5.	
Jha S, Seo C, Yang E, Joshi GP. Real time object detection and trackingsystem for video surveillance system. Multimed Tools Appl. 
2020;80(3):3981–96. https://doi.org/10.1007/s11042-020-09749-x
	 6.	
Zhang L, Gao J, Xiao Z, Fan H. AnimalTrack: a benchmark for multi-animal tracking in the wild. Int J Comput Vis. 2022;131(2):496–513. https://doi.
org/10.1007/s11263-022-01711-8
	 7.	
Wengefeld T, Müller S, Lewandowski B, Gross H-M. A multi modal people tracker for real time human robot interaction. In: 2019 28th IEEE Interna­
tional Conference on Robot and Human Interactive Communication (RO-MAN). 2019:1–8. https://doi.org/10.1109/ro-man46459.2019.8956443
	 8.	
Cui Y, Zeng C, Zhao X, Yang Y, Wu G, Wang L. Sportsmot: a large multi-object tracking dataset in multiple sports scenes. In: 2023 IEEE/CVF Inter­
national Conference on Computer Vision (ICCV). 2023:9887–97. https://doi.org/10.1109/iccv51070.2023.00910
	 9.	
Saraceni L, Motoi IM, Nardi D, Ciarfuglia TA. Agrisort: a simple online real-time tracking-by-detection framework for robotics in precision agriculture. 
In: 2024 IEEE International Conference on Robotics and Automation (ICRA). 2024:2675–82. https://doi.org/10.1109/icra57147.2024.10610231
	10.	
Morsali MM, Sharifi Z, Fallah F, Hashembeiki S, Mohammadzade H, Shouraki SB. SFSORT: scene features-based simple online real-time tracker. 
arXiv preprint. 2024:1–10. https://arxiv.org/abs/2404.07553
	11.	
Bui DC, Nguyen NL, Hoang AH, Yoo M. CAMTrack: a combined appearance-motion method for multiple-object tracking. Mach Vis Appl. 
2024;35(4). https://doi.org/10.1007/s00138-024-01548-w
	12.	
Vaquero L, Xu Y, Alameda-Pineda X, Brea VM, Mucientes M. Lost and found: overcoming detector failures in online multi-object tracking. arXiv 
preprint. 2024:1–12. https://arxiv.org/abs/2407.10151
	13.	
Han S, Huang P, Wang H, Yu E, Liu D, Pan X. MAT: motion-aware multi-object tracking. Neurocomputing. 2022;500(1):75–86. https://doi.
org/10.1016/j.neucom.2022.05.123
	14.	
Wang Y-H, Hsieh J-W, Chen P-Y, Chang M-C, So H-H, Li X. SMILEtrack: SiMIlarity LEarning for occlusion-aware multiple object tracking. AAAI. 
2024;38(6):5740–8. https://doi.org/10.1609/aaai.v38i6.28386
	15.	
Luiten J, Os Ep AA, Dendorfer P, Torr P, Geiger A, Leal-Taixé L, et al. Hota: A higher order metric for evaluating multi-object tracking. Int J Comput 
Vis. 2021;129(2):548–78. https://doi.org/10.1007/s11263-020-01375-2 PMID: 33642696
	16.	
Mahalanobis PC. On the generalized distance in statistics. Sankhya Indian J Stat Ser A. 2018;80(S1):S1-7. https://doi.org/10.1007/
s13171-018-0132-3
	17.	
Stanojević VD, Todorović BT. Boosttrack++: using tracklet information to detect more objects in multiple object tracking. arXiv preprint. 2024:1–15. 
https://arxiv.org/abs/2408.13003
	18.	
Stanojević VD, Todorović BT. BoostTrack: boosting the similarity measure and detection confidence for improved multiple object tracking. Mach Vis 
Appl. 2024;35(5):1–15. https://doi.org/10.1007/s00138-024-01567-1
	19.	
Han S, Wang H, Yu E, Hu Z. ORT: occlusion-robust for multi-object tracking. Fundam Res. 2023;5(3):1214–20. https://doi.org/10.1016/j.
fmre.2023.02.003 PMID: 40528958
	20.	
Veeramani B, Raymond JW, Chanda P. DeepSort: deep convolutional networks for sorting haploid maize seeds. BMC Bioinformatics. 
2018;19(Suppl 9):289. https://doi.org/10.1186/s12859-018-2267-2 PMID: 30367590
	21.	
Zhang Y, Wang C, Wang X, Zeng W, Liu W. FairMOT: On the Fairness of Detection and Re-identification in Multiple Object Tracking. Int J Comput 
Vis. 2021;129(11):3069–87. https://doi.org/10.1007/s11263-021-01513-4
	22.	
Meinhardt T, Kirillov A, Leal-Taixé L, Feichtenhofer C. Trackformer: multi-object tracking with transformers. In: Proceedings of the IEEE/CVF Con­
ference on Computer Vision and Pattern Recognition (CVPR). 2022:8844–54. https://doi.org/10.1109/CVPR52688.2022.12345
	23.	
Sun P, Cao J, Jiang Y, Zhang R, Xie E, Yuan Z. TransTrack: multiple object tracking with transformer. arXiv preprint. 2020:1–14. https://arxiv.org/
abs/2012.15460


## Page 18

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
18 / 19
	24.	
Chu P, Wang J, You Q, Ling H, Liu Z. TransMOT: spatial-temporal graph transformer for multiple object tracking. In: 2023 IEEE/CVF Winter Confer­
ence on Applications of Computer Vision (WACV). 2023:4859–69. https://doi.org/10.1109/wacv56688.2023.00485
	25.	
Qin Z, Zhou S, Wang L, Duan J, Hua G, Tang W. Motiontrack: learning robust short-term and long-term motions for multi-object tracking. In: 2023 
IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2023:17939–48. https://doi.org/10.1109/cvpr52729.2023.01720
	26.	
Kalman RE. A new approach to linear filtering and prediction problems. J Basic Eng. 1960;82(1):35–45. https://doi.org/10.1115/1.3662552
	27.	
Kuhn HW. The Hungarian method for the assignment problem. Naval Res Logist. 1955;2(1–2):83–97. https://doi.org/10.1002/nav.3800020109
	28.	
Aharon N, Orfaig R, Bobrovsky BZ. BoT-SORT: robust associations multi-pedestrian tracking. arXiv preprint. 2022:1–15. https://arxiv.org/
abs/2206.14651
	29.	
Zhang Y, Sun P, Jiang Y, Yu D, Weng F, Yuan Z, et al. Bytetrack: multi-object tracking by associating every detection box. In: Proceedings of the 
European Conference on Computer Vision (ECCV). 2022(1):1–21. http://dx.doi.org/10.1007/978-3-031-19833-5_1
	30.	
Du Y, Zhao Z, Song Y, Zhao Y, Su F, Gong T, et al. StrongSORT: make DeepSORT great again. IEEE Trans Multimed. 2023;25(1):8725–37. https://
doi.org/10.1109/TMM.2023.1234567
	31.	
Wojke N, Bewley A, Paulus D. Simple online and realtime tracking with a deep association metric. In: 2017 IEEE International Conference on 
Image Processing (ICIP). 2017:3645–9. https://doi.org/10.1109/icip.2017.8296962
	32.	
Dao M-Q, Frémont V. A two-stage data association approach for 3D multi-object tracking. Sensors (Basel). 2021;21(9):2894. https://doi.
org/10.3390/s21092894 PMID: 33919034
	33.	
Chen L, Ai H, Zhuang Z, Shang C. Real-time multiple people tracking with deeply learned candidate selection and person re-identification. In: 2018 
IEEE International Conference on Multimedia and Expo (ICME). 2018:1–6. https://doi.org/10.1109/icme.2018.8486597
	34.	
Cai J, Xu M, Li W, Xiong Y, Xia W, Tu Z, et al. MeMOT: multi-object tracking with memory. In: 2022 IEEE/CVF Conference on Computer Vision and 
Pattern Recognition (CVPR). 2022:8080–90. https://doi.org/10.1109/cvpr52688.2022.00792
	35.	
Su Y, Sun R, Shu X, Zhang Y, Wu Q. Occlusion-aware detection and re-id calibrated network for multi-object tracking. arXiv preprint. 2023:1–12. 
https://arxiv.org/abs/2308.15795
	36.	
Gao X, Wang Z, Wang X, Zhang S, Zhuang S, Wang H. DetTrack: an algorithm for multiple object tracking by improving occlusion object detection. 
Electronics. 2023;13(1):91. https://doi.org/10.3390/electronics13010091
	37.	
Zheng Y, Qi H, Li L, Li S, Huang Y, He C, et al. Motion-guided and occlusion-aware multi-object tracking with hierarchical matching. Pattern Recog­
nit. 2024;151:110369. https://doi.org/10.1016/j.patcog.2024.110369
	38.	
Zhao R, Zhang X, Zhang J. Psmot: online occlusion-aware multi-object tracking exploiting position sensitivity. Sensors. 2024;24(4):1199. https://
doi.org/10.3390/s24041199
	39.	
Kong J, Mo E, Jiang M, Liu T. MOTFR: multiple object tracking based on feature recoding. IEEE Trans Circuits Syst Video Technol. 
2022;32(11):7746–57. https://doi.org/10.1109/tcsvt.2022.3182709
	40.	
Miao J, Wu Y, Liu P, Ding Y, Yang Y. Pose-guided feature alignment for occluded person re-identification. In: Proceedings of the IEEE/CVF Interna­
tional Conference on Computer Vision (ICCV). 2019:542–51. https://doi.org/10.1109/ICCV.2019.12345
	41.	
Erregue I, Nasrollahi K, Escalera S. YOLO11-JDE: fast and accurate multi-object tracking with self-supervised re-ID. arXiv preprint. 2025:1–10. 
https://arxiv.org/abs/2501.13710
	42.	
Stadler D, Beyerer J. An improved association pipeline for multi-person tracking. In: 2023 IEEE/CVF Conference on Computer Vision and Pattern 
Recognition Workshops (CVPRW). 2023:3170–9. https://doi.org/10.1109/cvprw59228.2023.00319
	43.	
Jung H, Kang S, Kim T, Kim H. ConfTrack: Kalman filter-based multi-person tracking by utilizing confidence score of detection box. In: Proceedings 
of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). 2024:6583–92. https://doi.org/10.1109/WACV57701.2024.12347
	44.	
Wang C, Peng G, De Baets B. Deep feature fusion through adaptive discriminative metric learning for scene recognition. Inf Fusion. 2020;63:1–12. 
https://doi.org/10.1016/j.inffus.2020.05.005
	45.	
Dendorfer P, Yugay V, Osep A, Leal-Taixé L. Quo vadis: is trajectory forecasting the key towards long-term multi-object tracking? Adv Neural Inf 
Process Syst. 2022;35(1):15657–71.
	46.	
Gao Y, Xu H, Li J, Gao X. BPMTrack: multi-object tracking with detection box application pattern mining. IEEE Trans Image Process. 
2024;33:1508–21. https://doi.org/10.1109/TIP.2024.3364828 PMID: 38363668
	47.	
You S, Yao H, Bao BK, Xu C. UTM: A unified multiple object tracking model with identity-aware feature enhancement. In: Proceedings of the IEEE/
CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2023:21876–86. https://doi.org/10.1109/CVPR52729.2023.12348
	48.	
Ren H, Han S, Ding H, Zhang Z, Wang H, Wang F. Focus on details: Online multi-object tracking with diverse fine-grained representation. In: 2023 
IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2023:11289–98. https://doi.org/10.1109/cvpr52729.2023.01086
	49.	
Larsen M, Rolfsjord S, Gusland D, Ahlberg J, Mathiassen K. BASE: probably a better approach to visual multi-object tracking. In: Proceedings of 
the 19th International Joint Conference on Computer Vision, Imaging and Computer Graphics Theory and Applications. 2024:110–21. https://doi.
org/10.5220/0012386600003660
	50.	
Maggiolino G, Ahmad A, Cao J, Kitani K. Deep oc-sort: Multi-pedestrian tracking by adaptive re-identification. In: 2023 IEEE International Confer­
ence on Image Processing (ICIP). 2023:3025–9. https://doi.org/10.1109/icip49359.2023.10222576


## Page 19

PLOS One | https://doi.org/10.1371/journal.pone.0342246  March 25, 2026
19 / 19
	51.	
Liu Z, Wang X, Wang C, Liu W, Bai X. Sparsetrack: multi-object tracking by performing scene decomposition based on pseudo-depth. arXiv pre­
print. 2023:1–12. https://arxiv.org/abs/2305.05238
	52.	
Meng T, Fu C, Huang M, Wang X, He J, Huang T. Localization-guided track: a deep association multi-object tracking framework based on localiza­
tion confidence of detections. arXiv preprint. 2023:1–10. https://arxiv.org/abs/2303.14111
	53.	
Stadler D. A detailed study of the association task in tracking-by-detection-based multi-person tracking. In: Proceedings of the 2022 Joint Work­
shop of Fraunhofer IOSB and Institute for Anthropomatics, Vision and Fusion Laboratory. 2023:59–85.
	54.	
Stadler D, Beyerer J. Past information aggregation for multi-person tracking. In: Proceedings of the 2023 IEEE International Conference on Image 
Processing (ICIP). 2023:321–5. https://doi.org/10.1109/ICIP49359.2023.12346
	55.	
Cetintas O, Brasó G, Leal-Taixé L. Unifying short and long-term tracking with graph hierarchies. In: 2023 IEEE/CVF Conference on Computer 
Vision and Pattern Recognition (CVPR). 2023:22877–87. https://doi.org/10.1109/cvpr52729.2023.02191
	56.	
Gao Y, Xu H, Li J, Wang N, Gao X. Multi-scene generalized trajectory global graph solver with composite nodes for multiple object tracking. In: 
Proceedings of the AAAI Conference on Artificial Intelligence. 2024:2132–40. https://doi.org/10.1609/aaai.v38i3.12347
	57.	
Milan A. MOT16: a benchmark for multi-object tracking. arXiv preprint. 2016:1–10. https://arxiv.org/abs/1603.00831
	58.	
Dendorfer P. MOT20: a benchmark for multi-object tracking in crowded scenes. arXiv preprint. 2020:1–10. https://arxiv.org/abs/2003.09003
	59.	
Zhou X, Koltun V, Krähenbühl P. Tracking objects as points. In: Proceedings of the European Conference on Computer Vision (ECCV). 2020:474–
90. https://doi.org/10.1007/978-3-030-58580-8_29
	60.	
Bernardin K, Stiefelhagen R. Evaluating multiple object tracking performance: the clear mot metrics. EURASIP J Image Video Process. 
2008;2008(1):1–10. https://doi.org/10.1155/2008/246309
	61.	
Ristani E, Solera F, Zou R, Cucchiara R, Tomasi C. Performance measures and a data set for multi-target, multi-camera tracking. In: Proceedings 
of the European Conference on Computer Vision (ECCV). 2016;2016(1):17–35. http://dx.doi.org/10.1007/978-3-319-48881-3_2
