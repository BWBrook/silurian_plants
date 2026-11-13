"""Evidence failures and the complete calibration/acceptance/stage-2 lifecycle."""

import copy
import csv
import gzip
import io
import json
import math
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

import designs as dz
import envelope as ev
import m2
import qualification_contract as qc
import qualify as qa


@pytest.fixture
def binding():
    return dict(design="TEST", rho=1.0, files={"active_declaration": "a" * 64}, generated_units=[],
                fitted_reference_rates=[1.0], derived_tolerance=qc.DERIVED_TOLERANCE,
                protocol=qc.protocol(dz.declarations()), qualification_classes=["H0"],
                grid=[dict(name="A", kind="acceptance", quantities=["f_H0", "o_H0_0.1"]),
                      dict(name="B", kind="acceptance", quantities=["f_H0"]),
                      dict(name="X", kind="diagnostic", quantities=["f_H0"])])


def rows_for(cells, hits=None, n=1000):
    hits = hits or {}
    rows = []
    for c in cells:
        for i in range(n):
            row = dict(cell=c["name"], rep=i, passed=True, error="", trivial=False,
                       screen_status="evaluated", screen_converged=True, screen_n_older_detections=0,
                       screen_lr=7.0, screen_crit=ev.count_crit(0))
            for q in c["quantities"]:
                ok = i < hits.get((c["name"], q), n)
                row[f"c_{q}"], row[f"m_{q}"] = ok, -1.0 if ok else 1.0
            rows.append(row)
    return rows


def save(base, binding, phase, hits=None, first=None, rows=None):
    cal = qc.load(base, binding, "calibrate") if phase != "calibrate" else None
    dependencies = {} if cal is None else {"calibrate": cal.sha256}
    if phase == "stage2":
        first = qc.load(base, binding, "accept")
        dependencies["accept"] = first.sha256
        first = first.record
    grid = qc.phase_cells(binding, phase, first)
    if rows is None:
        rows = rows_for(grid, hits)
    p = binding["protocol"]
    return qc.write(base, binding, phase, rows, p["root_seeds"][phase], p["target_passing"],
                    p["max_attempts"], 0.0 if cal is None else cal.record["delta"], dependencies,
                    {"python": "test"}, 0.0, first)


def edit_record(path, change):
    record = json.loads(path.read_text())
    change(record)
    path.write_text(json.dumps(qc.seal(record)))


def edit_reps(base, binding, phase, change):
    rec_path, rep_path = qc.paths(base, binding, phase)
    reader = csv.DictReader(io.StringIO(gzip.decompress(rep_path.read_bytes()).decode()))
    fields, rows = reader.fieldnames, list(reader)
    change(fields, rows)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    rep_path.write_bytes(gzip.compress(buf.getvalue().encode(), mtime=0))
    edit_record(rec_path, lambda r: r["replicates"].update(sha256=qc.file_hash(rep_path)))


@pytest.mark.parametrize("second,expected", [(946, "pass"), (945, "fail")])
def test_valid_lifecycle_pools_only_borderline_quantities(tmp_path, binding, second, expected):
    save(tmp_path, binding, "calibrate")
    save(tmp_path, binding, "accept", {("A", "f_H0"): 940})
    first = qc.load(tmp_path, binding, "accept").record
    assert first["result"] == "borderline" and first["borderline_cells"] == ["A"]
    save(tmp_path, binding, "stage2", {("A", "f_H0"): second, ("A", "o_H0_0.1"): 0})
    final = qc.load(tmp_path, binding, "stage2").record
    assert final["result"] == expected
    assert final["verdicts"]["A:o_H0_0.1"] == "pass"
    assert {s["cell"] for s in final["cells"]} == {"A"}


def test_stage2_is_not_a_replacement_for_passed_stage1(tmp_path, binding):
    save(tmp_path, binding, "calibrate")
    save(tmp_path, binding, "accept")
    with pytest.raises(qc.EvidenceError, match="borderline"):
        save(tmp_path, binding, "stage2")


@pytest.mark.parametrize("key,value", [("phase", "dev"), ("root", 123), ("target", 5), ("cap", 1000),
                                       ("shift", -1), ("shift", True), ("delta", -1), ("delta", math.inf)])
