# C61 group bounds and interval-wide shape review

Codex, 16 November 2026. Reviewed HEAD `ed538ba9aa6917b516da171a13ec751060c693f5`.
Scope: `models/loop3/groups.py`, `out/groups.csv`, the declared horizon inputs, group
counting, steady endpoints/frontiers and shape tests. Fossil source verification and
inside/gap measures were assigned separately. This review changes no analysis or product.

## Findings requiring action

1. **“434.6 Ma or older at every count” is incorrect.** Main Results (i) and the
   abstract need to distinguish the locality–age result from the full counting
   sensitivity. The existing collection rule has 101 guaranteed B1 finds and a
   limit of **434.087039 Ma**, younger than 434.6 Ma. The four declared primary
   counting rules all give limits older than **431.2 Ma**; that narrower comparison
   holds. In the formula, the bound decreases towards 432.9 Ma as the count grows,
   so 434.6 Ma cannot be a lower limit for every possible count either.
2. **The new script omits both single-straddler inclusion states.** `shape()` at
   lines 79–90 searches only the guaranteed and all-possible inventories. The
   older interval-analysis implementation explicitly searches all four states.
   Independent verification below establishes that the omission changes none of
   C61's pass/fail conclusions for the present inputs, but the production code
   should enumerate them if the result is to remain an exhaustive reproducible
   claim. A future inventory can make the omitted states decisive.
3. **“Fits” means an admissible non-rejection witness.** The B1 steady history has
   a permissible allocation with finite-sample KS p about 0.21; the record does
   not establish model adequacy, estimate the true ages, or rank that history
   against the alternatives. Table 2's short “Yes” should carry this definition.
4. **“The calibrated check” is conditional.** The exact finite-sample reference
   is valid for fixed history, cutoff, timescale, inventory and unit rule, iid
   continuous draws, and age supports containing the true ages. Requiring failure
   for every supported allocation/inclusion state makes rejection conservative
   under those conditions. It does not restore calibration after selection of
   histories or inventories, supply joint geological-age coverage, or establish
   a calibrated dependence model for region–stage units. S5.2 and the conditions
   table must continue to govern the shorter C61 wording.

The numeric C61 endpoints, contrasts and saved shape p values checked here are
correct to the precision reported. This is a component review, not approval of
the complete C61 source/inventory and interpretation claim.

## Independent unit reconstruction and closed forms

Read `studies/f3/data/macro/horizons_reviewed.csv` with the standard-library CSV
reader; retained the declared reading, category, eligible-primary flag and ages
reaching above c = 393.47 Ma. Independently grouped by locality plus recorded
age-group, or by region and the stage containing each row's midpoint, obtaining
stage intervals directly from `data/timescale.csv`. For each group, used the
maximum of the member lower ages and maximum of the member upper ages. Removed
the entire Oman-containing unit for the declared no-Oman sensitivity. Compared
all member-ID sets and age supports against `analysis.select_records`: exact
agreement, not merely matching totals. No source-level membership verification
is implied by this comparison.

Independently calculated

\[
 U=c+(A-c)\exp[-\log(0.05)/n],\qquad
 F(t)=\frac{t-A}{(A-c)\operatorname{expm1}[-\log(0.05)/n]}.
\]

Every saved numeric endpoint/frontier cell in `groups.csv` agrees at its stated
precision. “No factor” below means t is not older than A; the equation is not an
older-ancestor extension in that case.

| Group | Certain / possible locality–age units | Region–stage units | A (Ma) | U (Ma) | Region–stage U (Ma) | F(444), F(452) | Region–stage factors |
|---|---:|---:|---:|---:|---:|---|---|
| B0 +Oman | 76 / 78 | 31 | 452.8 | 455.185345 | 458.819619 | No factor | No factor |
| B0 −Oman | 75 / 77 | 30 | 432.9 | 434.506834 | 437.040691 | 6.907996, 11.886731 | 2.680712, 4.612757 |
| B1 main | 69 / 71 | 29 | 432.9 | 434.649615 | 437.190979 | 6.344252, 10.916686 | 2.586822, 4.451198 |
| B1 inclusive | 73 / 75 | 32 | 445.2 | 447.367027 | 450.276714 | No factor, 3.137940 | No factor, 1.339449 |
| B2 main | 48 / 50 | 19 | 426.7 | 428.840006 | 432.375017 | 8.084090, 11.822397 | 3.048449, 4.458137 |

For B1 main, adding one through four later independent units gives limits
434.624082, 434.599283, 434.575188 and 434.551766 Ma. The complete four-rule
primary count comparison, independently reconstructed, is:

| Counting rule | Guaranteed count | Steady upper limit (Ma) |
|---|---:|---:|
| Collection | 101 | 434.087039 |
| Locality–age | 69 | 434.649615 |
| Locality | 67 | 434.703019 |
| Region–stage | 29 | 437.190979 |

These are limits on the start of the declared recoverable category under the
assumed recording history. They are not evidence that the category actually
started before 431.2 Ma, nor posterior 95% calibration probabilities for a crown
ancestor. Range containment and the use of A as an oldest possible age matter.

