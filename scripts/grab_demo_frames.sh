#!/bin/bash
# Screenshot frame demo tracking (OC-SORT vs DiffMOT vs GT) untuk figur kualitatif 4.2/4.3.
set -e
cd "$(dirname "$0")/.."
D=experiments/s2_tracker/demo
O=experiments/journal_figs
mkdir -p "$O"
# ambil frame di detik ke-10 (tengah klip, saat kerumunan padat)
ffmpeg -y -v error -ss 10 -i "$D/MOT20-02_f1-450_tracked.mp4" -frames:v 1 "$O/fig10a_ocsort.png"
ffmpeg -y -v error -ss 10 -i "$D/MOT20-02_f1-450_tracked_diffmot.mp4" -frames:v 1 "$O/fig10b_diffmot.png"
ffmpeg -y -v error -ss 10 -i "$D/MOT20-02_f1-450_gt.mp4" -frames:v 1 "$O/fig10c_gt.png"
echo OK
