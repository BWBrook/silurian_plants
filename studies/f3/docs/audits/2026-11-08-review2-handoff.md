# GPT-6 Pro follow-up: Codex implementation and semantic reconciliation

Codex (`gpt-6.1-sol`), 8 November 2026. Base: Claude's `8a2194e`, Board 140 message 2969.
Scope: F1/F9/F10/F12, C47 verification, propagation of affected results and a cross-product semantic
read. No new molecular clocks, measurements, external correspondence or frozen qualification runs.

## Decision

**The Codex implementation tranche is complete.** The B1 source correction is implemented and
independently checked; the reproduction routes run; S2.2 is now mathematically explicit; the revised
products state their results with the governing conditions. Claude retains the agreed editorial check
of the new mathematical exposition before Barry reads the paper. Loop 3 remains closed, and this
follow-up requires no further analysis. Release/submission remain Barry's decisions.

## F1: source-backed B1 restoration

`2026-11-08-b1-restoration.md` records the primary-source check and regenerated output inventory.
Libertín's *C. bohemica* specimens and the Edwards–Rogerson Capel Horeb fertile specimens provide E3
independently of their qualified or separate E4 anatomical evidence. The main interpretations and
reading assignments now carry that E3 evidence. The sterile Lang axis remains E4-only and outside B1.
An adjacent stale card-support locator was refreshed without changing its alternative interpretation.

| B1 reading | Possible / guaranteed units | Constant bound (Ma) |
|---|---:|---:|
| Main | 71 / 69 | 434.649615 |
| Inclusive | 75 / 73 | 447.367027 |

The parent independently recounted primary membership and computed
$c+(A-c)0.05^{-1/n}$: main $A=432.9$, $n=69$; inclusive $A=445.2$, $n=73$; $c=393.47$ Ma.
Removing *C. barrandei* gives 432.272324 Ma under the main reading, a −2.377291 Myr change; the
inclusive change is +0.030728 Myr. A separate flat-plus-step exposure inversion reproduces the
main B1 tenfold scenario, 447.920156 Ma.

Nine scientific output CSVs changed, confined to B1 rows. All non-B1 rows in category-labelled output
tables are exactly unchanged, including B0/B2 bounds, allocations, shape, delay, simulation,
suppression and membership. Frontier, interval and timescale numerical tables are unchanged; their
receipts follow the updated input hashes. B2 remains 50/48 units and 428.840006 Ma. B1 simulations were
rerun at the restored counts: the overall exact-age matched range remains 0.941–0.958, while the
constant-fit/true-decline10 failure range is now 0.034–0.244.

C25/C39/C32/C52 and the C34 failure-range endpoint are updated before the products. Existing B1
influence bindings still round to −2.38 Myr. The ledger/source evidence is reverified and stamped;
unchanged B0/B2 claims are restamped because their shared CSVs also contain B1 rows.

## F2/F10 and C47: mathematical and source checks

- `2026-11-08-math-specification-review.md` verifies the finite-sample KS reference after removal of
  the maximum ($n-1$ ages), the matching diagnostic and the interval-wide rejection argument. The
  rejection is conservative under an observation model with almost-sure containment of the latent
  ages/inclusion state, fixed history/cutoff/timescale/inventory/unit rule and independent continuous
  occurrence ages. Containment failure probability delta permits only an alpha + delta size bound.
  Geological ranges have no demonstrated joint coverage. Berger–Boos is a related construction, not
  the proof that these coarsened data have error-free supports. Numbers and C49 status are unchanged.
- S2.2 now gives age-integrated unit probabilities, the joint Gamma-well likelihood, profiled nuisance
  rates and fixed delivery ratios, the exposure-weighted target, H0c/H0/H0m/H1 restrictions, the
  chord/Jensen upper envelope, the nonnegative likelihood statistic and the critical/qualification
  rule. The distinction between mean-intensity and pointwise origin/window read-outs is explicit.
  Qualification retains its frozen finite-grid scope. No model or qualification result was changed.
