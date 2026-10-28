# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///
"""Aggregates out/recovery_grid.csv into out/recovery_summary.csv and prints the README tables.

    uv run models/f3/report.py

One summary row per channel set x estimator x growth, over the 24 scenarios that remain after fixing
growth (3 origination windows x 2 efforts x 4 preservation levels). The printed pass tables pool growth
into families.
"""

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "out"
ESTIMATORS = ("classical", "griwm", "ramp_logistic", "ramp_logistic_kfree", "ramp_bd")
CHANNELS = ("spores", "bodies", "joint")
FAMILIES = {
    "constant": ("constant",),
    "logistic, capacity right": ("logistic_r0.15", "logistic_r0.3", "logistic_r0.6"),
    "logistic, capacity wrong": ("logistic_r0.3_k30", "logistic_r0.3_k300"),
    "birth-death": ("bd_g0.05", "bd_g0.10"),
}
SUMMARY_COLUMNS = [
    "channels", "estimator", "growth", "n_scenarios", "n_pass", "n_usable", "min_coverage", "median_coverage",
    "median_bias_ma", "min_bias_ma", "max_bias_ma", "median_width_ma", "mean_frac_unbounded",
]


def read_grid(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def number(row: dict, key: str) -> float:
    return float(row[key]) if row[key] != "" else np.nan


def coverage(row: dict) -> float:
    key = {"classical": "coverage_upper", "griwm": "coverage_calibrated"}.get(row["estimator"], "coverage_interval")
    return number(row, key)


def summarise(rows: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[(r["channels"], r["estimator"], r["growth"])].append(r)
    out = []
    for (channels, estimator, growth), g in groups.items():
        cov = np.array([coverage(r) for r in g])
        bias = np.array([number(r, "median_bias_ma") for r in g])
        out.append({
            "channels": channels, "estimator": estimator, "growth": growth, "n_scenarios": len(g),
            "n_pass": sum(r["passes"] == "True" for r in g), "n_usable": sum(r["usable"] == "True" for r in g),
            "min_coverage": np.nanmin(cov), "median_coverage": np.nanmedian(cov), "median_bias_ma": np.nanmedian(bias),
            "min_bias_ma": np.nanmin(bias), "max_bias_ma": np.nanmax(bias),
            "median_width_ma": np.nanmedian([number(r, "median_width_ma") for r in g]),
            "mean_frac_unbounded": np.nanmean([number(r, "frac_unbounded") for r in g]),
        })
    order = lambda r: (CHANNELS.index(r["channels"]), ESTIMATORS.index(r["estimator"]))
    return sorted(out, key=order)


def write_summary(summary: list[dict], path: Path) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for r in summary:
            writer.writerow({k: (round(float(v), 3) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})


def pass_table(summary: list[dict], key: str) -> str:
    lines = ["| channels | estimator | " + " | ".join(FAMILIES) + " |", "|---|---|" + "---|" * len(FAMILIES)]
    for channels in CHANNELS:
        for estimator in ESTIMATORS:
            cells = []
            for growths in FAMILIES.values():
                sel = [r for r in summary if r["channels"] == channels and r["estimator"] == estimator and r["growth"] in growths]
                cells.append(f"{sum(r[key] for r in sel)}/{sum(r['n_scenarios'] for r in sel)}")
            lines.append(f"| {channels} | {estimator} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def criterion_table(rows: list[dict], criterion: str) -> str:
    """Scenarios meeting one criterion alone: 'coverage' (>= 0.90) or 'bias' (|median bias| < 2 Myr)."""
    meets = {
        "coverage": lambda r: coverage(r) >= 0.90,
        "bias": lambda r: abs(number(r, "median_bias_ma")) < 2.0,
    }[criterion]
    lines = ["| channels | estimator | " + " | ".join(FAMILIES) + " |", "|---|---|" + "---|" * len(FAMILIES)]
    for channels in CHANNELS:
        for estimator in ESTIMATORS:
            cells = []
            for growths in FAMILIES.values():
                sel = [r for r in rows if r["channels"] == channels and r["estimator"] == estimator and r["growth"] in growths]
                cells.append(f"{sum(meets(r) for r in sel)}/{len(sel)}")
            lines.append(f"| {channels} | {estimator} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def upper_table(rows: list[dict], effort: str, level: str) -> str:
    growths = list(dict.fromkeys(r["growth"] for r in rows))
    estimators = [e for e in ESTIMATORS if e != "griwm"]
    lines = ["| growth | " + " | ".join(estimators) + " |", "|---|" + "---|" * len(estimators)]
    for growth in growths:
        cells = []
        for estimator in estimators:
            sel = [r for r in rows if r["growth"] == growth and r["estimator"] == estimator and r["channels"] == "joint" and r["effort"] == effort and r["level"] == level]
            cells.append(f"{np.median([number(r, 'coverage_upper') for r in sel]):.2f} / {np.median([number(r, 'median_upper_excess_ma') for r in sel]):+.1f}")
        lines.append(f"| {growth} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def count_table(rows: list[dict]) -> str:
    lines = ["| level | spores target | spores realised (median of cell medians) | bodies target | bodies realised |", "|---|---|---|---|---|"]
    for level in dict.fromkeys(r["level"] for r in rows):
        sel = [r for r in rows if r["level"] == level]
        lines.append(f"| {level} | {sel[0]['target_spores']} | {np.median([number(r, 'median_n_spores') for r in sel]):.0f} | {sel[0]['target_bodies']} | {np.median([number(r, 'median_n_bodies') for r in sel]):.0f} |")
    return "\n".join(lines)


def detail_table(rows: list[dict], effort: str, level: str) -> str:
    growths = list(dict.fromkeys(r["growth"] for r in rows))
    lines = ["| growth | " + " | ".join(f"{e}" for e in ESTIMATORS) + " |", "|---|" + "---|" * len(ESTIMATORS)]
    for growth in growths:
        cells = []
        for estimator in ESTIMATORS:
            sel = [r for r in rows if r["growth"] == growth and r["estimator"] == estimator and r["channels"] == "joint" and r["effort"] == effort and r["level"] == level]
            cov = np.median([coverage(r) for r in sel])
            bias = np.median([number(r, "median_bias_ma") for r in sel])
            unb = np.median([number(r, "frac_unbounded") for r in sel])
            width = np.median([number(r, "median_width_ma") for r in sel])
            cells.append(f"{cov:.2f} / {bias:+.1f} / {width:.1f}" + (f" / {unb:.2f}" if estimator.startswith("ramp") else ""))
        lines.append(f"| {growth} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def unbounded_table(rows: list[dict], estimator: str, effort: str) -> str:
    growths = list(dict.fromkeys(r["growth"] for r in rows))
    levels = list(dict.fromkeys(r["level"] for r in rows))
    lines = ["| growth | " + " | ".join(levels) + " |", "|---|" + "---|" * len(levels)]
    for growth in growths:
        cells = []
        for level in levels:
            by_channel = []
            for channels in CHANNELS:
                sel = [number(r, "frac_unbounded") for r in rows if r["growth"] == growth and r["estimator"] == estimator and r["effort"] == effort and r["level"] == level and r["channels"] == channels]
                by_channel.append(f"{np.mean(sel):.2f}")
            cells.append("/".join(by_channel))
        lines.append(f"| {growth} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    rows = read_grid(OUT / "recovery_grid.csv")
    summary = summarise(rows)
    write_summary(summary, OUT / "recovery_summary.csv")
    print("Scenarios passing the plan criteria, by channels, estimator and growth:\n")
    print(pass_table(summary, "n_pass"))
    print("\nScenarios usable (pass and identified):\n")
    print(pass_table(summary, "n_usable"))
    print("\nScenarios meeting the coverage criterion alone (own interval, at least 0.90):\n")
    print(criterion_table(rows, "coverage"))
    print("\nScenarios meeting the bias criterion alone (|median bias| under 2 Myr):\n")
    print(criterion_table(rows, "bias"))
    print("\nRecord counts:\n")
    print(count_table(rows))
    for effort, level in (("real", "mid"), ("real", "high")):
        print(f"\nJoint fit, {effort} effort, {level} preservation (median over windows): coverage / median bias Myr / median width Myr / fraction unbounded:\n")
        print(detail_table(rows, effort, level))
    for effort, level in (("real", "mid"), ("real", "high")):
        print(f"\nUpper limit, joint fit, {effort} effort, {level} preservation: coverage of hi >= T0 / median (hi - T0) in Myr:\n")
        print(upper_table(rows, effort, level))
    for estimator in ("ramp_logistic", "ramp_logistic_kfree", "ramp_bd"):
        print(f"\nFraction of unbounded profiles, {estimator}, real effort, spores/bodies/joint (mean over origination windows):\n")
        print(unbounded_table(rows, estimator, "real"))
    print(f"\n{len(summary)} summary rows -> {OUT / 'recovery_summary.csv'}")


if __name__ == "__main__":
    main()
