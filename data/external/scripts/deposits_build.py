#!/usr/bin/env python3
"""Copy the nectar mirror of the deposits to the Mac and write deposits/MANIFEST.tsv.

Run on the Mac (needs ssh and rsync access to nectar):
    uv run --with openpyxl --with xlrd python3 deposits_build.py

Placement rule (task brief): a file goes to data/external/deposits/<id>/ when the licence allows redistribution
(CC0, CC BY, OGL, public domain, MIT, Apache; CC BY-NC and the data.bris NC Government Licence are tracked but flagged)
and the file is under 20 MB; every other file goes to data/external/local/deposits/<id>/ (git-ignored).
Europe PMC supplementaryFiles zips stay whole on the mirror host; their non-image members are extracted here, and
the small zips that carry data tables are opened one level (CAT[...]["open_nested"]).
Every copied file is re-hashed after the copy and must match the sha256 the mirroring tool recorded.
"""
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REMOTE = "nectar"
RAW = "/data/codex/silurian_plants/raw/deposits"
EXT = Path(__file__).resolve().parents[1]
DEP, LOC = EXT / "deposits", EXT / "local" / "deposits"
LIMIT = 20_000_000
EXTRACTED = "2026-10-27"
RUN = "scripts/deposits_mirror_run.sh"

sys.path.insert(0, str(Path(__file__).parent))
from deposits_catalogue import CAT  # noqa: E402

csv.field_size_limit(1 << 30)


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw).stdout


def remote_manifests():
    code = (
        "import json,glob\n"
        f"R='{RAW}'\n"
        "out=[]\n"
        "for m in sorted(glob.glob(R+'/*/*/raw/*/MANIFEST.json')):\n"
        "    p=m[len(R)+1:].split('/')\n"
        "    out.append({'id':p[0],'stamp':p[1],'vdir':p[3],'manifest':json.load(open(m))})\n"
        "print(json.dumps(out))\n"
    )
    return json.loads(sh(["ssh", REMOTE, "python3", "-"], input=code))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def count_rows(path):
    p = Path(path)
    name = p.name.lower()
    try:
        if name.endswith((".csv", ".tsv")):
            with open(p, newline="", encoding="utf-8-sig", errors="replace") as f:
                reader = csv.reader(f, delimiter="\t" if name.endswith(".tsv") else ",")
                return str(max(sum(1 for _ in reader) - 1, 0))
        if name.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            return "; ".join(f"{ws.title}: {ws.max_row}" for ws in wb.worksheets)
        if name.endswith(".xls"):
            import xlrd
            wb = xlrd.open_workbook(p)
            return "; ".join(f"{s.name}: {s.nrows}" for s in wb.sheets())
    except Exception as e:  # noqa: BLE001
        return f"unreadable ({type(e).__name__})"
    return ""


def nested_dir(zip_name, names):
    """Where a nested zip's members go: beside the zip when they share one top-level folder, else in a folder named for the zip."""
    members = [n for n in names if n and not n.startswith("__MACOSX") and not n.endswith("/")]
    tops = {n.split("/")[0] for n in members}
    single = len(tops) == 1 and all("/" in n for n in members)
    return Path(zip_name).parent if single else Path(zip_name[:-4])


def describe(dep_id, name):
    c = CAT[dep_id]
    for pat, text in c.get("files", []):
        if re.search(pat, name):
            return text
    return c["desc"]


def dep_of(path):
    parts = path.split("/")
    return parts[2] if parts[0] == "local" else parts[1]


