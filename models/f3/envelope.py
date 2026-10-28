# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""F3 reshape v3 (docs/f3-shape.md): the compatibility estimator for fossil absences.

Given eligible, binary sampling units it answers, under a named history class H: how intense could the
lineage's encounter intensity have been between the first appearance and a candidate origin T, and
which origins T are excluded by the empty older units?

Ages are Ma, decreasing towards the present, so older means larger. Units, stage ranges and the first
appearance follow the analysis specification (models/f3/specs/README.md).

Model. Unit i has a latent age t_i, uniform within its stage range given the stage boundaries, an
eligibility class c(i), a cluster k(i) and a binary outcome d_i. It detects with probability
1 - exp(-r_c u_k a(t_i)), where r_c = -log(1 - p_c), a(t) is the relative encounter intensity (1 in the
reference window) and u_k ~ Gamma(shape k, rate k) is a mean-one cluster effect (k = inf: none). Cluster
k then has no detection with probability (1 + Lambda_k / k)^-k, Lambda_k = sum r_i a(t_i).

Computation. Every likelihood is one integral over the cluster effect, with the units independent given
u and the boundary draw: L = mean_s prod_k  integral Gamma(u) prod_{i in k} phi_i(u; s) du, where
phi_i is the unit's detection (d = 1) or non-detection probability given u, averaged over its latent
age, and s indexes the boundary draws shared by all units. The integral is a trapezoid sum in log u
(spectrally accurate for these integrands; tests check it against the closed form and against
enumeration). Reference units (a = 1) and older units enter the same cluster integral, so a cluster
that spans the first appearance is treated jointly, and with finite k the reference likelihood is the
cluster-integrated one rather than a plain binomial (the two coincide for k = inf).

First appearance. tau is the older boundary of the oldest stage that contains a certain detection (a
detected unit whose whole range lies in that stage); that stage and the next reference_stages - 1
younger stages form the reference window, and units whose whole range lies in it are the reference
units. Units with any part of their range older than tau are the older units. A class with fewer than
min_units_per_class reference units is uncalibrated and its units are dropped.

History classes for the period older than tau (origin T > tau; a(t) = 0 for t > T):
  H0c  a = f on (tau, T], f in [0, 1].
  H0m  monotone non-decreasing towards tau, <= 1. Members: the constant, and the delayed step (a = 0
       on (T - d, T], then f), d from a declared grid. A delayed step is the constant history with
       origin T - d, so the likelihood is H0c's at T - d and only the target's exposure uses T.
  H0   any path 0 <= a <= 1. Convex-order bound: for fixed age-averaged intensities m_i = E[a(t_i)],
       P(no detection) is largest when each a(t_i) is replaced by an independent Bernoulli(m_i), because
       e^(-r x) and the cluster function (1 + x/k)^(-k) are convex and Bernoulli(m) dominates every
       [0, 1] variable with mean m in the convex order. So P0_max(m) = prod_k E_B[(1 + sum_{i in k} r_i
       B_i / k)^-k], B_i ~ Bernoulli(m_i) independent, which equals the u-integral above with
       phi_i = 1 - m_i (1 - e^(-r_i u)). It is attained by bang-bang paths, so it is exact for the
       worst case with a given duty cycle x: here m_i = Qref + x Qmid for the proportional allocation,
       whose reference part (a = 1) stays exact. A detected older unit uses the opposite extreme, the
       constant path a = x (Jensen), which maximises its detection probability. Each unit's bound
       depends only on its own mean, so the product is a valid upper bound on the likelihood of every
       path with those means. The bound treats ages as independent given the boundary draw, and is
       averaged over boundary draws. Limitation: only equal-duty paths are bounded. A path that puts
       more of its duty where the units' rates are higher can fit better at the same abar when the
       class mix differs between stages; for p = 0.30 against 0.03 in separate stages the gap is at
       most 0.06 in log P0 (about 3% in f*). f*_H0 is therefore the equal-duty bound, not the
       supremum over every path.
  logistic  a(t) = L(t) / L(tau), L(t) = 1 / (1 + exp(-g ((T - t) - h))), g and h profiled over a grid (h as a
       fraction of T - tau, so that late rises are on it; g = 0.001 is the near-constant member). Its
       members are tested against the same alternative as H0c (the best constant history, f = 0 included),
       not against the best logistic member, so that f* for a subclass never exceeds f* for H0.
  H1   sensitivity: any path 0 <= a <= h1_ceiling, so every pulse of that height or less, of any
       duration; the same bound with Bernoulli height C. With no ceiling the bound is trivial and the
       result unbounded.

