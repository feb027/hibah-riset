# References

This folder stores citation infrastructure for the PUU 2026 SOTA manuscript.

## Files

- `references.bib` — machine-readable bibliography generated from DOI/arXiv metadata where possible.
- `source-id-map.md` — mapping between `S###` source IDs in `docs/research/source-ledger.md` and citation keys/URLs.

## Rules

- Do not cite directly from `source-ledger.md` in final prose. Use `references.bib` and verify the specific claim from full text first.
- Keep source IDs stable. If a source is rejected later, mark it in the ledger; do not silently reuse the same ID for a different source.
- Vendor/preprint sources can appear in the bibliography, but final novelty claims must be anchored to peer-reviewed sources when possible.
