# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "openpyxl", "scipy"]
# ///
"""Inventory-symmetry audit, Stage 2: Tasks 3, 4, 5 and 6 and the gate table
(studies/f3/docs/audits/2026-11-21-inventory-symmetry-spec.md, rules S3-A10 to S3-A24 in
2026-11-21-inventory-symmetry-s3-rules.md).

Runs every inventory at its natural oldest age and, for Task 6, with the Yea units removed (A = 425.0 Ma):
- Task 3: C59 placement and C60 through inventory_symmetry_tests.run (S3-A15, S3-A16, S3-A19);
- Task 4.1: T, m*(n), K(n), zero-delay folds and the six-history older bounds (C27, C48, C55, C58); B1 and
  B0 limits, folds and the spore-anchored requirement (C61, C62) on S0 and S1;
- Task 4.2: the Devonian-free window (c = 419.62 Ma) under all six histories, with leave-Bathurst-out;
- Task 5: the interval-wide KS feasibility over the four inclusion states (C49), S0-S2b, and B1, B0 on S1;
- the gate table (S3-A17, S3-A21 to S3-A23).
Every piece is checked against its committed S0 values (check_s0) before any output is written. It writes
only inventory_symmetry_stage2_*.csv.

    uv run studies/f3/models/loop3/inventory_symmetry_stage2.py
"""

import math
from concurrent.futures import ProcessPoolExecutor

import pandas as pd

import capel_s3
import groups
from analysis import envelope
from endpoint import known_cutoff_summary
from histories import load_histories
from inventory_symmetry import MACRO, OUT, SETS, build, dispositions, units
from inventory_symmetry_tests import C, LOCHKOVIAN_BASE, proxies, run

YEA_TAIL = {"tail:M-ghin-ghin", "tail:M-ghin-ghin-b2", "tail:M-limestone-road"}
YEA_ROWS = (124, 734, 1199)
READINGS = ("main", "f3_strict", "permissive", "capel_groups")
CANDIDATES = (444.0, 452.0)
HISTORIES = ("flat", "pbdb_all", "pbdb_plant_excluded", "decline25", "decline10", "pbdb_excluded_decline10")


def inventories():
    """(set, run, la, rs, family): rs is None for S3, whose region-stage pair has no legacy reading."""
    h = pd.read_csv(MACRO / "horizons_reviewed.csv")
    disp = dispositions(h)
    out = []
    for s in SETS:
        for run_name, ex in (("natural", None), ("bathurst_425", YEA_TAIL)):
            la = units(h, disp, s, exclude_members=ex)
            rs = units(h, disp, s, counting="region_stage", exclude_members=ex)
            if ex:
                assert la.max_ma.max() == 425.0, (s, la.max_ma.max())
            out.append((s, run_name, la, rs, "S0-S2"))
    d, _ = capel_s3.parse()
    for v in READINGS:
        for y in capel_s3.YEA_TREATMENTS:
            out.append((f"S3_{v}_{y}", "natural", capel_s3.units(d, v, yea=y), None, "S3"))
        la = capel_s3.units(d, v, exclude_rows=YEA_ROWS)
        if v == "permissive":
            assert la.max_ma.max() == 426.7
            out.append((f"S3_{v}", "noYea_unforced_426.7", la, None, "S3"))
            la = capel_s3.units(d, v, exclude_rows=YEA_ROWS + (6,))
            out.append((f"S3_{v}", "bathurst_425_forced_row6", la, None, "S3"))
        else:
            assert la.max_ma.max() == 425.0, (v, la.max_ma.max())
            out.append((f"S3_{v}", "bathurst_425", la, None, "S3"))
    la = capel_s3.units(d, "yea_literal")
    assert la.max_ma.max() == 425.0
    out.append(("S3_yea_literal", "natural", la, None, "S3"))
    la = capel_s3.units(d, "yea_literal", exclude_rows=YEA_ROWS)
    assert la.equals(capel_s3.units(d, "main", exclude_rows=YEA_ROWS)) and la.max_ma.max() == 425.0
    out.append(("S3_yea_literal", "bathurst_425", la, None, "S3"))
    return h, disp, d, out


def s3_split(name):
    """S3 set name -> (reading, Yea treatment)."""
    v = name[3:]
    for t in sorted(capel_s3.YEA_TREATMENTS, key=len, reverse=True):
        if v.endswith("_" + t):
            return v[: -len(t) - 1], t
    return v, "ref"


