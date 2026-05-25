---
source_id: S022
title: DiffusionTrack: Diffusion Model for Multi-Object Tracking
source_url: https://ojs.aaai.org/index.php/AAAI/article/download/28192/28382
source_file: docs/research/papers/S022-diffusiontrack-diffusion-model-for-multi-object-tracking.pdf
source_kind: pdf
extraction_note: downloaded PDF retry
---

# Extracted text: S022-diffusiontrack-diffusion-model-for-multi-object-tracking.pdf


## Page 1

DiffusionTrack: Diffusion Model For Multi-Object Tracking
Run Luo123, Zikai Song3*, Lintao Ma3, Jinlin Wei34, Wei Yang3, Min Yang12*
1Shenzen Institute of Advanced Technology, Chinese Academy of Sciences
2University of Chinese Academy of Sciences
3Huazhong University of Science and Technology
4University of California, Santa Barbara
{r.luo,min.yang}@siat.ac.cn, {skyesong, mltdml,weiyangcs}@hust.edu.cn, jinlinwei@ucsb.edu
Abstract
Multi-object tracking (MOT) is a challenging vision task
that aims to detect individual objects within a single frame
and associate them across multiple frames. Recent MOT
approaches can be categorized into two-stage tracking-by-
detection (TBD) methods and one-stage joint detection and
tracking (JDT) methods. Despite the success of these ap-
proaches, they also suffer from common problems, such as
harmful global or local inconsistency, poor trade-off between
robustness and model complexity, and lack of flexibility in
different scenes within the same video. In this paper we pro-
pose a simple but robust framework that formulates object
detection and association jointly as a consistent denoising dif-
fusion process from paired noise boxes to paired ground-truth
boxes. This novel progressive denoising diffusion strategy
substantially augments the tracker’s effectiveness, enabling it
to discriminate between various objects. During the training
stage, paired object boxes diffuse from paired ground-truth
boxes to random distribution, and the model learns detection
and tracking simultaneously by reversing this noising pro-
cess. In inference, the model refines a set of paired randomly
generated boxes to the detection and tracking results in a flex-
ible one-step or multi-step denoising diffusion process. Ex-
tensive experiments on three widely used MOT benchmarks,
including MOT17, MOT20, and DanceTrack, demonstrate
that our approach achieves competitive performance com-
pared to the current state-of-the-art methods. Code is avail-
able at https://github.com/RainBowLuoCS/DiffusionTrack.
1
Introduction
Multi-object Tracking is one of the fundamental vision tasks
with applications ranging from human-computer interaction,
surveillance, autonomous driving, etc. It aims at detecting
the bounding box of the object and associating the same
object across consecutive frames in a video sequence. Re-
cent MOT approaches can be categorized into two-stage
tracking-by-detection (TBD) methods and one-stage joint
detection and tracking (JDT) methods. TBD methods de-
tect the bounding boxes of the objects within a single
frame using a detector and associate the same object cross
frames by employing supplementary trackers. These track-
ers encompass a spectrum of techniques, such as motion-
*co-corresponding author
Copyright © 2024, Association for the Advancement of Artificial
Intelligence (www.aaai.org). All rights reserved.
Backbone
Diffusion 
Head
f𝐫𝐚𝐦𝐞 𝐭−𝟏
Input
Output
𝑥𝑇
𝑥𝑡
𝑥𝑡−1
𝑥0
𝒑𝜽(𝒙𝒕−𝟏|𝒙𝒕)
𝒒𝜽(𝒙𝒕|𝒙𝒕−𝟏)
Denoising
f𝐫𝐚𝐦𝐞 𝐭−𝟏
f𝐫𝐚𝐦𝐞 𝐭
f𝐫𝐚𝐦𝐞 𝐭
Diffusion
Track
Process
Figure 1: DiffusionTrack formulates object association as
a denoising diffusion process from paired noise boxes to
paired object boxes within two adjacent frames t −1 and t.
The diffusion head receives the two-frame image informa-
tion extracted by the frozen backbone and then iteratively
denoises the paired noise boxes to obtain the final paired ob-
ject boxes.
based trackers (Bewley et al. 2016; Cao et al. 2022; Zhang
et al. 2022; Aharon, Orfaig, and Bobrovsky 2022; Zhao
et al. 2022; Wojke, Bewley, and Paulus 2017; Zhang et al.
2021; Liu et al. 2023) that employ the Kalman filter frame-
work (Welch, Bishop et al. 1995). In addition, certain TBD
approaches establish object associations through the utiliza-
tion of Re-identification (Re-ID) techniques (Chen et al.
2018; Bergmann, Meinhardt, and Leal-Taixe 2019a), and
others that rely on graph-based trackers (He et al. 2021;
Rangesh et al. 2021; Li, Gao, and Jiang 2020) that model
the association process as minimization of a cost flow prob-
lem.
JDT approaches try to combine the tracking and detection
process in a unified manner. This paradigm consists of three
mainstream strategies: query-based trackers (Sun et al. 2020;
Meinhardt et al. 2022; Zeng et al. 2022; Cai et al. 2022; Chen
et al. 2021) that adopt unique query implicitly by forcing
each query to track the same object, offset-based trackers
(Bergmann, Meinhardt, and Leal-Taixe 2019b; Tokmakov
et al. 2021; Xu et al. 2022; Zhou, Koltun, and Kr¨ahenb¨uhl
2020) utilizing the motion feature to predict motion off-
set, and trajectory-based trackers (Pang et al. 2020; Zhou
et al. 2022) that tackle severe object occlusions via spatial-
temporal information. However, most of TBD and JDT ap-
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3991


## Page 2

