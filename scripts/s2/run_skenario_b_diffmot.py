#!/usr/bin/env python3
"""Skenario B — jalur DiffMOT (GPU kampus). Satu perintah: patch+smoke+config+run+verify.

Pengganti kombinasi notebook 40 + 50. Dirancang untuk PC kampus (RTX 4090, JupyterHub),
dijalankan DARI kernel `s2-diffmot` (python 3.9 + torch 2.0.1 cu118). Subproses memakai
`sys.executable` (python KERNEL), bukan `!python` yang bisa menunjuk python PATH lain.

Alur (idempotent; --force untuk mengulang):
  ensure : cek torch/CUDA; auto-install deep-person-reid (torchreid) bila import gagal; patch diffmot.py
  gt     : bangun trackers_gt/{split}/{seq}/img1/{frame}.txt dari gt/gt.txt (dibutuhkan DiffMOTDataset)
  config : tulis configs_s2/{mot20_test,dancetrack_test}.yaml dari threshold rilis
  run    : python main.py --dataset mot/dancetrack  (7-10 & 15-20 mnt di 4090)
  verify : hitung file hasil + baris per sekuens ke experiments/s2_tracker/diffmot_results/

Contoh:
  python scripts/s2/run_skenario_b_diffmot.py                       # ensure,gt,config,run,verify
  python scripts/s2/run_skenario_b_diffmot.py --steps ensure,gt,config # cek + config tanpa run
  python scripts/s2/run_skenario_b_diffmot.py --steps verify        # output sudah ada, refresh hitungan
  python scripts/s2/run_skenario_b_diffmot.py --force               # ulang semua run
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def repo_root() -> Path:
    p = Path.cwd()
    while not (p / "AGENTS.md").exists() and p.parent != p:
        p = p.parent
    return p


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo-root", type=Path, default=repo_root())
    p.add_argument("--data-dir", type=Path, default=None, help="default: <repo>/data/s2")
    p.add_argument("--exp-dir", type=Path, default=None, help="default: <repo>/experiments/s2_tracker")
    p.add_argument("--ext-dir", type=Path, default=None, help="default: <repo>/external")
    p.add_argument("--steps", default="ensure,gt,config,run,verify",
                   help="koma: ensure,gt,config,run,verify (default ensure,gt,config,run,verify)")
    p.add_argument("--force", action="store_true", help="ulangi langkah walau output sudah ada")
    return p.parse_args()


def py() -> str:
    return sys.executable


def run(cmd, cwd=None):
    print("   $", " ".join(cmd) if isinstance(cmd, list) else cmd)
    subprocess.run(cmd if isinstance(cmd, list) else cmd.split(), cwd=cwd, check=True)


# ---------------------------------------------------------------- ensure
def step_ensure(a: argparse.Namespace) -> None:
    print("\n== ensure: torch/CUDA + torchreid + patch diffmot ==")
    import torch
    print(f"   torch {torch.__version__} | cuda {torch.cuda.is_available()}")
    assert torch.cuda.is_available(), "CUDA tidak aktif — DiffMOT butuh GPU"
    print("   GPU  :", torch.cuda.get_device_name(0))

    # Auto-fix pitfall notebook-10 ter-skip: deep-person-reid (torchreid) belum terinstall.
    try:
        import torchreid  # noqa: F401
        print("   torchreid: OK")
    except ImportError:
        dpr = a.ext_dir / "diffmot" / "external" / "deep-person-reid"
        assert dpr.is_dir(), f"tidak ada {dpr} — jalankan setup (clone + submodule) dulu"
        print("   torchreid MISSING -> install deep-person-reid (editable) ...")
        run([py(), "-m", "pip", "install", "-q", "-r", str(dpr / "requirements.txt")], cwd=str(dpr))
        run([py(), "-m", "pip", "install", "-q", "-e", "."], cwd=str(dpr))
        import torchreid  # noqa: F401
        print("   torchreid terinstall")

    run([py(), str(a.repo_root / "scripts/s2/patch_diffmot_eval.py"), "--diffmot-root", str(a.ext_dir / "diffmot")])
    src = (a.ext_dir / "diffmot" / "diffmot.py").read_text()
    for pat in ["img = cv2.imread(im_path)", "tag, img)"]:
        print(f"   patch {pat!r}:", "OK" if pat in src else "MISSING")


# ---------------------------------------------------------------- gt
def step_gt(a: argparse.Namespace) -> None:
    """Bangun folder trackers_gt dari gt/gt.txt (yang dibutuhkan DiffMOTDataset).

    DiffMOTDataset membaca {data_dir}/{seq}/img1/*.txt (track GT per-frame, 7 kolom),
    BUKAN folder data dengan gt/gt.txt + img1/*.jpg. `_build_train_loader` tetap
    membangun dataset ini walau eval_mode, dan IndexError 'list index out of range'
    muncul persis saat folder itu kosong. eval() sendiri tidak membaca data ini.
    """
    print("\n== gt: susun trackers_gt dari gt/gt.txt ==")
    for ds, split in [("mot20", "train"), ("dancetrack", "val")]:
        split_root = a.data_dir / ds / split
        if not split_root.exists():
            print(f"   (skip {ds}/{split}: belum ada)")
            continue
        out_root = a.data_dir / ds / "trackers_gt" / split
        n_gt, n_empty = 0, 0
        for seq in sorted(p for p in split_root.iterdir() if p.is_dir()):
            gt = seq / "gt" / "gt.txt"
            if not gt.exists():
                print(f"   (skip {seq.name}: tidak ada gt/gt.txt)")
                continue
            by_frame = {}
            for line in gt.read_text().splitlines():
                if not line.strip():
                    continue
                parts = line.split(",")
                fr = int(parts[0])
                # 7 kolom per baris: frame,id,x,y,w,h,mark — spasi, karena
                # DiffMOTDataset pakai np.loadtxt TANPA delimiter (beda dengan eval).
                by_frame.setdefault(fr, []).append(" ".join([str(fr)] + parts[1:7]))
            img1 = out_root / seq.name / "img1"
            img1.mkdir(parents=True, exist_ok=True)
            written = 0
            for fr in sorted(by_frame):
                rows = by_frame[fr]
                if not rows:
                    n_empty += 1
                    continue
                (img1 / f"{fr:08d}.txt").write_text("\n".join(rows) + "\n")
                written += 1
            n_gt += len(by_frame)
            print(f"      {seq.name}: {written} frame file (dari {len(by_frame)} frame GT)")
        if n_gt == 0:
            print(f"   !! tidak ada GT ditulis untuk {ds} — DiffMOT akan gagal di _build_train_loader")
        print(f"   {ds}: {n_gt} frame GT, {n_empty} frame kosong di-skip")


# ---------------------------------------------------------------- config
def make_config(data_dir, split, eval_expname, high_thres, low_thres, ds, exp_dir):
    import yaml

    return yaml.safe_dump({
        "eps": 0.001, "eval_mode": True, "lr": 0.0001,
        "data_dir": str(data_dir / ds / "trackers_gt" / split),  # DiffMOTDataset butuh img1/*.txt
        "diffnet": "HMINet", "interval": 5, "augment": True,
        "encoder_dim": 256, "tf_layer": 3, "epochs": 800,
        "batch_size": 2048, "seed": 123, "eval_every": 20, "gpus": [0], "eval_at": 800,
        "det_dir": str(data_dir / ds / "detections" / split),
        "info_dir": str(data_dir / ds / split),
        "reid_dir": str(data_dir / "embeddings" / ds),
        "save_dir": str(exp_dir / "diffmot_results" / ds),
        "eval_expname": eval_expname,
        "high_thres": high_thres, "low_thres": low_thres,
        "w_assoc_emb": 2.2, "aw_param": 1.7,
        "preprocess_workers": 8, "device": "cuda", "eval_device": None,
    }, default_flow_style=False)


def step_config(a: argparse.Namespace) -> None:
    print("\n== config: tulis configs_s2 yaml ==")
    cfg_dir = a.ext_dir / "diffmot" / "configs_s2"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    specs = [("mot20", "train", "diffmot_mot", 0.4, 0.1, "mot20_test.yaml"),
             ("dancetrack", "val", "diffmot_dance", 0.6, 0.4, "dancetrack_test.yaml")]
    for ds, split, expname, hi, lo, fname in specs:
        text = make_config(a.data_dir, split, expname, hi, lo, ds, a.exp_dir)
        (cfg_dir / fname).write_text(text)
        print(f"   {fname}: {ds}/{split} hi={hi} lo={lo} expname={expname}")
    print("   configs ditulis ke", cfg_dir)


# ---------------------------------------------------------------- run
def step_run(a: argparse.Namespace) -> None:
    print("\n== run: DiffMOT (GPU) ==")
    diffmot = a.ext_dir / "diffmot"
    for ds, dataset_flag, cfgf, label in [
        ("mot20", "mot", "mot20_test.yaml", "MOT20 (4 sekuens, ~7-10 mnt)"),
        ("dancetrack", "dancetrack", "dancetrack_test.yaml", "DanceTrack (25 sekuens, ~15-20 mnt)"),
    ]:
        out = a.exp_dir / "diffmot_results" / ds
        if any(out.glob("*.txt")) and not a.force:
            print(f"   skip {ds}: hasil sudah ada di {out}")
            continue
        print(f"   run {label} ...")
        run([py(), "main.py", "--config", f"configs_s2/{cfgf}", "--dataset", dataset_flag], cwd=str(diffmot))


# ---------------------------------------------------------------- verify
def step_verify(a: argparse.Namespace) -> None:
    print("\n== verify: hasil DiffMOT ==")
    got = 0
    for ds in ["mot20", "dancetrack"]:
        out = a.exp_dir / "diffmot_results" / ds
        files = sorted(out.glob("*.txt")) if out.exists() else []
        print(f"   {ds}: {len(files)} sekuens")
        for f in files[:5]:
            n = sum(1 for _ in f.open())
            print("     ", f.name, n, "baris")
        got += len(files)
    if got == 0:
        print("   !! belum ada hasil — jalankan --steps run (butuh GPU) atau pindahkan hasil")


# ---------------------------------------------------------------- main
def main() -> int:
    a = parse_args()
    a.data_dir = a.data_dir or a.repo_root / "data" / "s2"
    a.exp_dir = a.exp_dir or a.repo_root / "experiments" / "s2_tracker"
    a.ext_dir = a.ext_dir or a.repo_root / "external"
    for d in (a.data_dir, a.exp_dir):
        d.mkdir(parents=True, exist_ok=True)

    steps = [s.strip() for s in a.steps.split(",") if s.strip()]
    t0 = time.time()
    for s in steps:
        fn = {"ensure": step_ensure, "gt": step_gt, "config": step_config,
              "run": step_run, "verify": step_verify}.get(s)
        if fn is None:
            print(f"!! langkah tak dikenal: {s}"); return 1
        fn(a)
    print(f"\nSELESAI dalam {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())