---
source_id: S028
title: Crowd counting at the edge using weighted knowledge distillation
source_url: https://www.nature.com/articles/s41598-025-90750-5.pdf
source_file: docs/research/papers/S028-crowd-counting-at-the-edge-using-weighted-knowledge-distillation.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S028-crowd-counting-at-the-edge-using-weighted-knowledge-distillation.pdf
## PDF metadata
- format: PDF 1.4
- creator: Adobe InDesign 18.3 (Windows)
- producer: Adobe PDF Library 17.0; modified using iText® 5.3.5 ©2000-2012 1T3XT BVBA (SPRINGER SBM; licensed version)
- creationDate: D:20250407092416+02'00'
- modDate: D:20250408054810+02'00'


## Page 1

Crowd counting at the edge using 
weighted knowledge distillation
Muhammad Asif Khan1, Hamid Menouar1,3, Ridha Hamila2,3 & Adnan Abu-Dayya2,3
Visual crowd counting has gained serious attention during the last couple of years. The consistent 
contributions to this topic have now solved several inherited challenges such as scale variations, 
occlusions, and cross-scene applications. However, these works attempt to improve accuracy and 
often ignore model size and computational complexity. Several practical applications employ 
resource-limited stand-alone devices like drones to run crowd models and require real-time inference. 
Though there have been some good efforts to develop lightweight shallow crowd models offering fast 
inference time, the relevant literature dedicated to lightweight crowd counting is limited. One possible 
reason is that lightweight deep-learning models suffer from accuracy degradation in complex scenes 
due to limited generalization capabilities. This paper addresses this important problem by proposing 
knowledge distillation to improve the learning capability of lightweight crowd models. Knowledge 
distillation enables lightweight models to emulate deeper models by distilling the knowledge 
learned by the deeper model during the training process. The paper presents a detailed experimental 
analysis with three lightweight crowd models over six benchmark datasets. The results report a clear 
significance of the proposed method supported by several ablation studies.
Unmanned Aerial Vehicles (UAVs) using visual computing enable automated crowd surveillance and analysis1,2 
during mega-events, transportation planning, and search and rescue missions. An interesting application is to 
automatically collect and analyze crowd statistics (e.g., crowd-counting and density estimation) in a geographical 
area. Deep learning serves a major role in the automated analysis of crowd images or videos. However, the 
deployment of deep learning models on edge devices such as drones poses unique challenges due to limited 
computational resources, power constraints, and slow inference3. Though several lightweight crowd-counting 
models have been proposed during the last few years for resource-constraint devices like drones2,4, the accuracy 
of such models significantly degrades in complex scenes due to limited learning capabilities. Recent studies have 
shown that lightweight models suffer from large generalization errors with poor adaptation capabilities. Thus, 
when a model trained on a given scene/dataset is deployed in a new scene/dataset, the accuracy drops.
To address these challenges, this paper explores the application of knowledge distillation (KD) to train 
lightweight models tailored for deployment on drones. Knowledge distillation5 is a model compression method 
that allows the transfer of learned knowledge from a cumbersome (deep) model to a lightweight (shallow) 
model. In the context of knowledge distillation, the cumbersome (deep) model is called the “teacher” model, 
whereas the lightweight ( shallow) model is referred to as the “student” model. It is argued that by distilling the 
knowledge learned by the teacher into the student, it is possible to achieve a significant reduction in model size 
and computational complexity without compromising performance5. The integration of knowledge distillation 
into the training process for lightweight models is a promising avenue to overcome resource limitations while 
maintaining or even enhancing the model’s effectiveness. Figure 1 depicts the potential scenario of training 
compact models using KD. The figure also highlights how KD framework can be integrated with federated 
learning (FL) scenarios in which the model updates flow in the opposite direction.
Over the last few years, KD has gained significant attention in the computer vision community which resulted 
in strong theoretical foundations and experimental studies in several vision problems. However, the applications 
of KD in crowd counting and density estimation have been untouched. Thus, it is interesting as well as useful 
to unveil the potential of KD in this significant application. This paper delves into the intricacies of knowledge 
distillation techniques, illustrating how they can be adapted and optimized for compact crowd-counting models 
suitable for drone applications. This paper presents a detailed and thorough experimental study encompassing 
three (3) lightweight crowd-counting models trained over six (6) benchmark datasets using knowledge 
distillation. The study covers diverse data-centric scenarios and several ablation studies to confidently conclude 
the potential benefits that can be achieved and the limitations of KD in the given context.
The contribution of this paper is as follows:
1Qatar Mobility Innovations Center, Qatar University, Doha, Qatar. 2Electrical Engineering, Qatar University, 
Doha, Qatar. 3Hamid Menouar, Ridha Hamila and Adnan Abu-Dayya contributed equally to this work. email: 
asifk@ieee.org
OPEN
Scientific Reports |        (2025) 15:11932 
1
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports


## Page 2

•	 We propose knowledge distillation (KD) to train lightweight models for crowd density estimation. The KD 
loss is formulated which allows distillation at any intermediate layers across both teacher and student models.
•	 The proposed method is extensively evaluated using three baseline lightweight models and two cumbersome 
teacher models over six benchmark crowd datasets to evaluate performance gains using the proposed scheme.
•	 Ablation studies are conducted to validate the results in diverse scenarios e.g., cross-domain adaptation, and 
different-teacher models.
The rest of the paper is organized as follows: Section “Knowledge distillation” presents a detailed theoretical 
overview of the knowledge distillation, whereas section “Crowd counting” presents a brief background of crowd 
counting methods and developments. Section “Related work” discusses recent relevant studies on KD and crowd 
counting to identify the research gap that motivates this work. Section “Proposed scheme” presents the proposed 
KD framework for crowd density estimation, which is investigated using a thorough set of experimental analyses 
presented in section “Experiments”. The results are reported and discussed in section “Results and discussion”. 
Further validation of the results is provided using ablation study in section “Ablation study”. Lastly, conclusions 
are drawn in section “Conclusion”.
Knowledge distillation
Knowledge Distillation (KD) refers to the mechanism in which the knowledge learned by a cumbersome 
and sophisticated model (teacher) is transferred to a shallow model (student) to improve the student model’s 
generalization performance. Using KD, the student can capture the finer details learned by the teacher instead of 
learning from the labels. The student model is the model that will be deployed for the application.
In its simpler form, the student model can mimic the performance of the teacher model by using the class 
prediction probabilities of the teacher called “soft targets”. The soft targets are calculated using the “temperature” 
parameter in the softmax function.
	
qi =
exp ( zi
T
)
∑
j exp
zj
T

(1)
where T is the “temperature” parameter used to soften the probabilities.
Knowledge can be distilled in three different ways. First, response-based KD5 in which the student model 
aims to mimic the teacher’s predictions, with the help of a distillation loss function that measures the difference 
between their logits. As the loss decreases over time, the student becomes more accurate in making predictions 
similar to the teacher. Second, feature-based distillation6 in which the teacher model, distills the data knowledge 
in its intermediate layers into the student models. The student model thus learns the same feature activations as 
the teacher. This is achieved by minimizing the difference between the feature activations of both models. Third, 
relation-based distillation7 in which connections between different layers or data samples are used employing a 
Flow of Solution Process (FSP) based on Gram matrices between layers to explore relationships among feature 
maps. The FSP matrix summarizes these relationships through inner product calculations between feature maps. 
Singular value decomposition is used to distill knowledge, with correlations between feature maps representing 
the distilled knowledge. This approach encapsulates relationships through feature maps, graphs, similarity 
matrices, feature embeddings, and probabilistic distributions, enhancing our understanding of knowledge 
distillation. Figure 2 illustrates the three types of KD in neural networks8. investigates KD and observed that 
a student model trained via KD can exhibit higher intra-class variance than the teacher model, and thus act as 
a better teacher9. have proposed an evolutionary knowledge distillation mechanism in which the pretrained 
teacher network is replaced by an online learned teacher model9. also consider training multiple teacher 
Fig. 1.  Collaborative training of multiple local models (student models) running over edge devices and a 
single global model (teacher model) running over an edge server via knowledge distillation.
 
