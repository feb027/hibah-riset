---
source_id: S037
title: DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion
source_url: https://arxiv.org/pdf/2111.14690
source_file: docs/research/papers/S037-dancetrack-multi-object-tracking-in-uniform-appearance-and-diverse-mot.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S037-dancetrack-multi-object-tracking-in-uniform-appearance-and-diverse-mot.pdf
## PDF metadata
- format: PDF 1.5
- creator: LaTeX with hyperref
- producer: pdfTeX-1.40.21
- creationDate: D:20220525003355Z
- modDate: D:20220525003355Z


## Page 1

DanceTrack: Multi-Object Tracking in Uniform Appearance and Diverse Motion
Peize Sun1∗, Jinkun Cao2∗, Yi Jiang3, Zehuan Yuan3, Song Bai3, Kris Kitani2, Ping Luo1
1The University of Hong Kong
2Carnegie Mellon University
3ByteDance Inc.
1
3 4
5
6
3
4
2
5
9
1
2
8
7
2
9
4
8
7 5
1
3
9
4
8
7
5
3
1
2
Figure 1 – Sample images from a video in DanceTrack: 1st, 66th, 307th and 327th frame in DanceTrack0027 video. The emphasized
properties of this dataset are (1) uniform appearance: humans are in highly similar and almost undistinguished appearance. (2) diverse
motion: they are in complicated motion and interaction pattern. The numbers below show their identiﬁcations which experience frequent
relative position switches and occlusions. We expect the combination of uniform appearance and complicated motion pattern makes
DanceTrack a platform to encourage more comprehensive and intelligent multi-object tracking algorithms.
Abstract
A typical pipeline for multi-object tracking (MOT) is to
use a detector for object localization, and following re-
identiﬁcation (re-ID) for object association. This pipeline is
partially motivated by recent progress in both object detec-
tion and re-ID, and partially motivated by biases in existing
tracking datasets, where most objects tend to have distin-
guishing appearance and re-ID models are sufﬁcient for es-
tablishing associations. In response to such bias, we would
like to re-emphasize that methods for multi-object track-
ing should also work when object appearance is not sufﬁ-
ciently discriminative. To this end, we propose a large-scale
dataset for multi-human tracking, where humans have sim-
ilar appearance, diverse motion and extreme articulation.
As the dataset contains mostly group dancing videos, we
name it “DanceTrack”. We expect DanceTrack to provide
a better platform to develop more MOT algorithms that rely
less on visual discrimination and depend more on motion
analysis. We benchmark several state-of-the-art trackers on
our dataset and observe a signiﬁcant performance drop on
DanceTrack when compared against existing benchmarks.
The dataset, project code and competition is released at:
https://github.com/DanceTrack.
* indicates equal contribution.
1. Introduction
Object tracking has been long studied and can be ben-
eﬁcial to applications such as autonomous driving, video
analysis and robot planning [1,4,27,37]. Multi-object track-
ing aims to localize and associate objects of interest along
time. Interestingly, we observe that recent developments in
multi-object tracking rely heavily on a paradigm of detec-
tion followed by re-ID, where mostly appearance cues are
used to associate objects. This trend in algorithmic devel-
opment makes existing solutions fail catastrophically in sit-
uations where objects share very similar appearance, e.g.,
group dancing where performers wear uniform clothes. It
inspires us to propose more comprehensive solutions by tak-
ing other cues into modeling, such as object motion patterns
and temporal dynamics.
As with many other areas of computer vision, the de-
velopment of multi-object tracking is inﬂuenced by bench-
mark datasets. Based on speciﬁed datasets [11, 15, 24, 38],
data-driven methods are sometimes argued to be biased to
certain data distributions. In this work, we recognize the
limitations of existing multi-object tracking datasets lie on
that many objects have distinct appearance and the motion
pattern of objects are very regular or even linear. Moti-
vated by these dataset properties, most recently developed
multi-object tracking methods [25, 34, 35, 41] highly rely
on appearance matching to associate detected objects while
arXiv:2111.14690v3  [cs.CV]  24 May 2022


## Page 2

