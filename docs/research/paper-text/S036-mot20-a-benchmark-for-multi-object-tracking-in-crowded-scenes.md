---
source_id: S036
title: MOT20: A benchmark for multi object tracking in crowded scenes
source_url: https://arxiv.org/pdf/2003.09003
source_file: docs/research/papers/S036-mot20-a-benchmark-for-multi-object-tracking-in-crowded-scenes.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S036-mot20-a-benchmark-for-multi-object-tracking-in-crowded-scenes.pdf
## PDF metadata
- format: PDF 1.5
- creator: LaTeX with hyperref package
- producer: pdfTeX-1.40.17
- creationDate: D:20200323003610Z
- modDate: D:20200323003610Z


## Page 1

1
MOT20: A benchmark for multi object tracking in
crowded scenes
Patrick Dendorfer, Hamid Rezatoﬁghi, Anton Milan, Javen Shi, Daniel Cremers, Ian Reid,
Stefan Roth, Konrad Schindler, and Laura Leal-Taix´e
Abstract—Standardized benchmarks are crucial for the majority of computer vision applications. Although leaderboards and ranking
tables should not be over-claimed, benchmarks often provide the most objective measure of performance and are therefore important
guides for research. The benchmark for Multiple Object Tracking, MOTChallenge, was launched with the goal to establish a standardized
evaluation of multiple object tracking methods. The challenge focuses on multiple people tracking, since pedestrians are well studied in
the tracking community, and precise tracking and detection has high practical relevance. Since the ﬁrst release, MOT15 [5], MOT16 [8],
and MOT17 [8] have tremendously contributed to the community by introducing a clean dataset and precise framework to benchmark
multi-object trackers. In this paper, we present our MOT20 benchmark, consisting of 8 new sequences depicting very crowded
challenging scenes. The benchmark was presented ﬁrst at the 4th BMTT MOT Challenge Workshop at the Computer Vision and
Pattern Recognition Conference (CVPR) 2019, and gives to chance to evaluate state-of-the-art methods for multiple object tracking
when handling extremely crowded scenarios.
Index Terms—multiple people tracking, benchmark, evaluation metrics, dataset
!
1
INTRODUCTION
Since its ﬁrst release in 2014, MOTChallenge has attracted
more than 1, 000 active users who have successfully
submitted their trackers and detectors to ﬁve different
challenges, spanning 44 sequences with 2.7M bounding
boxes over a total length of 36k seconds. As evaluating
and comparing multi-target tracking methods is not
trivial (cf. e.g. [10]), MOTChallenge provides carefully
annotated datasets and clear metrics to evaluate the per-
formance of tracking algorithms and pedestrian detec-
tors. Parallel to the MOTChallenge all-year challenges, we
organize workshop challenges on multi-object tracking
for which we often introduce new data.
In this paper, we introduce the MOT20 benchmark,
consisting of 8 novel sequences out of 3 very crowded
scenes. All sequences have been carefully selected and
annotated according to the evaluation protocol of pre-
vious challenges [5], [8]. This benchmark addresses the
challenge of very crowded scenes in which the density
can reach values of 246 pedestrians per frame. The
P. Dendorfer and L. Leal-Taix´e are with the Dynamic Vision and Learning
Group at TUM Munich, Germany.
H. Rezatoﬁghi, J. Shi, and I. Reid are with the Australian Institute for
Machine Learning and the School of Computer Science at University of
Adelaide.
A. Milan is with Amazon, Berlin, Germany. This work was done prior to
joining Amazon.
K. Schindler is with the Photogrammetry and Remote Sensing Group at ETH
Zurich, Switzerland.
D. Cremers is with the Computer Vision Group at TUM Munich, Germany.
S. Roth is with the Department of Computer Science, Technische Universit¨at
Darmstadt, Germany.
Primary contacts: patrick.dendorfer@tum.de, leal.taixe@tum.de
sequences were ﬁlmed in both indoor and outdoor lo-
cations, and include day and night time shots. Figure 1
shows the split of the sequences of the three scenes into
training and testing sets. The testing data consists of
sequences from known as well as from an unknown
scenes in order to measure the genralization capabilities
of both detectors and trackers. We make available the
images for all sequences, the ground truth annotations
for the training set as well as a set of public detections
(obtained from a Faster R-CNN trained on the training
data) for the tracking challenge.
The MOT20 challenges and all data, current ranking
and submission guidelines can be found at:
http://www.motchallenge.net/
2
ANNOTATION RULES
For the annotation of the dataset, we follow the protocol
introduced in MOT16, ensuring that every moving per-
son or vehicle within each sequence is annotated with a
bounding box as accurately as possible. In the following,
we deﬁne a clear protocol that was obeyed throughout
the entire dataset to guarantee consistency.
2.1
Target class
In this benchmark, we are interested in tracking moving
objects in videos. In particular, we are interested in
evaluating multiple people tracking algorithms, hence,
people will be the center of attention of our annotations.
We divide the pertinent classes into three categories:
arXiv:2003.09003v1  [cs.CV]  19 Mar 2020


