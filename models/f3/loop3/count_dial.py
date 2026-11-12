"""How the crown vascular-plant bound and the frontier depend on the number of independent finds.

Under constant recording the one-sided older bound is T(n) = c + (A - c) * alpha**(-1/n), and the
later/earlier recording ratio placing a candidate lineage age t (zero delay) on it is
(t - A) / ((A - c) * (alpha**(-1/n) - 1)). The primary, region-stage and curated unit treatments share
A and c and differ only in n, so they are three points on one curve. This script checks that against
the reviewed outputs and tabulates the curve. Treating n as an effective count of independent finds is
a reading of the closed form, not a fitted dependence model.

    python3 models/f3/loop3/count_dial.py
"""

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
BOUNDS = OUT / "reviewed_bounds.csv"
FRONTIER = OUT / "frontier.csv"
MAXIMUM = 431.2
CANDIDATES = (444.0, 452.0)


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    base = {"category": "B2", "reading": "main", "excluded_region": "", "cutoff": "Emsian", "history": "flat"}
    bounds = [r for r in read(BOUNDS) if all(r[k] == v for k, v in base.items())]
    treatments = {"primary": ("locality_age", "primary"), "region_stage": ("region_stage", "primary"),
                  "curated": ("locality_age", "curated_tail_only")}
    rows = {k: next(r for r in bounds if (r["units"], r["variant"]) == v) for k, v in treatments.items()}
    A = float(rows["primary"]["oldest_possible_ma"])
    c = float(rows["primary"]["cutoff_ma"])
    alpha = 1 - float(rows["primary"]["confidence_conditional_on_fixed_history_iid_units"])

    def bound(n):
        return c + (A - c) * alpha ** (-1 / n)

    def ratio(n, t):
        return (t - A) / ((A - c) * (alpha ** (-1 / n) - 1))

    frontier = [r for r in read(FRONTIER) if r["reading"] == "main" and r["category"] == "B2"
                and float(r["assumed_diagnostic_delay_myr"]) == 0 and r["status"] == "contour"]
    for key, r in rows.items():
        n = int(r["n_guaranteed"])
        assert float(r["oldest_possible_ma"]) == A and float(r["cutoff_ma"]) == c, key
        assert abs(bound(n) - float(r["older_bound_ma"])) < 1e-6, (key, bound(n), r["older_bound_ma"])
        for t in CANDIDATES:
            f = next(x for x in frontier if x["unit_treatment"] == key and float(x["candidate_lineage_ma"]) == t)
            assert abs(ratio(n, t) - float(f["later_to_earlier_intensity"])) < 1e-6, (key, t)

    crossing = math.log(1 / alpha) / math.log((MAXIMUM - c) / (A - c))
    marked = {int(r["n_guaranteed"]): k for k, r in rows.items()}
    OUT.mkdir(exist_ok=True)
    with open(OUT / "count_dial.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["n_independent", "older_bound_ma", "later_to_earlier_444", "later_to_earlier_452",
                    "unit_treatment", "note"])
        for n in range(10, 61):
            w.writerow([n, f"{bound(n):.4f}", f"{ratio(n, 444.0):.4f}", f"{ratio(n, 452.0):.4f}",
                        marked.get(n, ""), ""])
        w.writerow([f"{crossing:.4f}", f"{MAXIMUM:.4f}", f"{ratio(crossing, 444.0):.4f}",
                    f"{ratio(crossing, 452.0):.4f}", "", f"crossing of the {MAXIMUM} Ma maximum"])
    print(f"A={A} c={c} alpha={alpha:.4f}; 431.2 Ma crossed at n={crossing:.2f}; wrote {OUT / 'count_dial.csv'}")


if __name__ == "__main__":
    main()