proaches suffer from the following common drawbacks: (1)
Harmful global or local inconsistency plagues both methods.
In TBD approaches, the segmentation of detection and track-
ing tasks into distinct training processes engenders global
inconsistencies that curtail overall performance. Although
JDT approaches aim to bridge the gap between detection
and tracking, they still treat them as disparate tasks through
various branches or modules, not fully resolving the incon-
sistency; (2) A suboptimal balance between robustness and
model complexity is evident in both approaches. While the
simple structure of TBD methods suffers from poor per-
formance when faced with detection perturbation, the com-
plex design of JDT approaches ensures stability and ro-
bustness but compromises detection accuracy compared to
TBD methods; (3) Both approaches also exhibit inflexibility
across different scenes within the same video. Conventional
methods process videos under uniform settings, hindering
the adaptive application of strategies for varying scenes and
consequently limiting their efficacy.
Recently, diffusion models have not only excelled in var-
ious generative tasks but also demonstrated potential in
confronting complex discriminative computer vision chal-
lenges (Chen et al. 2022; Gu et al. 2022). This paper intro-
duces DiffusionTrack, inspired by the progress in diffusion
models, and constructs a novel consistent noise-to-tracking
paradigm. DiffusionTrack directly formulates object associ-
ations from a set of paired random boxes within two adjacent
frames, as illustrated in Figure 1. The motivation is to metic-
ulously refine the coordinates of these paired boxes so that
they accurately cover the same targeted objects across two
consecutive frames, thereby implicitly performing detection
and tracking within a uniform model pipeline. This innova-
tive coarse-to-fine paradigm is believed to compel the model
to learn to accurately distinguish objects from one another,
ultimately leading to enhanced performance. DiffusionTrack
addresses the multi-object tracking task by treating data as-
sociation as a generative endeavor within the space of paired
bounding boxes over two successive frames. Extensive ex-
periments on 3 challenging datasets including MOT17 (Mi-
lan et al. 2016), MOT20 (Dendorfer et al. 2020) and Dance-
Track (Sun et al. 2022), exhibit the state-of-the-art perfor-
mance among the JDT multi-object trackers, which is also
compared with TBD approaches.
In summary, our main contributions include:
1. We propose DiffusionTrack, which is the first work to
employ the diffusion model for multi-object tracking by
formulating it as a generative noise-to-tracking diffusion
process.
2. Experimental results show that our noise-to-tracking
paradigm has several appealing properties, such as de-
coupling training and evaluation stage for dynamic
boxes and progressive refinement, promising consistency
model structure for two tasks, and strong robustness to
detection perturbation results.
2
Related Work
Existing MOT algorithms can be divided into two categories
according to the paradigm of handling the detection and as-
sociation, i.e., the two-stage TBD methods and the one-stage
JDT methods.
Two-stage TBD methods is a common practice in the
MOT field, where object detection and data association are
treated as separate modules. The object detection module
uses an existing detector (Ren et al. 2015; Duan et al. 2019;
Ge et al. 2021), and the data association module can be
further divided into motion-based methods(Bewley et al.
2016; Wojke, Bewley, and Paulus 2017; Zhang et al. 2022;
Aharon, Orfaig, and Bobrovsky 2022; Cao et al. 2022) and
graph-based (Zhang, Li, and Nevatia 2008; Jiang et al. 2019;
Bras´o and Leal-Taix´e 2020; Li, Gao, and Jiang 2020; He
et al. 2021) methods. Motion-based methods integrate de-
tections through a distingct motion tracker across consecu-
tive frames, employing various techniques. SORT (Bewley
et al. 2016) initialed the use of the Kalman filter (Welch,
Bishop et al. 1995) for object tracking, associating each
bounding box with the highest overlap through the Hun-
garian algorithm (Kuhn 1955). DeepSORT (Wojke, Bewley,
and Paulus 2017) enhanced this by incorporating both mo-
tion and deep appearance features, while StrongSORT (Du
et al. 2022) further integrated lightweight, appearance-free
algorithms for detection and association. ByteTrack (Zhang
et al. 2022) addressed fragmented trajectories and missing
detections by utilizing low-confidence detection similari-
ties. P3AFormer (Zhao et al. 2022) combined pixel-wise
distribution architecture with Kalman filter to refine ob-
ject association, and OC-SORT (Cao et al. 2022) amended
the linear motion assumption within the Klaman Filter for
superior adaptability to occlusion and non-linear motion.
Graph-based methods, including Graph Neural Networks
(GNN) (Gori, Monfardini, and Scarselli 2005) and Graph
Convolutional Networks (GCN) (Kipf and Welling 2016),
have been widely explored in MOT, with vertices represent-
ing detection bounding boxes or tracklets and edges across
frames denoting similarities. This setup allows the associa-
tion challenge to be cast as a min-cost flow problem. MPN-
Track (Bras´o and Leal-Taix´e 2020) introduced a message-
passing network to capture information between vertices
across frames, GNMOT
(Li, Gao, and Jiang 2020) con-
structed dual graph networks to model appearance and mo-
tion features, and GMTracker (He et al. 2021) emphasized
both inter-frame matching and intra-frame context.
One-stage JDT methods. In recent years, there have been
several explorations into the one-stage paradigm, which
combines object detection and data association into a sin-
gle pipeline. Query-based methods, a burgeoning trend, uti-
lize DETR (Carion et al. 2020; Zhu et al. 2020) exten-
sions for MOT by representing each object as a query re-
gressed across various frames. Techniques such as Track-
Former (Meinhardt et al. 2022) and MOTR (Zeng et al.
2022) perform simultaneous object detection and associa-
tion using concatenated object and track queries. TransTrack
(Sun et al. 2020) employs cyclical feature passing to ag-
gregate embeddings, while MeMOT (Cai et al. 2022) en-
codes historical observations to preserve extensive spatio-
temporal memory. Offset-based methods, in contrast, by-
pass inter-frame association and instead focus on regress-
ing past object locations to new positions. This approach
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3992


## Page 3

