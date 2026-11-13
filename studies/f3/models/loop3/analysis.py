# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Conditional positive-record bounds and declared data/age/geographic sensitivities."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from endpoint import known_cutoff_bound, known_cutoff_summary, observed_range_bound
from histories import CUTOFFS, DOMAIN, YOUNG, load_histories, stage_bounds

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SEED = 20261102
AGE_DRAWS = 256


def case_rng(*parts):
    key = "|".join([str(SEED), *map(str, parts)]).encode()
    seed = int.from_bytes(hashlib.sha256(key).digest()[:16], "big")
    return np.random.default_rng(seed)


def select_records(h, category, reading="main", units="locality_age", variant="primary", exclude_region=None,
                   exclude_members=None):
    r = h[h.reading.isin(["all", reading]) & h[category.lower()]].copy()
    if variant == "wide_age":
        include = r.eligible_primary | (r.disposition.eq("wide_age_sensitivity") & (r.max_ma <= DOMAIN))
    elif variant == "unresolved_material":
        include = r.eligible_primary | r.disposition.eq("unresolved_material_sensitivity")
    else:
        include = r.eligible_primary
    r = r[include & (r.max_ma > YOUNG)]
    if variant == "without_low_confidence":
        r = r[~r.low_confidence]
    elif variant == "curated_tail_only":
        r = r[r.source == "tail"]
    elif variant == "without_weak_botanical_source":
        r = r[~r.horizon_id.isin(["pbdb:13895"])]
    elif variant == "kosov_podolia_links":
        r.loc[r.horizon_id.isin(["pbdb:14045", "tail:M-bohemica"]), "locality"] = "sensitivity:kosov"
        r.loc[r.horizon_id.isin(["pbdb:13873", "pbdb:52702"]), "locality"] = "sensitivity:podolia"
    if exclude_region is not None:
        r = r[r.region != exclude_region]
    if exclude_members:
        r = r[~r.horizon_id.isin(exclude_members)]
    if units == "collection":
        r["unit_id"] = r.horizon_id
    elif units == "locality_age":
        r["unit_id"] = r.locality + "|" + r.age_group
    elif units == "locality":
        r["unit_id"] = r.locality
    elif units == "region_stage":
        _, old = stage_bounds(np.minimum(DOMAIN, (r.min_ma.values + r.max_ma.values) / 2))
        r["unit_id"] = r.region + "|midpoint-stage:" + pd.Series(old, index=r.index).astype(str)
    else:
        raise ValueError(units)
    if variant == "kosov_podolia_links":
        linked = r.locality.str.startswith("sensitivity:")
        r.loc[linked, "unit_id"] = r.loc[linked, "locality"]
    return r.groupby("unit_id", as_index=False).agg(
        min_ma=("min_ma", "max"), max_ma=("max_ma", "max"), region=("region", "first"),
        member_ids=("horizon_id", lambda x: ";".join(sorted(set(x)))), n_members=("horizon_id", "size"))


def envelope(r, recovery, cutoff):
    possible = r[r.max_ma > cutoff]
    certain = possible[possible.min_ma >= cutoff]
    if possible.empty:
        oldest = cutoff
    else:
        oldest = possible.max_ma.max()
    fit = known_cutoff_summary(len(certain), oldest, recovery, cutoff)
    return fit, len(possible), len(certain), oldest


def shape_check(ages, recovery, cutoff):
    used = np.asarray(ages)[np.asarray(ages) >= cutoff]
    if len(used) < 3:
        return np.nan, np.nan
    exposure = np.sort(recovery.exposure(used) - recovery.exposure(cutoff))
    if exposure[-1] <= 0:
        return np.nan, np.nan
    test = stats.kstest(exposure[:-1] / exposure[-1], "uniform", method="asymp")
    return float(test.statistic), float(test.pvalue)


