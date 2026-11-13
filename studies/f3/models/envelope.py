# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""F3 reshape v3 (studies/f3/docs/f3-shape.md): the compatibility estimator for fossil absences.

Given eligible, binary sampling units it answers, under a named history class K: how intense could the
lineage's encounter intensity have been between the first appearance and a candidate origin T, and
which origins T are excluded by the empty older units?

Ages are Ma, decreasing towards the present, so older means larger. Stage s spans (base[s-1], base[s]].
Units, stage ranges and the first appearance follow the analysis specification (studies/f3/models/specs/README.md).

Model. Unit i has a latent age t_i, uniform within its stage range, an eligibility class c(i), a cluster
k(i) and a binary outcome d_i. It detects with probability 1 - exp(-r_c u_k a(t_i)), r_c = -log(1 - p_c),
a(t) the relative encounter intensity (1 in the reference window) and u_k ~ Gamma(shape k, rate k) a
mean-one cluster effect (k = inf: none). Stage boundaries are fixed (AgeModel: the chart, or the older and
younger scenarios), so a unit's range is known and its latent age is integrated exactly.

First appearance. tau is the base of the oldest stage that contains a certain detection (a detected unit
whose whole range lies in that stage); that stage and the next reference_stages - 1 younger stages form
the reference window, and units whose whole range lies in it are the reference units. Units with any part
of their range older than tau are the older units. A class with fewer than min_units_per_class reference
units is uncalibrated and its units are dropped. The reference rates r_ref are fitted to the reference
units alone; they start the fits and test for exposure, but the target is weighted by the rates being fitted.

Pieces. For an origin T > tau and an optional lag D, (tau, T] is cut at the stage bases strictly between
tau and T and at T - D. Stage ranges align with the bases, so an older unit overlaps each piece p in a
fraction w_ip of its range (0 or the piece's share) and has Qref_i of its range at or younger than tau
(a = 1) and the rest older than T (a = 0). A path enters the likelihood through its piece means x_p.

Likelihood. Units are independent given the cluster effect u, and a cluster's likelihood is the integral of
Gamma(k, k)(u) times the product of its units' outcome probabilities (a trapezoid sum in log u, spectrally
accurate here; tests check it against the closed form and against enumeration). Reference and older units
share the integral, so a cluster spanning the first appearance is treated jointly. Per unit, with rate r:
  exact (piecewise-constant path x):  D_i(u) = Qref (1 - e^-ru) + sum_p w_ip (1 - e^(-r u x_p)), P0 = 1 - D.
  bound (paths with pointwise values in [L_p, U_p] and piece means x_p), used by H0m, H0 and H1:
    non-detected unit: P0_i(u) = Qref e^-ru + sum_p w_ip chi_p(u) + (1 - Qref - sum_p w_ip), with the chord
      chi_p(u) = [(U_p - x_p) e^(-ru L_p) + (x_p - L_p) e^(-ru U_p)] / (U_p - L_p), which by convexity of
      e^(-ru a) bounds E e^(-ru a) over every a in [L_p, U_p] with mean x_p;
    detected unit: D_i(u) = the exact formula at x (Jensen: it bounds the detection probability).
  The product over units of these bounds is an upper bound on the likelihood of every path in the class
  with those piece means. With no detected older unit it is attained, by a path that sits at L_p or U_p
  within each piece. Gradients with respect to x and log r are analytic.

History classes for the period older than tau (origin T > tau; a(t) = 0 for t > T), each summarised by
the target abar = sum_p c_p(r) x_p, c_p(r) = sum_i r_c(i) w_ip / sum_i r_c(i) Qmid_i over the older units,
Qmid_i = sum_p w_ip: the mean intensity over (tau, T] weighted by the true reference rates and integrated over
the latent ages (sum c_p = 1). The rates are those of the fit, so a supremum under abar >= f constrains the
true-rate target, not a plug-in; c depends on r only through the class mix of the exposure:
  H0c  a = x constant on [0, 1]; exact likelihood.
  H0   any path 0 <= a <= 1: x in [0, 1]^P, bound.
  H0m  as H0 with x non-decreasing towards tau (a younger piece at least every older piece). The bound is
       conservative for the monotone class: it bounds the likelihood of every monotone path with those
       piece means, but monotone paths inside a piece are not excluded from the chord, so it can be
       attained only by non-monotone ones.
  H1   sensitivity: x in [0, C]^P, C = h1_ceiling, bound; H1-no-ceiling has no finite bound.
f*_K(T) is the largest f in [0, C_K] with LR_K(f) <= crit, where LR_K(f) = max(0, 2 (alt - sup{l_K(r, x) :
abar(x) >= f})), the supremum taken jointly over the reference rates and x. alt is the best constant
history (exact likelihood) on [0, C_K], with C_K the class ceiling (1 for H0c, H0m and H0; C for H1), so
H0c, H0m and H0 share one alternative and f*(H0c) <= f*(H0m) <= f*(H0). LR_K is non-decreasing in f.
States: finite, ceiling-limited (LR_K(C_K) <= crit), unbounded (H1-no-ceiling), zero-exposure.

Optimisation. SLSQP over (log r, x) with the analytic jacobian, the target as a bilinear constraint (linear
when one class carries the exposure or there is one piece) and monotone constraints for H0m; multi-start
from (a) the constant history at max(f, best constant), (b) a hiding allocation that fills the target on
the pieces with least exposure per Myr (from the youngest piece for H0m), (c) the previous solution on the
same window, and the best single-piece vertex (a step from the youngest piece for H0m) by likelihood, since
with finite k the supremum has local optima at vertices. The result is the highest feasible candidate over
all starts; candidates within TIE in log-likelihood are equal, and a converged one is preferred among them.
When the selected run did not converge it is restarted once from where it stopped (REPAIR_ITER iterations)
and keeps the repaired value when that is no lower; a result that still has not converged is failed. spread is the gap between the highest and lowest feasible candidates, a diagnostic of multiple
optima; a fit is flagged when it failed or spread exceeds SPREAD_FLAG. A statistic carries the status of
both of its fits: it failed when its alternative or its null failed. With no detected older unit and no
active target every non-detection bound falls in each x_p, so the supremum is at x = L and only log r is
profiled.

Critical value. count_crit(n) is a declared rule matched to the one-sided Poisson (Garwood) limit for n
older detections: 5.99 at n = 0 falling towards 2.71. It is exact only for fixed rates and independent
Poisson counts; the procedure's coverage is established by simulation (validate.py), and crit_shift moves
the rule by the amount the simulation asks for.