Scientific Reports |        (2025) 15:11932 
2
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 3

networks online synchronously, which all distill knowledge to the student and improves its performance10. 
propose a unique type of KD that uses heuristics to let the student learn from the teacher’s failures. This can also 
be applied to self-distillation.
Crowd counting
Traditionally, crowd counting aims to detect simply the total object (e.g., people) count in an image11. These 
methods manually apply a feature detector to extract features such as full body shape12, or body parts13–16 and 
then apply ML models such as linear or ridge regression, support vector machines (SVMs), random forest (RF), 
gradient methods, or multi-layer perceptrons (MLPs) to predict the total count. These methods underperform 
in dense crowds due to occlusions, low resolution, and perspective distortions. Traditional methods regress the 
total count in an image17 or image patch18 using global features such as texture19, foreground20, gradients21. 
However, these methods provide poor estimates of high-density crowd images. Authors in22 used an alternative 
approach to divide images into patches, classify patches as crowd/no-crowd using SVM, and then count heads 
using head detection CNN network. The authors further proposed an enhancement in23 of the method in22, by 
classifying patches as low, medium, high-dense, or no-crowd. The patches of different density levels are then 
zoomed accordingly before regressing the count in them.
The most recent methods for crowd counting use density map estimation in which the input is an image and 
the output is the density map of the crowd24,25. The pixel values in the density map are summed up to get the 
total head count. Thus, a density map contains additional location information along with the total head count 
of the crowd scene. Density estimation typically uses convolution neural networks (CNNs)26–34. CNNs offer a 
strong capability of automatic feature extraction and have shown remarkable performance in several computer 
vision problems such as image classification35,36, object detection37, and image segmentation38. CNNs can be 
used for both global count estimation as well as density map estimation39. A two-stage crowd counting has 
been proposed in29 to regress both local density and global count. Similarly40, proposed a cascaded architecture 
of a density map regressor and a global crowd count regressor (using weak supervision). The global count 
regressor learns scene-level features, whereas the density map regressor effectively learns features such as shape 
variation and background effects. The multistream convolutional neural network (AMS-CNN) is proposed in41 
to learn features using three streams and then fuses the spatial, temporal, and spatial foreground features from 
different cues of the crowd scene42. proposes a multi-attention Spatial-Temporal CNN architecture to learn 
cluttered background and scale variation in crowd scenes. Scale variation and background noise and clutters are 
challenging problems in crowd counting and several works have been published recently to address the issue. 
For instance43, proposed a novel architecture (SA2Net) to address these challenges by proposing a multiscale 
feature aggregator (MFA) module and a background noise suppressor (BNS). The SA2Net uses a composite 
loss (global consistency loss and Euclidean loss) to optimize the network. Similarly44, further proposed FPANet 
to solve the scale variation problem in lightweight models through special attention modules by suppressing 
misleading information. Authors in45 addressed the scale variation challenge using a different approach by 
jointly solving the counting and localization problems, using a combined Euclidean and structural similarity 
loss function. Emerging concepts such as quantum machine learning have been used in34 for crowd counting 
for dense crowd counting with extreme background noise to boost the model’s generalization capabilities. 
Recently46, proposed incremental learning for crowd object counting for improved learning of new object 
classes. The images are annotated by humans by placing a dot on the head position, there might be small errors in 
the annotation, however such errors (if not significantly high) do not significantly impact the accuracy much47. 
When using knowledge distillation, the teacher model, which has a higher capacity and is trained on a larger 
set of labeled data, helps reduce the impact of annotation noise when transferring knowledge to the student 
model. By using soft labels and intermediate feature maps from the teacher model, the student model gains a 
more robust representation, which can help it generalize better even when training data includes some level of 
human error. The performance of the shallow crowd models is significantly impacted by scale variations in head 
sizes, background clutters, illumination variations, and occlusions. However, the method distill knowledge from 
a deeper model trained with multi-scale features to help the shallow model to cope with scale variations, and 
Fig. 2.  Three types of knowledge distillation (KD).
 
Scientific Reports |        (2025) 15:11932 
3
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 4

other challenges such as background clutters and occlusions. The teacher model captures and transfers these 
scale-aware features to the student model, enabling it to better handle variations in object size within the scene.
Related work
Knowledge distillation (KD) in neural networks was proposed by Hinton et al. in5 which is inspired by the 
work48 demonstrating that “knowledge learned by a large ensemble of models can be transferred to a single 
model”. Hinton et al.5 introduced the “temperature” parameter T in the softmax function at the output layer used 
to distill the knowledge from the teacher model to the student model by training the student model using the 
same dataset as used for training the teacher model with a high value of T. Once the student model is trained, 
the value of T is set to T = 1 (standard softmax function) during the inference. The student model’s accuracy 
can be highly improved by using two objective (loss) functions i.e., a cross-entropy (CE) function with the soft 
targets (produced by the teacher) and a CE with the actual ground truth labels. The authors suggest using a 
high value of T in the first case (same T in student and teacher) and T = 1 for the second case. However, the 
method was limited to supervised learning. To extend the KD concept to any type of deep learning model, 
Romero et al.6 proposed feature-based KD to learn the intermediate representation (activation maps). They 
proposed to match the intermediate layer outputs of the teacher and student models to guide the student model. 
Several works extended this model to propose different methods to match feature activation maps such as using 
attention maps49, neuron selectivity50, and factors51. Similar to the response-based KD in which the knowledge 
is distilled from the output layer, in feature-based KD the knowledge is distilled from a single intermediate layer. 
In contrast,7 proposed relations-based KD in which a Gram matrix is calculated as an inner product between 
the feature maps of two layers. The model has been further extended by52 to learn from more than one teacher.
Authors in53 highlighted that the transfer of knowledge is impacted by the difference in the capacity of the 
teacher and student models. Knowledge distillation from multiple teacher networks is proposed in54. In this 
work, the authors used two teacher networks, where one teacher network distills knowledge from intermediate 
feature maps to the student (feature-based KD), whereas the second teacher network directly distills the output 
probabilities (response-based KD). Knowledge distillation can also be used alongside other model compression 
techniques. For example, authors in55 propose knowledge distillation with quantization. Similarly, authors in56 
suggest incorporating pruning with knowledge distillation.
The aforementioned works illustrate the benefits and different approaches to KD in neural networks mostly 
in classification tasks. KD typically performs well in classification due to the so-called “dark knowledge” in the 
softened logits of the teacher which the student uses to emulate the generalization capability of the teacher57. On 
the contrary, KD in image regression tasks that involve predicting continuous and unbounded outputs can be 
limited58. KD has been used in a few regression tasks such as pose estimation57, and gaze estimation59. Recently, 
KD has been applied in crowd counting based on the density estimation method. For instance, authors in60 applied 
KD in crowd counting to train a shallow network (EdgeCount) using a teacher network (EdgeCount_T). Both 
EdgeCount and EdgeCount_T use the same architecture i.e., encoder-decoder architecture using MobileViT61 
as the encoder. EdgeCount60 uses extra modules such as spatial channel reconstruction convolution (SCConv) 
composed of spatial reconstruction unit (SRU) and channel reconstruction unit (CRU) and a low parameter 
weighted multi-scale feature fusion module (LWMFFM) to enhance the model performance. Similarly62, 
proposes using self-distillation for crowd counting to help a crowd model using previous meaningful knowledge. 
Self-distillation can help the model to retain the most recent knowledge, but it can not be used to make shallow 
model learns more features from deeper models. Authors in63 used KD to distill foreground knowledge from a 
density map to enhance counting performance in challenging scenarios. This method does not use KD to train 
shallow networks.
This paper studies and evaluates through extensive experiments the benefits of KD in model-agnostic 
(different student/teacher) settings using multiple teacher and student models, on cross-scene datasets of 
different crowd data (humans, cars, animals).
Proposed scheme
The proposed method (Fig. 3) is based on knowledge distillation (KD). KD originally has been defined as a logits-
matching problem for classification. Let T be the teacher model, and S be the student model, both generating 
outputs OT = softmax(aT ), and OS = softmax(aS), respectively. aT  and aS are the pre-softmax logits and 
OT  and OS are the class probabilities of T and S models, respectively.
Since the teacher outputs are usually very close to true labels (assuming T has a very high accuracy), a 
temperature variable τ is used to soften the outputs of T, and the same τ is used in the student model S as 
well during training. Then in the inference stage, S uses τ = 1. The softened outputs potentially provide more 
information to the student model than the hard labels.
	
