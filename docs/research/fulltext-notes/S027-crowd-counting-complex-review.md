# Full-Text Note — S027 Deep learning for crowd counting in complex environments: challenges and novel trends

## Source identity

- Source ID: S027
- Title: Deep learning for crowd counting in complex environments: challenges and novel trends
- Authors: Heba F. Elsepae; Heba M. El-Hoseny; Ehab K. I. Hamad; El-Sayed M. El-Rabaie
- URL/DOI/arXiv: https://doi.org/10.1007/s10791-026-09928-8 ; official Springer page: https://link.springer.com/article/10.1007/s10791-026-09928-8
- Access date: 2026-05-25 WIB
- Venue/source type: *Discover Computing* 2026, volume 29, article 101; Springer Nature review article; open access.
- Indexed/peer-reviewed status: Peer-reviewed review article per source ledger; full text read from official SpringerLink HTML/PDF landing page.
- Citation key in `references/references.bib`: `S027`.

## Why this source matters

This is a recent review source for crowd-counting challenges, datasets, metrics, and deep-learning trends in complex environments. It is valuable for distinguishing **density-map crowd counting** from **detection/tracking/counting** approaches and for citing common challenges such as occlusion, scale variation, perspective distortion, lighting, weather, and domain shift. Because it is a review, it should support taxonomy/background claims rather than performance claims about the proposed system.

## Problem addressed

The review addresses how deep-learning methods count crowds under diverse and harsh conditions: dense crowds, occlusion, cluttered backgrounds, varying viewpoints, low light, uneven density, scale variation, perspective distortion, and adverse weather. It surveys methods, datasets, metrics, practical trends, and future directions rather than proposing one deployable people-counting system.

## Method summary

- Review type: narrative review with structured source selection.
- Search scope stated by authors: IEEE Xplore, Scopus, Web of Science, and Google Scholar; publications from 2010–2025; keywords including crowd counting, density estimation, computer vision, deep learning, and surveillance.
- Inclusion/exclusion stated by authors: peer-reviewed journal articles and reputable conference proceedings; preprints and non-scholarly sources excluded where possible; studies had to address crowd-counting methods, datasets, or applications.
- Taxonomy covered:
  - Detection-based counting: detects individuals with boxes/parts; useful in sparse/low-density crowds and gives localization, but struggles in dense occlusion.
  - Heatmap/density-map counting: estimates a density map and sums pixel values to estimate total count; stronger for dense scenes but generally does not preserve exact individual identities or trajectories.
  - Regression and density-estimation approaches.
  - Tracking-by-detection approaches: detect people frame-by-frame and associate detections over time using Kalman filter, DeepSORT, ByteTrack-like association, etc.; useful for trajectories and behavior analysis.
  - Deep-learning families: CNN, multi-column CNN, single-column CNN, attention, transformers, GAN/U-Net, fuzzy preprocessing, curriculum/adaptive learning, lightweight/edge models.

## Dataset / evaluation protocol

- No new primary experimental dataset for a proposed model; this is a review.
- Surveyed density-map/counting datasets include ShanghaiTech Part A/B, UCF-QNRF, UCF-CC-50, UCSD, Mall, JHU-CROWD++, and NWPU-Crowd.
- Surveyed detection/tracking datasets include CrowdHuman, CroHD, and Cchead.
- Useful dataset facts verified from the paper:
  - ShanghaiTech A: 482 images, 300 train/182 test, 241,677 annotated heads; ShanghaiTech B: 716 images, 400 train/316 test, 88,488 annotated heads.
  - UCF-QNRF: 1535 images, 1,525,272 annotated heads, 1201 train/334 test.
  - UCF-CC-50: 50 images, 63,296 annotated heads; standard 5-fold protocol.
  - UCSD: 2880 video frames and 7014 annotated people.
  - Mall: 2000 frames and about 60,000 annotated pedestrians.
  - JHU-CROWD++: 4372 images and over 1.51 million people.
  - NWPU-Crowd: 5109 images and over 2 million people.
  - CrowdHuman: about 15,000 images and over 330,000 labeled people with occlusion level.
  - CroHD: 9 video sequences, 11,463 frames, over 2.27 million annotations, 5230 unique tracks.
  - Cchead: 50,528 frames, over 2.36 million annotated heads, 2358 unique tracks.

## Metrics reported