- `2026-11-08-c47-source-check.md` checks the original Hooper rule, Libertín's inferred Sheinwoodian
  horizon and decimal stage arithmetic independently: 431.9 vs 434.1 Ma on the current scale (2.2 Myr),
  and 434.1 vs the historical 431.2 Ma (2.9 Myr). C47 is supported with its mapping/correlation limits.

## F9/F12: public reproduction

`2026-11-08-reproduction-repairs.md` describes the implementation. `check-public` fetches the archived
PBDB input first. Byte identity remains required except for one declared optimiser CSV, where
floating-point fields have absolute tolerance 1e-9; schema, row order, identity/discrete fields and
categorical values remain exact. Receipts retain both hashes and the actual UTC run date, preserving
the historical 7 November receipts.

| Executed check | Result |
|---|---|
| `make check-public` | 63 tests pass |
| Same command in a tracked-file copy, raw PBDB input initially absent | Input fetched/hash-checked; 63 tests pass |
| `make reproduce-derived` | 65 selected CSVs pass; all byte-identical on this run |
| `make rebuild-source` | 76 selected CSVs pass; all byte-identical on this run |
| `make check-sources` | Held thesis byte count/hash and observation checks pass |
| `uv run tools/occurrences.py check` | 242 observations, 353 interpretations, 160 sources; zero problems |

The machine-readable public-check and reproduction receipts are beside this audit. The source check
also supplies the public White Rose route and expected hash when it reports a missing-source skip.
The thesis PDF remains excluded. These checks do not authenticate every palaeontological identification
or rerun the frozen F3 qualification/R pilot.

## Cross-product meaning and rendering

The parent read article results/discussion/conclusions, the new frontier caption, brief, guide and
relevant supplement against `estimands.md`, source passages and output selectors. The Silvestro
comparison matches its published genus-level occurrence/preservation analysis and quoted interval;
its posterior and this study's conditional category bound remain different objects. The agnostic
position on biological plausibility is retained. The abstract and brief preserve the primary/coarse
unit contrast and the zero-delay condition, and the Libyan result remains local and conditional.

Three additional semantic repairs emerged:

1. The frontier target is $T-d$, not the crown age $T$. Undefined combinations $T-d\le A$ were being
   drawn at a ratio of one; they are now omitted. The caption explicitly states the capped
   no-reduction display for ratios at or above one. At fixed crown age a longer assumed delay reduces
   the required recording contrast. These changes preserve every numerical table.
2. The fossil bands show category-level first-record supports
   $[\max_i \min_i,\max_i \max_i]$. Their endpoints can come from different finds, rather than one
   specimen's age range. Figure 1 and brief labels/captions now state that meaning; the support data
   are unchanged. The independent mathematical reviewer confirmed both figure repairs.
3. The conclusion now states a body-record bound younger than the maximum under its recording/unit
   assumptions, rather than treating interval agreement as support for a maximum. The brief names
   the shared well effect and describes a conditional older limit without a posterior-age reading.

All plots and borrowed supplementary diagnostics are refreshed with current input/output hashes.
The rebuilt brief is two pages, article eighteen and supplement twenty-seven. Ten affected/summary
pages were rendered and visually inspected, including both brief pages, the new equations/class table,
the interval argument/table, B1 table, conclusion, frontier and reproduction instructions. A clipped
code comment found during that inspection was shortened. The six rendered source files pass the
glyph scan; mathematical symbols render. The new methods prose received the scientific writing audit
and manual clarity check; technical tables and envelope terminology are retained deliberately.

The 52-claim numerical check, manuscript lint and citation audits pass. Fifty claims are supported and
two superseded. Claims checking verifies bindings, not these semantic conclusions.

## Remaining limits

The correct Edwards–Rogerson Capel paper was read from its public ORCA full text but is not held as a
local byte archive; its route/identity is registered without an invented hash. The similarly named local
Freshwater East paper is a different work. The evidence/recording, unit-dependence and geological-age
limits described in the paper remain; none is a request for new work before this revision can finish.

Next: Claude — check the new S2.2 exposition and final diff, then hand the revised paper to Barry.