taking little other cues into consideration. The dominant
paradigm will fail in situations out of the biased distribu-
tion. This phenomenon is not what we expect if we aim to
build more general and intelligent tracking algorithms.
To provide a new platform for more comprehensive
multi-object tracking studies, we propose a new dataset
in this paper. Because it mostly contains group dancing
videos, we name it “DanceTrack”. The dataset contains
over 100K image frames (almost 10× more than MOT17
datatset [24]). As shown in Figure 1, the emphasized prop-
erties of this dataset are (1) uniform appearance: people in
videos wear very similar or even the same clothes, making
their visual features hard to be distinguished by re-ID model
and (2) diverse motion: people usually have very large-
range motion and complex body gesture variation, propos-
ing higher requirements for motion modeling. The second
property also brings occlusion and crossover as a side-effect
that human body has a large ratio of overlap with each other
and their relative position exchanges frequently.
With the proposed dataset, we build a new bench-
mark including existing popular multi-object tracking meth-
ods.
The results prove that current state-of-the-art algo-
rithms [25, 29, 35, 39–42] fail to make satisfactory perfor-
mance when they simply use appearance matching or linear
motion models to associate objects across frames. Consid-
ering the cases focused on in this dataset happen frequently
in our real life, we believe it shows the limitations of ex-
isting multi-object tracking algorithms on practical applica-
tions. To provide potential guidelines for further research,
we analyze a range of choices in associating objects and
achieve some beneﬁcial conclusions: (1) ﬁne-grained rep-
resentations of objects, e.g., segmentation and pose, exhibit
better ability than coarse bounding box; (2) depth informa-
tion shows positive inﬂuence on associating objects, though
we are solving a 2D tracking task; (3) motion modeling of
temporal dynamics is important.
To conclude, the key contributions of our work to the
object tracking community are as follows:
1. We build a new large-scale multi-object tracking dataset,
DanceTrack, covering the scenarios where tracking suf-
fers from low distinguishability of object appearance and
diverse non-linear motion patterns.
2. We benchmark baseline methods on this newly built
dataset with various evaluation metrics, showing the lim-
itation of existing multi-object tracking algorithms.
3. We provide comprehensive analysis to discover more
cues for developing multi-object trackers that are more
robust in complicated real-life situations.
2. Related Works
Multi-object tracking datasets. Many multi-object track-
ing datasets have been proposed for different scenarios.
Similar to our proposed dataset, many existing datasets fo-
cus on human tracking. PETS2009 [13] dataset is one of
the earliest in this area.
The more recent MOT15 [19],
MOT17 [24] and MOT20 [11] datasets are all popular in
this community. These datasets are limited in the aspects of
undistinguished appearance and diverse motion. For exam-
ple, MOT17 contains only a handful of videos and scenar-
ios. Even MOT20 increases the density of objects and em-
phasizes the occlusion among them, the movements of ob-
jects are very regular and they still have distinguishable ap-
pearances. Association by pure appearance matching [25]
could easily make success on these datasets and we will
show that given the perfect detector, the tracking problem
on these datasets can be solved by a very naive association
strategy, in Section 4.2.
Besides, many other datasets are proposed for diverse
objectives, e.g., WILDTRACK [7] for multi-camera track-
ing, Youtube-VIS [36] for video instance segmentation and
tracking.
With the increasing attraction of autonomous
driving, some datasets are speciﬁcally built where the ob-
jects of interest are vehicles and pedestrians. KITTI [15] is
one of the earliest large-scale multi-object tracking datasets
for driving scenarios.
More recently, BDD100K [38],
Waymo [30] and KITTI360 [20] are made available to the
public, still focusing on autonomous driving scenarios but
providing much larger scale data than KITTI. With the lim-
itation of lanes and trafﬁc rules, the motion patterns of ob-
jects in these datasets are even more regular than those fo-
cusing on only moving people. There are many datasets fo-
cusing on more diverse object categories than persons and
vehicles. The ImageNet-Vid [12] provides trajectory an-
notations for 30 object categories in over 1000 videos and
TAO [10] annotates even 833 object categories to study ob-
ject tracking on long-tailed distribution.
Tracking by matching appearance. In the recent develop-
ment of multi-object tracking, appearance similarity serves
as the dominant cue in many popular methods.
For ex-
ample, JDE [33] and FairMOT [41] learn object localiza-
tion and appearance embedding using a shared backbone
for better appearance representation. QDTrack [25] designs
a contrastive training paradigm and dense localization for
object detection and uses highly sensitive appearance com-
parison to match objects across frames. More recently, with
the new focus of applying transformers [32] in vision tasks,
TransTrack [29], TrackFormer [23] and MOTR [39] make
attempts to leverage the attention mechanism in tracking
objects in videos. In these works, the features of previous
tracklets are passed to the following frames as the query to
associate the same objects across frames. The appearance
information contained in the query is critical to keep track-
let consistency.
Although the rise of deep-learning model brings much
more powerful visual representations than ever before, we
2


## Page 3

still witness the failure of appearance matching in many
real-world situations and expect to improve the tracking
performance by taking other cues into account.
Motion analysis in object tracking.
The displacement
of objects-of-interest provides important cues for object
tracking. Tracking objects by estimating their motions has
inspired a line of researches.
These tracking algorithms
mainly follow the tracking-by-detection paradigm. Sequen-
tial analysis tools such as Particle ﬁlter [16,17] and Kalman
ﬁlter [18] are found efﬁcient in such applications, for ex-
ample, SORT [3] is developed on the Kalman ﬁlter mo-
tion model. Even though motion analysis has been used in
many object tracking methods [33,40,41], all these methods
can only handle simple linear motion pattern and provide
limited help in more complicated situations. Furthermore,
as deep networks bring the revolutionary ability to extract
high-quality visual features, DeepSORT [34] tries to com-
bine deep visual features and motion models to gain per-
formance gain. Since then, motion-based object tracker has
shown weak competitiveness and many focuses are towards
appearance cues.
However, we argue that a more comprehensive and intel-
ligent tracking algorithm should pay more attention to mo-
tion analysis since appearance is not always reliable.
3. DanceTrack
3.1. Dataset Construction
Dataset design. We focus on the scenarios where objects
have similar or even the same appearance and diverse mo-
tion patterns, including frequent crossover, occlusion and
body deformation. The ﬁrst property makes tracking by
purely comparing object appearance invalid because the ex-
tracted visual features are no longer distinguishable for dif-
ferent objects. The second property further requires more
informative clues rather than appearance in tracking, such
as motion analysis and temporal dynamics.
We argue that “crowd” by simply increasing the den-
sity of objects is not what we expect.
For example,
MOT20 [11] contains videos where groups of pedestrians
are very crowded. But as the pedestrian movement is very
regular, the relative position and occlusion area keep almost
consistent, such “crowd” is not an obstacle for appearance
matching. Therefore, we focus on situations where multi-
ple objects are moving in a “relatively” large range, where
the occluded areas are dynamically changing, and they are
even in crossover. Such cases are common in real world but
naive linear motion models can not handle them anymore.
Video collection. To achieve the design goals described
above, we collected videos including mostly group danc-
ing from the Internet. As shown in Figure 2, the dancers
usually wear very similar or even the same clothes. They
Dataset
MOT17 [24]
MOT20 [11]
DanceTrack
Videos
14
8
100
Avg. tracks
96
432
9
Total tracks
1342
3456
990
Avg. len. (s)
35.4
66.8
52.9
Total len. (s)
463
535
5292
FPS
30
25
20
Total images
11,235
13,410
105,855
Table 1 – The comparison of dataset meta-information between
DanceTrack and its closest benchmark for multi-human track-
ing, MOT17 and MOT20.
DanceTrack contains much more
videos and images than MOT datasets.
make a large-range motion, diverse gestures and frequent
crossover. These properties greatly satisfy our motivation.
We collect the videos from different search engines with
keywords like “street dance”, “hip-pop dance”, “cheerlead-
ing dance”, “rhythmic gymnastics” and so on. The collec-
tion is only for publicly available videos and under the per-
mit of fair use of video resources.
Annotation. We use a commercial tool to annotate the col-
lected videos. The annotated labels include bounding boxes
and identiﬁcations.
For a partly-occluded object, a full-
body box is annotated. For a fully-occluded object, we do
not annotate it; when it re-appears in the future frame, its
identiﬁcation is kept as the same as in the previous frame
when it is visible. To facilitate the annotation process, our
tool can automatically propagate the annotated boxes from
the previous frame to the current frame, and the annotator
only needs to reﬁne the boxes in the current frame. To build
a high-quality dataset, the annotations have been checked
by another group of people and errors are reported back to
the annotators for re-annotation.
3.2. Dataset Statistic
We provide some analytical information of DanceTrack
dataset and compare it with existing multi-object tracking
datasets. The statistical information helps to understand the
uniqueness of the proposed dataset.
Dataset split. We collect 100 videos in DanceTrack dataset,
by default using 40 videos as training set, 25 as valida-
tion set and 35 as test set. For splitting, we keep the dis-
tribution of subsets close in terms of average length, aver-
age bounding box number, scenes and the motion diversity.
We make the annotation of training set and validation set
public while keeping the testing set annotation private for
competition use. Some basic information of DanceTrack is
shown in Table 1. Compared with MOT datasets, Dance-
Track has much larger volume (10x more images and 10x
more videos). MOT20 focuses on crowded scenes, so it
has more tracks but the appearance of objects is very distin-
3


