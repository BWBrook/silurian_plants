"""Check current bindings on this host and compare regenerated empirical outputs."""
import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'models/f3'))
import qualify


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output', type=Path)
    ap.add_argument('--receipt', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    plan = json.loads((out / 'run-plan.json').read_text())
    completion = json.loads((out / 'completion.json').read_text())
    assert len(plan['combinations']) == 14
    checks = []
    for design, rho in plan['combinations']:
        delta, verdict, digest, binding = qualify.load_qualification(design, rho, out / 'qual')
        checks.append(dict(design=design, rho=rho, delta=delta, verdict=verdict,
                           receipt_sha256=digest, classes=binding['qualification_classes']))
    old = list(csv.DictReader(io.StringIO(subprocess.check_output(
        ['git', 'show', 'f08afb4:models/f3/out/m2_results.csv'], cwd=ROOT, text=True))))
    new = list(csv.DictReader((out / 'm2_results.csv').open()))
    key = lambda r: tuple(r[k] for k in ('design', 'variant', 'min_ref', 'rho'))
    oldmap, newmap = {key(r): r for r in old}, {key(r): r for r in new}
    assert len(oldmap) == len(old) and len(newmap) == len(new)
    assert oldmap.keys() == newmap.keys()
    fields = [k for k in old[0] if k not in ('qualification',)]
    changes = [dict(key=list(k), field=f, old=oldmap[k][f], new=r[f])
               for k, r in newmap.items() for f in fields if oldmap[k][f] != r[f]]
    primary = [r for r in new if r['primary'] == 'True']
    for r in new:
        if r['primary'] != 'True':
            assert r['qualification'] != 'pass'
        if r['design'] == 'QB-CO' and r['primary'] == 'True' and r['qualification'] == 'pass':
            assert r['qualification_H0c'] == 'unqualified-class-diagnostic'
    counts = Counter(r['qualification'] for r in new)
    result = dict(source_commit='31fab51', historical_commit='f08afb4',
                  total_seconds=completion['seconds'], current_host_binding_checks=checks,
                  empirical_rows=len(new), primary_rows=len(primary),
                  empirical_statuses=dict(counts), numerical_or_design_changes=changes,
                  primary_mz=[{k:r[k] for k in ('rho','qualification','fstar_H0_459.1','window_1')}
                              for r in primary if r['design']=='LY-MZ-CU'])
    args.receipt.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='current_host_binding_checks'}, indent=2))


if __name__ == '__main__':
    main()