def row_for(r, history, recovery, category, reading, units, variant, cutoff_name, excluded_region=""):
    cutoff = CUTOFFS[cutoff_name]
    fit, possible, certain, oldest = envelope(r, recovery, cutoff)
    return {"category": category, "reading": reading, "units": units, "variant": variant,
            "excluded_region": excluded_region, "cutoff": cutoff_name, "cutoff_ma": cutoff,
            "history": history, "age_rule": "conservative range envelope", "n_possible": possible,
            "n_guaranteed": certain, "oldest_possible_ma": oldest,
            "older_bound_ma": fit.bound_ma, "status": fit.status, "domain_max_ma": DOMAIN,
            "confidence_conditional_on_fixed_history_iid_units": .95}


def main():
    OUT.mkdir(exist_ok=True)
    inputs = [ROOT / "studies/f3/data/macro/horizons_reviewed.csv", ROOT / "studies/f3/data/macro/effort_reviewed.csv",
              ROOT / "studies/f3/data/macro/build_receipt.json", ROOT / "data/timescale.csv",
              HERE / "endpoint.py", HERE / "histories.py", Path(__file__).resolve()]
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    h = pd.read_csv(inputs[0])
    histories = load_histories()
    rows, membership, dates, classical, adequacy = [], [], [], [], []
    for reading in ("main", "inclusive"):
        for category in ("B0", "B1", "B2"):
            r = select_records(h, category, reading)
            membership.extend(r.assign(category=category, reading=reading).to_dict("records"))
            without_oman = (select_records(h, category, reading,
                                           exclude_members={"tail:S-w22-K12"})
                            if category == "B0" else None)
            for name, cutoff in CUTOFFS.items():
                for history, recovery in histories.items():
                    rows.append(row_for(r, history, recovery, category, reading, "locality_age", "primary", name))
                    if without_oman is not None:
                        rows.append(row_for(without_oman, history, recovery, category, reading, "locality_age",
                                            "without_oman_fragments", name))
                inventories = [("primary", r)]
                if without_oman is not None:
                    inventories.append(("without_oman_fragments", without_oman))
                for inventory_variant, inventory in inventories:
                    for mode in ("independent_uniform", "shared_quantile"):
                        if mode == "independent_uniform":
                            rng_key = (reading, category, name, mode)
                            if inventory_variant != "primary":
                                rng_key += (inventory_variant,)
                            rng = case_rng(*rng_key)
                            draws = rng.uniform(inventory.min_ma.values, inventory.max_ma.values,
                                                size=(AGE_DRAWS, len(inventory)))
                        else:
                            q = (np.arange(AGE_DRAWS) + .5)[:, None] / AGE_DRAWS
                            draws = (inventory.min_ma.values +
                                     q * (inventory.max_ma.values - inventory.min_ma.values))
                        for history, recovery in histories.items():
                            limits, statuses, ns = [], [], []
                            for ages in draws:
                                used = ages[ages >= cutoff]
                                f = known_cutoff_bound(used, recovery, cutoff)
                                ns.append(len(used))
                                limits.append(f.bound_ma if f.status in ("bounded", "at_boundary") else np.inf)
                                statuses.append(f.status)
                            a = np.sort(limits)
                            def order_q(q):
                                v = a[min(len(a) - 1, int(q * len(a)))]; return v if np.isfinite(v) else np.nan
                            dates.append({"category": category, "reading": reading,
                                          "variant": inventory_variant, "cutoff": name,
                                          "history": history, "age_rule": mode, "draws": AGE_DRAWS,
                                          "bound_q05_ma": order_q(.05), "bound_median_ma": order_q(.5),
                                          "bound_q95_ma": order_q(.95),
                                          "beyond_domain_fraction": statuses.count("beyond_domain") / AGE_DRAWS,
                                          "undefined_fraction": statuses.count("undefined") / AGE_DRAWS,
                                          "n_min": min(ns), "n_max": max(ns),
                                          "interpretation": "age-allocation sensitivity; quantiles are not confidence bounds"})
                            if name == "Emsian":
                                checks = np.array([shape_check(a, recovery, cutoff) for a in draws])
                                midpoint = (inventory.min_ma.values + inventory.max_ma.values) / 2
                                d, p = shape_check(midpoint, recovery, cutoff)
                                adequacy.append({"category": category, "reading": reading,
                                                 "variant": inventory_variant, "history": history,
                                                 "age_rule": mode, "midpoint_D": d, "midpoint_nominal_p": p,
                                                 "imputed_D_q05": np.quantile(checks[:, 0], .05),
                                                 "imputed_D_q95": np.quantile(checks[:, 0], .95),
                                                 "imputed_nominal_p_q05": np.quantile(checks[:, 1], .05),
                                                 "imputed_nominal_p_q95": np.quantile(checks[:, 1], .95),
                                                 "interpretation": "conditional-max KS; asymptotic exact-age p only; imputation spread not a combined test"})
                    midpoint = ((inventory.min_ma + inventory.max_ma) / 2).values
                    used = midpoint[midpoint >= cutoff]
                    f = observed_range_bound(used, histories["flat"])
                    classical.append({"category": category, "reading": reading,
                                      "variant": inventory_variant, "cutoff": name,
                                      "n": len(used), "older_bound_ma": f.bound_ma, "status": f.status,
                                      "interpretation": "classical observed-range comparison at midpoint ages; conditional only"})
    for category in ("B0", "B1", "B2"):
        scenarios = [(u, "primary", None) for u in ("collection", "locality", "region_stage")]
        scenarios += [("locality_age", v, None) for v in ("wide_age", "unresolved_material", "without_low_confidence",
                      "curated_tail_only", "without_weak_botanical_source", "kosov_podolia_links")]
        regions = sorted(h[h.eligible_primary & h.reading.isin(["all", "main"]) & h[category.lower()]].region.unique())
        scenarios += [("locality_age", "primary", region) for region in regions]
        for units, variant, region in scenarios:
            r = select_records(h, category, units=units, variant=variant, exclude_region=region,
                               exclude_members=None)
            matched = load_histories(exclude_region=region) if region else histories
            for history, recovery in matched.items():
                rows.append(row_for(r, history, recovery, category, "main", units, variant, "Emsian", region or ""))
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "reviewed_bounds.csv", index=False, lineterminator="\n", float_format="%.8f")
    pd.DataFrame(dates).to_csv(OUT / "age_sensitivity.csv", index=False, lineterminator="\n", float_format="%.8f")
    pd.DataFrame(classical).to_csv(OUT / "classical_comparison.csv", index=False, lineterminator="\n", float_format="%.8f")
    pd.DataFrame(membership).to_csv(OUT / "primary_unit_membership.csv", index=False, lineterminator="\n")
    pd.DataFrame(adequacy).to_csv(OUT / "shape_diagnostics.csv", index=False, lineterminator="\n", float_format="%.10g")
    delay = []
    primary = result[(result.reading == "main") & (result.cutoff == "Emsian") &
                     (result.units == "locality_age") & (result.variant == "primary") & result.excluded_region.eq("")]
    for r in primary.itertuples():
        for lag in (0, 5, 10, 20):
            delay.append({"category": r.category, "history": r.history, "assumed_delay_myr": lag,
                          "recoverability_bound_ma": r.older_bound_ma,
                          "lineage_bound_if_delay_fixed_ma": r.older_bound_ma + lag,
                          "lineage_domain_max_ma": DOMAIN + lag,
                          "status": r.status, "interpretation": "assumed delay, not inferred or transferred from spores"})
    pd.DataFrame(delay).to_csv(OUT / "delay_sensitivity.csv", index=False, lineterminator="\n", float_format="%.8f")
    after = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    if before != after:
        raise RuntimeError("analysis inputs drifted")
    outputs = [OUT / n for n in ("reviewed_bounds.csv", "age_sensitivity.csv", "classical_comparison.csv",
                                 "primary_unit_membership.csv", "delay_sensitivity.csv", "shape_diagnostics.csv")]
    receipt = {"seed": SEED, "age_draws_per_cell": AGE_DRAWS,
               "age_rng": "SHA-256 keyed per reading/category/cutoff/rule; first 128 bits",
               "domain_ma": [YOUNG, DOMAIN],
               "inputs": before, "outputs": {str(p.relative_to(ROOT)): digest(p) for p in outputs},
               "bound_rows": len(result), "age_sensitivity_rows": len(dates),
               "scope": "conditional estimates; no empirical qualification or clock-posterior validation"}
    (OUT / "analysis_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(primary[["category", "history", "n_guaranteed", "n_possible", "older_bound_ma", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