## Page 2

2
Fig. 1: An overview of the MOT20 dataset. The dataset consists of 8 different sequences from 3 different scenes.
The test dataset has two known and one unknown scene. Top: training sequences; bottom: test sequences.
Fig. 2: we provide for the challenges. Left: Image of each frame of the sequences; middle: ground truth labels
including all classes. Only provided for training set; right: public detections from trained Faster R-CNN.
(i) moving pedestrians;
(ii) people that are not in an upright position, not moving,
or artiﬁcial representations of humans; and
(iii) vehicles and occluders.
In the ﬁrst group, we annotate all moving pedestrians
that appear in the ﬁeld of view and can be determined
as such by the viewer. Furthermore, if a person brieﬂy
bends over or squats, e.g., to pick something up or to talk
to a child, they shall remain in the standard pedestrian
class. The algorithms that submit to our benchmark are
expected to track these targets.
In the second group, we include all people-like objects
whose exact classiﬁcation is ambiguous and can vary de-
pending on the viewer, the application at hand, or other
factors. We annotate all static people, e.g., sitting, lying
down, or do stand still at the same place over the whole
sequence. The idea is to use these annotations in the
evaluation such that an algorithm is neither penalized
nor rewarded for tracking, e.g., a sitting or not moving
person.
In the third group, we annotate all moving vehicles
such as cars, bicycles, motorbikes and non-motorized
vehicles (e.g., strollers), as well as other potential oc-
cluders. These annotations will not play any role in
the evaluation, but are provided to the users both for
training purposes and for computing the level of occlu-
sion of pedestrians. Static vehicles (parked cars, bicycles)
are not annotated as long as they do not occlude any
pedestrians.
3
DATASETS
The dataset for the new benchmark has been carefully
selected to challenge trackers and detectors on extremely
crowded scenes. In contrast to previous challenges, some
of the new sequences show a pedestrian density of 246
pedestrians per frame. In Fig. 1 and Tab. 1, we show an
overview of the sequences included in the benchmark.
3.1
MOT 20 sequences
We have compiled a total of 8 sequences, of which we
use half for training and half for testing. The annotations
of the testing sequences will not be released in order
to avoid (over)ﬁtting of the methods to the speciﬁc
sequences. The sequences are ﬁlmed in three different
scenes. Several sequences are ﬁlmed per scene and dis-
tributed in the train and test sets. One of the scenes
though, is reserved for test time, in order to challenge
the generalization capabilities of the methods.
The new data contains circa 3 times more bounding
boxes for training and testing compared to MOT17.
All sequences are ﬁlmed in high resolution from an
elevated viewpoint, and the mean crowd density reaches
246 pedestrians per frame which 10 times denser when
compared to the ﬁrst benchmark release. Hence, we
expect the new sequences to be more challenging for
the tracking community and to push the models to their
limits when it comes to handling extremely crowded
scenes. In Tab. 1, we give an overview of the training
and testing sequence characteristics for the challenge,
including the number of bounding boxes annotated.
Aside from pedestrians, the annotations also include
other classes like vehicles or bicycles, as detailed in
Sec. 2. In Tab. 2, we detail the types of annotations that
can be found in each sequence of MOT20.


