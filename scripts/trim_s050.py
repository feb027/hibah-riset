"""Buang entri S050 duplikat dari references.bib (S014 sudah ada, DOI sama)."""
content = open('references/references.bib').read()
idx = content.find('% S050')
assert idx > 0, 'S050 block not found'
open('references/references.bib', 'w').write(content[:idx].rstrip() + '\n')
print('removed S050 block; bib now has', open('references/references.bib').read().count('@'), 'entries')
