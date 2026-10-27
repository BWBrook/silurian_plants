"""Chunked Codex verification jobs for the literature library (phase 2). Runs on the Mac.

Usage (from data/external/):
  python3 scripts/library_codex.py prep-cited                 # job `cited`: is each cited DOI the work the project meant
  python3 scripts/library_codex.py prep-screen                # job `screen`: independent re-screen of priority_spores + 200 excluded
  python3 scripts/library_codex.py prep-identity --excerpts F # job `identity`: fetched text vs expected metadata
  python3 scripts/library_codex.py prep-quarantine --excerpts F
  python3 scripts/library_codex.py run JOB [--only 1,3]       # launch chunks in parallel, wait, then check
  python3 scripts/library_codex.py check JOB                  # coverage and enum check, merge to results.json, list gaps
  python3 scripts/library_codex.py rerun JOB                  # rerun items missing from the merged results, as extra chunks

Each job lives in local/library/codex/<JOB>/ (git-ignored): schema.json, chunk_NN.json (input), prompt_NN.txt,
out_NN.json (Codex's reply), results.json (merged). A chunk is about 100 items; the prompt states the expected count and
`check` verifies every id came back once (a long Codex job once returned 6 of 144 items and still exited 0).
Codex runs read-only in the job folder with no keys, no git and no web search. `run` goes through
~/.claude/bin/codex-delegate (stdin closed, read-only, timeout, --expect coverage, cost log in
~/.local/state/codex-delegate/jobs.jsonl, label silurian-library-<job>-<chunk>). The `cited` and `screen` jobs were first
run with raw `codex exec -m MODEL -c model_reasoning_effort=high -s read-only -C JOBDIR --skip-git-repo-check --ephemeral
--output-schema ... -o ... PROMPT < /dev/null`.
"""

import argparse
import csv
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXT = ROOT / "data" / "external"
LIB = EXT / "library"
CODEX = EXT / "local" / "library" / "codex"
csv.field_size_limit(sys.maxsize)
CHUNK = 104

MODELS = {"cited": "gpt-6.1-terra", "identity": "gpt-6.1-terra", "quarantine": "gpt-6.1-terra", "screen": "gpt-6.1-sol"}

REGION_NAMES = ["Laurentia (incl. Scotland, Svalbard)", "Avalonia, Baltica, peri-Gondwanan Europe", "North Africa",
                "Arabia, Iran, Turkey", "South America", "South Africa, Australia, other Gondwana",
                "South China, Tarim, E Asia, Siberia, Kazakhstania", "Unassigned"]


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def schema(item_props, required):
    for v in item_props.values():
        if "enum" in v and "type" not in v:
            v["type"] = "string"
    return {"type": "object", "additionalProperties": False, "required": ["results"], "properties": {"results": {
        "type": "array", "items": {"type": "object", "additionalProperties": False, "required": required,
                                   "properties": item_props}}}}


