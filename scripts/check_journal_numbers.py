import re

draft = open('docs/journal/4.1-object-detection-results.md').read()
src = open('docs/reports/laporan-skenario-a-finetuning-yolo.md').read()
ledger = open('docs/research/source-ledger.md').read()

draft_norm = draft.replace(',', '.')
src_norm = src.replace(',', '.')
nums = re.findall(r'\d+\.\d+|\d+%', draft_norm)
missing = sorted({n for n in nums if n.rstrip('%') not in src_norm})
print("Angka draft yang TIDAK ditemukan di sumber:", missing if missing else "SEMUA KETEMU")

sids = sorted(set(re.findall(r'S\d{3}', draft)))
for s in sids:
    print(f"  {s}:", "ADA di ledger" if s in ledger else "TIDAK ADA di ledger !")
