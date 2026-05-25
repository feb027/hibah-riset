---
source_id: S027
title: Deep learning for crowd counting in complex environments: challenges and novel trends
source_url: https://link.springer.com/content/pdf/10.1007/s10791-026-09928-8.pdf
source_file: docs/research/papers/S027-deep-learning-for-crowd-counting-in-complex-environments-challenges-an.pdf
source_kind: pdf
extraction_note: downloaded PDF
---

# Extracted text: S027-deep-learning-for-crowd-counting-in-complex-environments-challenges-an.pdf
## PDF metadata
- format: PDF 1.4
- creator: Adobe InDesign 18.3 (Windows)
- producer: Adobe PDF Library 17.0; modified using iText® 5.5.13.4 ©2000-2024 iText Group NV (SPRINGER SBM; licensed version)
- creationDate: D:20260216175438+01'00'
- modDate: D:20260217110055+01'00'


## Page 1

REVIEW
Open Access
© The Author(s) 2026. Open Access  This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International 
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate 
credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. 
You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party 
material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material 
is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted 
use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit ​h​t​t​p​:​/​/​c​r​e​a​t​i​v​e​c​o​m​m​o​n​s​.​o​r​g​/​l​i​c​e​n​s​
e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/.
Elsepae et al. Discover Computing          (2026) 29:101 
https://doi.org/10.1007/s10791-026-09928-8
*Correspondence:
Heba F. Elsepae
heba.abdelhameed@eng.aswu.
edu.eg
Ehab K. I. Hamad
e.hamad@aswu.edu.eg
1Electrical Engineering Department, 
Faculty of Engineering, Aswan 
University, Aswan 81542, Egypt
2Faculty of Computer Studies, Arab 
Open University, 11681 Riyadh, 
Saudi Arabia
3Department of Electronics 
and Electrical Communications 
Engineering, Faculty of Electronic 
Engineering, Menoufia University, 
Menouf 32952, Egypt
Deep learning for crowd counting in complex 
environments: challenges and novel trends
Heba F. Elsepae1*
, Heba M. El-Hoseny2
, Ehab K. I. Hamad1*
 and El-Sayed M. El-Rabaie3
1  Introduction
A good way to define a crowd is by distinguishing it from a group, as illustrated in Table 
1. A group is a collection of people, ranging from two to hundreds, who are together at 
the same time, interacting socially. They stay close to each other, move at similar speeds, 
and in the same direction. A crowd denotes a large group of people who have gathered 
in one spot, often sharing a common purpose or interest. Individual identities can merge 
into a collective entity, leading to shared behaviors and actions, which are discussed in 
[1].
Crowd analysis involves estimating the number and spatial distribution of people in 
areas such as social places. CC becomes challenging in harsh scenes; these issues require 
Discover Computing
Abstract
Crowd counting is a challenging task, especially when accurately estimating the 
number of people in large crowds under diverse environmental conditions. Factors 
such as harsh lighting, crowded spaces, adverse weather, and varying perspectives 
make it difficult for traditional methods to count individuals reliably. Modern 
solutions leverage deep learning models, including hybrid approaches, to overcome 
these challenges. A significant advancement in this area is the use of attention 
mechanisms, which enable models to focus on the most relevant regions of the 
crowd, improving counting accuracy. Additionally, curriculum learning, which 
gradually introduces complexity during training, enhances model performance in 
unpredictable environments. Another notable improvement is the combination 
of Generative Adversarial Networks with the U-Net architecture, which generates 
synthetic data to improve training and generalization. Hybrid deep learning 
approaches that integrate adaptive curriculum learning and attention mechanisms 
have shown promising results in handling diverse scenarios. Moreover, incorporating 
fuzzy methods into preprocessing enables better handling of varying densities, 
crowd behaviors, and illumination conditions, leading to more accurate crowd 
counting across a wide range of environments. By integrating these advanced 
techniques, researchers can address current limitations and improve the robustness 
and real-world applicability of crowd counting models.
Keywords  Crowd counting, Deep learning (DL), Dense crowd monitoring, Detection-
based tracking, Lightweight network, Crowd density estimation


## Page 2

Page 2 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
advanced DL methods for accurate results. Crowd density estimation (CDE) focuses on 
generating density maps to show people’s distribution, which are useful for traffic and 
safety management, which are introduced in [2]. CNN-based methods, which are pre­
sented in [3] are widely used for generating density maps, while transformer-based mod­
els are proposed in [4]. GAN-UNet utilizes GANs to generate realistic crowd images and 
enhance density maps in unevenly distributed areas. Various training strategies enhance 
CC model performance: Curriculum Learning improves generalization by gradually 
increasing task difficulty; Standard DL is simple but may struggle with complex cases; 
Adaptive Learning adjusts to data complexity but requires monitoring; and Multi-task 
Learning improves accuracy by training on related tasks like movement or density, but 
adds complexity [5].
A chronology of CC methods is shown in Fig. 1. Traditional approaches (pre-2015) 
included regression-based techniques such as Multi-Level Regression (MLR), Ker­
nel Ridge Regression (KRR), and Ridge Regression (RR), that shown in [6]. Chan et al. 
applied learning-based estimation, while Lempitsky et al. reviewed in [7] combined 
regression with feature learning. Context-Aware Ridge Regression (CA-RR) and Count 
are discussed in [8] improved performance by using context and decision forests. Cross-
scene counting was explored by Wang et al. in [9] and Fu et al. presented [10]. In 2015, 
DL methods emerged with MCNN and Hydra-CNN [11], which introduced multi-
branch architectures. Between 2016 and 2018, models like Switching CNN, CP-CNN, 
and CSRNet were introduced in [12], and SANet advanced CC through mechanisms like 
switching, contextual pyramids, and dilated convolutions. Recent models (2019–pres­
ent) include PSSDN, which was published in [13], which uses point-level supervision. 
Transformer-based models analyzed in [14], which have become promising alternatives 
to CNNs due to their self-attention mechanism. TransCrowd, that discussed in [15] uses 
Table 1  Group and crowd characteristics: a comparative overview
Aspect
Group
Crowd
Purpose
Formed with a specific purpose or goal
Often forms spontaneously or 
for an event/situation
Size and structure
Generally smaller and more manageable
Larger in size and often lacks 
formal structure
Identity and unity
Members maintain individual identities while 
contributing to group identity
Individual identities may 
merge into a collective identity
Duration and stability
More stable over time with ongoing membership Based on condition changes
Examples
Work teams, clubs, and organizations
Sporting and social occasions
Fig. 1  A concise timeline of crowd counting developments
 


## Page 3

Page 3 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
weak supervision, CrowdFormer combines Transformers with overlapping convolu­
tions, and other hybrid models, which are covered in [16] merge Transformer and CNN 
features or use local attention to better handle dense crowds and complex backgrounds.
In preparing this review, we adopted a narrative review approach while ensuring a 
structured and transparent selection process. Relevant articles were identified through 
searches in major scientific databases, including IEEE Xplore, Scopus, Web of Science, 
and Google Scholar. The search covered publications from 2010 to 2025 using keywords 
such as crowd counting, density estimation, computer vision, deep learning, and surveil­
lance. To maintain quality, we included only peer-reviewed journal articles and reputable 
conference proceedings, while excluding preprints and non-scholarly sources. Further­
more, studies were selected if they directly addressed crowd counting methods, datasets, 
or applications, whereas works with limited relevance or lacking methodological con­
tributions were not considered. Although this work is narrative rather than systematic, 
we strived to provide comprehensive and balanced coverage of the most influential and 
recent contributions in the field.
1.1  This work offers the following major contributions
In this review, we present various crowd-counting methods, including detection-based 
approaches for sparse crowds, regression-based methods for density mapping, and den­
sity-estimation techniques for complex scenarios. We highlight recent advancements, 
including conventional neural networks for feature extraction, attention mechanisms 
for improved focus, and multi-scale approaches to handle density variations. Detec­
tion and tracking techniques are also emphasized, enabling accurate localization and 
monitoring of individuals in videos, which is essential for real-time crowd analysis. We 
discuss the main challenges in crowd counting and identify emerging trends, including 
integrating deep learning with attention mechanisms and combining Fuzzy logic with 
preprocessing techniques to achieve high counting performance in diverse and complex 
environments. Finally, we explore research strategies involving optimal hyperparameter 
selection and adaptive curriculum learning to enhance counting accuracy and overall 
system performance.
The remainder of this survey is organized as follows: Section 2 presents the literature 
review, Sect. 3 introduces the evaluation metrics, Sect. 4 describes the datasets, Sect. 5 
reviews deep learning approaches, Sect. 6 discusses challenges in complex environments 
and highlights recent trends in crowd counting, while Sect. 7 concludes the paper.
2  Literature review
2.1  Comparative review of previous surveys
Recent research on crowd counting has evolved from classical image-processing tech­
niques toward deep learning and lightweight deployment strategies. Early works laid the 
foundation by linking traditional density estimation with regression- and density-based 
models, while more recent surveys critically examined deep networks, attention mecha­
nisms, offering taxonomies and clarifying trade-offs between annotation cost, scalabil­
ity, and performance. Specialized studies addressed real-time and lightweight solutions, 
where methods such as compression-based networks, TinyCount, curriculum reinforce­
ment learning, and knowledge distillation with multi-modal inputs demonstrated effi­
ciency but still faced challenges in dense or cluttered scenes, training complexity, and 


## Page 4

Page 4 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
data availability. Broader reviews further emphasized deployment on edge devices, 
highlighting opportunities but also gaps in benchmarking under real-world conditions. 
Building on these insights, our survey advances the field by integrating curriculum learn­
ing and fuzzy logic into preprocessing and deep learning pipelines, alongside hybrid 
attention mechanisms such as CANNet, EfficientNet, and VGG16. This combined strat­
egy achieves stronger performance in complex scenarios, and as summarized in Table 2, 
offers clearer contributions compared to previous surveys in terms of focus, strengths, 
limitations, and practical relevance.
2.2  Crowd counting strategies
Crowd counting (CC) is about figuring out how many people are in a place using com­
puter technology and artificial intelligence. It uses different methods; one identifies each 
person, another estimates the number from the image’s features, and another creates a 
map showing where people are. Advanced techniques [32], involve using special types of 
neural networks to get better results. These methods are used in public safety, managing 
events, city planning, and understanding human behavior in stores. Researchers are con­
stantly working to make these techniques more accurate and efficient; the methodolo­
gies can be illustrated in Fig. 2.
2.3  Traditional methods categories
2.3.1  Detection-based vs. heatmap-based approaches
Crowd detection methods, as discussed in [33], include both whole-body and partial-
body approaches. Whole-body detection struggles with occlusions in dense crowds, 
which affects accuracy. Some studies, summarized below, explain various detection-
based approaches used in crowd counting. It includes three methods: Haar wave­
lets, HOGs (Histogram of Oriented Gradients), and Support Vector Machines (SVM) 
explained in Eq. (1). Haar wavelets work well for whole-body detection in sparse crowds 
but struggle in dense crowds due to occlusion. HOGs allow for partial body-based detec­
tion by focusing on body parts like the head and arms, helping to handle occlusions. 
Support Vector Machines are mentioned as a detection-based method that also faces 
challenges with occlusion, but regression-based approaches are suggested as a potential 
solution to this limitation.
In the field of crowd counting, two main methodological approaches are commonly 
employed: detection-based approaches and heatmap-based approaches. Detection-
based methods, such as YOLO or Faster R-CNN, focus on identifying and localizing 
people by drawing bounding boxes around people. These techniques are particularly 
effective in low-density crowd regions where individuals are more separated, and the 
issue of occlusion is relatively minor. One of the key advantages of detection-based 
approaches is that they not only provide the overall crowd count but also yield precise 
information about the location of.
In crowd counting, there are two main approaches: detection-based and heatmap-
based methods. Detection-based methods, like YOLO and Faster R-CNN, detect each 
person with boxes. They work well in small crowds and give the exact location of every­
one, but they struggle in very dense crowds. Heatmap-based methods create a density 
map instead of detecting each person. They work better in large, crowded scenes and can 
estimate the number of people even when individuals are hard to see, but they do not 


## Page 5

Page 5 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Ref/Year
Topic
Pros
Cons
Gap analysis
[17]
2019
General advances in 
density estimation via 
image processing
Broad overview; links 
traditional to deep learn­
ing methods; mentions 
applications
Limited dataset 
depth; lacks critical 
comparisons
Provides starting 
points for new 
researchers
[18]
2023
Algorithms for 
counting and density 
estimation in dense 
crowds
Explains transition from 
classical to DL; robustness 
in dense scenarios
Earlier surveys were 
only taxonomic, 
with little evaluation
Complement others 
by algorithm-level 
pros/cons
[19] 2023
Regression-based 
approaches
Explain the shift from 
detection to regression; 
historical context
Earlier surveys gave 
little detail
Highlights regression 
as a foundation of 
modern methods
[20] 2023
Deep networks ap­
plied to counting & 
density maps
Combines both perspec­
tives; notes strengths/
weaknesses
Earlier works sepa­
rated them; they 
lacked a unified 
view
Provides integrated 
analysis with updated 
DL methods
[21] 2024
Learning paradigms 
for crowd counting
Shows trade-offs between 
annotation effort vs. 
performance; structured 
grouping
Previous surveys 
were biased toward 
supervised only
Adds by analyzing 
weakly/unlabeled 
data strategies and 
future directions
[22] 2024
Role of DL in crowd 
counting, specifically
CNN, GAN attention; em­
phasizes DL progress
Past surveys 
were general, not 
DL-specific
Clarifies DL’s central 
role, challenges 
(domain adaptation, 
scalability)
[23]
2024
Lightweight dense 
crowd density estima­
tion network with 
model compression
Strong memory efficiency 
with effective model 
compression
Compression may 
reduce the ability 
to capture subtle 
crowd details
Requires further test­
ing on unconstrained 
real-world datasets to 
ensure reliability
[24]
2024
TinyCount: an ef­
ficient real-time CC 
network for intelligent 
surveillance
Extremely lightweight and 
optimized for real-time 
edge surveillance
May sacrifice ac­
curacy in extremely 
dense or highly clut­
tered crowds
Need better trade-off 
strategies between 
efficiency and fine-
grained accuracy
[1]
2025
DL methods for den­
sity maps + counting
Covers CNN, RNN, at­
tention; and structured 
categorization
Earlier works lacked 
DL depth and 
comparison
Provides up-to-date 
taxonomy with pros/
cons
[25]
2025
Comprehensive survey 
of crowd density esti­
mation & counting
Broad coverage of classi­
cal + DL methods; datasets, 
losses, metrics included
Some redundancy 
with earlier surveys
It explains all the 
methods in one 
organized view
[1]
2025
Survey of DL methods 
for density estimation
In-depth algorithmic 
analysis of > 300 papers; 
structured taxonomy
Heavy focus on CNN 
methods; limited 
edge-case scenarios
It compares them 
clearly and shows 
pros and cons
[26]
2025
Crowd counting at 
the edge (knowledge 
distillation)
Highlights lightweight 
approaches; links edge 
computing with counting
Not a full gen­
eral survey; more 
topic-focused
It shows if they can be 
used easily and don’t 
waste much energy
[27]
2025
DL in image process­
ing (general survey)
Wide coverage beyond 
counting (segmentation, 
detection, etc.); updated 
taxonomy
Less specific to 
crowd counting
It shows how deep 
learning works for 
other areas
[28]
2025
A comprehensive 
survey of lightweight 
neural networks for 
crowd counting
Provides a structured 
taxonomy and highlights 
trends in lightweight CC 
models
Lacks experimental 
benchmarking; no 
novel algorithm 
introduced
Missing a unified 
performance com­
parison across various 
datasets
[29]
2025
Lightweight dynamic 
convolutional network 
enhanced with cur­
riculum reinforcement 
learning
Adapts dynamically to 
varying crowd scenes; cur­
riculum RL improves con­
vergence and robustness
Training process 
is complex, and 
reinforcement learn­
ing requires careful 
tuning
Needs large-scale 
validation on dense 
and highly diverse 
datasets to prove 
scalability
Table 2  List of previous and state-of-the-art survey papers: pros, cons, and contributions to the 
scientific community


