"""Write the supplement's body-record tables into text/supplement.md from the reviewed Loop 3 outputs.

Each table replaces the block between `<!-- table:NAME -->` and `<!-- /table:NAME -->`."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "studies/f3/models/loop3/out"
SUPPLEMENT = Path(__file__).resolve().parent / "text/supplement.md"
BLOCKS = {}

CAT = {"B0": "B0 +Oman", "B1": "B1", "B2": "B2"}
HIST = {"flat": "Constant", "pbdb_all": "PBDB collection density", "pbdb_plant_excluded": "PBDB density, plant matches removed",
        "decline25": "Decline into past, 25 Myr", "decline10": "Decline into past, 10 Myr",
        "pbdb_excluded_decline10": "Plant-excluded PBDB × 10 Myr decline"}
SHORT = {"flat": "Const.", "pbdb_all": "PBDB", "pbdb_plant_excluded": "PBDB −plant", "decline25": "Decl. 25",
         "decline10": "Decl. 10", "pbdb_excluded_decline10": "−plant × decl. 10"}
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
    return f"{float(r[key]):.2f}" if r["status"] == "bounded" else "none"


def table(name, header, rows):
    widths = [max(6, len(h), *(len(str(row[i])) for row in rows)) for i, h in enumerate(header)]
    seps = ["-" * widths[0]] + ["-" * (w - 1) + ":" for w in widths[1:]]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(seps) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    BLOCKS[name] = "\n".join(lines)


def primary(r):
    return r["units"] == "locality_age" and r["variant"] == "primary" and not r["excluded_region"]


def main():
    bounds = read("reviewed_bounds.csv")

    rows = []
    for reading in ("main", "inclusive"):
        for cat in CAT:
            sel = {r["history"]: r for r in bounds if primary(r) and r["reading"] == reading and r["category"] == cat
                   and r["cutoff"] == "Emsian"}
            any_r = next(iter(sel.values()))
            rows.append([reading, CAT[cat], f"{any_r['n_guaranteed']}/{any_r['n_possible']}",
                         f"{float(any_r['oldest_possible_ma']):.1f}"] + [fmt(sel[h]) for h in HIST])
    table("primary", ["Reading", "Category", "Units", "Oldest"] + list(SHORT.values()), rows)

    rows = []
    for cut in ("Emsian", "Pragian", "Lochkovian", "Pridoli"):
        sel = {r["history"]: r for r in bounds if primary(r) and r["reading"] == "main" and r["category"] == "B2"
               and r["cutoff"] == cut}
        rows.append([f"{cut} ({float(sel['flat']['cutoff_ma']):.2f})", sel["flat"]["n_guaranteed"]]
                    + [fmt(sel[h]) for h in HIST])
    table("cutoffs", ["Cutoff (Ma)", "Units"] + list(SHORT.values()), rows)

    rows = []
    for (units, variant), label in VARIANT.items():
        sel = {r["history"]: r for r in bounds if r["units"] == units and r["variant"] == variant and not r["excluded_region"]
               and r["reading"] == "main" and r["category"] == "B2" and r["cutoff"] == "Emsian"}
        rows.append([label, sel["flat"]["n_guaranteed"], fmt(sel["flat"]), fmt(sel["pbdb_all"]), fmt(sel["decline25"])])
    table("units", ["B2 unit or source variant", "Units", "Constant", "PBDB density", "Decline 25 Myr"], rows)

    rows = []
    for r in sorted((r for r in bounds if r["excluded_region"] and r["reading"] == "main" and r["category"] == "B2"
                     and r["cutoff"] == "Emsian" and r["history"] == "flat"), key=lambda r: float(r["older_bound_ma"])):
        pb = next(x for x in bounds if x["excluded_region"] == r["excluded_region"] and x["reading"] == "main"
                  and x["category"] == "B2" and x["cutoff"] == "Emsian" and x["history"] == "pbdb_all")
        rows.append([r["excluded_region"].replace("-", " "), r["n_guaranteed"], f"{float(r['oldest_possible_ma']):.1f}",
                     fmt(r), fmt(pb)])
    table("regions", ["Region left out", "Units", "Oldest possible", "Constant", "PBDB density"], rows)

    rows = []
    shape = {(r["category"], r["variant"], r["history"], r["age_rule"]): r for r in read("shape_diagnostics.csv") if r["reading"] == "main"}
    span = lambda r: f"{float(r['imputed_nominal_p_q05']):.2g}–{float(r['imputed_nominal_p_q95']):.2g}"
    for cat, variant in (("B0", "primary"), ("B0", "without_oman_fragments"), ("B1", "primary"), ("B2", "primary")):
        label = "B0 -Oman" if variant == "without_oman_fragments" else CAT[cat]
        for h in HIST:
            u, q = shape[(cat, variant, h, "independent_uniform")], shape[(cat, variant, h, "shared_quantile")]
            rows.append([label, SHORT[h], f"{float(u['midpoint_nominal_p']):.2g}", span(u), span(q)])
    table("shape", ["Category", "History", "Nominal p, midpoint ages", "Independent-uniform ages, 5–95%",
                    "Shared-quantile ages, 5–95%"], rows)

    rows = []
    for reading in ("main", "inclusive"):
        for variant, label in (("primary", "included"), ("without_oman_fragments", "excluded")):
            sel = {r["history"]: r for r in bounds if r["category"] == "B0" and r["reading"] == reading
                   and r["units"] == "locality_age" and r["variant"] == variant and not r["excluded_region"]
                   and r["cutoff"] == "Emsian"}
            r = sel["flat"]
            rows.append([reading, label, f"{r['n_guaranteed']}/{r['n_possible']}", f"{float(r['oldest_possible_ma']):.1f}"]
                        + [fmt(sel[h]) for h in HIST])
    table("oman", ["Reading", "Oman", "Units", "Oldest"] + list(SHORT.values()), rows)

    rows = []
    for r in read("suppression_sensitivity.csv"):
        if r["reading"] == "main" and r["category"] == "B2":
            rows.append([r["baseline"].replace("pbdb_all", "PBDB density").replace("flat", "constant"), r["break_ma"],
                         r["older_multiplier"], r["modified_segment_overlaps_age_support"],
                         fmt(r), f"{float(r['midpoint_nominal_shape_p']):.3g}"])
    table("suppression", ["Baseline", "Break (Ma)", "Older multiplier", "Changes age support?",
                                      "Older bound (Ma)", "Midpoint shape p"], rows)

    rows = []
    for r in read("age_sensitivity.csv"):
        if r["reading"] == "main" and r["cutoff"] == "Emsian" and r["history"] in ("flat", "pbdb_all", "decline25"):
            q = (lambda k: f"{float(r[k]):.2f}" if r[k] else "—")
            rows.append([("B0 -Oman" if r["variant"] == "without_oman_fragments" else CAT[r["category"]]), SHORT[r["history"]], ("indep." if r["age_rule"] == "independent_uniform" else "shared q"),
                         q("bound_q05_ma"), q("bound_median_ma"), q("bound_q95_ma"), r["beyond_domain_fraction"][:4]])
    table("ages", ["Category", "History", "Allocation", "5%", "Median", "95%", "Unbounded fraction"], rows)

    rows = []
    for r in read("delay_sensitivity.csv"):
        if r["history"] == "flat":
            rows.append([CAT[r["category"]], r["assumed_delay_myr"], f"{float(r['recoverability_bound_ma']):.2f}",
                         f"{float(r['lineage_bound_if_delay_fixed_ma']):.2f}"])
    table("delay", ["Category", "Assumed delay (Myr)", "Recoverability bound", "Lineage bound"], rows)

    rows = []
    for r in read("simulation_results.csv"):
        if r["category"] != "B2":
            continue
        cov = f"{float(r['coverage_including_no_claim']):.3f} ({float(r['coverage_wilson_low']):.3f}–{float(r['coverage_wilson_high']):.3f})"
        true_delay = float(r["target_truth_ma"]) - float(r["recovery_truth_ma"])
        rows.append([r["scenario"].replace("_", " "), SHORT.get(r["true_history"], r["true_history"]),
                     SHORT.get(r["fitted_history"], r["fitted_history"]), r["age_mode"].replace("_", " "), r["duplicate_factor"],
                     f"{true_delay:g}", r["delay_adjustment_ma"], f"{float(r['claim_frequency']):.3f}", cov])
    table("simulation", ["Scenario", "True", "Fitted", "Ages", "Dup.", "True delay", "Adj.", "Claims", "Coverage (95% CI)"], rows)

    cands = ("431.2", "440", "444", "447", "452")
    names = {"primary": "Locality–age (primary)", "region_stage": "Region–stage", "curated": "Curated oldest set"}
    fr = {(r["unit_treatment"], r["assumed_diagnostic_delay_myr"], r["candidate_lineage_ma"]): r
          for r in read("frontier.csv") if r["reading"] == "main"}
    rows = []
    for ut in names:
        for d in ("0", "5", "10", "20"):
            cells = []
            for c in cands:
                r = fr[(ut, d, c)]
                cells.append(f"{float(r['earlier_to_later_intensity']):.3f}" if r["status"] == "contour" else "—")
            rows.append([names[ut], d] + cells)
    table("frontier", ["Units", "Delay (Myr)"] + [f"{c} Ma" for c in cands], rows)

    def p(v):
        v = float(v)
        return f"{v:.3f}" if v >= 0.001 else f"{v:.0e}"
    states = [("B2_guaranteed", "B2", "48 guaranteed"), ("B2_partial_01", "B2", "49 (one straddling)"),
              ("B2_possible", "B2", "50 possible"), ("B0_guaranteed", "B0 +Oman", "76 guaranteed"),
              ("B0_partial_01", "B0 +Oman", "77 (one straddling)"), ("B0_canonical", "B0 +Oman", "78 possible")]
    iv = {(r["category"], r["history"]): r for r in read("stage2_interval/interval_feasibility_summary.csv")}
    rows = []
    for key, cat, label in states:
        cells = []
        for h in HIST:
            r = iv[(key, h)]
            fs = r["any_finite_sample_p_ge_0_05"] == "True"
            mark = "" if fs else ("†" if r["any_asymptotic_p_ge_0_05"] == "True" else "*")
            cells.append(f"{p(r['witness_finite_sample_p'])}{mark}")
        rows.append([cat, label] + cells)
    table("interval", ["Category", "Units"] + [SHORT[h] for h in HIST], rows)

    ts = {(r["scenario"], r["history"]): r for r in read("stage2_timescale/bound_sensitivity.csv")
          if r["category"] == "B2_primary"}
    rows = []
    for sc in ("baseline", "all_younger", "all_older", "alternating_a", "alternating_b"):
        base = ts[(sc, "flat")]
        cells = [f"{float(ts[(sc, h)]['older_bound_ma']):.2f}" for h in ("flat", "pbdb_all", "pbdb_plant_excluded", "decline25")]
        rows.append([sc.replace("_", " "), f"{float(base['cutoff_ma']):.2f}", base["n_guaranteed"]] + cells
                    + [f"{float(base['candidate_same_scale_ma']):.2f}", f"{float(base['candidate_source_rule_ma']):.2f}"])
    table("timescale", ["Scenario", "Cutoff", "Units", "Const.", "PBDB", "PBDB −plant", "Decl. 25",
                        "431.2 mapped", "Source rule"], rows)

    text = SUPPLEMENT.read_text()
    for name, block in BLOCKS.items():
        text, n = re.subn(rf"(<!-- table:{name} -->\n).*?(\n<!-- /table:{name} -->)",
                          lambda m: m.group(1) + block + m.group(2), text, flags=re.S)
        if n != 1:
            raise ValueError(f"marker for table {name} found {n} times")
    SUPPLEMENT.write_text(text)


if __name__ == "__main__":
    main()
