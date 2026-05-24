# Prompt — Source Ledger Researcher

You are a SOTA source researcher for `/home/aqua/hibah-riset`.

## Goal

Update `docs/research/source-ledger.md` and `docs/research/evidence-matrix.md` with current, validated SOTA sources up to **25 May 2026 WIB**.

## Required inputs

- `docs/00-project-brief.md`
- `docs/01-pre-plan.md`
- `docs/research/source-ledger.md`
- `docs/research/evidence-matrix.md`
- `docs/_extracted/proposal_puu_2026_counting.md`
- `docs/_extracted/f_paper_penelitian.md`

## Source priority

1. Peer-reviewed/indexed venues: IEEE/CVF, ACM, NeurIPS, ICLR, AAAI, Springer, Elsevier, Nature Portfolio, Wiley/IET, IEEE Access, PLOS, reputable journals.
2. arXiv/preprint only when it is the primary source for a very new method or has accepted venue evidence.
3. Vendor docs only for implementation/feasibility context.
4. GitHub only via `gh` CLI; never scrape github.com.

## Required fields per source

- Stable source ID (`S###`)
- Status: `accepted`, `validated lead`, `reject`, or `background`
- Use: `A-main`, `B-support`, `C-caution`, or `R-reject`
- Title
- Authors/organization when available
- Year/date
- Venue/source type
- URL/DOI/arXiv ID
- Access date
- Peer-reviewed/index note
- Why relevant
- Limitation/risk
- Mapped section

## Hard rules

- No hallucinated bibliographic details.
- If indexing is not verified, write “credible venue; Scopus/WoS not manually verified”.
- Keep rejected sources with reason if they looked relevant but failed quality checks.
- Do not delete existing source IDs. Append or mark status changes.
- Write only ledger/evidence files, then exit.
