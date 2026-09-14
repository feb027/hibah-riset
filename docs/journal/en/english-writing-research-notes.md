# English Journal Writing — Research Notes (Sep 2026)

Notes behind the EN translation of the RANCAGE manuscript. Purpose: write English that reads like a
non-native researcher who knows the field, not like a model. Sources listed at the bottom with access date.

---

## 1. What actually makes non-native academic English read "translated"

Grammar is almost never the tell. Four patterns do nearly all the damage
([TextPulse, Aug 2026](https://textpulse.ai/blog/how-to-sound-natural-in-english-academic-writing)):

1. **Wrong collocations** — grammatically fine, not what a reader in the field expects.
   `conducted/ran a study, an experiment, a survey, an analysis` · `drew a conclusion, a comparison, a distinction`
   · `posed a question` · `raised a concern` · `reached a consensus` · `yielded/produced a result`.
   → Do NOT write "made an analysis" (that is the classic giveaway).
2. **Hedging at the wrong strength** — overclaiming (`proves`, `demonstrates conclusively`) from a design that
   cannot support it, or stacking hedges (`may perhaps possibly suggest`). One calibrated hedge beats four.
3. **Uniform sentence length** — a paragraph where every sentence is 18–25 words reads flat. Mark runs of three
   similarly sized sentences and break one.
4. **Over-nominalisation** — turning verbs into `-tion/-ment/-ance` nouns.
   `The implementation of the revised protocol resulted in a reduction in contamination events`
   → `Implementing the revised protocol reduced contamination events`.

## 2. What makes academic writing look AI-generated (and the fix)

Same class of problem, different framing ([TextSight, Jul 2026](https://www.textsight.ai/blog/research-paper-doesnt-read-ai/);
[Alfred Scholar, 2026](https://www.alfredscholar.com/blog/the-ai-slop-problem-scholarly-voice-2026)):

- **Generic academic vocabulary** — `significant, demonstrates, suggests, evidence indicates, the results show,
  robust, comprehensive, leverage, pivotal, underscores`. Reviewers now read these as slop markers. Use
  discipline-specific terms instead: HOTA, IDF1, IDSW, fragmentation, amodal fbox, observation-centric,
  appearance embedding, cooldown debounce, tail latency.
- **One citation-integration pattern** — AI defaults to `According to X (year)` / `[Claim] ([X], year)`. Vary:
  author-prominent, finding-prominent, grouped synthesis. (Limited here by JESTEC's numbered style, but the
  sentence shape around `[4]` can still vary.)
- **Summary instead of interpretation** — one genuinely interpretive sentence per literature paragraph. AI
  summarises well and interprets badly; that gap is the human tell.
- **Paragraph template** — claim → evidence → explanation → transition, every time, all the same length. Vary it.
- **Emphasis never shifts** — AI holds the same confidence level throughout. Lean into the central finding,
  hedge the edge cases.
- **Hollow transitions** — `Moreover, Furthermore, Additionally, It is important to note that`. Delete; put back
  only where the logic would not survive without them.
- **AI triplets** — `robust, scalable, and transformative`. Cap tricolons at roughly one per 500 words.
- **No grounded specifics** — a real instrument model, a real configuration value, a real failure. This manuscript
  is unusually easy here: keep every number, every configuration (CD = 30, threshold 0.30, 640×640, RTX 4090,
  29 sequences, 4,370 images, 103,115 boxes).

## 3. Indonesian → English translation pitfalls for this text

From corpus studies of ID→EN academic translation
([Retorika, 2022](https://doi.org/10.55637/jr.8.2.5416.206-213);
[UNIMED/Language Literacy, 2023](https://jurnal.uisu.ac.id/index.php/languageliteracy/article/download/10252/pdf)):

| Error type | Frequency | Applied rule here |
| --- | --- | --- |
| **Literalness** | ~31% (most common) | Translate the *claim*, not the word order. `Penelitian ini tidak mengklaim ... melainkan berfokus pada` → English sentence built around one main clause, not a comma splice. |
| **Usage** (articles, prepositions, collocations) | ~22% | Indonesian has no articles. Add `the/a` deliberately: "the counting logic", "a state machine". `konsisten terhadap` → "consistent with/across", never "consistent to". |
| Terminology | ~8% | Keep the field term: *counterclockwise test*, *amodal fbox annotation*, *min-hits*, *max-age*, *debounce*. Do not paraphrase into generic words. |
| Verb form / tense | ~7% | Methods + results in past tense (`was fine-tuned`, `produced`, `reached`); standing facts and model behaviour in present (`DiffMOT operates`, `the state machine guarantees`). |
| Style / register | ~5% | Drop Indonesian run-on comma chains. The Indonesian master had several 60+ word sentences; those became 2–3 English sentences. |
| Redundant pairs | — | `seperti yang ditunjukkan` → "as shown in", not "as shown by the figure that is displayed in". |

Also avoided, from the same studies: `besides` as a sentence-initial connective (reads casual in a Methods
section), and passive constructions inherited from Indonesian `dapat ... oleh` (`can be ... by`).

## 4. JESTEC-specific rules applied

Source: [JESTEC submission page](https://jestec.taylors.edu.my/submit%20a%20paper.htm) (accessed 14 Sep 2026)
and the Blind Review template.

- **English (UK).** → `optimisation`, `standardised`, `behaviour`, `centre`, `quantisation`, `licence` (noun).
  Decimal separator is a **point**; thousands separator a **comma**. The Indonesian master used commas for
  decimals throughout (0,4974 / 14.293) and was converted (0.4974 / 14,293).
- **Length 10–15 pages.** Body word budget roughly 4,500–5,500 words at single spacing with 7 tables and 6 figures.
- **Structure order**: Title → Authors (omitted for blind review) → Abstract (100–200 words) → Keywords (≤5,
  alphabetical) → Introduction → Theory (if applicable) → Methodology → Results and Discussion → Conclusions →
  Nomenclature (alphabetical, immediately before References) → References → Appendix (if any).
  → The manuscript keeps its own `Related Works` section, matching the Indonesian master. Nomenclature was
  **added** in the EN file because JESTEC makes it mandatory; every entry was taken from symbols already used in
  the body. Delete the section if the Indonesian master is meant to be reproduced exactly.
- **Captions**: figures cited as `Fig. 1` (or `Figure 1` at sentence start), caption **below**; tables as
  `Table 1`, caption **above**; equations as `Eq. (1)`.
- **References** numbered by first appearance. Not APA. JESTEC style:
  `Surname, A.B.; and Surname, C.D. (Year). Title. Journal, Vol(Issue), pages.`
  → **Not yet applied.** Entries were carried over unchanged from the Indonesian master; several are missing
  venue, volume/pages or year.
- **AI-use declaration** — required by JESTEC, placed immediately before the References section. Not yet written.
- **Similarity** ≤ 20% (Turnitin), references excluded.
- PDF metadata leaks the template origin → clear Title/Author/Comments via Inspect Document before export.

## 5. Editing checks run on the EN draft

1. Banned-phrase sweep (see `anti-ai-slop-writing`): no `penting untuk dicatat`, no `Moreover/Furthermore`,
   no `delve/leverage/robust/comprehensive/seamless`, no `it is worth noting that`, no `in order to`.
2. Collocation check on every verb+noun pair (`conducted`, `yielded`, `raised`, `reached`, `posed`).
3. Hedge calibration — `suppressed`, `gave`, `reaches`, `suggests` matched to what the design supports; no
   `proves`/`demonstrates conclusively` anywhere.
4. Sentence-length variance — checked per paragraph, long analytic sentences broken by short declaratives
   ("Computational cost is therefore dominated by detection and tracking." / "CrowdHuman is dense.").
5. Nominalisations converted back to verbs where the noun added no meaning.
6. Every number re-read against the Indonesian master after the decimal-separator conversion.
7. Em-dash audit — the raw count matters less than the **pattern**. A list framed by a *paired* em-dash
   (`The trackers — A, B, C — all run …`) reads as AI even once or twice in a paper. Convert to a colon,
   brackets, or a restructured clause. Keep at most one em-dash in the whole manuscript, and only for a real
   interruption; the en-dash in numeric ranges (`88.7–155.1%`) is unaffected and stays.
8. Opener audit on paragraphs — `Overall,`, `In summary,`, `Taken together,` used to launch a concluding
   paragraph. Cut the opener and let the claim carry itself.

## 6. Open items before submission

- [ ] Reformat all 31 references to JESTEC style; fill in missing venue/year/volume/pages.
- [ ] Insert the AI-use declaration immediately before References.
- [ ] Re-insert 3 equations with the Word Equation Editor — the master stores them as OMML objects that do not
      survive a Markdown round-trip (Eq. 1 CCW test, Eq. 2 cross product, Eq. 3/4 counting-error definitions).
- [ ] Check the page count in Word; trim from Related Works paragraph 1 and the Discussion if it exceeds 15 pages.
- [ ] Fix one inconsistency inherited from the master: the text cited "Fig. 6" for the per-device latency
      decomposition while the caption reads "Fig. 5". The EN file uses Fig. 5 in both places.
- [ ] Add author names + affiliations only in the camera-ready version, not the blind-review version.

## 7. Word formatting spec — read directly from the JESTEC template XML

`word/styles.xml` + `word/document.xml` of the Blind Review template, inspected 14 Sep 2026.
**Paste the text into the template file itself** — do not rebuild the styles; the template already carries every
named style below and pasting as plain text + reapplying the style is faster than re-creating them.

### Page

| Item | Value |
| --- | --- |
| Page size | A4 (11907 × 16840 twips) |
| Margins | top 1" (1440), right 2.44" (3514), bottom 2.25" (3240), left 1.25" (1800) |
| Columns | single (`<w:cols w:space="720"/>`) |

### Text styles (Times New Roman unless noted)

| Element | Style name | Size | Weight/style | Layout |
| --- | --- | --- | --- | --- |
| Title | `JESTECTitle` | 11 pt **Arial** | bold | centred, 60 pt before / 15 pt after |
| Author | `JESTECAuthor` | 10 pt | — | centred |
| Affiliation | `JESTECAffiliation` | 9 pt | — | centred |
| "Abstract" / "Keywords" heading | `AbstractandKeywordsHeading` | 10 pt | bold | left |
| Abstract body | `JESTECAbstract` | 9 pt | regular | justified, 6 pt before, 0 after |
| Body text | `JESTECStyleBodyTextIndentComplex10ptFirstline` | 10 pt | regular | justified, first-line indent 0.5 cm |
| Section heading (1, 2, 3 …) | `JESTECHeading1` | 11 pt | bold | 6 pt before / 6 pt after |
| Sub-section heading | `JESTECHeading2` | 11 pt | bold | 6 pt before / 6 pt after |
| **Figure caption** | `figurecaption` | 11 pt | **bold** | centred, caption **below** the figure |
| **Table caption** | `tablecaption` | 10 pt | **bold** | centred, caption **above** the table |
| Table title row (inside the table, grey `F2F2F2` fill) | — | 8 pt | **bold + italic** | centred |
| Nomenclature sub-heading ("Greek Symbols", etc.) | — | — | **bold + italic** | left |
| Reference entry | — | 10 pt | regular | hanging indent 357 twips, 3 pt before |

### Where the template actually uses italics

Confirmed by listing every run carrying `<w:i/>` in `document.xml` (100 italic runs; the clean list collapses to
six rules). Italic is **not** decorative and is **not** applied to body prose.

| # | What | Example from the template | Notes |
| --- | --- | --- | --- |
| 1 | **Variables / symbols**, including subscripts | `*C*<sub>D0</sub>`, `*C*<sub>N</sub>`, `*D*`, `*d*`, `*L*<sub>ref</sub>`, `*x*<sub>cp</sub>` | The submission page states it outright: "Symbols: Italicize variables". Subscripts follow the same italic run in this template. |
| 2 | **`Appendix …` cross-references** | `Appendix A` | The only cross-reference type set in italic. |
| 3 | **Journal / proceedings name** in a reference | `*Journal of Engineering Science and Technology*` | Article title stays upright. |
| 4 | **Conference proceedings name** in a reference | `*Proceedings of the 1<sup>st</sup> Conference on Power, Manufacturing, and Materials*` | |
| 5 | **Book / report / thesis title** in a reference | `*Advances in education*`, `*NACA Report No. 6623*`, `*PhD Thesis*` | |
| 6 | Greek symbols in the Nomenclature | `*α*, *β*, *θ*` | |

**Not italic in this template** (common false assumptions):

- `Fig. 1` and `Eq. (1)` cross-references — upright. Only `Appendix A` is italic.
- Figure captions — **bold**, not italic.
- Table captions — **bold**, not italic (the 8 pt bold+italic row is the table *title row inside the table*).
- Section and sub-section headings — **bold**, not italic.
- Reference author names, years, volume/issue and page numbers — upright. Only the venue/book/report title is italic.

Applied to `jestec-manuscript-en.md`: variables in Eq. (1)–(4), the `*p*₁/*p*₂/*q*₁/*q*₂` definitions, the `*D*`
sign test, the four affected reference venues (`*IEEE Access*`, `*Int. J. Inf. Technol.*`, `*Computers in Industry*`,
`*Computational Geometry in C*`) and the Nomenclature symbol column are marked up with `*…*` so the italics are
visible before pasting. Everything else stays upright.

---

## Sources (accessed 14 September 2026)

1. TextPulse AI — "How to Sound Natural in Academic English Without a Native Editor", 8 Aug 2026, updated 29 Aug 2026. https://textpulse.ai/blog/how-to-sound-natural-in-english-academic-writing
2. TextSight — "How to Write a Research Paper That Doesn't Read Like AI", 16 Jul 2026. https://www.textsight.ai/blog/research-paper-doesnt-read-ai/
3. Alfred Scholar — "The AI Slop Problem and the Scholarly Voice", 2026. https://www.alfredscholar.com/blog/the-ai-slop-problem-scholarly-voice-2026
4. Paperpal — "7 Reasons Your Writing Looks AI-Like (and How to Fix It Manually)". https://paperpal.com/blog/academic-writing-guides/reasons-your-writing-looks-like-ai-and-how-to-fix-it-manually
5. Retorika: Jurnal Ilmu Bahasa — "Types of Translation Errors from Indonesia Language into English in Pharmacy Journal Articles", 2022. https://doi.org/10.55637/jr.8.2.5416.206-213
6. Language Literacy — "Translation Errors in Undergraduate Scientific Writings: A Corpus-Based Study", Vol. 7 No. 1, 2023. https://jurnal.uisu.ac.id/index.php/languageliteracy/article/download/10252/pdf
7. JESTEC — "Submit a paper" / submission checklist, Taylor's University. https://jestec.taylors.edu.my/submit%20a%20paper.htm
