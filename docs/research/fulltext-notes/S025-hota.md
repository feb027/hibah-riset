# Full-Text Note — S025 HOTA: A Higher Order Metric for Evaluating Multi-object Tracking

## Source identity

- Source ID: S025
- Title: HOTA: A Higher Order Metric for Evaluating Multi-object Tracking
- Authors: Jonathon Luiten, Aljoša Ošep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixé, Bastian Leibe
- URL/DOI/arXiv: https://link.springer.com/article/10.1007/s11263-020-01375-2 ; DOI: 10.1007/s11263-020-01375-2
- Access date: 25 May 2026 WIB
- Venue/source type: International Journal of Computer Vision, Volume 129, pp. 548–578; published online 8 October 2020, issue year 2021; Springer open-access journal article
- Indexed/peer-reviewed status: Peer-reviewed Springer IJCV article; source-ledger `B-support` canonical MOT metric source.

## Why this source matters

HOTA is the key metric source for evaluating MOT in the proposed people-counting pipeline. The paper explains why tracking evaluation should not rely only on detection-heavy metrics such as MOTA or identity-heavy metrics such as IDF1. It supports the proposal's plan to evaluate tracker quality with a balanced detection-association metric before interpreting counting results.

## Problem addressed

- MOT evaluation is difficult because a tracker must detect objects, localize them, and preserve identities/associations over time.
- Previous metrics can overemphasize one aspect: the authors argue that MOTA is weak for association quality, while IDF1 and Track-mAP can behave non-intuitively with respect to detection quality.
- The paper proposes HOTA to provide a unified metric that balances detection, association, and localization, while still decomposing into interpretable sub-metrics.

## Method summary

- HOTA stands for **Higher Order Tracking Accuracy**.
- Matching is performed at the detection level: true positives, false positives, and false negatives are defined using a localization similarity threshold `alpha` with one-to-one matching per frame.
- For each true positive match, HOTA measures association alignment using:
  - TPA: true positive associations, detections with the same ground-truth ID and same predicted ID as the matched true positive.
  - FNA: false negative associations, detections from the same ground-truth trajectory assigned a different predicted ID or missed.
  - FPA: false positive associations, detections from the same predicted trajectory assigned to a different ground-truth ID or false positive.
- At a fixed localization threshold, HOTA is a "double Jaccard" formulation: a detection-level Jaccard score weighted by an association Jaccard score.
- The paper decomposes HOTA into:
  - DetA: detection accuracy.
  - AssA: association accuracy.
  - LocA: localization accuracy.
  - DetRe/DetPr: detection recall/precision.
  - AssRe/AssPr: association recall/precision.
- Key relation verified from the full text: `HOTA_alpha = sqrt(DetA_alpha * AssA_alpha)`.
- Final HOTA is obtained by averaging HOTA over localization thresholds from 0.05 to 0.95 in 0.05 increments.

## Dataset / evaluation protocol

- This is a metric paper, not a tracking method paper.
- The authors evaluate HOTA on the MOTChallenge MOT17 benchmark to compare HOTA with MOTA and IDF1 for real tracker submissions.
- They restrict one analysis to 37 published peer-reviewed trackers on MOT17.
- The paper also conducts a large-scale human visual assessment study:
  - MOT17 test-set sequences are split into 36 six-second clips.
  - The study evaluates 175 trackers across 108 combinations of sub-sequences and detector inputs.
  - 230 participants contributed 2075 tracker comparisons; 62 participants self-reported as MOT researchers and 122 as computer vision researchers.
- Track-mAP could not be compared on MOTChallenge because it requires tracker confidence scores that MOTChallenge submissions did not provide.

## Metrics reported

- Proposed metric: HOTA.
- HOTA sub-metrics: DetA, AssA, LocA, DetRe, DetPr, AssRe, AssPr.
- Compared metrics: MOTA, IDF1, Track-mAP, plus discussion of CLEAR MOT and other secondary tracking metrics.
- Human-study agreement values reported:
  - All users: HOTA agrees with human evaluators 61.6% of the time against MOTA and 72.0% against IDF1, excluding pairs marked equal.
  - MOT researchers: agreement with HOTA is 79.3% against MOTA and 85.9% against IDF1.
