# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""The three nested body-fossil groups on one footing (Fable issue 3, 15 November 2026).

For land-plant bodies (B0, with and without the Oman fragments), branched plants (B1, main and
inclusive readings) and crown vascular plants (B2), reports:

- the steady-rate 95% limit from reviewed_bounds.csv and the rule-of-three requirement for ancestors
  at 444 and 452 Ma with zero delay, r = (A - c)(0.05^(-1/n) - 1)/(t - A), as 1/r;
- the steady-rate limit under each counting rule (collection, locality, locality and age, region and stage);
- the interval-wide shape test: the best finite-sample KS p over every admissible allocation of ages, for
  every inclusion state of the units straddling the cutoff (interval_feasibility.py method), written to
  groups_shape.csv; a passing allocation shows only that the history is not excluded;
- inside measures, chosen after seeing the finds, conditional benchmarks under a two-rate model: how much less often finds could have been made in a
  stretch right after the oldest find than after it, from the count observed in that stretch;
- the spore-anchored span: land plants lived before SPORE = 454.41 Ma (nominal age of the Kinnekulle
  K-bentonite above the definite Borenshult-1 triletes, claim C43). Over SPORE to 432.9 Ma the accepted
  B0 inventory holds one unit (Oman) among 76; the two-rate limit uses k = 1 of n = 76 (all draws on
  [c, SPORE]). The without-Oman sensitivity has k = 0 of 75 and equals C48's zero-delay fold at t = SPORE.
  n_other in these rows is the total unit count; n_later counts units after 432.9 Ma.

Inside measure. Conditional on the oldest unit at its true age a0, the other n units are independent
draws on [c, a0]. With finding rate rho in the stretch (b, a0] relative to 1 on [c, b], the chance that
at most k of them fall in the stretch is a binomial tail with p = rho G / (rho G + L), G = a0 - b,
L = b - c. The one-sided 95% upper limit on rho solves P(X <= k) = 0.05. The shortest G the age range
of the oldest unit admits gives the weakest limit; the longest G is also reported. k counts every other
unit whose range reaches into the stretch. Region-and-stage rows reuse that k.

Missing localities (Freshwater East, Targrove, Brown Clee Hill, Ludford Lane) are Pridoli or younger, so
they could only add later units; steady_limit_plus1 and plus4 give the limit with one or four more. For k = 0 the limit is
(L/G)(0.05^(-1/n) - 1), the rule of three in reverse.

    uv run studies/f3/models/loop3/groups.py