def chunks_of(items, size=CHUNK):
    n = max(1, round(len(items) / size))
    k = -(-len(items) // n)
    return [items[i:i + k] for i in range(0, len(items), k)]


def write_job(job, items, sch, prompt_for, extra=None):
    d = CODEX / job
    d.mkdir(parents=True, exist_ok=True)
    for old in list(d.glob("chunk_*.json")) + list(d.glob("prompt_*.txt")) + list(d.glob("out_*.json")):
        old.unlink()
    (d / "schema.json").write_text(json.dumps(sch, indent=1))
    manifest = {"job": job, "model": MODELS[job], "chunks": {}}
    for i, part in enumerate(chunks_of(items), 1):
        name = f"{i:02d}"
        (d / f"chunk_{name}.json").write_text(json.dumps(part, ensure_ascii=False, indent=1))
        (d / f"prompt_{name}.txt").write_text(prompt_for(name, len(part)))
        manifest["chunks"][name] = [x["id"] for x in part]
    manifest["expected"] = sum(len(v) for v in manifest["chunks"].values())
    manifest.update(extra or {})
    (d / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"{job}: {manifest['expected']} items in {len(manifest['chunks'])} chunks -> {d}")


# ------------------------------------------------------------------ job builders

def prep_cited():
    works = {r["openalex_id"]: r for r in read_tsv(LIB / "works.tsv")}
    res = read_tsv(LIB / "cited_dois_resolution.tsv")
    doi_rx = re.compile(r"\b10\.\d{4,9}/[^\s\"]+")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from library_cited_seed import clean_doi
    lines = {}
    for path in sorted((ROOT / "taxa").glob("*.md")) + sorted((ROOT / "docs").glob("*.md")):
        text = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(text):
            for raw in doi_rx.findall(line):
                ctx = line.strip()
                if re.match(r"doi:", ctx) and i > 0:
                    ctx = text[i - 1].strip() + " " + ctx
                lines.setdefault(clean_doi(raw).lower(), []).append((str(path.relative_to(ROOT)), ctx[:600]))
    by_work = {}
    for r in res:
        by_work.setdefault(r["openalex_id"], []).append(r["doi"])
    items = []
    for wid in sorted(by_work):
        w = works[wid]
        cites, seen = [], set()
        for doi in by_work[wid]:
            for f, ctx in lines.get(doi, []):
                key = re.sub(r"\s+", " ", ctx)
                if key not in seen and len(cites) < 4:
                    seen.add(key)
                    cites.append({"file": f, "line": ctx})
        items.append({"id": wid, "cited_dois": by_work[wid], "project_citation_lines": cites,
                      "openalex": {"title": w["title"], "first_authors": w["first_author"], "year": w["year"],
                                   "venue": w["venue"], "type": w["type"], "doi": w["doi"]}})
    sch = schema({"id": {"type": "string"}, "verdict": {"enum": ["same_work", "different_work", "unclear"]},
                  "note": {"type": "string"}}, ["id", "verdict", "note"])

    def prompt(name, n):
        return (f"Read chunk_{name}.json in the current folder: a JSON array of exactly {n} items. Each item is a work that a research "
                "project cited by DOI. 'project_citation_lines' are the project's own lines citing that DOI (author, year, title, venue "
                "as the project wrote them); 'openalex' is the record OpenAlex returned for the DOI (title, first-author surnames, year, venue, type). "
                "For every item decide whether the OpenAlex record is the same publication as the one the project's line cites: "
                "same_work (same title and authors; differences of capitalisation, punctuation, subtitle, spelling, journal abbreviation, "
                "translated or transliterated title, or a year that differs by one are fine), different_work (a clearly different "
                "publication, for example a different title or authors, or a dataset, supplement, erratum, review stub or preprint of something else), or "
                "unclear (the lines do not allow a decision). Give one short sentence of evidence in 'note'. Use only the file; do not "
                f"search the web. Reply with JSON {{\"results\": [...]}} holding exactly {n} objects, one per input id, with the id copied unchanged.")

    write_job("cited", items, sch, prompt)


def prep_screen():
    exp = json.loads((CODEX / "screen_export.json").read_text())
    scr = {r["openalex_id"]: r for r in exp}
    rules = [r for r in read_tsv(LIB / "screen.tsv") if r["kind"] == "rule"]
    rules_text = "\n".join(f"{r['rule']}: {r['reason']}" for r in rules)
    include = {}
    for r in exp:
        if r["decision"].startswith("include") and r["canonical_id"] not in include:
            include[r["canonical_id"]] = r["openalex_id"]
    prio_ids = sorted(include.values())
    excluded = sorted(r["openalex_id"] for r in exp if r["decision"] == "exclude")
    rng = random.Random(20261027)
    sample = sorted(rng.sample(excluded, 200))
    ids = prio_ids + sample
    rng.shuffle(ids)
    key = {"priority_spores": prio_ids, "excluded_sample": sample, "seed": 20261027, "excluded_pool": len(excluded)}
    items = []
    for w in ids:
        r = scr[w]
        items.append({"id": w, "year": r["year"], "type": r["type"], "rule_hit": r["rule"], "title": r["title"],
                      "abstract": (r["abstract"] or "(no abstract in OpenAlex)")[:1800]})
    sch = schema({"id": {"type": "string"}, "decision": {"enum": ["include", "include_borderline", "exclude"]},
                  "reason_class": {"enum": ["occurrence", "review_or_synthesis", "ultrastructure", "in_situ_only", "outside_period",
                                            "middle_late_devonian_only", "tremadocian_floian_only", "marine_palynomorphs_only",
                                            "methods_catalogue_or_geochemistry", "not_a_spore_paper", "other"]},
                  "region": {"enum": REGION_NAMES + [""]}, "reason": {"type": "string"}},
                 ["id", "decision", "reason_class", "region", "reason"])

    def prompt(name, n):
        return ("You are an independent second screener for a literature compilation of dispersed-spore and cryptospore occurrence papers "
                f"(Dapingian to Emsian, 470 to 393 Ma). Read chunk_{name}.json in the current folder: a JSON array of exactly {n} candidate papers, each with "
                "year, type, rule_hit (which candidate rule found it), title and abstract. Decide from the title and abstract alone, under these rules:\n\n"
                f"{rules_text}\n\n"
                "Regions are exactly: " + "; ".join(REGION_NAMES) + ". Give region only for include and include_borderline (otherwise an empty "
                "string). 'reason' is one short phrase. Do not search the web and do not guess beyond the text. "
                f"Reply with JSON {{\"results\": [...]}} holding exactly {n} objects, one per input id, ids copied unchanged.")

    write_job("screen", items, sch, prompt, {"key_file": "key.json"})
    (CODEX / "screen" / "key.json").write_text(json.dumps(key, indent=1))
    print(f"screen: {len(prio_ids)} priority + {len(sample)} excluded sampled of {len(excluded)}")


def prep_identity(job, excerpts_file):
    ex = json.loads(Path(excerpts_file).read_text())
    works = {r["openalex_id"]: r for r in read_tsv(LIB / "works.tsv")}
    extra_path = CODEX / "identity_extra.json"  # works with no OpenAlex record (pseudo ids from library_open_unread.py)
    extra = json.loads(extra_path.read_text()) if extra_path.exists() else {}
    items = []
    for e in ex:
        wid = e["id"].split("|")[0]
        w = works.get(wid) or {"title": extra[wid]["title"], "first_author": extra[wid]["first_authors"], "year": extra[wid]["year"],
                               "venue": extra[wid]["venue"], "doi": extra[wid].get("doi", "")}
        items.append({"id": e["id"], "expected": {"title": w["title"], "first_authors": w["first_author"], "year": w["year"],
                                                  "venue": w["venue"], "doi": w["doi"]}, "text_start": e["text"]})
    sch = schema({"id": {"type": "string"}, "verdict": {"enum": ["same_work" if job == "quarantine" else "match",
                                                                  "different_work" if job == "quarantine" else "mismatch",
                                                                  "unreadable" if job == "quarantine" else "unclear"]},
                  "evidence": {"type": "string"}}, ["id", "verdict", "evidence"])
    if job == "quarantine":
        what = ("Each item is a PDF that an automated downloader rejected because its first pages did not seem to contain the expected title. "
                "Decide whether the PDF is nevertheless the expected publication: same_work (title, authors or journal in the text start identify "
                "it as the expected work, for example a different title rendering, translated title or OCR noise), different_work (clearly another "
                "publication, such as an unrelated article, a whole issue or a cover page of another work), or unreadable (no usable text, "
                "garbled, or too short to judge). If the PDF is the supplementary material of the expected work, answer same_work and "
                "start the evidence with 'SUPPLEMENT:'; if it is the main text, start it with 'MAIN TEXT:'.")
    else:
        what = ("Each item is an open-access PDF whose text the downloader accepted by a loose title-word check. Decide whether the start of the "
                "text is the expected publication: match (title, authors, year or journal in the text start fit the expected metadata; "
                "differences of rendering, translation, preprint or accepted-manuscript versions of the same article are fine), mismatch (clearly "
                "another publication or a different document, such as a whole issue, volume front matter, a review of another work or an "
                "unrelated paper), or unclear (cannot tell, for example garbled text or a cover page with no bibliographic data).")

    def prompt(name, n):
        return (f"Read chunk_{name}.json in the current folder: a JSON array of exactly {n} items, each with 'expected' metadata (title, "
                f"first-author surnames, year, venue, DOI) and 'text_start' (the first pages of the PDF as extracted text). {what} "
                "Give one short sentence of evidence in 'evidence'. Use only the file; do not search the web. "
                f"Reply with JSON {{\"results\": [...]}} holding exactly {n} objects, one per input id, ids copied unchanged.")

    write_job(job, items, sch, prompt)


# ------------------------------------------------------------------ run and check

def run_chunks(job, names):
    """Launch chunks in parallel through the shared wrapper ~/.claude/bin/codex-delegate (stdin closed, read-only, timeout,
    --expect coverage, cost log). The `cited` and `screen` jobs of 2026-10-27 ran earlier with raw `codex exec`."""
    d = CODEX / job
    man = json.loads((d / "manifest.json").read_text())
    role = "sol" if "sol" in man["model"] else "terra"
    wrapper = str(Path.home() / ".claude" / "bin" / "codex-delegate")
    procs = []
    for name in names:
        n = len(man["chunks"][name])
        cmd = [wrapper, "-m", role, "-e", "high", "-f", str(d / f"prompt_{name}.txt"), "--schema", str(d / "schema.json"),
               "--expect", str(n), "--count", ".results | length", "-o", str(d / f"out_{name}.json"), "-C", str(d),
               "--label", f"silurian-library-{job}-{name}"]
        log = open(d / f"run_{name}.log", "w")
        t0 = time.time()
        procs.append((name, subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT), t0, log))
        print(f"{job} chunk {name}: started ({role}, expect {n})", flush=True)
    for name, p, t0, log in procs:
        rc = p.wait()
        log.close()
        (d / f"time_{name}.txt").write_text(f"{time.time() - t0:.0f} s, exit {rc}\n")
        print(f"{job} chunk {name}: exit {rc} after {time.time() - t0:.0f} s", flush=True)


