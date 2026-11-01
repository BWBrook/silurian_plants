# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Manuscript support, conditional-calculation and biological-mapping figures.

Figure 2 reuses the sprint-1 figures in models/f3/loop2/out/ unchanged.
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

QSIM = ROOT / "data" / "units" / "loop2" / "replication" / "qsim801_vecoli2017_table1.csv"
TIMESCALE = ROOT / "data" / "timescale.csv"


def stage_base(name: str) -> float:
    with TIMESCALE.open() as f:
        for row in csv.reader(f):
            if row[2] == name:
                return float(row[3])
    raise KeyError(name)


def fig_support(path: Path) -> None:
    frame = contamination.build_frame("stage")
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    rows = []
    for well in frame.wells:
        for lo, hi in zip(well.older_lo, well.older_hi):
            rows.append((well.name, lo, hi))
    y = 0
    labels = []
    for name in sorted({r[0] for r in rows}):
        units = [r for r in rows if r[0] == name]
        for _, lo, hi in units:
            ax.plot([hi, lo], [y, y], color="#3b6ea8", lw=1.2, alpha=0.55)
        labels.append((y, f"Murzuq {name}: {len(units)} older cuttings, 0 triletes"))
        y += 1
    llo, lhi = stage_base("Rhuddanian"), stage_base("Sheinwoodian")
    ax.fill_betweenx([y - 0.4, y + 0.4], lhi, llo, color="#3b6ea8", alpha=0.85)
    labels.append((y, "Murzuq reference: 59 Llandovery cuttings, 51 with triletes"))
    y += 1.4
    with QSIM.open() as f:
        q = list(csv.DictReader(f))
    m = sum(int(r["cryptospore_marks"]) for r in q)
    qlo, qhi = stage_base("Sandbian"), stage_base("Dapingian")
    ax.fill_betweenx([y - 0.3, y + 0.3], qlo, qhi, facecolor="none", edgecolor="#c47f2c", hatch="///")
    labels.append((y, f"QSIM-801: {m} marks; late Dapingian–early Darriwilian (hatching: full-stage enclosure only)"))
    y += 1.4
    s4lo, s4hi = stage_base("Wuliuan"), stage_base("Stage 4")
    ax.fill_betweenx([y - 0.4, y + 0.4], s4lo, s4hi, color="#7a7a7a", alpha=0.6)
    labels.append((y, "Stage 4 forms: main E2 not accepted; inclusive assumption retained; no pre-M1 design"))
    y += 1.4
    labels.append((y, "M3: selected axes and qualitative fossil-free beds; no admitted searched-unit frame"))
    for x, lab in ((515.5, "M1 515.5"), (459.1, "M2 459.1"), (431.2, "M3 431.2")):
        ax.axvline(x, color="#a32020", lw=1.1, ls="--")
        ax.text(x, y + 1.45, lab, color="#a32020", ha="center", fontsize=8.5)
    for yy, lab in labels:
        ax.text(527, yy + 0.42, lab, va="bottom", ha="left", fontsize=7.4,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.6, "alpha": 0.9}, zorder=5)
    ax.set_xlim(528, 425)
    ax.set_ylim(-1, y + 2.0)
    ax.set_yticks([])
    ax.set_xlabel("Age (Ma); bars are age support, not occurrence dates")
    ax.spines[["left", "top", "right"]].set_visible(False)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200)
    plt.close(fig)


def fig_qsim(path: Path) -> None:
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
    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200)
    plt.close(fig)


def fig_mapping(path: Path) -> None:
    with (ROOT / "manuscript/mapping.csv").open() as f:
        rows = list(csv.DictReader(f))
    cols = [("material", "Observed material"), ("event", "Named event reading"),
            ("encounter", "Observation / inference"), ("persistence", "Trait persistence"),
            ("node", "Node interpretation")]
    fig, ax = plt.subplots(figsize=(8.5, 7.8))
    ax.set_xlim(-1.6, 6.35)
    ax.set_ylim(-.65, 5.55)
    ax.axis("off")
    for j, (_, title) in enumerate(cols):
        ax.text(-.15, 4.75-j*1.1, textwrap.fill(title, 15), ha="right", va="center", weight="bold", fontsize=10)
    for i, row in enumerate(rows):
        x = i*2.1
        ax.text(x+.96, 5.45, row["maximum"], ha="center", va="center", weight="bold", fontsize=11)
        for j, (key, _) in enumerate(cols):
            y = 4.75-j*1.1
            ax.add_patch(plt.Rectangle((x+.025, y-.45), 1.87, .9, facecolor=["#edf0f2", "#e8f0f5", "#f6ede4"][i],
                                       edgecolor="0.65", linewidth=.65))
            ax.text(x+.96, y, textwrap.fill(row[key], 25), ha="center", va="center", fontsize=9.5)
            if j<4:
                ax.annotate("", xy=(x+.96,y-.64), xytext=(x+.96,y-.46), arrowprops={"arrowstyle":"->", "color":"0.5"})
    fig.suptitle("Each node argument requires the full sequence of links", fontsize=12)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    fig_support(OUT / "fig1_support")
    fig_qsim(OUT / "fig3_qsim_share")
    fig_mapping(OUT / "fig4_mapping")
    inputs = [QSIM, TIMESCALE, ROOT / "models/f3/loop2/contamination.py", Path(__file__), ROOT / "manuscript/mapping.csv"]
    bound = contamination._input_hashes()
    bound.update({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
    outputs = sorted(OUT.glob("*.png")) + sorted(OUT.glob("*.pdf"))
    (OUT / "figures.json").write_text(json.dumps(
        {"inputs": bound, "outputs": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs},
         "status": "source-support-and-model-conditional-illustrations"}, indent=2) + "\n")


if __name__ == "__main__":
    main()