Oτ
T = softmax
(aT
τ
)
=
exp(
aT
i
τ )
∑
i exp(
aT
j
τ )

(2)
	
Oτ
S = softmax
(aS
τ
)
=
exp(
aS
i
τ )
∑
i exp(
aS
j
τ )

(3)
At high τ values, the distillation loss can be calculated as5:
Scientific Reports |        (2025) 15:11932 
4
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 5

	
L = 1
2(zi −vi)2
(4)
where zi and vi are zero-meaned logits of the student and teacher models, respectively.
If the true labels are available, distillation loss is calculated as a weighted sum of two errors: (i) hard label 
error H (y, OS) and (ii) soft label error H (Oτ
T , Oτ
S).
	
LKD = αH (y, OS) + (1 −α)H (Oτ
T , Oτ
S)
(5)
where H  is the cross entropy and y is the hard label or ground truth. The term α is a balancing parameter 
between the hard label error H (y, OS) and the soft label error H (Oτ
T , Oτ
S). For instance, setting the value of 
α < 0.5 means a higher weight is assigned to the soft label error.
In the density estimation problem, the model estimates the density map i.e., true pixel values rather than the 
sparse class labels. In the proposed system, the teacher model is trained on the labeled dataset to produce density 
maps. T(xi) for each input xi. The student model is trained on the same labeled dataset but it also utilizes the 
predictions of the teacher model. The distillation loss function is typically based on the L2 distance between 
the teacher’s predictions T(xi) and the student’s predictions S(xi). The student model is trained to minimize 
this loss function, aiming to match the teacher’s predictions. The temperature parameter is used to soften the 
predictions of both the teacher and the student models.
As the crowd scenes might be complex (e.g., dense crowds, clutters, complex background, etc.), the teacher 
model thus captures general trends under varying conditions and the student benefits from this knowledge, 
learning a more robust regression function that generalizes better across diverse scenarios. In such scenarios, 
the temperature parameter τ plays a crucial role. The temperature parameter τ in Eq. 5 directly influences the 
transfer of knowledge to the student model. Unlike classification tasks, in which the temperature smoothens the 
logits to emphasize the relative probabilities between classes, in regression, it smoothens the output distribution 
or modulates the gradients during training. This helps in capturing broader patterns rather than exact pointwise 
predictions. A higher temperature emphasizes learning the overall trends or correlations in the data as provided 
by the teacher, rather than overfitting the fine-grained teacher outputs, whereas, a lower temperature makes 
the student model mimic the teacher more closely, which could lead to overfitting to the teacher’s noise or 
inaccuracies. In other words, a higher value of the temperature parameter leads to better generalization, whereas 
a lower value enforces precision in mimicking the teacher’s outputs, which might be advantageous when the 
teacher model is highly accurate and represents the desired regression function well. In the proposed KD-based 
regression framework, the temperature parameter scales gradients, influencing how much the student prioritizes 
the teacher’s predictions over the ground truth data. Thus, the temperature parameter needs finetuning to help 
the student model converge more effectively by balancing the trade-off between learning from ground truth data 
and the teacher’s knowledge.
We formulate the loss function for density map distillation as follows57:
	
Lreg = 1
n
n
∑
i=1
α ∥pS −pGT ∥2 + (1 −α)ϕi ∥pS −pT ∥2
(6)
In eq. 6, ϕ is the normalized teacher loss and is calculated as follows:
Fig. 3.  Proposed scheme using knowledge distillation from a deeper teacher network into a smaller student 
network.
 
Scientific Reports |        (2025) 15:11932 
5
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 6

	
ϕi =
(
1 −∥pT −pGT ∥2
η
)

(7)
where LT  is the L2 loss of the teacher over the train dataset.
	
η =max(LT ) −min(LT )

(8)
	
