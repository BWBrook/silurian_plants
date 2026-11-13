# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Figures for the reconstructed manuscript and its supplement.

Main text, in citation order: fig1_dispute, fig2_bound, fig3_requirements (figures_main.py); figS_murzuq is supplement figure S2.
Graphical abstract, also the brief's figure: graphical_abstract (figures_abstract.py). Supplement: figS2_qsim, figS7_mapping, plus the reviewed Loop 2 and Loop 3 figures reused unchanged from studies/f3/models/.
Every number drawn here is read from a frozen or reviewed output table, never retyped, except the
published clock intervals and calibration maxima, which are taken from docs/primer.md §5.3.
"""

import csv
import hashlib
import json
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "figures"
sys.path.insert(0, str(ROOT / "studies" / "f3" / "models" / "loop2"))
sys.path.insert(0, str(ROOT / "studies" / "f3" / "models"))
import contamination  # noqa: E402

QSIM = ROOT / "studies/f3/data/units/loop2/replication/qsim801_vecoli2017_table1.csv"
TIMESCALE = ROOT / "data/timescale.csv"
SPORES = ROOT / "data/spores/first_appearances.csv"
MEMBERS = ROOT / "studies/f3/models/loop3/out/primary_unit_membership.csv"
BOUNDS = ROOT / "studies/f3/models/loop3/out/reviewed_bounds.csv"
SUPPRESS = ROOT / "studies/f3/models/loop3/out/suppression_sensitivity.csv"
BENTONITE_MA = 454.41
MAPPING = ROOT / "studies/f3/manuscript/mapping.csv"

# Published crown-age intervals (Ma, older first) and calibration maxima; docs/primer.md §5.3.
CLOCKS = {
    "embryophyta": [("Morris et al. 2018", 515.2, 473.5), ("Harris et al. 2022", 515.0, 493.0),
                    ("Hooper et al. 2026", 457.0, 450.0)],
    "tracheophyta": [("Morris et al. 2018", 450.8, 419.3), ("Harris et al. 2022", 452.0, 447.0),
                     ("Hooper et al. 2026", 432.0, 428.0)],
}
MAXIMA = {"embryophyta": [(515.5, "515.5 Ma maximum\n(Cambrian cryptospores)"),
                          (459.1, "459.1 Ma maximum\n(Sandbian base; oldest\npossible trilete)")],
          "tracheophyta": [(431.2, "431.2 Ma maximum\n(Cooksonia-type bodies)")]}
CLOCK_COLOURS = {"Morris et al. 2018": "#9aa9b8", "Harris et al. 2022": "#c98a3a", "Hooper et al. 2026": "#3f7f5f"}
REGIONS = ["Laurentia", "Avalonia", "Baltica", "peri-Gondwana-Europe", "Gondwana-North-Africa-Arabia",
           "Gondwana-South-America", "Gondwana-Australia-Antarctica", "South-China", "Tarim", "Kazakhstania",
           "multiple", "unknown"]
REGION_LABEL = {"peri-Gondwana-Europe": "peri-Gondwanan Europe", "Gondwana-North-Africa-Arabia": "N Africa–Arabia",
                "Gondwana-South-America": "South America", "Gondwana-Australia-Antarctica": "Australia–Antarctica",
                "South-China": "South China", "multiple": "several regions", "unknown": "unassigned"}
CAT_COLOUR = {"B2": "#1f6f4a", "B1": "#7fb069", "B0": "#c9b458"}


def stage_base(name: str) -> float:
    with TIMESCALE.open() as f:
        for row in csv.DictReader(f):
            if row["stage"] == name:
                return float(row["base_ma"])
    raise KeyError(name)


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def save(fig, path):
    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200,
                    metadata={"CreationDate": None, "ModDate": None} if ext == "pdf" else None)
    plt.close(fig)


def spore_first(cls):
    row = next(r for r in read(SPORES) if r["record_set"] == "strict" and r["class_group"] == cls
               and r["spore_class"] == "(all)" and r["palaeo_unit"] == "(all)")
    return float(row["fa_possible_ma"]), float(row["fa_certain_ma"])


def primary_bound(cat, history, variant="primary"):
    r = next(r for r in read(BOUNDS) if r["category"] == cat and r["reading"] == "main" and r["units"] == "locality_age"
             and r["variant"] == variant and not r["excluded_region"] and r["cutoff"] == "Emsian"
             and r["history"] == history)
    return (float(r["older_bound_ma"]) if r["status"] == "bounded" else None), float(r["oldest_possible_ma"]), r


def suppressed(cat, mult):
    r = next(r for r in read(SUPPRESS) if r["category"] == cat and r["reading"] == "main" and r["baseline"] == "flat"
             and float(r["break_ma"]) == 426.7 and float(r["older_multiplier"]) == mult)
    return float(r["older_bound_ma"]) if r["status"] == "bounded" else None


def body_first(cat, exclude_oman=False):
    """Oldest possible age, and the age by which a unit of this category is certainly present."""
    units = [r for r in read(MEMBERS) if r["reading"] == "main" and r["category"] == cat]
    if exclude_oman:
        units = [r for r in units if "tail:S-w22-K12" not in r["member_ids"]]
    return max(float(r["max_ma"]) for r in units), max(float(r["min_ma"]) for r in units)


def fig_mapping(path):
    rows = read(MAPPING)
    cols = [("material", "Observed material"), ("event", "What it is taken to be"),
            ("encounter", "Sampling evidence"), ("persistence", "Trait persistence"),
            ("node", "What it says about the crown node")]
    fig, ax = plt.subplots(figsize=(8.5, 7.8))
    ax.set_xlim(-1.6, 6.35)
    ax.set_ylim(-.65, 5.55)
    ax.axis("off")
    for j, (_, title) in enumerate(cols):
        ax.text(-.15, 4.75-j*1.1, textwrap.fill(title, 15), ha="right", va="center", weight="bold", fontsize=10)
    for i, row in enumerate(rows):
        x = i*2.1
        ax.text(x+.96, 5.4, textwrap.fill(row["maximum"], 24), ha="center", va="center", weight="bold", fontsize=10)
        for j, (key, _) in enumerate(cols):
            y = 4.75-j*1.1
            ax.add_patch(plt.Rectangle((x+.025, y-.45), 1.87, .9, facecolor=["#edf0f2", "#e8f0f5", "#f6ede4"][i],
                                       edgecolor="0.65", linewidth=.65))
            ax.text(x+.96, y, textwrap.fill(row[key], 25), ha="center", va="center", fontsize=9)
            if j < 4:
                ax.annotate("", xy=(x+.96, y-.64), xytext=(x+.96, y-.46), arrowprops={"arrowstyle": "->", "color": "0.5"})
    fig.tight_layout()
    save(fig, path)


def fig_qsim(path):
    with QSIM.open() as f:
        m = sum(int(r["cryptospore_marks"]) for r in csv.DictReader(f))
    theta = np.logspace(-3, 0.6, 400)
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    for h, c in ((1.0, "#1b4f8a"), (0.5, "#3b7dbf"), (0.25, "#77a7d8"), (0.1, "#b5cde8")):
        ax.plot(theta, (1 + h * theta) ** (-m), color=c, lw=1.8, label=f"h = {h}")
        ax.plot([(0.05 ** (-1 / m) - 1) / h], [0.05], "o", color=c, ms=4)
    ax.axhline(0.05, color="#555", lw=0.8, ls=":")
    ax.axvspan(1.0, theta[-1], color="#c47f2c", alpha=0.15)
    ax.text(1.05, 0.5, "floor ≥ 1\nscenario only", fontsize=7.5, va="center")
    ax.set_xscale("log")
    ax.set_xlabel("Persistent trilete : cryptospore floor ψ")
    ax.set_ylabel(f"Upper bound on P(no targets)\n(assumed ≥{m} independent units)")
    ax.set_title("Model-conditional calculation; no empirical qualification", fontsize=10)
    ax.legend(frameon=False, fontsize=8, title="relative recovery", title_fontsize=8)
    fig.tight_layout()
    save(fig, path)


def main():
    OUT.mkdir(exist_ok=True)
    for stale in ("fig1_support", "fig3_qsim_share", "fig2_mapping", "fig3_evidence", "fig4_bodies", "fig4_mapping", "figS1_qsim",
                  "fig1_problem", "fig2_evidence", "fig3_bodies", "fig4_frontier", "figB1_brief", "fig3_murzuq", "fig4_requirements"):
        for ext in ("png", "pdf"):
            (OUT / f"{stale}.{ext}").unlink(missing_ok=True)
    fig_mapping(OUT / "figS7_mapping")
    fig_qsim(OUT / "figS2_qsim")
    import figures_main
    figures_main.draw(OUT)
    import figures_abstract
    figures_abstract.draw(OUT / "graphical_abstract")
    figures_abstract.draw(OUT / "graphical_abstract_journal", headline=False)
    inputs = [QSIM, TIMESCALE, SPORES, MEMBERS, BOUNDS, SUPPRESS, MAPPING,
              ROOT / "studies/f3/models/loop2/contamination.py", Path(__file__), *figures_main.INPUTS,
              *figures_abstract.INPUTS]
    bound = contamination._input_hashes()
    bound.update({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
    outputs = sorted(OUT.glob("*.png")) + sorted(OUT.glob("*.pdf"))
    (OUT / "figures.json").write_text(json.dumps(
        {"inputs": bound, "outputs": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs},
         "status": "manuscript figures drawn from frozen or reviewed output tables"}, indent=2) + "\n")


if __name__ == "__main__":
    main()
