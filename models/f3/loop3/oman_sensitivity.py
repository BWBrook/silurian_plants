# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""B0 with the Katian Oman sporangial fragments (review C, C1/R2).

Loop 3's declared B0 is "accepted land-plant macro- or mesofossil, sterile axes included"
(docs/plan-loop3.md). The frozen inventory takes its curated tail from E3-E5 only, so the Ghaba-1
spore-filled sporangial fragments (S-w22-K12, E2, main reading, Katian) never entered B0. This
additive sensitivity adds them as one locality-age unit and recomputes the B0 envelopes with the
frozen code and inputs. Frozen outputs are read, never rewritten.
"""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analysis import AGE_DRAWS, SEED, envelope, select_records, shape_check
from endpoint import known_cutoff_bound
from histories import CUTOFFS, load_histories

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SPORE_CERTAIN_MA = 458.2
OMAN = {"unit_id": "Oman|ghaba-1 borehole|Katian", "min_ma": 445.2, "max_ma": 452.8,
        "region": "Gondwana-North-Africa-Arabia", "member_ids": "tail:S-w22-K12", "n_members": 1}


def main():
    inputs = [ROOT / "data/macro/horizons_reviewed.csv", ROOT / "data/macro/effort_reviewed.csv",
              ROOT / "data/occurrences/observations.csv", ROOT / "data/occurrences/reading_assignments.csv",
              ROOT / "data/timescale.csv", HERE / "analysis.py", HERE / "endpoint.py", HERE / "histories.py",
              Path(__file__).resolve()]
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    ra = pd.read_csv(inputs[3])
    k12 = ra[ra.obs_id.eq("S-w22-K12")]
    if set(k12.reading_id) < {"main", "inclusive"} or not (k12.stage_oldest.eq("Katian") & k12.stage_youngest.eq("Katian")).all():
        raise ValueError("S-w22-K12 is no longer Katian in main and inclusive readings")
    h = pd.read_csv(inputs[0])
    histories = load_histories()
    rows, shape = [], []
    rng = np.random.default_rng(SEED)
    for reading in ("main", "inclusive"):
        frozen = select_records(h, "B0", reading)
        with_oman = pd.concat([frozen, pd.DataFrame([OMAN])], ignore_index=True)
        for inventory, r in (("frozen_E3_E5_tail", frozen), ("with_oman_fragments", with_oman)):
            for cutoff_name, cutoff in CUTOFFS.items():
                for history, recovery in histories.items():
                    fit, possible, certain, oldest = envelope(r, recovery, cutoff)
                    rows.append({"category": "B0", "reading": reading, "inventory": inventory,
                                 "cutoff": cutoff_name, "cutoff_ma": cutoff, "history": history,
                                 "n_possible": possible, "n_guaranteed": certain, "oldest_possible_ma": oldest,
                                 "older_bound_ma": fit.bound_ma, "status": fit.status,
                                 "separation_from_458_2_myr": SPORE_CERTAIN_MA - fit.bound_ma
                                 if fit.status == "bounded" else np.nan})
            cutoff = CUTOFFS["Emsian"]
            draws = rng.uniform(r.min_ma.values, r.max_ma.values, size=(AGE_DRAWS, len(r)))
            for history, recovery in histories.items():
                checks = np.array([shape_check(a, recovery, cutoff) for a in draws])
                limits = [known_cutoff_bound(a[a >= cutoff], recovery, cutoff) for a in draws]
                finite = np.sort([f.bound_ma if f.status in ("bounded", "at_boundary") else np.inf for f in limits])
                d, p = shape_check((r.min_ma.values + r.max_ma.values) / 2, recovery, cutoff)
                shape.append({"category": "B0", "reading": reading, "inventory": inventory, "history": history,
                              "midpoint_nominal_p": p,
                              "independent_uniform_p_q05": np.quantile(checks[:, 1], .05),
                              "independent_uniform_p_q95": np.quantile(checks[:, 1], .95),
                              "independent_uniform_bound_median_ma": finite[len(finite) // 2],
                              "interpretation": "age-allocation sensitivity; not confidence bounds or a combined test"})
    after = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    if before != after:
        raise RuntimeError("inputs drifted")
    t = pd.DataFrame(rows)
    frozen = pd.read_csv(OUT / "reviewed_bounds.csv")
    frozen = frozen[(frozen.category == "B0") & (frozen.units == "locality_age") & (frozen.variant == "primary")
                    & frozen.excluded_region.isna()]
    check = t[t.inventory.eq("frozen_E3_E5_tail")].merge(frozen, on=["reading", "cutoff", "history"], suffixes=("", "_frozen"))
    if len(check) != 48 or not np.allclose(check.older_bound_ma, check.older_bound_ma_frozen, equal_nan=True):
        raise RuntimeError("frozen B0 bounds not reproduced")
    a, b = OUT / "oman_sensitivity.csv", OUT / "oman_shape.csv"
    pd.DataFrame(rows).to_csv(a, index=False, lineterminator="\n", float_format="%.8f")
    pd.DataFrame(shape).to_csv(b, index=False, lineterminator="\n", float_format="%.10g")
    receipt = {"seed": SEED, "added_unit": OMAN, "inputs": before,
               "outputs": {str(p.relative_to(ROOT)): digest(p) for p in (a, b)},
               "scope": "declared sensitivity for the B0 definition; frozen Loop 3 outputs unchanged"}
    (OUT / "oman_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(t[(t.cutoff == "Emsian")][["reading", "inventory", "history", "n_guaranteed", "oldest_possible_ma",
                                      "older_bound_ma", "status", "separation_from_458_2_myr"]].to_string(index=False))


if __name__ == "__main__":
    main()
