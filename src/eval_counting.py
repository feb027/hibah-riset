"""Counting-error metrics: MAE, MAPE, RMSE.

For datasets that provide a per-frame ground-truth count (e.g. Mall,
ShanghaiTech, JHU-CROWD++). Used by S3 quant (not S1), but kept in the
library early so notebooks can compose it freely.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class CountingResult:
    num_frames: int
    mae: float
    mape: float
    rmse: float
    mean_gt: float
    mean_pred: float
    total_gt: int
    total_pred: int
    note: str = ""


def evaluate_counting(
    gt_counts: list[int],
    pred_counts: list[int],
    *,
    epsilon: float = 1e-6,
) -> CountingResult:
    """MAE, MAPE, RMSE between ground-truth and predicted per-frame counts."""
    if len(gt_counts) != len(pred_counts):
        raise ValueError(
            f"Length mismatch: gt={len(gt_counts)} pred={len(pred_counts)}"
        )
    if not gt_counts:
        raise ValueError("Empty input lists")

    gt = np.asarray(gt_counts, dtype=np.float64)
    pr = np.asarray(pred_counts, dtype=np.float64)
    abs_err = np.abs(gt - pr)
    # MAPE: avoid div-by-zero via epsilon; mask frames with gt=0 because
    # percentage error is undefined there.
    safe_gt = np.where(gt == 0, np.nan, gt)
    pct_err = np.abs((gt - pr) / safe_gt)

    return CountingResult(
        num_frames=len(gt),
        mae=float(abs_err.mean()),
        mape=float(np.nanmean(pct_err) * 100.0),
        rmse=float(np.sqrt(np.mean(abs_err ** 2))),
        mean_gt=float(gt.mean()),
        mean_pred=float(pr.mean()),
        total_gt=int(gt.sum()),
        total_pred=int(pr.sum()),
    )


def write_counting_result_json(result: CountingResult, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result.__dict__, indent=2))
    return p
