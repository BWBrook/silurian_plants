#!/usr/bin/env python3
"""Mirror versions of a Zenodo record, Figshare collection or GitHub repository into a read-only local archive.

Usage:
  python3 data_mirror.py zenodo RECORD_ID DEST [--latest] [--only VERSION_DIR ...] [--files GLOB ...] [--jobs N] [--index-only]
  python3 data_mirror.py figshare COLLECTION_ID|article/ARTICLE_ID DEST [--latest] [--only VERSION_DIR ...] [--files GLOB ...] [--jobs N] [--index-only]
  python3 data_mirror.py github OWNER/REPO DEST [--latest] [--only VERSION_DIR ...] [--files GLOB ...] [--jobs N] [--index-only]
  python3 data_mirror.py dryad DOI DEST [--latest] [--only VERSION_DIR ...] [--files GLOB ...] [--jobs N] [--index-only]
  python3 data_mirror.py wfs WFS_URL LAYER[,LAYER...] DEST --license TEXT
  python3 data_mirror.py url DEST --license TEXT [--specs-file FILE] [--pause SECONDS] [NAME::]URL [[NAME::]URL ...]
  python3 data_mirror.py verify DEST [--only VERSION_DIR ...]

Writes DEST/versions.tsv (every version the provider offers) and
DEST/raw/<version_dir>/ holding the unchanged files plus MANIFEST.json for the
selected versions: --latest takes the newest version of each record (Figshare:
of each article; Zenodo, Dryad and Figshare: by the provider's own version
order, not the publication dates, which depositors set and which need not
increase; a tie at the newest version is an error),
--only names version_dirs, and both may be combined. --files keeps only the
files whose names match the glob patterns; the manifest records the patterns,
and a version once mirrored is skipped, so a different selection of the same
versions needs its own DEST. --jobs fetches that many versions at once
(Zenodo serves each connection slowly). Zenodo
version_dirs are <version>_<record>; Figshare ones are <article-title>_v<N>_<article>,
one per version of every article in the collection; GitHub ones are
<commit-date>_<sha10>, one per commit on the default branch; Dryad ones are
v<version>_<version-id>, one per published version (catalogue reads are open,
but file downloads need a Dryad API account: DRYAD_CLIENT_ID and
DRYAD_CLIENT_SECRET in the environment or ~/.config/dryad/credentials, mode
600, exchanged for a bearer token). Files are verified
against the provider's size and checksum (md5 for Zenodo and Figshare, md5 or
sha256 for Dryad, the blob hash for GitHub),
hashed with sha256, then made read-only. A live WFS has no versions: each `wfs`
run writes a dated snapshot, raw/<UTC timestamp>_wfs/, with one CSV per layer
(GeoServer outputFormat=csv) and its schema; the row count must equal the
server's numberMatched, and DEST/versions.tsv lists all snapshots. `url` does the
same for plain files with no provider checksum (raw/<UTC timestamp>_url/), waiting
--pause seconds between requests to small servers and web archives. A live
snapshot cannot resume, so a failed wfs or url run removes its partial directory.
`url` refuses an HTML response for a file not named .html or .htm (a login or
bot-check page served in place of the file).
Interrupted downloads resume from their .part files and completed versions are
skipped. verify re-hashes mirrored files against their manifests. Standard
library only.
"""

import argparse
import concurrent.futures
import datetime as dt
import email.utils
import fcntl
import fnmatch
import hashlib
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "eprp-data-mirror/4 (research data archive)"
RETRYABLE = (429, 500, 502, 503, 504)
TRANSIENT = (urllib.error.URLError, http.client.HTTPException, TimeoutError, ConnectionError)


def retry_wait(err, attempt):
    after = getattr(err, "headers", None) and err.headers.get("Retry-After")
    if after:
        if after.isdigit():
            return int(after)
        when = email.utils.parsedate_to_datetime(after)
        return max(0, (when - dt.datetime.now(dt.timezone.utc)).total_seconds())
    return 2 ** attempt * 5


def get_json(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except TRANSIENT as e:
            if attempt == 5 or (isinstance(e, urllib.error.HTTPError) and e.code not in RETRYABLE):
                raise
            time.sleep(retry_wait(e, attempt))


def slug(text):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(text).strip()).strip("-")