## Page 4

classical
large
group
pop
street dance
sports
(a)
(b)
(c)
(d)
Figure 2 – Sampled scenes from DanceTrack dataset. DanceTrack contains multiple genres of dance, including classical dance, street
dance, pop dance, large group dance and sports. The scenes in DanceTrack are diverse: (a) outdoor scenes; (b) low-lighting and distant
camera scenes; (c) large group of dancing people; (d) gymnastics scene where the motion is usually even more diverse and people have
more aggressive deformation.
guishable and their motion is regular. As a consequence, the
association on MOT20 still requires little motion estimation
when good detection results are provided.
Scene diversity. DanceTrack contains diverse scenes. Sam-
ples from all 100 videos are provided in Figure 2. One
shared property for all videos is that the instances of people
in a video usually have very similar appearance. This is de-
signed on purpose to avoid the shortcut of tracking by pure
appearance matching. DanceTrack contains multiple genres
of dance, such as street dance, pop dance, classical dance
(ballet, tango, etc.) and large group dancing. It also contains
some sports scenarios such as gymnastics, Chinese Kung Fu
and cheerleader dancing. Figure 2(a) shows outdoor scenes
though most included videos are indoor. Figure 2(b) shows
some especially hard cases, such as low lighting and distant
camera. Figure 2(c) shows a large group of people dancing,
including at most 40 people. Figure 2(d) shows gymnastics
where people show extremely diverse body gestures, fre-
quent pose variation and complicated motion pattern.
Appearance similarity.
We make quantitative analysis
about how appearance-only matching is not reliable on
DanceTrack by measuring the appearance similarity among
objects. We use a pre-trained re-ID model [26] to extract
the appearance features F(Bt
i) of object Bi on a frame t,
and then compute the sum of cosine distance of the re-ID
features among objects in the video as
V = 1
T
T
X
t=1
1
N 2
t
Nt
X
i
Nt
X
j̸=i
(1 −cos < F(Bt
i), F(Bt
j) >),
(1)
where T is the number of frames in the video sequence, Nt
is the number of objects on the frame t and <·> is the angle
between two vectors.
We compare the object appearance similarity in Dance-
Track to that in MOT17 dataset, as shown in Figure 3(a),
each bin represents one video sequence. It is obvious that
the cosine distance of re-ID features of DanceTrack is lower
than that of MOT17, in other words, the appearance simi-
larity among co-existing objects is higher. This quantitative
analysis shows the challenge of DanceTrack to current pop-
ular appearance matching for association.
Motion pattern. We introduce two metrics to analyze the
motion pattern in DanceTrack dataset and compare that to
other multi-object tracking datasets.
IoU on adjacent frames: a natural measurement of ob-
ject movement range is its bounding-box IoU (Intersection-
over-Union) on two adjacent frames. A low IoU indicates
fast-moving objects or the low frame rate of videos. Given
a video with N objects and T frames, the averaged IoU on
adjacent frames for this video is
U =
1
N(T −1)
N
X
i
T −1
X
t=1
IoU(Bt
i, Bt+1
i
).
(2)
Frequency of Relative Position Switch: a metric to measure
the diversity of objects’ motion in a global view is the fre-
quency for two objects to switch their relative position. This
could happen between leftward and rightward or between
upward and downward. On the contrary, movement with
consistent velocity tends to cause a lower chance of relative
position switch. Given a video, the average frequency of
relative position switch is deﬁned as
S =
PN
i
PN
j̸=i
PT −1
t=1 sw(Bt
i, Bt
j, Bt+1
i
, Bt+1
j
)
2N(T −1)(N −1)
,
(3)
where sw is an indicator function, where sw(·)=1 if the two
objects swap their left-right relative position or top-down
relative position on the adjacent frames, sw(·)=0 if there is
no swap. We measure their relative position by comparing
4


## Page 5

