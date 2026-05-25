---
source_id: S006
title: DEIM: DETR with Improved Matching for Fast Convergence
source_url: https://openaccess.thecvf.com/content/CVPR2025/papers/Huang_DEIM_DETR_with_Improved_Matching_for_Fast_Convergence_CVPR_2025_paper.pdf
source_file: docs/research/papers/S006-deim-detr-with-improved-matching-for-fast-convergence.pdf
source_kind: pdf
extraction_note: downloaded PDF retry
---

# Extracted text: S006-deim-detr-with-improved-matching-for-fast-convergence.pdf


## Page 1

DEIM: DETR with Improved Matching for Fast Convergence
Shihua Huang1†
Zhichao Lu2
Xiaodong Cun3
Yongjun Yu1
Xiao Zhou4
Xi Shen1B
1Intellindust AI Lab
2City University of Hong Kong
3Great Bay University
4Hefei Normal University
B Corresponding author: shenxiluc@gmail.com; † Project lead.
20
40
60
80
500
Training Epochs
48
49
50
51
52
53
54
55
56
COCO APval
2 ×  faster in convergence
<<
DEIM-D-FINE-L
D-FINE-L
YOLOv11
RT-DETRv2-R50
(a) Faster: training is more compute-efficient
2
4
6
8
10
12
14
Latency on T4 GPU (ms)
46
48
50
52
54
56
58
COCO APval
49.0
52.7
54.7
56.5
Ours
D-FINE
YOLOv11
YOLOv10
RT-DETRv3
RT-DETRv2
RT-DETR
(b) Better: exceeding all real-time detectors
Figure 1. Comparison with state-of-the-art real-time object detectors on COCO [20]. The proposed DEIM achieves faster convergence (a)
and superior performance in terms of average precision (AP) and latency (b) when compared to state-of-the-art real-time object detectors.
Abstract
We introduce DEIM, an innovative and efficient train-
ing framework designed to accelerate convergence in real-
time object detection with Transformer-based architectures
(DETR). To mitigate the sparse supervision inherent in one-
to-one (O2O) matching in DETR models, DEIM employs
a Dense O2O matching strategy. This approach increases
the number of positive samples per image by incorporat-
ing additional targets, using standard data augmentation
techniques. While Dense O2O matching speeds up conver-
gence, it also introduces numerous low-quality matches that
could affect performance. To address this, we propose the
Matchability-Aware Loss (MAL), a novel loss function that
optimizes matches across various quality levels, enhancing
the effectiveness of Dense O2O. Extensive experiments on
the COCO dataset validate the efficacy of DEIM. When in-
tegrated with RT-DETR and D-FINE, it consistently boosts
performance while reducing training time by 50%.
No-
tably, paired with RT-DETRv2, DEIM achieves 53.2% AP
in a single day of training on an NVIDIA 4090 GPU. Addi-
tionally, DEIM-trained real-time models outperform lead-
ing real-time object detectors, with DEIM-D-FINE-L and
DEIM-D-FINE-X achieving 54.7% and 56.5% AP at 124
and 78 FPS on an NVIDIA T4 GPU, respectively, with-
out the need for additional data. We believe DEIM sets a
new baseline for advancements in real-time object detec-
tion.
Our code and pre-trained models are available at
https://www.shihuahuang.cn/DEIM/.
1. Introduction
Object detection is a fundamental task in computer vision,
widely applied in fields like autonomous driving [5, 6],
robot navigation [9], etc.
The growing demand for effi-
cient detectors has spurred the development of real-time
detection methods. In particular, YOLO emerges as one
of the main paradigms for real-time object detection, ow-
ing to its compelling trade-off between latency and accu-
racy [1, 28, 32, 34, 44]. YOLO models are widely recog-
nized as one-stage detectors based on convolutional neu-
ral networks. One-to-many (O2M) assignment strategy has
been widely used in YOLO series [1, 28, 34, 44], where
each target box is associated with multiple anchors. This
strategy is known to be effective, as it provides dense super-
vision signals, which accelerate convergence and enhance
This CVPR paper is the Open Access version, provided by the Computer Vision Foundation.
Except for this watermark, it is identical to the accepted version;
the final published version of the proceedings is available on IEEE Xplore.
15162


## Page 2

