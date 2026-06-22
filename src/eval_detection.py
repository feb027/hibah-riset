"""Detection-quality metrics for Tier 1 smoke test.

Computes per-frame detector statistics. Does NOT compute mAP against
ground truth boxes (that needs a labelled eval set like CrowdHuman or
MOT17 — out of scope for Tier 1 smoke test).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.detector import FrameDetections


@dataclass
class DetectionStats:
    total_frames: int
    frames_with_detections: int
    total_person_detections: int
    mean_persons_per_frame: float
    median_persons_per_frame: float
    max_persons_in_frame: int
    min_persons_in_frame: int
    std_persons_per_frame: float


def aggregate(frame_detections: list[FrameDetections]) -> DetectionStats:
    if not frame_detections:
        raise ValueError("frame_detections is empty")
    counts = np.array([fd.person_count for fd in frame_detections], dtype=np.int64)
    return DetectionStats(
        total_frames=len(counts),
        frames_with_detections=int((counts > 0).sum()),
        total_person_detections=int(counts.sum()),
        mean_persons_per_frame=float(counts.mean()),
        median_persons_per_frame=float(np.median(counts)),
        max_persons_in_frame=int(counts.max()),
        min_persons_in_frame=int(counts.min()),
        std_persons_per_frame=float(counts.std()),
    )