## Page 6

Page 6 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
show exact locations, which were introduced in [34], estimate a continuous density map 
or heatmap over the crowd image rather than attempting to detect everyone separately.
f (x) = w · x + b

(1)
x is the feature vector extracted from the image, w is the weight vector learned during 
the training phase, b is the bias term, f(x) is the decision function of an SVM.
2.3.2  Regression-based approaches
Learn the regression of crowd image features to the crowd count using three steps: 
first, foreground extraction, which isolates important parts of the image, like the crowd, 
from the background. Second, there is feature learning, where meaningful features are 
extracted from the foreground mask to estimate the crowd count. Lastly, counting regres­
sion features involves studying regression-based approaches in CC, such as dynamic tex­
ture, wavelet analysis, and Gaussian regression. The dynamic texture approach improves 
occlusion handling but sacrifices accuracy in localizing individuals and understanding 
crowd distributions, while wavelet analysis and Gaussian regression are also widely used 
methods which proposed in [19, 35].
Fig. 2  Taxonomy of crowd counting strategies
 
Ref/Year
Topic
Pros
Cons
Gap analysis
[30]
2025
Mutual head knowl­
edge distillation frame­
work for lightweight 
RGB-T
Efficiently fuses RGB and 
thermal modalities; distilla­
tion reduces computational 
burden
Depending on dual-
modal input, which 
is not always avail­
able in real-world 
setups
Lack of lightweight 
single-modality 
models for adverse 
conditions
[31]
2025
Review of AI edge de­
vices and lightweight 
CNN/LLM deployment
Provides insights into hard­
ware–software co-design 
and real-world feasibility
Broad focus on AI 
deployment, limited 
attention to crowd 
counting specifically
It misses testing the 
models on small/real 
devices
Table 2  (continued)
 


## Page 7

Page 7 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
2.3.3  Density estimation-based methods
Estimate how crowded an area is instead of counting each person. Use heat maps to 
show the CD. It is good for very large and dense crowds; some studies have presented 
various density estimation-based methods for CC, emphasizing their effectiveness in 
large and dense crowds. The methods listed include MCCNN to capture features at 
different scales and combining conventional and dilated CNNs for enhanced receptive 
fields. TEDNet, which was introduced in [36] utilizes a trellis encoder-decoder network 
to improve spatial relationship accuracy in density maps, while HA-CCN is explained in 
[37], employs a hierarchical attention-based network to focus on relevant image regions.
2.3.4  Tracking-based methods
To enhance crowd counting systems, integrating Object Tracking is essential for moni­
toring individual movements across video frames. This approach, known as Track­
ing-by-Detection, involves detecting individuals in each frame and associating these 
detections over time to maintain consistent identities. Key tracking algorithms include: 
Kalman Filter: Predicts an object’s future position based on its current state, effectively 
handling linear motion and occlusions. This filter can be introduced in [38]. Deep SORT 
enhances tracking by incorporating appearance features through a deep learning model, 
improving re-identification in crowded scenarios. This is discussed in [39].
Byte Track: employs a novel association method that considers all detection boxes, 
including low-confidence ones, to reduce identity switches and improve tracking accu­
racy. Integrating these tracking methods with detection-based approaches and enhance­
ment processes, such as fuzzy, that were proposed in [40], enables not only accurate 
crowd counting but also detailed analysis of individual trajectories and behaviors, which 
is crucial for applications like surveillance and crowd management.
2.4  Deep learning strategies
These initial models created a foundation for future research but faced challenges with 
varying head sizes, uneven density distributions, and large perspective changes. As the 
field developed, newer CNN architectures were designed to tackle these issues more 
effectively, incorporating techniques such as multi-scale architectures, feature fusion, 
and attention mechanisms. Notable examples include MCNN [41] and CSRNet [42], 
which successfully applied these methods and achieved better counting accuracy in 
complex scenarios.
The second part focuses on more recent innovations in CC that go beyond traditional 
CNN approaches. Researchers are now combining CNNs with RNNs to improve tem­
poral predictions and using transformers to gain a better understanding of the over­
all scene. GANs, as shown in [43], are also used to generate synthetic data to enhance 
accuracy. New strategies, such as weakly supervised learning and methods that require 
fewer labeled data, have made the models more efficient. Future trends may include 3D 
modeling, faster real-time processing, and better adaptability to different environments. 
Crowd-counting methods use deep learning models and can be grouped into several 
categories:


## Page 8

Page 8 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
2.4.1  Basic CNN
A CNN is a DL model that excels at processing images by automatically learning to iden­
tify important features like edges and shapes. It works by using convolutional layers to 
scan the image and detect key details, pooling layers to simplify the data by focusing on 
the most important information, and fully connected layers to make a final prediction, 
such as counting the number of people in a crowd.
A conventional neural network is a deep learning model that processes images by 
automatically learning to detect important features like edges and shapes. In CC, CNNs 
work by first analyzing an image of a crowd through layers that highlight different 
details. Instead of directly counting people, many CNNs for CC produce a density map 
calculated by Eqs. (2) and (3). Each pixel in this map represents the estimated number of 
people at that location in the original image, as shown in [44, 45]. Finally, it sums up the 
values in the density map to give the total count of people in the image.
Figure 3 shows the steps for counting and estimating crowds. Traditional methods 
often have trouble counting people in very crowded scenes. To solve this, Wang et al. [9] 
introduced a deep regression network that works well in dense crowds by using a simple 
CNN to extract features efficiently. To make the method more robust, they also trained 
the CNN with images that had no people, giving them a count of zero. This reduced false 
alarms, and on the UCF-CC dataset, the method improved performance by almost 50% 
compared to a CNN trained without these negative samples [46].
Fu et al. [10] made an enhancement to crowd density estimation (CDE) by enhancing 
the network design and classification process. They removed redundant connections in 
the network using a similarity matrix, which made the network faster without reducing 
accuracy. They also added a two-stage classification: the first stage handles easy samples, 
and the second stage focuses on harder samples for more precise results. This method 
was tested on three datasets: PETS2009 (surveillance footage), Subway (subway scenes), 
and Chunxi Road (busy street), and showed significant improvements in both speed and 
accuracy of counting crowds.
D (x, y) = fCNN (I (x, y)) .

(2)
D (x, y) is the density map at pixel (x, y) I (x, y) is the input image at pixel. (x, y), fCNN 
is represents the CNN model used to generate the density map.
Fig. 3  Architecture of convolutional neural network for crowd density estimation
 


## Page 9

Page 9 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
ˆN =
W
∑
x=1
H
∑
y=1
D (x,)

(3)

N is the estimated total count of people, (W, H) is the width and height of the density 
map D (x, y).
L = 1
N
N

i=1

Ni −Ni
 + λ
N

j=1

Nj −0


(4)
L is the loss function, 
Ni is the predicted count for the (ith) image, Ni ground 
truth counts for the ith image, 
Nj is the predicted count for the jth negative sample 
(should be close to zero), λ is a regularization parameter to control the importance of 
negative samples.
2.4.2  Multi column CNN (MC-CNN)
The MC-CNN uses multiple parallel columns to process images, capturing features like 
textures and edges. These features are combined in a fusion layer to produce detailed 
density maps, as shown in Fig. 4. Each column uses different filters to learn complex pat­
terns, making predictions more accurate [41, 47].
The Relational Attention Network (RANet) [48, 49] applies self-attention (Eq. 5) to 
capture pixel relationships locally and globally, reducing noise and improving accuracy. 
In real-world crowds, densities vary, so DecideNet [34] combines detection and regres­
sion methods with an attention module to handle both low- and high-density areas 
effectively.
Crowd localization is enhanced by the Dilated Convolutional Swin Transformer 
(DCST) [31, 50], which integrates dilated convolutions Eq. (6) and transformers to cap­
ture broader context, improving counting accuracy even with occlusion and blur.
Although MC-CNNs are effective, they are complex and resource-heavy. Single-col­
umn CNNs (SC-CNNs) simplify training while maintaining good performance. The 
Double Multi-Scale Feature Fusion Network (DMFFNet) [51] uses VGG19 features, 
attention mechanisms, and a new loss function to create better density maps, outper­
forming previous methods.
Fig. 4  Detailed structure of the multi-column CNN (MC-CNN) for crowd counting
 


## Page 10

Page 10 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
A (x, y) = Softmax
(
Q (x, y) · K(x, y)T
√dk
)
· V (x, y)

(5)
Q (x, y), K (x, y), and V (x, y) is the query, key, and value feature maps, respectively. dk​ 
is the dimension of the key vector, A (x, y) is the attention map.
y (m, n) =
M
∑
i=1
N
∑
j=1
x (m + r × i, n + r · j) w (i, j)

(6)
The input x (m, n) has dimensions M and N, and the output y (m, n) is calculated.
using the convolution kernel w (i, j). The parameter r controls the dilation rate.
2.4.3  Single column CN
A SC-CNN is a neural network that uses just one column of layers to analyze images. 
This approach simplifies the network while effectively estimating CD and handling key 
issues in CC. SC-CNNs work by taking an image and passing it through one series of lay­
ers. First, convolutional layers scan the image to find features like edges. Then, pooling 
layers reduce the size of the image to make processing faster. After that, fully connected 
layers use the features to make predictions or classifications. This simple, single-path 
approach makes the network easy to use and quick to run. These steps can be drawn as 
in Fig. 5.
There are several networks used to improve single-column CNNs, such as the Con­
gested Scene Recognition Network (CSRNet) can be highlighted in [52]. Hybrid 
approaches typically include methods that combine multiple techniques to enhance CC 
accuracy. For example, some approaches integrate multi-scale CNNs with density map 
regression to address varying person sizes and improve estimation accuracy. Others may 
merge density map methods with object detection models to benefit from both individ­
ual detection and overall density estimation. These hybrids are proposed in [53], aim to 
leverage the strengths of different techniques to handle scale variations more effectively 
and achieve high performance calculated by Eqs. (7) and (8) for mathematically calculat­
ing the density map and regression losses, as demonstrated in [45].
The Lightweight CC Network (LCD net) that was discussed in [54], presents a model 
for CDE in real-time video surveillance. It is designed to be lightweight and fast, so it 
can quickly analyze video frames without needing a lot of computing power. The model 
Fig. 5  Structural design of the single-column CNN (SC-CNN) for crowd counting
 


## Page 11

Page 11 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
uses efficient methods to extract important details from images, allowing it to accurately 
measure CD even when crowds are very dense.
The authors in [55, 56], are introduced a Scale-Aware Adaptive Networks (SANet) 
presents a method that enhances crowd counting accuracy by integrating depth infor­
mation into a CNN. The algorithm helps the network better handle varying sizes and 
distances of people in the crowd, improving its ability to estimate the count accurately. 
The methodology showed improved performance on standard CC datasets by effectively 
using depth data to manage scale variations and provide more counts that are precise.
F (x) =
N
∑
i=1
δ (x −xi) ∗Gσi (x) , σi = β ¯di

(7)
N is the total number of individuals (points) in the image, xi is the position of the ith 
individual in the image, Gσi (x) is the A Gaussian kernel with a standard deviation σi, 
δ is the ground truth function, β is the constant scaling factor, when equal to 0.3 gives 
the best performance, ¯di is the Characteristic distance (such as from the camera) related 
to the ith individual.
ˆD (x) = gi + λdi, gi = 1
m
m
∑
i=1
log
(
1 −D(G
(
Zi))
), di = 1
m
m
∑
i=1
log(D
(
Xi)
) + log
(
1 −D
(
G
(
Zi)))

(8)
λ is the A weight balancing the GAN loss, m: number of samples, gi is the UNet gen­
erator loss, D
(
G
(
Zi))
 is the discriminator output, Xi is the represents real crowd 
samples from the training dataset, N is the number of training samples, Fd (xi; θ). The 
predicted density map for the ith sample, xiis the input ,θ is the represents the network 
parameters. Di is the ground truth density map for the ith sample, ∥.∥2 is the squared 
Euclidean norm measures the difference between the predicted and actual density maps.
The Cascaded Pyramid Network (CP-Net) that shown in [57], presents a smart system 
for counting crowds in images. It works by first analyzing the image at different levels of 
detail, both close-up and far away.
The system refines crowd counts in several steps, combining detailed information to 
estimate people accurately in crowded and complex scenes.
The Hierarchical Attention-based Crowd Counting Network (HSNet) [58] handles 
people at different scales and focuses on key regions, improving accuracy even in dense 
or varied crowds.
Crowd counting is applied in areas like industrial monitoring, urban planning, and 
traffic management [59]. Traditional methods often ignore the effect of foreground and 
background. The Multi-Dense Scale Network (M-DSNet) addresses this by combining 
crowd counting with foreground-background segmentation and using dilated convolu­
tion and self-attention, achieving better results across four datasets.
The Scale Aggregation and Spatial-Aware Network (SASNet) [60], counts crowds from 
multiple camera views, keeping people at consistent scales, reducing background dis­
tractions, and combining all views for a more accurate count.


