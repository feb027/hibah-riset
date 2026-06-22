"""Video IO helpers — small, dependency-light wrappers around OpenCV."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2
import numpy as np


@dataclass
class VideoMeta:
    """Minimal video metadata."""

    path: Path
    fps: float
    width: int
    height: int
    total_frames: int | None  # None if backend cannot determine
    fourcc: str


def probe_video(path: str | Path) -> VideoMeta:
    """Read fps, resolution, frame count. Raises if video cannot be opened."""
    p = Path(path)
    cap = cv2.VideoCapture(str(p))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {p}")

    try:
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_frames = int(total) if total and total > 0 else None
        fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
        fourcc = "".join(chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4))
        return VideoMeta(
            path=p,
            fps=fps,
            width=width,
            height=height,
            total_frames=total_frames,
            fourcc=fourcc,
        )
    finally:
        cap.release()


def iter_frames(video_path: str | Path) -> Iterator[tuple[int, np.ndarray]]:
    """Yield (frame_index, BGR frame) until EOF."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")
    try:
        idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield idx, frame
            idx += 1
    finally:
        cap.release()


def write_video(
    output_path: str | Path,
    frames: Iterator[np.ndarray],
    fps: float,
    width: int,
    height: int,
    codec: str = "mp4v",
) -> Path:
    """Write an iterable of BGR frames to a video file. Returns output path."""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(str(p), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"Cannot open VideoWriter for: {p}")
    try:
        for frame in frames:
            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))
            writer.write(frame)
    finally:
        writer.release()
    return p


def draw_boxes(
    frame: np.ndarray,
    boxes: list[tuple[float, float, float, float]],
    labels: list[str] | None = None,
    color: tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
) -> np.ndarray:
    """Draw rectangles and optional labels on a BGR frame. Returns the frame."""
    out = frame.copy()
    for i, (x1, y1, x2, y2) in enumerate(boxes):
        cv2.rectangle(out, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        if labels and i < len(labels):
            cv2.putText(
                out,
                labels[i],
                (int(x1), max(int(y1) - 6, 12)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                thickness=1,
                lineType=cv2.LINE_AA,
            )
    return out


def put_text(
    frame: np.ndarray,
    text: str,
    org: tuple[int, int] = (16, 32),
    color: tuple[int, int, int] = (255, 255, 255),
    bg_color: tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    """Overlay a single text line with a contrasting background box."""
    out = frame.copy()
    (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    x, y = org
    cv2.rectangle(out, (x - 4, y - th - 6), (x + tw + 4, y + baseline), bg_color, -1)
    cv2.putText(
        out,
        text,
        (x, y - 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        thickness=2,
        lineType=cv2.LINE_AA,
    )
    return out
