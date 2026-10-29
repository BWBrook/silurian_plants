# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Simulated sampling-unit tables for validating the F3 compatibility estimator (envelope.py).

A lineage has a true origin t0 and an encounter-intensity path a(t): 1 for t <= tau0 (the established
lineage), a history between tau0 and t0, and 0 beyond t0. Units are drawn on the real design, then detect
with probability 1 - exp(-r_c u_k a(t_i)). The estimator sees only stage ranges, recorded classes, clusters
and outcomes, and must find its own first appearance and reference window from them: the real selection.

Design. Units per stage are round(scale * n_docs), where n_docs is the Palynodata spore effort of
data/occurrences/effort.csv summed over palaeogeographic units (the 2006 count). A fraction `broad_frac` of
units have a range widened by up to three stages on either side. The true stage bases are those of
`truth_scenario` (an AgeModel) and each unit's true age is uniform within its range under them. Units are
grouped into clusters of consecutive true age, size 1 + Poisson(cluster_mean - 1), each with its own
mean-one Gamma(k, k) detection effect. Eligibility class is drawn independently per unit unless
`class_trend` confounds it with age. Cells are correctly specified unless a misspecification option is on:
  class_trend  P(class 0 | age) = clip(w0 + class_trend (z - 1/2), 0.05, 0.95), z the position of the unit's
               true age in the design span (0 youngest, 1 oldest); the other classes share the rest;
  misassign    the fraction of units whose recorded class is replaced by another class (the truth keeps the
               real class);
  older_report the rate multiplier for units older than tau0 (a reporting difference);
  confine      each cluster is in region B with this probability, where a = 0 for t > tau0.

Truth histories between tau0 and t0, each times f, the nominal level:
  H0c       a = f.
  step      a = 0 for the `delay` Myr after t0, then f.
  ramp      linear from 0 at t0 to f at tau0.
  logistic  L(t) / L(tau0), L(t) = 1 / (1 + exp(-g ((t0 - t) - h))): g per Myr, h Myr after t0.
  hide      a 0/1 path at height 1 on the stages between tau0 and t0 with the fewest expected units per Myr,
            filled in that order (the last stage at its older end) until the time-average over (tau0, t0]
            is f: the least favourable member of H0.
  hide_h1   the same at height `pulse`: the least favourable member of H1.

    uv run models/f3/units_sim.py     # prints one simulated table's summary
