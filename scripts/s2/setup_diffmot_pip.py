#!/usr/bin/env python3
"""Setup DiffMOT — jalur pip-only untuk PC kampus (Jupyter, tanpa conda/venv).

Jalankan SEKALI di env Jupyter yang sudah diisolasi:
    python scripts/s2/setup_diffmot_pip.py

Yang dilakukan:
1.  Cek python + torch/CUDA (torch yang sudah ada TIDAK ditimpa kalau CUDA aktif;
    kalau belum ada CUDA dan python <= 3.10, install torch 2.0.1 dari index cu118).
2.  pip install paket Skenario B + dependency DiffMOT (requirement.txt DIFFMOT
    tidak mengunci versi torch — aman untuk env yang sudah ada).
3.  Clone DiffMOT / OC_SORT / TrackEval ke external/ (git clone --depth 1).
4.  Install YOLOX, deep-person-reid, fast_reid (editable) — WAJIB walau YOLOX
    tidak dipakai untuk deteksi: kode DiffMOT mengimpornya saat load.
5.  Download 4 bobot rilis DiffMOT v1.0 (2 motion + 2 ReID FastReID).
6.  Verifikasi akhir.

Catatan: deteksi TETAP memakai YOLO26 fine-tune Skenario A (best.pt) lewat
notebook 30; DiffMOT hanya membaca file deteksi (det_dir), YOLOX bawaan tidak
dipakai untuk deteksi.
"""

import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path.cwd()
if not (ROOT / "AGENTS.md").exists():
    ROOT = Path.home() / "hibah-riset"
DATA, EXT = ROOT / "data" / "s2", ROOT / "external"
EXT.mkdir(parents=True, exist_ok=True)


def run(cmd: list[str], **kw) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, **kw)


def pip_install(*pkgs: str, extra: list[str] | None = None) -> None:
    run([sys.executable, "-m", "pip", "install", "-q", *pkgs] + (extra or []))


def git_clone(url: str, dst: Path) -> None:
    if dst.exists():
        print(f"   (skip clone: {dst} sudah ada)")
        return
    run(["git", "clone", "--depth", "1", url, str(dst)])


def download(url: str, dst: Path) -> None:
    if dst.exists() and dst.stat().st_size > 1_000_000:
        print(f"   (skip download: {dst.name} sudah ada)")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    print(f"   download {dst.name} ...")
    urllib.request.urlretrieve(url, dst)
    print(f"   -> {dst.stat().st_size / 1e6:.1f} MB")


def main() -> None:
    print("== 1. python & torch ==")
    print("python:", sys.executable, sys.version.split()[0])
    try:
        import torch

        print("torch:", torch.__version__, "| cuda:", torch.cuda.is_available())
        if torch.cuda.is_available():
            print("GPU  :", torch.cuda.get_device_name(0))
    except ImportError:
        torch = None
        print("torch: belum terpasang")
    if torch is None or not torch.cuda.is_available():
        py3 = sys.version_info
        if py3[:2] <= (3, 10):
            print("   install torch 2.0.1 cu118 (wajib untuk DiffMOT; index cu118, bukan PyPI)")
            pip_install("torch==2.0.1", "torchvision==0.15.2", "torchaudio==2.0.2",
                        extra=["--index-url", "https://download.pytorch.org/whl/cu118"])
        else:
            print(f"   python {py3[0]}.{py3[1]} > 3.10: torch 2.0.1 tidak punya wheel. "
                  "Gunakan torch CUDA yang sudah ada; kalau DiffMOT error, minta admin "
                  "menyediakan env python 3.9/3.10.")

    print("\n== 2. paket Skenario B + dependency DiffMOT ==")
    pip_install("ultralytics", "trackeval", "motmetrics", "filterpy", "loguru",
                "pandas", "openpyxl", "matplotlib", "huggingface_hub",
                "einops", "pyyaml", "easydict", "tensorboardX", "tqdm",
                "opencv-python", "scipy", "lap", "cython", "fvcore")
    try:
        pip_install("cython-bbox")
    except Exception:
        print("   ! cython-bbox gagal build. Coba: pip install cython-bbox --no-build-isolation")
        raise

    print("\n== 3. clone DiffMOT / OC_SORT / TrackEval ==")
    git_clone("https://github.com/Kroery/DiffMOT", EXT / "diffmot")
    git_clone("https://github.com/noahcao/OC_SORT", EXT / "OC_SORT")
    git_clone("https://github.com/JonathonLuiten/TrackEval", EXT / "TrackEval")
    # external/ DiffMOT kadang berupa submodule — pastikan isi
    subprocess.run(["git", "submodule", "update", "--init", "--recursive"],
                   cwd=EXT / "diffmot", check=False)

    print("\n== 4. YOLOX / deep-person-reid / fast_reid (editable) ==")
    for sub, req in [("YOLOX", "requirements.txt"), ("deep-person-reid", "requirements.txt")]:
        d = EXT / "diffmot" / "external" / sub
        if not d.exists():
            sys.exit(f"   ! {d} tidak ada — cek hasil clone DiffMOT (submodule?)")
        if (d / req).exists():
            pip_install("-r", str(d / req))
        run([sys.executable, "-m", "pip", "install", "-q", "-e", str(d)])
    fr = EXT / "diffmot" / "external" / "fast_reid"
    if (fr / "docs" / "requirements.txt").exists():
        pip_install("-r", str(fr / "docs" / "requirements.txt"))

    print("\n== 5. bobot DiffMOT v1.0 ==")
    base = "https://github.com/Kroery/DiffMOT/releases/download/v1.0"
    dl = [
        (f"{base}/MOT_epoch800.pt",
         EXT / "diffmot" / "experiments" / "diffmot_mot" / "mot_epoch800.pt"),
        (f"{base}/DanceTrack_epoch800.pt",
         EXT / "diffmot" / "experiments" / "diffmot_dance" / "dancetrack_epoch800.pt"),
        (f"{base}/mot20_sbs_S50.pth",
         EXT / "diffmot" / "external" / "weights" / "mot20_sbs_S50.pth"),
        (f"{base}/dance_sbs_S50.pth",
         EXT / "diffmot" / "external" / "weights" / "dance_sbs_S50.pth"),
    ]
    for url, dst in dl:
        download(url, dst)

    print("\n== 6. verifikasi ==")
    import torch

    print("torch:", torch.__version__, "| cuda:", torch.cuda.is_available())
    for url, dst in dl:
        ok = dst.exists() and dst.stat().st_size > 1_000_000
        print(("OK  " if ok else "FAIL"), dst.name, f"({dst.stat().st_size/1e6:.0f} MB)" if dst.exists() else "")
    print("\nSelesai. Lanjut:")
    print("  python scripts/s2/run_skenario_b_ocsort.py --steps data,arrange")
    print("  (data: MOT20-train + val.zip saja; set HF_TOKEN untuk download cepat)")
    print("  lalu notebook 30 -> 40 -> 50 -> 70 (kernel apa pun, pakai env ini).")


if __name__ == "__main__":
    main()