def test_resealed_wrong_protocol_or_shift_is_refused(tmp_path, binding, key, value):
    written = save(tmp_path, binding, "calibrate")
    edit_record(written.path, lambda r: r.update({key: value}))
    with pytest.raises(qc.EvidenceError):
        qc.load(tmp_path, binding, "calibrate")


@pytest.mark.parametrize("component", ["files", "generated_units", "protocol", "grid"])
def test_stale_binding_is_refused(tmp_path, binding, component):
    save(tmp_path, binding, "calibrate")
    changed = copy.deepcopy(binding)
    if component == "files":
        changed["files"]["active_declaration"] = "b" * 64
    elif component == "generated_units":
        changed[component] = [{"d": 1}]
    elif component == "protocol":
        changed[component]["root_seeds"]["accept"] += 1
    else:
        changed[component][0]["quantities"].append("w_1")
    with pytest.raises(qc.EvidenceError, match="bind"):
        qc.load(tmp_path, changed, "calibrate")


def test_derived_fits_allow_only_declared_numerical_tolerance(tmp_path, binding):
    save(tmp_path, binding, "calibrate")
    changed = copy.deepcopy(binding)
    changed["fitted_reference_rates"][0] += 1e-10
    assert qc.load(tmp_path, changed, "calibrate").record["complete"]
    changed["fitted_reference_rates"][0] += 1e-4
    with pytest.raises(qc.EvidenceError, match="tolerance"):
        qc.load(tmp_path, changed, "calibrate")


def test_acceptance_must_retain_exact_calibration_truth(tmp_path, binding):
    save(tmp_path, binding, "calibrate")
    accepted = save(tmp_path, binding, "accept")
    def change(r):
        r["binding"]["fitted_reference_rates"][0] += 1e-10
        r["binding_sha256"] = qc.digest(r["binding"])
    edit_record(accepted.path, change)
    with pytest.raises(qc.EvidenceError, match="exact resolved truth"):
        qc.load(tmp_path, binding, "accept")


@pytest.mark.parametrize("which", ["one", "whole_column"])
def test_missing_required_coverage_cannot_default_to_success(tmp_path, binding, which):
    save(tmp_path, binding, "calibrate")
    def remove(fields, rows):
        for row in rows if which == "whole_column" else rows[:1]:
            row["c_f_H0"] = ""
    edit_reps(tmp_path, binding, "calibrate", remove)
    with pytest.raises(qc.EvidenceError, match="declared quantities"):
        qc.load(tmp_path, binding, "calibrate")


@pytest.mark.parametrize("value", ["", "true", "1", "NaN"])
def test_strict_boolean_flags(tmp_path, binding, value):
    save(tmp_path, binding, "calibrate")
    edit_reps(tmp_path, binding, "calibrate", lambda fields, rows: rows[0].update(passed=value))
    with pytest.raises(qc.EvidenceError):
        qc.load(tmp_path, binding, "calibrate")


@pytest.mark.parametrize("mutation", ["duplicate", "reordered", "removed", "no_cell", "screen_contradiction"])
def test_resealed_malformed_attempt_ledger_is_refused(tmp_path, binding, mutation):
    save(tmp_path, binding, "calibrate")
    def change(fields, rows):
        if mutation == "duplicate":
            rows[1]["rep"] = rows[0]["rep"]
        elif mutation == "reordered":
            rows[0], rows[1] = rows[1], rows[0]
        elif mutation == "removed":
            rows.pop(0)
        elif mutation == "no_cell":
            rows[:] = [r for r in rows if r["cell"] != "B"]
        else:
            rows[0]["screen_lr"] = "0"
    edit_reps(tmp_path, binding, "calibrate", change)
    with pytest.raises(qc.EvidenceError):
        qc.load(tmp_path, binding, "calibrate")


def test_forged_summary_or_dependency_is_recomputed(tmp_path, binding):
    cal = save(tmp_path, binding, "calibrate")
    accepted = save(tmp_path, binding, "accept")
    edit_record(accepted.path, lambda r: r["cells"][0].update(cover_f_H0=999))
    with pytest.raises(qc.EvidenceError, match="replicate evidence"):
        qc.load(tmp_path, binding, "accept")
    edit_record(accepted.path, lambda r: r["cells"][0].update(cover_f_H0=1000))
    edit_record(cal.path, lambda r: r.update(runtime={"python": "another recorded machine"}))
    with pytest.raises(qc.EvidenceError, match="another calibration"):
        qc.load(tmp_path, binding, "accept")