## Page 3

3
Training sequences
Name
FPS
Resolution
Length
Tracks
Boxes
Density
Description
Source
MOT20-01
25
1920x1080
429 (00:17)
74
19,870
46.32
indoor
new
MOT20-02
25
1920x1080
2,782 (01:51)
270
154,742
55.62
indoor
new
MOT20-03
25
1173x880
2,405 (01:36)
702
313,658
130.42
outdoor, night
new
MOT20-05
25
1654x1080
3,315 (02:13)
1169
646,344
194.98
outdoor, night
new
Total training
8,931 (05:57)
2,215
1,134,614
127.04
Testing sequences
Name
FPS
Resolution
Length
Tracks
Boxes
Density
Description
Source
MOT20-04
25
1545x1080
2,080 (01:23)
669
274,084
131.77
outdoor, night
new
MOT20-06
25
1920x734
1,008 (00:40)
271
132,757
131.70
outdoor, day
new
MOT20-07
25
1920x1080
585 (00:23)
111
33,101
56.58
indoor
new
MOT20-08
25
1920x734
806 (00:32)
191
77,484
96.13
outdoor, day
new
Total training
4,479 (02:58)
1,242
517,426
115.52
TABLE 1: Overview of the sequences currently included in the MOT20 benchmark considering pedestrians.
Annotation classes
Sequence
Pedestrian
Non motorized vehicle
Static person
Occluder on the ground
crowd
Total
MOT20-01
19,870
0
2,574
4,203
0
26,647
MOT20-02
154,742
4,021
11,128
32,324
0
202,215
MOT20-03
313,658
1,436
22,310
16,835
2,489
356,728
MOT20-04
274,084
3,110
92,251
2,080
0
371,525
MOT20-05
646,344
7,513
90,843
6,630
0
751,330
MOT20-06
132,757
1,248
60,102
12,428
1,008
207,543
MOT20-07
33,101
800
3,685
3,510
0
41,096
MOT20-08
77,484
4,237
52,998
9,776
806
145,301
Total
1,652,040
22,365
335,891
87,786
4,303
2,102,385
TABLE 2: Overview of the types of annotations currently found in the MOT20 benchmark.
3.2
Detections
We trained a Faster R-CNN [11] with ResNet101 [4]
backbone on the MOT20 training sequences, obtaining
the detection results presented in Table 6. This evaluation
follows the standard protocol for the MOT20 challenge
and only accounts for pedestrians. Static persons and
other classes are not considered and ﬁltered out from
both, the detections, as well as the ground truth.
A detailed breakdown of detection bounding boxes on
individual sequences is provided in Tab. 3.
Seq
nDet.
nDet./fr.
min height
max height
MOT20-01
12610
29.39
30
289
MOT20-02
89837
32.29
25
463
MOT20-03
177347
73.74
16
161
MOT20-04
228298
109.76
23
241
MOT20-05
381349
115.04
26
245
MOT20-06
69467
68.92
27
304
MOT20-07
20330
34.75
21
381
MOT20-08
43703
54.22
37
302
Total
1022941
76.28
16
463
TABLE 3: Detection bounding box statistics.
For the tracking challenge, we provide these public
detections as a baseline to be used for training and
testing of the trackers. For the MOT20 challenge, we will
only accept results on public detections. When later the
benchmark will be open for continuous submissions, we
will accept both public as well as private detections.
3.3
Data format
All images were converted to JPEG and named sequen-
tially to a 6-digit ﬁle name (e.g. 000001.jpg). Detection
and annotation ﬁles are simple comma-separated value
(CSV) ﬁles. Each line represents one object instance and
contains 9 values as shown in Tab. 4.
The ﬁrst number indicates in which frame the object
appears, while the second number identiﬁes that object
as belonging to a trajectory by assigning a unique ID (set
to −1 in a detection ﬁle, as no ID is assigned yet). Each
object can be assigned to only one trajectory. The next
four numbers indicate the position of the bounding box
of the pedestrian in 2D image coordinates. The position
is indicated by the top-left corner as well as width
and height of the bounding box. This is followed by a
single number, which in case of detections denotes their
conﬁdence score. The last two numbers for detection ﬁles
are ignored (set to -1).
An example of such a 2D detection ﬁle is:
1, -1, 794.2, 47.5, 71.2, 174.8, 67.5, -1, -1
1, -1, 164.1, 19.6, 66.5, 163.2, 29.4, -1, -1
1, -1, 875.4, 39.9, 25.3, 145.0, 19.6, -1, -1
2, -1, 781.7, 25.1, 69.2, 170.2, 58.1, -1, -1
For the ground truth and results ﬁles, the 7th value
(conﬁdence score) acts as a ﬂag whether the entry is to
be considered. A value of 0 means that this particular
instance is ignored in the evaluation, while a value of
1 is used to mark it as active. The 8th number indicates
the type of object annotated, following the convention of
Tab. 5. The last number shows the visibility ratio of each


