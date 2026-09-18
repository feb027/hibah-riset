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

  # 3. Buat SATU paragraf acuan, ulangi sampai suaranya cocok
  python scripts/video/render_narasi.py naskah-tts.txt --out acuan --only 1 \
      --voice-desc "(Pria muda, suara tenang, tempo agak cepat)"

  # 4. Render semua paragraf dengan suara terkunci dari acuan itu
  python scripts/video/render_narasi.py naskah-tts.txt --out out \
      --reference-wav acuan/narasi_01.wav

  # 5. Render ulang satu paragraf saja
  python scripts/video/render_narasi.py naskah-tts.txt --out out \
      --reference-wav acuan/narasi_01.wav --only 4 --force
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


def render_voxcpm(items: list[tuple[int, str]], args, out: Path) -> None:
    import torch
    from voxcpm import VoxCPM
    import soundfile as sf

    # Mode suara. Voice Design dari teks TIDAK mengunci suara antar pemanggilan
    # (dokumentasi resmi: "a bit like hiring a new voice actor each time"), jadi
    # untuk narasi banyak paragraf wajib memakai audio referensi.
    gen_kwargs = {}
    if args.prompt_wav:
        gen_kwargs["prompt_wav_path"] = args.prompt_wav
        gen_kwargs["prompt_text"] = args.prompt_text
        if args.reference_wav:
            gen_kwargs["reference_wav_path"] = args.reference_wav
    elif args.reference_wav:
        gen_kwargs["reference_wav_path"] = args.reference_wav

    print("memuat openbmb/VoxCPM2 ...", flush=True)
    # optimize=False secara default: torch.compile justru 10-20x lebih lambat untuk
    # pemakaian sekali-sekali, dan di Tesla T4 kompilasi bfloat16 dilewati (tanpa efek).
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False,
                                   optimize=args.optimize)

    # generate() versi 2.0.3 tidak punya parameter seed; determinisme diatur lewat
    # torch.manual_seed sebelum tiap paragraf.
    for nomor, teks in items:
        target = out / f"narasi_{nomor:02d}.wav"
        if target.exists() and not args.force:
            print(f"[{nomor}] lewati (sudah ada): {target.name}")
            continue
        teks = f"{args.voice_desc}{teks}" if args.voice_desc else teks
        print(f"[{nomor}] render: {target.name}", flush=True)
        torch.manual_seed(args.seed)
        wav = model.generate(
            text=teks,
            cfg_value=args.cfg,
            inference_timesteps=args.steps,
            **gen_kwargs,
        )
        sf.write(target, wav, model.tts_model.sample_rate)


def render_edge(items: list[tuple[int, str]], args, out: Path) -> None:
    if not shutil.which("edge-tts"):
        sys.exit("edge-tts tidak ditemukan. Pasang dulu: pipx install edge-tts")

    for nomor, teks in items:
        target = out / f"narasi_{nomor:02d}.mp3"
        if target.exists() and not args.force:
            print(f"[{nomor}] lewati (sudah ada): {target.name}")
            continue
        print(f"[{nomor}] render: {target.name}", flush=True)
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
                    help="kontrol gaya/deskripsi suara, disisipkan di awal tiap paragraf "
                         "(mode voice design atau kloning referensi)")
    ap.add_argument("--reference-wav", type=Path,
                    help="audio acuan untuk mengunci timbre suara (WAJIB untuk narasi banyak paragraf)")
    ap.add_argument("--prompt-wav", type=Path,
                    help="audio acuan mode kloning hi-fi; butuh --prompt-text")
    ap.add_argument("--prompt-text",
                    help="transkrip persis dari --prompt-wav")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--optimize", action="store_true",
                    help="aktifkan torch.compile VoxCPM (default mati: lebih lambat untuk sekali jalan)")
    ap.add_argument("--cfg", type=float, default=2.0)
    ap.add_argument("--steps", type=int, default=10)
    ap.add_argument("--start", type=int, default=1,
                    help="mulai dari paragraf ke-N sampai paragraf terakhir")
    ap.add_argument("--only", type=int,
                    help="render HANYA paragraf ke-N (untuk membuat audio acuan)")
    ap.add_argument("--force", action="store_true", help="timpa hasil yang sudah ada")
    ap.add_argument("--dry-run", action="store_true", help="cetak rencana saja")
    args = ap.parse_args()

    if not args.naskah.is_file():
        sys.exit(f"naskah tidak ditemukan: {args.naskah}")
    for label, p in (("--reference-wav", args.reference_wav),
                     ("--prompt-wav", args.prompt_wav)):
        if p and not p.is_file():
            sys.exit(f"{label} tidak ditemukan: {p}")
    if args.prompt_wav and not args.prompt_text:
        sys.exit("--prompt-wav butuh --prompt-text (transkrip persis audio itu)")
    if args.prompt_wav and args.voice_desc:
        sys.exit("--voice-desc tidak bisa dipakai bersama --prompt-wav/--prompt-text")

    semua = baca_paragraf(args.naskah)
    if not semua:
        sys.exit("naskah kosong: tidak ada paragraf yang terbaca")
    n = len(semua)
    if args.only is not None and args.start != 1:
        sys.exit("--only dan --start tidak bisa dipakai bersamaan")
    if args.only is not None:
        if not 1 <= args.only <= n:
            sys.exit(f"--only di luar rentang 1..{n}")
        items = [(args.only, semua[args.only - 1])]
    else:
        if not 1 <= args.start <= n:
            sys.exit(f"--start di luar rentang 1..{n}")
        items = [(k, semua[k - 1]) for k in range(args.start, n + 1)]

    total_kata = sum(len(t.split()) for _, t in items)
    ext = EXT[args.engine]
    args.out.mkdir(parents=True, exist_ok=True)

    print(f"naskah   : {args.naskah}")
    print(f"paragraf : {len(items)} dari {n}"
          + (f" (hanya nomor {items[0][0]})" if args.only is not None
             else f" (mulai nomor {args.start})"))
    print(f"kata     : {total_kata}  (perkiraan {total_kata / 140:.1f} menit pada 140 kata/menit)")
    print(f"mesin    : {args.engine}"
          + (f" / {args.voice}" if args.engine == "edge" else ""))
    if args.engine == "voxcpm":
        if args.prompt_wav:
            print("suara    : kloning hi-fi dari " + str(args.prompt_wav))
        elif args.reference_wav:
            print("suara    : kloning dari referensi " + str(args.reference_wav) + " (terkunci)")
        else:
            print("suara    : voice design dari teks "
                  "PERINGATAN: tanpa --reference-wav, tiap paragraf jadi suara berbeda")
    print(f"keluaran : {args.out}/narasi_NN{ext}")

    if args.dry_run:
        print("\n--dry-run, tidak ada model yang dimuat.\n")
        for nomor, teks in items:
            nama = f"narasi_{nomor:02d}{ext}"
            ada = " (sudah ada)" if (args.out / nama).exists() and not args.force else ""
            print(f"  {nama}{ada}  {teks[:70]}{'...' if len(teks) > 70 else ''}")
        return 0

    if args.engine == "voxcpm":
        render_voxcpm(items, args, args.out)
    else:
        render_edge(items, args, args.out)

    print(f"\nselesai. {len(items)} paragraf di {args.out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
