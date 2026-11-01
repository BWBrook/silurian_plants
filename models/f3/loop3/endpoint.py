# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///
"""One-sided origination bounds under a fixed positive recovery history.

Conditional on the number of independent fossil horizons, cumulative recovery exposure transforms
their ages to uniform order statistics. This module implements the exact known-younger-cutoff bound
and the Strauss-Sadler/Marshall observed-range bound in that exposure coordinate.
"""

from dataclasses import dataclass
from typing import Literal

import numpy as np


Status = Literal["bounded", "at_boundary", "beyond_domain", "undefined"]


@dataclass(frozen=True)
class EndpointBound:
    bound_ma: float
    status: Status
    confidence: float
    n_horizons: int
    oldest_ma: float
    youngest_ma: float
    target_exposure: float
    exposure_cap: float
    domain_max_ma: float
    method: Literal["known_cutoff", "observed_range"]


class PiecewiseRecovery:
    """Piecewise-constant recovery density on ascending age edges (Ma)."""

    def __init__(self, edges_ma: np.ndarray, density_per_myr: np.ndarray):
        edges = np.asarray(edges_ma, dtype=float)
        density = np.asarray(density_per_myr, dtype=float)
        if edges.ndim != 1 or density.ndim != 1 or len(edges) != len(density) + 1:
            raise ValueError("edges must be one-dimensional and one longer than density")
        if len(density) == 0 or not np.all(np.isfinite(edges)) or not np.all(np.isfinite(density)):
            raise ValueError("recovery edges and densities must be finite and non-empty")
        if np.any(np.diff(edges) <= 0):
            raise ValueError("recovery edges must increase with age")
        if np.any(density <= 0):
            raise ValueError("recovery density must be strictly positive")
        self.edges_ma = edges
        self.density_per_myr = density
        self._cumulative = np.concatenate([[0.0], np.cumsum(np.diff(edges) * density)])

    @property
    def exposure_cap(self) -> float:
        return float(self._cumulative[-1])

    def exposure(self, age_ma: np.ndarray | float) -> np.ndarray | float:
        """Cumulative recovery exposure from the youngest edge to each age."""
        age = np.asarray(age_ma, dtype=float)
        if np.any(~np.isfinite(age)) or np.any(age < self.edges_ma[0]) or np.any(age > self.edges_ma[-1]):
            raise ValueError("age lies outside the recovery history")
        i = np.searchsorted(self.edges_ma, age, side="right") - 1
        i = np.minimum(i, len(self.density_per_myr) - 1)
        out = self._cumulative[i] + (age - self.edges_ma[i]) * self.density_per_myr[i]
        return float(out) if age.ndim == 0 else out

    def age_at(self, exposure: np.ndarray | float) -> np.ndarray | float:
        """Inverse cumulative exposure within the declared recovery history."""
        value = np.asarray(exposure, dtype=float)
        if np.any(~np.isfinite(value)) or np.any(value < 0) or np.any(value > self.exposure_cap):
            raise ValueError("exposure lies outside the recovery history")
        i = np.searchsorted(self._cumulative, value, side="right") - 1
        i = np.minimum(i, len(self.density_per_myr) - 1)
        out = self.edges_ma[i] + (value - self._cumulative[i]) / self.density_per_myr[i]
        return float(out) if value.ndim == 0 else out


def _ages(ages_ma: np.ndarray, recovery: PiecewiseRecovery) -> np.ndarray:
    ages = np.asarray(ages_ma, dtype=float)
    if ages.ndim != 1 or np.any(~np.isfinite(ages)):
        raise ValueError("fossil ages must be a finite one-dimensional array")
    if len(ages) and (ages.min() < recovery.edges_ma[0] or ages.max() > recovery.edges_ma[-1]):
        raise ValueError("fossil age lies outside the recovery history")
    return ages


def _confidence(confidence: float) -> float:
    if not np.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must lie strictly between zero and one")
    return 1.0 - float(confidence)


