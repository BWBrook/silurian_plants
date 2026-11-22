# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "openpyxl", "scipy"]
# ///
"""Inventory-symmetry audit, Tasks 3 and 4 harness (studies/f3/docs/audits/2026-11-21-inventory-symmetry-spec.md).

For one inventory and oldest age A, reports per late-Silurian interval and counting rule, under the
counting and tail rules of S3-A15 and S3-A16 (2026-11-21-inventory-symmetry-s3-rules.md):
- n is conditioned on the guaranteed window inventory (units with min >= 393.47 and max <= A). Every test is
  evaluated at each admissible (n, k): at locality-age n is fixed and k runs from units wholly inside the
  interval (k_min) to units reaching into it (k_max); at region-stage each unit reaching into the interval
  without lying wholly inside it is placed in every stage its range allows, which changes cells and hence
  n and k jointly, while other units keep their midpoint cell. A test's p is the largest over the
  placements; an excess, a deficit or a two-sided departure is established only if every placement rejects.
  The two-sided p is twice the smaller one-sided tail.
- Counting rules: locality_age; region_stage (cells = region x stage of guaranteed locality-age units, the
  same cells in numerator and denominator); region_stage_named (the same, omitting the pooled codes
  "multiple" and "unknown"); region_stage_legacy (switch_reading.py's pair: n from region-stage units, k as
  distinct (region, min, max) among late locality-age units; reproduction only).
- C59 placement: each proxy's share of the later-window integral in the interval, the expected count at the
  reported n, the largest P(X >= k) over placements and the smallest count that an upper-tail test at 0.05
  rejects at the reported n.
- C60: the smallest one-sided 95% Clopper-Pearson lower share over placements, over the level share; the
  largest P(X >= k) and P(X <= k); the largest count that a lower-tail test at 0.05 rejects at the reported
  n; whether a deficit and a two-sided departure are established; the largest exponential change factor
  (cutoff over A) with P(X >= k) >= 0.05 at the reported n and k_min, as in switch_reading.py (the share is
  not monotone in the change factor for an interval short of A, so no range over placements is reported);
  and the named regions.
- C27/C48 arithmetic: T = c + (A - c) 0.05^(-1/n) and zero-delay folds at 444 and 452 Ma.

    uv run studies/f3/models/loop3/inventory_symmetry_tests.py S0          # reproduces the committed S0 values
"""

import itertools
import math
import sys

import pandas as pd

from capel_s3 import midpoint_stage
from combined_rulers import mean
from inventory_symmetry import MACRO, OUT, ROOT, dispositions, units
from rulers import rock, search, spores

C, LOCHKOVIAN_BASE, LUDFORDIAN_BASE = 393.47, 419.62, 425.0
CANDIDATES = (444.0, 452.0)
POOLED = {"multiple", "unknown"}


