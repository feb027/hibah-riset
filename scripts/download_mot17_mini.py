"""Download a small MOT17 subset for tracker smoke tests (Tier 2+).

MOT17 is hosted on motchallenge.net. The full train+test set is multi-GB.
For Tier 1 we only need a single short sequence to confirm the IO + format
work. This script downloads the smallest public sequence (MOT17-13) and
extracts just the FRCNN-style detections file to verify parsing.

NOTE: not run in Tier 1 by default. Invoked from a Colab cell when needed.
"""
from __future__ import annotations

import argparse
import logging
import urllib.request
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


# Public MOT17 mini mirror (smallest sequence). Replace if link rots.
MOT17_MIRRORS: list[tuple[str, int]] = [
    # (zip_url, approximate_size_mb)
    ("https://motchallenge.net/data/MOT17.zip", 1500),
]


def download_mot17_mini(
    output_dir: Path,
    max_size_mb: int = 300,
    mirror_index: int = 0,
) -> Path:
    """Download MOT17 zip and extract. Caller decides which sequence to use."""
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / "MOT17.zip"

    if mirror_index >= len(MOT17_MIRRORS):
        raise ValueError("mirror_index out of range")

    url, approx_mb = MOT17_MIRRORS[mirror_index]
    if approx_mb > max_size_mb:
        logger.warning(
            "Requested MOT17 mirror is %d MB > %d MB cap. Skipping download.",
            approx_mb,
            max_size_mb,
        )
        raise RuntimeError(
            f"MOT17 mirror too large ({approx_mb} MB). "
            "Tier 1 does not need MOT17 — use a short CC0 video instead."
        )

    if not zip_path.exists():
        logger.info("Downloading %s -> %s", url, zip_path)
        urllib.request.urlretrieve(url, zip_path)
    else:
        logger.info("Zip already present at %s", zip_path)

    extract_dir = output_dir / "MOT17"
    if not extract_dir.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)
    return extract_dir


def main() -> int:
    p = argparse.ArgumentParser(description="Download MOT17 mini (Tier 2 helper).")
    p.add_argument("--out", type=Path, default=Path("data/raw/mot17"))
    p.add_argument("--max-size-mb", type=int, default=300)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s | %(message)s")
    try:
        extract_dir = download_mot17_mini(args.out, max_size_mb=args.max_size_mb)
        print(f"MOT17 extracted at: {extract_dir}")
        return 0
    except Exception as e:
        logger.error("Failed: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