performance [44]. However, it produces multiple overlap-
ping bounding boxes per object, requiring a hand-crafted
Non-Maximum Suppression (NMS) to remove redundan-
cies, introducing latency and instability [32, 43].
The advent of Transformer-based detection (DETR)
paradigm [3] has attracted significant attention [4, 39, 46],
leveraging multi-head attention to capture global context,
thereby enhancing localization and classification. DETRs
adopt a one-to-one (O2O) matching strategy that leverages
the Hungarian [16] algorithm to establish a unique corre-
spondence between predicted boxes and the ground-truth
objects during training, eliminating the need for NMS. This
end-to-end framework offers a compelling alternative for
real-time object detection.
However, slow convergence remains one of the primary
limitations of DETRs, and we hypothesize that the rea-
sons are two-fold. ❶Sparse supervision: The O2O match-
ing mechanism assigns only one positive sample per target,
greatly limiting the number of positive samples. In con-
trast, O2M generates several times more positive samples.
This scarcity of positive samples restricts dense supervision,
which impedes effective model learning—particularly for
small objects, where dense supervision is crucial for perfor-
mance. ❷Low-quality matches: Unlike traditional methods
that rely on dense anchors (usually > 8000), DETR em-
ploys a small number (100 or 300) of randomly initialized
queries. These queries lack spatial alignment with targets,
leading to numerous low-quality matches in the training,
where matched boxes have low IoU with the targets but high
confidence scores.
To address the scarcity of supervision in DETR, recent
studies have relaxed the constraints of O2O matching by in-
corporating O2M assignments into O2O training, thereby
introducing auxiliary positive samples per target to increase
supervision. Group DETR [4] achieves this by using mul-
tiple query groups, each with independent O2O matching,
while Co-DETR [46] incorporates O2M methods from ob-
ject detectors like Faster R-CNN [29] and FCOS [31]. Al-
though these approaches successfully increase the number
of positive samples, they also require additional decoders,
which increases computational overhead and risks generat-
ing redundant high-quality predictions as traditional detec-
tors. In contrast, we propose a novel yet straightforward
approach named dense one-to-one (Dense O2O) match-
ing. Our key idea is to increase the number of targets in
each training image, which in turn generates more posi-
tive samples during the training. Notably, this can be eas-
ily achieved using classical techniques such as mosaic [1]
and mixup [38] augmentations, which generates additional
positive samples per image while preserving the one-to-one
matching framework. Dense O2O matching can provide a
level of supervision comparable to O2M approaches, with-
out the added complexity and overhead typically associated
with O2M methods.
Despite attempts to improve query initialization using
priors [18, 39, 43, 45], which enable more effective query
distributions around objects. These improved initialization
methods, often relying on limited feature information ex-
tracted from the encoder [39, 43], tend to cluster queries
around a few prominent objects.
In contrast, most non-
salient objects lack nearby queries, leading to low-quality
matches. This issue becomes even more pronounced when
using Dense O2O. As the number of targets increases,
the disparity between prominent and non-prominent targets
grows, leading to a rise in low-quality matches despite the
overall increase in matching quantity. In this case, if the
loss function has limitations in handling these low-quality
matches, this disparity will persist, hindering the model
from achieving better performance.
Existing loss functions [19, 40] in DETRs, such as Vari-
focal Loss (VFL) [40], are tailored to dense anchors where
the number of low-quality matches is relatively low. They
primarily penalize high-quality matches, especially matches
with high IoU but low confidence, and discard low-quality
matches. To address low-quality matches and further im-
prove Dense O2O, we propose Matchability-Aware Loss
(MAL). MAL scales the penalty based on matchability by
incorporating the IoU between matched queries and targets
with classification confidence. MAL performs similarly to
VFL for high-quality matches but places greater empha-
sis on low-quality matches, improving the utility of limited
positive samples during training. Furthermore, MAL pro-
vides a simpler mathematical formulation than VFL.
The proposed DEIM combines Dense O2O with MAL
to create an effective training framework. We conducted
extensive experiments on the COCO [20] dataset to evalu-
ate the effectiveness of DEIM. The results in Fig. 1 (a) show
that DEIM significantly accelerates the convergence of RT-
DETRv2 [24] and D-FINE [27] and achieves improved per-
formance as well. Specifically, with only half the number of
training epochs, our method outperforms RT-DETRv2 and
D-FINE by 0.2 and 0.6 AP, respectively. Additionally, our
approach enables training a ResNet50-based DETR model
on a single 4090 GPU, achieving 53.2% mAP within a sin-
gle day (approximately 24 epochs). By incorporating more
efficient models, we also introduce a new set of real-time
detectors that outperform existing models, including the lat-
est YOLOv11 [13], setting a new state-of-the-art (SoTA) for
real-time object detection (Fig. 1 (b)).
The main contributions of this work are summarized as
follows:
• We introduce DEIM, a simple and flexible training frame-
work for real-time object detection.
• DEIM accelerates the convergence by improving the
quantity and quality of matching with Dense O2O and
MAL, respectively.
15163


## Page 3

(a) O2M: 1 target and 4 pos.
(b) O2O: 1 target and 1 pos.
(c) Dense O2O by stitching: 4 targets and 4 pos.
(d) Low-quality matching
(e) Loss landscape of VFL
(f) Loss landscape of MAL
Figure 2. An illustration of our proposed DEIM. Yellow, red, and green boxes represent the GT, positive and negative samples, respec-
tively. ’pos.’ denotes the positive samples. Top: Our Dense O2O (Fig. 2c) can provide the same quality of positive samples as O2M
(Fig. 2a). Bottom: For the low-quality matching, its loss values when using VFL [40] and MAL are marked by ⋆, indicating MAL can
optimize those cases more effectively.
• With our method, existing real-time DETRs achieve bet-
ter performance while halving training costs. Specifically,
our method exceeds YOLOs and establishes a new SoTA
in real-time object detection after being paired with effi-
cient models in D-FINE.
2. Related Work
Object detection with transformer (DETR) [3] represents
a shift from traditional CNN architectures to transformers.
By using Hungarian [16] algorithm for one-to-one match-
ing, DETR eliminates the need for hand-crafted NMS as
the post-processing and enables end-to-end object detec-
tion. However, it suffers from slow convergence and dense
computation.
Increasing positive samples.
One-to-one matching lim-
its each target to a single positive sample, providing far
less supervision than O2M and hindering the optimiza-
tion. Some studies have explored ways to increase super-
vision within the O2O framework. Group DETR [4], for
instance, employs the concept of “groups” to approximate
the O2M. It uses K groups of queries, where K > 1, and
performs O2O matching independently within each group.
This allows each target to be assigned K positive sam-
ples. However, to prevent communication between groups,
each group requires a separate decoder layer, ultimately
resulting in K parallel decoders.
The hybrid matching
scheme in H-DETR [15] works similarly to Group DETR.
Co-DETR [46] reveals that a one-to-many assignment ap-
proach helps the model learn more distinctive feature in-
formation, so it proposed a collaborative hybrid assignment
scheme to enhance encoder representations through auxil-
iary heads with one-to-many label assignments, like Faster
R-CNN [29] and FCOS [31]. The existing methods aim to
increase the number of positive samples per target to en-
hance supervision. In contrast, Our Dense O2O explores
another direction — increasing the number of targets per
training image to boost supervision effectively. Unlike ex-
isting methods, which require additional decoders or heads
and thus increase training resource consumption, our ap-
proach is computation-free.
Optimizing low-quality matches.
The sparse and ran-
domly initialized queries lack spatial alignment with tar-
gets, resulting in a high proportion of low-quality matches
that impede model convergence. Several methods have in-
troduced prior knowledge into query initialization, such as
anchor queries [35], DAB-DETR [21], DN-DETR [18], and
dense distinct queries [41]. More recently, inspired by two-
stage paradigms [29, 45], methods like DINO [39] and RT-
DETR [43] leverage top-ranked predictions from the en-
coder’s dense outputs to refine decoder queries [36]. These
strategies enable more effective query initialization closer
to target regions. However, low-quality matches persist as
15164


