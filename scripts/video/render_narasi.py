#!/usr/bin/env python3
"""Render narasi video dari satu file teks: satu paragraf -> satu WAV/MP3.

Alur: tulis naskah di satu file .txt, pisahkan paragraf dengan baris kosong,
lalu jalankan skrip ini. Hasilnya out/narasi_01.wav, narasi_02.wav, dan
seterusnya, siap disusun di editor video.

Contoh:
  # 1. Lihat rencana tanpa memuat model (jalan di mesin mana pun)
  python scripts/video/render_narasi.py naskah-tts.txt --dry-run

  # 2. Draft cepat, tanpa GPU
  python scripts/video/render_narasi.py naskah-tts.txt \
      --engine edge --voice id-ID-ArdiNeural --out out_draft

  # 3. Final dengan VoxCPM2 (butuh GPU)
  python scripts/video/render_narasi.py naskah-tts.txt \
      --voice-desc "(Pria muda, suara tenang, tempo sedang)"
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

EXT = {"voxcpm": ".wav", "edge": ".mp3"}


def baca_paragraf(path: Path) -> list[str]:
    """Pecah file jadi paragraf. Baris kosong = pemisah."""
    teks = path.read_text(encoding="utf-8")
    par = [p.strip() for p in teks.replace("\r\n", "\n").split("\n\n")]
    return [p for p in par if p]


def render_voxcpm(par: list[str], args, out: Path) -> None:
    import torch
    from voxcpm import VoxCPM
    import soundfile as sf

    print("memuat openbmb/VoxCPM2 ...", flush=True)
    # optimize=False secara default: torch.compile justru 10-20x lebih lambat untuk
    # pemakaian sekali-sekali, dan di Tesla T4 kompilasi bfloat16 dilewati (tanpa efek).
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False,
                                   optimize=args.optimize)

    # generate() versi 2.0.3 tidak punya parameter seed; determinisme diatur lewat
    # torch.manual_seed sebelum tiap paragraf.
    for i, teks in enumerate(par, 1):
        target = out / f"narasi_{i:02d}.wav"
        if target.exists() and not args.force:
            print(f"[{i}/{len(par)}] lewati (sudah ada): {target.name}")
            continue
        teks = f"{args.voice_desc}{teks}" if args.voice_desc else teks
        print(f"[{i}/{len(par)}] render: {target.name}", flush=True)
        torch.manual_seed(args.seed)
        wav = model.generate(
            text=teks,
            cfg_value=args.cfg,
            inference_timesteps=args.steps,
        )
        sf.write(target, wav, model.tts_model.sample_rate)


def render_edge(par: list[str], args, out: Path) -> None:
    if not shutil.which("edge-tts"):
        sys.exit("edge-tts tidak ditemukan. Pasang dulu: pipx install edge-tts")

    for i, teks in enumerate(par, 1):
        target = out / f"narasi_{i:02d}.mp3"
        if target.exists() and not args.force:
            print(f"[{i}/{len(par)}] lewati (sudah ada): {target.name}")
            continue
        print(f"[{i}/{len(par)}] render: {target.name}", flush=True)
        subprocess.run(
            ["edge-tts", "--voice", args.voice, "--rate", args.rate,
             "--text", teks, "--write-media", str(target)],
            check=True,
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("naskah", type=Path, help="file .txt naskah (versi fonetis)")
    ap.add_argument("--engine", choices=["voxcpm", "edge"], default="voxcpm")
    ap.add_argument("--out", type=Path, default=Path("out"), help="folder keluaran")
    ap.add_argument("--voice", default="id-ID-ArdiNeural", help="suara edge-tts")
    ap.add_argument("--rate", default="+0%", help="tempo edge-tts, mis. -10%%")
    ap.add_argument("--voice-desc", default="",
                    help="deskripsi suara VoxCPM2, ikut disisipkan di awal tiap paragraf")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--optimize", action="store_true",
                    help="aktifkan torch.compile VoxCPM (default mati: lebih lambat untuk sekali jalan)")
    ap.add_argument("--cfg", type=float, default=2.0)
    ap.add_argument("--steps", type=int, default=10)
    ap.add_argument("--start", type=int, default=1, help="mulai dari paragraf ke-N")
    ap.add_argument("--force", action="store_true", help="timpa hasil yang sudah ada")
    ap.add_argument("--dry-run", action="store_true", help="cetak rencana saja")
    args = ap.parse_args()

    if not args.naskah.is_file():
        sys.exit(f"naskah tidak ditemukan: {args.naskah}")

    par = baca_paragraf(args.naskah)
    if not par:
        sys.exit("naskah kosong: tidak ada paragraf yang terbaca")
    if not 1 <= args.start <= len(par):
        sys.exit(f"--start di luar rentang 1..{len(par)}")
    par = par[args.start - 1:]

    total_kata = sum(len(p.split()) for p in par)
    ext = EXT[args.engine]
    args.out.mkdir(parents=True, exist_ok=True)

    print(f"naskah   : {args.naskah}")
    print(f"paragraf : {len(par)} (mulai dari nomor {args.start})")
    print(f"kata     : {total_kata}  (perkiraan {total_kata / 140:.1f} menit pada 140 kata/menit)")
    print(f"mesin    : {args.engine}"
          + (f" / {args.voice}" if args.engine == "edge" else ""))
    print(f"keluaran : {args.out}/narasi_NN{ext}")

    if args.dry_run:
        print("\n--dry-run, tidak ada model yang dimuat.\n")
        for i, p in enumerate(par, args.start):
            nama = f"narasi_{i:02d}{ext}"
            ada = " (sudah ada)" if (args.out / nama).exists() and not args.force else ""
            print(f"  {nama}{ada}  {p[:70]}{'...' if len(p) > 70 else ''}")
        return 0

    if args.engine == "voxcpm":
        render_voxcpm(par, args, args.out)
    else:
        render_edge(par, args, args.out)

    print(f"\nselesai. {len(par)} paragraf di {args.out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
