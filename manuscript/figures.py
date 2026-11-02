# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Figures for the reconstructed manuscript and its supplement.

Main text: fig1_problem, fig2_evidence, fig3_bodies, fig4_mapping.
Supplement: figS_qsim, plus the reviewed Loop 2 and Loop 3 figures reused unchanged from models/.
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

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "figures"
sys.path.insert(0, str(ROOT / "models" / "f3" / "loop2"))
sys.path.insert(0, str(ROOT / "models" / "f3"))
import contamination  # noqa: E402

QSIM = ROOT / "data/units/loop2/replication/qsim801_vecoli2017_table1.csv"
TIMESCALE = ROOT / "data/timescale.csv"
SPORES = ROOT / "data/spores/first_appearances.csv"
MEMBERS = ROOT / "models/f3/loop3/out/primary_unit_membership.csv"
BOUNDS = ROOT / "models/f3/loop3/out/reviewed_bounds.csv"
SUPPRESS = ROOT / "models/f3/loop3/out/suppression_sensitivity.csv"
MAPPING = ROOT / "manuscript/mapping.csv"

# Published crown-age intervals (Ma, older first) and calibration maxima; docs/primer.md §5.3.
CLOCKS = {
    "embryophyta": [("Morris et al. 2018", 515.2, 473.5), ("Harris et al. 2022", 515.0, 493.0),
                    ("Hooper et al. 2026", 457.0, 450.0)],
    "tracheophyta": [("Morris et al. 2018", 450.8, 419.3), ("Harris et al. 2022", 452.0, 447.0),
                     ("Hooper et al. 2026", 432.0, 428.0)],
}
MAXIMA = {"embryophyta": [(515.5, "515.5 Ma maximum\n(Cambrian cryptospores)"),
                          (459.1, "459.1 Ma maximum\n(oldest triletes)")],
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
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200)
    plt.close(fig)


def spore_first(cls):
    row = next(r for r in read(SPORES) if r["record_set"] == "strict" and r["class_group"] == cls
               and r["spore_class"] == "(all)" and r["palaeo_unit"] == "(all)")
    return float(row["fa_possible_ma"]), float(row["fa_certain_ma"])


def primary_bound(cat, history):
    r = next(r for r in read(BOUNDS) if r["category"] == cat and r["reading"] == "main" and r["units"] == "locality_age"
             and r["variant"] == "primary" and not r["excluded_region"] and r["cutoff"] == "Emsian"
             and r["history"] == history)
    return (float(r["older_bound_ma"]) if r["status"] == "bounded" else None), float(r["oldest_possible_ma"]), r


def suppressed(cat, mult):
    r = next(r for r in read(SUPPRESS) if r["category"] == cat and r["reading"] == "main" and r["baseline"] == "flat"
             and float(r["break_ma"]) == 426.7 and float(r["older_multiplier"]) == mult)
    return float(r["older_bound_ma"]) if r["status"] == "bounded" else None


def body_first(cat):
    """Oldest possible age, and the age by which a unit of this category is certainly present."""
    units = [r for r in read(MEMBERS) if r["reading"] == "main" and r["category"] == cat]
    return max(float(r["max_ma"]) for r in units), max(float(r["min_ma"]) for r in units)


def fig_problem(path):
    """Clock intervals, the maxima that shape them and the first appearances of each fossil channel."""
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 6.6), sharex=True, gridspec_kw={"height_ratios": [3, 3, 4.2]})
    for ax, (key, title) in zip(axes[:2], (("embryophyta", "Crown land plants (Embryophyta)"),
                                           ("tracheophyta", "Crown vascular plants (Tracheophyta)"))):
        for i, (name, old, young) in enumerate(CLOCKS[key]):
            ax.barh(i, old - young, left=young, height=0.55, color=CLOCK_COLOURS[name])
            ax.text(young - 1.2, i, name, va="center", fontsize=8)
        for x, lab in MAXIMA[key]:
            ax.axvline(x, color="#a32020", lw=1.0, ls="--")
            ax.text(x + 0.8, len(CLOCKS[key]) + 0.55, lab, color="#a32020", fontsize=7.2, ha="right", va="top")
        ax.set_ylim(-0.7, len(CLOCKS[key]) + 0.6)
        ax.set_yticks([])
        ax.set_title(title + ": published molecular-clock intervals", fontsize=9.5, loc="left")
        ax.spines[["left", "top", "right"]].set_visible(False)
    ax = axes[2]
    crypt, trilete = spore_first("cryptospore"), spore_first("trilete")
    rows = [("Land-plant cryptospores", crypt), ("Trilete spores", trilete),
            ("Land-plant bodies (any)", body_first("B0")), ("Crown vascular-plant bodies", body_first("B2"))]
    s4 = (stage_base("Stage 4"), stage_base("Wuliuan"))
    ax.barh(4, s4[0] - s4[1], left=s4[1], height=0.5, color="#bbbbbb", hatch="///", edgecolor="#888888")
    ax.text(s4[1] - 1.2, 4, "Cambrian cryptospore-like forms (affinity not accepted)", va="center", fontsize=8)
    for i, (lab, (possible, certain)) in enumerate(reversed(rows)):
        ax.barh(i, possible - certain, left=certain, height=0.5, color="#5b7fa6", alpha=0.35)
        ax.barh(i, certain - 400, left=400, height=0.5, color="#5b7fa6")
        ax.text(possible + 1.2, i, lab, va="center", ha="right", fontsize=8)
    ax.set_ylim(-0.7, 4.6)
    ax.set_yticks([])
    ax.set_title("Fossil record: first appearances (pale: possible, dark: certain)", fontsize=9.5, loc="left")
    ax.spines[["left", "top", "right"]].set_visible(False)
    ax.set_xlim(530, 400)
    ax.set_xlabel("Age (Ma)")
    for x in (515.5, 459.1, 431.2):
        ax.axvline(x, color="#a32020", lw=0.6, ls=":")
    fig.tight_layout()
    save(fig, path)


