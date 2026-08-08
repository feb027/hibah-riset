"""INRIA Person dataset loader (Dalal & Triggs, CVPR 2005).

Parses INRIA's Matlab annotation files (.mat) into the COCO-format
dict structure expected by `src.eval_mAP.evaluate_map()`.

INRIA layout (after `download_inria.py` extracts the tar):
    inria_person/
        Train/
            pos/      <- positive training images (.png)
            posGt/    <- one .mat per image, each contains `box_coord` (Nx4)
            neg/      <- negative training images (no annotations)
        Test/
            pos/      <- positive test images
            posGt/    <- one .mat per image
            neg/      <- negative test images (no annotations)

Each .mat has a single variable `box_coord` (also seen as `box_coordinates`
in some mirrors). It is an (N, 4) numpy array of [x, y, w, h] in image
pixel coordinates.

Reference: Dalal, Triggs. "Histograms of Oriented Gradients for Human
Detection." CVPR 2005.
"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Iterator

import numpy as np


def _mat_to_box_coord(mat_path: Path) -> np.ndarray:
    """Read a single INRIA .mat annotation file and return Nx4 array.

    The .mat is a Matlab v5 file. scipy.io.loadmat handles it, but the
    variable name can vary by mirror ('box_coord' / 'box_coordinates').
    """
    try:
        from scipy.io import loadmat  # type: ignore
    except ImportError as e:
        raise ImportError(
            "scipy is required to parse INRIA .mat files. "
            "Run: pip install scipy>=1.10"
        ) from e

    data = loadmat(str(mat_path))
    for key in ("box_coord", "box_coordinates", "boxes"):
        if key in data:
            arr = data[key]
            return np.atleast_2d(arr).astype(float)

    numeric = [
        (k, v) for k, v in data.items()
        if not k.startswith("__") and isinstance(v, np.ndarray) and v.ndim == 2 and v.shape[1] == 4
    ]
    if not numeric:
        raise ValueError(
            f"No 4-column box array found in {mat_path}. "
            f"Available keys: {[k for k in data if not k.startswith('__')]}"
        )
    return numeric[0][1].astype(float)


def iter_inria_positives(
    inria_root: Path,
    splits: tuple[str, ...] = ("Train", "Test"),
) -> Iterator[dict]:
    """Yield one record per positive INRIA image.

    Yields dict with keys: image_id, image_path, width, height, bboxes
    (Nx4 numpy array of [x, y, w, h] in absolute pixel coords).
    """
    if not inria_root.exists():
        raise FileNotFoundError(
            f"INRIA root not found: {inria_root}. "
            f"Run scripts/download_inria.py first."
        )

    image_id = 0
    for split in splits:
        pos_dir = inria_root / split / "pos"
        gt_dir = inria_root / split / "posGt"
        if not pos_dir.exists() or not gt_dir.exists():
            continue

        try:
            from PIL import Image  # type: ignore
        except ImportError as e:
            raise ImportError(
                "Pillow is required to read INRIA image dimensions. "
                "Run: pip install pillow>=10"
            ) from e

        for img_path in sorted(pos_dir.glob("*.png")):
            stem = img_path.stem
            mat_path = gt_dir / f"{stem}.mat"
            if not mat_path.exists():
                mat_path = gt_dir / f"{stem}.png.mat"
            if not mat_path.exists():
                # Mirror sometimes uses .mat key per image instead of filename
                candidates = list(gt_dir.glob(f"{stem}*.mat"))
                if not candidates:
                    continue
                mat_path = candidates[0]

            with Image.open(img_path) as im:
                width, height = im.size

            bboxes = _mat_to_box_coord(mat_path)
            yield {
                "image_id": image_id,
                "image_path": str(img_path),
                "split": split,
                "width": width,
                "height": height,
                "bboxes": bboxes,
            }
            image_id += 1


def inria_to_coco_records(
    inria_root: Path,
    splits: tuple[str, ...] = ("Train", "Test"),
    category_id: int = 1,
) -> list[dict]:
    """Convert INRIA annotations to flat COCO-format GT records.

    Returns list of dicts with keys: image_id, image_path, width, height,
    bbox (list of 4 floats), area, category_id, iscrowd. These can be
    fed directly into `src.eval_mAP.evaluate_map(ground_truth=...)`.
    """
    out: list[dict] = []
    for rec in iter_inria_positives(inria_root, splits=splits):
        img_id = rec["image_id"]
        bboxes = rec["bboxes"]
        if bboxes.size == 0:
            continue
        for box in bboxes:
            x, y, w, h = (float(v) for v in box)
            if w <= 0 or h <= 0:
                continue
            out.append(
                {
                    "image_id": img_id,
                    "image_path": rec["image_path"],
                    "image_width": rec["width"],
                    "image_height": rec["height"],
                    "bbox": [x, y, w, h],
                    "area": float(w * h),
                    "category_id": category_id,
                    "iscrowd": 0,
                }
            )
    return out


__all__ = ["iter_inria_positives", "inria_to_coco_records", "_mat_to_box_coord"]