def zenodo_versions(record_id):
    api = "https://zenodo.org/api/records"
    hits, page = {}, 1
    while True:
        data = get_json(f"{api}/{record_id}/versions?size=25&page={page}")
        total = data["hits"]["total"]
        batch = data["hits"]["hits"]
        hits.update((h["id"], h) for h in batch)
        if len(hits) >= total or not batch:
            break
        page += 1
        time.sleep(1)
    if len(hits) != total:
        raise RuntimeError(f"index incomplete: {len(hits)} of {total} versions")
    out = []
    for h in hits.values():
        m = h["metadata"]
        v = slug(m.get("version", ""))
        files = [{"key": x["key"], "size": x["size"], "checksum": x["checksum"], "url": x["links"]["self"]}
                 for x in h["files"]]
        rel = ((m.get("relations") or {}).get("version") or [{}])[0]
        if "index" not in rel:
            raise RuntimeError(f"record {h['id']}: Zenodo gives no version index")
        out.append({
            "dir": f"{v}_{h['id']}" if v else str(h["id"]), "provider": "zenodo", "record": h["id"],
            "index": rel["index"],
            "version": m.get("version"), "doi": h.get("doi"), "concept_doi": h.get("conceptdoi"),
            "publication_date": m.get("publication_date", ""), "title": m.get("title"),
            "creators": [c.get("name") for c in m.get("creators", [])],
            "license": (m.get("license") or {}).get("id", ""), "files": files,
        })
    return sorted(out, key=lambda r: r["index"])  # Zenodo's own order; depositors set publication dates by hand


def figshare_versions(record_id):
    api = "https://api.figshare.com/v2"
    if record_id.startswith("article/"):
        collection, articles = {}, [{"id": int(record_id.split("/", 1)[1])}]
    else:
        collection = get_json(f"{api}/collections/{record_id}")
        articles = get_json(f"{api}/collections/{record_id}/articles?page_size=1000")
        if len(articles) != collection["articles_count"]:
            raise RuntimeError(f"index incomplete: {len(articles)} of {collection['articles_count']} articles")
    out = []
    for a in articles:
        for v in get_json(f"{api}/articles/{a['id']}/versions"):
            d = get_json(f"{api}/articles/{a['id']}/versions/{v['version']}")
            time.sleep(0.3)
            files = [{"key": f["name"], "size": f["size"], "checksum": "md5:" + f["computed_md5"],
                      "url": f["download_url"]} for f in d["files"]]
            out.append({
                "dir": f"{slug(d['title'])}_v{v['version']}_{a['id']}", "provider": "figshare", "record": a["id"],
                "version": v["version"], "doi": d.get("doi"), "concept_doi": collection.get("doi"),
                "publication_date": (d.get("published_date") or "")[:10], "title": d.get("title"),
                "creators": [x.get("full_name") for x in d.get("authors", [])],
                "license": (d.get("license") or {}).get("name", ""), "files": files,
            })
    return sorted(out, key=lambda r: (r["publication_date"], r["record"], r["version"]))


DRYAD = "https://datadryad.org"
_dryad_token = None