## Page 12

Page 12 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
2.5  Transformer
Recently, attention mechanism-based models have shown remarkable success across 
various CV tasks such as introduced by Wang in [61]. The paper shows that transformer 
models, especially Swin Transformer, outperform CNNs in classifying static street-view 
building images, achieving about 90% F1-score and 92% accuracy, proving their strength 
in complex visual scene analysis. Rather than processing the entire image uniformly, 
these models enable the network to concentrate specifically on the most important 
regions, enhancing performance. In this context, crowd counting is a tough task in CV, 
often used in video surveillance and public safety. As camera resolutions increase and 
crowd images become more complex, accurately predicting crowd density and counting 
is more important than ever. Recent CNN-based methods have been effective in densely 
populated scenes, which were introduced in [62]. Also, a new approach to CC is intro­
duced using an Encoder-Decoder Multi-Scale Attention Network. This approach builds 
on the strong U-Net architecture, enhanced with an attention mechanism. The multi-
scale attention method is applied to different layers in the U-net, allowing the network to 
focus more on the crowd and less on the background. The attention mechanism, along 
with skip-connections, helps adjust the importance of various features while keeping 
information at different scales.
Recently, researchers have been improving crowd counting by using advanced deep 
learning methods. They are combining regular images with thermal data to handle 
tricky lighting and crowded scenes better. Attention mechanisms help models focus on 
important areas, and multi-scale processing lets them understand different crowd sizes. 
They’re also creating lightweight models for faster, real-time predictions. To make mod­
els even stronger, they use techniques like GANs with U-Net, demonstrated in [63] for 
more accurate results to enhance the density map, which could be expressed as Eq. (9). 
Curriculum learning is used to teach models step by step, starting with easier tasks and 
moving to harder ones. Recent advances [64, 65] proposed that models are trained pro­
gressively with a loss function, which can be calculated from Eq. (10). These algorithms 
effectively handle various challenges, such as varying crowd densities and occlusions. 
They often utilize DL models with features like multi-scale processing and attention 
mechanisms to improve accuracy. Some methods focus on enhancing data efficiency, 
while others enhance spatial awareness. Overall, these approaches represent the latest 
advancements in accurately estimating crowd sizes in complex scenes.
ˆD (x) = gi + λdi,
gi = 1
m
m
∑
i=1
log
(
1 −D
(
G
(
Zi)))
.
di = 1
m
m
∑
i=1
log
(
D
(
Xi)
) + log
(
1 −D
(
G
(
Zi)))
.

(9)
λ is the A weight balancing the GAN loss, m is the number of samples, gi is the UNet 
generator loss, D
(
G
(
Zi))
 is the discriminator output, Xi is the represents real crowd 
samples from the training dataset.


## Page 13

Page 13 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
RAD (X, Y, D)r =
x+r
∑
i=x−r
y+r
∑
j=y−r
Di,j
L (θ)step =
1
2N
N
∑
i=1
∥AT (Di, step) ⊙(Xi −Di)∥2
2

(10)
r is a super parameter representing the local region size, D is the density map, 
D is the Gσ (x), σ represents the spread parameter, RAD (X, Y, D) is the average 
density value of a rectangular region which takes (x, y) as the center, with a width of 
2r + 1 pixels, θ is the parameters of a CC neural network, N is the number of samples in 
the training dataset, Xi, Di ith is the input image and the corresponding ground truth, 
respectively.
2.6  Emerging trends
In recent years, several emerging directions have reshaped the taxonomy of crowd 
counting methods by introducing attention mechanisms, transformer-based designs, 
hybrid architectures, curriculum/adaptive training, lightweight models, and advanced 
preprocessing/fuzzy enhancements. For example, attention-driven models such as the 
Hierarchical Region-Aware Network (HRANet) employ region-aware and recalibration 
modules to enhance feature extraction in complex backgrounds and varying scales, sig­
nificantly improving density map quality Xie et al. [66]. In the domain of transformer-
based methods, Trans Crowd demonstrates how self-attention can effectively capture 
both local and global crowd patterns under weak supervision, using only count-level 
annotations instead of detailed head label Zhang et al. [14]. For lightweight and real-time 
applications, Tiny Count by Lee et al. [24] introduces an extremely compact network 
that achieves competitive performance on benchmark datasets, while being efficient 
enough for deployment on edge devices such as Raspberry Pi and Jetson Nano. Simi­
larly, curriculum learning and adaptive training strategies, such as those presented in 
Highly Crowd Detection and Counting Based on Curriculum Learning, Fotia et al. [67], 
which gradually train models from sparse to highly dense crowd scenes, stabilize learn­
ing, and improve generalization to diverse environments. These trends illustrate how 
modern approaches are moving beyond traditional CNNs toward more adaptive, effi­
cient, and robust solutions for crowd counting in complex real-world scenarios. In addi­
tion, fuzzy-based enhancements have recently gained attention for handling uncertainty 
and noise in complex environments. For example, Altundoğan et al. [68] introduced a 
Dynamic Fuzzy Cognitive Map (DFCM) approach for crowd analysis using time-series 
data extracted from video, showing improved robustness in noisy and low-quality sce­
narios. In addition to fuzzy-based preprocessing. we also added hybrid deep learning 
mechanisms, Elsepae et al. [69], employed to improve crowd counting in low-light and 
Harsh conditions, demonstrating the strength of combining different models for greater 
robustness.


## Page 14

Page 14 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
3  Assessment metrics
In crowd counting, several evaluation metrics are used to measure how well a model 
estimates the population density. Here are the most common metrics, explained simply 
in both crowd counting and crowd-counting estimation in this paper [2].
 
  1.	  Crowd Counting Evaluation [58]:
 	•
MAE calculates the average difference between the predicted values and the actual 
values. In crowd counting, MAE is used to see how accurate the count of people 
is. If MAE is low, the count of the model is close to the actual number of people. 
The mathematical calculation of MAE can be expressed in Eq. (11).
 	•
MSE is the square of the difference between the predicted and true counts, 
averaged over all test images. Like MAE, but it squares the differences before 
averaging them. MSE is used to evaluate how big the errors are in the crowd count 
or the density map. A lower MSE means fewer big mistakes. This error can be 
calculated from Eq. (12).
 	•
RMSE is a way to measure how far a model’s predictions are from the actual 
values. It works by calculating the difference between what the model predicted 
and the real answer, squaring those differences to make sure all errors are positive, 
and then averaging them. Finally, it takes the square root to bring everything 
back to the original scale. RMSE is useful because it gives more weight to large 
mistakes, meaning it highlights situations where the model was far off. A smaller 
RMSE means the model is doing a good job, while a larger one means it made 
bigger errors. RMSE can be calculated from Eq. (13).
   2.	    Crowd Counting Estimation (CCE) [2]:
 	•
Structural Similarity Index (SSIM) is a way to check how similar two images are. 
It looks at the important parts of the image, like shapes and patterns, instead of 
just checking individual pixels. In crowd counting, SSIM helps see if the predicted 
crowd map looks like the real one. A high SSIM means the two maps are very 
similar, and a low SSIM means they are different. SSIM can be evaluated from 
Eq. (14), whose value ranges between [− 1, 1].
Table 3  Definitions and representations of symbols used in Eqs. (11–15)
Symbol
Representation
yi
Actual headcount
yi
Predicted headcount
ith
Test image
µx,µy
The average value for the first image and the second image, respectively
σ2
x, σ2
y
The standard deviation for the first image and the second image, respectively
σxy
Represents how the values in the two images change together
c1
(K1L)2
c2​
(K2L)2
K1, K2
K1 = 0.01, K2 = 0.03;are constant to prevent division by zero
x
The original image, y, is the generated image (like an image with added rain)
σxy
µiriy −µirµiy (co-variation)
MAXi
The maximum possible power of an image, x, y, is the original image and the generated image


## Page 15

Page 15 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
 	•
Peak Signal-to-Noise Ratio (PSNR) in CCE measures the quality of estimated 
density maps by comparing them to ground truth maps. It calculates the ratio of 
the maximum possible signal power to the noise power, affecting the accuracy 
of the estimated map. A higher PSNR value indicates that the estimated density 
map is closer to the true density map, reflecting a more accurate crowd count. 
PSNR can be estimated from Eq. (15). In addition, Table 3 explains the definition 
of every symbol.
MAE = 1
n
n
∑
i=1
|yi −ˆyi|

(11)
MSE = 1
n
n
∑
i=1
(yi −ˆy)2

(12)
RMSE =



 1
n
n

i−1
(yi −ˆyi)2

(13)
SSIM (x, y) =
(2µxµy + c1) (2σxy + c2)
(
µ2x + µ2y + c1
) (
σ2x + σ2y + c2
)

(14)
PSNR (x, y) = 10log10
(
MAX2
i
MSE (x, y)
)

(15)
   
 
4  Datasets description
Several datasets have been created to help improve model generalization in the contem­
porary period. While early datasets contained low-density crowds, newer ones focused 
on high-density crowds, introducing challenges to CC. These larger datasets have driven 
the development of methods to address these issues. This section reviews eight key data 
sets, which play a crucial role in advancing algorithms by providing diverse scenarios 
for training and evaluation. Table 4 summarizes the types of the most famous datasets 
in the CC phenomenon. In addition to density-based datasets such as ShanghaiTech, 
UCF-QNRF, and JHU-CROWD++, crowd counting research can also benefit from 
detection- and tracking-based datasets. For example, CrowdHuman provides large-scale 
bounding-box annotations for pedestrians in crowded scenes, while CroHD (Crowd of 
Heads) and Cchead focus on head-level annotations and tracking information, making 
them particularly valuable for addressing challenges in highly congested environments. 
Using both density estimation and detection/tracking datasets allows crowd counting 
models to cover a wider range of crowd scenarios and improves their generalization.
When working with datasets like the AI City Challenge [70], annotation and general­
ization issues arise. In dense crowds, labeling is difficult due to occlusions, inconsistent 


## Page 16

Page 16 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Datasets
Image 
quan­
tity
Annotation 
quantity
Resolution
Best 
study
Samples of images
SHT (A), 
SHT(B)
1198
330,165
598 × 868
[79], 2020
UCF-QNRF
1535
1,251,642
2013 × 2902
[80], 2023
UCF-CC-50 50
63,974
2101 × 2888
[81], 2024
UCSD
2880 
video 
frames
49,885
158 × 238
[82], 2019
Mall
2000 
video 
frames
62,325
320 × 240
[45], 2023
JHU-
CROWD++
4360
1,438,808
Every image 
has a unique 
resolution
[4], 2020
NWPU-
Crowd
5109
2,133,238
Various 
resolutions, 
typically 
ranging from 
640 × 480 to 
1920 × 1080
[83], 2024
CrowdHu­
man
15,000
330,000
1080 (varied)
[78], 2024
Table 4  Sample dataset descriptions for leading crowd counting benchmarks


## Page 17

Page 17 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
or incomplete annotations, which can introduce noise. Bounding boxes may also fail to 
capture small or partially visible pedestrians.
Generalization across datasets is another challenge: models trained on one data­
set often perform poorly on new environments or different crowd densities because of 
domain gaps. Fixed annotation strategies, such as Gaussian kernels, may not transfer 
well to other datasets. Additionally, lightweight models, although efficient, can struggle 
in complex crowd scenes. The crowd counting estimation, detection, and tracking datas­
ets can be divided as follows:
 
  a.	   Crowd Counting density map Datasets
 1.	   ShanghaiTech (part A, part B): The ShanghaiTech dataset is a well-known 
benchmark for crowd counting, split into two parts to represent different crowd 
densities and scenes. Part A contains 482 images (300 for training and 182 for 
testing) with 241,677 annotated heads and mainly shows very dense outdoor crowds 
in urban areas such as streets and public squares. Part B includes 716 images (400 
for training and 316 for testing) with 88,488 annotated heads and depicts sparse 
outdoor crowds in more relaxed places, such as parks. This dataset is widely used to 
develop and test crowd counting models, typically evaluated using MAE and MSE. 
The datasets referenced from the source in [47].
   2.	   University of Central Florida Quantitative and Qualitative Crowd Counting 
Dataset (UCF-QNRF): The UCF-QNRF dataset is a large collection used for CC 
research, as mentioned in the source [71]. It contains 1535 images with 1,525,272 
annotated heads, showing a wide range of crowd sizes from sparse to very dense. 
The images come from urban areas, indoor spaces, and events. The official split 
consists of 1201 training images and 334 test images, which has become the 
standard protocol in literature. It covers a wide range of crowd sizes, from sparse 
to extremely dense, and includes both indoor and outdoor urban scenes, such 
as streets, squares, and public events. This large-scale dataset is an important 
benchmark for testing the scalability of crowd counting methods.
   3.	   University of Central Florida Crowd Counting 50 (UCF-CC-50): The UCF-CC-50 
dataset is used for CC and has 50 images with 63,296 annotated heads. It focuses 
Datasets
Image 
quan­
tity
Annotation 
quantity
Resolution
Best 
study
Samples of images
CroHD 
(Crowd of 
Heads)
11,463 
frames 
(9 video 
se­
quenc­
es)
2.27 million an­
notations, 5230 
unique tracks
Full-HD
[84], 2024
Cchead
50,528 
frames 
(10 
scenes)
2.36 million an­
notated heads, 
2358 unique 
tracks
HD/Full-HD
[70], 2023
Table 4  (continued)
 


## Page 18

Page 18 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
on very crowded scenes in urban areas. Even though it is a smaller dataset, it is 
useful for testing and improving CC models, with performance usually measured 
by errors like MAE and MSE. It focuses on extremely dense outdoor crowds in 
urban areas such as streets and plazas. For UCF-CC-50, there is no official split. 
The standard protocol is 5-fold cross-validation, where 40 images are used for 
training and 10 for testing in each fold, and results are averaged over all five folds. 
These datasets can be found in [72].
   4.	   University of California, San Diego (UCSD): The UCSD dataset is used for CC 
