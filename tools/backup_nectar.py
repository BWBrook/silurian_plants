#!/usr/bin/env python3
"""Private retained project generations; run snapshot on mini.

Adapted from BWBrook/eprp resources/tools/paleodata_backup.py at 995e1a2.
"""

import argparse
import configparser
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import time

PROTECTED_NAMES = {"pbdb_access_global.tsv", "pbdb_access_region.tsv"}
KNOWN_MDB = {"data/external/local/spores/work/paly.mdb":
             "eb1fa8c3b2f8a1e06a31e2194846ae541ac5240338b4194f63b00823ccde85c1"}
LOCK_ROOT = Path("/private/tmp/silurian-plants-backup")
SCRUB_INTERVAL = dt.timedelta(days=7)


def run(args, **kwargs):
    return subprocess.run([str(x) for x in args], check=True, **kwargs)


def remote(host, script, *args, capture=False):
    result = run(["ssh", "-oBatchMode=yes", "-oConnectTimeout=15", host,
                  shlex.join(["python3", str(script), *map(str, args)])],
                 capture_output=capture, text=True)
    return json.loads(result.stdout) if capture else result


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def protected(path):
    p = Path(path)
    lower = path.lower()
    return (p.name.lower() in PROTECTED_NAMES
            or ("pbdb" in lower and any(x in lower for x in
                ("receipt", "quarantine", "access_global", "access_region", "history"))))


def signature(path):
    s = path.stat(follow_symlinks=False)
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns,
            stat.S_IMODE(s.st_mode)]


def inventory(root):
    files, dirs, modes = {}, [], {}
    def fail(error):
        raise error
    for directory, dirnames, filenames in os.walk(root, followlinks=False, onerror=fail):
        for name in sorted(dirnames + filenames):
            path = Path(directory) / name
            rel = path.relative_to(root).as_posix()
            if protected(rel):
                raise RuntimeError("Protected PBDB receipt/history path found; no payload read: " + rel)
            s = path.lstat()
            if ".git" in path.relative_to(root).parts and name.endswith(".lock"):
                raise RuntimeError("Git lock present; retry after the Git operation: " + rel)
            lower_name = name.lower()
            if (lower_name == ".env" or lower_name.startswith(".env.")
                    or lower_name in {"credentials.json", "token.json", "id_rsa", "id_ed25519"}
                    or lower_name.endswith((".pem", ".key", ".p12", ".pfx", ".kdbx"))):
                raise RuntimeError("Credential-like path requires review before backup: " + rel)
            if stat.S_ISREG(s.st_mode) and lower_name.endswith((
                    ".sqlite", ".sqlite3", ".db", ".db3", ".duckdb", ".duckdb.wal", ".accdb",
                    ".sqlite-wal", ".sqlite-shm", ".sqlite-journal", ".sqlite3-wal",
                    ".sqlite3-shm", ".sqlite3-journal", ".db-wal", ".db-shm",
                    ".db-journal", ".ldb", ".laccdb")):
                raise RuntimeError("Database or live database sidecar requires a dedicated capture method: " + rel)
            if stat.S_ISREG(s.st_mode) and lower_name.endswith(".mdb") and rel not in KNOWN_MDB:
                raise RuntimeError("Unrecognised Access database requires a dedicated capture method: " + rel)
            modes[rel] = stat.S_IMODE(s.st_mode)
            if stat.S_ISLNK(s.st_mode) or not (stat.S_ISDIR(s.st_mode) or stat.S_ISREG(s.st_mode)):
                raise RuntimeError("Unsupported symlink/special path: " + rel)
            if stat.S_ISDIR(s.st_mode):
                dirs.append(rel)
            else:
                files[rel] = signature(path)
    return {"files": files, "dirs": sorted(dirs), "modes": modes}


def stable(inventory_a, inventory_b):
    return all(inventory_a[k] == inventory_b[k] for k in ("files", "dirs", "modes"))