video sequences
0.0
0.1
0.2
0.3
appearance similarity
MOT17
DanceTrack
(a) Cosine distance of re-ID feature
MOT17
MOT20
KITTI
DanceTrack
0.00
0.25
0.50
0.75
1.00
adjacent_IoU
(b) IoU on adjacent frames
MOT17
MOT20
KITTI
DanceTrack
0.000
0.005
0.010
0.015
0.020
switch
(c) Frequency of relative position switch
Figure 3 – (a) Cosine distance of re-ID features. The dashed lines are for the average cosine distance similarity for the two datasets. The
cosine distance of re-ID features of DanceTrack is lower than that of MOT17, in other words, the appearance similarity between different
objects is higher. (b) IoU on adjacent frames. Compared to MOT17 and MOT20, DanceTrack has a similar score. It means that the
frame rate and object motion speed are still reasonable in DanceTrack. (c) Frequency of relative position switch. This metric measures
the frequency of crossover and is highly related to the occlusion between objects. DanceTrack has much more frequent relative position
switches than other pedestrian tracking datasets, such as MOT17 and MOT20. Even compared to the driving dataset KITTI, where the
moving camera naturally causes many relative position switches, DanceTrack still has a higher frequency.
their bounding box center locations. And considering that
such crossover causes potential difﬁculty only when the ob-
jects have overlap, we only take the objects with overlap
into the calculation.
From the results shown in Figure 3(b), we could ﬁnd that
DanceTrack and MOT datasets have close average IoU on
adjacent frames. This indicates that DanceTrack does not
have unreasonably fast object movement.
On the other hand, from Figure 3(c) we could ﬁnd
that DanceTrack has much more frequent relative position
switches than other datasets such as KITTI, MOT17 and
MOT20. The frequent relative position switches are caused
by highly non-linear motion pattern and result in frequent
crossover and inter-object occlusion. This result shows that
the challenge of motion diversity in DanceTrack.
3.3. Evaluation Metrics
For a long time, multi-object tracking community used
Multi-Object Tracking Accuracy (MOTA) as the main met-
ric for evaluation. However, recently, the community real-
izes that MOTA focuses too much on detection quality in-
stead of association quality. Thus, Higher Order Tracking
Accuracy (HOTA) [22] is proposed to correct this historical
bias. Up to now, HOTA has been used for the main metrics
to evaluate tracking quality on multiple popular benchmarks
such as BDD100K [38] and KITTI [15]. We follow this set-
ting for evaluation metrics of DanceTrack. In our protocol,
the main metric is HOTA. We also use AssA and IDF1 score
to measure association performance and DetA and MOTA
for detection quality. For the detailed deﬁnitions of these
metrics, we refer to [2, 22, 28]. To make it convenient to
run for ﬁne-grained analysis, the evaluation tools also pro-
vide previously widely-used statistics, such as False Posi-
tive (FP), False Negative (FN) and ID switch (IDs).
3.4. Limitation
We discuss some limitations of the proposed dataset.
First, given the mentioned motivation and the proposed
dataset, we do not provide an algorithm that highly outper-
forms previous multi-object tracking algorithms but keep
this as an open question for future study. Second, for the
cases we emphasize in this work, the annotation of human
pose or segmentation mask should be important for more
ﬁne-grained study. But limited by time and resources, we
only provide the annotation of bounding boxes in this ver-
sion.
4. Experiments
4.1. Experiment Setup
Dataset conﬁgurations We compare DanceTrack with its
closest dataset, MOT17.
For MOT17, because the test
server is not available easily, we follow the train-val split-
ting provided in CenterTrack [43] to evaluate on the vali-
dation subset, unless in Section 4.3. For DanceTrack, we
follow the default splitting described in the previous sec-
tion.
Model conﬁguration Unless speciﬁed otherwise, we in-
herit the default training settings of the investigated algo-
rithms provided in the original papers or the ofﬁcially re-
leased codebases.
4.2. Oracle Analysis
To decompose the analysis over object localization and
association, we perform oracle analysis here. We use the
ground truth bounding boxes with different association al-
gorithms to achieve the upper-bound performance.
This
analysis can help us to understand what is the true bottle-
neck of tracking on different datasets.
We compare IoU matching, motion modeling and ap-
pearance matching for the association.
IoU matching is
simply performed by calculating the IoU of objects’ bound-
ing boxes in adjacent frames.
We use a pre-trained Re-
ID model [26] for appearance matching and a Kalman Fil-
ter [18] for motion modeling under linear motion assump-
tion. We have experiments on MOT17 and DanceTrack re-
5


## Page 6

