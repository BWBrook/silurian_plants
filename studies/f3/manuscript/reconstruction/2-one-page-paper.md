# Reconstruction step 2: the one-page paper

Claude Opus 5.5 draft revised by Codex (`gpt-6.1-sol`), then reconciled by Claude, 10 November 2026. Target: about 600 words,
readable as a complete paper. The questions organise completed analyses; their formulation belongs to
this reconstruction. Claude's version is preserved at `1fe577c`. Review decisions and remaining
disagreements are indexed in `README.md`.

---

## When did living land plants arise? What their fossil age limits require

**Background.** Molecular clocks combine DNA differences and fossil limits to date ancestors.
Morris et al. (2018), Harris et al. (2022) and Hooper et al. (2026) place the ancestor shared by living
land plants at 515–474, 515–493 and 457–450 million years ago (Ma), respectively. Hooper reused Harris's
DNA data with revised fossil calibrations. These dates concern a shared ancestor; earlier extinct lineages could already have occupied land. A fossil maximum sets an older age
limit, drawing on an argument that earlier plants would probably have left recognisable evidence.

**Questions.** We examined three maxima: 515.5 and 459.1 Ma for living land plants, and 431.2 Ma for
vascular plants, the group containing ferns, conifers, flowering plants and their relatives. We asked
which evidence underlies each maximum, what Libyan spores constrain, and which early recording rates
or delays before recognisable bodies permit older vascular-plant origins.

**Approach.** We audited the calibration fossils' identities, ages and sampling opportunities. In the Murzuq Basin, Libya, a model combines the spore reports from
older and younger well cuttings (rock chips from drilling), age uncertainty, delivery from land and a
shared well effect.
For vascular-plant fossils, we grouped finds into [48]{.C25} locality–age units and calculated a
conservative 95% older bound on when their recognisable record began. The base treatment assumes that
identifiable finds accumulated at a constant rate. A step model then lowers the rate before the oldest
find; the drop needed to reach each candidate origin is its recording contrast.

**Results: calibration evidence.** The 515.5 Ma rationale uses older marine algal cysts as a
preservation control for land-plant spores. The assembled material leaves the relevant search
opportunity and terrestrial delivery unquantified. The younger maxima use a geological stage's oldest age plus its uncertainty, keyed to Swedish
triletes (three-rayed spores) and Irish *Cooksonia* bodies. An older Czech *Cooksonia* offers another
candidate body anchor.

**Results: Libyan spores.** The charts record triletes in [51 of 59]{.C02} younger cuttings and zero
of [28]{.C01} older cuttings. If spores reached the older rocks as readily as the younger ones, the
model allows a sustained local spore supply of at most about a tenth of the younger level. If delivery
to the older rocks was ten times poorer, a supply near the younger level fits.

**Results: plant bodies.** At a constant rate, the bound is about [429]{.C27 .V002} Ma; halving the
earlier rate gives 431.0 Ma. Both lie younger than the 431.2 Ma maximum. Origins at 444–452 Ma, spanning
the Morris mean dates and the Harris interval, need an earlier rate [8]{.C48 .V054}–[12]{.C48 .V055}
times lower. At a constant rate, they instead need recognisable bodies to have appeared at least
[15–23]{.C33} million years after the origin. Adding
Ordovician spore-capsule fragments from Oman moves the broader land-plant body bound under constant recording from
[434.5]{.C28} to [455.2]{.C40 .V022} Ma.

**Assumptions and sensitivity.**

- The spore model assumes uniform ages within stages and an indigenous younger reference. Eighteen of
  the older cuttings are younger than 459.1 Ma; ten broadly dated cuttings reach before it.
- Cutting outcomes are independent given the shared well effect. Discounting repeated
  cuttings within wells and rock units gives an exploratory comparison near 0.4.
- Body units are independent and their age ranges contain the true ages. Coarser groupings or a
  curated subset give bounds of [432–434]{.C30} Ma and recording contrasts of
  [2.4]{.C48 .V056}–[4.5]{.C48 .V057} times.
- Relating bodies to the ancestor of living vascular plants assumes the fossils belong among its
  descendants and specifies a delay before recognisable bodies. The recording contrasts and offsets specify scenarios; they remain quantities to
  constrain independently.
- The constant-rate model fits the Oman-inclusive age sequence poorly; its bounds illustrate inventory
  sensitivity.

**Conclusions.** Older dates for living land plants fit the fossil record if early plants were found
several times less often, or recognisable features evolved later. Clock builders should justify each maximum's
character, geographical and recording assumptions and its soft-bound tail. Independent evidence on
early recording and diagnostic characters would narrow the compatible histories.

---

Numerical trace: C01/C02 (cuttings); C25/C27/C30 (body units and bounds); C48 (zero-delay step
contours); C33 (minimum assumed offsets); C28/C40 (Oman comparison); C49 (Oman-inclusive shape check); half-rate bound 430.98 Ma from `studies/f3/models/loop3/out/suppression_sensitivity.csv` (B2, main, primary, flat, 0.5), not yet a ledger value; C24/C45/C51 (Libyan model,
time support and unqualified block sensitivity). Clock intervals and source identities are traced in
the frozen article's Introduction and calibration account. The body is a reconstruction draft;
`studies/f3/manuscript/text/`, the ledger, models and generators retain their frozen versions.
