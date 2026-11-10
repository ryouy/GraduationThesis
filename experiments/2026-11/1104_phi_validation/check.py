from pathlib import Path
import csv,json,re,hashlib,sys
import grade
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def preflight():
 rows=list(csv.DictReader((HERE/'questions.csv').open()));assert len(rows)==72
 assert len({r['item_id'] for r in rows})==len({r['text'] for r in rows})==72
 from collections import Counter
 assert Counter(r['target'] for r in rows)==Counter({**{t:10 for t in grade.RULES['aliases']},'none':12})
 old=set()
 for p in ROOT.glob('1103*/**/*.csv'):
  try:
   for r in csv.DictReader(p.open()):
    if r.get('text'):old.add(re.sub(r'\s+',' ',r['text'].casefold()).strip())
  except (UnicodeError,csv.Error):pass
 for r in rows:
  assert re.sub(r'\s+',' ',r['text'].casefold()).strip() not in old,r['item_id']
  assert not any(re.search(r'\b'+re.escape(v)+r'\b',r['text'],re.I) for vs in grade.RULES['aliases'].values() for v in vs),r['item_id']
 cases=[('Banana','banana',True,True),('A banana.','banana',True,True),('Banana. It has yellow skin.','banana',True,False),('Not a banana','banana',False,False),('Banana. Actually apple.','banana',False,False),('Violin or viola','violin',False,False),('Fiddle','violin',True,True),('Keyboard','piano',False,False),('Plantain','banana',False,False),('None','none',True,True),('None. The context does not describe a specific animal.','none',True,False),('None. Banana.','none',False,False),('None. However, there is a fruit.','none',False,False),('There is no specific animal','none',False,False)]
 for answer,target,correct,fmt in cases:
  got=grade.grade(answer,target);assert (got['correct'],got['format_ok'])==(correct,fmt),(answer,got)
 print('Preflight PASS: 72 unique descriptions, no exact old-text matches or answer-name leakage; 14 scoring cases.')
def verify(out):
 import pandas as pd
 m=json.loads((out/'manifest.json').read_text());assert m['status']=='COMPLETED'
 assert m['revision']=='2fe192450127e6a83f7441aef6e3ca586c338b77'
 for name,h in m['hashes'].items():assert sha(HERE/name)==h,name
 assert sha(HERE/'questions.csv')==m['questions_sha256'] and sha(HERE/'rules.json')==m['rules_sha256']
 a=pd.read_csv(out/'answers.csv',keep_default_na=False);q=pd.read_csv(HERE/'questions.csv',keep_default_na=False).set_index('item_id');tokens=json.loads((out/'tokens.json').read_text());assert len(a)==len(tokens)==72 and a.item_id.is_unique
 tm={r['item_id']:r for r in tokens}
 for r in a.itertuples():
  for key in ['text','prompt','target']:assert getattr(r,key)==q.loc[r.item_id,key]
  g=grade.grade(r.answer,r.target)
  for key in ['correct','format_ok','prefix','found','conflict']:assert getattr(r,key)==g[key],(r.item_id,key)
  t=tm[r.item_id];assert len(t['output_ids'])==r.output_tokens and len(t['input_ids'])==len(t['attention_mask'])
 for key,value in grade.summarize(a).items():assert m[key]==value,key
 assert m['actual_dtype']=='torch.float16' and m['generation_config']['do_sample']==False and m['generation_config']['repetition_penalty']==1
 print('Result verification PASS:',json.dumps(grade.summarize(a)))
if __name__=='__main__':
 preflight()
 if len(sys.argv)>1:verify(Path(sys.argv[1]))
