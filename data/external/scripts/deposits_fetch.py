#!/usr/bin/env python3
"""Fetch the openly licensed third-party deposits listed in data/external/deposits/MANIFEST.tsv.

Usage:
  python3 data/external/scripts/deposits_fetch.py [--only ID ...] [--manifest FILE] [--dest DIR]

For every manifest row under deposits/ (except PROVENANCE.json and the project's own documents) the script
downloads the row's `source` URL and writes the file to DEST/<path>, by default
data/external/local/deposits/<id>/..., which is git-ignored. Each file is verified against the sha256 in the
manifest; files already present with the right hash are skipped. Where one URL serves an archive (Europe PMC
`supplementaryFiles`, data.bris zips) and the row names a member, the member is located by its sha256 in the
archive, one nested zip deep. Rows under local/deposits/ (paywalled or unlicensed works held on one machine only)
are not fetched. The retry and HTML-refusal logic is that of deposits_data_mirror.py. Standard library only.
"""

import argparse
import csv
import datetime as dt
import email.utils
import hashlib
import http.client
import io
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

UA = "silurian-plants-deposits-fetch/1 (research data archive)"
RETRYABLE = (429, 500, 502, 503, 504)
TRANSIENT = (urllib.error.URLError, http.client.HTTPException, TimeoutError, ConnectionError)
EXT = Path(__file__).resolve().parents[1]
NOT_FETCHED = {"README.md", "crossref_check.tsv", "deposit_index.csv", "MANIFEST.tsv", "PROVENANCE.json"}


def retry_wait(err, attempt):
    after = getattr(err, "headers", None) and err.headers.get("Retry-After")
    if after:
        if after.isdigit():
            return int(after)
        when = email.utils.parsedate_to_datetime(after)
        return max(0, (when - dt.datetime.now(dt.timezone.utc)).total_seconds())
    return 2 ** attempt * 5


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def download(url, dest, html_ok):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as out:
                if not html_ok and "text/html" in r.headers.get("Content-Type", ""):
                    raise RuntimeError("HTML served in place of the file (login or bot-check page)")
                while block := r.read(1 << 20):
                    out.write(block)
            return
        except TRANSIENT as e:
            if attempt == 5 or (isinstance(e, urllib.error.HTTPError) and e.code not in RETRYABLE):
                raise
            time.sleep(retry_wait(e, attempt))


def zip_members(data, depth=2):
    """Yield (sha256, bytes) for every member of a zip, recursing into nested zips."""
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            body = z.read(info)
            yield hashlib.sha256(body).hexdigest(), body
            if depth > 1 and info.filename.lower().endswith(".zip"):
                try:
                    yield from zip_members(body, depth - 1)
                except zipfile.BadZipFile:
                    pass


def write(dest, data=None, src=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    if src is not None:
        tmp.write_bytes(Path(src).read_bytes())
    else:
        tmp.write_bytes(data)
    os.replace(tmp, dest)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", default=[], metavar="ID", help="fetch only these deposit folders")
    ap.add_argument("--manifest", default=EXT / "deposits" / "MANIFEST.tsv")
    ap.add_argument("--dest", default=EXT / "local")
    args = ap.parse_args()
    dest_root = Path(args.dest)

    with open(args.manifest, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    want = [r for r in rows
            if r["path"].startswith("deposits/") and Path(r["path"]).name not in NOT_FETCHED
            and r["source"].startswith("http")
            and (not args.only or r["path"].split("/")[1] in args.only)]

    todo, have = {}, 0
    for r in want:
        target = dest_root / r["path"]
        if target.is_file() and sha256_file(target) == r["sha256"]:
            have += 1
        else:
            todo.setdefault(r["source"], []).append(r)

    done, failed = 0, []
    with tempfile.TemporaryDirectory() as tmp:
        for url, group in todo.items():
            fetched = Path(tmp) / "download"
            html_ok = all(Path(r["path"]).suffix.lower() in (".html", ".htm") for r in group)
            try:
                download(url, fetched, html_ok)
            except Exception as e:
                failed += [(r["path"], f"{url}: {e}") for r in group]
                continue
            digest = sha256_file(fetched)
            members = None
            for r in group:
                target = dest_root / r["path"]
                if digest == r["sha256"]:
                    write(target, src=fetched)
                else:
                    if members is None:
                        try:
                            members = dict(zip_members(fetched.read_bytes()))
                        except zipfile.BadZipFile:
                            members = {}
                    if r["sha256"] in members:
                        write(target, data=members[r["sha256"]])
                    else:
                        failed.append((r["path"], f"{url}: sha256 matches neither the download nor an archive member"))
                        continue
                done += 1
                print(f"fetched {r['path']}")

    print(f"{done} fetched, {have} already present, {len(failed)} failed of {len(want)} files", file=sys.stderr)
    for path, why in failed:
        print(f"FAILED {path}: {why}", file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