LT = ∥pT −pGT ∥2
∀j ∈N 
(9)
Experiments
The proposed method is evaluated over 6 benchmark datasets and three well-known crowd models, explained 
in this section.
Datasets
There are a number of publicly available crowd-counting datasets64 of various sizes and complexity. However, we 
carefully considered these and chose five datasets for specific reasons as explained in the following. We omitted 
the use of datasets with too congested scenes as the student models used in this study are too shallow and will 
certainly not achieve sufficient accuracy. It is worth noting that the aim of this study is to effectively apply 
KD to train extremely lightweight and shallow architectures (≤ 0.2 million parameters), which are suitable for 
deployment over resource-constrained edge devices in real-time applications and especially when the crowd 
estimate is required rather than the most accurate count.
Mall
The Mall dataset65 is a publicly available dataset containing 2000 video frames of fixed size (640x480 pixels) 
captured from a single webcam (single scene). The dataset contains a total of 60,000 pedestrians annotated. The 
dataset is chosen to evaluate the models’ performance in a single-scene CCTV deployment.
ShanghaiTech
The ShanghaiTech dataset26 is a widely used benchmark dataset tailored for crowd counting research. It features 
high-resolution images captured from diverse real-world scenes, primarily in the streets of Shanghai, China. The 
dataset comprises a total of 1198 images with 330,165 annotations. It is partitioned into two distinct parts: Part-A 
containing 482 images, and Part-B, containing 716 images. Within Part-A, there are train and test subsets, each 
containing 300 and 182 images, respectively. Similarly, Part-B is subdivided into train and test subsets, with 400 
and 316 images, respectively. The dataset is chosen to evaluate the models’ performance in a cross-scene CCTV 
deployment.
CARPK
The Car Parking Lot (CARPK) dataset66 comprises images of car parking containing a total of 90,000 vehicles 
gathered from four distinct parking lots using a PHANTOM 3 PROFESSIONAL drone. The images were 
captured from an aerial perspective at an altitude of approximately 40 meters. Each image in the dataset is 
annotated with bounding boxes delineating the position of individual cars. The dataset facilitates tasks such as 
object counting, and object detection. The dataset is chosen to evaluate the models’ performance in a cross-scene 
drone deployment for vehicle counting.
DroneRGBT
The DroneRGBT dataset67 is a collection of images captured using a drone equipped with both RGB (Red, Green, 
Blue) and thermal (T) sensors. This dataset combines information from both visual and thermal spectrums, 
providing a rich source of data for various computer vision and remote sensing tasks. The images are obtained 
from aerial viewpoints, offering unique perspectives on different environments. The dataset is annotated and 
categorized to facilitate tasks such as object detection, classification, and semantic segmentation in both RGB 
and thermal domains. The dataset contains 3600 pairs of RGB and thermal images. The dataset is chosen to 
evaluate the models’ performance in a cross-scene drone deployment for people counting, especially in low light 
conditions.
Aerial sheeps
The aerial sheep dataset68 consists of 1727 images of sheep from a birds-eye view. The dataset is divided into 
train (1203 images), validation (350 images), and test (174 images) sets. All images are of fixed spatial resolution 
(600 × 600). The dataset is chosen to evaluate the models’ performance in a cross-scene drone deployment for 
animal counting.
Figure 4 shows the count histograms of the six datasets used in this study.
Baselines
We used two deep neural networks called CSRNet and CSRNet_lite2 that serve as teacher models, and three 
shallow networks i.e., MCNN, DroneNet4, LCDnet2 as student models.
MCNN
This multi-column CNN26 architecture uses adaptive kernels to capture perspective distortion in crowd images. 
The network consists of three columns of Conv layers with different sizes of filters. MCNN uses max pooling 
Scientific Reports |        (2025) 15:11932 
6
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 7

layers of 2 × 2 after each Conv layer and ReLU activation function. The outputs of the three columns are stacked 
to get the final density map. The spatial resolution of the final density map is one-fourth of the size of the input 
image.
DroneNet
The DroneNet crowd model4 uses the same three-column structure of MCNN with the Conv layers replaced 
with Self-ONN layers69. Self-ONN (Operational Neural Networks) layers perform non-linear operations to 
learn more fine-grained features.
LCDnet
The lightweight crowd density estimation (LCDnet) model2 is an extremely lightweight architecture proposed 
for aerial surveillance using drones. Since drones capture the top view of the scene, the perspective distortion 
Fig. 4.  Count histograms of various datasets used in this study.
 
Scientific Reports |        (2025) 15:11932 
7
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 8

arising from the camera field-of-view is minimal when the drone is at a constant altitude. LCDnet achieves 
comparable performance to MCNN26 on aerial images (e.g., DroneRGBT and CARPK datasets) with almost 
half the number of parameters. Also, the spatial resolution of the output density map in LCDnet is double of 
MCNN output.
The three models are chosen because these models are extremely lightweight with parameters less than 
0.2 million (Table 2). All three models do not rely on transfer learning. The MCNN and DroneNet are both 
multicolumn architectures, but MCNN uses CNN layers with non-linear activation functions, whereas 
DroneNet uses non-linear self-ONN layers. The LCDnet uses a shallower hybrid architecture with only 0.05 
million parameters.
Training
We used the PyTorch framework to implement the proposed scheme. First, the annotations (localization maps) 
are converted into density maps using Gaussian kernel using the following Eq. 10.
	
D =
N
∑
i=1
δ(x −xi) ∗Gσ
(10)
Eq.  10 convolves the dot annotations δ(x −xi) with the Gaussian function Gσ =
1
s
√
2π e−(x−µ)2
2σ2
 for all 
N (number of points i.e., head positions in the dot annotation matrix). For simplicity and reproducibility, 
we use fixed-size kernels (i.e., the scale parameter σ) for all the images in the same dataset. Specifically, the 
σ = [10, 15, 7, 8, 10] are used for ShanghaiTech Part A, ShanghaiTech Part B, DroneRGBT, CARPK, and Mall 
datasets, respectively.
All models are trained on a Lambda machine with Quadro RTX-8000 GPUs. We use a constant learning 
rate of 0.001 in all experiments. the student models using KD use the loss function defined in Eq. 6, whereas the 
baseline models (students without KD) and the teacher model (without KD) use the standard training method 
using mean squared error (MSE) as a loss function as defined in Eq. 11.
	
L (Θ) = 1
N
N
∑
1
||D(Xi; Θ) −Dgt
i ||2
2
(11)
where N is the number of samples in the training set, D(Xi; Θ) is the model estimated density map for the input 
image Xi, and Dgt
i  is the ground truth density map.
Evaluation metric
All the models are compared using the mean absolute error (MAE) metric which is commonly used in crowd 
counting research. Though there are alternate metrics available e.g., Grid Average Mean Error (GAME), MAE 
is a more common and standard metric. Also, any performance gain achieved using MAE also holds true for 
GAME2,4.
MAE is the average of absolute count error in predicted and actual density maps and is calculated using 12:
	
MAE = 1
N
N
∑
1
(en −ˆgn)
(12)
where, N is number of images, gn is actual count and ˆen is estimated count in the nth image.
Results and discussion
The proposed method is evaluated over the benchmark datasets by training the three baseline models using 
standard training (without KD), and using the proposed method (with KD). To inspect the learning performance, 
the activation maps at different layers from both teacher and student models were analyzed to compare the 
model’s capabilities. An example of activation maps from a single layer from both teacher and student models 
are presented in Fig. 5.
Table 1 presents the counting performance of the proposed method over the four benchmark datasets. The 
mean absolute error (MAE) is compared against baseline models. Figure 6 illustrates the comparison more 
intuitively using spider charts. The figure depicts a percent reduction in MAE using the proposed scheme with 
respect to all baseline models. More specifically, each spider subplot represents the percent reduction in MAE of 
the three student models (MCNN, DroneNet, and LCDnet) when the proposed scheme is used. The reduction 
is reported for four different cases (Table 1). The analysis of the results shows that: (i) MCNN achieves higher 
gains on all datasets except on DroneRGBT in a few cases (at 40%, 100%). This is a model-specific observation 
that shows better learning or generalization capabilities of MCNN in most scenarios. However, DroneNet and 
LCDnet using KD achieve higher gains on the DroneRGBT dataset in a few cases. The results should not be 
confused with the overall accuracy (or error performance) of the models, but these only reflect the gains using 
the proposed scheme. For instance, DroneNet outperforms MCNN on almost all datasets. (ii) The performance 
gains for all models are typically maximum at the 40% labeled data and minimum at 100% labeled data. This is 
an expected and most significant result that was expected. This means that when the amount of labeled data is 
reduced, the baseline models start underperforming and the MAE increases. At the same time, by applying the 
Scientific Reports |        (2025) 15:11932 
8
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 9

