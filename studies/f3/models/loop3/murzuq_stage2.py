# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "scipy", "matplotlib"]
# ///
"""Local time support and retrospective dependence sensitivities for Murzuq."""

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize, special

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent / "out" / "stage2_murzuq"
CRITICAL = -2 * np.log(.05)


def units():
    u = pd.read_csv(ROOT / "studies/f3/models/out/m2_units.csv")
    u = u[(u.design == "LY-MZ-CU") &
          (u.variant == "allocation=stage;material_type=chart-code") &
          u.excluded.isna() & u.d.notna()].copy()
    scale = pd.read_csv(ROOT / "data/timescale.csv")
    base = dict(zip(scale.stage, scale.base_ma))
    top = dict(zip(scale.stage, scale.base_ma.shift(1)))
    u["min_ma"] = u.youngest_stage.map(top)
    u["max_ma"] = u.oldest_stage.map(base)
    u["old"] = u.transported.astype(bool)
    u["exposure_459_1"] = np.where(u.old, np.clip(
        (np.minimum(u.max_ma, 459.1) - np.maximum(u.min_ma, 443.1)) /
        (u.max_ma - u.min_ma), 0, 1), 1.)
    u["possible_pre_459_1"] = u.old & (u.max_ma > 459.1)
    u["wholly_post_459_1"] = u.old & (u.max_ma < 459.1)
    if len(u) != 87 or u.old.sum() != 28 or u.loc[~u.old, "d"].sum() != 51:
        raise ValueError("primary frame changed; re-adjudicate the stage 2 check")
    return u


def block_weights(u, grouping):
    if grouping == "independent":
        return np.ones(len(u))
    keys = ["cluster", "old"]
    if grouping == "well_formation":
        keys += ["formation"]
    elif grouping == "well_stage_support":
        keys += ["oldest_stage", "youngest_stage"]
    else:
        raise ValueError(grouping)
    return 1. / u.groupby(keys, dropna=False).unit_id.transform("size").to_numpy()


def fit(u, grouping="independent", frailty=2., separate=False):
    u = u.copy()
    u["weight"] = block_weights(u, grouping)
    if np.isinf(frailty):
        nodes, logweights = np.array([1.]), np.array([0.])
    else:
        z, w = special.roots_genlaguerre(128, frailty - 1.)
        nodes, logweights = z / frailty, np.log(w) - special.gammaln(frailty)

    def well_ll(rows, rate, f):
        r = rate * nodes
        old = rows[rows.old]
        ref = rows[~rows.old]
        positives = np.sum(ref.weight * ref.d)
        negatives = np.sum(ref.weight * (1 - ref.d))
        ll = positives * np.log(-np.expm1(-r)) - negatives * r
        for q, weight in zip(old.exposure_459_1, old.weight):
            if q == 1:
                ll -= weight * r * f
            elif q > 0:
                ll += weight * np.logaddexp(np.log1p(-q), np.log(q) - r * f)
        return special.logsumexp(logweights + ll)

    wells = [rows for _, rows in u.groupby("cluster")]

    def profile(f):
        groups = [[r] for r in wells] if separate else [wells]
        total = 0.
        for rows in groups:
            result = optimize.minimize_scalar(
                lambda x: -sum(well_ll(r, np.exp(x), f) for r in rows),
                bounds=(-15, np.log(1000 if separate else 8)), method="bounded",
                options={"xatol": 1e-10})
            if not result.success:
                raise RuntimeError(result.message)
            total -= result.fun
        return total

    alt = profile(0.)
    lr = lambda f: 2 * (alt - profile(f))
    upper = 1.
    while lr(upper) < CRITICAL and upper < 1024:
        upper *= 2
    limit = optimize.brentq(lambda f: lr(f) - CRITICAL, 0, upper) if upper < 1024 else np.nan
    return {"grouping": grouping, "frailty_shape": str(frailty), "separate_well_rates": separate,
            "n_reference": int((~u.old).sum()), "n_older": int(u.old.sum()),
            "effective_reference_weight": u.loc[~u.old, "weight"].sum(),
            "effective_older_weight": u.loc[u.old, "weight"].sum(),
            "rho_f_contour": limit, "lr_at_f1": lr(1.), "critical": CRITICAL,
            "scope": "retrospective unqualified sensitivity; block weights give a composite likelihood"}


def panel(u):
    fig, ax = plt.subplots(figsize=(9, 5.5), constrained_layout=True)
    labels = []
    for well, rows in u.groupby("cluster", sort=True):
        for row in rows.sort_values("depth").itertuples():
            y = len(labels)
            color = "#0072B2" if row.d else "#D55E00"
            ax.plot([row.min_ma, row.max_ma], [y, y], color=color, lw=1.3)
            labels.append((well, y))
    ticks = [(name, np.mean([y for w, y in labels if w == name])) for name in dict(labels)]
    ax.set_yticks([x[1] for x in ticks], [x[0] for x in ticks])
    ax.axvline(459.1, color="black", ls="--", label="459.1 Ma maximum")
    ax.plot([], [], color="#0072B2", label="trilete reported")
    ax.plot([], [], color="#D55E00", label="no trilete reported")
    ax.set_xlim(469.4, u.min_ma.min() - .5)
    ax.set_xlabel("Age support (Ma); full stage enclosure, not a point date")
    ax.set_ylabel("Well; samples ordered by depth within well")
    ax.legend(loc="upper left", fontsize=8)
    for suffix in ("png", "pdf"):
        fig.savefig(OUT / f"time_by_well.{suffix}", dpi=180)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    u = units()
    u.to_csv(OUT / "sample_time_support.csv", index=False)
    summary = u[u.old].groupby(["cluster", "formation", "oldest_stage", "youngest_stage"]).agg(
        n=("unit_id", "size"), possible_pre=("possible_pre_459_1", "sum"),
        wholly_post=("wholly_post_459_1", "sum"), uniform_exposure=("exposure_459_1", "sum")).reset_index()
    summary.to_csv(OUT / "older_support_summary.csv", index=False)
    rows = [fit(u), fit(u, frailty=np.inf), fit(u, frailty=np.inf, separate=True)]
    rows += [fit(u, grouping=g) for g in ("well_formation", "well_stage_support")]
    for well in sorted(u.cluster.unique()):
        r = fit(u[u.cluster != well]);r["excluded_well"] = well;rows.append(r)
    pd.DataFrame(rows).to_csv(OUT / "dependence_sensitivity.csv", index=False)
    panel(u)
    paths = [ROOT / "studies/f3/models/out/m2_units.csv", ROOT / "data/timescale.csv", Path(__file__)]
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    receipt = {"inputs": {str(p.relative_to(ROOT)): digest(p) for p in paths},
               "outputs": {str(p.relative_to(ROOT)): digest(p) for p in OUT.glob("*") if p.name != "receipt.json"},
               "age_model": "independent uniform full-stage support for exposure; diagnostic only",
               "block_model": "inverse block-size weights; not a calibrated confidence procedure"}
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(summary.to_string(index=False))
    print(pd.DataFrame(rows)[["grouping", "frailty_shape", "separate_well_rates", "rho_f_contour", "excluded_well"]].to_string(index=False))


if __name__ == "__main__":
    main()
