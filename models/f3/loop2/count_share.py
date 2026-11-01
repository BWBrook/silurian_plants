"""Protocol-limited relative-count share bounds for the Loop 2 count gate.

This module does not apply the model to QSIM or Murzuq.  It supplies the small
mathematical method that can be used only when target and control counts share
a documented effective effort.  ``h`` is target effort divided by control
effort.  Under independent Poisson sampling, conditioning on the observed total
gives a binomial target share; the recovered rate ratio is the binomial odds
divided by ``h``.  Producer output still requires the declared relative
delivery/recovery assumption contained in ``h``.

If the effective effort can be zero, the relative output is unidentified and
the returned upper bound is the vacuous bound 1 (infinite rate ratio).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import brentq
from scipy.stats import beta


@dataclass(frozen=True)
class ShareBound:
    """One-sided upper bound and its status for a target/control count pair."""

    target_count: int
    control_count: int
    alpha: float
    effort_ratio: float
    share_upper: float
    rate_ratio_upper: float
    biological_share_upper: float
    status: str


def _integer(value: object, name: str) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer count")
    value = int(value)
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def _alpha(alpha: float) -> float:
    if isinstance(alpha, (bool, np.bool_)) or not isinstance(alpha, (int, float, np.integer, np.floating)):
        raise TypeError("alpha must be a finite number in (0, 1)")
    alpha = float(alpha)
    if not math.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be a finite number in (0, 1)")
    return alpha


def _effort(value: float, name: str = "effort_ratio", *, allow_zero: bool = True) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise TypeError(f"{name} must be a finite non-negative number")
    value = float(value)
    if not math.isfinite(value) or value < 0.0 or (not allow_zero and value == 0.0):
        raise ValueError(f"{name} must be a finite {'positive' if not allow_zero else 'non-negative'} number")
    return value


def _odds(share: float) -> float:
    if share >= 1.0:
        return math.inf
    return share / (1.0 - share)


def common_effort_bound(target_count: int, control_count: int, effort_ratio: float,
                        alpha: float = 0.05) -> ShareBound:
    """Return a one-sided exact Clopper--Pearson upper bound.

    ``target_count`` and ``control_count`` are counts from the same documented
    effective sampling effort.  ``effort_ratio = e_target/e_control`` must be
    positive for a finite rate-ratio bound.  A zero or empty control effort is
    explicitly represented as unidentified.
    """
    t = _integer(target_count, "target_count")
    c = _integer(control_count, "control_count")
    h = _effort(effort_ratio, allow_zero=True)
    a = _alpha(alpha)
    n = t + c
    if n == 0 or h == 0.0:
        return ShareBound(t, c, a, h, 1.0, math.inf, 1.0, "unidentified-zero-effort")
    if c == 0:
        q = 1.0
    else:
        # Exact one-sided upper CP limit for Binomial(t+c, q).
        q = float(beta.ppf(1.0 - a, t + 1, c))
        q = min(1.0, max(0.0, q))
    theta = _odds(q) / h
    bio = 1.0 if math.isinf(theta) else theta / (1.0 + theta)
    return ShareBound(t, c, a, h, q, theta, bio, "finite" if math.isfinite(theta) else "vacuous-all-target")


def zero_target_stratified_bound(control_counts: Sequence[int], effort_ratios: Sequence[float],
                                 alpha: float = 0.05) -> dict[str, object]:
    """Upper bound on a common rate ratio when every target count is zero.

    For independent strata with observed controls ``C_i`` and known target /
    control effort ratios ``h_i``, the exact zero-target likelihood is
    ``prod_i (1 + h_i*theta)**(-C_i)``.  The returned ``theta_upper`` solves
    its one-sided alpha equation.  If all information is zero, the bound is
    infinite and biological share is one.
    """
    if isinstance(control_counts, (str, bytes)) or isinstance(effort_ratios, (str, bytes)):
        raise TypeError("control_counts and effort_ratios must be numeric sequences")
    counts = [_integer(x, f"control_counts[{i}]") for i, x in enumerate(control_counts)]
    efforts = [_effort(x, f"effort_ratios[{i}]") for i, x in enumerate(effort_ratios)]
    if len(counts) != len(efforts):
        raise ValueError("control_counts and effort_ratios must have equal length")
    a = _alpha(alpha)
    information = sum(c * h for c, h in zip(counts, efforts))
    if not counts or information == 0.0:
        return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
                "theta_upper": math.inf, "biological_share_upper": 1.0,
                "status": "unidentified-zero-effort"}

    target = -math.log(a)

    def equation(theta: float) -> float:
        # log1p keeps the calculation stable at small effort/rate products.
        return sum(c * math.log1p(h * theta) for c, h in zip(counts, efforts)) - target

    hi = 1.0
    while equation(hi) < 0.0:
        hi *= 2.0
        if math.isinf(hi):
            return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
                    "theta_upper": math.inf, "biological_share_upper": 1.0,
                    "status": "numerically-unbounded"}
    theta = float(brentq(equation, 0.0, hi, xtol=1e-13, rtol=1e-14))
    return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
            "theta_upper": theta, "biological_share_upper": theta / (1.0 + theta),
            "status": "finite"}


def validate_zero_inputs(control_counts: Iterable[int], effort_ratios: Iterable[float]) -> None:
    """Validate stratified inputs without calculating a bound."""
    zero_target_stratified_bound(list(control_counts), list(effort_ratios))