def dryad_token():
    """Bearer token for Dryad file downloads, from DRYAD_CLIENT_ID and DRYAD_CLIENT_SECRET in the
    environment or in ~/.config/dryad/credentials (KEY=VALUE lines, readable only by the owner)."""
    global _dryad_token
    if _dryad_token:
        return _dryad_token
    creds = {k: os.environ[k] for k in ("DRYAD_CLIENT_ID", "DRYAD_CLIENT_SECRET") if k in os.environ}
    path = os.path.expanduser("~/.config/dryad/credentials")
    if len(creds) < 2 and os.path.exists(path):
        if os.stat(path).st_mode & 0o077:
            sys.exit(f"{path} must be readable by its owner only (chmod 600)")
        for line in open(path):
            k, sep, v = line.strip().partition("=")
            if sep:
                creds.setdefault(k.strip(), v.strip())
    if not {"DRYAD_CLIENT_ID", "DRYAD_CLIENT_SECRET"} <= creds.keys():
        sys.exit("Dryad downloads need an API account: set DRYAD_CLIENT_ID and DRYAD_CLIENT_SECRET")
    body = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": creds["DRYAD_CLIENT_ID"],
                                   "client_secret": creds["DRYAD_CLIENT_SECRET"]}).encode()
    req = urllib.request.Request(f"{DRYAD}/oauth/token", data=body, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        _dryad_token = json.load(r)["access_token"]
    return _dryad_token


def dryad_versions(doi):
    ds = urllib.parse.quote(f"doi:{doi.removeprefix('doi:')}", safe="")
    meta = get_json(f"{DRYAD}/api/v2/datasets/{ds}")
    vers = get_json(f"{DRYAD}/api/v2/datasets/{ds}/versions")["_embedded"]["stash:versions"]
    out = []
    for v in vers:
        files, url = [], DRYAD + v["_links"]["stash:files"]["href"]
        while url:
            page = get_json(url)
            files += [{"key": f["path"], "size": f["size"], "checksum": f"{f['digestType'].replace('-', '')}:{f['digest']}",
                       "url": DRYAD + f["_links"]["stash:download"]["href"]} for f in page["_embedded"]["stash:files"]]
            nxt = page["_links"].get("next")
            url = DRYAD + nxt["href"] if nxt else None
        vid = v["_links"]["self"]["href"].rsplit("/", 1)[1]
        out.append({
            "dir": f"v{v['versionNumber']}_{vid}", "provider": "dryad", "record": vid, "version": v["versionNumber"],
            "doi": meta.get("identifier"), "concept_doi": meta.get("identifier"),
            "publication_date": v.get("publicationDate") or "", "title": v.get("title"),
            "creators": [f"{x.get('firstName', '')} {x.get('lastName', '')}".strip() for x in meta.get("authors", [])],
            "license": meta.get("license", ""), "files": files,
        })
    return sorted(out, key=lambda r: r["version"])  # Dryad publication dates are not monotonic in version


def github_versions(repo):
    api = f"https://api.github.com/repos/{repo}"
    meta = get_json(api)
    commits, page = [], 1
    while True:
        batch = get_json(f"{api}/commits?sha={meta['default_branch']}&per_page=100&page={page}")
        commits.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    out = []
    for c in commits:
        when = c["commit"]["committer"]["date"]
        out.append({
            "dir": f"{when[:10]}_{c['sha'][:10]}", "provider": "github", "record": c["sha"], "version": c["sha"][:10],
            "doi": None, "concept_doi": f"https://github.com/{repo}", "publication_date": when,
            "title": c["commit"]["message"].splitlines()[0], "creators": [c["commit"]["author"]["name"]],
            "license": (meta.get("license") or {}).get("spdx_id") or "none stated", "files": None, "repo": repo,
        })
    return sorted(out, key=lambda r: r["publication_date"])


def github_files(repo, sha):
    tree = get_json(f"https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError(f"tree listing truncated for {repo}@{sha}")
    return [{"key": t["path"], "size": t["size"], "checksum": "gitblob:" + t["sha"],
             "url": f"https://raw.githubusercontent.com/{repo}/{sha}/{urllib.parse.quote(t['path'])}"}
            for t in tree["tree"] if t["type"] == "blob"]


def write_index(versions, path):
    cols = ["version_dir", "version", "record_id", "doi", "publication_date", "license", "total_bytes", "files"]
    tmp = path + ".part"
    with open(tmp, "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in versions:
            fl = sorted(r["files"] or [], key=lambda x: x["key"])
            files = ";".join(f"{x['key']}|{x['size']}|{x['checksum']}" for x in fl)
            total = str(sum(x["size"] for x in fl)) if r["files"] is not None else ""
            row = [r["dir"], str(r["version"] or ""), str(r["record"]), r["doi"] or "", r["publication_date"],
                   r["license"], total, files]
            f.write("\t".join(row) + "\n")
    os.replace(tmp, path)


def hash_file(path, *algos):
    hs = []
    for a in algos:
        h = hashlib.sha1() if a == "gitblob" else hashlib.new(a)
        if a == "gitblob":
            h.update(b"blob %d\0" % os.path.getsize(path))
        hs.append(h)
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            for h in hs:
                h.update(chunk)
    return [h.hexdigest() for h in hs]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def dryad_resolve(url):
    """Dryad's file API redirects to pre-signed storage, which rejects the bearer token: return the target."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Authorization": f"Bearer {dryad_token()}"})
    try:
        with urllib.request.build_opener(_NoRedirect).open(req, timeout=60):
            return url
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308):
            return e.headers["Location"]
        raise


def download(url, dest, size, checksum):
    algo, expected = checksum.split(":", 1)
    part = dest + ".part"
    if size == 0:
        open(part, "wb").close()
    for attempt in range(8):
        have = os.path.getsize(part) if os.path.exists(part) else 0
        if have > size:
            os.remove(part)
            have = 0
        try:
            if have < size:
                fetch, headers = url, {"User-Agent": UA}
                if url.startswith(f"{DRYAD}/api/"):
                    fetch = dryad_resolve(url)
                    if fetch == url:
                        headers["Authorization"] = f"Bearer {dryad_token()}"
                if have:
                    headers["Range"] = f"bytes={have}-"
                with urllib.request.urlopen(urllib.request.Request(fetch, headers=headers), timeout=300) as r:
                    mode = "ab" if have and r.status == 206 else "wb"
                    with open(part, mode) as out:
                        while chunk := r.read(1 << 20):
                            out.write(chunk)
            got_sum, sha = hash_file(part, algo, "sha256")
            got = os.path.getsize(part)
            if got == size and got_sum == expected:
                os.replace(part, dest)
                return sha
            if got >= size:
                os.remove(part)
            print(f"  incomplete or mismatched ({got}/{size} bytes); attempt {attempt + 1}", flush=True)
        except TRANSIENT as e:
            if attempt == 7 or (isinstance(e, urllib.error.HTTPError) and e.code not in RETRYABLE):
                raise
            print(f"  retry {attempt + 1} after {e!r}", flush=True)
            time.sleep(retry_wait(e, attempt))
    raise IOError(f"could not fetch {url} intact")


def mirror_version(r, raw_root, tool_sha, patterns=None):
    vdir = os.path.join(raw_root, r["dir"])
    manifest_path = os.path.join(vdir, "MANIFEST.json")
    if os.path.exists(manifest_path):
        return False
    if r["files"] is None:
        r["files"] = github_files(r["repo"], r["record"])
    selected = [x for x in r["files"] if not patterns or any(fnmatch.fnmatchcase(x["key"], p) for p in patterns)]
    if patterns and not selected:
        raise RuntimeError(f"{r['dir']}: no file matches {' '.join(patterns)}")
    os.makedirs(vdir, exist_ok=True)
    files = []
    for x in sorted(selected, key=lambda x: x["key"]):
        dest = os.path.join(vdir, x["key"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        algo, expected = x["checksum"].split(":", 1)
        if os.path.exists(dest):
            got_sum, sha = hash_file(dest, algo, "sha256")
            if got_sum != expected:
                raise IOError(f"{dest} exists with wrong {algo}")
        else:
            sha = download(x["url"], dest, x["size"], x["checksum"])
        os.chmod(dest, 0o444)
        files.append({**x, "sha256": sha})
        time.sleep(1)
    manifest = {k: r[k] for k in ("provider", "record", "version", "doi", "concept_doi", "publication_date",
                                  "title", "creators", "license")}
    manifest.update(files=files, retrieved_utc=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    tool={"name": "data_mirror.py", "sha256": tool_sha})
    if patterns:
        manifest["files_selected"] = patterns
    with open(manifest_path + ".part", "w") as f:
        json.dump(manifest, f, indent=2)
    os.replace(manifest_path + ".part", manifest_path)
    os.chmod(manifest_path, 0o444)
    os.chmod(vdir, 0o555)
    return True


def wfs_snapshot(url, layers, dest, vdir, stamp, licence, tool_sha):
    import csv
    files, counts = [], {}
    for layer in layers:
        q = f"{url}?service=WFS&version=2.0.0&request=GetFeature&typeNames={urllib.parse.quote(layer)}"
        with urllib.request.urlopen(urllib.request.Request(q + "&resultType=hits", headers={"User-Agent": UA}), timeout=120) as r:
            head = r.read().decode("utf-8", "replace")
        matched = int(re.search(r'numberMatched="(\d+)"', head).group(1))
        served = re.search(r'timeStamp="([^"]+)"', head)
        name = layer.split(":")[-1]
        for kind, suffix, query in (("data", ".csv", q + "&outputFormat=csv"),
                                    ("schema", "_schema.xml", f"{url}?service=WFS&version=2.0.0&request=DescribeFeatureType&typeNames={urllib.parse.quote(layer)}")):
            target = os.path.join(vdir, name + suffix)
            with urllib.request.urlopen(urllib.request.Request(query, headers={"User-Agent": UA}), timeout=600) as r, \
                    open(target, "wb") as out:
                while chunk := r.read(1 << 20):
                    out.write(chunk)
            if kind == "data":
                with open(target, newline="", encoding="utf-8", errors="replace") as f:
                    rows = sum(1 for _ in csv.reader(f)) - 1
                if rows != matched:
                    raise IOError(f"{layer}: {rows} CSV rows but numberMatched {matched}")
                counts[layer] = {"numberMatched": matched, "server_timeStamp": served.group(1) if served else None}
            os.chmod(target, 0o444)
            files.append({"key": os.path.basename(target), "size": os.path.getsize(target), "checksum": "none (live service)",
                          "sha256": hash_file(target, "sha256")[0], "url": query})
        print(f"{layer}: {matched} features", flush=True)
    manifest = {"provider": "wfs", "record": url, "version": stamp, "layers": counts, "license": licence,
                "files": files, "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "tool": {"name": "data_mirror.py", "sha256": tool_sha}}
    finish_snapshot(vdir, manifest, dest)


def url_snapshot(urls, dest, vdir, stamp, licence, tool_sha, pause):
    files = []
    for i, spec in enumerate(urls):
        if i and pause:
            time.sleep(pause)
        name, sep, u = spec.partition("::")
        if not sep:
            name, u = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(spec).path)) or "download", spec
        target = os.path.join(vdir, name)
        for attempt in range(6):
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=600) as r, \
                        open(target + ".part", "wb") as out:
                    if r.headers.get_content_type() == "text/html" and not name.endswith((".html", ".htm")):
                        raise ValueError(f"{u}: served an HTML page (login or bot check?), not {name}")
                    expected = r.headers.get("Content-Length")
                    while chunk := r.read(1 << 20):
                        out.write(chunk)
                if expected is not None and os.path.getsize(target + ".part") != int(expected):
                    raise IOError(f"{u}: {os.path.getsize(target + '.part')} of {expected} bytes")
                break
            except TRANSIENT + (IOError,) as e:
                if attempt == 5 or (isinstance(e, urllib.error.HTTPError) and e.code not in RETRYABLE):
                    raise
                time.sleep(retry_wait(e, attempt))
        os.replace(target + ".part", target)
        os.chmod(target, 0o444)
        files.append({"key": os.path.basename(target), "size": os.path.getsize(target), "checksum": "none (plain URL)",
                      "sha256": hash_file(target, "sha256")[0], "url": u})
        print(f"{os.path.basename(target)}: {os.path.getsize(target)} bytes", flush=True)
    manifest = {"provider": "url", "record": urls[0], "version": stamp, "license": licence, "files": files,
                "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "tool": {"name": "data_mirror.py", "sha256": tool_sha}}
    finish_snapshot(vdir, manifest, dest)


def finish_snapshot(vdir, manifest, dest):
    with open(os.path.join(vdir, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    os.chmod(os.path.join(vdir, "MANIFEST.json"), 0o444)
    os.chmod(vdir, 0o555)
    snapshots = []
    for v in sorted(os.listdir(os.path.join(dest, "raw"))):
        mpath = os.path.join(dest, "raw", v, "MANIFEST.json")
        if v.endswith(("_wfs", "_url")) and os.path.exists(mpath):
            m = json.load(open(mpath))
            snapshots.append({"dir": v, "version": m["version"], "record": m["record"], "doi": None,
                              "publication_date": m["retrieved_utc"], "license": m["license"],
                              "files": [{"key": x["key"], "size": x["size"], "checksum": "sha256:" + x["sha256"]} for x in m["files"]]})
    write_index(snapshots, os.path.join(dest, "versions.tsv"))


def verify(raw_root, only):
    bad = 0
    for v in sorted(os.listdir(raw_root)):
        manifest = os.path.join(raw_root, v, "MANIFEST.json")
        if (only and v not in only) or not os.path.exists(manifest):
            continue
        for f in json.load(open(manifest))["files"]:
            ok = hash_file(os.path.join(raw_root, v, f["key"]), "sha256")[0] == f["sha256"]
            bad += not ok
            print(f"{'ok ' if ok else 'BAD'} {v}/{f['key']}", flush=True)
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="command", required=True)
    for provider in ("zenodo", "figshare", "github", "dryad"):
        p = sub.add_parser(provider)
        p.add_argument("record_id")
        p.add_argument("dest")
        p.add_argument("--only", nargs="*", default=None, help="version_dir names to fetch")
        p.add_argument("--latest", action="store_true", help="fetch the newest version of each record")
        p.add_argument("--files", nargs="+", default=None, help="fetch only files whose names match these glob patterns")
        p.add_argument("--jobs", type=int, default=1, help="versions fetched at once")
        p.add_argument("--index-only", action="store_true")
    p = sub.add_parser("wfs")
    p.add_argument("wfs_url")
    p.add_argument("layers")
    p.add_argument("dest")
    p.add_argument("--license", required=True, help="licence as stated by the provider (a WFS carries none)")
    p = sub.add_parser("url")
    p.add_argument("dest")
    p.add_argument("urls", nargs="*")
    p.add_argument("--specs-file", help="file of further NAME::URL lines (for lists too long for the command line)")
    p.add_argument("--license", required=True, help="licence or terms as stated by the provider")
    p.add_argument("--pause", type=float, default=0, help="seconds to wait between requests")
    p = sub.add_parser("verify")
    p.add_argument("dest")
    p.add_argument("--only", nargs="*", default=None)
    a, extra = ap.parse_known_args()
    if extra:  # url takes its URLs before or after the options
        if a.command == "url" and not any(x.startswith("-") for x in extra):
            a.urls += extra
        else:
            ap.error("unrecognized arguments: " + " ".join(extra))
    raw_root = os.path.join(a.dest, "raw")
    if a.command == "verify":
        bad = verify(raw_root, a.only)
        print(f"{bad} files failed verification", flush=True)
        return 1 if bad else 0
    with open(__file__, "rb") as f:
        tool_sha = hashlib.sha256(f.read()).hexdigest()
    if a.command in ("wfs", "url"):
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
        vdir = os.path.join(raw_root, f"{stamp}_{a.command}")
        os.makedirs(vdir)
        try:
            if a.command == "wfs":
                wfs_snapshot(a.wfs_url, a.layers.split(","), a.dest, vdir, stamp, a.license, tool_sha)
            else:
                urls = list(a.urls)
                if a.specs_file:
                    with open(a.specs_file) as f:
                        urls += [line.strip() for line in f if line.strip()]
                if not urls:
                    sys.exit("url: no URLs given")
                url_snapshot(urls, a.dest, vdir, stamp, a.license, tool_sha, a.pause)
        except BaseException:
            for name in os.listdir(vdir):
                os.chmod(os.path.join(vdir, name), 0o644)
                os.remove(os.path.join(vdir, name))
            os.rmdir(vdir)
            print(f"snapshot failed; removed partial {vdir}", file=sys.stderr, flush=True)
            raise
        return 0
    os.makedirs(raw_root, exist_ok=True)
    lock = open(os.path.join(a.dest, ".mirror.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"another mirror run holds {a.dest}/.mirror.lock")
    versions = {"zenodo": zenodo_versions, "figshare": figshare_versions, "github": github_versions,
                "dryad": dryad_versions}[a.command](a.record_id)
    write_index(versions, os.path.join(a.dest, "versions.tsv"))
    print(f"{len(versions)} versions indexed", flush=True)
    if a.index_only:
        return 0
    if a.only is not None:
        unknown = set(a.only) - {r["dir"] for r in versions}
        if unknown:
            sys.exit(f"unknown version_dir: {' '.join(sorted(unknown))}")
    chosen = set(a.only or [])
    if a.latest:
        group = (lambda r: r["record"]) if a.command == "figshare" else (lambda r: "all")
        order = {"zenodo": lambda r: r["index"], "dryad": lambda r: r["version"],
                 "figshare": lambda r: r["version"]}.get(
            a.command, lambda r: (r["publication_date"], str(r["version"])))
        newest, tied = {}, set()
        for r in versions:
            key = group(r)
            if key not in newest or order(r) > order(newest[key]):
                newest[key] = r
                tied.discard(key)
            elif order(r) == order(newest[key]):
                tied.add(key)
        if tied:
            sys.exit(f"--latest: the provider's order ties at the newest version of {' '.join(map(str, tied))}; use --only")
        chosen |= {r["dir"] for r in newest.values()}
    wanted = [r for r in versions if r["dir"] in chosen] if (a.only is not None or a.latest) else versions

    def run(item):
        i, r = item
        done = mirror_version(r, raw_root, tool_sha, a.files)
        print(f"[{i}/{len(wanted)}] {r['dir']} {'fetched' if done else 'present'}", flush=True)

    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(run, enumerate(wanted, 1)))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
