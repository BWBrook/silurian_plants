# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Profile-likelihood surfaces of origination age T0 against growth rate for one simulated clade.

    uv run models/f3/identifiability.py

Writes out/identifiability_surface_<T0>.png for an origination in the Telychian (435 Ma) and one in the
Darriwilian (460 Ma). Each simulates one realisation (real effort; 100 expected spore records and 30
body records) under logistic growth and under birth-death growth, and fits each by the matching ramp
model on spores alone, bodies alone, and both channels. Rows: the log-likelihood below its maximum over
(T0, rate), with psi profiled out, and the contour of the 95% joint region; the one-dimensional profile
for T0 with its 95% level; and the psi that the best rate implies at each T0, the old-origin,
poor-preservation against young-origin, good-preservation trade-off. Where the region runs to the left
edge, the data do not bound T0 from above.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

import inputs
import ramp
import recovery
import sim

OUT = Path(__file__).resolve().parent / "out"
ORIGINATIONS = (435.0, 460.0)
SEED = 20261030
TARGETS = recovery.LEVELS["mid"]
TRUTHS = {
    "logistic": (sim.Logistic(r=0.3, k=100), ramp.Logistic(100.0), 0.3),
    "birth-death": (sim.BirthDeath(lam=0.25, mu=0.15), ramp.ExpectedBirthDeath(), 0.10),
}
CHANNEL_SETS = {"spores": [0], "bodies": [1], "joint": [0, 1]}
JOINT_LEVEL = 0.5 * stats.chi2.ppf(0.95, 2)
SHADES = [0.0, ramp.PROFILE_LEVEL, JOINT_LEVEL, 5.0, 10.0, 20.0, 40.0]


def simulate_counts(
    growth: sim.Growth, t0: float, series: inputs.EffortSeries, ts: sim.Timescale, effort: np.ndarray
) -> np.ndarray:
    first = ts.index(inputs.YOUNGEST)
    ab = sim.simulate_abundance(growth, t0, float(series.edges[0]), sim.child_seed(SEED, 0))
    mass = sim.stage_exposure(ab, ts)[first : first + len(series.stages)]
    psi = recovery.psi_for_targets(effort, mass, TARGETS)
    channels = {
        name: sim.Channel(psi[c], dict(zip(series.stages, effort[c].tolist()))) for c, name in enumerate(("spores", "bodies"))
    }
    records = sim.simulate_records(ab, channels, ts, sim.child_seed(SEED, 1))
    return np.array([np.bincount(records[name].stage - first, minlength=len(series.stages)) for name in ("spores", "bodies")])


def implied_psi(model: ramp.RampModel, n: np.ndarray, effort: np.ndarray) -> np.ndarray:
    """psi of each channel at each T0, at the rate that maximises the likelihood there: (T0, channel)."""
    surface = model.surface(n, effort)
    best = surface.argmax(axis=1)
    mass = model.mass[np.arange(len(best)), best]
    psi = n.sum(axis=1)[None, :] / (mass @ effort.T)
    return np.where(np.isfinite(surface.max(axis=1))[:, None], psi, np.nan)


