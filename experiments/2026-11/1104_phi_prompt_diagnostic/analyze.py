from pathlib import Path
import sys,json,hashlib,re
import pandas as pd
import grade
HERE=Path(__file__).resolve().parent
CONDITIONS=['A_original','B_best_match']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root):
 out=root/'phi3_5mini';m=json.loads((out/'manifest.json').read_text())
 assert m['status']=='COMPLETED' and m['revision']=='2fe192450127e6a83f7441aef6e3ca586c338b77'
 for name,h in m['hashes'].items():assert sha(HERE/name)==h,name
 for name,h in json.loads((HERE/'FROZEN_SHA256.json').read_text()).items():assert sha(HERE/name)==h,name
 a=pd.read_csv(out/'answers.csv',keep_default_na=False);q=pd.read_csv(HERE/'questions.csv',keep_default_na=False).set_index('item_id')
 tokens=json.loads((out/'tokens.json').read_text());tm={t['item_id']:t for t in tokens}
 assert len(a)==len(q)==len(tokens)==len(tm)==144 and a.item_id.is_unique
 for r in a.itertuples():
  for field in ['source_item_id','condition','target','text','prompt']:assert getattr(r,field)==q.loc[r.item_id,field]
  g=grade.grade(r.answer,r.target)
  for field in ['correct','format_ok','prefix','found','conflict']:assert getattr(r,field)==g[field],(r.item_id,field)
  t=tm[r.item_id];assert len(t['output_ids'])==r.output_tokens and len(t['input_ids'])==len(t['attention_mask'])
 for key,value in grade.summarize(a).items():assert m[key]==value,key
 assert m['actual_dtype']=='torch.float16' and m['generation_config']['repetition_penalty']==1 and not m['generation_config']['do_sample']
 return a

def analyze(root):
 a=verify(root);summaries=[]
 for condition in CONDITIONS:
  rows=a[a.condition==condition];clear=rows[rows.target!='none'];none=rows[rows.target=='none'];assert len(clear)==60 and len(none)==12
  summaries.append(dict(condition=condition,naming_correct=int(clear.correct.sum()),naming_n=60,none_correct=int(none.correct.sum()),none_n=12,format_correct=int(rows.format_ok.sum()),truncations=int(rows.truncated.sum()),clear_none_answers=int(clear.answer.str.match(r'(?i)^\s*none\b').sum())))
 pd.DataFrame(summaries).to_csv(root/'condition_summary.csv',index=False)
 a.groupby(['condition','target']).correct.agg(['sum','count']).to_csv(root/'per_concept.csv')
 original=a[a.condition=='A_original'].set_index('source_item_id');best=a[a.condition=='B_best_match'].set_index('source_item_id');assert set(original.index)==set(best.index)
 paired=original[['target','text']].copy()
 for name,frame in [('A',original),('B',best)]:
  for col in ['answer','correct','format_ok','truncated']:paired[name+'_'+col]=frame[col]
 paired['transition']=[('correct' if a else 'wrong')+' -> '+('correct' if b else 'wrong') for a,b in zip(paired.A_correct,paired.B_correct)]
 paired.to_csv(root/'paired_answers.csv')
 counts={}
 for subset,frame in [('naming',paired[paired.target!='none']),('none',paired[paired.target=='none'])]:counts[subset]={s:int((frame.transition==s).sum()) for s in ['correct -> correct','wrong -> correct','correct -> wrong','wrong -> wrong']}
 (root/'paired_transitions.json').write_text(json.dumps(counts,indent=2)+'\n')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(9,4),layout='constrained')
 for ax,col,n,title in [(axes[0],'naming_correct',60,'Description naming /60'),(axes[1],'none_correct',12,'Unrelated controls /12')]:
  values=[s[col] for s in summaries];bars=ax.bar(['A: original','B: best match'],values,color=['#708396','#397e78']);ax.bar_label(bars,labels=[f'{v}/{n}' for v in values],padding=3);ax.set_ylim(0,n*1.2);ax.set_title(title);ax.spines[['top','right']].set_visible(False)
 fig.savefig(root/'comparison.png',dpi=170)
 text='# Phi prompt diagnostic: exploratory results\n\nRaw answers require review; no model adoption decision is automatic.\n\n'+pd.DataFrame(summaries).to_csv(index=False)+'\nPaired transitions:\n```json\n'+json.dumps(counts,indent=2)+'\n```\n'
 (root/'README.md').write_text(text)
 # File checksums help verify the later upload without exposing any credentials.
 paths=['resolved_models.json','phi3_5mini/manifest.json','phi3_5mini/answers.csv','phi3_5mini/tokens.json','phi3_5mini/correct_per_concept.csv','condition_summary.csv','per_concept.csv','paired_answers.csv','paired_transitions.json','comparison.png','README.md']
 (root/'RESULT_SHA256.json').write_text(json.dumps({p:sha(root/p) for p in paths},indent=2)+'\n')
 print(pd.DataFrame(summaries).to_string(index=False));print(json.dumps(counts));print('Verification passed. Raw-answer review remains required.')
if __name__=='__main__':analyze(Path(sys.argv[1]))
