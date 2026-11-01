# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Retrospective stage-break sensitivity, not selection-adjusted confidence inference."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

import analysis
from endpoint import PiecewiseRecovery
from histories import DOMAIN, YOUNG, load_histories

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "out"
BREAKS = (419.62, 426.7, 432.9)
MULTIPLIERS = (1., .5, .1, .01)


def step_history(baseline, break_ma, older_multiplier):
    if not 0 < older_multiplier <= 1:
        raise ValueError("older multiplier must lie in (0,1]")
    edges = np.unique(np.r_[baseline.edges_ma, break_ma])
    if edges[0] != baseline.edges_ma[0] or edges[-1] != baseline.edges_ma[-1]:
        raise ValueError("break outside declared domain")
    mid = (edges[:-1] + edges[1:]) / 2
    idx = np.searchsorted(baseline.edges_ma, mid, side="right") - 1
    density = baseline.density_per_myr[idx] * np.where(mid >= break_ma, older_multiplier, 1.)
    return PiecewiseRecovery(edges, density)


def main():
    inputs = [ROOT / "data/macro/horizons_reviewed.csv", ROOT / "data/macro/effort_reviewed.csv",
              ROOT / "data/macro/build_receipt.json", ROOT / "data/timescale.csv",
              HERE / "analysis.py", HERE / "histories.py", HERE / "endpoint.py", Path(__file__).resolve()]
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    h = pd.read_csv(inputs[0])
    histories = load_histories()
    rows = []
    for reading in ("main", "inclusive"):
        for category in ("B0", "B1", "B2"):
            records = analysis.select_records(h, category, reading)
            midpoint = (records.min_ma.values + records.max_ma.values) / 2
            for baseline in ("flat", "pbdb_all"):
                for break_ma in BREAKS:
                    for multiplier in MULTIPLIERS:
                        recovery = step_history(histories[baseline], break_ma, multiplier)
                        fit, possible, certain, oldest = analysis.envelope(records, recovery, YOUNG)
                        d, p = analysis.shape_check(midpoint, recovery, YOUNG)
                        modified_support = int((records.max_ma > break_ma).sum())
                        rows.append({"category": category, "reading": reading, "baseline": baseline,
                                     "break_ma": break_ma, "older_multiplier": multiplier,
                                     "n_guaranteed": certain, "n_possible": possible, "oldest_possible_ma": oldest,
                                     "n_units_support_older_than_break": modified_support,
                                     "n_units_guaranteed_older_than_break": int((records.min_ma > break_ma).sum()),
                                     "modified_segment_overlaps_age_support": modified_support > 0,
                                     "older_bound_ma": fit.bound_ma, "status": fit.status,
                                     "domain_max_ma": DOMAIN, "midpoint_shape_D": d, "midpoint_nominal_shape_p": p,
                                     "interpretation": "retrospective sensitivity using 0.05 endpoint rule; no nominal or selection-adjusted confidence claim"})
    out = OUT / "suppression_sensitivity.csv"
    pd.DataFrame(rows).to_csv(out, index=False, lineterminator="\n", float_format="%.10g")
    if before != {str(p.relative_to(ROOT)): sha(p) for p in inputs}:
        raise RuntimeError("suppression inputs drifted")
    (OUT / "suppression_receipt.json").write_text(json.dumps({"inputs": before, "outputs": {str(out.relative_to(ROOT)): sha(out)},
        "breaks_ma": BREAKS, "older_multipliers": MULTIPLIERS, "rows": len(rows),
        "scope": "retrospective complete sensitivity grid; not fitted or selected against clock ages"}, indent=2) + "\n")
    print(pd.DataFrame(rows).query("category == 'B2' and reading == 'main' and baseline == 'flat'")[["break_ma", "older_multiplier", "older_bound_ma", "status", "modified_segment_overlaps_age_support"]].to_string(index=False))


if __name__ == "__main__":
    main()
