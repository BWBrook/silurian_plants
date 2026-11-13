"""Inventory the internal release candidate without copying private source texts."""

import csv
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ARCHIVAL_RECEIPTS = {"models/f3/loop3/out/oman_receipt.json": "df805b2"}


def dependency_closure(seeds):
    pending = [(p, "product or declared analysis dependency") for p in sorted(seeds)]
    seen, edges = set(), []
    archive = json.loads((ROOT / "data/external/pbdb-snapshot.json").read_text())
    while pending:
        relative, parent = pending.pop()
        p = ROOT / relative
        if relative in seen:
            continue
        seen.add(relative)
        if relative in ARCHIVAL_RECEIPTS:
            availability = "archived provenance; regenerate at historical commit"
            locator = f"https://github.com/BWBrook/silurian_plants/blob/{ARCHIVAL_RECEIPTS[relative]}/{relative}"
        elif "library" in p.relative_to(ROOT).parts or "local" in p.relative_to(ROOT).parts:
            availability, locator = "excluded source; see source register", "docs/sources.md"
        elif relative == archive["path"]:
            availability, locator = "public immutable archive; bulk input excluded from Git", archive["url"]
        elif p.is_file() and not p.is_symlink():
            availability, locator = "candidate", ""
        else:
            raise FileNotFoundError(f"missing declared dependency {relative} from {parent}")
        edges.append({"path": relative, "declared_by": parent, "availability": availability,
                      "sha256": hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "",
                      "locator": locator})
        if availability != "candidate":
            continue
        if p.suffix == ".json":
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                continue
            maps = [data.get(k, {}) for k in ("inputs", "outputs")]
            maps += [data.get("binding", {}).get("files", {})]
            for mapping in maps:
                if not isinstance(mapping, dict):
                    continue
                for path in mapping:
                    path = "models/f3/designs/m2.toml" if path == "active_declaration" else path
                    if path.startswith(("data/", "models/", "tools/", "manuscript/", "docs/", "library/")):
                        pending.append((path, relative))
                    elif Path(path).suffix:
                        candidates = {q.resolve() for q in (p.parent / path, p.parent.parent / path)
                                      if q.is_file() and q.resolve().is_relative_to(ROOT)}
                        if len(candidates) != 1:
                            raise ValueError(f"unresolved or ambiguous receipt-local dependency {path} in {relative}")
                        pending.append((str(candidates.pop().relative_to(ROOT)), relative))
        elif p.suffix == ".py":
            for node in ast.walk(ast.parse(p.read_text())):
                names = []
                if isinstance(node, ast.Import):
                    names = [x.name for x in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for name in names:
                    for directory in (p.parent, ROOT / "tools", ROOT / "models/f3", ROOT / "models/f3/loop2"):
                        q = directory / (name.replace(".", "/") + ".py")
                        if q.is_file():
                            pending.append((str(q.relative_to(ROOT)), relative))
                            break
    return edges


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

    for name in ("claims.csv", "value-bindings.csv", "estimands.md", "makedoc.lock.json", "external_candidates.csv", "mapping.csv", "figures.py", "figures_main.py", "figures_abstract.py", "tables.py", "package.py",
                 "README.md", "authors.yaml", "Makefile", "settings/build.yaml", "csl/chicago-author-date.csl",
                 "csl/proceedings-of-the-royal-society-b.csl"):
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
    collect("models/f3/loop3/out/**/*", "reviewed body-record output, superseded pilot output or receipt")
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
    for path in ("Makefile", "tools/reproduce.py", "data/external/pbdb-snapshot.json",
                 "data/external/scripts/fetch_pbdb_snapshot.py", "data/spores/first_appearances.csv"):
        add(path, "public reproduction dependency")
    collect("docs/audits/2026-11-07*.md", "review and analysis disposition")
    collect("docs/audits/2026-11-08*.md", "follow-up source, numerical and semantic review")
    collect("docs/audits/2026-11-08*.json", "follow-up public reproduction receipt")
    collect("data/units/borenshult_review/*", "calibration reading dependency")
    add("models/f3/borenshult_review.py", "calibration reading screen")
    collect("models/f3/out/borenshult_review/*", "calibration reading screen output")
    seeds = {str(p.relative_to(ROOT)) for p in files}
    with (HERE / "claims.csv").open() as f:
        for row in csv.DictReader(f):
            for path in row["evidence"].split(";"):
                if (ROOT / path).is_dir():
                    seeds.update(str(p.relative_to(ROOT)) for p in (ROOT / path).rglob("*") if p.is_file())
                else:
                    seeds.add(path)
    closure = dependency_closure(seeds)
    for row in closure:
        if row["availability"] == "candidate":
            add(row["path"], "dependency closure: " + row["declared_by"])
    write(HERE / "dependency-manifest.csv", ["path", "declared_by", "availability", "sha256", "locator"],
          sorted(closure, key=lambda row: row["path"]))
    add("manuscript/dependency-manifest.csv", "declared dependency closure and excluded-source locations")
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
        dict(path=archive_path(), role="frozen all-taxa PBDB raw input to inventory/effort rebuild",
             distribution="CC0; exact bytes publicly archived at https://doi.org/10.5281/zenodo.24028289; restore with make fetch-pbdb"),
    ])
    print(json.dumps({"candidate_files": len(records), "bytes": sum(r["bytes"] for r in records),
                      "private_source_files_included": 0}))


def archive_path():
    return json.loads((ROOT / "data/external/pbdb-snapshot.json").read_text())["path"]


if __name__ == "__main__":
    main()
