# C59: independent later-find placement check

Codex, 14 November 2026. Bounded review at `1a399f6`. This audit reconstructs
the finding units and placement calculations without importing `rulers.py`,
`combined_rulers.py` or their functions. No numerical output or manuscript file
was changed. The parent reviewer owns integration and the ledger disposition.

## Finding units and intervals

Starting from `studies/f3/data/macro/horizons_reviewed.csv`, I selected the
source-declared main/all reading, eligible-primary B2 rows and independently
grouped them using the published unit rules:

- Locality plus age group gives 50 units, exactly matching every unit, age
  enclosure and member-ID set in `out/primary_unit_membership.csv`. Of these,
  48 are guaranteed older than the 393.47 Ma cutoff; their oldest possible
  age is 426.7 Ma.
- Region plus the stage containing the age-range midpoint gives 19 units,
  matching the canonical region-stage treatment. All 19 are guaranteed in
  the window.
- There are 13 locality-age units whose complete age enclosure lies in
  419.62–426.7 Ma (Gorstian–Pridoli), and the same 13 lie wholly in
  419.62–425.0 Ma (Ludfordian–Pridoli). They form six canonical region-stage
  units. The script's shortcut of distinct region/minimum/maximum triples
  happens to give the same six for this inventory; the canonical grouping
  is midpoint-stage rather than that shortcut in general.
- Three other locality-age units have positive-length age overlap with
  either interval, giving a possible true count of 13–16. The corresponding
  canonical regional count can be 6–7. Units whose ranges merely touch the
  419.62 Ma boundary from the younger side have no positive-probability
  overlap under the assumed continuous-age model and are excluded from
  these maximum-count statements.

The 13 guaranteed units comprise nine Pridoli-range finds and four
Ludfordian–Pridoli Bathurst finds, spread over Baltica, Kazakhstania,
peri-Gondwana Europe, Laurentia, South China and South America. Thus the
comparison uses a global body record against a North American rock proxy;
it is a check of transferring that proxy to global finding, not a check of
actual North American rock availability everywhere.

## Independent integration and binomial arithmetic

I reconstructed the active North American non-marine Macrostrat column-area
function directly from `data/eprp/record/macrostrat_units_window.csv`, counting
each active column once at each age. Spore shares were reconstructed from
the numerator/denominator document counts in
`data/spores/effort_global_by_stage.csv` and the shared timescale. Searching
densities came directly from the global rows of `effort_reviewed.csv`.
Integrals were evaluated exactly over the union of all unit and stage
boundaries; products were formed pointwise before integration.

For a declared later interval I and proxy x, let

`p_I = integral_I x / integral_[c,A] x`.

Conditional on n independent draws from a fixed [c,A] window with density
proportional to x, their number in I is `Binomial(n,p_I)`. I computed the
expectation `n*p_I` and upper tail by direct summation of the binomial
probabilities. All 32 rows of `combined_rulers_placement.csv` match at the
displayed precision: share to four decimals, expected count to three
decimals, and tail to three significant figures.

Selected exact-integration results for Gorstian–Pridoli are:

| Proxy | Expected with 48 | Tail at least 13 | Expected with 19 | Tail at least 6 |
|---|---:|---:|---:|---:|
| Level | 10.22690340 | 0.20792454 | 4.04814926 | 0.20252341 |
| Rock | 0.45145727 | 6.39800404e-16 | 0.17870184 | 1.69075827e-08 |
| Spore share | 3.76223980 | 5.89502938e-05 | 1.48921992 | 0.00256985 |
| Searching | 10.08926214 | 0.19382245 | 3.99366627 | 0.19351817 |
| Rock times spore share | 0.14107785 | 2.14137879e-22 | 0.05584332 | 1.69258609e-11 |

For Ludfordian–Pridoli the level and searching expectations are 7.77129100
and 7.83210224, with tails 0.03819095 and 0.04036514 at 13 of 48. Rock and
its spore-share product have the same integrals under both splits because
the selected rock proxy is zero throughout 420.39–426.7 Ma. The zero is a
property of these database/filter/geographical inputs, not evidence of
globally absent terrestrial sediment or finding opportunities.

## Inferential conditions and required interpretation

The numerical table is correct as a **fixed-window model allocation
calculation**. Its expectations make the product's later-record mismatch
plain: approximately 0.14 allocated finds against at least 13. The following
distinctions are necessary before using its tails as tests of historical
finding processes:

1. **The window and split were selected from the record.** Here A is the
   data-derived oldest possible age, rather than a prespecified cutoff.
   Choosing A and inspecting/changing the late-Silurian split are not
   incorporated in a calibrated testing procedure. The saved tails can be
   retained as retrospective descriptive model checks, with no nominal
   repeated-sampling rejection level claimed for that selection.
2. **Conditioning on an exact oldest find is different.** If the exact
   maximum were m and its density were positive, conditioning on that
   maximum leaves n-1 independent truncated draws. For an interval
   containing m the count is `1 + Binomial(n-1,p_I(m))`, not the saved
   `Binomial(n,p_I(A))`. Here A is only an upper age support, not the exact
   maximum. Rock/product density is zero near A, so substituting A into
   the exact-maximum law is not a justified corrected test either. A
   formal conditional-age test would need its own declared treatment of
   the unknown maximum and coarsened supports.
3. **Guaranteed counts support a one-sided discrepancy, not model fit.**
   For fixed windows and valid age enclosures, the true count is at least
   the guaranteed count, so its upper-tail value is no larger. Failure to
   reject at 13 does not establish agreement for every possible count;
   the 13–16 possibilities and the alternative split affect the level and
   searching cases. Current wording should say non-rejection at the
   minimum, not empirical validation of those histories.
4. **The 19-unit binomial law is another assumption.** Merging occurrences
   into regional stage cells does not itself create independent event ages
   drawn from the same proxy-weighted density. Treating those cells as 19
   independent finds is the declared counting scenario, not an estimated
   or calibrated dependence correction. The correct six-cell membership
   does not remove that assumption.
5. **Mismatch concerns the stipulated global proportional transfer.** A
   North American rock-area series and global spore-reporting share need
   not trace global vascular-body finding. Neither the tiny descriptive
   tail nor the weak correlation of proxy series identifies the underlying
   biological or sampling cause.

**Disposition:** accept all placement arithmetic and the 13/6 minimum
counts. Retain the strong expected-count mismatch and the distinction
between pointwise tracking and a contrast between window means. Narrow any
formal rejection or calibrated-p-value reading to a retrospective allocation
diagnostic unless selection, age supports and the exact-maximum conditioning
are explicitly handled. This requires no new scientific numerical result.
