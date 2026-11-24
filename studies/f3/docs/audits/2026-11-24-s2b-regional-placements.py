# /// script
# requires-python = ">=3.12"
# dependencies = ["scipy"]
# ///
"""Enumerate S2b region–stage counts for Table S20's broad interval. Write one row per attainable pair."""

import csv
import sys
from collections import defaultdict
from itertools import pairwise
from pathlib import Path

from scipy.stats import beta, binom


ROOT = Path(__file__).resolve().parents[4]


def read_rows(path):
    with (ROOT / path).open(newline="") as source:
        return list(csv.DictReader(source))


def count_pairs(units, stages, split, include_pooled, move_all):
    late_stages = {name for young, _, name in stages if young >= split}
    regions = defaultdict(lambda: {frozenset()})
    for row in units:
        region = row["region"]
        if not include_pooled and region in {"multiple", "unknown"}:
            continue
        youngest, oldest = float(row["min_ma"]), float(row["max_ma"])
        if move_all or youngest < split < oldest:
            allowed = [name for young, old, name in stages if youngest < old and oldest > young]
        else:
            midpoint = (youngest + oldest) / 2
            allowed = [name for young, old, name in stages if young <= midpoint < old]
        assert allowed, row["unit_id"]
        regions[region] = {occupied | {stage} for occupied in regions[region] for stage in allowed}

    pairs = {(0, 0)}
    for possible_occupancies in regions.values():
        regional = {(len(used), len(used & late_stages)) for used in possible_occupancies}
        pairs = {(total + n, late + k) for total, late in pairs for n, k in regional}
    return sorted(pairs)


def main():
    bases = {r["stage"]: float(r["base_ma"]) for r in read_rows("data/timescale.csv")}
    cutoff, split, edge = (bases[stage] for stage in ("Eifelian", "Lochkovian", "Gorstian"))
    boundaries = sorted((age, name) for name, age in bases.items())
    stages = [(young, old, name) for (young, _), (old, name) in pairwise(boundaries)
              if cutoff <= young and old <= edge]
    shares = {r["stage"]: int(r["n_docs_with_triletes"]) / int(r["n_docs"])
              for r in read_rows("data/spores/effort_global_by_stage.csv")}
    whole = sum((old - young) * shares[name] for young, old, name in stages)
    late = sum((old - young) * shares[name] for young, old, name in stages if young >= split)
    proxy_share = late / whole
    level_share = (edge - split) / (edge - cutoff)

    inventory = read_rows("studies/f3/models/loop3/out/inventory_symmetry_units.csv")
    units = [r for r in inventory if r["set"] == "S2b" and r["counting"] == "locality_age"
             and float(r["min_ma"]) >= cutoff and float(r["max_ma"]) <= edge]
    assert len(units) == 59
    # The signed S2b inventory contains only the lower Ghin Ghin bed from the ordered pair.
    members = {m for r in units for m in r["member_ids"].split(";")}
    assert "tail:M-ghin-ghin" in members and "tail:M-ghin-ghin-b2" not in members

    output = csv.writer(sys.stdout, lineterminator="\n")
    output.writerow(["region_codes", "units_allowed_to_move", "total_cells", "late_silurian_cells",
                     "lower_rate_ratio", "spore_upper_tail_p", "is_min_rate_ratio", "is_max_spore_p"])
    for include_pooled in (False, True):
        for move_all in (False, True):
            pairs = count_pairs(units, stages, split, include_pooled, move_all)
            rates = {
                (n, k): beta.ppf(0.05, k, n - k + 1) / level_share if k else 0.0
                for n, k in pairs
            }
            tails = {(n, k): binom.sf(k - 1, n, proxy_share) for n, k in pairs}
            min_rate, max_tail = min(rates.values()), max(tails.values())
            for n, k in pairs:
                rate, tail = rates[n, k], tails[n, k]
                output.writerow(["named_and_pooled" if include_pooled else "named_only",
                                 "all" if move_all else "boundary_crossers", n, k,
                                 f"{rate:.12f}", f"{tail:.12f}", int(rate == min_rate), int(tail == max_tail)])


if __name__ == "__main__":
    main()
