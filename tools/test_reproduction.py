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
    (tmp_path / "library").mkdir()
    (tmp_path / "library/closed.tsv").write_text(
        "abuhmida2013-thesis-related_macbook20261030\t\ttitle\tclosed/x.pdf\t"
        "https://etheses.whiterose.ac.uk/id/eprint/4475/\troute\t641\t9\t"
        "expected-hash\tdate\tnote\n"
    )
    reproduce.source_checks()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "SKIPPED"
    assert report["missing"] == ["library/closed/abuhmida2013-thesis-related_macbook20261030.pdf"]
    assert report["expected_bytes"] == 9
    assert report["expected_sha256"] == "expected-hash"
    assert report["public_route"].startswith("https://etheses.whiterose.ac.uk/")


def test_optimiser_comparison_allows_roundoff_but_keeps_identity_exact(tmp_path):
    reproduce = module(ROOT / "tools/reproduce.py", "reproduce_compare_test")
    reference = tmp_path / "reference.csv"
    candidate = tmp_path / "candidate.csv"
    content = "grouping,n_reference,rho_f_contour,scope\nindependent,59,0.09102964787638201,retrospective\n"
    reference.write_text(content)
    candidate.write_text(content.replace("0.09102964787638201", "0.09102964787638246"))
    assert reproduce.compare_csv(reference, candidate, identity_columns={"grouping", "n_reference"})["status"] == "PASS"
    candidate.write_text(content.replace(",59,", ",60,"))
    assert reproduce.compare_csv(reference, candidate, identity_columns={"grouping", "n_reference"})["status"] == "FAIL"


def test_optimiser_comparison_rejects_non_numeric_or_large_numeric_drift(tmp_path):
    reproduce = module(ROOT / "tools/reproduce.py", "reproduce_compare_drift_test")
    reference = tmp_path / "reference.csv"
    candidate = tmp_path / "candidate.csv"
    reference.write_text("key,value,note\nA,1.0,ok\n")
    candidate.write_text("key,value,note\nA,1.0001,ok\n")
    assert reproduce.compare_csv(reference, candidate, identity_columns={"key"})["status"] == "FAIL"
    candidate.write_text("key,value,note\nA,1.0,changed\n")
    assert reproduce.compare_csv(reference, candidate, identity_columns={"key"})["status"] == "FAIL"


def test_public_source_check_reports_route_and_hash(tmp_path, capsys):
    reproduce = module(ROOT / "tools/reproduce.py", "reproduce_source_manifest_test")
    reproduce.ROOT = tmp_path
    source = tmp_path / "library/closed/abuhmida2013-thesis-related_macbook20261030.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"test source")
    manifest = tmp_path / "library/closed.tsv"
    expected = __import__("hashlib").sha256(source.read_bytes()).hexdigest()
    manifest.write_text("abuhmida2013-thesis-related_macbook20261030\t\ttitle\tclosed/x.pdf\thttps://etheses.whiterose.ac.uk/id/eprint/4475/\troute\t641\t11\t" + expected + "\tdate\tnote\n")
    reproduce.execute = lambda command, cwd: None
    reproduce.source_checks()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "PASS"
    assert report["public_route"].startswith("https://etheses.whiterose.ac.uk/")
    assert report["sha256"] == expected