## Page 4

4
Position
Name
Description
1
Frame number
Indicate at which frame the object is present
2
Identity number
Each pedestrian trajectory is identiﬁed by a unique ID (−1 for detections)
3
Bounding box left
Coordinate of the top-left corner of the pedestrian bounding box
4
Bounding box top
Coordinate of the top-left corner of the pedestrian bounding box
5
Bounding box width
Width in pixels of the pedestrian bounding box
6
Bounding box height
Height in pixels of the pedestrian bounding box
7
Conﬁdence score
DET:
Indicates
how
conﬁdent
the
detector
is
that
this
instance
is
a
pedestrian.
GT: It acts as a ﬂag whether the entry is to be considered (1) or ignored (0).
8
Class
GT: Indicates the type of object annotated
9
Visibility
GT: Visibility ratio, a number between 0 and 1 that says how much of that object is visible. Can be due
to occlusion and due to image border cropping.
TABLE 4: Data format for the input and output ﬁles, both for detection (DET) and annotation/ground truth (GT)
ﬁles.
Label
ID
Pedestrian
1
Person on vehicle
2
Car
3
Bicycle
4
Motorbike
5
Non motorized vehicle
6
Static person
7
Distractor
8
Occluder
9
Occluder on the ground
10
Occluder full
11
Reﬂection
12
Crowd
13
TABLE 5: Label classes present in the annotation ﬁles and
ID appearing in the 8th column of the ﬁles as described
in Tab. 4.
bounding box. This can be due to occlusion by another
static or moving object, or due to image border cropping.
An example of such an annotation 2D ﬁle is:
1, 1, 794.2, 47.5, 71.2, 174.8, 1, 1, 0.8
1, 2, 164.1, 19.6, 66.5, 163.2, 1, 1, 0.5
2, 4, 781.7, 25.1, 69.2, 170.2, 0, 12, 1.
In this case, there are 2 pedestrians in the ﬁrst frame
of the sequence, with identity tags 1, 2. In the second
frame, we can see a static person (class 7), which is to
be considered by the evaluation script and will neither
count as a false negative, nor as a true positive, inde-
pendent of whether it is correctly recovered or not. Note
that all values including the bounding box are 1-based,
i.e. the top left corner corresponds to (1, 1).
To obtain a valid result for the entire benchmark,
a separate CSV ﬁle following the format described
above must be created for each sequence and called
‘‘Sequence-Name.txt’’. All ﬁles must be com-
pressed into a single ZIP ﬁle that can then be uploaded
to be evaluated.
4
EVALUATION
Our framework is a platform for fair comparison of state-
of-the-art tracking methods. By providing authors with
standardized ground truth data, evaluation metrics and
scripts, as well as a set of precomputed detections, all
methods are compared under the exact same conditions,
thereby isolating the performance of the tracker from
everything else. In the following paragraphs, we detail
the set of evaluation metrics that we provide in our
benchmark.
4.1
Evaluation metrics
In the past, a large number of metrics for quantitative
evaluation of multiple target tracking have been pro-
posed [2], [6], [12]–[14], [16]. Choosing “the right” one
is largely application dependent and the quest for a
unique, general evaluation metric is still ongoing. On the
one hand, it is desirable to summarize the performance
into one single number to enable a direct comparison. On
the other hand, one might not want to lose information
about the individual errors made by the algorithms and
provide several performance estimates, which precludes
a clear ranking.
Following a recent trend [1], [9], [15], we employ two
sets of measures that have established themselves in the
literature: The CLEAR metrics proposed by Stiefelhagen
et al. [14], and a set of track quality measures introduced
by Wu and Nevatia [16]. The evaluation scripts used in
our benchmark are publicly available.1
4.1.1
Tracker-to-target assignment
There are two common prerequisites for quantifying the
performance of a tracker. One is to determine for each
hypothesized output, whether it is a true positive (TP)
that describes an actual (annotated) target, or whether
the output is a false alarm (or false positive, FP). This
decision is typically made by thresholding based on
a deﬁned distance (or dissimilarity) measure d (see
Sec. 4.1.2). A target that is missed by any hypothesis
is a false negative (FN). A good result is expected to
have as few FPs and FNs as possible. Next to the
absolute numbers, we also show the false positive ratio
measured by the number of false alarms per frame (FAF),
sometimes also referred to as false positives per image
(FPPI) in the object detection literature.
Obviously, it may happen that the same target is
covered by multiple outputs. The second prerequisite
before computing the numbers is then to establish the
1. http://motchallenge.net/devkit