## Page 4

a significant challenge [22]. In RT-DETR [43], Varifocal
Loss (VFL) is employed to reduce the uncertainty between
classification confidence and box quality, enhancing real-
time performance. Yet, VFL is primarily designed for tra-
ditional detectors with fewer low-quality matches and fo-
cuses on high-IoU optimization, leaving low-IoU matches
under-optimized due to their minimal and flat loss values.
Building on those advanced initializations, we introduce a
matchability-aware loss to better optimize matches across
varying quality levels, significantly enhancing the effective-
ness of Dense O2O matching.
Reducing computation cost.
Standard attention mecha-
nisms involve dense computation. To improve efficiency
and facilitate interactions with multi-scale features, sev-
eral advanced attentions have been developed, such as
deformable attention [45], multi-scale deformable atten-
tion [42], dynamic attention [7], and cascade window at-
tention [37].
Additionally, recent research has focused
on creating more efficient encoders.
For example, Lite
DETR [17] introduces an encoder block that interleaves up-
dates between high-level and low-level features, while RT-
DETR [43] combines CNN and self-attention in its encoder.
Both designs significantly reduce resource consumption, es-
pecially RT-DETR. RT-DETR is the first real-time object
detection model within the DETR framework.
Building
on this hybrid encoder, D-FINE [27] further optimizes RT-
DETR with additional modules and refines the regression
process by iteratively updating probability distributions in-
stead of predicting fixed coordinates. This approach enables
D-FINE to achieve a more favorable trade-off between la-
tency and performance, slightly surpassing recent YOLO
models. Leveraging these advancements in real-time DE-
TRs, our method achieves impressive performance with re-
duced training costs, outperforming YOLO models by a
substantial margin in real-time object detection.
3. Method
3.1. Preliminaries
O2M vs. O2O.
The O2M assignment strategy [10, 44] is
widely adopted in traditional object detectors, and its super-
vision can be formulated as follows:
loss =
N
X
i=0
Mi
X
j=0
f(ˆyij, yi),
(1)
where N is the total number of targets, Mi is the number of
matches for the i-th target, ˆyij represents the j-th match for
the i-th target, yi denotes the i-th ground-truth label, and
f is the loss function. O2M enhances supervision by in-
creasing Mi, i.e., assigning multiple queries to each target
(Mi > 1) and thus providing dense supervision, as illus-
trated in Fig. 2a. In contrast, the O2O assignment only pairs
0
10
20
30
40
50
60
70
80
# Positive Samples
0.000
0.025
0.050
0.075
0.100
0.125
0.150
0.175
Density
Hungarian
SimOTA
(a) Matching distribution
1
2
3
4
5
6
7
8
9
10
Ratio
0.0
0.1
0.2
0.3
0.4
0.5
Density
(b) Ratios between O2M and O2O
Figure 3. Anchor/Query Match Comparison. Comparison of
the number of matched anchors/queries per image in one COCO
epoch using one-to-many (SimOTA [44]) and one-to-one (Hungar-
ian [3]) matching schemes.
each target with a single best prediction, determined via the
Hungarian algorithm, which minimizes a cost function bal-
ancing classification and localization errors (Fig. 2b). O2O
can be considered a special case of O2M where Mi = 1 for
all targets.
Focal loss.
Focal loss (FL) [19] was introduced to pre-
vent an abundance of easy negatives from overwhelming
the detector during training, directing focus instead towards
a sparse set of hard examples. It serves as the default clas-
sification loss in DETRs [39, 45] and is defined as follows:
FL(p, y) =
(
−α(1 −p)γ log(p)
y = 1
−(1 −α)pγ log(1 −p)
y = 0,
(2)
where y ∈{0, 1} specifies the ground-truth class and p ∈
[0, 1] represents the predicted probability for the foreground
class. The parameter γ controls the balance between easy
and hard samples, while α adjusts the weighting between
foreground and background classes. In the FL, only the
sample’s class and confidence are considered, with no at-
tention given to bounding box quality, i.e., localization.
3.2. Improving matching efficiency: Dense O2O
The one-to-one (O2O) matching scheme, commonly used
in DETR-based models, matches each target to only one
predicted query. This approach, implemented via the Hun-
garian algorithm [16], allows for end-to-end training and
eliminates the need for NMS. However, a key limitation of
O2O is that it generates significantly fewer positive sam-
ples compared to traditional one-to-many (O2M) methods
like SimOTA [44]. This leads to sparse supervision, which
can slow down convergence during training.
To better understand this issue,
we trained RT-
DETRv2 [24] with a ResNet50 backbone on the MS COCO
dataset [20]. We compared the number of positive matches
generated by both Hungarian (O2O) and SimOTA (O2M)
strategies. As shown in Fig. 3a, O2O produces a sharp peak
under 10 positive matches per image, while O2M generates
a broader distribution with many more positive matches,
15165


## Page 5

sometimes exceeding 80 positive samples for a single im-
age. Fig. 3b further highlights that SimOTA generates about
10 times as many matches as O2O in extreme cases. This
demonstrates that O2O has fewer positive matches, poten-
tially slowing down optimization.
We propose Dense O2O as an efficient alternative. This
strategy retains the one-to-one matching structure of O2O
(with Mi = 1), but increases the number of targets (N)
per image, achieving denser supervision. For example, as
shown in Fig. 2c, we replicate the original image into four
quadrants and combine them into a single composite im-
age, maintaining the original image dimensions. This in-
creases the number of targets from 1 to 4, boosting the su-
pervision level in Eq. 1 while keeping the matching struc-
ture unchanged. Dense O2O achieves a level of supervision
comparable to O2M but without the added complexity and
computational overhead.
3.3. Improving matching quality:
Matchability-
Aware Loss
Limitations of VFL.
The VariFocal Loss (VFL) [40],
built on the FL [19], has been shown to improve object
detection performance, especially in DETR models [2, 24,
43]. VFL loss is expressed as :
VFL(p, q, y) =
(
−q(q log(p) + (1 −q) log(1 −p))
q > 0
−αpγ log(1 −p)
q = 0,
(3)
where q denotes the IoU between the predicted bounding
box and its target box. For foreground samples (q > 0),
the target label is set to q, while background samples (q =
0) have a target label of 0. VFL incorporates the IoU to
improve the quality of queries in DETR [43].
However, VFL has two key limitations when optimiz-
ing low-quality matches: i). Low-Quality Matches. VFL
focuses mainly on high-quality matches (high IoU). For
low-quality matches (low IoU), the loss remains small,
preventing the model from refining predictions for low-
quality boxes.
For low-quality matching (with low IoU,
e.g., Fig. 2d), however, the loss remains minimal (marked
by a ⋆in Fig. 2e). ii) Negative Samples. VFL treats matches
with no overlap as negative samples, which reduces the
number of positive samples and limits effective training.
These issues are less problematic for traditional detec-
tors due to their dense anchors and one-to-many assign-
ment strategies. However, in the DETR framework, where
queries are sparse and matching is more rigid, these limita-
tions become more pronounced.
Matchability-Aware Loss.
To address these issues, we
propose the Matchability-Aware Loss (MAL), which ex-
tends the benefits of VFL while mitigating its shortcom-
ings. MAL incorporates the matching quality directly into
(a) Low quality: IoU = 0.05
(b) High quality: IoU = 0.95
Figure 4. VFL vs. MAL Comparison. Comparison of VFL and
our MAL for low-quality (IoU = 0.05, Fig. 4a) and high-quality
(IoU = 0.95, Fig. 4b) matching cases.
the loss function, making it more sensitive to low-quality
matches. The formula for MAL is:
MAL(p, q, y) =
(
−qγ log(p) + (1 −qγ) log(1 −p)
y = 1
−pγ log(1 −p)
y = 0.
(4)
Compared to VFL, we introduce several small but impor-
tant changes. Specifically, the target label has been modi-
fied from q to qγ, simplifying the loss weights for positive
and negative samples and removing the hyperparameter α
used to balance positive and negative samples. This change
helps to avoid the overemphasis on high-quality boxes and
improves the overall training process. This can be easily
seen from the loss landscape between VFL (in Fig. 2e) and
MAL (in Fig. 2f). Note that the impact of γ is provided in
Section 4.5.
Comparison with VFL.
We compare MAL and VFL in
handling both low-quality and high-quality matches.
In
the case of low-quality matches (IoU = 0.05, in Fig. 4a),
MAL shows a sharper increase in loss as predicted confi-
dence grows, compared to VFL, which remains almost un-
changed. For high-quality matches (IoU = 0.95, in Fig. 4b),
both MAL and VFL perform similarly, confirming that
MAL improves training efficiency without compromising
the performance on high-quality matches.
4. Experiments
4.1. Training details
For Dense O2O, we apply mosaic augmentation [1] and
mixup augmentation [38] to generate additional positive
samples per image.
The impact of these augmentations
is discussed in Section 4.5. We train our models on the
MS-COCO dataset [20] using the AdamW optimizer [23].
Standard data augmentations, such as color jitter and zoom-
out, are used, as in RT-DETR [24, 43] and D-FINE [27].
We employ a flat cosine learning rate scheduler [25] and
propose a novel data augmentation scheduler. A data aug-
mentation warmup strategy is used in the first few train-
ing epochs (four usually) for simplifying attention learning.
15166


## Page 6

Table 1. Comparison with real-time object detectors on COCO [20] val2017. By integrating our method into D-FINE-L [27] and D-
FINE-X [27], we build DEIM-D-FINE-L and DEIM-D-FINE-X. We compare our method with YOLO-based and DETR-based real-time
object detectors. ⋆indicates that the NMS is tuned with a confidence threshold of 0.01.
Model
#Epochs
#Params
GFLOPs
Latency (ms)
APval
APval
50
APval
75
APval
S
APval
M
APval
L
YOLO-based Real-time Object Detectors
YOLOv8-L [12]
500
43
165
12.31
52.9
69.8
57.5
35.3
58.3
69.8
YOLOv8-X [12]
500
68
257
16.59
53.9
71.0
58.7
35.7
59.3
70.7
YOLOv9-C [34]
500
25
102
10.66
53.0
70.2
57.8
36.2
58.5
69.3
YOLOv9-E [34]
500
57
189
20.53
55.6
72.8
60.6
40.2
61.0
71.4
Gold-YOLO-L [33]
300
75
152
9.21
53.3
70.9
-
33.8
58.9
69.9
YOLOv10-L⋆[32]
500
24
120
7.66
53.2
70.1
58.1
35.8
58.5
69.4
YOLOv10-X⋆[32]
500
30
160
10.74
54.4
71.3
59.3
37.0
59.8
70.9
YOLO11-L⋆[13]
500
25
87
6.31
52.9
69.4
57.7
35.2
58.7
68.8
YOLO11-X⋆[13]
500
57
195
10.52
54.1
70.8
58.9
37.0
59.2
69.7
DETR-based Real-time Object Detectors
RT-DETR-HG-L [43]
72
32
107
8.77
53.0
71.7
57.3
34.6
57.4
71.2
RT-DETR-HG-X [43]
72
67
234
13.51
54.8
73.1
59.4
35.7
59.6
72.9
D-FINE-L [27]
72
31
91
8.07
54.0
71.6
58.4
36.5
58.0
71.9
DEIM-D-FINE-L
50
31
91
8.07
54.7
72.4
59.4
36.9
59.6
71.8
D-FINE-X [27]
72
62
202
12.89
55.8
73.7
60.2
37.3
60.5
73.4
DEIM-D-FINE-X
50
62
202
12.89
56.5
74.0
61.5
38.8
61.4
74.2
Disabling Dense O2O after 50% of training epochs leads to
better results. Following RT-DETRv2 [43], we turn off data
augmentation in the last two epochs. Our LR and DataAug
schedulers are depicted specifically in Fig. ??. Our back-
bones are pre-trained on ImageNet1k [8]. We evaluate our
models on the MS-COCO validation set at a resolution of
640 × 640. Additional details about the hyperparameters
are provided in the supplementary material.
4.2. Comparisons with real-time detectors
We integrate our method into D-FINE-L [27] and D-FINE-
X [27] building our DEIM-D-FINE-L and DEIM-D-FINE-
X. We then evaluate these models and benchmark their
real-time object detection performance against state-of-
the-art models, including YOLOv8 [12], YOLOv9 [34],
YOLOv10 [34], YOLOv11 [13], as well as DETR-based
models like RT-DETRv2 [24] and D-FINE [27].
Tab. 1
compares the models in terms of epochs, parameters,
GFLOPs, latency, and detection accuracy. Additional com-
parisons of smaller model variants (S and M) are included
in the supplementary material.
Our method outperforms the current state-of-the-art
models in training cost, inference latency, and detection ac-
curacy, setting a new benchmark for real-time object de-
tection. Note that D-FINE [27] is a very recent work that
enhances the performance of RT-DETRv2 [24] by incorpo-
rating distillation and bounding box refinement, establish-
ing itself as a leading real-time detector. Our DEIM fur-
ther boosts the performance of D-FINE, achieving a 0.7 AP
gain while reducing training costs by 30%, with no added
inference latency. The most significant improvement is ob-
served in small object detection, where D-FINE-X [27],
when trained with our method, achieves a 1.5 AP gain as
DEIM-D-FINE-X.
When compared directly to YOLOv11-X [13], our
DEIM-D-FINE-L outperforms this SoTA model, achiev-
ing slightly higher performance (54.7 vs.
54.1 AP) and
reducing inference time by 20% (8.07 ms vs. 10.74 ms).
Although YOLOv10 [34] uses a hybrid O2M and O2O
assignment strategy, our models consistently outperform
YOLOv10, demonstrating the effectiveness of Dense O2O.
Despite significant improvements in small object detec-
tion over other DETR-based models, our approach shows a
slight decrease in small object AP compared to YOLO mod-
els. For example, YOLOv9-E [34] outperforms D-FINE-
L [27] by approximately 1.4 AP on small objects, though
our model achieves a higher overall AP (56.5 vs. 55.6).
This gap underscores the ongoing challenges in small ob-
ject detection within the DETR architecture and suggests
potential areas for further improvement.
4.3. Comparisons with ResNet [14]-based DETRs
Most DETR research uses ResNet [14] as the backbone,
and to enable a comprehensive comparison across exist-
ing DETR variants, we also applied our method to RT-
DETRv2 [24], a state-of-the-art DETR variant. The results
are summarized in Tab. 2. Unlike the original DETR, which
requires 500 epochs for effective training, recent DETR
variants, including ours, reduce training time while im-
proving model performance. Our method shows the most
significant improvements, surpassing all variants after just
36 epochs. Specifically, DEIM reduces training time by
half and increases AP by 0.5 and 0.9 on RT-DETRv2 [24]
with ResNet-50 [14] and ResNet-101 [14] backbones, re-
spectively. Moreover, it outperforms DINO-Deformable-
DETR [39] by 2.7 AP with the ResNet-50 [14] backbone.
15167


## Page 7

Table 2.
Comparison with ResNet-based DETRs on COCO [20] val2017.
By integrating our method into ResNet50 [14] and
ResNet101 [14], we build DEIM-RT-DETRv2-R50 and DEIM-RT-DETRv2-R101. We compare our method with competitive DETR-
based object detectors that use ResNet50 [14] or ResNet101 [14] as backbones.
Model
#Epochs
#Params
GFLOPs
APval
APval
50
APval
75
APval
S
APval
M
APval
L
ResNet50 [14]-based
DETR-DC5 [3]
500
41
187
43.3
63.1
45.9
22.5
47.3
61.1
Anchor-DETR-DC5 [35]
50
39
172
44.2
64.7
47.5
24.7
48.2
60.6
Conditional-DETR-DC5 [26]
108
44
195
45.1
65.4
48.5
25.3
49.0
62.2
Efficient-DETR [36]
36
35
210
45.1
63.1
49.1
28.3
48.4
59.0
SMCA-DETR [11]
108
40
152
45.6
65.5
49.1
25.9
49.3
62.6
Deformable-DETR [45]
50
40
173
46.2
65.2
50.0
28.8
49.2
61.7
DAB-Deformable-DETR [21]
50
48
195
46.9
66.0
50.8
30.1
50.4
62.5
DN-Deformable-DETR [18]
50
48
195
48.6
67.4
52.7
31.0
52.0
63.7
DINO-Deformable-DETR [39]
36
47
279
50.9
69.0
55.3
34.6
54.1
64.6
RT-DETR [43]
72
42
136
53.1
71.3
57.7
34.8
58.0
70.0
RT-DETRv2 [24]
72
42
136
53.4
71.6
57.4
36.1
57.9
70.8
DEIM-RT-DETRv2
36
42
136
53.9
71.7
58.6
36.7
58.9
70.9
DEIM-RT-DETRv2
60
42
136
54.3
72.3
58.8
37.5
58.7
70.8
ResNet101 [14]-based
DETR-DC5 [3]
500
60
253
44.9
64.7
47.7
23.7
49.5
62.3
Anchor-DETR-DC5 [35]
50
-
-
45.1
65.7
48.8
25.8
49.4
61.6
Conditional-DETR-DC5 [26]
108
63
262
45.9
66.8
49.5
27.2
50.3
63.3
Efficient-DETR [36]
36
54
289
45.7
64.1
49.5
28.2
49.1
60.2
SMCA-DETR [11]
108
58
218
46.3
66.6
50.2
27.2
50.5
63.2
RT-DETR [43]
72
76
259
54.3
72.7
58.6
36.0
58.8
72.1
RT-DETRv2 [24]
72
76
259
54.3
72.8
58.8
35.8
58.8
72.1
DEIM-RT-DETRv2
36
76
259
55.2
73.3
59.9
37.8
59.6
72.8
DEIM-RT-DETRv2
60
76
259
55.5
73.5
60.3
37.9
59.9
73.0
Table 3. Comparison of the D-FINE and when with our DEIM
on CrowdHuman [30]. Both are trained with 120 epochs.
Method
AP
AP50
AP75
APs
APm
APl
D-FINE-L
56.0
87.2
59.4
29.0
46.1
54.6
w/ DEIM
57.5
87.6
62.9
33.2
48.7
55.7
DEIM also significantly enhances small-object detec-
tion.
For example, while achieving comparable overall
AP to RT-DETRv2 [24], our DEIM-RT-DETRv2-R50 sur-
passes RT-DETRv2 by 1.3 AP on small objects. This im-
provement is even more pronounced with the larger ResNet-
101 backbone, where our DEIM-RT-DETRv2-R101 outper-
forms RT-DETRv2-R101 by 2.1 AP on small objects. Ex-
tending training to 72 epochs further improves overall per-
formance, especially with the ResNet-50 backbone, indicat-
ing that smaller models benefit from additional training.
4.4. Comparisons on CrowdHuman
CrowdHuman [30] is a benchmark dataset designed to eval-
uate object detectors in dense crowd scenarios. We applied
both D-FINE and our proposed method to the CrowdHu-
man dataset, following the configurations provided in the
D-FINE. As shown in Tab. 3, our approach (D-FINE-L en-
hanced with DEIM) achieves a notable improvement of 1.5
AP over D-FINE-L. In particular, our method delivers a sig-
nificant performance boost (greater than 3% improvement)
on small objects (APs) and high-quality detections (AP75),
demonstrating its ability to detect objects more accurately in
Table 4. Comparison of Dense O2O methods with different
combinations of mosaic and mixup augmentation strategies.
The probability values denote the likelihood of applying mosaic
and mixup in each mini-batch during training.
Mosaic Prob.
Mixup Prob.
AP
AP50
AP75
APs
APm
APl
Training 12 Epochs
0.0
0.0
49.6
67.1
53.6
31.3
54.2
67.8
0.5
0.0
50.4
68.4
54.5
32.7
54.6
68.1
0.0
0.5
50.1
67.7
54.0
31.1
54.5
68.7
0.5
0.5
50.4
68.1
54.2
32.7
54.7
68.2
Training 24 Epochs
0.0
0.0
51.7
69.5
55.8
32.8
56.4
69.7
0.5
0.0
51.9
70.1
55.9
34.9
56.1
69.3
0.0
0.5
51.5
69.4
55.5
33.2
56.3
69.3
0.5
0.5
52.5
70.6
56.7
34.9
57.1
70.1
challenging scenarios. Furthermore, this experiment under-
scores the strong generalization capability of DEIM across
diverse datasets, confirming its robustness.
4.5. Analysis
In the following studies, we use RT-DETRv2 [24] paired
with ResNet50 [14] to conduct experiments and report the
performance on MS-COCO val2017 as the default setup un-
less otherwise specified.
Methods for achieving Dense O2O.
We explored two
approaches to implement Dense O2O: mosaic [1] and
mixup [38]. Mosaic is a data augmentation that combines
15168


## Page 8

Table 5. Impact of γ in MAL(Eqn. 4). We report the performance
on COCO [20] val2017 for 24 epochs.
γ
1.3
1.5
1.8
2.0
AP
52.2
52.4
52.1
51.9
Table 6. Impact of Dense O2O and MAL. We conduct experi-
ments with RT-DETRv2-R50 [24] and D-FINE-L [27].
Epochs
Dense O2O
MAL
AP
AP50
AP75
RT-DETRv2-R50 [24]
72
53.4
71.6
57.4
36
✓
53.6
71.9
58.2
✓
✓
53.9
71.7
58.6
D-FINE-L [27]
72
54.0
71.6
58.4
36
✓
54.2
72.1
58.9
✓
✓
54.6
72.2
59.5
four images into one, while mixup overlays two images at a
random ratio. Both methods effectively increase the number
of targets per image, enhancing supervision during training.
As shown in Tab. 4, both mosaic and mixup lead to sig-
nificant improvements after 12 epochs compared to training
without target augmentation, highlighting the effectiveness
of Dense O2O. Moreover, combining mosaic and mixup ac-
celerates model convergence, further emphasizing the bene-
fits of augmented supervision. We further tracked the num-
ber of positive samples per image over one training epoch,
with results shown in Fig. ??. Compared to traditional O2O,
Dense O2O significantly increases positive samples.
Overall, Dense O2O intensifies supervision by increas-
ing target counts per image, leading to faster model conver-
gence. Mosaic and mixup are simple, computationally effi-
cient techniques that achieve this goal, and their effective-
ness suggests further potential for exploring other methods
to augment target counts during training.
Impact of γ in MAL(Eqn. 4).
The results in Table 5
show the effect of different γ values on MAL after 24
epochs. Based on these experiments, we empirically set γ
to 1.5, as it yields the best performance.
Effectiveness of Dense O2O and MAL.
Tab. 6 presents
the effectiveness of the two core components: Dense O2O
and MAL. Dense O2O significantly accelerates model con-
vergence, achieving performance similar to the baseline af-
ter just 36 epochs, as opposed to the 72 epochs required for
the original model. When combined with MAL, our method
further improves performance. This improvement is largely
driven by better box quality, aligning with our goal of op-
timizing low-quality matches to improve high-quality box
predictions. Overall, Dense O2O and MAL consistently
deliver performance gains across both RT-DETRv2 and D-
FINE, demonstrating their robustness and generalizability.
Table 7. Training time in GPU hours.
Method
Epoch
#GPU hr
AP
RT-DETRv2-R50
1
1.181
-
w/ DEIM
1
1.183
-
RT-DETRv2-R50
72
∼85
53.4
w/ DEIM
60
∼71
54.3
Table 8. Fine-tuned results from Object365 pre-training.
Method
Epoch
AP
AP50
AP75
D-FINE-X
32
59.3
76.8
64.6
w/ DEIM
24
59.5
76.4
65.2
Training speed.
We provide an efficient implementation
using Mosaic with caching and Mixup within batches.
Tab. 7 shows the one-epoch training time on a single 4090
GPU, where DEIM is almost as fast as the baseline (1.183
vs. 1.181) and requires less training time to converge (71
vs. 85 hours). This highlights that our approach improves
convergence while maintaining efficiency.
Finetuning from Object365.
We directly employ the
pre-trained Object365 weights from D-FINE and compare
the results of fine-tuning with and without DEIM. As shown
in Tab. 8, DEIM achieves better performance with fewer
fine-tuning epochs. It further validates that DEIM delivers
consistent gains, even when pre-trained on larger datasets.
5. Conclusion
In this paper, we present DEIM, a method designed to accel-
erate convergence in DETR-based real-time object detec-
tors by improving matching. DEIM integrates Dense O2O
matching, which increases the number of positive samples
per image, with MAL, a novel loss designed to optimize
matches across varying quality and specifically enhance
low-quality matches. This combination substantially im-
proves training efficiency, allowing DEIM to achieve supe-
rior performance in fewer epochs compared to models such
as YOLOv11. DEIM demonstrates clear advantages over
SoTA DETR models like RT-DETR and D-FINE, showing
measurable gains in detection accuracy and training speed
without compromising inference latency. These attributes
establish DEIM as a highly effective solution for real-time
applications, with the potential for further refinement and
application across other high-performance detection tasks.
Acknowledgements. We thank Xuanlong Yu, Longfei Liu,
and Haiyang Xie for their valuable discussions. This work
was supported by the Horizontal Project of Hefei Normal
University (No. HXXM2022236) and the Key Projects of
the National Natural Science Foundation of Universities in
Anhui Province (No. 2023AH051302).
15169


## Page 9

References
[1] Alexey
Bochkovskiy,
Chien-Yao
Wang,
and
Hong-
Yuan Mark Liao. Yolov4: Optimal speed and accuracy of
object detection. arXiv, 2020. 1, 2, 5, 7
[2] Zhi Cai, Songtao Liu, Guodong Wang, Zheng Ge, Xiangyu
Zhang, and Di Huang. Align-detr: Improving detr with sim-
ple iou-aware bce loss. In BMVC, 2024. 5
[3] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas
Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-
end object detection with transformers. In ECCV, 2020. 2,
3, 4, 7
[4] Qiang Chen, Xiaokang Chen, Jian Wang, Shan Zhang, Kun
Yao, Haocheng Feng, Junyu Han, Errui Ding, Gang Zeng,
and Jingdong Wang.
Group detr: Fast detr training with
group-wise one-to-many assignment. In ICCV, 2023. 2, 3
[5] Xiaozhi Chen, Kaustav Kundu, Ziyu Zhang, Huimin Ma,
Sanja Fidler, and Raquel Urtasun. Monocular 3d object de-
tection for autonomous driving. In CVPR, 2016. 1
[6] Xiaozhi Chen, Huimin Ma, Ji Wan, Bo Li, and Tian Xia.
Multi-view 3d object detection network for autonomous
driving. In CVPR, 2017. 1
[7] Xiyang Dai, Yinpeng Chen, Jianwei Yang, Pengchuan
Zhang, Lu Yuan, and Lei Zhang. Dynamic detr: End-to-
end object detection with dynamic attention. In ICCV, 2021.
4
[8] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li,
and Li Fei-Fei. Imagenet: A large-scale hierarchical image
database. In CVPR, 2009. 6
[9] Andreas Ess, Konrad Schindler, Bastian Leibe, and Luc
Van Gool.
Object detection and tracking for autonomous
navigation in dynamic environments.
The International
Journal of Robotics Research, 2010. 1
[10] Chengjian Feng, Yujie Zhong, Yu Gao, Matthew R Scott,
and Weilin Huang. Tood: Task-aligned one-stage object de-
tection. In ICCV, 2021. 4
[11] Peng Gao, Minghang Zheng, Xiaogang Wang, Jifeng Dai,
and Hongsheng Li. Fast convergence of detr with spatially
modulated co-attention. In ICCV, 2021. 7
[12] Jocher Glenn. Yolov8. https://docs.ultralytics.
com/models/yolov8/, 2023. 6
[13] Jocher Glenn. Yolo11. https://docs.ultralytics.
com/models/yolo11/, 2024. 2, 6
[14] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
Deep residual learning for image recognition.
In CVPR,
2016. 6, 7
[15] Ding Jia, Yuhui Yuan, Haodi He, Xiaopei Wu, Haojun Yu,
Weihong Lin, Lei Sun, Chao Zhang, and Han Hu. Detrs with
hybrid matching. In CVPR, 2023. 3
[16] Harold W Kuhn. The hungarian method for the assignment
problem. Naval research logistics quarterly, 1955. 2, 3, 4
[17] Feng Li, Ailing Zeng, Shilong Liu, Hao Zhang, Hongyang
Li, Lei Zhang, and Lionel M Ni. Lite detr: An interleaved
multi-scale encoder for efficient detr. In CVPR, 2023. 4
[18] Feng Li, Hao Zhang, Shilong Liu, Jian Guo, Lionel M Ni,
and Lei Zhang. Dn-detr: Accelerate detr training by intro-
ducing query denoising. In CVPR, 2022. 2, 3, 7
[19] Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and
Piotr Doll´ar. Focal loss for dense object detection. In ICCV,
2017. 2, 4, 5
[20] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays,
Pietro Perona, Deva Ramanan, Piotr Doll´ar, and C Lawrence
Zitnick. Microsoft coco: Common objects in context. In
ECCV, 2014. 1, 2, 4, 5, 6, 7, 8
[21] Shilong Liu, Feng Li, Hao Zhang, Xiao Yang, Xianbiao Qi,
Hang Su, Jun Zhu, and Lei Zhang. Dab-detr: Dynamic an-
chor boxes are better queries for detr. In ICLR, 2022. 3,
7
[22] Shilong Liu, Tianhe Ren, Jiayu Chen, Zhaoyang Zeng, Hao
Zhang, Feng Li, Hongyang Li, Jun Huang, Hang Su, Jun
Zhu, et al. Detection transformer with stable matching. In
ICCV, 2023. 4
[23] Ilya Loshchilov and Frank Hutter. Decoupled weight decay
regularization. In ICLR, 2017. 5
[24] Wenyu Lv,
Yian Zhao,
Qinyao Chang,
Kui Huang,
Guanzhong Wang, and Yi Liu. Rt-detrv2: Improved base-
line with bag-of-freebies for real-time detection transformer.
arXiv, 2024. 2, 4, 5, 6, 7, 8
[25] Chengqi Lyu, Wenwei Zhang, Haian Huang, Yue Zhou,
Yudong Wang, Yanyi Liu, Shilong Zhang, and Kai Chen.
Rtmdet: An empirical study of designing real-time object
detectors. arXiv, 2022. 5
[26] Depu Meng, Xiaokang Chen, Zejia Fan, Gang Zeng,
Houqiang Li, Yuhui Yuan, Lei Sun, and Jingdong Wang.
Conditional detr for fast training convergence.
In ICCV,
2021. 7
[27] Yansong Peng, Hebei Li, Peixi Wu, Yueyi Zhang, Xiaoyan
Sun, and Feng Wu. D-fine: Redefine regression task in detrs
as fine-grained distribution refinement. arXiv, 2024. 2, 4, 5,
6, 8
[28] J Redmon. You only look once: Unified, real-time object
detection. In CVPR, 2016. 1
[29] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun.
Faster r-cnn: Towards real-time object detection with region
proposal networks. TPAMI, 2016. 2, 3
[30] Shuai Shao, Zijian Zhao, Boxun Li, Tete Xiao, Gang Yu,
Xiangyu Zhang, and Jian Sun. Crowdhuman: A benchmark
for detecting human in a crowd. arXiv, 2018. 7
[31] Zhi Tian, Xiangxiang Chu, Xiaoming Wang, Xiaolin Wei,
and Chunhua Shen. Fully convolutional one-stage 3d object
detection on lidar range images. In NIPS, 2022. 2, 3
[32] Ao Wang, Hui Chen, Lihao Liu, Kai Chen, Zijia Lin, Jun-
gong Han, and Guiguang Ding. Yolov10: Real-time end-to-
end object detection. 2024. 1, 2, 6
[33] Chengcheng Wang, Wei He, Ying Nie, Jianyuan Guo,
Chuanjian Liu, Yunhe Wang, and Kai Han. Gold-yolo: Ef-
ficient object detector via gather-and-distribute mechanism.
NeurIPS, 2023. 6
[34] Chien-Yao Wang, I-Hau Yeh, and Hong-Yuan Mark Liao.
Yolov9:
Learning what you want to learn using pro-
grammable gradient information. arXiv, 2024. 1, 6
[35] Yingming Wang, Xiangyu Zhang, Tong Yang, and Jian Sun.
Anchor detr: Query design for transformer-based detector.
In AAAI, 2022. 3, 7
[36] Zhuyu Yao, Jiangbo Ai, Boxun Li, and Chi Zhang. Efficient
detr: improving end-to-end object detector with dense prior.
arXiv, 2021. 3, 7
[37] Mingqiao Ye, Lei Ke, Siyuan Li, Yu-Wing Tai, Chi-Keung
Tang, Martin Danelljan, and Fisher Yu. Cascade-detr: delv-
15170


## Page 10

ing into high-quality universal object detection. In ICCV,
2023. 4
[38] Hongyi Zhang. mixup: Beyond empirical risk minimization.
In ICLR, 2017. 2, 5, 7
[39] Hao Zhang, Feng Li, Shilong Liu, Lei Zhang, Hang Su, Jun
Zhu, Lionel M Ni, and Heung-Yeung Shum.
Dino: Detr
with improved denoising anchor boxes for end-to-end object
detection. In ICLR, 2023. 2, 3, 4, 6, 7
[40] Haoyang Zhang, Ying Wang, Feras Dayoub, and Niko Sun-
derhauf. Varifocalnet: An iou-aware dense object detector.
In CVPR, 2021. 2, 3, 5
[41] Shilong Zhang, Xinjiang Wang, Jiaqi Wang, Jiangmiao
Pang, Chengqi Lyu, Wenwei Zhang, Ping Luo, and Kai
Chen. Dense distinct query for end-to-end object detection.
In CVPR, 2023. 3
[42] Chuyang Zhao, Yifan Sun, Wenhao Wang, Qiang Chen, Er-
rui Ding, Yi Yang, and Jingdong Wang. Ms-detr: Efficient
detr training with mixed supervision. In CVPR, 2024. 4
[43] Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei,
Guanzhong Wang, Qingqing Dang, Yi Liu, and Jie Chen.
Detrs beat yolos on real-time object detection.
In CVPR,
2024. 2, 3, 4, 5, 6, 7
[44] Ge Zheng, Liu Songtao, Wang Feng, Li Zeming, and Sun
Jian. Yolox: Exceeding yolo series in 2021. arXiv, 2021. 1,
2, 4
[45] Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang,
and Jifeng Dai. Deformable detr: Deformable transformers
for end-to-end object detection. In ICLR, 2021. 2, 3, 4, 7
[46] Zhuofan Zong, Guanglu Song, and Yu Liu. Detrs with col-
laborative hybrid assignments training. In ICCV, 2023. 2,
3
15171
