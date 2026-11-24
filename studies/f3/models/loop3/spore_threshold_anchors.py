"""Spore-share contrast and matching independent-find count at both older window edges (C56, S5.12).

For the share of Palynodata documents reporting triletes, integrated exactly over stage overlaps, the
later and earlier integrals I_L over [c, A] and I_E over [A, t] give the count n at which an ancestor at t
leaves a 5% chance of no find before A: n = ln(20) / ln(1 + I_E / I_L). The restored database-backed (S2b)
regional cell counts at each anchor are copied from the Stage 2 placement rows for its late interval.

    python3 studies/f3/models/loop3/spore_threshold_anchors.py
"""

import csv
import math

from rulers import OUT, ROOT, read, stages

CUTOFF = 393.47
ANCHORS = (("natural", 426.7, "Gorstian-Pridoli"), ("bathurst_425", 425.0, "Ludfordian-Pridoli"))
CANDIDATES = (444.0, 452.0)


def share():
    st = stages()
    return [(st[r["stage"]], int(r["n_docs_with_triletes"]) / int(r["n_docs"]))
            for r in read(ROOT / "data/spores/effort_global_by_stage.csv") if r["stage"] in st]


def integral(pieces, lo, hi):
    return sum(v * max(0.0, min(hi, base) - max(lo, top)) for (top, base), v in pieces)


def cells(run, interval):
    rows = read(OUT / "inventory_symmetry_stage2_tests.csv")
    out = {}
    for counting in ("region_stage_named", "region_stage"):
        r = next(x for x in rows if (x["set"], x["run"], x["test"], x["interval"], x["counting"], x["proxy"])
                 == ("S2b", run, "C59_placement", interval, counting, "spore_share"))
        lo, hi = r["n_range"].split("-")
        out[counting] = (int(lo), int(hi))
    return out


def main():
    pieces = share()
    with open(OUT / "spore_threshold_anchors.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["anchor_ma", "candidate_ma", "later_to_earlier_mean", "matching_n", "largest_whole_n",
                    "p_no_early_find_at_next_whole_n", "s2b_named_cells_min", "s2b_named_cells_max",
                    "s2b_pooled_cells_min", "s2b_pooled_cells_max"])
        for run, a, interval in ANCHORS:
            c = cells(run, interval)
            i_l = integral(pieces, CUTOFF, a)
            for t in CANDIDATES:
                i_e = integral(pieces, a, t)
                ratio = (i_l / (a - CUTOFF)) / (i_e / (t - a))
                n = math.log(20) / math.log1p(i_e / i_l)
                whole = math.floor(n)
                p_next = (i_l / (i_l + i_e)) ** (whole + 1)
                w.writerow([f"{a:g}", f"{t:g}", f"{ratio:.5f}", f"{n:.5f}", whole, f"{p_next:.7f}",
                            *c["region_stage_named"], *c["region_stage"]])
                print(a, t, round(ratio, 5), round(n, 5), whole, round(p_next, 7), c)


if __name__ == "__main__":
    main()
