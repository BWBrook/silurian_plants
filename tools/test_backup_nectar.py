#!/usr/bin/env python3
"""Local integration and regression checks for the Nectar backup."""

import contextlib
import datetime as dt
import fcntl
import io
import json
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
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "source"
        self.source.mkdir()
        subprocess.run(["git", "init", "-q", str(self.source)], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.name", "Backup Test"], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.email", "test@example.invalid"], check=True)
        (self.source / "tracked.txt").write_text("first version\n")
        (self.source / "nested").mkdir()
        (self.source / "nested" / "untracked.txt").write_text("private work\n")
        (self.source / "tools").mkdir()
        shutil.copy2(Path(backup.__file__), self.source / "tools/backup_nectar.py")
        subprocess.run(["git", "-C", str(self.source), "add", "tracked.txt"], check=True)
        subprocess.run(["git", "-C", str(self.source), "-c", "core.hooksPath=/dev/null",
                        "commit", "-qm", "fixture"], check=True)
        self.destination = self.root / "remote"
        self.destination.mkdir()
        self.stage = self.root / "staging"

    def tearDown(self):
        for directory, _, files in os.walk(self.root):
            os.chmod(directory, stat.S_IMODE(os.stat(directory).st_mode) | 0o700)
            for name in files:
                path = Path(directory) / name
                path.chmod(stat.S_IMODE(path.stat().st_mode) | 0o600)
        self.temp.cleanup()

    def snapshot(self, scrub=False, after_clone=None, after_transfer=None):
        args = SimpleNamespace(source=self.source, stage=self.stage, root=self.destination,
                               host="local-fixture", reserve_gib=0, scrub=scrub)
        original_run = backup.run
        original_subprocess = subprocess.run

        def local_run(argv, **kwargs):
            result = original_run(argv, **kwargs)
            if str(argv[0]) == "/bin/cp" and after_clone:
                after_clone()
            return result

        def local_subprocess(argv, **kwargs):
            if str(argv[0]) == "rsync":
                argv = list(argv)
                index = argv.index("-e")
                del argv[index:index + 2]
                argv[-1] = argv[-1].split(":", 1)[1]
                result = original_subprocess(argv, **kwargs)
                if result.returncode == 0 and after_transfer:
                    after_transfer(Path(argv[-1]))
                return result
            return original_subprocess(argv, **kwargs)

        def local_driver(host, driver, remote_script):
            remote_script.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(driver, remote_script)

        def local_state(host, stage, partial, names):
            for name in names:
                shutil.copy2(stage / name, partial / name)

        def local_remote(host, script, operation, *values, capture=False):
            if operation == "_prepare":
                root, generation, required, reserve, force = values
                return backup.prepare(root, generation, required, reserve, bool(force))
            if operation == "_inherit":
                return backup.inherit(*values)
            if operation == "_publish":
                return backup.publish(*values)
            raise AssertionError("unexpected remote operation " + operation)

        with patch.object(backup, "LOCK_ROOT", self.root / "lock"), \
                patch.object(backup, "on_data_volume", return_value=True), \
                patch.object(backup, "run", side_effect=local_run), \
                patch.object(backup.subprocess, "run", side_effect=local_subprocess), \
                patch.object(backup, "send_driver", side_effect=local_driver), \
                patch.object(backup, "send_state", side_effect=local_state), \
                patch.object(backup, "remote", side_effect=local_remote), \
                contextlib.redirect_stdout(io.StringIO()):
            backup.snapshot(args)
        generation = (self.destination / "latest").resolve().parent
        return generation, json.loads((self.stage / generation.name / "result.json").read_text())

    def corrupt(self, path):
        original = path.stat()
        original_mode = stat.S_IMODE(original.st_mode)
        content = path.read_bytes()
        path.chmod(original_mode | 0o200)
        path.write_bytes(bytes([content[0] ^ 1]) + content[1:])
        path.chmod(original_mode)
        os.utime(path, ns=(original.st_atime_ns, original.st_mtime_ns))

    def test_guards_reject_unstable_or_sensitive_inputs(self):
        cases = [(".git/index.lock", "Git lock"), (".env", "Credential-like"),
                 ("other.sqlite3-wal", "Database"), ("other.mdb", "Access database")]
        for name, message in cases:
            with self.subTest(name=name):
                path = self.source / name
                path.write_text("fixture")
                with self.assertRaisesRegex(RuntimeError, message):
                    backup.inventory(self.source)
                path.unlink()
        (self.source / "link").symlink_to("target")
        with self.assertRaisesRegex(RuntimeError, "Unsupported symlink"):
            backup.inventory(self.source)
        (self.source / "link").unlink()

    def test_two_generations_reuse_and_restore_same_size_preserved_mtime_edit(self):
        first, first_result = self.snapshot()
        self.assertEqual(first_result["verification"]["sha256"], "all_match")
        self.assertEqual(first_result["scrub"]["status"], "passed")
        self.assertEqual(first_result["transfer_stats"]["attempts"], 1)
        self.assertGreater(first_result["transfer_stats"]["final_attempt"][
            "Number of regular files transferred"], 0)
        tracked = self.source / "tracked.txt"
        old = tracked.stat()
        tracked.write_text("other version\n")
        self.assertEqual(tracked.stat().st_size, old.st_size)
        os.utime(tracked, ns=(old.st_atime_ns, old.st_mtime_ns))
        second, result = self.snapshot()
        self.assertEqual(result["verification"]["sha256"], "fresh_match_inherited_metadata_trusted")
        self.assertGreater(result["verification"]["inherited_files"], 0)
        self.assertTrue(os.path.samefile(first / "project/nested/untracked.txt",
                                         second / "project/nested/untracked.txt"))
        self.assertFalse(os.path.samefile(first / "project/tracked.txt", second / "project/tracked.txt"))
        self.assertEqual((first / "project/tracked.txt").read_text(), "first version\n")
        self.assertEqual((second / "project/tracked.txt").read_text(), "other version\n")
        self.assertEqual(backup.verify(second)["sha256"], "all_match")
        restored = self.root / "restored"
        self.assertEqual(backup.restore(second, restored)["sha256"], "all_match")
        self.assertEqual((restored / "tracked.txt").read_text(), "other version\n")
        self.assertEqual((restored / "nested/untracked.txt").read_text(), "private work\n")
        self.assertEqual(stat.S_IMODE((restored / "tracked.txt").stat().st_mode),
                         stat.S_IMODE(tracked.stat().st_mode))
        with self.assertRaisesRegex(RuntimeError, "must be new"):
            backup.restore(second, restored)

    def test_zero_change_generation_reuses_every_file(self):
        first, _ = self.snapshot()
        second, result = self.snapshot()
        verification = result["verification"]
        self.assertEqual(verification["fresh_files"], 0)
        self.assertEqual(verification["inherited_files"], verification["files"])
        self.assertEqual(result["transfer_stats"]["attempts"], 0)
        self.assertIsNone(result["scrub"])
        self.assertTrue(os.path.samefile(first / "project/tracked.txt", second / "project/tracked.txt"))
        self.assertEqual(backup.verify(first)["sha256"], "all_match")

    def test_corrupt_copied_file_does_not_move_latest(self):
        first, _ = self.snapshot()
        (self.source / "tracked.txt").write_text("other version\n")
        with self.assertRaisesRegex(RuntimeError, "Checksum/size mismatch"):
            self.snapshot(after_transfer=lambda project: self.corrupt(project / "tracked.txt"))
        self.assertEqual((self.destination / "latest").resolve(), first / "project")
        self.assertTrue(list((self.destination / "snapshots").glob("*.partial")))

    def test_scrub_detects_corruption_in_shared_inode_without_success_marker(self):
        first, _ = self.snapshot()
        second, _ = self.snapshot()
        first_shared = first / "project/nested/untracked.txt"
        self.assertTrue(os.path.samefile(first_shared, second / "project/nested/untracked.txt"))
        marker = (self.destination / "last-scrub.json").read_bytes()
        self.corrupt(first_shared)
        with self.assertRaisesRegex(RuntimeError, "Checksum/size mismatch"):
            self.snapshot(scrub=True)
        self.assertEqual((self.destination / "latest").resolve(), second / "project")
        self.assertEqual((self.destination / "last-scrub.json").read_bytes(), marker)

    def test_scrub_detects_corruption_in_older_unique_version(self):
        first, _ = self.snapshot()
        (self.source / "tracked.txt").write_text("other version\n")
        second, _ = self.snapshot()
        self.assertFalse(os.path.samefile(first / "project/tracked.txt", second / "project/tracked.txt"))
        marker = (self.destination / "last-scrub.json").read_bytes()
        self.corrupt(first / "project/tracked.txt")
        with self.assertRaisesRegex(RuntimeError, "Checksum/size mismatch"):
            self.snapshot(scrub=True)
        self.assertEqual((self.destination / "latest").resolve(), second / "project")
        self.assertEqual((self.destination / "last-scrub.json").read_bytes(), marker)

    def test_scrub_does_not_rebaseline_unchanged_source_signature(self):
        first, _ = self.snapshot()
        original = backup.file_record

        def silent_corruption(path):
            record = original(path)
            if path == self.source / "tracked.txt":
                record["sha256"] = "0" * 64
            return record

        with patch.object(backup, "file_record", side_effect=silent_corruption):
            with self.assertRaisesRegex(RuntimeError, "Unchanged-signature source checksum mismatch"):
                self.snapshot(scrub=True)
        self.assertEqual((self.destination / "latest").resolve(), first / "project")
        self.assertTrue((self.destination / "scrub-pending.json").is_file())
        _, retried = self.snapshot()
        self.assertEqual(retried["scrub"]["status"], "passed")
        self.assertFalse((self.destination / "scrub-pending.json").exists())

    def test_previous_file_replacement_with_identical_metadata_is_rejected(self):
        first, _ = self.snapshot()
        target = first / "project/nested/untracked.txt"
        original = target.stat()
        parent = target.parent
        parent_mode = stat.S_IMODE(parent.stat().st_mode)
        parent.chmod(parent_mode | 0o200)
        replacement = parent / "replacement"
        replacement.write_bytes(target.read_bytes())
        replacement.chmod(stat.S_IMODE(original.st_mode))
        os.utime(replacement, ns=(original.st_atime_ns, original.st_mtime_ns))
        replacement.replace(target)
        parent.chmod(parent_mode)
        self.assertNotEqual(target.stat().st_ino, original.st_ino)
        self.assertEqual(target.stat().st_size, original.st_size)
        self.assertEqual(target.stat().st_mtime_ns, original.st_mtime_ns)
        with self.assertRaisesRegex(RuntimeError, "Destination file identity mismatch"):
            self.snapshot()
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_previous_file_mtime_change_is_rejected(self):
        first, _ = self.snapshot()
        target = first / "project/nested/untracked.txt"
        original = target.stat()
        os.utime(target, ns=(original.st_atime_ns, original.st_mtime_ns + 1_000_000))
        with self.assertRaisesRegex(RuntimeError, "Destination file identity mismatch"):
            self.snapshot()
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_missing_previous_source_inventory_stops_before_rebaseline(self):
        first, _ = self.snapshot()
        first_mode = stat.S_IMODE(first.stat().st_mode)
        first.chmod(first_mode | 0o200)
        (first / "source-before.json").unlink()
        first.chmod(first_mode)
        with self.assertRaisesRegex(RuntimeError, "no source inventory"):
            self.snapshot(scrub=True)
        self.assertTrue((self.destination / "scrub-pending.json").exists())
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_source_identity_change_stops_before_rebaseline(self):
        first, _ = self.snapshot()
        old_source = self.root / "source-old"
        self.source.rename(old_source)
        shutil.copytree(old_source, self.source)
        with self.assertRaisesRegex(RuntimeError, "Source identity differs"):
            self.snapshot(scrub=True)
        self.assertTrue((self.destination / "scrub-pending.json").exists())
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_missing_latest_does_not_start_a_new_lineage(self):
        first, _ = self.snapshot()
        (self.destination / "latest").unlink()
        with self.assertRaisesRegex(RuntimeError, "Latest is missing while retained generations exist"):
            self.snapshot()
        self.assertTrue(first.is_dir())
        self.assertFalse((self.destination / "latest").exists())

    def test_remote_publication_lock_blocks_competing_publisher(self):
        first, _ = self.snapshot()
        with (self.destination / ".publish.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):
                backup.publish(self.destination, "not-started")
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_seven_day_scrub_and_force_scrub(self):
        first, _ = self.snapshot()
        real_datetime = dt.datetime

        class FutureDateTime(real_datetime):
            @classmethod
            def now(cls, tz=None):
                return real_datetime.now(tz) + dt.timedelta(days=8)

        with patch.object(backup.dt, "datetime", FutureDateTime):
            second, result = self.snapshot()
        self.assertIsNotNone(result["scrub"])
        self.assertEqual(result["scrub"]["generations"], 1)
        self.assertEqual(result["verification"]["sha256"], "all_match")
        self.assertEqual(json.loads((self.destination / "last-scrub.json").read_text())["generation"],
                         second.name)
        _, forced = self.snapshot(scrub=True)
        self.assertEqual(forced["scrub"]["generations"], 2)
        self.assertTrue((first / "project/tracked.txt").exists())

    def test_source_drift_during_capture_does_not_move_latest(self):
        first, _ = self.snapshot()
        with self.assertRaisesRegex(RuntimeError, "Source drift while cloning"):
            self.snapshot(after_clone=lambda: (self.source / "tracked.txt").write_text("changed during clone\n"))
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_replaced_legacy_source_is_rejected(self):
        first, _ = self.snapshot()
        manifest_path = first / "manifest.json"
        manifest_path.chmod(0o600)
        manifest = json.loads(manifest_path.read_text())
        manifest.pop("source_root")
        backup.write_json(manifest_path, manifest)
        manifest_path.chmod(0o400)
        replacement = self.root / "replacement"
        shutil.copytree(self.source, replacement)
        self.source.rename(self.root / "retired-source")
        replacement.rename(self.source)
        with self.assertRaisesRegex(RuntimeError, "Legacy source identity"):
            self.snapshot(scrub=True)
        self.assertEqual((self.destination / "latest").resolve(), first / "project")

    def test_legacy_generation_is_accepted_and_scrubbed(self):
        first, _ = self.snapshot()
        first_mode = stat.S_IMODE(first.stat().st_mode)
        first.chmod(first_mode | 0o200)
        (first / "file-identities.json").unlink()
        first.chmod(first_mode)
        manifest_path = first / "manifest.json"
        manifest_path.chmod(0o600)
        manifest = json.loads(manifest_path.read_text())
        for key in ("source_root", "inherited", "scrub", "based_on"):
            manifest.pop(key, None)
        manifest["format"] = 1
        backup.write_json(manifest_path, manifest)
        manifest_path.chmod(0o400)
        second, result = self.snapshot()
        self.assertEqual(result["scrub"]["generations"], 1)
        self.assertEqual(result["verification"]["sha256"], "all_match")
        self.assertTrue(os.path.samefile(first / "project/nested/untracked.txt",
                                         second / "project/nested/untracked.txt"))


if __name__ == "__main__":
    unittest.main()
