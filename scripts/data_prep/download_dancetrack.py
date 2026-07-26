"""Unduh dan siapkan dataset DanceTrack untuk Skenario B (evaluasi tracker).

DanceTrack (Sun et al., 2022) [S037] memuat 100 video dengan gerak non-linear dan
penampilan yang sangat seragam antar objek. Kombinasi itu menekan kualitas
asosiasi identitas dari sisi yang berbeda dari MOT20: bila MOT20 menekan lewat
kepadatan, DanceTrack menekan lewat gerak yang sulit diprediksi dan kemiripan
visual yang membuat fitur penampilan nyaris tak berguna. Keduanya diperlukan
untuk menilai klaim DiffMOT tentang gerak non-linear.

Sumber resmi repo DanceTrack mengarahkan ke HuggingFace, jadi unduhannya memakai
perkakas yang sama dengan CrowdHuman. Ukuran total sekitar 17,7 GB.

Lisensi: anotasi CC-BY-4.0; datanya untuk keperluan riset non-komersial. Jangan
mendistribusikan ulang data mentah lewat repositori ini (data/ sudah di-ignore).

Contoh:
    python scripts/data_prep/download_dancetrack.py
    python scripts/data_prep/download_dancetrack.py --local-dir data/raw/dancetrack
    python scripts/data_prep/download_dancetrack.py --verify-only
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ID = "noahcao/dancetrack"
DEFAULT_LOCAL_DIR = Path("data/raw/dancetrack")
PERKIRAAN_BYTE = 17.7 * (1 << 30)

PETUNJUK_MANUAL = """
Unduhan lewat pustaka Python gagal. Dua jalur alternatif:

  1. Lewat CLI (perkakas yang sama seperti CrowdHuman):
       pip install -U "huggingface_hub[cli]"
       huggingface-cli download {repo} --repo-type dataset --local-dir {dir}

  2. Lewat peramban, dari https://huggingface.co/datasets/{repo}
     atau mirror yang tercantum di https://github.com/DanceTrack/DanceTrack

Setelah berkasnya ada, jalankan ulang script ini dengan --verify-only untuk
memeriksa struktur foldernya.
"""


def ukuran_terbaca(n):
    for satuan in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024 or satuan == "TB":
            return f"{n:.1f} {satuan}"
        n /= 1024


def periksa_ruang(target, perlu):
    target.mkdir(parents=True, exist_ok=True)
    bebas = shutil.disk_usage(target).free
    print(f"Ruang kosong di {target}: {ukuran_terbaca(bebas)}")
    if bebas < perlu:
        print(f"  PERINGATAN: perkiraan kebutuhan {ukuran_terbaca(perlu)}. "
              "Unduhan kemungkinan gagal di tengah jalan.")
        return False
    return True


def ringkas_struktur(root):
    """Laporkan sekuens per split beserta kelengkapan img1/ dan gt/.

    Struktur yang diharapkan: <root>/dancetrack/{train,val,test}/<sekuens>/img1.
    Ekstraksi dapat menempatkannya lebih dalam, jadi pencariannya rekursif.
    """
    total = 0
    for split in ["train", "val", "test"]:
        folder = [p for p in root.rglob(split) if p.is_dir()]
        sekuens = []
        for f in folder:
            sekuens += [p for p in f.iterdir() if p.is_dir() and (p / "img1").is_dir()]

        if not sekuens:
            print(f"  {split:<6} tidak ditemukan")
            continue

        n_gt = sum(1 for s in sekuens if (s / "gt" / "gt.txt").exists())
        n_frame = sum(len(list((s / "img1").glob("*.jpg"))) for s in sekuens)
        total += len(sekuens)
        print(f"  {split:<6} {len(sekuens):>3} sekuens | {n_frame:>7} frame | {n_gt} ber-gt.txt")

    if total == 0:
        print("\n  PERINGATAN: tidak ada sekuens ber-img1/ ditemukan. "
              "Berkas mungkin masih berupa arsip yang belum diekstrak.")
    else:
        print(f"\n  Total {total} sekuens.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-id", default=REPO_ID)
    parser.add_argument("--local-dir", type=Path, default=DEFAULT_LOCAL_DIR)
    parser.add_argument("--verify-only", action="store_true", help="Lewati unduhan, periksa struktur saja")
    args = parser.parse_args()

    if not args.verify_only:
        try:
            from huggingface_hub import snapshot_download
        except ImportError:
            print("Pustaka huggingface_hub belum terpasang.")
            print(PETUNJUK_MANUAL.format(repo=args.repo_id, dir=args.local_dir))
            return 1

        periksa_ruang(args.local_dir, PERKIRAAN_BYTE * 1.1)

        print(f"\nMengunduh {args.repo_id} ke {args.local_dir} ...")
        print("Unduhan dapat dilanjutkan bila terputus - jalankan ulang perintah yang sama.\n")
        try:
            snapshot_download(
                repo_id=args.repo_id,
                repo_type="dataset",
                local_dir=str(args.local_dir),
                resume_download=True,
            )
        except Exception as exc:  # noqa: BLE001 - kegagalan apa pun tetap ingin dilaporkan
            print(f"\nGAGAL: {type(exc).__name__}: {exc}")
            print(PETUNJUK_MANUAL.format(repo=args.repo_id, dir=args.local_dir))
            return 1
        print("\nUnduhan selesai.")

    if not args.local_dir.exists():
        print(f"Folder {args.local_dir} tidak ada.")
        print(PETUNJUK_MANUAL.format(repo=args.repo_id, dir=args.local_dir))
        return 1

    print(f"\nMemeriksa struktur di {args.local_dir} ...")
    ringkas_struktur(args.local_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
