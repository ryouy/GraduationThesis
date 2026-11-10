from pathlib import Path
import csv,json,hashlib
import pandas as pd
H=Path(__file__).resolve().parent;R=H.parent
PAIRS={'banana':'apple','elephant':'giraffe','piano':'violin'}
INSTRUCTIONS={'neutral':'Read the context carefully.','mention_x':'The topic word is {x}.','think_x':'Think about {x}.','avoid_x':'Do not think about {x}.','think_y':'Think about {y}.'}
READOUT='Give one short response about the context.'
def prompt(instruction,text):return f'Instruction: {instruction}\n\nContext:\n{text}\n\n{READOUT}'
def write(name,rows):
 with (H/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 old=pd.read_csv(R/'1103_model_check/results/1.5B/training_design.csv',keep_default_na=False)
 old=old[old.task=='naming'];train=[]
 for x,y in PAIRS.items():
  subset=old[old.concept==x].drop_duplicates('group')
  for r in subset.itertuples():
   if r.group.split('_')[1]=='0':continue # Exclude standalone target names.
   text=r.prompt.split('Context:\n',1)[1].split('\n\nName the specific',1)[0]
   word=x if r.label==1 else y
   train.append(dict(item_id=f'train_{word}_{r.group.split("_")[1]}',concept=word,text=text,prompt=prompt(INSTRUCTIONS['neutral'],text)))
 write('training.csv',train)
 held=json.loads((R/'1103_fresh_check/items.json').read_text())
 none=[text for k,vs in held.items() if k.startswith('none_') for text in vs]
 assert len(none)==6
 design=[]
 for x,y in PAIRS.items():
  cues=[('x',f'{x}_{i}',s) for i,s in enumerate(held[x])]+[('y',f'{y}_{i}',s) for i,s in enumerate(held[y])]+[('unrelated',f'unrelated_{i}',s) for i,s in enumerate(none)]+[('empty','empty','[No descriptive context.]')]
  for kind,cue_id,text in cues:
   for condition,template in INSTRUCTIONS.items():
    instruction=template.format(x=x,y=y)
    design.append(dict(item_id=f'{x}__{cue_id}__{condition}',pair=x,comparison=y,cue_kind=kind,cue_id=cue_id,condition=condition,text=text,prompt=prompt(instruction,text)))
 write('design.csv',design)
 (H/'config.json').write_text(json.dumps(dict(model='microsoft/Phi-3.5-mini-instruct',revision='2fe192450127e6a83f7441aef6e3ca586c338b77',system='You are a helpful assistant.',expected_depth=32,layers=[16,24,31,32],positions=['context_end','assistant_start'],primary_layer=31,primary_position='assistant_start',pairs=PAIRS,conditions=list(INSTRUCTIONS),C=0.1,shuffle_repeats=100,seed=42,probe_auc_min=0.8,interpretation='Calibration flags only; no model-adoption gate or causal claim.'),indent=2)+'\n')
 sources=['1103_model_check/results/1.5B/training_design.csv','1103_fresh_check/items.json']
 (H/'sources.json').write_text(json.dumps({p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in sources},indent=2)+'\n')
if __name__=='__main__':main()
