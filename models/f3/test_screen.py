import itertools
import math

import pytest

import screen


def test_profiled_statistic_never_exceeds_the_known_rate_bound_the_screen_uses():
    for k, n, m, f in itertools.product((1, 3, 7, 20), (20, 31, 200), (1, 3, 34), (0.01, 0.1, 1.0)):
        if k < n:
            assert screen.profile_lr(k, n, m, f) <= 2 * m * f * screen.rate(k, n) + 1e-12
    k, n, m = 2000, 10000, 5
    assert screen.profile_lr(k, n, m, 1.0) == pytest.approx(2 * m * screen.rate(k, n), rel=1e-3)
    assert screen.profile_lr(0, 30, 34, 1.0) == 0.0


def test_older_units_needed_inverts_the_known_rate_bound():
    for p, f in ((0.1, 1.0), (0.3, 0.1)):
        m = screen.older_units_needed(p, f)
        assert 2 * m * f * -math.log(1 - p) == pytest.approx(screen.CRIT)