def s3_region_units(d, name, run_name, extra=()):
    v, y = s3_split(name)
    ex = () if run_name == "natural" else YEA_ROWS + ((6,) if "row6" in run_name else ())
    return capel_s3.units(d, v, counting="region_stage", exclude_rows=ex + tuple(extra), yea=y if not ex else "ref")


def region_units_without_bathurst(h, disp, d, name, run_name, family, la):
    _, members = bathurst_silurian(la)
    if family == "S3":
        return s3_region_units(d, name, run_name, sorted(int(m) for m in members))
    ex = (set() if run_name == "natural" else set(YEA_TAIL)) | members
    return units(h, disp, name, counting="region_stage", exclude_members=ex)


def bathurst_silurian(la):
    """Member ids of the Bathurst Island units wholly in the Silurian (S3-A24)."""
    sil = la[(la.min_ma >= LOCHKOVIAN_BASE - 1e-9) & la.unit_id.str.lower().str.contains("bathurst")]
    return sil, {m for ids in sil.member_ids for m in str(ids).split(";")}


def admissible(u, cutoff, recovery=None):
    """The jointly possible allocation with the oldest bound (S3-A25). The conservative envelope pairs the
    guaranteed count with the oldest possible age, which can come from a unit outside the guaranteed set. Here
    each straddling unit lies either outside the window or inside it at its oldest age. More units tighten
    the bound and an older A loosens it, so the candidates are the guaranteed units alone and the guaranteed
    units plus one straddling unit older than all of them. recovery None is the steady-rate formula."""
    possible = u[u.max_ma > cutoff]
    certain = possible[possible.min_ma >= cutoff]
    kc = len(certain)
    ac = certain.max_ma.max() if kc else -math.inf
    cands = ([(kc, ac)] if kc else []) + [(kc + 1, a) for a in possible[possible.min_ma < cutoff].max_ma if a > ac]
    out = []
    for k, a in cands:
        q = 0.05 ** (-1 / k) - 1
        if recovery is None:
            out.append((a + (a - cutoff) * q, "constant", k, a, [(t - a) / ((a - cutoff) * q) for t in CANDIDATES]))
        else:
            fit = known_cutoff_summary(k, a, recovery, cutoff)
            out.append((fit.bound_ma, fit.status, k, a, None))
    bound, status, k, a, _ = max(out, key=lambda x: x[0] if math.isfinite(x[0]) else math.inf)
    row = {"admissible_n": k, "admissible_A": a, "admissible_bound_ma": f"{bound:.8f}", "admissible_status": status,
           "admissible_candidates": "; ".join(f"{c[2]}@{c[3]:g}" for c in out)}
    if recovery is None:
        row.update({f"admissible_min_fold_{int(t)}": f"{min(c[4][i] for c in out):.4f}" for i, t in enumerate(CANDIDATES)})
    return row