def _result(
    target: float,
    recovery: PiecewiseRecovery,
    confidence: float,
    ages: np.ndarray,
    method: Literal["known_cutoff", "observed_range"],
) -> EndpointBound:
    tolerance = 64 * np.finfo(float).eps * max(1.0, recovery.exposure_cap)
    if target < recovery.exposure_cap - tolerance:
        bound, status = recovery.age_at(target), "bounded"
    elif target <= recovery.exposure_cap + tolerance:
        bound, status = float(recovery.edges_ma[-1]), "at_boundary"
    else:
        bound, status = float("nan"), "beyond_domain"
    return EndpointBound(
        bound_ma=bound,
        status=status,
        confidence=confidence,
        n_horizons=len(ages),
        oldest_ma=float(ages.max()),
        youngest_ma=float(ages.min()),
        target_exposure=float(target),
        exposure_cap=recovery.exposure_cap,
        domain_max_ma=float(recovery.edges_ma[-1]),
        method=method,
    )


def known_cutoff_bound(
    ages_ma: np.ndarray,
    recovery: PiecewiseRecovery,
    cutoff_ma: float,
    confidence: float = 0.95,
) -> EndpointBound:
    """Exact conditional bound when the lineage is recoverable to a fixed younger cutoff.

    Given n independent horizons from density proportional to the fixed recovery history between
    the cutoff and origination T, the maximum transformed age M satisfies
    P(M / U(T) <= x | n) = x**n. Inverting its lower alpha tail gives the older bound.
    """
    ages = _ages(ages_ma, recovery)
    if len(ages) == 0:
        return known_cutoff_summary(0, float("nan"), recovery, cutoff_ma, confidence)
    if np.any(ages < cutoff_ma):
        raise ValueError("all fossil ages must be at least as old as the fixed cutoff")
    return known_cutoff_summary(len(ages), float(ages.max()), recovery, cutoff_ma, confidence)


def known_cutoff_summary(
    n_horizons: int,
    oldest_ma: float,
    recovery: PiecewiseRecovery,
    cutoff_ma: float,
    confidence: float = 0.95,
) -> EndpointBound:
    """Known-cutoff bound from the sufficient statistics n and the oldest horizon age."""
    alpha = _confidence(confidence)
    if not isinstance(n_horizons, (int, np.integer)) or n_horizons < 0:
        raise ValueError("n_horizons must be a non-negative integer")
    cutoff = float(cutoff_ma)
    cutoff_exposure = recovery.exposure(cutoff)
    if n_horizons == 0:
        return EndpointBound(float("nan"), "undefined", confidence, 0, float("nan"), cutoff,
                             float("nan"), recovery.exposure_cap, float(recovery.edges_ma[-1]),
                             "known_cutoff")
    oldest = float(oldest_ma)
    if not np.isfinite(oldest) or oldest < cutoff:
        raise ValueError("oldest_ma must be finite and at least as old as the fixed cutoff")
    oldest_exposure = recovery.exposure(oldest) - cutoff_exposure
    target = cutoff_exposure + oldest_exposure * alpha ** (-1.0 / n_horizons)
    synthetic = np.array([cutoff, oldest])
    result = _result(target, recovery, confidence, synthetic, "known_cutoff")
    return EndpointBound(result.bound_ma, result.status, confidence, n_horizons, oldest, cutoff,
                         result.target_exposure, result.exposure_cap, result.domain_max_ma,
                         "known_cutoff")


def observed_range_bound(
    ages_ma: np.ndarray,
    recovery: PiecewiseRecovery,
    confidence: float = 0.95,
) -> EndpointBound:
    """Strauss-Sadler/Marshall one-endpoint bound after recovery-exposure transformation."""
    ages = _ages(ages_ma, recovery)
    alpha = _confidence(confidence)
    if len(ages) < 2:
        value = float(ages[0]) if len(ages) else float("nan")
        return EndpointBound(float("nan"), "undefined", confidence, len(ages), value, value,
                             float("nan"), recovery.exposure_cap, float(recovery.edges_ma[-1]),
                             "observed_range")
    exposure = recovery.exposure(ages)
    youngest, oldest = float(exposure.min()), float(exposure.max())
    if oldest == youngest:
        value = float(ages[0])
        return EndpointBound(float("nan"), "undefined", confidence, len(ages), value, value,
                             float("nan"), recovery.exposure_cap, float(recovery.edges_ma[-1]),
                             "observed_range")
    target = youngest + (oldest - youngest) * alpha ** (-1.0 / (len(ages) - 1))
    return _result(target, recovery, confidence, ages, "observed_range")
