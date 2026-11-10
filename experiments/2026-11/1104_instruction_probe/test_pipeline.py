"""Synthetic offline features only: no model inference and no experimental data."""
from pathlib import Path
import json,shutil,tempfile,unittest
import numpy as np
import pandas as pd
from check import check_design
from analyze import analyze
from verify import verify
H=Path(__file__).resolve().parent
class PipelineTest(unittest.TestCase):
 def test_full_analysis_and_tamper_detection(self):
  train,design,cfg=check_design();concepts=[c for x,y in cfg['pairs'].items() for c in [x,y]];cols={c:i for i,c in enumerate(concepts)}
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)
   for name in ['training.csv','design.csv','config.json','sources.json','PLAN.md','FROZEN_SHA256.json']:shutil.copyfile(H/name,out/name)
   prompts=list(dict.fromkeys([r['prompt'] for r in train]+[r['prompt'] for r in design]));index=[dict(prompt_id=f'p{i:04d}',prompt=p,text='synthetic',rendered_prompt=p) for i,p in enumerate(prompts)]
   (out/'prompt_index.json').write_text(json.dumps(index));(out/'tokens.json').write_text(json.dumps([dict(prompt_id=r['prompt_id'],input_ids=[1,2,3],attention_mask=[1,1,1],context_end_char=0,context_end_offset=[0,1],positions={'context_end':0,'assistant_start':2}) for r in index]))
   by_prompt={r['prompt']:r for r in train+design};rng=np.random.default_rng(42);features=[]
   for p in prompts:
    r=by_prompt[p];v=rng.normal(0,.01,8)
    c=r.get('concept') or (r['pair'] if r['cue_kind']=='x' else r['comparison'] if r['cue_kind']=='y' else None)
    if c:v[cols[c]]+=1
    if r.get('condition') in ['mention_x','think_x','avoid_x']:v[cols[r['pair']]]+=.3
    if r.get('condition')=='think_y':v[cols[r['comparison']]]+=.3
    features.append(v)
   for l in cfg['layers']:
    for p in cfg['positions']:np.savez_compressed(out/f'features_L{l}_{p}.npz',features=np.array(features,dtype=np.float16))
   (out/'manifest.json').write_text(json.dumps(dict(status='FEATURES_COMPLETED',config=cfg,fixed_hashes=json.loads((H/'FROZEN_SHA256.json').read_text()),forward_count=361,generated_answers=0,hidden_size=8,actual_dtype='torch.float16',actual_depth=32,synthetic_test=True)))
   analyze(out);self.assertTrue(verify(out))
   scores=pd.read_csv(out/'scores.csv');neutral=scores[scores.condition=='neutral'];other=scores[scores.condition=='think_x']
   self.assertGreater(other[other.cue_kind=='empty'].z_score.mean(),neutral[neutral.cue_kind=='empty'].z_score.mean())
   scores.loc[0,'score']+=.5;scores.to_csv(out/'scores.csv',index=False)
   with self.assertRaises(AssertionError):verify(out)
if __name__=='__main__':unittest.main()