class Builder:
    def __init__(self):
        self.rows = []
        self.placed = {}
        self.folds = {}

    def base(self, dep_id, size):
        ok = CAT[dep_id]["policy"] in ("track", "track-nc") and size < LIMIT
        return (DEP if ok else LOC) / dep_id

    def emit(self, dep_id, rel, data, source, version, licence, desc_name, note="", script_extra=""):
        out = self.base(dep_id, len(data)) / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        self.record(dep_id, out, source, version, licence, desc_name, note, script_extra)
        return out

    def record(self, dep_id, out, source, version, licence, desc_name, note="", script_extra=""):
        if CAT[dep_id].get("fold"):
            self.folds.setdefault((dep_id, out.relative_to(EXT).parts[0] == "local"), []).append(
                (out.relative_to(EXT).as_posix(), sha256_of(out), out.stat().st_size))
            return
        desc = describe(dep_id, desc_name) + note
        script = f"{RUN} item_{CAT[dep_id]['item']}" + (f"; {script_extra}" if script_extra else "")
        flag = " [NC licence: tracked and flagged]" if CAT[dep_id]["policy"] == "track-nc" and out.is_relative_to(DEP) else ""
        self.rows.append([out.relative_to(EXT).as_posix(), desc + flag, source, version, licence, script,
                          count_rows(out), sha256_of(out), EXTRACTED])
        self.placed.setdefault(dep_id, []).append({"path": out.relative_to(EXT).as_posix(), "size": out.stat().st_size})


