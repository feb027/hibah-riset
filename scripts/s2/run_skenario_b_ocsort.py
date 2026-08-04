#!/usr/bin/env python3
"""Skenario B — jalur OC-SORT: satu perintah dari data sampai metrik (CPU-only).

Dirancang untuk PC rumah (i5-12400F, RAM 16 GB, tanpa GPU) atau VPS — tidak butuh CUDA.
Alur: arrange data -> deteksi YOLO fine-tune (CPU) -> track OC-SORT -> eval TrackEval.

Langkah (idempotent; --force untuk mengulang):
  arrange  : susun sekuens dari hasil unduhan ke layout data/s2/{ds}/{split}/ + seqinfo + verify
  detect   : YOLO (bobot Skenario A) atas MOT20-train + DanceTrack-val -> det_mot + detections/
  track    : OC-SORT atas deteksi -> experiments/s2_tracker/ocsort_results/
  eval     : TrackEval (HOTA/IDF1/MOTA/IDSW/Frag) -> experiments/s2_tracker/eval_results.csv

Contoh:
  # 1) unduh data (lihat docs/panduan-skenario-b-oc-sort.md) lalu:
  python scripts/s2/run_skenario_b_ocsort.py --steps arrange,detect,track,eval

  # hanya evaluasi ulang (deteksi & tracking sudah ada):
  python scripts/s2/run_skenario_b_ocsort.py --steps eval

  # satu perintah lengkap termasuk unduh (butuh bandwidth besar):
  python scripts/s2/run_skenario_b_ocsort.py --steps data,arrange,detect,track,eval
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

TRAIN_MOT20 = {"MOT20-01", "MOT20-02", "MOT20-03", "MOT20-05"}


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
    p.add_argument("--weights", type=Path, default=None, help="bobot YOLO fine-tune Skenario A (default: *.pt pertama di data-dir/weights)")
    p.add_argument("--steps", default="arrange,detect,track,eval",
                   help="koma: data,arrange,detect,track,eval (default arrange,detect,track,eval)")
    p.add_argument("--force", action="store_true", help="ulangi langkah walau output sudah ada")
    # deteksi
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.05)
    p.add_argument("--iou", type=float, default=0.7)
    # OC-SORT
    p.add_argument("--track-thresh", type=float, default=0.3)
    p.add_argument("--min-conf", type=float, default=0.3, help="threshold score deteksi sebelum OC-SORT")
    p.add_argument("--iou-thresh", type=float, default=0.3)
    p.add_argument("--delta-t", type=int, default=3)
    p.add_argument("--min-hits", type=int, default=3)
    p.add_argument("--max-age", type=int, default=30)
    p.add_argument("--skip-verify", action="store_true", help="lewati verify_mot_dataset.py saat arrange")
    return p.parse_args()


def py() -> str:
    return sys.executable


# ---------------------------------------------------------------- data
def step_data(a: argparse.Namespace) -> None:
    """Unduh MOT20 (HF Lekim89/MOT20) + DanceTrack (HF noahcao/dancetrack, tanpa test)."""
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        sys.exit("huggingface_hub belum terpasang: pip install huggingface_hub")

    print("\n== data: MOT20 (HF Lekim89/MOT20) ==")
    snapshot_download(repo_id="Lekim89/MOT20", repo_type="dataset",
                      local_dir=str(a.data_dir / "mot20_hf"),
                      ignore_patterns=["test/*"])   # hanya butuh train
    print("\n== data: DanceTrack (HF noahcao/dancetrack, tanpa test/train) ==")
    snapshot_download(repo_id="noahcao/dancetrack", repo_type="dataset",
                      local_dir=str(a.data_dir / "dancetrack_hf"),
                      # mirror menyimpan zip: val.zip, train1/2.zip, test1/2.zip, *.xlsx
                      ignore_patterns=["test/*", "test*", "train*", "*.xlsx"])


# ---------------------------------------------------------------- arrange
def find_seqs(root: Path, need_gt: bool):
    """Cari folder sekuens (punya img1/, opsional gt/gt.txt) di bawah root."""
    found = []
    for img1 in root.rglob("img1"):
        if img1.is_dir() and any(img1.iterdir()):
            seq = img1.parent
            if not need_gt or (seq / "gt" / "gt.txt").exists():
                found.append(seq)
    return sorted(found, key=lambda p: p.name)


def unlink_layout(target: Path) -> None:
    """Hapus entry layout lama (junction/symlink/copy) TANPA menyentuh sumber.
    Windows junction: `cmd /c rmdir` menghapus junction saja, tidak mengikuti target."""
    if not target.exists() and not os.path.islink(str(target)):
        return
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "rmdir", str(target)], check=True, capture_output=True)
    elif target.is_symlink():
        target.unlink()
    elif target.is_dir():
        import shutil
        shutil.rmtree(target)
    else:
        target.unlink()


def link_seq(src: Path, dst_dir: Path, force: bool = False) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    target = dst_dir / src.name
    if target.exists() and not force:
        return target
    if target.exists() or os.path.islink(str(target)):
        unlink_layout(target)  # relink dari sumber TERBARU (download yang sudah lengkap)
    if os.name == "nt":
        # Windows: junction (tidak butuh admin/Developer Mode), setara symlink dir
        subprocess.run(["cmd", "/c", "mklink", "/J", str(target), str(src)],
                       check=True, capture_output=True)
    else:
        os.symlink(src, target, target_is_directory=True)
    return target


def synth_seqinfo(seq_dir: Path, force: bool = False) -> bool:
    """Tulis seqinfo.ini valid (dari frame nyata). force=True menimpa yang lama — TrackEval
    membaca file ini persis di path ini dan mirror kadang menyediakan yang rusak/tak terbaca."""
    ini = seq_dir / "seqinfo.ini"
    if ini.exists() and not force:
        return False
    import cv2
    imgs = sorted((seq_dir / "img1").glob("*.*"))
    if not imgs:
        return False
    h, w = cv2.imread(str(imgs[0])).shape[:2]
    ini.write_text(
        f"[Sequence]\nname={seq_dir.name}\nimDir=img1\nframeRate=30\n"
        f"seqLength={len(imgs)}\nimWidth={w}\nimHeight={h}\nimExt={imgs[0].suffix}\n"
    )
    return True


def step_arrange(a: argparse.Namespace) -> None:
    print("\n== arrange: susun sekuens ke layout kerja ==")
    # MOT20 -> data/s2/mot20/train (hanya 4 sekuens train ber-GT)
    src = a.data_dir / "mot20_hf"
    if src.exists():
        cands = find_seqs(src, need_gt=True)
        linked = set()
        for s in cands:
            if s.name in TRAIN_MOT20 and s.name not in linked:
                link_seq(s, a.data_dir / "mot20" / "train", force=a.force)
                linked.add(s.name)
        n = len(linked)
        if n == 0:
            print("!! TIDAK ada sekuens MOT20 train (01/02/03/05) ber-GT ditemukan di", src)
            print("   Nama yang ditemukan:", [s.name for s in cands][:20])
            print("   Cek sumber lain: HF Lekim89/MOT20 atau motchallenge.net (registrasi).")
            sys.exit(1)
        print(f"   MOT20 train: {n} sekuens")
    else:
        print(f"   (skip: {src} belum ada — jalankan --steps data dulu)")

    # DanceTrack -> data/s2/dancetrack/val (link SEMUA sekuens ber-img1; GT dilaporkan terpisah)
    src = a.data_dir / "dancetrack_hf"
    if src.exists():
        # Mirror noahcao/dancetrack menyimpan arsip zip (val.zip, train*.zip, test*.zip)
        zips = sorted(src.glob("*.zip"))
        if zips:
            import zipfile
            extract_dir = src / "extracted"
            extract_dir.mkdir(parents=True, exist_ok=True)
            for z in zips:
                if z.stem.startswith(("test", "train")):
                    continue  # hanya butuh val
                target = extract_dir / z.stem
                if target.exists() and any(target.iterdir()):
                    print(f"   (skip extract {z.name}: sudah ada)")
                    continue
                print(f"   extract {z.name} ...")
                with zipfile.ZipFile(z) as zf:
                    zf.extractall(extract_dir)
        cands = find_seqs(src, need_gt=False)
        linked, with_gt = set(), 0
        for s in cands:
            if s.name in linked:
                continue
            link_seq(s, a.data_dir / "dancetrack" / "val", force=a.force)
            linked.add(s.name)
            if (s / "gt" / "gt.txt").exists():
                with_gt += 1
        print(f"   DanceTrack val: {len(linked)} sekuens ditautkan ({with_gt} ber-GT)")
        if not linked:
            print("   !! tidak ada folder ber-img1 ditemukan di", src)
            print("   Isi:", [p.name for p in src.iterdir()][:20])
            print("   Cek apakah unduhan selesai: foldernya harus berisi val/ (atau sekuens dancetrack00XX/)")
        elif with_gt == 0:
            print("   !! TIDAK ada gt.txt di sekuens val — eval DanceTrack tidak bisa berjalan")
            print("   Sumber GT: pastikan mirror menyertakan gt/gt.txt per sekuens val (resmi: noahcao/dancetrack)")
    else:
        print(f"   (skip: {src} belum ada — jalankan --steps data dulu)")

    # seqinfo synthesis — SELALU ditulis ulang (TrackEval baca persis di path ini)
    n = 0
    for split_root in [a.data_dir / "mot20" / "train", a.data_dir / "dancetrack" / "val"]:
        if split_root.exists():
            for seq in sorted(p for p in split_root.iterdir() if p.is_dir()):
                n += synth_seqinfo(seq, force=True)
    if n:
        print(f"   seqinfo: {n} ditulis/diperbarui")

    # verify
    if not a.skip_verify:
        for root, extra in [(a.data_dir / "mot20" / "train", []),
                            (a.data_dir / "dancetrack" / "val", ["--min-sequences", "20"])]:
            if root.exists() and any(root.iterdir()):
                print(f"   verify {root} ...")
                r = subprocess.run([py(), str(a.repo_root / "scripts/data_prep/verify_mot_dataset.py"),
                                    str(root), *extra])
                if r.returncode != 0:
                    sys.exit(f"VERIFY GAGAL: {root} tidak layak (kemungkinan mirror tanpa track ID). "
                             "Ganti sumber dataset lalu ulangi.")


# ---------------------------------------------------------------- detect
def step_detect(a: argparse.Namespace) -> None:
    print("\n== detect: YOLO fine-tune (CPU) ==")
    if a.weights is None or not a.weights.exists():
        wts = sorted((a.data_dir / "weights").glob("*.pt")) or sorted((a.data_dir / "weights").glob("*.onnx"))
        if not wts:
            sys.exit(f"Tidak ada bobot di {a.data_dir / 'weights'}/ — taruh best.pt (atau best.onnx) "
                     "Skenario A di sana (--weights untuk path lain; onnx ~2x lebih cepat di CPU)")
        a.weights = wts[0]
    print("   weights:", a.weights)

    import cv2
    import numpy as np
    import pandas as pd
    from ultralytics import YOLO

    model = YOLO(str(a.weights))
    stats_all = []
    for ds, split in [("mot20", "train"), ("dancetrack", "val")]:
        split_root = a.data_dir / ds / split
        if not split_root.exists():
            print(f"   (skip {ds}/{split}: belum ada)")
            continue
        det_dir = a.data_dir / ds / "detections" / split
        det_mot_dir = a.data_dir / ds / "det_mot" / split
        det_dir.mkdir(parents=True, exist_ok=True)
        det_mot_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n   === {ds}/{split} ===")
        for seq in sorted(p for p in split_root.iterdir() if p.is_dir()):
            out_mot = det_mot_dir / f"{seq.name}.txt"
            if out_mot.exists() and not a.force:
                print(f"   skip {seq.name} (sudah ada)")
                continue
            frames = sorted((seq / "img1").glob("*.*"))
            t0 = time.time()
            tot_det = 0
            with open(out_mot, "w") as mf:
                for i, fp in enumerate(frames):
                    frame = i + 1
                    img = cv2.imread(str(fp))
                    H, W = img.shape[:2]
                    r = model.predict(img, imgsz=a.imgsz, conf=a.conf, iou=a.iou,
                                      device="cpu", verbose=False)[0]
                    lines = []
                    for b in r.boxes:
                        x1, y1, x2, y2 = b.xyxy[0].tolist()
                        x1, y1 = max(0.0, x1), max(0.0, y1)
                        x2, y2 = min(W, x2), min(H, y2)
                        w, h = x2 - x1, y2 - y1
                        if w <= 1 or h <= 1:
                            continue
                        sc = float(b.conf)
                        lines.append(f"{frame},{x1:.2f},{y1:.2f},{w:.2f},{h:.2f},{sc:.4f}\n")
                        mf.write(f"{frame},-1,{x1:.2f},{y1:.2f},{w:.2f},{h:.2f},{sc:.4f},-1,-1,-1\n")
                    if lines:
                        (det_dir / seq.name).mkdir(parents=True, exist_ok=True)
                        (det_dir / seq.name / f"{frame:08d}.txt").write_text("".join(lines))
                    tot_det += len(lines)
            n = len(frames)
            dt = time.time() - t0
            stats_all.append({"dataset": ds, "seq": seq.name, "frames": n, "dets": tot_det,
                              "dets/frame": round(tot_det / n, 2) if n else 0.0,
                              "seconds": round(dt, 1)})
            print(f"   {seq.name:16s} frames={n:5d} dets={tot_det:6d} {dt:6.1f}s")
    if stats_all:
        df = pd.DataFrame(stats_all)
        df.to_csv(a.exp_dir / "detection_stats.csv", index=False)
        print("\n   detection_stats.csv:", a.exp_dir / "detection_stats.csv")


# ---------------------------------------------------------------- track
def step_track(a: argparse.Namespace) -> None:
    print("\n== track: OC-SORT ==")
    try:
        import filterpy  # noqa: F401
    except ImportError:
        print("   filterpy belum ada — install otomatis ...")
        subprocess.run([py(), "-m", "pip", "install", "-q", "filterpy"], check=True)
    ocsort_root = a.ext_dir / "OC_SORT"
    if not (ocsort_root / "trackers").exists():
        print("   clone OC_SORT ...")
        subprocess.run(["git", "clone", "--depth", "1",
                        "https://github.com/noahcao/OC_SORT", str(ocsort_root)], check=True)
    runner = a.repo_root / "scripts/s2/run_ocsort_mot.py"
    for ds, split in [("mot20", "train"), ("dancetrack", "val")]:
        det_dir = a.data_dir / ds / "det_mot" / split
        if not det_dir.exists():
            print(f"   (skip {ds}: deteksi belum ada)")
            continue
        out_dir = a.exp_dir / "ocsort_results" / ds
        if any(out_dir.glob("*.txt")) and not a.force:
            print(f"   skip {ds} (hasil sudah ada)")
            continue
        print(f"   {ds}/{split} ...")
        subprocess.run([py(), str(runner),
                        "--ocsort-root", str(ocsort_root),
                        "--det-dir", str(det_dir),
                        "--out-dir", str(out_dir),
                        "--track-thresh", str(a.track_thresh),
                        "--min-conf", str(a.min_conf),
                        "--iou-thresh", str(a.iou_thresh),
                        "--delta-t", str(a.delta_t),
                        "--min-hits", str(a.min_hits),
                        "--max-age", str(a.max_age)], check=True)


# ---------------------------------------------------------------- eval
def write_seqmap(seqs, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("name\n" + "\n".join(seqs) + "\n")


def step_eval(a: argparse.Namespace) -> None:
    print("\n== eval: TrackEval (HOTA/IDF1/MOTA/IDSW/Frag) ==")
    import shutil
    import pandas as pd
    import trackeval

    trackers_root = a.exp_dir / "trackeval_trackers"
    for ds, src in [("mot20", a.exp_dir / "ocsort_results" / "mot20"),
                    ("dance", a.exp_dir / "ocsort_results" / "dancetrack")]:
        dst = trackers_root / ds / "ocsort" / "data"
        dst.mkdir(parents=True, exist_ok=True)
        n = 0
        for f in src.glob("*.txt"):
            shutil.copy2(f, dst / f.name)
            n += 1
        print(f"   {ds}: {n} hasil disalin")

    def preflight_eval(gt_folder: Path, trackers_folder: Path, tracker: str,
                       seqmap: Path) -> None:
        """Validasi layout langsung yang benar-benar akan dibaca TrackEval."""
        seqs = [line.strip() for line in seqmap.read_text().splitlines()[1:] if line.strip()]
        missing = []
        for seq in seqs:
            for path in [gt_folder / seq / "seqinfo.ini",
                         gt_folder / seq / "gt" / "gt.txt",
                         trackers_folder / tracker / "data" / f"{seq}.txt"]:
                if not path.is_file():
                    missing.append(path)
        if missing:
            preview = "\n".join(f"     - {p}" for p in missing[:10])
            raise FileNotFoundError(
                f"Preflight TrackEval gagal: {len(missing)} file tidak ada:\n{preview}"
            )
        print(f"   preflight: {len(seqs)} sekuens, semua GT/seqinfo/tracker ada")

    def run_eval(gt_folder, trackers_folder, tracker, seqmap, split):
        preflight_eval(gt_folder, trackers_folder, tracker, seqmap)
        eval_cfg = trackeval.Evaluator.get_default_eval_config()
        eval_cfg.update(USE_PARALLEL=False, NUM_PARALLEL_CORES=8,
                        PLOT_CURVES=False, DISPLAY_LESS_PROGRESS=True,
                        PRINT_ONLY_COMBINED=True)
        ds_cfg = trackeval.datasets.MotChallenge2DBox.get_default_dataset_config()
        ds_cfg.update(BENCHMARK="MOT20", GT_FOLDER=str(gt_folder),
                      TRACKERS_FOLDER=str(trackers_folder), TRACKERS_TO_EVAL=[tracker],
                      SEQMAP_FILE=str(seqmap), SPLIT_TO_EVAL=split,
                      # Kedua dataset sudah disusun langsung sebagai GT_FOLDER/{seq}/.
                      # False akan menambahkan folder MOT20-{split} yang tidak ada.
                      SKIP_SPLIT_FOL=True, DO_PREPROC=False)
        metrics = [trackeval.metrics.HOTA(), trackeval.metrics.CLEAR(), trackeval.metrics.Identity()]
        return trackeval.Evaluator(eval_cfg).evaluate(
            [trackeval.datasets.MotChallenge2DBox(ds_cfg)], metrics)

    def extract(out):
        import numpy as np

        # TrackEval >= 1.0 mengembalikan (output_res, output_msg).
        results = out[0] if isinstance(out, tuple) else out
        rows = []
        for ds_name, trackers in results.items():
            for trk, seq_results in trackers.items():
                combined = seq_results["COMBINED_SEQ"]
                for cls, metrics in combined.items():
                    hota = float(np.mean(metrics["HOTA"]["HOTA"])) * 100.0
                    mota = float(metrics["CLEAR"]["MOTA"]) * 100.0
                    idf1 = float(metrics["Identity"]["IDF1"]) * 100.0
                    rows.append(dict(
                        dataset=ds_name, tracker=trk, cls=cls,
                        HOTA=round(hota, 4), MOTA=round(mota, 4), IDF1=round(idf1, 4),
                        IDSW=int(metrics["CLEAR"]["IDSW"]),
                        Frag=int(metrics["CLEAR"]["Frag"]),
                    ))
        return rows

    seqs_mot = [p.name for p in (a.data_dir / "mot20" / "train").iterdir()
                if p.is_dir() and (p / "gt" / "gt.txt").exists()]
    val_dir = a.data_dir / "dancetrack" / "val"
    if val_dir.exists() and any(val_dir.iterdir()):
        seqs_dance = [p.name for p in val_dir.iterdir()
                      if p.is_dir() and (p / "gt" / "gt.txt").exists()]
    else:
        seqs_dance = []
        print("   (skip dance: data/s2/dancetrack/val belum ada — jalankan --steps arrange dulu)")
    seqmap_mot = a.data_dir / "seqmaps" / "MOT20-train.txt"
    seqmap_dance = a.data_dir / "seqmaps" / "dancetrack-val.txt"
    write_seqmap(sorted(seqs_mot), seqmap_mot)
    if seqs_dance:
        write_seqmap(sorted(seqs_dance), seqmap_dance)

    all_rows = []
    for ds_key, gt, trk_root, seqmap, split in [
        # Layout datar: SKIP_SPLIT_FOL=True (hardcoded di run_eval) + GT_FOLDER = folder sekuens.
        # TrackEval 1.3.0 membangun gt_fol = GT_FOLDER + "{BENCHMARK}-{SPLIT}" kalau skip=False
        # (mis. "MOT20-train"), jadi layout datar menghindari folder tambahan yang tidak ada.
        ("mot20", a.data_dir / "mot20" / "train", trackers_root / "mot20", seqmap_mot, "train"),
        ("dance", a.data_dir / "dancetrack" / "val", trackers_root / "dance", seqmap_dance, "val"),
    ]:
        if ds_key == "dance" and not seqs_dance:
            print("   (skip eval dance: GT val belum tersedia)")
            continue
        print(f"   eval {ds_key} ...")
        out = run_eval(gt, trk_root, "ocsort", seqmap, split)
        rows = extract(out)
        for row in rows:
            row["benchmark"] = "MOT20" if ds_key == "mot20" else "DanceTrack"
        all_rows += rows
    df = pd.DataFrame(all_rows)
    df.to_csv(a.exp_dir / "eval_results.csv", index=False)
    print("\n   eval_results.csv:", a.exp_dir / "eval_results.csv")
    print(df.to_string(index=False))


# ---------------------------------------------------------------- main
def main() -> int:
    a = parse_args()
    a.data_dir = a.data_dir or a.repo_root / "data" / "s2"
    a.exp_dir = a.exp_dir or a.repo_root / "experiments" / "s2_tracker"
    a.ext_dir = a.ext_dir or a.repo_root / "external"
    a.data_dir.mkdir(parents=True, exist_ok=True)
    a.exp_dir.mkdir(parents=True, exist_ok=True)

    steps = [s.strip() for s in a.steps.split(",") if s.strip()]
    t0 = time.time()
    for s in steps:
        fn = {"data": step_data, "arrange": step_arrange,
              "detect": step_detect, "track": step_track, "eval": step_eval}.get(s)
        if fn is None:
            print(f"!! langkah tak dikenal: {s}"); return 1
        fn(a)
    print(f"\nSELESAI dalam {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
