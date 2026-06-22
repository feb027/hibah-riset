"""CLI entry point for the Tier 1 smoke test.

Thin wrapper around src.pipeline to make the invocation discoverable
from the repo root and to set PYTHONPATH correctly for the `src/` package.

Usage (from repo root):
    PYTHONPATH=. python scripts/smoke_test_detector.py \
        --video path/to/crowd.mp4 \
        --out experiments/s1_detector_smoke \
        --detector yolov10s
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow `from src...` imports when running as a plain script.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure cwd is the repo root (matters when called from elsewhere).
os.chdir(ROOT)

from src.pipeline import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
