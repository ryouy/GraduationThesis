from pathlib import Path
import csv,json,re,hashlib,io
from collections import Counter,defaultdict
H=Path(__file__).resolve().parent

def check_design():
 train=list(csv.DictReader(io.StringIO((H/'training.csv').read_text())));design=list(csv.DictReader(io.StringIO((H/'design.csv').read_text())));cfg=json.loads((H/'config.json').read_text())
 assert len(train)==90 and len({r['text'] for r in train})==90 and len({r['item_id'] for r in train})==90
 assert Counter(r['concept'] for r in train)==Counter({c:15 for x,y in cfg['pairs'].items() for c in [x,y]})
 assert len(design)==285 and len({r['item_id'] for r in design})==285
 for p,digest in json.loads((H/'sources.json').read_text()).items():assert hashlib.sha256((H.parent/p).read_bytes()).hexdigest()==digest
 normalize=lambda s:re.sub(r'\s+',' ',s.casefold()).strip()
 training={normalize(r['text']) for r in train}
 forbidden=[c for x,y in cfg['pairs'].items() for c in [x,y]]+['fiddle']
 for r in train:
  assert r['prompt'].startswith('Instruction: Read the context carefully.')
  assert not any(re.search(r'\b'+w+r's?\b',r['text'],re.I) for w in forbidden),r['item_id']
 groups=defaultdict(list)
 for r in design:
  assert normalize(r['text']) not in training
  assert r['pair'] in cfg['pairs'] and r['comparison']==cfg['pairs'][r['pair']]
  assert r['condition'] in cfg['conditions']
  assert not any(re.search(r'\b'+w+r's?\b',r['text'],re.I) for w in forbidden)
  groups[(r['pair'],r['cue_id'])].append(r)
 assert len(groups)==57
 for rows in groups.values():
  assert len(rows)==5 and len({r['text'] for r in rows})==1 and {r['condition'] for r in rows}==set(cfg['conditions'])
 for x in cfg['pairs']:
  assert Counter(r['cue_kind'] for r in design if r['pair']==x)==Counter(x=30,y=30,unrelated=30,empty=5)
 prompts=list(dict.fromkeys([r['prompt'] for r in train]+[r['prompt'] for r in design]))
 assert len(prompts)==361
 print('PASS: 90 training texts; 285 factorial rows; 361 unique prompts; exact split separation; no target names in descriptions.')
 return train,design,cfg
if __name__=='__main__':check_design()