frame@ t-1
frame@ t
Gaussian 
Noise
Backbone
Self-Attention
Head
V
Raw Video
Sample 
Interval
Center 
Point
SFT
Self-Attention
Head
SFT
Self-Attention
Head
ROI 
Pooler
SFT
𝐿𝑐𝑙𝑠
𝐿𝑔𝑖𝑜𝑢3𝑑
𝐿𝑟𝑒𝑔
Focal Loss
L1 Loss
GIOU3d Loss
Post Process
Diffusion
Head
X N
Basic Block
Figure 2: The architecture of DiffusionTrack. Given the images and corresponding ground-truth in the frame t and frame t-1,
we extract features from two adjacent frames through the frozen backbone, then the diffusion head takes paired noise boxes
as input and predicts category classification, box coordinates and association score of the same object in two adjacent frames.
During training, the noise boxes are constructed by adding Gaussian noise to paired ground-truth boxes of the same object. In
inference, the noise boxes are constructed by adding Gaussian noise to the padded prior object boxes in the previous frame.
includes Tracktor++ (Cai et al. 2022) for temporal realign-
ment of bounding boxes, CenterTrack (Zhou, Koltun, and
Kr¨ahenb¨uhl 2020) for object localization and offset predic-
tion, and PermaTrack (Tokmakov et al. 2021), which fuses
historical memory to reason target location and occlusion.
TransCenter (Xu et al. 2022) further advances this cate-
gory by adopting dense representations with image-specific
detection queries and tracking. Trajectory-based methods
extract spatial-temporal information from historical track-
lets to associate objects. GTR (Zhou et al. 2022) groups
detections from consecutive frames into trajectories using
trajectory queries, and TubeTK (Pang et al. 2020) extends
bounding-boxes to video-based bounding-tubes for predic-
tion. Both efficiently handle occlusion issues by utilizing
long-term tracklet information.
Diffusion model. As a class of deep generative models,
diffusion models (Ho, Jain, and Abbeel 2020; Song and Er-
mon 2019; Song et al. 2020) start from the sample in ran-
dom distribution and recover the data sample via a gradual
denoising process.
However, their potential for visual understanding tasks
has yet to be fully explored. Recently, DiffusionDet (Chen
et al. 2022) and DiffusionInst (Gu et al. 2022) have suc-
cessfully applied diffusion models to object detection and
instance segmentation as noise-to-box and noise-to-filter
tasks, respectively. Inspired by their successful application
of the diffusion model, we proposed DiffusionTrack, which
further broadens the application of the diffusion model by
formalizing MOT as a denoising process. To the best of
our knowledge, this is the first work that adopts a diffusion
model for the MOT task.
3
Method
In this section, we present our DiffusionTrack. In contrast to
existing motion-based and query-based methods, we design
a consistent tracker that performs tracking implicitly by pre-
dicting and associating the same object across two adjacent
frames within the video sequence. We first briefly review
the pipeline of multi-object tracking and diffusion models.
Then, we introduce the architecture of DiffusionTrack. Fi-
nally, we present model training and inference.
3.1
Preliminaries
Multi-object tracking. The learning objective of MOT is a
set of input-target pairs (Xt, Bt, Ct) sorted by time t, where
Xt is the input image at time t, Bt and Ct are a set of bound-
ing boxes and category labels for objects in the video at time
t respectively. More specifically, we formulate the i-th box
in the set Bt as Bi
t = (ci
x, ci
y, wi, hi), where (ci
x, ci
y) is the
center coordinates of the bounding box, (wi, hi) are width
and height of that bounding box, i is the identity number
respectively. Specially, Bi
t = ∅when i-th object miss in Xt.
Diffusion model. Recent diffusion models usually use two
Markov chains: a forward chain that perturbs the image to
noise and a reverse chain that refines noise back to the im-
age. Formally, given a data distribution x0 ∼q(x0), the
forward noise perturbing process at time t is defined as
q(xt|xt−1). It gradually adds Gaussian noise to the data ac-
cording to a variance schedule β1, · · · , βT :
q(xt|xt−1) = N(xt;
p
1 −βtxt−1, βtI).
(1)
Given x0, we can easily obtain a sample of xt by sampling
a Gaussian vector ϵ ∼N(0, I) and applying the transforma-
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3993


## Page 4

Denoising
f𝐫𝐚𝐦𝐞 𝐭−𝟏
f𝐫𝐚𝐦𝐞 𝐭−𝟏
f𝐫𝐚𝐦𝐞 𝐭−𝟏
prior
 boxes
noise
 boxes
(𝟏−𝜶𝒕)
𝜶𝒕
Gaussian Noise
Noise Type: Gaussian , Poisson or Uniform Noise
f𝐫𝐚𝐦𝐞 t
f𝐫𝐚𝐦𝐞 𝐭
Figure 3: The inference of DiffusionTrack can be divided into three steps: (1) padding repeated prior boxes with given noise
boxes until predefined number Ntest is reached. (2) adding Gaussian noise to input boxes according to B = (1 −αt) · B + αt ·
Bnoise under the control of αt. (3) getting tracking results by a denoising process with the number of DDIM sampling steps s.
tion as follows:
xt = √¯αtx0 + (1 −¯αt)ϵ,
(2)
where ¯αt = Qt
s=0(1 −βs). During training, a neural net-
work predict x0 from xt for different t ∈{1, · · · , T}. In
inference, we start from a random noise xT and iteratively
apply the reverse chain to obtain x0.
3.2
DiffusionTrack
The overall framework of our DiffusionTrack is visualized
in Figure 2, which consists of two major components: a fea-
ture extraction backbone and a data association denoising
head (diffusion head), where the former runs only once to
extract a deep feature representation from two adjacent in-
put image (Xt−1, Xt), and the latter takes this deep fea-
tures as condition, instead of two adjacent raw images, to
progressively refine the paired association box predictions
from paired noise boxes. In our setting, data samples are
a set of paired bounding boxes z0 = (Bt−1, Bt), where
z0 ∈RN×8. A neural network fθ(zs, s, Xt−1, Xt)
s =
{0, · · · , T} is trained to predict z0 from paired noise boxes
zs, conditioned on the corresponding two adjacent images
(Xt−1, Xt). The corresponding category label (Ct−1, Ct)
and association confidence score S are produced accord-
ingly. If Xt−1 = Xt, the multi-object tracking task degener-
ates into an object detection problem. The consistent design
allows DiffusionTrack to solve the two tasks simultaneously.
Backbone. We employ the backbone of YOLOX (Ge et al.
2021) as our backbone. The backbone extracts high-level
features of the two adjacent frames with FPN (Lin et al.
2017) and then feeds them into the following diffusion head
for conditioned data association denoising.
Diffusion head. The diffusion head takes a set of proposal
boxes as input to crop RoI-feature (Jiang et al. 2018) from
the feature map generated by the backbone and sends these
RoI-features to different blocks to obtain box regression,
classification results, and association confidence scores, re-
spectively. To solve the object tracking problem, we add
a spatial-temporal fusion module (STF) and an association
score head to each block of the diffusion head.
Spatial-temporal fusion module. We design a new spatial-
temporal fusion module so that the same paired box can ex-
change temporal information with each other to ensure that
the data association on two consecutive frames can be com-
pleted. Given the RoI-features f t−1
roi , f t
roi ∈RN×R×d, and
the self-attention output query qt−1
pro , qt
pro ∈RN×d at cur-
rent block, we conduct linear project and batch matrix mul-
tiplication to get the object query qt−1, qt ∈RN×d as:
Pi
1, Pi
2 = Split(Linear1(qi
pro)),
feat = Bmm(Bmm(Concat(f i
roi, f j
roi), Pi
1), Pi
2)
qi = Linear2(feat),
qi ∈RN×d
(i, j) ∈[(t −1, t), (t, t −1)]
(3)
Association score head. In addition to the box head and
class head, we add an extra association score head to obtain
the confidence score of the data association by feeding the
fused features of the two paired boxes into a Linear Layer.
The head is used to determine whether the paired boxes
output belongs to the same object in the subsequent Non-
Maximum Suppression (NMS) post-processing process.
3.3
Model Training and Inference
In the training phase, our approach takes a pair of frames
randomly sampled from sequences in the training set with an
interval of 5 as input. we first pad some extra boxes to orig-
inal ground-truth boxes appearing in both frames such that
all boxes are summed up to a fixed number Ntrain. Then we
add Gaussian noise to the padded ground-truth boxes with
the monotonically decreasing cosine schedule for αt in time
step t. We finally conduct a denoising process to get asso-
ciation results from these constructed noise boxes. We also
design a baseline that only corrupts the ground-truth boxes
in frame t and conditionally denoises the corrupted boxes
based on the prior boxes in frame t −1 to verify the neces-
sity of corruption design for both frames in DiffusionTrack.
Loss Function. GIoU (Rezatofighi et al. 2019) loss is an ex-
tension of IoU loss which solves the problem that there is no
supervisory information when the predicted boxes have no
intersection with the ground-truth. We extend the definition
of GIoU to make it compatible with paired boxes design.
3D GIoU and 3D IoU are the volume-extended versions of
the original area ones. For each pair paired (Td, Tgt) in the
matching set M obtained by the Hungarian matching algo-
rithm, we denote its class score, predicted boxes result, and
association score as (Ct−1
d
, Ct
d), (Bt−1
d
, Bt
d), and Sd. The
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3994


