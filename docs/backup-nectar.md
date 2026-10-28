# Private Nectar backup

The mac-mini checkout can be captured as a private, dated generation at
`nectar-codex-ts:/data/codex/silurian_plants/backups/mac-mini/`. The payload includes
Git metadata, tracked and untracked work, and git-ignored data and literature. It does
not change the separate EPRP paleodata mirror. Each successful run retains earlier
generations and updates `latest` only after verification; no automatic pruning is used.

From the project root on mac-mini, create a new generation with:

```sh
python3 tools/backup_nectar.py snapshot --source "$PWD"
```

Run the offline integrity regression checks with `python3 tools/test_backup_nectar.py`.

The intended Codex scheduled task runs the same command daily at 02:00 on the mac-mini's
local clock. Check Scheduled in the app for whether it is active and for failures. The
mac-mini and desktop app must be running for an unattended task to start.

The script checks the source inventory and hashes, requests a local macOS copy-on-write
capture, checks it against the source, and transfers that stable capture over SSH with
compression. If the filesystem cannot clone, macOS falls back to a normal copy; the script reserves
enough local space for that case. If another job changes the source during hashing or
capture, the script stops; retry once the source is quiet.
The destination verifies every file's SHA-256 and size, checks the captured Git
objects, and performs a sample restore before promotion. The capture is not an atomic
transaction across independently updated files. It preserves file bytes, paths and
POSIX modes, not macOS extended attributes, ACLs, owners or resource forks.

The backup root is private to the `codex` account and its administrators. Completed
generations are made read-only by ordinary filesystem permissions, not WORM protection.
Incremental generations share read-only hardlinks for unchanged files: in-place edits,
permission changes or corruption of a shared inode can affect several generations.
Never edit the backup tree; restore to a new location first. The previous and new
generations are checksum-verified before promotion.

The attached `/data` volume is not included in Nectar's instance-root snapshots. The
script stops on symlinks, special files, Git locks, credential-like filenames, sensitive
Git configuration, protected PBDB receipt/history names, and recognised SQLite,
Access or DuckDB files or sidecars without a dedicated capture method. The known
fixed-release Palynodata Access database is accepted only at its recorded SHA-256.
These checks are not a general classifier for every possible secret or database.
Failed staging is retained for inspection. Local captures are under
`/private/tmp/silurian-plants-backup/` and
removed after a verified successful run; small receipts remain. The backup root is for
the mac-mini producer only: all its invocations use one local lock, but another host
writing the same root would not be coordinated. Each run reserves enough free space
for twice the full payload plus 20 GiB, even when an incremental run needs less.

For recovery, identify a generation under `snapshots/` and use the remote script to
verify it, then restore to a **new** directory. For example, replace `GENERATION` with
the recorded generation name in these commands:

```sh
ssh nectar-codex-ts python3 /data/codex/silurian_plants/backups/mac-mini/backup_nectar.py verify /data/codex/silurian_plants/backups/mac-mini/snapshots/GENERATION
ssh nectar-codex-ts python3 /data/codex/silurian_plants/backups/mac-mini/backup_nectar.py restore /data/codex/silurian_plants/backups/mac-mini/snapshots/GENERATION /data/codex/silurian_plants/restores/GENERATION
rsync -a nectar-codex-ts:/data/codex/silurian_plants/restores/GENERATION/ /path/to/new-local-directory/
```

The restore command refuses an existing target and reinstates the captured POSIX
modes. Confirm the destination before using the restored project; do not overwrite an
active checkout.