def task4(name, run_name, la, rs_units, rs_nobath, hist):
    """Task 4.1 and 4.2 rows for one B2 inventory. rs_nobath: region-stage cells formed after removing the
    Bathurst Silurian units (Codex, 23 November)."""
    A = la.max_ma.max()
    rows = []
    for counting, u in (("locality_age", la), ("region_stage", rs_units)):
        n = len(u[(u.min_ma >= C) & (u.max_ma <= A + 1e-9)])
        q = 0.05 ** (-1 / n) - 1
        rows.append({"set": name, "run": run_name, "task": "4.1", "counting": counting, "c_ma": C, "A": A, "n": n,
                     "T_constant_ma": f"{C + (A - C) * (1 + q):.4f}", "m_star": f"{n * q:.4f}",
                     "K_myr": f"{(A - C) * q:.4f}",
                     **{f"fold_{int(t)}": f"{(t - A) / ((A - C) * q):.4f}" for t in CANDIDATES},
                     **admissible(u, C)})
        for hname in HISTORIES:
            fit, _, certain, oldest = envelope(u, hist[hname], C)
            rows.append({"set": name, "run": run_name, "task": "4.1_history", "counting": counting, "c_ma": C,
                         "A": oldest, "n": certain, "history": hname, "older_bound_ma": f"{fit.bound_ma:.8f}",
                         "status": fit.status, **admissible(u, C, hist[hname])})
    bath, _ = bathurst_silurian(la)
    variants = [("all", la, "locality_age"), ("all", rs_units, "region_stage")]
    if len(bath) > 1:
        variants.append(("bathurst_collapsed", la.drop(index=bath.index[1:]), "locality_age"))
    if len(bath):
        variants.append(("bathurst_removed", la.drop(index=bath.index), "locality_age"))
        variants.append(("bathurst_removed", rs_nobath, "region_stage"))
    for leave, u, counting in variants:
        k = int((u.min_ma >= LOCHKOVIAN_BASE - 1e-9).sum())
        Au = u.max_ma.max()
        q = 0.05 ** (-1 / k) - 1
        K = (Au - LOCHKOVIAN_BASE) * q
        base = {"set": name, "run": run_name, "task": "4.2", "counting": counting, "leave_bathurst": leave,
                "c_ma": LOCHKOVIAN_BASE, "A": Au, "n": k, "n_bathurst_silurian": len(bath)}
        rows.append({**base, "history": "constant_formula", "K_myr": f"{K:.4f}", "T_constant_ma": f"{Au + K:.4f}",
                     **{f"fold_{int(t)}": f"{(t - Au) / K:.4f}" for t in CANDIDATES},
                     **admissible(u, LOCHKOVIAN_BASE)})
        for hname in HISTORIES:
            fit, _, certain, oldest = envelope(u, hist[hname], LOCHKOVIAN_BASE)
            assert certain == k and oldest == Au
            rows.append({**base, "history": hname, "older_bound_ma": f"{fit.bound_ma:.8f}", "status": fit.status,
                         **admissible(u, LOCHKOVIAN_BASE, hist[hname])})
    return rows


def group_rows(records, label):
    """C61 and C62 quantities from groups.py's functions on one inventory's records."""
    rows = []
    for category, reading, note in groups.GROUPS[:4]:
        by_rule = {k: groups.steady(groups.units_for(records, category, reading, note, k)) for k in groups.COUNTING}
        n, _, A, _ = by_rule["locality_age"]
        n_rs = by_rule["region_stage"][0]
        row = {"set": label, "category": category, "reading": reading, "variant": note or "primary",
               "oldest_possible_ma": f"{A:g}", "n_guaranteed": n, "n_region_stage": n_rs,
               **{f"steady_limit_{k}_ma": f"{v[3]:.4f}" for k, v in by_rule.items()},
               **{f"n_{k}": v[0] for k, v in by_rule.items()}}
        for t in CANDIDATES:
            for lab, cnt in (("all", n), ("region_stage", n_rs)):
                row[f"fold_{int(t)}_{lab}"] = f"{(t - A) / ((A - C) * groups.m_star(cnt)):.4f}" if t > A else ""
        rows.append(row)
    cases = (("B0", "main", "with Oman", 432.9, "gap after the Oman fragments"),
             ("B1", "inclusive", "", 432.9, "gap after Zbrza"),
             ("B1", "main", "", 426.7, "Wenlock after C. barrandei"))
    for category, reading, note, edge, stretch in cases:
        u = groups.units_for(records, category, reading, note)
        n_other = groups.steady(u)[0] - 1
        oldest, k_min, k_max, gap, later, rho = groups.inside(u, edge, n_other)
        n_rs = groups.steady(groups.units_for(records, category, reading, note, "region_stage"))[0] - 1
        rows.append({"set": label, "category": category, "reading": reading, "variant": note or "primary",
                     "stretch": stretch, "n_other": n_other, "k_in_span": k_max,
                     "level_expected": f"{n_other * gap / (gap + later):.2f}",
                     "times_less_often_at_least": f"{1 / rho:.4f}",
                     "times_less_often_at_least_longest_gap":
                         f"{1 / groups.rho_upper(n_other, k_max, oldest.max_ma - edge, later):.4f}",
                     "times_less_often_at_least_region_stage": f"{1 / groups.rho_upper(n_rs, k_max, gap, later):.4f}"})
    for note, k in (("with Oman", 1), ("without Oman", 0)):
        u = groups.units_for(records, "B0", "main", note)
        n_all = groups.steady(u)[0]
        n_rs = groups.steady(groups.units_for(records, "B0", "main", note, "region_stage"))[0]
        gap, later = groups.SPORE - 432.9, 432.9 - C
        rows.append({"set": label, "category": "B0", "reading": "main", "variant": f"{note}, spore anchor",
                     "n_guaranteed": n_all, "n_region_stage": n_rs, "k_in_span": k,
                     "times_less_often_at_least": f"{1 / groups.rho_upper(n_all, k, gap, later):.4f}",
                     "times_less_often_at_least_region_stage": f"{1 / groups.rho_upper(n_rs, k, gap, later):.4f}"})
    return rows


