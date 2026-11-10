# F3 article against *Proc B* conventions: format and structure comparison

10 November 2026. Barry, in chat, asked for a subagent to "cross-compare the current article's format,
layout, structure, narrative style, section breakdown, number and form of display items etc., to 5 other
recent relevant works from that journal, and report back on incongruities". The comparison was run by a
Claude Sonnet 5.5 subagent, briefed and checked by Claude Opus 5.5. The draft compared is `main` at
`96960a4` (`manuscript/text/main.md`, built PDF about 18 pages). Barry asked for the report to be kept
for the revision.

## Access and verification

- **Proc B author pages blocked.** royalsocietypublishing.org (author guidelines, for-authors, submit)
  returned 403 to automated fetches. In the in-app browser it stops at a Cloudflare human-verification
  checkbox, which agents do not tick.
- **Rules below are from the Royal Society's general author guidelines**,
  <https://royalsociety.org/journals/authors/author-guidelines/>, fetched 10 November 2026. That page
  says length limits are journal-specific.
- **The *Proc B* length limit is unverified.** A search-tool summary attributes it to
  royalsocietypublishing.org/rspb/pages/for-authors: up to 12 pages including figures and tables, no
  more than 10,000 words including title page, abstract, legends, tables and references. It also gives
  about 850 words to a page.
  - *To do before planning cuts:* confirm the limit, the display-item limits and the AI-authorship
    policy on the live *Proc B* pages.
- **Comparator DOIs** were checked through the Crossref API (ISSN 0962-8452) and Europe PMC; all are
  *Proc B* and open access. Full texts were read from Europe PMC XML.
- **Electronic supplementary material (ESM) was not read.** Comparator ESM load is inferred from how
  often the main text points to it.
- **Draft facts were re-checked** by Claude Opus against the source:
  - the heading scheme;
  - the "Methods in brief" placed after the Conclusions;
  - draft artefacts in the back matter (main.md lines 534, 542, 553);
  - 31 distinct citation keys in `main.md` and `figures.md`;
  - the AI byline entry in `manuscript/authors.yaml`.

## Royal Society general rules relevant to the draft

- **Abstract:** "no more than 200 words".
- **Keywords:** 3–10.
- **Sections:** the main text should be in clearly labelled sections, usually background, methods,
  results, discussion and conclusions.
- **Methods:** they should contain all elements needed to interpret and replicate the results, and
  "the main article should stand on its own merit".
- **References:**
  - Vancouver style, numbered in order of appearance;
  - datasets cited in the reference list;
  - references in the ESM kept to an "absolute minimum".
- **Data and code:** must be public; "available on request" is not permitted.
- **Required statements:**
  - Ethics, including fossil specimen details where relevant;
  - Authors' contributions (CRediT);
  - Competing interests;
  - Funding, with grant numbers;
  - Declaration of AI use, with a published statement of how AI was used.
- **Media summary:** at most 100 words.

## Comparators

| | Our draft | A | B | C | D | E |
|---|---|---|---|---|---|---|
| DOI | – | 10.1098/rspb.2026.0635 | 10.1098/rspb.2025.1133 | 10.1098/rspb.2023.2618 | 10.1098/rspb.2022.1079 | 10.1098/rspb.2024.0165 |
| Why chosen | – | Calibration and divergence-time methods compared | Bayesian fossil-record model of origination and extinction ages (Hemiptera) | Tip-dating of crown-clade divergences | Devonian flora, palaeobotany (Angarida) | Fossil compilation with statistical modelling |
| Main text, words (approx.) | about 6,400 (about 7,000 with captions; PDF total about 9,150) | 5,340 | 5,850 | 3,005 | 3,390 | 5,560 |
| Abstract, words | about 268 | 202 | 207 | 188 | 115 | 211 |
| Results and Discussion | separate | separate | separate | combined | combined | separate |
| Figures / tables in main text | 4 / 5 | 4 / 0 | 3 / 0 | 3 / 1 | 2 / 2 | 4 / 3 |
| References | 31 (Chicago author-date) | 66 | 75 | 52 | 64 | 57 |
| ESM load | 27 pp, about 11,000 words, own reference list | light | heavy | very light | none | moderate |
| Introduction | 8 paragraphs, about 870 words, opens with a question, contains Table 1 | 2 paragraphs | 5 | 5 | 6 | 3 |
| Methods placement | almost all in ESM; 10-line "Methods in brief" after Conclusions | before Results | before Results | before Results | before Results | before Results |
| End matter | Roles of AI; Data and code | Ethics, Data accessibility, Declaration of AI use, Authors' contributions, Conflict of interest, Funding | same | same | Data accessibility, Authors' contributions, Conflict of interest, Funding | same |

