"""Estimators of a clade's origination age from the ages of its fossil records.

Ages are Ma, decreasing towards the present. The first appearance is the oldest record, and the
true origination is at least that old, so every bound extends to older ages. All estimators take
an array of record ages (last axis) and return an Interval of the same leading shape, so a batch
of resampled age sets runs in one call. Too few records (none, or fewer than two) give NaN.

Sources (see README.md): Marshall (1990) and Strauss & Sadler (1989) classical intervals, read
in PAST's manual and tbea's source; Bradshaw et al. (2012) GRIWM, read in the paper and the
authors' Rextinct code.
"""

from typing import Callable, NamedTuple

import numpy as np

UNIT_MA = 0.001  # the discrete time step of McInerny's sighting rate (the "+1 year" of the GRIWM code)
LOWER_Q, UPPER_Q = 0.025, 0.975


class Interval(NamedTuple):
    """Lower end, point estimate and upper end of the origination age; all older than the oldest
    record except `lo` of the classical intervals, which is the oldest record itself."""

    lo: np.ndarray | float
    point: np.ndarray | float
    hi: np.ndarray | float


def _undefined(ages: np.ndarray) -> Interval:
    nan = np.full(ages.shape[:-1], np.nan) if ages.ndim > 1 else np.nan
    return Interval(nan, nan, nan)


def oldest(ages: np.ndarray) -> Interval:
    """The naive estimate: origination at the oldest record."""
    if ages.shape[-1] < 1:
        return _undefined(ages)
    first = ages.max(axis=-1)
    return Interval(first, first, first)


def range_extension(n_records: int, conf: float) -> float:
    """Classical extension of the observed range, as a fraction of its length, that holds the
    true endpoint with probability `conf` when horizons are uniform over the true range."""
    return (1.0 - conf) ** (-1.0 / (n_records - 1)) - 1.0


def marshall_1990(ages: np.ndarray, conf: float = 0.95) -> Interval:
    """Marshall's classical interval on the first appearance. The source gives an interval, not a
    point estimate, so `point` is the oldest record."""
    if ages.shape[-1] < 2:
        return _undefined(ages)
    first = ages.max(axis=-1)
    span = first - ages.min(axis=-1)
    return Interval(first, first, first + range_extension(ages.shape[-1], conf) * span)


def strauss_sadler_1989(ages: np.ndarray, conf: float = 0.95) -> Interval:
    """Strauss & Sadler's one-parameter bound (the same interval as Marshall's single endpoint).
    The point estimate is the 50% bound, the median of the endpoint under the model, following
    Saltre et al. (2015), who took median estimates at alpha = 0.5."""
    if ages.shape[-1] < 2:
        return _undefined(ages)
    first = ages.max(axis=-1)
    span = first - ages.min(axis=-1)
    h = ages.shape[-1]
    return Interval(first, first + range_extension(h, 0.5) * span, first + range_extension(h, conf) * span)


def weighted_mcinerny(ages: np.ndarray, alpha: float = 0.05, unit: float = UNIT_MA) -> Interval:
    """Inverse-weighted McInerny estimate of the first appearance (one set of dates, no resampling).

    Takes the m oldest records for m = 2..n. For each series, the estimate lies beyond the oldest
    record by (span + unit) * (-ln alpha) / m, where span is the age range of the m records. Series
    are weighted by 1 / span, so those reaching further from the oldest record count less.
    This is the extinction algorithm of Bradshaw et al. (2012) on a mirrored age axis. Series with
    zero span get zero weight. lo = point = hi."""
    n = ages.shape[-1]
    if n < 2:
        return _undefined(ages)
    a = -np.sort(-ages, axis=-1)
    span = a[..., :1] - a[..., 1:]
    series_len = np.arange(2, n + 1)
    estimate = a[..., :1] + (span + unit) * (-np.log(alpha)) / series_len
    weight = np.where(span > 0, 1.0 / np.where(span > 0, span, 1.0), 0.0)
    total = weight.sum(axis=-1)
    point = np.where(total > 0, (weight * estimate).sum(axis=-1) / np.where(total > 0, total, 1.0), np.nan)
    return Interval(point, point, point)


def griwm(
    ages: np.ndarray,
    sd: np.ndarray | float,
    rng: np.random.Generator,
    alpha: float = 0.05,
    n_resample: int = 10_000,
    unit: float = UNIT_MA,
) -> Interval:
    """Gaussian-resampled, inverse-weighted McInerny estimate (GRIWM) of the first appearance.

    Each record age is redrawn from a normal with its own sd, weighted_mcinerny is recomputed for
    each draw, and the 2.5%, 50% and 97.5% quantiles of the draws are the interval and point."""
    if ages.shape[-1] < 2:
        return _undefined(ages)
    draws = rng.normal(ages, sd, size=(n_resample, ages.shape[-1]))
    return _pool(weighted_mcinerny(draws, alpha, unit))


def _pool(draws: Interval) -> Interval:
    return Interval(
        np.quantile(draws.lo, LOWER_Q),
        np.median(draws.point),
        np.quantile(draws.hi, UPPER_Q),
    )


def stage_resampled(
    estimator: Callable[[np.ndarray], Interval],
    young: np.ndarray,
    old: np.ndarray,
    rng: np.random.Generator,
    n_draws: int = 500,
) -> Interval:
    """Estimate from records dated only to stage ranges [young, old] (Ma, per record).

    Each record's age is drawn uniformly within its stage, `estimator` is applied to every draw,
    and the draws are pooled: lo and hi are the 2.5% quantile of the draws' lo and the 97.5%
    quantile of their hi, and the point is the median of their points."""
    if len(old) < 2:
        return _undefined(np.asarray(old))
    return _pool(estimator(rng.uniform(young, old, size=(n_draws, len(old)))))
