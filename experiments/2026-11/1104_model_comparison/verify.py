from pathlib import Path
import sys,json,re,hashlib
import pandas as pd
root=Path(sys.argv[1]);repo=Path(__file__).resolve().parents[1]
questions=pd.read_csv(repo/'1103_fresh_check/results/answers.csv',keep_default_na=False).set_index('item_id')
rules=json.loads((repo/'1103_fresh_check/rules.json').read_text());models=json.loads((root/'resolved_models.json').read_text());summary=[]
for e in models:
 p=root/e['key'];m=json.loads((p/'manifest.json').read_text());assert m['model']==e['model'] and m['revision']==e['revision']
 for name,h in m['hashes'].items():assert hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()==h
 if m['status']!='COMPLETED':print(e['key'],'ERROR (not scored)');continue
 a=pd.read_csv(p/'answers.csv',converters={'answer':str,'found':str});tokens=json.loads((p/'tokens.json').read_text());assert len(a)==len(tokens)==42 and a.item_id.is_unique
 tokenmap={r['item_id']:r for r in tokens}
 for r in a.itertuples():
  assert r.prompt==questions.loc[r.item_id,'prompt'] and r.text==questions.loc[r.item_id,'text'] and r.target==questions.loc[r.item_id,'target']
  found=[w for w,vs in rules['aliases'].items() if any(re.search(r'\b'+re.escape(v)+r'\b',r.answer,re.I) for v in vs)]
  neg=bool(re.search(r'\b(not|neither|isn.t|aren.t)\b',r.answer,re.I));none=r.answer.strip().lower().strip('.! "\'') in rules['none_answers']
  assert r.correct==(none if r.target=='none' else found==[r.target] and not neg)
  t=tokenmap[r.item_id];assert len(t['output_ids'])==r.output_tokens and len(t['input_ids'])==len(t['attention_mask'])
 c=a[a.target!='none'];n=a[a.target=='none'];low=int(c.groupby('target').correct.sum().min())
 assert int(c.correct.sum())==m['correct'] and int(n.correct.sum())==m['none_correct'] and low==m['min_per_concept']
 assert m['all_pass']==bool(c.correct.sum()>=30 and low>=4 and n.correct.sum()>=5)
 assert m['generation_config']['do_sample']==False and m['generation_config']['repetition_penalty']==1 and m['actual_dtype']=='torch.float16'
 summary.append(dict(model=e['label'],correct=m['correct'],none_correct=m['none_correct'],all_pass=m['all_pass']))
 print(e['key'],'PASS: 42 unchanged prompts, raw answer scoring, token lengths and frozen hashes verified.')
assert len(summary)>=3,'Fewer than 3 models completed.'
print(pd.DataFrame(summary).to_string(index=False))
