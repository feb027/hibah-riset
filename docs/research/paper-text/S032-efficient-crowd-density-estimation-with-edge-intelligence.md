---
source_id: S032
title: Efficient crowd density estimation with edge intelligence via structural reparameterization and knowledge transfer
source_url: https://doi.org/10.1016/j.asoc.2024.111366
source_file: unavailable_pdf_firecrawl_query
source_kind: firecrawl_query_extract
extraction_note: Elsevier PDF/full text was not directly downloadable by script; saved Firecrawl query extraction and article preview details.
---

# Extracted source notes

## Bibliographic metadata

- Title: Efficient crowd density estimation with edge intelligence via structural reparameterization and knowledge transfer
- Authors: Chenxi Lin; Xiaojian Hu
- Journal: Applied Soft Computing, Volume 154, Article 111366
- DOI/URL: https://doi.org/10.1016/j.asoc.2024.111366
- Year: 2024

## Query extraction fields

- Problem: real-time crowd density estimation is useful for public safety and crowd-flow management, but many crowd-counting models rely on heavy backbones or complex modules that are difficult to deploy on edge devices.
- Contribution: proposes Repmobilenet, a lightweight multi-branch convolutional network for edge crowd counting; introduces structural reparameterization to convert the training-time multi-branch model into a single-branch inference model; adds multi-layer knowledge distillation.
- Method/solution: uses depthwise separable convolution blocks for multi-scale spatial features, dilated convolutions for larger receptive field, structural reparameterization for lower inference latency, and teacher-student knowledge transfer to maintain accuracy.
- Main results: reports comparable counting performance to state-of-the-art methods while keeping model size and latency low; demonstrates deployment on Jetson Nano.
- Limitations: density-estimation paradigm, not trajectory/ID-based line or zone counting; full text not directly downloadable in this extraction.
- Relevance: supports the edge-deployment side of the proposed research, especially latency, model size, and trade-off between accuracy and real-time operation.