proposed scheme, the student models learn from the teacher’s knowledge to improve their performance (MAE 
reduces). This results in reduced MAE using baseline models (using the proposed scheme) as compared to the 
baseline models (without KD), ultimately resulting in higher percent gains (Fig. 6). (iii) The percent gains are 
minimal for the Mall dataset as compared to the other dataset due to the lower MAE values (high accuracy) for 
the baseline models and thus less room for improvement to reflect in the percent gains.
Furthermore, the LCDnet model is an extremely lightweight architecture with only 0.05M parameters 
as compared to MCNN (0.13M) and DroneNet (0.15). LCDnet also uses only two columns (3 columns in 
MCNN and DroneNet), with fewer layers. Thus, the relative lower accuracy (or higher MAE) of LCDnet is 
justified. Similarly, DroneNet achieves superior performance than MCNN due to the fact that DroneNet uses 
more powerful non-linear self-ONN operations rather than the linear convolution operations of CNN, in a 
similar architecture as MCNN. However, it is worth noting that the purpose of the study is not to evaluate the 
individual capabilities of different models to learn from KD but rather to evaluate the overall efficacy of KD in 
training lightweight crowd counting models of which MCNN, DroneNet, and LCDnet are examples. Figure 7 
presents a single prediction output for a single sample from each dataset (Mall, ShanghaiTech Part A, Part B, 
and DroneRGBT).
Computational complexity
Although the study aims to investigate knowledge distillation and its efficacy in training shallow student 
models since the final student models are designed to be deployed at the edge, it is significant to analyze the 
computational complexity of these models. Table 2 reports the computational complexity of the teacher and 
Student ↓
Labelled data 40%
Labelled data 60%
Labelled data 80%
Labelled data 100%
Standard
Ours
Standard
Ours
Standard
Ours
Standard
Ours
Mall
 MCNN
9.8
8 (+ 18.3%)
6.1
5.2 (+ 14.9%)
4.8
4.2 (+ 11.6%)
3.6
3.3 (+ 8.0%)
 DroneNet
9.3
7.6 (+ 17.9%)
6.5
5.4 (+ 16.3%)
4.5
3.9 (+ 12.5%)
3.3
3 (+ 9.6%)
 LCDnet
9.9
8.5 (+ 14.3%)
7.2
6.2 (+ 13.6%)
5.6
4.9 (+ 12.2%)
4.2
3.8 (+ 8.8%)
ShanghaiTech Part A
 MCNN
140.2
103.7 (+ 26.0%)
125.4
94.6 (+ 24.6%)
118.6
96.9 (+ 18.3%)
110.2
91.9 (+ 16.6%)
 DroneNet
128.8
101.9 (+ 20.9%)
114.8
93.6 (+ 18.5%)
105.7
88.6 (+ 16.2%)
98.5
83.9 (+ 14.8%)
 LCDnet
156.3
128.5 (+ 17.8%)
134.5
111.5 (+ 17.1%)
127.4
110.2 (+ 13.5%)
118.4
107.9 (+ 8.9%)
ShanghaiTech Part B
 MCNN
40.5
29.8 (− 26.4%)
33.3
25.9 (− 22.2%)
29.1
24.3 (− 16.5%)
26.4
22.3 (− 15.5%)
 DroneNet
38.6
31.1 (− 19.5%)
32.5
27.2 (− 16.2%)
24.8
21.6 (13.1%)
22.4
19.6 (− 12.6%)
 LCDnet
44.3
34.5 (− 22.1%)
41.8
33.2 (− 20.6%)
35.9
29.7 (− 17.3%)
31.6
26.3 (− 16.8%)
DroneRGBT
 MCNN
36.4
27.5 (+ 24.5%)
28.5
22.9 (+ 19.6%)
21.6
17.6 (+ 18.4%)
17.9
15.7 (+ 12.3%)
 DroneNet
33.7
25 (+ 25.7%)
22.9
17.8 (+ 22.3%)
18.7
14.8 (+ 20.6%)
11.3
9.7 (+ 14.5%)
 LCDnet
38.5
30.8 (+ 19.9%)
29.3
23.9 (+ 18.3%)
24.6
20.5 (+ 16.8%)
21.4
18.4 (+ 14.2%)
Table 1.  Counting accuracy performance of the proposed method on four benchmark datasets, using mean 
absolute error (MAE) metric.
 
Fig. 5.  An illustration of activation maps obtained from the teacher and student network. This shows better 
learning ability of the teacher network which learned more fine-grained features. The student’s features are 
apparently less rich than the teacher network which are highly improved using the knowledge distilled from 
the teacher network.
 
Scientific Reports |        (2025) 15:11932 
9
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 10

student models to understand why efficient shallow models are more suitable for edge devices, especially in 
real-time or near real-time applications. The analysis shows that the inference time of MCNN and DroneNet is 
reduced by a factor of 8 compared to the teacher model, while LCDnet achieves an 18-fold reduction. Similarly, 
the storage size of these student models is negligible (less than 1 MB) as compared to the teacher model (65 MB).
Ablation study
The experiments and results discussed earlier comprised people crowds (surveillance and aerial views). This 
section aims to validate the results achieved in the aforementioned section by further ablation studies. Specifically, 
we aim to evaluate the proposed method using different a teacher model, and datasets of nun-human objects 
(e.g., people, animals).
Different teachers models
We use the CSRNet_lite2 model as a teacher to replace the CSRNet model (used in the earlier experiment) to 
validate the performance gains using different teacher models. The results are reported in Table 3.
The results show that the proposed scheme outperforms baseline models even for the new teacher model 
(i.e., CSRNet_lite). Furthermore, CSRNet_lite also achieves slightly better accuracy (lower MAE) than CSRNet. 
These results signify the importance of the selection of a better teacher model to improve the performance of 
the student model.
Cross-domain adaptation
Previously, we evaluated our proposed models on human crowds. We further studied the cross-domain 
adaptation using KD using two datasets of cars66 and sheep crowds68. The results are reported in Tables 4 and 5, 
respectively.
The results reported in Tables 4 and 5 further validate the results reported in section “Results and discussion” 
and dictate that the KD framework is both data-agnostic and model-agnostic. Furthermore, we introduced two 
new metrics i.e., structural similarity index (SSIM) and pixel signal-to-noise ratio (PSNR) as in2,27,70 to measure 
Fig. 6.  Percent (%) reduction in mean absolute error (MAE) using the proposed scheme against the respective 
baseline models for four different datasets.
 
Scientific Reports |        (2025) 15:11932 
10
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 11

the quality of predicted density maps alongside the MAE metric for counting accuracy (or error) performance. 
The results show that the proposed method outperforms over the two datasets using all metrics.
Figures 8 and 9 depict sample predictions on the Sheep68 and CARPK66 datasets, respectively.
Conclusion
This paper proposed the use of knowledge distillation (KD) to train compact crowd-counting architectures. 
KD improves the performance and accuracy of the compact model by distilling the dark knowledge from a 
cumbersome model during the training stage. It enhances the learning capability of the compact model by 
guiding the network to learn more fine-grained features under the supervision of the cumbersome model. KD 
has been applied in several computer vision and other deep learning tasks, but very few works exist on the 
use of KD in regression tasks such as crowd density estimation. This paper provides an intuitive framework 
Fig. 7.  Predictions results on the sample images from Mall, ShanghaiTech Part A, Part B, and DroneRGBT 
datasets.
 
Scientific Reports |        (2025) 15:11932 
11
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 12

