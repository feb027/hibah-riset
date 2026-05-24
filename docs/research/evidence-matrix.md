# Evidence Matrix — Mapping Sources to Claims

| Claim/gap | Supporting sources | Counterpoints/limitations | Draft target |
|---|---|---|---|
| Real-time people counting needs robust detection + tracking under dense occlusion, not just frame-level counting. | TBD | Need avoid overclaiming without deployment evidence. | Pendahuluan + Related Work |
| NMS-free/end-to-end detectors reduce post-processing latency and may help edge deployment. | S001, S002 after validation | Vendor/blog claims must not replace peer-reviewed evidence; YOLO26 may be preprint. | Detector subsection |
| Classical SORT/Kalman assumptions can struggle with non-linear/crowded movement and occlusion. | S008 + modern MOT sources | OC-SORT partially addresses this; present as baseline/fallback not strawman. | Tracker subsection |
| Diffusion/transformer/modern trackers address non-linear trajectory/occlusion but may be computationally heavier. | S007, S004, S005 after validation | Need exact runtime/FPS evidence. | Tracker + gap synthesis |
| Counting logic needs RoI/trajectory/state memory to prevent double counting after ID switches. | Need sources | Must cite people-counting/ROI studies, not infer only from tracker papers. | Counting logic subsection |