def tail_ge(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def tail_le(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(0, k + 1))


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def proxies():
    rock_x, _ = rock({"non-marine"})
    spore_x = spores()
    search_x, search_px = search("all_density_per_myr"), search("plant_excluded_density_per_myr")
    singles = {"rock": rock_x, "spore_share": spore_x, "search": search_x, "search_plant_excluded": search_px}
    out = {"level": lambda s: 1.0, **singles}
    for a, b in (("rock", "spore_share"), ("search", "spore_share"), ("search_plant_excluded", "spore_share")):
        out[f"{a}_x_{b}"] = (lambda xa, xb: lambda s: xa(s) * xb(s))(singles[a], singles[b])
    return out


def stage_table(A):
    t = pd.read_csv(ROOT / "data/timescale.csv").sort_values("base_ma").reset_index(drop=True)
    t["top_ma"] = t.base_ma.shift(1)
    return [(b, top) for b, top in zip(t.base_ma, t.top_ma) if b > C and top < A]


def cells(g, named):
    g = g[~g.region.isin(POOLED)] if named else g
    stage = midpoint_stage(((g.min_ma + g.max_ma) / 2).values)
    return g.assign(cell=g.region + "|" + pd.Series(stage, index=g.index).astype(str))


def placements(g, named, lo, hi, A):
    """(n, k) for every admissible stage placement of the units that reach into [lo, hi] without lying wholly
    inside it; all other units keep their midpoint cell (S3-A15)."""
    c = cells(g, named)
    inside = (c.min_ma >= lo) & (c.max_ma <= hi + 1e-9)
    edge = (c.max_ma > lo) & (c.min_ma < hi) & ~inside
    fixed = c[~edge]
    fixed_cells, fixed_late = set(fixed.cell), set(fixed.cell[inside[~edge]])
    stages = stage_table(A)
    options = [[(f"{r.region}|{b}", b <= hi + 1e-9 and top >= lo - 1e-9) for b, top in stages
                if b > r.min_ma + 1e-9 and top < r.max_ma - 1e-9] for r in c[edge].itertuples()]
    assert math.prod(len(o) for o in options) <= 10 ** 5, "too many straddler placements"
    out = set()
    for combo in itertools.product(*options):
        cs = fixed_cells | {x for x, _ in combo}
        late = fixed_late | {x for x, in_late in combo if in_late}
        out.add((len(cs), len(late)))
    return sorted(out), len(set(c.cell)), sorted(set(c.region[inside]) - POOLED)


def counts(g, rs, lo, hi, A):
    """(counting, n reported, [(n, k) admissible], regions) for each counting rule on the guaranteed units g."""
    inside = (g.min_ma >= lo) & (g.max_ma <= hi + 1e-9)
    reach = (g.max_ma > lo) & (g.min_ma < hi)
    out = [("locality_age", len(g), [(len(g), k) for k in range(int(inside.sum()), int(reach.sum()) + 1)],
            sorted(set(g.region[inside])))]
    for named in (False, True):
        pl, n_mid, regions = placements(g, named, lo, hi, A)
        out.append(("region_stage_named" if named else "region_stage", n_mid, pl, regions))
    late = g[inside]
    out.append(("region_stage_legacy", len(rs), [(len(rs), late.groupby(["region", "min_ma", "max_ma"]).ngroups)],
                sorted(set(late.region))))
    return out


def lower95(n, k):
    return bisect(lambda p: tail_ge(n, k, p) - 0.05, 1e-9, k / n) if k else 0.0


def run(name, la, rs, A, prox):
    g = la[(la.min_ma >= C) & (la.max_ma <= A + 1e-9)]
    gr = rs[(rs.min_ma >= C) & (rs.max_ma <= A + 1e-9)]
    assert cells(g, False).cell.nunique() == len(gr), (name, cells(g, False).cell.nunique(), len(gr))
    L = A - C
    rows = []
    for interval, (lo, hi) in {"Gorstian-Pridoli": (LOCHKOVIAN_BASE, A), "Ludfordian-Pridoli": (LOCHKOVIAN_BASE, LUDFORDIAN_BASE)}.items():
        if hi <= lo:
            continue
        level = (hi - lo) / L

        def share_exp(gr_):
            u1, u2 = A - hi, A - lo
            return (u2 - u1) / L if abs(gr_) < 1e-12 else (math.exp(gr_ * u2) - math.exp(gr_ * u1)) / (math.exp(gr_ * L) - 1)

        def factor(n, k):
            return math.exp(bisect(lambda x: tail_ge(n, k, share_exp(x)) - 0.05, -1.0, 1.0) * L)
        for counting, n, pl, regions in counts(g, gr, lo, hi, A):
            ns, ks = [a for a, _ in pl], [b for _, b in pl]
            p_lo = min(lower95(a, b) for a, b in pl)
            reject_le = max([j for j in range(n + 1) if tail_le(n, j, level) < 0.05], default=-1)
            base = {"set": name, "A": A, "interval": interval, "interval_ma": f"{lo:g}-{hi:g}", "counting": counting,
                    "n": n, "n_range": f"{min(ns)}-{max(ns)}", "k_min": min(ks), "k_max": max(ks),
                    "placements": len(pl)}
            for proxy, x in prox.items():
                share = mean(x, lo, hi) * (hi - lo) / (mean(x, C, A) * L)
                reject_ge = min([j for j in range(n + 1) if tail_ge(n, j, share) < 0.05], default=n + 1)
                p_ge = max(tail_ge(a, b, share) for a, b in pl)
                rows.append({**base, "test": "C59_placement", "proxy": proxy, "share": f"{share:.4f}",
                             "expected": f"{n * share:.3f}", "p_ge": f"{p_ge:.4g}",
                             "smallest_k_rejected_high": reject_ge, "excess_established": p_ge < 0.05})
            p_ge = max(tail_ge(a, b, level) for a, b in pl)
            p_le = max(tail_le(a, b, level) for a, b in pl)
            rows.append({**base, "test": "C60", "proxy": "level", "share": f"{level:.4f}", "expected": f"{n * level:.3f}",
                         "p_ge": f"{p_ge:.4g}", "p_le": f"{p_le:.4g}",
                         "largest_k_rejected_low": reject_le, "deficit_established": p_le < 0.05,
                         "two_sided_rejected_at_all_counts": all(
                             2 * min(tail_ge(a, b, level), tail_le(a, b, level)) < 0.05 for a, b in pl),
                         "share_lower95": f"{p_lo:.4f}", "least_rate_relative_to_mean": f"{p_lo / level:.3f}",
                         "largest_change_factor_cutoff_over_A": f"{factor(n, min(ks)):.6f}",
                         "n_regions": len(regions), "regions": ";".join(regions)})
    n = len(g)
    m = 0.05 ** (-1 / n) - 1
    rows.append({"set": name, "A": A, "test": "C27_C48", "counting": "locality_age", "n": n,
                 "T_ma": f"{C + (A - C) * (1 + m):.4f}",
                 **{f"fold_{int(t)}": f"{(t - A) / ((A - C) * m):.4f}" for t in CANDIDATES}})
    return rows


def main(names):
    h = pd.read_csv(MACRO / "horizons_reviewed.csv")
    disp = dispositions(h)
    prox = proxies()
    rows = []
    for name in names:
        la, rs = units(h, disp, name), units(h, disp, name, counting="region_stage")
        rows += run(name, la, rs, la.max_ma.max(), prox)
    out = pd.DataFrame(rows)
    if names == ["S0"]:
        sw = pd.read_csv(OUT / "switch_reading.csv")
        mine = out[out.test.eq("C60")]
        legacy = {"locality_age": "locality_age", "region_stage": "region_stage_legacy"}
        for r in sw.itertuples():
            m = mine[mine.interval.eq(r.interval) & mine.counting.eq(legacy[r.counting])].iloc[0]
            assert (m.n, m.k_min) == (r.n, r.observed_min), (r, m)
            assert m.least_rate_relative_to_mean == f"{r.least_rate_relative_to_mean:.3f}", (r, m)
            assert abs(float(m.largest_change_factor_cutoff_over_A) - r.largest_change_factor_cutoff_over_A) < 1e-5
        pl = pd.read_csv(OUT / "combined_rulers_placement.csv")
        mine = out[out.test.eq("C59_placement")]
        for r in pl.itertuples():
            m = mine[mine.proxy.eq(r.proxy) & mine.interval.eq(r.interval) & mine.counting.eq(legacy[r.counting])].iloc[0]
            assert (m.n, m.k_min, m.share) == (r.n, r.observed, f"{r.share:.4f}"), (r, m)
            assert f"{float(m.p_ge):.3g}" == f"{r.p_at_least_observed:.3g}", (r, m)
        e = out[out.test.eq("C27_C48")].iloc[0]
        assert e.T_ma == "428.8400" and e.fold_444 == "8.0841" and e.fold_452 == "11.8224", e
        print("S0 reproduces switch_reading.csv, combined_rulers_placement.csv and C27/C48")
    tag = "_".join(names)
    out.to_csv(OUT / f"inventory_symmetry_tests_{tag}.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    main(sys.argv[1:] or ["S0"])
