import csv

for bench, trk in (('mot20', 'deepocsort'), ('dance', 'deepocsort')):
    path = f'experiments/s2_tracker/trackeval_trackers/{bench}/{trk}/pedestrian_detailed.csv'
    rows = list(csv.DictReader(open(path)))
    rows = [r for r in rows if r['seq'] != 'COMBINED']
    n = len(rows)
    out = {}
    for key in ('HOTA(0)', 'MOTA', 'IDF1', 'IDSW', 'Frag'):
        vals = [float(r[key]) for r in rows]
        out[key] = sum(vals) / n
    print(f"{bench},{trk},HOTA {out['HOTA(0)']*100:.2f},MOTA {out['MOTA']*100:.2f},IDF1 {out['IDF1']*100:.2f},IDSW {out['IDSW']:.0f},Frag {out['Frag']:.0f},{n} seq")