def test_payload_and_replicate_hashes_are_both_checked(tmp_path, binding):
    written = save(tmp_path, binding, "calibrate")
    original = written.path.read_text()
    written.path.write_text(original.replace('"seconds": 0.0', '"seconds": 1.0'))
    with pytest.raises(qc.EvidenceError, match="payload checksum"):
        qc.load(tmp_path, binding, "calibrate")
    written.path.write_text(original)
    _, reps = qc.paths(tmp_path, binding, "calibrate")
    reps.write_bytes(reps.read_bytes() + b"extra")
    with pytest.raises(qc.EvidenceError, match="replicate file checksum"):
        qc.load(tmp_path, binding, "calibrate")


def test_pre_screen_error_prevents_completion_even_after_target_passes(tmp_path, binding):
    rows = rows_for(qc.phase_cells(binding, "calibrate"))
    for row in rows:
        if row["cell"] == "A":
            row["rep"] += 1
    rows.insert(0, dict(cell="A", rep=0, passed=False, error="simulation failed", screen_status="error", screen_converged=False))
    save(tmp_path, binding, "calibrate", rows=rows)
    receipt = qc.load(tmp_path, binding, "calibrate").record
    assert not receipt["complete"] and receipt["delta"] is None
    assert receipt["cells"][0]["errors_before_screen"] == 1
    with pytest.raises(qc.EvidenceError):
        save(tmp_path, binding, "accept")


def test_post_screen_error_stays_in_every_quantity_denominator(binding):
    c = binding["grid"][0]
    rows = rows_for([c])
    rows[0].update(error="optimizer failed")
    for q in c["quantities"]:
        rows[0][f"c_{q}"], rows[0][f"m_{q}"] = False, math.inf
    summary = qc.summarise(rows, c, 1000, 20000, 0.0, 0.955)
    assert summary["complete"] and summary["errors"] == 1
    assert all(summary[f"cover_{q}"] == 999 and summary[f"claimmiss_{q}"] == 1 for q in c["quantities"])


def test_incomplete_attempt_cap_cannot_calibrate(tmp_path, binding):
    c = binding["grid"][0]
    rows = [dict(cell=c["name"], rep=i, passed=False, error="", screen_status="no-first-appearance") for i in range(20000)]
    rows += rows_for(binding["grid"][1:])
    save(tmp_path, binding, "calibrate", rows=rows)
    record = qc.load(tmp_path, binding, "calibrate").record
    assert not record["complete"] and record["delta"] is None


def test_binding_artifacts_are_immutable_and_dev_is_not_binding(tmp_path, binding):
    save(tmp_path, binding, "calibrate")
    with pytest.raises(qc.EvidenceError, match="already exist"):
        save(tmp_path, binding, "calibrate")
    with pytest.raises(qc.EvidenceError, match="development"):
        qc.load(tmp_path, binding, "dev")


@pytest.mark.parametrize("phase,flag", [("calibrate", "--target"), ("accept", "--target"), ("stage2", "--no-diagnostics")])
def test_cli_rejects_binding_target_or_diagnostic_overrides(phase, flag):
    args = ["--design", "LY-H2-CU", "--rho", "1", "--phase", phase, flag]
    if flag == "--target":
        args.append("4")
    with pytest.raises(SystemExit):
        qa.main(args)


def test_active_declaration_sources_statistical_dependencies_and_class_scope_are_bound(monkeypatch, tmp_path):
    active = tmp_path / "active.toml"
    active.write_text(dz.DESIGNS.read_text())
    monkeypatch.setattr(dz, "DESIGNS", active)
    _, binding, _ = qa.build_binding("QB-CO", 1.0)
    assert binding["files"]["active_declaration"] == qc.file_hash(active)
    assert {"studies/f3/models/validate.py", "studies/f3/models/sim.py", "studies/f3/models/units_sim.py", "data/timescale.csv",
            "studies/f3/data/units/outcomes.csv", "studies/f3/data/units/qusaiba_inventory.csv", "studies/f3/data/units/borenshult_ages.csv",
            "studies/f3/data/units/source_files.csv", "studies/f3/data/units/reporting-rule.md"} <= set(binding["files"])
    assert binding["generated_units"]["rows"] and binding["qualification_classes"] == ["H0m", "H0", "H1"]
    assert all("H0c" not in q for c in binding["grid"] for q in c["quantities"])
    b3 = next(c for c in binding["grid"] if c["name"] == "B3")
    assert b3["t0"] == b3["f_data"]["at"] == 459.1 and "f_H0" in b3["quantities"]
    with pytest.raises(qc.EvidenceError, match="historical"):
        m2.shift_for("LY-H2-CU", 1.0)


