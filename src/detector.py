"""Detector wrapper for the people-counting pipeline (Tier 1 smoke test).

Wraps Ultralytics YOLO with a minimal interface so the rest of the pipeline
does not depend on Ultralytics internals. Supports the detectors that are
explicitly referenced in our source ledger:

- YOLOv10n/s  (S003 - Wang et al., NeurIPS 2024)
- RT-DETR-l   (S004 - Zhao et al., CVPR 2024)
- YOLOv11n    (Ultralytics 2024 baseline, no S-code yet)
- YOLO26n     (S001/S002 - preprint + vendor docs; caution status)

This module does NOT train anything. Inference only.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)


# Canonical detector catalogue. Map short alias -> ultralytics model id.
# Anchored to source-ledger.md (see AGENTS.md / references.bib).
DETECTOR_CATALOGUE: dict[str, dict] = {
    "yolov10n": {
        "model": "yolov10n.pt",
        "source_id": "S003",
        "description": "YOLOv10 nano (NeurIPS 2024). Academic anchor for NMS-free YOLO.",
        "size": "nano",
    },
    "yolov10s": {
        "model": "yolov10s.pt",
        "source_id": "S003",
        "description": "YOLOv10 small (NeurIPS 2024). Default for Tier 1 smoke test.",
        "size": "small",
    },
    "yolov11n": {
        "model": "yolo11n.pt",
        "source_id": None,
        "description": "YOLOv11 nano (Ultralytics 2024). Generic baseline, not yet in source ledger.",
        "size": "nano",
    },
    "yolo26n": {
        "model": "yolo26n.pt",
        "source_id": "S001/S002",
        "description": "YOLO26 nano. S001 is preprint, S002 is vendor doc. Caution status in source ledger.",
        "size": "nano",
    },
    "rtdetr-l": {
        "model": "rtdetr-l.pt",
        "source_id": "S004",
        "description": "RT-DETR large (CVPR 2024). Transformer end-to-end detector baseline.",
        "size": "large",
    },
}


@dataclass
class Detection:
    """One detection in one frame."""

    bbox_xyxy: tuple[float, float, float, float]
    confidence: float
    class_id: int
    class_name: str

    def is_person(self) -> bool:
        # COCO class id 0 = person.
        return self.class_id == 0


@dataclass
class FrameDetections:
    """All detections for one frame, plus latency in ms."""

    frame_index: int
    detections: list[Detection] = field(default_factory=list)
    latency_ms: float = 0.0

    @property
    def person_count(self) -> int:
        return sum(1 for d in self.detections if d.is_person())

    @property
    def person_boxes(self) -> list[tuple[float, float, float, float]]:
        return [d.bbox_xyxy for d in self.detections if d.is_person()]


class PeopleDetector:
    """Thin wrapper around ultralytics.YOLO for people-only inference.

    Filters detections to COCO class 0 (person) by default.
    """

    def __init__(
        self,
        detector_name: str = "yolov10s",
        confidence_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        device: str | None = None,
        person_only: bool = True,
    ) -> None:
        if detector_name not in DETECTOR_CATALOGUE:
            raise ValueError(
                f"Unknown detector '{detector_name}'. "
                f"Available: {sorted(DETECTOR_CATALOGUE)}"
            )

        try:
            from ultralytics import YOLO  # local import keeps CPU-only fallback working
        except ImportError as e:
            raise ImportError(
                "ultralytics not installed. Run: pip install ultralytics>=8.3.0"
            ) from e

        entry = DETECTOR_CATALOGUE[detector_name]
        self.detector_name = detector_name
        self.source_id = entry["source_id"]
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.person_only = person_only

        logger.info(
            "Loading detector '%s' (%s) — source_id=%s",
            detector_name,
            entry["model"],
            entry["source_id"],
        )
        self.model = YOLO(entry["model"])
        if device is not None:
            self.model.to(device)

    def detect_frame(self, frame, frame_index: int = 0) -> FrameDetections:
        """Run detection on a single BGR frame (numpy array).

        Returns FrameDetections with latency_ms measured locally.
        """
        import time

        start = time.perf_counter()
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            verbose=False,
        )
        latency_ms = (time.perf_counter() - start) * 1000.0

        detections: list[Detection] = []
        if not results:
            return FrameDetections(frame_index=frame_index, latency_ms=latency_ms)

        r = results[0]
        names = r.names
        boxes = r.boxes
        if boxes is None:
            return FrameDetections(frame_index=frame_index, latency_ms=latency_ms)

        for box in boxes:
            cls_id = int(box.cls.item())
            if self.person_only and cls_id != 0:
                continue
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = (float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3]))
            conf = float(box.conf.item())
            detections.append(
                Detection(
                    bbox_xyxy=(x1, y1, x2, y2),
                    confidence=conf,
                    class_id=cls_id,
                    class_name=names.get(cls_id, str(cls_id)),
                )
            )

        return FrameDetections(
            frame_index=frame_index,
            detections=detections,
            latency_ms=latency_ms,
        )

    def detect_video(
        self, video_path: str | Path, max_frames: int | None = None
    ) -> Iterable[FrameDetections]:
        """Stream detections over a video file. Lazy generator."""
        cap = self._open_capture(video_path)
        idx = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                yield self.detect_frame(frame, frame_index=idx)
                idx += 1
                if max_frames is not None and idx >= max_frames:
                    break
        finally:
            cap.release()

    @staticmethod
    def _open_capture(video_path: str | Path):
        import cv2

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")
        return cap