## Page 5

training loss function can be formulated as:
Lcls(Td, Tgt) =
t
X
i=t−1
Lcls(
q
Ci
d × Sd, Ci
gt)
Lreg(Td, Tgt) =
t
X
i=t−1
Lreg(Bi
d, Bi
gt)
Ldet =
1
Npos
X
(Td,Tgt)∈M
λ1Lcls(Td, Tgt)
+
λ2Lreg(Td, Tgt) + λ3(1 −GIoU3d(Td, Tgt))
(4)
where Td and Tgt are square frustums consisting of esti-
mated detection boxes and ground-truth bounding boxes for
the same target in two adjacent frames respectively. Npos de-
notes the number of positive foreground samples. λ1, λ2 and
λ3 are the weight coefficients that are assigned as 2, 5 and 2
during training experiments. Lcls is the focal loss proposed
in (Lin et al. 2017) and Lreg is the L1 loss.
As shown in Figure.3, the inference pipeline of Diffusion-
Track is a denoising sampling process from paired noise
boxes to association results. Unlike the detection task that
selects random boxes from the Gaussian distribution, the
tracking task has prior information about an object in the
frame t−1, so we can use prior boxes to generate initialized
noise boxes with a fixed number of Ntest as in the training
phase to benefit data association. In contrast to Diffusion-
Track, we simply repeat the prior box without padding extra
random boxes and add Gaussian noise to prior boxes only
at t in the baseline model. Once the association results are
derived, IoU is utilized as the similarity metric to connect
the object tracklets. To address potential occlusions, a sim-
ple Kalman filter is implemented to reassociate lost objects
and more details exist in the Appendix.
4
Experiments
In this section, we first introduce experimental setting and
show the intriguing properties of DiffusionTrack. Then we
verify the individual contributions in the ablation study and
finally present the tracking evaluation on several challeng-
ing benchmarks, including MOT17 (Milan et al. 2016),
MOT20 (Dendorfer et al. 2020) and DanceTrack (Sun et al.
2022). We also present the comparison with baseline model
and carry out a deep analysis for DiffusionTrack.
4.1
Setting
Datasets. We evaluate our method on multiple multi-object
tracking datasets including MOT17 (Milan et al. 2016),
MOT20 (Dendorfer et al. 2020) and DanceTrack (Sun et al.
2022). MOT17 and MOT20 are for pedestrian tracking,
where targets mostly move linearly, while scenes in MOT20
are more crowded. For the data in DanceTrack, the objects
have a similar appearance, severe occlusion, and frequent
crossovers with highly non-linear motion.
Metric. We mainly use Multiple Object Tracking Accuracy
(MOTA)
(Bernardin and Stiefelhagen 2008), Identity F1
Score (IDF1) (Ristani et al. 2016), and Higher Order Track-
ing Accuracy (HOTA) (Luiten et al. 2021) for evaluation.
1
2
4
8
number of sample steps
70
71
72
73
74
75
MOTA
71.49
71.74
72.37
72.91
73.61
73.95
74.15
74.49
74.09
74.43
74.77
75.15
500
800
1000
(a) Dynamic boxes and progressive refinement. Diffusion-
Track is trained on the MOT17 train-half set with 500 pro-
posal boxes and evaluated on the MOT17 val-half set with
different numbers of proposal boxes. More sampling steps
and proposal boxes in inference bring performance gain, but
the effect is gradually saturated
0
0.01
0.02
0.03
0.04
0.1
t
40
20
0
20
40
60
80
100
MOTA
87.4
88.8
89.2
49.8
41.4
16.0
65.6
65.4
64.6
13.3
-1.8
-37.5
ByteTrack
CenterTrack
TrackFormer
DiffusionTrack
(b) Robustness to detection perturbation. All trackers are
trained on MOT17 training set and evaluated on MOT17 val-
half set with little detection perturbation as Bdet = (1−αt)·
Bdet + αt · Bnoise. DiffusionTrack is robust to perturbation
attacks with 800 proposal boxes while other approaches are
vulnerable.
Figure 4: Intriguing properties of DiffusionTrack. Diffusion-
Track obtains performance gain by enlarging proposal box
numbers and sampling steps while being robust to detection
perturbation compared with the previous tracker.
Implementation Details. We adopt the pre-trained YOLOX
detector from ByteTrack (Zhang et al. 2022) and train Dif-
fusionTrack on MOT17, MOT20, and DanceTrack training
sets in two phases. For MOT17, the training schedule con-
sists of 30 epochs on the combination of MOT17, Crowd-
Human, Cityperson and ETHZ for detection and another 30
epochs on MOT17 solely for tracking. For MOT20, we only
add CrowdHuman as additional training data. For Dance-
Track, we do not use additional training data and only train
40 epochs. We also use Mosaic (Bochkovskiy, Wang, and
Liao 2020) and Mixup (Zhang et al. 2017) data augmenta-
tion during the detection and tracking training phases. The
training samples are directly sampled from the same video
within the interval length of 5 frames. The size of an input
image is resized to 1440×800. The 236M trainable diffu-
sion head parameters are initialized with Xavier Uniform.
The AdamW (Loshchilov and Hutter 2018) optimizer is em-
ployed with an initial learning rate of 1e-4, and the learning
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3995


