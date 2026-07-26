"""Unduh dan siapkan dataset MOT20 untuk Skenario B (evaluasi tracker).

MOT20 (Dendorfer et al., 2020) [S036] menyediakan delapan sekuens pejalan kaki
sangat padat dari tiga scene, dengan kepadatan yang dapat mencapai ratusan orang
per frame. Dataset ini dipakai menguji stabilitas identitas tracker pada kondisi
kerumunan - prasyarat bagi counting berbasis lintasan.

Berbeda dari CrowdHuman, MOT20 tidak tersedia sebagai repo HuggingFace resmi,
sehingga unduhannya mengarah ke server MOTChallenge. URL bawaan di bawah adalah
pola yang lazim dipakai komunitas, TETAPI tidak diverifikasi oleh penulis script
ini. Karena itu script memeriksa ketersediaan berkas lebih dulu dan berhenti
dengan petunjuk manual bila polanya meleset - bukan mengunduh sesuatu yang salah
lalu gagal di tengah jalan.

Lisensi: MOT20 didistribusikan untuk keperluan riset. Periksa dan patuhi
ketentuan di https://motchallenge.net/ sebelum memakainya, dan jangan
mendistribusikan ulang data mentah lewat repositori ini (data/ sudah di-ignore).

Contoh:
    python scripts/data_prep/download_mot20.py
    python scripts/data_prep/download_mot20.py --raw-dir data/raw/mot20 --extract
    python scripts/data_prep/download_mot20.py --url https://alamat/lain/MOT20.zip
"""
from __future__ import annotations

import argparse
import shutil
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_URL = "https://motchallenge.net/data/MOT20.zip"
DEFAULT_RAW_DIR = Path("data/raw/mot20")
CHUNK = 1 << 20  # 1 MiB

PETUNJUK_MANUAL = """
Unduhan otomatis gagal. Jalur manual:

  1. Buka https://motchallenge.net/data/MOT20/ di peramban.
  2. Unduh berkas arsip MOT20 (biasanya bernama MOT20.zip).
  3. Letakkan berkas itu di: {raw_dir}
  4. Jalankan ulang script ini dengan --extract untuk verifikasi dan ekstraksi.

Bila nama atau alamat berkasnya berbeda dari dugaan script ini, teruskan
alamat yang benar lewat --url, atau langsung --extract bila berkasnya sudah ada.
"""


def ukuran_terbaca(n):
    for satuan in ["B", "KB", "MB", "GB"]:
        if n < 1024 or satuan == "GB":
            return f"{n:.1f} {satuan}"
        n /= 1024


def periksa_url(url):
    """Cek ketersediaan dan ukuran berkas sebelum mengunduh apa pun.

    Mengunduh berkas multi-giga lewat koneksi bersama itu mahal; memastikan
    alamatnya benar lebih dulu jauh lebih murah daripada gagal di tengah jalan.
    """
    permintaan = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(permintaan, timeout=30) as respons:
            panjang = respons.headers.get("Content-Length")
            return True, int(panjang) if panjang else None, None
    except urllib.error.HTTPError as exc:
        return False, None, f"HTTP {exc.code} {exc.reason}"
    except Exception as exc:  # noqa: BLE001 - jaringan apa pun tetap ingin dilaporkan
        return False, None, f"{type(exc).__name__}: {exc}"


def unduh(url, tujuan, total=None):
    """Unduh dengan dukungan lanjut (resume) supaya putus koneksi tidak mengulang dari nol."""
    sudah = tujuan.stat().st_size if tujuan.exists() else 0

    if total is not None and sudah >= total:
        print(f"  Berkas sudah lengkap ({ukuran_terbaca(sudah)}), unduhan dilewati.")
        return

    permintaan = urllib.request.Request(url)
    if sudah:
        permintaan.add_header("Range", f"bytes={sudah}-")
        print(f"  Melanjutkan dari {ukuran_terbaca(sudah)} ...")

    with urllib.request.urlopen(permintaan, timeout=60) as respons, open(tujuan, "ab") as f:
        terunduh = sudah
        while True:
            potongan = respons.read(CHUNK)
            if not potongan:
                break
            f.write(potongan)
            terunduh += len(potongan)
            if total:
                print(f"\r  {ukuran_terbaca(terunduh)} / {ukuran_terbaca(total)} "
                      f"({100 * terunduh / total:5.1f}%)", end="", flush=True)
            else:
                print(f"\r  {ukuran_terbaca(terunduh)}", end="", flush=True)
    print()