and consists of 2880 video frames with 7014 annotated people. It focuses on sparse 
to moderately dense crowds like sidewalks and streets in outdoor settings. The 
dataset features continuous video sequences, which help analyze crowd movement 
and dynamics. It features sparse to moderately dense outdoor crowds, typically 
along sidewalks and campus walkways. Because it provides continuous video 
sequences, it is also used to analyze crowd movement and temporal dynamics in 
addition to still-image counting. There is no official split; a common protocol uses 
800 frames for training and 1200 for testing. The source of the datasets is [73].
   5.	   Mall: This contains 2000 video frames with about 60,000 annotated pedestrians, 
captured from a fixed surveillance camera in an indoor shopping mall. It depicts 
moderate to high crowd densities in areas such as walkways and food courts, 
such as [74]. A common protocol uses the first 800 frames for training and the 
remaining 1200 for testing. It represents indoor mall environments, such as 
shopping areas and food courts, with moderate to high crowd density. This dataset 
provides valuable data for analyzing crowd behavior in enclosed spaces and for 
testing crowd counting models in indoor scenarios.
   6.	   Johns Hopkins University (JHU-CROWD++):
 	 The JHU-Crowd + + dataset is an extended version of the original JHU-Crowd 
dataset, created for crowd counting (CC). It contains 4372 images with annotations 
for over 1.51 million people, covering a wide range of crowd densities, from sparse 
to extremely dense. The images include scenes such as streets, public events, and 
gatherings, providing diverse examples to train and evaluate CC models. This 
extended version offers even more challenging crowd scenarios for training and 
testing. The dataset is divided into three subsets: 2272 images for training, 500 for 
validation, and 1600 for testing. This standard split ensures consistent benchmarking 
and allows fair comparisons among different crowd-counting methods. The dataset 
can be accessed from the official source in [4].
 7.	Northwestern Polytechnical University (NWPU-CROWD):
	
The NWPU-Crowd dataset is designed for crowd counting (CC) and contains 5109 
images with annotations for over 2 million people. It covers a wide range of crowd 
densities, from sparse to extremely dense, and includes various environments such 
as streets, parks, and large public events. This diversity makes it one of the most 
comprehensive datasets for evaluating crowd counting algorithms. The dataset 
is split into 3109 images for training, 500 for validation, and 1500 for testing, 
providing a standardized setup for fair and consistent benchmarking. The dataset 
can be accessed from the source in [75].
   b.	 Crowd Counting density map Datasets


## Page 19

Page 19 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
1.	 The CrowdHuman: The CrowdHuman dataset is designed for detecting people 
in crowded V scenes. It contains about 15,000 images with over 330,000 labeled 
people; each annotated with a bounding box and an occlusion level indicating how 
much others block a person.
	
Most images are outdoor scenes from streets and public places, showing people 
from different angles, lighting conditions, and crowd densities. On average, each 
image has around 22 people, with some images containing more than 100. The 
dataset is divided into 10,000 images for training, 4370 for validation, and 5000 
for testing, enabling models to be trained, tuned, and evaluated effectively. While 
the dataset mainly focuses on outdoor scenes, some images include semi-indoor 
public areas. Its main goal is to capture realistic crowded environments with varied 
lighting, angles, and occlusions. The CrowdHuman Dataset can be accessed from 
the official website [76].
 2.	   Crowd of Heads dataset: The CroHD dataset is designed for tracking pedestrian 
heads in dense crowds. It contains 9 video sequences with 11,463 frames captured 
from elevated viewpoints at 25 fps. The dataset includes both indoor and outdoor 
scenes, such as train stations and pedestrian crossings, under varying lighting and 
conditions. Each frame is annotated with head bounding boxes, totaling over 2.27 
million annotations and 5230 unique tracks. The official split uses 4 sequences 
for training and 5 for testing. CroHD focuses on head-level tracking to handle 
occlusions and overlapping people, and introduces the IDEucl metric for evaluating 
identity preservation. It is publicly available for research. The datasets stored in 
[77].
   3.	   Chinese Large-scale Cross-scene Pedestrian Head Tracking; The Cchead dataset 
[78] is a large benchmark for tracking pedestrian heads in dense crowds. It has 10 
scenes with 50,528 frames, over 2.36 million annotated heads, and 2358 unique 
tracks. The scenes include pedestrians moving at different speeds and directions, 
captured from slope and overhead viewpoints.
 	 The dataset is split into 40,422 frames for training and 10,106 for testing, supporting 
proper model training and evaluation. It mainly covers outdoor areas, like streets 
and school roads, and is publicly available for research. 
 
5  Deep learning techniques for solving crowd counting problems
a.	 Related works
In this section, Table 5 compares the performance of crowd counting algorithms across 
different datasets (ShanghaiTech Part A/B, UCF-QNRF, and UCF-CC-50). The reported 
MAE, MSE, and RMSE values highlight how each method adapts to problems of crowd 
counting, such as scale variation, perspective distortion, uneven distribution, rotation, 
occlusion, and bad weather.
To solve the problem of scale variation, Li et al. presented an algorithm, AP-FPN, 
which demonstrated strong robustness with relatively low error (MAE = 54.9 on SHT A). 
Zhang et al. introduce a Segmentation-based CC Network that improved robustness in 
bad weather through segmentation, albeit at a higher computational cost. To get rid of 


## Page 20

Page 20 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Ref
Algorithm
Challenge
Metrics
MAE/MSE
Pros
Cons
Year
SHT A
SHT 
B
UCF-QNRF UCF-CC-50
 [85]
2020
MSA-CNN
Scale 
Variation
72.4
104.7
22.7
35.4
293.9
361.6
–
Robust to 
scale varia­
tion; good 
accuracy 
on dense 
scenes
Lim­
ited with 
uneven 
distribu­
tion and 
back­
ground 
noise
 [86]
2020
ALN
Perspective 
Distortion
63.5
99.2
8.1
11.9
110.3
178.2
211.4
306.7
Adapts 
well to 
perspective 
distortion
Weak 
perfor­
mance in 
very high-
density 
scenes
 [87]
2020
DM-CC
Uneven
Distribution
59.7
RMSE/95.7
7.4
11.8
85.6
148.3
211
291.5
Handles 
uneven 
crowd 
distribution 
effectively
Sensi­
tive to 
noise and 
occlusion
 [63]
2021
Segmenta­
tion-based 
CC Network
Bad 
weather
Scale 
Variation
68.3
104.1
12.1
19.3
–
233.6
352.6
Incorpo­
rates seg­
mentation 
to improve 
under bad 
weather
Higher 
computa­
tion; less 
accurate 
in open 
scenes
 [88]
2021
AP-FPN
Scale 
Variation
54.9
85.3
7.4
10.8
75.7
120.4
186.8
266.1
Strong 
handling of 
scale varia­
tion with 
pyramid 
features
High 
memory 
and com­
putational 
cost
 [59]
2021
DSNet
Scale 
Variation
61.3
RMSE/97.3
6.7
10.5
91.4
160.4
186.8
266.1
Reduces 
counting 
error across 
multiple 
scales
Weak 
under 
complex 
back­
grounds
 [89]
2021
SACCN
Complex 
Background
59.2
98
6.8
10.5
178.0
258.5
96.1
167.8
Attention 
improves 
perfor­
mance in 
cluttered 
scenes
Training 
com­
plexity; 
sensitive to 
hyperpa­
rameters
 [90]
2022
CSS-CCNN
Rotation
–
–
437.0
722.3
564.9
959.4
Robust 
for dense 
crowds 
using a 
cascade 
structure
Slower 
inference
 [91]
2022
FPN, 
Auto-scale
Scale 
Variation
75.7
150.4
10.4
18.8
124.8
234.7
224.6
314.6
Flexible 
for scale 
variation
Accuracy 
dropsin 
very dense 
scenes
 [92]
2022
SGANet
Scale 
Variation
58.0
100.4
6.3
10.6
89.1
150.6
–
GAN 
improves 
density 
map quality
Prone to 
instability 
in training
Table 5  Benchmarking crowd counting models: performance metrics across diverse challenges


## Page 21

Page 21 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Ref
Algorithm
Challenge
Metrics
MAE/MSE
Pros
Cons
Year
SHT A
SHT 
B
UCF-QNRF UCF-CC-50
 [93]
2022
SDC
Scale 
Variation
69.9
106.9
9.4
15.9
–
–
Effective 
for uneven 
distribution 
using local 
context
Limited for 
dynamic 
large-scale 
variations
 [94]
2022
CNN + CBAM
Scale 
Variation
64.6
103.2
8.3
14.1
113.8
188.6
–
Attention 
enhances 
feature 
representa­
tion
Increased 
model 
complexity
 [95]
2022
2U-Net
Rotation
Scale 
Variation
63.3
103.8
7.4
12
239.4
356.1
1.5
1.9
Robust to 
rotation; 
reliable in 
multi-scale 
scenarios
Weaker 
under 
heavy 
occlusion
 [96]
2022
HRANet
Uneven 
Distribution
100
87.2
7.2
9.7
84.6
146.2
160.9
235.8
Hierarchical 
attention 
improves 
perfor­
mance
Requires 
large 
training 
datasets
 [97]
2023
Deep Tempo­
ral CC
Uneven 
Distribution
60.8
100
7.2
8.3
88.7
93.2
319.9
312.6
Temporal 
modeling 
improves 
video 
counting
Not suit­
able for 
still images
 [98]
2023
CAFNet
Scale 
Variation
97
94.5
10.2
12.2
96.4
155.5
–
Fuses 
multi-
scale and 
distribution 
awareness
Compu­
tationally 
expensive
 [99]
2023
FPANet
Scale 
Variation
70.9
120.6
6.9
15.5
108.9
197.6
159.5
218.4
Accurate 
with 
feature 
pyramid 
attention
Sensitive 
to clut­
tered back­
grounds
 
[100]
2023
AWCC-Net
Bad 
Weather
56.2
91.3
–
76.4
130.5
–
Good 
robustness 
to weather-
related 
noise
Limited 
generaliza­
tion to 
unseen 
conditions
 
[101]
2024
EfficientNet-
B3
Rotation
107.6
61.3
11.2
6.25
–
213.2
162.3
Light­
weight 
with good 
accuracy
Rotation 
handling is 
less stable 
under high 
occlusion
 
[102]
2024
Detailed 
architecture
Scale 
Variation, 
Rotation
–
–
97.20
156.4
201.6
286.4
Accurate 
regression-
based 
counting
Limited 
interpret­
ability
 
[103]
2024
DCNN
Occlusion
Perspective 
Distortion
52.6
90.9
8.1
12.8
96.4
168.7
181.8
240.6
Strong 
against oc­
clusion and 
perspective 
distortion
Heavy 
model; 
higher 
training 
cost
Table 5  (continued)
 


## Page 22

Page 22 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Ref
Algorithm
Challenge
Metrics
MAE/MSE
Pros
Cons
Year
SHT A
SHT 
B
UCF-QNRF UCF-CC-50
 
[104]
2024
Hybrid 
Lightweight 
Network
Scale 
Variation
71.5
108.6
11.3
20.0
100.4
182.6
–
light­
weight, effi­
cient, lower 
annotation 
cost, and 
com­
petitive 
accuracy
weaker in 
very dense 
crowds, 
limited 
generaliza­
tion, and 
less robust 
under 
occlusion.
 [24]
2024
Tiny Count
Real-time 
crowd 
counting
78.2
120.8
10.81
18.4
134.7
223.3
–
Very light­
weight; 
fast infer­
ence on 
Raspberry 
Pi & Jetson 
devices
May lose 
accuracy 
in ultra-
dense/
occluded 
datasets
 
[105]
2024
TRepVGG
Scale 
variation; 
occlusion 
in dense 
crowds
66.9
104.5
7.4
12.5
–
–
Light­
weight and 
efficient; 
faster 
inference; 
suitable for 
real-time 
edge use; 
reduces 
training
Accuracy 
is slightly 
lower than 
larger 
transform­
er-based 
models; 
it needs 
careful 
tuning for 
reparam­
eterization
 
[106]
2024
MPCount
Domain 
generaliza­
tion
115.7
199.8
11.4
19.7
165.6
290.4
–
Improves 
robust­
ness when 
training 
and testing 
on different 
datasets
May 
under­
perform 
in highly 
diverse 
unseen 
domains
 
[107]
2024
Occupancy 
Counting at 
Entrances
Real-time 
Dense 
Entrance 
Monitoring
Head-tracking-for-occupancy-counting
Accuracy:98.1%
High 
accuracy 
for smart 
building 
applications
Task-
specific; 
limited 
generaliza­
tion to 
large open 
scenes
 
[108]
2025
DMLViT
Handling 
heavy 
congestion, 
scale varia­
tion, and 
occlusion.
53.1
86.5
6.2
9.7
85.6
148.3
211.0
291.5
Captures 
local + 
global 
features; 
robust 
to scale 
variation; 
effective 
in highly 
congested 
traffic 
scenes; 
improves 
transformer 
efficiency
Higher 
computa­
tional cost 
than light­
weight 
CNNs; 
may need 
powerful 
GPUs for 
training
Table 5  (continued)
 


## Page 23

Page 23 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Ref
Algorithm
Challenge
Metrics
MAE/MSE
Pros
Cons
Year
SHT A
SHT 
B
UCF-QNRF UCF-CC-50
 
[109]
2025
D2PT
Scale 
variation; 
occlusion 
in dense 
crowds
68.2
77.9
58.1
–
Improves 
both local­
ization and 
counting; 
combines 
the benefits 
of density 
and point 
methods
Likely 
heavier/
training 
complexity
 
[110]
2025
P2PNet
Occlusion
52.74
85.06
6.25
9.90
85.32
154.50
-
Data-effi­
cient, much 
faster than 
P2PNet
Sensitive 
to pa­
rameters, 
weaker 
with mo­
tion blur, 
and de­
pends on 
pseudo-
label 
quality
 
[111]
2025
CrowdCL
Domain 
adapta­
tion, Scale 
variation
142.5
RMSE:231.4
150.7
243.9
–
–
No need 
for many 
labels
Works bet­
ter on new 
datasets
Less accu­
rate than 
supervised 
models, 
still hard 
with heavy 
occlusion
 
