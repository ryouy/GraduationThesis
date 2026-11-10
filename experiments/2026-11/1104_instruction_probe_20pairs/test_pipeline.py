"""Artificial features only: these are software tests, never empirical results."""
from pathlib import Path
import tempfile,json,shutil,unittest
import numpy as np
from check import check_design,H
from analyze import analyze
from verify import verify
class PipelineTest(unittest.TestCase):
 def test_full_analysis_and_tamper_detection(self):
  train,design,cfg=check_design()
  with tempfile.TemporaryDirectory(prefix='synthetic_probe20_') as temp:
   out=Path(temp)
   for name in ['config.json','training.csv','design.csv','sources.json','PLAN.md','FROZEN_SHA256.json']:shutil.copyfile(H/name,out/name)
   rows={r['prompt']:r for r in train+design};prompts=list(dict.fromkeys(r['prompt'] for r in train+design));rng=np.random.default_rng(391);width=12
   vectors=[];index=[];tokens=[]
   for i,p in enumerate(prompts):
    r=rows[p];v=rng.normal(size=width)
    if 'concept' in r:
     v[0]=2 if r['concept'] in cfg['pairs'] else -2
    else:
     v[0]={'x':2,'y':-2,'unrelated':0,'empty':0}[r['cue_kind']]
     v[1]={'neutral':0,'mention_x':1,'think_x':1,'avoid_x':-.2,'think_y':-1}[r['condition']]
    vectors.append(v);pid=f'p{i:04d}';index.append(dict(prompt_id=pid,prompt=p))
    tokens.append(dict(prompt_id=pid,input_ids=[1,2,3],attention_mask=[1,1,1],context_end_char=0,context_end_offset=[0,1],positions=dict(context_end=1,assistant_start=2)))
   (out/'prompt_index.json').write_text(json.dumps(index));(out/'tokens.json').write_text(json.dumps(tokens))
   for pos in cfg['positions']:np.savez_compressed(out/f'features_L31_{pos}.npz',features=np.array(vectors,dtype=np.float16))
   m=dict(status='FEATURES_COMPLETED',config=cfg,fixed_hashes=json.loads((H/'FROZEN_SHA256.json').read_text()),forward_count=len(index),generated_answers=0,hidden_size=width,actual_depth=32,actual_dtype='torch.float16',synthetic_test=True)
   (out/'manifest.json').write_text(json.dumps(m));analyze(out);self.assertTrue(verify(out))
   import pandas as pd
   s=pd.read_csv(out/'scores.csv');s.loc[0,'score']+=1;s.to_csv(out/'scores.csv',index=False)
   with self.assertRaises(AssertionError):verify(out)
if __name__=='__main__':unittest.main()
