# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Graphical abstract, also the two-page brief's figure: clock ancestors against the oldest fossils.

Every number is read from the frozen or reviewed tables behind the main figures, except the published clock
intervals and maxima, which figures.py takes from docs/primer.md §5.3. Set in Lato from TeX Live (found with
kpsewhich), so the drawing reproduces on any machine with TeX Live.
"""

import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, transforms
from matplotlib.patches import Circle, Ellipse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import figures as F  # noqa: E402

FRONTIER = ROOT / "models/f3/loop3/out/frontier.csv"
RESULTS = ROOT / "models/f3/out/m2_results.csv"
INPUTS = [FRONTIER, RESULTS, Path(__file__)]

INK, MUTED = "#2b2b2a", "#6b6a64"
CLOCK = {"Morris et al. 2018": "#2a78d6", "Harris et al. 2022": "#eb6834", "Hooper et al. 2026": "#187b56"}
ROCK, ROCK_LIGHT, ROCK_PALE, MESSAGE = "#6e5a3c", "#c9b48f", "#f1e8d6", "#104281"
PERIODS = {"Cambrian": "#d3dfc3", "Ordovician": "#bfe0d4", "Silurian": "#ddefdc", "Devonian": "#ecd8bb"}
X0, X1 = 524, 398
W, H = 6.54, 4.35


def lato():
    folder = Path(subprocess.run(["kpsewhich", "Lato-Regular.ttf"], capture_output=True, text=True,
                                 check=True).stdout.strip()).parent
    for style in ("Regular", "Bold", "Italic", "Semibold", "Medium"):
        font_manager.fontManager.addfont(str(folder / f"Lato-{style}.ttf"))
    return {"font.family": "Lato", "font.size": 7.2, "text.color": INK, "pdf.fonttype": 42}


def numbers():
    steady = F.primary_bound("B2", "flat")[0]
    frontier = {float(r["candidate_lineage_ma"]): float(r["later_to_earlier_intensity"]) for r in F.read(FRONTIER)
                if r["reading"] == "main" and r["category"] == "B2" and r["unit_treatment"] == "primary"
                and r["status"] == "contour" and float(r["assumed_diagnostic_delay_myr"]) == 0}
    ages = (444.0, 452.0)
    murzuq = next(r for r in F.read(RESULTS) if r["design"] == "LY-MZ-CU" and r["primary"] == "True"
                  and r["variant"] == "allocation=stage;cluster_k=2.0;material_type=chart-code"
                  and float(r["rho"]) == 1.0)
    units = sorted(float(r["max_ma"]) for r in F.read(F.MEMBERS) if r["reading"] == "main" and r["category"] == "B2"
                   and float(r["min_ma"]) >= float(F.primary_bound("B2", "flat")[2]["cutoff_ma"]))
    assert len(units) == int(F.primary_bound("B2", "flat")[2]["n_guaranteed"]) == 48
    return {"steady": steady, "ratio": [frontier[t] for t in ages], "ages": ages,
            "delay": [t - steady for t in ages], "units": units, "limit": float(murzuq["fstar_H0c_459.1"]),
            "n_old": int(murzuq["n_old"]), "n_ref": int(murzuq["n_ref"]), "k_ref": int(murzuq["k_ref"])}


def pts(ax, x, y):
    """Coordinates in points around a data anchor, so glyphs keep their shape at any aspect or resolution."""
    return transforms.Affine2D().scale(1 / 72) + ax.figure.dpi_scale_trans + \
        transforms.ScaledTranslation(x, y, ax.transData)


def spore(ax, tr):
    ax.add_patch(Circle((0, 0), 5.2, transform=tr, facecolor=ROCK_PALE, edgecolor=ROCK, lw=0.8, zorder=6))
    for dx, dy in ((0, 3.4), (-2.95, -1.7), (2.95, -1.7)):
        ax.plot([0, dx], [0, dy], transform=tr, color=ROCK, lw=0.8, solid_capstyle="round", zorder=7)


def cooksonia(ax, tr):
    for (x0, y0), (x1, y1) in [((0, -9), (0, 0)), ((0, 0), (-4, 5)), ((0, 0), (4, 5)), ((-4, 5), (-6.5, 10)),
                               ((-4, 5), (-1.5, 10)), ((4, 5), (1.5, 10)), ((4, 5), (6.5, 10))]:
        ax.plot([x0, x1], [y0, y1], transform=tr, color=ROCK, lw=0.9, solid_capstyle="round", zorder=6)
    for tip in (-6.5, -1.5, 1.5, 6.5):
        ax.add_patch(Ellipse((tip, 11.3), 3.6, 2.6, transform=tr, facecolor=ROCK_PALE, edgecolor=ROCK, lw=0.7,
                             zorder=7))


def bar(ax, old, young, y, colour, lw, myr_per_pt, **kw):
    """A rounded bar whose caps end exactly at the interval's ends."""
    inset = lw / 2 * myr_per_pt
    ax.plot([old - inset, young + inset], [y, y], color=colour, lw=lw, solid_capstyle="round", **kw)


