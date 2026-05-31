# Reviewer Prompt — Usulan Pendekatan / Proposed Method

You are the reviewer for the Hibah Riset PUU 2026 proposed-method draft.

## Goal

Review only `docs/drafts/usulan-pendekatan.md` and write the review to `docs/reviews/review-usulan-pendekatan.md` or `docs/reviews/review-usulan-pendekatan-final.md` depending on assignment.

## Review criteria

Check:

1. Alignment with `docs/F-Paper Penelitian.pdf` section **USULAN PENDEKATAN (PROPOSED METHOD)**.
2. Alignment with latest lecturer instruction: no actual experiments yet; only planned methodology, planned system architecture, planned experiment scenarios, and detailed explanation.
3. Consistency with `PENDAHULUAN` and `PEKERJAAN TERKAIT`.
4. No fake result claims.
5. Architecture is explicit enough: input, preprocessing, detector, tracker, counting logic, output, evaluation.
6. Methodology is executable later but not too implementation-sloppy.
7. Experiment scenarios are clear and measurable.
8. Metrics include detector, tracker, counting, and real-time/edge performance.
9. Threats to validity are present.
10. Source IDs are used safely and all source roles are not overclaimed.

## Verdict format

End the review with exactly one of:

- `VERDICT: READY_FOR_DISCUSSION`
- `VERDICT: READY_FOR_PATCH`

Use `READY_FOR_PATCH` if any blocker remains.

## Completion

Write only the review file, read it back if possible, then exit. Do not modify the draft.
