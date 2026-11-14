# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Main-text figures 1-4 of the F3 article, drawn by figures.py into studies/f3/manuscript/figures/.

Numerical results are read from frozen or reviewed output tables; the published clock intervals,
maxima and ash age come from figures.py. Diagnostic delays are declared scenarios. Built from the
reconstruction (studies/f3/manuscript/reconstruction/README.md, step 4) and reviewed by Codex.
"""

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import figures as F  # noqa: E402

UNITS = ROOT / "studies/f3/models/out/m2_units.csv"
RESULTS = ROOT / "studies/f3/models/out/m2_results.csv"
FRONTIER = ROOT / "studies/f3/models/loop3/out/frontier.csv"
DIAL = ROOT / "studies/f3/models/loop3/out/count_dial.csv"
RULERS = ROOT / "studies/f3/models/loop3/out/rulers.csv"
COMBINED = ROOT / "studies/f3/models/loop3/out/combined_rulers_curve.csv"
RISE = ROOT / "studies/f3/models/loop3/out/rise_shapes.csv"
CUTOFF = float(F.primary_bound("B2", "flat")[2]["cutoff_ma"])
ALPHA = 1 - float(F.primary_bound("B2", "flat")[2]["confidence_conditional_on_fixed_history_iid_units"])
EMBRYOPHYTE_MAXIMA = tuple(age for age, _ in F.MAXIMA["embryophyta"])
SPORE_MAXIMUM = EMBRYOPHYTE_MAXIMA[1]
VASCULAR_MAXIMUM = F.MAXIMA["tracheophyta"][0][0]

INK, MUTED, GRID = "#2b2b2a", "#6b6a64", "#d9d8d2"
CLOCK = {"Morris et al. 2018": "#2a78d6", "Harris et al. 2022": "#eb6834", "Hooper et al. 2026": "#187b56"}
BLUE = {"650": "#104281", "450": "#2a78d6", "250": "#597ca5"}
FOSSIL = "#8a8a84"

plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.linewidth": 0.6,
                     "font.family": "sans-serif"})


def save(fig, path):
    for ext in ("png", "pdf"):
        metadata = {"CreationDate": None, "ModDate": None} if ext == "pdf" else None
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200, bbox_inches="tight", pad_inches=0.06, metadata=metadata)
    plt.close(fig)


def maxima_lines(ax, which=EMBRYOPHYTE_MAXIMA + (VASCULAR_MAXIMUM,), lw=0.8):
    for x in which:
        ax.axvline(x, color=INK, lw=lw, ls=(0, (4, 3)), zorder=0)


def clean(ax, left=False):
    ax.spines[["top", "right"] + ([] if left else ["left"])].set_visible(False)
    if not left:
        ax.set_yticks([])


def fig1(path):
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 6.4), sharex=True, gridspec_kw={"height_ratios": [2.6, 2.6, 4.6]})
    groups = (("embryophyta", "(a) Ancestor of living land plants: molecular-clock estimates", EMBRYOPHYTE_MAXIMA),
              ("tracheophyta", "(b) Ancestor of living vascular plants: molecular-clock estimates", (VASCULAR_MAXIMUM,)))
    for ax, (key, title, maxima) in zip(axes[:2], groups):
        labels = []
        for i, (name, old, young) in enumerate(reversed(F.CLOCKS[key])):
            ax.barh(i, old - young, left=young, height=0.5, color=CLOCK[name], edgecolor="white", lw=1)
            labels.append(f"{name}  {old:.0f}–{young:.0f} Ma")
        maxima_lines(ax, maxima)
        for x in maxima:
            ax.text(x - 0.8, 2.85, f"{x} Ma maximum", fontsize=7, ha="left", va="top", color=INK)
        ax.set_ylim(-0.6, 2.9)
        ax.set_title(title, fontsize=8.5, loc="left", color=INK)
        clean(ax)
        ax.set_yticks(range(3), labels, fontsize=7.5)
        ax.tick_params(axis="y", length=0)
    ax = axes[2]
    crypt, tril = F.spore_first("cryptospore"), F.spore_first("trilete")
    bor = (F.stage_base("Sandbian"), F.BENTONITE_MA)
    oman = (F.body_first("B0")[0], F.stage_base("Hirnantian"))
    b2 = F.body_first("B2")
    rows = [("Land-plant cryptospores\n(strict compilation)", crypt),
            ("Trilete spores\n(strict compilation)", tril),
            ("Borenshult-1 trilete,\npossible identification", bor),
            ("Borenshult-1 triletes,\ndefinite identification", bor),
            ("Sporangial fragments,\nGhaba-1, Oman", oman),
            ("Crown vascular-\nplant bodies", b2)]
    for i, (lab, (possible, certain)) in enumerate(reversed(rows)):
        ax.barh(i, possible - certain, left=certain, height=0.46, color=FOSSIL, alpha=0.45, lw=0)
        ax.plot([certain, certain], [i - 0.23, i + 0.23], color=INK, lw=2.0, solid_capstyle="butt")
        ax.text(certain - 1.0, i, f"{possible:.1f}–{certain:.1f}", va="center", ha="left", fontsize=7,
                color=INK)
    maxima_lines(ax, lw=0.6)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_title("(c) Possible ages of the oldest finds, by labelled identification",
                 fontsize=8.5, loc="left")
    clean(ax)
    ax.set_yticks(range(len(rows)), [r[0] for r in reversed(rows)], fontsize=7.2)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(528, 410)
    ax.set_xlabel("Age (million years ago)")
    fig.tight_layout()
    save(fig, path)


def fig2(path):
    units = [r for r in F.read(F.MEMBERS) if r["reading"] == "main" and r["category"] == "B2"
             and float(r["max_ma"]) > CUTOFF]
    ages = sorted(float(r["max_ma"]) for r in units if float(r["min_ma"]) >= CUTOFF)
    A = max(float(r["max_ma"]) for r in units)
    flat, _, case = F.primary_bound("B2", "flat")
    assert len(units) == int(case["n_possible"]) and len(ages) == int(case["n_guaranteed"])
    steps = [r for r in F.read(F.SUPPRESS) if r["category"] == "B2" and r["reading"] == "main"
             and r["inventory_variant"] == "primary" and r["baseline"] == "flat"
             and float(r["break_ma"]) == A and r["status"] == "bounded"]
    endpoints = {float(r["older_multiplier"]): float(r["older_bound_ma"]) for r in steps}
    assert len(endpoints) == len(steps)
    half, tenth = endpoints[0.5], endpoints[0.1]
    d = 20.0
    fig, (top, bot) = plt.subplots(2, 1, figsize=(7.2, 4.4), sharex=True, gridspec_kw={"height_ratios": [2, 3]})
    x0, x1 = 456, 390
    for w, col, lab in ((1.0, BLUE["650"], "steady finding rate"), (0.5, BLUE["450"], "earlier rate halved"),
                        (0.1, BLUE["250"], "earlier rate a tenth")):
        top.plot([x0, A, A, x1], [w, w, 1, 1], color=col, lw=2, solid_joinstyle="miter",
                 drawstyle="default", label=lab)
    rise = next(r for r in F.read(RISE) if r["n"] == case["n_guaranteed"])
    tau = float(rise["K_myr"])
    xs = np.linspace(A, x0, 400)
    top.plot(np.r_[xs[::-1], A, x1], np.r_[np.exp(-(xs[::-1] - A) / tau), 1, 1], color="#4f8a3a", lw=1.4,
             ls=(0, (4, 2)), label=f"limiting rise: finds doubling every {float(rise['exp_limit_doubling_myr']):.2f} Myr")
    top.axvline(A, color=MUTED, lw=0.6, ls=":")
    top.text(A - 0.4, 1.12, f"A = {A} Ma, oldest possible find", fontsize=7, color=MUTED, va="bottom")
    top.set_ylim(0, 1.35)
    top.set_yticks([0, 0.5, 1])
    top.set_ylabel("Relative finding\nrate, w")
    top.legend(frameon=False, fontsize=7, loc="lower right")
    top.set_title("(a) Assumed finding-rate histories, differing only before A",
                  fontsize=8.5, loc="left")
    top.spines[["top", "right"]].set_visible(False)
    seen = {}
    for a in ages:
        k = seen.get(a, 0)
        seen[a] = k + 1
        bot.plot(a, 0.04 + 0.075 * k, "o", ms=2.6, color=INK)
    bot.axvline(CUTOFF, color=MUTED, lw=0.8)
    bot.text(CUTOFF + 0.4, 1.7, f"c = {CUTOFF} Ma\n(end of Emsian)", fontsize=7, color=MUTED, ha="right", va="top")
    bot.text((A + CUTOFF) / 2, -0.12, f"n = {len(ages)} finds certainly inside the window, stacked at their oldest possible ages",
             fontsize=7, ha="center", va="top", color=MUTED)
    for T, col, lab, ha in ((flat, BLUE["650"], f"T = {flat:.1f} Ma\n(steady)", "left"),
                            (half, BLUE["450"], f"{half:.1f} Ma\n(halved: scenario)", "right"),
                            (tenth, BLUE["250"], f"{tenth:.1f} Ma\n(a tenth: scenario)", "right")):
        bot.annotate("", xy=(T, 0.55), xytext=(T, 1.05), arrowprops={"arrowstyle": "-|>", "color": col, "lw": 1.4})
        bot.text(T + (0.5 if ha == "right" else -0.5), 0.95, lab, color=INK, fontsize=7, ha=ha, va="top")
    bot.annotate("", xy=(flat + d, 1.35), xytext=(flat, 1.35),
                 arrowprops={"arrowstyle": "-|>", "color": CLOCK["Harris et al. 2022"], "lw": 1.4})
    bot.plot([flat, flat], [1.05, 1.35], color=CLOCK["Harris et al. 2022"], lw=0.8, ls=":")
    bot.text(flat + d / 2, 1.42, f"assumed delay d = {d:.0f} Myr: candidate ancestor t = {flat + d:.1f} Ma",
             fontsize=7, ha="center", va="bottom")
    bot.set_ylim(-0.4, 1.75)
    bot.set_title("(b) Finds, the 95% limit T, and scenarios chosen after seeing the data",
                  fontsize=8.5, loc="left")
    clean(bot)
    bot.set_xlim(x0, x1)
    bot.set_xlabel("Age (million years ago)")
    fig.tight_layout()
    save(fig, path)


def murzuq_units():
    rows = [r for r in F.read(UNITS) if r["design"] == "LY-MZ-CU"
            and r["variant"] == "allocation=stage;material_type=chart-code" and not r["excluded"]]
    stages = [r["stage"] for r in F.read(F.TIMESCALE)]

    def top(stage):
        return F.stage_base(stages[stages.index(stage) - 1])

    return [(r["cluster"], F.stage_base(r["oldest_stage"]), top(r["youngest_stage"]), r["d"] == "1",
             r["oldest_stage"] in ("Rhuddanian", "Aeronian", "Telychian")) for r in rows]


def fig3(path):
    units = murzuq_units()
    older = [u for u in units if not u[4]]
    ref = [u for u in units if u[4]]
    assert len(older) == 28 and not any(u[3] for u in older) and len(ref) == 59 and sum(u[3] for u in ref) == 51
    wells = sorted({u[0] for u in units})
    broad = [u for u in older if u[1] > SPORE_MAXIMUM]
    younger = [u for u in older if u[1] < SPORE_MAXIMUM]
    assert len(broad) == 10 and len(younger) == 18 and len({u[0] for u in broad}) == 2
    assert all(u[2] < SPORE_MAXIMUM for u in broad)
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 5.6), gridspec_kw={"width_ratios": [3.2, 2]})
    a.axvspan(F.stage_base("Rhuddanian"), F.stage_base("Sheinwoodian"), color=GRID, alpha=0.6, lw=0)
    y, ticks = 0.0, []
    for j, w in enumerate(wells):
        start = y
        block = sorted((u for u in units if u[0] == w), key=lambda u: (-u[1], -u[2]))
        for _, hi, lo, pos, _r in block:
            a.plot([hi, lo], [y, y], color=MUTED, lw=0.5)
            a.plot((hi + lo) / 2, y, "o", ms=2.7, mfc=INK if pos else "white", mec=INK, mew=0.6)
            y += 1
        ticks.append(((start + y - 1) / 2, f"{w}\n({len(block)} samples)"))
        if j < len(wells) - 1:
            a.axhline(y + 0.75, color=GRID, lw=0.7)
        y += 2.5
    a.set_yticks([t for t, _ in ticks], [lab for _, lab in ticks], fontsize=7)
    a.tick_params(axis="y", length=0)
    a.set_ylim(y - 1.5, -12)
    a.vlines(SPORE_MAXIMUM, -1.2, y - 1.5, color=INK, lw=0.8, ls=(0, (4, 3)))
    a.set_xlim(F.stage_base("Darriwilian") + 1, F.stage_base("Sheinwoodian") - 0.5)
    a.set_xlabel("Age (million years ago)")
    a.text(0.015, 0.985, f"Older samples: {len(broad)} broadly dated Darriwilian,\n"
           f"{len(younger)} wholly younger than {SPORE_MAXIMUM} Ma",
           transform=a.transAxes, fontsize=7, ha="left", va="top", color=INK)
    a.text(SPORE_MAXIMUM - 0.3, -2.2, f"{SPORE_MAXIMUM} Ma", fontsize=7, va="center")
    a.text((F.stage_base("Rhuddanian") + F.stage_base("Sheinwoodian")) / 2, -2.2, "Llandovery reference",
           fontsize=7, ha="center", va="center")
    a.plot([], [], "o", ms=3.2, mfc=INK, mec=INK, label="triletes reported")
    a.plot([], [], "o", ms=3.2, mfc="white", mec=INK, label="no triletes")
    a.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    a.set_title("(a) Samples by well, with their age ranges", fontsize=8.5, loc="left")
    a.spines[["top", "right", "left"]].set_visible(False)
    res = sorted(((float(r["rho"]), float(r["fstar_H0c_459.1"]), float(r["fstar_H0_459.1"])) for r in F.read(RESULTS)
                  if r["design"] == "LY-MZ-CU" and r["primary"] == "True"
                  and r["variant"] == "allocation=stage;cluster_k=2.0;material_type=chart-code"))
    rho = [r[0] for r in res]
    assert len(res) == 4 and len(set(rho)) == 4
    b.plot(rho, [r[1] for r in res], ":o", color=CLOCK["Morris et al. 2018"], lw=1, ms=5, label="steady supply")
    b.plot(rho, [r[2] for r in res], ":s", color=CLOCK["Harris et al. 2022"], lw=1, ms=5,
           label="varying supply (0 to Llandovery level),\nweighted by sample age ranges")
    for r_, c_, e_ in res:
        b.text(r_ * 0.93, c_ - 0.02, f"{c_:.3f}", fontsize=6.5, ha="left", va="top", color=INK)
    b.set_xscale("log")
    b.set_xticks(rho, [f"{r:g}" for r in rho])
    b.minorticks_off()
    b.invert_xaxis()
    b.set_ylim(0, 1.0)
    b.set_xlabel("Delivery ratio ρ (older / Llandovery)")
    b.set_ylabel("Upper 95% limit on older supply, f")
    b.legend(frameon=False, fontsize=7, loc="upper left")
    b.text(0.5, -0.16, "Markers: evaluated scenarios\nDotted lines: visual guides",
           transform=b.transAxes, ha="center", va="top", fontsize=7, color=MUTED)
    b.set_title(f"(b) Limits from {SPORE_MAXIMUM} Ma", fontsize=8.5, loc="left")
    b.spines[["top", "right"]].set_visible(False)
    b.grid(axis="y", color=GRID, lw=0.5)
    fig.tight_layout()
    save(fig, path)


def fig4(path):
    units = sorted(((float(r["max_ma"]), float(r["min_ma"])) for r in F.read(F.MEMBERS)
                    if r["reading"] == "main" and r["category"] == "B2"
                    and float(r["max_ma"]) > CUTOFF), reverse=True)
    flat, _, case = F.primary_bound("B2", "flat")
    assert len(units) == int(case["n_possible"])
    assert sum(young >= CUTOFF for _, young in units) == int(case["n_guaranteed"])
    alt = [float(r["older_bound_ma"]) for r in F.read(F.BOUNDS) if r["category"] == "B2" and r["reading"] == "main"
           and r["history"] == "flat" and (r["units"], r["variant"]) in (("region_stage", "primary"),
                                                                         ("locality_age", "curated_tail_only"))
           and not r["excluded_region"] and r["cutoff"] == "Emsian"]
    assert len(alt) == 2 and abs(min(alt) - 432.38) < 0.01 and abs(max(alt) - 434.05) < 0.01, alt
    rows = [r for r in F.read(FRONTIER) if r["reading"] == "main" and r["category"] == "B2"]
    params = {}
    for r in rows:
        A, c, n = float(r["oldest_possible_ma"]), float(r["cutoff_ma"]), int(r["n_guaranteed"])
        assert params.setdefault(r["unit_treatment"], (A, c, n)) == (A, c, n)
        if r["status"] == "contour":
            t, d = float(r["candidate_lineage_ma"]), float(r["assumed_diagnostic_delay_myr"])
            ratio = (t - d - A) / ((A - c) * (ALPHA ** (-1 / n) - 1))
            assert abs(ratio - float(r["later_to_earlier_intensity"])) < 1e-6, r
    dial = F.read(DIAL)
    curve = [(float(r["n_independent"]), float(r["older_bound_ma"])) for r in dial if not r["note"]]
    cross = next(float(r["n_independent"]) for r in dial if r["note"])
    marks = {r["unit_treatment"]: (float(r["n_independent"]), float(r["older_bound_ma"])) for r in dial
             if r["unit_treatment"]}
    assert abs(marks["primary"][1] - flat) < 1e-3 and abs(marks["region_stage"][1] - min(alt)) < 1e-3
    assert abs(marks["curated"][1] - max(alt)) < 1e-3 and marks["primary"][0] == float(case["n_guaranteed"])
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 4.4), gridspec_kw={"width_ratios": [2, 3]})
    a.plot([n for n, _ in curve], [T for _, T in curve], color=BLUE["650"], lw=2)
    a.axhline(VASCULAR_MAXIMUM, color=INK, lw=0.8, ls=(0, (4, 3)))
    a.text(59, VASCULAR_MAXIMUM + 0.12, f"{VASCULAR_MAXIMUM} Ma maximum", fontsize=6.8, ha="right", va="bottom")
    a.plot([cross, cross], [427.5, VASCULAR_MAXIMUM], color=MUTED, lw=0.7, ls=":")
    a.text(cross - 0.8, 429.0, f"{cross:.1f} finds:\nabout half\nthe main count", fontsize=6.8, color=MUTED, ha="right",
           va="center")
    for key, lab, ha, dx, dy, nd in (("primary", "main count", "center", 0, -0.45, 1),
                                     ("region_stage", "region and stage", "left", 1.5, 0.0, 1),
                                     ("curated", "curated oldest records", "left", 1.5, 0.0, 2)):
        n, T = marks[key]
        a.plot(n, T, "o", color=BLUE["650"], ms=5, mec="white", mew=1)
        a.text(n + dx, T + dy, f"{lab}\n{int(n)} finds, {T:.{nd}f} Ma", fontsize=6.6, ha=ha,
               va="top" if dy else "center")
    a.set_xlim(10, 60)
    a.set_ylim(427.5, 437.5)
    a.set_xlabel("Independent finds, n")
    a.set_ylabel("95% confidence limit on record start (Ma)")
    a.set_title("(a) The limit depends on the count", fontsize=8.5, loc="left")
    a.spines[["top", "right"]].set_visible(False)
    a.grid(axis="y", color=GRID, lw=0.5)
    t = np.linspace(426.8, 456, 800)

    def contrast(key, d):
        A, c, n = params[key]
        with np.errstate(divide="ignore", invalid="ignore"):
            k = np.where(t - d > A, (t - d - A) / ((A - c) * (ALPHA ** (-1 / n) - 1)), np.nan)
        return np.maximum(k, 1.0)

    for name, old, young in F.CLOCKS["tracheophyta"]:
        b.axvspan(young, min(old, 456), color=CLOCK[name], alpha=0.10 if name.startswith("Morris") else 0.2, lw=0)
    b.text(449.5, 125, "Harris", fontsize=7, ha="center", color=INK)
    b.text(430, 125, "Hooper", fontsize=7, ha="center", color=INK)
    b.text(440, 125, "Morris (to 451 Ma)", fontsize=7, ha="center", color=INK)
    b.axvline(VASCULAR_MAXIMUM, color=INK, lw=0.8, ls=(0, (4, 3)))
    for d, step, style in ((0, "650", "-"), (10, "450", (0, (6, 2))), (20, "250", (0, (3, 1, 1, 1)))):
        b.plot(t, contrast("primary", d), color=BLUE[step], lw=2, ls=style,
               label=f"main count (n = {params['primary'][2]}), delay {d} Myr")
    b.plot(t, contrast("region_stage", 0), color=MUTED, lw=1.3, ls="--",
           label=f"region and stage (n = {params['region_stage'][2]}), no delay")
    b.plot(t, contrast("curated", 0), color=MUTED, lw=1.3, ls=":",
           label=f"curated oldest records (n = {params['curated'][2]}), no delay")
    ruler_rows = F.read(RULERS)
    for key, col, style, lab in (("rock_nonmarine_area", "#8c6d46", "-", "rock"),
                                 ("search_all", "#8f8e86", (0, (5, 1.5, 1, 1.5)), "searching"),
                                 ("spores_trilete_share", "#4f8a3a", "-", "spores")):
        pts = sorted((float(r["candidate_ma"]), float(r["later_to_earlier"])) for r in ruler_rows
                     if r["ruler"] == key and r["later_to_earlier"] not in ("inf",) )
        xs, ys = [x for x, _ in pts], [y for _, y in pts]
        b.plot(xs, ys, color=col, lw=1.2, ls=style, label=f"ruler: {lab}")
        b.text(455.6, ys[-1] * (1.09 if lab != "rock" else 0.93), lab, fontsize=6.6, color=col, ha="left",
               va="bottom" if lab != "rock" else "top")
    combo = sorted((float(r["candidate_ma"]), float(r["q_combined"])) for r in F.read(COMBINED)
                   if r["combination"] == "rock_x_spore_share" and r["q_combined"] != "inf" and float(r["candidate_ma"]) <= 456)
    b.plot([x for x, _ in combo], [y for _, y in combo], color="#6b7a35", lw=1.2, ls=(0, (2, 1.5)),
           label="rock × spores (chosen after seeing both)")
    b.text(455.6, combo[-1][1] * 1.08, "rock × spores", fontsize=6.6, color="#6b7a35", ha="left", va="bottom")
    for r in rows:
        if r["status"] == "contour" and r["unit_treatment"] == "primary" and float(r["assumed_diagnostic_delay_myr"]) == 0 \
                and float(r["candidate_lineage_ma"]) in (444.0, 452.0):
            k = float(r["later_to_earlier_intensity"])
            b.plot(float(r["candidate_lineage_ma"]), k, "o", color=BLUE["650"], ms=5, mec="white", mew=1)
            b.text(float(r["candidate_lineage_ma"]), k * 1.18, f"{k:.1f}×", fontsize=7, ha="center", va="bottom")
    b.set_yscale("log")
    b.set_ylim(0.9, 170)
    b.set_yticks([1, 2, 5, 10, 20, 50, 100], ["1", "2", "5", "10", "20", "50", "100"])
    b.minorticks_off()
    b.set_xlim(456, 426)
    b.set_xlabel("Candidate ancestor age, t (Ma)")
    b.set_ylabel("Times less often found before A")
    b.legend(frameon=False, fontsize=6.4, loc="upper center", bbox_to_anchor=(0.45, -0.16), ncol=2)
    b.set_title("(b) Reductions that would fit, and outside rulers", fontsize=8.5, loc="left")
    b.spines[["top", "right"]].set_visible(False)
    b.grid(axis="y", color=GRID, lw=0.5)
    fig.tight_layout()
    save(fig, path)


INPUTS = [UNITS, RESULTS, FRONTIER, DIAL, RULERS, COMBINED, RISE, Path(__file__)]


def draw(out):
    fig1(out / "fig1_dispute")
    fig2(out / "fig2_bound")
    fig3(out / "figS_murzuq")
    fig4(out / "fig3_requirements")
