# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Simulated sampling-unit tables for validating the F3 compatibility estimator (envelope.py).

A lineage has a true origin t0 and an encounter-intensity path a(t) (1 for t <= tau0, the established
lineage; a history class between tau0 and t0; 0 before t0). Units are drawn on the real design, then
detect with probability 1 - exp(-r_c u_k a(t_i)). The estimator sees only stage ranges, classes, clusters
and outcomes, and must find its own first appearance and reference window from them: the real selection.

Design. Units per stage are round(scale * n_docs), where n_docs is the Palynodata spore effort of
data/occurrences/effort.csv summed over palaeogeographic units (the 2006 count). A fraction `broad_frac`
of units have a range widened by up to three stages on either side. The true stage boundaries are one
draw from the timescale uncertainty, and each unit's true age is uniform within its (true-boundary)
range, which is the age model the estimator assumes: cells are correctly specified. Units are grouped
into clusters of consecutive true age, size 1 + Poisson(cluster_mean - 1), each with its own mean-one
Gamma(k, k) detection effect. Eligibility class is independent per unit.

    uv run models/f3/units_sim.py     # prints one simulated table's summary
"""

import csv
from dataclasses import dataclass
from functools import cache

import numpy as np

import envelope as ev
import sim

EFFORT_CSV = sim.ROOT / "data" / "occurrences" / "effort.csv"
HISTORIES = ("H0c", "H0m", "H0", "logistic", "H1")


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
class Truth:
    """The true history. a = 1 for t <= tau0 and a = 0 for t > t0; between them:
    H0c: f.  H0m: f, but 0 on the last `delay` Myr before t0 (a delayed step).  H0: a comb of 0 and 1
    with duty cycle f (period 0.4 Myr, so the units see Bernoulli(f)).  logistic: L(t) / L(tau0) with
    steepness g and midpoint h Myr after t0.  H1: the comb of duty f, replaced by one pulse of height
    `pulse` and duration `pulse_myr` centred between tau0 and t0."""

    history: str = "H0c"
    t0: float = 466.0
    tau0: float = 452.8
    f: float = 1.0
    delay: float = 0.0
    g: float = 0.4
    h: float = 4.0
    pulse: float = 3.0
    pulse_myr: float = 2.0
    period: float = 0.4

    def path(self, t: np.ndarray) -> np.ndarray:
        t = np.asarray(t, float)
        comb = (((t - self.tau0) % self.period) < self.f * self.period).astype(float)
        if self.history == "H0c":
            mid = np.full_like(t, self.f)
        elif self.history == "H0m":
            mid = np.where(t <= self.t0 - self.delay, self.f, 0.0)
        elif self.history == "H0":
            mid = comb
        elif self.history == "logistic":
            num = 1.0 + np.exp(-self.g * ((self.t0 - self.tau0) - self.h))
            mid = num / (1.0 + np.exp(-self.g * ((self.t0 - t) - self.h)))
        elif self.history == "H1":
            centre = (self.tau0 + self.t0) / 2
            mid = np.where(np.abs(t - centre) <= self.pulse_myr / 2, self.pulse, comb)
        else:
            raise ValueError(self.history)
        return np.where(t > self.t0, 0.0, np.where(t > self.tau0, mid, 1.0))

    def min_intensity(self, back: float = 0.0, start: float | None = None) -> float:
        """The smallest intensity on (start, t0 - back] (start defaults to tau0): the largest f_min for which
        'a >= f_min' is true there. back is the delay a history class may skip (0 for H0c)."""
        lo, hi = (self.tau0 if start is None else start), self.t0 - back
        if hi <= lo:
            return 1.0
        return float(self.path(np.linspace(lo, hi, 2001)[1:]).min())

    @property
    def members(self) -> tuple[str, ...]:
        """The history classes of the estimator that contain this truth."""
        return {
            "H0c": ("H0c", "H0m", "H0", "H1"),
            "H0m": ("H0m", "H0", "H1"),
            "H0": ("H0", "H1"),
            "logistic": ("logistic", "H0", "H1"),
            "H1": ("H1",),
        }[self.history]


@dataclass(frozen=True)
class Design:
    p: tuple[float, ...] = (0.12, 0.04)
    class_weights: tuple[float, ...] = (0.6, 0.4)
    k: float = 2.0
    scale: float = 0.05
    broad_frac: float = 0.12
    cluster_mean: float = 3.0


@dataclass(frozen=True)
class Sim:
    units: ev.Units
    t_true: np.ndarray
    r: np.ndarray  # true reference rates, one per class


def simulate(truth: Truth, design: Design, age: ev.AgeModel, seed: int | np.random.SeedSequence) -> Sim:
    rng = np.random.default_rng(seed)
    ts = age.timescale
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
    b = age.draw_boundaries(rng, 1)[0]
    t_true = b[young - 1] + rng.random(n) * (b[old] - b[young - 1])

    order = np.argsort(t_true)
    sizes = []
    while sum(sizes) < n:
        sizes.append(1 + rng.poisson(design.cluster_mean - 1))
    cluster = np.empty(n, int)
    cluster[order] = np.repeat(np.arange(len(sizes)), sizes)[:n]
    u = np.ones(len(sizes)) if np.isinf(design.k) else rng.gamma(design.k, 1.0 / design.k, len(sizes))
    cls = rng.choice(len(design.p), n, p=np.array(design.class_weights) / sum(design.class_weights))
    r = -np.log1p(-np.array(design.p))
    p_detect = -np.expm1(-r[cls] * u[cluster] * truth.path(t_true))
    d = (rng.random(n) < p_detect).astype(int)
    return Sim(ev.Units(young, old, cls, cluster, d), t_true, r)


if __name__ == "__main__":
    age = ev.AgeModel.load()
    s = simulate(Truth(), Design(), age, 1)
    names = age.timescale.names
    u = s.units
    print(f"{len(u)} units, {u.d.sum()} detections, {len(np.unique(u.cluster))} clusters")
    for stage in sorted(set(u.old), reverse=True):
        m = (u.old == stage) & (u.young == stage)
        print(f"{names[stage]:13s} units {m.sum():3d} detected {u.d[m].sum()}")
