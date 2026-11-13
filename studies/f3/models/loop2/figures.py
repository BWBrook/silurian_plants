# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Render the labelled Loop 2 sensitivity figures from the recorded CSVs."""

import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def read(name):
    with (OUT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "savefig.dpi": 180})
    rows = [r for r in read("engine_sensitivity.csv") if float(r["rho"]) == 1]
    labels = [r["case"].replace("omit-", "Omit ").replace("ages-", "Ages: ")
              .replace("allocation-pre459", "Hawaz pre-459.1") for r in rows]
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.8), sharey=True, layout="constrained")
    y = np.arange(len(rows))
    axs[0].scatter([float(r["fstar_H0"]) for r in rows], y, label="Flexible history H0", color="#125e83")
    axs[0].scatter([float(r["fstar_H0c"]) for r in rows], y, label="Constant history H0c", marker="s", color="#b34e1f")
    axs[0].set_yticks(y, labels)
    axs[0].invert_yaxis()
    axs[0].set_xlabel("Relative intensity limit at 459.1 Ma")
    axs[0].set_title("A  Intensity comparison")
    axs[0].legend(loc="lower right", fontsize=8)
    axs[1].scatter([float(r["window_1"]) for r in rows], y, color="#125e83")
    axs[1].axvline(462.6, color="0.6", linestyle=":")
    axs[1].set_xlabel("Reference-level window endpoint (Ma)")
    axs[1].set_title("B  Persistent reference-level window")
    for ax in axs:
        ax.grid(axis="y", color="0.92")
        ax.set_axisbelow(True)
    fig.suptitle("Murzuq: well influence and age assumptions at equal delivery\nUnqualified sensitivity calculations; baseline reproduces frozen results", fontsize=12)
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"engine_influence.{ext}")
    plt.close(fig)

    grid = read("contamination_grid.csv")
    chronologies = ["independent-uniform", "shared-quantile-0.1", "shared-quantile-0.5", "shared-quantile-0.9"]
    kappas = [0.0, 0.1, 1.0]
    gs = [0.1, 0.25, 0.5, 0.75, 1.0]
    rhos = [0.1, 0.25, 0.5, 1.0]
    states = {"not-rejected-by-comparison": 0, "rejected-by-comparison": 1, "model-conflict": 2}
    colours = ["#e4edf0", "#126183", "#df9d62"]
    cmap = ListedColormap(colours)
    norm = BoundaryNorm([-.5, .5, 1.5, 2.5], cmap.N)
    fig, axs = plt.subplots(3, 4, figsize=(10.4, 7.2), layout="constrained", sharex=True, sharey=True)
    selected = [r for r in grid if r["allocation"] == "stage" and r["target"] == "window462.6" and float(r["f"]) == 1]
    for i, kappa in enumerate(kappas):
        for j, chronology in enumerate(chronologies):
            ax = axs[i, j]
            lookup = {(float(r["rho"]), float(r["g"])): states[r["comparison_status"]] for r in selected
                      if float(r["kappa"]) == kappa and r["chronology"] == chronology}
            z = np.array([[lookup[rho, g] for g in gs] for rho in rhos])
            ax.imshow(z, origin="lower", cmap=cmap, norm=norm, aspect="auto")
            ax.set_xticks(range(len(gs)), gs)
            ax.set_yticks(range(len(rhos)), rhos)
            if i == 0:
                ax.set_title(["Independent uniform ages", "Shared 10% ages", "Shared 50% ages", "Shared 90% ages"][j], fontsize=10)
            if j == 0:
                ax.set_ylabel(f"κ = {kappa:g}\nDelivery ratio ρ")
            if i == 2:
                ax.set_xlabel("Indigenous reference fraction g")
    fig.suptitle("Murzuq 459.1–462.6 Ma window: joint assumption sensitivity\nConstant indigenous intensity f = 1; stage allocation; comparison convention only", fontsize=12)
    fig.legend(handles=[Patch(color=c, label=l) for c, l in zip(colours,
               ["Not rejected by comparison", "Rejected by comparison", "Contamination model conflict"])],
               loc="outside lower center", ncol=3, frameon=False, fontsize=9)
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"joint_window_sensitivity.{ext}")
    plt.close(fig)
    paths = [Path(__file__), OUT / "engine_sensitivity.csv", OUT / "contamination_grid.csv"]
    outputs = [OUT / f"{stem}.{ext}" for stem in ("engine_influence", "joint_window_sensitivity") for ext in ("png", "pdf")]
    record = {"status": "illustration-of-unqualified-sensitivities", "matplotlib": matplotlib.__version__,
              "inputs": {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              "outputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}}
    (OUT / "figures.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
