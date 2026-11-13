# /// script
# requires-python = ">=3.12"
# ///

"""Paired comparison of two validation runs on the same seeds: the data must agree replicate by replicate,
so differences in f* and coverage are the code's.

    uv run studies/f3/models/check_paired.py studies/f3/models/out/validation_dev_reps.csv.gz studies/f3/models/out/validation_dev2_reps.csv.gz
"""

import csv, gzip, math, statistics as st, sys, collections

old_path, new_path = sys.argv[1], sys.argv[2]
op = gzip.open if old_path.endswith(".gz") else open
old = {(r["cell"], r["rep"]): r for r in csv.DictReader(op(old_path, "rt"))}
np_ = gzip.open if new_path.endswith(".gz") else open
new = {(r["cell"], r["rep"]): r for r in csv.DictReader(np_(new_path, "rt"))}
assert old.keys() == new.keys(), "replicate sets differ"

same = collections.Counter()
for k in old:
    for col in ("tau", "n_ref", "n_old", "n_old_detected", "trivial"):
        if col in old[k] and old[k][col] != new[k][col]:
            same[col] += 1
print("replicates whose data differ, by column:", dict(same) or "none")

def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return math.nan

cells = sorted({k[0] for k in old}, key=lambda c: (c[0], int(c[1:])))
print("cell cls | n_both | median d f* | p05 p95 | share |d|>0.01 | old>new new>old | cover old new (all reps, delta 0)")
for c in cells:
    for cls in ("H0c", "H0m", "H0", "H1"):
        col = f"fstar_{cls}"
        ks = [k for k in old if k[0] == c]
        if col not in old[ks[0]] or all(old[k][col] == "" for k in ks):
            continue
        d = []
        for k in ks:
            a, b = fl(old[k][col]), fl(new[k][col])
            if math.isfinite(a) and math.isfinite(b):
                d.append(b - a)
        if not d:
            continue
        d.sort()
        n = len(d)
        def cov(rows):
            ok = 0
            for r in rows:
                lr, cr = fl(r.get(f"lr_{cls}")), fl(r.get("crit_t0"))
                if r.get("trivial") == "True" or not math.isfinite(lr):
                    ok += 1
                elif lr <= cr:
                    ok += 1
            return ok / len(rows)
        print(c, cls, "|", n, "| %.4f" % st.median(d), "| %.3f %.3f" % (d[int(.05 * n)], d[min(n - 1, int(.95 * n))]),
              "| %.3f" % (sum(abs(x) > 0.01 for x in d) / n), "|", sum(x < -0.01 for x in d), sum(x > 0.01 for x in d),
              "| %.3f %.3f" % (cov([old[k] for k in ks]), cov([new[k] for k in ks])))