Target. For origin T, abar(T) = E_ages[sum_i r_i a(t_i) 1{tau < t_i <= T}] / E_ages[sum_i r_i 1{tau < t_i
<= T}], expectations over the boundary draws and the latent ages (the integrated reference exposure in
the denominator). a = 1 is the reference window's own intensity, wherever the first appearance puts
the window, so abar is relative to it. f*_H(T) is the largest abar(T) over paths in H that a profile
likelihood-ratio test does not reject, the reference rates p_c profiled jointly with the history
parameters. H0c, H0, logistic and H1 are tested against the same alternative, the best constant
history on [0, C]. It belongs to each of those classes, so the statistic never exceeds the one with the
class's own supremum, and the test stays conservative where the H0 bound is not attained. H0m's members
are explicit, so it uses its exact supremum. Each (H, T) has one of four states: finite, ceiling-limited,
unbounded, zero-exposure.

Critical value. Both f* and the origin sets are one-sided upper limits on the older units' exposure.
The statistic is referred to exact_count_crit(n), n the older units detected with part of their range in
(tau, T]: the value that reproduces the exact one-sided Poisson (Garwood) limit. With no older detection
it is -2 log alpha = 5.99 (P0 >= alpha), falling towards the one-sided chi-square value 2.71. Chi-square(1)
at 3.84 is anti-conservative at zero counts, where the data lie: it rejects whenever P0 < 0.147.

