---
source_id: S019
title: Handling Heavy Occlusion in Dense Crowd Tracking by Focusing on the Heads
source_url: https://dl.acm.org/doi/abs/10.1007/978-981-99-8388-9_7
source_file: unavailable_pdf_firecrawl_query
source_kind: firecrawl_query_extract
extraction_note: Publisher PDF/full text was not directly downloadable by script; saved Firecrawl query extraction and public abstract metadata.
---

# Extracted source notes

## Bibliographic metadata

- Title: Handling Heavy Occlusion in Dense Crowd Tracking by Focusing on the Heads
- Authors: Yu Zhang; Huaming Chen; Zhongzheng Lai; Zao Zhang; Dong Yuan
- Venue: AI 2023: Advances in Artificial Intelligence, Springer LNCS / ACM DL page
- DOI/URL: https://doi.org/10.1007/978-981-99-8388-9_7

## Public abstract / extracted details

The paper addresses dense crowd multi-object tracking where pedestrians are heavily occluded. The abstract notes that MOT20 has much denser pedestrian scenes than MOT17, making full-body detection/tracking unreliable. The proposed approach uses a joint head-and-body detector in an anchor-free style to improve recall and precision for small and medium pedestrians. Instead of assuming a fixed statistical head-body ratio, the model learns that relationship dynamically. Experiments are reported on MOT20, CrowdHuman, and HT21, with improved recall/precision and state-of-the-art claims on challenging dense-crowd datasets.

## Query extraction fields

- Problem: tracking all pedestrians in dense crowd scenes is difficult because heavy occlusion hides bodies and causes detection/tracking failure.
- Contribution: joint head-body anchor-free detector; dynamic learning of head-body ratio; improved detection of small/medium pedestrians.
- Method/solution: focus on head cues because heads remain more visible under dense occlusion; combine head and body information for robust pedestrian detection/tracking.
- Main results: improved recall and precision on small/medium pedestrians; evaluated on MOT20, CrowdHuman, and HT21.
- Limitations: full text not directly accessible in this extraction; abstract does not detail runtime/edge deployment.
- Relevance: supports the argument that dense people-counting systems cannot rely only on full-body detection; head/partial-body cues can help when occlusion is severe.