Appearance
IoU
Motion
MOT17
DanceTrack (Proposed Dataset)
HOTA
DetA
AssA
MOTA
IDF1
HOTA
DetA
AssA
MOTA
IDF1
✓
98.1
98.9
97.3
98.0
97.8
72.8
98.9
53.6
98.7
63.5
✓
✓
96.4
97.1
95.8
99.7
98.1
69.4
87.9
54.8
99.4
71.3
✓
✓
✓
95.0
94.7
95.4
99.3
98.8
59.7
82.5
43.2
97.2
60.5
✓
93.3
99.0
87.9
98.9
90.9
68.0
97.7
47.4
97.9
58.7
Table 2 – Oracle analysis of different association models on MOT17 and DanceTrack validation set, respectively. The detection boxes
are ground-truth boxes. The result comparison shows the evident increased difﬁculty of performing multi-object tracking on DanceTrack
than MOT17 dataset.
…
MOT17-05
DanceTrack0019
Figure 4 – Visualization of re-ID feature from sampled video
in MOT17 and DanceTrack dataset using t-SNE [31]. The same
object is coded by the same color. For better visualization, we
only select ﬁrst 200 frames in each video sequence.
spectively. The results are shown in Table 2.
From the results, the performance is almost perfect in
terms of all metrics on MOT17. And it is interesting that
using only IoU matching achieves the best performance,
which proves that MOT17 contains objects with simple and
regular motion patterns and the bottleneck does not lie in
association in most cases.
On the other hand, using only IoU matching on Dance-
Track gives a much lower performance than on MOT17.
Given DetA and MOTA scores are already close to 100, the
bottleneck is obviously in the association part. All associ-
ation metric scores in all cases experience a dramatic drop
compared with that on MOT17. Besides, the best perfor-
mance lies in only IoU matching, even combining a linear
motion model or additional appearance information does
not help.
When using appearance similarity, all metrics
are worse than not using any appearance cue. This is be-
cause the objects in DanceTrack videos usually have indis-
tinguishable appearance so simply using appearance match-
ing makes negative effects in some cases. In Figure 4, we
visualize the appearance feature of objects extracted from
DanceTrack and MOT17 videos respectively. We can ob-
serve that the appearance features of different objects are
very distinguishable in the feature space on MOT17 while
highly entangled on DanceTrack. This qualitatively pro-
vides evidence for the high similar appearance of objects
in the proposed DanceTrack dataset.
Given the results shown in the analysis with oracle object
localization, we can reach a clear conclusion that existing
datasets have a heavy bias that it focuses more on the de-
tection quality only and the involved simple trajectory pat-
terns limit the study in this area. On the contrary, Dance-
Track is proposing a much higher requirement to develop
multi-object trackers with improvement in association abil-
ity. Considering the scenarios included in DanceTrack are
what we experience in real life, we believe it is meaningful
to provide such a platform.
4.3. Benchmark Results
We benchmark the current state-of-the-art multi-object
tracking algorithms on MOT17 and DanceTrack. The eval-
uation is in the “private” setting that the algorithm performs
both detection and association. The methods basically in-
herit the settings on MOT17 for training on DanceTrack
training set. The benchmark results are reported in Table 3.
For tracking quality measured by HOTA, IDF1 and
AssA, all algorithms show a signiﬁcant performance gap
from MOT17 to DanceTrack. For all investigated methods,
their performance on DanceTrack is far from satisfactory.
Notably, the detection quality metrics, MOTA and DetA,
of all algorithms are in fact higher on DanceTrack than on
MOT17. This suggests that detection is not the bottleneck
to have good tracking performance on DanceTrack and fur-
ther highlights the drop of association performance. The
benchmark results prove that DanceTrack raises the chal-
lenge to make robust association in the cases of the uniform
appearance and the diverse motion of objects.
4.4. Association Strategy
The methods in the previous section entangle the detec-
tion and tracking modules. To have an independent study on
association algorithms, we use the most recently developed
YOLOX [14] detector for object detection on DanceTrack
and conduct different association algorithms following that.
6


## Page 7

Methods
MOT17
DanceTrack (Proposed Dataset)
HOTA
DetA
AssA
MOTA
IDF1
HOTA
DetA
AssA
MOTA
IDF1
CenterTrack1 [42]
52.2
53.8
51.0
67.8
64.7
41.8
78.1
22.6
86.8
35.7
FairMOT1 [41]
59.3
60.9
58.0
73.7
72.3
39.7
66.7
23.8
82.2
40.8
QDTrack3 [25]
53.9
55.6
52.7
68.7
66.3
54.2
80.1
36.8
87.7
50.4
TransTrack1 [29]
54.1
61.6
47.9
75.2
63.5
45.5
75.9
27.5
88.4
45.2
TraDes1 [35]
52.7
55.2
50.8
69.1
63.9
43.3
74.5
25.4
86.2
41.2
MOTR2 [39]
57.2
58.9
55.8
71.9
68.4
54.2
73.5
40.2
79.7
51.5
GTR2 [44]
59.1
61.6
57.0
75.3
71.5
48.0
72.5
31.9
84.7
50.3
ByteTrack1 [40]
63.1
64.5
62.0
80.3
77.3
47.7
71.0
32.1
89.6
53.9
OC-SORT2 [5]
63.2
63.2
63.2
78.0
77.5
55.1
80.3
38.3
92.0
54.6
Table 3 – Tracking performance of investigated algorithms on MOT17 and DanceTrack test set. The result comparison shows the evident
increased difﬁculty of performing multi-object tracking on DanceTrack than MOT17 dataset.
Association
HOTA DetA AssA MOTA IDF1
IoU
44.7
79.6
25.3
87.3
36.8
SORT [3]
47.8
74.0
31.0
88.2
48.3
DeepSORT [34]
45.8
70.9
29.7
87.1
46.8
MOTDT [8]
39.2
68.8
22.5
84.3
39.6
BYTE [40]
47.1
70.5
31.5
88.2
51.9
OC-SORT [5]
52.1
79.8
35.3
87.3
51.6
Table 4 – Comparison of different association algorithms on
DanceTrack validation set. The detection results are output by
YOLOX [14] detector, trained on DanceTrack training set.
Motion
HOTA DetA AssA MOTA IDF1
None(IoU)
44.7
79.6
25.3
87.3
36.8
Kalman ﬁlter [3]
47.8
74.0
31.0
88.2
48.3
LSTM [6]
51.6
78.2
34.2
89.2
50.8
Table 5 – Comparison of different motion models on Dance-
Track validation set.
The detection results are output by
YOLOX [14] detector, trained on DanceTrack training set.
The results are shown in Table 4.
SORT [3] uses Kalman Filter to model the object mo-
tion and DeepSORT [34] adds appearance matching. Com-
pared to SORT, DeepSORT shows no performance boost
but worse performance instead, suggesting the negative
gain due to appearance matching.
On the other hand,
MOTDT [8] uses the tracking result to help detect bound-
ing boxes. But in fact, detection performance can be re-
ally good on DanceTrack dataset and the exact bottleneck
is the association part, so MOTDT shows even worse per-
formance on both detection quality and association quality
with its design. Lastly, BYTE [40] uses a high-tolerance
strategy to select detection results into the association stage.
The design aims to decrease tracklet fragmentation in track-
ing. OC-SORT [5, 9] improves the association robustness
for non-linear object motion in pure motion-based manner
and it shows the best association performance on Dance-
The number is arXiv version. For details, refer to change log in ap-
pendix. We thank the authors for reporting their updated results.
Track where object motion is highly non-linear. The results
reveal that DanceTrack is not a strict challenge for object
detectors, the true challenge is in the object association part.
We further use different motion models to introduce tem-
poral dynamics in the tracking process to facilitate better
association, as shown in Table 5. Obviously, both Kalman
ﬁlter [3] and LSTM [6] outperform naive IoU association
(without temporal dynamics) by a large margin, indicating
the great potential of motion models in tracking objects, es-
pecially when appearance cues are not reliable. With the
relatively slow progress of object model motion in the ﬁeld
of multi-object tracking, we expect to see more researches.
4.5. Analysis of More Modalities
Considering high scores of MOTA and DetA on Dance-
Track, the limited performance on DanceTrack is an exact
failure of trackers instead of detectors. To boost perfor-
mance, a straightforward strategy is to add more cues other
than frame-wise bounding box. Since DanceTrack contains
bounding boxes and identities annotations only, we propose
to use joint-training technology with other datasets to en-
able the model output more modalities.
Does ﬁne-grained representation help ? We investigate
the inﬂuence of adding segmentation mask into the model.
From Table 6, we observe a performance boost by using
the segmentation mask. First, the introduction of more ﬁne-
grained annotation beneﬁts the model by multi-task learn-
ing. Second, for crowded and occluded situations, mask is
a more reliable information than bounding box to associate
objects. Besides mask, adding pose information in training
better boosts the model performance on DanceTrack, and
using the output pose in association further helps to achieve
better tracking results. When most areas of a human body
are occluded, bounding box usually can not provide reliable
output while the pose estimation model focusing on certain
human body key-points usually shows higher robustness.
Does depth information help ? We use additional depth
information to help tracking on DanceTrack. The results
are shown in Table 6. In contrast to the COCO segmenta-
7


