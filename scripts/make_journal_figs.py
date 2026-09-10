"""Grafik Bab 4 (4.3/4.4/4.5) dari CSV eksperimen - jalankan dengan .venv-s2/bin/python."""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = 'experiments/journal_figs'
import os
os.makedirs(OUT, exist_ok=True)

def read_csv(path):
    return list(csv.DictReader(open(path)))

# ---- Fig 5: galat hitung per tracker (4.3, Tabel 6) ----
rows = read_csv('experiments/s3_counting/counting_metrics.csv')
trackers = []
mae = []
err = []
seen = set()
for r in rows:
    t = r['tracker']
    if t not in seen:
        seen.add(t)
        trackers.append(t)
        # rata-rata 29 sekuens per tracker
vals = {t: {'mae': [], 'err': []} for t in trackers}
for r in rows:
    vals[r['tracker']]['mae'].append(float(r['MAE']))
    vals[r['tracker']]['err'].append(float(r['Error_Pct']))
order = ['GroundTruth', 'diffmot', 'deepocsort', 'ocsort', 'lighttrack']
labels = {'GroundTruth': 'GT Track', 'diffmot': 'DiffMOT', 'deepocsort': 'Deep-OC-SORT', 'ocsort': 'OC-SORT', 'lighttrack': 'LightTrack'}
mae_m = [sum(vals[t]['mae'])/len(vals[t]['mae']) for t in order if vals[t]['mae']]
err_m = [sum(vals[t]['err'])/len(vals[t]['err']) for t in order if vals[t]['err']]
use = [t for t in order if vals[t]['mae']]

fig, ax = plt.subplots(figsize=(7, 3.6))
x = range(len(use))
w = 0.38
b1 = ax.bar([i - w/2 for i in x], mae_m, w, label='MAE (orang)', color='#4472c4')
b2 = ax.bar([i + w/2 for i in x], err_m, w, label='Galat (%)', color='#ed7d31')
for b in list(b1) + list(b2):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.5, f'{b.get_height():.1f}', ha='center', fontsize=8)
ax.set_xticks(list(x))
ax.set_xticklabels([labels[t] for t in use], fontsize=9)
ax.set_ylabel('Nilai')
ax.legend(fontsize=8)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(f'{OUT}/fig5_counting_error.png', dpi=200)
plt.close()

# ---- Fig 6: sensitivitas cooldown (4.4, Tabel 8) - galat% + MAE dua sumbu ----
rows = read_csv('experiments/s3_counting/sensitivity_cooldown.csv')
cd = {}
for r in rows:
    if r['tracker'] == 'deepocsort':
        cd[int(r['cooldown_frames'])] = (float(r['mae']), float(r['error_pct']), float(r['bias']))
cds = sorted(cd)
fig, ax1 = plt.subplots(figsize=(7, 3.6))
ax1.plot(cds, [cd[c][0] for c in cds], 'o-', color='#4472c4', label='MAE (orang)')
ax1.set_xlabel('Cooldown (frame)')
ax1.set_ylabel('MAE (orang)', color='#4472c4')
ax1.tick_params(axis='y', labelcolor='#4472c4')
ax2 = ax1.twinx()
ax2.plot(cds, [cd[c][1] for c in cds], 's--', color='#ed7d31', label='Galat (%)')
ax2.set_ylabel('Galat (%)', color='#ed7d31')
ax2.tick_params(axis='y', labelcolor='#ed7d31')
if 0 in cd:
    ax1.axvline(0, color='gray', linestyle=':', alpha=0.5)
    ax2.annotate('naive = 101,99%', xy=(0, cd[0][1]), xytext=(8, 88), fontsize=8, color='#555')
ax1.spines[['top']].set_visible(False)
ax2.spines[['top']].set_visible(False)
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.95), fontsize=8)
plt.tight_layout()
plt.savefig(f'{OUT}/fig6_cooldown_sensitivity.png', dpi=200)
plt.close()

# ---- Fig 7: sensitivitas confidence (4.4, Tabel 9) ----
rows = read_csv('experiments/s3_counting/sensitivity_confidence.csv')
conf = [float(r['conf_threshold']) for r in rows]
err = [float(r['error_pct']) for r in rows]
fps = [float(r['fps_throughput']) for r in rows]
fig, ax1 = plt.subplots(figsize=(7, 3.6))
ax1.plot(conf, err, 's-', color='#ed7d31', label='Galat (%)')
ax1.set_xlabel('Confidence threshold')
ax1.set_ylabel('Galat (%)', color='#ed7d31')
ax1.tick_params(axis='y', labelcolor='#ed7d31')
ax2 = ax1.twinx()
ax2.plot(conf, fps, '^--', color='#70ad47', label='Throughput (FPS)')
ax2.set_ylabel('Throughput (FPS)', color='#70ad47')
ax2.tick_params(axis='y', labelcolor='#70ad47')
ax1.axvspan(0.25, 0.30, alpha=0.15, color='green')
ax1.annotate('rentang operasional', xy=(0.275, 14), fontsize=8, ha='center', color='#375623')
ax1.spines[['top']].set_visible(False)
ax2.spines[['top']].set_visible(False)
fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=2, fontsize=8)
plt.tight_layout()
plt.savefig(f'{OUT}/fig7_conf_sensitivity.png', dpi=200)
plt.close()

# ---- Fig 8: latency breakdown stacked bar (4.5, Tabel 10-11) ----
rows = read_csv('experiments/s4_realtime/latency_breakdown.csv')
names = {'ocsort': 'OC-SORT (edge CPU)', 'deepocsort': 'Deep-OC-SORT (edge CPU)'}
stages = [('mean_preprocess_ms', 'Preprocessing', '#a5a5a5'), ('mean_detect_ms', 'Deteksi', '#4472c4'),
          ('mean_tracker_ms', 'Tracker+Re-ID', '#ed7d31'), ('mean_counter_ms', 'Counter', '#70ad47')]
fig, ax = plt.subplots(figsize=(7, 3.4))
for i, r in enumerate(rows):
    bottom = 0
    for col, lab, c in stages:
        v = float(r[col])
        ax.bar(i, v, bottom=bottom, label=lab if i == 0 else None, color=c, width=0.5)
        bottom += v
    ax.text(i, bottom + 2.5, f"{float(r['mean_total_latency_ms']):.1f} ms\n{float(r['effective_fps']):.1f} FPS".replace('.', ','), ha='center', fontsize=8)
gpu_total = 24.61
gpu_parts = [0.85, 14.20, 9.45, 0.11]
bottom = 0
for (col, lab, c), v in zip(stages, gpu_parts):
    ax.bar(2, v, bottom=bottom, color=c, width=0.5)
    bottom += v
ax.text(2.55, gpu_total - 6, f"24,61 ms\n40,6 FPS", ha='center', fontsize=8, color='#333')
ax.set_xticks([0, 1, 2])
ax.set_xticklabels([names.get(r['tracker'], 'Deep-OC-SORT (RTX 4090)') for r in rows] + ['Deep-OC-SORT (RTX 4090)'], fontsize=9)
ax.axhline(33.3, color='red', linestyle='--', linewidth=1)
ax.text(2.35, 34.5, 'anggaran real-time 33,3 ms', fontsize=8, color='red')
ax.set_ylabel('Latensi (ms)')
ax.legend(fontsize=8, loc='upper left')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(f'{OUT}/fig8_latency_breakdown.png', dpi=200)
plt.close()

print('OK - 4 figur dibuat di', OUT)
