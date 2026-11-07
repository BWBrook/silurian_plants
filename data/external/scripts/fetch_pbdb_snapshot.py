"""Restore the immutable CC0 PBDB effort input; never substitute a live database query."""

import gzip
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "data/external/pbdb-snapshot.json"


def restore(destination=None):
    manifest = json.loads(MANIFEST.read_text())
    target = Path(destination) if destination else ROOT / manifest["path"]
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest() != manifest["sha256"]:
            raise ValueError("existing PBDB snapshot has different bytes; refusing to overwrite")
        return target
    request = urllib.request.Request(manifest["url"], headers={"User-Agent": "silurian-plants-reproduction/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    if hashlib.sha256(payload).hexdigest() != manifest["gzip_sha256"]:
        raise ValueError("archived gzip checksum mismatch")
    raw = gzip.decompress(payload)
    if hashlib.sha256(raw).hexdigest() != manifest["sha256"] or len(raw) != manifest["bytes"]:
        raise ValueError("decompressed PBDB snapshot checksum mismatch")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".part")
    temporary.write_bytes(raw)
    temporary.replace(target)
    return target


if __name__ == "__main__":
    print(restore())