with rigorous experimental analysis alongside ablation studies on domain adaptation and different teacher and 
student models to validate the performance gains. In future work, we aim to extend this study to integrate KD in 
federated learning (FL) to develop two-way privacy-preserving learning between student models (local models 
in the edge devices) and the teacher model (global model on the server). We also aim to investigate a novel case 
of server-less FL architecture with KD across edge devices.
Models
MAE
SSIM
PSNR
Baseline
Ours
Baseline
Ours
Baseline
Ours
MCNN
10.20
8.05
0.76
0.80
19.6
24.22
DroneNet
9.10
7.67
0.81
0.85
21.08
25.83
LCDnet
13.05
10.18
0.71
0.79
20.8
23.44
Table 5.  Ablation study for domain adaptation on CARPK dataset.
 
Models
MAE
SSIM
PSNR
Baseline
Ours
Baseline
Ours
Baseline
Ours
MCNN
5.76
4.13
0.88
0.92
28.6
30.94
DroneNet
5.11
4.06
0.90
0.94
29.9
32.15
LCDnet
7.82
5.36
0.76
0.85
25.47
29.02
Table 4.  Ablation study for domain adaptation on Sheeps dataset.
 
Models
Mall
ST Part A
ST Part B
DroneRGBT
MCNN
+ 1.3 ↑
− 3.6 ↑
+ 2.2 ↑
+ 1.3 ↑
DroneNet
+ 0.7 ↑
− 2.8 ↑
+ 1.2 ↑
+ 0.9 ↑
LCDnet
+ 0.8 ↑
− 1.2 ↑
− 0.7 ↑
+ 1.1 ↑
Table 3.  Ablation study using CSRNet_lite as a teacher with 60% labelled data.  The ↓↑ signs indicate the 
decrease/increase with respect to the baseline model, whereas the ± sign indicates an increase/decrease in 
MAE as compared to CSRNet as a teacher.
 
Model
Output
Parameters(M)
Size(MB)
GMACs
Inference time(s)
Server
Jetson Xavier
Jetson Nano
Teacher model
 CSRNet27
1/8
16.26
65.05
135.4
0.19
1.01
1.88
Student models
 MCNN26
1/4
0.13
0.53
8.82
0.05
0.10
0.21
 DroneNet26
1/4
0.15
0.60
8.92
0.056
0.15
0.28
 LCDnet
1/2
0.05
0.21
4.85
0.006
0.05
0.10
Table 2.  Computational complexity of the student models trained with KD in terms of number of parameters 
(in Million), GMACs, size (in MB), and inference time (in mili seconds) for fixed input size.
 
Scientific Reports |        (2025) 15:11932 
12
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 13

Data availability
The Mall dataset analyzed during the current study is publicly available at: ​h​t​t​p​s​:​/​/​p​e​r​s​o​n​a​l​.​i​e​.​c​u​h​k​.​e​d​u​.​h​k​/​~​c​c​l​o​
y​/​d​o​w​n​l​o​a​d​s​_​m​a​l​l​_​d​a​t​a​s​e​t​.​h​t​m​l The ShanghaiTech dataset analyzed during the current study is publicly availa­
ble in the Github repository, https://github.com/desenzhou/ShanghaiTechDataset. The CARPK dataset analyzed 
during the current study is publicly available at https://lafi.github.io/LPN/. The DroneRGBT dataset analyzed 
during the current study is publicly available in the Github repository: ​h​t​t​p​s​:​/​/​g​i​t​h​u​b​.​c​o​m​/​V​i​s​D​r​o​n​e​/​D​r​o​n​e​R​G​B​
T​ The Aerial Sheeps dataset analyzed during the current study is publicly available in the Github repository: ​h​t​t​
p​s​:​/​/​h​u​g​g​i​n​g​f​a​c​e​.​c​o​/​d​a​t​a​s​e​t​s​/​k​e​r​e​m​b​e​r​k​e​/​a​e​r​i​a​l​-​s​h​e​e​p​-​o​b​j​e​c​t​-​d​e​t​e​c​t​i​o​n.
Received: 19 August 2024; Accepted: 14 February 2025
Fig. 9.  Predictions results on the CARPK dataset.
 
Fig. 8.  Predictions results on the Sheeps dataset.
 
Scientific Reports |        (2025) 15:11932 
13
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 14

References
	 1.	 Simpson, T. Real-time drone surveillance system for violent crowd behavior unmanned aircraft system (uas)—human autonomy 
teaming (hat). In 2021 IEEE/AIAA 40th Digital Avionics Systems Conference (DASC), 1–9 (2021). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​D​A​S​C​5​2​
5​9​5​.​2​0​2​1​.​9​5​9​4​3​3​2​.​
	 2.	 Khan, M. A., Menouar, H. & Hamila, R. LCDnet: A lightweight crowd density estimation model for real-time video surveillance. 
J. Real-Time Image Process. 20, 29 (2023).
	 3.	 Cai, H., Gan, C., Lin, J. & Han, S. Network augmentation for tiny deep learning. In International Conference on Learning 
Representations (2022).
	 4.	 Khan, M. A., Menouar, H. & Hamila, R. DroneNet: Crowd density estimation using self-ONNs for drones. In 2023 IEEE 20th 
Consumer Communications & Networking Conference (CCNC), 455–460 (IEEE, 2023).
	 5.	 Hinton, G. E., Vinyals, O. & Dean, J. Distilling the knowledge in a neural network. ArXiv ArXiv:1503.02531 (2015).
	 6.	 Romero, A. et al. FitNets: Hints for thin deep nets. arXiv preprint arXiv:1412.6550 (2014).
	 7.	 Yim, J., Joo, D., Bae, J.-H. & Kim, J. A gift from knowledge distillation: Fast optimization, network minimization and transfer 
learning. In 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 7130–7138 (2017).
	 8.	 Li, C., Cheng, G. & Han, J. Boosting knowledge distillation via intra-class logit distribution smoothing. IEEE Trans. Circuits Syst. 
Video Technol.[SPACE]https://doi.org/10.1109/TCSVT.2023.3327113 (2023).
	 9.	 Zhang, K., Zhang, C., Li, S., Zeng, D. & Ge, S. Student network learning via evolutionary knowledge distillation. IEEE Trans. 
Circuits Syst. Video Technol. 32, 2251–2263. https://doi.org/10.1109/TCSVT.2021.3090902 (2022).
	10.	 Xu, K., Wang, L., Xin, J., Li, S. & Yin, B. Learning from teacher’s failure: A reflective learning paradigm for knowledge distillation. 
IEEE Trans. Circuits Syst. Video Technol. 34, 384–396. https://doi.org/10.1109/TCSVT.2023.3285213 (2024).
	11.	 Li, T. et al. Crowded scene analysis: A survey. IEEE Trans. Circuits Syst. Video Technol. 25, 367–386. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​C​S​V​
T​.​2​0​1​4​.​2​3​5​8​0​2​9​ (2015).
	12.	 Lin, Z. & Davis, L. S. Shape-based human detection and segmentation via hierarchical part-template matching. IEEE Trans. Pattern 
Anal. Mach. Intell. 32, 604–618. https://doi.org/10.1109/TPAMI.2009.204 (2010).
	13.	 Viola, P. & Jones, M. Robust real-time face detection. In Proceedings Eighth IEEE International Conference on Computer Vision. 
ICCV 2001, vol. 2, 747–747 (2001). https://doi.org/10.1109/ICCV.2001.937709.
	14.	 Lin, S.-F., Chen, J.-Y. & Chao, H.-X. Estimation of number of people in crowded scenes using perspective transformation. IEEE 
