import itertools
import math

import pytest

import screen
import test_envelope as te


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


@pytest.mark.parametrize("n", [17, 31])
def test_in_its_homogeneous_design_the_screen_equals_the_engine_at_each_ceiling_and_is_never_weaker_below(n):
    """Codex's 7/17 and 7/31 Borenshult-like designs: the engine's class statistic at the ceiling is the constant
    history's, and below it the class's wider null set can only lower it."""
    rows = [("Sandbian", "Sandbian", 0, j, int(j < 7)) for j in range(n)]
    rows += [("Darriwilian", "Darriwilian", 0, 100 + j, 0) for j in range(3)]
    pr = te.problem(rows, nodes=128, h1_ceiling=3.0)
    T = float(te.AGE.base[te.I("Darriwilian")])
    for cls, C in screen.CEILINGS.items():
        assert pr.lr(cls, T, C).value == pytest.approx(screen.profile_lr(7, n, 3, C), rel=1e-9)
        for f in (0.25, 0.5, 0.9 * C):
            assert pr.lr(cls, T, f).value <= screen.profile_lr(7, n, 3, f) + 1e-9
        bound = pr.fstar(cls, T)
        _, profiled = screen.smallest_excludable(7, n, 3, C)
        assert (bound.state == "ceiling-limited") == math.isinf(profiled)
        if bound.state == "finite":
            assert profiled <= bound.value + 1e-9


def test_screen_domains_are_explicit():
    with pytest.raises(ValueError):
        screen.rate(0, 0)
    with pytest.raises(ValueError):
        screen.smallest_excludable(0, 0, 3)
    assert screen.smallest_excludable(0, 17, 3) == (math.inf, math.inf)
    assert screen.smallest_excludable(7, 17, 0) == (math.inf, math.inf)
    assert screen.smallest_excludable(7, 17, 3, 1.0) == (math.inf, math.inf)
    known, profiled = screen.smallest_excludable(7, 17, 3, 3.0)
    assert 1 < known < profiled < 3
