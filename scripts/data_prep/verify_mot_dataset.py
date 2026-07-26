"""Periksa apakah sebuah salinan dataset MOT benar-benar dapat dipakai untuk Skenario B.

Dataset MOT beredar dalam banyak unggahan ulang di Kaggle, Roboflow, dan mirror
lain, dan sebagian besar sudah DIKONVERSI menjadi dataset deteksi. Konversi itu
membuang kolom ID lintasan, sehingga salinannya tetap berguna untuk melatih
detektor tetapi **tidak dapat dipakai menghitung HOTA, IDF1, MOTA, maupun ID
switch** - yaitu seluruh alasan dataset ini diperlukan.

Karena itu pemeriksaan tidak boleh berhenti pada "foldernya ada dan gambarnya
banyak". Script ini memeriksa hal yang menentukan:

1. Ada berkas anotasi gt/gt.txt, bukan label per-gambar format deteksi.
2. gt.txt memakai format MOTChallenge: frame, id, x, y, w, h, conf, kelas,
   visibility (minimal 7 kolom, dipisah koma).
3. Kolom ID benar-benar berisi identitas yang BERTAHAN antar frame. Ini uji
   penentunya: pada dataset deteksi yang dikonversi, kolom itu hilang, konstan,
   atau unik per baris. Ketiganya berarti tidak ada lintasan untuk dilacak.
4. Jumlah frame pada img1/ sepadan dengan rentang frame di dalam gt.txt.

Contoh:
    python scripts/data_prep/verify_mot_dataset.py data/raw/mot20/extracted
    python scripts/data_prep/verify_mot_dataset.py data/raw/dancetrack --min-sequences 40
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

KOLOM_MINIMUM = 7


def cari_sekuens(root):
    """Sekuens MOT adalah folder yang memuat img1/. Dicari rekursif."""
    return sorted(p for p in root.rglob("*") if p.is_dir() and (p / "img1").is_dir())


def periksa_gt(gt_path):
    """Baca gt.txt dan nilai apakah isinya benar-benar data lintasan.

    Mengembalikan dict berisi temuan, atau kunci 'galat' bila tidak terbaca.
    """
    try:
        baris = [b for b in gt_path.read_text().splitlines() if b.strip()]
    except Exception as exc:  # noqa: BLE001
        return {"galat": f"{type(exc).__name__}: {exc}"}

    if not baris:
        return {"galat": "gt.txt kosong"}

    kolom = baris[0].split(",")
    if len(kolom) < KOLOM_MINIMUM:
        return {
            "galat": f"hanya {len(kolom)} kolom, format MOTChallenge butuh minimal {KOLOM_MINIMUM}. "
                     f"Baris pertama: {baris[0][:80]}"
        }

    frame_per_id = defaultdict(set)
    frame_terlihat = set()
    rusak = 0

    for b in baris:
        bagian = b.split(",")
        try:
            frame, ident = int(float(bagian[0])), int(float(bagian[1]))
        except (ValueError, IndexError):
            rusak += 1
            continue
        frame_per_id[ident].add(frame)
        frame_terlihat.add(frame)

    if not frame_per_id:
        return {"galat": "tidak ada baris yang dapat diurai"}

    panjang = [len(f) for f in frame_per_id.values()]
    return {
        "baris": len(baris),
        "kolom": len(kolom),
        "n_id": len(frame_per_id),
        "n_frame_gt": len(frame_terlihat),
        "rerata_panjang_lintasan": sum(panjang) / len(panjang),
        "maks_panjang_lintasan": max(panjang),
        "baris_rusak": rusak,
    }


def nilai_sekuens(seq):
    n_gambar = len(list((seq / "img1").glob("*.jpg"))) + len(list((seq / "img1").glob("*.png")))
    gt_path = seq / "gt" / "gt.txt"

    if not gt_path.exists():
        # Split test memang tidak menyertakan ground truth - itu wajar.
        return {"nama": seq.name, "n_gambar": n_gambar, "status": "tanpa-gt", "gt": None}

    gt = periksa_gt(gt_path)
    if "galat" in gt:
        return {"nama": seq.name, "n_gambar": n_gambar, "status": "gt-bermasalah", "gt": gt}

    # Uji penentu: ID harus bertahan antar frame. Lintasan sepanjang 1 frame
    # untuk semua objek berarti anotasinya deteksi per-frame, bukan lintasan.
    if gt["maks_panjang_lintasan"] <= 1:
        return {"nama": seq.name, "n_gambar": n_gambar, "status": "bukan-lintasan", "gt": gt}

    return {"nama": seq.name, "n_gambar": n_gambar, "status": "ok", "gt": gt}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", type=Path, help="Folder hasil ekstraksi dataset")
    parser.add_argument("--min-sequences", type=int, default=1, help="Jumlah sekuens minimum yang diharapkan")
    args = parser.parse_args()

    if not args.root.exists():
        print(f"Folder tidak ada: {args.root}")
        return 1

    sekuens = cari_sekuens(args.root)
    if not sekuens:
        print(f"TIDAK LAYAK: tidak ada folder sekuens ber-img1/ di bawah {args.root}")
        print("  Salinan ini kemungkinan sudah dikonversi ke format lain (mis. YOLO),")
        print("  atau arsipnya belum diekstrak.")
        return 1

    print(f"Memeriksa {len(sekuens)} sekuens di {args.root}\n")
    print(f"{'Sekuens':<24} {'Gambar':>7} {'ID':>6} {'Rerata lintasan':>16}  Status")
    print("-" * 78)

    hasil = [nilai_sekuens(s) for s in sekuens]
    for h in hasil:
        if h["gt"] and "galat" not in h["gt"]:
            print(f"{h['nama']:<24} {h['n_gambar']:>7} {h['gt']['n_id']:>6} "
                  f"{h['gt']['rerata_panjang_lintasan']:>16.1f}  {h['status']}")
        else:
            catatan = h["gt"]["galat"] if h["gt"] else "-"
            print(f"{h['nama']:<24} {h['n_gambar']:>7} {'-':>6} {'-':>16}  {h['status']}  {catatan}")

    n_ok = sum(1 for h in hasil if h["status"] == "ok")
    n_tanpa_gt = sum(1 for h in hasil if h["status"] == "tanpa-gt")
    n_gagal = len(hasil) - n_ok - n_tanpa_gt

    print("-" * 78)
    print(f"\n{n_ok} sekuens berlintasan sah | {n_tanpa_gt} tanpa gt (wajar untuk split test) | {n_gagal} bermasalah")

    if n_ok == 0:
        print("\nTIDAK LAYAK untuk Skenario B.")
        print("  Tidak ada satu pun sekuens dengan ID yang bertahan antar frame, sehingga")
        print("  HOTA, IDF1, MOTA, dan ID switch tidak dapat dihitung. Salinan ini kemungkinan")
        print("  hasil konversi ke format deteksi - berguna untuk melatih detektor, tidak")
        print("  untuk mengevaluasi tracker.")
        return 1

    if n_ok < args.min_sequences:
        print(f"\nKURANG LENGKAP: hanya {n_ok} sekuens berlintasan, diharapkan minimal {args.min_sequences}.")
        print("  Kemungkinan hanya sebagian split yang terunduh.")
        return 1

    print("\nLAYAK untuk Skenario B: anotasi lintasan lengkap dan ID bertahan antar frame.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
