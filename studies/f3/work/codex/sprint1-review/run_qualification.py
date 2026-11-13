# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.3.4", "scipy==1.16.3"]
# ///
"""Rerun declared primary M2 qualification and empirical read-outs after review."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'models/f3'))
import designs as dz
import m2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=62)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        if os.environ.get(key) != '1':
            raise SystemExit(f'{key}=1 must be set before starting Python')
    decl = dz.declarations()
    screened = m2.run_screen()
    m2.write(output / 'm2_screen.csv', screened)
    designs = {d['id']:d for d in decl['design']}
    combos = [(r['design'], float(r['rho'])) for r in screened
              if r['primary'] and r['passes'] and designs[r['design']].get('qualify', True)]
    assert len(combos) == len(set(combos))
    plan = dict(combinations=combos, workers=args.workers, output=str(output),
                interpretation='per-design marginal qualification; QB H0c excluded; not joint selection coverage')
    (output / 'run-plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    started = time.time()
    done = []
    qdir = output / 'qual'
    for phase in ('calibrate', 'accept'):
        for design, rho in combos:
            command = [sys.executable, str(ROOT/'models/f3/qualify.py'), '--design', design,
                       '--rho', str(rho), '--phase', phase, '--workers', str(args.workers), '--out-dir', str(qdir)]
            print(f'{phase} {design} rho={rho} starting', flush=True)
            with (output/f'{design}_rho{rho:g}_{phase}.log').open('w') as log:
                subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
            rec = json.loads((qdir/f'{design}_rho{rho:g}_{phase}.json').read_text())
            done.append(dict(design=design,rho=rho,phase=phase,complete=rec.get('complete'),result=rec.get('result'),delta=rec.get('delta')))
            print(json.dumps(done[-1]), flush=True)
            if phase == 'accept' and rec['result'] == 'borderline':
                command[command.index('--phase')+1] = 'stage2'
                with (output/f'{design}_rho{rho:g}_stage2.log').open('w') as log:
                    subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
                final=json.loads((qdir/f'{design}_rho{rho:g}_stage2.json').read_text())
                done.append(dict(design=design,rho=rho,phase='stage2',result=final['result']))
                print(json.dumps(done[-1]),flush=True)
    command=[sys.executable,str(ROOT/'models/f3/m2.py'),'results',str(args.workers),'--qual-dir',str(qdir),'--out-dir',str(output)]
    with (output/'empirical.log').open('w') as log:
        subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    (output/'completion.json').write_text(json.dumps(dict(seconds=time.time()-started,phases=done),indent=2)+'\n')
    print('All declared phases and empirical read-outs completed',flush=True)


if __name__ == '__main__':
    main()
