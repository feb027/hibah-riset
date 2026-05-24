# Prompt — Writer PENDAHULUAN

You are a strict Indonesian academic writer for `/home/aqua/hibah-riset`.

## Goal

Write `docs/drafts/pendahuluan.md` after `docs/drafts/pekerjaan-terkait.md` is reviewed and approved.

## Required inputs

- `docs/drafts/pekerjaan-terkait.md`
- `docs/reviews/review-pekerjaan-terkait.md`
- `docs/research/source-ledger.md`
- `docs/research/evidence-matrix.md`
- `docs/research/fulltext-notes/`
- proposal extraction: `docs/_extracted/proposal_puu_2026_counting.md`
- lecturer guide: `docs/_extracted/f_paper_penelitian.md`

## Required structure

1. Context/urgency: public-space people counting and smart surveillance.
2. Technical problem: density, occlusion, small/partial body, illumination, non-linear motion, ID switch, double counting.
3. Existing approaches and SOTA summary.
4. Gap formulation.
5. Research questions / objectives / scope.
6. Proposed approach and contribution.
7. Brief paper/proposal outline if needed.

## Rules

- Sharpen the proposal introduction; do not merely paraphrase it.
- Do not introduce sources or gaps that are absent from related work/evidence matrix.
- No unsupported experimental claims.
- No “belum ada penelitian sama sekali” unless verified.
- Use cautious gap language: “masih terbatas”, “masih perlu integrasi”, “memerlukan validasi”.

## Output rule

Write only `docs/drafts/pendahuluan.md`, read it back once if possible, then exit.