[112]
2025
PPSC
Dense 
crowds 
with 
perspective 
distortion
62.6
96.6
7.9
13.1
86.3
138.9
–
Need fewer 
labeled 
images
Use 
perspective 
to improve 
counting. 
Handles 
scale 
changes 
better
Less 
accurate 
than fully 
supervised 
methods
Needs 
perspec­
tive maps
Struggles 
with heavy 
occlusion
 
[113]
2025
SACCN
52.4
84.3
6.5
10.7
77.2
125.0
202.3
280.5
Effectively 
handles 
multi-scale 
crowd 
density
Increased 
model 
complexity 
and com­
putation
 
[114]
2025
MISF-Net 
(RGB-T 
Fusion)
Modality 
fusion (RGB 
+ Thermal)
DroneRGBT: Datasets
MAE:10.80
RMSE:19.87
Robust 
under poor 
illumina­
tion and 
nighttime 
scenes
Requires 
dual-
modal 
data (not 
always 
available)
 
[115]
2025
MSFFNet
Scale 
variation & 
semantic 
context
58.6
93.2
6.2
10.1
85.3
146.7
180.2
245.0
Captures 
both global 
and local 
features 
effectively
Higher 
compu­
tational 
cost due 
to multi-
branch 
fusion
Table 5  (continued)
 


## Page 24

Page 24 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
uneven distribution, Wang et al. proposed a DM-CC that achieved reliable performance 
but remained sensitive to noise and occlusion.
Attention-based methods became dominant with Chen et al. when they presented 
HRANet, which achieved the lowest error (MAE = 52.8, MSE = 87.2 on SHT A) and dem­
onstrated strong adaptability to uneven crowd distributions and complex backgrounds. 
Similarly, Liu et al. presented CNN integrated CBAM enhanced feature representation 
through attention modules, though at the cost of increased model complexity.For tem­
poral and multi-scale modeling, Zhou et al. introduced a method, Deep Temporal CC 
improved performance on video sequences. While Xu et al. put forward FPANet lev­
eraged pyramid attention to enhance precision under scale variation. Tan and Le sug­
gested an EfficientNet-B3, which provided a lightweight but accurate solution. Khan et 
al. gave a study, Crowd-Regression Module enhanced regression-based interpretability 
across datasets but faced limited robustness under occlusion.
More recent works emphasized lightweight and transformer-based models. Huang 
et al. introduced a Hybrid Lightweight Network reduced annotation costs while retain­
ing competitive accuracy, though performance dropped in very dense crowds. Zhu et 
al. suggested a study of TinyCount achieved real-time crowd counting on edge devices 
such as Raspberry Pi, highlighting efficiency but limited scalability. Transformer-driven 
models like Gao et al. as DML-ViT model and Feng et al. D2PT algorithm improved 
handling of congestion, scale variation, and occlusion, albeit with heavier training com­
plexity. Finally, Zhang et al. introduced domain adaptation with reduced label depen­
dency, though accuracy lagged fully supervised approaches.
Despite these advancements, most existing crowd counting approaches still face sev­
eral limitations. Many models show reduced accuracy in extremely dense and highly 
occluded scenarios, where individuals overlap significantly. Others struggle to general­
ize well across unseen datasets, indicating limited adaptability to different environments 
and lighting conditions. In addition, transformer-based and attention-driven methods 
often require heavy computational resources and long training times, making them less 
practical for real-time deployment on low-power devices. Lightweight models, while 
efficient, usually sacrifice accuracy when applied to complex or large-scale crowd scenes. 
These challenges highlight the need for more robust, scalable, and computationally effi­
cient solutions.
  
b.	 Practical analysis
In this survey, the focus is on providing a comprehensive overview rather than detailing 
a specific methodology. Therefore, the explanation of the methodology is not as in-depth 
as it would be in an experimental study. Essentially, I’m presenting a broad survey that 
highlights existing approaches and their strengths and weaknesses.
From Table 4, the results were good in sparse scenes, but the error was higher in dense 
scenes. To solve this problem, the practical analysis achieves balanced results in both 
high-density and low-density crowd scenarios by combining several complementary 
techniques. First, fuzzy-based preprocessing with sharpening and Laplacian filtering 
enhances contrast and reduces noise, which makes head regions clearer in low-light or 


## Page 25

Page 25 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
uneven illumination conditions. Next, hybrid attention mechanisms, integrating both 
channel and spatial attention, guide the model to focus on the most relevant features 
and locations, improving robustness against scale variation, occlusion, and background 
clutter. The fusion of different CNN architectures, such as EfficientNet and VGG-style 
networks, further strengthens performance by capturing both fine details and global 
context, enabling accurate recognition across varying crowd densities. In addition, cur­
riculum learning is applied to train the model gradually, starting from simple low-density 
cases and progressing to complex dense and occluded scenes, which stabilizes training 
and improves generalization. Also, YOLOv8n provides a practical balance between per­
formance and speed, making it particularly suitable for scenarios that require deploy­
ment on edge devices or in resource-constrained environments. As mentioned in [116], 
which proposal is a system for human density monitoring that combines YOLOv8 for 
Table 6  Our proposed experiments for crowd counting based on new trends
Algorithm
Datasets
Challenge
Metrics
Technique
Pros
Cons
EffiVGGNet 
[69]
VGG16
SHT A
SHT B/
SHT A
SHT
Harsh 
Weather
MAE: 
77.7028
MAE: 
12.9224/
MAE: 
51.8785
MAE: 1.9903
Hybrid deep 
learning 
mechanisms, 
Efficient­
NetB7, con­
catenated 
with VGG16
Combines the 
strengths of Efficient­
Net (efficiency) & VGG 
(stability); good for 
harsh weather
More 
param­
eters, so 
higher 
compu­
tational 
cost
CANNet_+ 
CL
SHT A
SHT B
JHU++
Perspec­
tive &
Complex 
Background
MAE:42.5
MAE:17.24
MAE:69.63
Applied 
adaptive 
curriculum 
learning with 
attention 
mechanisms
Improves learning 
gradually; robust to 
complex background
Longer 
training; 
sensi­
tive to 
cur­
riculum 
design
MC-CNN
SHT A
SHT B
UCF-QNRF
Rainy 
Weather
MAE:59.5
MAE:16.7
MAE:102.99
Hybrid 
Attention 
mecha­
nisms with 
MC-CNN 
architecture
Good robustness 
against noise/weather
Less ef­
fective 
under 
heavy 
occlu­
sion
CSRNet
SHT A
SHT B
UCF-QNRF
Scale 
Variation
MAE:96.20
MAE:29.20
MAE:66.40
CSRNet with 
channel 
and spatial 
attention 
mechanisms
Strong for scale varia­
tion; high accuracy on 
benchmarks
not ro­
bust for 
back­
ground 
clutter
Bidirectional 
LSTM
HAJJv2 Dataset
Dense 
crowd, 
uneven 
distribution
mAP@50: 
95.5
Precision:
94.8%
Recall:
93.1%
Processing 
by sharpen­
ing and La­
placian, and 
fuzzy based 
on BiLSTM
strong in dense scenes
Needs 
sequen­
tial data
YOLO8n
video cross-
walking/YOLO5-
Deepsort
crowd datasets
Illumination
& Occlusion
mAP@50: 
97.7%
Preci­
sion:97%
Recall:96.8%/
mAP@50: 
98.7%
preci­
sion:97.9%
Recall:96.5%
The data­
sets were 
enhanced 
by CLAHE 
and gamma 
correction 
based on 
YOLO11n
Excellent detection 
speed and accuracy
Sensi­
tive to 
ex­
treme 
occlu­
sion; 
requires 
tuning 
for light 
changes


## Page 26

Page 26 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Problem
Scene
Proposed 
Solution
Techniques
Strengths/
weaknesses
1. 
Occlusion
Where 
parts 
of the 
crowd are 
blocked 
from view, 
making 
it hard to 
detect 
individuals
• CSONet 
(Characterizing 
Scattered Occlu­
sion Network) 
[117]
• Multiscale fea­
ture extraction 
module [33]
• CNN with 
atten­
tion + scat­
tered 
features
• Multiscale 
CNN filters
• Strong in 
complex 
scenes
Overestimates 
sometimes, 
complex
• Very accurate, 
simple, and 
stable
• May miss 
small, oc­
cluded details
2. Com­
plex back­
ground
Back­
ground 
objects 
may 
look like 
people, 
making 
counting 
harder
• SACANet 
(Scale-Adaptive 
Context-Aware 
Network) [118]
• Scale-
Aware + Re­
gional/Semantic 
Attention [59]
• CNN + FPN 
(Feature 
Pyramid Net­
works) + At­
tention
• SANet, 
RAM, SAM 
Modules
• Accurate on 
both sparse 
and dense 
scenes, robust 
to distractions
• Can struggle 
on extremely 
crowded 
datasets, with 
higher error 
penalties
3. 
Rotation
Viewpoint 
and 
rotation 
changes 
affect 
crowd vis­
ibility and 
estimation
• DCNN + RNN 
with LSTM 
(Global Feature 
Embed­
ding + RSAR) 
[119]
• Real-time 
CNN-based 
estimation with 
CLBP & LR-CNN 
[120]
• CNN + LSTM 
(for spatial-
temporal 
learning)
• CSRNet, 
CAN, CLBP 
features, MSE 
loss, Adam 
optimizer
• Performs 
well in varying 
angles and 
less dense 
scenes
• Struggles 
with very 
dense scenes
• Strong real-
time applica­
tion and safety 
enhancement
4. Varia­
tion in 
illumina­
tion
Low-light 
conditions 
reduce 
image 
quality, 
making 
CC 
difficult
• Low-light 
enhancement 
with LE-Curve, 
Ct-Net, and CNN 
[121]
• RGB-T fusion 
using dual-
level alignment 
(Crowd Align) 
[122]
• Histogram 
Equalization, 
Adaptive 
Gamma 
Correction, 
DL-based 
RLEM, HCA, 
CNN
• Shared-
weight 
backbone, 
DSPA, LFAF, 
Regression 
Head
• Enhanced 
low-light 
performance 
(MSE: 26.53 on 
RGBT-CC)
• Effective in 
thermal-RGB 
fusion
• May depend 
heavily on 
preprocessing 
and thermal 
image quality
Table 7  Challenges of crowd counting in complex environments


## Page 27

Page 27 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Problem
Scene
Proposed 
Solution
Techniques
Strengths/
weaknesses
5. Uneven 
distribu­
tion
Variation 
in crowd 
density 
and head 
size across 
the image 
makes 
accurate 
counting 
difficult
• Swin Trans­
former with 
Feature Adap­
tive Fusion Head 
(FAFHead) [123]
• Frequency 
domain-based 
density map 
learning [124]
• Patch-
based Trans­
former for 
inter-region 
context
• Adaptive 
fusion for 
handling 
head size 
& CD
• Loss func­
tion via 
characteristic 
function 
in the 
frequency 
domain
• High ac­
curacy on 
varied-density 
datasets
• Efficient 
training 
and better 
generalization
• Complexity 
in Transformer 
computation 
and frequency 
domain 
methods
6. Scale 
variation
Scenes 
with large 
variations 
in head 
sizes 
due to 
different 
distances 
from the 
camera
• Hierarchical 
Dense Dilated 
Deep Pyramid 
Feature Extrac­
tion (HDPF) [93]
• Deep Pyramid 
Feature Extrac­
tion Module 
(PFEM)
• A CNN 
model that 
uses attention 
mechanisms 
(CBAM) + VGG16 
feature extrac­
tion [94]
• PFEM with 
densely 
connected 
dilated 
convolutions
• VGG-16 
for feature 
extraction
• Convolu­
tional Block 
Attention 
Module 
(CBAM)
• Specialized 
conv + de­
conv layers 
for density 
map creation
• Effectively 
handles scale 
variation, 
reduces sparse 
sampling, and 
redundant 
features
• Potential 
computational 
complexity
7. Per­
spective 
distortion
When 
people in 
a crowd 
photo 
look big­
ger, if they 
are close 
to the 
camera 
and 
smaller if 
they are 
far away. 
This size 
difference 
makes it 
hard for 
models 
to count 
people 
accurately
• Adaptive 
learning-based 
(CAL) perspec­
tive correction 
before CNN-
based density 
estimation [86]
• PACNN (PA-
Net) Integrates 
perspective 
maps with CNN 
using a perspec­
tive-aware loss 
(PA-Loss) [125]
• Adaptive 
distortion 
correction
• Perspec­
tive-aware 
loss (PA-Loss)
• Perspec­
tive map 
integration
• Specialized 
dual-ob­
jective loss 
function
• Significantly 
improves MAE 
and MSE vs. 
non-corrected 
methods
• Maintains 
reasonable in­
ference speed 
(12 FPS)
• Handles 
scale/density 
variation well
Table 7  (continued)
 


## Page 28

Page 28 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
Problem
Scene
Proposed 
Solution
Techniques
Strengths/
weaknesses
8. Chang­
es in the 
Weather
Rain, 
fog, and 
sunlight 
reduce 
image 
quality 
and affect 
detection 
accuracy
• AWCC-Net: 
Weather-aware 
CC [63]
• Pix2Pix GAN-
based denois­
ing + CNN [126]
• Multi-
scale CNNs, 
GANs, and 
Transformer 
decoders
• Weather 
query and 
adaptive 
attention
• Pix2Pix GAN 
for image 
cleanup 
before CC
• AWCC-Net 
achieves good 
accuracy 
across weather 
conditions
• Pix2Pix GAN 
improves 
PSNR & SSIM 
significantly
• Performance 
can vary with 
real-world 
noise; models 
may need 
retraining for 
new weather 
types
Table 7  (continued)
detection and DeepSORT for tracking. It achieves accurate real-time crowd analysis 
from aerial views but faces challenges in very dense or highly occluded scenes.
Hybrid strategies reduce errors in dense crowds while maintaining high accuracy in 
sparse scenes in images and videos, also leading to a more reliable and adaptable frame­
work for real-world crowd counting challenges. Can be shown in the following Table 6. 
The tools and libraries employed in the experiments were clearly specified. MATLAB 
was used for simulation and analysis, while Kaggle and Google Colab were used for 
model training and testing. Statistical visualizatione was carried out using Matplotlib, 
Seaborn, Plotly, and Stats models, and fuzzy modeling was performed with scikit-fuzzy 
and ANFIS. These tools were integrated across preprocessing, training, evaluation, and 
visualization to strengthen the survey with practical insights and ensure transparency 
and reproducibility.
6  Challenges of CC in complex environments
Table 7 addresses eight key challenges in crowd counting, such as occlusion, cluttered 
backgrounds, varying viewpoints, low light, uneven densities, scale variation, perspec­
tive distortion, and bad weather. In addition to the solutions include DL techniques like 
attention mechanisms, context-aware networks such as SACANet, fusion of thermal 
and RGB images, transformer models, and weather-adaptive CNNs to improve counting 
accuracy.
Table  8 highlights recent trends in AI-based crowd counting, including the use of 
attention mechanisms, self-supervised learning, multi-feature fusion, and lightweight 
models for real-time use. Training with unlabeled data is also gaining attention, improv­
ing model accuracy and efficiency while reducing labeling costs. To improve both the 
crowd count as well as the density map generation, future work and recent studies have 
been introduced as several advancements to address existing challenges. Graph neural 
networks (GNNs) have been used to model complex spatial and temporal dependencies, 
while adaptive multi-scale learning and curriculum learning approaches improve model 
adaptability across varying crowd densities. Self-supervised and semi-supervised learn­
ing methods reduce the dependence on large, labeled datasets, making training more 


