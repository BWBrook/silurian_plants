#!/usr/bin/env python3
"""Independently reconstruct sprint-1 stored counts at the immutable handoff."""
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = 'f08afb4'
OUT = Path(__file__).resolve().parent


def blob(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def main():
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'models/f3/out/qual'], cwd=ROOT, text=True).splitlines()
    results, hashes, failures = [], {}, []
    for path in sorted(p for p in paths if p.endswith('.json')):
        raw = blob(path)
        receipt = json.loads(raw)
        table_path = path[:-5] + '_reps.csv.gz'
        table = blob(table_path)
        hashes[path] = hashlib.sha256(raw).hexdigest()
        hashes[table_path] = hashlib.sha256(table).hexdigest()
        for code, digest in receipt['code'].items():
            assert hashlib.sha256(blob('models/f3/' + code)).hexdigest() == digest, code
        rows = list(csv.DictReader(io.StringIO(gzip.decompress(table).decode())))
        assert {r['cell'] for r in rows} == {s['cell'] for s in receipt['cells']}
        for s in receipt['cells']:
            rr = [r for r in rows if r['cell'] == s['cell']]
            ids = [int(r['rep']) for r in rr]
            assert ids == sorted(set(ids)) and len(ids) == s['passes']
            assert s['complete'] == (len(ids) >= receipt['target'])
            if s['kind'] == 'acceptance':
                assert len(ids) == receipt['target']
            assert ids[-1] + 1 == s['attempts'] if s['complete'] else s['attempts'] == receipt['cap']
            assert all(r['passed'] == 'True' for r in rr)
            assert sum(bool(r['error']) for r in rr) == s['errors']
            assert math.isclose(len(rr) / s['attempts'], s['pass_rate'])
            for key in sorted(k for k in s if k.startswith('cover_')):
                q = key[6:]
                hit = lambda r: not r['error'] and r.get('c_' + q, '') in ('True', '')
                claims = [r for r in rr if r['error'] or r.get('trivial') != 'True']
                cover = sum(hit(r) for r in rr)
                misses = sum(not hit(r) for r in claims)
                assert (cover, len(claims), misses) == (s[key], s['claims_' + q], s['claimmiss_' + q])
                margins = [math.inf if r['error'] else float(r.get('m_' + q) or '-inf') for r in rr]
                delta = max(0., sorted(margins)[math.ceil(.955 * len(rr)) - 1])
                assert delta == s['delta_' + q]
                missing_nontrivial = sum(not r.get('c_' + q) and r.get('trivial') != 'True' and not r['error'] for r in rr)
                results.append(dict(design=receipt['design'], rho=receipt['rho'], phase=receipt['phase'], cell=s['cell'], kind=s['kind'], quantity=q, passes=len(rr), attempts=s['attempts'], covers=cover, claims=len(claims), claim_misses=misses, missing_nontrivial=missing_nontrivial))
        if receipt['phase'] == 'calibrate':
            assert receipt['delta'] == max(v for s in receipt['cells'] if s['kind'] == 'acceptance' for k,v in s.items() if k.startswith('delta_'))
            assert receipt['complete']
        else:
            assert receipt['result'] == 'pass'
    with (OUT / 'historical_counts.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]), lineterminator='\n')
        w.writeheader(); w.writerows(results)
    acc = [r for r in results if r['phase'] == 'accept' and r['kind'] == 'acceptance']
    summary = dict(base_commit=BASE, receipts=len(hashes)//2, summary_quantities=len(results), acceptance_claim_evaluations=sum(r['claims'] for r in acc), acceptance_claim_misses=sum(r['claim_misses'] for r in acc), worst_observed_false_claim=max(1-r['covers']/r['passes'] for r in acc), missing_nontrivial_quantity_fields=sum(r['missing_nontrivial'] for r in results), status='stored counts reproduce; not current qualification or independent scientific acceptance', file_sha256=hashes)
    (OUT / 'historical_receipt.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k != 'file_sha256'}, indent=2))


if __name__ == '__main__':
    main()