## Page 6

prior Info
MOTA
IDF1
HOTA
AssA
proportion
0%
71.2
65.9
58.1
54.9
25%
73.6
70.0
60.7
58.4
50%
74.5
71.2
61.8
60.1
75%
74.1
71.4
61.9
60.7
100%
72.9
66.8
58.4
54.7
(a) Proportion of prior information. Using prior information
benefit data association.
padding
MOTA
IDF1
HOTA
AssA
strategy
Repeat
72.9
66.8
58.4
54.7
Cat Poisson
71.9
67.1
58.9
56.1
Cat Gaussian
73.6
70.0
60.7
58.4
Cat Uniform
71.5
63.9
56.8
52.2
Cat Full
71.2
64.4
57.3
53.7
(b) Box padding strategy. Compared to other padding strategy, concate-
nating Gaussian noise works best.
perturbation
MOTA
IDF1
HOTA
AssA
strategy f(x)
0.4
73.0
67.2
58.2
54.2
x
73.6
70.0
60.7
58.4
(ex −1)/(e −1)
74.3
70.5
61.4
59.7
log(x + 1)/log2
74.4
72.0
62.6
61.9
(c) Perturbation schedule. Choosing t through a logarithmic
perturbation strategy works best.
box
sampling
MOTA
IDF1
HOTA
FLOPs(G)
FPS
step
500
1
71.5
66.3
58.4
229.6
21.05
500
2
71.7
68.1
59.5
459.2
10.47
800
1
73.6
70.0
60.7
367.3
15.89
1000
1
74.1
70.7
61.3
459.1
13.37
(d) Efficiency comparison. Adopting more proposal boxes and sampling
steps brings performance gain at the cost of latency.
Table 1: Ablation experiments. The model is trained on the MOT17 train-half and tested on the MOT17 val-half. Default settings
are marked in gray. See Sec 4.3 for more details.
rate decreases according to the cosine function with the fi-
nal decrease factor of 0.1. We adopt a warm-up learning rate
of 2.5e-5 with a 0.2 warm-up factor on the first 5 epochs.
We train our model on 8 NVIDIA GeForce RTX 3090 with
FP32-precision and a constant seed for all experiments. The
mini-batch size is set to 16, with each GPU hosting two
batches with Ntrain = 500. Our approach is implemented
in Python 3.8 with PyTorch 1.10. We set association score
threshold τconf = 0.25, 3D NMS threshold τnms3d = 0.6,
detection score threshold τdet = 0.7 and 2D NMS threshold
τnms2d = 0.7 for default hyper-parameter setting. The total
training time is about 30 hours, and FPS is measured with
FP16-precision and batch size of 1 on a single GPU.
4.2
Intriguing Properties
DiffusionTrack has several intriguing properties, such as the
ability to achieve better accuracy through more boxes or/and
more refining steps at the higher latency cost, and strong
robustness to detection perturbation for safety application.
Dynamic boxes and progressive refinement. Once the
model is trained, it can be used by changing the number of
boxes and the number of sample steps in inference. There-
fore, we can deploy a single DiffusionTrack to multiple
scenes and obtain a desired speed-accuracy trade-off without
retraining the network. In Figure 4a, we evaluate Diffusion-
Track with 500, 800, and 1000 proposal boxes by increasing
their sampling steps from 1 to 8, showing that high MOTA
in DiffusionTrack could be achieved by either increasing the
number of random boxes or the sampling steps.
Robustness to detection perturbation. Almost all previ-
ous approaches are very sensitive to detection perturbation
which poses significant risks to safety-critical applications
such as autonomous driving. Figure 4b shows the robust-
ness of the four mainstream trackers under detection per-
turbation. As can be seen from the performance compari-
son, DiffusionTrack has no performance penalty for pertur-
bation, while other trackers are severely affected, especially
the two-stage ByteTrack.
4.3
Ablation Study
We conduct ablation experiments on several relevant factors
in Figure 3 to study DiffusionTrack in detail.
Proportion of prior information. In contrast to object de-
tection, multi-object tracking has prior information about the
object location in the previous frame t −1. When construct-
ing Ntest proposal boxes, we can control the proportion of
prior information by simply repeating prior boxes. we can
find that an appropriate proportion of prior information can
improve the tracking performance from Table 1a.
Box padding strategy. Table 1b shows different box
padding strategies. Our Concatenating Gaussian random
boxes outperforms repeating existing prior boxes, concate-
nating random boxes in different noise types or image-size.
Perturbation schedule. Proposal boxes are initialized by
adding Gaussian noise to padded prior boxes under the con-
trol of αt. We need a perturbation schedule to deal with com-
plicated scenes, such as a larger αt when facing non-linear
object motion. The perturbation schedule can be modeled by
t and formulated as t = 1000 · f(x), where x is the average
percentage of object motion cross two frames and f is the
perturbation schedule function. As shown in Table 1c, us-
ing a logarithmic function f(x) = log(x+1)
log2
as perturbation
schedule works best.
Efficiency comparison. Table 1d shows the efficiency com-
parison with different numbers of proposal boxes and sam-
pling steps. The run time is evaluated on a single NVIDIA
GeForce 3090 GPU with a mini-batch size of 1 and FP16-
precision. We observe that more refinements cost brings
more performance gain and results in less FPS. Diffusion-
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3996