"""

import csv
import math
from pathlib import Path

import pandas as pd
from scipy import optimize, stats

from analysis import select_records
from histories import YOUNG, load_histories
from interval_feasibility import threshold_certificate, witness_allocation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
CANDIDATES = (444.0, 452.0)
GROUPS = (("B0", "main", "with Oman"), ("B0", "main", "without Oman"), ("B1", "main", ""),
          ("B1", "inclusive", ""), ("B2", "main", ""))
OMAN = "tail:S-w22-K12"
COUNTING = ("collection", "locality", "locality_age", "region_stage")
SPORE = 454.41


def units_for(records, category, reading, note, units="locality_age"):
    r = select_records(records, category, reading=reading, units=units)
    if note == "without Oman":
        r = r[~r.member_ids.str.contains(OMAN, regex=False)]
    return r.reset_index(drop=True)


def steady(units):
    """n guaranteed, oldest possible age and the steady-rate 95% limit c + (A - c) 0.05^(-1/n)."""
    A = float(units.max_ma.max())
    n = int((units.min_ma >= YOUNG).sum())
    return n, int((units.max_ma > YOUNG).sum()), A, YOUNG + (A - YOUNG) * 0.05 ** (-1 / n)


def check_reviewed(category, reading, note, units, limit):
    variant = "without_oman_fragments" if note == "without Oman" else "primary"
    rows = [r for r in csv.DictReader(open(OUT / "reviewed_bounds.csv"))
            if (r["category"], r["reading"], r["units"], r["variant"], r["excluded_region"], r["cutoff"],
                r["history"]) == (category, reading, units, variant, "", "Emsian", "flat")]
    if rows:
        assert abs(float(rows[0]["older_bound_ma"]) - limit) < 1e-6, (category, reading, note, units)
    return bool(rows)


def m_star(n):
    return 0.05 ** (-1 / n) - 1


def shape(units, recovery):
    """Best KS p and feasibility for every inclusion state of the units straddling the cutoff."""
    possible = units[units.max_ma > YOUNG].copy()
    possible["recorded_min_ma"] = possible.min_ma
    guaranteed = possible[possible.min_ma >= YOUNG]
    partial = possible[possible.min_ma < YOUNG].sort_values("unit_id").reset_index(drop=True)
    out = {}
    for mask in range(2 ** len(partial)):
        sel = pd.concat([guaranteed, partial.iloc[[i for i in range(len(partial)) if mask & (1 << i)]]],
                        ignore_index=True)
        sel["min_ma"] = sel.min_ma.clip(lower=YOUNG)
        _, summary, lower, upper = witness_allocation(sel, recovery)
        _, feasible, _ = threshold_certificate(lower, upper, "finite_sample")
        out[f"{mask:0{len(partial)}b}" if len(partial) else "none"] = (len(sel), summary["witness_finite_sample_p"], feasible)
    return out


def rho_upper(n, k, gap, later):
    if k == 0:
        return later / gap * m_star(n)
    f = lambda rho: stats.binom.cdf(k, n, rho * gap / (rho * gap + later)) - 0.05  # noqa: E731
    return optimize.brentq(f, 1e-9, 1e3)


def inside(units, edge, n_other):
    """Stretch from the oldest unit's youngest possible age down to `edge`, against [c, edge].
    The longest-gap variant puts the oldest unit at its oldest possible age."""
    oldest = units.loc[units.max_ma.idxmax()]
    others = units.drop(index=oldest.name)
    others = others[others.min_ma >= YOUNG]
    assert len(others) == n_other, (len(others), n_other)
    k_max = int((others.max_ma > edge + 1e-9).sum())
    k_min = int((others.min_ma >= edge - 1e-9).sum())
    gap = oldest.min_ma - edge
    later = edge - YOUNG
    rho = rho_upper(n_other, k_max, gap, later)
    return oldest, k_min, k_max, gap, later, rho


def main():
    records = pd.read_csv(ROOT / "studies/f3/data/macro/horizons_reviewed.csv")
    histories = load_histories()
    table, insides, shapes = [], [], []
    for category, reading, note in GROUPS:
        u = units_for(records, category, reading, note)
        n, n_poss, A, lim = steady(u)
        by_rule = {k: steady(units_for(records, category, reading, note, k)) for k in COUNTING}
        assert all(v[2] == A for v in by_rule.values())
        n_rs, lim_rs = by_rule["region_stage"][0], by_rule["region_stage"][3]
        checked = [check_reviewed(category, reading, note, k, v[3]) for k, v in by_rule.items()]
        req = {}
        for t in CANDIDATES:
            for lab, cnt in (("all", n), ("region_stage", n_rs)):
                req[(t, lab)] = (t - A) / ((A - YOUNG) * m_star(cnt)) if t > A else float("nan")
        sh = {h: shape(u, histories[h]) for h in histories}
        label = f"{category} {reading} {note}".strip()
        shapes += [{"group": label, "history": h, "partial_inclusion_mask": m, "n": v[0], "best_p": f"{v[1]:.3g}",
                    "feasible": v[2]} for h in histories for m, v in sh[h].items()]
        table.append({
            "category": category, "reading": reading, "variant": note or "primary",
            "n_guaranteed": n, "n_possible": n_poss, "n_region_stage": n_rs,
            "oldest_possible_ma": f"{A:g}", "steady_limit_ma": f"{lim:.4f}",
            "steady_limit_region_stage_ma": f"{lim_rs:.4f}",
            **{f"n_{k}": v[0] for k, v in by_rule.items() if k not in ("locality_age", "region_stage")},
            **{f"steady_limit_{k}_ma": f"{v[3]:.4f}" for k, v in by_rule.items() if k not in ("locality_age", "region_stage")},
            "steady_limit_plus1_ma": f"{YOUNG + (A - YOUNG) * 0.05 ** (-1 / (n + 1)):.4f}",
            "steady_limit_plus4_ma": f"{YOUNG + (A - YOUNG) * 0.05 ** (-1 / (n + 4)):.4f}", "matches_reviewed_bounds": ";".join(map(str, checked)),
            **{f"fold_{int(t)}_{lab}": f"{v:.4f}" for (t, lab), v in req.items()},
            "n_inclusion_states": len(sh["flat"]),
            **{f"shape_best_p_{h}": f"{max(v[1] for v in sh[h].values()):.3g}" for h in histories},
            **{f"shape_states_pass_{h}": sum(v[2] for v in sh[h].values()) for h in histories},
        })
    pd.DataFrame(table).to_csv(OUT / "groups.csv", index=False, lineterminator="\n")
    pd.DataFrame(shapes).to_csv(OUT / "groups_shape.csv", index=False, lineterminator="\n")

    cases = (("B0", "main", "with Oman", 432.9, "gap after the Oman fragments"),
             ("B1", "inclusive", "", 432.9, "gap after Zbrza"),
             ("B1", "main", "", 426.7, "Wenlock after C. barrandei"))
    for category, reading, note, edge, label in cases:
        u = units_for(records, category, reading, note)
        n_other = steady(u)[0] - 1
        oldest, k_min, k_max, gap, later, rho = inside(u, edge, n_other)
        level_expected = n_other * gap / (gap + later)
        insides.append({"category": category, "reading": reading, "variant": note or "primary", "stretch": label,
                        "oldest_unit": oldest.unit_id, "oldest_range_ma": f"{oldest.min_ma:g}-{oldest.max_ma:g}",
                        "stretch_ma": f"{edge:g}-{oldest.min_ma:g}", "shortest_gap_myr": f"{gap:.2f}",
                        "later_myr": f"{later:.2f}", "n_other": n_other, "k_in_stretch_min": k_min,
                        "k_in_stretch_max": k_max, "level_expected": f"{level_expected:.2f}",
                        "rate_ratio_upper95": f"{rho:.4f}", "times_less_often_at_least": f"{1 / rho:.4f}"})
        long_gap = oldest.max_ma - edge
        rho_long = rho_upper(n_other, k_max, long_gap, later)
        insides[-1].update({"longest_gap_myr": f"{long_gap:.2f}",
                            "level_expected_longest_gap": f"{n_other * long_gap / (long_gap + later):.2f}",
                            "times_less_often_at_least_longest_gap": f"{1 / rho_long:.4f}"})
        n_rs = steady(units_for(records, category, reading, note, "region_stage"))[0] - 1
        rho_rs = rho_upper(n_rs, k_max, gap, later)
        insides[-1].update({"n_other_region_stage": n_rs, "times_less_often_at_least_region_stage": f"{1 / rho_rs:.4f}"})
    for note, k in (("with Oman", 1), ("without Oman", 0)):
        u = units_for(records, "B0", "main", note)
        n_all = steady(u)[0]
        later_units = u[(u.min_ma >= YOUNG) & (u.max_ma <= 432.9 + 1e-9)]
        assert len(later_units) == n_all - k
        n_rs = steady(units_for(records, "B0", "main", note, "region_stage"))[0]
        gap, later = SPORE - 432.9, 432.9 - YOUNG
        rho, rho_rs = rho_upper(n_all, k, gap, later), rho_upper(n_rs, k, gap, later)
        if k == 0:
            assert abs(1 / rho - gap / (later * m_star(n_all))) < 1e-9
        insides.append({"category": "B0", "reading": "main", "variant": f"{note}, spore anchor",
                        "stretch": "span after the oldest definite triletes", "oldest_unit": "C43 Borenshult-1 triletes",
                        "oldest_range_ma": f">{SPORE:g}", "stretch_ma": f"432.9-{SPORE:g}", "shortest_gap_myr": f"{gap:.2f}",
                        "later_myr": f"{later:.2f}", "n_other": n_all, "n_later": len(later_units),
                        "k_in_stretch_min": k, "k_in_stretch_max": k,
                        "level_expected": f"{n_all * gap / (gap + later):.2f}", "rate_ratio_upper95": f"{rho:.4f}",
                        "times_less_often_at_least": f"{1 / rho:.4f}", "n_other_region_stage": n_rs,
                        "times_less_often_at_least_region_stage": f"{1 / rho_rs:.4f}"})
    pd.DataFrame(insides).to_csv(OUT / "groups_inside.csv", index=False, lineterminator="\n")
    print(pd.DataFrame(table).T.to_string())
    print(pd.DataFrame(insides).T.to_string())


if __name__ == "__main__":
    main()
