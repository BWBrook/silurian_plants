"""Combined outside measures for early crown vascular-plant finding (studies/f3/docs/plan-rulers.md, addendum
of 14 November 2026, chosen after the single measures were seen; a guide with no confidence level).

If finding is proportional to a proxy x(s) over [c, t], the chance that all n finds fall after A depends
only on the share of the integral of x before A. With Q = mean x over [c, A] / mean x over [A, t], the
expected early finds at the later rate n/(A - c) are E = n (t - A) / ((A - c) Q), the chance of no early
find is (1 + E/n)^(-n), and the ancestor fits the oldest find when E <= m*(n) = n(0.05^(-1/n) - 1) (C58).
The ratio_of_product_means rows use that proportional history. The product_of_ratios rows instead
assume that the ratio of mean finding rates equals the product of the two single-measure ratios.

    python3 studies/f3/models/loop3/combined_rulers.py
"""

import csv
import math

from rulers import OUT, ROOT, STEP, read, rock, search, spores, stages

COUNTS = (48, 24, 19, 15)
CANDIDATES = (444.0, 452.0)
GRID = [round(427.0 + 0.5 * i, 2) for i in range(85)]
OVERLAP_STAGES = ("Katian", "Hirnantian", "Rhuddanian", "Aeronian", "Telychian", "Sheinwoodian", "Homerian",
                  "Gorstian", "Ludfordian", "Pridoli", "Lochkovian", "Pragian", "Emsian")


def mean(x, lo, hi):
    n = round((hi - lo) / STEP)
    return sum(x(lo + (i + 0.5) * STEP) for i in range(n)) / n


def m_star(n):
    return n * (0.05 ** (-1 / n) - 1)


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return num / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))


def spearman_exact_p(a, b):
    """Two-sided permutation p for Spearman's rho, by exhaustive enumeration when feasible, else 200000 shuffles."""
    import itertools
    import random
    ra, rb = ranks(a), ranks(b)
    obs = abs(pearson(ra, rb))
    n = len(a)
    if n <= 9:
        perms = itertools.permutations(rb)
        hits = total = 0
        for p in perms:
            total += 1
            hits += abs(pearson(ra, list(p))) >= obs - 1e-12
        return hits / total
    rng = random.Random(20261114)
    hits, total = 0, 200000
    rb = list(rb)
    for _ in range(total):
        rng.shuffle(rb)
        hits += abs(pearson(ra, rb)) >= obs - 1e-12
    return (hits + 1) / (total + 1)


