# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Paper and supplement figures from the reviewed Loop 3 outputs."""

import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "out"
CATEGORIES = [("B0", "Embryophyte bodies"), ("B1", "Polysporangiophyte bodies"), ("B2", "Crown-tracheophyte members")]
HISTORIES = ["flat", "pbdb_all", "pbdb_plant_excluded", "decline25", "decline10", "pbdb_excluded_decline10"]
LABELS = ["Constant", "PBDB density", "Plant-filter matches removed", "Decline into past: 25 Myr",
          "Decline into past: 10 Myr", "Plant-excluded PBDB × decline"]
REGIONS = {"Laurentia": "#355f8d", "Avalonia": "#1f968b", "Baltica": "#73b761",
           "peri-Gondwana-Europe": "#d39435", "Kazakhstania": "#9254a2", "South-China": "#cf5f57",
           "Gondwana-Australia-Antarctica": "#586bb0", "Gondwana-South-America": "#a27653",
           "Tarim": "#b18aab", "unknown": "#8a8a8a", "multiple": "#b0b0b0"}


def read(name):
    return list(csv.DictReader(open(OUT / name)))


def primary(r):
    return r["reading"] == "main" and r["units"] == "locality_age" and r["variant"] == "primary" and not r["excluded_region"] and r["cutoff"] == "Emsian"


def save(fig, name):
    fig.savefig(OUT / (name + ".png"), dpi=220)
    fig.savefig(OUT / (name + ".pdf"))
    plt.close(fig)


def main_figure():
    bounds = [r for r in read("reviewed_bounds.csv") if primary(r)]
    suppression = [r for r in read("suppression_sensitivity.csv") if r["reading"] == "main" and r["baseline"] == "flat" and float(r["break_ma"]) == 426.7]
    units = [r for r in read("primary_unit_membership.csv") if r["reading"] == "main"]
    fig, axes = plt.subplots(3, 2, figsize=(12, 10), gridspec_kw={"width_ratios": [1.12, 1]}, layout="constrained")
    for i, (cat, label) in enumerate(CATEGORIES):
        a, b = axes[i]
        r = sorted([r for r in units if r["category"] == cat and float(r["max_ma"]) >= 413.02],
                   key=lambda r: (r["region"], -float(r["max_ma"])))
        for y, row in enumerate(r):
            a.plot([float(row["min_ma"]), float(row["max_ma"])], [y, y],
                   color=REGIONS.get(row["region"], "#888888"), lw=1.8)
        a.set_xlim(447, 392)
        a.set_ylim(-2, len(r) + 1)
        a.set_yticks([])
        a.set_title(f"{label}\n{len(r)} units with age support extending beyond 413 Ma", fontsize=10, loc="left")
        a.set_xlabel("Reported age support (Ma)")
        for y, (history, lab) in enumerate(zip(HISTORIES, LABELS)):
            if y < 4:
                row = next(x for x in bounds if x["category"] == cat and x["history"] == history)
            else:
                row = next(x for x in suppression if x["category"] == cat and float(x["older_multiplier"]) == (.1 if y == 4 else .01))
            colour = "#1d6782" if y < 3 else ("#b4642d" if y == 3 else "#9254a2")
            if row["status"] in ("bounded", "at_boundary"):
                value = float(row["older_bound_ma"])
                b.plot(value, y, "o" if y < 4 else "^", color=colour, ms=6)
                b.annotate(f"{value:.1f}", (value, y), xytext=(5, 0), textcoords="offset points", va="center", fontsize=8)
            else:
                b.annotate("", xy=(469.4, y), xytext=(463, y), arrowprops={"arrowstyle": "->", "color": colour, "lw": 1.5})
                b.text(462, y, "no bound", ha="right", va="center", fontsize=8, color=colour)
        if cat == "B0":
            b.axvline(458.2, color="#734f0c", ls=":", lw=1.2)
            b.text(458.7, 2.4, "Spore minimum, 458.2 Ma", rotation=90, ha="left", va="center", fontsize=8, color="#734f0c")
        if cat == "B2":
            b.axvspan(428, 432, color="#72ab7c", alpha=.2)
            b.axvspan(447, 452, color="#72ab7c", alpha=.2)
            b.axvline(431.2, color="#a03939", ls="--", lw=1)
            b.text(430, 5.6, "Hooper", ha="center", va="top", fontsize=8, color="#3f7448")
            b.text(449.5, 5.6, "Harris", ha="center", va="top", fontsize=8, color="#3f7448")
        b.set_yticks(range(6), LABELS[:4] + ["Pre-Ludlow recovery × 0.1 †", "Pre-Ludlow recovery × 0.01 †"], fontsize=8)
        b.set_ylim(6.2, -.7)
        b.set_xlim(419, 473)
        b.set_xlabel("Conditional older bound (Ma; older →)")
        n = next(x for x in bounds if x["category"] == cat)
        b.set_title(f"Conservative ages; {n['n_guaranteed']} guaranteed / {n['n_possible']} possible units", fontsize=9)
        for ax in (a, b):
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(axis="x", color=".92", lw=.5)
    handles = [Line2D([0], [0], color=c, lw=2, label=region.replace("Gondwana-", "G.-")) for region, c in REGIONS.items()
               if any(r["region"] == region for r in units)]
    fig.legend(handles=handles, loc="outside lower center", ncol=4, fontsize=7.5, frameon=False)
    fig.suptitle("Body-fossil timing depends on recovery assumptions\nMain reading; recoverable-process endpoints. † Retrospective sensitivity, break at 426.7 Ma", fontsize=12)
    save(fig, "fig_macro_recovery")