def check_git_config(source):
    config = configparser.ConfigParser(interpolation=None, strict=False)
    config.read(source / ".git/config")
    for section in config.sections():
        for key, value in config.items(section):
            if any(term in key.lower() for term in ("password", "token", "secret", "extraheader")):
                raise RuntimeError("Sensitive Git configuration requires review before backup")
            if key.lower() == "url" and "://" in value:
                from urllib.parse import urlsplit
                if urlsplit(value).username is not None:
                    raise RuntimeError("Credentials in a Git remote URL require review before backup")


def file_record(path):
    return {"bytes": path.stat().st_size, "sha256": digest(path)}


def safe_relative(value):
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or value == ".":
        raise RuntimeError("Invalid manifest path: " + value)
    return p


def verify_metadata(generation):
    manifest = json.loads((generation / "manifest.json").read_text())
    root = generation / "project"
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError("Generation project must be a directory: " + str(root))
    found = inventory(root)
    actual = set(found["files"])
    if actual != set(manifest["files"]):
        raise RuntimeError("Destination file inventory differs from manifest")
    if found["dirs"] != manifest["directories"]:
        raise RuntimeError("Destination directory inventory differs from manifest")
    partial = generation.name.endswith(".partial")
    for rel in manifest["directories"]:
        expected_mode = manifest["source_modes"][rel]
        if not partial:
            expected_mode &= ~0o222
        if found["modes"][rel] != expected_mode:
            raise RuntimeError("Directory mode mismatch: " + rel)
    total = 0
    for rel, expected in manifest["files"].items():
        path = root / safe_relative(rel)
        if found["files"][rel][2] != expected["bytes"]:
            raise RuntimeError("Checksum/size mismatch: " + rel)
        if found["modes"][rel] != (manifest["source_modes"][rel] & ~0o222):
            raise RuntimeError("File mode mismatch: " + rel)
        total += expected["bytes"]
    return manifest, found, total


def destination_identities(found):
    return {rel: [sig[1], sig[2], sig[3], sig[5]] for rel, sig in found["files"].items()}


def check_destination_identities(generation, found, required=False):
    path = generation / "file-identities.json"
    if not os.path.lexists(path):
        if required:
            raise RuntimeError("Previous generation has no file-identity receipt")
        return False
    if path.is_symlink() or not path.is_file():
        raise RuntimeError("Invalid file-identity receipt: " + str(path))
    receipt = json.loads(path.read_text())
    if receipt.get("format") != 1 or receipt.get("files") != destination_identities(found):
        raise RuntimeError("Destination file identity mismatch: " + str(generation))
    return True


def check_source_inventory(manifest, before):
    try:
        files = before["files"]
        if (set(files) != set(manifest["files"]) or
                before["dirs"] != manifest["directories"] or
                before["modes"] != manifest["source_modes"]):
            raise RuntimeError("Manifest differs from the source inventory")
        for rel, record in manifest["files"].items():
            sig = files[rel]
            if (not isinstance(sig, list) or len(sig) != 6 or
                    any(not isinstance(value, int) for value in sig) or
                    sig[2] != record["bytes"] or sig[5] != before["modes"][rel]):
                raise RuntimeError("Invalid source inventory entry: " + rel)
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError("Invalid previous source inventory") from error


def verify(generation, inode_cache=None):
    manifest, found, total = verify_metadata(generation)
    check_destination_identities(generation, found)
    cache = {} if inode_cache is None else inode_cache
    for rel, expected in manifest["files"].items():
        path = generation / "project" / safe_relative(rel)
        sig = found["files"][rel]
        inode = tuple(sig[:2])
        if inode in cache:
            previous_sig, checksum = cache[inode]
            if previous_sig != sig:
                raise RuntimeError("Shared inode changed during verification: " + rel)
        else:
            checksum = digest(path)
            if signature(path) != sig:
                raise RuntimeError("File changed during verification: " + rel)
            cache[inode] = (sig, checksum)
        if checksum != expected["sha256"]:
            raise RuntimeError("Checksum/size mismatch: " + rel)
    if not stable(found, inventory(generation / "project")):
        raise RuntimeError("Generation changed during verification: " + str(generation))
    return {"files": len(found["files"]), "bytes": total, "sha256": "all_match"}


