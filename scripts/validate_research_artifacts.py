#!/usr/bin/env python3
"""Validation gate for hibah-riset research artifacts."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    'AGENTS.md',
    'README.md',
    'docs/00-project-brief.md',
    'docs/01-pre-plan.md',
    'docs/PROGRESS.md',
    'docs/_extracted/manifest.json',
    'docs/research/source-ledger.md',
    'docs/research/source-ledger-ringkasan-indonesia.md',
    'docs/research/papers/manifest.md',
    'docs/research/evidence-matrix.md',
    'docs/research/phase1-source-notes.md',
    'docs/research/fulltext-notes/README.md',
    'docs/outlines/pekerjaan-terkait-outline.md',
    'docs/drafts/pekerjaan-terkait.md',
    'docs/drafts/pendahuluan.md',
    'docs/reviews/review-source-ledger.md',
    'docs/reviews/review-pekerjaan-terkait-outline.md',
    'docs/reviews/review-fulltext-notes.md',
    'docs/reviews/review-pekerjaan-terkait.md',
    'docs/reviews/review-pekerjaan-terkait-patch.md',
    'docs/reviews/review-pendahuluan.md',
    'docs/reviews/review-pendahuluan-patch.md',
    'docs/reviews/review-handoff-package.md',
    'docs/handoff/lecturer-handoff-2026-05-25.md',
    'docs/handoff/draft-sections-clean.md',
    'references/README.md',
    'references/source-id-map.md',
    'references/references.bib',
    'prompts/researcher-source-ledger.md',
    'prompts/fulltext-reader.md',
    'prompts/writer-pekerjaan-terkait.md',
    'prompts/writer-pendahuluan.md',
    'prompts/reviewer-brutal.md',
    'prompts/citation-auditor.md',
    'prompts/final-verifier.md',
]

BAD_TOKENS = ['{Formatting Citation}', 'Field Code Changed']
errors: list[str] = []
warnings: list[str] = []

def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8', errors='replace')

for rel in REQUIRED:
    if not (ROOT / rel).exists():
        errors.append(f'missing required file: {rel}')

for rel in [
    'docs/drafts/pekerjaan-terkait.md',
    'docs/drafts/pendahuluan.md',
    'docs/research/source-ledger.md',
    'docs/research/evidence-matrix.md',
    'docs/outlines/pekerjaan-terkait-outline.md',
]:
    p = ROOT / rel
    if p.exists():
        text = p.read_text(encoding='utf-8', errors='replace')
        for token in BAD_TOKENS:
            if token in text:
                errors.append(f'{rel} contains extraction/Word artifact token: {token}')

ledger_path = ROOT / 'docs/research/source-ledger.md'
if ledger_path.exists():
    ledger = read('docs/research/source-ledger.md')
    rows = [ln for ln in ledger.splitlines() if re.match(r'\| S\d+', ln)]
    if len(rows) < 20:
        errors.append(f'source ledger too small: {len(rows)} source rows; expected >=20')
    a_main = [r for r in rows if '| A-main |' in r]
    if len(a_main) < 15:
        errors.append(f'A-main source count too small: {len(a_main)}; expected >=15')
    recent = [r for r in rows if re.search(r'\| 202[4-6](?:\D|$)', r)]
    if len(rows) and len(recent) / len(rows) < 0.70:
        errors.append(f'recent source ratio too low: {len(recent)}/{len(rows)}; expected >=70%')
    if 'YOLO26' in ledger and 'C-caution' not in ledger:
        errors.append('YOLO26 appears in ledger but caution classification is missing')

bib_path = ROOT / 'references/references.bib'
if bib_path.exists():
    bib = read('references/references.bib')
    entries = re.findall(r'^@\w+\{', bib, flags=re.M)
    if len(entries) < 20:
        errors.append(f'references.bib has too few entries: {len(entries)}; expected >=20')
    for sid in ['S001', 'S002', 'S003', 'S004', 'S010', 'S011', 'S018', 'S021', 'S024', 'S025', 'S027', 'S028']:
        if f'{{{sid},' not in bib:
            warnings.append(f'priority source {sid} not found as a BibTeX key')
    for draft_rel in ['docs/drafts/pekerjaan-terkait.md', 'docs/drafts/pendahuluan.md']:
        draft_path = ROOT / draft_rel
        if draft_path.exists():
            cited_ids = sorted(set(re.findall(r'\[S(\d{3})\]', draft_path.read_text(encoding='utf-8', errors='replace'))))
            missing = [f'S{sid}' for sid in cited_ids if f'{{S{sid},' not in bib]
            if missing:
                errors.append(f'{draft_rel} cites IDs missing from references.bib: {", ".join(missing)}')

notes_dir = ROOT / 'docs/research/fulltext-notes'
PRIORITY_NOTE_IDS = ['S001', 'S002', 'S003', 'S004', 'S010', 'S011', 'S018', 'S021', 'S024', 'S025', 'S027', 'S028']
REQUIRED_NOTE_SECTIONS = [
    '## Source identity',
    '## Why this source matters',
    '## Problem addressed',
    '## Method summary',
    '## Dataset / evaluation protocol',
    '## Metrics reported',
    '## Findings safe to cite',
    '## Limitations stated by authors',
    '## Limitations inferred for this project',
    '## Exact claims allowed in draft',
    '## Claims NOT allowed',
    '## Mapped sections',
    '## Notes for citation auditor',
]
if notes_dir.exists():
    notes = [p for p in notes_dir.glob('S*.md')]
    if len(notes) < 10:
        errors.append(f'fulltext note templates too few: {len(notes)}; expected >=10')
    for sid in PRIORITY_NOTE_IDS:
        matches = list(notes_dir.glob(f'{sid}*.md'))
        if not matches:
            errors.append(f'missing priority fulltext note for {sid}')
            continue
        text = matches[0].read_text(encoding='utf-8', errors='replace')
        for section in REQUIRED_NOTE_SECTIONS:
            if section not in text:
                errors.append(f'{matches[0].relative_to(ROOT)} missing section: {section}')
        for token in ['TODO', 'S###', 'Short Title']:
            if token in text:
                errors.append(f'{matches[0].relative_to(ROOT)} still contains template marker: {token}')
else:
    errors.append('missing docs/research/fulltext-notes directory')

summary_path = ROOT / 'docs/research/source-ledger-ringkasan-indonesia.md'
if summary_path.exists():
    summary = summary_path.read_text(encoding='utf-8', errors='replace')
    summary_ids = sorted(set(re.findall(r'(?m)^##\s+(S\d{3})\b', summary)))
    expected_ids = [f'S{i:03d}' for i in range(1, 39)]
    missing_summary = [sid for sid in expected_ids if sid not in summary_ids]
    if missing_summary:
        errors.append(f'Indonesian source summary missing IDs: {", ".join(missing_summary)}')
    required_fields = [
        '**Judul:**',
        '**Penulis:**',
        '**Jurnal/Konferensi:**',
        '**URL:**',
        '**Permasalahan:**',
        '**Kontribusi:**',
        '**Metode/solusi:**',
        '**Hasil utama:**',
        '**Batasan:**',
        '**Relevansi dengan penelitian ini:**',
    ]
    for sid in expected_ids:
        m = re.search(rf'(?ms)^##\s+{sid}\b(.*?)(?=^##\s+S\d{{3}}\b|\Z)', summary)
        if not m:
            continue
        block = m.group(1)
        for field in required_fields:
            if field not in block:
                errors.append(f'Indonesian source summary {sid} missing field: {field}')

paper_text_dir = ROOT / 'docs/research/paper-text'
if paper_text_dir.exists():
    text_ids = sorted({p.name[:4] for p in paper_text_dir.glob('S*.md')})
    expected_ids = [f'S{i:03d}' for i in range(1, 39)]
    missing_text = [sid for sid in expected_ids if sid not in text_ids]
    if missing_text:
        errors.append(f'paper-text extraction missing IDs: {", ".join(missing_text)}')
else:
    errors.append('missing docs/research/paper-text directory')

reviews = {
    'docs/reviews/review-source-ledger.md': ['READY_FOR_OUTLINE'],
    'docs/reviews/review-pekerjaan-terkait-outline.md': ['READY_FOR_DRAFT'],
    'docs/reviews/review-fulltext-notes.md': ['READY_FOR_DRAFT'],
    'docs/reviews/review-pekerjaan-terkait.md': ['READY_FOR_PATCH', 'READY_FOR_NEXT_PHASE'],
    'docs/reviews/review-pekerjaan-terkait-patch.md': ['READY_FOR_NEXT_PHASE'],
    'docs/reviews/review-pendahuluan.md': ['READY_FOR_PATCH', 'READY_FOR_NEXT_PHASE'],
    'docs/reviews/review-pendahuluan-patch.md': ['READY_FOR_NEXT_PHASE'],
    'docs/reviews/review-handoff-package.md': ['READY_FOR_DELIVERY'],
}
for rel, accepted in reviews.items():
    p = ROOT / rel
    if p.exists():
        text = p.read_text(encoding='utf-8', errors='replace')
        if not any(v in text for v in accepted):
            errors.append(f'{rel} missing accepted verdict {accepted}')

outline_path = ROOT / 'docs/outlines/pekerjaan-terkait-outline.md'
if outline_path.exists():
    outline = read('docs/outlines/pekerjaan-terkait-outline.md')
    required_terms = [
        'People counting',
        'NMS-free',
        'Multi-object tracking',
        'Diffusion-based MOT',
        'Counting logic',
        'Dataset',
        'Sintesis gap',
        'Anti-overclaim',
    ]
    for term in required_terms:
        if term.lower() not in outline.lower():
            errors.append(f'outline missing required concept: {term}')

if warnings:
    print('VALIDATION WARNINGS')
    for w in warnings:
        print('-', w)

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)

print('VALIDATION PASSED')