## Independent interval-wide shape verification

The independent route imported none of `analysis`, `histories`, `endpoint` or
`interval_feasibility`. It reconstructed unit supports and piecewise cumulative
histories from the CSV inputs. It shared SciPy's finite KS distribution with the
production implementation, so this is an independent feasibility/statistic
check, not an independent implementation of the KS probability distribution.

For a trial discrepancy D and trial maximum exposure M, rank j among the n−1
conditional ages must lie in

\[
 [\max(0,j/(n-1)-D),\min(1,(j-1)/(n-1)+D)]\,M.
\]

A fossil's supported exposure interval therefore allows a contiguous range of
rank slots. A final slot represents the profiled maximum M. Rather than invoking
the production sparse bipartite matching or optimiser, the independent code
solves this interval-slot assignment by **earliest-deadline scheduling**. It
exhausts every event point and intervening open cell at which an allowed slot
can appear/disappear as M varies. This gives an exact continuous-M feasibility
test up to floating-point tolerance, not a grid search. The points are ratios of
support endpoints to rank-band edges, plus endpoints for the maximum slot.

All five groups have the same two cutoff straddlers: Trout Valley
(`pbdb:10614;pbdb:10617`) and Shanda (`pbdb:35721`), each 387.95–399.5 Ma.
Every inclusion subset was tested. All 120 group × history × inclusion-state
finite-sample threshold decisions agree with the saved aggregate decisions.
All 60 saved guaranteed/all-possible optimum p values were independently
bounded within their three-significant-digit rounding intervals by checking
feasibility on both sides of each p interval. For every passing construction,
the code checked all exposure supports and recomputed the two-sided KS statistic
directly from the sorted constructed ages/exposures.

| Group | Flat | PBDB all | PBDB plant-excluded | Decline 25 | Decline 10 | PBDB-excluded × decline 10 |
|---|---|---|---|---|---|---|
| B0 +Oman | Fail all four states | Fail all | Fail all | Fail all | Fail all | Fail all |
| B0 −Oman | Pass all four | Pass all | Pass all | Fail all | Fail all | Fail all |
| B1 main | Pass all four | Pass all | Pass all | Fail all | Fail all | Fail all |
| B1 inclusive | Fail all four | Fail all | Fail all | Fail all | Fail all | Fail all |
| B2 main | Pass all four | Pass all | Pass all | Pass only with both straddlers | Fail all | Pass with either or both straddlers |

Thus the interval-wide change from the B1 midpoint failure to an admissible
steady-history witness is real. Its declining histories fail for every supported
age allocation in every cutoff inclusion state. All six histories fail for
the declared B0+Oman and B1-inclusive inventories. This remains a check of those
six histories under locality–age independence; it does not reject arbitrary
finding histories or establish the same verdict under coarser counts.

### Reproducible independent verifier

From the repository root, pass the following block to
`uv run --with numpy --with scipy python -u -`. It writes no project output.
The final optional witness print reconstructs a B1-main flat-history witness
near the reported p interval, including its maximum, D, p and support slack.
The verification run completed in about one second after imports.