Origins. T is excluded at level alpha when the hypothesis "a >= f_min on (tau, T]" is rejected against the
best constant history on [0, 1] at T. H0c: constant in [f_min, 1], exact. H0: pieces with L = f_min,
U = 1, bound (equal to H0c when no older unit detects). H0m: pieces in (tau, T - D] have L = f_min, pieces
in (T - D, T] have L = 0, monotone, D = h0m_lag_ma (the delayed step when no older unit detects). Each f_min
read-out is a marginal statement. Every origin from base[s*-1], the top of the first-appearance stage,
to tau is in the set by construction.
"""

import csv
import math
import tomllib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import optimize, stats

import sim

LOG_R_BOUNDS = (math.log(1e-5), math.log(8.0))
TINY = 1e-300
STATES = ("finite", "ceiling-limited", "unbounded", "zero-exposure")
SCENARIOS = ("chart", "older", "younger")
FA_RULES = {"base-of-oldest-certain-detection-stage": "certain", "base-of-oldest-possible-detection-stage": "oldest-possible"}
SPREAD_FLAG = 0.05
REPAIR_ITER = 1000
TIE = 1e-6
FLOOR = 0.02
VIOLATION = 1e-6


class NoFirstAppearance(ValueError):
    """No certain detection, so the first appearance and the reference boundary are undefined."""


@dataclass(frozen=True)
class AgeModel:
    """Stage bases: the chart (data/timescale.csv), or shifted by the printed uncertainty (older: base +
    unc, younger: base - unc; a blank uncertainty is 0). No uncertainty is propagated: each scenario is
    one fixed set of bases."""

    timescale: sim.Timescale
    unc: np.ndarray
    scenario: str = "chart"

    def __post_init__(self):
        if self.scenario not in SCENARIOS:
            raise ValueError(f"scenario must be one of {SCENARIOS}")
        if np.any(np.diff(self.base) <= 0):
            raise ValueError("stage bases must stay strictly increasing")

    @classmethod
    def load(cls, path: Path = sim.TIMESCALE_CSV, scenario: str = "chart") -> "AgeModel":
        with open(path, newline="") as f:
            unc = np.array([float(r["base_unc_ma"] or 0.0) for r in csv.DictReader(f)])
        return cls(sim.Timescale.load(path), unc, scenario)

    @property
    def base(self) -> np.ndarray:
        shift = {"chart": 0.0, "older": 1.0, "younger": -1.0}[self.scenario]
        return self.timescale.base + shift * self.unc

    @property
    def top(self) -> np.ndarray:
        return np.concatenate([[np.nan], self.base[:-1]])


@dataclass(frozen=True)
class Units:
    """Eligible binary sampling units. young and old index the youngest and oldest stage of the range.
    mult is a declared, fixed multiplier of the class rate (a transport scenario between material types,
    facies or regions; 1 by default). lo_ma and hi_ma optionally narrow an older unit's age range to a
    numerical interval inside its stage range (NaN: the whole stage range)."""

    young: np.ndarray
    old: np.ndarray
    cls: np.ndarray
    cluster: np.ndarray
    d: np.ndarray
    mult: np.ndarray | None = None
    lo_ma: np.ndarray | None = None
    hi_ma: np.ndarray | None = None

    def __post_init__(self):
        n = len(self.d)
        for name, fill in (("mult", 1.0), ("lo_ma", math.nan), ("hi_ma", math.nan)):
            if getattr(self, name) is None:
                object.__setattr__(self, name, np.full(n, fill))
        if not all(len(a) == n for a in (self.young, self.old, self.cls, self.cluster, self.mult, self.lo_ma, self.hi_ma)):
            raise ValueError("unit arrays differ in length")
        if np.any(~(self.mult > 0)):
            raise ValueError("rate multipliers must be positive")
        if np.any(np.isnan(self.lo_ma) != np.isnan(self.hi_ma)) or np.any(self.lo_ma >= self.hi_ma):
            raise ValueError("a numerical age range needs both ends, younger first")
        if np.any(self.young > self.old) or np.any(self.young < 1):
            raise ValueError("a unit's range must run from a stage younger than or equal to its oldest, and not the first stage")
        if not np.all((self.d == 0) | (self.d == 1)):
            raise ValueError("outcomes must be 0 or 1")

    def __len__(self) -> int:
        return len(self.d)

    def take(self, mask: np.ndarray) -> "Units":
        return Units(*(a[mask] for a in (self.young, self.old, self.cls, self.cluster, self.d, self.mult, self.lo_ma, self.hi_ma)))


@dataclass(frozen=True)
class Spec:
    """The inference-side fields of an analysis specification (studies/f3/models/specs/)."""

    reference_stages: int = 5
    min_units_per_class: int = 10
    domain_ma: tuple[float, float] = (0.0, 560.0)
    classes: tuple[str, ...] = ("H0c", "H0m", "H0", "H1")
    h1_ceiling: float = 3.0
    h0m_lag_ma: float = 10.0
    alpha: float = 0.05
    readouts: tuple[float, ...] = (1.0, 0.1, 0.01)
    cluster_shape_k: float = 2.0
    crit_shift: float = 0.0
    age_scenario: str = "chart"
    nodes: int = 48
    fa_rule: str = "certain"

    @classmethod
    def from_toml(cls, path: Path) -> "Spec":
        with open(path, "rb") as f:
            t = tomllib.load(f)
        h, inf = t["history"], t["inference"]
        return cls(
            reference_stages=t["first_appearance"]["reference_stages"],
            min_units_per_class=t["reference"]["min_units_per_class"],
            domain_ma=tuple(t["older"]["domain_ma"]),
            classes=tuple(h["classes"]),
            h1_ceiling=h["h1_ceiling"],
            h0m_lag_ma=h["h0m_lag_ma"],
            alpha=inf["alpha"],
            readouts=tuple(inf["readouts"]),
            cluster_shape_k=inf["cluster_shape_k"],
            crit_shift=inf["crit_shift"],
            age_scenario=inf["age_scenario"],
            nodes=inf["nodes"],
            fa_rule=FA_RULES[t["first_appearance"]["rule"]],
        )


def gamma_nodes(k: float, n: int = 48, eps: float = 1e-9) -> tuple[np.ndarray, np.ndarray]:
    """Nodes u and log weights of a trapezoid rule in log u for the Gamma(k, k) density (mean 1).

    The weights sum to 1 - O(eps); k = inf is the single node u = 1."""
    if math.isinf(k):
        return np.array([1.0]), np.array([0.0])
    lo, hi = stats.gamma.ppf(eps, k, scale=1 / k), stats.gamma.isf(eps, k, scale=1 / k)
    v = np.linspace(math.log(lo), math.log(hi), n)
    u = np.exp(v)
    return u, stats.gamma.logpdf(u, k, scale=1 / k) + v + math.log(v[1] - v[0])


def _lse(a: np.ndarray, axis: int = -1) -> np.ndarray:
    m = a.max(axis=axis, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)
    return (np.log(np.exp(a - m).sum(axis=axis, keepdims=True)) + m).squeeze(axis)


def no_detection_probability(r: np.ndarray, vals: np.ndarray, probs: np.ndarray, k: float, nodes: int = 48) -> float:
    """P(no detection) of one cluster: units i with rate r[i] and intensity a_i taking vals[i, j] with
    probability probs[i, j], independent across units, sharing a Gamma(k, k) cluster effect."""
    u, logw = gamma_nodes(k, nodes)
    psi = (probs[:, :, None] * np.exp(-r[:, None, None] * vals[:, :, None] * u)).sum(axis=1)
    return float(np.exp(_lse(np.log(psi).sum(axis=0) + logw)))


def count_crit(n: int, alpha: float = 0.05) -> float:
    """A declared critical value matched to the one-sided Poisson (Garwood) limit for n older detections:
    the LR value at which the Poisson upper limit for the older exposure equals the exact one-sided limit,
    2 (mu - n + n log(n / mu)) with mu = chi2_{2(n+1)}(1 - alpha) / 2. For n = 0 it is -2 log(alpha) = 5.99
    (the rule of three); it falls towards 2.71 as n grows. It is exact only for fixed rates and independent
    Poisson counts; the coverage of the whole procedure is established by simulation."""
    mu = stats.chi2.ppf(1 - alpha, 2 * (n + 1)) / 2
    return float(2 * (mu - n + (n * math.log(n / mu) if n else 0.0)))


@dataclass(frozen=True)
class Fit:
    """A supremum over the reference rates and the history: value, argmax, whether the run that produced it
    converged (after the repair restart), and spread, the gap between the highest and lowest feasible
    candidates over the starts."""

    value: float
    theta: np.ndarray | None
    x: np.ndarray | None
    converged: bool
    spread: float

    @property
    def flagged(self) -> bool:
        return (not self.converged) or self.spread > SPREAD_FLAG


def select(candidates: list[tuple[float, np.ndarray, bool]]) -> tuple[tuple[float, np.ndarray, bool], float]:
    """The highest candidate (value, argmax, converged) with its own convergence status, and the spread of
    the values over all candidates. A non-converged run that reached a higher feasible value is kept: it is
    the better estimate of the supremum, and its status marks the result for repair. Candidates within TIE
    of the highest are equal (a run inside the constraint tolerance can gain 1e-8), and a converged one is
    preferred among them."""
    top = max(c[0] for c in candidates)
    best = max((c for c in candidates if c[0] >= top - TIE), key=lambda c: (c[2], c[0]))
    values = [c[0] for c in candidates]
    return best, max(values) - min(values)


@dataclass(frozen=True)
class Bound:
    """One (history class, T) result: the state and f*, the largest unrejected target."""

    cls: str
    T: float
    state: str
    value: float
    ceiling: float
    converged: bool = True
    spread: float = 0.0


@dataclass(frozen=True)
class Statistic:
    """LR_K(f) at one target f, with the fit's convergence record."""

    value: float
    converged: bool
    spread: float