- **Headings.** All five comparators use unnumbered Introduction, (Material and) methods, Results,
  Discussion and Conclusion, with at most one level of sub-heading. Ours numbers its sections, adds a
  separate "2. Evidence" section, and numbers sub-headings 3.1–3.5 and 4.1–4.4.
- **Numeric density** is about 62 numeric tokens per 1,000 words in ours, against about 44–61 in the
  comparators whose counts are clean. It is not distinctive.
- **First-person use** (24 instances) is within the comparators' range.
- **Closeness of match.** None of the comparators is a direct calibration paper for early land plants.
  A and D are the nearest in kind. Further candidates, not measured: 10.1098/rspb.2024.2337
  (*Zosterophyllum*, Lower Devonian) and 10.1098/rspb.2024.1293 (fossil calibration of osteoglossid
  biogeography).

## Incongruities, ranked

**Rule breaches**

1. **Abstract** is about 268 words, against a limit of 200. Lead with the question and the result, and
   move the 8–12× and 2.4–4.5× detail to the Results.
2. **Methods are in the ESM.** Write a Material and methods section of about 1,200–1,800 words, placed
   after the Introduction.
   - It should cover the unit rules, the Murzuq model, the body-record bound, the step model and
     frontier, and the interval tests.
   - Detailed derivations stay in the ESM.
3. **End matter.** Add the standard *Proc B* statements:
   - Ethics: no fieldwork; specimens studied only from the literature.
   - Data accessibility: keep our specific deposit statement.
   - Declaration of AI use: our roles statement goes here (see item 6).
   - Authors' contributions (CRediT).
   - Competing interests.
   - Funding, with the ARC Laureate grant number.
   - Keywords.
4. **References.** Switch the citation style file to numbered Vancouver, and cite the Zenodo deposit
   in the reference list.
5. **Length** (limit unverified). We are near 10,000 words before the methods return, so cut the
   Results and move tables to the ESM; comparators carry 0–3 tables. Candidates: Table 1 to the
   Results or the ESM, and Tables 3–5 to the ESM or into figures.
6. **AI byline.** `authors.yaml` lists "Claude Opus 5.5 (Anthropic) and OpenAI Codex" as a byline
   entry, and *Proc B*'s policy is unread. **Deferred by Barry:** a placeholder stays for now, and the
   byline is crafted as one of the last tasks before submission.
7. **ESM reference list.** The supplement carries its own list; fold what it needs into the main list
   and keep the ESM's own references to a minimum.

**Conventions**

8. **Headings.** Adopt the plain, unnumbered scheme. Fold "Evidence" into the Methods and Results, and
   drop "Methods in brief".
9. **Introduction.** Cut it to 4–5 paragraphs, open with a statement rather than a question, and move
   Table 1 out of it.
10. **Draft scaffolding.** Remove "awaiting his final review", the commit hashes, the repository paths
    and "Public release … is Barry W. Brook's decision" from the submitted text; the repository keeps
    them.
11. **Reference count.** We cite 31 works, against 52–75 in the comparators. Expect a referee to ask
    for more of the calibration, fossil-sampling and stratigraphic-confidence-interval literature.

**Softer contrasts**

12. **Results sub-headings** are claim sentences; the comparators mostly use short descriptive labels.
13. **Hedging.** "Compatible with" language is dense. A referee will look for a clearer headline;
    see the main-message entry of 10 November in `docs/decisions.md`.

## Where the draft is stronger

- Number-to-claim binding through the claims ledger, which none of the comparators has.
- A specific, hash-verified data and code deposit.
- A detailed statement of AI roles. Keep it as the AI declaration and compress it.

## Effort

- **Quick:** items 1, 3, 4, 10 and 12.
- **Substantial:** items 2, 5, 8, 9 and 11, which together restructure the article rather than polish
  it.