## Page 5

5
Training sequences
Sequence
AP
Rcll
Prcn
FAR
GT
TP
FP
FN
MODA
MODP
MOT20-01
0.82
86.5
99.5
0.14
12945
11199
58
1746
86.06
91.61
MOT20-02
0.82
85.9
99.5
0.15
93107
79971
421
13136
85.44
92.13
MOT20-03
0.54
59.0
98.4
1.10
278148
163988
2653
114160
58.00
86.00
MOT20-05
0.63
64.2
99.4
0.60
528037
338826
1979
189211
63.79
87.59
Testing sequences
Sequence
AP
Rcll
Prcn
FAR
GT
TP
FP
FN
MODA
MODP
MOT20-04
0.63
69.7
98.0
1.55
230729
160783
3230
69946
68.29
81.41
MOT20-06
0.43
57.9
74.4
12.64
63889
37002
12745
26887
37.97
73.67
MOT20-07
0.78
83.6
92.5
1.89
16298
13627
1106
2671
76.83
79.11
MOT20-08
0.38
55.2
61.6
13.93
32608
17998
11230
14610
20.76
71.55
TABLE 6: Overview of performance of Faster R-CNN detector trained on the MOT20 training dataset.
GT
Traj.
ID sw.
ID sw.
FP
TP FN Tracked
Frag.
ID sw.
(a)
(b)
(c)
(d)
Frag.
1
2
3
4
5
6
1
2
3
4
5
6
1
2
3
4
5
6
1
2
3
4
5
6
frame
Fig. 3: Four cases illustrating tracker-to-target assignments. (a) An ID switch occurs when the mapping switches
from the previously assigned red track to the blue one. (b) A track fragmentation is counted in frame 3 because
the target is tracked in frames 1-2, then interrupts, and then reacquires its ‘tracked’ status at a later point. A new
(blue) track hypothesis also causes an ID switch at this point. (c) Although the tracking results is reasonably good,
an optimal single-frame assignment in frame 1 is propagated through the sequence, causing 5 missed targets (FN)
and 4 false positives (FP). Note that no fragmentations are counted in frames 3 and 6 because tracking of those
targets is not resumed at a later point. (d) A degenerate case illustrating that target re-identiﬁcation is not handled
correctly. An interrupted ground truth trajectory will cause a fragmentation. Note the less intuitive ID switch, which
is counted because blue is the closest target in frame 5 that is not in conﬂict with the mapping in frame 4.
correspondence between all annotated and hypothesized
objects under the constraint that a true object should be
recovered at most once, and that one hypothesis cannot
account for more than one target.
For the following, we assume that each ground truth
trajectory has one unique start and one unique end
point, i.e. that it is not fragmented. Note that the current
evaluation procedure does not explicitly handle target
re-identiﬁcation. In other words, when a target leaves
the ﬁeld-of-view and then reappears, it is treated as an
unseen target with a new ID. As proposed in [14], the
optimal matching is found using Munkre’s (a.k.a. Hun-
garian) algorithm. However, dealing with video data,
this matching is not performed independently for each
frame, but rather considering a temporal correspon-
dence. More precisely, if a ground truth object i is
matched to hypothesis j at time t −1 and the distance
(or dissimilarity) between i and j in frame t is below
td, then the correspondence between i and j is carried
over to frame t even if there exists another hypothesis
that is closer to the actual target. A mismatch error (or
equivalently an identity switch, IDSW) is counted if a
ground truth target i is matched to track j and the last
known assignment was k ̸= j. Note that this deﬁnition
of ID switches is more similar to [6] and stricter than
the original one [14]. Also note that, while it is certainly
desirable to keep the number of ID switches low, their
absolute number alone is not always expressive to assess
the overall performance, but should rather be considered
in relation to the number of recovered targets. The
intuition is that a method that ﬁnds twice as many
trajectories will almost certainly produce more identity
switches. For that reason, we also state the relative
number of ID switches, i.e., IDSW/Recall.
These relationships are illustrated in Fig. 3. For sim-
plicity, we plot ground truth trajectories with dashed
curves, and the tracker output with solid ones, where
the color represents a unique target ID. The grey areas
indicate the matching threshold (see next section). Each
true target that has been successfully recovered in one
particular frame is represented with a ﬁlled black dot
with a stroke color corresponding to its matched hypoth-
esis. False positives and false negatives are plotted as
empty circles. See ﬁgure caption for more details.
After determining true matches and establishing cor-
respondences it is now possible to compute the metrics.
We do so by concatenating all test sequences and eval-
uating on the entire benchmark. This is in general more
meaningful instead of averaging per-sequences ﬁgures
due to the large variation in the number of targets.


