"""How fast could crown vascular-plant finding have changed after the oldest possible age A?

Post hoc (14 November 2026, after the placement check of C59), a guide without confidence level for the
history as a whole. Inputs are the C59 placement counts: finds whose whole age range lies in a late-Silurian
interval, a guaranteed minimum. Reports, for each interval and counting rule:

- the one-sided 95% Clopper-Pearson lower bound on the interval's share of later-window finds, divided by
  the share a level rate gives (the least relative rate there compatible with the minimum count);
- the fastest exponential change through the later window, rate proportional to exp(g u) with u Myr after
  A, that still gives P(at least the observed count) >= 0.05, as the factor exp(g L) between the rate at
  the cutoff and at A (above 1 a rise towards the present, below 1 a fall);
- the regions represented among the late-Silurian finds.

The oldest find (two Australian units, 426.7-393.47 Ma) lies in none of the late-Silurian counts, so A does
not enter them by construction.

    python3 studies/f3/models/loop3/switch_reading.py
"""

import csv
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
A, C = 426.7, 393.47
L = A - C
LOCHKOVIAN_BASE, LUDFORDIAN_BASE = 419.62, 425.0
INTERVALS = {"Gorstian-Pridoli": (LOCHKOVIAN_BASE, A), "Ludfordian-Pridoli": (LOCHKOVIAN_BASE, LUDFORDIAN_BASE)}


def tail(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def share_exp(lo, hi, g):
    u1, u2 = A - hi, A - lo
    if abs(g) < 1e-12:
        return (u2 - u1) / L
    return (math.exp(g * u2) - math.exp(g * u1)) / (math.exp(g * L) - 1)


def main():
    rows = list(csv.DictReader(open(OUT / "primary_unit_membership.csv")))
    finds = [r for r in rows if r["category"] == "B2" and r["reading"] == "main"
             and float(r["min_ma"]) >= C and float(r["max_ma"]) <= A + 1e-9]
    assert len(finds) == 48
    out = []
    for name, (lo, hi) in INTERVALS.items():
        late = [r for r in finds if float(r["min_ma"]) >= lo and float(r["max_ma"]) <= hi + 1e-9]
        assert not any(float(r["max_ma"]) == A for r in late)
        regions = sorted({r["region"] for r in late})
        cells = len({(r["region"], r["min_ma"], r["max_ma"]) for r in late})
        level = (hi - lo) / L
        for counting, n, k in (("locality_age", 48, len(late)), ("region_stage", 19, cells)):
            p_lo = bisect(lambda p: tail(n, k, p) - 0.05, 1e-9, k / n)
            g_max = bisect(lambda g: tail(n, k, share_exp(lo, hi, g)) - 0.05, -1.0, 1.0)
            out.append([name, f"{lo:g}-{hi:g}", counting, n, k, f"{level:.4f}", f"{p_lo:.4f}", f"{p_lo / level:.3f}",
                        f"{tail(n, k, level):.4f}", f"{math.exp(g_max * L):.3f}", len(regions), ";".join(regions)])
    with open(OUT / "switch_reading.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["interval", "interval_ma", "counting", "n", "observed_min", "level_share", "share_lower95",
                    "least_rate_relative_to_mean", "p_level", "largest_change_factor_cutoff_over_A",
                    "n_regions", "regions"])
        w.writerows(out)
    for r in out:
        print(r[:11])


if __name__ == "__main__":
    main()
