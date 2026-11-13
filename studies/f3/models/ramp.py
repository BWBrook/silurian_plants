"""Ramp-aware likelihood estimators of a clade's origination age from stage-binned record counts.

Ages are Ma, decreasing towards the present: older is larger. The clade originates at T0 with one
lineage; N(t) = 0 for t > T0 and N grows as s = T0 - t Myr pass. Channel c records in stage j are
Poisson with mean psi_c * E_cj * integral of N over the stage, with E a known effort series. The
data are the counts per stage and channel, so no dating within a stage enters.

Growth forms (`Logistic`, `ExpectedBirthDeath`) have closed-form stage integrals. For fixed T0 and
growth rate the maximum-likelihood psi_c is n_c / (sum_j E_cj I_j), so psi is profiled out exactly and
the surface is a function of T0 and the rate. `RampModel` caches the stage integrals on a grid of
both; `fit` finds the maximum on the grid, polishes it with scipy, and reads the 95% profile
interval for T0 (a chi-square drop of 1.92 in log-likelihood) off the profile over the rate. The
profile is unbounded when it is still inside the interval at the oldest origination considered,
`T0_MAX`: the records then do not exclude an arbitrarily old origination.

Channels share N(t) and T0 and have separate psi and E, so the joint fit is the same surface with the
channels' log-likelihoods added. A channel without records adds nothing.
"""

from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np
from scipy import optimize, stats

T0_MAX = 515.5  # Ma; oldest origination searched: the oldest clock maximum named in studies/f3/docs/plan-f3.md
T0_STEP = 0.5  # Myr
PROFILE_LEVEL = 0.5 * stats.chi2.ppf(0.95, 1)
LOG_ZERO = -1e30
POLISH_CELLS = 3
NARROW_MYR = 1.5
FINE_HALF_WIDTH = 1.0
RATES = np.geomspace(0.01, 3.0, 80)
NET_RATES = np.concatenate([[0.0], np.geomspace(1e-4, 1.0, 99)])
GRID_DEFICIT = 0.2  # log-likelihood units by which the polished maximum may exceed the grid profile before the interval is recomputed finely


class Family(Protocol):
    name: str
    default_rates: np.ndarray

    def grid(self, rates: np.ndarray) -> dict[str, np.ndarray]: ...

    def cumulative(self, s: np.ndarray, **p: np.ndarray) -> np.ndarray:
        """Phi(s) with Phi' = N, up to a constant: stage integrals are differences of Phi."""
        ...


@dataclass(frozen=True)
class Logistic:
    """N(s) = k / (1 + (k - 1) exp(-r s)), N(0) = 1, with capacity k fixed and rate r free."""

    k: float = 100.0
    name: str = "logistic"
    default_rates = RATES

    def grid(self, rates: np.ndarray) -> dict[str, np.ndarray]:
        return {"rate": rates, "k": np.full(len(rates), float(self.k))}

    def cumulative(self, s: np.ndarray, rate: np.ndarray, k: np.ndarray) -> np.ndarray:
        return k * s + (k / rate) * np.log1p((k - 1.0) * np.exp(-rate * s))


@dataclass(frozen=True)
class ExpectedBirthDeath:
    """The expected birth-death curve N(s) = exp(g s) with net rate g = lambda - mu >= 0 free.
    g = 0 is the constant-abundance case."""

    name: str = "birth-death"
    default_rates = NET_RATES

    def grid(self, rates: np.ndarray) -> dict[str, np.ndarray]:
        return {"rate": rates}

    def cumulative(self, s: np.ndarray, rate: np.ndarray) -> np.ndarray:
        safe = np.where(rate > 0, rate, 1.0)
        return np.where(rate > 0, np.expm1(rate * s) / safe, s)


@dataclass(frozen=True)
class Fit:
    t0: float
    params: dict[str, float]
    psi: np.ndarray
    loglik: float
    lo: float
    hi: float
    bounded: bool
    t0_grid: np.ndarray
    profile: np.ndarray


def _check(n: np.ndarray, effort: np.ndarray, n_stages: int) -> tuple[np.ndarray, np.ndarray]:
    n, effort = np.atleast_2d(np.asarray(n, dtype=float)), np.atleast_2d(np.asarray(effort, dtype=float))
    if n.shape != effort.shape or n.shape[1] != n_stages:
        raise ValueError(f"counts and effort must both have shape (channels, {n_stages})")
    if np.any(n < 0) or np.any(effort < 0):
        raise ValueError("counts and effort must be non-negative")
    if np.any((n > 0) & (effort == 0)):
        raise ValueError("records in a stage with zero effort")
    if n.sum() == 0:
        raise ValueError("no records: the origination age is not estimable")
    return n, effort


