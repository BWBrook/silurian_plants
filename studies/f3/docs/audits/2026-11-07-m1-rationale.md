# M1: the published rationale for the 515.5 Ma maximum (Q2, Q5)

Claude Opus 5.5, 7 November 2026, prompted by the independent GPT-6 Pro review of `60c406b` (R1). Sources
read in this task:

- Morris et al. (2018), PNAS 115: E2274–E2283, https://doi.org/10.1073/pnas.1719588115, main text
  (`library/closed/morris2018_firststudy.pdf`) and SI Appendix, node 110
  (`library/closed/morris2018_firststudy_SI1.pdf`);
- Morris et al. (2018), "Reply to Hedges et al.: Accurate timetrees do indeed require accurate
  calibrations", PNAS 115: E9512–E9513, https://doi.org/10.1073/pnas.1812816115 (PubMed Central
  PMC6187173, read through its HTML text).

## What the sources say

**Where the number comes from (SI, node 110).** The soft maximum "must encompass all total group
Embryophyta, including all cryptospores". The oldest deposits with probable non-marine palynomorphs are
Middle Cambrian (Stage 5: Conasauga Group, Tennessee; Bright Angel Shale, Arizona). Cryptospores had been
reported from the underlying Rome Formation, correlated to the *Olenellus* Biozone (Stage 4). The base of
that biozone, about 515.5 Ma, is the maximum. So 515.5 Ma is placed below the oldest *possible* total-group
records, by design. The minimum (469 Ma) is the Dapingian *Tetrahedraletes* cf. *medinensis* from
Argentina.

**Why an absence there counts (main text).** The authors argue that land-plant spores occur commonly in
marine palynomorph assemblages and share the fossilisation and sampling potential of acritarchs. The
oldest possible embryophyte records are preceded by thick sequences with marine palynomorphs only, which
show that conditions for preserving embryophyte remains existed; the absence of land-plant spores there is
therefore taken as evidence that embryophytes were absent. They used this to discount analyses without the
embryophyte calibration.

**The reply.** It restates the same argument: the maximum was set from occurrence, absence and stratigraphic
structure. Marine algal cysts, made of sporopollenin and known back into the Proterozoic, act as a
preservation control; where cysts occur without land-plant spores, the absence of spores is informative.

## What we got wrong (Q5)

Our manuscript (abstract and §3.1, through `60c406b`) said the 515.5 Ma maximum "rests on the affinity of
Cambrian spore-like fossils ... not on sampled absence", and that it "is a judgement about affinity". The
published rationale has two parts: affinity sets where the bound is placed, and a qualitative
preservation-control argument from older marine-palynomorph-only sequences supplies the absence. We
described one part and called the maximum untestable as an absence. Our further point, that the Stage 4
material is younger than 515.5 Ma, is not a criticism: the maximum is meant to lie below the oldest
possible records.

## What remains true

- No assessed source supplies an enumerated, comparably searched pre-515.5 Ma frame with sample-level
  target and control counts (C16). We therefore cannot put a controlled non-detection probability on the
  argument.
- The control establishes that sporopollenin-walled microfossils survived and were recovered. It does not
  by itself establish equal terrestrial delivery to marine basins, equal geographic coverage of
  terrestrial source areas, equal preparation and search sensitivity for small cryptospores, or that the
  earliest producers made recognisable dispersed spores. These are the observation-model links the F3
  framework separates.
- The affinity part is unchanged: the three sources assessed for the Stage 4 material do not accept it as
  embryophyte (C15).

## Disposition

Rewrite §3.1, the abstract, the brief, Fig. 2 and `mapping.csv` to state the maximum as affinity plus a
qualitative preservation-control argument, and the study's result as: that argument cannot be quantified
from the assembled material, and its unquantified links are delivery, coverage, search sensitivity and
character production. Ledger: new claim C46.