## Page 8

mask
pose
depth
Figure 5 – Visualization of adding more information beyond bounding box on DanceTrack. Tracks are coded by color. The 1st, 2nd and
3rd column are frame20, 120 and 200 of DanceTrack0007 video.
Data
Ass.
HOTA
DetA
AssA
MOTA
IDF1
DanceTrack
box
36.9
63.6
21.6
78.8
39.2
+ COCOmask [21]
box
38.1 (+1.2)
64.5 (+0.9)
22.6 (+1.0)
80.6 (+1.8)
40.3 (+1.1)
+ COCOmask
+ mask
39.2 (+1.1)
64.9 (+0.4)
23.9 (+1.3)
80.7 (+0.1)
41.6 (+0.3)
DanceTrack
box
36.9
63.6
21.6
78.8
39.2
+ COCOpose [21]
box
40.6 (+3.7)
65.5 (+1.9)
25.3 (+3.7)
82.9 (+4.1)
42.9 (+3.7)
+ COCOpose
+ pose
41.0 (+0.4)
65.9 (+0.4)
25.6 (+0.3)
83.1 (+0.3)
43.9 (+1.0)
DanceTrack
box
36.9
63.6
21.6
78.8
39.2
+ KITTI [15]
box
34.4 (- 2.5)
57.8 (- 5.8)
20.7 (- 0.9)
72.9 (- 5.9)
38.5 (- 0.7)
+ KITTI
+ depth
35.1 (+0.7)
57.3 (- 0.5)
21.6 (+0.9)
72.8 (- 0.1)
40.2 (+1.7)
Table 6 – Ablation study on adding more information beyond bounding box on DanceTrack validation set. All experiments are based on
CenterNet [43] model and BYTE [40] association. (a) Segmentation mask improves the tracking performance on DanceTrack. (b) Pose
information boosts the tracking performance with an even larger gap than segmentation mask. (c) Though adding depth information into
association shows a slightly positive inﬂuence, the results still blame the domain shift between KITTI and DanceTrack.
tion mask and human pose, depth information learned from
KITTI dataset does not increase the performance on Dance-
Track. We explain that COCO segmentation and pose esti-
mation datasets contain human as the main category, while
KITTI mainly contains vehicle instances. Thus, the object
and scene prior in DanceTrack and KITTI change and this
domain shift degenerates the model. Nevertheless, depth
information indeed helps association performance if we re-
gard the baseline as the model trained on joint-dataset of
DanceTrack and KITTI. However, limited by the available
resources of depth-annotated data, this is the best we could
try for now. We expect more study on the inﬂuence of depth
information to associate objects with uniform appearance
and diverse motion.
5. Conclusion
In this paper, we propose a new multi-object tracking
dataset called DanceTrack. The objects have uniform ap-
pearance and diverse motion pattern in DanceTrack, pre-
venting being taken short-cuts by Re-ID algorithms. The
motivation behind it is to reveal the bias in existing datasets
that tend to emphasize detection quality and matching ap-
pearance only. This makes other cues to associate objects
underrepresented. We believe that the ability to analyze the
complex motion pattern is necessary for building a more
comprehensive and intelligent tracker.
DanceTrack pro-
vides such a platform to encourage future works.
Acknowledgement We would like to thank the annotator
teams and coordinators to build DanceTrack dataset. We
appreciate Xinshuo Weng, Yifu Zhang for valuable discus-
sion and suggestions. We would also like to thank Vivek
Roy, Pedro Morgado, Shuyang Sun for their proof reading
and suggestions on paper writing. This work was sponsored
in part by NSF NRI Award IIS2024173. Ping Luo is sup-
ported by the General Research Fund of HK No.27208720
and 17212120.
8


