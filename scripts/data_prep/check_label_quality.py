"""Audit kualitas anotasi CrowdHuman sebelum/sesudah konversi ke format YOLO.

Script ini hanya membaca file .odgt dan header gambar (tidak mendekode piksel),
jadi ringan di CPU dan aman dijalankan saat training GPU sedang berlangsung.

Yang diukur:
  1. Berapa box yang titik tengahnya jatuh di luar frame. Ini satu-satunya kasus
     di mana clipping per-komponen pada convert_crowdhuman_to_yolo.py menghasilkan
     geometri yang salah (center di-snap ke tepi, w/h tetap).
  2. Berapa box yang menembus tepi frame tapi center-nya masih di dalam. Box ini
     tetap ditulis apa adanya sebagai fbox amodal - pilihan yang sah, tapi harus
     dinyatakan di metodologi.
  3. Berapa box person bertanda extra.ignore == 1, yang pada protokol CrowdHuman
     standar diperlakukan sebagai ignore region, bukan positif.

--images-dir dicari rekursif, jadi boleh diarahkan ke folder ekstrak mana pun
(zip CrowdHuman menaruh gambarnya di subfolder `Images/`) atau ke folder hasil
konversi di data/processed/.

Contoh:
    python scripts/data_prep/check_label_quality.py \
        --odgt data/raw/crowdhuman/extracted/annotation_val.odgt \
        --images-dir data/raw/crowdhuman/extracted
"""

import argparse
import json
from pathlib import Path

from PIL import Image


def index_images(images_dir):
    """Petakan nama gambar (tanpa ekstensi) -> path, dicari rekursif.

    Zip CrowdHuman mengekstrak isinya ke subfolder `Images/`, jadi lokasi gambar
    tidak bisa diasumsikan sejajar dengan folder yang diberikan user.
    """
    index = {p.stem: p for p in Path(images_dir).rglob("*.jpg")}
    if not index:
        raise FileNotFoundError(
            f"Tidak ada file .jpg di bawah {images_dir} (pencarian rekursif). "
            "Periksa kembali path-nya."
        )
    return index


def audit(odgt_path, images_dir, limit=None):
    images = index_images(images_dir)
    print(f"Terindeks {len(images)} gambar di bawah {images_dir}")

    n_images = 0
    n_missing = 0
    n_person = 0
    n_ignore = 0
    n_center_outside = 0
    n_crosses_border = 0
    n_degenerate = 0

    with open(odgt_path, "r") as f:
        for i, line in enumerate(f):
            if limit is not None and n_images >= limit:
                break

            data = json.loads(line)
            img_path = images.get(data["ID"])
            if img_path is None:
                n_missing += 1
                continue

            # Image.open bersifat lazy: .size hanya membaca header, bukan piksel.
            with Image.open(img_path) as img:
                img_w, img_h = img.size

            n_images += 1

            for gt in data.get("gtboxes", []):
                if gt["tag"] != "person":
                    continue

                n_person += 1
                if gt.get("extra", {}).get("ignore", 0) == 1:
                    n_ignore += 1

                x, y, w, h = gt["fbox"]
                if w <= 0 or h <= 0:
                    n_degenerate += 1
                    continue

                x1, y1, x2, y2 = x, y, x + w, y + h
                if x1 < 0 or y1 < 0 or x2 > img_w or y2 > img_h:
                    n_crosses_border += 1

                cx, cy = x + w / 2.0, y + h / 2.0
                if not (0 <= cx <= img_w and 0 <= cy <= img_h):
                    n_center_outside += 1

    return {
        "images": n_images,
        "missing_images": n_missing,
        "person_boxes": n_person,
        "ignore_boxes": n_ignore,
        "center_outside": n_center_outside,
        "crosses_border": n_crosses_border,
        "degenerate": n_degenerate,
    }


def pct(part, whole):
    return f"{100.0 * part / whole:.2f}%" if whole else "n/a"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odgt", required=True, help="Path ke file .odgt")
    parser.add_argument("--images-dir", required=True, help="Folder gambar terkait")
    parser.add_argument("--limit", type=int, default=None, help="Batasi jumlah gambar (untuk uji cepat)")
    args = parser.parse_args()

    stats = audit(args.odgt, args.images_dir, args.limit)
    total = stats["person_boxes"]

    print(f"\nSumber : {args.odgt}")
    print(f"Gambar : {stats['images']} terbaca, {stats['missing_images']} tidak ditemukan")
    print(f"Box    : {total} box bertag 'person'\n")

    print("--- Dampak bug clipping (menentukan perlu-tidaknya retrain) ---")
    print(f"Center di luar frame  : {stats['center_outside']:>7} ({pct(stats['center_outside'], total)})")
    print("  -> hanya box ini yang geometrinya rusak oleh clipping per-komponen.")
    print("  -> di bawah ~1%: abaikan, catat sebagai batasan. di atas ~5%: pertimbangkan konversi ulang.\n")

    print("--- Keputusan metodologis (cukup ditulis di paper) ---")
    print(f"Menembus tepi frame   : {stats['crosses_border']:>7} ({pct(stats['crosses_border'], total)})")
    print("  -> ditulis apa adanya sebagai fbox amodal, tanpa clipping.")
    print(f"Bertanda ignore=1     : {stats['ignore_boxes']:>7} ({pct(stats['ignore_boxes'], total)})")
    print("  -> saat ini ikut jadi label positif; protokol standar memperlakukannya sebagai ignore.")

    if stats["degenerate"]:
        print(f"\nBox dengan w/h <= 0   : {stats['degenerate']:>7} (dilewati saat audit)")

    print()


if __name__ == "__main__":
    main()