## Page 6

6
4.1.2
Distance measure
In the most general case, the relationship between
ground truth objects and a tracker output is established
using bounding boxes on the image plane. Similar to
object detection [3], the intersection over union (a.k.a.
the Jaccard index) is usually employed as the similarity
criterion, while the threshold td is set to 0.5 or 50%.
4.1.3
Target-like annotations
People are a common object class present in many
scenes, but should we track all people in our benchmark?
For example, should we track static people sitting on
a bench? Or people on bicycles? How about people
behind a glass? We deﬁne the target class of CVPR19
as all upright walking people that are reachable along
the viewing ray without a physical obstacle, i.e. reﬂec-
tions, people behind a transparent wall or window are
excluded. We also exclude from our target class people
on bicycles or other vehicles. For all these cases where
the class is very similar to our target class (see Figure 4),
we adopt a similar strategy as in [7]. That is, a method
is neither penalized nor rewarded for tracking or not
tracking those similar classes. Since a detector is likely to
ﬁre in those cases, we do not want to penalize a tracker
with a set of false positives for properly following that
set of detections, i.e. of a person on a bicycle. Likewise,
we do not want to penalize with false negatives a tracker
that is based on motion cues and therefore does not track
a sitting person.
In order to handle these special cases, we adapt the
tracker-to-target assignment algorithm to perform the
following steps:
1) At each frame, all bounding boxes of the result ﬁle
are matched to the ground truth via the Hungarian
algorithm.
2) In contrast to MOT17 we account for the very
crowded scenes and exclude result boxes that over-
lap > 75% with one of these classes (distractor,
static person, reﬂection, person on vehicle) and
remove them from the solution in the detection
challenge.
3) During the ﬁnal evaluation, only those boxes that
are annotated as pedestrians are used.
4.1.4
Multiple Object Tracking Accuracy
The MOTA [14] is perhaps the most widely used metric
to evaluate a tracker’s performance. The main reason for
this is its expressiveness as it combines three sources of
errors deﬁned above:
MOTA = 1 −
P
t (FNt + FPt + IDSWt)
P
t GTt
,
(1)
where t is the frame index and GT is the number of
ground truth objects. We report the percentage MOTA
(−∞, 100] in our benchmark. Note that MOTA can also
be negative in cases where the number of errors made
by the tracker exceeds the number of all objects in the
scene.
Even though the MOTA score gives a good indica-
tion of the overall performance, it is highly debatable
whether this number alone can serve as a single perfor-
mance measure.
Robustness. One incentive behind compiling this
benchmark was to reduce dataset bias by keeping the
data as diverse as possible. The main motivation is to
challenge state-of-the-art approaches and analyze their
performance in unconstrained environments and on un-
seen data. Our experience shows that most methods can
be heavily overﬁtted on one particular dataset, and may
not be general enough to handle an entirely different
setting without a major change in parameters or even in
the model.
To indicate the robustness of each tracker across all
benchmark sequences, we show the standard deviation
of their MOTA score.
4.1.5
Multiple Object Tracking Precision
The Multiple Object Tracking Precision is the average
dissimilarity between all true positives and their corre-
sponding ground truth targets. For bounding box over-
lap, this is computed as
MOTP =
P
t,i dt,i
P
t ct
,
(2)
where ct denotes the number of matches in frame t
and dt,i is the bounding box overlap of target i with
its assigned ground truth object. MOTP thereby gives
the average overlap between all correctly matched hy-
potheses and their respective objects and ranges between
td := 50% and 100%.
It is important to point out that MOTP is a measure of
localization precision, not to be confused with the positive
predictive value or relevance in the context of precision /
recall curves used, e.g., in object detection.
In practice, it mostly quantiﬁes the localization ac-
curacy of the detector, and therefore, it provides little
information about the actual performance of the tracker.
4.1.6
Track quality measures
Each ground truth trajectory can be classiﬁed as mostly
tracked (MT), partially tracked (PT), and mostly lost
(ML). This is done based on how much of the trajectory is
recovered by the tracking algorithm. A target is mostly
tracked if it is successfully tracked for at least 80% of
its life span. Note that it is irrelevant for this measure
whether the ID remains the same throughout the track.
If a track is only recovered for less than 20% of its
total length, it is said to be mostly lost (ML). All other
tracks are partially tracked. A higher number of MT and
few ML is desirable. We report MT and ML as a ratio
of mostly tracked and mostly lost targets to the total
number of ground truth trajectories.
In certain situations one might be interested in ob-
taining long, persistent tracks without gaps of untracked
periods. To that end, the number of track fragmentations