def _shape_job(args):
    label, category, run_name, u = args
    hist = load_histories()
    out = []
    for hname in HISTORIES:
        for mask, (n, p, feasible) in groups.shape(u, hist[hname]).items():
            out.append({"set": label, "category": category, "run": run_name, "history": hname, "mask": mask,
                        "n": n, "best_finite_p": p, "feasible_finite_0_05": feasible})
    return out


def shape_jobs(h, disp):
    jobs = []
    for s in SETS:
        for run_name, ex in (("natural", None), ("bathurst_425", YEA_TAIL)):
            jobs.append((s, "B2", run_name, units(h, disp, s, exclude_members=ex)))
    for s in ("S0", "S1"):
        r = build(h, disp, s)
        for category, reading, note in groups.GROUPS[:4]:
            jobs.append((s, f"{category} {reading} {note}".strip(), "natural", groups.units_for(r, category, reading, note)))
    return jobs


def check_s0(t4, grp, shp):
    rb = pd.read_csv(OUT / "reviewed_bounds.csv")
    rb = rb[rb.category.eq("B2") & rb.reading.eq("main") & rb.units.eq("locality_age") & rb.variant.eq("primary")
            & rb.excluded_region.isna()]
    for cutoff, task in (("Emsian", "4.1_history"), ("Pridoli", "4.2")):
        for r in rb[rb.cutoff.eq(cutoff)].itertuples():
            m = t4[t4.set.eq("S0") & t4.run.eq("natural") & t4.task.eq(task) & t4.history.eq(r.history)
                   & t4.counting.eq("locality_age") & (t4.leave_bathurst.isna() | t4.leave_bathurst.eq("all"))]
            mine, ref = float(m.older_bound_ma.iloc[0]), r.older_bound_ma
            assert len(m) == 1 and m.status.iloc[0] == r.status, (cutoff, r.history)
            assert (math.isnan(mine) and math.isnan(ref)) or abs(mine - ref) < 1e-6, (cutoff, r.history)
    assert float(t4[t4.set.eq("S0") & t4.run.eq("natural") & t4.task.eq("4.2") & t4.history.eq("decline10")
                    & t4.counting.eq("locality_age") & t4.leave_bathurst.eq("all")].older_bound_ma.iloc[0]) == 429.80490705
    g = pd.read_csv(OUT / "groups.csv", dtype=str)
    mine = grp[grp.set.eq("S0") & grp.n_guaranteed.notna() & ~grp.variant.str.contains("spore")]
    for r in g[g.category.ne("B2")].itertuples():
        m = mine[mine.category.eq(r.category) & mine.reading.eq(r.reading) & mine.variant.eq(r.variant)].iloc[0]
        assert m.steady_limit_locality_age_ma == r.steady_limit_ma and m.steady_limit_region_stage_ma == r.steady_limit_region_stage_ma
        for k in ("collection", "locality"):
            assert m[f"steady_limit_{k}_ma"] == getattr(r, f"steady_limit_{k}_ma")
        for col in ("fold_444_all", "fold_452_all", "fold_444_region_stage", "fold_452_region_stage"):
            assert (m[col] or "nan") == (getattr(r, col) if isinstance(getattr(r, col), str) else "nan"), (r.category, col)
    gi = pd.read_csv(OUT / "groups_inside.csv", dtype=str)
    for r in gi.itertuples():
        sel = grp.set.eq("S0") & grp.variant.eq(r.variant)
        if "spore" not in r.variant:
            sel &= grp.stretch.eq(r.stretch)
        m = grp[sel].iloc[0]
        assert (m.times_less_often_at_least, m.times_less_often_at_least_region_stage) == (
            r.times_less_often_at_least, r.times_less_often_at_least_region_stage), r.variant
        if "spore" not in r.variant:
            assert m.times_less_often_at_least_longest_gap == r.times_less_often_at_least_longest_gap, r.stretch
    s = pd.read_csv(OUT / "stage2_interval/interval_feasibility_summary.csv")
    label = {"00": "B2_guaranteed", "11": "B2_possible", "01": "B2_partial_01", "10": "B2_partial_10"}
    mine = shp[shp.set.eq("S0") & shp.category.eq("B2") & shp.run.eq("natural")]
    for r in mine.itertuples():
        ref = s[s.category.eq(label[r.mask]) & s.history.eq(r.history)].iloc[0]
        assert abs(r.best_finite_p - ref.witness_finite_sample_p) < 1e-9 and r.feasible_finite_0_05 == ref.any_finite_sample_p_ge_0_05
    gs = pd.read_csv(OUT / "groups_shape.csv")
    for r in shp[shp.set.eq("S0") & shp.category.ne("B2")].itertuples():
        ref = gs[gs.group.eq(r.category) & gs.history.eq(r.history) & gs.partial_inclusion_mask.astype(str).str.zfill(2).eq(r.mask)]
        assert len(ref) == 1 and f"{r.best_finite_p:.3g}" == f"{ref.best_p.iloc[0]:.3g}" and r.feasible_finite_0_05 == ref.feasible.iloc[0], r
    print("S0 reproduces reviewed_bounds.csv (Emsian, Pridoli), groups.csv, groups_inside.csv, groups_shape.csv and "
          "interval_feasibility_summary.csv")


