import csv

# laporan B: OC-SORT MOT20 HOTA 36.51 - cek COMBINED vs mean
for trk in ('ocsort', 'diffmot', 'lighttrack', 'deepocsort'):
    path = f'experiments/s2_tracker/trackeval_trackers/mot20/{trk}/pedestrian_detailed.csv'
    rows = list(csv.DictReader(open(path)))
    comb = [r for r in rows if r['seq'] == 'COMBINED']
    per = [r for r in rows if r['seq'] != 'COMBINED']
    if comb:
        print(trk, 'COMBINED HOTA', float(comb[0]['HOTA(0)'])*100, 'MOTA', float(comb[0]['MOTA'])*100, 'IDF1', float(comb[0]['IDF1'])*100)
    if per:
        n = len(per)
        print(trk, 'mean%d HOTA %.2f MOTA %.2f IDF1 %.2f' % (n, sum(float(r['HOTA(0)']) for r in per)/n*100, sum(float(r['MOTA']) for r in per)/n*100, sum(float(r['IDF1']) for r in per)/n*100))