## Page 7

MOT17
MOT20
Methods
MOTA↑IDF1↑HOTA↑AssA↑DetA↑IDs↓Frag↓
MOTA↑IDF1↑HOTA↑AssA↑DetA↑IDs↓Frag↓
Two-Stage:
OC-SORT
78.0
77.5
63.2
63.4
63.2
1950 2040
75.7
76.3
62.4
62.5
62.4
942 1086
BoT-SORT
80.5
80.2
65.0
65.5
64.9
1212 1803
77.8
77.5
63.3
62.9
64.0 1313 1545
Bytetrack
80.3
77.3
63.1
62.0
64.5
2196 2277
77.8
75.2
61.3
59.6
63.4 1223 1460
StrongSORT
79.6
79.5
64.4
64.4
64.6
1194 1866
73.8
77.0
62.6
64.0
61.3
770 1003
P3AFormer
81.2
78.1
/
/
/
1893
/
78.1
76.4
/
/
/
1332
/
GMTracker
61.5
66.9
/
/
/
2415
/
/
/
/
/
/
/
/
GNMOT
50.2
47.0
/
/
/
5273
/
/
76.4
/
/
/
/
/
One-Stage:
TrackFormer
74.1
68.0
57.3
54.1
60.9
2829 4221
68.6
65.7
54.7
53.0
56.7 1532 2474
MeMOT
72.5
69.0
56.9
55.2
/
2724
/
63.7
66.1
54.1
55.0
/
1938
/
MOTR
71.9
68.4
57.2
55.8
/
2115 3897
/
/
/
/
/
/
/
CenterTrack
67.8
64.7
52.2
51.0
53.8
3039 6102
/
/
/
/
/
/
/
PermaTrack
73.8
68.9
55.5
53.1
58.5
3699 6132
/
/
/
/
/
/
/
TransCenter
73.2
62.2
54.5
49.7
60.1
4614 9519
67.7
58.7
/
/
/
3759
/
GTR
75.3
71.5
59.1
57.0
61.6
2859
/
/
/
/
/
/
/
/
TubeTK
63.0
58.6
/
/
/
4137
/
/
/
/
/
/
/
/
Baseline
74.6
66.7
55.9
50.8
61.9 16375 7206
63.3
49.5
42.5
34.7
52.5 9990 6710
DiffusionTrack
77.9
73.8
60.8
58.8
63.2
3819 4815
72.8
66.3
55.3
51.3
59.9 4117 4446
Table 2: Performance comparison to state-of-the-art approaches on the MOT17 and MOT20 test set with the private detections.
The best results are shown in bold. The offline method is marked in underline.
Methods
HOTA↑MOTA ↑DetA↑AssA ↑IDF1↑
QDTrack
45.7
83.0
72.1
29.2
44.8
TraDes
43.3
86.2
74.5
25.4
41.2
SORT
47.9
91.8
72.0
31.2
50.8
ByteTrack
47.3
89.5
71.6
31.4
52.5
OC-SORT
54.6
89.6
80.4
40.2
54.6
TransTrack
45.5
88.4
75.9
27.5
45.2
CenterTrack
41.8
86.8
78.1
22.6
35.7
GTR
48.0
84.7
72.5
31.9
50.3
Baseline
44.0
79.4
74.1
26.2
40.2
DiffusionTrack
52.4
89.3
82.2
33.5
47.5
Table 3: Performance comparison to state-of-the-art ap-
proaches on the DanceTrack test set. The best results are
shown in bold. Offline method is marked in underline
Track can flexibly choose different settings for every single
frame to deal with complicated scenes within a video.
4.4
State-of-the-art Comparison
Here we report the benchmark results of DiffusionTrack and
baseline compared with other mainstream methods on mul-
tiple datasets. We evaluated DiffusionTrack on DanceTrack,
MOT17, and MOT20 test datasets with 500, 800, and 1000
noise boxes respectively in same default setting.
MOT17 and MOT20. We use the standard split and obtain
the test set evaluation by submitting the results to the online
website. As can be seen from the performance comparison in
Table2, our DiffusionTrack achieves state-of-the-art both in
MOT17 and MOT20 for one-stage methods with the MOTA
of 77.9 and 72.8 respectively.
DanceTrack. To evaluate DiffusionTrack under challenging
non-linear object motion, we report results on the Dance-
Track in Table 3. DiffusionTrack achieves the state-of-the-
art on DanceTrack with HOTA (52.4).
The baseline model has a close performance to Diffusion-
Track on MOT17 but performs very poorly on MOT20 and
DanceTrack. In our understanding, Baseline simply learns a
coordinate regression between boxes Bt−1 and boxes Bt at
conditioned on the pooled features at time t −1 which can
not deal with crowed and non-linear object motion problem.
We guess the coarse-to-fine diffusion process is a special
data-augmented method that can enable DiffusionTrack to
discriminate between various objects.
5
Conclusion
In this work, we propose a novel end-to-end multi-object
tracking approach that formulates object detection and as-
sociation jointly as a consistent denoising diffusion process
from paired noise boxes to object association. Our noise-to-
tracking pipeline has several appealing properties, such as
dynamic box and progressive refinement, consistent model
structure, and robustness to perturbation detection results,
enabling us to to obtain the desired speed-accuracy trade-
off with same network parameters. Extensive experiments
show that DiffusionTrack achieves favorable performance
compared to previous strong baseline methods. We hope that
our work will provide a interesting insight into multi-object
tracking from the perspective of the diffusion model, and
that the performance of a wide variety of trackers can be
enhanced by local or global denoising processes.
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3997


## Page 8