- Correlation analysis on MOT17 reported in the text:
  - MOTA correlates highly with DetA (`R^2=0.96`) and weakly with AssA (`R^2=0.46`).
  - IDF1 correlates highly with AssA (`R^2=0.97`) and weakly with DetA (`R^2=0.58`).
  - HOTA lies between these extremes, correlating with DetA (`R^2=0.67`) and AssA (`R^2=0.94`).

## Findings safe to cite

- HOTA is designed to balance detection and association accuracy and incorporate localization by averaging over thresholds.
- The paper states that HOTA can serve as a single ranking metric while decomposing into sub-metrics for error diagnosis.
- HOTA's decomposition is useful for identifying whether a tracker fails from missed/extra detections, association fragmentation/merging, or localization errors.
- In the authors' MOT17 analysis, MOTA behaves largely as a proxy for detection accuracy, while IDF1 depends more strongly on association accuracy.
- The human visual assessment study found HOTA aligned better with human judgments than MOTA or IDF1 in the tested comparisons.
- For the proposal, HOTA is a suitable tracking metric to pair with IDF1/MOTA and count-error/FPS metrics; it is not itself a counting metric.

## Limitations stated by authors

- The paper does not present a conventional limitations section.
- It explicitly notes that Track-mAP could not be compared on MOTChallenge because tracker confidence scores were unavailable.
- The human visual assessment is described as not a perfect proxy for usefulness in every tracking application; it is a study of alignment with human ranking under the chosen visualization and task design.
- The authors emphasize that different applications may prioritize different error types; HOTA's sub-metrics should be used to analyze those requirements rather than relying blindly on the single score.

## Limitations inferred for this project

- HOTA evaluates tracking, not people-counting correctness; the project still needs counting error/MAE or event-level count metrics for line/zone counting.
- HOTA requires ground-truth tracks/IDs and localization annotations; it cannot be computed for unlabeled deployment videos without annotation.
- A high HOTA score does not automatically mean low double-counting if the counting logic is poorly designed.
- HOTA should be reported together with IDF1/MOTA, count error, and FPS/latency/resource usage to match the proposal's real-time people-counting goal.

## Exact claims allowed in draft

- "HOTA is a MOT evaluation metric that explicitly balances detection and association by using the geometric mean of DetA and AssA at each localization threshold."
- "The final HOTA score averages over localization thresholds from 0.05 to 0.95, so localization quality is incorporated into the metric."
- "HOTA decomposes into DetA, AssA, LocA, DetRe/DetPr, and AssRe/AssPr, enabling diagnosis of detector versus association errors."
- "For tracking-based people counting, HOTA can evaluate whether a tracker preserves detections and identities well enough to support downstream counting, but it must be complemented with counting-error and runtime metrics."

## Claims NOT allowed

- Do not claim HOTA measures people-counting accuracy or line-crossing accuracy.
- Do not claim HOTA replaces all other metrics; the paper itself motivates sub-metric analysis and application-specific priorities.
- Do not claim HOTA is a tracking algorithm.
- Do not use HOTA as proof that a detector/tracker pipeline is real-time.
- Do not cite HOTA percentages as performance of the proposed system; they are metric-evaluation/user-study results from the paper.

## Mapped sections

- `docs/outlines/pekerjaan-terkait-outline.md` Section 6: Dataset, metrik evaluasi, dan constraint real-time/edge.
- Section 5: Counting logic berbasis RoI/line/zone/ID memory, as support that stable ID association must be evaluated before counting.
- Section 7: Sintesis gap dan posisi penelitian, as support for multi-metric evaluation: HOTA, IDF1/MOTA, count error, and FPS/latency.

## Notes for citation auditor

- Bibliography key in `references/references.bib`: `S025`.
- Ledger status: `B-support`, canonical MOT metric, Springer IJCV peer-reviewed.
- Full text accessed from official Springer open-access article page on 25 May 2026 WIB.
- Use DOI `10.1007/s11263-020-01375-2`; issue year in citation may appear as 2021, with online publication in 2020.
