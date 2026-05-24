# Source ID Map

> Mapping from source ledger IDs to intended citation handles. Citation keys may change when `references.bib` is regenerated; keep this file as the human-readable control map.

| Source ID | Short handle | Preferred citation use | Status |
|---|---|---|---|
| S001 | YOLO26 arXiv | Context only for YOLO26 technical claims | caution |
| S002 | Ultralytics YOLO26 docs | Implementation/vendor context only | caution |
| S003 | YOLOv10 | Academic anchor for NMS-free/end-to-end YOLO | main |
| S004 | RT-DETR | Academic anchor for real-time end-to-end detector | main |
| S005 | D-FINE | Detector comparator | main |
| S006 | DEIM | Detector matching/training comparator | main |
| S007 | RF-DETR | 2026 detector comparator | main |
| S008 | Decade of YOLO review | YOLO background/review | support |
| S009 | Edge object recognition review | Edge constraints | support |
| S010 | Passenger flow YOLO Edge AI | Applied edge people counting | main |
| S011 | Vision-based people counting/tracking | Applied people counting/tracking | main |
| S018 | OcclusionTrack | Dense-scene occlusion MOT | main |
| S021 | DiffMOT | Core proposed MOT method | main |
| S024 | OC-SORT | Lightweight fallback/baseline | support |
| S025 | HOTA | MOT metric | support |
| S027 | Complex crowd counting review | Challenge/background | main |
| S028 | Edge crowd counting KD | Edge counting | main |

## Update policy

- Current `references.bib` uses source IDs as citation keys where metadata was fetched successfully, e.g. `S021`.
- Before Phase 3 final draft, every source cited in prose should have a matching row here and an entry in `references.bib`.
- If a nicer citation key is later introduced, keep the `S###` key as an alias or update this map in the same commit.
