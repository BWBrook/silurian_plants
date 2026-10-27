"""Run EPRP's library.py with OpenAlex credit accounting and without its publisher TDM routes.

Usage (on deep-server, from _tools/):
  python3 library_run.py resolve --store /data/codex/silurian_plants/library
  python3 library_run.py index --store STORE --out STORE/_index
  python3 library_run.py fetch --store STORE --tier ...      (phase 2 only; needs approval)

library.py is imported unchanged. This wrapper
  * empties library.TDM_ROUTES, so `fetch` cannot use a publisher TDM licence (Wiley's token is installed
    on deep-server and would otherwise be tried automatically after the open routes fail);
  * wraps library.get_json to add up the X-RateLimit-Credits-Used header of each OpenAlex response, and
    appends the total to STORE/credits.tsv. It never reads or prints a key.
"""

import datetime
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import library as L  # noqa: E402

L.TDM_ROUTES.clear()

TALLY = {"used": 0, "calls": 0, "remaining": ""}
_get_json = L.get_json


def counted_get_json(url, tries=5, headers=None):
    data, h = _get_json(url, tries, headers)
    if url.startswith("https://api.openalex.org/"):
        TALLY["calls"] += 1
        TALLY["used"] += int(h.get("X-RateLimit-Credits-Used") or 0)
        TALLY["remaining"] = h.get("X-RateLimit-Remaining") or TALLY["remaining"]
    return data, h


L.get_json = counted_get_json


def log_credits(store, label):
    path = Path(store) / "credits.tsv"
    new = not path.exists()
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write("when\tcommand\topenalex_calls\tcredits_used\tcredits_remaining_after\n")
        f.write(f"{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ}\t{label}\t{TALLY['calls']}\t"
                f"{TALLY['used']}\t{TALLY['remaining']}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        if L.TDM_ROUTES:
            sys.exit("TDM routes are active; refusing to fetch")
        print("library_run: publisher TDM routes active: none (library.TDM_ROUTES is empty); open routes only", flush=True)
    store = sys.argv[sys.argv.index("--store") + 1] if "--store" in sys.argv else None
    label = " ".join(a for a in sys.argv[1:] if not a.startswith("/"))
    try:
        L.main()
    finally:
        print(f"OpenAlex credits used by this run: {TALLY['used']} in {TALLY['calls']} calls "
              f"(remaining today: {TALLY['remaining']})")
        if store:
            log_credits(store, label)
