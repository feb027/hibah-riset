"""Download the INRIA Person dataset (Dalal & Triggs, CVPR 2005).

Standard small people-detection benchmark, ~50 MB.
- 614 training images + 288 test images (96x160 normalized).
- BBox labels in .mat files.

Mirror choice: original is offline; we use the community mirror at
Caltech (Crowd Maciej) which preserves the original tar structure.

NOTE: For real experiments, verify the mirror still serves the canonical
files. This script is idempotent (skips download if zip exists).
"""
from __future__ import annotations

import argparse
import logging
import shutil
import urllib.request
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

# Public mirror (best-effort; verify before running big experiment).
# Fallback chain: try multiple mirrors in order.
INRIA_MIRRORS: list[str] = [
    "https://www.cs.cmu.edu/~katef/datasets/inria_person_96x160.tar",
]


def download_inria(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    extract_dir = output_dir / "inria_person"

    if (extract_dir / "INRIAPerson").exists() or (extract_dir / "Train").exists():
        logger.info("INRIA already extracted at %s", extract_dir)
        return extract_dir

    tar_path = output_dir / "inria_person_96x160.tar"
    if not tar_path.exists():
        last_err: Exception | None = None
        for url in INRIA_MIRRORS:
            try:
                logger.info("Downloading %s -> %s", url, tar_path)
                urllib.request.urlretrieve(url, tar_path)
                break
            except Exception as e:
                logger.warning("Mirror failed: %s :: %s", url, e)
                last_err = e
        else:
            if last_err is not None:
                raise RuntimeError(
                    f"All INRIA mirrors failed. Last error: {last_err}. "
                    "INRIA's original tar requires an HTTP source that may have rotted. "
                    "Alternative: use a Caltech pedestrian or KITTI-person subset."
                ) from last_err

    # tar is a tar archive; many tools (Python's tarfile) handle it.
    import tarfile

    with tarfile.open(tar_path) as tf:
        tf.extractall(extract_dir)
    return extract_dir


def main() -> int:
    p = argparse.ArgumentParser(description="Download INRIA Person dataset.")
    p.add_argument("--out", type=Path, default=Path("data/raw/inria"))
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s | %(message)s")
    try:
        d = download_inria(args.out)
        print(f"INRIA extracted at: {d}")
        return 0
    except Exception as e:
        logger.error("Failed: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