def sensitivity_figure():
    rows = [r for r in read("reviewed_bounds.csv") if r["category"] == "B2" and r["reading"] == "main" and r["cutoff"] == "Emsian"]
    def label(r):
        if r["excluded_region"]:
            return "Omit " + r["excluded_region"].replace("Gondwana-", "G.-")
        if r["variant"] != "primary":
            return r["variant"].replace("_", " ")
        return r["units"].replace("_", " ")
    names = list(dict.fromkeys(label(r) for r in rows))
    matrix = np.full((len(names), len(HISTORIES)), np.nan)
    for r in rows:
        if r["older_bound_ma"]:
            matrix[names.index(label(r)), HISTORIES.index(r["history"])] = float(r["older_bound_ma"])
    fig, ax = plt.subplots(figsize=(10, max(6, .36 * len(names))), layout="constrained")
    cmap = plt.get_cmap("YlGnBu").copy(); cmap.set_bad("#e6e6e6")
    im = ax.imshow(np.ma.masked_invalid(matrix), aspect="auto", cmap=cmap, vmin=425, vmax=469.4)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            ax.text(j, i, f"{value:.1f}" if np.isfinite(value) else "> domain", ha="center", va="center", fontsize=8,
                    color="white" if np.isfinite(value) and value > 449 else "#222222")
    ax.set_yticks(range(len(names)), names, fontsize=8)
    ax.set_xticks(range(6), ["Constant", "PBDB", "Plant-excluded\nPBDB", "25 Myr\ndecline", "10 Myr\ndecline", "PBDB ×\n10 Myr decline"], fontsize=8)
    ax.set_title("Crown-member endpoint: unit, source and geographic sensitivity\nConservative age ranges; > domain = no bound through 469.4 Ma", fontsize=11)
    fig.colorbar(im, ax=ax, shrink=.7, label="Conditional older bound (Ma)")
    save(fig, "fig_macro_sensitivity")


def suppression_figure():
    rows = [r for r in read("suppression_sensitivity.csv") if r["category"] == "B2" and r["reading"] == "main"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), layout="constrained", sharey=True)
    for ax, baseline in zip(axes, ["flat", "pbdb_all"]):
        for i, (break_ma, colour) in enumerate([(419.62, "#1d6782"), (426.7, "#9254a2"), (432.9, "#b4642d")]):
            rr = sorted([r for r in rows if r["baseline"] == baseline and float(r["break_ma"]) == break_ma],
                        key=lambda r: -float(r["older_multiplier"]))
            values = [float(r["older_bound_ma"]) if r["older_bound_ma"] else np.nan for r in rr]
            xx = np.arange(4) + (i-1)*.08
            ax.plot(xx, values, "o-", color=colour, label=f"Before {break_ma:g} Ma")
            for j, r in enumerate(rr):
                if r["status"] == "beyond_domain":
                    ax.annotate("", xy=(xx[j], 470), xytext=(xx[j], 465), arrowprops={"arrowstyle": "->", "color": colour})
        ax.set_xticks(range(4), ["1", "0.5", "0.1", "0.01"])
        ax.set_xlabel("Multiplier applied to older recovery")
        ax.set_title("Constant baseline" if baseline == "flat" else "PBDB density baseline")
        ax.set_ylim(425, 472)
        ax.axhline(469.4, color=".6", ls=":", lw=1)
        ax.axhspan(447, 452, color="#72ab7c", alpha=.15)
        ax.grid(axis="y", color=".92")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Sensitivity older bound (Ma)")
    axes[1].legend(loc="lower right", frameon=False, fontsize=8)
    fig.suptitle("Recovery before the oldest crown-member record is not identified\nComplete stage-break grid; retrospective sensitivity, not selection-adjusted confidence", fontsize=11)
    save(fig, "fig_macro_suppression")


def main():
    inputs = [OUT / p for p in ("reviewed_bounds.csv", "primary_unit_membership.csv", "suppression_sensitivity.csv")]
    inputs += [ROOT / "docs/primer.md", ROOT / "data/spores/first_appearances.csv", Path(__file__).resolve()]
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    main_figure(); sensitivity_figure(); suppression_figure()
    if hashes != {str(p.relative_to(ROOT)): sha(p) for p in inputs}:
        raise RuntimeError("figure input drift")
    outputs = [OUT / (stem + ext) for stem in ("fig_macro_recovery", "fig_macro_sensitivity", "fig_macro_suppression") for ext in (".png", ".pdf")]
    (OUT / "figure_receipt.json").write_text(json.dumps({"inputs": hashes,
        "outputs": {str(p.relative_to(ROOT)): sha(p) for p in outputs}, "matplotlib": matplotlib.__version__}, indent=2) + "\n")


if __name__ == "__main__":
    main()