def scrub_generations(root, inode_cache=None):
    started = time.monotonic()
    cache = {} if inode_cache is None else inode_cache
    generations = 0
    snapshots = root / "snapshots"
    for generation in sorted(snapshots.iterdir()):
        if generation.name.endswith(".partial"):
            continue
        if generation.is_symlink() or not generation.is_dir():
            raise RuntimeError("Unexpected item among retained generations: " + str(generation))
        verify(generation, cache)
        generations += 1
    return {"status": "passed", "generations": generations, "unique_inodes": len(cache),
            "seconds": round(time.monotonic() - started, 3)}


def restore(generation, destination, sample=False):
    manifest = json.loads((generation / "manifest.json").read_text())
    if destination.exists():
        raise RuntimeError("Restore target must be new: " + str(destination))
    destination.mkdir(parents=True, mode=0o700)
    paths = sorted(manifest["files"])
    if sample:
        ordinary = sorted(paths, key=lambda p: hashlib.sha256(p.encode()).digest())[:20]
        manifests = sorted((p for p in paths if p.endswith("MANIFEST.json")),
                           key=lambda p: hashlib.sha256(p.encode()).digest())[:20]
        paths = sorted(set(ordinary + manifests) |
                       ({"README.md", "library/closed.tsv", "library/open.tsv",
                         "library/closed/edwards2007.pdf", "library/open/W1820528062_SI.doc",
                         ".git/HEAD"} & set(paths)))
    else:
        for rel in manifest["directories"]:
            (destination / safe_relative(rel)).mkdir(parents=True, exist_ok=True)
    total = 0
    for rel in paths:
        output = destination / safe_relative(rel)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(generation / "project" / rel, output)
        if file_record(output) != manifest["files"][rel]:
            raise RuntimeError("Restore checksum failed: " + rel)
        total += manifest["files"][rel]["bytes"]
        output.chmod(manifest["source_modes"][rel])
    if not sample:
        for rel in sorted(manifest["directories"], key=lambda p: len(Path(p).parts), reverse=True):
            (destination / rel).chmod(manifest["source_modes"][rel])
    return {"kind": "sample" if sample else "full", "files": len(paths), "bytes": total,
            "sha256": "all_match", "target": str(destination)}


def seal(generation):
    for directory, dirs, files in os.walk(generation):
        for name in files:
            p = Path(directory) / name
            mode = stat.S_IMODE(p.stat().st_mode)
            if mode & 0o222:
                p.chmod(mode & ~0o222)
    for directory, dirs, files in os.walk(generation, topdown=False):
        p = Path(directory)
        p.chmod(stat.S_IMODE(p.stat().st_mode) & ~0o222)


def on_data_volume(root):
    return os.stat(root).st_dev != os.stat("/").st_dev


def scrub_due(root, force=False):
    if force:
        return True
    if os.path.lexists(root / "scrub-pending.json"):
        return True
    try:
        last = json.loads((root / "last-scrub.json").read_text())
        generation = safe_relative(last["generation"])
        if len(generation.parts) != 1 or generation.name.endswith(".partial"):
            return True
        previous = root / "snapshots" / generation / "scrub.json"
        if previous.is_symlink():
            return True
        report = json.loads(previous.read_text())
        completed = dt.datetime.fromisoformat(last["completed_utc"])
        now = dt.datetime.now(dt.timezone.utc)
        if (last["status"] != "passed" or report != last or completed.tzinfo is None
                or completed > now):
            return True
        return now - completed >= SCRUB_INTERVAL
    except (OSError, ValueError, KeyError, TypeError):
        return True


