"""End-to-end smoke-test pipeline.

Input: a video file path (or path to a directory of frames — TODO).
Output:
- Annotated video with bounding boxes + person count overlay.
- Per-frame CSV: frame_index, person_count, latency_ms.
- Summary JSON: detector name, source_id, fps_avg, p95_latency, total_frames.

This is Tier 1 — inference only, no training, no tracking.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from src.detector import DETECTOR_CATALOGUE, PeopleDetector
from src.utils.video_io import (
    draw_boxes,
    iter_frames,
    probe_video,
    put_text,
    write_video,
)

logger = logging.getLogger(__name__)


@dataclass
class SmokeTestSummary:
    detector: str
    source_id: str | None
    video_path: str
    fps_video: float
    fps_processed: float
    fps_avg: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_mean_ms: float
    total_frames: int
    total_person_detections: int
    mean_persons_per_frame: float
    max_persons_in_frame: int
    max_persons_frame_index: int


def run_smoke_test(
    video_path: str | Path,
    output_dir: str | Path,
    detector_name: str = "yolov10s",
    confidence_threshold: float = 0.25,
    iou_threshold: float = 0.45,
    max_frames: int | None = None,
    device: str | None = None,
) -> SmokeTestSummary:
    """Run detector over a video and write annotated video + CSV + summary JSON."""
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    meta = probe_video(video_path)
    logger.info(
        "Video: %s | %dx%d @ %.2f fps | frames=%s",
        video_path,
        meta.width,
        meta.height,
        meta.fps,
        meta.total_frames,
    )

    detector = PeopleDetector(
        detector_name=detector_name,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold,
        device=device,
        person_only=True,
    )

    annotated_path = output_dir / f"annotated_{detector_name}.mp4"
    csv_path = output_dir / f"per_frame_{detector_name}.csv"

    # Buffers for summary + per-frame CSV streaming
    latencies: list[float] = []
    counts: list[int] = []
    max_count = 0
    max_count_frame = 0
    total_person_detections = 0

    # Annotate frames in a streaming pass
    def annotated_stream():
        nonlocal max_count, max_count_frame, total_person_detections
        with csv_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["frame_index", "person_count", "latency_ms", "fps_instant"])
            for idx, frame in iter_frames(video_path):
                t0 = time.perf_counter()
                fd = detector.detect_frame(frame, frame_index=idx)
                wall = (time.perf_counter() - t0) * 1000.0
                boxes = [d.bbox_xyxy for d in fd.detections]
                labels = [
                    f"person {d.confidence:.2f}" for d in fd.detections
                ]
                annotated = draw_boxes(frame, boxes, labels=labels)
                annotated = put_text(
                    annotated,
                    f"{detector_name} | frame {idx} | persons: {fd.person_count}",
                )
                writer.writerow([idx, fd.person_count, f"{fd.latency_ms:.3f}", f"{1000.0 / wall:.2f}" if wall > 0 else "0"])
                latencies.append(fd.latency_ms)
                counts.append(fd.person_count)
                total_person_detections += fd.person_count
                if fd.person_count > max_count:
                    max_count = fd.person_count
                    max_count_frame = idx
                if max_frames is not None and idx + 1 >= max_frames:
                    break
                yield annotated

    fps_write = meta.fps if meta.fps > 0 else 25.0
    write_video(annotated_path, annotated_stream(), fps=fps_write, width=meta.width, height=meta.height)
    processed_frames = len(counts)

    if processed_frames == 0:
        raise RuntimeError("No frames processed — video unreadable or empty.")

    summary = SmokeTestSummary(
        detector=detector_name,
        source_id=DETECTOR_CATALOGUE[detector_name]["source_id"],
        video_path=str(video_path),
        fps_video=meta.fps,
        fps_processed=fps_write,
        fps_avg=processed_frames / (sum(latencies) / 1000.0) if sum(latencies) > 0 else 0.0,
        latency_mean_ms=float(np.mean(latencies)),
        latency_p50_ms=float(np.percentile(latencies, 50)),
        latency_p95_ms=float(np.percentile(latencies, 95)),
        total_frames=processed_frames,
        total_person_detections=total_person_detections,
        mean_persons_per_frame=float(np.mean(counts)),
        max_persons_in_frame=max_count,
        max_persons_frame_index=max_count_frame,
    )

    summary_path = output_dir / f"summary_{detector_name}.json"
    summary_path.write_text(json.dumps(asdict(summary), indent=2))

    logger.info("Done. Summary written to %s", summary_path)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Hibah riset Tier-1 smoke test: run a people detector over a video."
    )
    p.add_argument("--video", required=True, type=Path, help="Path to input video")
    p.add_argument("--out", required=True, type=Path, help="Output directory")
    p.add_argument(
        "--detector",
        default="yolov10s",
        choices=sorted(DETECTOR_CATALOGUE),
        help="Detector alias (default: yolov10s — anchor from S003)",
    )
    p.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    p.add_argument("--iou", type=float, default=0.45, help="IoU threshold")
    p.add_argument("--max-frames", type=int, default=None, help="Limit frames (smoke)")
    p.add_argument("--device", default=None, help="cuda:0 / cpu / None (auto)")
    p.add_argument("--log-level", default="INFO")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
    )
    summary = run_smoke_test(
        video_path=args.video,
        output_dir=args.out,
        detector_name=args.detector,
        confidence_threshold=args.conf,
        iou_threshold=args.iou,
        max_frames=args.max_frames,
        device=args.device,
    )
    # Print a tight summary — no extras.
    print(json.dumps(asdict(summary), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