def figure(t0_true: float, ts: sim.Timescale, series: inputs.EffortSeries, effort: np.ndarray) -> Path:
    fig, axes = plt.subplots(4, 3, figsize=(12.5, 15), constrained_layout=True)
    fits: dict[str, dict[str, ramp.Fit]] = {}
    for row, (name, (growth, family, true_rate)) in enumerate(TRUTHS.items()):
        counts = simulate_counts(growth, t0_true, series, ts, effort)
        model = ramp.RampModel(series.edges, family)
        rates = model.params["rate"]
        keep = rates > 0
        fits[name] = {}
        for col, (label, idx) in enumerate(CHANNEL_SETS.items()):
            n, e = counts[idx], effort[idx]
            fit = ramp.fit(model, n, e)
            fits[name][label] = fit
            drop = np.where(np.isfinite(fit.loglik - model.surface(n, e)), fit.loglik - model.surface(n, e), 1e3)[:, keep]
            ax = axes[row, col]
            filled = ax.contourf(model.t0_grid, rates[keep], drop.T, levels=SHADES, cmap="viridis_r", extend="max")
            ax.contour(model.t0_grid, rates[keep], drop.T, levels=[JOINT_LEVEL], colors="black", linewidths=1.2)
            ax.plot(t0_true, true_rate, marker="*", color="red", markersize=14, markeredgecolor="white", linestyle="none", label="truth")
            ax.plot(fit.t0, fit.params["rate"], marker="o", color="white", markeredgecolor="black", linestyle="none", label="maximum")
            ax.set(yscale="log", xlim=(ramp.T0_MAX, t0_true - 25), xlabel="origination T0 (Ma)", ylabel="growth rate (per Myr)")
            state = "bounded" if fit.bounded else "unbounded"
            ax.set_title(f"{name} growth, {label}: {int(n.sum())} records\n95% for T0: {fit.lo:.1f} to {fit.hi:.1f} Ma ({state})", fontsize=10)
            if row == 0 and col == 0:
                ax.legend(loc="lower left", fontsize=8)
        fits[name]["counts"] = counts
        fits[name]["model"] = model
    fig.colorbar(filled, ax=axes[:2, :], shrink=0.5, label="log-likelihood below the maximum (contour: 95% joint region)")
    for col, (label, idx) in enumerate(CHANNEL_SETS.items()):
        ax_profile, ax_psi = axes[2, col], axes[3, col]
        for (name, style), colour in zip(zip(TRUTHS, ("-", "--")), ("tab:blue", "tab:orange")):
            fit, model, counts = fits[name][label], fits[name]["model"], fits[name]["counts"]
            ax_profile.plot(fit.t0_grid, np.maximum(fit.profile - fit.loglik, -12.0), style, color=colour, label=f"{name} fit")
            psi = implied_psi(model, counts[idx], effort[idx])
            inside = fit.profile >= fit.loglik - ramp.PROFILE_LEVEL
            for c, channel in enumerate(idx):
                ax_psi.plot(fit.t0_grid, psi[:, c], style, color=colour, linewidth=0.8, alpha=0.5)
                ax_psi.plot(fit.t0_grid[inside], psi[inside, c], style, color=colour, linewidth=2.2, label=f"{name}, {('spores', 'bodies')[channel]}")
        ax_profile.axhline(-ramp.PROFILE_LEVEL, color="black", linewidth=0.8)
        ax_profile.axvline(t0_true, color="red", linewidth=1.0)
        ax_profile.set(xlim=(ramp.T0_MAX, t0_true - 25), ylim=(-12.0, 0.5), xlabel="origination T0 (Ma)", ylabel="profile log-likelihood minus maximum")
        ax_profile.set_title(f"profile for T0, {label}", fontsize=10)
        ax_psi.axvline(t0_true, color="red", linewidth=1.0)
        ax_psi.set(yscale="log", xlim=(ramp.T0_MAX, t0_true - 25), xlabel="origination T0 (Ma)", ylabel="implied psi (records per lineage per Myr)")
        ax_psi.set_title(f"implied preservation psi, {label}", fontsize=10)
        if col == 0:
            ax_profile.legend(fontsize=8, loc="lower left")
        ax_psi.legend(fontsize=7, loc="lower right")
    fig.suptitle(f"Origination against growth rate: one clade originating {t0_true:g} Ma, real effort, {TARGETS[0]} spore and {TARGETS[1]} body records expected\n(bottom row: thick lines lie inside the 95% interval for T0)", fontsize=12)
    path = OUT / f"identifiability_surface_{t0_true:g}.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    for name, by_set in fits.items():
        for label in CHANNEL_SETS:
            f = by_set[label]
            print(f"T0 {t0_true:g} {name:12s} {label:7s} max T0 {f.t0:.1f} rate {f.params['rate']:.3f} 95% [{f.lo:.1f}, {f.hi:.1f}] bounded={f.bounded}")
    return path


def main() -> None:
    ts = sim.Timescale.load()
    series = inputs.effort_series(timescale=ts)
    effort = recovery.context().effort["real"]
    OUT.mkdir(exist_ok=True)
    for t0 in ORIGINATIONS:
        print(f"-> {figure(t0, ts, series, effort)}")


if __name__ == "__main__":
    main()