Acknowledgments
Min Yang was supported by National Key Research and
Development
Program
of
China
(2022YFF0902100),
Shenzhen
Scienceand
Technology
Innovation
Pro-
gram
(KOTD20190929172835662).
Shenzhen
Basic
Research
Foundation
(JCYJ20210324115614039
and
JCYJ20200109113441941). The computation is completed
in the HPC Platform of Huazhong University of Science
and Technology.
References
Aharon, N.; Orfaig, R.; and Bobrovsky, B.-Z. 2022. BoT-
SORT: Robust associations multi-pedestrian tracking. arXiv
preprint arXiv:2206.14651.
Bergmann, P.; Meinhardt, T.; and Leal-Taixe, L. 2019a.
Tracking without bells and whistles. In Proceedings of the
IEEE/CVF International Conference on Computer Vision,
941–951.
Bergmann, P.; Meinhardt, T.; and Leal-Taixe, L. 2019b.
Tracking without bells and whistles. In Proceedings of the
ICCV, 941–951.
Bernardin, K.; and Stiefelhagen, R. 2008. Evaluating mul-
tiple object tracking performance: the clear mot metrics.
EURASIP Journal on Image and Video Processing, 2008:
1–10.
Bewley, A.; Ge, Z.; Ott, L.; Ramos, F.; and Upcroft, B. 2016.
Simple online and realtime tracking. In 2016 IEEE interna-
tional conference on image processing (ICIP), 3464–3468.
IEEE.
Bochkovskiy, A.; Wang, C.-Y.; and Liao, H.-Y. M. 2020.
Yolov4: Optimal speed and accuracy of object detection.
arXiv preprint arXiv:2004.10934.
Bras´o, G.; and Leal-Taix´e, L. 2020.
Learning a neural
solver for multiple object tracking.
In Proceedings of
the IEEE/CVF conference on computer vision and pattern
recognition, 6247–6257.
Cai, J.; Xu, M.; Li, W.; Xiong, Y.; Xia, W.; Tu, Z.; and
Soatto, S. 2022. MeMOT: multi-object tracking with mem-
ory. In Proceedings of the CVPR, 8090–8100.
Cao, J.; Weng, X.; Khirodkar, R.; Pang, J.; and Kitani, K.
2022. Observation-centric sort: Rethinking sort for robust
multi-object tracking. arXiv preprint arXiv:2203.14360.
Carion, N.; Massa, F.; Synnaeve, G.; Usunier, N.; Kirillov,
A.; and Zagoruyko, S. 2020. End-to-end object detection
with transformers. In Proceedings of the ECCV, 213–229.
Springer.
Chen, L.; Ai, H.; Zhuang, Z.; and Shang, C. 2018. Real-
time multiple people tracking with deeply learned candidate
selection and person re-identification. In 2018 IEEE inter-
national conference on multimedia and expo (ICME), 1–6.
IEEE.
Chen, S.; Sun, P.; Song, Y.; and Luo, P. 2022. Diffusion-
det: Diffusion model for object detection.
arXiv preprint
arXiv:2211.09788.
Chen, X.; Yan, B.; Zhu, J.; Wang, D.; Yang, X.; and Lu, H.
2021. Transformer tracking. In Proceedings of the CVPR,
8126–8135.
Dendorfer, P.; Rezatofighi, H.; Milan, A.; Shi, J.; Cremers,
D.; Reid, I.; Roth, S.; Schindler, K.; and Leal-Taix´e, L. 2020.
Mot20: A benchmark for multi object tracking in crowded
scenes. arXiv preprint arXiv:2003.09003.
Du,
Y.;
Song,
Y.;
Yang,
B.;
and
Zhao,
Y.
2022.
Strongsort: Make deepsort great again.
arXiv preprint
arXiv:2202.13514.
Duan, K.; Bai, S.; Xie, L.; Qi, H.; Huang, Q.; and Tian, Q.
2019. Centernet: Keypoint triplets for object detection. In
Proceedings of the ICCV, 6569–6578.
Ge, Z.; Liu, S.; Wang, F.; Li, Z.; and Sun, J. 2021.
Yolox: Exceeding yolo series in 2021.
arXiv preprint
arXiv:2107.08430.
Gori, M.; Monfardini, G.; and Scarselli, F. 2005.
A new
model for learning in graph domains. In Proceedings. 2005
IEEE International Joint Conference on Neural Networks,
2005., volume 2, 729–734. IEEE.
Gu, Z.; Chen, H.; Xu, Z.; Lan, J.; Meng, C.; and Wang, W.
2022. DiffusionInst: Diffusion Model for Instance Segmen-
tation. arXiv preprint arXiv:2212.02773.
He, J.; Huang, Z.; Wang, N.; and Zhang, Z. 2021. Learnable
graph matching: Incorporating graph partitioning with deep
feature learning for multiple object tracking. In Proceedings
of the CVPR, 5299–5309.
Ho, J.; Jain, A.; and Abbeel, P. 2020. Denoising diffusion
probabilistic models. Advances in Neural Information Pro-
cessing Systems, 33: 6840–6851.
Jiang, B.; Luo, R.; Mao, J.; Xiao, T.; and Jiang, Y. 2018. Ac-
quisition of localization confidence for accurate object de-
tection. In Proceedings of the ECCV, 784–799.
Jiang, X.; Li, P.; Li, Y.; and Zhen, X. 2019.
Graph neu-
ral based end-to-end data association framework for online
multiple-object tracking. arXiv preprint arXiv:1907.05315.
Kipf, T. N.; and Welling, M. 2016. Semi-supervised classi-
fication with graph convolutional networks. arXiv preprint
arXiv:1609.02907.
Kuhn, H. W. 1955. The Hungarian method for the assign-
ment problem. Naval research logistics quarterly, 2(1-2):
83–97.
Li, J.; Gao, X.; and Jiang, T. 2020. Graph networks for mul-
tiple object tracking. In Proceedings of the IEEE/CVF win-
ter conference on applications of computer vision, 719–728.
Lin, T.; Goyal, P.; Girshick, R.; He, K.; and Doll´ar, P. 2017.
Focal Loss for Dense Object Detection.
IEEE TPAMI,
PP(99): 2999–3007.
Lin, T.-Y.; Doll´ar, P.; Girshick, R.; He, K.; Hariharan, B.;
and Belongie, S. 2017. Feature pyramid networks for object
detection. In Proceedings of the CVPR, 2117–2125.
Liu, Z.; Wang, X.; Wang, C.; Liu, W.; and Bai, X. 2023.
SparseTrack: Multi-Object Tracking by Performing Scene
Decomposition based on Pseudo-Depth.
Loshchilov, I.; and Hutter, F. 2018. Decoupled weight decay
regularization. In Proceedings of the ICLR.
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3998