def draw(path):
    with plt.rc_context(lato()):
        _draw(path, numbers())


def _draw(path, n):
    fig = plt.figure(figsize=(W, H))
    left, right = 0.015, 0.985
    ax = fig.add_axes([left, 0.01, right - left, 0.855])
    ax.set_xlim(X0, X1)
    ax.set_ylim(1.15, 10.0)
    ax.axis("off")
    myr_per_pt = (X0 - X1) / (W * (right - left) * 72)

    fig.text(left, 0.975, "Older dates for living land plants fit the fossil record if early plants were found"
             "\nseveral times less often, or recognisable features evolved later.", fontsize=10, weight="bold",
             color=MESSAGE, va="top", linespacing=1.2)

    def maximum(m, y0, y1, label, ha, y_label):
        ax.plot([m, m], [y0, y1], color=INK, lw=0.6, ls=(0, (3, 2.5)), zorder=2)
        ax.text(m + (0.6 if ha == "right" else -0.6), y_label, label, fontsize=6.3, color=MUTED, ha=ha,
                va="center")

    def lineage(y, ancestor, possible, certain):
        ax.plot([ancestor, possible], [y, y], color=ROCK_LIGHT, lw=0.8, zorder=3)
        ax.plot(ancestor, y, "o", ms=3.6, mfc="white", mec=ROCK_LIGHT, mew=0.9, zorder=5)
        bar(ax, possible, certain, y, ROCK_LIGHT, 5.5, myr_per_pt, zorder=4, solid_joinstyle="round")
        ax.plot([certain, X1], [y, y], color=ROCK, lw=5.5, solid_capstyle="butt", zorder=4)

    def clocks(group, y_top):
        for i, (name, old, young) in enumerate(F.CLOCKS[group]):
            bar(ax, old, young, y_top - i * 0.3, CLOCK[name], 4.6, myr_per_pt, zorder=4)

    # Lane 1: all living land plants
    y1 = 7.75
    spore(ax, pts(ax, X0 - 2.0, 9.72))
    ax.text(X0 - 5.4, 9.72, "Ancestor of all living land plants", fontsize=8.4, weight="bold", va="center")
    clocks("embryophyta", 9.2)
    (m_old, _), (m_spore, _) = F.MAXIMA["embryophyta"]
    maximum(m_old, y1 - 0.25, 9.4, "", "right", 0)
    ax.text(m_old - 0.8, y1 - 0.42, f"{m_old:g} Ma maximum, argued from\nspores absent in older marine rocks",
            fontsize=6.3, color=MUTED, ha="left", va="top", linespacing=1.15)
    maximum(m_spore, y1 - 0.62, 9.4, f"{m_spore:g} Ma maximum", "right", y1 - 0.45)
    possible, certain = F.spore_first("cryptospore")
    lineage(y1, max(o for _, o, _ in F.CLOCKS["embryophyta"]), possible, certain)
    ax.text(possible + 0.8, y1 + 0.3, "oldest land-plant spores", fontsize=6.6, color=ROCK, ha="right", va="center")

    base = F.stage_base("Rhuddanian")
    for k in range(n["n_old"]):
        c, r = divmod(k, 4)
        ax.add_patch(Circle((-4.5 - c * 3.6, -r * 3.6), 1.25, transform=pts(ax, base, y1 - 0.45),
                            facecolor="white", edgecolor=ROCK, lw=0.6, zorder=5))
    for k in range(n["n_ref"]):
        c, r = divmod(k, 4)
        filled = k < n["k_ref"]
        ax.add_patch(Circle((4.5 + c * 3.6, -r * 3.6), 1.25, transform=pts(ax, base, y1 - 0.45),
                            facecolor=ROCK if filled else "white", edgecolor=ROCK, lw=0.6, zorder=5))
    ax.text(base + 4.2, y1 - 1.0, f"none of {n['n_old']} older samples", fontsize=6.3, color=ROCK, ha="right",
            va="top")
    ax.text(base - 0.6, y1 - 1.0, f"three-rayed (trilete) spores in {n['k_ref']} of {n['n_ref']} younger samples", fontsize=6.3,
            color=ROCK, ha="left", va="top")
    ax.text(474, y1 - 1.33, f"Libyan boreholes: a steady flow of spores into these rocks since {m_spore:g} Ma fits"
            " only\nbelow about a tenth of the later flow, as from rarer or more distant plants, or poorer delivery.",
            fontsize=6.4, ha="left", va="top", linespacing=1.2)

    # Lane 2: living vascular plants
    y2 = 3.5
    cooksonia(ax, pts(ax, X0 - 2.6, 5.52))
    title = ax.text(X0 - 5.4, 5.55, "Ancestor of living vascular plants", fontsize=8.4, weight="bold", va="center")
    ax.annotate("clubmosses, ferns and seed plants", xy=(1, 0.5), xycoords=title, xytext=(5, 0),
                textcoords="offset points", fontsize=7, color=MUTED, va="center")
    clocks("tracheophyta", 5.05)
    (m_vasc, _), = F.MAXIMA["tracheophyta"]
    maximum(m_vasc, y2 - 0.25, 5.3, f"{m_vasc:g} Ma maximum", "right", 5.3)
    ancestor = max(o for _, o, _ in F.CLOCKS["tracheophyta"])
    possible, certain = F.body_first("B2")
    lineage(y2, ancestor, possible, certain)
    counts = {}
    for u in n["units"]:
        counts[u] = counts.get(u, 0) + 1
    for age, k in counts.items():
        for j in range(k):
            c, r = j % 2, j // 2
            ax.add_patch(Circle(((c - 0.5) * 3.2, 5.6 + r * 3.2), 1.25, transform=pts(ax, age, y2),
                                facecolor=ROCK, edgecolor="none", zorder=5))
    ax.text(X1 + 0.3, 5.15, f"each dot: one of {len(n['units'])} dated\ngroups of vascular-plant fossils", fontsize=6.4,
            color=ROCK, ha="right", va="top", linespacing=1.15)
    ax.plot(n["steady"], y2 - 0.36, marker="^", ms=4.2, color=INK, zorder=6)
    ax.text(n["steady"] - 1.4, y2 - 0.28, f"if found at a steady rate,\nthe record starts no earlier\nthan"
            f" {n['steady']:.1f} Ma (95% limit)", fontsize=6.3, color=INK, ha="left", va="top", linespacing=1.15)

    lo, hi = n["ratio"]
    d0, d1 = n["delay"]
    a0, a1 = n["ages"]
    ax.text((ancestor + possible) / 2, y2 + 0.12, f"① found {lo:.0f}–{hi:.0f}× less often", fontsize=6.9,
            color=MESSAGE, ha="center", va="bottom", weight="bold", zorder=6,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.6})
    yb = y2 - 1.0
    ax.annotate("", xy=(n["steady"], yb), xytext=(a1, yb),
                arrowprops={"arrowstyle": "<->", "color": MESSAGE, "lw": 0.8, "shrinkA": 0, "shrinkB": 0})
    ax.plot([a0, a0], [yb - 0.12, yb + 0.12], color=MESSAGE, lw=0.8)
    ax.text((a1 + n["steady"]) / 2, yb - 0.14, f"② recognisable at least {d0:.0f}–{d1:.0f} Myr later",
            fontsize=6.9, color=MESSAGE, ha="center", va="top", weight="bold")
    tx = X0 - 2.2
    ax.text(tx, 4.75, f"The older clock dates ({a0:.0f}–{a1:.0f} Ma) fit if early vascular plants were",
            fontsize=7.4, color=MESSAGE, va="top")
    ax.text(tx, 4.25, f"①  found {lo:.0f}–{hi:.0f}× less often before their oldest fossil, or",
            fontsize=7.4, color=MESSAGE, weight="semibold", va="top")
    ax.text(tx, 3.8, f"②  recognisable at least {d0:.0f}–{d1:.0f} million years after their ancestor.",
            fontsize=7.4, color=MESSAGE, weight="semibold", va="top")
    ax.text(tx, 3.25, "Both are what the fossil record requires, not estimates of how common the plants were.",
            fontsize=6.6, color=MUTED, va="top")

    bases = {}
    for r in F.read(F.TIMESCALE):
        bases[r["period"]] = max(bases.get(r["period"], 0), float(r["base_ma"]))
    order = list(PERIODS)
    for i, p in enumerate(order):
        old = min(bases[p], X0)
        young = max(bases[order[i + 1]] if i + 1 < len(order) else X1, X1)
        ax.fill_between([old, young], 1.55, 1.9, color=PERIODS[p], lw=0)
        ax.text((old + young) / 2, 1.725, p, fontsize=6.6, ha="center", va="center")
    for t in range(500, X1 - 1, -20):
        ax.plot([t, t], [1.55, 1.45], color=MUTED, lw=0.5)
        ax.text(t, 1.38, f"{t}", fontsize=6.3, ha="center", va="top", color=MUTED)
    ax.text(X0, 1.38, "million years ago", fontsize=6.3, ha="left", va="top", color=MUTED)

    lx = 446.5
    ax.text(lx, 9.72, "Molecular-clock estimates", fontsize=6.6, color=MUTED, va="center")
    for i, name in enumerate(CLOCK):
        y = 9.37 - i * 0.27
        bar(ax, lx, lx - 4, y, CLOCK[name], 4.6, myr_per_pt)
        ax.text(lx - 5.5, y, name, fontsize=6.4, va="center")
    y = 9.37 - 3 * 0.27
    ax.plot([lx, lx - 4], [y, y], color=ROCK, lw=5.5, solid_capstyle="butt")
    ax.text(lx - 5.5, y, "fossil record", fontsize=6.4, va="center")
    y -= 0.27
    ax.plot([lx, lx - 4], [y, y], color=ROCK_LIGHT, lw=0.8)
    ax.plot(lx, y, "o", ms=3.6, mfc="white", mec=ROCK_LIGHT, mew=0.9)
    ax.text(lx - 5.5, y, "clock ancestor, no fossils yet", fontsize=6.4, va="center")
    y -= 0.27
    ax.plot([lx - 2, lx - 2], [y - 0.11, y + 0.11], color=INK, lw=0.6, ls=(0, (2, 1.5)))
    ax.text(lx - 5.5, y, "fossil maximum used by a clock", fontsize=6.4, va="center")

    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=300,
                    metadata={"CreationDate": None, "ModDate": None} if ext == "pdf" else None)
    plt.close(fig)


if __name__ == "__main__":
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "figures" / "graphical_abstract")
