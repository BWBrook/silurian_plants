"""Reproduce the S2b Silurian-only regional bound after removing Bathurst."""

import csv
import math
from bisect import bisect_right
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CUTOFF = 419.62
BATHURST = {"tail:M-bathurst-us384", "tail:M-bathurst-us385"}


def main():
    with (ROOT / "data/timescale.csv").open() as stream:
        bases = sorted(float(row["base_ma"]) for row in csv.DictReader(stream))
    inventory = ROOT / "studies/f3/models/loop3/out/inventory_symmetry_units.csv"
    cells = {}
    removed = set()
    with inventory.open() as stream:
        for row in csv.DictReader(stream):
            if (row["set"], row["counting"]) != ("S2b", "locality_age"):
                continue
            members = set(row["member_ids"].split(";"))
            if members & BATHURST:
                assert members <= BATHURST
                removed.update(members)
                continue
            young, old = float(row["min_ma"]), float(row["max_ma"])
            stage = bases[bisect_right(bases, (young + old) / 2)]
            cells.setdefault((row["region"], stage), []).append((young, old))
    assert removed == BATHURST

    # A cell's oldest find takes the maximum of its members' ages.
    ranges = {cell: (max(y for y, _ in ages), max(o for _, o in ages))
              for cell, ages in cells.items()}
    certain = {cell: old for cell, (young, old) in ranges.items() if young >= CUTOFF}
    optional = {cell: old for cell, (young, old) in ranges.items() if young < CUTOFF < old}
    assert sorted(region for region, _ in certain) == ["Baltica", "Kazakhstania"]
    assert [region for region, _ in optional] == ["Gondwana-Australia-Antarctica"]
    k = len(certain)
    oldest_certain, oldest_possible = max(certain.values()), max(optional.values())
    assert (oldest_certain, oldest_possible) == (422.7, 426.7)

    print("case\tk\toldest_Ma\tsteady_limit_Ma\tfold_444\tfold_452")
    cases = (("conservative envelope", k, oldest_possible),
             ("Yea outside the window", k, oldest_certain),
             ("Yea inside the window", k + 1, oldest_possible))
    for label, count, oldest in cases:
        gap = (oldest - CUTOFF) * math.expm1(math.log(20) / count)
        print(f"{label}\t{count}\t{oldest:.1f}\t{oldest + gap:.4f}\t"
              f"{(444 - oldest) / gap:.4f}\t{(452 - oldest) / gap:.4f}")


if __name__ == "__main__":
    main()
