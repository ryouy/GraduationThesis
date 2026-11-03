from pathlib import Path
import sys,json
import pandas as pd
from sklearn.metrics import roc_auc_score
p=Path(sys.argv[1])
for size in ['0.5B','1.5B']:
 d=p/size;a=pd.read_csv(d/'answers.csv');s=pd.read_csv(d/'holdout_scores.csv');u=pd.read_csv(d/'probe_auc.csv');n=pd.read_csv(d/'shuffled.csv');m=json.loads((d/'manifest.json').read_text())
 assert m['status']=='COMPLETED' and len(a)==144 and len(s)==576 and len(u)==48 and len(n)==120
 assert not a.duplicated(['concept','task','split','text']).any()
 for r in u.itertuples():
  g=s[(s.concept==r.concept)&(s.task==r.task)&(s.position==r.position)&(s.layer==r.layer)]
  assert len(g)==12 and abs(roc_auc_score(g.label,g.score)-r.auc)<1e-12
 assert not a[a.split=='cue'].correct.notna().any()
 print(size,'PASS: 144 responses, 576 individual scores, 48 AUCs, 120 shuffle controls')
