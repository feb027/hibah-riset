#!/usr/bin/env python3
"""Patch diffmot.py agar evaluasi DiffMOT mengirim img ke tracker (embedding cache).

Latar: di Kroery/DiffMOT, baris `img = cv2.imread(im_path)` DIKOMENTARI, sehingga
`compute_embedding(img=None, ...)` akan crash bila cache `{reid_dir}/{seq}_embedding.pkl`
belum ada. Patch ini mengaktifkan pembacaan img dan meneruskannya ke tracker.update,
sehingga cache terisi otomatis saat run pertama (dump_cache per sekuens) dan dipakai
ulang pada run berikutnya. Idempotent: bila patch sudah terpasang, tidak mengubah apa-apa.

Contoh:
    python scripts/s2/patch_diffmot_eval.py --diffmot-root external/diffmot
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

OLD_IMG = "                # img = cv2.imread(im_path)\n"
NEW_IMG = "                img = cv2.imread(im_path)\n"
OLD_UPDATE = (
    "                online_targets = tracker.update(dets, self.model, frame_id, seq_width, seq_height, tag)\n"
)
NEW_UPDATE = (
    "                online_targets = tracker.update(dets, self.model, frame_id, seq_width, seq_height, tag, img)\n"
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--diffmot-root", required=True, help="root repo Kroery/DiffMOT")
    args = p.parse_args()

    target = Path(args.diffmot_root) / "diffmot.py"
    if not target.exists():
        print(f"ERROR: {target} tidak ditemukan"); return 1
    src = target.read_text()

    changed = 0
    if OLD_IMG in src:
        src = src.replace(OLD_IMG, NEW_IMG); changed += 1
    if OLD_UPDATE in src:
        src = src.replace(OLD_UPDATE, NEW_UPDATE); changed += 1

    if changed:
        target.write_text(src)
        print(f"PATCH DITERAPKAN ({changed} perubahan) di {target}")
    else:
        ok_img = "img = cv2.imread(im_path)" in src
        ok_upd = "tag, img)" in src
        print(f"SUDAH TERPATCH (img_read={ok_img}, pass_img={ok_upd}) — tidak ada perubahan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