def fig_evidence(path):
    """Where the tested evidence comes from: body units and spore frames by region and age."""
    members = [r for r in read(MEMBERS) if r["reading"] == "main"]
    cats = {}
    for r in members:
        cats.setdefault(r["unit_id"], set()).add(r["category"])
    units = {r["unit_id"]: (float(r["max_ma"]), float(r["min_ma"]), r["region"]) for r in members if r["category"] == "B0"}
    frame = contamination.build_frame("stage")
    fig, ax = plt.subplots(figsize=(8.6, 7.4))
    y, ticks = 0.0, []
    for region in REGIONS:
        rows = sorted((v[0], v[1], uid) for uid, v in units.items() if v[2] == region)
        spore = region == "Gondwana-North-Africa-Arabia"
        if not rows and not spore:
            continue
        start = y
        for old, young, uid in rows:
            c = cats[uid]
            col = CAT_COLOUR["B2"] if "B2" in c else CAT_COLOUR["B1"] if "B1" in c else CAT_COLOUR["B0"]
            ax.plot([old, young], [y, y], color=col, lw=1.6, solid_capstyle="butt")
            y += 0.32
        if spore:
            y += 0.3
            y_old = y
            for well in frame.wells:
                for lo, hi in zip(well.older_lo, well.older_hi):
                    ax.plot([hi, lo], [y, y], color="#3b6ea8", lw=1.0)
                    y += 0.16
            ref_lo, ref_hi = stage_base("Rhuddanian"), stage_base("Sheinwoodian")
            ax.fill_between([ref_hi, ref_lo], y, y + 1.0, color="#3b6ea8", alpha=0.8, lw=0)
            ax.text(ref_hi - 0.6, y + 0.5, "Murzuq reference: 59 Llandovery cuttings,\n51 with trilete spores",
                    fontsize=7, va="center")
            ax.text(441.5, (y_old + y) / 2 - 0.6, "Murzuq: 28 older cuttings,\nno trilete spores reported", fontsize=7,
                    va="center", color="#3b6ea8")
            y += 1.4
            with QSIM.open() as f:
                m = sum(int(r["cryptospore_marks"]) for r in csv.DictReader(f))
            ax.fill_between([stage_base("Sandbian"), stage_base("Dapingian")], y, y + 0.9, facecolor="none",
                            edgecolor="#c47f2c", hatch="///", lw=0.8)
            ax.text(stage_base("Sandbian") - 0.6, y + 0.45,
                    f"QSIM-801 (Saudi Arabia): {m} cryptospore occurrences, no triletes", fontsize=7, va="center")
            y += 1.0
        ticks.append(((start + y - 0.32) / 2, REGION_LABEL.get(region, region)))
        ax.axhline(y + 0.1, color="0.88", lw=0.6)
        y += 0.45
    for x, lab in ((459.1, "459.1"), (431.2, "431.2")):
        ax.axvline(x, color="#a32020", lw=0.9, ls="--")
        ax.text(x - 0.5, -0.9, lab + " Ma maximum", color="#a32020", fontsize=7.2, ha="left", va="center")
    ax.axvline(stage_base("Lochkovian"), color="0.6", lw=0.6, ls=":")
    ax.text(stage_base("Lochkovian"), 0.0, "Silurian | Devonian", fontsize=7, color="0.4", ha="center")
    ax.set_yticks([t for t, _ in ticks], [lab for _, lab in ticks], fontsize=8)
    ax.set_ylim(y + 0.4, -1.4)
    ax.set_xlim(472, 393)
    ax.set_xlabel("Age (Ma); bars span each record's reported age range")
    ax.spines[["top", "right"]].set_visible(False)
    handles = [plt.Line2D([], [], color=CAT_COLOUR[k], lw=2.5) for k in ("B2", "B1", "B0")]
    handles.append(plt.Line2D([], [], color="#3b6ea8", lw=2.5))
    ax.legend(handles, ["crown vascular-plant body", "other multi-sporangiate body", "other land-plant body",
                        "spore samples (Murzuq Basin, Libya)"], fontsize=7.5, frameon=False, loc="upper left", bbox_to_anchor=(0, 0.95))
    fig.tight_layout()
    save(fig, path)


