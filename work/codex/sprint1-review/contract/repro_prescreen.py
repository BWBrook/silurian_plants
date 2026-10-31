import json,sys
sys.path.insert(0,'/Users/bwbrook/papers/silurian_plants/models/f3')
import qualification_contract as qc

cell=dict(name='T',kind='acceptance',quantities=['f_H0'])
binding=dict(grid=[cell],protocol=dict(calibration_target=.955))
failed=dict(cell='T',rep=0,passed=False,error='RuntimeError: simulator failed')
passed=[dict(cell='T',rep=i+1,passed=True,error='',trivial=False,
             screen_lr=7.,c_f_H0=True,m_f_H0=-1.) for i in range(1000)]
print(json.dumps(qc.assessment(binding,'accept',[failed]+passed,1000,20000,0.),indent=2))
