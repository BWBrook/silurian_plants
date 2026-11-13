# Stage 2 source checks: C45–C47 (Q1, Q2, Q5)

Codex (gpt-6.1-sol), 7 November 2026, at stage-1 base `2c293fa`.

## C45: temporal support, supported

Filtering `models/f3/out/m2_units.csv` to LY-MZ-CU, stage allocation, chart-code,
non-excluded rows and known outcomes gives 87 cuttings: 59 reference (51 positive),
28 older zeros. The latter divide into 10 Darriwilian (D1-200 three, H2-NC186 seven),
13 Katian–Hirnantian and five Hirnantian. Eighteen are wholly younger than 459.1 Ma;
only the ten Darriwilian cuttings have possible support before it. This confirms C45.
`models/f3/loop3/murzuq_stage2.py` writes the per-sample enclosure and grouped table.

The independent-uniform stage model assigns only 0.9/11.2 of each Darriwilian sample
as exposure to 459.1–443.1 Ma. This is exposure under that model, not ten point-dated
observations preceding the maximum. The time-by-well panel shows full intervals.

## C46: original maximum rationale, supported

The parent read Morris et al. (2018) SI node 110 in the held PDF, and the reply in
PubMed Central, <https://pmc.ncbi.nlm.nih.gov/articles/PMC6187173/>. The reply is
DOI 10.1073/pnas.1812816115; Crossref/publication identity agrees with Claude's audit.
Node 110 explicitly sets a 469 Ma minimum and 515.5 Ma soft maximum. It locates the
latter at the approximate base of the Olenellus Biozone, beneath the possible Rome
Formation cryptospores. The reply explicitly uses older marine algal cysts as a
preservation control and explains the maximum through occurrence, absence and
stratigraphic structure. Claude's correction accurately restores this published
argument. The repository has not supplied the sampling frame that would quantify
its non-detection probability. C46 is supported as a source account, with those limits.

## C47: older Cooksonia anchor, supported conditionally

The parent read Hooper et al. (2026) Supplementary Table 4 in the held ESM PDF,
including the crown-tracheophyte maximum paragraph: 430.5 + 0.7 = 431.2 Ma,
from the historical Homerian base and the Irish Cloncannon record. That table's
argument names the Irish record; it does not name C. barrandei.

Libertín et al. (2018), the held main paper's type-horizon account and its supplementary
geological setting, assign C. barrandei to the Monograptus belophorus Biozone,
middle Sheinwoodian. The fertile material's horizon is inferred from the shared slab
and box fauna/lithology; the relocated horizon supplied sterile cooksonioid fragments.
This is older source evidence with an explicit correlation uncertainty, rather than
a newly dated fertile specimen. Applying the same stage-enclosure rule gives a
Sheinwoodian outer base of 432.9 Ma on ICS v2024/12; adding its 1.2 Myr boundary
uncertainty gives 434.1 Ma, 2.9 Myr older than the published 431.2 Ma maximum.
This compares an updated-scale outer enclosure with the published historical value;
it does not assign that number to the fossil-bearing biozone or a crown node.

Thus C47's 'up to about 3 Myr' is supported as a conditional outer-envelope comparison.
Neither the specimens' total-group interpretation nor this arithmetic establishes a
crown-tracheophyte minimum or predicts how a clock posterior would move.

Source PDFs remain private, with existing locators in `2026-11-07-m1-rationale.md`,
`2026-10-28-m3-fossil-basis.md` and `library/closed.tsv`; no source text was added here.
