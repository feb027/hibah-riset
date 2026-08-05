#!/usr/bin/env python3
"""Patch DiffMOT agar evaluasi berjalan (diffmot.py + DiffMOTtracker.py). Idempotent.

Patch yang ditangani:
1. diffmot.py — aktifkan `img = cv2.imread(im_path)` dan teruskan img ke
   `tracker.update(...)`. Source asli meng-komentari keduanya, jadi embedding cache
   (`{reid_dir}/{seq}_embedding.pkl`) tidak pernah terisi → crash saat `__getitem__`.
   Sekaligus tambah `import cv2` (source asli tidak punya).
2. DiffMOTtracker.py — baris embedder hardcode `'dancetrack'`, padahal embedding.py
   hanya mengenal dataset `mot17/mot20/dance/sports`. Akibatnya `initialize_model()`
   selalu raise `RuntimeError("Need the path for a new ReID model.")` saat cache ReID
   kosong. Patch mengganti dataset hardcoded dengan peta dari `config.dataset`.

Contoh:
    python scripts/s2/patch_diffmot_eval.py --diffmot-root external/diffmot
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

IMPORT_NAME = "import numpy as np\n"
IMPORT_PATCH = "import numpy as np\nimport cv2\n"

IMG_OLD = "                # img = cv2.imread(im_path)\n"
IMG_NEW = "                img = cv2.imread(im_path)\n"
UPDATE_OLD = (
    "                online_targets = tracker.update(dets, self.model, frame_id, seq_width, seq_height, tag)\n"
)
UPDATE_NEW = (
    "                online_targets = tracker.update(dets, self.model, frame_id, seq_width, seq_height, tag, img)\n"
)

EMB_OLD = "        self.embedder = EmbeddingComputer(self.config, 'dancetrack', False, True)\n"
EMB_NEW = (
    "        reid_ds = {'mot': 'mot20', 'mot17': 'mot17', 'dancetrack': 'dance', 'dance': 'dance',\n"
    "                   'sports': 'sports'}.get(self.config.dataset, 'dance')\n"
    "        self.embedder = EmbeddingComputer(self.config, reid_ds, False, True)\n"
)


def patch_text(label: str, old: str, new: str, src: str) -> tuple[str, bool]:
    # Marker full string (dengan indentasi) supaya baris KOMENTAR "# ... tag, img)"
    # tidak dianggap sudah terpatch. import_cv2: cek import top-level.
    marker = "import cv2" if label == "import_cv2" else new
    if marker in src:
        return src, False
    if old not in src:
        print(f"   (skip {label}: pola lama tidak ditemukan — periksa manual)")
        return src, False
    return src.replace(old, new), True


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--diffmot-root", required=True, help="root repo Kroery/DiffMOT")
    args = p.parse_args()
    root = Path(args.diffmot_root)

    targets = [
        ("diffmot.py", [("img_read", IMG_OLD, IMG_NEW),
                        ("pass_img", UPDATE_OLD, UPDATE_NEW),
                        ("import_cv2", IMPORT_NAME, IMPORT_PATCH)]),
        ("tracker/DiffMOTtracker.py", [("reid_ds", EMB_OLD, EMB_NEW)]),
    ]

    for fname, patches in targets:
        fp = root / fname
        if not fp.exists():
            print(f"ERROR: {fp} tidak ditemukan"); return 1
        src = fp.read_text()
        n = 0
        for label, old, new in patches:
            src, changed = patch_text(label, old, new, src)
            n += changed
        if n:
            fp.write_text(src)
            print(f"PATCH DITERAPKAN ({n} perubahan) di {fp}")
        else:
            print(f"SUDAH TERPATCH di {fp} — tidak ada perubahan")
    return 0


if __name__ == "__main__":
    sys.exit(main())