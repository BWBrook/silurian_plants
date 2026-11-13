# F3: fossil absences and molecular-clock maxima

The programme's first study. It asks what missing fossils can say about the age of land plants:
how three fossil maxima used by molecular clocks (515.5, 459.1 and 431.2 Ma) rest on their evidence,
what a local spore absence in Libya shows, and how much less often early vascular-plant fossils
would have to have been found for older clock dates to fit. Framing F3 was adopted on 28 October 2026
(`../../docs/framings.md`); the plan is `docs/plan-f3.md` and its governing shape `docs/f3-shape.md`.

**Status:** the paper is in revision for *Proceedings of the Royal Society B*. Its claims are in
`manuscript/claims.csv`; everything the paper reports cites a claim ID there.

## Where things are

| Folder | Holds |
|---|---|
| `manuscript/` | The paper, built with makedoc: article, supplement, two-page brief and agent guide (`text/for-agents.md`, the entry point for an agent), with the claims ledger and figures. |
| `docs/` | Plans, loop and sprint records, the trait pilot, the first-study literature tables, and this study's decision log (`docs/decisions.md`). |
| `docs/audits/` | Independent reviews and reproduction receipts for this study. |
| `data/` | Evidence derived for F3: sampling units (`units/`), the body-fossil inventory (`macro/`), occurrences, the trait pilot and the Q9 provenance check. |
| `models/` | Analysis code and outputs: the Loop 1–3 models, the trait-pilot ancestral-state analysis (`pilot-asr/`, R under renv) and the GRIWM/CRIWM estimators. |
| `tools/` | F3-only scripts, including the reproduction runner and `moved.py`. |
| `work/codex/` | Records of delegated Codex jobs. |

F3 also reads the shared commons at the repository root: `data/timescale.csv`, `data/spores/`,
`data/eprp/`, `data/external/`, `references/` and `tools/claims.py`.

## Rebuild and check

From the repository root:

```bash
make -C studies/f3 check-public        # restore the archived PBDB input, then the public tests
make -C studies/f3 reproduce-derived   # byte-identity reproduction of selected outputs
make -C studies/f3/manuscript check    # claims drift check, makedoc lint and citation audit
make -C studies/f3/manuscript          # PDF and DOCX for article, supplement and brief
```

## Paths before 14 November 2026

This study lived at the repository root until the study-first move. Records written before it (audits,
decision entries, receipts) name the old paths: `models/f3/`, `data/units/`, `manuscript/` and so on.
`PATHS.tsv` maps every moved file and directory, with each file's hash before the move and after its
path repair; `tools/moved.py` resolves them in code.