Trans. Syst. Man Cybern. Part A 31, 645–654 (2001).
	15.	 Felzenszwalb, P. F., Girshick, R. B., McAllester, D. & Ramanan, D. Object detection with discriminatively trained part-based 
models. IEEE Trans. Pattern Anal. Mach. Intell. 32, 1627–1645. https://doi.org/10.1109/TPAMI.2009.167 (2010).
	16.	 Topkaya, I. S., Erdogan, H. & Porikli, F. Counting people by clustering person detector outputs. In 2014 11th IEEE International 
Conference on Advanced Video and Signal Based Surveillance (AVSS), 313–318 (2014). https://doi.org/10.1109/AVSS.2014.6918687.
	17.	 Paragios, N. & Ramesh, V. A mrf-based approach for real-time subway monitoring. In Proceedings of the 2001 IEEE Computer 
Society Conference on Computer Vision and Pattern Recognition. CVPR 2001, vol. 1, I–I (2001). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​.​2​0​0​
1​.​9​9​0​6​4​4​.​
	18.	 Tian, Y., Sigal, L., Badino, H., la Torre, F. D. & Liu, Y. Latent gaussian mixture regression for human pose estimation. In ACCV 
(2010).
	19.	 Chen, K., Loy, C. C., Gong, S. & Xiang, T. Feature mining for localised crowd counting. In BMVC (2012).
	20.	 Davies, A. C., Yin, J. H. & Velastín, S. A. Crowd monitoring using image processing. Electron. Commun. Eng. J. 7, 37–47 (1995).
	21.	 Chan, A. B. & Vasconcelos, N. Bayesian poisson regression for crowd counting. In 2009 IEEE 12th International Conference on 
Computer Vision, 545–551 (2009). https://doi.org/10.1109/ICCV.2009.5459191.
	22.	 Shami, M. B., Maqbool, S., Sajid, H., Ayaz, Y. & Cheung, S.-C.S. People counting in dense crowd images using sparse head 
detections. IEEE Trans. Circuits Syst. Video Technol. 29, 2627–2636. https://doi.org/10.1109/TCSVT.2018.2803115 (2019).
	23.	 Sajid, U., Sajid, H., Wang, H. & Wang, G. ZoomCount: A zooming mechanism for crowd counting in static images. IEEE Trans. 
Circuits Syst. Video Technol. 30, 3499–3512. https://doi.org/10.1109/TCSVT.2020.2978717 (2020).
	24.	 Khan, M. A., Menouar, H. & Hamila, R. Revisiting crowd counting: State-of-the-art, trends, and future perspectives. Image Vis. 
Comput. 129, 104597 (2023).
	25.	 Khan, M. A., Menouar, H. & Hamila, R. Visual crowd analysis: Open research problems. AI Mag. 44, 296–311 (2023).
	26.	 Zhang, Y., Zhou, D., Chen, S., Gao, S. & Ma, Y. Single-image crowd counting via multi-column convolutional neural network. In 
2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 589–597 (2016). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​.​2​0​1​6​.​
7​0​.​
	27.	 Li, Y., Zhang, X. & Chen, D. CSRNet: Dilated convolutional neural networks for understanding the highly congested scenes. In 
2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition 1091–1100 (2018).
	28.	 Cao, X., Wang, Z., Zhao, Y. & Su, F. Scale aggregation network for accurate and efficient crowd counting. In ECCV (2018).
	29.	 Zheng, H., Lin, Z., Cen, J., Wu, Z. & Zhao, Y. Cross-line pedestrian counting based on spatially-consistent two-stage local crowd 
density estimation and accumulation. IEEE Trans. Circuits Syst. Video Technol. 29, 787–799. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​C​S​V​T​.​2​0​1​8​.​
2​8​0​7​8​0​6​ (2019).
	30.	 Yan, Z. et al. Perspective-guided convolution networks for crowd counting. In 2019 IEEE/CVF International Conference on 
Computer Vision (ICCV), 952–961 (2019).
	31.	 Jiang, X. et al. Attention scaling for crowd counting. In 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition 
(CVPR), 4705–4714 (2020).
	32.	 Wang, Q. & Breckon, T. Crowd counting via segmentation guided attention networks and curriculum loss. IEEE Trans. Intell. 
Transp. Syst. 23, 15233–15243 (2022).
	33.	 Zhang, A., Xu, J., Luo, X., Cao, X. & Zhen, X. Cross-domain attention network for unsupervised domain adaptation crowd 
counting. IEEE Trans. Circuits Syst. Video Technol. 32, 6686–6699. https://doi.org/10.1109/TCSVT.2022.3179824 (2022).
	34.	 Zhai, W., Xing, X. & Jeon, G. Region-Aware Quantum Network for Crowd Counting. IEEE Trans. Consum. Electron. 70, 5536–5544 
(2024).
	35.	 Simonyan, K. & Zisserman, A. Very deep convolutional networks for large-scale image recognition. In 3rd International Conference 
on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings (2015).
	36.	 Szegedy, C. et al. Going deeper with convolutions. In 2015 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 
1–9 (2015).
	37.	 Redmon, J., Divvala, S. K., Girshick, R. B. & Farhadi, A. You only look once: Unified, real-time object detection. In 2016 IEEE 
Conference on Computer Vision and Pattern Recognition (CVPR), 779–788 (2016).
	38.	 Badrinarayanan, V., Handa, A. & Cipolla, R. Segnet: A deep convolutional encoder-decoder architecture for robust semantic pixel-
wise labelling. ArXiv ArXiv:1505.07293 (2015).
	39.	 Gao, J., Wang, Q. & Li, X. PCC Net: Perspective crowd counting via spatial convolutional network. IEEE Trans. Circuits Syst. Video 
Technol. 30, 3486–3498. https://doi.org/10.1109/TCSVT.2019.2919139 (2020).
	40.	 Tripathy, S. K., Srivastava, S., Bajaj, D. & Srivastava, R. A novel cascaded deep architecture with weak-supervision for video crowd 
counting and density estimation. Soft. Comput. 28, 8319–8335. https://doi.org/10.1007/s00500-024-09681-4 (2024).
	41.	 Tripathy, S. K. & Srivastava, R. AMS-CNN: Attentive multi-stream CNN for video-based crowd counting. Int. J. Multimed. Inf. Retr. 
10, 239–254. https://doi.org/10.1007/s13735-021-00220-7 (2021).
Scientific Reports |        (2025) 15:11932 
14
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 15

	42.	 Tripathy, S. K., Srivastava, S. & Srivastava, R. MHAMD-MST-CNN: Multiscale head attention guided multiscale density maps 
fusion for video crowd counting via multi-attention spatial-temporal CNN. Comput. Methods Biomech. Biomed. Eng. Imaging 
Visualization 11, 1777–1790. https://doi.org/10.1080/21681163.2023.2188971 (2023).
	43.	 Zhai, W. et al. Scale attentive aggregation network for crowd counting and localization in smart city. ACM Trans. Sen. 
Netw.[SPACE]https://doi.org/10.1145/3653454 (2024).
	44.	 Zhai, W., Gao, M., Li, Q., Jeon, G. & Anisetti, M. FPANet: Feature pyramid attention network for crowd counting. Appl. Intell. 53, 
19199–19216 (2023).
	45.	 Zhai, W., Gao, M., Guo, X., Li, Q. & Jeon, G. Scale-context perceptive network for crowd counting and localization in smart city 
