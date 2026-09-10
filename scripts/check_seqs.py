import csv

rows = list(csv.DictReader(open('experiments/s2_tracker/trackeval_trackers/mot20/deepocsort/pedestrian_detailed.csv')))
print('MOT20 deepocsort seqs:', sorted(r['seq'] for r in rows))

rows = list(csv.DictReader(open('experiments/s2_tracker/trackeval_trackers/dance/deepocsort/pedestrian_detailed.csv')))
print('dance deepocsort n seq:', len(rows), sorted(r['seq'] for r in rows)[:30])