def check(job):
    d = CODEX / job
    man = json.loads((d / "manifest.json").read_text())
    sch = json.loads((d / "schema.json").read_text())
    enums = {k: v.get("enum") for k, v in sch["properties"]["results"]["items"]["properties"].items() if v.get("enum")}
    got, problems = {}, []
    for out in sorted(d.glob("out_*.json")):
        try:
            data = json.loads(out.read_text())["results"]
        except Exception as e:
            problems.append(f"{out.name}: unreadable ({type(e).__name__})")
            continue
        for r in data:
            if r["id"] in got:
                problems.append(f"{out.name}: duplicate {r['id']}")
            bad = [k for k, v in enums.items() if r.get(k) not in v]
            if bad:
                problems.append(f"{out.name}: {r['id']} bad {bad}")
                continue
            got[r["id"]] = r
    expected = [i for ids in man["chunks"].values() for i in ids]
    for name in man["chunks"]:
        have = sum(1 for i in man["chunks"][name] if i in got)
        print(f"  chunk {name}: {have}/{len(man['chunks'][name])}")
    extra = [i for i in got if i not in set(expected)]
    missing = [i for i in expected if i not in got]
    (d / "results.json").write_text(json.dumps(list(got.values()), ensure_ascii=False, indent=1))
    (d / "gaps.json").write_text(json.dumps(missing))
    print(f"{job}: {len(got)}/{len(expected)} returned; missing {len(missing)}; unexpected {len(extra)}; problems {len(problems)}")
    for p in problems[:10]:
        print("   ", p)
    return missing


