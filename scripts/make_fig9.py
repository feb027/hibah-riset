"""Figur tracking metrics 4 tracker x 2 benchmark (untuk 4.2) - jalankan dengan .venv-s2/bin/python."""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open('experiments/s2_tracker/eval_results.csv')))
trackers = ['ocsort', 'deepocsort', 'diffmot', 'lighttrack']
tlabels = {'ocsort': 'OC-SORT', 'deepocsort': 'Deep-OC-SORT', 'diffmot': 'DiffMOT', 'lighttrack': 'LightTrack'}
metrics = [('HOTA', 'HOTA'), ('MOTA', 'MOTA'), ('IDF1', 'IDF1')]
benchmarks = [('MOT20', 'MOT20'), ('DanceTrack', 'DanceTrack')]

data = {(r['tracker'], r['benchmark']): {m: float(r[col]) for m, col in metrics} for r in rows}

fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
colors = ['#4472c4', '#ed7d31', '#70ad47', '#c00000']
width = 0.2
for ax, (bench, blabel) in zip(axes, benchmarks):
    for i, (t, tl) in enumerate([(t, tlabels[t]) for t in trackers]):
        vals = [data[(t, bench)][m] for m, _ in metrics]
        xs = [j + (i - 1.5) * width for j in range(3)]
        ax.bar(xs, vals, width, label=tl if bench == 'MOT20' else None, color=colors[i])
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.8, f'{v:.1f}'.replace('.', ','), ha='center', fontsize=7)
    ax.set_xticks(range(3))
    ax.set_xticklabels([m for m, _ in metrics], fontsize=9)
    ax.set_title(blabel, fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
axes[0].set_ylabel('Skor (0-100)', fontsize=9)
axes[0].legend(fontsize=8, loc='upper left')
plt.tight_layout()
plt.savefig('experiments/journal_figs/fig9_tracking_metrics.png', dpi=200)
plt.close()
print('OK fig9')
