"""Download helper for CrowdHuman (Shao et al., 2018).

CrowdHuman is the canonical crowd-detection benchmark used in many
people-counting papers. It contains ~15K training, 4,370 validation,
and 5,000 test images with BBox + visibility + head-annotation labels.

CAUTION: the official download requires manual registration at
https://www.crowdhuman.org/ (the user must accept their terms). This
script does NOT bypass that — it documents the steps and validates an
already-downloaded directory.

Steps the USER must do manually:

1. Register at https://www.crowdhuman.org/ and accept the license.
2. Download these three files via the official link:
   - `CrowdHuman_train01.zip`  (Train part 1, ~3.5 GB)
   - `CrowdHuman_train02.zip`  (Train part 2, ~3.5 GB)
   - `CrowdHuman_train03.zip`  (Train part 3, ~3.5 GB)
   - `CrowdHuman_val.zip`       (Val, ~1.5 GB)
   - `annotation_train.odgt`    (Train labels, JSON-lines)
   - `annotation_val.odgt`      (Val labels, JSON-lines)
3. Place all six files into a single directory (default: data/raw/crowdhuman/).
4. Run this script to extract and verify.

Anti-overclaim: the official download is gated; do not commit the raw
data or annotations to the repo. data/ is .gitignored.
"""
from __future__ import annotations

import argparse
import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


EXPECTED_FILES = [
    "CrowdHuman_train01.zip",
    "CrowdHuman_train02.zip",
    "CrowdHuman_train03.zip",
    "CrowdHuman_val.zip",
    "annotation_train.odgt",
    "annotation_val.odgt",
]


def validate_inputs(raw_dir: Path) -> list[Path]:
    missing = [f for f in EXPECTED_FILES if not (raw_dir / f).exists()]
    if missing:
        raise FileNotFoundError(
            "Missing files in " + str(raw_dir) + ":\n  - " + "\n  - ".join(missing) + "\n\n"
            "Please download them manually from https://www.crowdhuman.org/ "
            "(registration required, license must be accepted) and place them in "
            + str(raw_dir) + " before re-running this script."
        )
    return [raw_dir / f for f in EXPECTED_FILES]


def extract_zip_safely(zf_path: Path, extract_to: Path) -> None:
    logger.info("Extracting %s -> %s", zf_path.name, extract_to)
    with zipfile.ZipFile(zf_path) as zf:
        zf.extractall(extract_to)


def setup_crowdhuman(raw_dir: Path, extract_root: Path | None = None) -> Path:
    """Validate that the user-supplied raw files exist, then extract.

    Returns the path containing the extracted images and odgt files.
    """
    files = validate_inputs(raw_dir)
    extract_root = extract_root or raw_dir / "extracted"
    extract_root.mkdir(parents=True, exist_ok=True)

    for f in files:
        if f.suffix == ".zip":
            extract_to = extract_root / f.stem
            if not extract_to.exists():
                extract_to.mkdir(parents=True, exist_ok=True)
                extract_zip_safely(f, extract_to)
            else:
                logger.info("Already extracted: %s", extract_to)
        else:
            # .odgt — copy to extract root for easy discovery
            target = extract_root / f.name
            if not target.exists():
                target.write_bytes(f.read_bytes())
                logger.info("Linked %s -> %s", f, target)
    return extract_root


def main() -> int:
    p = argparse.ArgumentParser(description="Set up CrowdHuman dataset.")
    p.add_argument("--raw-dir", type=Path, default=Path("data/raw/crowdhuman"),
                   help="Directory containing the user-downloaded CrowdHuman files.")
    p.add_argument("--extract-dir", type=Path, default=None)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s | %(message)s")
    try:
        d = setup_crowdhuman(args.raw_dir, args.extract_dir)
        print(f"CrowdHuman ready at: {d}")
        return 0
    except Exception as e:
        logger.error("Failed: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