def main():
    bound = next(r for r in read(OUT / "reviewed_bounds.csv")
                 if (r["category"], r["reading"], r["units"], r["variant"], r["excluded_region"], r["cutoff"], r["history"])
                 == ("B2", "main", "locality_age", "primary", "", "Emsian", "flat"))
    A, c = float(bound["oldest_possible_ma"]), float(bound["cutoff_ma"])
    L = A - c
    rock_x, _ = rock({"non-marine"})
    spore_x = spores()
    search_x = search("all_density_per_myr")
    search_px = search("plant_excluded_density_per_myr")
    singles = {"rock": rock_x, "spore_share": spore_x, "search": search_x, "search_plant_excluded": search_px}
    combos = {"rock_x_spore_share": ("rock", "spore_share"), "search_x_spore_share": ("search", "spore_share"),
              "search_plant_excluded_x_spore_share": ("search_plant_excluded", "spore_share")}

    def q_single(name, t):
        x = singles[name]
        return mean(x, c, A) / mean(x, A, t)

    def q_product(a, b, t):
        xa, xb = singles[a], singles[b]
        prod = lambda s: xa(s) * xb(s)  # noqa: E731
        early = mean(prod, A, t)
        return mean(prod, c, A) / early if early > 0 else float("inf")

    rows = []
    for key, (a, b) in combos.items():
        for t in CANDIDATES:
            qa, qb = q_single(a, t), q_single(b, t)
            forms = {"product_of_ratios": qa * qb, "ratio_of_product_means": q_product(a, b, t)}
            for form, q in forms.items():
                for n in COUNTS:
                    e = n * (t - A) / (L * q)
                    rows.append([key, form, f"{t:g}", n, f"{qa:.4f}", f"{qb:.4f}", f"{q:.4f}", f"{e:.4f}",
                                 f"{m_star(n):.4f}", f"{(1 + e / n) ** (-n):.4f}", "fits" if e <= m_star(n) else "exceeds"])
    with open(OUT / "combined_rulers.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["combination", "form", "candidate_ma", "n", "q_first", "q_second", "q_combined",
                    "expected_early_finds", "limit_expected_early_finds", "p_no_early_find", "verdict"])
        w.writerows(rows)

    with open(OUT / "combined_rulers_curve.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["combination", "candidate_ma", "q_combined"] + [f"expected_early_n{n}" for n in COUNTS])
        for key, (a, b) in combos.items():
            for t in GRID:
                q = q_product(a, b, t)
                w.writerow([key, f"{t:g}", f"{q:.4f}"] + [f"{n * (t - A) / (L * q):.4f}" for n in COUNTS])  # inf q gives 0

    st = stages()
    series = {name: [mean(x, *sorted(st[s])) for s in OVERLAP_STAGES] for name, x in singles.items()}
    with open(OUT / "combined_rulers_stages.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["stage", "top_ma", "base_ma"] + list(series))
        for i, s in enumerate(OVERLAP_STAGES):
            w.writerow([s, f"{st[s][0]:g}", f"{st[s][1]:g}"] + [f"{series[k][i]:.6g}" for k in series])
    pairs = [("rock", "spore_share"), ("rock", "search"), ("search", "spore_share"), ("rock", "search_plant_excluded")]
    with open(OUT / "combined_rulers_overlap.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["first", "second", "stages", "spearman_rho", "permutation_p", "pearson_log"])
        for a, b in pairs:
            va, vb = series[a], series[b]
            rho = pearson(ranks(va), ranks(vb))
            logr = pearson([math.log(v) for v in va], [math.log(v) for v in vb]) if min(va + vb) > 0 else float("nan")
            w.writerow([a, b, len(va), f"{rho:.4f}", f"{spearman_exact_p(va, vb):.4f}", f"{logr:.4f}"])
    placement(singles, combos, A, c)
    for r in rows:
        if r[0] == "rock_x_spore_share" and r[3] in (48, 15):
            print(r)


def binom_tail(n, k, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def placement(singles, combos, A, c):
    """Where would the later finds lie if finding tracked each measure stage by stage? Compare the share of
    the later window's proxy integral in a late-Silurian interval with the finds whose whole age range lies
    there (a guaranteed minimum): 13 of 48 locality-age finds, 6 of 19 region-and-stage finds, for both
    Gorstian-Pridoli (Lochkovian base to A) and Ludfordian-Pridoli (Lochkovian base to Gorstian top).
    These are fixed-window allocation benchmarks. A and the interval splits were chosen from the
    observed age supports; the binomial tails do not calibrate that selection or condition on an
    exact oldest find. Treating regional cells as iid draws is a separate counting scenario.
    """
    st = stages()
    lochkovian_base, ludfordian_base = st["Lochkovian"][1], st["Ludfordian"][1]
    finds = [r for r in read(OUT / "primary_unit_membership.csv")
             if r["category"] == "B2" and r["reading"] == "main" and float(r["min_ma"]) >= c and float(r["max_ma"]) <= A + 1e-9]
    proxies = {"level": lambda s: 1.0, **singles}
    for key, (a, b) in combos.items():
        proxies[key] = (lambda xa, xb: lambda s: xa(s) * xb(s))(singles[a], singles[b])
    with open(OUT / "combined_rulers_placement.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["proxy", "interval", "interval_ma", "share", "counting", "n", "observed", "expected", "p_at_least_observed"])
        for interval, top in (("Gorstian-Pridoli", A), ("Ludfordian-Pridoli", ludfordian_base)):
            late = [r for r in finds if float(r["min_ma"]) >= lochkovian_base and float(r["max_ma"]) <= top + 1e-9]
            counts = {"locality_age": (len(finds), len(late)),
                      "region_stage": (19, len({(r["region"], r["min_ma"], r["max_ma"]) for r in late}))}
            assert counts == {"locality_age": (48, 13), "region_stage": (19, 6)}, counts
            for key, x in proxies.items():
                share = mean(x, lochkovian_base, top) * (top - lochkovian_base) / (mean(x, c, A) * (A - c))
                for counting, (n, k) in counts.items():
                    w.writerow([key, interval, f"{lochkovian_base:g}-{top:g}", f"{share:.4f}", counting, n, k,
                                f"{n * share:.3f}", f"{binom_tail(n, k, share):.3g}"])


if __name__ == "__main__":
    main()