def gate_table(t3, shp, t4):
    """Gates 1-4 (S3-A17, S3-A21 to S3-A23). Deciding sets: S1, S2b, S3_main_ref; alternatives swap one in."""
    c60 = t3[t3.test.eq("C60")]
    c59 = t3[t3.test.eq("C59_placement")]

    def cells(df, s, grains, runs):
        """Rows of set s at the given grains; runs is a subset of ("natural", "425")."""
        if not s.startswith("S3"):
            x = df[df.set.eq(s) & df.run.isin([{"425": "bathurst_425"}.get(r, r) for r in runs])]
        else:
            parts = [df[df.set.eq(s) & df.run.eq("natural")]] if "natural" in runs else []
            if "425" in runs:
                base = "S3_" + s3_split(s)[0]
                parts.append(df[df.set.eq(base) & df.run.isin(["bathurst_425", "bathurst_425_forced_row6"])])
            x = pd.concat(parts)
        return x[x.counting.isin(grains)]

    LA, RS = ["locality_age", "region_stage_named"], ["region_stage_named"]

    def gate12(m, proxies_, which):
        req = [cells(c59, m[key], LA, ["natural", "425"]).assign(role=key) for key in ("S1", "S2b")]
        req.append(cells(c59, m["S3"], RS, ["natural", "425"]).assign(role="S3"))
        req = pd.concat(req)
        req = req[req.proxy.isin(proxies_)]
        est = req.excess_established.astype(str).eq("True")
        if est.all():
            return "holds", ""
        s2b = req[req.role.eq("S2b")]
        s3 = req[req.role.eq("S3")]
        if which == 1:
            gone = not s2b.excess_established.astype(str).eq("True").any() and not s3.excess_established.astype(str).eq("True").any()
        else:
            gone = (not s2b[s2b.counting.eq("locality_age")].excess_established.astype(str).eq("True").any()
                    and not s3.excess_established.astype(str).eq("True").any())
        failing = req[~est]
        desc = "; ".join(sorted({f"{r.role}:{r.counting}:{r.interval}:{r.run}:{r.proxy}" for r in failing.itertuples()}))
        return ("withdrawn" if gone else "narrower"), desc

    def gate3(m, run_name="natural"):
        nat = []
        for key, grains in (("S1", LA), ("S2b", LA), ("S3", RS)):
            x = cells(c60, m[key], grains, [run_name])
            if run_name == "425" and key == "S3":
                x = x[x.run.ne("natural")]
            nat.append(x.assign(role=key))
        assert all(len(x) for x in nat)
        nat = pd.concat(nat)
        rsn = nat[nat.counting.eq("region_stage_named")]
        compat = ~rsn.two_sided_rejected_at_all_counts.astype(str).eq("True")
        ratio = rsn.least_rate_relative_to_mean.astype(float)
        holds = bool(compat.all() and (ratio >= 0.40).all() and (rsn.n_regions.astype(float) >= 5).all())
        w = nat[nat.role.isin(["S2b", "S3"])]
        gone = bool(w.deficit_established.astype(str).eq("True").all() and (w.least_rate_relative_to_mean.astype(float) < 0.25).all())
        desc = "; ".join(f"{r.role}:{r.counting}:{r.interval}: ratio {r.least_rate_relative_to_mean}, deficit "
                         f"{r.deficit_established}, two-sided {r.two_sided_rejected_at_all_counts}, regions {int(r.n_regions)}"
                         for r in nat.itertuples())
        return ("holds" if holds else "withdrawn" if gone else "narrower"), desc

    def gate4c(m):
        """C49's S0 statement that decline25 fails on guaranteed finds: dropped if decline25 passes in both the
        guaranteed (00) and the all-possible (11) state on S1 and S2b."""
        x = shp[shp.category.eq("B2") & shp.run.eq("natural") & shp.history.eq("decline25")]
        state = {(s, k): bool(x[x.set.eq(s) & x["mask"].eq(k)].feasible_finite_0_05.iloc[0])
                 for s in ("S0", m["S1"], m["S2b"]) for k in ("00", "11")}
        fails_guaranteed = [not state[(s, "00")] for s in ("S0", m["S1"], m["S2b"])]
        drop = all(state[(s, k)] for s in (m["S1"], m["S2b"]) for k in ("00", "11"))
        out = "holds" if all(fails_guaranteed) else "narrower: S0-specific, drop" if drop else "narrower"
        return out, "; ".join(f"{s} {k}: {'passes' if v else 'fails'}" for (s, k), v in state.items())

    def gate4(m, hname, want_pass):
        sets = ["S0", m["S1"], m["S2b"]]
        x = shp[shp.category.eq("B2") & shp.run.eq("natural") & shp.history.eq(hname)]
        any_pass = {s: bool(x[x.set.eq(s)].feasible_finite_0_05.any()) for s in sets}
        if want_pass:
            out = "holds" if all(any_pass.values()) else "narrower"
        else:
            out = "holds" if not any(any_pass.values()) else "narrower"
        return out, "; ".join(f"{s}: {'passes' if v else 'fails'} in some state" if v else f"{s}: fails in every state"
                              for s, v in any_pass.items())

    deciding = {"S1": "S1", "S2b": "S2b", "S3": "S3_main_ref"}
    alts = ([("S1", s) for s in SETS if s.startswith("S1_")] + [("S2b", s) for s in SETS if s.startswith("S2") and s != "S2b"]
            + [("S3", f"S3_{v}_{y}") for v in READINGS for y in capel_s3.YEA_TREATMENTS if (v, y) != ("main", "ref")]
            + [("S3", "S3_yea_literal")])
    gates = {
        "1 C59 rock, rock x spore": lambda m: gate12(m, ["rock", "rock_x_spore_share"], 1),
        "2 C59 spore share": lambda m: gate12(m, ["spore_share"], 2),
        "3 C60 level rate": gate3,
        "3b C60 level rate at A = 425.0 Ma (Task 6)": lambda m: gate3(m, "425"),
        "4a C27 flat passes": lambda m: gate4(m, "flat", True),
        "4b C49 decline10 fails": lambda m: gate4(m, "decline10", False),
        "4c C49 decline25 fails on guaranteed finds": gate4c,
    }
    rows = []
    for gname, f in gates.items():
        out, desc = f(deciding)
        changed = []
        for role, alt in alts:
            if gname.startswith("4") and role == "S3":
                continue
            if role == "S3" and alt == "S3_yea_literal" and not gname.startswith(("1", "2", "3")):
                continue
            m = {**deciding, role: alt}
            o2, _ = f(m)
            if o2 != out:
                changed.append(f"{alt}: {o2}")
        final = "narrower, inventory-dependent" if changed and out in ("holds", "withdrawn") else out
        rows.append({"gate": gname, "deciding_outcome": out, "outcome": final, "changed_by": "; ".join(changed),
                     "detail": desc})
    rows.append(gate5(t4))
    return pd.DataFrame(rows)


