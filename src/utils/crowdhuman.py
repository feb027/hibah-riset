"""Helpers for selecting CrowdHuman test images reproducibly.

The S1 latency experiments measure post-processing (NMS) cost, which scales
with the number of candidate boxes an image produces. Picking whichever file
the filesystem happens to return first both understates that cost and makes
the measurement unreproducible across machines. These helpers select images
by annotated crowd density instead, with a deterministic ordering.
"""
from __future__ import annotations

import json
from pathlib import Path

__all__ = ["person_box_counts", "densest_images"]


def person_box_counts(odgt_path: str | Path, exclude_ignore: bool = True) -> dict[str, int]:
    """Count annotated person boxes per image ID from a CrowdHuman .odgt file.

    `exclude_ignore` drops boxes flagged `extra.ignore == 1`, which the
    CrowdHuman protocol treats as ignore regions rather than positives.
    """
    counts: dict[str, int] = {}

    with open(odgt_path, "r") as f:
        for line in f:
            record = json.loads(line)
            n = 0
            for gt in record.get("gtboxes", []):
                if gt["tag"] != "person":
                    continue
                if exclude_ignore and gt.get("extra", {}).get("ignore", 0) == 1:
                    continue
                n += 1
            counts[record["ID"]] = n

    return counts


def densest_images(
    odgt_path: str | Path,
    images_dir: str | Path,
    n: int = 5,
    exclude_ignore: bool = True,
) -> list[tuple[Path, int]]:
    """Return the `n` most crowded images as (path, person_count) pairs.

    Images are searched recursively under `images_dir`. Ordering is by
    descending person count, with the image ID as tie-breaker so the same
    selection is produced on every machine and every run.
    """
    available = {p.stem: p for p in Path(images_dir).rglob("*.jpg")}
    if not available:
        raise FileNotFoundError(f"Tidak ada file .jpg di bawah {images_dir}")

    counts = person_box_counts(odgt_path, exclude_ignore=exclude_ignore)
    present = [(img_id, c) for img_id, c in counts.items() if img_id in available]
    if not present:
        raise FileNotFoundError(
            f"Tidak ada ID dari {odgt_path} yang cocok dengan gambar di {images_dir}. "
            "Periksa apakah .odgt dan folder gambar berasal dari split yang sama."
        )

    present.sort(key=lambda item: (-item[1], item[0]))
    return [(available[img_id], count) for img_id, count in present[:n]]
