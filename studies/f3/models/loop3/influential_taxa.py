# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Targeted leave-group-out checks for influential body-fossil units."""

import hashlib
import json
from pathlib import Path

import pandas as pd

from analysis import envelope, select_records
from histories import CUTOFFS, load_histories

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
UNITS = "locality_age"
CUTOFF_NAME = "Emsian"
GROUPS = {
    "yea_baragwanathia": {
        "categories": ("B2",),
        "members": {"tail:M-ghin-ghin", "tail:M-ghin-ghin-b2", "tail:M-limestone-road"},
    },
    "bathurst_zosterophyllum": {
        "categories": ("B2",),
        "members": {"tail:M-bathurst-us383", "tail:M-bathurst-us384", "tail:M-bathurst-us385",
                    "tail:M-bathurst-us688", "pbdb:11421", "pbdb:11425"},
    },
    "cooksonia_barrandei": {
        "categories": ("B0", "B1"),
        "members": {"tail:M-barrandei"},
    },
}


def contains_member(value, members):
    return any(member in members for member in str(value).split(";"))


def main():
    inputs = [ROOT / "studies/f3/data/macro/horizons_reviewed.csv", ROOT / "studies/f3/data/macro/effort_reviewed.csv",
              ROOT / "data/timescale.csv", HERE / "analysis.py", HERE / "endpoint.py",
              HERE / "histories.py", Path(__file__).resolve()]
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    h = pd.read_csv(inputs[0])
    histories = load_histories()
    cutoff = CUTOFFS[CUTOFF_NAME]
    rows = []
    for group_name, specification in GROUPS.items():
        for category in specification["categories"]:
            for reading in ("main", "inclusive"):
                baseline = select_records(h, category, reading=reading, units=UNITS)
                remove = baseline.member_ids.map(lambda value: contains_member(value, specification["members"]))
                reduced = baseline[~remove].copy()
                removed_ids = sorted(set(";".join(baseline.loc[remove, "member_ids"]).split(";")))
                removed_ids = [value for value in removed_ids if value]
                for history, recovery in histories.items():
                    base_fit, base_possible, base_certain, base_oldest = envelope(baseline, recovery, cutoff)
                    reduced_fit, reduced_possible, reduced_certain, reduced_oldest = envelope(reduced, recovery, cutoff)
                    rows.append({"comparison": group_name, "category": category, "reading": reading,
                                 "units": UNITS, "cutoff": CUTOFF_NAME, "cutoff_ma": cutoff,
                                 "history": history, "target_members": ";".join(sorted(specification["members"])),
                                 "removed_members": ";".join(removed_ids), "n_units_removed": int(remove.sum()),
                                 "baseline_n_possible": base_possible, "excluded_n_possible": reduced_possible,
                                 "baseline_n_guaranteed": base_certain, "excluded_n_guaranteed": reduced_certain,
                                 "baseline_oldest_possible_ma": base_oldest,
                                 "excluded_oldest_possible_ma": reduced_oldest,
                                 "baseline_older_bound_ma": base_fit.bound_ma,
                                 "excluded_older_bound_ma": reduced_fit.bound_ma,
                                 "delta_bound_ma": reduced_fit.bound_ma - base_fit.bound_ma,
                                 "baseline_status": base_fit.status, "excluded_status": reduced_fit.status,
                                 "interpretation": "targeted leave-group-out sensitivity at the same unit and cutoff"})
    after = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    if before != after:
        raise RuntimeError("influential-taxon inputs drifted")
    output = OUT / "influential_taxa.csv"
    pd.DataFrame(rows).to_csv(output, index=False, lineterminator="\n", float_format="%.10g")
    receipt = {"unit_treatment": UNITS, "fixed_cutoff": CUTOFF_NAME, "fixed_cutoff_ma": cutoff,
               "groups": {key: {"categories": list(value["categories"]),
                                 "members": sorted(value["members"])} for key, value in GROUPS.items()},
               "inputs": before, "outputs": {str(output.relative_to(ROOT)): digest(output)},
               "rows": len(rows),
               "scope": "targeted leave-group-out sensitivity; fossil identity and age ranges otherwise unchanged"}
    (OUT / "influential_taxa_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(pd.DataFrame(rows).query("reading == 'main' and history == 'flat'")[
        ["comparison", "category", "n_units_removed", "baseline_oldest_possible_ma",
         "excluded_oldest_possible_ma", "baseline_older_bound_ma", "excluded_older_bound_ma",
         "delta_bound_ma"]].to_string(index=False))


if __name__ == "__main__":
    main()
