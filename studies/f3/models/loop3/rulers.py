"""Outside rulers for the earlier/later finding-rate ratio (studies/f3/docs/plan-rulers.md).

For a proxy density x(s), Q(t) = mean x over [c, A] / mean x over [A, t], with A = 426.7 Ma and
c = 393.47 Ma from the reviewed primary bound. Proxies, not estimates; they enter no 95% inference.

    python3 studies/f3/models/loop3/rulers.py
"""

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
STEP = 0.01
POINTS = (431.2, 444.0, 447.0, 452.0)
GRID_T = [round(427.0 + 0.5 * i, 2) for i in range(59)]


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def stages():
    t = read(ROOT / "data/timescale.csv")
    out = {}
    for i, r in enumerate(t):
        top = float(t[i - 1]["base_ma"]) if i else 0.0
        out[r["stage"]] = (top, float(r["base_ma"]))
    return out


def piecewise(values, bounds):
    def x(s):
        for name, v in values.items():
            top, base = bounds[name]
            if top < s <= base:
                return v
        raise ValueError(s)
    return x


def rock(env_classes, project="North America", weight="area"):
    units = [u for u in read(ROOT / "data/eprp/record/macrostrat_units_window.csv")
             if u["j_project_name"] == project and u["j_status_code"] == "active" and u["d_env_class"] in env_classes]

    def x(s):
        cols = {}
        n = 0
        for u in units:
            if float(u["t_age"]) < s <= float(u["b_age"]):
                cols[u["col_id"]] = float(u["j_col_area_km2"])
                n += 1
        return sum(cols.values()) if weight == "area" else n
    return x, len(units)


def search(column):
    rows = [r for r in read(ROOT / "studies/f3/data/macro/effort_reviewed.csv") if r["region"] == "global"]
    return piecewise({r["stage"]: float(r[column]) for r in rows}, {r["stage"]: (float(r["young_ma"]), float(r["old_ma"]))
                                                                   for r in rows})


def spores():
    rows = read(ROOT / "data/spores/effort_global_by_stage.csv")
    st = stages()
    return piecewise({r["stage"]: int(r["n_docs_with_triletes"]) / int(r["n_docs"]) for r in rows if r["stage"] in st}, st)


def main():
    bound = next(r for r in read(OUT / "reviewed_bounds.csv")
                 if (r["category"], r["reading"], r["units"], r["variant"], r["excluded_region"], r["cutoff"], r["history"])
                 == ("B2", "main", "locality_age", "primary", "", "Emsian", "flat"))
    A, c = float(bound["oldest_possible_ma"]), float(bound["cutoff_ma"])
    rulers = {}
    x, n = rock({"non-marine"}); rulers["rock_nonmarine_area"] = (x, f"Macrostrat North America, non-marine column area ({n} units)")
    x, n = rock({"non-marine", "both"}); rulers["rock_nonmarine_both_area"] = (x, f"Macrostrat North America, non-marine or mixed column area ({n} units)")
    x, n = rock({"non-marine"}, weight="count"); rulers["rock_nonmarine_count"] = (x, f"Macrostrat North America, non-marine unit count ({n} units)")
    x, n = rock({"non-marine", "both"}, project="South America"); rulers["rock_south_america_area"] = (x, f"Macrostrat South America, non-marine or mixed column area ({n} units; secondary)")
    rulers["search_all"] = (search("all_density_per_myr"), "PBDB land and marginal-marine collections per Myr")
    rulers["search_plant_excluded"] = (search("plant_excluded_density_per_myr"), "PBDB collections per Myr, plant-filter matches removed")
    rulers["spores_trilete_share"] = (spores(), "Share of Palynodata documents reporting triletes")

    def mean(x, lo, hi):
        n = round((hi - lo) / STEP)
        return sum(x(lo + (i + 0.5) * STEP) for i in range(n)) / n

    OUT.mkdir(exist_ok=True)
    with open(OUT / "rulers.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ruler", "description", "candidate_ma", "later_mean", "earlier_mean", "later_to_earlier"])
        for key, (x, desc) in rulers.items():
            later = mean(x, c, A)
            for t in sorted(set(POINTS) | set(GRID_T)):
                earlier = mean(x, A, t)
                ratio = later / earlier if earlier > 0 else float("inf")
                w.writerow([key, desc, f"{t:g}", f"{later:.6g}", f"{earlier:.6g}", f"{ratio:.4f}"])
            print(key, {t: round(later / mean(x, A, t), 2) if mean(x, A, t) else "inf" for t in POINTS})

    alpha = 1 - float(bound["confidence_conditional_on_fixed_history_iid_units"])

    def matching_n(q, t):
        lo, hi = 1.0, 1000.0
        for _ in range(100):
            m = (lo + hi) / 2
            if (t - A) / ((A - c) * (alpha ** (-1 / m) - 1)) < q:
                lo = m
            else:
                hi = m
        return lo

    with open(OUT / "rulers_matching_n.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ruler", "candidate_ma", "later_to_earlier", "largest_n_matched"])
        for key, (x, _) in rulers.items():
            later = mean(x, c, A)
            for t in (444.0, 452.0):
                q = later / mean(x, A, t)
                w.writerow([key, f"{t:g}", f"{q:.4f}", f"{matching_n(q, t):.2f}"])


if __name__ == "__main__":
    main()
