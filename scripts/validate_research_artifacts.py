#!/usr/bin/env python3
"""Lightweight validation for hibah-riset research artifacts."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'AGENTS.md',
    'docs/00-project-brief.md',
    'docs/01-pre-plan.md',
    'docs/PROGRESS.md',
    'docs/_extracted/manifest.json',
    'docs/research/source-ledger.md',
    'docs/research/evidence-matrix.md',
    'docs/outlines/pekerjaan-terkait-outline.md',
    'docs/drafts/pekerjaan-terkait.md',
    'docs/drafts/pendahuluan.md',
]

errors = []
for rel in REQUIRED:
    if not (ROOT / rel).exists():
        errors.append(f'missing required file: {rel}')

for rel in ['docs/drafts/pekerjaan-terkait.md', 'docs/drafts/pendahuluan.md', 'docs/research/source-ledger.md']:
    p = ROOT / rel
    if p.exists():
        text = p.read_text(encoding='utf-8', errors='replace')
        bad = ['{Formatting Citation}', 'Field Code Changed']
        for token in bad:
            if token in text:
                errors.append(f'{rel} contains extraction/Word artifact token: {token}')

ledger = ROOT / 'docs/research/source-ledger.md'
if ledger.exists():
    text = ledger.read_text(encoding='utf-8', errors='replace')
    rows = [ln for ln in text.splitlines() if re.match(r'\| S\d+', ln)]
    if len(rows) < 10:
        errors.append(f'source ledger too small: {len(rows)} source rows')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('VALIDATION PASSED')