def mark_scrub_pending(root, generation):
    pending = root / "scrub-pending.json"
    if os.path.lexists(pending):
        if pending.is_symlink() or not pending.is_file():
            raise RuntimeError("Invalid pending scrub marker")
        return
    temporary = root / (".scrub-pending-" + generation)
    write_json(temporary, {"generation": generation,
                           "requested_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
    temporary.replace(pending)


def prepare(root, generation, required, reserve, force_scrub=False):
    if not root.is_absolute() or root == Path("/"):
        raise RuntimeError("Backup root must be an absolute dedicated path")
    if not on_data_volume(root):
        raise RuntimeError("Backup target is on root filesystem; data volume required")
    if shutil.disk_usage(root).free < required + reserve:
        raise RuntimeError("Insufficient capacity including reserve")
    root.chmod(0o700)
    require_scrub = scrub_due(root, force_scrub)
    if require_scrub:
        mark_scrub_pending(root, generation)
    latest = root / "latest"
    previous = None
    baseline = None
    if latest.is_symlink():
        previous = latest.resolve(strict=True)
        if (previous.name != "project" or previous.parent.name.endswith(".partial")
                or previous.parent.parent != (root / "snapshots").resolve()
                or not (previous.parent / "verification.json").is_file()
                or not (previous.parent / "restore-test.json").is_file()):
            raise RuntimeError("Latest does not point to a verified generation")
        if any(stat.S_IMODE(p.stat().st_mode) & 0o222 for p in (previous, previous.parent)):
            raise RuntimeError("Previous generation root is not sealed read-only")
        verification = json.loads((previous.parent / "verification.json").read_text())
        drill = json.loads((previous.parent / "restore-test.json").read_text())
        if (verification.get("sha256") not in
                {"all_match", "fresh_match_inherited_metadata_trusted"}
                or drill.get("sha256") != "all_match"):
            raise RuntimeError("Previous generation has no successful verification and restore receipt")
        previous_manifest, previous_found, _ = verify_metadata(previous.parent)
        if not check_destination_identities(previous.parent, previous_found):
            require_scrub = True
            mark_scrub_pending(root, generation)
        before_path = previous.parent / "source-before.json"
        if before_path.is_symlink() or not before_path.is_file():
            raise RuntimeError("Previous generation has no source inventory")
        before = json.loads(before_path.read_text())
        check_source_inventory(previous_manifest, before)
        baseline = {"manifest": previous_manifest, "source_before": before}
    elif os.path.lexists(latest):
        raise RuntimeError("Latest exists but is not a generation symlink")
    else:
        snapshots = root / "snapshots"
        if snapshots.exists() and any(not path.name.endswith(".partial")
                                      for path in snapshots.iterdir()):
            raise RuntimeError("Latest is missing while retained generations exist")
        require_scrub = True
        mark_scrub_pending(root, generation)
    partial = root / "snapshots" / (generation + ".partial")
    partial.mkdir(parents=True, mode=0o700, exist_ok=False)
    (partial / "project").mkdir(mode=0o700)
    plan = {"previous": str(previous) if previous else None,
            "scrub": require_scrub}
    write_json(partial / "plan.json", plan)
    return {"partial": str(partial), "free_bytes": shutil.disk_usage(root).free,
            "previous": plan["previous"], "scrub": plan["scrub"], "baseline": baseline}


def check_inherited(partial, previous):
    manifest = json.loads((partial / "manifest.json").read_text())
    inherited = manifest["inherited"]
    if len(inherited) != len(set(inherited)):
        raise RuntimeError("Duplicate inherited path")
    before = json.loads((partial / "source-before.json").read_text())
    check_source_inventory(manifest, before)
    if previous is None:
        if inherited:
            raise RuntimeError("Cannot inherit without a prior generation")
        return
    previous_manifest, previous_found, _ = verify_metadata(previous.parent)
    plan = json.loads((partial / "plan.json").read_text())
    check_destination_identities(previous.parent, previous_found, required=not plan["scrub"])
    previous_before = json.loads((previous.parent / "source-before.json").read_text())
    check_source_inventory(previous_manifest, previous_before)
    if (manifest["source"] != previous_manifest.get("source") or
            manifest["source_host"] != previous_manifest.get("source_host") or
            ("source_root" in previous_manifest and
             manifest["source_root"] != previous_manifest["source_root"])):
        raise RuntimeError("Inherited files come from a different source")
    for rel in inherited:
        safe_relative(rel)
        if (rel not in manifest["files"] or
                manifest["files"][rel] != previous_manifest["files"].get(rel) or
                before["files"].get(rel) != previous_before["files"].get(rel) or
                rel not in before["files"]):
            raise RuntimeError("Inherited manifest or source signature mismatch: " + rel)


def inherit(root, generation):
    partial = root / "snapshots" / (generation + ".partial")
    plan = json.loads((partial / "plan.json").read_text())
    previous = Path(plan["previous"]) if plan["previous"] else None
    manifest = json.loads((partial / "manifest.json").read_text())
    if manifest.get("based_on") != plan["previous"] or manifest.get("scrub") != plan["scrub"]:
        raise RuntimeError("Capture does not match the prepared plan")
    check_inherited(partial, previous)
    project = partial / "project"
    for rel in manifest["directories"]:
        directory = project / safe_relative(rel)
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        directory.chmod(0o700)
    for rel in manifest["inherited"]:
        os.link(previous / safe_relative(rel), project / safe_relative(rel))
    return {"inherited_files": len(manifest["inherited"])}


def verify_incremental(partial, previous, hash_fresh=True):
    manifest, found, total = verify_metadata(partial)
    check_inherited(partial, previous)
    inherited = set(manifest["inherited"])
    for rel, expected in manifest["files"].items():
        path = partial / "project" / safe_relative(rel)
        if rel in inherited:
            if not os.path.samefile(path, previous / safe_relative(rel)):
                raise RuntimeError("Inherited file is not linked to prior generation: " + rel)
        else:
            if previous and (previous / safe_relative(rel)).exists() and os.path.samefile(
                    path, previous / safe_relative(rel)):
                raise RuntimeError("Fresh file unexpectedly shares prior inode: " + rel)
            if hash_fresh and (file_record(path) != expected or
                               signature(path) != found["files"][rel]):
                raise RuntimeError("Checksum/size mismatch: " + rel)
    if not stable(found, inventory(partial / "project")):
        raise RuntimeError("Generation changed during verification")
    return {"files": len(found["files"]), "bytes": total,
            "fresh_files": len(found["files"]) - len(inherited),
            "inherited_files": len(inherited),
            "sha256": "fresh_match_inherited_metadata_trusted"}


def assert_latest(root, previous):
    latest = root / "latest"
    if (previous is not None and (not latest.is_symlink() or latest.resolve() != previous)) or (
            previous is None and os.path.lexists(latest)):
        raise RuntimeError("Latest changed after preparation")


def publish(root, generation):
    with (root / ".publish.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return publish_locked(root, generation)


def publish_locked(root, generation):
    started = time.monotonic()
    partial = root / "snapshots" / (generation + ".partial")
    plan = json.loads((partial / "plan.json").read_text())
    previous = Path(plan["previous"]) if plan["previous"] else None
    assert_latest(root, previous)
    latest = root / "latest"
    manifest = json.loads((partial / "manifest.json").read_text())
    if manifest.get("based_on") != plan["previous"] or manifest.get("scrub") != plan["scrub"]:
        raise RuntimeError("Capture does not match the prepared plan")
    project = partial / "project"
    for rel in sorted(manifest["directories"], key=lambda p: len(Path(p).parts), reverse=True):
        directory = project / safe_relative(rel)
        if not stat.S_ISDIR(directory.lstat().st_mode):
            raise RuntimeError("Expected directory: " + rel)
        directory.chmod(manifest["source_modes"][rel])
    _, verification_before, _ = verify_metadata(partial)
    result = verify_incremental(partial, previous, hash_fresh=not plan["scrub"])
    scrub = None
    if plan["scrub"]:
        cache = {}
        result = verify(partial, cache)
        result["fresh_files"] = len(manifest["files"]) - len(manifest["inherited"])
        result["inherited_files"] = len(manifest["inherited"])
        scrub = scrub_generations(root, cache)
        scrub["generation"] = generation
        scrub["completed_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    head = run(["git", "-C", project, "rev-parse", "HEAD"], capture_output=True, text=True, env=env).stdout.strip()
    if head != manifest["git_head"]:
        raise RuntimeError("Captured Git HEAD differs from the source")
    run(["git", "-C", project, "fsck", "--no-dangling", "--no-reflogs", "--no-progress"],
        capture_output=True, text=True, env=env, timeout=180)
    result["git"] = {"head": head, "fsck": "ok"}
    drill = restore(partial, root / "restore-tests" / generation, sample=True)
    _, verification_after, _ = verify_metadata(partial)
    if not stable(verification_before, verification_after):
        raise RuntimeError("Generation changed before promotion")
    result["seconds"] = round(time.monotonic() - started, 3)
    write_json(partial / "file-identities.json",
               {"format": 1, "files": destination_identities(verification_after)})
    write_json(partial / "verification.json", result)
    write_json(partial / "restore-test.json", drill)
    if scrub:
        write_json(partial / "scrub.json", scrub)
    seal(partial)
    completed = root / "snapshots" / generation
    if completed.exists():
        raise RuntimeError("Completed generation already exists")
    assert_latest(root, previous)
    partial.rename(completed)
    temporary = root / (".latest-" + generation)
    temporary.symlink_to(Path("snapshots") / generation / "project")
    temporary.replace(latest)
    if scrub:
        temporary_scrub = root / (".last-scrub-" + generation)
        write_json(temporary_scrub, scrub)
        temporary_scrub.replace(root / "last-scrub.json")
        (root / "scrub-pending.json").unlink()
    return {"generation": str(completed), "verification": result, "restore_test": drill,
            "scrub": scrub}


def send_driver(host, driver, remote_script):
    run(["ssh", "-oBatchMode=yes", "-oConnectTimeout=15", host,
         shlex.join(["mkdir", "-p", str(remote_script.parent)])])
    run(["scp", "-q", str(driver), f"{host}:{remote_script}"])


def send_state(host, stage, partial, names):
    run(["scp", "-q", *[str(stage / name) for name in names], f"{host}:{partial}/"])


def transfer(capture, partial, files_from, host):
    rsync = ["rsync", "-zdtp", "--checksum", "--chmod=Fugo-w", "--from0", "--relative",
             "--files-from=" + str(files_from), "--protect-args", "--partial", "--stats",
             "--timeout=600", "-e", "ssh -oBatchMode=yes -oConnectTimeout=15",
             str(capture) + "/", f"{host}:{partial}/project/"]
    for attempt in range(3):
        result = subprocess.run(rsync, capture_output=True, text=True,
                                env=dict(os.environ, LC_ALL="C"))
        if result.returncode == 0:
            stats = {}
            for name, value in re.findall(r"^([^:\n]+):\s*([0-9,]+)(?:\s|$)",
                                          result.stdout, flags=re.MULTILINE):
                if name in {"Number of regular files transferred", "Total transferred file size",
                            "Literal data", "Total bytes sent"}:
                    stats[name] = int(value.replace(",", ""))
            return {"attempts": attempt + 1, "final_attempt": stats}
        if attempt == 2:
            raise RuntimeError("rsync failed after three attempts; partial retained: " + result.stderr.strip())
        time.sleep(5)


def snapshot(args):
    started = time.monotonic()
    timings = {}
    source = args.source.resolve()
    if not source.is_dir():
        raise RuntimeError("Source missing")
    if not (source / ".git").is_dir() or (source / ".git/objects/info/alternates").exists():
        raise RuntimeError("A self-contained Git directory is required")
    check_git_config(source)
    if args.stage.resolve().is_relative_to(source) or args.root.is_relative_to(source):
        raise RuntimeError("Backup state cannot be inside the source")
    args.stage.mkdir(parents=True, exist_ok=True, mode=0o700)
    LOCK_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (LOCK_ROOT / "snapshot.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        generation = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        stage = args.stage / generation
        stage.mkdir(mode=0o700)
        root_sig = signature(source)[:2]
        before = inventory(source)
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
        git_head = run(["git", "-C", source, "rev-parse", "HEAD"], capture_output=True, text=True, env=env).stdout.strip()
        git_status = run(["git", "-C", source, "status", "--short", "--branch"], capture_output=True, text=True, env=env).stdout
        write_json(stage / "source-before.json", before)
        print(json.dumps({"phase": "inventory", "files": len(before["files"])}), flush=True)
        total = sum(sig[2] for sig in before["files"].values())
        timings["inventory_seconds"] = round(time.monotonic() - started, 3)
        driver_rel = "tools/backup_nectar.py"
        if driver_rel not in before["files"]:
            raise RuntimeError("Backup tool missing from source checkout")
        driver = stage / "backup_nectar.py"
        shutil.copy2(source / driver_rel, driver)
        if (signature(source / driver_rel) != before["files"][driver_rel] or
                digest(driver) != digest(source / driver_rel) or
                signature(source / driver_rel) != before["files"][driver_rel]):
            raise RuntimeError("Backup tool changed while preparing remote driver")
        remote_script = args.root / "backup_nectar.py"
        send_driver(args.host, driver, remote_script)
        receipt = remote(args.host, remote_script, "_prepare", args.root, generation,
                         2 * total, args.reserve_gib * 1024**3,
                         int(getattr(args, "scrub", False)), capture=True)
        partial = Path(receipt["partial"])
        baseline = receipt["baseline"]
        same_source = False
        if receipt["previous"]:
            if (not baseline or baseline["manifest"].get("source") != str(source) or
                    baseline["manifest"].get("source_host") != os.uname().nodename or
                    baseline["manifest"].get("source_root", root_sig[1]) != root_sig[1]):
                raise RuntimeError("Source identity differs from the previous generation")
            if "source_root" not in baseline["manifest"] and not any(
                    baseline["source_before"]["files"].get(rel) == sig
                    for rel, sig in before["files"].items()):
                raise RuntimeError("Legacy source identity cannot be established")
            same_source = True
        files, inherited = {}, []
        hash_started = time.monotonic()
        for rel, sig in before["files"].items():
            eligible = (same_source and baseline["source_before"]["files"].get(rel) == sig and
                        rel in baseline["manifest"]["files"])
            expected = baseline["manifest"]["files"].get(rel) if eligible else None
            if receipt["scrub"] or not eligible:
                files[rel] = file_record(source / rel)
                if receipt["scrub"] and eligible and files[rel] != expected:
                    raise RuntimeError("Unchanged-signature source checksum mismatch: " + rel)
            else:
                files[rel] = expected
            if signature(source / rel) != sig:
                raise RuntimeError("Source changed while hashing: " + rel)
            if rel in KNOWN_MDB and files[rel]["sha256"] != KNOWN_MDB[rel]:
                raise RuntimeError("Access database differs from the recorded fixed release: " + rel)
            if eligible:
                inherited.append(rel)
        after_hash = inventory(source)
        if signature(source)[:2] != root_sig or not stable(before, after_hash):
            raise RuntimeError("Source drift while hashing; keep failed staging and rerun")
        timings["source_hash_seconds"] = round(time.monotonic() - hash_started, 3)
        if shutil.disk_usage(stage).free < total + 10 * 1024**3:
            raise RuntimeError("Insufficient local space for a full-copy fallback plus 10 GiB reserve")
        capture = stage / "capture"
        capture.mkdir(mode=0o700)
        print(json.dumps({"phase": "local_clone"}), flush=True)
        capture_started = time.monotonic()
        run(["/bin/cp", "-cRp", str(source) + "/.", capture])
        after_capture = inventory(source)
        write_json(stage / "source-after.json", after_capture)
        if signature(source)[:2] != root_sig or not stable(before, after_capture):
            raise RuntimeError("Source drift while cloning; keep failed staging and rerun")
        captured = inventory(capture)
        if (set(captured["files"]) != set(before["files"]) or
                captured["dirs"] != before["dirs"] or captured["modes"] != before["modes"] or
                any(captured["files"][rel][2:4] != sig[2:4]
                    for rel, sig in before["files"].items())):
            raise RuntimeError("Local clone inventory or modes differ from the source")
        inherited_set = set(inherited)
        for rel, expected in files.items():
            if (receipt["scrub"] or rel not in inherited_set) and file_record(capture / rel) != expected:
                raise RuntimeError("Local clone checksum differs from the source: " + rel)
        check_git_config(capture)
        if not stable(captured, inventory(capture)):
            raise RuntimeError("Local clone changed while hashing")
        timings["capture_seconds"] = round(time.monotonic() - capture_started, 3)
        manifest = {"format": 2, "generation": generation, "source_host": os.uname().nodename,
                    "source": str(source), "git_head": git_head, "git_status": git_status,
                    "files": files, "directories": before["dirs"],
                    "source_modes": before["modes"], "source_root": root_sig[1],
                    "based_on": receipt["previous"], "inherited": sorted(inherited),
                    "scrub": receipt["scrub"],
                    "consistency": (
                        "Source paths and signatures stable across capture; all files SHA256-checked against source, clone and destination. This is not an atomic multi-file transaction."
                        if receipt["scrub"] else
                        "Source paths and signatures stable across capture; fresh files SHA256-checked against clone and destination; inherited files trust matching source metadata. This is not an atomic multi-file transaction.")}
        write_json(stage / "manifest.json", manifest)
        send_state(args.host, stage, partial, ["manifest.json", "source-before.json"])
        remote(args.host, remote_script, "_inherit", args.root, generation, capture=True)
        changed = sorted(set(before["files"]) - inherited_set)
        ordinary = stage / "changed-files.txt"
        ordinary.write_bytes(b"".join(os.fsencode(p) + b"\0" for p in changed))
        print(json.dumps({"phase": "transfer", "fresh_files": len(changed),
                          "inherited_files": len(inherited), "partial": str(partial)}), flush=True)
        transfer_started = time.monotonic()
        stats = (transfer(capture, partial, ordinary, args.host) if changed else
                 {"attempts": 0, "final_attempt": {}})
        timings["transfer_seconds"] = round(time.monotonic() - transfer_started, 3)
        if not stable(captured, inventory(capture)):
            raise RuntimeError("Local clone changed during transfer; generation not published; partial retained")
        manifest["transfer_stats"] = stats
        write_json(stage / "manifest.json", manifest)
        send_state(args.host, stage, partial, ["manifest.json", "source-before.json", "source-after.json"])
        publish_started = time.monotonic()
        result = remote(args.host, remote_script, "_publish", args.root, generation, capture=True)
        timings["publish_seconds"] = round(time.monotonic() - publish_started, 3)
        try:
            for directory, _, _ in os.walk(capture):
                os.chmod(directory, stat.S_IMODE(os.stat(directory).st_mode) | 0o700)
            shutil.rmtree(capture)
            result["local_staging_cleanup"] = "complete"
        except OSError as error:
            result["local_staging_cleanup"] = "failed: " + str(error)
        timings["total_seconds"] = round(time.monotonic() - started, 3)
        result["timings"] = timings
        result["transfer_stats"] = stats
        write_json(stage / "result.json", result)
        print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot")
    snap.add_argument("--source", type=Path, required=True)
    snap.add_argument("--host", default="nectar")
    snap.add_argument("--root", type=Path, default=Path("/data/codex/silurian_plants/backups/mac-mini"))
    snap.add_argument("--stage", type=Path, default=Path("/private/tmp/silurian-plants-backup"))
    snap.add_argument("--reserve-gib", type=int, default=20)
    snap.add_argument("--scrub", action="store_true", help="force a full integrity scrub")
    ver = commands.add_parser("verify")
    ver.add_argument("generation", type=Path)
    res = commands.add_parser("restore")
    res.add_argument("generation", type=Path)
    res.add_argument("destination", type=Path)
    res.add_argument("--sample", action="store_true")
    prep = commands.add_parser("_prepare")
    prep.add_argument("root", type=Path)
    prep.add_argument("generation")
    prep.add_argument("required", type=int)
    prep.add_argument("reserve", type=int)
    prep.add_argument("force_scrub", type=int, choices=[0, 1])
    inh = commands.add_parser("_inherit")
    inh.add_argument("root", type=Path)
    inh.add_argument("generation")
    pub = commands.add_parser("_publish")
    pub.add_argument("root", type=Path)
    pub.add_argument("generation")
    args = parser.parse_args()
    if args.command == "snapshot":
        snapshot(args)
    elif args.command == "verify":
        print(json.dumps(verify(args.generation), indent=2))
    elif args.command == "restore":
        print(json.dumps(restore(args.generation, args.destination, args.sample), indent=2))
    elif args.command == "_prepare":
        print(json.dumps(prepare(args.root, args.generation, args.required, args.reserve,
                                 bool(args.force_scrub))))
    elif args.command == "_inherit":
        print(json.dumps(inherit(args.root, args.generation)))
    elif args.command == "_publish":
        print(json.dumps(publish(args.root, args.generation)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        sys.exit(str(error))
