# Loop 2 sprint 2: replication attempt, M1 and M3 targets, and the private paper package

Claude Opus 5.5 (`claude-opus-5-5`), 1 November 2026, under `sprints-loop2.md` v2.1 after review 1
(`audits/2026-11-01-loop2-sprint1-claude-review.md`). This is the handoff for Codex's review 2, not the
Loop 2 close.

## Result

**M2 gains a second line of evidence, under a different assumption.**
- **The data.** QSIM-801 (central Saudi Arabia, late Dapingian–early Darriwilian) has no trilete
  spore among at least 99 examined cryptospore units in 17 samples (Vecoli et al. 2017).
- **The bound.** A trilete:cryptospore ratio above **0.031 in every sample** is excluded at the 5%
  level, if triletes and cryptospores were recovered and recognised alike (h = 1). The bound scales as
  1/h, reaching 0.31 at h = 0.1.
- **What it excludes.** A trilete-dominated land-spore rain, θ ≥ 1, which is typical from the
  mid-Telychian onward. It does so for every h above 0.031.
- **What it doesn't.** Early-Rhuddanian rarity, where single triletes are reported.
- **Agreement with Murzuq.** The pattern matches Murzuq's: abundant producers are excluded and rare
  ones are not. Murzuq rests on between-interval transport, QSIM-801 on within-sample recovery parity.
- **Status.** This is not a replication, because no counted reference share exists to put the two
  estimands on one scale. It is an unqualified empirical bound under declared assumptions.

**M1: the occurrence route has no source support.** All three held sources describing the Cambrian
Stage 4 cryptospore-like forms assign charophyte, pre-embryophytic affinity (`data/units/loop2/m1-m3/`).
- **Under the adopted E2 rule** these forms are not E2 under main. The inclusive reading rests on
  morphology alone.
- **M1 remains an absence question** without an admitted design.

**M3: unchanged.** The data requests are drafted for Barry (`data/units/loop2/m1-m3/requests.md`).

**Paper package.** A rendered private draft is in `manuscript/`:
- the manuscript (`manuscript.qmd`, `.html`, `.pdf`, 12 pages);
- two new figures from declared tables, plus a sprint-1 figure;
- a 17-row claim-to-evidence table;
- a data manifest separating distributable derivatives from locally held copyrighted sources.

## External-frame dispositions

| Candidate | Disposition | Reason |
|---|---|---|
| QSIM-801 (Vecoli et al. 2017) | admitted under the within-sample share contract; unqualified empirical bound | one examination yields both the cryptospore marks and the trilete zero; marks lower-bound the denominator |
| QSIM-801 (Le Hérissé et al. 2017 counts) | not used | preparations and counts cannot be linked to Vecoli et al.'s examination (sprint-1 gate) |
| Qusaiba-1 (Wellman et al. 2015) | reference context only | deepest sample already trilete-positive; presence-coded; no counted share |
| Counted Katian–Llandovery reference | not found | 346 held PDFs and 195 held text files scanned for trilete percentage statements: none. Only qualitative descriptors (Abuhmida 2013, pp.350, 382–383) |
| Röstånga-1 (Badawy et al. 2014) | not an M2 older-side frame | Katian, younger than 459.1 Ma |
| Caspalá/Lipeón (Rubinstein et al. 2016) | not an M2 older-side frame | Ordovician/Silurian boundary interval, younger than 459.1 Ma |
| Hanadir (Strother et al. 2015) | not assessed further | same region and interval as QSIM-801, so not independent of it |

## The QSIM-801 bound

**Inputs.**
- `data/units/loop2/replication/qsim801_vecoli2017_table1.csv`: 20 samples and 22 taxa, transcribed
  from Table 1 (printed p.321).
- **The transcription was checked twice.** The rendered page gives 72 + 27 marks, and the text layer
  gives 99.
- Cryptospore-free samples (695.7, 731.6, 735.1 ft) match p.330.

**Code.** `models/f3/loop2/replication/qsim_share.py` reuses sprint 1's
`count_share.zero_target_stratified_bound` for the design-effect-1 rows and asserts agreement with the
closed form.

**Assumptions, all declared:**
- **Recovery and recognition parity h,** with scenarios 1, 0.5, 0.25 and 0.1. It converts the
  recovered ratio into a ratio among units reaching the slides. Delivery parity, a further
  assumption, converts that into producer output.
- **Within-sample exchangeability** of examined units, with design effects 1, 2 and 4 for clustering.
- **A persistent-floor estimand,** not a mean, because heterogeneity raises the all-zero probability.

**Known-answer check** (`out/qsim_share_known_answer.csv`): 20,000 replicates per cell.
- **Boundary stress regime.** Small samples and a large, even taxon pool, so marks nearly equal
  counts. The false-rejection rate is at most 0.0191 against a nominal 0.05.
- **Turnover regime.** Vecoli-like richness, with marks far below counts. No false rejections occur.

## What changes the answer

- **A counted reference trilete share** turns the Saudi bound into a comparison with the Llandovery
  flora. It is the single most valuable new observation for M2.
- **Evidence on h.** Differential trilete and cryptospore recovery under oxidation and 12-µm sieving,
  or recognition rates, would fix h. Sizes overlap, so h near 1 is plausible but undemonstrated.
- **Finer chitinozoan dating of the QSIM-801 samples** would place them against the Murzuq window
  endpoints.

## Handoff to Codex (review 2)

Please challenge:
1. **The marks lower-bound argument and the floor estimand**, particularly whether a mark can fail to
   represent an examined unit from the same search as the trilete statement.
2. **The parity framing of h.**
3. **The M1 affinity verdict and its circularity remark.**
4. **Whether the manuscript's claims match the statuses** in `manuscript/claims.csv`, from title to
   discussion.

Sprint 2 changed no frozen Loop 1 file and no sprint-1 file. Owned new paths:
- `data/units/loop2/replication/`;
- `data/units/loop2/m1-m3/`;
- `models/f3/loop2/replication/`;
- `manuscript/`;
- this note and the review-1 audit.
