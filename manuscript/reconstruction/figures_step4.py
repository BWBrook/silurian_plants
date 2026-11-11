# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Figures 1-4 for the reconstructed F3 article (reconstruction step 4).

Numerical results are read from frozen or reviewed output tables; the published clock intervals,
maxima and ash age come from manuscript/figures.py. Diagnostic delays are declared scenarios. Outputs go to
manuscript/reconstruction/figures/, with input and output hashes in figures.json.

    uv run manuscript/reconstruction/figures_step4.py
"""

import csv
import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "figures"
sys.path.insert(0, str(ROOT / "manuscript"))
import figures as F  # noqa: E402

UNITS = ROOT / "models/f3/out/m2_units.csv"
RESULTS = ROOT / "models/f3/out/m2_results.csv"
FRONTIER = ROOT / "models/f3/loop3/out/frontier.csv"
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
    ax.set_title("(c) First-record age supports under the labelled identification readings",
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
    for w, col, lab in ((1.0, BLUE["650"], "constant recording"), (0.5, BLUE["450"], "earlier recording halved"),
                        (0.1, BLUE["250"], "earlier recording a tenth")):
        top.plot([x0, A, A, x1], [w, w, 1, 1], color=col, lw=2, solid_joinstyle="miter",
                 drawstyle="default", label=lab)
    top.axvline(A, color=MUTED, lw=0.6, ls=":")
    top.text(A - 0.4, 1.12, f"A = {A} Ma, oldest possible find", fontsize=7, color=MUTED, va="bottom")
    top.set_ylim(0, 1.35)
    top.set_yticks([0, 0.5, 1])
    top.set_ylabel("Relative recording\nrate, w")
    top.legend(frameon=False, fontsize=7, loc="lower right")
    top.set_title("(a) Assumed recording histories, differing only before A",
                  fontsize=8.5, loc="left")
    top.spines[["top", "right"]].set_visible(False)
    seen = {}
    for a in ages:
        k = seen.get(a, 0)
        seen[a] = k + 1
        bot.plot(a, 0.04 + 0.075 * k, "o", ms=2.6, color=INK)
    bot.axvline(CUTOFF, color=MUTED, lw=0.8)
    bot.text(CUTOFF + 0.4, 1.7, f"c = {CUTOFF} Ma\n(end of Emsian)", fontsize=7, color=MUTED, ha="right", va="top")
    bot.text((A + CUTOFF) / 2, -0.12, f"n = {len(ages)} guaranteed units, stacked at their oldest possible ages",
             fontsize=7, ha="center", va="top", color=MUTED)
    for T, col, lab, ha in ((flat, BLUE["650"], f"T = {flat:.1f} Ma\n(constant)", "left"),
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
    bot.set_title("(b) Finds, fixed-history 95% bound T, and retrospective step/delay scenarios",
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
        ticks.append(((start + y - 1) / 2, f"{w}\n({len(block)} cuttings)"))
        if j < len(wells) - 1:
            a.axhline(y + 0.75, color=GRID, lw=0.7)
        y += 2.5
    a.set_yticks([t for t, _ in ticks], [lab for _, lab in ticks], fontsize=7)
    a.tick_params(axis="y", length=0)
    a.set_ylim(y - 1.5, -12)
    a.vlines(SPORE_MAXIMUM, -1.2, y - 1.5, color=INK, lw=0.8, ls=(0, (4, 3)))
    a.set_xlim(F.stage_base("Darriwilian") + 1, F.stage_base("Sheinwoodian") - 0.5)
    a.set_xlabel("Age (million years ago)")
    a.text(0.015, 0.985, f"Older frame: {len(broad)} broad Darriwilian supports\n"
           f"{len(younger)} cuttings wholly younger than {SPORE_MAXIMUM} Ma",
           transform=a.transAxes, fontsize=7, ha="left", va="top", color=INK)
    a.text(SPORE_MAXIMUM - 0.3, -2.2, f"{SPORE_MAXIMUM} Ma", fontsize=7, va="center")
    a.text((F.stage_base("Rhuddanian") + F.stage_base("Sheinwoodian")) / 2, -2.2, "Llandovery reference",
           fontsize=7, ha="center", va="center")
    a.plot([], [], "o", ms=3.2, mfc=INK, mec=INK, label="triletes reported")
    a.plot([], [], "o", ms=3.2, mfc="white", mec=INK, label="trilete zero (audited)")
    a.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    a.set_title("(a) Cuttings by well: stage-range support", fontsize=8.5, loc="left")
    a.spines[["top", "right", "left"]].set_visible(False)
    res = sorted(((float(r["rho"]), float(r["fstar_H0c_459.1"]), float(r["fstar_H0_459.1"])) for r in F.read(RESULTS)
                  if r["design"] == "LY-MZ-CU" and r["primary"] == "True"
                  and r["variant"] == "allocation=stage;cluster_k=2.0;material_type=chart-code"))
    rho = [r[0] for r in res]
    assert len(res) == 4 and len(set(rho)) == 4
    b.plot(rho, [r[1] for r in res], ":o", color=CLOCK["Morris et al. 2018"], lw=1, ms=5, label="constant input")
    b.plot(rho, [r[2] for r in res], ":s", color=CLOCK["Harris et al. 2022"], lw=1, ms=5,
           label="exposure-weighted mean,\nbounded variable input")
    for r_, c_, e_ in res:
        b.text(r_ * 0.93, c_ - 0.02, f"{c_:.3f}", fontsize=6.5, ha="left", va="top", color=INK)
    b.set_xscale("log")
    b.set_xticks(rho, [f"{r:g}" for r in rho])
    b.minorticks_off()
    b.invert_xaxis()
    b.set_ylim(0, 1.0)
    b.set_xlabel("Delivery ratio ρ (older / reference)")
    b.set_ylabel("Upper 95% limit on older input, f")
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
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 4.4), gridspec_kw={"width_ratios": [2, 3]})
    for i, (old, young) in enumerate(units):
        straddle = young < CUTOFF
        a.plot([old, max(young, 386)], [i, i], color=MUTED if not straddle else CLOCK["Harris et al. 2022"], lw=1.1,
               ls="-" if not straddle else (0, (2, 1.5)))
    a.axvline(CUTOFF, color=MUTED, lw=0.6, ls=":")
    a.axvspan(min(alt), max(alt), color=BLUE["250"], alpha=0.35, lw=0)
    a.axvline(flat, color=BLUE["650"], lw=1.6)
    a.axvline(VASCULAR_MAXIMUM, color=INK, lw=0.8, ls=(0, (4, 3)))
    a.text(flat - 0.6, -2.0, f"{flat:.1f} Ma, constant recording", fontsize=6.8, color=INK, va="center", ha="left")
    a.text(flat - 0.6, -5.0, f"{min(alt):.1f}–{max(alt):.2f} Ma, alternative units", fontsize=6.8, va="center",
           ha="left")
    a.text(flat - 0.6, -8.0, f"{VASCULAR_MAXIMUM} Ma maximum (dashed)", fontsize=6.8, va="center", ha="left")
    a.set_ylim(len(units) + 1, -10)
    a.set_xlim(437, 386)
    a.set_yticks([])
    a.set_xlabel("Age (million years ago)")
    a.plot([], [], color=MUTED, lw=1.1, label="guaranteed unit (48)")
    a.plot([], [], color=CLOCK["Harris et al. 2022"], lw=1.1, ls=(0, (2, 1.5)), label="straddles cutoff (2)")
    a.legend(frameon=False, fontsize=6.8, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=1)
    a.set_title("(a) Crown vascular-plant units", fontsize=8.5, loc="left")
    a.spines[["top", "right", "left"]].set_visible(False)
    t = np.linspace(426.8, 456, 800)

    def contrast(key, d):
        A, c, n = params[key]
        with np.errstate(divide="ignore", invalid="ignore"):
            k = np.where(t - d > A, (t - d - A) / ((A - c) * (ALPHA ** (-1 / n) - 1)), np.nan)
        return np.maximum(k, 1.0)

    for name, old, young in F.CLOCKS["tracheophyta"]:
        b.axvspan(young, min(old, 456), color=CLOCK[name], alpha=0.10 if name.startswith("Morris") else 0.2, lw=0)
    b.text(449.5, 34, "Harris", fontsize=7, ha="center", color=INK)
    b.text(430, 34, "Hooper", fontsize=7, ha="center", color=INK)
    b.text(440, 34, "Morris (to 451 Ma)", fontsize=7, ha="center", color=INK)
    b.axvline(VASCULAR_MAXIMUM, color=INK, lw=0.8, ls=(0, (4, 3)))
    for d, step, style in ((0, "650", "-"), (10, "450", (0, (6, 2))), (20, "250", (0, (3, 1, 1, 1)))):
        b.plot(t, contrast("primary", d), color=BLUE[step], lw=2, ls=style,
               label=f"primary units (n = {params['primary'][2]}), delay {d} Myr")
    b.plot(t, contrast("region_stage", 0), color=MUTED, lw=1.3, ls="--",
           label=f"region–stage units (n = {params['region_stage'][2]}), no delay")
    b.plot(t, contrast("curated", 0), color=MUTED, lw=1.3, ls=":",
           label=f"curated units (n = {params['curated'][2]}), no delay")
    for r in rows:
        if r["status"] == "contour" and r["unit_treatment"] == "primary" and float(r["assumed_diagnostic_delay_myr"]) == 0 \
                and float(r["candidate_lineage_ma"]) in (444.0, 452.0):
            k = float(r["later_to_earlier_intensity"])
            b.plot(float(r["candidate_lineage_ma"]), k, "o", color=BLUE["650"], ms=5, mec="white", mew=1)
            b.text(float(r["candidate_lineage_ma"]), k * 1.18, f"{k:.1f}×", fontsize=7, ha="center", va="bottom")
    b.set_yscale("log")
    b.set_ylim(0.9, 40)
    b.set_yticks([1, 2, 5, 10, 20], ["1", "2", "5", "10", "20"])
    b.minorticks_off()
    b.set_xlim(456, 426)
    b.set_xlabel("Candidate ancestor age, t (Ma)")
    b.set_ylabel("Later / earlier recording ratio")
    b.legend(frameon=False, fontsize=6.6, loc="upper center", bbox_to_anchor=(0.45, -0.16), ncol=2)
    b.set_title("(b) Retrospective recording/delay compatibility", fontsize=8.5, loc="left")
    b.spines[["top", "right"]].set_visible(False)
    b.grid(axis="y", color=GRID, lw=0.5)
    fig.tight_layout()
    save(fig, path)


def main():
    OUT.mkdir(exist_ok=True)
    fig1(OUT / "fig1_dispute")
    fig2(OUT / "fig2_bound")
    fig3(OUT / "fig3_murzuq")
    fig4(OUT / "fig4_requirements")
    inputs = [F.TIMESCALE, F.SPORES, F.MEMBERS, F.BOUNDS, F.SUPPRESS, UNITS, RESULTS, FRONTIER,
              ROOT / "manuscript/figures.py", Path(__file__)]
    outputs = sorted(OUT.glob("*.png")) + sorted(OUT.glob("*.pdf"))
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    (OUT / "figures.json").write_text(json.dumps(
        {"inputs": {str(p.relative_to(ROOT)): digest(p) for p in inputs},
         "outputs": {str(p.relative_to(ROOT)): digest(p) for p in outputs}}, indent=2) + "\n")


if __name__ == "__main__":
    main()