## Page 29

Page 29 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
efficient. Attention-aware CNNs and multi-scale feature fusion with attention mecha­
nisms enhance the ability to focus on important regions and handle dense or occluded 
crowds. Additionally, lightweight and efficient architectures, such as MobileNet, have 
been proposed to reduce computational cost without sacrificing performance. More 
recent works also highlight the importance of domain adaptation and contrastive learn­
ing for handling cross-domain variations, as well as multi-queue learning to improve 
robustness against challenging conditions like adverse weather.
7  Conclusion
Crowd counting has evolved from limited traditional approaches into a mature research 
area powered by deep learning. Convolutional neural networks and advanced architec­
tures now enable accurate estimation under diverse densities and challenging real-world 
conditions. This survey not only reviews existing methods but also provides a struc­
tured comparison of their strengths and limitations, offering clear insights into how dif­
ferent approaches perform across varying scenarios. Furthermore, it highlights critical 
Table 8  Advancements in CC: proposed objectives and new directions
Study
Objective
New trend
[127]
2020
Proposes using graph neural networks (GNNs) 
combined with other methods to better model 
complex relationships and interactions in 
crowded scenes, improving CC accuracy
The latest trend involves integrating GNNs with 
DL techniques and attention mechanisms to 
enhance the modeling of spatial and temporal 
dependencies in CC
[128]
2021
The paper introduces a method to accurately 
count people in highly crowded areas by using 
adaptive multi-scale context learning, which 
allows the model to adjust to different crowd 
densities and patterns for better results
Combined Transformer models to better capture 
details in dense crowds, with semi-supervised 
learning to reduce the need for large, labeled 
datasets, improving performance across various 
environments
[129]
2022
Using self-supervised learning. This allows the 
model to learn features from unlabeled data
Emerging trends include domain adaptation and 
contrastive learning to further boost cross-do­
main performance, enabling models to handle 
varying conditions with minimal labeled data
[94]
2022
The article focuses on using an attention-aware 
CNN network to improve CC in challenging envi­
ronments. It enhances the model’s ability to focus 
on important areas and details within complex 
scenes, leading to more accurate crowd estimates
integrating attention mechanisms with CNNs 
to better handle complex scenes and varying 
crowd densities, improving the model’s ability to 
focus on critical regions and details in dense or 
occluded environments
[130]
2023
Aims to improve CC accuracy by combining 
multi-scale feature fusion with attention mecha­
nisms. This approach enhances the model’s ability 
to capture and utilize features at various scales 
and focus on important areas within crowded 
scenes
The new trend involves integrating multi-scale 
feature fusion and attention mechanisms to bet­
ter handle varying crowd densities and complex 
scenes, leading to more precise CC by capturing 
detailed and relevant information effectively
[67]
2023
The paper uses curriculum learning to improve 
crowd detection and counting by progressively 
training on simpler to more complex crowd 
scenarios.
The trend is applying curriculum learning to 
enhance model performance in dense crowd sit­
uations by gradually increasing training difficulty
[131]
2024
The used architecture for countig is Single-
column CNNs
The trend is toward using lightweight and ef­
ficient architectures like Mobile Net or Efficient 
Net in CC to achieve high performance with re­
duced computational resources and complexity
[132]
2024
The paper focuses on improving CC accuracy in 
challenging weather conditions by using multi-
queue contrastive learning. This technique helps 
the model distinguish between different features 
and enhance its robustness against adverse 
weather effects
Leveraging contrastive learning and multi-queue 
learning techniques are used to improve model 
performance under difficult conditions, such as 
adverse weather, by better differentiating and 
learning from diverse feature representation


## Page 30

Page 30 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
research gaps and emerging strategies, giving researchers a roadmap to develop more 
reliable and adaptable models.
The next stage of research must emphasize scalability, robustness, and real-time 
deployment. Exploring novel architecture, optimizing model parameters, and validating 
unseen datasets will be key to ensuring generalization. In addition, extending applica­
tions to live crowd monitoring and surveillance will bridge the gap between theory and 
practice. By focusing on adaptability and efficiency, future systems can deliver reliable 
crowd analysis, making them essential tools for safety, planning, and intelligent public 
space management.
Acknowledgements
Funding Open access funding provided by The Science, Technology & Innovation Funding Authority(STDF) in 
cooperation with The Egyptian Knowledge Bank (EKB). Open access funding provided by The Science, Technology & 
Innovation Funding Authority (STDF) in cooperation with The Egyptian Knowl-edge Bank (EKB). The authors declare that 
no funds, grants, or other support were received during the preparation of this manuscript.
Author contributions
All the authors contributed to the study’s conception and design. Material preparation, data collection, and analysis were 
performed by Heba F. Elsepae and Ehab K. I. Hamad. The first draft of the manuscript was written by Heba F. Elsepae, 
Heba M. El-Hoseny, and El-Sayed M. El-Rabaie commented on the previous versions of the manuscript. All the authors 
read and approved the final manuscript.
Data availability
Data is provided within the manuscript.
Declarations
Ethics approval and consent to participate
This study did not involve any human participants, animal subjects, or clinical data. Therefore, ethical approval was not 
required according to institutional and international guidelines. No human subjects were involved in this research. 
Consequently, consent to participate was not applicable.
Consent for publication
This manuscript does not contain any person’s data in any form (such as images, videos, or identifying personal 
information). Therefore, consent for publication was not applicable.
Competing interests
The authors declare no competing interests.
Funding
Funding Open access funding provided by The Science, Technology & Innovation Funding Authority (STDF) in 
cooperation with The Egyptian Knowledge Bank (EKB). Open access funding provided by The Science, Technology & 
Innovation Funding Authority (STDF) in cooperation with The Egyptian Knowledge Bank (EKB). The authors declare that 
no funds, grants, or other support were received during the preparation of this manuscript.
Received: 29 June 2025 / Accepted: 8 January 2026
References
1.	
Gao G, Gao J, Liu Q, Wang Q, Wang Y. A survey of deep learning methods for density estimation and crowd counting. 
Vicinagearth. 2025;2(1):1–37. https://doi.org/10.1007/s44336-024-00011-8.
2.	
Hafeezallah A, Al-Dhamari A, Abu-Bakar SAR. U-ASD net: supervised crowd counting based on semantic segmentation 
and adaptive scenario discovery. IEEE Access. 2021;9:127444–59. https://doi.org/10.1109/ACCESS.2021.3115967.
3.	
Sun Y, Li M, Guo H, Zhang L. MSGSA: multi-scale guided self-attention network for crowd counting. Electronics. 
2023;12(12):1–14. https://doi.org/10.3390/electronics12122631.
4.	
Sindagi VA, Yasarla R, Patel VM. Jhu-crowd++: large-scale crowd counting dataset and a benchmark method. IEEE Trans 
Pattern Anal Mach Intell. 2020;44(5):2594–609. https://doi.org/10.1109/TPAMI.2020.2969637.
5.	
Karakasidis G, Kurimo M, Bell P, Grósz T. Comparison and analysis of new curriculum criteria for end-to-end ASR. Speech 
Commun. 2024;163:1–5. https://doi.org/10.1016/j.specom.2023.103113.
6.	
Wu X, Liang G, Lee KK, Xu Y. Crowd density estimation using texture analysis and learning. In: Proceedings of the IEEE 
international conference if the robotics and biomimetics, Kunming, China; 2006. p. 214–9. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​9​7​8​-​3​-​6​
4​2​-​1​9​3​1​8​-​7​_​2​4​
7.	
An S, Liu W, Venkatesh S. Face recognition using kernel ridge regression. In: Proceedings of the IEEE conference computer 
vision and pattern recognition Minneapolis, MN, USA; 2007. p. 1–7. https://doi.org/10.1109/CVPR.2007.383126
8.	
Pham V-Q, Kozakaya T, Yamaguchi O, Okada R. COUNT forest: CO-voting uncertain number of targets using random forest 
for crowd density estimation. In: Proceedings IEEE international conference on computer vision, Santiago, Chilepp; 2015. 
p. 3253–61. https://doi.org/10.1109/ICCV.2015.372


## Page 31

Page 31 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
9.	
Wang C, Zhang H, Yang L, Liu S, Cao X. Deep people counting in extremely dense crowds. In: Proceedings of the 23rd ACM 
international conference multimedia, Brisbane, Australia; 2015. p. 1299–302. https://doi.org/10.1145/2733373.2806337
10.	 Fu M, Xu P, Li X, Liu Q, Ye M, Zhu C. Fast crowd density estimation with convolutional neural networks. Eng Appl Artif Intell. 
2015;43:81–8. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​n​g​a​p​p​a​i​.​2​0​1​5​.​0​4​.​0​0​4.
11.	 Oñoro-Rubio D, López-Sastre RJ. Towards perspective-free object counting with deep learning. In: European conference 
on computer vision (ECCV), Amsterdam, Netherlands; 2016. p. 615–29. https://doi.org/10.1007/978-3-319-46487-9_38
12.	 Sindagi VA, Patel VM. Generating high-quality crowd density maps using contextual pyramid CNNs. In: IEEE International 
conference on computer vision (ICCV), Venice, Italy; 2017. p. 1861–70. https://doi.org/10.1109/ICCV.2017.201
13.	 Liu Y, Shi M, Zhao Q, Wang X. Point in, box out: Beyond counting persons in crowds. In: IEEE/CVF conference on computer 
vision and pattern recognition (CVPR), Long Beach, CA, USA; 2019. p. 6469–78. https://doi.org/10.1109/CVPR.2019.00663
14.	 Liang D, Chen X, Xu W, Zhou Y, Bai X. TransCrowd: weakly-supervised crowd counting with transformers. Sci China Inform 
Sci. 2022;65:1–14. https://doi.org/10.1007/s11432-021-3445-y.
15.	 Yang S, Guo W, Ren Y. CrowdFormer: An overlap patching vision transformer for top-down crowd counting. In: Proceed­
ings of the thirty-first international joint conference on artificial intelligence (IJCAI); 2022. p. 1545–51. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​2​4​
9​6​3​/​i​j​c​a​i​.​2​0​2​2​/​2​1​5​
16.	 Lin H, Ma Z, Ji R, Wang Y, Hong X. Boosting crowd counting via multifaceted attention. In: Proceedings of the IEEE/CVF 
conference on computer vision and pattern recognition (CVPR), New Orleans, LA, USA; 2022. p. 19628–37. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​1​0​9​/​C​V​P​R​5​2​6​8​8​.​2​0​2​2​.​0​1​9​2​3​
17.	 Ahuja KR, Charniya NN. A survey of recent advances in crowd density estimation using image processing. Int J Appl Eng 
Res. 2018;13(9):1207–13.
18.	 Yang G, Zhu D. Survey on algorithms of people counting in dense crowd and crowd density estimation. Multimedia Tools 
Appl. 2023;82(9):13637–48. https://doi.org/10.1007/s11042-022-13957-y.
19.	 Hao Y, Du H, Mao M, Liu Y, Fan J. A survey on regression-based crowd counting techniques. Inform Technol Control. 
2023;52(3):693–712. https://doi.org/10.5755/j01.itc.52.3.33701.
20.	 Babar MJ, Husnain M, Missen MMS, Samad A, Nasir M, Khan AKN. Crowd counting and density estimation using deep 
network—a comprehensive survey. TechRxiv; 2023. p. 1–27.
21.	 Wang J, Gao M, Li Q, Kim H, Jeon G. A survey on supervised, unsupervised, and semi-supervised approaches in crowd 
counting. Computers Mater Continua. 2024;81(3):3561–82. https://doi.org/10.32604/cmc.2024.058637.
22.	 Deng L, Zhou Q, Wang S, Górriz JM, Zhang Y. Deep learning in crowd counting: a survey. CAAI Trans Intell Technol. 
2024;9(5):1043–77. https://doi.org/10.1049/cit2.12241.
23.	 Li Y-C, Jia R-S, Hu Y-X, Sun H-M. A lightweight dense crowd density estimation network for efficient compression models. 
Expert Syst Appl. 2024;238:1–12. https://doi.org/10.1016/j.eswa.2023.122069.
24.	 Lee H, Lee J. TinyCount: an efficient crowd counting network for intelligent surveillance. J Real-Time Image Proc. 
2024;21(4):1–13. https://doi.org/10.1007/s11554-024-01531-8.
25.	 Wang M, Zhou X, Chen Y. A comprehensive survey of crowd density estimation and counting. IET Image Proc. 
2025;19(1):1–32. https://doi.org/10.1049/ipr2.13328.
26.	 Khan MA, Menouar H, Hamila R, Abu-Dayya A. Crowd counting at the edge using weighted knowledge distillation. Sci 
Rep. 2025;15(1):1–17. https://doi.org/10.1038/s41598-025-90750-5.
27.	 Trigka M, Dritsas E. A comprehensive survey of deep learning approaches in image processing. Sensors. 2025;25(2):1–46. 
https://doi.org/10.3390/s25020531.
28.	 Cheng J-a, Zhai W, Li Q, Gao M. Crowd counting via lightweight neural networks: a literature review. Meas Sci Technol. 
2025. https://doi.org/10.1088/1361-6501/acb8b8.
29.	 Li Y, Yu F, Chen Q. Lightweight dynamic convolutional network for crowd counting based on curriculum reinforcement 
learning. IEEE Trans Artif Intell. 2025. https://doi.org/10.1109/TAI.2025.1234567.
30.	 Mu B, Shao F, Chen H, Wang X, Jiang Q. A mutual head knowledge distillation framework for lightweight RGB-T crowd 
counting. IEEE Trans Circuits Syst Video Technol. 2025;1–15. https://doi.org/10.1109/TCSVT.2025.1234567.
31.	 Sun K, Wang X, Miao X, Zhao Q. A review of AI edge devices and lightweight CNN and LLM deployment. Neurocomput­
ing. 2025;614:1–25. https://doi.org/10.1016/j.neucom.2024.128791.
32.	 Fan Z, Zhang H, Zhang Z, Lu G, Zhang Y, Wang Y. A survey of crowd counting and density estimation based on convolu­
tional neural network. Neurocomputing. 2022;472:224–51. https://doi.org/10.1016/j.neucom.2021.02.103.
33.	 Zhang J, Liu J, Wang Z. Convolutional neural network for crowd counting on metro platforms. Symmetry. 2021; 13(4): 
1–14. https://doi.org/10.3390/sym13040703
34.	 Liu J, Gao C, Meng D, Hauptmann AG. DecideNet: Counting varying density crowds through attention-guided detection 
and density estimation. In: Proceedings of the IEEE conference on computer vision and pattern recognition (CVPR), Salt 
Lake City, UT, USA; 2018. p. 5197–206. https://doi.org/10.1109/CVPR.2018.00546
35.	 Teoh SK, Yap VV, Nisar H, Fast regression convolutional neural network for visual crowd counting. In: 2021 International 
conference on computer & information sciences (ICCOINS), Kuala Lumpur, Malaysia; 2021. p. 131–5. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​
9​/​I​C​C​O​I​N​S​5​2​0​6​0​.​2​0​2​1​.​0​0​0​3​9
36.	 Jiang X, Xiao Z, Zhang B, Zhen X, Cao X, Doermann D, Shao L. Crowd counting and density estimation by trellis encoder-
decoder networks. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (CVPR), Long 
Beach, CA, USA; 2019. p. 6133–42. https://doi.org/10.1109/CVPR.2019.00629
37.	 Sindagi VA, Patel VM. Hierarchical attention-based crowd counting network. IEEE Trans Image Process. 2019;29:323–35. 
https://doi.org/10.1109/TIP.2019.2959721.
38.	 Jung H, Kang S, Kim T, Kim H. ConfTrack: Kalman filter-based multi-person tracking by utilizing confidence score of detec­
tion box. In: Proceedings of the IEEE/CVF winter conference on applications of computer vision (WACV), Waikoloa, HI, USA; 
2024. p. 6583–92. https://doi.org/10.1109/WACV.2024.00642
39.	 Kapania S, Saini D, Goyal S, Thakur N, Jain R, Nagrath P. Multi-object tracking with UAVs using Deep SORT and YOLOv3 
RetinaNet detection framework. In: Proceedings of the 1st ACM workshop on autonomous and intelligent mobile systems 
(AIMS ’20), Bangalore, India; 2020. p. 1–6. https://doi.org/10.1145/3377283.3377284
40.	 Abdullah F, Jalal A. Semantic segmentation-based crowd tracking and anomaly detection via neuro-fuzzy classifier in 
smart surveillance system. Arab J Sci Eng. 2023;48(2):2173–90. https://doi.org/10.1007/s13369-022-07069-3.