```python
import csv, math, heapq
import numpy as np
from scipy.stats import kstwo
from scipy.optimize import brentq

c, domain = 393.47, 469.4
rows = list(csv.DictReader(open('studies/f3/data/macro/horizons_reviewed.csv')))
eff = sorted((x for x in csv.DictReader(open(
    'studies/f3/data/macro/effort_reviewed.csv')) if x['region'] == 'global'),
    key=lambda x: float(x['young_ma']))
edges = np.unique(np.r_[np.arange(c, domain, .05),
    [float(x['young_ma']) for x in eff],
    [float(x['old_ma']) for x in eff], domain])
mid = (edges[:-1] + edges[1:]) / 2
j = np.searchsorted([float(x['old_ma']) for x in eff], mid)
allw = np.array([float(x['all_density_per_myr']) for x in eff])[j]
exw = np.array([float(x['plant_excluded_density_per_myr']) for x in eff])[j]
rates = dict(flat=np.ones(len(mid)), pbdb_all=allw,
    pbdb_plant_excluded=exw, decline25=np.exp(-(mid-c)/25),
    decline10=np.exp(-(mid-c)/10),
    pbdb_excluded_decline10=exw*np.exp(-(mid-c)/10))

def exposure(ages, w):
    cumul = np.r_[0, np.cumsum(np.diff(edges)*w)]
    ind = np.minimum(np.searchsorted(edges, ages, side='right')-1, len(w)-1)
    return cumul[ind] + (ages-edges[ind])*w[ind]

def units(cat, reading, note):
    group = {}
    for x in rows:
        if (x['reading'] not in ('all', reading) or x[cat.lower()] != 'True'
            or x['eligible_primary'] != 'True' or float(x['max_ma']) <= c):
            continue
        group.setdefault(x['locality']+'|'+x['age_group'], []).append(x)
    if note == 'without Oman':
        group = {k: v for k, v in group.items() if not any(
            x['horizon_id'] == 'tail:S-w22-K12' for x in v)}
    return [(k, max(float(x['min_ma']) for x in v),
        max(float(x['max_ma']) for x in v)) for k, v in sorted(group.items())]

def schedule(L, U, D):
    n, m = len(L), len(L)-1
    if D < 1/(2*m)-1e-13:
        return None
    lb = np.maximum(np.arange(1, m+1)/m-D, 0)
    ub = np.minimum(np.arange(m)/m+D, 1)
    loM, hiM = max(L), max(U)
    with np.errstate(divide='ignore', invalid='ignore'):
        pts = np.r_[loM, hiM, (np.unique(L)[:, None]/ub).ravel(),
            (np.unique(U)[:, None]/lb).ravel(), L, U]
    pts = np.unique(pts[np.isfinite(pts) & (pts >= loM-1e-12)
        & (pts <= hiM+1e-12)])
    cand = np.unique(np.r_[pts, (pts[1:]+pts[:-1])/2])
    aa = np.searchsorted(ub, L[None, :]/cand[:, None]-2e-12, side='left')
    bb = np.searchsorted(lb, U[None, :]/cand[:, None]+2e-12, side='right')-1
    bb = np.where((L[None, :] <= cand[:, None]+2e-12)
        & (U[None, :] >= cand[:, None]-2e-12), n-1, bb)
    for z, (a, b) in enumerate(zip(aa, bb)):
        if np.any(a > b) or np.any(a >= m):
            continue
        order, nexti, heap, picked = np.argsort(a, kind='stable'), 0, [], []
        for slot in range(n):
            while nexti < n and a[order[nexti]] <= slot:
                i = int(order[nexti])
                heapq.heappush(heap, (int(b[i]), i))
                nexti += 1
            if not heap:
                break
            deadline, i = heapq.heappop(heap)
            if deadline < slot:
                break
            picked.append(i)
        else:
            return cand[z], picked
    return None

def inverse_p(p, m):
    return brentq(lambda d: kstwo.logsf(d, m)-math.log(p),
        1e-12, .99999, xtol=1e-14)

def check_witness(found, L, U):
    M, picked = found
    n, m = len(L), len(L)-1
    values = np.empty(n)
    for slot, i in enumerate(picked):
        values[i] = M if slot == n-1 else np.clip(
            (slot+.5)/m*M, L[i], min(U[i], M))
    assert np.all(values >= L-1e-10) and np.all(values <= U+1e-10)
    ss = np.sort(values)
    q = ss[:-1]/ss[-1]
    D = max(np.max(np.arange(1, m+1)/m-q), np.max(q-np.arange(m)/m))
    p = kstwo.sf(D, m)
    assert p >= .05-1e-8
    return M, D, p, min(np.min(values-L), np.min(U-values))

saved = list(csv.DictReader(open('studies/f3/models/loop3/out/groups.csv')))
checks = 0
for row in saved:
    cat, reading, note = row['category'], row['reading'], row['variant']
    u = units(cat, reading, note)
    guaranteed = [x for x in u if x[1] >= c]
    partial = [x for x in u if x[1] < c]
    assert len(partial) == 2
    for history, w in rates.items():
        verdicts = []
        for mask in range(4):
            selected = guaranteed + [x for i, x in enumerate(partial)
                if mask & (1 << i)]
            L = exposure(np.array([max(c, x[1]) for x in selected]), w)
            U = exposure(np.array([x[2] for x in selected]), w)
            scale = max(U)
            L, U = L/scale, U/scale
            m = len(L)-1
            found = schedule(L, U, kstwo.ppf(.95, m))
            verdicts.append(found is not None)
            checks += 1
            if mask in (0, 3):
                key = 'guaranteed' if mask == 0 else 'possible'
                ptext = row[f'shape_p_{history}_{key}']
                p = float(ptext)
                places = 2-math.floor(math.log10(p))
                delta = .5*10**(-places)
                plow, phigh = max(1e-300, p-delta), min(1-1e-12, p+delta)
                assert schedule(L, U, inverse_p(phigh, m)) is None
                good = schedule(L, U, inverse_p(plow, m))
                assert good is not None
                if cat == 'B1' and reading == 'main' and history == 'flat' and mask == 0:
                    print('B1 flat witness M,D,p,normalised_support_slack:',
                        check_witness(good, L, U))
            if found is not None:
                check_witness(found, L, U)
        assert any(verdicts) == (row['shape_any_pass_'+history] == 'True')
        print(cat, reading, note, history, verdicts)
print(checks, 'threshold checks; 60 independently bounded saved optimum p values')
```

The verifier's probability inversion uses `kstwo.logsf` and root finding;
`kstwo.isf` alone loses precision for saved p values near 10⁻¹⁷. That issue was
in the temporary verifier's first attempt, not in the production results.

Executed the fenced verifier itself after saving this audit: all assertions
passed. Its independently constructed B1-main flat witness has normalised
maximum exposure 0.9472668002164835, D = 0.1265907745672068,
p = 0.20750000000000368, with minimum support slack zero (some allocations lie
on permitted interval endpoints). The witness is deliberately at the lower
rounding edge, not a claim of a newly estimated optimal p or true fossil ages.
