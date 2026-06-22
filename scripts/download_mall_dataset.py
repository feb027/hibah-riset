"""Download the Mall dataset for people-counting baseline (Tier 2+).

The Mall dataset (Chen et al., CVPR 2012) is a classic small people-counting
benchmark: ~2,000 frames of a shopping mall entrance, with crowd-count
labels and RoI. Used here only as a sanity-check dataset for the counting
pipeline once S3 work begins.

License: research use, courtesy of the authors. See http://personal.ie.cuhk.edu.hk/~ccloy/downloads_mall_dataset.html
"""
from __future__ import annotations

import argparse
import logging
import urllib.request
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

# Public CC0 mirror chosen for reproducibility. Replace if the URL rots.
# Original distribution requires a form; mirror chosen to keep script self-contained.
MALL_DATASET_URL = (
    "https://github.com/Neerajj9/Person-Counting-using-Caffe-model/raw/master/dataset/mall_dataset.zip"
)


def download_mall_dataset(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / "mall_dataset.zip"

    if not zip_path.exists():
        logger.info("Downloading %s -> %s", MALL_DATASET_URL, zip_path)
        urllib.request.urlretrieve(MALL_DATASET_URL, zip_path)
    else:
        logger.info("Zip already present at %s", zip_path)

    extract_dir = output_dir / "mall_dataset"
    if not extract_dir.exists():
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)
    return extract_dir


def main() -> int:
    p = argparse.ArgumentParser(description="Download Mall dataset (Tier 2+).")
    p.add_argument("--out", type=Path, default=Path("data/raw/mall"))
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s | %(message)s")
    try:
        extract_dir = download_mall_dataset(args.out)
        print(f"Mall dataset extracted at: {extract_dir}")
        return 0
    except Exception as e:
        logger.error("Failed: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
