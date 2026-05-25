---
source_id: S013
title: Sentinel for confidence-aware multi-object tracking
source_url: https://www.nature.com/articles/s41598-026-43938-2.pdf
source_file: docs/research/papers/S013-sentinel-for-confidence-aware-multi-object-tracking.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S013-sentinel-for-confidence-aware-multi-object-tracking.pdf
## PDF metadata
- format: PDF 1.4
- creator: Adobe InDesign 18.3 (Windows)
- producer: Adobe PDF Library 17.0; modified using iText® 5.5.13.4 ©2000-2024 iText Group NV (SPRINGER SBM; licensed version)
- creationDate: D:20260314100443+01'00'
- modDate: D:20260428010746+02'00'


## Page 1

Sentinel for confidence-aware 
multi-object tracking
Hyun-Sung Yang1, Sung-Wook Park1, Chun-Bo Sim1 & Se-Hoon Jung2
Multi-object tracking faces two persistent challenges: managing detector confidence and preventing 
track loss under prolonged occlusions. We introduce Sentinel, an uncertainty-aware tracker that 
diagnoses per-track uncertainty online and proactively optimizes its tracking strategy. Sentinel consists 
of two components. Confidence Aware Association (CAA) dynamically reweighs the association-cost 
terms according to the current track state, enabling the effective use of low-confidence detections 
while suppressing identity switches. Survival Boosting Mechanism (SBM) preserves tracks at risk 
of disappearance by exploiting weak detection signals to bridge long occlusions, thereby reducing 
fragmentation and maintaining identity continuity. Evaluations on MOT17, MOT20, and DanceTrack 
demonstrate that Sentinel achieves strong performance in Higher Order Tracking Accuracy (HOTA), 
Identification F1-score (IDF1), and Association Accuracy (AssA), demonstrating its strength in identity 
preservation and association quality. While this design introduces modest computational overhead 
and may increase false positives when exploiting low-confidence detections, Sentinel improves 
robustness in realistic, crowded environments by moving beyond passive reliance on detector outputs 
to uncertainty-driven, per-track optimization.
Keywords  Multi-object tracking, CAA, SBM, State dependent weighted association
Multi-object tracking (MOT) is a computer-vision task for understanding dynamic environments. It detects 
multiple objects in video sequences, maintains a consistent identity for each object over time, and estimates 
their trajectories. Its importance continues to grow as a core technology across a wide range of applications, 
including autonomous driving, intelligent surveillance, sports analytics, and robotics. The tracking-by-detection 
(TBD)1,2 paradigm has become a mainstream approach in modern MOT research. TBD decomposes tracking 
into per-frame object detection and a temporal association stage that links detection to trajectories. Advances in 
deep learning have markedly improved this paradigm: high-performance detectors increase the reliability of the 
detection itself, while refined appearance feature extractors enhance interobject discriminability and thus AssA. 
As a result, recent MOT methods have achieved state-of-the-art performance on benchmark datasets3,4. Despite 
these gains, MOT still fails to fully handle the complexity and unpredictability of real-world scenarios. Heavy 
reliance on detector outputs leads to two entrenched issues that undermine long-term stability and reliability. 
The first is the detector-confidence dilemma5. Conventional TBD pipelines typically restrict their association to 
high-confidence detections. While this reduces errors from false positives (FPs) and improves precision, it also 
discards valid low-confidence detections, thereby degrading recall. Under occlusion or motion blur, such low-
confidence detections are excluded from the tracklets, inflating false negatives (FNs) and fragments. To address 
this issue, ByteTrack6 proposed a two-stage association strategy that leverages low-confidence detections. 
Although this substantially reduces FNs and improves tracking recall, it introduces a new challenge: admitting a 
large volume of low-confidence candidates increases the ambiguity between true objects and background noise, 
increasing the association complexity and risk of ID-switches (IDSW) driven by FPs. Ultimately, managing 
detection confidence is not merely a matter of tuning thresholds; it requires a principled approach to interpret 
and control the uncertainty of each detection. The second problem is the vulnerability of track lifecycle 
management7–9. Various MOT studies employ linear motion models, such as the Kalman filter, to predict the 
next position of an object and use a simple age-based management method that terminates the corresponding 
tracklet when the object has not been observed for a certain number of frames10,11. Age-based approaches may 
be effective for short occlusions or linear motion; however, they are vulnerable to long-term occlusions, abrupt 
direction changes, and nonlinear motion, which frequently occur in real-world environments. Consequently, 
tracklets are unnecessarily split into multiple fragments, and multiple identities are assigned to the same object; 
consequently, evaluation metrics such as IDF1 and HOTA12 are degraded.
1Interdisciplinary Program in IT-Bio Convergence System, Sunchon National University, Suncheon 57922, 
Korea. 2Department of Computer Engineering, Sunchon National University, Suncheon 57922, Korea. email: 
cbsim@scnu.ac.kr; shjung@scnu.ac.kr
OPEN
Scientific Reports |        (2026) 16:13571 
1
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports


## Page 2

We propose the use of Sentinel to address these problems. Sentinel departs from the conventional approach, 
which passively relies on detection outputs, and presents a paradigm that actively optimizes the tracking strategy 
around the uncertainty faced by each trajectory. To this end, we introduced two strategies. The first is CAA. 
CAA uses the confidence score of a detected object not only as a filtering criterion but also as information 
to regulate uncertainty in the association process. High-confidence detections are reliably linked to existing 
tracks through a strong association that combines appearance features and motion information, whereas low-
confidence detections are used only to recover lost tracks, considering the potential risk of FP. This differential 
association increases recall by leveraging low-confidence detections while effectively suppressing side effects 
such as IDSW. The second is a SBM. SBM dynamically manages a survival score by considering each track’s 
state and surrounding context instead of using a fixed frame count. When a tracklet becomes unobserved, SBM 
updates the survival score by integrating the track’s last observed position, velocity, and occlusion likelihood. 
When the score remains above a certain level, the track remains active, enabling immediate reassociation when 
the object reappears.
We demonstrated the superiority of the proposed Sentinel through experiments on standard benchmark 
datasets, such as MOT1713 MOT20, and DanceTrack14. The experimental results show that Sentinel achieved 
the highest performance on metrics other than Multiple Object Tracking Accuracy (MOTA) in MOT17 and 
MOT20 and attained remarkable performance on DanceTrack as well. These results indicate that compared 
with existing state-of-the-art trackers, Sentinel not only exhibits competitive overall tracking accuracy but also 
delivers consistent improvements in tracking continuity and identity preservation.
Related work
Reliability and uncertainty management in data-association methods
Data association is central to MOT because it assigns the objects detected in each frame to the correct 
trajectories along the time axis. Early MOT studies sought to solve association problems by using motion 
models. SORT15 uses the Kalman filter16 to predict object positions and adopts Intersection over Union (IoU) 
between the predicted bounding box and the actual detected bounding box as the sole association criterion. 
Although SORT’s approach is fast and efficient, it has the limitation that it easily misses the ID of the object 
when the object’s motion deviates from the prediction or when occlusion occurs. To overcome these limitations, 
subsequent studies have begun to exploit appearance information. DeepSORT improves AssA by extracting each 
object’s appearance features with a pretrained Re-ID model and combining them with motion information17, 
thereby mitigating the problem of IDSW that occur when visually similar objects are in close proximity. By 
contrast, many studies, including DeepSORT, have adopted a scheme that combines motion and appearance 
information with fixed weights18,19. As a result, the same combination ratio is applied to all scenes, revealing 
a limitation in which association is attempted uniformly without distinguishing between a situation in which 
an object is tracked stably for a long period and a situation immediately after occlusion in which the position 
is uncertain. Another axis of data association concerns how to trust and utilize the detector’s outputs. Early 
trackers adopted a conservative strategy of using only high-confidence detections to avoid FPs. This approach 
increased the precision of tracking but sacrificed recall by discarding detections that were actual objects yet 
measured with low confidence, and induced track fragments20–24. One study that brought about a change to 
this paradigm was ByteTrack. ByteTrack proposed a two-stage association strategy that does not discard low-
confidence detections but uses them to recover trajectories that are unmatched in the first association. This 
approach effectively addresses the missed-detection problem and dramatically improves MOT performance. 
However, ByteTrack’s uniform handling causes opposite side effects depending on the state of the trajectory. 
Stable trajectories induce unnecessary associations with background noise, thereby increasing the risk of identity 
switching. Unstable trajectories immediately before disappearance may fail to provide a robust association in 
a timely manner, leading to premature termination. Recent studies have also attempted to address detection 
and association challenges from broader perspectives. Few-shot object detection via class encoding and 
multi-target decoding25 addresses detection reliability under limited supervision, and pose-aware association 
methods such as PB-MOT26 demonstrate that geometric cues can enhance 3D multi-object tracking. However, 
these approaches focus on improving specific components and do not directly resolve the fundamental issue 
of adapting association strategies to per-trajectory uncertainty. Therefore, rather than simply adjusting the 
confidence threshold or relying on auxiliary modalities, an association strategy that dynamically diagnoses the 
per-trajectory uncertainty and adapts accordingly is required.
Occlusion handling and long-term tracking stability
Whereas data association focuses on frame-to-frame linkages, trajectory lifecycle management focuses 
on ensuring identity persistence over the entire time axis27,28. Long-term occlusion is the primary factor 
that undermines identity consistency, and its handling determines a tracker’s long-term stability. Lifecycle 
management commonly used in MOT is age-based termination29. When a tracker fails to find an object 
corresponding to a given trajectory for a specified number of frames, it completely deletes the trajectory from 
memory. Although this method is easy to implement, it can be fatal in long-occlusion scenarios. To mitigate 
this problem, auxiliary techniques, such as Camera Motion Compensation (CMC) and Trajectory Interpolation, 
have been proposed30–32. Occlusion handling has also been investigated in autonomous multi-agent systems, 
including ground vehicle tracking in wireless motion capture environments33 and UAV tracking in low-altitude 
airspace34. These studies provide complementary perspectives on trajectory survival and identity continuity that 
may inform pedestrian tracking research. However, these techniques are often confined to specific scenarios or 
applied uniformly without a fundamental diagnosis of the cause of trajectory loss; thus, they do not provide a 
general solution. More recently, trackers have partially compensated for the drawbacks of age-based termination 
by leveraging low-confidence detections to provide opportunities for recovering lost trajectories. Nevertheless, 
Scientific Reports |        (2026) 16:13571 
2
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 3

