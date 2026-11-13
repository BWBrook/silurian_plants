# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Graphical abstract: clock ancestors against the oldest fossils, with and without the brief's headline.

Every number is read from the frozen or reviewed tables behind the main figures, except the published clock
intervals and maxima, which figures.py takes from docs/primer.md §5.3. Set in Lato from TeX Live (found with
kpsewhich), so the drawing reproduces on any machine with TeX Live. No label is smaller than 7.5 pt at the
printed width of 166 mm (Royal Society figure guidance).
"""

import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, transforms
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import figures as F  # noqa: E402

FRONTIER = ROOT / "models/f3/loop3/out/frontier.csv"
RESULTS = ROOT / "models/f3/out/m2_results.csv"
DEPENDENCE = ROOT / "models/f3/loop3/out/stage2_murzuq/dependence_sensitivity.csv"
INPUTS = [FRONTIER, RESULTS, DEPENDENCE, Path(__file__)]
HEADLINE = ("Older dates for living land plants fit the fossil record if early plants were found\n"
            "several times less often, or recognisable features evolved later.")

INK, MUTED = "#2b2b2a", "#6b6a64"
CLOCK = {"Morris et al. 2018": "#2a78d6", "Harris et al. 2022": "#eb6834", "Hooper et al. 2026": "#187b56"}
ROCK, ROCK_LIGHT, ROCK_PALE, MESSAGE = "#6e5a3c", "#c9b48f", "#f6f0e4", "#104281"
PERIODS = {"Cambrian": "#d3dfc3", "Ordovician": "#bfe0d4", "Silurian": "#ddefdc", "Devonian": "#ecd8bb"}
X0, X1 = 524, 398
W, BODY, HEAD = 6.54, 4.3, 0.5
SMALL, LABEL, TITLE = 7.5, 8.0, 9.0


def lato():
    folder = Path(subprocess.run(["kpsewhich", "Lato-Regular.ttf"], capture_output=True, text=True,
                                 check=True).stdout.strip()).parent
    for style in ("Regular", "Bold", "Italic", "Semibold", "Medium"):
        font_manager.fontManager.addfont(str(folder / f"Lato-{style}.ttf"))
    return {"font.family": "Lato", "font.size": SMALL, "text.color": INK, "pdf.fonttype": 42}


def numbers():
    steady, _, case = F.primary_bound("B2", "flat")
    coarse = sorted(float(r["older_bound_ma"]) for r in F.read(F.BOUNDS)
                    if r["category"] == "B2" and r["reading"] == "main" and r["history"] == "flat"
                    and (r["units"], r["variant"]) in (("region_stage", "primary"), ("locality_age", "curated_tail_only"))
                    and not r["excluded_region"] and r["cutoff"] == "Emsian")
    assert len(coarse) == 2
    ages = (444.0, 452.0)
    ratio = {}
    for r in F.read(FRONTIER):
        if r["reading"] == "main" and r["category"] == "B2" and r["status"] == "contour" \
                and float(r["assumed_diagnostic_delay_myr"]) == 0 and float(r["candidate_lineage_ma"]) in ages:
            ratio.setdefault(r["unit_treatment"], []).append(float(r["later_to_earlier_intensity"]))
    murzuq = next(r for r in F.read(RESULTS) if r["design"] == "LY-MZ-CU" and r["primary"] == "True"
                  and r["variant"] == "allocation=stage;cluster_k=2.0;material_type=chart-code"
                  and float(r["rho"]) == 1.0)
    block = next(float(r["rho_f_contour"]) for r in F.read(DEPENDENCE) if r["grouping"] == "well_formation"
                 and r["frailty_shape"] == "2.0" and r["separate_well_rates"] == "False" and not r["excluded_well"])
    units = sorted(float(r["max_ma"]) for r in F.read(F.MEMBERS) if r["reading"] == "main" and r["category"] == "B2"
                   and float(r["min_ma"]) >= float(case["cutoff_ma"]))
    assert len(units) == int(case["n_guaranteed"]) == 48
    return {"steady": steady, "coarse": coarse, "ages": ages, "ratio": sorted(ratio["primary"]),
            "coarse_ratio": (min(ratio["region_stage"] + ratio["curated"]), max(ratio["region_stage"] + ratio["curated"])),
            "delay": [t - steady for t in ages], "units": units, "limit": float(murzuq["fstar_H0c_459.1"]),
            "block": block, "n_old": int(murzuq["n_old"]), "n_ref": int(murzuq["n_ref"]), "k_ref": int(murzuq["k_ref"])}


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


def draw(path, headline=True):
    with plt.rc_context(lato()):
        _draw(path, numbers(), headline)


def _draw(path, n, headline):
    head = HEAD if headline else 0.05
    H = BODY + head
    fig = plt.figure(figsize=(W, H))
    left, right = 0.015, 0.985
    ax = fig.add_axes([left, 0.01, right - left, (BODY - 0.04) / H])
    ax.set_xlim(X0, X1)
    ax.set_ylim(1.15, 10.0)
    ax.axis("off")
    myr_per_pt = (X0 - X1) / (W * (right - left) * 72)
    if headline:
        fig.text(left, 1 - 0.04 / H, HEADLINE, fontsize=10.5, weight="bold", color=MESSAGE, va="top",
                 linespacing=1.2)

    def maximum(m, y0, y1):
        ax.plot([m, m], [y0, y1], color=INK, lw=0.6, ls=(0, (3, 2.5)), zorder=2)

    def lineage(y, ancestor, possible, certain):
        ax.plot([ancestor, possible], [y, y], color=ROCK_LIGHT, lw=0.9, zorder=3)
        ax.plot(ancestor, y, "o", ms=3.8, mfc="white", mec=ROCK_LIGHT, mew=0.9, zorder=5)
        bar(ax, possible, certain, y, ROCK_LIGHT, 5.5, myr_per_pt, zorder=4)
        ax.plot([certain, X1], [y, y], color=ROCK, lw=5.5, solid_capstyle="butt", zorder=4)

    def clocks(group, y_top):
        for i, (name, old, young) in enumerate(F.CLOCKS[group]):
            bar(ax, old, young, y_top - i * 0.3, CLOCK[name], 4.6, myr_per_pt, zorder=4)

    # Lane 1: all living land plants
    y1 = 7.7
    spore(ax, pts(ax, X0 - 2.0, 9.75))
    ax.text(X0 - 5.4, 9.75, "Ancestor of all living land plants", fontsize=TITLE, weight="bold", va="center")
    clocks("embryophyta", 9.3)
    (m_old, _), (m_spore, _) = F.MAXIMA["embryophyta"]
    maximum(m_old, y1 - 0.25, 9.5)
    ax.text(m_old - 0.8, y1 - 0.3, f"{m_old:g} Ma maximum, argued\nfrom spores absent in\nolder marine rocks",
            fontsize=SMALL, color=MUTED, ha="left", va="top", linespacing=1.2)
    maximum(m_spore, y1 - 0.62, 9.5)
    ax.text(m_spore + 0.7, y1 - 0.45, f"{m_spore:g} Ma maximum", fontsize=SMALL, color=MUTED, ha="right",
            va="center")
    possible, certain = F.spore_first("cryptospore")
    lineage(y1, max(o for _, o, _ in F.CLOCKS["embryophyta"]), possible, certain)
    ax.text(possible + 0.8, y1 + 0.3, "oldest land-plant spores", fontsize=SMALL, color=ROCK, ha="right",
            va="center")

    bx0, bx1, by0, by1 = 457.5, X1 + 0.3, 5.72, y1 - 0.3
    ax.add_patch(FancyBboxPatch((bx1, by0), bx0 - bx1, by1 - by0, boxstyle="round,pad=0,rounding_size=1.2",
                                mutation_aspect=0.08, facecolor=ROCK_PALE, edgecolor="none", zorder=1))
    ax.text(bx0 - 1.0, by1 - 0.12, "Libyan boreholes: samples with three-rayed (trilete) spores",
            fontsize=SMALL, weight="semibold", color=ROCK, va="top")
    gx, gy = 455.5, by1 - 0.55
    for k in range(n["n_old"]):
        c, r = divmod(k, 4)
        ax.add_patch(Circle((c * 3.6, -r * 3.6), 1.3, transform=pts(ax, gx, gy), facecolor="white",
                            edgecolor=ROCK, lw=0.6, zorder=5))
    gx2 = gx - 10.5
    for k in range(n["n_ref"]):
        c, r = divmod(k, 4)
        ax.add_patch(Circle((c * 3.6, -r * 3.6), 1.3, transform=pts(ax, gx2, gy),
                            facecolor=ROCK if k < n["k_ref"] else "white", edgecolor=ROCK, lw=0.6, zorder=5))
    ax.text(gx + 0.4, gy - 0.62, f"0 of {n['n_old']}\nolder", fontsize=SMALL, color=ROCK, va="top",
            linespacing=1.15)
    ax.text(gx2 + 0.4, gy - 0.62, f"{n['k_ref']} of {n['n_ref']} younger\nthan ~443 Ma", fontsize=SMALL, color=ROCK,
            va="top", linespacing=1.15)
    ax.text(426.0, gy + 0.12, f"A steady input since {m_spore:g} Ma\nfits only below {n['limit']:.2f} of the later"
            f"\ninput ({n['block']:.2f} if samples are\nweighted by well and rock unit)", fontsize=SMALL, va="top",
            linespacing=1.2)

    # Lane 2: living vascular plants
    y2 = 3.35
    cooksonia(ax, pts(ax, X0 - 2.6, 5.3))
    title = ax.text(X0 - 5.4, 5.33, "Ancestor of living vascular plants", fontsize=TITLE, weight="bold",
                    va="center")
    ax.annotate("clubmosses, ferns, seed plants", xy=(1, 0.5), xycoords=title, xytext=(5, 0),
                textcoords="offset points", fontsize=SMALL, color=MUTED, va="center")
    clocks("tracheophyta", 4.95)
    (m_vasc, _), = F.MAXIMA["tracheophyta"]
    maximum(m_vasc, y2 - 0.25, 5.25)
    ax.text(m_vasc + 0.7, 5.3, f"{m_vasc:g} Ma maximum", fontsize=SMALL, color=MUTED, ha="right", va="center")
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

    ys = y2 - 0.36
    ax.plot(n["coarse"], [ys, ys], color=INK, lw=4.0, alpha=0.4, solid_capstyle="butt", zorder=5)
    ax.plot(n["steady"], ys, marker="^", ms=4.4, color=INK, zorder=6)
    lo, hi = n["coarse"]
    ax.text(n["steady"] - 1.6, ys + 0.12, f"steady finding, 95% limits on\nthe record's start: {n['steady']:.1f} Ma"
            f"\n({lo:.0f}–{hi:.0f} Ma if counted coarsely)", fontsize=SMALL, va="top", linespacing=1.2)

    a0, a1 = n["ages"]
    r0, r1 = n["ratio"]
    c0, c1 = n["coarse_ratio"]
    d0, d1 = n["delay"]
    ax.text((ancestor + possible) / 2 + 2.5, y2 + 0.12, "①", fontsize=LABEL + 1, color=MESSAGE, ha="center",
            va="bottom", weight="bold", zorder=6)
    yb = y2 - 1.05
    ax.annotate("", xy=(n["steady"], yb), xytext=(a1, yb),
                arrowprops={"arrowstyle": "<->", "color": MESSAGE, "lw": 0.8, "shrinkA": 0, "shrinkB": 0})
    ax.plot([a0, a0], [yb - 0.12, yb + 0.12], color=MESSAGE, lw=0.8)
    ax.text((a1 + n["steady"]) / 2, yb - 0.14, "②", fontsize=LABEL + 1, color=MESSAGE, ha="center", va="top",
            weight="bold")
    tx, ty, lead = X0 - 2.2, 4.55, 0.33
    lines = [(f"Two examples in which older clock dates ({a0:.0f}–{a1:.0f} Ma) fit:", "normal"),
             (f"①  no delay in recognisable features; fossils found {r0:.0f}–{r1:.0f}×", "semibold"),
             ("     less often before the oldest one than after it", "semibold"),
             ("②  fossils found at a steady rate; recognisable features", "semibold"),
             (f"     appearing at least {d0:.0f}–{d1:.0f} million years after the ancestor", "semibold")]
    for i, (text, weight) in enumerate(lines):
        ax.text(tx, ty - i * lead, text, fontsize=LABEL, color=MESSAGE, weight=weight, va="top")
    ax.text(tx, ty - 5 * lead - 0.1, f"Both count the {len(n['units'])} fossil groups as independent; counted"
            f" coarsely, ① needs\n{c0:.1f}–{c1:.1f}×. They show what fits, not how common the plants were.",
            fontsize=SMALL, color=MUTED, va="top", linespacing=1.25)

    bases = {}
    for r in F.read(F.TIMESCALE):
        bases[r["period"]] = max(bases.get(r["period"], 0), float(r["base_ma"]))
    order = list(PERIODS)
    for i, p in enumerate(order):
        old = min(bases[p], X0)
        young = max(bases[order[i + 1]] if i + 1 < len(order) else X1, X1)
        ax.fill_between([old, young], 1.55, 1.9, color=PERIODS[p], lw=0)
        ax.text((old + young) / 2, 1.725, p, fontsize=SMALL, ha="center", va="center")
    for t in range(500, X1 - 1, -20):
        ax.plot([t, t], [1.55, 1.45], color=MUTED, lw=0.5)
        ax.text(t, 1.38, f"{t}", fontsize=SMALL, ha="center", va="top", color=MUTED)
    ax.text(X0, 1.38, "million years ago", fontsize=SMALL, ha="left", va="top", color=MUTED)

    lx, ly, step = 446.5, 9.75, 0.28
    ax.text(lx, ly, "Molecular-clock estimates", fontsize=SMALL, color=MUTED, va="center")
    for i, name in enumerate(CLOCK):
        y = ly - (i + 1) * step
        bar(ax, lx, lx - 4, y, CLOCK[name], 4.6, myr_per_pt)
        ax.text(lx - 5.5, y, name, fontsize=SMALL, va="center")
    y = ly - 4 * step
    ax.plot([lx, lx - 4], [y, y], color=ROCK, lw=5.5, solid_capstyle="butt")
    ax.text(lx - 5.5, y, "fossil record (pale: possible ages of the oldest)", fontsize=SMALL, va="center")
    y -= step
    ax.plot([lx, lx - 4], [y, y], color=ROCK_LIGHT, lw=0.9)
    ax.plot(lx, y, "o", ms=3.8, mfc="white", mec=ROCK_LIGHT, mew=0.9)
    ax.text(lx - 5.5, y, "gap from oldest clock-range edge", fontsize=SMALL, va="center")
    y -= step
    ax.add_patch(Circle((0, 0), 1.25, transform=pts(ax, lx - 2, y), facecolor=ROCK, edgecolor="none"))
    ax.text(lx - 5.5, y, "fossil group at its oldest allowed age", fontsize=SMALL, va="center")

    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=300,
                    metadata={"CreationDate": None, "ModDate": None} if ext == "pdf" else None)
    plt.close(fig)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "figures" / "graphical_abstract"
    draw(out)
    draw(out.with_name(out.name + "_journal"), headline=False)
