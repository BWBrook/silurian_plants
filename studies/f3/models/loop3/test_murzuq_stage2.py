import numpy as np

import murzuq_stage2 as mz


def test_only_ten_dated_cuttings_have_possible_pre_maximum_support():
    u = mz.units()
    assert u.possible_pre_459_1.sum() == 10
    assert u.wholly_post_459_1.sum() == 18
    assert set(u[u.possible_pre_459_1].cluster) == {"D1-200", "H2-NC186"}
    assert np.isclose(u.loc[u.possible_pre_459_1, "exposure_459_1"].sum(), 10 * .9 / 11.2)


def test_block_weights_count_each_stage_well_phase_once():
    u = mz.units()
    u["weight"] = mz.block_weights(u, "well_stage_support")
    sums = u.groupby(["cluster", "old", "oldest_stage", "youngest_stage"]).weight.sum()
    assert np.allclose(sums, 1.)
    assert np.all(u.weight > 0)


def test_independent_arithmetic_reproduces_qualified_constant_readout():
    result = mz.fit(mz.units())
    assert abs(result["rho_f_contour"] - .09103) < .00001
    separate = mz.fit(mz.units(), frailty=np.inf, separate=True)
    assert abs(separate["rho_f_contour"] - .099513) < .00001