def test_declared_boundary_and_origin_step_are_used():
    calls = []
    ctx = SimpleNamespace(decl={"common": {"domain_ma": 560.0}}, spec0=SimpleNamespace(classes=("H0",)), tau0=443.1,
                          data=SimpleNamespace(fstar=lambda k, t: calls.append((k, t)) or SimpleNamespace(value=.3, converged=True)))
    assert qa.resolve(dict(f_data={"class": "H0", "at": 480.0}), ctx)["f"] == .3
    assert calls == [("H0", 480.0)]
    pr = SimpleNamespace(tau=443.1, spec=SimpleNamespace(classes=(), readouts=()), grid=lambda step: calls.append(step))
    m2.readouts(pr, dict(report_ma=[], origin_step_ma=.25))
    assert calls[-1] == .25


def test_unconverged_screen_is_not_an_ordinary_rejection():
    pr = SimpleNamespace(n_old=1, spec=SimpleNamespace(domain_ma=(0, 560), alpha=.05), exposure=lambda t: 1,
                         n_older_detections=lambda t: 0, lr=lambda *a: SimpleNamespace(converged=False, value=1.0))
    with pytest.raises(RuntimeError, match="converge"):
        m2.screen(pr)


def test_run_cell_retains_every_consumed_attempt():
    class Pool:
        def map(self, func, jobs, chunksize):
            return [dict(rep=j[3], passed=j[3] in {1, 3}) for j in jobs]
    rows, attempts = qa.run_cell(Pool(), "test", 1, {}, 1, 0, 2, 40, [1.0])
    assert attempts == 4 and [r["rep"] for r in rows] == [0, 1, 2, 3]


@pytest.mark.parametrize("design_id,reading,role", [("QB-CO", "main", "primary"),
                                                   ("QB-CO", "zero", "inadmissible-coding-diagnostic"),
                                                   ("LY-H2-CU", "appendix-only", "sensitivity")])
def test_empirical_scope_does_not_qualify_sensitivities(monkeypatch, tmp_path, design_id, reading, role):
    decl = dz.declarations()
    design = next(d for d in decl["design"] if d["id"] == design_id)
    variant = {k: v for k, v in design["primary"].items() if k != "min_ref_units"}
    if reading == "zero":
        variant["bor_unresolved"] = "zero"
    elif reading == "appendix-only":
        variant["material_type"] = reading
    binding = dict(qualification_classes=design.get("qualification_classes", decl["common"]["classes"]))
    monkeypatch.setattr(m2, "shift_for", lambda *a: (0.0, "pass", "a" * 64, binding))
    monkeypatch.setattr(m2, "readouts", lambda *a: {})
    monkeypatch.setattr(m2, "problem", lambda *a, **k: SimpleNamespace(tau=443.1, n_ref=2, rd=np.array([1]),
                                                                     n_old=1, od=np.array([0]), r_ref=[1.0]))
    m2._QUALIFICATIONS.clear()
    row = m2._result((design_id, variant, 5, 1.0, tmp_path))
    assert row["analysis_role"] == role
    if role == "primary":
        assert row["qualification_H0"] == "pass" and row["qualification_H0c"] == "unqualified-class-diagnostic"
    else:
        assert row["qualification"] != "pass" and row["qualification_H0"] != "pass"


