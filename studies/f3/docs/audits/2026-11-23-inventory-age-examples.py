# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy"]
# ///
"""Write two possible S2b age assignments to stdout and their checks to stderr."""

import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kstwo


F3 = Path(__file__).resolve().parents[2]
MODEL = F3 / "models/loop3"
sys.path.insert(0, str(MODEL))
from histories import load_histories
from interval_feasibility import witness_allocation


def main():
    stages = pd.read_csv(F3.parents[1] / "data/timescale.csv").set_index("stage").base_ma
    cutoff, boundary = stages["Eifelian"], stages["Lochkovian"]
    units = pd.read_csv(MODEL / "out/inventory_symmetry_units.csv")
    guaranteed = units[(units.counting == "locality_age") & (units.min_ma >= cutoff)
                       & (units.max_ma > cutoff)].sort_values("unit_id")
    s1, s2a, s2b = (guaranteed[guaranteed["set"] == label].reset_index(drop=True)
                    for label in ("S1", "S2a", "S2b"))
    restored = ~s2b.unit_id.isin(s2a.unit_id)
    assert set(s2a.unit_id) <= set(s2b.unit_id) and len(s2b) == 59 and restored.sum() == 21
    assert (s2b.loc[restored, "min_ma"] == cutoff).all() and (s2b.loc[restored, "max_ma"] == boundary).all()

    history = load_histories()["decline10"]
    effort = pd.read_csv(F3 / "data/macro/effort_reviewed.csv").query("region == 'global'")
    edges = np.unique(np.r_[np.arange(cutoff, stages["Darriwilian"], 0.05), effort.young_ma, effort.old_ma])
    midpoints = (edges[1:] + edges[:-1]) / 2
    exposure = np.r_[0, np.cumsum(np.diff(edges) * np.exp(-(midpoints - cutoff) / 10))]

    def score(label, ages):
        # Condition on the actual oldest age of this assignment, leaving 58 ranks on S2b.
        x = np.sort(np.interp(ages, edges, exposure))
        u = x[:-1] / x[-1]
        ranks = np.arange(1, len(u) + 1)
        d = max(np.max(ranks / len(u) - u), np.max(u - (ranks - 1) / len(u)))
        p = kstwo.sf(d, len(u))
        print(f"{label}: max {max(ages):.4f} Ma, D {d:.9f}, exact p {p:.9g}", file=sys.stderr)
        return p

    def example(ranges):
        w, _, _, _ = witness_allocation(ranges.assign(recorded_min_ma=ranges.min_ma), history)
        assert w.unit_id.equals(ranges.unit_id)
        ages = w.allocated_ma.to_numpy()
        low, high = ranges.min_ma.to_numpy(), ranges.max_ma.to_numpy()
        assert np.all(ages >= low - 2e-9) and np.all(ages <= high + 2e-9)
        return np.round(np.clip(ages, low, high), 12)

    score("S2b at midpoints", (s2b.min_ma + s2b.max_ma) / 2)
    saved = s2b[["member_ids", "min_ma", "max_ma"]].copy()
    assert saved.member_ids.is_unique
    saved["restored_in_s2b"] = restored
    first_two = s2b.member_ids.isin(["pbdb:10625", "pbdb:20841"])
    assert first_two.sum() == 2 and restored[first_two].all()
    for n_young, young in ((2, first_two), (21, restored)):
        ranges = s2b.copy()
        ranges.loc[young, "max_ma"] = 399.9
        ranges.loc[restored & ~young, "min_ma"] = 400.1
        ages = example(ranges)
        assert (ages[restored] < 400).sum() == n_young
        assert score(f"S2b, {n_young} restored younger than 400 Ma", ages) > 0.05
        saved[f"example_{n_young}_younger_ma"] = ages

    outer = s2b.copy()
    for member, stage_base in (("pbdb:25242", "Pragian"), ("pbdb:34965", "Emsian")):
        match = outer.member_ids == member
        assert match.sum() == 1 and restored[match].all()
        outer.loc[match, "min_ma"] = stages[stage_base]
    score("S2b, Newton Dingle and La Gileppe restricted to full source stages", example(outer))

    devonian = s1.max_ma <= boundary
    assert len(s1) == 69 and devonian.sum() == 53 and (s1.min_ma >= boundary).sum() == 13
    score("S1, recorded ranges", example(s1))
    wider = s1.copy()
    wider.loc[devonian, ["min_ma", "max_ma"]] = [cutoff, boundary]
    score("S1, only Devonian-only ranges widened to their epoch", example(wider))

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(saved.columns)
    for ids, low, high, added, two, all_restored in saved.itertuples(index=False, name=None):
        writer.writerow([ids, low, high, str(added).lower(), f"{two:.12f}", f"{all_restored:.12f}"])


if __name__ == "__main__":
    main()