## Page 7

7
Fig. 4: The annotations include different classes. The target class are pedestrians (left). Besides pedestrians there
exist special classes in the data such as static person and non-motorized vehicles (non mot vhcl). However, these
classes are ﬁlter out during evaluation and do not effect the test score. Thirdly, we annotate occluders and crowds.
(FM) counts how many times a ground truth trajectory is
interrupted (untracked). In other words, a fragmentation
is counted each time a trajectory changes its status from
tracked to untracked and tracking of that same trajectory
is resumed at a later point. Similarly to the ID switch
ratio (cf. Sec. 4.1.1), we also provide the relative number
of fragmentations as FM / Recall.
4.1.7
Tracker ranking
As we have seen in this section, there are a number of
reasonable performance measures to assess the quality
of a tracking system, which makes it rather difﬁcult to
reduce the evaluation to one single number. To never-
theless give an intuition on how each tracker performs
compared to its competitors, we compute and show
the average rank for each one by ranking all trackers
according to each metric and then averaging across all
performance measures.
5
CONCLUSION AND FUTURE WORK
We have presented a new challenging set of sequences
within the MOTChallenge benchmark. Theses sequences
contain a large number of targets to be tracked and the
scenes are substantially more crowded when compared
to previous MOTChallenge releases. The scenes are care-
fully chosen and included indoor/ outdoor and day/
night scenarios.
We believe that the MOT20 release within the already
established MOTChallenge benchmark provides a fairer
comparison of state-of-the-art tracking methods, and
challenges researchers to develop more generic methods
that perform well in unconstrained environments and on
very crowded scenes.
REFERENCES
[1]
S.-H. Bae and K.-J. Yoon.
Robust online multi-object tracking
based on tracklet conﬁdence and online discriminative appear-
ance learning. In CVPR 2014.
[2]
K. Bernardin and R. Stiefelhagen.
Evaluating multiple object
tracking performance: The CLEAR MOT metrics. Image and Video
Processing, 2008(1):1–10, May 2008.
[3]
M. Everingham, L. Van Gool, C. Williams, J. Winn, and A. Zisser-
man. The PASCAL Visual Object Classes Challenge 2012 (VOC2012)
Results. 2012.
[4]
K. He, X. Zhang, S. Ren, and J. Sun.
Deep Residual Learning
for Image Recognition. arXiv e-prints, page arXiv:1512.03385, Dec
2015.
[5]
L. Leal-Taix´e, A. Milan, I. Reid, S. Roth, and K. Schindler.
MOTChallenge 2015: Towards a benchmark for multi-target track-
ing. arXiv:1504.01942, 2015.
[6]
Y. Li, C. Huang, and R. Nevatia. Learning to associate: Hybrid-
boosted multi-target tracker for crowded scene. In CVPR 2009.
[7]
M. Mathias, R. Benenson, M. Pedersoli, and L. V. Gool.
Face
detection without bells and whistles. In ECCV 2014, 2014.
[8]
A. Milan, L. Leal-Taix´e, I. Reid, S. Roth, and K. Schindler. MOT16:
A benchmark for multi-object tracking. arXiv:1603.00831 [cs], Mar.
2016. arXiv: 1603.00831.
[9]
A. Milan, S. Roth, and K. Schindler.
Continuous energy mini-
mization for multitarget tracking. PAMI, 36(1):58–72, 2014.
[10] A. Milan, K. Schindler, and S. Roth. Challenges of ground truth
evaluation of multi-target tracking. In 2013 IEEE Conference on
Computer Vision and Pattern Recognition Workshops (CVPRW), pages
735–742, June 2013.
[11] S. Ren, K. He, R. Girshick, and J. Sun. Faster R-CNN: Towards
Real-Time Object Detection with Region Proposal Networks.
arXiv e-prints, page arXiv:1506.01497, Jun 2015.
[12] D. Schuhmacher, B.-T. Vo, and B.-N. Vo. A consistent metric for
performance evaluation of multi-object ﬁlters. IEEE Transactions
on Signal Processing, 56(8):3447–3457, Aug. 2008.
[13] K. Smith, D. Gatica-Perez, J.-M. Odobez, and S. Ba. Evaluating
multi-object tracking. In Workshop on Empirical Evaluation Methods
in Computer Vision (EEMCV).
[14] R.
Stiefelhagen,
K.
Bernardin,
R.
Bowers,
J.
S.
Garofolo,
D. Mostefa, and P. Soundararajan. The clear 2006 evaluation. In
CLEAR, 2006.
[15] L. Wen, W. Li, J. Yan, Z. Lei, D. Yi, and S. Z. Li. Multiple target
tracking based on undirected hierarchical relation hypergraph. In
CVPR 2014.
[16] B. Wu and R. Nevatia. Tracking of multiple, partially occluded
humans based on static body part detection. In CVPR 2006, pages
951–958, 2006.
