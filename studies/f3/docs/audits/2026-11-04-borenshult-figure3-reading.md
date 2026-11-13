# Borenshult-1 triletes: the authors' published definite/possible split (Q1, Q2, Q5)

Claude Opus 5.5, 2026-11-04. Source: Rubinstein & Vajda (2019), GFF 141: 181–190,
https://doi.org/10.1080/11035897.2019.1636860 (held as `library/closed/rubinstein2019-open_firststudy.pdf`,
the open DiVA copy). Read: Fig. 3 (p. 183), Fig. 4 (p. 184) and the Fig. 5 caption (p. 185), rendered
at 400–500 dpi.

A reply from the authors arrived on 2026-11-04. It is held privately in
`library/closed/correspondence/` and is **not cited here**, because the request promised to cite their
answers only with their permission. Everything below rests on the published paper alone.

## What the paper already says

**Fig. 3 distinguishes definite from possible triletes.** Its legend has separate symbols for
"Trilete spore" and "? Possible trilete spore". Reading symbol positions against the depth scale
(about ±0.1 m, matched to the sampled depths in the Fig. 4 header):

- definite triletes at six depths: 43.1, 41.9, 41.1, 40.35 (drawn offset on a leader line),
  40.2 and 33.05 m;
- possible triletes only at 48.2 and 34.0 m;
- none below 48.2 m. The Darriwilian samples at 59.1, 67.6 and 71.1 m carry cryptospores only.

**Fig. 4 lists trilete taxa at seven depths.**

| Depth (m) | Fig. 4 trilete taxa | Fig. 3 symbol |
|---:|---|---|
| 48.2 | *Chelinospora?* sp. | possible |
| 43.1 | *Aneurospora* sp. | definite |
| 41.9 | *Ambitisporites* sp. | definite |
| 41.1 | none | definite |
| 40.35 | *Leiotriletes* sp. | definite |
| 40.2 | *Ambitisporites?* sp., *Leiotriletes* sp., *Leiotriletes?* sp., *Retusotriletes* sp. | definite |
| 34.0 | *Retusotriletes?* sp. | possible |
| 33.05 | *Leiotriletes* sp. | definite |

The two figures agree on which depths are possible only: 48.2 and 34.0 m. These are the two depths
whose only trilete taxon carries a query. At 40.2 m, unqueried *Leiotriletes* and *Retusotriletes*
(Fig. 5A, F) sit beside the queried forms (Fig. 5J, K), so the depth counts as definite either way.

**The figures disagree at 41.1 m.** Fig. 3 plots a definite trilete there; Fig. 4 lists no trilete
taxon at that depth. Our table `data/units/borenshult_reporting.csv` follows Fig. 4 (E1
`category-not-listed`), so it matches its declared source. Fig. 3 gives six definite trilete samples,
and Fig. 4 with queried depths removed gives five. The paper does not say which figure is right.

## What we got wrong (Q5)

Our earlier treatment took all seven Fig. 4 depths as the authors' trilete reports. Two records
carried that error:

- `docs/audits/2026-10-31-borenshult-reading-and-screen.md`;
- the 2026-10-31 request, which described the authors' reading as "trilete spores at seven depths
  from 48.2 to 33.05 m".

The authors' own Fig. 3 had already marked 48.2 and 34.0 m as possible only. Our claim failed against
its source.

`docs/rejected-records.md` entry 15 also listed Rubinstein & Vajda as "not read". It was held, and is
now read for Figs. 3–5.

## Consequences, by reading (proposal; not adopted)

