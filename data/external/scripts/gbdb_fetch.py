"""Download the GBDB snapshot from Zenodo, verify its checksum and unzip it.

Usage (on deep-server):
  ssh deep-server python3 -I - /data/codex/silurian_plants/raw/gbdb < gbdb_fetch.py
Creates <ROOT>/<UTC stamp>/ holding the zip, headers.txt, extracted/ (the two workbooks) and provenance.json
(URL, UTC time, licence, md5 declared by Zenodo and observed, sha256). Uses a plain user agent with no contact
details, makes no login and creates no account. Prints the versions listing so a newer record is noticed.
"""
import hashlib
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

API = "https://zenodo.org/api/records/4245604"
UA = "Mozilla/5.0 (compatible; research-fetch)"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120)


root = Path(sys.argv[1])
rec = json.load(get(API))
versions = json.load(get(API + "/versions"))
f = rec["files"][0]
md5_declared = f["checksum"].split(":", 1)[1]
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
d = root / stamp
d.mkdir(parents=True)
zp = d / f["key"]
md5, sha = hashlib.md5(), hashlib.sha256()
with get(f["links"]["self"]) as resp, open(zp, "wb") as out:
    (d / "headers.txt").write_text(str(resp.headers))
    while chunk := resp.read(1 << 20):
        out.write(chunk)
        md5.update(chunk)
        sha.update(chunk)
assert md5.hexdigest() == md5_declared, f"md5 mismatch: {md5.hexdigest()} vs {md5_declared}"
with zipfile.ZipFile(zp) as z:
    z.extractall(d / "extracted")
prov = {"doi": rec["doi"], "version": rec["metadata"].get("version"), "licence": rec["metadata"]["license"]["id"], "api_url": API,
        "file_url": f["links"]["self"], "file_name": f["key"], "size_bytes": f["size"], "md5_declared": md5_declared,
        "md5_observed": md5.hexdigest(), "sha256": sha.hexdigest(), "downloaded_utc": stamp, "user_agent": UA,
        "versions_listed": [(h["id"], h["metadata"].get("version"), h["created"][:10]) for h in versions["hits"]["hits"]]}
(d / "provenance.json").write_text(json.dumps(prov, indent=1))
print(json.dumps(prov, indent=1))