def main():
    only = set(sys.argv[1:])
    unknown = only - set(CAT)
    if unknown:
        raise SystemExit(f"unknown deposit ids: {sorted(unknown)}")
    ids = [d for d in CAT if not only or d in only]
    manifest = DEP / "MANIFEST.tsv"
    kept = []
    if only and manifest.exists():
        with open(manifest, newline="") as f:
            kept = [r for r in csv.reader(f, delimiter="\t")][1:]
        kept = [r for r in kept if dep_of(r[0]) not in only]
    for d in ids:
        for base in (DEP, LOC):
            if (base / d).exists():
                shutil.rmtree(base / d)
    by_id = {}
    for m in remote_manifests():
        by_id.setdefault(m["id"], []).append(m)
    b = Builder()
    tmp = Path(tempfile.mkdtemp(prefix="deposits_build_"))
    for dep_id in ids:
        snaps = by_id.get(dep_id)
        if not snaps:
            print("NOT MIRRORED:", dep_id)
            continue
        multi = sum(len(s["manifest"]["files"]) > 0 for s in snaps) > 1 and len({s["vdir"] for s in snaps}) > 1
        prov = []
        for s in snaps:
            man = s["manifest"]
            prov.append({"stamp": s["stamp"], "version_dir": s["vdir"], **man})
            sub = s["vdir"].rsplit("_", 1)[-1] if multi else ""
            src_dir = f"{RAW}/{dep_id}/{s['stamp']}/raw/{s['vdir']}"
            ver = man.get("version") or man["record"]
            vlabel = f"{man['provider']} {man.get('doi') or man['record']}, version {ver}; mirrored {man['retrieved_utc'][:16]}Z"
            for f in man["files"]:
                key, url = f["key"], f["url"]
                dest_rel = Path(sub) / key if sub else Path(key)
                if re.fullmatch(r"PMC\d+_supplementaryFiles\.zip", key):
                    zdir = tmp / dep_id
                    zdir.mkdir(exist_ok=True)
                    sh(["rsync", "-a", f"{REMOTE}:{src_dir}/{key}", f"{zdir}/"])
                    if sha256_of(zdir / key) != f["sha256"]:
                        raise SystemExit(f"sha256 mismatch for {key}")
                    with zipfile.ZipFile(zdir / key) as z:
                        for info in z.infolist():
                            n = info.filename
                            if n.endswith("/") or n.lower().endswith((".jpg", ".gif", ".png")) or n.endswith("__index.html"):
                                continue
                            data = z.read(n)
                            note = f" [extracted from {key} (sha256 {f['sha256'][:12]}.., kept whole on deep-server)]"
                            b.emit(dep_id, Path(sub) / n if sub else n, data, url, vlabel, man["license"], n, note, "scripts/deposits_build.py")
                            nested = CAT[dep_id].get("open_nested")
                            if nested and n.lower().endswith(".zip") and re.search(nested, n) and len(data) < LIMIT:
                                with zipfile.ZipFile(io.BytesIO(data)) as zz:
                                    root = nested_dir(n, zz.namelist())
                                    for zi in zz.infolist():
                                        if zi.filename.endswith("/") or "__MACOSX" in zi.filename or Path(zi.filename).name.startswith("."):
                                            continue
                                        rel2 = root / zi.filename
                                        b.emit(dep_id, Path(sub) / rel2 if sub else rel2, zz.read(zi.filename), url, vlabel, man["license"],
                                               zi.filename, f" [opened from {n}, which came from {key}]", "scripts/deposits_build.py")
                    continue
                dest = b.base(dep_id, f["size"]) / dest_rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                sh(["rsync", "-a", f"{REMOTE}:{src_dir}/{key}", str(dest)])
                if sha256_of(dest) != f["sha256"]:
                    raise SystemExit(f"sha256 mismatch after copy: {dest}")
                b.record(dep_id, dest, url, vlabel, man["license"], key)
                nested = CAT[dep_id].get("open_nested")
                if nested and key.lower().endswith(".zip") and re.search(nested, key) and f["size"] < LIMIT:
                    with zipfile.ZipFile(dest) as zz:
                        root = nested_dir(key, zz.namelist())
                        for zi in zz.infolist():
                            if zi.filename.endswith("/") or "__MACOSX" in zi.filename or Path(zi.filename).name.startswith("."):
                                continue
                            rel2 = root / zi.filename
                            b.emit(dep_id, Path(sub) / rel2 if sub else rel2, zz.read(zi.filename), url, vlabel, man["license"],
                                   zi.filename, f" [opened from {key}]", "scripts/deposits_build.py")
        for (fd, is_local), items in b.folds.items():
            if fd != dep_id:
                continue
            base = (LOC if is_local else DEP) / dep_id
            items.sort()
            digest = hashlib.sha256("".join(f"{h}  {rel}\n" for rel, h, _ in items).encode()).hexdigest()
            c = CAT[dep_id]
            b.rows.append([base.relative_to(EXT).as_posix() + "/",
                           f"{c['desc']} ({len(items)} files, {sum(x[2] for x in items)} bytes; one row for the folder, sha256 is of the sorted '<sha256>  <path>' lines; per-file sha256 in PROVENANCE.json)",
                           snaps[0]["manifest"].get("concept_doi") or snaps[0]["manifest"]["record"],
                           f"{snaps[0]['manifest']['provider']} {snaps[0]['manifest'].get('version') or snaps[0]['manifest']['record']}; mirrored {snaps[0]['manifest']['retrieved_utc'][:16]}Z",
                           c["licence"], f"{RUN} item_{c['item']}", "", digest, EXTRACTED])
        for basedir in (DEP / dep_id, LOC / dep_id):
            if basedir.exists():
                p = basedir / "PROVENANCE.json"
                p.write_text(json.dumps(prov, indent=1, ensure_ascii=False) + "\n")
                b.rows.append([p.relative_to(EXT).as_posix(),
                               "Mirror provenance: the mirroring tool's manifest for each snapshot (URLs, sizes, provider checksums, sha256, retrieval time, licence as recorded)",
                               "deposits_data_mirror.py on deep-server", f"stamp {snaps[0]['stamp']}", CAT[dep_id]["licence"], RUN, "", sha256_of(p), EXTRACTED])
    shutil.rmtree(tmp)
    b.rows = sorted(kept + b.rows, key=lambda r: r[0])
    with open(DEP / "MANIFEST.tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["path", "description", "source", "source_version", "licence", "script", "rows", "sha256", "extracted"])
        w.writerows(b.rows)
    print(len(b.rows), "manifest rows;", len(ids), "deposits built")


if __name__ == "__main__":
    main()