## Page 9

References
[1] Philipp Bergmann, Tim Meinhardt, and Laura Leal-Taixe.
Tracking without bells and whistles. In Proceedings of the
IEEE/CVF International Conference on Computer Vision,
pages 941–951, 2019. 1
[2] Keni Bernardin and Rainer Stiefelhagen. Evaluating mul-
tiple object tracking performance: the clear mot metrics.
EURASIP Journal on Image and Video Processing, 2008:1–
10, 2008. 5
[3] Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, and
Ben Upcroft. Simple online and realtime tracking. In IEEE
international conference on image processing, pages 3464–
3468, 2016. 3, 7
[4] Jinkun Cao, Xin Wang, Trevor Darrell, and Fisher Yu.
Instance-aware predictive navigation in multi-agent environ-
ments. arXiv preprint arXiv:2101.05893, 2021. 1
[5] Jinkun Cao, Xinshuo Weng, Rawal Khirodkar, Jiangmiao
Pang, and Kris Kitani. Observation-centric sort: Rethink-
ing sort for robust multi-object tracking.
arXiv preprint
arXiv:2203.14360, 2022. 7
[6] Mohamed Chaabane, Peter Zhang, Ross Beveridge, and
Stephen O’Hara. Deft: Detection embeddings for tracking.
arXiv preprint arXiv:2102.02267, 2021. 7
[7] Tatjana Chavdarova, Pierre Baqu´e, St´ephane Bouquet, An-
drii Maksai, Cijo Jose, Timur Bagautdinov, Louis Lettry,
Pascal Fua, Luc Van Gool, and Franc¸ois Fleuret.
Wild-
track: A multi-camera hd dataset for dense unscripted pedes-
trian detection. In Proceedings of the IEEE/CVF Conference
on Computer Vision and Pattern Recognition, pages 5030–
5039, 2018. 2
[8] Long Chen, Haizhou Ai, Zijie Zhuang, and Chong Shang.
Real-time multiple people tracking with deeply learned can-
didate selection and person re-identiﬁcation.
In IEEE in-
ternational conference on multimedia and expo, pages 1–6,
2018. 7
[9] M Contributors. Mmtracking: Openmmlab video perception
toolbox and benchmark, 2020. 7
[10] Achal Dave, Tarasha Khurana, Pavel Tokmakov, Cordelia
Schmid, and Deva Ramanan. Tao: A large-scale benchmark
for tracking any object. In European Conference on Com-
puter Vision, pages 436–454. Springer, 2020. 2
[11] Patrick Dendorfer, Hamid Rezatoﬁghi, Anton Milan, Javen
Shi, Daniel Cremers, Ian Reid, Stefan Roth, Konrad
Schindler, and Laura Leal-Taix´e.
Mot20: A benchmark
for multi object tracking in crowded scenes. arXiv preprint
arXiv:2003.09003, 2020. 1, 2, 3
[12] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li,
and Li Fei-Fei. Imagenet: A large-scale hierarchical image
database. In Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition, pages 248–255,
2009. 2
[13] James Ferryman and Ali Shahrokni. Pets2009: Dataset and
challenge. In IEEE international workshop on performance
evaluation of tracking and surveillance, pages 1–6, 2009. 2
[14] Zheng Ge, Songtao Liu, Feng Wang, Zeming Li, and Jian
Sun. Yolox: Exceeding yolo series in 2021. arXiv preprint
arXiv:2107.08430, 2021. 6, 7
[15] Andreas Geiger, Philip Lenz, and Raquel Urtasun.
Are
we ready for autonomous driving? the kitti vision bench-
mark suite.
In Proceedings of the IEEE/CVF Conference
on Computer Vision and Pattern Recognition, pages 3354–
3361, 2012. 1, 2, 5, 8
[16] Fredrik Gustafsson. Particle ﬁlter theory and practice with
positioning applications.
IEEE Aerospace and Electronic
Systems Magazine, 25(7):53–82, 2010. 3
[17] Rooji Jinan and Tara Raveendran. Particle ﬁlters for multiple
target tracking. Procedia Technology, 24:980–987, 2016. 3
[18] Rudolph Emil Kalman. A new approach to linear ﬁltering
and prediction problems. 1960. 3, 5
[19] Laura Leal-Taix´e, Anton Milan, Ian Reid, Stefan Roth,
and Konrad Schindler.
Motchallenge 2015:
Towards
a benchmark for multi-target tracking.
arXiv preprint
arXiv:1504.01942, 2015. 2
[20] Yiyi Liao, Jun Xie, and Andreas Geiger. Kitti-360: A novel
dataset and benchmarks for urban scene understanding in 2d
and 3d. arXiv preprint arXiv:2109.13410, 2021. 2
[21] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays,
Pietro Perona, Deva Ramanan, Piotr Doll´ar, and C Lawrence
Zitnick. Microsoft coco: Common objects in context. In
European Conference on Computer Vision, pages 740–755.
Springer, 2014. 8
[22] Jonathon Luiten, Aljosa Osep, Patrick Dendorfer, Philip
Torr,
Andreas Geiger,
Laura Leal-Taix´e,
and Bastian
Leibe.
Hota: A higher order metric for evaluating multi-
object tracking. International Journal of Computer Vision,
129(2):548–578, 2021. 5
[23] Tim Meinhardt, Alexander Kirillov, Laura Leal-Taixe, and
Christoph Feichtenhofer. Trackformer: Multi-object track-
ing with transformers.
arXiv preprint arXiv:2101.02702,
2021. 2
[24] Anton Milan, Laura Leal-Taix´e, Ian Reid, Stefan Roth, and
Konrad Schindler.
Mot16: A benchmark for multi-object
tracking. arXiv preprint arXiv:1603.00831, 2016. 1, 2, 3
[25] Jiangmiao Pang, Linlu Qiu, Xia Li, Haofeng Chen, Qi
Li, Trevor Darrell, and Fisher Yu.
Quasi-dense similar-
ity learning for multiple object tracking. In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern
Recognition, pages 164–173, 2021. 1, 2, 7
[26] Ziqiang Pei. Deepsort pytorch. https://github.com/
ZQPei/deep_sort_pytorch, 2019. 4, 5
[27] Akshay Rangesh and Mohan Manubhai Trivedi. No blind
spots: Full-surround multi-object tracking for autonomous
vehicles using cameras and lidars.
IEEE Transactions on
Intelligent Vehicles, 4(4):588–599, 2019. 1
[28] Ergys Ristani, Francesco Solera, Roger Zou, Rita Cucchiara,
and Carlo Tomasi. Performance measures and a data set for
multi-target, multi-camera tracking. In European Conference
on Computer Vision, pages 17–35. Springer, 2016. 5
[29] Peize Sun, Yi Jiang, Rufeng Zhang, Enze Xie, Jinkun Cao,
Xinting Hu, Tao Kong, Zehuan Yuan, Changhu Wang, and
Ping Luo. Transtrack: Multiple-object tracking with trans-
former. arXiv preprint arXiv:2012.15460, 2020. 2, 7
[30] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien
Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou,
9