def rerun(job):
    d = CODEX / job
    missing = check(job)
    if not missing:
        return
    man = json.loads((d / "manifest.json").read_text())
    all_items = {}
    for f in d.glob("chunk_*.json"):
        for x in json.loads(f.read_text()):
            all_items[x["id"]] = x
    base = max(int(k) for k in man["chunks"] if k.isdigit()) if any(k.isdigit() for k in man["chunks"]) else 0
    names = []
    for j, part in enumerate(chunks_of([all_items[i] for i in missing]), 1):
        name = f"g{base + j}"
        (d / f"chunk_{name}.json").write_text(json.dumps(part, ensure_ascii=False, indent=1))
        template = (d / "prompt_01.txt").read_text()
        template = re.sub(r"chunk_\d+\.json", f"chunk_{name}.json", template)
        template = re.sub(r"exactly \d+", f"exactly {len(part)}", template)
        (d / f"prompt_{name}.txt").write_text(template)
        man["chunks"][name] = [x["id"] for x in part]
        names.append(name)
    (d / "manifest.json").write_text(json.dumps(man, indent=1))
    run_chunks(job, names)
    check(job)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("prep-cited", "prep-screen"):
        sub.add_parser(c)
    for c in ("prep-identity", "prep-quarantine"):
        p = sub.add_parser(c)
        p.add_argument("--excerpts", required=True)
    for c in ("run", "check", "rerun"):
        p = sub.add_parser(c)
        p.add_argument("job")
        if c == "run":
            p.add_argument("--only")
    a = ap.parse_args()
    if a.cmd == "prep-cited":
        prep_cited()
    elif a.cmd == "prep-screen":
        prep_screen()
    elif a.cmd == "prep-identity":
        prep_identity("identity", a.excerpts)
    elif a.cmd == "prep-quarantine":
        prep_identity("quarantine", a.excerpts)
    elif a.cmd == "run":
        man = json.loads((CODEX / a.job / "manifest.json").read_text())
        names = a.only.split(",") if a.only else [k for k in man["chunks"] if not k.startswith("g")]
        run_chunks(a.job, names)
        check(a.job)
    elif a.cmd == "check":
        check(a.job)
    else:
        rerun(a.job)


if __name__ == "__main__":
    main()
