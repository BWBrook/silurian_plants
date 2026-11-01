# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Manuscript figures 1 and 3 from declared source tables (Loop 2 sprint 2).

Figure 2 reuses the sprint-1 figures in models/f3/loop2/out/ unchanged.
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
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
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
    ax.fill_betweenx([y - 0.4, y + 0.4], qlo, qhi, color="#c47f2c", alpha=0.35)
    labels.append((y, f"QSIM-801: 20 samples, {m} cryptospore marks, 0 triletes (late Dapingian–early Darriwilian)"))
    y += 1.4
    s4lo, s4hi = stage_base("Wuliuan"), stage_base("Stage 4")
    ax.fill_betweenx([y - 0.4, y + 0.4], s4lo, s4hi, color="#7a7a7a", alpha=0.6)
    labels.append((y, "Cambrian Stage 4 cryptospore-like forms (charophyte affinity in all describing sources)"))
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
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    for h, c in ((1.0, "#1b4f8a"), (0.5, "#3b7dbf"), (0.25, "#77a7d8"), (0.1, "#b5cde8")):
        ax.plot(theta, (1 + h * theta) ** (-m), color=c, lw=1.8, label=f"h = {h}")
        ax.plot([(0.05 ** (-1 / m) - 1) / h], [0.05], "o", color=c, ms=4)
    ax.axhline(0.05, color="#555", lw=0.8, ls=":")
    ax.axvspan(1.0, theta[-1], color="#c47f2c", alpha=0.15)
    ax.text(1.05, 0.5, "triletes\ndominate\n(mid-Telychian\nonward)", fontsize=7.5, va="center")
    ax.set_xscale("log")
    ax.set_xlabel("Persistent trilete : cryptospore ratio θ in every sample")
    ax.set_ylabel(f"P(no triletes among ≥{m} examined units)")
    ax.legend(frameon=False, fontsize=8, title="relative recovery", title_fontsize=8)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{ext}"), dpi=200)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    fig_support(OUT / "fig1_support")
    fig_qsim(OUT / "fig3_qsim_share")
    inputs = [QSIM, TIMESCALE, ROOT / "models/f3/loop2/contamination.py", Path(__file__)]
    (OUT / "figures.json").write_text(json.dumps(
        {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}, indent=2) + "\n")


if __name__ == "__main__":
    main()
