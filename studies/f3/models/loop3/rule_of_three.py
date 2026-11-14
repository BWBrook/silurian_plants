"""The rule of three behind the crown vascular-plant body-fossil results.

With the finding rate level after the oldest possible age A, zero delay, n finds counted in [c, A] and the
one-sided limit at alpha = 0.05, each find falls before A with probability p = R / (L + R), where L = A - c and
R is the integral of the relative earlier finding rate over [A, t]. No early find has probability (1 - p)**n,
which equals alpha when R = K = L * (alpha**(-1/n) - 1). At the later rate of n / L finds per Myr, the earlier
interval then holds m*(n) = n * (alpha**(-1/n) - 1) expected finds, which tends to ln(1/alpha) = ln 20 = 3.00
(the rule of three for zero counts; Hanley and Lippman-Hand 1983). This script checks that the steady-rate
limits, the step ratios, the linear and exponential rises, the minimum delays and the outside-measure matches
all sit at m*(n) expected early finds, using the reviewed outputs.

    python3 studies/f3/models/loop3/rule_of_three.py
"""

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
A, C, ALPHA = 426.7, 393.47, 0.05
L = A - C
COUNTS = (48, 24, 19, 15)


def read(name):
    with open(OUT / name, newline="") as f:
        return list(csv.DictReader(f))


def limit(n):
    return n * (ALPHA ** (-1 / n) - 1)


def per_myr(n):
    return n / L


def main():
    rows = []

    def add(case, n, candidate, quantity, value, early):
        assert abs(early - limit(n)) < 2e-3 * limit(n), (case, n, candidate, early, limit(n))
        rows.append([case, f"{n:g}", candidate, quantity, f"{value:.4f}", f"{early:.4f}", f"{limit(n):.4f}"])

    dial = {round(float(r["n_independent"]), 4): r for r in read("count_dial.csv")}
    rise = {int(r["n"]): r for r in read("rise_shapes.csv")}
    for n in COUNTS:
        K = L * (ALPHA ** (-1 / n) - 1)
        add("steady-rate 95% limit", n, "", "older_bound_ma", A + K, per_myr(n) * K)
        r = rise[n]
        assert abs(float(r["K_myr"]) - K) < 1e-3
        t_lin = float(r["linear_oldest_ma"])
        add("linear rise from zero at the ancestor", n, f"{t_lin:.2f}", "linear_oldest_ma", t_lin, per_myr(n) * (t_lin - A) / 2)
        tau = float(r["exp_limit_doubling_myr"]) / math.log(2)
        add("exponential rise, any older ancestor", n, "unbounded", "exp_limit_doubling_myr", tau * math.log(2), per_myr(n) * tau)
        if n in dial:
            for t in (444.0, 452.0):
                q = float(dial[n][f"later_to_earlier_{t:g}"])
                add("step: later/earlier finding-rate ratio", n, f"{t:g}", "later_to_earlier", q, per_myr(n) * (t - A) / q)
    crossing = next(r for r in read("count_dial.csv") if r["note"].startswith("crossing"))
    nx = float(crossing["n_independent"])
    add("count at which the limit reaches 431.2 Ma", nx, "431.2", "n_independent", nx, per_myr(nx) * (431.2 - A))
    for t in (444.0, 452.0):
        d = t - A - L * (ALPHA ** (-1 / 48) - 1)
        add("minimum delay at a steady rate", 48, f"{t:g}", "delay_myr", d, per_myr(48) * (t - d - A))
    for r in read("rulers_matching_n.csv"):
        n, t, q = float(r["largest_n_matched"]), float(r["candidate_ma"]), float(r["later_to_earlier"])
        if r["ruler"] in {"rock_nonmarine_area", "spores_trilete_share"}:
            rows.append([f"outside measure {r['ruler']}, at 48 finds", "48", f"{t:g}", "later_to_earlier", f"{q:.4f}",
                         f"{per_myr(48) * (t - A) / q:.4f}", f"{limit(48):.4f}"])
            add(f"outside measure {r['ruler']}, matching count", n, f"{t:g}", "largest_n_matched", n, per_myr(n) * (t - A) / q)
    rows.append(["limit as n grows", "inf", "", "ln(1/alpha)", f"{math.log(1 / ALPHA):.4f}", f"{math.log(1 / ALPHA):.4f}",
                 f"{math.log(1 / ALPHA):.4f}"])
    with open(OUT / "rule_of_three.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["case", "n", "candidate_ma", "quantity", "value", "expected_early_finds", "limit_expected_early_finds"])
        w.writerows(rows)
    print({n: round(limit(n), 4) for n in COUNTS}, "ln20", round(math.log(20), 4), f"; wrote {OUT / 'rule_of_three.csv'}")


if __name__ == "__main__":
    main()
