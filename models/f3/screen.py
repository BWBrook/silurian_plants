"""What a sampling frame could deliver for one event and reading, before any binding qualification.

With no detections among m older units, the zero-count statistic for a constant path at a fraction f of the reference
is at most 2 m f r, where r is the reference rate estimated from the frame's own reference units as if it were known.
Everything the real test adds can only lower that statistic or raise its critical value:
- profiling the reference rate (the bound holds exactly: see `profile_lr`);
- latent ages that put an older unit outside (T, first appearance];
- shared ages, clusters and overdispersion, which the calibrated shift absorbs, and the shift is not below 0.

So if 2 m r < CRIT the frame cannot exclude the reference itself (f = 1): every history class is ceiling-limited
at every candidate origin, whatever the age model. The most favourable conversion is taken on each side: every
documented non-detection is an older zero, and a reference unit counts against r only if its non-detection is
explicit. This is a design screen, not an inference; it releases no bound.

    uv run --with numpy --with scipy models/f3/screen.py    # out/screen_borenshult.csv and the requirement table
"""

import csv
import math
from pathlib import Path

from scipy.optimize import brentq

CRIT = 5.991464547107979  # the declared critical value for no older detections (README: zero-count statistic)
UNITS = Path(__file__).resolve().parents[2] / "data" / "units"
OUT = Path(__file__).resolve().parent / "out"


def profile_lr(k: int, n: int, m: int, f: float) -> float:
    """Zero-count statistic for a constant path at f: k of n reference units detect, m older units are empty, and
    the reference rate is profiled. Never above 2 m f r_hat."""
    if k == 0:
        return 0.0
    alt = k * math.log(k / n) + ((n - k) * math.log(1 - k / n) if k < n else 0.0)
    rest = n - k + m * f
    null = k * math.log(k / (k + rest)) + (rest * math.log(rest / (k + rest)) if rest > 0 else 0.0)
    return 2 * (alt - null)


def rate(k: int, n: int) -> float:
    return math.inf if k == n else -math.log(1 - k / n)


def smallest_excludable(k: int, n: int, m: int, crit: float = CRIT) -> tuple[float, float]:
    """The smallest f the frame could exclude: with the rate known, and with it profiled (inf if not even f = 1)."""
    r = rate(k, n)
    known = crit / (2 * m * r) if m and r > 0 else math.inf
    profiled = brentq(lambda f: profile_lr(k, n, m, f) - crit, 1e-9, 1.0) if profile_lr(k, n, m, 1.0) > crit else math.inf
    return known, profiled


def older_units_needed(p: float, f: float = 1.0, crit: float = CRIT) -> float:
    """Empty, comparable older units needed to exclude f at a known per-unit reference detection probability p."""
    return crit / (2 * f * -math.log(1 - p))


def borenshult() -> list[dict]:
    depth = {f"BOR-{r['depth_m']}": float(r["depth_m"]) for r in csv.DictReader(open(UNITS / "borenshult_ages.csv"))}
    rows = [r for r in csv.DictReader(open(UNITS / "outcomes.csv")) if r["unit_id"].startswith("BOR-") and r["event_id"] == "E1"]
    out = []
    for reading in ("main", "inclusive"):
        mine = {r["unit_id"]: r["outcome"] for r in rows if r["reading_id"] == reading}
        hits = [u for u, o in mine.items() if o == "detected"]
        if not hits:
            out.append(dict(reading=reading, first_appearance_m="", k=0, n_ref=0, n_ref_explicit=0,
                            m_older=sum(o in ("explicit_non_detection", "not_reported") for o in mine.values()),
                            m_unresolved=sum(o == "unresolved" for o in mine.values()),
                            r_hat=0.0, lr_max=0.0, lr_profile=0.0, f_known="inf", f_profile="inf",
                            verdict="no reference detection in the frame: uninformative without an external reference"))
            continue
        fa = max(hits, key=depth.get)
        ref = [u for u in mine if depth[u] <= depth[fa]]
        older = [u for u in mine if depth[u] > depth[fa] and mine[u] in ("explicit_non_detection", "not_reported")]
        k, n = len(hits), len(ref)
        n_explicit = k + sum(mine[u] == "explicit_non_detection" for u in ref)
        r_max = rate(k, n_explicit)
        known, profiled = smallest_excludable(k, n, len(older))
        lr_max = 2 * len(older) * r_max
        out.append(dict(reading=reading, first_appearance_m=depth[fa], k=k, n_ref=n, n_ref_explicit=n_explicit,
                        m_older=len(older), m_unresolved=sum(mine[u] == "unresolved" for u in mine if depth[u] > depth[fa]),
                        r_hat=round(r_max, 4), lr_max=round(lr_max, 3),
                        lr_profile=round(profile_lr(k, n, len(older), 1.0), 3), f_known=f"{CRIT / lr_max:.3g}",
                        f_profile="inf" if math.isinf(profiled) else f"{profiled:.3g}",
                        verdict="ceiling-limited at every origin" if lr_max < CRIT else "could exclude the reference"))
    return out


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = borenshult()
    with open(OUT / "screen_borenshult.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)
    print("\nempty comparable older units needed (known rate, shift 0): p, f = 1, f = 0.1")
    for p in (0.05, 0.1, 0.2, 0.3, 0.5):
        print(f"{p:.2f}  {older_units_needed(p):6.1f}  {older_units_needed(p, 0.1):7.1f}")


if __name__ == "__main__":
    main()
