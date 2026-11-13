import sys
from pathlib import Path

import numpy as np
from scipy import integrate

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "models/f3"))

import envelope as ev
import sim
import units_sim as us
import validate as val


def integrated_reference_mean(s, pr, path, spec, age):
    ref = (
        (s.units.old <= pr.s_star)
        & (s.units.young >= pr.s_star - spec.reference_stages + 1)
        & np.isin(s.units.cls, pr.calibrated)
    )
    lo = age.base[s.units.young[ref] - 1]
    hi = age.base[s.units.old[ref]]
    rates = s.r[s.cls_true[ref]]
    means = np.array(
        [
            integrate.quad(
                lambda t: float(path(np.array([t]))[0]),
                float(a),
                float(b),
                epsabs=1e-12,
                epsrel=1e-12,
                limit=300,
            )[0]
            / (b - a)
            for a, b in zip(lo, hi)
        ]
    )
    realised = float(np.sum(rates * path(s.t_true[ref])) / np.sum(rates))
    marginal = float(np.sum(rates * means) / np.sum(rates))
    return realised, marginal


age = ev.AgeModel.load()
cell = next(c for c in val.CELLS if c["name"] == "A12")
truth, design, spec = val.cell_objects(cell)

for rep in (129, 163):
    seed = np.random.SeedSequence(val.ROOT_SEED, spawn_key=(cell["id"], rep))
    s = us.simulate(truth, design, sim.child_seed(seed, 0))
    pr = ev.Problem(s.units, spec, age)
    path = us.effective_path(truth.path(design), truth, design)
    r_true = s.r[pr.calibrated]
    target_true_weights = pr.abar_truth(path, truth.t0, r_true)
    target_plugin_weights = pr.abar_truth(path, truth.t0, pr.r_ref)
    a_ref_realised, a_ref_integrated = integrated_reference_mean(s, pr, path, spec, age)

    print(f"A12 replicate {rep}")
    print(f"  tau={pr.tau:.12g}")
    print(f"  calibrated={pr.calibrated.tolist()}")
    print(f"  true_rates={r_true.tolist()}")
    print(f"  fitted_reference_rates={pr.r_ref.tolist()}")
    print(f"  older_target_true_rate_weights={target_true_weights:.15g}")
    print(f"  older_target_plugin_weights={target_plugin_weights:.15g}")
    print(f"  plugin_over_true_target={target_plugin_weights / target_true_weights:.15g}")
    print(f"  a_ref_realised_latent_ages={a_ref_realised:.15g}")
    print(f"  a_ref_integrated_age_ranges={a_ref_integrated:.15g}")
    print(f"  realised_over_integrated_a_ref={a_ref_realised / a_ref_integrated:.15g}")
    print(f"  validation_target={target_true_weights / a_ref_realised:.15g}")
    print(f"  integrated_true_rate_target={target_true_weights / a_ref_integrated:.15g}")
    print(f"  integrated_plugin_target={target_plugin_weights / a_ref_integrated:.15g}")