system. IEEE Internet Things J. 10, 18930–18940 (2023).
	46.	 Jiang, S., Wang, Q., Cheng, F., Qi, Y. & Liu, Q. A unified object counting network with object occupation prior. IEEE Trans. Circuits 
Syst. Video Technol. 34, 1147–1158. https://doi.org/10.1109/TCSVT.2023.3291824 (2024).
	47.	 Khan, M. A., Menouar, H. & Hamila, R. Crowd density estimation using imperfect labels. In 2023 IEEE International Conference 
on Consumer Electronics (ICCE), 1–6 (IEEE, 2023).
	48.	 Buciluundefined, C., Caruana, R. & Niculescu-Mizil, A. Model compression. In Proceedings of the 12th ACM SIGKDD International 
Conference on Knowledge Discovery and Data Mining, KDD ’06, 535-541 (Association for Computing Machinery, New York, NY, 
USA, 2006). https://doi.org/10.1145/1150402.1150464.
	49.	 Zagoruyko, S. & Komodakis, N. Paying more attention to attention: Improving the performance of convolutional neural networks 
via attention transfer. ArXiv ArXiv: 1612.03928 (2016).
	50.	 Huang, Z. & Wang, N. Like what you like: Knowledge distill via neuron selectivity transfer. arXiv preprint arXiv:1707.01219 
(2017).
	51.	 Passalis, N. & Tefas, A. Learning deep representations with probabilistic knowledge transfer. In European Conference on Computer 
Vision (2018).
	52.	 Zhang, C. & Peng, Y. Better and faster: Knowledge transfer from multiple self-supervised learning tasks via graph distillation for 
video classification. In International Joint Conference on Artificial Intelligence (2018).
	53.	 Mirzadeh, S. I. et al. Improved knowledge distillation via teacher assistant. In AAAI Conference on Artificial Intelligence (2019).
	54.	 Chen, X., Su, J. & Zhang, J. A two-teacher framework for knowledge distillation. In International Symposium on Neural Networks 
(2019).
	55.	 Theis, L., Korshunova, I., Tejani, A. & Huszár, F. Faster gaze prediction with dense networks and fisher pruning. ArXiv ArXiv: 
1801.05787 (2018).
	56.	 Ashok, A., Rhinehart, N., Beainy, F. N. & Kitani, K. M. N2n learning: Network to network compression via policy gradient 
reinforcement learning. ArXiv ArXiv: 1709.06030 (2017).
	57.	 Saputra, M. R. U., Gusmao, P., Almalioglu, Y., Markham, A. & Trigoni, N. Distilling knowledge from a deep pose regressor network. 
In 2019 IEEE/CVF International Conference on Computer Vision (ICCV), 263–272 (2019). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​C​C​V​.​2​0​1​9​.​0​0​0​3​
5​.​
	58.	 Cheng, Y., Wang, D., Zhou, P. & Zhang, T. Model compression and acceleration for deep neural networks: The principles, progress, 
and challenges. IEEE Signal Process. Mag. 35, 126–136. https://doi.org/10.1109/MSP.2017.2765695 (2018).
	59.	 Takamoto, M., Morishita, Y. & Imaoka, H. An efficient method of training small models for regression problems with knowledge 
distillation. In 2020 IEEE Conference on Multimedia Information Processing and Retrieval (MIPR), 67–72 (2020). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​1​0​9​/​M​I​P​R​4​9​0​3​9​.​2​0​2​0​.​0​0​0​2​1​.​
	60.	 Shen, Z., Li, G., Xia, R., Meng, H. & Huang, Z. A lightweight object counting network based on density map knowledge distillation. 
IEEE Trans. Circuits Syst. Video Technol.[SPACE]https://doi.org/10.1109/TCSVT.2024.3469933 (2024).
	61.	 Mehta, S. & Rastegari, M. MobileViT: Light-weight, general-purpose, and mobile-friendly vision transformer. In International 
Conference on Learning Representations (2022).
	62.	 Gao, J. et al. Forget less, count better: A domain-incremental self-distillation learning benchmark for lifelong crowd counting. 
Front. Inf. Technol. Electron. Eng. 24, 187–202 (2022).
	63.	 Shi, Z., Mettes, P. & Snoek, C. G. M. Focus for free in density-based counting. Int. J. Comput. Vis. 132, 2600–2617. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​0​0​7​/​s​1​1​2​6​3​-​0​2​4​-​0​1​9​9​0​-​3​ (2024).
	64.	 Khan, M. A., Menouar, H. & Hamila, R. Revisiting crowd counting: State-of-the-art, trends, and future perspectives. Image Vis. 
Comput. 129, 104597 (2022).
	65.	 Chen, K., Loy, C. C., Gong, S. & Xiang, T. Feature mining for localised crowd counting. In Proceedings of the British Machine Vision 
Conference, 21.1–21.11 (BMVA Press, 2012).
	66.	 Hsieh, M.-R., Lin, Y.-L. & Hsu, W. H. Drone-based object counting by spatially regularized regional proposal network. 2017 IEEE 
International Conference on Computer Vision (ICCV) 4165–4173 (2017).
	67.	 Peng, T., Li, Q. & Zhu, P. RGB-T crowd counting from drone: A benchmark and mmccn network. In Computer Vision - ACCV 
2020: 15th Asian Conference on Computer Vision, Kyoto, Japan, November 30 - December 4, 2020, Revised Selected Papers, Part VI, 
497–513 (Springer-Verlag, Berlin, Heidelberg, 2020).
	68.	 Riis. Aerial sheep dataset. https://universe.roboflow.com/riis/aerial-sheep (2022). Visited on 2024-02-23.
	69.	 Malik, J., Kiranyaz, S. & Gabbouj, M. Self-organized operational neural networks for severe image restoration problems. Neural 
Netw. 135, 201–211 (2021).
	70.	 Wen, L. et al. Detection, tracking, and counting meets drones in crowds: A benchmark. In 2021 IEEE/CVF Conference on Computer 
Vision and Pattern Recognition (CVPR), 7808–7817 (2021).
Acknowledgements
This publication was made possible by the PDRA award PDRA7-060621012 from the Qatar National Research 
Fund (a member of The Qatar Foundation). The statements made herein are solely the responsibility of the au­
thors. Open Access funding provided by the Qatar National Library.
Author contributions
M. A. Khan wrote the main manuscript text and conducted the experiment. H. Menouar, R. Hamila, and A. Abu-
Dayya contributed to the problem formulation and reviewed the paper.
Funding
Open Access funding provided by the Qatar National Library.
Declarations
Competing interests
The authors declare no competing interests.
Scientific Reports |        (2025) 15:11932 
15
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/


## Page 16

Additional information
Correspondence and requests for materials should be addressed to M.A.K.
Reprints and permissions information is available at www.nature.com/reprints.
Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and 
institutional affiliations.
Open Access   This article is licensed under a Creative Commons Attribution 4.0 International License, which 
permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give 
appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and 
indicate if changes were made. The images or other third party material in this article are included in the article’s 
Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included 
in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or 
exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy 
of this licence, visit http://creativecommons.org/licenses/by/4.0/.
© The Author(s) 2025 
Scientific Reports |        (2025) 15:11932 
16
| https://doi.org/10.1038/s41598-025-90750-5
www.nature.com/scientificreports/
