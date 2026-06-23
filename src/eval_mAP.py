"""COCO-style mAP evaluation for people detection.

Computes mAP@0.5:0.95, AP50, AP75, AR via pycocotools. Designed to be
used by notebooks 03 (INRIA) and 04 (CrowdHuman).

Inputs:
- predictions: iterable of dicts with keys
    image_id: int
    category_id: int  (1 = person for COCO; configurable)
    bbox: [x, y, w, h] in absolute pixel coords
    score: float (confidence)
- ground_truth: iterable of dicts with keys
    image_id: int
    category_id: int
    bbox: [x, y, w, h]
    iscrowd: int (0 or 1)
    area: float (optional, computed if missing)

Both iterables can be lists, generators, or readers.

Anti-overclaim rules:
- mAP must come from a real labelled eval set, not smoke test.
- Number of images + total GT boxes must be reported alongside mAP.
- Confidence threshold sweep must be explicit (we compute at a fixed
  conf passed by caller; sweeping is the caller's job).
"""
from __future__ import annotations

import contextlib
import io
import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class MapResult:
    map_5095: float
    ap50: float
    ap75: float
    ap_per_category: dict[int, float]
    ar_per_category: dict[int, float]
    num_images: int
    num_gt_total: int
    num_pred_total: int
    num_pred_after_conf: int
    confidence_threshold: float
    note: str = ""


def _check_pycocotools():
    try:
        from pycocotools.coco import COCO  # type: ignore
        from pycocotools.cocoeval import COCOeval  # type: ignore
    except ImportError as e:
        raise ImportError(
            "pycocotools is required for S1 quant. Run: pip install pycocotools>=2.0.7"
        ) from e
    return COCO, COCOeval


def evaluate_map(
    predictions: list[dict],
    ground_truth: list[dict],
    *,
    confidence_threshold: float = 0.001,
    iou_type: str = "bbox",
    category_id: int | None = None,
) -> MapResult:
    """Run COCO-style mAP evaluation.

    `predictions` and `ground_truth` follow the COCO JSON result format
    (bbox = [x, y, w, h], absolute pixels).
    """
    COCO, COCOeval = _check_pycocotools()

    # Build ground-truth structure
    images = sorted({g["image_id"] for g in ground_truth})
    image_records = [{"id": int(img_id), "width": 0, "height": 0} for img_id in images]
    gt_records = []
    for g in ground_truth:
        bbox = list(g["bbox"])
        gt_records.append(
            {
                "id": len(gt_records) + 1,
                "image_id": int(g["image_id"]),
                "category_id": int(g.get("category_id", category_id or 1)),
                "bbox": bbox,
                "area": float(g.get("area", bbox[2] * bbox[3])),
                "iscrowd": int(g.get("iscrowd", 0)),
            }
        )

    # Filter predictions by confidence threshold
    pred_after = [p for p in predictions if float(p.get("score", 0.0)) >= confidence_threshold]
    pred_records = []
    for p in pred_after:
        bbox = list(p["bbox"])
        pred_records.append(
            {
                "id": len(pred_records) + 1,
                "image_id": int(p["image_id"]),
                "category_id": int(p.get("category_id", category_id or 1)),
                "bbox": bbox,
                "score": float(p["score"]),
                "area": float(bbox[2] * bbox[3]),
            }
        )

    if category_id is not None:
        gt_records = [g for g in gt_records if g["category_id"] == category_id]

    # Build coco_gt via in-memory file
    coco_gt_dict = {
        "images": image_records,
        "annotations": gt_records,
        "categories": [{"id": category_id or 1, "name": "person"}],
    }
    coco_gt = COCO()
    coco_gt.dataset = coco_gt_dict
    coco_gt.createIndex()

    if not pred_records:
        return MapResult(
            map_5095=0.0, ap50=0.0, ap75=0.0,
            ap_per_category={}, ar_per_category={},
            num_images=len(images),
            num_gt_total=len(gt_records),
            num_pred_total=len(predictions),
            num_pred_after_conf=0,
            confidence_threshold=confidence_threshold,
            note="No predictions above confidence threshold.",
        )

    # pycocotools can also load from a JSON file path; use io to keep it in-memory
    with contextlib.redirect_stdout(io.StringIO()):
        coco_dt = coco_gt.loadRes(pred_records)
        coco_eval = COCOeval(coco_gt, coco_dt, iouType=iou_type)
        if category_id is not None:
            coco_eval.params.catIds = [category_id]
        coco_eval.evaluate()
        coco_eval.accumulate()
        coco_eval.summarize()

    s = coco_eval.stats  # [AP, AP50, AP75, APs, APm, APl, AR1, AR10, AR100, ARs, ARm, ARl]
    return MapResult(
        map_5095=float(s[0]),
        ap50=float(s[1]),
        ap75=float(s[2]),
        ap_per_category={category_id or 1: float(s[0])},
        ar_per_category={category_id or 1: float(s[8])},
        num_images=len(images),
        num_gt_total=len(gt_records),
        num_pred_total=len(predictions),
        num_pred_after_conf=len(pred_records),
        confidence_threshold=confidence_threshold,
    )


def write_map_result_json(result: MapResult, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result.__dict__, indent=2))
    return p
