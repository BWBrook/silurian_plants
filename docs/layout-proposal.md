# Repository layout for a multi-study programme (proposal, 2026-11-02)

Status: **adopted 13 November 2026** (Barry; `docs/decisions.md`, 14 November entry), with three
differences: each study mirrors the root's folders (`studies/f3/docs/`, `data/`, `models/`, `tools/`,
`manuscript/`), the paper keeps the name `manuscript/`, and F3's folder is `studies/f3/`. The text below
is the original proposal. Barry raised the question in chat on 2026-11-02: "Is the repo well organised to
handle additional focused studies like this, or will all all smoosh together over time?"

## Diagnosis

The repository grew around one study, and it shows. Programme-level knowledge and F3's working files
share the same directories:

- `docs/` holds about 40 files. The charter, primer, questions, sources and rejected records serve
  every study. About 25 others belong to F3 alone: `plan-f3.md`, `f3-shape.md`, `loop1-close.md`,
  the Loop 2 and Loop 3 records, the sprint records, `pilot-traits.md` and the first-study literature
  tables. `docs/audits/` mixes card and programme audits with F3 reviews.
- `data/` mixes curated, reusable datasets (`timescale.csv`, `traits.csv`, `spores/`, `occurrences/`,
  `eprp/`, `external/`) with F3's derived evidence (`units/`, `pilot/`, `macro/`, `sprint2/`) and Q9's
  provenance check (`q9/`).
- `manuscript/` is singular. A second paper has nowhere to go.
- `docs/decisions.md` is 1,500 lines, mostly F3 detail, and every study would append to it.

With one more study the result would be two plans, two loop histories and two papers interleaved by
date, and an agent could no longer tell which files a claim depends on. A cold agent can find F3's
evidence today only because `manuscript/text/for-agents.md` and `claims.csv` index it.

## Proposal: shared commons, self-contained studies

```text
README.md  AGENTS.md  CLAUDE.md  CITATION.cff  LICENSE*  THIRD_PARTY.md
docs/            programme: charter, decisions (cross-study only), questions, primer,
                 precedents, framings, sources, rejected-records, closed-literature, audits/ (programme)
taxa/            taxon cards (shared knowledge base)
data/            curated datasets any study may use: timescale, traits, spores, occurrences, eprp, external
references/      one bibliography for all studies: dois.txt -> refs.yaml
library/         private source texts (ignored)
tools/           shared tooling (cards.py, refs.py, units.py, backups)
portal/          reading room
studies/
  f3-clock-maxima/
    README.md    question, status, headline claims, how to rebuild: the study's front door
    docs/        plan, shape, design, loop and sprint records, decisions.md (study-level)
    audits/      reviews of this study's work
    data/        study-derived evidence (today's data/units, pilot, macro, sprint2)
    models/      analysis code and outputs (today's models/f3, models/pilot-asr)
    paper/       makedoc sources and renderings: text/{main,supplement,brief,for-agents}.md,
                 figures/, settings/, csl/, build/, and claims.csv, the single ledger all four cite
  q9-hooper-provenance/   parked; today's data/q9 and its audit
```

Rules that keep it from re-smooshing:

1. **Dependencies point inward.** A study may read the commons. The commons never reads a study.
   Studies do not import each other's internals. A study that produces something reusable promotes
   it to `data/` or `tools/` with a README and a decision entry. A later study may also pin an
   earlier one's tagged release.
2. **One ledger per paper.** Every rendering cites `claims.csv` IDs, and `tools/claims.py check` fails on drift
   (adopted 2026-11-02 for F3; see `AGENTS.md`).
3. **One study, one folder, one front door.** Everything needed to rebuild a study's claims is in its
   folder or in the commons. Its `README.md` and `paper/text/for-agents.md` are the entry points.
4. **Two decision logs.** `docs/decisions.md` keeps charter-level and cross-study decisions, and links
   each study log. Each study keeps its own routine record. The questions register stays
   programme-wide, and studies cite Q IDs.
5. **Releases are per study.** Tag `f3-v1.0` with its own Zenodo DOI and `CITATION.cff` entry. The
   journal article, the brief and the agent paper are renderings of that tag. The repository stays the
   living record.
6. **Each study names its framing and question.** For example, `f3-*` cites `docs/framings.md` F3 and
   Q1. A new study needs its own decision before model code starts, as `AGENTS.md` already requires.

## Alternatives considered

- **One repository per study,** with a programme repository holding the commons. Each study would
  get a clean release and smaller clones. But the shared taxa, data and bibliography would need
  submodules or packaging. Cross-study provenance would leave the repository, and agents would lose
  cheap cross-reading. Revisit this only if a study needs different collaborators, licence terms or
  scale. `git subtree split` can extract a study folder with its history.
- **Leave F3 in place and start new studies under `studies/`.** This is cheaper now, but it keeps the
  asymmetry for good, and F3 is the template every later study will copy.

## Cost and sequence

The main cost is path-bound evidence. At least 55 JSON receipts bind paths under `models/f3/` or
`data/units/`, and `claims.csv`, the READMEs, `package.py`, `figures.py`, the tests and the portal name
those paths. Commit a657d54 established that hash-bound records stay byte-identical. So the
migration should:

1. wait for Codex's review C and the Loop 3 close, so no review runs against moving paths;
2. agree file ownership with Codex on the Board, since much of `models/f3/` is Codex's code;
3. move the files with `git mv` in one commit. It adds `studies/f3-clock-maxima/PATHS.tsv` (old path →
   new path), and every receipt verifier resolves old paths through that map. The receipts themselves
   stay unchanged;
4. update live references (scripts, tests, READMEs, `claims.csv`, `package.py`, the portal build), then
   rerun every check in `paper/text/for-agents.md` §6 and confirm that the outputs regenerate
   byte-identically;
5. record the move in both decision logs.

The new `references/` directory already sits at programme level, and the paper sources are already in
makedoc's layout, so the paper moves as one directory.