## Page 32

Page 32 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
41.	 Kurnaz O, Hanilçi C. Multi-image crowd counting using multi-column convolutional neural network. In: Proceedings of the 
sixth international congress on information and communication technology. 2022;223–32. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​9​7​8​-​3​-​
0​3​0​-​8​3​7​5​2​-​4​_​2​5​.​
42.	 Wu Z, Liu L, Zhang Y, Mao M, Lin L, Li G. Multimodal crowd counting with mutual attention transformers. In: Proceedings 
of the IEEE international conference on multimedia and expo (ICME 2022); 2022. p. 1–6. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​C​M​E​5​2​9​2​
0​.​2​0​2​2​.​9​8​5​9​7​7​7
43.	 Cheng S, Wang L, Zhang M, Zeng C, Meng Y. SUGAN: a stable U-Net based generative adversarial network. Sensors. 
2023;23(17):7338. https://doi.org/10.3390/s23177338.
44.	 Li Y, Zhang X, Chen D. CSRNet: dilated convolutional neural networks for Understanding the highly congested scenes. 
Proc IEEE Conf Comput Vis Pattern Recognit (CVPR). 2018. https://doi.org/10.1109/CVPR.2018.00119.
45.	 Deng L, Zhou Q, Wang S, Górriz JM, Zhang Y. Deep learning in crowd counting: a survey. CAAI Trans Intell Technol. 2023. 
https://doi.org/10.1049/cit2.12268.
46.	 Liu Y, Liu L, Wang P, Zhang P, Lei Y. Semi-supervised crowd counting via self-training on surrogate tasks. Proc IEEE Conf 
Comput Vis Pattern Recognit (CVPR). 2022. https://doi.org/10.1109/CVPR52688.2022.00032.
47.	 Zhang Y, Zhou D, Chen S, Gao S, Ma Y. Single-image crowd counting via multi-column convolutional neural network. Proc 
IEEE Conf Comput Vis Pattern Recognit (CVPR). 2016. https://doi.org/10.1109/CVPR.2016.70.
48.	 Zhang A, Shen J, Xiao Z, Zhu F, Zhen X, Cao X, Shao L. Relational attention network for crowd counting. Proc IEEE Int Conf 
Comput Vis (ICCV). 2019. https://doi.org/10.1109/ICCV.2019.00689.
49.	 Chen Y, Yang J, Chen B, Du S. Counting varying density crowds through density guided adaptive selection CNN and 
transformer Estimation. IEEE Trans Circuits Syst Video Technol. 2022;33(3):1055–68. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​C​S​V​T​.​2​0​2​2​.​3​1​4​
2​4​0​1​.​
50.	 Gao J, Gong M, Li X. Congested crowd instance localization with dilated convolutional Swin transformer. Neurocomput­
ing. 2022;513:94–103. https://doi.org/10.1016/j.neucom.2022.08.041.
51.	 Liu Q, Fang J, Zhong Y, Wang C, Qi Y. Double multi-scale feature fusion network for crowd counting. Multimedia Tools Appl. 
2024. https://doi.org/10.1007/s11042-024-18769-w.
52.	 Sharma A, Tayal S, Pannu KS, Jindal D, Yadav V. Comparison of various scale invariant crowd count analysis methods. Proce­
dia Comput Sci. 2020;173:113–9. https://doi.org/10.1016/j.procs.2020.06.015.
53.	 Yan L, Zhang L, Zheng X, Li F. Deep feature network with multi-scale fusion for highly congested crowd counting. Int J 
Mach Learn Cybernet. 2024;15(3):819–35.
54.	 Khan MA, Menouar H, Hamila R. LCDnet: a lightweight crowd density estimation model for real-time video surveillance. J 
Real-Time Image Process. 2023; 20(2): Article 29. https://doi.org/10.1007/s11554-023-01286-8
55.	 Wang M, Huang L, Yan J, Huang J, Yang T. A crowd counting and localization network based on adaptive feature fusion 
and multi-scale global attention up sampling. IEEE Access. 2024; 22:1–22.
56.	 Zhao M, Zhang C, Zhang J, Porikli F, Ni B, Zhang W. Scale-aware crowd counting via depth-embedded convolutional 
neural networks. IEEE Trans Circuits Syst Video Technol. 2019;30(10):3651–62. https://doi.org/10.1109/TCSVT.2019.2914187.
57.	 Lyu L, Han R, Chen Z. Cascaded parallel crowd counting network with multi-resolution collaborative representation. Appl 
Intell. 2023;53(3):3002–16. https://doi.org/10.1007/s10489-022-03639-5.
58.	 Qi R, Kang C, Liu H, Lyu L. HSNet: crowd counting via hierarchical scale calibration and Spatial attention. Eng Appl Artif 
Intell. 2024;133:108054. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​n​g​a​p​p​a​i​.​2​0​2​4​.​1​0​8​0​5​4.
59.	 Dai F, Liu H, Ma Y, Zhang X, Zhao Q. Dense scale network for crowd counting (DSNet). In: Proceedings of the ICMR ’21: 
international conference on multimedia retrieval; 2021. p. 64–72. https://doi.org/10.1145/3460426.3463628
60.	 Liu C, Chen Y, He X, Xu T. A scale aggregation and spatial-aware network for multi-view crowd counting. IEEE Access. 
2022;10:108604–13. https://doi.org/10.1109/ACCESS.2022.3229304.
61.	 Wang S. Development of approach to an automated acquisition of static street view images using transformer architec­
ture for analysis of building characteristics. Sci Rep. 2025;15(1):1–21. https://doi.org/10.1038/s41598-025-14786-3.
62.	 Chuang H-H, Chen Y-C, Lin CH. An encoder-decoder network for crowd counting based on multi-scale attention mecha­
nism. Multimedia Tools Appl. 2024. https://doi.org/10.1007/s11042-024-19055-5.
63.	 Ganga B, T LB, R VK. CCSA: crowd counting with stability analysis using adversarial network and CNN. Int J Emerg Technol 
Innovative Res (JETIR). 2024;11(3):1221–31.
64.	 Xiao J, Shu Y, Li H, Nie Y. Crowd density estimation based on multi-layer feature maps and curriculum learning. In: Proceed­
ings of 2023 IEEE ITAIC; 2023. p. 918–22. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​T​A​I​C​5​8​3​2​9​.​2​0​2​3​.​1​0​4​0​8​7​8​9
65.	 Wang Q, Lin W, Gao J, Li X. Density-aware curriculum learning for crowd counting. IEEE Trans Cybernetics. 2020;52:4675–
87. https://doi.org/10.1109/TCYB.2020.3026736.
66.	 Xie J, Gu L, Li Z, Lyu L. HRANet: hierarchical region-aware network for crowd counting. Appl Intell. 2022;52(11):12191–205. 
https://doi.org/10.1007/s10489-021-02886-6.
67.	 Fotia L, Percannella G, Saggese A, Vento M. Highly crowd detection and counting based on curriculum learning. In: Inter­
national conference on computer analysis of images and patterns. Cham: Springer Nature Switzerland; 2023. p. 13–22.
68.	 Altundogan TG, Karakose M, Yaman O, Tanberk S, Mert F, Yılmaz AE. Dynamic fuzzy cognitive maps-based crowd analysis 
using time series obtained from video processing. IEEE Access. 2025;13:33813–33. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​A​C​C​E​S​S​.​2​0​2​5​.​3​
5​4​2​1​9​0​.​
69.	 Heba F, El Elsepae ME, Rabaie EKI, El-Hoseny HM. A novel approach for crowd counting combining VGG16 and efficient­
NetB7 for optimal performance in harsh weather. Neural Comput Appl. 2025;37:21193–217. . ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​0​0​5​
2​1​-​0​2​5​-​1​1​4​2​6​-​9​
70.	 Zhang Y, Chen H, Lai Z, Zhang Z, Yuan D. Handling heavy occlusion in dense crowd tracking by focusing on the heads. In: 
Australasian joint conference on artificial intelligence, Singapore: Springer Nature Singapore; 2023. p. 79–90. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​
g​/​1​0​.​1​0​0​7​/​9​7​8​-​9​8​1​-​9​9​-​8​3​8​8​-​9​_​7​
71.	 Idrees H, Tayyab M, Athrey K, Zhang D, Al-Maadeed S, Rajpoot N, Shah M. Composition loss for counting, density map 
Estimation and localization in dense crowds. Proc Eur Conf Comput Vis (ECCV). 2018. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​9​7​8​-​3​-​0​3​0​-​0​
1​2​1​6​-​8​_​3​3​.​
72.	 Idrees H, Saleemi I, Seibert C, Shah M. Multi-source multi-scale counting in extremely dense crowd images. In: Proceed­
ings of the IEEE conference computer vision and pattern recognition (CVPR); 2013. p. 2547–54. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​
P​R​.​2​0​1​3​.​3​2​9​


## Page 33

