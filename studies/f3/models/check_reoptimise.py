# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Re-evaluate miscovering calibration replicates with a much wider optimiser search.

For each (cell, rep, class) whose stored statistic at the truth exceeded the critical value, rebuild the
replicate from the calibration seed, reproduce the standard statistic, then recompute the null supremum
and the alternative from many extra starts. A null that rises (or an alternative that falls, which cannot
happen) by more than the tolerance means the standard search missed an optimum in the anti-conservative
direction.

    uv run models/f3/check_reoptimise.py models/f3/out/validation_cal_reps.csv.gz models/f3/out/reoptimise_cal.csv 60

Run on nectar (c3.3xlarge, 62 workers, 2026-10-29) for the second-review rehearsal; the output is
out/reoptimise_cal.csv. A wider local search is not a global-optimality certificate.
"""

import csv
import gzip
import math
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import envelope as ev
import sim
import units_sim as us
import validate as val

ROOT = val.ROOT_SEEDS["calibrate"]
CLASSES = ("H0c", "H0m", "H0", "H1")
N_RANDOM = 40


def theta_starts(pr):
    base = np.log(pr.r_ref)
    offs = np.array([-3.0, -1.5, 0.0, 1.5, 3.0])
    grid = np.stack(np.meshgrid(*[offs] * pr.n_cls), -1).reshape(-1, pr.n_cls)
    return [np.clip(base + o, *ev.LOG_R_BOUNDS) for o in grid]


def profile_multi(pr, T, x):
    win = pr.window(pr.edges_const(T))
    xv = np.full(win.P, float(x))
    best = -math.inf
    for th in theta_starts(pr) + [pr._th.copy()]:
        v = pr._profile(win, xv, xv, xv, False, th0=th)[0]
        best = max(best, v)
    return best


def alt_multi(pr, T, C):
    alt0 = pr.const_max(T, 0.0, C)[0]
    grid = np.linspace(0.0, C, 61)
    return max([alt0] + [profile_multi(pr, T, x) for x in grid])


def null_standard(pr, cls, T, f):
    C = pr.ceiling(cls)
    alt, x_hat, _, _ = pr.const_max(T, 0.0, C)
    if cls == "H0c" or f >= C - 1e-9:
        return pr._const_profile(T, min(f, C))[0]
    win = pr.window(pr.edges(T))
    x_c = max(f, x_hat)
    return pr.bound_sup(win, np.zeros(win.P), np.full(win.P, C), cls == "H0m", f, x_const=(x_c, pr._const_profile(T, x_c)[1])).value


def null_thorough(pr, cls, T, f, rng):
    C = pr.ceiling(cls)
    if cls == "H0c" or f >= C - 1e-9:
        return profile_multi(pr, T, min(f, C))
    original = pr._starts

    def starts(win, L, U, mono, f_, target, key, x_const):
        out = original(win, L, U, mono, f_, target, key, x_const)
        for th in theta_starts(pr):
            x = L + rng.random(win.P) * (U - L)
            if mono:
                x = np.sort(x)[::-1]
            out.append(np.r_[th, x])
        for _ in range(N_RANDOM):
            th = np.clip(np.log(pr.r_ref) + rng.normal(0, 1.5, pr.n_cls), *ev.LOG_R_BOUNDS)
            x = L + rng.random(win.P) ** rng.uniform(0.3, 3) * (U - L)
            if mono:
                x = np.sort(x)[::-1]
            out.append(np.r_[th, x])
        return out

    pr._starts = starts
    try:
        return null_standard(pr, cls, T, f)
    finally:
        pr._starts = original


def job(item):
    cell_name, rep, classes, stored = item
    cell = next(c for c in val.CELLS if c["name"] == cell_name)
    truth, design, spec = val.cell_objects(cell, 0.0)
    ss = np.random.SeedSequence(ROOT, spawn_key=(cell["id"], rep))
    s = us.simulate(truth, design, sim.child_seed(ss, 0))
    pr = ev.Problem(s.units, spec, val._age())
    T0 = truth.t0
    rows = []
    for cls in val.evaluated_classes(truth, spec):
        pr.fstar(cls, T0)
        if cls not in classes:
            continue
        f = stored[cls]["abar_rel"]
        st = pr.lr(cls, T0, f)
        C = pr.ceiling(cls)
        alt_s = pr.const_max(T0, 0.0, C)[0]
        null_s = null_standard(pr, cls, T0, f)
        rng = np.random.default_rng([cell["id"], rep, CLASSES.index(cls)])
        null_t = max(null_s, null_thorough(pr, cls, T0, f, rng))
        alt_t = max(alt_s, alt_multi(pr, T0, C))
        lr_t = max(0.0, 2 * (alt_t - null_t)) if math.isfinite(null_t) else math.inf
        rows.append(dict(
            cell=cell_name, rep=rep, cls=cls, n_flagged_stored=stored[cls]["n_flagged"], crit=stored[cls]["crit"],
            lr_stored=stored[cls]["lr"], lr_recomputed=st.value, alt_standard=alt_s, alt_thorough=alt_t,
            null_standard=null_s, null_thorough=null_t, lr_thorough=lr_t,
            covers_thorough=lr_t <= stored[cls]["crit"] + 1e-12,
        ))
    return rows


def main():
    src, dst, workers = sys.argv[1], sys.argv[2], int(sys.argv[3])
    items = {}
    for r in csv.DictReader((gzip.open if src.endswith(".gz") else open)(src, "rt")):
        if r.get("trivial") == "True" or r.get("error"):
            continue
        crit = float(r["crit_t0"])
        for cls in CLASSES:
            try:
                lr = float(r.get(f"lr_{cls}") or "nan")
            except ValueError:
                continue
            if math.isfinite(lr) and lr > crit:
                key = (r["cell"], int(r["rep"]))
                cl, st = items.setdefault(key, ([], {}))
                cl.append(cls)
                st[cls] = dict(abar_rel=float(r["abar_rel"]), lr=lr, crit=crit, n_flagged=int(float(r["n_flagged"])))
    work = [(c, rep, cl, st) for (c, rep), (cl, st) in items.items()]
    print(len(work), "replicates,", sum(len(w[2]) for w in work), "statistics", flush=True)
    out = []
    with ProcessPoolExecutor(workers) as ex:
        for rows in ex.map(job, work, chunksize=1):
            out.extend(rows)
    with open(dst, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(len(out), "rows ->", dst)


if __name__ == "__main__":
    main()