they still remain passive schemes that wait for matching until a trajectory is terminated, lacking a mechanism 
that diagnoses the trajectory’s risk state in advance and responds proactively.
Proposed method
Existing tracking methodologies have limitations in that they either use fixed association rules based on detection 
confidence or manage all trajectories using identical termination rules35. We present a paradigm that selectively 
utilizes detection information centered on the state and uncertainty of each trajectory and actively manages the 
lifecycle of trajectories by leveraging two components: CAA and SBM.
CAA
Existing trackers calculate data-association costs by combining the appearance and motion information with 
fixed weights. This static weight approach evaluates all trajectories and situations using the same criteria; thus, 
it fails to reflect the individual circumstances and uncertainties faced by each trajectory. Nevertheless, when a 
single association rule is uniformly applied, IDSW frequently occurs when objects with similar appearances are 
in close proximity, as shown in Fig. 1(a).
To address this issue, we propose CAA. The core of CAA is to diagnose the state of each trajectory in real time 
and dynamically adjust the weights of the data-association cost function, as shown in Fig. 1(b). CAA classifies 
the state of trajectories into three categories: Confident, Critical, and Uncertain, based on the information 
accumulated during the lifecycle of each trajectory, as expressed in Eq. (1).
	
st
i =
{
Confident
if hitt
i ≥τc ∧¯pt
i > θc,
Critical
if misst
i ≥τm ∨¯pt
i < θm,
Uncertain
otherwise

(1)
In Eq. (1), state is determined by synthesizing the number of consecutive tracking successes and failures of the 
corresponding trajectory and the recent confidence score. The Confident state is assigned when both of the 
following conditions are satisfied: The number of consecutive tracking successes hitt
i of trajectory imust be 
equal to or greater than the threshold τc, and the average detection confidence ¯pt
i must exceed the threshold θc. 
Trajectories in this state are assumed to have a very high motion prediction accuracy when using the Kalman 
filter. The Critical state is entered when one of the following conditions is satisfied: This occurs when the number 
of consecutive tracking failures misst
i of trajectory i is equal to or greater than the threshold τm or when 
′p
t
i is 
below the threshold θm. This indicates a state with a high risk of termination, where the object is in a long-term 
occlusion state or the detector fails to stably detect the object. An Uncertain state corresponds to all trajectories 
that do not belong to the Confident or Critical states. It includes newly generated trajectories or trajectories 
experiencing intermittent tracking failures and is the most common state.
The dynamic weighted association cost according to the trajectory state is expressed in Eq. (2).
	
Cij = ωiou

st
i

diou
ij
+ ωapp

st
i

dapp
ij
+ ωangdang
ij
+ ωconfdconf
i
diou
ij
= 1 −IoU (bi, bj)
dapp
ij
= 1 −cos (fi, fj)
dang
ij
= 1
4
4

k=1
arccos (clip (⟨vi,k, uij,k⟩, −1, 1))
π
dconf
i
=

∼p
t
i −pt
i

∼p
t
i = 2pt−1
i
−pt−2
i

(2)
In Eq. (2), the association cost Cij is defined as the weighted sum of the four terms. The IoU-based position 
mismatch term diou
ij reflects the lack of overlap between the predicted bounding box bi and candidate bj as 
a penalty. The appearance-mismatch term dapp
ij  represents the appearance difference based on the cosine 
similarity between the Re-ID embeddings fi and fj. The movement direction consistency term dang
ij  evaluates 
the motion direction consistency by normalizing the angle between the recent trajectory movement direction 
Fig. 1.  Process of resolving IDSW through dynamic association strategy of confidence-aware association.
 
Scientific Reports |        (2026) 16:13571 
3
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 4

and the vector connecting the predicted position and the actual observed position in the current frame. vi,k is 
the estimated movement direction vector in the recent k-th interval of trajectory i, uij,k is the vector pointing 
to the position of the current frame prediction candidate j, and clipis an operation that restricts the inner 
product value to [−1, 1]. The confidence fluctuation term dconf
i
measures the difference between the linearly 
extrapolated confidence ¯pt
i and current confidence pt
i, where pt
i is the detection confidence associated with 
trajectory i at frame t. Because this term is independent of the candidate j, it is applied uniformly to all 
candidate associations for trajectory i, effectively modulating the overall association willingness based on the 
temporal stability of detections. This regularization prevents the dynamic weighting mechanism from switching 
rapidly between association modes due to transient detection failures, thereby maintaining temporally stable 
state transitions. The diou weight ωiou and the dapp weight ωapp are applied variably according to st
i, while the 
weights ωang and ωconf for dang and dconf are set as fixed constants independent of state since they are auxiliary 
terms for search constraint and stabilization. The Confident state increases the weight of the IoU distance and 
decreases the weight of the appearance distance, because the reliability of the position prediction is high. This 
prevents IDSW by ensuring that, even if other objects with similar appearances appear nearby, candidates that 
deviate significantly from the predicted position are not associated. The Critical state reduces the reliability of 
the position information because the prediction error of the Kalman filter likely accumulates when it is not 
observed for a long period. Instead, because the validity of the last observed appearance features is maintained, 
the weight of the IoU distance is decreased and the weight of the appearance distance is increased to search 
a wider area and increase the probability of detecting objects with similar appearances. The Uncertain state 
performs standard association by considering the position and appearance information in a balanced manner. 
State-dependent weight adjustment directly reflects the uncertainty of each trajectory in the association process, 
thereby prioritizing ID preservation in the Confident state and expanding reconnection opportunities in the 
Critical state to enhance overall tracking performance.
SBM
Trajectory lifecycle management in MOT universally relies on age-based methods that terminate trajectories 
that have not been observed for a specific period. This passive approach reveals the fundamental vulnerabilities 
in long-term occlusion situations36. When an object is occluded by other objects or crowds and reappears, it 
commits the critical error of prematurely terminating the corresponding trajectory and assigning a new ID to 
the reappearing object. This causes unnecessary track fragmentation, as shown in Fig. 2 (a), and is a major cause 
of the degradation of key metrics such as IDF1. To overcome these limitations, we propose an SBM that actively 
rescues trajectories at risk of termination. SBM is an active hypothesis verification mechanism that departs 
from the existing paradigm of simply managing trajectories by survival time. Instead, it establishes survival 
hypotheses for each trajectory and statistically verifies them using low-confidence detection information. In 
other words, SBM establishes the hypothesis that a lost trajectory still exists within the scene and extends the 
life of the trajectory by discovering the most likely candidate from the low-confidence detection candidate pool. 
Fig. 2.  Response to long-term occlusion and securing trajectory continuity through survival boosting 
mechanism.
 
Scientific Reports |        (2026) 16:13571 
4
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 5

The first step in SBM is to quantify the uncertainty and termination risks of the lost trajectories. Therefore, we 
introduce a state variable D that explicitly models the reconnection necessity of the trajectories, as shown in 
Eq. (3).
	
Dt
i = max
(
Dmin, min(misst
i
τD
, 1)
)

(3)
misst
i represents the number of frames in which trajectory i has consecutively failed to associate up to frame 
t, and τD denotes the reference number of frames at which D reaches its maximum value. The lower bound of 
D is set to Dmin(> 0) and the upper bound to 1. When a trajectory fails to associate and misst
i accumulates, Dt
i 
increases linearly, and when successfully connected with a candidate object, misst
i is reset to 0 and Dt
i decreases. 
Because this value is re-evaluated for every frame, it can respond sensitively to dynamic situational changes 
such as abrupt scene changes, crowd congestion, and occlusion. Dmin > 0 serves as a safety margin. Linear 
prediction models such as the Kalman filter are effective in stationary or constant-velocity motion sections; 
however, it is easy to overtrust the prediction in sections where nonlinear movements such as sudden stops 
or sharp turns occur37. If D = 0 were allowed, it would indicate absolute trust in the prediction model, which 
would weaken the alternative hypothesis search and pose a high risk that accumulated detection failures would 
eventually lead to ID fragmentation. Therefore, the positive lower bound maintains a minimum alert state in 
the tracker, continuing the alternative hypothesis search even in stable tracking sections, thereby improving 
resilience in situations where the prediction fails. After diagnosing the risk level of trajectories through D, SBM 
defines the possibility that a low-confidence detection candidate j is the same object as the lost trajectory i as a 
survival hypothesis and verifies it by quantifying it as a survival score Sij. Sij is calculated as the weighted sum 
of spatial similarity IoUb, appearance similarity cos(fi, fj), and kinematic constraint Πij, and dynamically 
adjusts the weight ω of each term according to D as shown in Eq. (4). Specifically, as Dt
i increases, indicating 
prolonged occlusion, the emphasis shifts from position-based cues to appearance-based cues, reflecting the 
increased positional uncertainty.
	
Sij = ωiou
(
Dt
i
)
IoU b (i, j) + ωapp
(
Dt
i
)
cos (fi, fj) + ωmov
(
Dt
i
) ∏
ij
(4)
The first component, IoUb, is expressed in Eq. (5).
	
IoU b (i, j) = IoU

expand

bt
i, βt
i

, bj

βt
i = β0 + κDt
i

(5)
IoU b is a spatial similarity metric for compensating for the prediction uncertainty of the Kalman filter that 
occurs in long-term occlusion situations. The standard IoU is effective when the object movement is linear and 
the occlusion is short; however, when a trajectory is not observed for a long time, the state covariance of the 
Kalman filter increases, and the position accuracy of the predicted bounding box bt
i deteriorates. In this state, 
excluding potential reconnection candidates solely because the overlap between the predicted position and the 
actual detection region bj is small becomes a major cause of tracking failure. To solve this problem, IoUb forms 
a flexible search gate that accommodates the prediction uncertainty by calculating IoU after expanding both 
the predicted and detection bounding boxes by the same ratio. The expansion ratio βt
i increases linearly in 
proportion to Dt
i. This approximation models the possibility that the object deviates further from the predicted 
position as the loss period increases. β0 is the basic expansion rate that compensates for the minimum prediction 
error that can occur even in short-term occlusion situations, and κ is a hyperparameter that controls the rate at 
which uncertainty increases over time. Consequently, IoUb plays the role of maximizing the research success 
rate of lost trajectories by adaptively adjusting the search area according to the state of the trajectory.
The second component, cos(fi, fj), was measured as the cosine similarity between the appearance feature 
embeddings extracted using the Re-ID model. fi represents the appearance feature vector when trajectory i 
was last observed and fj is the feature vector of low-confidence detection candidate j. ByteTrack applies low-
confidence detections in the same manner to all unmatched trajectories that were missed in the first matching 
stage, thereby increasing the risk of false associations with background noise, even for stable trajectories. In 
contrast, SBM is activated only for trajectories in the Critical state and utilizes appearance similarity as a core 
cue for survival hypothesis verification. This state-dependent weight adjustment expands the reassociation 
opportunities while suppressing false associations compared with ByteTrack’s static association method. 
Particularly, in conditions where multiple objects with similar appearances exist, appearance information 
becomes a decisive cue that resolves association ambiguity, which is difficult to address using spatial cues alone. 
Only candidates for which Sij exceeds the predefined threshold θ pass the first validity verification, and by 
verifying the survival hypothesis based on the last observed high-confidence appearance information, confusion 
with incorrect low-confidence background noise or other objects is prevented.
The third component, Πij, is as shown in Eq. (6). Πij operates as a constraint that evaluates the relationship 
between the predicted position of track i and the observed position of candidate j to filter out associations that 
are physically impossible or have remarkably low plausibility in advance. Even if the appearance is similar, if an 
object has moved a distance that is physically difficult to reach within a single frame, it is highly likely to have 
an incorrect association. Πij determines whether it is within a realistic motion range based on the Euclidean 
distance between the observed center point cj and the predicted center point ci, and can include normalization 
tailored to scene-specific motion limits such as previous velocity or the maximum speed of pedestrians. At this 
Scientific Reports |        (2026) 16:13571 
5
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 6

time, Πij is a scalar gate with a range of [0,1], where a value of 0 means candidate j is physically excluded for 
track i, and a value greater than 0 maintains it as an association candidate. Furthermore, Πij is directly reflected 
as the motion plausibility term of Sij and is combined with spatial proximity and appearance similarity through 
a state-dependent weighted sum.
	

ij = max(0, 1 −||cj −ci||
dmax
)
cj =
x1j + x2j
2
, y1j + y2j
2
T
ci = [xi, yi]T

(6)
The identified low-confidence candidate j∗ is not matched immediately but undergoes a selective candidate 
promotion procedure to prevent damage to global optimality owing to greedy decisions. First, the first validity 
is verified by confirming whether the calculated highest survival score Sij∗ exceeds θ, thereby blocking 
indiscriminate promotion of implausible candidates. The confidence scores of the candidates that passed 
verification were adjusted using Eq. (7).
	
p+
j∗= min (
1, pj∗+ µ1 + µ2Dt
i
)

(7)
µ1 is a static confidence correction term, and µ2Dt
i operates as a dynamic correction term proportional to 
the trajectory’s disappearance period. Thus, the disappearance risk is lowered with priority while adjusting the 
trade-off with the FP risk within a limited range. Only when the elevated score p+
j∗ satisfies the high-confidence 
criterion is candidate j∗ incorporated into the high-confidence candidate group and subsequently competes for 
final matching with equal qualification to other high-confidence detections in the state-dependent association 
stage of CAA.
Pipeline
Sentinel operates according to the procedure shown in Fig. 3 and Algorithm 1: When the current frame is 
provided, the CMC is applied to reduce the prediction errors caused by global motion. The trajectories from the 
previous frame predict the current object state using the Kalman filter, and the detection results are separated 
into high-confidence and low-confidence sets according to the confidence criteria. The state of each trajectory 
is classified as Confident, Critical, or Uncertain using the CAA. The classification process is performed by 
comprehensively analyzing the number of consecutive tracking successes, the number of consecutive tracking 
failures, and the recent average confidence. The results are utilized as criteria for adjusting the weights of 
association costs and determining whether to activate SBM. At this time, SBM is applied to trajectories 
classified as Critical. SBM searches for candidates associated with Critical trajectories within the low-confidence 
detection set, selects valid candidates, adjusts the confidence scores upward, and then includes them in the 
final detection candidate group. By contrast, trajectories in the Confident and Uncertain states proceed to the 
next association stage without going through SBM. In the CAA-Weighted Association stage, an association is 
performed between the final detection candidate group and all trajectories whose states have been classified. 
The association cost is calculated using a cost function that is dynamically weighted according to the CAA state 
of each trajectory. Confident trajectories prioritize position information, whereas Critical trajectories prioritize 
appearance information. When the association is complete, the matched trajectories update the Kalman filter 
state, unassociated detections are initialized as new trajectories, and long-term unobserved trajectories are 
removed according to the lifetime policy.
Fig. 3.  Sentinel pipeline overview.
 
Scientific Reports |        (2026) 16:13571 
6
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 7

Experimental and results
Datasets
We conducted experiments on three standard benchmark datasets—MOT17, MOT20, and DanceTrack—to 
validate the performance of Sentinel. MOT17 is a standard benchmark consisting of seven training and seven 
test sequences that include diverse lighting conditions, camera movements, and pedestrian densities, and it plays 
a key role in evaluating the overall robustness and generalization performance of algorithms. MOT20 focuses 
on crowded pedestrian environments and provides scenarios in which severe interobject occlusions frequently 
occur. Such environments present extreme conditions in which trackers are prone to cause IDSW. DanceTrack 
poses various challenges to existing pedestrian datasets. It is characterized by dancers with similar appearances 
exhibiting nonlinear and unpredictable movements, which invalidates the assumptions of linear motion models 
such as the Kalman filter and creates an environment where appearance similarity is maximized.
Metric
We used standard evaluation metrics in the MOT field to comprehensively evaluate the performance of 
Sentinel. As primary metrics, we adopted MOTA, IDF1, and HOTA to quantitatively analyze the various 
aspects of tracking performance. MOTA is a traditional metric that measures tracking accuracy based on FP, 
FN, and IDSW. It is highly dependent on detection performance and is useful for identifying the basic error 
level of a tracker. However, it has the limitation of placing greater weight on detection accuracy rather than 
on association quality. IDF1 focuses on evaluating ID preservation performance. It measures how long each 
trajectory consistently maintains the correct ID, thereby demonstrating the effectiveness of the proposed CAA 
and SBM in preventing trajectory fragmentation and suppressing IDSW in long-term occlusions. HOTA has 
recently been recognized as the most balanced evaluation metric. It explicitly separates and calculates detection 
and association accuracy and derives the final score through the geometric mean of the two. This allowed for 
an independent yet comprehensive evaluation of the quality of detection and association, showing the highest 
correlation with human visual assessment.
Implementation details
For object detection, we adopted YOLOX-X38, which is widely used in MOT research. The detector was 
pretrained on the COCO dataset and the hyperparameters were optimized for the training dataset of each 
benchmark. For appearance feature extraction, we used SBS5039 from the FastRe-ID framework. The appearance 
feature extractor was pretrained on each dataset, and the default settings of the framework were used. During the 
tracking process, we utilized both the standard Kalman filter and the CMC to improve the prediction accuracy 
of the linear motion model. The cost matrix for data association was calculated using the weighted summation 
of four components: IoU, cosine, confidence, and angular distance, and was dynamically adjusted. To find the 
Algorithm 1.  Sentinel tracking pipeline.
 
Scientific Reports |        (2026) 16:13571 
7
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 8

optimal matching pairs, we used a strategy of sequentially connecting clear pairs through an iterative allocation 
method that starts with an initial threshold and then decreases it. The experimental setup is listed in Table 1.
Experimental results
Table 2 shows that Sentinel achieved overall superior performance on the MOT17 test dataset. It recorded 66.0 
in HOTA, achieving the highest score alongside PIA2, and a competitive score of 80.3 in MOTA, confirming 
its excellent ability to manage basic tracking errors. Notably, it achieved the best performance for IDF1, 
Mostly Tracked (MT), and Recall (Rcll), which are directly related to ID preservation and long-term stability, 
and recorded the lowest number of IDSW. The highest Rcll is the result of effectively utilizing low-confidence 
detection, which differs from ByteTrack’s approach of uniformly associating all low-confidence candidates. 
ByteTrack attempts to associate all candidates without a state distinction, which leads to numerous IDSW 
owing to associations with background noise or incorrect objects. In contrast, SBM selectively utilizes low-
confidence detection only for Critical-state trajectories immediately before loss to recover the trajectories. This 
approach, which minimizes side effects from unnecessary association attempts and reduces FNs, reduces IDSW 
by approximately 25% and improves IDF1 by 3.1% compared with ByteTrack. Furthermore, CAA’s dynamic 
association strategy played a crucial role in minimizing IDSW. Trackers such as StrongSORT and BOTSORT use 
a static association method that combines motion and appearance information with fixed weights. Although this 
method is effective in stable tracking situations, it has limitations in situations with high positional prediction 
uncertainty, such as immediately after occlusion. CAA diagnoses the trajectory state in real time, increasing the 
weight of motion information in the Confident state to conservatively suppress IDSW and increasing the weight 
of appearance information in the Critical state to enable a broader search. This ability to dynamically optimize the 
association strategy according to the situation enables a more robust handling of various environmental changes 
compared to trackers that rely on fixed rules, leading to the lowest IDSW. These improvements in IDSW, MT, 
and IDF1 collectively indicate suppression of track fragmentation. In contrast to ByteTrack, which accumulates 
fragmentation errors due to uniform low-confidence associations, Sentinel’s selective candidate promotion 
through SBM prevents unnecessary trajectory splits while CAA’s state-dependent weighting maintains stable 
identity assignment.
Table 3 presents the experimental results for the MOT20 dataset. Sentinel achieved the best performance 
with a HOTA of 65.6, an IDF1 of 81.0, and recorded the lowest number of IDSW at 920. In addition, MT and 
Rcll exhibited the best performance. This proves that individual identities are maintained most stably, even in 
extreme situations where objects overlap and are difficult to identify54. The excellent performance of Sentinel 
is attributed to overcoming the limitations in trajectory lifecycle management shown by existing trackers in 
extreme crowding and long-term occlusion situations, which are the core challenges of MOT20. Most trackers 
Method
MOTA (%)
IDF1 (%)
HOTA (%)
MT (%)
Rcll (%)
IDSW
EnhanceCenter40
70.4
66.3
55.1
38.9
76.4
-
BUSCA41
78.6
79.2
63.9
48.5
83.2
1,428
MAA42
79.4
75.9
62.0
57.6
86.2
1,452
RTU + +43
79.5
79.1
63.9
55.3
85.0
1,302
StrongSORT++
79.6
79.5
64.4
53.6
84.7
1,194
RAP-SORT44
80.0
79.4
64.4
-
-
-
ConfTrack45
80.0
81.2
65.4
58.7
87.7
1,155
REAL-SORT46
80.1
79.1
64.7
-
-
-
BoTSORT
80.5
80.2
65.0
54.4
84.8
1,212
ByteTrack
80.6
78.9
63.6
57.6
87.0
1,239
UCMCTrack
80.6
81.0
65.7
58.9
87.3
1,689
SparseTrack47
81.0
80.1
65.1
54.6
85.5
1,170
StrongTBD
81.6
80.8
65.6
55.7
86.0
954
PIA248
82.2
81.1
66.0
57.3
87.6
1,026
Sentinel
80.3
82.0
66.0
61.1
88.3
921
Table 2.  Performance comparison of Sentinel against state-of-the-art trackers on MOT17 test set.
 
Hardware Specifications
Software Versions
CPU
Intel Core i9-10900 K
Operating system
Ubuntu Linux 20.04.3 LTS (https://ubuntu.com)
Graphics card
NVIDIA GeForce RTX 3090
Programming language
Python 3.9.7 (https://www.python.org)
SSD
Samsung SSD 980 PRO 1 TB
GPGPU
CUDA 11.4.r11.4 (https://developer.nvidia.com/cuda-toolkit)
RAM
Samsung DDR5-4800 64GB
Deep neural network library
cuDNN 8.6.0 (https://developer.nvidia.com/cudnn)
Deep learning framework
PyTorch 1.12.1 (https://pytorch.org)
Table 1.  Hardware specifications and software versions.
 
Scientific Reports |        (2026) 16:13571 
8
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 9

use age-based termination methods that cause trajectory fragmentation when objects are occluded by crowds 
for several seconds or longer. For example, ImprAsso and PIA2 focus on optimizing the association matching 
process and securing association robustness through the aggregation of past information, respectively. However, 
their trajectory lifecycle itself relies on age-based management, making them fundamentally vulnerable to long-
term occlusion. By contrast, SBM, instead of passively waiting for termination when a trajectory disappears, 
establishes a survival hypothesis and actively verifies survival through low-confidence detections. This is an active 
rescue mechanism that probes the survival possibility of trajectories without relying on fixed time thresholds 
and is a factor that prevents errors of prematurely terminating trajectories owing to long-term occlusion and 
suppressed trajectory fragmentation, which other trackers commit. This is also different from the reactive 
approach of OCSORT, which retrospectively corrects the state of the reconnected trajectories after occlusion. 
Whereas OCSORT focuses on recovering already broken trajectories, SBM takes a preventive approach that 
utilizes low-confidence detection to prevent situations where trajectories break first, thereby securing high ID 
continuity55. The highest HOTA was attributed to the synergistic effect of SBM and CAA. When SBM robustly 
maintains trajectory life in long-term occlusion situations, CAA dynamically lowers the weight of motion 
information for objects in Uncertain states emerging from occlusion and relies on appearance information to 
stably reconnect them. This combination achieved high accuracy in both detection and association aspects and 
is why Sentinel is significantly ahead in core indicators of tracking association quality, such as HOTA, IDF1, and 
IDSW, despite ImprAsso recording the highest MOTA score. The combination of the lowest IDSW and highest 
MT further demonstrates that Sentinel suppresses track fragmentation even under extreme crowding, validating 
the preventive design of SBM over conventional reactive approaches.
Table 4 lists the experimental results for the DanceTrack test dataset. Sentinel achieved the best performance, 
recording the highest performance in all metrics and surpassing all the compared trackers. This performance 
superiority stems from the adaptive association strategy of Sentinel, which responds to situations in which the 
reliability of information fluctuates dynamically. Trackers such as MotionTrack and OCSORT rely heavily on 
Kalman-filter-based linear motion prediction. However, in the face of sudden directional changes or vigorous 
Method
MOTA (%)
IDF1 (%)
HOTA (%)
AssA (%)
GTR52
84.7
48.0
50.3
31.9
ByteTrack
89.9
47.7
53.9
32.1
FineTrack53
89.9
52.7
59.8
38.5
FCG56
89.9
48.7
46.5
29.9
StrongSORT++
91.1
55.6
55.2
38.6
MotionTrack
91.3
58.2
58.6
41.7
GHOST
91.3
56.7
57.7
39.8
CBIoU57
91.6
60.6
61.6
45.4
BASE58
91.7
56.4
-
-
OCSORT
92.0
55.1
54.6
38.3
CMTrack59
92.5
61.8
63.3
46.4
Sentinel
93.4
62.8
65.7
47.5
Table 4.  Performance comparison on DanceTrack test set.
 
Method
MOTA (%)
IDF1 (%)
HOTA (%)
MT (%)
Rcll (%)
IDSW
EnhanceCenter
47.1
49.3
38.5
16.6
-
2,339
BUSCA
72.7
76.3
61.8
59.7
75.6
1,006
OCSORT
75.7
76.3
62.4
65.5
79.5
942
REAL-SORT
76.6
76.3
62.9
-
-
-
RAP-SORT
76.8
79.0
64.2
-
-
-
EscapeTrack49
77.4
80.5
64.8
70.9
83.5
1,061
ByteTrack
77.8
75.2
61.3
69.2
83.1
1,223
BoTSORT
77.8
77.5
63.3
70.2
82.8
1,313
GMMotion50
78.0
77.3
63.2
69.9
83.2
1,212
SparseTrack
78.1
77.6
63.5
70.0
83.3
1,120
MHO51
78.2
76.9
62.5
70.4
83.4
956
SuppTrack52
78.2
75.5
61.9
70.9
84.3
1,325
PIA2
78.5
79.0
64.7
69.2
83.5
1,023
ImprAsso53
78.6
78.8
64.6
70.8
84.0
992
Sentinel
77.3
81.0
65.6
70.9
84.3
920
Table 3.  Performance comparison of Sentinel against state-of-the-art trackers on MOT20 test set.
 
Scientific Reports |        (2026) 16:13571 
9
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 10

dance movements, these linear assumptions fail and directly lead to association errors. CBIoU uses a heuristic 
that expands the matching space by setting a buffer to compensate for this; however, it fails to resolve the 
fundamental modeling limitations. In contrast, CAA performs association by assigning a higher weight to 
appearance information when tracking failures of a trajectory accumulate and the reliability of the motion 
information is judged to be low. This ability to diagnose the trajectory state in real time and dynamically 
optimize the information utilization strategy is the key mechanism that overcomes the limitations that other 
trackers, which inherently rely on fixed rules, cannot overcome. In addition, models that focus on sophisticated 
appearance features, such as FineTrack and GHOST, encounter limitations in discriminability when dancers 
wearing similar costumes form groups or overlap. In these situations, Sentinel has a dual defense mechanism. 
First, when a dancer shows a stable trajectory for a moment, CAA conversely increases the weight of the motion 
information to prevent the ID from being transferred to other dancers with similar appearances nearby. Second, 
when frequent and long occlusions occur as dancers form groups, SBM actively rescues trajectories in danger of 
termination through hypothesis verification using low-confidence detection, preventing unnecessary trajectory 
fragmentation60. It is noteworthy that Sentinel achieved the highest MOTA score of 93.4, even though all the 
comparison trackers, except GTR, used the same detector. The highest MOTA was a remarkable achievement, 
considering that it recorded a relatively low MOTA compared with the other trackers in MOT17 and MOT20. 
This superiority originates from the interaction between DanceTrack’s unique characteristics and Sentinel. 
The unpredictable movements and frequent occlusions of DanceTrack are the main causes of existing trackers 
prematurely terminating trajectories and accumulating numerous FN errors. By contrast, SBM reduces the FN 
that frequently occurs in other trackers by actively utilizing low-confidence detection information to recover 
trajectories in danger of loss. In other words, the reduction in FN made a decisive contribution to MOTA 
improvement. Simultaneously, CAA suppresses IDSW, thus reducing other major error items in the MOTA. In 
conclusion, the high MOTA proved that Sentinel achieved additional performance in reducing tracking-specific 
errors while responding to specific challenges in the dataset.
Table 5 presents the stepwise application effects of CAA and SBM. After applying CAA to each benchmark, 
HOTA commonly increased, which is interpreted as a result of the state-awareness-based association strategy 
that structurally reduces false connections in crowded sections and improves association quality. Subsequently, 
when SBM was added, IDF1 consistently increased, which was explained by the suppression of disconnections in 
the reconnection stage after non-observation, thereby strengthening ID preservation. In MOT17, even amid the 
diversity of scene conditions, sequential improvement is observed, where CAA reduces association ambiguity 
in general scenes to stabilize the HOTA baseline and SBM-reinforced ID preservation by alleviating residual 
disconnections in intermittent occlusion and reappearance sections. In the MOT20, where the frequency of 
crowding and long-term occlusion is high, reconnection stability determines success or failure. CAA suppresses 
false connections between nearby objects to solidify the association quality, and SBM is effective in reducing 
fragmentation by alleviating critical situations occurring at the boundary before and after trajectory loss. In 
DanceTrack, nonlinear motion and high appearance similarity coexist, resulting in frequent sections where 
the reliability of linear motion-based prediction is low. Under these conditions, CAA preemptively improved 
HOTA by refining ambiguous associations through state-dependent weight adjustment, and IDF1 also increased 
concurrently. Subsequently, when SBM was combined, the disconnections in the reappearance section after 
occlusion decreased, leading to an additional increase in IDF1, and HOTA improved slightly. To evaluate real-
time applicability, FPS measurements are reported following standard MOT evaluation protocols. Only tracking 
components excluding detection time were measured, and the average FPS over three independent runs after a 
10-frame warm-up is presented. Applying CAA reduces FPS from 126.1 to 100.5 on MOT17, from 23.8 to 17.7 
on MOT20, and from 622.3 to 588.9 on DanceTrack. This reduction is attributed to real-time state diagnosis that 
classifies each trajectory into Confident, Critical, or Uncertain states, as well as dynamic weight computation for 
association costs. The relatively smaller reduction on DanceTrack compared to pedestrian-dense benchmarks 
is attributed to fewer trajectories per frame, which reduces the cumulative cost of per-trajectory state diagnosis. 
When SBM is added, noticeable additional reductions are observed across all datasets. MOT17 decreases from 
100.5 to 81.5 FPS, MOT20 from 17.7 to 14.1 FPS, and DanceTrack from 588.9 to 539.9 FPS. This overhead arises 
from the survival hypothesis verification process, which requires computing spatial similarity with expanded 
bounding boxes, appearance similarity through Re-ID embeddings, and kinematic constraints for candidate 
Dataset
CAA
SBM
IDF1 (%)
HOTA (%)
FPS
MOT17-val
86.63
69.90
126.1
✔
87.13
70.44
100.5
✔
✔
88.29
70.87
81.5
MOT20-val
88.34
68.20
23.8
✔
89.49
68.78
17.7
✔
✔
89.78
69.11
14.1
DanceTrack-val
65.20
62.12
622.3
✔
67.45
63.64
588.9
✔
✔
67.76
63.89
539.9
Table 5.  Ablation study on validation sets of MOT17, MOT20, and DanceTrack to analyze the contribution of 
each component of Sentinel.
 
Scientific Reports |        (2026) 16:13571 
10
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 11

evaluation. Although SBM is primarily activated for Critical-state trajectories, candidate search within the 
low-confidence detection pool and survival score computation introduce measurable costs across all datasets. 
The relatively smaller reduction on DanceTrack is attributed to fewer objects per frame compared to MOT17 
and MOT20, and the characteristics of dance scenarios where occlusions are resolved within relatively short 
durations, resulting in a lower proportion of trajectories reaching the Critical state. Despite these computational 
costs, Sentinel maintains real-time performance suitable for practical applications. Specifically, 81.5 FPS on 
MOT17 and 539.9 FPS on DanceTrack comfortably exceed real-time requirements, while MOT20’s 14.1 FPS 
remains reasonable given its extreme crowd density where even baseline tracking operates at only 23.8 FPS. In 
summary, CAA serves as a foundational element that systematically elevates association accuracy through state-
aware cost weighting, and SBM acts as a complementary element that reinforces ID preservation in long-term 
occlusion and re-entry sections. These two components work synergistically to produce consistent increases in 
HOTA and IDF1 across all three datasets, with the performance gains justifying the computational overhead in 
scenarios where identity preservation is critical.
Table 6 presents the sensitivity analysis of CAA and SBM hyperparameters on the DanceTrack validation set. 
For CAA, three parameters governing state classification were examined. τc achieved optimal performance at 45. 
A value of 40 caused premature Confident state transitions before reliable motion predictions were established, 
whereas 50 delayed the transition unnecessarily. θc showed optimal performance at 0.70, whereas 0.65 classified 
low-confidence tracks as Confident, causing inappropriate weight application. θm achieved optimal performance 
at 0.75. A value of 0.7 triggered Critical transitions even with minor confidence drops, causing unnecessarily 
aggressive matching, whereas 0.8 delayed Critical transitions, resulting in late responses to problematic tracks. 
For SBM, τD showed stable performance across values of 1, 5, and 10, with marginal improvement at 10. β0 
achieved optimal results at 40, whereas 35 provided insufficient expansion ratio to compensate for baseline 
prediction errors caused by nonlinear motion. θ performed best at 0.95. A value of 0.90 increased incorrect 
matches due to the low survival score threshold, resulting in AssA dropping to 48.67, whereas 1.00 missed 
legitimate reconnection opportunities through overly strict verification, resulting in AssA dropping to 50.27.
Table 7 presents the sensitivity analysis results on the MOT17 validation set. For CAA, τc achieved optimal 
performance at a lower value of 2, as the predictable linear motion patterns of pedestrians allow Confident 
state transitions with shorter tracking histories. θc performed best at 0.80, higher than 0.75, indicating that 
higher appearance distinctiveness among pedestrians allows stricter criteria. θm showed optimal results at 0.65, 
where 0.6 triggered Critical transitions too frequently and 0.7 delayed the transitions. For SBM, τD achieved 
optimal performance at 20, higher than DanceTrack, as the linear motion of pedestrians maintains valid 
position predictions longer during occlusion, making gradual increase of D appropriate. β0 performed best at 
45, indicating that a wider baseline search region is required in crowded pedestrian environments. θ achieved 
optimal performance at 0.75, lower than DanceTrack’s 0.95, indicating that higher appearance diversity among 
pedestrians allows permissive verification to expand reconnection opportunities. The difference in optimal 
values across datasets indicates that Sentinel can adaptively respond to diverse environmental characteristics; 
Hyper
parameters
HOTA(%)
AssA(%)
IDF1 (%)
Hyper
parameters
HOTA(%)
AssA(%)
IDF1 (%)
CAA
τ c
3
70.85
74.60
88.26
SBM
τ D
15
69.82
72.77
86.61
4
70.86
74.61
88.26
25
70.78
74.66
87.99
2
70.87
74.62
88.29
20
70.87
74.62
88.29
θc
0.75
70.85
74.57
88.19
β0
40
70.86
74.62
88.28
0.80
70.87
74.62
88.29
45
70.87
74.62
88.29
θm
0.60
70.85
74.59
88.21
θ
0.70
70.25
73.65
87.22
0.70
70.86
74.62
88.28
0.80
70.79
74.21
87.68
0.65
70.87
74.62
88.29
0.75
70.87
74.62
88.29
Table 7.  Sensitivity analysis of CAA and SBM hyperparameters on the MOT17 validation set.
 
Hyper
parameters
HOTA(%)
AssA(%)
IDF1 (%)
Hyper
parameters
HOTA(%)
AssA(%)
IDF1 (%)
CAA
τ c
40
63.82
50.55
67.61
SBM
τ D
1
63.84
50.57
67.71
50
63.34
49.78
67.06
5
63.85
50.59
67.72
45
63.89
50.65
67.76
10
63.89
50.65
67.76
θc
0.65
63.47
50.09
67.42
β0
35
63.70
50.34
67.52
0.70
63.89
50.65
67.76
40
63.89
50.65
67.76
θm
0.70
63.09
49.25
66.58
θ
0.90
62.58
48.67
66.19
0.80
62.94
49.13
66.32
1.00
63.64
50.27
67.45
0.75
63.89
50.65
67.76
0.95
63.89
50.65
67.76
Table 6.  Sensitivity analysis of CAA and SBM hyperparameters on the DanceTrack validation set.
 
Scientific Reports |        (2026) 16:13571 
11
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 12

DanceTrack’s nonlinear motion and high appearance similarity require conservative state transitions and strict 
candidate verification, whereas MOT17’s predictable pedestrian dynamics permit faster state classification and 
more permissive reconnection criteria.
Table 8 presents the FP and FN changes when SBM is activated on the MOT20 validation set. With SBM 
enabled, FP increases from 15,696 to 16,968, representing an 8.1% increase, whereas FN decreases from 32,630 to 
30,000, representing an 8.1% reduction. Notably, the absolute FN reduction of 2,630 is approximately 2.07 times 
greater than the absolute FP increase of 1,272, indicating that SBM recovers more true objects than it incorrectly 
admits. This trade-off stems from the design principles of SBM. SBM explores low-confidence detections only 
for trajectories in the Critical state and restricts candidate acceptance through survival score threshold θ and 
selective promotion procedures. This conservative verification mechanism suppresses the FP increase to 8.1% 
while effectively reducing FN caused by long-term occlusion. In the extreme crowding environment of MOT20, 
detection misses are a primary cause of trajectory fragmentation. Consequently, FN reduction has a substantial 
impact on overall tracking quality. The improvements in IDF1 and HOTA observed in Table 5 when SBM is 
applied demonstrate that this FN reduction translates into enhanced ID preservation and association quality.
Figure 4 shows the change in AssA according to the change in the number of consecutive tracking failure 
tolerance frames, which is a hyperparameter of SBM. The X-axis represents the number of non-observation 
frames allowed until trajectory termination, and the y-axis represents AssA. As the tolerance increases, AssA 
increases gently and converges to approximately 50.66 in the range above 50 frames. This rising and converging 
tendency is attributed to the following factors. The cause of the increase in AssA was analyzed as the effect of three 
mechanisms. First, the survival window is expanded. Increasing tolerance allows trajectories to be maintained 
longer, increasing opportunities for survival hypothesis verification, and strengthening reconnection attempts. 
Second, the search area is adaptively expanded. As tolerance frame count increases, Dit increases linearly 
and expands the prediction box at the same ratio, absorbing the positional uncertainty caused by long-term 
occlusion and reducing the omission of potential reconnection opportunities. Third, a false-positive suppression 
mechanism exists. Candidates must pass, and even after passing, confidence is conservatively adjusted to 
compete fairly well with other candidates in the final association stage. This process effectively controls false 
connections with background noise caused by indiscriminate search expansion. Convergence above a specific 
frame is interpreted as an upper-limit effect formed by the data distribution and design constraints. Owing to 
the tendency for long-term occlusion duration to be resolved within approximately 2.5 s in DanceTrack, when 
tolerance is expanded to that level, the majority that can be recovered are already reconnected. In the subsequent 
range, the proportion of scene exit cases and trajectories with large appearance and motion drift increases, 
making the reconnection probability low, even when an extended search is applied. Internal constraints, such 
as clipping for safety, also gradually reduce marginal gains; therefore, the additional tolerance above a specific 
Fig. 4.  Performance analysis of AssA on the DanceTrack validation set according to variations in non-
observation tolerance frames.
 
SBM
FP
FN
Off
15,696
32,630
On
16,968
30,000
Table 8.  FP-FN trade-off analysis of SBM on MOT20 validation set.
 
Scientific Reports |        (2026) 16:13571 
12
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 13

frame is offset on average, flattening the curve. Consequently, as the marginal utility of the tolerance increment 
is exhausted, AssA approaches its practical upper limit.
Figure 5 demonstrates the improvement of the ID-related metrics using the state-dependent weight 
adjustment method compared with the static method. This performance improvement was attributed to the 
following two mechanisms. First, decision-making reflects the asymmetry of false connection costs. During the 
tracking process, incorrect high-confidence connections serially distort the cost matrix of subsequent frames, 
causing ID theft and serial IDSW, leading to near-irreversible losses. In contrast, temporary FN occurring 
from withholding associations with low-confidence candidates have fewer serial ripple effects, resulting in 
relatively small losses. The conservative candidate promotion of SBM linked with CAA exploits this asymmetry. 
That is, instead of immediately connecting candidates lacking confidence, by granting only fair competition 
qualifications to the high-confidence candidate group, it accepts the small cost of a short-term FN increase 
and maximizes the large benefit of long-term ID preservation. Second, matching stabilization is achieved by 
resolving joint ambiguity. In crowded environments, the reliability of both appearance and motion information 
deteriorates simultaneously, generating numerous similar-cost candidates within the cost matrix. CAA diagnoses 
the trajectory state in real time, dynamically redistributes the weights of each cost term, and expands the cost gap 
between the top and second-best candidates. This increases the decision margin of the Hungarian assignment, 
structurally suppressing the possibility of rank reversal due to minute noise or uncertainty, thereby reducing 
IDSW. In conclusion, the two mechanisms operate complementarily, functioning as a principle by which CAA 
stably maintains ID continuity, even in crowded situations.
Figure 6 demonstrates the performance improvement of SBM through a comparison with the existing 
two-stage matching. SBM significantly reduces FP and IDSW and improves HOTA and MT, demonstrating 
superiority in long-term tracking stability. This superior performance originates from its robust ability to cope 
with long-term occlusions and nonlinear motion. Existing two-stage matching attempts to uniformly associate 
low-confidence candidates, absorb background noise, or terminate trajectories with long-term occlusion owing 
to fixed termination rules, accumulating false positives. In contrast, SBM responds with a single strategy that 
expands the search area according to the situation while performing conservative verification; as the loss period 
lengthens, it progressively widens the search radius to secure connection pathways with objects reappearing 
after a long time. Simultaneously, the matching process after confidence boosting selectively passes only high-
confidence candidates, thereby blocking the influx of background noise. As a result, reconnection failures 
decrease and false connections are suppressed, leading to concurrent increases in HOTA and MT. The effect of 
SBM is maximized when combined with CAA’s state-dependent weight adjustment. Such adaptive cue fusion 
enables trajectories restored by SBM to be stably reconnected, even in Uncertain states, immediately after 
occlusion. In summary, the excellent performance of SBM originates from the synergy of search space expansion 
prepared for long-term occlusion, false connection suppression through conservative verification, and real-time 
weight redistribution by CAA. The organic combination of the two mechanisms structurally reduces FP and 
IDSW, resulting in improvements in HOTA and MT.
Figure 7 presents a qualitative comparison between the baseline tracker and Sentinel on DanceTrack, where 
nonlinear motion and high appearance similarity make ID preservation differences most visually apparent. 
In the baseline tracker, the target object is initially assigned ID 2 at Frame 32. However, when the object 
enters an occlusion state at Frame 94, the baseline tracker completely loses the trajectory. When the object 
reappears at Frame 101, the tracker fails to recognize it as the same object and assigns a new ID 12, causing 
track fragmentation. This phenomenon demonstrates the fundamental vulnerability of age-based termination 
Fig. 5.  Comparison of ID-related metrics on the DanceTrack validation set between static method and state-
dependent weight adjustment method.
 
Scientific Reports |        (2026) 16:13571 
13
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 14

methods that prematurely terminate trajectories under long-term occlusion. In contrast, Sentinel maintains a 
consistent ID 2 throughout the entire sequence. When the object enters an occlusion state, SBM establishes a 
survival hypothesis and actively searches for reconnection candidates within the low-confidence detection pool. 
When the object reappears, CAA dynamically increases the weight of appearance information for trajectories in 
the Critical state, enabling stable reconnection with the original ID. These qualitative results demonstrate that 
the synergistic operation of CAA and SBM effectively prevents unnecessary ID switches and preserves trajectory 
continuity even under challenging occlusion scenarios.
Conclusions
We proposed Sentinel, which dynamically optimizes tracking strategies centered on trajectory uncertainty to 
address the chronic limitations of MOT, namely, the detection confidence dilemma and trajectory extinction 
vulnerability. Sentinel overcomes the limitations of existing tracking approaches by using two core components: 
CAA and SBM. CAA diagnoses the state of each trajectory in real time and dynamically adjusts the weights of 
the association costs, thereby conservatively protecting stable trajectories and actively reconnecting trajectories 
at risk of loss to minimize IDSW. SBM departs from conventional passive age-based extinction rules and actively 
validates the survival hypothesis of lost trajectories through low-confidence detections, robustly maintaining 
trajectory continuity even in long-term occlusion situations. Through extensive experiments on the MOT17, 
MOT20, and DanceTrack datasets, Sentinel achieved superior performance in HOTA and IDF1, demonstrating 
its strength in identity preservation and association quality. While Sentinel shows slightly lower MOTA 
compared to some recent trackers such as PIA2 and StrongTBD, this trade-off aligns with its design philosophy of 
prioritizing long-term tracking continuity. However, the proposed approach has several limitations. CAA incurs 
increased computational costs due to real-time state diagnosis and dynamic weight calculation, and the optimal 
state classification thresholds vary depending on dataset characteristics, requiring hyperparameter re-tuning 
for new environments. SBM may increase FP due to its aggressive utilization of low-confidence detections, and 
its effectiveness can be limited in environments where the detector itself has low recall, as fewer candidates are 
available for survival hypothesis verification. Despite these limitations, Sentinel showed consistent performance 
superiority in IDF1, which indicates ID continuity, and HOTA, a comprehensive performance metric, in 
challenging scenarios with extreme crowding, long-term occlusions, and frequent irregular movements. In 
Fig. 6.  Comparison of long-term tracking stability on the DanceTrack validation set between SBM and 
existing two-stage association method.
 
Scientific Reports |        (2026) 16:13571 
14
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 15

conclusion, Sentinel presents a new paradigm that intelligently adjusts association and lifecycle management 
strategies by focusing on the intrinsic state of individual trajectories, elevating tracking robustness and accuracy 
in various real-world environments to the next level.
Data availability
The data supporting the findings of this study are publicly available. The datasets used in this study include 
MOT17 and MOT20 from the MOT Challenge repository, and the DanceTrack dataset. They can be accessed 
at the following URLs respectively: https://motchallenge.net/data/MOT17/, ​h​t​t​p​s​:​/​/​m​o​t​c​h​a​l​l​e​n​g​e​.​n​e​t​/​d​a​t​a​/​M​O​
T​2​0​/​, and https://github.com/DanceTrack/DanceTrack. The MOT Challenge datasets are provided under the 
Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license ​(​h​t​t​p​s​:​/​/​c​r​e​a​t​i​v​e​c​o​m​m​o​n​s​.​o​r​g​/​l​i​c​e​n​s​e​
s​/​b​y​-​n​c​-​s​a​/​3​.​0​/​)​, while the DanceTrack dataset is available for non-commercial research purposes. All usage of 
the data in this study complies with the terms of their respective licenses.
Received: 16 October 2025; Accepted: 9 March 2026
References
	 1.	 Fengwei, Y. & et al. Poi: Multiple object tracking with high performance detection and appearance feature. In European conference 
on computer vision. 36–42, (2016). https://doi.org/10.1007/978-3-319-48881-3_3
	 2.	 Bochinski, E., Eiselein, V. & Sikora, T. High-speed tracking-by-detection without using image information. In 14th IEEE international 
conference on advanced video and signal based surveillance. 1–6,. 1–6, (2017). https://doi.org/10.1109/AVSS.2017.8078516 (2017).
	 3.	 Yunhao, D. Strongsort: Make deepsort great again. IEEE Trans. Multimedia. 25, 8725–8737. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​M​M​.​2​0​2​3​.​3​
2​4​0​8​8​1​ (2023).
	 4.	 Nguyen, P., Quach, K. G., Kitani, K. & Luu, K. Type-to-Track: Retrieve Any Object via Prompt-based Tracking. Proceedings of the 
37th International Conference on Neural Information Processing Systems. 3205–3219. (2024).
Fig. 7.  Qualitative comparison of ID preservation under occlusion between baseline tracker and Sentinel on 
DanceTrack.
 
Scientific Reports |        (2026) 16:13571 
15
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 16

	 5.	 Liu, Y., Li, Y., Xu, D., Yang, Q. & Tao, W. Adaptive Kalman Filter with power transformation for online multi-object tracking. 
Multimedia Syst. 29 (3), 1231–1244. https://doi.org/10.1007/s00530-023-01052-7 (2023).
	 6.	 Zhang, Y. & et al. Bytetrack: Multi-object tracking by associating every detection box. European conference on computer vision. 
1–21. (2022). https://doi.org/10.1007/978-3-031-20047-2_1
	 7.	 Pang, Z. & et al. SimpleTrack: Understanding and Rethinking 3D Multi-object Tracking. European Conference on Computer Vision. 
680–696, (2023). https://doi.org/10.1007/978-3-031-25056-9_43
	 8.	 Chiu, H. et al. &. Probabilistic 3D Multi-Modal, Multi-Object Tracking for Autonomous Driving. In IEEE International Conference 
on Robotics and Automation. 14227–14233,. 14227–14233, (2021). https://doi.org/10.1109/ICRA48506.2021.9561754 (2021).
	 9.	 Stadler, D. & et al. Improving Multiple Pedestrian Tracking by Track Management and Occlusion Handling. In Proceedings of the 
IEEE/CVF Conference on Computer Vision and Pattern Recognition. 10958–10967, (2021). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​4​6​4​3​7​.​2​0​
2​1​.​0​1​0​8​1​
	10.	 Aharon, N. & et al. BoT-SORT: Robust Associations Multi-Pedestrian Tracking. arXiv preprint arXiv :220614651 (2022).
	11.	 Miah, M., Bilodeau, G. A., and Saunier, N. Learning data association for multi-object tracking using only coordinates.Pattern 
Recognition 160, (2025).
	12.	 Luiten, J. et al. Hota: A higher order metric for evaluating multi-object tracking. Int. J. Comput. Vis. 129, 548–578. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​0​0​7​/​s​1​1​2​6​3​-​0​2​0​-​0​1​3​7​5​-​2​ (2021).
	13.	 Milan, A., Leal-Taixé, L., Reid, I., Roth, S. & Schindler, K. MOT16: A benchmark for multi-object tracking. arXiv preprint 
arXiv:1603.00831 (2016).
	14.	 Sun, P. et al. Multi-object tracking in uniform appearance and diverse motion, In Proceedings of the IEEE/CVF conference on 
computer vision and pattern recognition. 20993–21002. (2022). https://doi.org/10.1109/CVPR52688.2022.02032
	15.	 Bewley, A., Ge, Z., Ott, L., Ramos, F. & Upcroft, B. Simple online and realtime tracking. In IEEE international conference on image 
processing. 3464–3468,. 3464–3468, (2016). https://doi.org/10.1109/ICIP.2016.7533003 (2016).
	16.	 Kalman, R. E. A new approach to linear filtering and prediction problems. J. Basic Eng. 82(1), 35–45. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​5​/​1​.​3​6​
6​2​5​5​2​ (1960).
	17.	 Wojke, N., Bewley, A. & Paulus, D. Simple online and realtime tracking with a deep association metric. IEEE Int. Conf. Image 
Process. https://doi.org/10.1109/ICIP.2017.8296962 (2017).
	18.	 Liu, H. et al. Improved DeepSORT algorithm based on multi-feature fusion. Appl. Syst. Innov. https://doi.org/10.3390/asi5030055 
(2022).
	19.	 Wang, Z., Zheng, L., Liu, Y., Li, Y. & Wang, S. Towards real-time multi-object tracking. In European conference on computer vision. 
107–122, (2020). https://doi.org/10.1007/978-3-030-58621-8_7
	20.	 Zhang, Y., Wang, C., Wang, X., Zeng, W. & Liu, W. FairMOT: On the fairness of detection and re-identification in multiple object 
tracking. Int. J. Comput. Vis. https://doi.org/10.1007/s11263-021-01513-4 (2021).
	21.	 Zhou, X., Koltun, V. & Krähenbühl, P. Tracking objects as points. Eur. Conf. Comput. Vis. 474 (490). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​9​7​
8​-​3​-​0​3​0​-​5​8​5​4​8​-​8​_​2​8​ (2020).
	22.	 Pang, J. & et al. Quasi-dense similarity learning for multiple object tracking. In Proceedings of the IEEE/CVF conference on computer 
vision and pattern recognition. 164–173, (2021). https://doi.org/10.1109/CVPR46437.2021.00023
	23.	 Wu, J. & et al. Track to detect and segment: An online multi-object tracker. In Proceedings of the IEEE/CVF conference on computer 
vision and pattern recognition. 12352–12361, (2021). https://doi.org/10.1109/CVPR46437.2021.01217
	24.	 Liu, Z. et al. Multi-object tracking by performing scene decomposition based on pseudo-depth. arXiv preprint arXiv:2306.05238 
(2023).
	25.	 Guo, X., Yang, H., Wei, M. & Zhang, Y. Few-shot object detection via class encoding and multi-target decoding. IET Cyber-Systems 
Rob. 5 (2), 218–226. https://doi.org/10.1049/csy2.12088 (2023).
	26.	 Pang, B., Xu, Y., Chen, J. & Li, L. P. B. M. O. T. Pose-aware Association Boosted Online 3D Multi-Object Tracking. In Proceedings 
of the IEEE/RSJ International Conference on Intelligent Robots and Systems. 14170–14177,. 14170–14177, (2025). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​
.​1​1​0​9​/​I​R​O​S​6​0​1​3​9​.​2​0​2​5​.​1​1​2​4​7​3​7​5​ (2025).
	27.	 Wang, G., Wang, Y., Zhang, H., Gu, R. & Hwang, J. N. Exploit the Connectivity: Multi-Object Tracking with TrackletNet. arXiv 
preprint arXiv:1811.07258 (2018).
	28.	 Pang, B. et al. Adopting Tubes to Track Multi-Object in a One-Step Training Model. Proceedings of the IEEE/CVF Conference on 
Computer Vision and Pattern Recognition. 6307–6317, (2020). https://doi.org/10.1109/CVPR42600.2020.00634
	29.	 Kefu, Y. I. et al. UCMCTrack: Multi-Object Tracking with Uniform Camera Motion Compensation. Proc. AAAI Conf. Artif. Intell. 
38(7), 6702–6710. https://doi.org/10.1609/aaai.v38i7.28493 (2024).
	30.	 Guo, X., Zheng, Y. & Wang, D. PMTrack: Multi-object Tracking with Motion-Aware. Asian Conf. Comput. Vis. 3091-3106 ​h​t​t​p​s​:​/​/​
d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​9​7​8​-​9​8​1​-​9​6​-​0​9​6​0​-​4​_​2​6​ (2024).
	31.	 Sinishaw, M. L. & Liu, S. JDECMC: Improving JDE-based multi-object tracking with camera motion compensation. Displays 
https://doi.org/10.1016/j.displa.2024.102682 (2024).
	32.	 Zeng, K. Noise-control multi-object tracking. Complex. Intell. Syst. 9(4), 4331–4347. https://doi.org/10.1007/s40747-022-00946-9 
(2023).
	33.	 Memon, S. A. et al. Tracking multiple autonomous ground vehicles using motion capture system operating in a wireless network. 
IEEE Access 12, 60592–60604. https://doi.org/10.1109/ACCESS.2024.3394536 (2024).
	34.	 Memon, S. A. et al. Tracking multiple unmanned aerial vehicles through occlusion in low-altitude airspace. Drones 7(4), 241. 
https://doi.org/10.3390/drones7040241 (2023).
	35.	 Seidenschwarz, J., Braso, G., Elezi, I. & Leal-Taixe, L. Simple Cues Lead to a Strong Multi-Object Tracker. Conf. Comput. Vis. 
pattern Recognit. 13813-13823 https://doi.org/10.1109/CVPR52729.2023.01327 (2023).
	36.	 Wang, Y. H. & et al. Similarity learning for occlusion-aware multiple object tracking. In Proceedings of the AAAI Conference on 
Artificial Intelligence. 38(6), 5740–5748, (2024). https://doi.org/10.1609/aaai.v38i6.28386
	37.	 Xiao, C. et al. Motiontrack: Learning motion predictor for multiple object tracking. Neural. Netw. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​n​e​
t​.​2​0​2​4​.​1​0​6​5​3​9​ (2024).
	38.	 Ge, Z. et al. & Yolox: Exceeding yolo series in 2021. arXiv preprint arXiv:2107.08430 (2021).
	39.	 He, L. et al. Fastreid: a pytorch toolbox for real-world person re-identification. arXiv preprint arXiv:.02631 (2020). (2020). (2006).
	40.	 Yang, H. S., Park, S. W., Jung, S. H. & Sim, C. B. EnhanceCenter for improving point based tracking and rich feature representation. 
Sci. Rep. https://doi.org/10.1038/s41598-025-88924-2 (2025).
	41.	 Vaquero, L., Xu, Y., Alameda-Pineda, X., Brea, V. M. & Mucientes, M. Lost and found: Overcoming detector failures in online 
multi-object tracking. In European Conference on Computer Vision. 448–466, (2024). https://doi.org/10.48550/arXiv.2407.10151
	42.	 Stadler, D. & Beyerer, J. Modelling ambiguous assignments for multi-person tracking in crowds. In Proceedings of the IEEE/CVF 
winter conference on applications of computer vision. 133–142, (2022). https://doi.org/10.1109/WACVW54805.2022.00019
	43.	 Wang, S. et al. Extendable multiple nodes recurrent tracking framework with RTU++. IEEE Trans. Image Process. 31, 5257–5271. 
https://doi.org/10.1109/TIP.2022.3192706 (2022).
	44.	 Zhang, S., Zhu, Y., Sun, Y., Liu, W. & Huang, Z. RAP-SORT: Advanced multi-object tracking for complex scenarios. Displays 
https://doi.org/10.1016/j.displa.2026.103361 (2026).
	45.	 Zhang, X., Zhao, H., He, S. & Li, Y. REAL-SORT: Relation-aware for real-time multiple object tracking. Knowl. Based Syst. ​h​t​t​p​s​:​/​/​
d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​k​n​o​s​y​s​.​2​0​2​6​.​1​1​5​3​7​3​ (2026).
Scientific Reports |        (2026) 16:13571 
16
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 17

	46.	 Jung, H., Kang, S., Kim, T., Kim, H. & ConfTrack Kalman Filter-Based Multi-Person Tracking by Utilizing Confidence Score of 
Detection Box. In Proceedings of the IEEE/CVF Winter Conference on Computer Vision and Pattern Recognition. (2024). ​h​t​t​p​s​:​/​/​d​o​
i​.​o​r​g​/​1​0​.​1​1​0​9​/​W​A​C​V​5​7​7​0​1​.​2​0​2​4​.​0​0​6​4​5​
	47.	 Liu, Z., Wang, X., Wang, C., Liu, W. & Bai, X. Sparsetrack: Multi-object tracking by performing scene decomposition based on 
pseudo-depth. IEEE Trans. Circuits Syst. Video Technol. https://doi.org/10.1109/TCSVT.2024.3524670 (2025).
	48.	 Stadler, D. & Beyerer, J. Past information aggregation for multi-person tracking. In 2023 IEEE International Conference on Image 
Processing. 321–325, (2023)., October https://doi.org/10.1109/ICIP49359.2023.10223159 (2023).
	49.	 Yi, K., Wu, H., Hao, W. & Hu, R. EscapeTrack: Multi-object tracking with estimated camera parameters. Signal. Process. ​h​t​t​p​s​:​/​/​d​o​
i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​s​i​g​p​r​o​.​2​0​2​5​.​1​0​9​9​5​8​ (2025).
	50.	 Chen, B., Wei, Z., Lei, W., Wang, C. & GMMotion Neighborhood Information Matters for Online Multi-Pedestrian Tracking. In 
PRICAI 2024: Trends in Artificial Intelligence. (2024). https://doi.org/10.1007/978-981-96-0122-6_8
	51.	 Gao, Y., Xu, H., Li, J., Wang, N. & Gao, X. Multi-Scene Generalized Trajectory Global Graph Solver with Composite Nodes for 
Multiple Object Tracking. Proceedings of the AAAI Conference on Artificial Intelligence, 38(3), 1842–1850, (2024). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​6​0​9​/​a​a​a​i​.​v​3​8​i​3​.​2​7​9​5​3​
	52.	 Zhang, Y. et al. Handling Heavy Occlusion in Dense Crowd Tracking by Focusing on the Heads. In AI 2023: Advances in Artificial 
Intelligence. 79–90, (2023). https://doi.org/10.1007/978-981-99-8388-9_7
	53.	 Stadler, D. & Beyerer, J. An Improved Association Pipeline for Multi-Person Tracking. In 2023 IEEE/CVF Conference on Computer 
Vision and Pattern Recognition Workshops. 3170–3179, (2023). https://doi.org/10.1109/CVPRW59228.2023.00319
	54.	 Sun, P. et al. & Global Tracking Transformers. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern 
Recognition. 8761–8770 (2022).
	55.	 Ren, H. et al. Focus on Details: Online Multi-Object Tracking with Diverse Fine-Grained Representation. In Proceedings of the 
IEEE/CVF Conference on Computer Vision and Pattern Recognition. 11289–11298, (2023). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​5​2​7​2​9​.​2​0​
2​3​.​0​1​0​8​6​
	56.	 Fang, Y. M. O. T. & FCG++ Enhanced Representation of Spatio-temporal Motion and Appearance Features. arXiv preprint 
arXiv:2411.10028 (2024).
	57.	 Qin, Z. et al. Motiontrack: Learning robust short-term and long-term motions for multi-object tracking. In Proceedings of the IEEE/
CVF conference on computer vision and pattern recognition. 17939–17948, (2023). https://doi.org/10.1109/CVPR52729.2023.01720
	58.	 Yang, F., Odashima, S., Masui, S. & Jiang, S. Hard to Track Objects with Irregular Motions and Similar Appearances? Make It 
Easier by Buffering the Matching Space. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision. 
4799–4808. (2023). https://doi.org/10.1109/WACV56688.2023.00478
	59.	 Larsen, M., Rolfsjord, S., Gusland, D., Ahlberg, J. & Mathiassen, K. BASE: Probably a Better Approach to Visual Multi-Object 
Tracking. In Proceedings of the 19th International Joint Conference on Computer Vision. 110–121 (2024).
	60.	 Shim, K., Hwang, J., Ko, K. & Kim, C. A confidence-aware matching strategy for generalized multi-object tracking. In IEEE 
international conference on image processing. 4042–4048,. 4042–4048, (2024). https://doi.org/10.1109/ICIP51287.2024.10647729 
(2024).
Acknowledgements
This paper was supported by Sunchon National University Glocal University Project Fund in 2025. (Grant num­
ber: 2025-G024)
Author contributions
H.S.Y. conceived Sentinel and designed CAA and SBM. S.W.P. and C.B.S. implemented the tracking pipeline and 
conducted experiments on the MOT17, MOT20, and DanceTrack datasets. S.H.J. supervised the project and 
contributed to manuscript revision. All authors have reviewed and approved the final manuscript.
Declarations
Competing interests
The authors declare no competing interests.
Informed Consent
This study utilizes three publicly available datasets: MOT17 and MOT20 from the MOT Challenge benchmark, 
and the DanceTrack dataset. The MOT Challenge datasets consist of fully anonymized data, for which no 
additional informed consent is required. The DanceTrack dataset was collected with prior informed consent 
from all participants. All datasets were used in accordance with their terms and conditions, which permit their 
use for research purposes and in academic publications.
Additional information
Correspondence and requests for materials should be addressed to C.-B.S. or S.-H.J.
Reprints and permissions information is available at www.nature.com/reprints.
Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and 
institutional affiliations.
Scientific Reports |        (2026) 16:13571 
17
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/


## Page 18

Open Access   This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 
4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in 
any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide 
a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have 
permission under this licence to share adapted material derived from this article or parts of it. The images or 
other third party material in this article are included in the article’s Creative Commons licence, unless indicated 
otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence 
and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to 
obtain permission directly from the copyright holder. To view a copy of this licence, visit ​h​t​t​p​:​/​/​c​r​e​a​t​i​v​e​c​o​m​m​o​
n​s​.​o​r​g​/​l​i​c​e​n​s​e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/​.​
© The Author(s) 2026 
Scientific Reports |        (2026) 16:13571 
18
| https://doi.org/10.1038/s41598-026-43938-2
www.nature.com/scientificreports/