def gate5(t4):
    """Gate 5 records the zero-delay steady-rate folds (C48, C58) and their sensitivity (S3-A25). Upward: the
    S1 and S2b full-window locality-age folds are at least S0's. Downward: the smallest jointly possible
    Devonian-free fold at 444 Ma lies below the smallest Devonian-free locality-age envelope fold of S0, S1
    and S2b with every unit kept (the specification's baseline range starts there). The row names the rows
    whose fold at 444 Ma falls to 1 or below under either calculation."""
    x = t4[t4.task.eq("4.1") | (t4.task.eq("4.2") & t4.history.eq("constant_formula"))].copy()
    x = x[~x.set.str.startswith("S3")]
    for col in ("fold_444", "admissible_min_fold_444"):
        x[col] = x[col].astype(float)
    base = ["S0", "S1", "S2b"]
    full = x[x.task.eq("4.1") & x.counting.eq("locality_age") & x.run.eq("natural")].set_index("set")
    up = all(full.loc[s, "fold_444"] >= full.loc["S0", "fold_444"] for s in ("S1", "S2b"))
    dev = x[x.task.eq("4.2")]
    floor = dev[dev.set.isin(base) & dev.run.eq("natural") & dev.counting.eq("locality_age")
                & dev.leave_bathurst.eq("all")].fold_444.min()
    order = dev.assign(o=~dev.set.isin(base)).sort_values(["admissible_min_fold_444", "o"])
    lo = order.iloc[0]
    down = lo.admissible_min_fold_444 < floor
    label = lambda r: " ".join(str(v) for v in (r.set, r.run, r.task, r.counting, r.leave_bathurst) if isinstance(v, str))
    low_env = [f"{label(r)}: {r.fold_444:.2f}" for r in x[x.fold_444 <= 1].itertuples()]
    low_adm = [f"{label(r)}: {r.admissible_min_fold_444:.2f}" for r in x[x.admissible_min_fold_444 <= 1].itertuples()]
    detail = ("full-window locality-age folds 444/452: "
              + "; ".join(f"{s} {full.loc[s, 'fold_444']:.4f}/{float(full.loc[s, 'fold_452']):.4f}" for s in ("S0", "S1", "S2a", "S2b"))
              + f". Devonian-free baseline floor (locality-age envelope, all units, S0/S1/S2b): {floor:.4f}."
              + f" Smallest jointly possible Devonian-free fold at 444 Ma: {lo.admissible_min_fold_444:.4f} ({label(lo)})."
              + f" Envelope folds at or below 1: {'; '.join(low_env) or 'none'}."
              + f" Jointly possible folds at or below 1: {'; '.join(low_adm) or 'none'}.")
    out = ("holds; full-window folds rise and Devonian-free regional folds fall below the baseline" if up and down
           else "holds, upward sensitivity recorded" if up else "holds, sensitivity recorded")
    return {"gate": "5 C48, C58 zero-delay folds (S0-S2)", "deciding_outcome": out, "outcome": out, "changed_by": "",
            "detail": detail}