- For density-map/counting evaluation: MAE, MSE, RMSE.
- For density-map quality: SSIM and PSNR.
- The review summarizes benchmark performance of prior methods across ShanghaiTech Part A/B, UCF-QNRF, and UCF-CC-50, but these numbers belong to the cited primary papers, not to a new S027 model.
- Examples explicitly discussed in the review: AP-FPN MAE 54.9 on ShanghaiTech A; HRANet MAE 52.8 and MSE 87.2 on ShanghaiTech A.
- For tracking-related datasets/approaches, the review discusses identity preservation/tracking qualitatively, but it is not a primary MOT benchmark paper.

## Findings safe to cite

- Crowd counting contains multiple methodological families: detection-based, regression-based, density-estimation/heatmap, and tracking-based approaches.
- Detection-based methods such as YOLO/Faster R-CNN localize individuals and work better in sparse/low-density scenes, but struggle in very dense crowds because of occlusion.
- Heatmap/density-map methods are better suited to large/dense scenes and estimate a total count through a density map, but they generally do not provide exact identities, trajectories, or line/zone crossing events.
- Tracking-by-detection associates detections across frames to maintain identities; this supports trajectory/behavior analysis and is distinct from density-map counting.
- Core challenges in complex environments include occlusion, cluttered backgrounds, varying viewpoints, low light, uneven density, scale variation, perspective distortion, and adverse weather.
- Emerging trends include attention mechanisms, transformer-based designs, hybrid/multi-scale architectures, self/semi-supervised learning, fuzzy preprocessing, curriculum/adaptive training, domain adaptation, and lightweight models for real-time/edge contexts.

## Limitations stated by authors

- The authors describe the paper as a narrative review rather than a systematic review, though they attempted transparent selection.
- Existing crowd-counting models still show reduced accuracy in extremely dense and highly occluded scenarios.
- Generalization across unseen datasets remains difficult because of domain gaps, lighting differences, and density variation.
- Transformer/attention-heavy methods often require substantial training time and computational resources, limiting real-time low-power deployment.
- Lightweight models improve efficiency but often sacrifice accuracy in complex or large-scale crowd scenes.
- Dataset annotation in dense crowds is difficult due to occlusion, incomplete annotations, and small/partially visible pedestrians.

## Limitations inferred for this project

- S027 is a review, so it cannot be used to claim new experimental performance for the proposal.
- Several dataset descriptions and trend summaries should be used as background; exact benchmark numbers should ideally be cross-checked in the original primary papers before being cited as performance evidence.
- The review’s “crowd counting” focus is often density-map/head-count estimation; the proposal’s target is trajectory/ROI people counting, so the distinction must remain explicit.
- Detection/tracking coverage is useful but not as detailed as specialist MOT papers; tracker-specific claims should be anchored to MOT sources.

## Exact claims allowed in draft

- “Elsepae et al. (2026) distinguish detection-based and heatmap/density-map crowd-counting approaches; detection methods localize individuals but struggle in dense occlusion, while heatmap methods estimate total crowd count without exact identities.”
- “The review identifies occlusion, clutter, viewpoint changes, low light, uneven density, scale variation, perspective distortion, and bad weather as key challenges for crowd counting in complex environments.”
- “The review lists MAE, MSE, and RMSE as common count-error metrics and SSIM/PSNR as density-map quality metrics.”
- “For trajectory-based people counting, S027 is useful for explaining why detection/tracking is a distinct branch from density-map estimation.”

## Claims NOT allowed

- Do not claim S027 proposes a new deployable algorithm with validated FPS or edge performance.
- Do not cite S027’s summarized benchmark numbers as if they are the authors’ own experiments.
- Do not claim density-map crowd counting provides persistent IDs, entry/exit direction, or double-count prevention.
- Do not use S027 alone for precise claims about a specific detector/tracker’s SOTA status; use primary detector/MOT papers for that.
- Do not claim the review proves the proposal’s pipeline is novel or superior.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 1: domain framing and distinction between density-map crowd counting vs detection-tracking-counting.
- Section 3: dense scenes, occlusion, and tracking-by-detection context.
- Section 6: datasets and metrics for crowd/counting evaluation.
- Section 7: gap synthesis, especially the density-counting vs ID/trajectory-counting gap.

## Notes for citation auditor

- Full text was accessible on official SpringerLink page on 2026-05-25 WIB.
- `references/references.bib` contains `@article{S027,... DOI={10.1007/s10791-026-09928-8} ...}`.
- Article type is “Review”; use for taxonomy/background and challenge framing. For exact model performance, verify original papers.
