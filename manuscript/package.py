"""Inventory the internal release candidate without copying private source texts."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def write(path, fields, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    files = {}

    def add(path, role):
        p = ROOT / path
        if not p.is_file():
            raise FileNotFoundError(path)
        if p.is_symlink() or "library" in p.relative_to(ROOT).parts:
            raise ValueError(f"private source or link cannot enter candidate: {path}")
        files[p] = role

    def collect(pattern, role):
        found = list(ROOT.glob(pattern))
        if not found:
            raise ValueError(f"empty candidate pattern: {pattern}")
        for p in found:
            if p.is_file() and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".tex", ".log"}:
                add(p.relative_to(ROOT), role)

    for name in ("claims.csv", "external_candidates.csv", "mapping.csv", "figures.py", "tables.py", "package.py",
                 "README.md", "authors.yaml", "Makefile", "settings/build.yaml", "csl/chicago-author-date.csl"):
        add("manuscript/"+name, "authored manuscript build, evidence ledger or reproduction code")
    collect("manuscript/text/*.md", "authored paper source: main, supplement, brief, agent paper")
    collect("manuscript/build/*.pdf", "rendered snapshot of the paper sources")
    collect("manuscript/figures/*", "authored figure or bound figure receipt")
    for name in ("references/dois.txt", "references/manual.yaml", "references/refs.yaml", "tools/refs.py", "tools/claims.py"):
        add(name, "bibliography ledger, generated bibliography or its builder")
    for name in ("loop1-close.md", "loop2-close.md", "loop2-sprint1-results.md", "loop2-sprint2-results.md",
                 "f3-shape.md", "pilot-traits.md", "charter.md", "decisions.md", "plan-loop3.md", "loop3-pilot.md",
                 "loop3-design.md", "loop3-results.md"):
        add("docs/"+name, "authored methods, interpretation or provenance")
    collect("docs/audits/2026-11-01-loop2-*.md", "authored independent review")
    collect("docs/audits/2026-11-01-loop2-*.json", "verification receipt")
    collect("docs/audits/2026-11-01-loop3-*", "authored independent review or verification receipt")
    collect("models/f3/loop3/*.py", "body-record method, simulation or figure code")
    collect("models/f3/loop3/README.md", "body-record method guide")
    collect("models/f3/loop3/out/*", "reviewed body-record output, superseded pilot output or receipt")
    collect("data/macro/*", "source-linked body-record inventory and adjudication")
    collect("models/f3/loop2/**/*", "new method, sensitivity or conditional diagnostic")
    collect("data/units/loop2/**/*", "source-linked factual extraction or authored evidence ledger")
    collect("models/f3/out/qual/*", "frozen qualification evidence")
    for receipt in (ROOT / "models/f3/out/qual").glob("*.json"):
        for path in json.loads(receipt.read_text())["binding"]["files"]:
            add("models/f3/designs/m2.toml" if path == "active_declaration" else path,
                "frozen qualification input; upstream terms retained")
    for path in ("models/f3/out/m2_results.csv", "data/units/e2-unit-rule.md", "data/pilot/specimens.csv",
                 "data/pilot/combinations.csv", "data/pilot/README.md", "data/units/sprint2/m1_admission.csv"):
        add(path, "source-linked result or evidence table")
    collect("data/pilot/hooper2026-asr/*", "derived upstream-output extraction; upstream terms retained")
    collect("models/pilot-asr/out/*", "previously checked model-conditional pilot output")
    for name in ("README.md", "renv.lock", "common.R", "asr_persistence.R", "asr_diagnostics.R", "summarise_chains.R"):
        add("models/pilot-asr/"+name, "previously checked pilot source; not rerun for Loop 2 close")
    records = []
    for path, role in sorted(files.items()):
        content = path.read_bytes()
        records.append(dict(path=str(path.relative_to(ROOT)), role=role, bytes=len(content),
                            sha256=hashlib.sha256(content).hexdigest(),
                            distribution="internal candidate; not released; retain source and upstream terms"))
    write(HERE / "package_manifest.csv", ["path", "role", "bytes", "sha256", "distribution"], records)
    write(HERE / "data-manifest.csv", ["path", "role", "distribution"], [
        dict(path="manuscript/package_manifest.csv", role=f"exact hashed inventory of {len(records)} candidate files",
             distribution="internal release candidate; public release remains Barry's decision"),
        dict(path="library/closed/", role="primary copyrighted PDFs and private source quotes for verification",
             distribution="private reproduction inputs; excluded from candidate inventory"),
        dict(path="data/external/local/deposits/hooper2026-spore-evolution/", role="upstream ASR archives used by the existing pilot",
             distribution="not included; fetch with data/external/scripts/deposits_fetch.py under original provenance and licence terms"),
    ])
    print(json.dumps({"candidate_files": len(records), "bytes": sum(r["bytes"] for r in records),
                      "private_source_files_included": 0}))


if __name__ == "__main__":
    main()
