# Full-Text Note — S028 Crowd counting at the edge using weighted knowledge distillation

## Source identity

- Source ID: S028
- Title: Crowd counting at the edge using weighted knowledge distillation
- Authors: Muhammad Asif Khan; Hamid Menouar; Ridha Hamila; Adnan Abu-Dayya
- URL/DOI/arXiv: https://doi.org/10.1038/s41598-025-90750-5 ; official Nature page: https://www.nature.com/articles/s41598-025-90750-5
- Access date: 2026-05-25 WIB
- Venue/source type: *Scientific Reports* 2025, volume 15, article 11932; Springer Nature journal article; open access.
- Indexed/peer-reviewed status: Peer-reviewed journal article per source ledger; full text read from official Nature/Springer page.
- Citation key in `references/references.bib`: `S028`.

## Why this source matters

This paper is a strong recent source for lightweight/edge crowd counting and model compression through knowledge distillation. It is relevant to the proposal’s edge-deployment discussion, but it belongs primarily to **density-map crowd counting**, not detection-tracking-counting. It should therefore be used to discuss accuracy/efficiency trade-offs and edge constraints, not line/zone entry-exit counting or ID persistence.

## Problem addressed

The paper addresses the accuracy drop of shallow/lightweight crowd-counting models on complex scenes. The motivation is that drones and other edge devices need real-time or near-real-time crowd estimates under limited compute, storage, and power, while many crowd-counting models optimize accuracy without considering model size and computational complexity.

## Method summary

- Approach type: **density-map crowd counting / crowd density estimation**, not detection-tracking-counting.
- Core method: weighted knowledge distillation (KD) transfers information from a deep/cumbersome teacher model to lightweight/shallow student models.
- Teacher models: CSRNet and CSRNet_lite.
- Student models: MCNN, DroneNet, and LCDnet.
- Density-map training: point/head annotations are converted to density maps using Gaussian kernels; model output is a density map, and total count is obtained by summing density-map values.
- Loss: the paper formulates a density-map regression distillation loss combining ground-truth density-map error with a teacher-student loss term weighted by normalized teacher loss; temperature/weighting controls how strongly the student follows the teacher versus ground truth.
- Implementation: PyTorch; training performed on a Lambda machine with Quadro RTX-8000 GPUs; learning rate 0.001.

## Dataset / evaluation protocol

- The text says the proposed method is evaluated over six benchmark datasets/scenarios. In practice, the main human crowd-counting table covers Mall, ShanghaiTech Part A, ShanghaiTech Part B, and DroneRGBT; ablation/domain adaptation adds CARPK and Aerial Sheeps.
- Mall: 2000 frames, 640 × 480, about 60,000 annotated pedestrians; single-scene CCTV deployment.
- ShanghaiTech: 1198 images and 330,165 annotations; Part A 482 images (300 train/182 test) and Part B 716 images (400 train/316 test).
- DroneRGBT: 3600 RGB/thermal image pairs from drone viewpoints for people counting, including low-light contexts.
- CARPK: 90,000 vehicles from drone images; used for vehicle-counting cross-domain adaptation.
- Aerial Sheeps: 1727 images, split into 1203 train, 350 validation, and 174 test; used for animal-counting domain adaptation.
- Important design choice: the authors omitted datasets with too-congested scenes because the student models are extremely shallow and are aimed at efficient edge estimates rather than maximum-accuracy counting.

## Metrics reported

- Main counting metric: MAE between predicted count and actual count obtained from density maps.
- Additional ablation metrics: SSIM and PSNR for density-map quality in the domain-adaptation experiments.
- Complexity metrics: parameters (M), model size (MB), GMACs, and inference time on server, Jetson Xavier, and Jetson Nano.
- Verified Table 1 examples:
  - Mall, MCNN, 40% labels: MAE 9.8 standard vs 8.0 with KD (+18.3% reduction); 100% labels: 3.6 vs 3.3 (+8.0%).
  - ShanghaiTech Part A, DroneNet, 100% labels: 98.5 standard vs 83.9 with KD (+14.8%).
  - ShanghaiTech Part B, LCDnet, 100% labels: 31.6 standard vs 26.3 with KD (−16.8% as printed in table; direction is MAE reduction).
  - DroneRGBT, DroneNet, 100% labels: 11.3 standard vs 9.7 with KD (+14.5%).