@dataclass(frozen=True)
class OriginSet:
    """The origins not rejected on the grid T (ascending, first point = tau). lr is the statistic and ok
    whether each grid point's statistic converged. young_edge is base[s*-1], the top of the first-appearance
    stage: every origin from there to tau is in the set by construction."""

    cls: str
    f_min: float
    crit: np.ndarray
    T: np.ndarray
    lr: np.ndarray
    domain_hi: float
    young_edge: float
    ok: np.ndarray

    @property
    def keep(self) -> np.ndarray:
        return self.lr <= self.crit

    @property
    def runs(self) -> list[tuple[float, float]]:
        """Maximal runs of unrejected grid points from tau up, each widened to the next grid point (the
        bracket in which the boundary lies); the last run reaches the domain edge when it is unbounded."""
        out, i, keep = [], 0, self.keep
        while i < len(keep):
            if keep[i]:
                j = i
                while j + 1 < len(keep) and keep[j + 1]:
                    j += 1
                hi = self.T[j + 1] if j + 1 < len(keep) else self.domain_hi
                out.append((float(self.T[i]), float(hi)))
                i = j + 1
            else:
                i += 1
        return out

    @property
    def complete_runs(self) -> list[tuple[float, float]]:
        """The runs with the younger part included: the first starts at base[s*-1], not at tau."""
        runs = self.runs
        return [(float(self.young_edge), runs[0][1])] + runs[1:] if runs else []

    @property
    def unbounded(self) -> bool:
        return bool(self.keep[-1])

    @property
    def connected(self) -> bool:
        return len(self.runs) <= 1

    @property
    def older_endpoint(self) -> float:
        """The older end of the set (its last run); the domain edge when unbounded."""
        return self.runs[-1][1] if self.runs else float(self.T[0])

    def contains(self, T0: float) -> bool:
        if T0 <= self.T[0]:
            return True
        return any(lo <= T0 <= hi for lo, hi in self.runs)


@dataclass
class Block:
    """Units of one kind in a window, sorted by cluster. cpos: each unit's cluster position; seg_*: the
    segments of equal cluster (reduceat starts and cluster positions). Entries (m_*) are the nonzero
    (unit, piece) weights, sorted by unit; m_starts and m_units index the units that have any."""

    n: int
    cls: np.ndarray
    cpos: np.ndarray
    seg_starts: np.ndarray
    seg_pos: np.ndarray
    d: np.ndarray | None = None
    mult: np.ndarray | None = None
    qref: np.ndarray | None = None
    rest: np.ndarray | None = None
    m_unit: np.ndarray | None = None
    m_piece: np.ndarray | None = None
    m_w: np.ndarray | None = None
    m_starts: np.ndarray | None = None
    m_units: np.ndarray | None = None

    @property
    def m(self) -> int:
        return 0 if self.m_w is None else len(self.m_w)


@dataclass
class Window:
    """Everything the likelihood needs about one partition of (tau, T] into pieces. piece_lo and piece_hi
    are the kept pieces (those some older unit overlaps); W (older units x kept pieces) holds the overlap
    fractions; E (classes x kept pieces) sums them by class, the exposure from which the target
    coefficients follow (None without exposure)."""

    edges: np.ndarray
    T: float
    piece_lo: np.ndarray
    piece_hi: np.ndarray
    W: np.ndarray
    qmid: np.ndarray
    impossible: bool
    has_det: bool
    K: int
    ref: Block
    old0: Block
    old1: Block
    E: np.ndarray | None

    @property
    def P(self) -> int:
        return len(self.piece_lo)

    @property
    def rate_free(self) -> bool:
        """The target coefficients do not depend on the rates: one piece, or one class carries the exposure."""
        return self.P == 1 or int((self.E.sum(axis=1) > 0).sum()) <= 1

    def coef(self, theta: np.ndarray) -> np.ndarray:
        """c(r) at r = exp(theta): each piece's share of the older units' rate-weighted exposure."""
        rE = np.exp(theta) @ self.E
        return rE / rE.sum()

    def target(self, theta: np.ndarray, x: np.ndarray) -> tuple[float, np.ndarray]:
        """abar = c(r) . x and its gradient with respect to (log r, x)."""
        r, e = np.exp(theta), self.E.sum(axis=1)
        Ex, S = self.E @ x, float(r @ e)
        abar = float(r @ Ex) / S
        return abar, np.r_[r * (Ex - abar * e) / S, (r @ self.E) / S]

    def target_floor(self, L: np.ndarray) -> float:
        """The smallest abar at x = L over all rates: c(r) . L is a mix of the exposed classes' values."""
        e = self.E.sum(axis=1)
        return float(((self.E @ L)[e > 0] / e[e > 0]).min())


