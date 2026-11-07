# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Retrospective B2 age-intensity compatibility contours.

The break is fixed after inspection at the oldest permitted fossil age. These
are sensitivity contours under a flat-plus-step recording history, not fitted
rates or a joint confidence region.
"""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analysis import select_records
from histories import YOUNG

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
ALPHA = 0.05
CANDIDATES = (431.2, 432.0, 440.0, 444.0, 447.0, 450.0, 452.0)
DELAYS = (0.0, 5.0, 10.0, 20.0)
UNIT_TREATMENTS = {
    "primary": ("locality_age", "primary"),
    "region_stage": ("region_stage", "primary"),
    "curated": ("locality_age", "curated_tail_only"),
}


def contour(oldest_ma, n_guaranteed, candidate_lineage_ma, diagnostic_delay_myr,
            cutoff_ma=YOUNG, alpha=ALPHA):
    if n_guaranteed <= 0 or not cutoff_ma < oldest_ma:
        raise ValueError("frontier requires a positive count and oldest age above the cutoff")
    candidate_recoverability = candidate_lineage_ma - diagnostic_delay_myr
    extra_exposure = (oldest_ma - cutoff_ma) * (alpha ** (-1.0 / n_guaranteed) - 1.0)
    result = {"candidate_recoverability_ma": candidate_recoverability,
              "extra_earlier_exposure_required": extra_exposure}
    if candidate_recoverability <= oldest_ma:
        result.update({"earlier_to_later_intensity": np.nan,
                       "later_to_earlier_intensity": np.nan,
                       "contour_cdf_at_oldest": np.nan,
                       "status": "candidate_not_older_than_envelope_anchor"})
        return result
    multiplier = extra_exposure / (candidate_recoverability - oldest_ma)
    cdf = ((oldest_ma - cutoff_ma) /
           ((oldest_ma - cutoff_ma) + multiplier * (candidate_recoverability - oldest_ma))) ** n_guaranteed
    result.update({"earlier_to_later_intensity": multiplier,
                   "later_to_earlier_intensity": 1.0 / multiplier,
                   "contour_cdf_at_oldest": cdf,
                   "status": "contour"})
    return result


def main():
    inputs = [ROOT / "data/macro/horizons_reviewed.csv", ROOT / "data/timescale.csv",
              HERE / "analysis.py", HERE / "histories.py", Path(__file__).resolve()]
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    h = pd.read_csv(inputs[0])
    rows = []
    for reading in ("main", "inclusive"):
        for treatment, (units, variant) in UNIT_TREATMENTS.items():
            records = select_records(h, "B2", reading=reading, units=units, variant=variant)
            guaranteed = records[records.min_ma >= YOUNG]
            possible = records[records.max_ma > YOUNG]
            n = len(guaranteed)
            oldest = float(possible.max_ma.max())
            for delay in DELAYS:
                for candidate in CANDIDATES:
                    values = contour(oldest, n, candidate, delay)
                    rows.append({"category": "B2", "reading": reading,
                                 "unit_treatment": treatment, "units": units,
                                 "inventory_variant": variant, "cutoff": "Emsian",
                                 "cutoff_ma": YOUNG, "n_possible": len(possible),
                                 "n_guaranteed": n, "oldest_possible_ma": oldest,
                                 "candidate_lineage_ma": candidate,
                                 "assumed_diagnostic_delay_myr": delay, **values,
                                 "interpretation": (
                                     "retrospective flat-plus-step compatibility contour; "
                                     "not a fitted rate or joint confidence region")})
    after = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    if before != after:
        raise RuntimeError("frontier inputs drifted")
    output = OUT / "frontier.csv"
    pd.DataFrame(rows).to_csv(output, index=False, lineterminator="\n", float_format="%.10g")
    receipt = {"alpha": ALPHA, "fixed_cutoff_ma": YOUNG,
               "candidate_lineage_ages_ma": list(CANDIDATES),
               "assumed_diagnostic_delays_myr": list(DELAYS),
               "inputs": before, "outputs": {str(output.relative_to(ROOT)): digest(output)},
               "rows": len(rows),
               "scope": "retrospective compatibility contours; no fitted rate or joint confidence region"}
    (OUT / "frontier_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(pd.DataFrame(rows).query(
        "reading == 'main' and assumed_diagnostic_delay_myr == 0"
    )[["unit_treatment", "n_guaranteed", "oldest_possible_ma", "candidate_lineage_ma",
       "earlier_to_later_intensity", "later_to_earlier_intensity"]].to_string(index=False))


if __name__ == "__main__":
    main()
