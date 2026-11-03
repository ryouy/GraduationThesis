from pathlib import Path
import sys,json,re
import pandas as pd
from sklearn.metrics import roc_auc_score
p=Path(sys.argv[1])
for size in ['0.5B','1.5B']:
 d=p/size;a=pd.read_csv(d/'answers.csv',converters={'answer':str});s=pd.read_csv(d/'holdout_scores.csv');u=pd.read_csv(d/'probe_auc.csv');n=pd.read_csv(d/'shuffled.csv');m=json.loads((d/'manifest.json').read_text())
 assert m['status']=='COMPLETED' and len(a)==144 and len(s)==576 and len(u)==48 and len(n)==120
 assert not a.duplicated(['concept','task','split','text']).any()
 for r in u.itertuples():
  g=s[(s.concept==r.concept)&(s.task==r.task)&(s.position==r.position)&(s.layer==r.layer)]
  assert len(g)==12 and abs(roc_auc_score(g.label,g.score)-r.auc)<1e-12
 for r in a[a.split=='clear'].itertuples():
  found=[w for w in ['banana','elephant','piano','apple','giraffe','violin'] if re.search(r'\b'+w+r's?\b',r.answer,re.I)]
  assert bool(r.correct)==(found==[r.target])
 assert not a[a.split=='cue'].correct.notna().any()
 summary=pd.read_csv(d/'summary.csv')
 for r in summary.itertuples():
  g=a[(a.split=='clear')&(a.task==r.task)]
  assert len(g)==r.n==36 and int(g.correct.sum())==r.correct
  low=int(g.groupby('target').correct.sum().min())
  assert low==r.min_correct_per_concept
  assert bool(r.behavior_pass)==bool(r.correct>=30 and low>=4)
  pu=u[(u.task==r.task)&u.primary]
  th=n[n.task==r.task].groupby('concept').auc.quantile(.95)
  passed=all(z.auc>=.8 and z.auc>th[z.concept] for z in pu.itertuples())
  assert bool(r.probe_pass)==passed and abs(r.min_primary_auc-pu.auc.min())<1e-12
 print(size,'PASS: 144 responses, 576 individual scores, 48 AUCs, 120 shuffle controls')
