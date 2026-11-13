"""Resource triage for a sampling frame: could it exclude a target intensity, under one declared simple design?

Scope (corrected after Codex's review, docs/audits/2026-10-31-screen-and-persistence-review.md). The design is
homogeneous and independent:
- fixed reference membership;
- one comparable class;
- independent units;
- k detections among n reference units, m older units with no detection;
- a constant older intensity f times the reference rate r.

There log L(r, f) = k log(1 - exp(-r)) - (n - k + m f) r. Evaluating the null at the reference-only maximum
r_hat = -log(1 - k/n) gives profile LR(f) <= 2 m f r_hat (`profile_lr`, `rate`). Within this design it equals the
engine's statistic for a constant history (test_screen.py checks that). Uncertainty that only removes older
exposure keeps the bound.

Outside this design the bound is not a theorem. Clustering, several sampling classes or a pooled heterogeneous
reference can move the fitted reference information either way, and Codex's counterexamples exceed the bound.
Those designs are screened with the engine itself, under their declared structure.

Each result names its frame, reading, reference conversion, design, history-class ceiling C and target f. A
class is ceiling-limited for this design when LR(C) <= CRIT. Failing to exclude the target does not make every
class ceiling-limited: H1's ceiling is 3.

Choosing frames by their screen result is an outcome-dependent selection. f3-shape.md, "Frame selection", sets
what that means for coverage. This is triage; it releases no bound.

    uv run --with numpy --with scipy models/f3/screen.py    # out/screen_borenshult.csv
"""

import csv
import math
from pathlib import Path

from scipy.optimize import brentq

CRIT = 5.991464547107979  # the declared critical value for no older detections (README: zero-count statistic)
CEILINGS = {"H0": 1.0, "H1": 3.0}  # Spec defaults: 1 for every H0 class, h1_ceiling for H1
TARGET_F = 1.0  # M2's absence premise: older intensity at the reference level
DESIGN = "homogeneous independent; one comparable class; fixed reference membership"
UNITS = Path(__file__).resolve().parents[2] / "data" / "units"
OUT = Path(__file__).resolve().parent / "out"


def _domain(k: int, n: int, m: int) -> None:
    if not (n >= 1 and 0 <= k <= n and m >= 0):
        raise ValueError(f"screen needs n >= 1 reference units, 0 <= k <= n and m >= 0; got k={k}, n={n}, m={m}")


def rate(k: int, n: int) -> float:
    """Reference rate per unit from k detections in n units (inf when every unit detects)."""
    _domain(k, n, 0)
    return math.inf if k == n else -math.log(1 - k / n)


def profile_lr(k: int, n: int, m: int, f: float) -> float:
    """Zero-count statistic for a constant path at f, with the reference rate profiled. Never above 2 m f r_hat."""
    _domain(k, n, m)
    if k == 0 or m == 0:
        return 0.0
    alt = k * math.log(k / n) + ((n - k) * math.log(1 - k / n) if k < n else 0.0)
    rest = n - k + m * f
    null = k * math.log(k / (k + rest)) + (rest * math.log(rest / (k + rest)) if rest > 0 else 0.0)
    return 2 * (alt - null)


def smallest_excludable(k: int, n: int, m: int, ceiling: float = 1.0, crit: float = CRIT) -> tuple[float, float]:
    """The smallest f in (0, ceiling] the design could exclude, with the rate known and with it profiled.
    Both are inf when even the ceiling cannot be excluded (the class is ceiling-limited)."""
    r = rate(k, n)
    known = crit / (2 * m * r) if m and 0 < r else math.inf
    known = known if known <= ceiling else math.inf
    profiled = (brentq(lambda f: profile_lr(k, n, m, f) - crit, 1e-12, ceiling)
                if profile_lr(k, n, m, ceiling) > crit else math.inf)
    return known, profiled


def older_units_needed(p: float, f: float = 1.0, crit: float = CRIT) -> float:
    """Empty, comparable older units needed to exclude f at a known per-unit reference detection probability p."""
    return crit / (2 * f * -math.log(1 - p))


def borenshult() -> list[dict]:
    depth = {f"BOR-{r['depth_m']}": float(r["depth_m"]) for r in csv.DictReader(open(UNITS / "borenshult_ages.csv"))}
    rows = [r for r in csv.DictReader(open(UNITS / "outcomes.csv")) if r["unit_id"].startswith("BOR-") and r["event_id"] == "E1"]
    base = dict(frame="Borenshult-1", design=DESIGN, target_f=TARGET_F)
    out = []
    for reading in ("main", "inclusive"):
        mine = {r["unit_id"]: r["outcome"] for r in rows if r["reading_id"] == reading}
        hits = [u for u, o in mine.items() if o == "detected"]
        if not hits:
            out.append(base | dict(reading=reading, reference_conversion="", history_class="", ceiling="", k=0, n_ref=0,
                                   m_older="", lr_known_at_ceiling="", lr_profile_at_ceiling="", f_known="", f_profile="",
                                   excludes_target="", verdict="no in-frame reference detection: the screen does not apply"))
            continue
        fa = max(hits, key=depth.get)
        ref = [u for u in mine if depth[u] <= depth[fa]]
        m = sum(depth[u] > depth[fa] and mine[u] in ("explicit_non_detection", "not_reported") for u in mine)
        k = len(hits)
        conversions = {"complete reported-category": len(ref),
                       "explicit-only (optimistic diagnostic)": k + sum(mine[u] == "explicit_non_detection" for u in ref)}
        for conversion, n in conversions.items():
            for cls, C in CEILINGS.items():
                known, profiled = smallest_excludable(k, n, m, C)
                out.append(base | dict(
                    reading=reading, reference_conversion=conversion, history_class=cls, ceiling=C, k=k, n_ref=n,
                    m_older=m, lr_known_at_ceiling=round(2 * m * C * rate(k, n), 4),
                    lr_profile_at_ceiling=round(profile_lr(k, n, m, C), 4), f_known=f"{known:.4g}", f_profile=f"{profiled:.4g}",
                    excludes_target=profiled <= TARGET_F,
                    verdict="ceiling-limited" if math.isinf(profiled)
                    else f"not ceiling-limited; constant-path threshold {profiled:.3g} (the class bound is no lower)"))
    return out


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = borenshult()
    with open(OUT / "screen_borenshult.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[-1]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)
    print("\nempty comparable older units needed (known rate, shift 0): p, f = 1, f = 0.1")
    for p in (0.05, 0.1, 0.2, 0.3, 0.5):
        print(f"{p:.2f}  {older_units_needed(p):6.1f}  {older_units_needed(p, 0.1):7.1f}")


if __name__ == "__main__":
    main()