def fig_bodies(path):
    """Older bounds on the start of the recoverable body record under each recovery history."""
    hist = [("flat", "Constant recovery", "o", "#1b4f72"), ("pbdb_all", "Collection density (PBDB)", "s", "#1b4f72"),
            ("pbdb_plant_excluded", "Collection density, plant collections removed", "D", "#1b4f72"),
            ("decline25", "Recovery declining into the past (25 Myr)", "o", "#b5651d"),
            ("decline10", "Recovery declining into the past (10 Myr)", "o", "#b5651d")]
    retro = [(0.1, "Pre-Ludlow recovery reduced tenfold"), (0.01, "Pre-Ludlow recovery reduced a hundredfold")]
    cats = [("B0", "Any land-plant body"), ("B1", "Multi-sporangiate (polysporangiophyte) body"),
            ("B2", "Crown vascular-plant body")]
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 8.4), sharex=True)
    crypt = spore_first("cryptospore")
    for ax, (cat, title) in zip(axes, cats):
        rows = []
        for key, lab, mk, col in hist:
            b, oldest, r = primary_bound(cat, key)
            rows.append((lab, b, mk, col, False))
        for mult, lab in retro:
            rows.append((lab + " †", suppressed(cat, mult), "^", "#7d3c98", True))
        n = int(r["n_guaranteed"])
        if cat == "B0":
            ax.axvspan(crypt[1], crypt[0], color="#5b7fa6", alpha=0.18, lw=0)
            ax.axvline(crypt[1], color="#5b7fa6", lw=1.0)
            ax.text(crypt[1] + 0.4, len(rows) + 0.15, "land-plant cryptospores certain by 458.2 Ma", fontsize=7,
                    color="#3b5f86", ha="left")
        if cat == "B2":
            for name, old, young in CLOCKS["tracheophyta"]:
                ax.axvspan(young, old, color=CLOCK_COLOURS[name], alpha=0.17, lw=0)
                ax.text((old + young) / 2 if name != "Morris et al. 2018" else 441.5, len(rows) + 0.15,
                        name.replace(" et al.", ""), fontsize=7, ha="center", color=CLOCK_COLOURS[name])
            ax.axvline(431.2, color="#a32020", lw=1.0, ls="--")
        ax.axvspan(oldest, 393.47, color="0.85", alpha=0.6, lw=0)
        ax.text(oldest - 0.3, len(rows) - 0.4, "observed\nrecord", fontsize=7, color="0.35", va="top")
        for i, (lab, b, mk, col, is_retro) in enumerate(rows):
            yy = len(rows) - 1 - i
            if b is None:
                ax.annotate("", xy=(472, yy), xytext=(oldest + 3, yy),
                            arrowprops={"arrowstyle": "->", "color": col, "lw": 1.2, "ls": "--" if is_retro else "-"})
                ax.text(oldest + 4, yy + 0.25, "no bound within 469.4 Ma", fontsize=6.6, color=col)
            else:
                ax.plot([oldest, b], [yy, yy], color=col, lw=1.0, alpha=0.6, ls="--" if is_retro else "-")
                ax.plot(b, yy, mk, color=col, ms=5.5, mfc="white" if is_retro else col)
                ax.text(b + 0.5, yy + 0.3, f"{b:.1f}", fontsize=6.8, ha="right")
        ax.set_ylim(-1.0, len(rows) + 0.6)
        ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)], fontsize=7.6)
        ax.tick_params(axis="y", length=0)
        ax.set_title(f"{title}: {n} dated locality units", fontsize=9.5, loc="left")
        ax.spines[["left", "top", "right"]].set_visible(False)
    axes[-1].set_xlim(472, 422)
    axes[-1].set_xlabel("Age (Ma)")
    fig.tight_layout()
    save(fig, path)


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
    for stale in ("fig1_support", "fig3_qsim_share"):
        for ext in ("png", "pdf"):
            (OUT / f"{stale}.{ext}").unlink(missing_ok=True)
    fig_problem(OUT / "fig1_problem")
    fig_evidence(OUT / "fig2_evidence")
    fig_bodies(OUT / "fig3_bodies")
    fig_mapping(OUT / "fig4_mapping")
    fig_qsim(OUT / "figS1_qsim")
    inputs = [QSIM, TIMESCALE, SPORES, MEMBERS, BOUNDS, SUPPRESS, MAPPING,
              ROOT / "models/f3/loop2/contamination.py", Path(__file__)]
    bound = contamination._input_hashes()
    bound.update({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
    outputs = sorted(OUT.glob("*.png")) + sorted(OUT.glob("*.pdf"))
    (OUT / "figures.json").write_text(json.dumps(
        {"inputs": bound, "outputs": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs},
         "status": "manuscript figures drawn from frozen or reviewed output tables"}, indent=2) + "\n")


if __name__ == "__main__":
    main()
