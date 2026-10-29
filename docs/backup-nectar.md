# Private Nectar backup

The `mini` checkout can be captured as a private, dated generation at
`nectar:/data/codex/silurian_plants/backups/mac-mini/`. The payload includes
Git metadata, tracked and untracked work, and git-ignored data and literature. It does
not change the separate EPRP paleodata mirror. Each successful run retains earlier
generations and updates `latest` only after verification; no automatic pruning is used.

The SSH destination is `nectar`. The existing `mac-mini` storage directory is
kept unchanged so retained generations and their source-baseline checks stay together;
it is a storage identifier, not an SSH alias.

From the project root on `mini`, create a new generation with:

```sh
python3 tools/backup_nectar.py snapshot --source "$PWD"
```

Run the offline integrity regression checks with `python3 tools/test_backup_nectar.py`.

Barry approved daily incremental backups and weekly integrity scrubs on 29 October 2026.
The Codex scheduled task runs the same command daily at 02:00 on `mini`'s
local clock, notifying only on failures. Check Scheduled in the app for its current state. The
mini and desktop app must be running for an unattended task to start.

Daily runs compare the complete source inventory with the last successful capture,
using file identity, size, modification/change times and permissions. New or changed
files are SHA-256 checked against a local macOS copy-on-write capture and the delivered
Nectar copy. Unchanged files inherit their recorded hashes and are hardlinked from
the previous generation; the daily receipt distinguishes these metadata-trusted files
from freshly checksummed files. The full path, size and permission inventory is checked,
and inherited files must match the previous generation's saved inode and modification
time. Missing source-baseline records or a different source identity stop the run.
Git integrity and a sample restore are still checked before promotion.

A full integrity scrub runs automatically when seven days have elapsed since the last
successful scrub, including on the next run after a missed night. The first run after
this change establishes the scrub baseline. To force one sooner, use:

```sh
python3 tools/backup_nectar.py snapshot --source "$PWD" --scrub
```

The scrub hashes the source and capture, and checks all completed retained Nectar
generations against their recorded manifests, reading shared hardlinked content only
once. A source hash that changes despite an unchanged recorded source signature is an
integrity failure, not a new baseline. Failed scrubs do not advance the scrub date;
an outstanding scrub stays pending until a full scrub succeeds.
Metadata-only daily checks can leave silent corruption undetected until that scrub.
Each local staging directory retains `result.json` with fresh/inherited file counts,
phase timings and rsync transfer statistics. A successful scrub also leaves a sealed
`scrub.json` in its generation and updates `last-scrub.json` at the backup root.

If the filesystem cannot clone, macOS falls back to a normal copy; the script reserves
enough local space for that case. If another job changes the source during hashing or
capture, the script stops; retry once the source is quiet. The capture is not an atomic
transaction across independently updated files. It preserves file bytes, paths and
POSIX modes, not macOS extended attributes, ACLs, owners or resource forks.

The backup root is private to the `codex` account and its administrators. Completed
generations are made read-only by ordinary filesystem permissions, not WORM protection.
Incremental generations share read-only hardlinks for unchanged files: in-place edits,
permission changes or corruption of a shared inode can affect several generations.
Never edit the backup tree; restore to a new location first. Daily promotion verifies
changed files and inherited-file identity; the weekly scrub verifies all retained bytes.

The attached `/data` volume is not included in Nectar's instance-root snapshots. The
script stops on symlinks, special files, Git locks, credential-like filenames, sensitive
Git configuration, protected PBDB receipt/history names, and recognised SQLite,
Access or DuckDB files or sidecars without a dedicated capture method. The known
fixed-release Palynodata Access database is accepted only at its recorded SHA-256.
These checks are not a general classifier for every possible secret or database.
Failed staging is retained for inspection. Local captures are under
`/private/tmp/silurian-plants-backup/` and
removed after a verified successful run; small receipts remain. The backup root is for
the `mini` producer only: all its invocations use one local lock, but another host
writing the same root would not be coordinated. Each run reserves enough free space
for twice the full payload plus 20 GiB, even when an incremental run needs less.

For recovery, identify a generation under `snapshots/` and use the remote script to
verify it, then restore to a **new** directory. For example, replace `GENERATION` with
the recorded generation name in these commands:

```sh
ssh nectar python3 /data/codex/silurian_plants/backups/mac-mini/backup_nectar.py verify /data/codex/silurian_plants/backups/mac-mini/snapshots/GENERATION
ssh nectar python3 /data/codex/silurian_plants/backups/mac-mini/backup_nectar.py restore /data/codex/silurian_plants/backups/mac-mini/snapshots/GENERATION /data/codex/silurian_plants/restores/GENERATION
rsync -a nectar:/data/codex/silurian_plants/restores/GENERATION/ /path/to/new-local-directory/
```

The restore command refuses an existing target and reinstates the captured POSIX
modes. Confirm the destination before using the restored project; do not overwrite an
active checkout.