def _loglik(mass: np.ndarray, logmass: np.ndarray, n: np.ndarray, effort: np.ndarray) -> np.ndarray | float:
    """Poisson log-likelihood, up to the constant -sum log(n!), with psi profiled out. `mass` holds the
    stage integrals on its last axis; a channel's terms need only its occupied stages."""
    total = 0.0
    for n_c, e_c in zip(n, effort):
        t = n_c.sum()
        if t == 0:
            continue
        occupied = n_c > 0
        exposure = np.maximum(mass @ e_c, 1e-300)
        total = total + logmass @ n_c - t * np.log(exposure) + (n_c[occupied] * np.log(e_c[occupied])).sum() + t * np.log(t) - t
    return np.where(total < LOG_ZERO / 1e10, -np.inf, total)


def _log_mass(mass: np.ndarray) -> np.ndarray:
    return np.where(mass > 0, np.log(np.where(mass > 0, mass, 1.0)), LOG_ZERO)


class RampModel:
    """Stage integrals of one growth family on a grid of origination ages and growth rates."""

    def __init__(self, edges: np.ndarray, family: Family, t0_grid: np.ndarray | None = None, rates: np.ndarray | None = None):
        self.edges = np.asarray(edges, dtype=float)
        if np.any(np.diff(self.edges) <= 0):
            raise ValueError("stage edges must ascend: older is larger")
        self.family = family
        self.t0_grid = np.arange(T0_MAX, self.edges[0], -T0_STEP)[::-1] if t0_grid is None else np.asarray(t0_grid, float)
        self.params = family.grid(family.default_rates if rates is None else np.asarray(rates, dtype=float))
        self.mass = self.stage_mass(self.t0_grid[:, None], {k: v[None, :] for k, v in self.params.items()})
        self.logmass = _log_mass(self.mass)

    @property
    def n_stages(self) -> int:
        return len(self.edges) - 1

    def stage_mass(self, t0: np.ndarray | float, params: dict[str, np.ndarray | float]) -> np.ndarray:
        """Integral of N over each stage for origination at t0, on a new last axis. A stage older than
        t0 has none, and a stage holding t0 only the part younger than it."""
        t0 = np.asarray(t0, dtype=float)
        s = np.clip(t0[..., None] - self.edges, 0.0, None)
        phi = self.family.cumulative(s, **{k: np.asarray(v, dtype=float)[..., None] for k, v in params.items()})
        return np.maximum(phi[..., :-1] - phi[..., 1:], 0.0)

    def surface(self, n: np.ndarray, effort: np.ndarray) -> np.ndarray:
        """Profile log-likelihood over (T0, rate); -inf where a stage with records is older than T0."""
        n, effort = _check(n, effort, self.n_stages)
        return _loglik(self.mass, self.logmass, n, effort)


def fit(models: RampModel | Sequence[RampModel], n: np.ndarray, effort: np.ndarray, polish: bool = True) -> Fit:
    """Maximum-likelihood T0, growth rate and psi per channel, with the 95% profile interval for T0.

    `n` and `effort` have shape (channels, stages). Several models on the same T0 grid (for example
    logistic with different capacities) are profiled over: the profile is their pointwise maximum.
    An interval narrower than NARROW_MYR, or a grid profile more than GRID_DEFICIT below the polished
    maximum, means the grid is too coarse for the likelihood: the interval is then recomputed on a
    fine grid of T0 and rate."""
    models = [models] if isinstance(models, RampModel) else list(models)
    n, effort = _check(n, effort, models[0].n_stages)
    surfaces = [m.surface(n, effort) for m in models]
    profiles = np.array([_profile(s) for s in surfaces])
    best = int(np.argmax([s.max() for s in surfaces]))
    model, surface, profile = models[best], surfaces[best], profiles.max(axis=0)
    i, j = np.unravel_index(int(np.argmax(surface)), surface.shape)
    t0_hat, params, ll_hat = float(model.t0_grid[i]), {k: float(v[j]) for k, v in model.params.items()}, float(surface[i, j])
    if polish:
        t0_hat, params, ll_hat = _polish(model, n, effort, i, j, t0_hat, params, ll_hat)
    edge = model.edges[np.flatnonzero((n > 0).any(axis=0)).max()]
    interval = _interval(model.t0_grid, profile, ll_hat, edge)
    if interval is None or interval[1] - interval[0] < NARROW_MYR or ll_hat - profile.max() > GRID_DEFICIT:
        interval = _fine_interval(models, n, effort, t0_hat, edge, interval)
    lo, hi, bounded = interval
    mass = model.stage_mass(t0_hat, params)
    exposure = np.array([mass @ e_c for e_c in effort])
    psi = np.divide(n.sum(axis=1), exposure, out=np.zeros(len(n)), where=exposure > 0)
    return Fit(t0_hat, params, psi, ll_hat, lo, hi, bounded, model.t0_grid, profile)


