# C47: same-scale and historical-anchor comparisons

Codex (`gpt-6.1-sol`), 8 November 2026. Independent check of Claude's provisional C47 revision at
`8a2194e`, for Q2/Q5.

## Source and arithmetic check

The parent read the crown-tracheophyte age justification in Hooper et al.'s held Supplementary Table 4
(`41477_2026_2432_MOESM1_ESM.pdf`). It names the Irish Cloncannon *Cooksonia*, its Homerian assignment
and the historical 430.5 ± 0.7 Ma stage base, giving 431.2 Ma. It does not name *C. barrandei*.

Libertín et al. (2018), especially the held supplement's Material and Type horizon accounts, assign
*C. barrandei* to the middle Sheinwoodian *Monograptus belophorus* Biozone. The fertile slab's horizon
is inferred from associated slab/box fauna, lithology and correlation with the relocated site, where
sterile cooksonioid fragments were found. This is not a direct numerical date for the fertile slab.

Independently summing the decimal stage-base and quoted-uncertainty columns of `data/timescale.csv`
gives:

| Comparison | Arithmetic (Ma) | Meaning |
|---|---|---|
| Current-scale Homerian rule | 430.6 + 1.3 = 431.9 | ICS v2024/12 stage enclosure plus uncertainty |
| Current-scale Sheinwoodian rule | 432.9 + 1.2 = 434.1 | Same rule and current scale |
| Same-scale difference | 434.1 − 431.9 = 2.2 Myr | Difference between the two rule-based outer values |
| Comparison with published anchor | 434.1 − 431.2 = 2.9 Myr | Current alternative against the historical GTS2012 value |

This confirms the revised article, guide and estimands wording. C47 can be **supported**. The number
neither dates the slab/biozone nor establishes a crown minimum, a dated older absence or a clock-posterior
shift. An older stem record is compatible with a younger crown maximum.

## Reproduce

Read the cited source passages and sum `base_ma + base_unc_ma` for Homerian and Sheinwoodian in
`data/timescale.csv`. Decimal rather than binary floating-point arithmetic gives 431.9, 434.1, 2.2
and 2.9 exactly at their stated precision. Source acquisition/hashes remain in `library/closed.tsv`
and the existing deposit manifests; no copyrighted source text is reproduced here.
