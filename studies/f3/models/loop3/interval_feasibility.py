# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Interval-feasibility witnesses for the conditional-on-maximum KS diagnostic.

The calculation treats every recorded age range as support, not as a probability
distribution. For each declared recording history it finds an attainable age
allocation and brackets the global minimum KS discrepancy by enumerating every
matching graph induced by the interval endpoints. A witness is not an estimate
of the fossil ages. Failure of the older finite-grid search is not used as proof.
"""

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import stats
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

from analysis import select_records, shape_check
from histories import YOUNG, load_histories


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "stage2_interval"
OPT_TOL = 5e-11
EDGE_TOL = 2e-12
# Comparison targets independently read from the supplied review package. The
# analysis itself does not import the reviewer's code or allocation tables.
REVIEWER_TARGETS = {
    ("B2_possible", "decline25"): (0.18244723543219032, 0.07660948249764679, 0.06713017662667609),
    ("B2_possible", "pbdb_excluded_decline10"): (0.18664876704527533, 0.0658096266107708, 0.05740523116179441),
    ("B2_guaranteed", "decline25"): (0.20328961493718384, 0.041107353691003434, 0.035217705489401174),
    ("B2_guaranteed", "pbdb_excluded_decline10"): (0.19706995679777206, 0.051948225281976124, 0.04483809483352574),
    ("B0_canonical", "flat"): (0.31866509674358146, 3.2314678398766504e-07, 1.8746647510730737e-07),
    ("B0_canonical", "decline25"): (0.1967743270971607, 0.0051448773412349855, 0.004351892383394876),
    ("B0_canonical", "decline10"): (0.4715662255793309, 2.68107809791088e-15, 3.110492133428958e-16),
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_b0(records):
    """Return declared B0 units after validating canonical Oman membership."""
    oman = records[(records.horizon_id == "tail:S-w22-K12") & (records.reading == "main")]
    if len(oman) != 1:
        raise ValueError(f"canonical inventory requires exactly one main S-w22-K12 row, found {len(oman)}")
    row = oman.iloc[0]
    if not (row.eligible_primary and row.b0 and not row.b1 and not row.b2
            and np.isclose(row.min_ma, 445.2) and np.isclose(row.max_ma, 452.8)):
        raise ValueError("canonical S-w22-K12 membership or Katian support is invalid")
    r = select_records(records, "B0").copy()
    if r.member_ids.fillna("").str.contains("S-w22-K12", regex=False).sum() != 1:
        raise ValueError("canonical B0 units do not contain exactly one S-w22-K12 unit")
    return r, "canonical_horizons_reviewed"


def analysis_sets(records):
    """Enumerate every inclusion state of units that straddle the cutoff."""
    b0, b0_source = canonical_b0(records)
    base_sets = {"B2": select_records(records, "B2").copy(), "B0": b0}
    sets, metadata, membership = {}, {}, []
    for base_category, units in base_sets.items():
        possible = units[units.max_ma > YOUNG].copy()
        guaranteed = possible[possible.min_ma >= YOUNG].copy()
        partial = possible[possible.min_ma < YOUNG].sort_values("unit_id").reset_index(drop=True)
        if len(partial) > 10:
            raise ValueError("too many cutoff-straddling units for explicit subset enumeration")
        for mask in range(2 ** len(partial)):
            included = [i for i in range(len(partial)) if mask & (1 << i)]
            selected = pd.concat([guaranteed, partial.iloc[included]], ignore_index=True)
            full_mask = 2 ** len(partial) - 1
            if base_category == "B2" and mask == 0:
                label = "B2_guaranteed"
            elif base_category == "B2" and mask == full_mask:
                label = "B2_possible"
            elif base_category == "B0" and mask == 0:
                label = "B0_guaranteed"
            elif base_category == "B0" and mask == full_mask:
                label = "B0_canonical"
            else:
                label = f"{base_category}_partial_{mask:0{len(partial)}b}"
            selected["recorded_min_ma"] = selected.min_ma
            selected["min_ma"] = selected.min_ma.clip(lower=YOUNG)
            selected = selected.reset_index(drop=True)
            sets[label] = selected
            included_units = partial.iloc[included].unit_id.tolist()
            excluded_units = partial.drop(index=included).unit_id.tolist()
            metadata[label] = {
                "base_category": base_category,
                "partial_inclusion_mask": f"{mask:0{len(partial)}b}",
                "n_partial_units": len(partial),
                "n_partial_included": len(included),
                "partial_included_units": ";".join(included_units),
                "partial_excluded_units": ";".join(excluded_units),
            }
            for row in partial.itertuples():
                membership.append({
                    "base_category": base_category, "analysis_set": label,
                    "partial_inclusion_mask": f"{mask:0{len(partial)}b}", "unit_id": row.unit_id,
                    "recorded_min_ma": row.min_ma, "recorded_max_ma": row.max_ma,
                    "included_at_or_above_cutoff": row.unit_id in included_units,
                    "omitted_age_implication": "allocated below cutoff" if row.unit_id in excluded_units else "allocated at or above cutoff",
                })
    return sets, metadata, pd.DataFrame(membership), b0_source


def _matching_at_discrepancy(lower, upper, discrepancy):
    """Exhaustively decide whether any maximum exposure admits this KS D."""
    n = len(lower)
    m = n - 1
    radius = discrepancy - 1.0 / (2 * m)
    if radius < -EDGE_TOL:
        return None, 0
    radius = max(0.0, radius)
    ranks = (np.arange(m) + 0.5) / m
    global_low = float(lower.max())
    global_high = float(upper.max())
    q_high = np.minimum(ranks + radius, 1.0)
    q_low = np.maximum(ranks - radius, 0.0)
    edge_low = lower[:, None] / q_high[None, :]
    edge_high = np.full((n, m), global_high)
    np.divide(upper[:, None], q_low[None, :], out=edge_high, where=q_low[None, :] > 0)
    edge_low = np.maximum(edge_low, global_low)
    edge_high = np.minimum(edge_high, global_high)
    # Final slot: observation designated as the maximum and omitted from KS.
    edge_low = np.c_[edge_low, np.maximum(lower, global_low)]
    edge_high = np.c_[edge_high, np.minimum(upper, global_high)]
    valid = edge_low <= edge_high + EDGE_TOL
    endpoints = np.unique(np.r_[edge_low[valid], edge_high[valid], global_low, global_high])
    endpoints = endpoints[(endpoints >= global_low - EDGE_TOL) & (endpoints <= global_high + EDGE_TOL)]
    candidates = np.unique(np.r_[endpoints, (endpoints[:-1] + endpoints[1:]) / 2])
    for maximum in candidates:
        graph = valid & (edge_low <= maximum + EDGE_TOL) & (edge_high >= maximum - EDGE_TOL)
        matching = maximum_bipartite_matching(csr_matrix(graph), perm_type="column")
        if np.all(matching >= 0):
            return (float(maximum), matching), len(candidates)
    return None, len(candidates)


def optimise_discrepancy(lower, upper):
    """Bracket the global infimum D and return a checkable near-optimal match."""
    low, high = 0.0, 1.0
    if _matching_at_discrepancy(lower, upper, high)[0] is None:
        raise RuntimeError("no interval-compatible allocation exists even at D=1")
    while high - low > OPT_TOL:
        middle = (low + high) / 2
        if _matching_at_discrepancy(lower, upper, middle)[0] is None:
            low = middle
        else:
            high = middle
    match, cells = _matching_at_discrepancy(lower, upper, high + 4 * EDGE_TOL)
    if match is None:
        raise RuntimeError("failed to recover the feasible side of the optimisation bracket")
    return low, high, match, cells


def witness_allocation(records, recovery):
    cutoff_exposure = recovery.exposure(YOUNG)
    lower_raw = np.asarray(recovery.exposure(records.min_ma.to_numpy()) - cutoff_exposure)
    upper_raw = np.asarray(recovery.exposure(records.max_ma.to_numpy()) - cutoff_exposure)
    scale = float(upper_raw.max())
    lower, upper = lower_raw / scale, upper_raw / scale
    d_lower, d_upper, (maximum, matching), cells = optimise_discrepancy(lower, upper)
    m = len(records) - 1
    ranks = (np.arange(m) + 0.5) / m
    u = np.empty(len(records))
    roles, rank_slots = [], []
    for i, slot in enumerate(matching):
        if slot == m:
            u[i] = 1.0
            roles.append("profiled_maximum")
            rank_slots.append(np.nan)
        else:
            lo = lower[i] / maximum
            hi = min(upper[i], maximum) / maximum
            u[i] = np.clip(ranks[slot], lo, hi)
            roles.append("conditional_age")
            rank_slots.append(int(slot) + 1)
    maximum_raw = maximum * scale
    ages = recovery.age_at(cutoff_exposure + u * maximum_raw)
    allocation = records[["unit_id", "recorded_min_ma", "min_ma", "max_ma", "member_ids", "n_members"]].copy()
    allocation = allocation.rename(columns={"min_ma": "analysis_min_ma", "max_ma": "recorded_max_ma"})
    allocation["allocated_ma"] = ages
    allocation["role"] = roles
    allocation["conditional_rank"] = rank_slots
    allocation["normalised_exposure"] = u
    allocation["within_recorded_support"] = (
        (allocation.allocated_ma >= allocation.analysis_min_ma - 2e-9)
        & (allocation.allocated_ma <= allocation.recorded_max_ma + 2e-9)
    )
    if not allocation.within_recorded_support.all():
        raise RuntimeError("optimisation returned an age outside recorded support")
    d, p_asymptotic = shape_check(ages, recovery, YOUNG)
    p_finite = float(stats.kstwo.sf(d, m))
    if d > d_upper + 2e-8:
        raise RuntimeError("constructed witness does not attain optimisation bracket")
    return allocation, {
        "cutoff_ma": YOUNG,
        "cutoff_treatment": "fixed_project_timescale; shared-boundary uncertainty analysed separately",
        "n_units": len(records),
        "n_conditional_ages": m,
        "max_unit": allocation.loc[allocation.role.eq("profiled_maximum"), "unit_id"].iloc[0],
        "maximum_ma": float(allocation.allocated_ma.max()),
        "witness_D": d,
        "witness_asymptotic_p": p_asymptotic,
        "witness_finite_sample_p": p_finite,
        "global_D_lower": d_lower,
        "global_D_upper": d_upper,
        "optimisation_tolerance_D": d_upper - d_lower,
        "optimisation_event_cells_at_witness": cells,
    }, lower, upper


def threshold_certificate(lower, upper, distribution):
    m = len(lower) - 1
    if distribution == "asymptotic":
        critical = float(stats.kstwobign.ppf(0.95) / np.sqrt(m))
    elif distribution == "finite_sample":
        critical = float(stats.kstwo.ppf(0.95, m))
    else:
        raise ValueError(distribution)
    match, cells = _matching_at_discrepancy(lower, upper, critical)
    return critical, match is not None, cells


def run(output=OUT):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    inputs = [
        ROOT / "data/macro/horizons_reviewed.csv",
        ROOT / "data/macro/effort_reviewed.csv",
        ROOT / "data/timescale.csv",
        HERE / "analysis.py",
        HERE / "endpoint.py",
        HERE / "histories.py",
        Path(__file__).resolve(),
    ]
    before = {str(p.relative_to(ROOT)): sha256(p) for p in inputs}
    records = pd.read_csv(inputs[0])
    sets, set_metadata, membership, b0_source = analysis_sets(records)
    histories = load_histories()
    summaries, allocations = [], []
    for category, units in sets.items():
        for history, recovery in histories.items():
            allocation, summary, lower, upper = witness_allocation(units, recovery)
            asym_critical, asym_feasible, asym_cells = threshold_certificate(lower, upper, "asymptotic")
            finite_critical, finite_feasible, finite_cells = threshold_certificate(lower, upper, "finite_sample")
            summary.update({
                "category": category,
                "history": history,
                **set_metadata[category],
                "asymptotic_critical_D_0_05": asym_critical,
                "finite_sample_critical_D_0_05": finite_critical,
                "any_asymptotic_p_ge_0_05": asym_feasible,
                "any_finite_sample_p_ge_0_05": finite_feasible,
                "asymptotic_threshold_event_cells": asym_cells,
                "finite_sample_threshold_event_cells": finite_cells,
                "asymptotic_p_upper_from_D_lower": float(stats.kstwobign.sf(summary["global_D_lower"] * np.sqrt(summary["n_conditional_ages"]))),
                "finite_sample_p_upper_from_D_lower": float(stats.kstwo.sf(summary["global_D_lower"], summary["n_conditional_ages"])),
                "inference": (
                    "permissible_nonrejection_witness_under_both_reference_distributions"
                    if asym_feasible and finite_feasible
                    else "no_5pct_nonrejection_allocation_by_exhaustive_event_matching"
                    if not asym_feasible and not finite_feasible
                    else "reference_distribution_changes_5pct_classification"
                ),
                "interpretation": "optimised allocation is a feasibility witness, not an age estimate or probability distribution",
            })
            filename = f"witness_{category}_{history}.csv"
            allocation.insert(0, "history", history)
            allocation.insert(0, "category", category)
            allocation["n_units"] = summary["n_units"]
            allocation["n_conditional_ages"] = summary["n_conditional_ages"]
            allocation.to_csv(output / filename, index=False, lineterminator="\n", float_format="%.12g")
            summary["allocation_file"] = filename
            summaries.append(summary)
            allocations.append(output / filename)
    summary_table = pd.DataFrame(summaries)
    summary_path = output / "interval_feasibility_summary.csv"
    summary_table.to_csv(summary_path, index=False, lineterminator="\n", float_format="%.12g")

    membership_path = output / "partial_inclusion_sets.csv"
    membership.to_csv(membership_path, index=False, lineterminator="\n", float_format="%.12g")
    synthesis = []
    for (base_category, history), group in summary_table.groupby(["base_category", "history"]):
        best_asym = group.loc[group.witness_asymptotic_p.idxmax()]
        best_finite = group.loc[group.witness_finite_sample_p.idxmax()]
        synthesis.append({
            "base_category": base_category, "history": history, "n_support_consistent_subsets": len(group),
            "any_subset_asymptotic_p_ge_0_05": bool(group.any_asymptotic_p_ge_0_05.any()),
            "any_subset_finite_sample_p_ge_0_05": bool(group.any_finite_sample_p_ge_0_05.any()),
            "all_subsets_asymptotic_p_below_0_05": bool((~group.any_asymptotic_p_ge_0_05).all()),
            "all_subsets_finite_sample_p_below_0_05": bool((~group.any_finite_sample_p_ge_0_05).all()),
            "best_asymptotic_subset": best_asym.category,
            "best_asymptotic_p": best_asym.witness_asymptotic_p,
            "best_finite_sample_subset": best_finite.category,
            "best_finite_sample_p": best_finite.witness_finite_sample_p,
            "interpretation": "enumerates inclusion above versus below cutoff for every partial-window unit; still conditional on recorded supports",
        })
    synthesis_path = output / "partial_subset_synthesis.csv"
    pd.DataFrame(synthesis).to_csv(synthesis_path, index=False, lineterminator="\n", float_format="%.12g")

    comparisons = []
    for key, expected in REVIEWER_TARGETS.items():
        row = summary_table[(summary_table.category == key[0]) & (summary_table.history == key[1])].iloc[0]
        comparisons.append({
            "category": key[0], "history": key[1],
            "reviewer_D": expected[0], "repository_D": row.witness_D,
            "absolute_D_difference": abs(expected[0] - row.witness_D),
            "reviewer_asymptotic_p": expected[1], "repository_asymptotic_p": row.witness_asymptotic_p,
            "reviewer_finite_sample_p": expected[2], "repository_finite_sample_p": row.witness_finite_sample_p,
            "reproduced_to_1e_8": abs(expected[0] - row.witness_D) < 1e-8,
        })
    comparison_path = output / "reviewer_reproduction.csv"
    pd.DataFrame(comparisons).to_csv(comparison_path, index=False, lineterminator="\n", float_format="%.12g")
    after = {str(p.relative_to(ROOT)): sha256(p) for p in inputs}
    if before != after:
        raise RuntimeError("interval-feasibility inputs changed during execution")
    outputs = allocations + [summary_path, membership_path, synthesis_path, comparison_path]
    receipt = {
        "method": "finite event-cell enumeration plus bipartite matching in cumulative-exposure coordinates",
        "optimisation_tolerance_D": OPT_TOL,
        "edge_numerical_tolerance": EDGE_TOL,
        "b0_membership_source": b0_source,
        "histories": list(histories),
        "inputs": before,
        "outputs": {str(p.relative_to(ROOT)): sha256(p) for p in outputs},
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__},
        "scope": "support-feasibility diagnostic; no latent-age prior, calibrated searched-date test, model probability, or true-date estimate",
    }
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return summary_table


def main():
    table = run()
    print(table[["category", "history", "n_units", "witness_D", "witness_asymptotic_p",
                 "witness_finite_sample_p", "any_finite_sample_p_ge_0_05", "inference"]].to_string(index=False))


if __name__ == "__main__":
    main()
