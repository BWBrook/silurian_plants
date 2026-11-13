"""Protocol-limited relative-count share bounds for the Loop 2 count gate.

This module does not apply the model to QSIM or Murzuq.  It supplies the small
mathematical method that can be used only when target and control counts share
a documented effective effort.  ``h`` is target effort divided by control
effort.  Under independent Poisson sampling, conditioning on the observed total
gives a binomial target share; the recovered rate ratio is the binomial odds
divided by ``h``.  Producer output still requires the declared relative
delivery/recovery assumption contained in ``h``.

If the effective effort is known to be zero, or its unknown allowed set reaches
zero, the relative output is unidentified and the returned upper bound is the
vacuous bound 1 (infinite rate ratio).  The latter is represented by ``None``
in the scalar API; it is not the same claim as observing a known zero effort.
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
    effort_ratio: float | None
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


def common_effort_bound(target_count: int, control_count: int, effort_ratio: float | None,
                        alpha: float = 0.05) -> ShareBound:
    """Return a one-sided exact Clopper--Pearson upper bound.

    ``target_count`` and ``control_count`` are counts from the same documented
    effective sampling effort.  ``effort_ratio = e_target/e_control`` must be
    positive for a finite rate-ratio bound.  A known zero effort is explicitly
    represented as ``0``.  Pass ``None`` when the effort is unknown and its
    allowed set reaches zero; taking the supremum over that allowed set is also
    vacuous, but is reported with a distinct status.
    """
    t = _integer(target_count, "target_count")
    c = _integer(control_count, "control_count")
    h = None if effort_ratio is None else _effort(effort_ratio, allow_zero=True)
    a = _alpha(alpha)
    n = t + c
    if h is None:
        return ShareBound(t, c, a, h, 1.0, math.inf, 1.0,
                          "unidentified-unknown-effort-includes-zero")
    if n == 0:
        return ShareBound(t, c, a, h, 1.0, math.inf, 1.0, "unidentified-no-counts")
    if h == 0.0:
        if t > 0:
            raise ValueError("positive target count is impossible with known zero target effort")
        return ShareBound(t, c, a, h, 1.0, math.inf, 1.0, "unidentified-known-zero-effort")
    if c == 0:
        q = 1.0
    else:
        # Exact one-sided upper CP limit for Binomial(t+c, q).
        q = float(beta.ppf(1.0 - a, t + 1, c))
        q = min(1.0, max(0.0, q))
    theta = _odds(q) / h
    bio = 1.0 if math.isinf(theta) else theta / (1.0 + theta)
    return ShareBound(t, c, a, h, q, theta, bio, "finite" if math.isfinite(theta) else "vacuous-all-target")


def zero_target_stratified_bound(control_counts: Sequence[int], effort_ratios: Sequence[float | None],
                                 alpha: float = 0.05) -> dict[str, object]:
    """Upper bound on a common rate ratio when every target count is zero.

    For independent strata with observed controls ``C_i`` and fixed, known
    target/control effort ratios ``h_i``, condition on each stratum's observed
    total ``N_i = C_i``.  With a common rate ratio ``theta``, the conditional
    target count is binomial, so the joint zero-target probability is
    ``prod_i (1 + h_i*theta)**(-C_i)``.  The returned ``theta_upper`` solves
    its one-sided alpha equation.  A known ``h_i=0`` contributes no information;
    ``None`` means that stratum's unknown allowed set reaches zero and is
    conservatively treated as no information.  If all information is zero, the
    bound is infinite and biological share is one.
    """
    if isinstance(control_counts, (str, bytes)) or isinstance(effort_ratios, (str, bytes)):
        raise TypeError("control_counts and effort_ratios must be numeric sequences")
    counts = [_integer(x, f"control_counts[{i}]") for i, x in enumerate(control_counts)]
    efforts = [None if x is None else _effort(x, f"effort_ratios[{i}]")
               for i, x in enumerate(effort_ratios)]
    if len(counts) != len(efforts):
        raise ValueError("control_counts and effort_ratios must have equal length")
    a = _alpha(alpha)
    positive = [(c, h) for c, h in zip(counts, efforts)
                if c > 0 and h is not None and h > 0.0]
    if not positive:
        return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
                "theta_upper": math.inf, "biological_share_upper": 1.0,
                "status": "unidentified-no-known-positive-effort"}

    target = -math.log(a)
    # Solve for x = theta * max(h_i).  An absolute tolerance on theta is
    # unusable when the effective effort is large; x stays on an O(1) scale.
    scale = max(h for _, h in positive)
    scaled = [(c, h / scale) for c, h in positive]

    def equation(x: float) -> float:
        # log1p keeps the calculation stable at small effort/rate products.
        return sum(c * math.log1p(ratio * x) for c, ratio in scaled) - target

    hi = 1.0
    while equation(hi) < 0.0:
        hi *= 2.0
        if math.isinf(hi):
            return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
                    "theta_upper": math.inf, "biological_share_upper": 1.0,
                    "status": "numerically-unbounded"}
    x = float(brentq(equation, 0.0, hi, xtol=5e-324, rtol=1e-14))
    theta = x / scale
    if theta == 0.0 and x > 0.0:
        # Preserve an upper bound when the mathematical answer is positive but
        # below the smallest representable float.
        theta = math.nextafter(0.0, 1.0)
    if not math.isfinite(theta):
        return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
                "theta_upper": math.inf, "biological_share_upper": 1.0,
                "status": "numerically-unbounded"}
    return {"control_counts": counts, "effort_ratios": efforts, "alpha": a,
            "theta_upper": theta, "biological_share_upper": theta / (1.0 + theta),
            "status": "finite"}


def validate_zero_inputs(control_counts: Iterable[int], effort_ratios: Iterable[float | None]) -> None:
    """Validate stratified inputs without calculating a bound."""
    zero_target_stratified_bound(list(control_counts), list(effort_ratios))
