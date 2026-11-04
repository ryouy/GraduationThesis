from pathlib import Path
import csv,json,re,io
from collections import Counter,defaultdict
H=Path(__file__).resolve().parent
def check_design():
 train=list(csv.DictReader(io.StringIO((H/'training.csv').read_text())));design=list(csv.DictReader(io.StringIO((H/'design.csv').read_text())));cfg=json.loads((H/'config.json').read_text())
 assert len(cfg['pairs'])==20 and len(set(cfg['pairs'])|set(cfg['pairs'].values()))==40
 assert len(train)==cfg['training_n']==1200 and len(design)==cfg['design_n']==6100
 assert len({r['item_id'] for r in train})==len(train) and len({r['item_id'] for r in design})==len(design)
 assert Counter(r['concept'] for r in train)==Counter({c:30 for c in list(cfg['pairs'])+list(cfg['pairs'].values())})
 assert set(Counter(r['family'] for r in train).values())=={5}
 normal=lambda s:re.sub(r'\s+',' ',s.casefold()).strip()
 training={normal(r['text']) for r in train};assert len(training)==len(train)
 forbidden=list(cfg['pairs'])+list(cfg['pairs'].values())+['fiddle']
 for r in train+design:
  if 'pair' in r:words=[r['pair'],r['comparison']]
  else:
   words=next([x,y] for x,y in cfg['pairs'].items() if r['concept'] in [x,y])
  if 'violin' in words:words=words+['fiddle']
  assert not any(re.search(r'\b'+re.escape(c)+r's?\b',r['text'],re.I) for c in words),(r['item_id'],r['text'])
 for r in design:assert normal(r['text']) not in training
 groups=defaultdict(list)
 for r in design:
  assert r['comparison']==cfg['pairs'][r['pair']] and r['condition'] in cfg['conditions']
  groups[(r['pair'],r['cue_id'])].append(r)
 assert len(groups)==1220
 for rows in groups.values():assert len(rows)==5 and len({r['text'] for r in rows})==1 and {r['condition'] for r in rows}==set(cfg['conditions'])
 for x in cfg['pairs']:
  assert Counter(r['cue_kind'] for r in design if r['pair']==x)==Counter(x=100,y=100,unrelated=100,empty=5)
  for kind in ['x','y']:
   subset=[r for r in design if r['pair']==x and r['cue_kind']==kind and r['condition']=='neutral']
   assert len(subset)==20 and len({r['family'] for r in subset})==5
 prompts={r['prompt'] for r in train+design};assert len(prompts)==cfg['unique_n']
 print(f'PASS: 20 pairs, {len(train)} training rows, {len(design)} design rows, {len(prompts)} unique prompts; 5 eval families/concept, 4 wrappers/family.')
 return train,design,cfg
if __name__=='__main__':check_design()