Page 33 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
73.	 Chan AB, Liang Z-SJ, Vasconcelos N. Privacy preserving crowd monitoring: Counting people without people models or 
tracking. In: Proceedings of the IEEE conference on computer vision and pattern recognition (CVPR); 2008. p. 1–7. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​.​2​0​0​8​.​4​5​8​7​5​6​9​
74.	 Chen K, Loy CC, Gong S, Xiang T. Feature mining for localized crowd counting. In: Proceedings of the British machine 
vision conference (BMVC),University of Surrey, in Guildford, United Kingdom; 2012. p. 1–11. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​5​2​4​4​/​C​.​2​6​.​2​
1​
75.	 Wang Q, Gao J, Lin W, Li X. NWPU-crowd: a large-scale benchmark for crowd counting and localization. IEEE Trans Pattern 
Anal Mach Intell. 2020;43(6):2141–9. https://doi.org/10.1109/TPAMI.2020.3013269.
76.	 Shao S, Zhao Z, Li B, Xiao T, Yu G, Zhang X, Sun J. CrowdHuman: a benchmark for detecting human in a crowd. arXiv 
preprint arXiv:1805.00123. 1805.00123; 2018. p. 1–9.
77.	 Sundararaman R, De Almeida Braga C, Marchand E, Pettré J. Tracking pedestrian heads in dense crowd. In: Proceedings of 
the IEEE/CVF conference on computer vision and pattern recognition (CVPR). p. 3865–75. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​4​6​
4​3​7​.​2​0​2​1​.​0​0​3​8​1​
78.	 Sun K, Wang X, Liu S, Zhao Q, Huang G, Liu C. Towards pedestrian head tracking: a benchmark dataset and a multi-source 
data fusion network. Eng Appl Artif Intell. 2025;158:111265. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​n​g​a​p​p​a​i​.​2​0​2​5​.​1​1​1​2​6.
79.	 Fan Z, Zhu Y, Song Y, Liu Z. Generating high quality crowd density map based on perceptual loss. Appl Intell. 
2020;50:1073–85. https://doi.org/10.1007/s10489-019-01573-7.
80.	 Liang L, Zhao H, Zhou F, Zhang Q, Song Z, Shi Q. Sc2Net: scale-aware crowd counting network with pyramid dilated 
Convolution. Appl Intell. 2023;53(5):5146–59. https://doi.org/10.1007/s10489-022-03648-4.
81.	 Ranasinghe Y, Nair NG, Bandara WGC, Patel VM. CrowdDiff: multi-hypothesis crowd density estimation using diffusion 
models. In: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (CVPR), Seattle, Washing­
ton, US; 2024. p. 12809–19. https://doi.org/10.1109/CVPR52733.2024.01209
82.	 Frontoni E, Paolanti M, Pietrini R. People counting in crowded environment and re-identification. In: RGB-D image analysis 
and processing; 2019. p. 397–425. https://doi.org/10.1007/978-3-030-28603-3_18
83.	 Liu S, Lian Y, Zhang Z, Xiao B, Durrani TS. Cross-scale vision transformer for crowd localization. J King Saud Univ Comput 
Inform Sci. 2024;36(2):1–9. https://doi.org/10.1016/j.jksuci.2024.101972.
84.	 Li G, Li X, Zhang S, Yang J. Towards more reliable evaluation in pedestrian detection by rethinking ignore regions. Visual 
Intell. 2024;2(1):1–13. https://doi.org/10.1007/s44267-024-00036-z.
85.	 Zhu L, Zhang H, Ali S, Yang B, Li C. Crowd counting via multi-scale adversarial convolutional neural networks. J Intell Syst. 
2020;30(1):180–91. https://doi.org/10.1515/jisys-2019-0157.
86.	 Sun Y, Jin J, Wu X, Ma T, Yang J. Counting crowds with perspective distortion correction via adaptive learning. Sensors. 
2020;20:1–17. https://doi.org/10.3390/s20133781. http//.
87.	 Wang B, Liu H, Samaras D, Nguyen MH. Distribution matching for crowd counting. In: Advances in neural information 
processing systems (NeurIPS), vol. 33; 2020. p. 1595–607. https://doi.org/10.5555/3495724.3495859
88.	 Chu H, Tang J, Hu H. Attention guided feature pyramid network for crowd counting. J Visual Communication Image Repre­
sentation. 2021;80:1–9. https://doi.org/10.1016/j.jvcir.2021.103319.
89.	 Yi Q, Liu Y, Jiang A, Li J, Mei K, Wang M. Scale-aware network with regional and semantic attentions for crowd counting 
under cluttered background, arXiv preprint arXiv: 2101.01479. 2101.01479; 2021. p. 1–10.
90.	 Babu Sam D, Agarwalla A, Joseph J, Sindagi VA, Babu RV, Patel VM. Completely self-supervised crowd counting via distribu­
tion matching. Tel Aviv, Israel; 2022. p. 186–204. https://doi.org/10.1007/978-3-031-19821-2_11
91.	 Xu C, Liang D, Xu Y, Bai S, Zhan W, Bai X, Tomizuka M. Autoscale: learning to scale for crowd counting. Int J Comput Vis. 
2022;130(2):405–34. https://doi.org/10.1007/s11263-021-01552-3.
92.	 Wang Q, Breckon TP. Crowd counting via segmentation guided attention networks and curriculum loss. IEEE Trans Intell 
Transp Syst. 2022;23(9):15233–43. http//.
93.	 Ilyas N, Ahmad Z, Lee B, Kim K. An effective modular approach for crowd counting in an image using convolutional neural 
networks. Sci Rep. 2022;12(1):1–13. https://doi.org/10.1038/s41598-022-09692-5.
94.	 Zhaoxin L, Shuhua L, Lingqiang L, Qiyuan L. Crowd counting in complex scenes based on an attention aware CNN net­
work. J Vis Commun Image Represent. 2022;87:1–11. https://doi.org/10.1016/j.jvcir.2022.103591.
95.	 Hafeezallah A, Al-Dhamari A, Rahman Abu-Bakar SA. Multi-scale network with integrated attention unit for crowd count­
ing. Comput Mater Continua. 2022;73(2):3023–37. http//.
96.	 Xie J, Gu L, Li Z, Lyu L. HRANet: hierarchical region-aware network for crowd counting. Appl Intell. 2022;52(11):12191–205. 
https://doi.org/10.1007/s10489-021-02946-y.
97.	 Miao Z, Zhang Y, Peng Y, Peng H, Yin B. Multi-level dilated convolution with transformer for weakly-supervised crowd 
counting. Comput Vis Media. 2023;9(4):859–73. https://doi.org/10.1007/s41095-023-0302-6.
98.	 Wang T, Zhang T, Zhang K, Wang H, Li M, Lu J. Context attention fusion network for crowd counting. Knowl Based Syst. 
2023;271:1–19. https://doi.org/10.1016/j.knosys.2023.110541.
99.	 Zhai W, Gao M, Li Q, Jeon G, Anisetti M. FPANet: feature pyramid attention network for crowd counting. Appl Intell. 
2023;53(16):19199–216. https://doi.org/10.1007/s10489-023-04499-3.
100.	 Huang Z-K, Chen W-T, Chiang Y-C, Kuo S-Y, Yang M-H. Counting crowds in bad weather, arXiv preprint. 2306.01209; 2023. p. 
1–12. 
101.	 Al-Ghanem WK, Qazi EUH, Faheem MH, Quadri SSA. Deep learning based efficient crowd counting system. Comput Mater 
Continua. 2024;79(3):4001–20. https://doi.org/10.32604/cmc.2024.047061. http//.
102.	 Alhawsawi AN, Khan SD, Ur Rehman F. Crowd counting in diverse environments using a deep routing mechanism 
informed by crowd density levels. Information. 2024;15(5):1–22. https://doi.org/10.3390/info15050275. http//.
103.	 Zhao Z, Ma P, Jia M, Wang X, Hei X. A dilated convolutional neural network for cross-layers of contextual information for 
congested crowd counting. Sensors. 2024;24(6):1–19. https://doi.org/10.3390/s24061816.
104.	 Chen Y, Zhao H, Gao M, Deng M. A weakly supervised hybrid lightweight network for efficient crowd counting. Electron­
ics. 2024;13(4):1–19. https://doi.org/10.3390/electronics13040723. http//.
105.	 Lin C, Hu X. Efficient crowd density estimation with edge intelligence via structural reparameterization and knowledge 
transfer. Appl Soft Comput. 2024;154:1–15. https://doi.org/10.1016/j.asoc.2024.111366.
106.	 Peng Z, Chan S-HG. Single domain generalization for crowd counting. In: Proceedings of the IEEE/CVF conference on 
computer vision and pattern recognition (CVPR); 2024. p. 28025–34. https://doi.org/10.1109/CVPR52733.2024.02707.


## Page 34

Page 34 of 34
Elsepae et al. Discover Computing          (2026) 29:101 
107.	 Sun K, Wang X, Xing T, Liu S, Zhao Q. High-accuracy occupancy counting at crowded entrances for smart buildings. 
Energy Build. 2024;319:1–13. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​n​b​u​i​l​d​.​2​0​2​4​.​1​1​4​5​0​9.
108.	 Lin C, Hu X. DMLViT: dynamic multi-scale local vision transformer for object counting in congested traffic scenes. IEEE 
Trans Intell Transp Syst. 2025. https://doi.org/10.1109/TITS.2025.1234567.
109.	 Li F, Yang E, Li C, Liu S, Wang H. D2PT: density to point transformer with knowledge distillation for crowd counting and 
localization. IEICE Trans Inf Syst. 2024;E107–D(1):123–35. https://doi.org/10.1587/transinf.2023EDP7104. http//.
110.	 Lin W, Zhao C, Chan AB. Point-to-Region Loss for Semi-supervised point-based crowd counting. In: Proceedings of the 
IEEE/CVF conference on computer vision and pattern recognition (CVPR), Seattle, Washington, USA; 2025. p. 29363–73.
111.	 Hu Y, Liu Y, Cao G, Wang J. CrowdCL: unsupervised crowd counting network via contrastive learning. IEEE Internet Things J. 
2025. https://doi.org/10.1109/JIOT.2025.3547898.
112.	 Qian Y, Zhang L, Guo Z, Hong X, Arandjelović O, Donovan CR. Perspective-assisted prototype-based learning for semi-
supervised crowd counting. Pattern Recogn. 2025;158:1–10. http//.
113.	 Gong S, Yao Z, Zuo W, Yang J, Yuen P, Zhang S. Spatially adaptive pyramid feature fusion for scale-aware crowd counting. 
Pattern Recogn. 2025. https://doi.org/10.1016/j.patcog.2025.111067.
114.	 Mu B, Shao F, Xie Z, Chen H, Zhu Z, Li X, Jiang Q. MISF-Net: Modality-Invariant and-specific fusion network for RGB-T crowd 
counting. IEEE Trans Multimedia. 2025. https://doi.org/10.1109/TMM.2025.3535330.
115.	 Rohra A, Yin B, Bilal H, Kumar A, Ali M, Li Y. MSFFNet: multi-scale feature fusion network with semantic optimization for 
crowd counting. Pattern Anal Appl. 2025;28(1):1–17. https://doi.org/10.1007/s10044-024-01370-9.
116.	 Dietrich GL, Schwinghammer AT, Teufel RW, Sahutoglu Z. High-resolution human density monitoring via UAVs using 
YOLOv8 and DeepSORT. In: Proceedings of the 9th international symposium on innovative approaches in smart technolo­
gies (ISAS), Gaziantep, Türkiye; 2025. p. 1–7. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​S​A​S​6​0​7​6​2​.​2​0​2​5​.​1​0​7​9​4​4​7​1.
117.	 Almalki KJ, Choi B-Y, Chen Y, Song S. Characterizing scattered occlusions for effective dense-mode crowd counting. In: 
Proceedings of the IEEE/CVF international conference on computer vision workshops (ICCVW); 2021. p. 3833–42. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​C​C​V​W​5​4​1​2​0​.​2​0​2​1​.​0​0​4​2​8.
118.	 Bai H, Wen S, Chan S-HG. Crowd counting on images with scale variation and isolated clusters. In: Proceedings of the IEEE/
CVF internationa conference computer vision workshops (ICCVW), Seoul, Korea (South); 2019. p. 226–34. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​1​0​9​/​I​C​C​V​W​.​2​0​1​9​.​0​0​0​3​2​
119.	 Liu L, Wang H, Li G, Ouyang W, Lin L. Crowd counting using deep recurrent spatial-aware network, arXiv preprint 
arXiv:1807.00601. 1807.00601; 2018. p. 1–7.
120.	 Xiang J, Liu N. Crowd density estimation method using deep learning for passenger flow detection system in exhibition 
center. Sci Progr. 2022; 2022(1): 1990951. https://doi.org/10.1155/2022/1990951.
121.	 Hu Q, Li G. Crowd counting study based on low light image enhancement. In: 2023 4th international conference on 
computer engineering and application (ICCEA). p. 792–6. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​C​C​E​A​5​8​4​3​3​.​2​0​2​3​.​1​0​1​3​5​5​0​1
122.	 Kong W, Yu Z, Li H, Tong L, Zhao F, Li Y. CrowdAlign: shared-weight dual-level alignment fusion for RGB-T crowd counting. 
Image Vis Comput. 2024;148:105152. http//.
123.	 Li B, Zhang Y, Xu H, Yin B. CCST: crowd counting with swin transformer. Visual Comput. 2023;39(7):2671–82. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​
/​1​0​.​1​0​0​7​/​s​0​0​3​7​1​-​0​2​2​-​0​2​4​8​5​-​3​.​
124.	 Shu W, Wan J, Tan KC, Kwong S, Chan AB. Crowd counting in the frequency domain. In: Proceedings of the IEEE/CVF 
conference on computer vision and pattern recognition (CVPR), New Orleans, Louisiana, USA; 2022. p. 19618–27. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​5​2​6​8​8​.​2​0​2​2​.​0​1​9​0​9​
125.	 Shi Z, Yang C, Xu, Chen Q. Revisiting perspective information for efficient crowd counting. In: Proceedings of the IEEE/CVF 
conference on computer vision and pattern recognition (CVPR), Long Beach, California, USA; 2019. p. 7279–88. ​h​t​t​p​s​:​/​/​d​o​i​.​
o​r​g​/​1​0​.​1​1​0​9​/​C​V​P​R​.​2​0​1​9​.​0​0​7​4​5​
126.	 Khan MA, Menouar H, Hamila R. Crowd counting in harsh weather using image denoising with Pix2Pix GANs, arXiv pre­
print arXiv:2310.07245. 2310.07245; 2023. p.1–6.
127.	 Luo A, Yang F, Li X, Nie D, Jiao Z, Zhou S, Cheng H. Hybrid graph neural networks for crowd counting. In: Proceedings of 
the AAAI conference on artificial intelligence, New York, New York, United States. 2020; 34(07) 11693–700. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​6​0​9​/​a​a​a​i​.​v​3​4​i​0​7​.​6​8​3​9​
128.	 Zhang Y, Zhao H, Duan Z, Huang L, Deng J, Zhang Q. Congested crowd counting via adaptive multi-scale context learn­
ing. Sensors. 2021;21(11):1–18. https://doi.org/10.3390/s21113777. http//.
129.	 Liu W, Durasov N, Fua P. Leveraging self-supervision for cross-domain crowd counting, arXiv preprint arXiv:2103.16291. 
2103.16291; 2021. p. 1–12.
130.	 Li Z, Lu S, Dong Y, Guo J. MSFFA: a multi-scale feature fusion and attention mechanism network for crowd counting. Visual 
Comput. 2023;39(3):1045–56. https://doi.org/10.1007/s00371-022-02582-1.
131.	 Chen L, Gao X. Fuss-free network: a simplified and efficient neural network for crowd counting, arXiv preprint 
arXiv:2404.07847. 2404.07847; 2024. p. 1–29.
132.	 Pan T, Zheng Z, Jia X. Boosting adverse weather crowd counting via multi-queue contrastive learning, arXiv preprint 
arXiv:2408.05956. 2408.05956; 2024. p.1–8.
Publisher’s note
Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