def test_results_screen_current_inputs_instead_of_reading_stale_csv(monkeypatch, tmp_path):
    decl = dict(common=dict(min_ref_units=[5], rho=[1.0]), design=[dict(id="LY-H2-CU")])
    variant = dict(cluster_k=math.inf)
    monkeypatch.setattr(dz, "declarations", lambda *a: decl)
    monkeypatch.setattr(dz, "variants", lambda *a: [variant])
    monkeypatch.setattr(qa, "bound_paths", lambda *a: {})
    monkeypatch.setattr(m2, "OUT", tmp_path)
    (tmp_path / "m2_screen.csv").write_text("stale and not even a CSV")
    called = []
    monkeypatch.setattr(m2, "run_screen", lambda: called.append(True) or
                        [dict(design="LY-H2-CU", variant=m2.vkey(variant), min_ref=5, rho=1.0, passes=True)])
    monkeypatch.setattr(m2, "_result", lambda job: dict(current=True))
    class Pool:
        def __init__(self, workers): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def map(self, f, jobs, chunksize): return list(map(f, jobs))
    monkeypatch.setattr("multiprocessing.Pool", Pool)
    assert m2.run_results(1) == [dict(current=True)] and called == [True]


def test_nonprimary_result_survives_a_failing_unqualified_primary(monkeypatch, tmp_path):
    monkeypatch.setattr(m2, "readouts", lambda *args: {})
    m2._QUALIFICATIONS.clear()
    row = m2._result(("QB-CO", dict(reading="inclusive", bor_unresolved="excluded", cluster_k=2.0), 5, .5, tmp_path))
    assert row["qualification"] == "sensitivity-unqualified" and row["primary_qualification"] == "not qualified"
    with pytest.raises(qc.EvidenceError, match="primary data do not pass"):
        qa.main(["--design", "QB-CO", "--rho", ".5", "--phase", "calibrate", "--out-dir", str(tmp_path)])


def test_window_boundary_path_is_nonmonotone_and_not_scored_as_h0m():
    declaration = dz.declarations()
    b4 = next(c for c in qa.cells(declaration) if c["name"] == "B4")
    path = qa.path_for(b4, 443.1, dict(start=459.1))
    assert np.array_equal(path(np.array([443.0, 444.0, 459.0, 460.0, 462.7])), [1, 0, 0, 1, 0])
    assert qa.members(b4) == {"H0", "H1"}
    q8 = next(c for c in qa.cells(declaration) if c["name"] == "Q8")
    assert q8["after"] == 1 and qa.members(q8) == {"H0m", "H0", "H1"}


def test_nectar_screen_critical_value_revalidates_on_mac(monkeypatch, binding):
    """5fcee58 LY-H2-CU/rho1 calibration Q1: Nectar 5.991464547107979, Mini 5.991464547107980."""
    cell = binding["grid"][0]
    rows = rows_for([cell])
    for row in rows:
        row["screen_crit"] = 5.991464547107979
    monkeypatch.setattr(ev, "count_crit", lambda n: 5.991464547107980)
    summary = qc.summarise(rows, cell, 1000, 20000, 0.0, .955)
    assert summary["complete"] and summary["cover_f_H0"] == 1000
    rows[0]["screen_lr"] = rows[0]["screen_crit"]
    with pytest.raises(qc.EvidenceError, match="screen flag contradicts"):
        qc.summarise(rows, cell, 1000, 20000, 0.0, .955)


@pytest.mark.parametrize("ulp_count,allowed", [(8, True), (-8, True), (9, False), (-9, False)])
def test_screen_critical_tolerance_is_bounded_to_roundoff(binding, ulp_count, allowed):
    cell = binding["grid"][0]
    rows = rows_for([cell])
    expected = ev.count_crit(0)
    rows[0]["screen_crit"] = expected + ulp_count * math.ulp(expected)
    if allowed:
        assert qc.summarise(rows, cell, 1000, 20000, 0.0, .955)["complete"]
    else:
        with pytest.raises(qc.EvidenceError, match="wrong screen critical"):
            qc.summarise(rows, cell, 1000, 20000, 0.0, .955)


@pytest.mark.parametrize("nonfinite", [math.inf, -math.inf, math.nan])
@pytest.mark.parametrize("field", ["stored", "expected"])
def test_screen_critical_values_must_both_be_finite(monkeypatch, binding, nonfinite, field):
    cell = binding["grid"][0]
    rows = rows_for([cell])
    if field == "stored":
        rows[0]["screen_crit"] = nonfinite
    else:
        monkeypatch.setattr(ev, "count_crit", lambda n: nonfinite)
    with pytest.raises(qc.EvidenceError, match="wrong screen critical"):
        qc.summarise(rows, cell, 1000, 20000, 0.0, .955)