def main():
    h, disp, d, invs = inventories()
    hist = load_histories()
    prox = proxies()
    t3, t4 = [], []
    for name, run_name, la, rs, family in invs:
        A = la.max_ma.max()
        rows = run(name, la, rs, A, prox)
        if (name, run_name) == ("S0", "natural"):
            s0_rows = rows
        t3 += [{**r, "run": run_name} for r in rows]
        rs_units = rs if rs is not None else s3_region_units(d, name, run_name)
        rs_nobath = region_units_without_bathurst(h, disp, d, name, run_name, family, la)
        t4 += task4(name, run_name, la, rs_units, rs_nobath, hist)
    t3, t4 = pd.DataFrame(t3), pd.DataFrame(t4)
    grp = pd.DataFrame(group_rows(build(h, disp, "S0"), "S0") + group_rows(build(h, disp, "S1"), "S1"))
    with ProcessPoolExecutor(max_workers=8) as ex:
        shp = pd.DataFrame([r for rows in ex.map(_shape_job, shape_jobs(h, disp)) for r in rows])
    check_s0(t4, grp, shp)
    signed = (OUT / "inventory_symmetry_tests_S0.csv").read_text()
    assert pd.DataFrame(s0_rows).to_csv(index=False, lineterminator="\n") == signed
    gates = gate_table(t3, shp, t4)
    for df, tag in ((t3, "tests"), (t4, "task4"), (grp, "groups"), (shp, "shape"), (gates, "gates")):
        df.to_csv(OUT / f"inventory_symmetry_stage2_{tag}.csv", index=False, lineterminator="\n")
    print(gates.to_string())


if __name__ == "__main__":
    main()