def verifikasi_zip(path):
    """Pastikan arsipnya utuh sebelum diekstrak, agar unduhan terpotong ketahuan lebih awal."""
    if not zipfile.is_zipfile(path):
        return False, "bukan berkas zip yang sah (unduhan kemungkinan terpotong)"
    try:
        with zipfile.ZipFile(path) as zf:
            rusak = zf.testzip()
        return (True, None) if rusak is None else (False, f"entri rusak: {rusak}")
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def ringkas_struktur(root):
    """Laporkan sekuens yang ditemukan beserta kelengkapan img1/ dan gt/."""
    sekuens = sorted(p for p in root.rglob("*") if p.is_dir() and (p / "img1").is_dir())
    if not sekuens:
        print("  PERINGATAN: tidak ada folder sekuens ber-img1/ yang ditemukan.")
        return

    print(f"\n  {len(sekuens)} sekuens ditemukan:")
    for seq in sekuens:
        n_frame = len(list((seq / "img1").glob("*.jpg")))
        ada_gt = (seq / "gt" / "gt.txt").exists()
        tanda = "gt ada" if ada_gt else "gt TIDAK ADA (sekuens test)"
        print(f"    {seq.relative_to(root)!s:<28} {n_frame:>6} frame  |  {tanda}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default=DEFAULT_URL, help="Alamat arsip MOT20")
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR, help="Folder penyimpanan arsip")
    parser.add_argument("--extract", action="store_true", help="Ekstrak setelah unduhan selesai")
    parser.add_argument("--skip-download", action="store_true", help="Pakai arsip yang sudah ada")
    args = parser.parse_args()

    args.raw_dir.mkdir(parents=True, exist_ok=True)
    arsip = args.raw_dir / Path(args.url).name

    if not args.skip_download:
        print(f"Memeriksa {args.url} ...")
        tersedia, total, galat = periksa_url(args.url)

        if not tersedia:
            print(f"  GAGAL: {galat}")
            print(PETUNJUK_MANUAL.format(raw_dir=args.raw_dir.resolve()))
            return 1

        print(f"  Tersedia, ukuran {ukuran_terbaca(total) if total else 'tidak diketahui'}")
        if total:
            bebas = shutil.disk_usage(args.raw_dir).free
            # Butuh ruang untuk arsip sekaligus hasil ekstraksinya.
            if bebas < total * 2.2:
                print(f"  PERINGATAN: ruang kosong {ukuran_terbaca(bebas)}, "
                      f"disarankan minimal {ukuran_terbaca(total * 2.2)} (arsip + hasil ekstrak).")

        print(f"\nMengunduh ke {arsip} ...")
        try:
            unduh(args.url, arsip, total)
        except Exception as exc:  # noqa: BLE001
            print(f"\n  GAGAL: {type(exc).__name__}: {exc}")
            print("  Unduhan parsial dipertahankan; jalankan ulang untuk melanjutkan.")
            print(PETUNJUK_MANUAL.format(raw_dir=args.raw_dir.resolve()))
            return 1

    if not arsip.exists():
        print(f"Arsip tidak ditemukan di {arsip}")
        print(PETUNJUK_MANUAL.format(raw_dir=args.raw_dir.resolve()))
        return 1

    print(f"\nMemverifikasi {arsip.name} ...")
    utuh, galat = verifikasi_zip(arsip)
    if not utuh:
        print(f"  GAGAL: {galat}")
        print("  Hapus berkas itu lalu jalankan ulang untuk mengunduh dari awal.")
        return 1
    print("  Arsip utuh.")

    if args.extract:
        tujuan = args.raw_dir / "extracted"
        print(f"\nMengekstrak ke {tujuan} ...")
        tujuan.mkdir(exist_ok=True)
        with zipfile.ZipFile(arsip) as zf:
            zf.extractall(tujuan)
        print("  Selesai.")
        ringkas_struktur(tujuan)
    else:
        print("\nJalankan ulang dengan --extract untuk mengekstrak.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