- Verified Table 2 complexity examples:
  - CSRNet teacher: 16.26M parameters, 65.05 MB, 135.4 GMACs, inference times 0.19 / 1.01 / 1.88 for server / Jetson Xavier / Jetson Nano.
  - MCNN student: 0.13M parameters, 0.53 MB, 8.82 GMACs, 0.05 / 0.10 / 0.21.
  - DroneNet student: 0.15M parameters, 0.60 MB, 8.92 GMACs, 0.056 / 0.15 / 0.28.
  - LCDnet student: 0.05M parameters, 0.21 MB, 4.85 GMACs, 0.006 / 0.05 / 0.10.

## Findings safe to cite

- S028 demonstrates that knowledge distillation can improve lightweight density-map crowd-counting models across several datasets while keeping the deployed student models very small.
- The authors report that KD typically gives the largest relative gains when labeled data are limited (e.g., 40%) and smaller gains when 100% labeled data are available.
- The paper supports the claim that edge crowd counting must consider not only count accuracy but also model size, computational complexity, and inference time on devices such as Jetson Nano/Xavier.
- LCDnet is extremely lightweight in the authors’ table: 0.05M parameters and 0.21 MB, with lower Jetson Nano inference time than MCNN/DroneNet, though with higher MAE in some scenarios.
- The method is density-map based: it predicts density maps and sums them for total counts; it does not maintain IDs, directions, trajectories, or line-crossing events.

## Limitations stated by authors

- Lightweight models suffer accuracy degradation in complex scenes due to limited generalization capacity.
- The authors intentionally omit too-congested datasets because the selected student models are shallow and unlikely to achieve sufficient accuracy there.
- The goal is effective edge crowd estimates rather than the most accurate possible count.
- KD performance depends on teacher selection; ablation with CSRNet_lite indicates teacher choice matters.
- Future work is planned for federated learning and server-less FL with KD across edge devices, so privacy-preserving distributed learning is not yet implemented in this paper.

## Limitations inferred for this project

- S028 is not a detection/tracking/ID-based people-counting paper; it cannot support claims about ROI line crossing, ID memory, double-count prevention, or entry/exit direction.
- Results are density-map count-error results on crowd-counting datasets; they are not MOT metrics and not detector AP metrics.
- Training uses a powerful RTX-8000 machine; the edge aspect is mainly about deploying/evaluating compact student models, not training on the edge device.
- The paper’s omission of very congested datasets limits claims about extreme crowd robustness.
- For the proposal, S028 should be used as edge/lightweight-counting evidence and a contrast case against trajectory-based people counting.

## Exact claims allowed in draft

- “Khan et al. (2025) applied weighted knowledge distillation to train compact density-map crowd-counting models for edge deployment.”
- “Their method uses teacher-student distillation for crowd density estimation; point annotations are converted to density maps, and total count is obtained from the density map.”
- “The paper reports MAE reductions for MCNN, DroneNet, and LCDnet across Mall, ShanghaiTech A/B, and DroneRGBT, while also reporting model size, GMACs, and inference time on server, Jetson Xavier, and Jetson Nano.”
- “S028 is evidence for edge-efficient density-map crowd counting, not for ID-based entry/exit counting.”

## Claims NOT allowed

- Do not claim S028 performs detection-tracking-counting, person re-identification, or line/zone crossing.
- Do not compare S028 MAE values directly with tracking/counting event accuracy from S010/S011.
- Do not claim the method works on extremely congested datasets; the authors explicitly omitted too-congested scenes for shallow student models.
- Do not claim training was performed on Jetson Nano; the experiments used a Quadro RTX-8000 machine for training and reported inference complexity on edge devices.
- Do not cite KD improvements as universal for all crowd-counting models; the experiments are bounded by the selected teacher/student models and datasets.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 1: density-map crowd counting as a distinct branch from detection-tracking-counting.
- Section 6: edge/deployment constraints, lightweight models, and metrics such as MAE and inference/resource cost.
- Section 7: gap synthesis, especially accuracy-vs-deployability and density-counting-vs-ID-counting distinctions.

## Notes for citation auditor

- Full text was accessible on official Nature page on 2026-05-25 WIB.
- `references/references.bib` contains `@article{S028,... DOI={10.1038/s41598-025-90750-5} ...}`.
- Treat as peer-reviewed Scientific Reports article. Use as a density-map/edge-counting contrast source; pair with S010/S011/MOT sources for trajectory-based counting claims.
