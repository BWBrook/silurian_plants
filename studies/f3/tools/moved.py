"""Current location of a path recorded before the study-first move (13 November 2026).

Receipts and specifications written before the move name pre-move paths and stay byte-identical;
studies/f3/PATHS.tsv maps each moved file, and each moved directory with a trailing slash.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
with open(ROOT / "studies/f3/PATHS.tsv", newline="") as f:
    MOVED = {r["old_path"]: r["new_path"] for r in csv.DictReader(f, delimiter="\t")}
PREMOVE = {new: old for old, new in MOVED.items() if not old.endswith("/")}
_DIRS = sorted((o for o in MOVED if o.endswith("/")), key=len, reverse=True)


def current(path):
    path = str(path)
    if path in MOVED:
        return MOVED[path]
    for old in _DIRS:
        if path.startswith(old):
            return MOVED[old] + path[len(old):]
    return path


# Files whose only change after the pre-move commit is the move's path repair carry both hashes, so
# hash-bound records made before the move still verify against them, and any later edit does not.
with open(ROOT / "studies/f3/PATHS.tsv", newline="") as f:
    _PREMOVE_HASH = {r["moved_sha256"]: r["premove_sha256"] for r in csv.DictReader(f, delimiter="\t")
                     if r.get("moved_sha256") and r["moved_sha256"] != r["premove_sha256"]}


def premove_hash(digest):
    return _PREMOVE_HASH.get(digest, digest)


def premove_files(files):
    """A binding's {path: sha256} map restated in pre-move paths and pre-move hashes."""
    return {PREMOVE.get(k, k): premove_hash(v) for k, v in files.items()}