## Page 10

Yuning Chai, Benjamin Caine, et al. Scalability in perception
for autonomous driving: Waymo open dataset. In Proceed-
ings of the IEEE/CVF Conference on Computer Vision and
Pattern Recognition, pages 2446–2454, 2020. 2
[31] Laurens Van der Maaten and Geoffrey Hinton.
Visualiz-
ing data using t-sne. Journal of machine learning research,
9(11), 2008. 6
[32] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko-
reit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia
Polosukhin. Attention is all you need. In Advances in neural
information processing systems, pages 5998–6008, 2017. 2
[33] Zhongdao Wang, Liang Zheng, Yixuan Liu, Yali Li, and
Shengjin Wang. Towards real-time multi-object tracking. In
European Conference on Computer Vision, pages 107–122.
Springer, 2020. 2, 3
[34] Nicolai Wojke, Alex Bewley, and Dietrich Paulus. Simple
online and realtime tracking with a deep association met-
ric. In IEEE international conference on image processing,
pages 3645–3649, 2017. 1, 3, 7
[35] Jialian Wu, Jiale Cao, Liangchen Song, Yu Wang, Ming
Yang, and Junsong Yuan. Track to detect and segment: An
online multi-object tracker. In Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition,
pages 12352–12361, 2021. 1, 2, 7
[36] Ning Xu, Linjie Yang, Yuchen Fan, Dingcheng Yue, Yuchen
Liang, Jianchao Yang, and Thomas Huang.
Youtube-vos:
A large-scale video object segmentation benchmark. arXiv
preprint arXiv:1809.03327, 2018. 2
[37] Alper Yilmaz, Omar Javed, and Mubarak Shah. Object track-
ing: A survey. Acm computing surveys (CSUR), 38(4):13–es,
2006. 1
[38] Fisher Yu, Wenqi Xian, Yingying Chen, Fangchen Liu, Mike
Liao, Vashisht Madhavan, and Trevor Darrell. Bdd100k: A
diverse driving video database with scalable annotation tool-
ing. arXiv preprint arXiv:1805.04687, 2(5):6, 2018. 1, 2,
5
[39] Fangao Zeng, Bin Dong, Tiancai Wang, Cheng Chen,
Xiangyu Zhang, and Yichen Wei.
Motr:
End-to-end
multiple-object tracking with transformer.
arXiv preprint
arXiv:2105.03247, 2021. 2, 7
[40] Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Zehuan
Yuan, Ping Luo, Wenyu Liu, and Xinggang Wang. Byte-
track: Multi-object tracking by associating every detection
box. arXiv preprint arXiv:2110.06864, 2021. 2, 3, 7, 8
[41] Yifu Zhang, Chunyu Wang, Xinggang Wang, Wenjun Zeng,
and Wenyu Liu. Fairmot: On the fairness of detection and
re-identiﬁcation in multiple object tracking.
International
Journal of Computer Vision, 129(11):3069–3087, 2021. 1,
2, 3, 7
[42] Xingyi Zhou, Vladlen Koltun, and Philipp Kr¨ahenb¨uhl.
Tracking objects as points. In European Conference on Com-
puter Vision, pages 474–490. Springer, 2020. 2, 7
[43] Xingyi Zhou, Dequan Wang, and Philipp Kr¨ahenb¨uhl. Ob-
jects as points. arXiv preprint arXiv:1904.07850, 2019. 5,
8
[44] Xingyi Zhou, Tianwei Yin, Vladlen Koltun, and Phillip
Kr¨ahenb¨uhl. Global tracking transformers. arXiv preprint
arXiv:2203.13250, 2022. 7
A. Change Log
Version 1 (2021-11-29)
- Initial arXiv version.
Version 2 (2022-05-05)
- Update MOTR in Table 3. For more details, please refer
to https://github.com/megvii-model/MOTR.
- Add GTR and OC-SORT in Table 3.
- Compare different motion models by using YOLOX
detector, in new Table 5, to be consistent with Table 4.
Version 3 (2022-05-24)
- Update QDTrack in Table 3. New QDTrack replaces
the Faster RCNN detector in the original QDTrack with a
YOLOX model, by applying the same data augmentation
strategy as in ByteTrack, and trained on DanceTrack train
for 24 epochs. The other hyperparameters are aligned with
ByteTrack, e.g. conﬁdence thresholds for new tracks and
existing tracks, input image resolution. Neither the tracking
algorithm was changed nor the embedding learning compo-
nent.
10
