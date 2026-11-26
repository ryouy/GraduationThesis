from pathlib import Path
import sys,json,importlib.util,hashlib
import pandas as pd
p=Path(sys.argv[1]);root=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('fresh_grade',root/'experiments/2026-11/1103_fresh_check/run.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
a=pd.read_csv(p/'answers.csv',converters={'answer':str,'old_answer':str,'found':str});s=pd.read_csv(p/'summary.csv');t=json.loads((p/'tokens.json').read_text());m=json.loads((p/'manifest.json').read_text());checks=pd.read_csv(p/'input_comparison.csv');old=pd.read_csv(root/'experiments/2026-11/1103_fresh_check/results/answers.csv',keep_default_na=False).set_index('item_id')
assert len(checks)==42 and len(a)==252 and len(s)==6 and not a.duplicated(['mode','item_id']).any()
for name,h in m['hashes'].items():assert hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()==h
assert len(t)==len(a)
lookup={(x['mode'],x['item_id']):x for x in t}
for r in a.itertuples():
 assert r.prompt==old.loc[r.item_id,'prompt'] and r.old_answer==old.loc[r.item_id,'answer']
 assert g.grade(r.answer,r.target)['correct']==r.correct
 assert r.matches_old==(r.answer==r.old_answer)
 x=lookup[r.mode,r.item_id];assert len(x['input_ids'])==len(x['attention_mask']) and len(x['output_ids'])==r.tokens
for r in s.itertuples():
 z=a[a['mode']==r.mode];c=z[z.target!='none'];n=z[z.target=='none']
 assert len(z)==r.n and int(c.correct.sum())==r.correct and int(n.correct.sum())==r.none_correct
 assert int(c[c.target=='banana'].correct.sum())==r.banana_correct and int(z.matches_old.sum())==r.matches_old
print('PASS:',len(a),'raw responses, token lengths, fixed prompts/scoring, old-answer comparisons and summaries independently verified.')
