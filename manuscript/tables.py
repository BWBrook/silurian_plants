"""Write the supplement's body-record tables as Markdown, directly from the reviewed Loop 3 outputs."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "models/f3/loop3/out"
TABLES = Path(__file__).resolve().parent / "tables"

CAT = {"B0": "Any land-plant body", "B1": "Polysporangiophyte body", "B2": "Crown vascular-plant body"}
HIST = {"flat": "Constant", "pbdb_all": "PBDB collection density", "pbdb_plant_excluded": "PBDB density, plant matches removed",
        "decline25": "Decline into past, 25 Myr", "decline10": "Decline into past, 10 Myr",
        "pbdb_excluded_decline10": "Plant-excluded PBDB × 10 Myr decline"}
VARIANT = {("collection", "primary"): "Individual collections/observations", ("locality_age", "primary"): "Locality–age proxies (primary)",
           ("locality", "primary"): "Whole localities", ("region_stage", "primary"): "Region–stage cells",
           ("locality_age", "wide_age"): "Wide-age records restored", ("locality_age", "unresolved_material"): "Uncertain material restored",
           ("locality_age", "without_low_confidence"): "Low-confidence names omitted",
           ("locality_age", "without_weak_botanical_source"): "Weak botanical source omitted",
           ("locality_age", "kosov_podolia_links"): "Kosov/Podolia links collapsed",
           ("locality_age", "curated_tail_only"): "Curated oldest-record set only"}


def read(name):
    with (OUT_DIR / name).open() as f:
        return list(csv.DictReader(f))


def fmt(r, key="older_bound_ma"):
    return f"{float(r[key]):.2f}" if r["status"] == "bounded" else "none ≤ 469.4"


def table(path, header, rows):
    widths = [max(6, len(h), *(len(str(row[i])) for row in rows)) for i, h in enumerate(header)]
    seps = ["-" * widths[0]] + ["-" * (w - 1) + ":" for w in widths[1:]]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(seps) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    path.write_text("\n".join(lines) + "\n")


def primary(r):
    return r["units"] == "locality_age" and r["variant"] == "primary" and not r["excluded_region"]


def main():
    TABLES.mkdir(exist_ok=True)
    bounds = read("reviewed_bounds.csv")

    rows = []
    for reading in ("main", "inclusive"):
        for cat in CAT:
            sel = {r["history"]: r for r in bounds if primary(r) and r["reading"] == reading and r["category"] == cat
                   and r["cutoff"] == "Emsian"}
            any_r = next(iter(sel.values()))
            rows.append([reading, CAT[cat], f"{any_r['n_guaranteed']}/{any_r['n_possible']}",
                         f"{float(any_r['oldest_possible_ma']):.1f}"] + [fmt(sel[h]) for h in HIST])
    table(TABLES / "primary.md", ["Reading", "Category", "Units", "Oldest possible"] + list(HIST.values()), rows)

    rows = []
    for cut in ("Emsian", "Pragian", "Lochkovian", "Pridoli"):
        sel = {r["history"]: r for r in bounds if primary(r) and r["reading"] == "main" and r["category"] == "B2"
               and r["cutoff"] == cut}
        rows.append([f"{cut} ({float(sel['flat']['cutoff_ma']):.2f})", sel["flat"]["n_guaranteed"]]
                    + [fmt(sel[h]) for h in HIST])
    table(TABLES / "cutoffs.md", ["Younger cutoff (Ma)", "Units"] + list(HIST.values()), rows)

    rows = []
    for (units, variant), label in VARIANT.items():
        sel = {r["history"]: r for r in bounds if r["units"] == units and r["variant"] == variant and not r["excluded_region"]
               and r["reading"] == "main" and r["category"] == "B2" and r["cutoff"] == "Emsian"}
        rows.append([label, sel["flat"]["n_guaranteed"], fmt(sel["flat"]), fmt(sel["pbdb_all"]), fmt(sel["decline25"])])
    table(TABLES / "units.md", ["B2 unit or source variant", "Units", "Constant", "PBDB density", "Decline 25 Myr"], rows)

    rows = []
    for r in sorted((r for r in bounds if r["excluded_region"] and r["reading"] == "main" and r["category"] == "B2"
                     and r["cutoff"] == "Emsian" and r["history"] == "flat"), key=lambda r: float(r["older_bound_ma"])):
        pb = next(x for x in bounds if x["excluded_region"] == r["excluded_region"] and x["reading"] == "main"
                  and x["category"] == "B2" and x["cutoff"] == "Emsian" and x["history"] == "pbdb_all")
        rows.append([r["excluded_region"].replace("-", " "), r["n_guaranteed"], f"{float(r['oldest_possible_ma']):.1f}",
                     fmt(r), fmt(pb)])
    table(TABLES / "regions.md", ["Region left out", "Units", "Oldest possible", "Constant", "PBDB density"], rows)

    rows = []
    for r in read("shape_diagnostics.csv"):
        if r["reading"] == "main" and r["age_rule"] == "independent_uniform":
            rows.append([CAT[r["category"]], HIST[r["history"]], f"{float(r['midpoint_D']):.3f}",
                         f"{float(r['imputed_nominal_p_q05']):.2g}–{float(r['imputed_nominal_p_q95']):.2g}"])
    table(TABLES / "shape.md", ["Category", "History", "KS D at midpoint ages", "Nominal p, 5–95% of age draws"], rows)

    rows = []
    for r in read("suppression_sensitivity.csv"):
        if r["reading"] == "main" and r["category"] == "B2":
            rows.append([r["baseline"].replace("pbdb_all", "PBDB density").replace("flat", "constant"), r["break_ma"],
                         r["older_multiplier"], r["modified_segment_overlaps_age_support"],
                         fmt(r), f"{float(r['midpoint_nominal_shape_p']):.3g}"])
    table(TABLES / "suppression.md", ["Baseline", "Break (Ma)", "Older multiplier", "Changes age support?",
                                      "Older bound (Ma)", "Midpoint shape p"], rows)

    rows = []
    for r in read("age_sensitivity.csv"):
        if r["reading"] == "main" and r["cutoff"] == "Emsian" and r["history"] in ("flat", "pbdb_all", "decline25"):
            q = (lambda k: f"{float(r[k]):.2f}" if r[k] else "—")
            rows.append([CAT[r["category"]], HIST[r["history"]], r["age_rule"].replace("_", " "),
                         q("bound_q05_ma"), q("bound_median_ma"), q("bound_q95_ma"), r["beyond_domain_fraction"][:4]])
    table(TABLES / "ages.md", ["Category", "History", "Allocation", "5%", "Median", "95%", "Unbounded fraction"], rows)

    rows = []
    for r in read("delay_sensitivity.csv"):
        if r["history"] == "flat":
            rows.append([CAT[r["category"]], r["assumed_delay_myr"], f"{float(r['recoverability_bound_ma']):.2f}",
                         f"{float(r['lineage_bound_if_delay_fixed_ma']):.2f}"])
    table(TABLES / "delay.md", ["Category", "Assumed delay (Myr)", "Recoverability bound", "Lineage bound"], rows)

    rows = []
    for r in read("simulation_results.csv"):
        if r["category"] != "B2":
            continue
        cov = f"{float(r['coverage_including_no_claim']):.3f} ({float(r['coverage_wilson_low']):.3f}–{float(r['coverage_wilson_high']):.3f})"
        rows.append([r["scenario"].replace("_", " "), HIST.get(r["true_history"], r["true_history"]),
                     HIST.get(r["fitted_history"], r["fitted_history"]), r["age_mode"].replace("_", " "), r["duplicate_factor"],
                     r["delay_adjustment_ma"], r["recovery_truth_ma"], f"{float(r['claim_frequency']):.3f}", cov])
    table(TABLES / "simulation.md", ["Scenario", "True history", "Fitted history", "Ages", "Duplication", "Delay adj.",
                                     "Endpoint (Ma)", "Claim frequency", "Coverage (Wilson 95%)"], rows)


if __name__ == "__main__":
    main()