Origins. T is excluded at level alpha when the hypothesis "a >= f_min on (tau, T]" is rejected (H0c) or
when no delay d on the grid and f >= f_min explains the absences (H0m). Each f_min read-out is a
marginal statement. If the profile reaches the edge of the domain, the origin is reported unbounded.
"""

import csv
import math
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy import optimize, stats

import sim

LOG_R_BOUNDS = (math.log(1e-5), math.log(8.0))
TINY = 1e-300
STATES = ("finite", "ceiling-limited", "unbounded", "zero-exposure")


class NoFirstAppearance(ValueError):
    """No certain detection, so the first appearance and the reference boundary are undefined."""


@dataclass(frozen=True)
class AgeModel:
    """ICS stage bases and their standard deviations (zero where data/timescale.csv is blank)."""

    timescale: sim.Timescale
    unc: np.ndarray

    @classmethod
    def load(cls, path: Path = sim.TIMESCALE_CSV) -> "AgeModel":
        with open(path, newline="") as f:
            unc = np.array([float(r["base_unc_ma"] or 0.0) for r in csv.DictReader(f)])
        return cls(sim.Timescale.load(path), unc)

    @property
    def base(self) -> np.ndarray:
        return self.timescale.base

    def draw_boundaries(self, rng: np.random.Generator, n: int) -> np.ndarray:
        """n draws of all stage bases: independent normals, then sorted so the stages stay ordered."""
        b = self.base + self.unc * rng.standard_normal((n, len(self.base)))
        return np.sort(b, axis=1)


@dataclass(frozen=True)
class Units:
    """Eligible binary sampling units. young and old index the youngest and oldest stage of the range."""

    young: np.ndarray
    old: np.ndarray
    cls: np.ndarray
    cluster: np.ndarray
    d: np.ndarray

    def __post_init__(self):
        n = len(self.d)
        if not all(len(a) == n for a in (self.young, self.old, self.cls, self.cluster)):
            raise ValueError("unit arrays differ in length")
        if np.any(self.young > self.old) or np.any(self.young < 1):
            raise ValueError("a unit's range must run from a stage younger than or equal to its oldest, and not the first stage")
        if not np.all((self.d == 0) | (self.d == 1)):
            raise ValueError("outcomes must be 0 or 1")

    def __len__(self) -> int:
        return len(self.d)

    def take(self, mask: np.ndarray) -> "Units":
        return Units(*(a[mask] for a in (self.young, self.old, self.cls, self.cluster, self.d)))


@dataclass(frozen=True)
class Spec:
    """The inference-side fields of an analysis specification (models/f3/specs/)."""

    reference_stages: int = 5
    min_units_per_class: int = 10
    domain_ma: tuple[float, float] = (0.0, 560.0)
    classes: tuple[str, ...] = ("H0c", "H0", "H0m", "logistic", "H1")
    h1_ceiling: float = 3.0
    delays_ma: tuple[float, ...] = (0.0, 2.0, 6.0, 10.0)
    logistic_g: tuple[float, ...] = (0.001, 0.15, 0.5, 2.0)
    logistic_h_frac: tuple[float, ...] = (0.0, 0.5, 1.0, 1.5)
    alpha: float = 0.05
    readouts: tuple[float, ...] = (1.0, 0.1, 0.01)
    cluster_shape_k: float = 2.0
    age_draws: int = 400
    nodes: int = 48

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
            delays_ma=tuple(h["delays_ma"]),
            logistic_g=tuple(h["logistic_g"]),
            logistic_h_frac=tuple(h["logistic_h_frac"]),
            alpha=inf["alpha"],
            readouts=tuple(inf["readouts"]),
            cluster_shape_k=inf["cluster_shape_k"],
            age_draws=inf["age_draws"],
            nodes=inf["nodes"],
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


def p0_bound(r: np.ndarray, m: np.ndarray, k: float, nodes: int = 48) -> float:
    """P0_max(m): the no-detection probability when each a(t_i) is Bernoulli(m_i), the maximum over
    all [0, 1]-valued a(t_i) with those means (convex order)."""
    vals = np.stack([np.zeros_like(m), np.ones_like(m)], axis=1)
    return no_detection_probability(r, vals, np.stack([1 - m, m], axis=1), k, nodes)


def exact_count_crit(n: int, alpha: float = 0.05) -> float:
    """The critical value: the LR value at which the Poisson upper limit for the older exposure equals the
    exact one-sided limit given n older detections, 2 (mu - n + n log(n / mu)) with
    mu = chi2_{2(n+1)}(1 - alpha) / 2. For n = 0 it is -2 log(alpha) = 5.99 (the rule of three); it falls
    towards 2.71 as n grows."""
    mu = stats.chi2.ppf(1 - alpha, 2 * (n + 1)) / 2
    return float(2 * (mu - n + (n * math.log(n / mu) if n else 0.0)))


@dataclass(frozen=True)
class Bound:
    """One (history class, T) result: the state and f*, the largest unrejected target."""

    cls: str
    T: float
    state: str
    value: float
    ceiling: float


@dataclass(frozen=True)
class OriginSet:
    """The origins not rejected on the grid T (ascending, first point = tau). lr is the statistic."""

    cls: str
    f_min: float
    crit: np.ndarray
    T: np.ndarray
    lr: np.ndarray
    domain_hi: float

    @property
    def keep(self) -> np.ndarray:
        return self.lr <= self.crit

    @property
    def runs(self) -> list[tuple[float, float]]:
        """Maximal runs of unrejected grid points, each widened to the next grid point (the bracket
        in which the boundary lies); the last run reaches the domain edge when it is unbounded."""
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
class Window:
    """Everything the likelihood needs about one candidate origin T: per-unit probabilities that the
    latent age falls in the reference regime (Qref) and in (tau, T] (Qmid), split into units whose
    values do not depend on the boundary draw (inv, with the reference units) and those that do (var),
    each sorted by cluster for segment sums."""

    T: float
    impossible: bool
    has_det: bool
    qmean: np.ndarray
    all_ids: np.ndarray
    pure: np.ndarray
    inv: dict
    var: dict | None
    var_pos: np.ndarray | None


class Problem:
    """One data set analysed under one specification: first appearance, reference window, boundary
    draws, and the profile likelihood machinery."""

    def __init__(self, units: Units, spec: Spec, age: AgeModel, seed: int | np.random.SeedSequence = 0):
        self.spec, self.age = spec, age
        ts = age.timescale
        certain = (units.d == 1) & (units.young == units.old)
        if not certain.any():
            raise NoFirstAppearance("no certain detection")
        self.s_star = int(units.old[certain].max())
        self.tau_nom = float(age.base[self.s_star])
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
        remap = np.full(len(counts), -1)
        remap[self.calibrated] = np.arange(len(self.calibrated))
        self.n_cls = len(self.calibrated)
        clusters, inv = np.unique(np.concatenate([ref.cluster, old.cluster]), return_inverse=True)
        self.rc, self.rd, self.rk = remap[ref.cls], ref.d, inv[: len(ref)]
        self.oc, self.od, self.ok = remap[old.cls], old.d, inv[len(ref):]
        self.n_ref, self.n_old = len(ref), len(old)
        S = spec.age_draws
        self.B = age.draw_boundaries(np.random.default_rng(seed), S)
        self.tau_s = self.B[:, self.s_star]
        self.lo = self.B[:, old.young - 1]
        self.hi = self.B[:, old.old]
        self.width = self.hi - self.lo
        self.Qref = np.clip((np.minimum(self.hi, self.tau_s[:, None]) - self.lo) / self.width, 0.0, 1.0)
        self.T_flat = float(self.hi.max()) if self.n_old else self.tau_nom
        self.u, self.logw = gamma_nodes(spec.cluster_shape_k, spec.nodes)
        self._windows: dict = {}
        self._cache: dict = {}
        self._th = np.full(self.n_cls, math.log(0.1))
        self.r_ref = np.exp(self._profile_theta(lambda r: self._ell_member(self.window(self.tau_nom), r, "const", 0.0, 1.0)))
        self._th = np.log(self.r_ref)

    # --- windows -----------------------------------------------------------------------------

    def window(self, T: float, all_var: bool = False) -> Window:
        T = max(float(T), float(self.tau_s.min()))
        key = (round(T, 9), all_var)
        if key in self._windows:
            return self._windows[key]
        if len(self._windows) > 150:
            self._windows.clear()
        w = self._build_window(T, all_var)
        self._windows[key] = w
        return w

    def _build_window(self, T: float, all_var: bool) -> Window:
        n = self.n_old
        if n:
            over = np.minimum(self.hi, T) - np.maximum(self.lo, self.tau_s[:, None])
            Qmid = np.clip(over / self.width, 0.0, 1.0)
            active = (self.Qref.max(0) > 0) | (Qmid.max(0) > 0)
            varies = (np.ptp(self.Qref, 0) > 1e-12) | (np.ptp(Qmid, 0) > 1e-12)
            var_mask = active & (varies | all_var)
            inv_mask = active & ~var_mask
            qmean = Qmid.mean(0)
        else:
            Qmid = np.zeros((len(self.tau_s), 0))
            active = var_mask = inv_mask = np.zeros(0, bool)
            qmean = np.zeros(0)
        impossible = bool(np.any((self.od == 1) & ~active))
        has_det = bool(np.any((self.od == 1) & (qmean > 0)))
        cluster = np.concatenate([self.rk, self.ok[inv_mask]])
        order = np.argsort(cluster, kind="stable")
        cl = cluster[order]
        starts = np.flatnonzero(np.r_[True, cl[1:] != cl[:-1]])
        inv = dict(
            cls=np.concatenate([self.rc, self.oc[inv_mask]])[order],
            d=np.concatenate([self.rd, self.od[inv_mask]])[order],
            qref=np.concatenate([np.ones(self.n_ref), self.Qref[0, inv_mask]])[order],
            qmid=np.concatenate([np.zeros(self.n_ref), Qmid[0, inv_mask]])[order],
            starts=starts,
            ids=cl[starts],
        )
        var = var_pos = None
        all_ids = inv["ids"]
        if var_mask.any():
            vorder = np.argsort(self.ok[var_mask], kind="stable")
            vcl = self.ok[var_mask][vorder]
            vstarts = np.flatnonzero(np.r_[True, vcl[1:] != vcl[:-1]])
            var = dict(
                cls=self.oc[var_mask][vorder],
                d=self.od[var_mask][vorder],
                qref=self.Qref[:, var_mask][:, vorder],
                qmid=Qmid[:, var_mask][:, vorder],
                lo=self.lo[:, var_mask][:, vorder],
                hi=self.hi[:, var_mask][:, vorder],
                starts=vstarts,
                ids=vcl[vstarts],
            )
            all_ids = np.union1d(inv["ids"], var["ids"])
            var_pos = np.searchsorted(all_ids, var["ids"])
        inv["pos"] = np.searchsorted(all_ids, inv["ids"])
        pure = np.ones(len(all_ids), bool)
        if var is not None:
            pure[var_pos] = False
        return Window(T, impossible, has_det, qmean, all_ids, pure, inv, var, var_pos)

    # --- likelihood --------------------------------------------------------------------------

    @staticmethod
    def _phi(d: np.ndarray, D: np.ndarray, axis: int) -> np.ndarray:
        """log of the outcome probability given u: log D for a detection, log(1 - D) for none. axis is the
        units axis of D."""
        out = np.log1p(-np.minimum(D, 1 - 1e-15))
        hit = d == 1
        if hit.any():
            idx = [slice(None)] * D.ndim
            idx[axis] = hit
            out[tuple(idx)] = np.log(np.maximum(D[tuple(idx)], TINY))
        return out

    def _ell(self, w: Window, Di: np.ndarray, Dv: np.ndarray | None) -> float:
        if w.impossible:
            return -math.inf
        J = len(self.u)
        Lk = np.zeros((len(w.all_ids), J))
        Lk[w.inv["pos"]] = np.add.reduceat(self._phi(w.inv["d"], Di, 0), w.inv["starts"], axis=0)
        total = float(_lse(Lk[w.pure] + self.logw).sum()) if w.pure.any() else 0.0
        if w.var is not None:
            S = Dv.shape[0]
            Lv = np.add.reduceat(self._phi(w.var["d"], Dv, 1), w.var["starts"], axis=1) + Lk[w.var_pos][None]
            per_s = _lse(Lv + self.logw).sum(axis=1)
            total += float(_lse(per_s) - math.log(S))
        return total

    def _ell_member(self, w: Window, r: np.ndarray, kind: str, x: float, C: float, atoms: np.ndarray | None = None) -> float:
        """Log-likelihood at reference rates r of one history member.

        const: a = x on (tau, T].  bound: duty cycle x at height C (Bernoulli bound, see the module
        docstring).  logistic: a(t) at the latent-age nodes `atoms` (S, n_var, Q)."""
        u = self.u
        A1 = -np.expm1(-np.outer(r, u))
        inv, var = w.inv, w.var
        if kind == "const":
            Ax = -np.expm1(-np.outer(r * x, u))
            mid_i = inv["qmid"][:, None] * Ax[inv["cls"]]
            mid_v = var["qmid"][:, :, None] * Ax[var["cls"]][None] if var else None
        elif kind == "bound":
            AC = -np.expm1(-np.outer(r * C, u))
            Ax = -np.expm1(-np.outer(r * x, u))
            mid_i = inv["qmid"][:, None] * np.where(inv["d"][:, None] == 0, (x / C) * AC[inv["cls"]], Ax[inv["cls"]])
            mid_v = (
                var["qmid"][:, :, None] * np.where(var["d"][None, :, None] == 0, (x / C) * AC[var["cls"]][None], Ax[var["cls"]][None])
                if var
                else None
            )
        else:
            mid_i = inv["qmid"][:, None] * 0.0
            Aa = -np.expm1(-(r[var["cls"]][None, :, None, None] * u[None, None, None, :]) * atoms[..., None]) if var else None
            mid_v = var["qmid"][:, :, None] * Aa.mean(axis=2) if var else None
        Di = inv["qref"][:, None] * A1[inv["cls"]] + mid_i
        Dv = var["qref"][:, :, None] * A1[var["cls"]][None] + mid_v if var else None
        return self._ell(w, Di, Dv)

    def _profile_theta(self, fn) -> np.ndarray:
        """Maximise fn(r) over the reference rates; returns log r at the optimum and keeps the value."""

        def obj(th):
            v = fn(np.exp(th))
            return -v if np.isfinite(v) else 1e12

        res = optimize.minimize(
            obj, self._th, method="L-BFGS-B", bounds=[LOG_R_BOUNDS] * self.n_cls, options={"ftol": 1e-10, "gtol": 1e-5}
        )
        self._last = -res.fun if res.fun < 1e11 else -math.inf
        if res.fun < 1e11:
            self._th = res.x
        return res.x

    def ell_p(self, kind: str, T: float, x: float, C: float = 1.0) -> float:
        """Profile (over the reference rates) log-likelihood of one history member at origin T."""
        key = (kind, round(float(T), 9), round(float(x), 12), C)
        if key in self._cache:
            return self._cache[key]
        w = self.window(T)
        if w.impossible:
            val = -math.inf
        else:
            self._profile_theta(lambda r: self._ell_member(w, r, kind, x, C))
            val = self._last
        if len(self._cache) > 20000:
            self._cache.clear()
        self._cache[key] = val
        return val

    def _maximise(self, kind: str, T: float, lo: float, hi: float, C: float) -> tuple[float, float]:
        """Max over x in [lo, hi] of ell_p; the boundary when no older unit is detected (ell decreases in x)."""
        w = self.window(T)
        if w.impossible:
            return -math.inf, lo
        f = lambda x: self.ell_p(kind, T, x, C)
        if not w.has_det or hi - lo < 1e-9:
            return f(lo), lo
        step = min(0.02, (hi - lo) / 4)
        if f(lo) >= f(lo + step) and f(lo) >= f(hi):
            return f(lo), lo
        res = optimize.minimize_scalar(lambda x: -f(x), bounds=(lo, hi), method="bounded", options={"xatol": 5e-3})
        best = max([(f(lo), lo), (f(hi), hi), (-res.fun, float(res.x))])
        return best

    def hat(self, kind: str, T: float, C: float = 1.0) -> tuple[float, float]:
        """The class maximum over x in [0, C] and its argmax."""
        return self._maximise(kind, T, 0.0, C, C)

    def null(self, kind: str, T: float, f_min: float, C: float = 1.0) -> float:
        """Maximum over x in [f_min, C]: the hypothesis a >= f_min on (tau, T]."""
        return self._maximise(kind, T, f_min, C, C)[0]

    def n_older_detections(self, T: float) -> int:
        """Older units that detected and have part of their age range in (tau, T]."""
        return int(((self.od == 1) & (self.window(T).qmean > 0)).sum())

    def crit(self, T: float) -> float:
        """The critical value at origin T (module docstring)."""
        return exact_count_crit(self.n_older_detections(T), self.spec.alpha)

    def exposure(self, T: float, r: np.ndarray | None = None) -> float:
        """The integrated reference exposure: sum_i r_i E[1{tau < t_i <= T}]."""
        w = self.window(T)
        r = self.r_ref if r is None else r
        return float(w.qmean @ r[self.oc]) if self.n_old else 0.0

    # --- bounds ------------------------------------------------------------------------------

    def _scalar_fstar(self, cls: str, kind: str, T: float, C: float, crit: float) -> Bound:
        if self.exposure(T) <= 0:
            return Bound(cls, T, "zero-exposure", math.nan, C)
        hat, x_hat = self.hat("const", T, C)
        lr = lambda x: 2 * (hat - self.ell_p(kind, T, x, C))
        if not np.isfinite(hat):
            return Bound(cls, T, "finite", 0.0, C)
        if lr(C) <= crit:
            return Bound(cls, T, "ceiling-limited", C, C)
        root = optimize.brentq(lambda x: lr(x) - crit, x_hat, C, xtol=1e-4, rtol=1e-4)
        return Bound(cls, T, "finite", float(root), C)

    def _h0m_fstar(self, T: float, crit: float) -> Bound:
        if self.exposure(T) <= 0:
            return Bound("H0m", T, "zero-exposure", math.nan, 1.0)
        delays = self.spec.delays_ma
        hats = {d: self.hat("const", T - d) for d in delays}
        class_hat = max(h for h, _ in hats.values())
        e_T = self.exposure(T)
        best, reached = 0.0, False
        for d in delays:
            hat_d, x_hat = hats[d]
            lr = lambda x: 2 * (class_hat - self.ell_p("const", T - d, x)) - crit
            if not np.isfinite(hat_d) or lr(x_hat) > 0:
                continue
            x_star = 1.0 if lr(1.0) <= 0 else optimize.brentq(lr, x_hat, 1.0, xtol=1e-4, rtol=1e-4)
            best = max(best, x_star * self.exposure(T - d) / e_T)
            reached |= d == 0 and x_star == 1.0
        return Bound("H0m", T, "ceiling-limited" if reached else "finite", 1.0 if reached else best, 1.0)

    def _logistic_atoms(self, w: Window, T: float, g: float, h: float, nq: int = 6) -> np.ndarray:
        """a(t) at nq midpoint nodes of each variable unit's age range within (tau_s, T]."""
        v = w.var
        lo = np.maximum(v["lo"], self.tau_s[:, None])
        hi = np.minimum(v["hi"], T)
        frac = (np.arange(nq) + 0.5) / nq
        t = lo[..., None] + np.maximum(hi - lo, 0.0)[..., None] * frac
        num = 1.0 + np.exp(-g * ((T - self.tau_s) - h))[:, None, None]
        return np.clip(num / (1.0 + np.exp(-g * ((T - t) - h))), 0.0, 1.0)

    def _logistic_fstar(self, T: float, crit: float) -> Bound:
        if self.exposure(T) <= 0:
            return Bound("logistic", T, "zero-exposure", math.nan, 1.0)
        w = self.window(T, all_var=True)
        members = []
        for g in self.spec.logistic_g:
            for frac in self.spec.logistic_h_frac:
                h = frac * (T - self.tau_nom)
                atoms = self._logistic_atoms(w, T, g, h) if w.var else None
                ell = -math.inf if w.impossible else self._ell_logistic(w, atoms)
                bar = self._abar_logistic(w, atoms)
                members.append((ell, bar))
        hat = self.hat("const", T)[0]  # the same alternative as H0c and H0, so f* is nested with them
        ok = [(bar, ell) for ell, bar in members if 2 * (hat - ell) <= crit]
        ceiling = max(bar for _, bar in members)
        top = max(ok)[0] if ok else 0.0
        top_member_ok = any(bar >= ceiling - 1e-9 for bar, _ in ok)
        return Bound("logistic", T, "ceiling-limited" if top_member_ok else "finite", float(ceiling if top_member_ok else top), float(ceiling))

    def _ell_logistic(self, w: Window, atoms: np.ndarray | None) -> float:
        self._profile_theta(lambda r: self._ell_member(w, r, "logistic", 0.0, 1.0, atoms))
        return self._last

    def _abar_logistic(self, w: Window, atoms: np.ndarray | None) -> float:
        if w.var is None:
            return 0.0
        v = w.var
        num = float((v["qmid"] * atoms.mean(axis=2) * self.r_ref[v["cls"]][None]).sum(axis=1).mean())
        den = float(w.qmean @ self.r_ref[self.oc])
        return num / den

    def fstar(self, cls: str, T: float, crit: float | None = None) -> Bound:
        """f*_H(T) and its state for one history class (names as in Spec.classes)."""
        crit = self.crit(T) if crit is None else crit
        if cls == "H0c":
            return self._scalar_fstar("H0c", "const", T, 1.0, crit)
        if cls == "H0":
            return self._scalar_fstar("H0", "bound", T, 1.0, crit)
        if cls == "H1":
            return self._scalar_fstar("H1", "bound", T, self.spec.h1_ceiling, crit)
        if cls == "H1-no-ceiling":
            return Bound(cls, T, "zero-exposure" if self.exposure(T) <= 0 else "unbounded", math.inf, math.inf)
        if cls == "H0m":
            return self._h0m_fstar(T, crit)
        if cls == "logistic":
            return self._logistic_fstar(T, crit)
        raise ValueError(cls)

    # --- origins -----------------------------------------------------------------------------

    def grid(self, step: float) -> np.ndarray:
        """Candidate origins: tau, then every step Myr to the oldest possible unit age plus the longest H0m
        delay, then the domain edge (beyond the oldest unit the likelihood does not change)."""
        top = min(self.T_flat + step + max(self.spec.delays_ma), self.spec.domain_ma[1])
        g = np.arange(self.tau_nom, top + 1e-9, step)
        if g[-1] < self.spec.domain_ma[1]:
            g = np.append(g, self.spec.domain_ma[1])
        return g

    def origin_tables(self, grid: np.ndarray) -> dict:
        """Constant-history log-likelihood tables on the grid: the class maximum, and the maximum under
        a >= f_min for each read-out."""
        hat = np.array([self.hat("const", T)[0] for T in grid])
        null = {f: np.array([self.null("const", T, f) for T in grid]) for f in self.spec.readouts}
        return dict(grid=grid, hat=hat, null=null)

    def origin_set(self, tables: dict, cls: str, f_min: float, crit: float | None = None) -> OriginSet:
        """Test inversion on the grid: T is excluded when the LR for 'a >= f_min on (tau, T]' exceeds crit.
        H0m takes the best delay d on the grid for both the null and the alternative: T - d is read at the
        grid point at or younger than it (the likelihood is flat past the oldest unit)."""
        grid, hat, null = tables["grid"], tables["hat"], tables["null"][f_min]
        crit = np.array([self.crit(T) for T in grid]) if crit is None else np.full(len(grid), float(crit))
        if cls == "H0m":
            idx = lambda d: np.clip(np.searchsorted(grid, grid - d, side="right") - 1, 0, None)
            hat = np.max([hat[idx(d)] for d in self.spec.delays_ma], axis=0)
            null = np.max([null[idx(d)] for d in self.spec.delays_ma], axis=0)
        elif cls != "H0c":
            raise ValueError("origin sets are defined for H0c and H0m")
        with np.errstate(invalid="ignore"):
            lr = np.where(np.isfinite(hat) & np.isfinite(null), np.maximum(2 * (hat - null), 0.0), math.inf)
        return OriginSet(cls, f_min, crit, grid, lr, self.spec.domain_ma[1])

    def lr_origin(self, cls: str, T: float, f_min: float) -> float:
        """The origin test statistic at one T, exactly (not on a grid). H0m uses the delays as given."""
        delays = (0.0,) if cls == "H0c" else self.spec.delays_ma
        hat = max(self.hat("const", T - d)[0] for d in delays)
        null = max(self.null("const", T - d, f_min) for d in delays)
        return 2 * (hat - null) if np.isfinite(hat) and np.isfinite(null) else math.inf

    def abar_truth(self, path, T: float, r: np.ndarray, step: float = 0.002) -> float:
        """The target abar(T) for a known path a(t) (vectorised) and reference rates r (one per
        calibrated class, in Problem order), by cumulative integration of the path."""
        t = np.arange(self.B.min() - 1.0, self.T_flat + 1.0, step)
        cum = np.concatenate([[0.0], np.cumsum(path(t[:-1] + step / 2) * step)])
        A = lambda x: np.interp(x, t, cum)
        over_hi = np.minimum(self.hi, T)
        over_lo = np.maximum(self.lo, self.tau_s[:, None])
        ok = over_hi > over_lo
        mass = np.where(ok, (A(over_hi) - A(over_lo)) / self.width, 0.0)
        qmid = np.where(ok, (over_hi - over_lo) / self.width, 0.0)
        den = (qmid * r[self.oc][None]).sum(axis=1).mean()
        return float((mass * r[self.oc][None]).sum(axis=1).mean() / den) if den > 0 else math.nan
