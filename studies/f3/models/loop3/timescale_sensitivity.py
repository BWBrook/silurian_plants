# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Shared geological-boundary sensitivity for primary B0 and B2 bounds.

Boundary scenarios are deterministic perturbations, not age priors. Each named
stage boundary moves once and is reused for curated stage-based fossil support,
exactly matching PBDB stage support, effort-stage widths and the analysis
cutoff. PBDB numerical ages without exact boundary support remain fixed.
"""

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd

from endpoint import PiecewiseRecovery, known_cutoff_summary
from analysis import select_records


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "stage2_timescale"
BASE_YOUNG = 393.47
BASE_DOMAIN = 469.4
BOUNDARY_TOL = 1e-6
MIN_ORDER_GAP = 1e-6
LAND = {"terrestrial indet.", "fluvial indet.", "fluvial-lacustrine indet.", "lacustrine indet.",
        "lacustrine - large", "pond", '"floodplain"', "wet floodplain", "fine channel fill",
        '"channel"', "alluvial fan", "crevasse splay", "mire/swamp", "fluvial-deltaic indet.",
        "delta plain"}
MARGINAL = {"coastal indet.", "marginal marine indet.", "lagoonal", "estuary/bay",
            "interdistributary bay", "paralic indet.", "deltaic indet.", "delta front", "prodelta",
            "peritidal", "foreshore"}

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_b0(records):
    oman = records[(records.horizon_id == "tail:S-w22-K12") & (records.reading == "main")]
    if len(oman) != 1:
        raise ValueError(f"canonical inventory requires exactly one main S-w22-K12 row, found {len(oman)}")
    row = oman.iloc[0]
    if not (row.eligible_primary and row.b0 and not row.b1 and not row.b2
            and np.isclose(row.min_ma, 445.2) and np.isclose(row.max_ma, 452.8)):
        raise ValueError("canonical S-w22-K12 membership or Katian support is invalid")
    units = select_records(records, "B0").copy()
    if units.member_ids.fillna("").str.contains("S-w22-K12", regex=False).sum() != 1:
        raise ValueError("canonical B0 units do not contain exactly one S-w22-K12 unit")
    return units, "canonical_horizons_reviewed"


def boundary_table(path=ROOT / "data/timescale.csv"):
    scale = pd.read_csv(path)
    selected = scale[(scale.base_ma >= BASE_YOUNG - BOUNDARY_TOL)
                     & (scale.base_ma <= BASE_DOMAIN + BOUNDARY_TOL)].copy()
    selected = selected.sort_values("base_ma").reset_index(drop=True)
    if selected.base_unc_ma.isna().any() or not np.all(np.diff(selected.base_ma) > 0):
        raise ValueError("analysis boundaries require finite uncertainties and strict age order")
    return selected[["period", "series", "stage", "base_ma", "base_unc_ma"]]


def _ordered_amplitude(base, uncertainty, signs):
    coefficient = np.diff(signs * uncertainty)
    narrowing = coefficient < 0
    if not narrowing.any():
        return 1.0
    limit = np.min((np.diff(base)[narrowing] - MIN_ORDER_GAP) / -coefficient[narrowing])
    return float(min(1.0, 0.99 * limit))


def boundary_scenarios(scale):
    n = len(scale)
    patterns = {
        "baseline": np.zeros(n),
        "all_younger": -np.ones(n),
        "all_older": np.ones(n),
        "alternating_a": np.where(np.arange(n) % 2 == 0, 1.0, -1.0),
        "alternating_b": np.where(np.arange(n) % 2 == 0, -1.0, 1.0),
    }
    scenarios = {}
    base = scale.base_ma.to_numpy(float)
    uncertainty = scale.base_unc_ma.to_numpy(float)
    for name, signs in patterns.items():
        amplitude = 0.0 if name == "baseline" else _ordered_amplitude(base, uncertainty, signs)
        shifted = base + amplitude * signs * uncertainty
        if not np.all(np.diff(shifted) > MIN_ORDER_GAP):
            raise RuntimeError(f"boundary scenario {name} violates stage order")
        table = scale.copy()
        table["scenario"] = name
        table["basis_sign"] = signs
        table["basis_amplitude"] = amplitude
        table["shift_ma"] = shifted - base
        table["scenario_base_ma"] = shifted
        table["gap_to_older_boundary_ma"] = np.r_[np.diff(shifted), np.nan]
        scenarios[name] = table
    return scenarios


def _boundary_match(value, scale):
    distance = np.abs(scale.base_ma.to_numpy(float) - float(value))
    index = int(distance.argmin())
    return index if distance[index] <= BOUNDARY_TOL else None


def map_support(minimum, maximum, source, scale, scenario):
    young_index = _boundary_match(minimum, scale)
    old_index = _boundary_match(maximum, scale)
    exact = young_index is not None and old_index is not None
    if source == "tail":
        if not exact:
            raise ValueError("curated stage-based support no longer matches the project timescale")
        basis = "shared_curated_stage_boundaries"
    elif source == "pbdb" and exact:
        basis = "shared_pbdb_exact_boundary_support"
    elif source == "pbdb":
        return float(minimum), float(maximum), "fixed_pbdb_numerical_support_not_exactly_mapped"
    else:
        raise ValueError(f"unknown unit source {source}")
    shifted = scenario.scenario_base_ma.to_numpy(float)
    return float(shifted[young_index]), float(shifted[old_index]), basis


def map_units(units, category, scale, scenario):
    rows = []
    for unit in units.itertuples(index=False):
        members = str(unit.member_ids).split(";")
        prefixes = {member.split(":", 1)[0] for member in members}
        if len(prefixes) != 1 or prefixes.pop() not in {"tail", "pbdb"}:
            raise ValueError(f"unit has mixed or unknown source channels: {unit.unit_id}")
        source = members[0].split(":", 1)[0]
        minimum, maximum, basis = map_support(unit.min_ma, unit.max_ma, source, scale, scenario)
        rows.append({
            "scenario": scenario.scenario.iloc[0], "category": category, "unit_id": unit.unit_id,
            "member_ids": unit.member_ids, "source": source,
            "baseline_min_ma": unit.min_ma, "baseline_max_ma": unit.max_ma,
            "scenario_min_ma": minimum, "scenario_max_ma": maximum, "mapping_basis": basis,
        })
    return pd.DataFrame(rows)


def _map_pbdb_frame(frame, scale, scenario):
    result = frame.copy()
    bases = scale.base_ma.to_numpy(float)
    shifted = scenario.scenario_base_ma.to_numpy(float)
    min_distance = np.abs(result.min_ma.to_numpy()[:, None] - bases[None, :])
    max_distance = np.abs(result.max_ma.to_numpy()[:, None] - bases[None, :])
    min_index = min_distance.argmin(axis=1)
    max_index = max_distance.argmin(axis=1)
    mapped = (min_distance[np.arange(len(result)), min_index] <= BOUNDARY_TOL) & (
        max_distance[np.arange(len(result)), max_index] <= BOUNDARY_TOL)
    result.loc[mapped, "min_ma"] = shifted[min_index[mapped]]
    result.loc[mapped, "max_ma"] = shifted[max_index[mapped]]
    result["timescale_mapping"] = np.where(
        mapped, "shared_pbdb_exact_boundary_support", "fixed_pbdb_numerical_support_not_exactly_mapped")
    return result


def effort_for_scenario(raw, plant_ids, scale, scenario):
    records = _map_pbdb_frame(raw, scale, scenario)
    environment = records.environment.fillna("").isin(LAND | MARGINAL).to_numpy()
    plant_overlap = records.collection_no.isin(plant_ids).to_numpy()
    boundaries = scenario.scenario_base_ma.to_numpy(float)
    stages = scale.stage.iloc[1:].to_numpy()
    rows = []
    widths = records.max_ma.to_numpy() - records.min_ma.to_numpy()
    for i, stage in enumerate(stages):
        young, old = boundaries[i], boundaries[i + 1]
        overlap = np.maximum(0.0, np.minimum(records.max_ma, old) - np.maximum(records.min_ma, young))
        weights = np.divide(overlap, widths, out=np.zeros(len(records)), where=widths > 0)
        all_count = float(weights[environment].sum())
        excluded = float(weights[environment & ~plant_overlap].sum())
        duration = old - young
        rows.append({
            "scenario": scenario.scenario.iloc[0], "stage": stage, "young_ma": young, "old_ma": old,
            "duration_myr": duration, "all_collection_equivalents": all_count,
            "plant_excluded_equivalents": excluded, "all_density_per_myr": all_count / duration,
            "plant_excluded_density_per_myr": excluded / duration,
            "pbdb_intervals_shared_boundary_mapped": int(records.timescale_mapping.str.startswith("shared").sum()),
            "pbdb_intervals_numeric_fixed": int(records.timescale_mapping.str.startswith("fixed").sum()),
        })
    return pd.DataFrame(rows)


def histories_for_scenario(effort, scenario):
    boundaries = scenario.scenario_base_ma.to_numpy(float)
    young, domain = boundaries[0], boundaries[-1]
    edges = np.unique(np.r_[np.arange(young, domain, 0.05), boundaries, domain])
    mid = (edges[:-1] + edges[1:]) / 2
    stage_old = effort.old_ma.to_numpy(float)
    index = np.searchsorted(stage_old, mid)
    all_density = effort.all_density_per_myr.to_numpy(float)[index]
    excluded = effort.plant_excluded_density_per_myr.to_numpy(float)[index]
    densities = {
        "flat": np.ones_like(mid),
        "pbdb_all": all_density,
        "pbdb_plant_excluded": excluded,
        "decline25": np.exp(-(mid - young) / 25),
        "decline10": np.exp(-(mid - young) / 10),
        "pbdb_excluded_decline10": excluded * np.exp(-(mid - young) / 10),
    }
    if any((density <= 0).any() for density in densities.values()):
        raise ValueError("scenario creates non-positive declared recording intensity")
    return {name: PiecewiseRecovery(edges, density) for name, density in densities.items()}


def map_candidate_431_2(scale, scenario):
    bases = scale.base_ma.to_numpy(float)
    index = np.searchsorted(bases, 431.2) - 1
    fraction = (431.2 - bases[index]) / (bases[index + 1] - bases[index])
    shifted = scenario.scenario_base_ma.to_numpy(float)
    mapped = shifted[index] + fraction * (shifted[index + 1] - shifted[index])
    return float(mapped), scale.stage.iloc[index], scale.stage.iloc[index + 1], float(fraction)


def source_rule_candidate(scale, scenario):
    """Reapply the published Homerian-base-plus-uncertainty rule on this scale."""
    index = scale.index[scale.stage.eq("Homerian")]
    if len(index) != 1:
        raise ValueError("timescale must contain exactly one Homerian boundary")
    row = scale.loc[index[0]]
    shifted_base = float(scenario.loc[index[0], "scenario_base_ma"])
    return shifted_base + float(row.base_unc_ma), shifted_base, float(row.base_unc_ma)


def run(output=OUT):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    inputs = [
        ROOT / "data/timescale.csv",
        ROOT / "data/macro/horizons_reviewed.csv",
        ROOT / "data/macro/effort_reviewed.csv",
        ROOT / "data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv",
        ROOT / "data/eprp/record/pbdb_plant_collections.csv",
        HERE / "analysis.py", HERE / "endpoint.py", HERE / "histories.py",
        Path(__file__).resolve(),
    ]
    before = {str(path.relative_to(ROOT)): sha256(path) for path in inputs}
    scale = boundary_table(inputs[0])
    scenarios = boundary_scenarios(scale)
    horizons = pd.read_csv(inputs[1])
    b2 = select_records(horizons, "B2")
    b0, b0_source = canonical_b0(horizons)
    categories = {"B0_canonical": b0, "B2_primary": b2}
    raw = pd.read_csv(inputs[3], low_memory=False)
    plant_ids = set(pd.read_csv(inputs[4], usecols=["collection_no"]).collection_no)
    bounds, mappings, efforts, boundary_rows = [], [], [], []
    baseline_effort = pd.read_csv(inputs[2])
    baseline_global = baseline_effort[baseline_effort.region.eq("global")].sort_values("young_ma").reset_index(drop=True)
    for name, scenario in scenarios.items():
        boundary_rows.append(scenario)
        effort = effort_for_scenario(raw, plant_ids, scale, scenario)
        efforts.append(effort)
        if name == "baseline":
            for column in ["young_ma", "old_ma", "duration_myr", "all_collection_equivalents",
                           "plant_excluded_equivalents", "all_density_per_myr", "plant_excluded_density_per_myr"]:
                if not np.allclose(effort[column], baseline_global[column], rtol=0, atol=2e-10):
                    raise RuntimeError(f"baseline effort reconstruction differs in {column}")
        histories = histories_for_scenario(effort, scenario)
        cutoff = float(scenario.scenario_base_ma.iloc[0])
        candidate, candidate_young, candidate_old, candidate_fraction = map_candidate_431_2(scale, scenario)
        rule_candidate, rule_base, rule_offset = source_rule_candidate(scale, scenario)
        for category, units in categories.items():
            mapped = map_units(units, category, scale, scenario)
            mappings.append(mapped)
            possible = mapped[mapped.scenario_max_ma > cutoff]
            certain = possible[possible.scenario_min_ma >= cutoff]
            oldest = float(possible.scenario_max_ma.max())
            for history, recovery in histories.items():
                fit = known_cutoff_summary(len(certain), oldest, recovery, cutoff)
                bounds.append({
                    "scenario": name, "category": category, "history": history,
                    "cutoff_ma": cutoff, "domain_max_ma": float(scenario.scenario_base_ma.iloc[-1]),
                    "n_possible": len(possible), "n_guaranteed": len(certain), "oldest_possible_ma": oldest,
                    "older_bound_ma": fit.bound_ma, "status": fit.status,
                    "published_candidate_fixed_ma": 431.2,
                    "candidate_same_scale_ma": candidate,
                    "candidate_mapping_young_boundary": candidate_young,
                    "candidate_mapping_old_boundary": candidate_old,
                    "candidate_fraction_from_young_boundary": candidate_fraction,
                    "candidate_source_rule_ma": rule_candidate,
                    "candidate_source_rule_boundary": "Homerian",
                    "candidate_source_rule_shifted_base_ma": rule_base,
                    "candidate_source_rule_quoted_offset_ma": rule_offset,
                    "margin_to_fixed_431_2_ma": fit.bound_ma - 431.2 if fit.status in {"bounded", "at_boundary"} else np.nan,
                    "margin_to_same_scale_candidate_ma": fit.bound_ma - candidate if fit.status in {"bounded", "at_boundary"} else np.nan,
                    "margin_to_source_rule_candidate_ma": fit.bound_ma - rule_candidate if fit.status in {"bounded", "at_boundary"} else np.nan,
                    "interpretation": "deterministic shared-boundary sensitivity; not a geological probability interval",
                })
    bound_table = pd.DataFrame(bounds)
    baseline = bound_table[bound_table.scenario.eq("baseline")][["category", "history", "older_bound_ma",
                                                                  "margin_to_same_scale_candidate_ma",
                                                                  "margin_to_source_rule_candidate_ma"]].rename(
        columns={"older_bound_ma": "baseline_bound_ma",
                 "margin_to_same_scale_candidate_ma": "baseline_candidate_margin_ma",
                 "margin_to_source_rule_candidate_ma": "baseline_source_rule_margin_ma"})
    bound_table = bound_table.merge(baseline, on=["category", "history"], validate="many_to_one")
    bound_table["bound_shift_from_baseline_ma"] = bound_table.older_bound_ma - bound_table.baseline_bound_ma
    bound_table["candidate_margin_shift_from_baseline_ma"] = (
        bound_table.margin_to_same_scale_candidate_ma - bound_table.baseline_candidate_margin_ma)
    bound_table["source_rule_margin_shift_from_baseline_ma"] = (
        bound_table.margin_to_source_rule_candidate_ma - bound_table.baseline_source_rule_margin_ma)
    influence = []
    for (category, history), group in bound_table.groupby(["category", "history"]):
        finite_bound = group[group.bound_shift_from_baseline_ma.notna()]
        finite_candidate = group[group.candidate_margin_shift_from_baseline_ma.notna()]
        finite_rule = group[group.source_rule_margin_shift_from_baseline_ma.notna()]
        row = finite_bound.loc[finite_bound.bound_shift_from_baseline_ma.abs().idxmax()] if len(finite_bound) else None
        candidate_row = finite_candidate.loc[finite_candidate.candidate_margin_shift_from_baseline_ma.abs().idxmax()] if len(finite_candidate) else None
        rule_row = finite_rule.loc[finite_rule.source_rule_margin_shift_from_baseline_ma.abs().idxmax()] if len(finite_rule) else None
        influence.append({
            "category": category, "history": history,
            "max_bound_influence_scenario": row.scenario if row is not None else "no_finite_bound",
            "max_absolute_bound_shift_ma": abs(row.bound_shift_from_baseline_ma) if row is not None else np.nan,
            "signed_bound_shift_ma": row.bound_shift_from_baseline_ma if row is not None else np.nan,
            "max_candidate_comparison_influence_scenario": candidate_row.scenario if candidate_row is not None else "no_finite_bound",
            "max_absolute_candidate_margin_shift_ma": abs(candidate_row.candidate_margin_shift_from_baseline_ma) if candidate_row is not None else np.nan,
            "signed_candidate_margin_shift_ma": candidate_row.candidate_margin_shift_from_baseline_ma if candidate_row is not None else np.nan,
            "max_source_rule_comparison_influence_scenario": rule_row.scenario if rule_row is not None else "no_finite_bound",
            "max_absolute_source_rule_margin_shift_ma": abs(rule_row.source_rule_margin_shift_from_baseline_ma) if rule_row is not None else np.nan,
            "signed_source_rule_margin_shift_ma": rule_row.source_rule_margin_shift_from_baseline_ma if rule_row is not None else np.nan,
        })
    paths = {
        "boundary_scenarios.csv": pd.concat(boundary_rows, ignore_index=True),
        "unit_age_mapping.csv": pd.concat(mappings, ignore_index=True),
        "effort_scenarios.csv": pd.concat(efforts, ignore_index=True),
        "bound_sensitivity.csv": bound_table,
        "max_influence.csv": pd.DataFrame(influence),
    }
    output_paths = []
    for filename, table in paths.items():
        path = output / filename
        table.to_csv(path, index=False, lineterminator="\n", float_format="%.12g")
        output_paths.append(path)
    after = {str(path.relative_to(ROOT)): sha256(path) for path in inputs}
    if before != after:
        raise RuntimeError("timescale inputs changed during execution")
    receipt = {
        "scenario_basis": {
            "baseline": "zero shift",
            "all_younger": "every boundary minus one quoted base_unc_ma",
            "all_older": "every boundary plus one quoted base_unc_ma",
            "alternating_a_b": "opposite-sign uncertainty basis, globally scaled to retain strict stage order with 1 percent gap reserve",
        },
        "pbdb_mapping_rule": f"move both endpoints only when both match project boundaries within {BOUNDARY_TOL} Ma; otherwise retain numerical support",
        "candidate_431_2_rule": "retain published numerical 431.2; report a conditional within-Sheinwoodian fractional mapping; and separately reapply the source Homerian-base-plus-quoted-uncertainty rule on the current shifted scale",
        "b0_membership_source": b0_source,
        "inputs": before,
        "outputs": {str(path.relative_to(ROOT)): sha256(path) for path in output_paths},
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__},
        "scope": "deterministic shared-boundary sensitivity; quoted uncertainties are not independent uniforms, priors, or propagated confidence distributions",
        "residual_age_uncertainty": "source correlations, biozone/order constraints, non-ICS PBDB numerical supports and uncertainty in published fossil assignments remain outside these scenarios",
    }
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return bound_table, pd.DataFrame(influence)


def main():
    bounds, influence = run()
    print(bounds[["scenario", "category", "history", "n_guaranteed", "oldest_possible_ma", "older_bound_ma",
                  "candidate_same_scale_ma", "margin_to_same_scale_candidate_ma"]].to_string(index=False))
    print("\nMaximum influence by cell")
    print(influence.to_string(index=False))


if __name__ == "__main__":
    main()
