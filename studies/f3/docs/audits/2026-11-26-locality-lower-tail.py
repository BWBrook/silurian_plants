"""Lower-tail level-rate probabilities at every admissible late-Silurian locality count (C60, Results h, S5.12).

The Stage 2 table reports, for each inventory, the largest lower-tail probability over admissible counts.
This script reads n and the count range from the C60 locality-age rows (natural run, Gorstian-Pridoli),
takes the level share exactly as the interval's fraction of the window from the older edge A to the
393.47 Ma cutoff, checks the largest tail against the table's p_le, and writes the exact binomial lower tail P(X <= k), upper tail P(X >= k) and two-sided probability
(twice the smaller tail, capped at 1) for every admissible k.

    python3 studies/f3/docs/audits/2026-11-26-locality-lower-tail.py
"""

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
TESTS = HERE.parents[1] / "models/loop3/out/inventory_symmetry_stage2_tests.csv"
OUT = HERE / "2026-11-26-locality-lower-tail.csv"
SETS = ("S0", "S1", "S2a", "S2b", "S3_main_ref")
CUTOFF = 393.47


def pmf(i, n, p):
    return math.comb(n, i) * p**i * (1 - p) ** (n - i)


def lower_tail(k, n, p):
    return sum(pmf(i, n, p) for i in range(k + 1))


def upper_tail(k, n, p):
    return sum(pmf(i, n, p) for i in range(k, n + 1))


def main():
    with open(TESTS, newline="") as f:
        rows = {r["set"]: r for r in csv.DictReader(f)
                if (r["test"], r["proxy"], r["run"], r["interval"], r["counting"])
                == ("C60", "level", "natural", "Gorstian-Pridoli", "locality_age") and r["set"] in SETS}
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["set", "n", "share", "expected", "k", "p_le", "p_ge", "p_two_sided"])
        for s in SETS:
            r = rows[s]
            n, a = int(r["n"]), float(r["A"])
            lo = float(r["interval_ma"].split("-")[0])
            p = (a - lo) / (a - CUTOFF)
            qs = [(k, lower_tail(k, n, p)) for k in range(int(float(r["k_min"])), int(float(r["k_max"])) + 1)]
            assert math.isclose(max(q for _, q in qs), float(r["p_le"]), rel_tol=1e-3), (s, qs, r["p_le"])
            assert math.isclose(n * p, float(r["expected"]), abs_tol=6e-4), (s, n * p, r["expected"])
            for k, q in qs:
                u = upper_tail(k, n, p)
                two = min(1.0, 2 * min(q, u))
                w.writerow([s, n, f"{p:.6f}", f"{n * p:.3f}", k, f"{q:.6g}", f"{u:.6g}", f"{two:.4g}"])
                print(s, n, k, round(n * p, 3), f"{q:.6g}", f"{u:.6g}", f"{two:.4g}")


if __name__ == "__main__":
    main()
