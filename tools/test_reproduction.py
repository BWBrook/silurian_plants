import importlib.util
import json
from pathlib import Path

import pytest


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


ROOT = Path(__file__).resolve().parents[1]


def test_restore_refuses_to_replace_different_existing_input(tmp_path):
    fetch = module(ROOT / "data/external/scripts/fetch_pbdb_snapshot.py", "pbdb_restore_test")
    target = tmp_path / "snapshot.csv"
    target.write_bytes(b"different historical snapshot")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        fetch.restore(target)
    assert target.read_bytes() == b"different historical snapshot"


def test_dependency_closure_requires_declared_input_and_finds_local_import(tmp_path):
    package = module(ROOT / "manuscript/package.py", "package_test")
    package.ROOT = tmp_path
    (tmp_path / "data/external").mkdir(parents=True)
    (tmp_path / "data/external/pbdb-snapshot.json").write_text(json.dumps({"path": "data/raw.csv", "url": "archive"}))
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/helper.py").write_text("value = 1\n")
    (tmp_path / "tools/runner.py").write_text("import helper\n")
    (tmp_path / "data/receipt.json").write_text(json.dumps({"inputs": {"tools/runner.py": "hash", "data/missing.csv": "hash"}}))
    with pytest.raises(FileNotFoundError, match="missing.csv"):
        package.dependency_closure({"data/receipt.json"})
    (tmp_path / "data/missing.csv").write_text("x\n1\n")
    rows = package.dependency_closure({"data/receipt.json"})
    assert {r["path"] for r in rows} == {"data/receipt.json", "data/missing.csv", "tools/runner.py", "tools/helper.py"}


def test_public_checkout_reports_private_source_check_as_skipped(tmp_path, capsys):
    reproduce = module(ROOT / "tools/reproduce.py", "reproduce_skip_test")
    reproduce.ROOT = tmp_path
    reproduce.source_checks()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "SKIPPED"
    assert report["missing"] == ["library/closed/abuhmida2013-thesis-related_macbook20261030.pdf"]
