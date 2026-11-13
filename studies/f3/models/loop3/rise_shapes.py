# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///
"""Shapes of an early rise in finding rate before the oldest crown vascular-plant find (studies/f3/docs/plan-rulers.md).

With the rate level after A and r(s) relative to it before A, an ancestor age t is compatible with the
95% limit when the integral of r over [A, t] is at most K(n) = (A - c)(alpha**(-1/n) - 1). Data-selected
shapes: they show what would fit, without 95% status.

    uv run studies/f3/models/loop3/rise_shapes.py
"""

import csv
import math
from pathlib import Path

import numpy as np

from endpoint import PiecewiseRecovery, known_cutoff_summary

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
COUNTS = (48, 24, 19, 15)
CANDIDATES = (444.0, 452.0, 500.0)
TOP = 700.0


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def solve_tau(span, K):
    lo, hi = K, 1e6
    for _ in range(200):
        tau = (lo + hi) / 2
        if tau * (1 - math.exp(-span / tau)) < K:
            lo = tau
        else:
            hi = tau
    return (lo + hi) / 2


def history(c, A, rate_before):
    edges = np.r_[c, A, np.linspace(A + 0.005, TOP, 139000)]
    edges = np.unique(edges)
    mid = (edges[:-1] + edges[1:]) / 2
    dens = np.where(mid <= A, 1.0, [max(rate_before(m), 1e-300) for m in mid])
    return PiecewiseRecovery(edges, dens)


def main():
    b = next(r for r in read(OUT / "reviewed_bounds.csv")
             if (r["category"], r["reading"], r["units"], r["variant"], r["excluded_region"], r["cutoff"], r["history"])
             == ("B2", "main", "locality_age", "primary", "", "Emsian", "flat"))
    A, c = float(b["oldest_possible_ma"]), float(b["cutoff_ma"])
    alpha = 1 - float(b["confidence_conditional_on_fixed_history_iid_units"])
    rows = []
    for n in COUNTS:
        K = (A - c) * (alpha ** (-1 / n) - 1)
        t_lin = A + 2 * K
        lin = history(c, A, lambda s, t=t_lin: max(0.0, (t - s) / (t - A)) if s < t else 0.0)
        assert abs(lin.exposure(t_lin) - lin.exposure(A) - K) < 1e-3 * K, n
        older = history(c, A, lambda s, t=t_lin + 2: max(0.0, (t - s) / (t - A)) if s < t else 0.0)
        assert older.exposure(t_lin + 2) - older.exposure(A) > K, n
        row = {"n": n, "K_myr": K, "linear_oldest_ma": t_lin, "exp_limit_doubling_myr": K * math.log(2)}
        for t in CANDIDATES:
            tau = solve_tau(t - A, K)
            row[f"exp_doubling_{t:g}_myr"] = tau * math.log(2)
            ex = history(c, A, lambda s, tau=tau: math.exp(-(s - A) / tau))
            assert abs(ex.exposure(t) - ex.exposure(A) - K) < 1e-3 * K, (n, t)
            if t < 460:
                assert abs(known_cutoff_summary(n, A, ex, c).bound_ma - t) < 0.05, (n, t)
        fast = history(c, A, lambda s: math.exp(-(s - A) / (0.98 * K)))
        assert known_cutoff_summary(n, A, fast, c).status != "bounded", n
        rows.append(row)
    st = read(ROOT / "data/spores/effort_global_by_stage.csv")
    ts = {r["stage"]: float(r["base_ma"]) for r in read(ROOT / "data/timescale.csv")}
    order = [r["stage"] for r in read(ROOT / "data/timescale.csv")]
    share = {r["stage"]: int(r["n_docs_with_triletes"]) / int(r["n_docs"]) for r in st if r["stage"] in ts}
    mid = {s: (ts[s] + ts[order[order.index(s) - 1]]) / 2 for s in share}
    spore = []
    for old, young in (("Hirnantian", "Rhuddanian"), ("Homerian", "Gorstian")):
        dt, ratio = mid[old] - mid[young], share[young] / share[old]
        spore.append({"older_stage": old, "younger_stage": young, "older_share": share[old], "younger_share": share[young],
                      "midpoint_gap_myr": dt, "share_ratio": ratio, "doubling_myr": dt * math.log(2) / math.log(ratio)})
    OUT.mkdir(exist_ok=True)
    with open(OUT / "rise_shapes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()} for r in rows)
    with open(OUT / "rise_spore_share.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(spore[0]), lineterminator="\n")
        w.writeheader()
        w.writerows({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()} for r in spore)
    for r in rows:
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    for r in spore:
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()