def _profile(surface: np.ndarray) -> np.ndarray:
    """Maximum over rate at each T0, refined by the parabola through the grid maximum and its two
    neighbours (the rate grids are uniform in log rate, so the parabola is in log rate)."""
    rows = np.arange(len(surface))
    j = surface.argmax(axis=1)
    b = surface[rows, j]
    a, c = surface[rows, np.maximum(j - 1, 0)], surface[rows, np.minimum(j + 1, surface.shape[1] - 1)]
    with np.errstate(invalid="ignore"):
        curvature = a - 2.0 * b + c
        usable = (j >= 2) & (j <= surface.shape[1] - 2) & np.isfinite(a) & np.isfinite(b) & np.isfinite(c) & (curvature < 0)
    refined = b.copy()
    refined[usable] = b[usable] - (c[usable] - a[usable]) ** 2 / (8.0 * curvature[usable])
    return refined


def _box(model: RampModel, i: int, j: int) -> tuple[float, float, float, float]:
    rates, grid = model.params["rate"], model.t0_grid
    lo_t, hi_t = max(grid[max(i - POLISH_CELLS, 0)], model.edges[0]), min(grid[min(i + POLISH_CELLS, len(grid) - 1)], T0_MAX)
    return lo_t, hi_t, rates[max(j - POLISH_CELLS, 0)], rates[min(j + POLISH_CELLS, len(rates) - 1)]


def _polish(model: RampModel, n, effort, i, j, t0_hat, params, ll_hat):
    """Refine the grid maximum with Nelder-Mead inside the box of POLISH_CELLS grid cells around it."""
    lo_t, hi_t, lo_r, hi_r = _box(model, i, j)
    fixed = {k: v for k, v in params.items() if k != "rate"}

    def negative(x: np.ndarray) -> float:
        t0, rate = lo_t + x[0] * (hi_t - lo_t), lo_r + x[1] * (hi_r - lo_r)
        mass = model.stage_mass(t0, {"rate": rate, **fixed})
        value = float(_loglik(mass, _log_mass(mass), n, effort))
        return -value if np.isfinite(value) else 1e30

    start = np.array([(t0_hat - lo_t) / (hi_t - lo_t), (params["rate"] - lo_r) / (hi_r - lo_r) if hi_r > lo_r else 0.5])
    simplex = np.array([start, start + [0.1, 0.0], start + [0.0, 0.1]])
    result = optimize.minimize(negative, start, method="Nelder-Mead", bounds=[(0, 1), (0, 1)],
                               options={"initial_simplex": np.clip(simplex, 0, 1), "xatol": 1e-4, "fatol": 1e-8})
    if -result.fun <= ll_hat:
        return t0_hat, params, ll_hat
    x = np.clip(result.x, 0, 1)
    return lo_t + x[0] * (hi_t - lo_t), {**params, "rate": lo_r + x[1] * (hi_r - lo_r)}, float(-result.fun)


def _fine_interval(models, n, effort, t0_hat, edge, coarse):
    """The profile interval on a T0 grid centred on the maximum and a rate grid four times finer than
    the default, over every model; the T0 grid is widened until the interval lies inside it. Falls
    back to the grid interval if none does."""
    for half in (FINE_HALF_WIDTH, 3 * FINE_HALF_WIDTH, 10 * FINE_HALF_WIDTH):
        t0 = np.linspace(t0_hat - half, t0_hat + half, 161)
        profile = np.max([_profile(RampModel(m.edges, m.family, t0, _fine_rates(m.family)).surface(n, effort)) for m in models], axis=0)
        fine = _interval(t0, profile, profile.max(), edge)
        if fine[2] and fine[0] > t0[0]:
            return fine
    return coarse or fine


def _fine_rates(family: Family) -> np.ndarray:
    rates = family.default_rates
    positive = rates[rates > 0]
    fine = np.geomspace(positive[0], positive[-1], 4 * len(rates))
    return np.concatenate([[0.0], fine]) if rates[0] == 0 else fine


def _interval(t0: np.ndarray, profile: np.ndarray, ll_hat: float, edge: float) -> tuple[float, float, bool] | None:
    """Hull of the T0 values within PROFILE_LEVEL of the maximum, by linear interpolation between grid
    points; None if no grid point is that close, which happens when the grid is too coarse for the
    likelihood. `edge` is the top of the oldest stage with records, the youngest origination possible."""
    level = max(ll_hat, profile.max()) - PROFILE_LEVEL
    inside = np.flatnonzero(profile >= level)
    if len(inside) == 0:
        return None
    first, last = inside[0], inside[-1]
    bounded = last < len(t0) - 1
    hi = _crossing(t0[last], profile[last], t0[last + 1], profile[last + 1], level) if bounded else float(t0[-1])
    if first == 0 or not np.isfinite(profile[first - 1]):
        lo = float(max(edge, t0[first - 1])) if first > 0 else float(t0[0])
    else:
        lo = _crossing(t0[first - 1], profile[first - 1], t0[first], profile[first], level)
    return lo, hi, bool(bounded)


def _crossing(x0: float, y0: float, x1: float, y1: float, level: float) -> float:
    return float(x0 + (level - y0) * (x1 - x0) / (y1 - y0))
