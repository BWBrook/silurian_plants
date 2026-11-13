# Loop 2 sprint 1: count-feasibility and contamination gate

Codex, 1 November 2026. Recorded before model implementation, after review of Claude's
`309074f` plan v2 and Board 2774. Barry authorised resolving the plan and proceeding with sprint 1.
Two independent source readers inspected the held primary texts/tables; a methods reviewer examined
the observation model. The parent verified source hashes and the decisive 695.7-ft text.

## Decision

Neither held frame currently admits an empirical trilete/cryptospore count-share analysis.
This is a protocol/denominator failure, not evidence that triletes were present or absent beyond
the sources' actual reporting scope. Sprint 1 proceeds with the count-free Murzuq analysis and a
conditional count-share method with known-answer checks. The latter is a method handoff for
sprint 2, not a qualified QSIM result. Full Saudi extraction/admission remains Claude's ownership.

### Murzuq

Abuhmida 2013 printed p.35 (PDF 51) distinguishes 200 organic particles counted on kerogen
preparations for palynofacies from counting all palynomorphs on the first biostratigraphic slide
and scanning additional slides for rare forms. The latter uses separately treated residues.
Printed pp.392–393 (PDF 408–409) define a broad cryptospore palynofacies group including some
incertae sedis. It is not a documented trilete-plus-cryptospore denominator.

The enclosure-4 palynofacies panels do contain per-sample aggregate cryptospore percentages;
plan v2's inference from the interval prose alone was incomplete. The paired range charts supply
taxon symbols, including *Ambitisporites dilutus*, not corresponding per-sample raw counts.
The panels are PDF 631 (A28i), 633 (B2), 635 (D1), 637 (E1), 639 (H2), 641 (I3), paired with the
range charts on the preceding pages. The source reader inspected all six chart sets. These are
different observation bases: a trilete mark cannot be the numerator of the 200-particle fraction.
Formation summaries such as Hawaz 20–44% are not copied to individual rows.

Reuse the 164-entry appendix inventory, 158 chart rows and existing literal joins/admission rules.
Annotate observation bases and missing links only; do not overwrite sources or existing E1 outcomes.
Do not digitise aggregate percentages merely because they exist: without a decision-relevant role,
this would not repair the missing trilete/count pairing.

### QSIM-801

Vecoli et al. 2017 printed p.320 (PDF 2) describes 20 approximately 30-g samples prepared at
Liège, including oxidation and 12-µm sieving. Table 1 (PDF 2–3) gives occurrence marks. Printed
p.330 (PDF 12) reports cryptospores in 17 samples and no triletes in the studied assemblages;
cryptospore-free depths are 735.1, 731.6 and 695.7 ft. Microscopy effort and counted spore totals
are not reported.

Le Hérissé et al. 2017 PDF 9–10 describes 42 samples and mixed Aramco/Brest/Liège preparation
series, including soft digestion and unfiltered residues. At least 300 palynomorphs were counted
per sample; percentages in Tables 2–4 are not exact raw tallies or exact totals. No row-level
preparation/slide linkage establishes that this count supplies the effort behind Vecoli's zero.
Table 4 (PDF 93, manuscript p.92) gives a broad morphological cryptospore group, not E2 affinity.

Read-only reconciliation finds 18 exact depth matches: 16 cryptospore-positive in both, and
695.7/731.6 negative in both. Vecoli's 735.1 and the companion's 735.11 (0.38%) are an unsafe
near-match; Vecoli's 719.9 is absent from the 42-row table, and 717.9 is a distinct label.
Depth agreement alone is not a shared rock split, preparation or searched-slide denominator.

The alleged 695.7 discrepancy is a source-reading error: PDF 38 (manuscript p.37) assigns 10.4%
to *Micrhystridium*. The following paragraph and Table 4 give cryptospores as 0%. This is a Q5
correction, not a revised fossil identification. Never substitute `300 × percentage` for a tally
or `20 × 300` for a trilete search denominator.

## Statistical and plan amendments

- A conditional share model needs matching counts, or independent matched-rate preparations with
  a known relative effective effort. If that ratio can approach zero, relative producer output
  is unbounded and the share upper limit is the trivial 1. A source's taxonomic zero and another
  preparation's percentage do not supply the missing ratio.
- A within-sample recovered share is not producer output without a relative delivery/recovery
  assumption. Between-interval normalisation additionally needs a suitable counted reference.
  QSIM remains a conditional method candidate, not an admitted two-frame replication result.
- Older Murzuq zeros constrain caved-report intensity in those older cuts, not a geological
  caving rate or contamination of the reference cuts. Separate indigenous reference intensity,
  reference contamination and older contamination. A depth-transfer relation is an assumption
  unless supported independently. Unmatched cores/cuttings cannot estimate a universal correction.
- Murzuq's frozen primary results remain unchanged. New leave-one-well-out, chronology and
  contamination calculations are unqualified sensitivities or identification limits. Releasing a
  new primary claim would require its own qualification; no such claim is assumed at this gate.

The sprint must still produce new joint break-even/identification results rather than repeating
the old ρ grid. Declared analytic conditions, a prospective numerical grid, source-bound outputs
and independent numerical checks will distinguish mathematical limits from empirical qualification.

## Primary-file hashes

| Held file under `library/closed/` | SHA-256 |
|---|---|
| `abuhmida2013-thesis-related_macbook20261030.pdf` | `c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211` |
| `vecoli2017.pdf` | `5932b8da36d10be365089f06cab55ad472ade98c238186432058e9493459936b` |
| `leherisse2017_firststudy.pdf` | `b5f8f0c7bedc95616390aad6bedcc6ccd6c0b39facce4bf5faadc5d0cf20c48c` |
