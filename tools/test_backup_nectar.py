#!/usr/bin/env python3
"""Offline regression checks for the Nectar backup's integrity guards."""

import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import backup_nectar as backup


class BackupIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="silurian-backup-test-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        for directory, _, _ in os.walk(self.root):
            os.chmod(directory, stat.S_IMODE(os.stat(directory).st_mode) | 0o700)
        self.temp.cleanup()

    def git_source(self):
        source = self.root / "source"
        source.mkdir()
        subprocess.run(["git", "init", "-q", str(source)], check=True)
        subprocess.run(["git", "-C", str(source), "config", "user.name", "Backup Test"], check=True)
        subprocess.run(["git", "-C", str(source), "config", "user.email", "test@example.invalid"], check=True)
        (source / "tracked.txt").write_text("first version\n")
        (source / "nested").mkdir()
        (source / "nested" / "untracked.txt").write_text("private work\n")
        subprocess.run(["git", "-C", str(source), "add", "tracked.txt"], check=True)
        subprocess.run(["git", "-C", str(source), "-c", "core.hooksPath=/dev/null",
                        "commit", "-qm", "fixture"], check=True)
        return source

    def partial_generation(self, source):
        root = self.root / "backup"
        generation = "20261028T000000.000000Z"
        partial = root / "snapshots" / (generation + ".partial")
        partial.mkdir(parents=True)
        before = backup.inventory(source)
        files = {rel: backup.file_record(source / rel) for rel in before["files"]}
        project = partial / "project"
        shutil.copytree(source, project)
        for rel in files:
            path = project / rel
            path.chmod(before["modes"][rel] & ~0o222)
        head = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"],
                              check=True, capture_output=True, text=True).stdout.strip()
        backup.write_json(partial / "manifest.json", {
            "files": files, "directories": before["dirs"],
            "source_modes": before["modes"], "git_head": head,
        })
        return root, generation, partial

    def test_guards_reject_unstable_or_sensitive_inputs(self):
        cases = [(".git/index.lock", "Git lock"), (".env", "Credential-like"),
                 ("other.sqlite3-wal", "Database"), ("other.mdb", "Access database")]
        for name, message in cases:
            with self.subTest(name=name):
                source = self.root / name.replace("/", "_")
                source.mkdir()
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture")
                with self.assertRaisesRegex(RuntimeError, message):
                    backup.inventory(source)
        source = self.root / "link-fixture"
        source.mkdir()
        (source / "link").symlink_to("target")
        with self.assertRaisesRegex(RuntimeError, "Unsupported symlink"):
            backup.inventory(source)

    def test_published_snapshot_and_restore_are_verified(self):
        source = self.git_source()
        root, generation, partial = self.partial_generation(source)
        result = backup.publish(root, generation)
        completed = root / "snapshots" / generation
        self.assertEqual(result["verification"]["sha256"], "all_match")
        self.assertEqual(result["verification"]["git"]["fsck"], "ok")
        self.assertEqual(result["restore_test"]["sha256"], "all_match")
        self.assertEqual((root / "latest").resolve(), (completed / "project").resolve())
        self.assertEqual(backup.verify(completed)["sha256"], "all_match")
        restored = self.root / "restored"
        self.assertEqual(backup.restore(completed, restored)["sha256"], "all_match")
        self.assertEqual((restored / "nested" / "untracked.txt").read_text(), "private work\n")
        self.assertEqual(stat.S_IMODE((restored / "tracked.txt").stat().st_mode),
                         stat.S_IMODE((source / "tracked.txt").stat().st_mode))
        with self.assertRaisesRegex(RuntimeError, "must be new"):
            backup.restore(completed, restored)
        self.assertFalse(partial.exists())

    def test_corrupt_partial_does_not_move_latest(self):
        source = self.git_source()
        root, generation, partial = self.partial_generation(source)
        previous = root / "snapshots" / "previous" / "project"
        previous.mkdir(parents=True)
        (root / "latest").symlink_to(Path("snapshots/previous/project"))
        path = partial / "project" / "tracked.txt"
        path.chmod(0o600)
        path.write_text("corrupted\n")
        with self.assertRaisesRegex(RuntimeError, "Checksum/size mismatch"):
            backup.publish(root, generation)
        self.assertEqual((root / "latest").resolve(), previous.resolve())
        self.assertTrue(partial.exists())

    def test_source_drift_stops_before_remote_transfer(self):
        source = self.git_source()
        real_run = backup.run

        def mutate_after_clone(args, **kwargs):
            if str(args[0]) in {"ssh", "scp", "rsync"}:
                raise AssertionError("unexpected network command")
            result = real_run(args, **kwargs)
            if str(args[0]) == "/bin/cp":
                (source / "tracked.txt").write_text("changed during capture\n")
            return result

        args = SimpleNamespace(source=source, stage=self.root / "staging",
                               root=Path("/data/unused-test-root"),
                               host="unused-test-host", reserve_gib=20)
        with patch.object(backup, "LOCK_ROOT", self.root / "lock"), \
                patch.object(backup, "run", side_effect=mutate_after_clone), \
                patch.object(backup, "remote", side_effect=AssertionError("unexpected remote call")):
            with self.assertRaisesRegex(RuntimeError, "Source drift while cloning"):
                backup.snapshot(args)


if __name__ == "__main__":
    unittest.main()
