#!/usr/bin/env bash
# Sweep final LightTrack: gate re-sweep di atas OCM (ma90_ea5) + ASW.
# Run: bash scripts/s2/run_sweep_final.sh   (dari root repo)
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

CKPT=out/phase3_fold1_v2/best.pt
[ -f "$CKPT" ] || { echo "CKPT tidak ada: $CKPT"; exit 1; }

# 1) gate sweep: score_min x appearance_w di atas OCM ma90_ea5
for cfg in "0.3 0.5" "0.2 0.5" "0.3 0.7"; do
  set -- $cfg; sm=$1; aw=$2
  D=experiments/s2_final/sm${sm}_aw${aw}
  echo "=== sm=$sm aw=$aw ==="
  python scripts/s2/run_lighttrack_mot.py --det-dir data/s2/mot20/det_mot/train \
    --out-dir "$D/lighttrack_results/mot20" --ckpt "$CKPT" --img-dir data/s2/mot20/train \
    --max-age 90 --emit-age 5 --score-min "$sm" --appearance-w "$aw" || exit 1
  python scripts/s2/run_lighttrack_mot.py --det-dir data/s2/dancetrack/det_mot/val \
    --out-dir "$D/lighttrack_results/dancetrack" --ckpt "$CKPT" --img-dir data/s2/dancetrack/val \
    --max-age 90 --emit-age 5 --score-min "$sm" --appearance-w "$aw" || exit 1
  python scripts/s2/run_skenario_b_ocsort.py --steps eval --tracker lighttrack --exp-dir "$D" || exit 1
done

# 2) ASW di atas OCM (gate default 0.3/0.5)
D=experiments/s2_final/asw
echo "=== ASW ==="
python scripts/s2/run_lighttrack_mot.py --det-dir data/s2/mot20/det_mot/train \
  --out-dir "$D/lighttrack_results/mot20" --ckpt "$CKPT" --img-dir data/s2/mot20/train \
  --max-age 90 --emit-age 5 --asw || exit 1
python scripts/s2/run_lighttrack_mot.py --det-dir data/s2/dancetrack/det_mot/val \
  --out-dir "$D/lighttrack_results/dancetrack" --ckpt "$CKPT" --img-dir data/s2/dancetrack/val \
  --max-age 90 --emit-age 5 --asw || exit 1
python scripts/s2/run_skenario_b_ocsort.py --steps eval --tracker lighttrack --exp-dir "$D" || exit 1

echo "=== RANGKUMAN ==="
for f in experiments/s2_final/*/eval_results.csv; do echo "-- ${f%/eval_results.csv}"; cat "$f"; done