## Page 9

Luiten, J.; Osep, A.; Dendorfer, P.; Torr, P.; Geiger, A.; Leal-
Taix´e, L.; and Leibe, B. 2021. Hota: A higher order metric
for evaluating multi-object tracking. International journal
of computer vision, 129: 548–578.
Meinhardt, T.; Kirillov, A.; Leal-Taixe, L.; and Feichten-
hofer, C. 2022.
Trackformer: Multi-object tracking with
transformers. In Proceedings of the CVPR, 8844–8854.
Milan, A.; Leal-Taix´e, L.; Reid, I.; Roth, S.; and Schindler,
K. 2016. MOT16: A benchmark for multi-object tracking.
arXiv preprint arXiv:1603.00831.
Pang, B.; Li, Y.; Zhang, Y.; Li, M.; and Lu, C. 2020. Tubetk:
Adopting tubes to track multi-object in a one-step training
model. In Proceedings of the IEEE/CVF conference on com-
puter vision and pattern recognition, 6308–6318.
Rangesh, A.; Maheshwari, P.; Gebre, M.; Mhatre, S.;
Ramezani, V.; and Trivedi, M. M. 2021.
Trackmpnn: A
message passing graph neural architecture for multi-object
tracking. arXiv preprint arXiv:2101.04206.
Ren, S.; He, K.; Girshick, R.; and Sun, J. 2015. Faster r-cnn:
Towards real-time object detection with region proposal net-
works. Advances in neural information processing systems,
28.
Rezatofighi, H.; Tsoi, N.; Gwak, J.; Sadeghian, A.; Reid, I.;
and Savarese, S. 2019. Generalized intersection over union:
A metric and a loss for bounding box regression. In Pro-
ceedings of the CVPR, 658–666.
Ristani, E.; Solera, F.; Zou, R.; Cucchiara, R.; and Tomasi,
C. 2016. Performance measures and a data set for multi-
target, multi-camera tracking. In Proceedings of the ECCV,
17–35. Springer.
Song, Y.; and Ermon, S. 2019. Generative modeling by esti-
mating gradients of the data distribution. Advances in neural
information processing systems, 32.
Song, Y.; Sohl-Dickstein, J.; Kingma, D. P.; Kumar, A.; Er-
mon, S.; and Poole, B. 2020. Score-based generative model-
ing through stochastic differential equations. arXiv preprint
arXiv:2011.13456.
Sun, P.; Cao, J.; Jiang, Y.; Yuan, Z.; Bai, S.; Kitani, K.;
and Luo, P. 2022. Dancetrack: Multi-object tracking in uni-
form appearance and diverse motion. In Proceedings of the
CVPR, 20993–21002.
Sun, P.; Cao, J.; Jiang, Y.; Zhang, R.; Xie, E.; Yuan, Z.;
Wang, C.; and Luo, P. 2020.
Transtrack: Multiple object
tracking with transformer. arXiv preprint arXiv:2012.15460.
Tokmakov, P.; Li, J.; Burgard, W.; and Gaidon, A. 2021.
Learning to track with object permanence. In Proceedings
of the ICCV, 10860–10869.
Welch, G.; Bishop, G.; et al. 1995. An introduction to the
Kalman filter.
Wojke, N.; Bewley, A.; and Paulus, D. 2017. Simple on-
line and realtime tracking with a deep association metric.
In 2017 IEEE international conference on image processing
(ICIP), 3645–3649. IEEE.
Xu, Y.; Ban, Y.; Delorme, G.; Gan, C.; Rus, D.; and
Alameda-Pineda, X. 2022. TransCenter: Transformers with
dense representations for multiple-object tracking.
IEEE
Transactions on Pattern Analysis and Machine Intelligence.
Zeng, F.; Dong, B.; Zhang, Y.; Wang, T.; Zhang, X.; and
Wei, Y. 2022.
Motr: End-to-end multiple-object tracking
with transformer. In Proceedings of the ECCV, 659–675.
Zhang, H.; Cisse, M.; Dauphin, Y. N.; and Lopez-Paz, D.
2017. mixup: Beyond empirical risk minimization. arXiv
preprint arXiv:1710.09412.
Zhang, L.; Li, Y.; and Nevatia, R. 2008. Global data associ-
ation for multi-object tracking using network flows. In 2008
IEEE conference on computer vision and pattern recogni-
tion, 1–8. IEEE.
Zhang, Y.; Sun, P.; Jiang, Y.; Yu, D.; Weng, F.; Yuan, Z.;
Luo, P.; Liu, W.; and Wang, X. 2022.
Bytetrack: Multi-
object tracking by associating every detection box. In Pro-
ceedings of the ECCV, 1–21. Springer.
Zhang, Y.; Wang, C.; Wang, X.; Zeng, W.; and Liu, W. 2021.
Fairmot: On the fairness of detection and re-identification in
multiple object tracking. International Journal of Computer
Vision, 129: 3069–3087.
Zhao, Z.; Wu, Z.; Zhuang, Y.; Li, B.; and Jia, J. 2022. Track-
ing objects as pixel-wise distributions. In Proceedings of the
ECCV, 76–94. Springer.
Zhou, X.; Koltun, V.; and Kr¨ahenb¨uhl, P. 2020. Tracking
objects as points. In Proceedings of the ECCV, 474–490.
Springer.
Zhou, X.; Yin, T.; Koltun, V.; and Kr¨ahenb¨uhl, P. 2022.
Global Tracking Transformers. In CVPR.
Zhu, X.; Su, W.; Lu, L.; Li, B.; Wang, X.; and Dai, J. 2020.
Deformable detr: Deformable transformers for end-to-end
object detection. arXiv preprint arXiv:2010.04159.
The Thirty-Eighth AAAI Conference on Artiﬁcial Intelligence (AAAI-24)
3999
