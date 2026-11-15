from pathlib import Path
import sys,json,re,hashlib
import pandas as pd
from sklearn.metrics import roc_auc_score
root=Path(sys.argv[1]);here=Path(__file__).parent
rules=json.loads((here/'rules.json').read_text());a=pd.read_csv(root/'answers.csv',converters={'answer':str,'found':str});s=pd.read_csv(root/'holdout_scores.csv');u=pd.read_csv(root/'probe_auc.csv');n=pd.read_csv(root/'shuffled.csv');m=json.loads((root/'manifest.json').read_text())
assert len(a)==42 and len(s)==288 and len(u)==24 and len(n)==60 and m['status']=='COMPLETED'
assert a.item_id.is_unique and a.text.is_unique
for r in a.itertuples():
 found=[w for w,aliases in rules['aliases'].items() if any(re.search(r'\b'+re.escape(v)+r'\b',r.answer,re.I) for v in aliases)]
 neg=bool(re.search(r'\b(not|neither|isn.t|aren.t)\b',r.answer,re.I))
 none=r.answer.strip().lower().strip('.! "\'') in rules['none_answers']
 correct=none if r.target=='none' else found==[r.target] and not neg
 assert correct==r.correct and '|'.join(found)==r.found
for r in u.itertuples():
 g=s[(s.pair==r.pair)&(s.position==r.position)&(s.layer==r.layer)]
 assert len(g)==12 and abs(roc_auc_score(g.label,g.score)-r.auc)<1e-12
clear=a[a.target!='none'];none=a[a.target=='none'];p=u[(u.position=='assistant_start')&(u.layer==27)];th=n.groupby('pair').auc.quantile(.95)
assert clear.correct.sum()==m['behavior_correct'] and none.correct.sum()==m['none_correct']
assert m['behavior_pass']==bool(clear.correct.sum()>=30 and clear.groupby('target').correct.sum().min()>=4)
assert m['none_pass']==bool(none.correct.sum()>=5)
assert m['probe_pass']==all(r.auc>=.8 and r.auc>th[r.pair] for r in p.itertuples())
for name,v in m['hashes'].items():assert hashlib.sha256((here/name).read_bytes()).hexdigest()==v
print('PASS: 42 responses, alias-aware scores, 288 individual probe scores, 24 AUCs, decision rules and frozen file hashes verified.')