"""

import csv
from dataclasses import dataclass
from functools import cache

import numpy as np

import envelope as ev
import sim

EFFORT_CSV = sim.ROOT / "data" / "occurrences" / "effort.csv"
HISTORIES = ("H0c", "step", "ramp", "logistic", "hide", "hide_h1")


@cache
def spore_effort() -> dict[str, float]:
    """n_docs summed over palaeogeographic units, by stage (all stages of the spore channel)."""
    out: dict[str, float] = {}
    with open(EFFORT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if row["channel"] == "spore":
                out[row["stage"]] = out.get(row["stage"], 0.0) + float(row["n_docs"] or 0.0)
    return out


@dataclass(frozen=True)
class Design:
    p: tuple[float, ...] = (0.12, 0.04)
    class_weights: tuple[float, ...] = (0.6, 0.4)
    k: float = 2.0
    scale: float = 0.05
    broad_frac: float = 0.12
    cluster_mean: float = 3.0
    class_trend: float = 0.0
    misassign: float = 0.0
    older_report: float = 1.0
    confine: float = 0.0
    truth_scenario: str = "chart"


@dataclass(frozen=True)
class Truth:
    """The true history (module docstring); a = 1 for t <= tau0 and a = 0 for t > t0."""

    history: str = "H0c"
    t0: float = 476.0
    tau0: float = 452.8
    f: float = 1.0
    delay: float = 0.0
    g: float = 0.4
    h: float = 4.0
    pulse: float = 3.0

    @property
    def members(self) -> tuple[str, ...]:
        """The history classes of the estimator that contain this truth."""
        return {
            "H0c": ("H0c", "H0m", "H0", "H1"),
            "step": ("H0m", "H0", "H1"),
            "ramp": ("H0m", "H0", "H1"),
            "logistic": ("H0m", "H0", "H1"),
            "hide": ("H0", "H1"),
            "hide_h1": ("H1",),
        }[self.history]

    def lit(self, design: Design, age: ev.AgeModel) -> list[tuple[float, float]]:
        """The intervals of (tau0, t0] where the hide histories are on: stages in order of increasing
        expected units per Myr, the last one filled from its older end."""
        base = age.base
        effort = spore_effort()
        height = self.pulse if self.history == "hide_h1" else 1.0
        need = self.f * (self.t0 - self.tau0) / height
        cells = []
        for s in range(1, len(base)):
            lo, hi = max(base[s - 1], self.tau0), min(base[s], self.t0)
            if hi > lo:
                n = round(effort.get(age.timescale.names[s], 0.0) * design.scale)
                cells.append((n / (base[s] - base[s - 1]), lo, hi))
        out = []
        for _, lo, hi in sorted(cells):
            if need <= 1e-12:
                break
            take = min(need, hi - lo)
            out.append((hi - take, hi))
            need -= take
        return out

    def path(self, design: Design = Design(), age: ev.AgeModel | None = None):
        """The true path as a function of age (vectorised)."""
        lit = self.lit(design, age or ev.AgeModel.load(scenario=design.truth_scenario)) if self.history in ("hide", "hide_h1") else None
        height = self.pulse if self.history == "hide_h1" else 1.0

        def a(t):
            t = np.asarray(t, float)
            if self.history == "H0c":
                mid = np.full_like(t, self.f)
            elif self.history == "step":
                mid = np.where(t <= self.t0 - self.delay, self.f, 0.0)
            elif self.history == "ramp":
                mid = self.f * (self.t0 - t) / (self.t0 - self.tau0)
            elif self.history == "logistic":
                num = 1.0 + np.exp(-self.g * ((self.t0 - self.tau0) - self.h))
                mid = self.f * num / (1.0 + np.exp(-self.g * ((self.t0 - t) - self.h)))
            else:
                mid = np.zeros_like(t)
                for lo, hi in lit:
                    mid = np.where((t > lo) & (t <= hi), height, mid)
            return np.where(t > self.t0, 0.0, np.where(t > self.tau0, mid, 1.0))

        return a


def effective_path(path, truth: Truth, design: Design):
    """The expected encounter intensity of a unit at age t once reporting and region are in: the path times
    older_report and (1 - confine) beyond tau0."""

    def a(t):
        t = np.asarray(t, float)
        return np.where(t > truth.tau0, path(t) * design.older_report * (1.0 - design.confine), path(t))

    return a


def min_intensity(path, lo: float, hi: float) -> float:
    """The smallest value of the path on (lo, hi]: the largest f_min for which 'a >= f_min' holds there."""
    if hi <= lo:
        return 1.0
    return float(path(np.linspace(lo, hi, 2001)[1:]).min())


@dataclass(frozen=True)
class Sim:
    units: ev.Units
    t_true: np.ndarray
    r: np.ndarray  # true reference rates, one per class
    a_unit: np.ndarray  # each unit's realised intensity (path, reporting and region)
    cls_true: np.ndarray


def simulate(truth: Truth, design: Design, seed: int | np.random.SeedSequence) -> Sim:
    rng = np.random.default_rng(seed)
    age = ev.AgeModel.load(scenario=design.truth_scenario)
    ts = age.timescale
    base = age.base
    effort = spore_effort()
    stages = [(ts.index(s), n) for s, n in effort.items() if s in ts.names and round(n * design.scale) > 0]
    lo_idx, hi_idx = min(i for i, _ in stages), max(i for i, _ in stages)
    nominal = np.repeat([i for i, _ in stages], [round(n * design.scale) for _, n in stages])
    n = len(nominal)
    broad = rng.random(n) < design.broad_frac
    ext = rng.integers(0, 4, (2, n)) * broad
    ext[1] = np.where(broad & (ext.sum(axis=0) == 0), 1, ext[1])
    young = np.clip(nominal - ext[0], max(lo_idx, 1), None)
    old = np.clip(nominal + ext[1], None, hi_idx)
    t_true = base[young - 1] + rng.random(n) * (base[old] - base[young - 1])

    order = np.argsort(t_true)
    sizes = []
    while sum(sizes) < n:
        sizes.append(1 + rng.poisson(design.cluster_mean - 1))
    cluster = np.empty(n, int)
    cluster[order] = np.repeat(np.arange(len(sizes)), sizes)[:n]
    u = np.ones(len(sizes)) if np.isinf(design.k) else rng.gamma(design.k, 1.0 / design.k, len(sizes))

    w = np.array(design.class_weights, float) / sum(design.class_weights)
    z = (t_true - base[lo_idx - 1]) / (base[hi_idx] - base[lo_idx - 1])
    p0 = np.clip(w[0] + design.class_trend * (z - 0.5), 0.05, 0.95)
    probs = np.concatenate([p0[:, None], (1 - p0)[:, None] * (w[1:] / w[1:].sum())[None]], axis=1)
    cls_true = np.minimum((rng.random(n)[:, None] > np.cumsum(probs, axis=1)).sum(axis=1), len(w) - 1)
    flip = rng.random(n) < design.misassign
    cls_rec = np.where(flip, (cls_true + rng.integers(1, len(w), n)) % len(w), cls_true)
    region_b = rng.random(len(sizes)) < design.confine

    r = -np.log1p(-np.array(design.p))
    a_unit = truth.path(design, age)(t_true)
    older = t_true > truth.tau0
    a_unit = np.where(older, a_unit * design.older_report * (1.0 - region_b[cluster]), a_unit)
    p_detect = -np.expm1(-r[cls_true] * u[cluster] * a_unit)
    d = (rng.random(n) < p_detect).astype(int)
    return Sim(ev.Units(young, old, cls_rec, cluster, d), t_true, r, a_unit, cls_true)


if __name__ == "__main__":
    s = simulate(Truth(), Design(), 1)
    names = ev.AgeModel.load().timescale.names
    u = s.units
    print(f"{len(u)} units, {u.d.sum()} detections, {len(np.unique(u.cluster))} clusters")
    for stage in sorted(set(u.old), reverse=True):
        m = (u.old == stage) & (u.young == stage)
        print(f"{names[stage]:13s} units {m.sum():3d} detected {u.d[m].sum()}")
