# Cross-family audit of Codex spore vetting and genus classes

2026-10-27. Claude Sonnet 5.5 audited a sample of Codex `gpt-6.1-sol` output for the spore dataset.
It answered blind before opening the Codex answers, then compared and adjudicated. Claude Opus 5.5
reviewed the adjudication. The blind answers are in `2026-10-27-spore-vetting-audit-blind-answers.csv`.

## Sample

- **Group verdicts:** 30 of 189 record groups: all 12 rejections, 9 doubtful and 9 accepted
  (seed 7).
- **Genus classes:** 40 Codex-classified genera with five or more rows (seed 7).

## Agreement

| Task | Exact agreement | Coarser agreement |
|---|---|---|
| Group verdicts | 19/30 (63%) | accept vs not-accept 25/30 (83%) |
| Genus classes | 32/40 (80%) | no cryptospore/trilete confusion; every split is within the trilete family, uncertain vs committed, or non-spore |

## Adjudication

- **Codex judged right on most disagreements.**
  - It catches "trilete" taxa that are hilate cryptospores (*Imperfectotriletes*, as *A.
    vavrdovae* and probably *A. imperfectus*).
  - It downgrades pooled stage windows.
  - It rejected the Floian *Tetrahedraletes* row of Vergel et al. (2002).
- **Two Codex verdicts changed:**
  - doc 11441 (Brazil): reject → doubtful;
  - doc 13611, other group (anachronistic *Laevigatosporites*): doubtful → reject.
- **Genus classes:** the auditor judged Codex right on four of the eight disagreements, and four
  are a wash.

## Bias

- **Vetting:** Codex is more conservative than Sonnet, and stricter about pooled ages and
  mismatched locations.
- **Classification:** Codex assigns high confidence freely and rarely uses `uncertain`.

## Consequence

First appearances are reported for a `strict` set and an `inclusive` set, because exact agreement
on vetting verdicts is modest. The accept/not-accept boundary that the strict set rests on agreed
at 83%. A record's class-level membership is reliable; its ornament subclass is less so. Analyses
that need the subclass should treat the trilete subclasses as soft.