- **Figure 3 reading (the describing authors').** Definite triletes at six depths from 43.1 m;
  48.2 and 34.0 m remain unresolved. Fig. 3 places 43.1 m at about 455 Ma, below the Kinnekulle
  K-bentonite (U-Pb 454.41 ± 0.17 Ma as the paper cites it). Under this reading the earliest definite
  trilete is about 455 Ma. That is about 10 Myr older than the strict compilation's certain trilete
  first appearance (445.20 Ma, `data/spores/first_appearances.csv`), and it lies in Baltica, not
  Gondwana.
- **The 459.1 Ma maximum.** Hooper et al. (2026) take it from the oldest *possible* trilete, the
  48.2 m specimen. The describing authors themselves plot that specimen as possible only. A maximum
  may rest on a possible record, but the paper should say so. Fig. 3 ties 48.2 m to the
  *B. variabilis* subzone, drawn between 458 and 456 Ma. How Hooper et al. reach 459.1 Ma from it is
  not established here (Q2).
- **Borenshult as an M2 frame.** Under this reading only the three Darriwilian samples (59.1, 67.6
  and 71.1 m) lie below the first definite trilete. That is the same older set as in the inclusive
  case, which bounded at 3.2 against the screen's 5.99 (2026-10-31 audit). The reference changes by
  at most one detection, so the core still cannot test M2's absence premise.
- **Results unchanged.** The Murzuq comparison, the body-record bounds and the known-answer check are
  untouched; the known-answer check uses cryptospores, not triletes. What changes is Fig. 1's trilete
  bar and the paper's account of M2's basis, if the reading is adopted.

## Consistency of standards (Q2, Q5)

`taxa/ambitisporites.md` records the Hirnantian Turkish trilete (Steemans et al. 1996) as accepted,
without stating how many specimens support it. The main reading meanwhile holds every Borenshult
trilete unresolved under a general compression caution. That is a different standard for the two
records. Proposed: score each earliest trilete claim on one rubric, then let the readings follow the
scores rather than the claim's place in a narrative. The claims are Borenshult, Hirnantian Turkey,
Zbrza and Qusaiba-1. The rubric:

- number of specimens;
- the describing authors' own confidence in the mark;
- independent age control;
- whether any source demonstrates an artefact, as opposed to raising the possibility of one.

## Addendum, 2026-11-05: how Hooper et al. derive 459.1 Ma (Q2)

Source: Hooper et al. (2026), main text (calibration paragraph) and Supplementary Table 4
(`data/external/local/deposits/hooper2026-spore-evolution-esm/41477_2026_2432_MOESM1_ESM.pdf`, crown-Embryophyta
entry). Read 2026-11-05.

- **Main text:** the maximum rests "on the basis of the oldest possible trilete spores" from the Dalby
  Limestone of Borenshult-1. They decline to use the same spores for a minimum because the trilete mark "might
  be an artefact of compression".
- **Supplementary Table 4:** the soft maximum is keyed to *Chelinospora?* sp. at 48.2 m, which the table
  calls a "probable trilete spore". The level lies in the *Baltoniodus variabilis* conodont zone (lower
  Sandbian), below the Kinnekulle K-bentonite (454.41 ± 0.17 Ma). The number is then taken from the
  stage, not from the level: the maximum "corresponds to the base of the Sandbian stage", dated
  458.4 ± 0.7 Ma, giving 459.1 Ma. So 459.1 = 458.4 + 0.7 (GTS2012 Sandbian base). Under ICS
  v2024/12 (`data/timescale.csv`, 458.2 ± 0.7) the same rule gives 458.9 Ma.

**Consequence for the Fig. 3 reading.** The definite triletes at 43.1 m are also lower Sandbian, below
the bentonite. Hooper et al.'s stage-base rule would therefore give the same 459.1 Ma from the describing
authors' lowest definite specimen. The value of M2 does not depend on the doubtful 48.2 m specimen. Our
2026-11-04 framing ("M2's 459.1 Ma rests on a specimen plotted as possible only") is true of the specimen
named but has no numerical consequence. The paper's wording ("rests on the oldest possible trilete spores")
quotes Hooper et al. correctly and needs only the stage-base derivation added. The table's "probable" for
the 48.2 m specimen is stronger than the describing authors' own "? Possible trilete spore" (Q5, minor).

**A consequence Hooper et al. do not draw (interpretation).** Their stated reason for not using the Dalby
spores as a minimum is the compression caution, applied to all figured specimens. The describing authors
plot six depths as definite. If those are accepted and triletes are taken as crown-embryophyte evidence, the
crown-Embryophyta minimum would rise from 426.9 Ma (Cooksonia, Homerian) to about 454.4 Ma (the
bentonite above 43.1 m), and the calibration window would shrink from 32 to about 5 Myr. Whether triletes
alone can place a fossil in the crown is a separate question (their minimum uses a total-group tracheophyte,
not a spore); this note records only that the minimum, not the maximum, is what the Borenshult reading moves.

**Correction, 2026-11-05 (Codex review C, R5; accepted).** The paragraph above runs together three
separate mappings. Under Hooper et al.'s own argument a trilete first appearance bears on the crown as a
maximum; it supplies a crown minimum only under an added mapping of its producer to the crown, which a
trilete mark alone does not give. If that mapping were adopted, the minimum would be the young edge of the
bentonite's uncertainty, about 454.24 Ma, not 454.4 Ma. The minimum consequence is therefore a conditional
alternative calibration, not a consequence of accepting the Figure 3 symbols.
