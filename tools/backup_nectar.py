#!/usr/bin/env python3
"""Private retained project generations; run snapshot on mac-mini.

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


def verify(generation):
    manifest = json.loads((generation / "manifest.json").read_text())
    root = generation / "project"
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
        if file_record(path) != expected:
            raise RuntimeError("Checksum/size mismatch: " + rel)
        if found["modes"][rel] != (manifest["source_modes"][rel] & ~0o222):
            raise RuntimeError("File mode mismatch: " + rel)
        total += expected["bytes"]
    return {"files": len(actual), "bytes": total, "sha256": "all_match"}


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
            p.chmod(stat.S_IMODE(p.stat().st_mode) & ~0o222)
    for directory, dirs, files in os.walk(generation, topdown=False):
        p = Path(directory)
        p.chmod(stat.S_IMODE(p.stat().st_mode) & ~0o222)


def prepare(root, generation, required, reserve):
    if not root.is_absolute() or root == Path("/"):
        raise RuntimeError("Backup root must be an absolute dedicated path")
    if os.stat(root).st_dev == os.stat("/").st_dev:
        raise RuntimeError("Backup target is on root filesystem; data volume required")
    if shutil.disk_usage(root).free < required + reserve:
        raise RuntimeError("Insufficient capacity including reserve")
    root.chmod(0o700)
    latest = root / "latest"
    previous = None
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
        if verification.get("sha256") != "all_match" or drill.get("sha256") != "all_match":
            raise RuntimeError("Previous generation has no successful verification and restore receipt")
        verify(previous.parent)
    elif os.path.lexists(latest):
        raise RuntimeError("Latest exists but is not a generation symlink")
    partial = root / "snapshots" / (generation + ".partial")
    partial.mkdir(parents=True, mode=0o700, exist_ok=False)
    (partial / "project").mkdir(mode=0o700)
    return {"partial": str(partial), "free_bytes": shutil.disk_usage(root).free,
            "previous": str(previous) if previous else None}


def publish(root, generation):
    partial = root / "snapshots" / (generation + ".partial")
    result = verify(partial)
    manifest = json.loads((partial / "manifest.json").read_text())
    project = partial / "project"
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    head = run(["git", "-C", project, "rev-parse", "HEAD"], capture_output=True, text=True, env=env).stdout.strip()
    if head != manifest["git_head"]:
        raise RuntimeError("Captured Git HEAD differs from the source")
    run(["git", "-C", project, "fsck", "--no-dangling", "--no-reflogs", "--no-progress"],
        capture_output=True, text=True, env=env, timeout=180)
    result["git"] = {"head": head, "fsck": "ok"}
    drill = restore(partial, root / "restore-tests" / generation, sample=True)
    write_json(partial / "verification.json", result)
    write_json(partial / "restore-test.json", drill)
    seal(partial)
    completed = root / "snapshots" / generation
    if completed.exists():
        raise RuntimeError("Completed generation already exists")
    partial.rename(completed)
    temporary = root / (".latest-" + generation)
    temporary.symlink_to(Path("snapshots") / generation / "project")
    temporary.replace(root / "latest")
    return {"generation": str(completed), "verification": result, "restore_test": drill}


def snapshot(args):
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
        before = inventory(source)
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
        git_head = run(["git", "-C", source, "rev-parse", "HEAD"], capture_output=True, text=True, env=env).stdout.strip()
        git_status = run(["git", "-C", source, "status", "--short", "--branch"], capture_output=True, text=True, env=env).stdout
        write_json(stage / "source-before.json", before)
        print(json.dumps({"phase": "inventory", "files": len(before["files"])}), flush=True)
        files = {}
        for rel, sig in before["files"].items():
            files[rel] = file_record(source / rel)
            if signature(source / rel) != sig:
                raise RuntimeError("Source changed while hashing: " + rel)
            if rel in KNOWN_MDB and files[rel]["sha256"] != KNOWN_MDB[rel]:
                raise RuntimeError("Access database differs from the recorded fixed release: " + rel)
        after_hash = inventory(source)
        if not stable(before, after_hash):
            raise RuntimeError("Source drift while hashing; keep failed staging and rerun")
        total = sum(record["bytes"] for record in files.values())
        if shutil.disk_usage(stage).free < total + 10 * 1024**3:
            raise RuntimeError("Insufficient local space for a full-copy fallback plus 10 GiB reserve")
        capture = stage / "capture"
        capture.mkdir(mode=0o700)
        print(json.dumps({"phase": "local_clone"}), flush=True)
        run(["/bin/cp", "-cRp", str(source) + "/.", capture])
        after_capture = inventory(source)
        write_json(stage / "source-after.json", after_capture)
        if not stable(before, after_capture):
            raise RuntimeError("Source drift while cloning; keep failed staging and rerun")
        captured = inventory(capture)
        if (set(captured["files"]) != set(before["files"]) or
                captured["dirs"] != before["dirs"] or captured["modes"] != before["modes"]):
            raise RuntimeError("Local clone inventory or modes differ from the source")
        for rel, expected in files.items():
            if file_record(capture / rel) != expected:
                raise RuntimeError("Local clone checksum differs from the source: " + rel)
        check_git_config(capture)
        if not stable(captured, inventory(capture)):
            raise RuntimeError("Local clone changed while hashing")
        manifest = {"format": 1, "generation": generation, "source_host": os.uname().nodename,
                    "source": str(source), "git_head": git_head, "git_status": git_status,
                    "files": files, "directories": before["dirs"],
                    "source_modes": before["modes"],
                    "consistency": "Source files and paths stable by metadata across hashing and clone; SHA256 checked against the clone and destination. This is not an atomic multi-file transaction."}
        write_json(stage / "manifest.json", manifest)
        remote_script = args.root / "backup_nectar.py"
        run(["ssh", "-oBatchMode=yes", "-oConnectTimeout=15", args.host,
             shlex.join(["mkdir", "-p", str(args.root)])])
        run(["scp", "-q", str(capture / "tools/backup_nectar.py"), f"{args.host}:{remote_script}"])
        receipt = remote(args.host, remote_script, "_prepare", args.root, generation,
                         2 * total, args.reserve_gib * 1024**3, capture=True)
        partial = Path(receipt["partial"])
        manifest["based_on"] = receipt["previous"]
        write_json(stage / "manifest.json", manifest)
        ordinary = stage / "ordinary-files.txt"
        ordinary.write_bytes(b"".join(os.fsencode(p) + b"\0" for p in sorted(set(before["files"]) | set(before["dirs"]))))
        rsync = ["rsync", "-dtp", "--checksum", "--chmod=Fugo-w", "--from0", "--relative", "--files-from=" + str(ordinary),
                 "--protect-args", "--partial", "--timeout=600", "-e", "ssh -oBatchMode=yes -oConnectTimeout=15"]
        if receipt["previous"]:
            rsync.append("--link-dest=" + receipt["previous"])
        print(json.dumps({"phase": "transfer", "bytes": total, "partial": str(partial)}), flush=True)
        for attempt in range(3):
            result = subprocess.run([*rsync, str(capture) + "/", f"{args.host}:{partial}/project/"])
            if result.returncode == 0:
                break
            if attempt == 2:
                raise RuntimeError("rsync failed after three attempts; partial retained")
            time.sleep(5)
        if not stable(captured, inventory(capture)):
            raise RuntimeError("Local clone changed during transfer; generation not published; partial retained")
        run(["scp", "-q", str(stage / "manifest.json"), str(stage / "source-before.json"),
             str(stage / "source-after.json"), f"{args.host}:{partial}/"])
        result = remote(args.host, remote_script, "_publish", args.root, generation, capture=True)
        try:
            for directory, _, _ in os.walk(capture):
                os.chmod(directory, stat.S_IMODE(os.stat(directory).st_mode) | 0o700)
            shutil.rmtree(capture)
            result["local_staging_cleanup"] = "complete"
        except OSError as error:
            result["local_staging_cleanup"] = "failed: " + str(error)
        write_json(stage / "result.json", result)
        print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot")
    snap.add_argument("--source", type=Path, required=True)
    snap.add_argument("--host", default="nectar-codex-ts")
    snap.add_argument("--root", type=Path, default=Path("/data/codex/silurian_plants/backups/mac-mini"))
    snap.add_argument("--stage", type=Path, default=Path("/private/tmp/silurian-plants-backup"))
    snap.add_argument("--reserve-gib", type=int, default=20)
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
        print(json.dumps(prepare(args.root, args.generation, args.required, args.reserve)))
    elif args.command == "_publish":
        print(json.dumps(publish(args.root, args.generation)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        sys.exit(str(error))