def _segsum(b: Block, a: np.ndarray) -> np.ndarray:
    out = np.zeros((b.n, a.shape[1]))
    out[b.m_units] = np.add.reduceat(a, b.m_starts, axis=0)
    return out


class Problem:
    """One data set analysed under one specification: first appearance, reference window, reference
    rates, and the likelihood and optimisation machinery."""

    def __init__(self, units: Units, spec: Spec, age: AgeModel):
        if age.scenario != spec.age_scenario:
            raise ValueError(f"age model scenario {age.scenario!r} differs from the specification's {spec.age_scenario!r}")
        self.spec, self.age = spec, age
        if spec.fa_rule not in FA_RULES.values():
            raise ValueError(f"fa_rule must be one of {tuple(FA_RULES.values())}")
        certain = (units.d == 1) & ((units.young == units.old) | (spec.fa_rule == "oldest-possible"))
        if not certain.any():
            raise NoFirstAppearance("no certain detection" if spec.fa_rule == "certain" else "no detection")
        base = age.base
        self.s_star = int(units.old[certain].max())
        self.tau = float(base[self.s_star])
        first = self.s_star - spec.reference_stages + 1
        is_ref = (units.old <= self.s_star) & (units.young >= first)
        is_old = units.old > self.s_star
        counts = np.bincount(units.cls[is_ref], minlength=int(units.cls.max()) + 1)
        calibrated = counts >= spec.min_units_per_class
        self.class_counts = counts
        self.calibrated = np.flatnonzero(calibrated)
        if len(self.calibrated) == 0:
            raise NoFirstAppearance("no class has min_units_per_class reference units")
        keep_cls = calibrated[units.cls]
        self.n_dropped_uncalibrated = int(((is_ref | is_old) & ~keep_cls).sum())
        self.n_dropped_outside = int((~(is_ref | is_old)).sum())
        ref, old = units.take(is_ref & keep_cls), units.take(is_old & keep_cls)
        ref = ref.take(np.argsort(ref.cluster, kind="stable"))
        old = old.take(np.argsort(old.cluster, kind="stable"))
        remap = np.full(len(counts), -1)
        remap[self.calibrated] = np.arange(len(self.calibrated))
        self.n_cls = len(self.calibrated)
        self.cluster_ids = np.unique(np.concatenate([ref.cluster, old.cluster]))
        self.rc, self.rd, self.rcl = remap[ref.cls], ref.d, np.searchsorted(self.cluster_ids, ref.cluster)
        self.oc, self.od, self.ocl = remap[old.cls], old.d, np.searchsorted(self.cluster_ids, old.cluster)
        self.n_ref, self.n_old = len(ref), len(old)
        lo, hi = base[old.young - 1], base[old.old]
        self.lo, self.hi = np.where(np.isnan(old.lo_ma), lo, old.lo_ma), np.where(np.isnan(old.hi_ma), hi, old.hi_ma)
        if np.any(self.lo < lo - 1e-9) or np.any(self.hi > hi + 1e-9):
            raise ValueError("a numerical age range must lie inside the unit's stage range")
        numeric = ~np.isnan(old.lo_ma)
        self._cuts = np.unique(np.r_[self.lo[numeric], self.hi[numeric]])
        self.rm, self.om = ref.mult, old.mult
        self.width = self.hi - self.lo
        self.Qref = np.clip((np.minimum(self.hi, self.tau) - self.lo) / self.width, 0.0, 1.0) if self.n_old else np.zeros(0)
        self.T_flat = float(self.hi.max()) if self.n_old else self.tau
        self.u, self.logw = gamma_nodes(spec.cluster_shape_k, spec.nodes)
        self.n_fits = self.n_flagged = self.n_failed = 0
        self._windows: dict = {}
        self._const: dict = {}
        self._profiles: dict = {}
        self._prev: dict = {}
        self.r_ref = np.full(self.n_cls, 0.1)
        self._th = np.log(self.r_ref)
        _, self._th, _ = self._profile(self.window((self.tau,), ref_only=True), np.zeros(0), np.zeros(0), np.zeros(0), False)
        self.r_ref = np.exp(self._th)
        self._wr = self.r_ref[self.oc] * self.om

    # --- windows -----------------------------------------------------------------------------

    def edges(self, T: float, lag: float = 0.0, cut: float | None = None) -> tuple[float, ...]:
        """Piece edges for origin T: tau, the stage bases and the ends of numerical unit ranges strictly
        between tau and T, T - lag and cut when they lie inside (tau, T), and T. Just (tau,) when T <= tau."""
        if T <= self.tau:
            return (self.tau,)
        b = np.r_[self.age.base, self._cuts]
        pts = [self.tau, float(T), *b[(b > self.tau + 1e-9) & (b < T - 1e-9)]]
        if lag > 0 and self.tau + 1e-9 < T - lag < T - 1e-9:
            pts.append(T - lag)
        if cut is not None and self.tau + 1e-9 < cut < T - 1e-9:
            pts.append(cut)
        return tuple(float(v) for v in np.unique(np.round(pts, 9)))

    def edges_const(self, T: float) -> tuple[float, ...]:
        return (self.tau, float(T)) if T > self.tau else (self.tau,)

    def window(self, edges, ref_only: bool = False) -> Window:
        key = (tuple(round(float(e), 9) for e in edges), ref_only)
        if key not in self._windows:
            if len(self._windows) > 400:
                self._windows.clear()
            self._windows[key] = self._build_window(np.array(key[0]), ref_only)
        return self._windows[key]

    def _build_window(self, edges: np.ndarray, ref_only: bool) -> Window:
        n = self.n_old
        plo, phi = edges[:-1], edges[1:]
        if n and len(plo):
            ov = np.clip(np.minimum(self.hi[:, None], phi[None]) - np.maximum(self.lo[:, None], plo[None]), 0.0, None) / self.width[:, None]
        else:
            ov = np.zeros((n, len(plo)))
        keep = ov.sum(axis=0) > 1e-12
        W = ov[:, keep]
        qmid = W.sum(axis=1)
        active = ((self.Qref > 0) | (qmid > 1e-12)) & (not ref_only)
        impossible = bool(np.any((self.od == 1) & ~active)) and not ref_only
        has_det = bool(np.any((self.od == 1) & (qmid > 1e-12)))
        rest = np.clip(1.0 - self.Qref - qmid, 0.0, 1.0)
        ids = np.unique(np.concatenate([self.rcl, self.ocl[active]]))
        ref = self._block(self.rcl, self.rc, ids, d=self.rd, mult=self.rm)
        old0 = self._old_block(active & (self.od == 0), ids, W, rest)
        old1 = self._old_block(active & (self.od == 1), ids, W, rest)
        E = None
        if not ref_only and n and qmid.sum() > 0:
            E = np.zeros((self.n_cls, W.shape[1]))
            np.add.at(E, self.oc, W * self.om[:, None])
        return Window(edges, float(edges[-1]), plo[keep], phi[keep], W, qmid, impossible, has_det, len(ids), ref, old0, old1, E)

    @staticmethod
    def _block(cluster: np.ndarray, cls: np.ndarray, ids: np.ndarray, **kw) -> Block:
        cpos = np.searchsorted(ids, cluster)
        starts = np.flatnonzero(np.r_[True, cpos[1:] != cpos[:-1]]) if len(cpos) else np.zeros(0, int)
        return Block(len(cpos), cls, cpos, starts, cpos[starts], **kw)

    def _old_block(self, mask: np.ndarray, ids: np.ndarray, W: np.ndarray, rest: np.ndarray) -> Block:
        idx = np.flatnonzero(mask)
        b = self._block(self.ocl[idx], self.oc[idx], ids, qref=self.Qref[idx], rest=rest[idx], mult=self.om[idx])
        ui, pi = np.nonzero(W[idx] > 1e-12) if W.shape[1] else (np.zeros(0, int), np.zeros(0, int))
        if len(ui):
            b.m_unit, b.m_piece, b.m_w = ui, pi, W[idx][ui, pi]
            b.m_starts = np.flatnonzero(np.r_[True, ui[1:] != ui[:-1]])
            b.m_units = ui[b.m_starts]
        return b

    # --- likelihood --------------------------------------------------------------------------

    def _eval(self, win: Window, theta: np.ndarray, x: np.ndarray, L: np.ndarray, U: np.ndarray, bound: bool, grad: bool = True):
        """Log-likelihood and its gradient with respect to (log r, x) for the piece means x. bound=False is
        the exact piecewise-constant likelihood; bound=True the chord and Jensen bound on [L, U]."""
        if win.impossible:
            return (-math.inf, np.zeros(len(theta) + len(x))) if grad else -math.inf
        r, u = np.exp(theta), self.u
        P = len(x)
        Lk = np.zeros((win.K, len(u)))
        rb, o0, o1 = win.ref, win.old0, win.old1

        ru_r = (r[rb.cls] * rb.mult)[:, None] * u
        d1 = rb.d == 1
        lp = np.where(d1[:, None], np.log(np.maximum(-np.expm1(-ru_r), TINY)), -ru_r)
        if rb.n:
            Lk[rb.seg_pos] += np.add.reduceat(lp, rb.seg_starts, axis=0)

        if bound:
            width = U - L
            pos = width > 0
            s = np.where(pos, (x - L) / np.where(pos, width, 1.0), 0.0)

        cache0 = None
        if o0.n:
            ru0 = (r[o0.cls] * o0.mult)[:, None] * u
            e1 = np.exp(-ru0)
            P0 = o0.qref[:, None] * e1 + o0.rest[:, None]
            if o0.m:
                R = ru0[o0.m_unit]
                if bound:
                    Lm, Um, sm = L[o0.m_piece][:, None], U[o0.m_piece][:, None], s[o0.m_piece][:, None]
                    eL, eU = np.exp(-R * Lm), np.exp(-R * Um)
                    chi = eL + sm * (eU - eL)
                else:
                    chi = np.exp(-R * x[o0.m_piece][:, None])
                P0 = P0 + _segsum(o0, o0.m_w[:, None] * chi)
            Lk[o0.seg_pos] += np.add.reduceat(np.log(np.maximum(P0, TINY)), o0.seg_starts, axis=0)
            cache0 = (ru0, e1, P0, R, chi) if o0.m else (ru0, e1, P0, None, None)

        cache1 = None
        if o1.n:
            ru1 = (r[o1.cls] * o1.mult)[:, None] * u
            e1b = np.exp(-ru1)
            D = o1.qref[:, None] * (1.0 - e1b)
            if o1.m:
                R1 = ru1[o1.m_unit]
                E1 = np.exp(-R1 * x[o1.m_piece][:, None])
                D = D + _segsum(o1, o1.m_w[:, None] * (1.0 - E1))
            Lk[o1.seg_pos] += np.add.reduceat(np.log(np.maximum(D, TINY)), o1.seg_starts, axis=0)
            cache1 = (ru1, e1b, D, R1, E1) if o1.m else (ru1, e1b, D, None, None)

        z = Lk + self.logw
        lc = _lse(z, axis=1)
        total = float(lc.sum())
        if not grad:
            return total
        pi = np.exp(z - lc[:, None])
        g_th, g_x = np.zeros(self.n_cls), np.zeros(P)

        pu = pi[rb.cpos]
        dl = np.where(d1[:, None], ru_r / np.expm1(ru_r), -ru_r)
        g_th += np.bincount(rb.cls, weights=(pu * dl).sum(axis=1), minlength=self.n_cls)

        if cache0 is not None:
            ru0, e1, P0, R, chi = cache0
            gi = np.where(P0 > TINY, pi[o0.cpos] / np.maximum(P0, TINY), 0.0)
            dth = -o0.qref[:, None] * ru0 * e1
            if o0.m:
                if bound:
                    dchi_th = -R * ((1.0 - sm) * Lm * eL + sm * Um * eU)
                    dchi_x = np.where(pos[o0.m_piece][:, None], (eU - eL) / np.where(pos, width, 1.0)[o0.m_piece][:, None], 0.0)
                else:
                    dchi_th = -R * x[o0.m_piece][:, None] * chi
                    dchi_x = -R * chi
                dth = dth + _segsum(o0, o0.m_w[:, None] * dchi_th)
                g_x += np.bincount(o0.m_piece, weights=o0.m_w * (gi[o0.m_unit] * dchi_x).sum(axis=1), minlength=P)
            g_th += np.bincount(o0.cls, weights=(gi * dth).sum(axis=1), minlength=self.n_cls)

        if cache1 is not None:
            ru1, e1b, D, R1, E1 = cache1
            gi = np.where(D > TINY, pi[o1.cpos] / np.maximum(D, TINY), 0.0)
            dth = o1.qref[:, None] * ru1 * e1b
            if o1.m:
                dth = dth + _segsum(o1, o1.m_w[:, None] * R1 * x[o1.m_piece][:, None] * E1)
                g_x += np.bincount(o1.m_piece, weights=o1.m_w * (gi[o1.m_unit] * R1 * E1).sum(axis=1), minlength=P)
            g_th += np.bincount(o1.cls, weights=(gi * dth).sum(axis=1), minlength=self.n_cls)
        return total, np.concatenate([g_th, g_x])

    # --- fits --------------------------------------------------------------------------------

    def _profile(self, win: Window, x, L, U, bound: bool, th0: np.ndarray | None = None):
        """Maximise over log r at fixed x (L-BFGS-B). Returns (value, theta, converged)."""
        if win.impossible:
            return -math.inf, self._th, True
        n = self.n_cls

        def obj(th):
            v, g = self._eval(win, th, x, L, U, bound)
            return (-v, -g[:n]) if np.isfinite(v) else (1e12, np.zeros(n))

        res = optimize.minimize(
            obj, self._th if th0 is None else th0, jac=True, method="L-BFGS-B", bounds=[LOG_R_BOUNDS] * n,
            options={"ftol": 1e-12, "gtol": 1e-6, "maxiter": 300},
        )
        ok = bool(res.success or np.abs(res.jac).max() < 1e-4)
        if res.fun < 1e11:
            self._th = res.x
            return -res.fun, res.x, ok
        return -math.inf, res.x, False

    def _record(self, fit: Fit) -> Fit:
        self.n_fits += 1
        self.n_flagged += int(fit.flagged)
        self.n_failed += int(not fit.converged)
        return fit

    def _const_profile(self, T: float, x: float) -> tuple[float, np.ndarray, bool]:
        """Profile (over the reference rates) log-likelihood of the constant history a = x on (tau, T], with
        its rates and convergence."""
        key = (round(float(T), 9), round(float(x), 12))
        if key not in self._profiles:
            win = self.window(self.edges_const(T))
            xv = np.full(win.P, float(x))
            self._profiles[key] = self._profile(win, xv, xv, xv, False)
        return self._profiles[key]

    def ell_const(self, T: float, x: float) -> float:
        return self._const_profile(T, x)[0]

    def const_max(self, T: float, lo: float = 0.0, hi: float = 1.0) -> tuple[float, float, bool, float]:
        """Maximum over constant x in [lo, hi] of the exact profile log-likelihood: (value, argmax, converged,
        spread). With no detected older unit the likelihood falls in x, so the maximum is at lo."""
        key = (round(float(T), 9), lo, hi)
        if key in self._const:
            return self._const[key]
        win = self.window(self.edges_const(T))
        n = self.n_cls
        if win.impossible:
            out = (-math.inf, lo, True, 0.0)
        elif not win.has_det or hi - lo < 1e-9:
            v, _, ok = self._profile(win, np.full(win.P, lo), np.zeros(win.P), np.zeros(win.P), False)
            self._record(Fit(v, None, None, ok, 0.0))
            out = (v, lo, ok, 0.0)
        else:
            def obj(z):
                v, g = self._eval(win, z[:n], np.full(win.P, z[n]), None, None, False)
                if not np.isfinite(v):
                    return 1e12, np.zeros(n + 1)
                return -v, -np.r_[g[:n], g[n:].sum()]

            def run(z0, maxiter):
                res = optimize.minimize(obj, z0, jac=True, method="L-BFGS-B", bounds=[LOG_R_BOUNDS] * n + [(lo, hi)],
                                        options={"ftol": 1e-12, "gtol": 1e-6, "maxiter": maxiter})
                return -res.fun, res.x, bool(res.success or np.abs(res.jac).max() < 1e-4)

            best, spread = select([run(np.r_[self._th, lo + frac * (hi - lo)], 300) for frac in (0.3, 0.7)])
            if not best[2]:
                again = run(best[1], REPAIR_ITER)
                if again[0] >= best[0] - 1e-9:
                    best = again
            self._record(Fit(best[0], best[1][:n], best[1][n:], best[2], spread))
            self._th = best[1][:n]
            out = (best[0], float(best[1][n]), best[2], spread)
        self._const[key] = out
        return out

    def _constraints(self, win: Window, mono: bool, target: bool, f: float):
        """Linear constraint rows on (log r, x): the target when its coefficients do not depend on the rates,
        and the monotone order for H0m."""
        n, P = self.n_cls, win.P
        rows, lb = [], []
        if target:
            rows.append(np.r_[np.zeros(n), win.coef(self._th)])
            lb.append(f)
        if mono:
            for p in range(P - 1):
                row = np.zeros(n + P)
                row[n + p], row[n + p + 1] = 1.0, -1.0
                rows.append(row)
                lb.append(0.0)
        return (np.array(rows), np.array(lb)) if rows else (None, None)

    def _starts(self, win: Window, L: np.ndarray, U: np.ndarray, mono: bool, f: float, target: bool, key, x_const) -> list[np.ndarray]:
        """The start (a), the constant history x_const = (x, theta) when given or else an even allocation
        at the reference rates, the hiding start (b), and the previous solution (c). The target allocations
        use the coefficients at the current rates."""
        P = win.P
        if x_const is not None:
            starts = [np.r_[x_const[1], np.clip(np.full(P, x_const[0]), L, U)]]
        else:
            x_even = np.clip(np.full(P, f), L, U) if target else L + 0.25 * (U - L)
            starts = [np.r_[np.log(self.r_ref), x_even]]
        x_hide = L + FLOOR * (U - L)
        if target:
            c = win.coef(self._th)
            need = f - c @ x_hide
            order = np.arange(P) if mono else np.argsort(c / (win.piece_hi - win.piece_lo), kind="stable")
            for p in order:
                if need <= 1e-14:
                    break
                add = min(U[p] - x_hide[p], need / c[p])
                x_hide[p] += add
                need -= add * c[p]
        starts.append(np.r_[self._th, x_hide])
        if target:
            vertex = self._vertex_start(win, L, U, mono, f)
            if vertex is not None:
                starts.append(np.r_[self._th, vertex])
        if key in self._prev:
            starts.append(self._prev[key])
        return starts

    def _vertex_start(self, win: Window, L: np.ndarray, U: np.ndarray, mono: bool, f: float) -> np.ndarray | None:
        """The best of the allocations that put the whole target on one piece (a step from the youngest piece
        for H0m), judged by the likelihood at the current rates: with finite k the supremum has local optima
        at such vertices."""
        base = L + FLOOR * (U - L)
        c = win.coef(self._th)
        best = None
        for p in range(win.P):
            idx = np.arange(p + 1) if mono else np.array([p])
            level = (f - c @ base + c[idx] @ base[idx]) / c[idx].sum()
            if level > U[idx].min() + 1e-12:
                continue
            x = base.copy()
            x[idx] = np.maximum(level, base[idx])
            v = self._eval(win, self._th, x, L, U, True, grad=False)
            if np.isfinite(v) and (best is None or v > best[0]):
                best = (v, x)
        return None if best is None else best[1]

    def bound_sup(self, win: Window, L: np.ndarray, U: np.ndarray, mono: bool = False, f: float = 0.0, x_const: tuple[float, np.ndarray] | None = None) -> Fit:
        """sup of the bound log-likelihood over (log r, x) with x_p in [L_p, U_p], monotone non-decreasing
        towards tau when mono, and the target c(r) . x >= f at the fit's own rates. x_const = (x, theta) adds
        the constant history x as a start."""
        P, n = win.P, self.n_cls
        if win.impossible:
            return Fit(-math.inf, None, None, True, 0.0)
        target = P > 0 and win.E is not None and f > win.target_floor(L) + 1e-12
        if (not win.has_det and not target) or np.all(U - L < 1e-12):
            if target:
                return self._record(Fit(-math.inf, None, None, False, 0.0))
            v, th, ok = self._profile(win, L.copy(), L, U, True)
            return self._record(Fit(v, th, L.copy(), ok, 0.0))
        bilinear = target and not win.rate_free
        A0, lb0 = self._constraints(win, mono, target and not bilinear, f)
        key = (win.edges.tobytes(), L.tobytes(), U.tobytes(), mono, target)
        starts = self._starts(win, L, U, mono, f, target, key, x_const)
        zlo, zhi = np.r_[[LOG_R_BOUNDS[0]] * n, L], np.r_[[LOG_R_BOUNDS[1]] * n, U]
        free = np.r_[np.ones(n, bool), U - L > 1e-12]
        fidx = np.flatnonzero(free)
        zfix = np.r_[np.zeros(n), L]
        A, lb = None, None
        if A0 is not None:
            lb = lb0 - A0[:, ~free] @ zfix[~free]
            A = A0[:, free]
            nnz = (A != 0).sum(axis=1)
            if np.any((nnz == 0) & (lb > VIOLATION)):
                return self._record(Fit(-math.inf, None, None, False, 0.0))
            for i in np.flatnonzero(nnz == 1):
                j = int(np.flatnonzero(A[i])[0])
                if A[i, j] > 0:
                    zlo[fidx[j]] = max(zlo[fidx[j]], lb[i] / A[i, j])
                else:
                    zhi[fidx[j]] = min(zhi[fidx[j]], lb[i] / A[i, j])
            keep = nnz >= 2
            A, lb = (A[keep], lb[keep]) if keep.any() else (None, None)
        flo, fhi = zlo[fidx], zhi[fidx]
        if np.any(flo > fhi + 1e-12):
            return self._record(Fit(-math.inf, None, None, False, 0.0))

        def expand(zf):
            z = zfix.copy()
            z[fidx] = zf
            return z

        def obj(zf):
            z = expand(zf)
            v, g = self._eval(win, z[:n], z[n:], L, U, True)
            return (-v, -g[fidx]) if np.isfinite(v) else (1e12, np.zeros(len(fidx)))

        constraints = [] if A is None else [optimize.LinearConstraint(A, lb, np.inf)]
        if bilinear:
            constraints.append(optimize.NonlinearConstraint(
                lambda zf: win.target(expand(zf)[:n], expand(zf)[n:])[0] - f, 0.0, np.inf,
                jac=lambda zf: win.target(expand(zf)[:n], expand(zf)[n:])[1][fidx][None, :],
            ))

        def violation(z):
            v = 0.0 if A0 is None else float((lb0 - A0[:, n:] @ z[n:]).max())
            if bilinear:
                v = max(v, f - win.target(z[:n], z[n:])[0])
            return max(0.0, v)

        def run(z0, maxiter):
            if constraints:
                res = optimize.minimize(obj, z0, jac=True, method="SLSQP", bounds=optimize.Bounds(flo, fhi),
                                        constraints=constraints, options={"ftol": 1e-10, "maxiter": maxiter})
                ok = bool(res.success)
            else:
                res = optimize.minimize(obj, z0, jac=True, method="L-BFGS-B", bounds=list(zip(flo, fhi)),
                                        options={"ftol": 1e-12, "gtol": 1e-6, "maxiter": maxiter})
                ok = bool(res.success or np.abs(res.jac).max() < 1e-4)
            z = expand(np.clip(res.x, flo, fhi))
            v = self._eval(win, z[:n], z[n:], L, U, True, grad=False)
            return (v, z, ok) if np.isfinite(v) and violation(z) <= VIOLATION else None

        results = [r for r in (run(np.clip(z0[fidx], flo, fhi), 400 if not constraints else 300) for z0 in starts) if r]
        if not results:
            return self._record(Fit(-math.inf, None, None, False, 0.0))
        best, spread = select(results)
        if not best[2]:
            again = run(best[1][fidx], REPAIR_ITER)
            if again and again[0] >= best[0] - 1e-9:
                best = again
        self._prev[key] = best[1]
        self._th = best[1][:n]
        return self._record(Fit(best[0], best[1][:n], best[1][n:], best[2], spread))

    # --- target and critical value -----------------------------------------------------------

    def _qmid(self, T: float) -> np.ndarray:
        over = np.minimum(self.hi, T) - np.maximum(self.lo, self.tau)
        return np.clip(over / self.width, 0.0, 1.0) if self.n_old else np.zeros(0)

    def exposure(self, T: float) -> float:
        """The integrated reference exposure: sum_i r_i Qmid_i(T), with the reference rates r_ref."""
        return float(self._wr @ self._qmid(T)) if self.n_old else 0.0

    def n_older_detections(self, T: float) -> int:
        """Older units that detected and have part of their age range in (tau, T]."""
        return int(((self.od == 1) & (self._qmid(T) > 0)).sum())

    def crit(self, T: float) -> float:
        """The critical value at origin T: count_crit of the older detections in (tau, T] plus crit_shift."""
        return count_crit(self.n_older_detections(T), self.spec.alpha) + self.spec.crit_shift

    def ceiling(self, cls: str) -> float:
        return self.spec.h1_ceiling if cls == "H1" else 1.0

    # --- f* and the statistic at a target ----------------------------------------------------

    def lr(self, cls: str, T: float, f: float) -> Statistic:
        """LR_K(f) at origin T for class cls (H0c, H0m, H0 or H1): 2 (alt - sup over the class of the
        log-likelihood given abar >= f), floored at 0; infinite when f exceeds the class ceiling or T is
        impossible. Needs exposure at T. Converged only when the alternative and the null both converged.
        At the ceiling (f within 1e-9 of C) every class's feasible set is the constant history C, whose bound
        likelihood is exact, so the null is that constant's profile likelihood."""
        C = self.ceiling(cls)
        alt, x_hat, alt_ok, alt_spread = self.const_max(T, 0.0, C)
        if not np.isfinite(alt) or f > C + 1e-9:
            return Statistic(math.inf, alt_ok, alt_spread)
        if cls == "H0c" or f >= C - 1e-9:
            if f <= x_hat:
                return Statistic(0.0, alt_ok, alt_spread)
            null, _, ok = self._const_profile(T, min(f, C))
            return Statistic(max(0.0, 2 * (alt - null)), alt_ok and ok, alt_spread)
        win = self.window(self.edges(T))
        zeros, top = np.zeros(win.P), np.full(win.P, C)
        x_c = max(f, x_hat)
        fit = self.bound_sup(win, zeros, top, cls == "H0m", f, x_const=(x_c, self._const_profile(T, x_c)[1]))
        value = max(0.0, 2 * (alt - fit.value)) if np.isfinite(fit.value) else math.inf
        return Statistic(value, alt_ok and fit.converged, max(alt_spread, fit.spread))

    def fstar(self, cls: str, T: float, crit: float | None = None) -> Bound:
        """f*_K(T) and its state for one history class (names as in Spec.classes, or H1-no-ceiling)."""
        crit = self.crit(T) if crit is None else crit
        if cls == "H1-no-ceiling":
            return Bound(cls, T, "zero-exposure" if self.exposure(T) <= 0 else "unbounded", math.inf, math.inf)
        if cls not in ("H0c", "H0m", "H0", "H1"):
            raise ValueError(cls)
        C = self.ceiling(cls)
        if self.exposure(T) <= 0:
            return Bound(cls, T, "zero-exposure", math.nan, C)
        alt, x_hat, alt_ok, alt_spread = self.const_max(T, 0.0, C)
        if not np.isfinite(alt):
            return Bound(cls, T, "finite", 0.0, C, alt_ok, alt_spread)
        seen: dict = {}

        def lr(f: float) -> float:
            if f not in seen:
                seen[f] = self.lr(cls, T, f)
            return seen[f].value

        if lr(C) <= crit:
            state, value = "ceiling-limited", C
        else:
            lo = x_hat if cls == "H0c" else 0.0
            value = float(optimize.brentq(lambda f: lr(f) - crit, lo, C, xtol=1e-3, rtol=1e-3))
            state = "finite"
        ok = all(s.converged for s in seen.values())
        return Bound(cls, T, state, value, C, ok, max(s.spread for s in seen.values()))

    # --- origins -----------------------------------------------------------------------------

    def grid(self, step: float) -> np.ndarray:
        """Candidate origins: tau, then every step Myr to the oldest possible unit age plus step plus the
        H0m lag, then the domain edge (beyond that the statistic does not change)."""
        top = min(self.T_flat + step + self.spec.h0m_lag_ma, self.spec.domain_ma[1])
        g = np.arange(self.tau, top + 1e-9, step)
        if g[-1] < self.spec.domain_ma[1]:
            g = np.append(g, self.spec.domain_ma[1])
        return g

    def origin_stat(self, cls: str, T: float, f_min: float, start: float | None = None) -> Statistic:
        """The origin test statistic at one T, exactly: 2 (alt - null), where alt is the best constant history
        on [0, 1] and null the supremum under the class's reading of "a >= f_min on (tau, T]" (module
        docstring). Zero for T <= tau; infinite when T is impossible. Converged only when the alternative and
        the null both converged.
        With start (H0 only), the window read-out: the null is "a >= f_min on (start, T]", with any path in
        [0, 1] on (tau, start]; zero for T <= start. It asks whether the lineage could have been at f_min
        before a given age, whatever it did afterwards."""
        if start is not None and cls != "H0":
            raise ValueError("the window read-out is defined for H0")
        if T <= self.tau or (start is not None and T <= start):
            return Statistic(0.0, True, 0.0)
        alt, _, alt_ok, alt_spread = self.const_max(T, 0.0, 1.0)
        if not np.isfinite(alt):
            return Statistic(math.inf, alt_ok, alt_spread)
        if cls == "H0c":
            null, _, ok, spread = self.const_max(T, f_min, 1.0)
        elif cls in ("H0", "H0m"):
            lag = self.spec.h0m_lag_ma if cls == "H0m" else 0.0
            win = self.window(self.edges(T, lag, start))
            if cls == "H0m":
                L = np.where(win.piece_hi <= T - lag + 1e-9, f_min, 0.0)
            elif start is not None:
                L = np.where(win.piece_lo >= start - 1e-9, f_min, 0.0)
            else:
                L = np.full(win.P, f_min)
            fit = self.bound_sup(win, L, np.ones(win.P), cls == "H0m")
            null, ok, spread = fit.value, fit.converged, fit.spread
        else:
            raise ValueError("origin sets are defined for H0c, H0 and H0m")
        ok, spread = alt_ok and ok, max(alt_spread, spread)
        return Statistic(max(0.0, 2 * (alt - null)) if np.isfinite(null) else math.inf, ok, spread)

    def lr_origin(self, cls: str, T: float, f_min: float) -> float:
        return self.origin_stat(cls, T, f_min).value

    def origin_set(self, cls: str, f_min: float, grid: np.ndarray, start: float | None = None) -> OriginSet:
        """Test inversion on the grid: T is excluded when the statistic exceeds crit. Past the point where
        every piece that carries weight lies at or younger than T - lag the statistic is constant, so it is
        copied. start gives the window read-out (origin_stat)."""
        lag = self.spec.h0m_lag_ma if cls == "H0m" else 0.0
        lr, ok = np.empty(len(grid)), np.empty(len(grid), bool)
        crit = np.array([self.crit(T) for T in grid])
        flat = np.flatnonzero(grid - lag >= self.T_flat - 1e-9)
        stop = int(flat[0]) if len(flat) else len(grid) - 1
        for i in range(stop + 1):
            st = self.origin_stat(cls, float(grid[i]), f_min, start)
            lr[i], ok[i] = st.value, st.converged
        lr[stop + 1:], ok[stop + 1:] = lr[stop], ok[stop]
        top = float(self.age.base[self.s_star - 1]) if self.s_star >= 1 else self.tau
        return OriginSet(cls, f_min, crit, grid, lr, self.spec.domain_ma[1], top, ok)

    def abar_truth(self, path, T: float, r: np.ndarray, step: float = 0.002) -> float:
        """The target abar(T) for a known path a(t) (vectorised) and reference rates r (one per
        calibrated class, in Problem order), by cumulative integration of the path."""
        if not self.n_old:
            return math.nan
        t = np.arange(self.lo.min() - 1.0, self.T_flat + 1.0, step)
        cum = np.concatenate([[0.0], np.cumsum(path(t[:-1] + step / 2) * step)])
        A = lambda v: np.interp(v, t, cum)
        over_hi, over_lo = np.minimum(self.hi, T), np.maximum(self.lo, self.tau)
        ok = over_hi > over_lo
        mass = np.where(ok, (A(over_hi) - A(over_lo)) / self.width, 0.0)
        qmid = np.where(ok, (over_hi - over_lo) / self.width, 0.0)
        w = r[self.oc] * self.om
        den = float((qmid * w).sum())
        return float((mass * w).sum() / den) if den > 0 else math.nan
