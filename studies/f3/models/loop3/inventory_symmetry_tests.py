# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "openpyxl", "scipy"]
# ///
"""Inventory-symmetry audit, Tasks 3 and 4 harness (studies/f3/docs/audits/2026-11-21-inventory-symmetry-spec.md).

For one inventory and oldest age A, reports per late-Silurian interval and counting rule:
- C59 placement: the share of each proxy's later-window integral in the interval, expected count and
  P(X >= k) for k the guaranteed minimum (units wholly inside the interval); k_max counts units reaching in;
- C60: one-sided 95% Clopper-Pearson lower share over the level share, P(X >= k) and P(X <= k) under a
  level rate, the largest exponential change factor (cutoff over A) with P(X >= k) >= 0.05, the
  expected count and the largest k that a lower-tail test at 0.05 rejects, and the regions;
- C27/C48 arithmetic: T = c + (A - c) 0.05^(-1/n) and zero-delay folds at 444 and 452 Ma.
Counting follows switch_reading.py: n from guaranteed units; region-stage k as distinct (region, min, max)
among the late locality-age units.

    uv run studies/f3/models/loop3/inventory_symmetry_tests.py S0          # reproduces the committed S0 values
"""

import math
import sys

import pandas as pd

from combined_rulers import mean
from inventory_symmetry import MACRO, OUT, dispositions, units
from rulers import rock, search, spores

C, LOCHKOVIAN_BASE, LUDFORDIAN_BASE = 393.47, 419.62, 425.0
CANDIDATES = (444.0, 452.0)


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


def run(name, la, rs, A, prox):
    g = la[(la.min_ma >= C) & (la.max_ma <= A + 1e-9)]
    gr = rs[(rs.min_ma >= C) & (rs.max_ma <= A + 1e-9)]
    L = A - C
    rows = []
    for interval, (lo, hi) in {"Gorstian-Pridoli": (LOCHKOVIAN_BASE, A), "Ludfordian-Pridoli": (LOCHKOVIAN_BASE, LUDFORDIAN_BASE)}.items():
        if hi <= lo:
            continue
        late = g[(g.min_ma >= lo) & (g.max_ma <= hi + 1e-9)]
        reach = g[(g.max_ma > lo) & (g.min_ma < hi)]
        cells = late.groupby(["region", "min_ma", "max_ma"]).ngroups
        regions = sorted(set(late.region))
        level = (hi - lo) / L

        def share_exp(gr_):
            u1, u2 = A - hi, A - lo
            return (u2 - u1) / L if abs(gr_) < 1e-12 else (math.exp(gr_ * u2) - math.exp(gr_ * u1)) / (math.exp(gr_ * L) - 1)
        for counting, n, k, kmax in (("locality_age", len(g), len(late), len(reach)), ("region_stage", len(gr), cells, None)):
            p_lo = bisect(lambda p: tail_ge(n, k, p) - 0.05, 1e-9, k / n) if k else 0.0
            g_max = bisect(lambda x: tail_ge(n, k, share_exp(x)) - 0.05, -1.0, 1.0)
            reject_le = max([j for j in range(n + 1) if tail_le(n, j, level) < 0.05], default=-1)
            base = {"set": name, "A": A, "interval": interval, "interval_ma": f"{lo:g}-{hi:g}", "counting": counting,
                    "n": n, "k_min": k, "k_max": kmax if kmax is not None else ""}
            for proxy, x in prox.items():
                share = mean(x, lo, hi) * (hi - lo) / (mean(x, C, A) * L)
                rows.append({**base, "test": "C59_placement", "proxy": proxy, "share": f"{share:.4f}",
                             "expected": f"{n * share:.3f}", "p_ge": f"{tail_ge(n, k, share):.4g}"})
            rows.append({**base, "test": "C60", "proxy": "level", "share": f"{level:.4f}", "expected": f"{n * level:.3f}",
                         "p_ge": f"{tail_ge(n, k, level):.4g}", "p_le": f"{tail_le(n, k, level):.4g}",
                         "share_lower95": f"{p_lo:.4f}", "least_rate_relative_to_mean": f"{p_lo / level:.3f}",
                         "largest_change_factor_cutoff_over_A": f"{math.exp(g_max * L):.6f}",
                         "largest_k_rejected_low": reject_le, "n_regions": len(regions), "regions": ";".join(regions)})
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
        for r in sw.itertuples():
            m = mine[mine.interval.eq(r.interval) & mine.counting.eq(r.counting)].iloc[0]
            assert (m.n, m.k_min) == (r.n, r.observed_min), (r, m)
            assert m.least_rate_relative_to_mean == f"{r.least_rate_relative_to_mean:.3f}", (r, m)
            assert abs(float(m.largest_change_factor_cutoff_over_A) - r.largest_change_factor_cutoff_over_A) < 1e-5
        pl = pd.read_csv(OUT / "combined_rulers_placement.csv")
        mine = out[out.test.eq("C59_placement")]
        for r in pl.itertuples():
            m = mine[mine.proxy.eq(r.proxy) & mine.interval.eq(r.interval) & mine.counting.eq(r.counting)].iloc[0]
            assert (m.n, m.k_min, m.share) == (r.n, r.observed, f"{r.share:.4f}"), (r, m)
            assert f"{float(m.p_ge):.3g}" == f"{r.p_at_least_observed:.3g}", (r, m)
        e = out[out.test.eq("C27_C48")].iloc[0]
        assert e.T_ma == "428.8400" and e.fold_444 == "8.0841" and e.fold_452 == "11.8224", e
        print("S0 reproduces switch_reading.csv, combined_rulers_placement.csv and C27/C48")
    tag = "_".join(names)
    out.to_csv(OUT / f"inventory_symmetry_tests_{tag}.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    main(sys.argv[1:] or ["S0"])
