from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
H=Path(__file__).resolve().parent

def verify(root):
 root=Path(root);m=json.loads((root/'manifest.json').read_text());cfg=json.loads((root/'config.json').read_text())
 assert m['config']==cfg and m['actual_depth']==cfg['expected_depth'] and m['actual_dtype']=='torch.float16'
 assert json.loads((root/'FROZEN_SHA256.json').read_text())==m['fixed_hashes']
 assert m['status']=='COMPLETED' and m['forward_count']==m['unique_prompts']==361
 assert m['generated_answers']==0 and m['factorial_rows']==285 and m['probes']==24
 for name,digest in m['fixed_hashes'].items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,name
 for name in ['training.csv','design.csv','config.json','sources.json','PLAN.md']:
  assert hashlib.sha256((root/name).read_bytes()).hexdigest()==m['fixed_hashes'][name],name
 index=json.loads((root/'prompt_index.json').read_text());tokens=json.loads((root/'tokens.json').read_text());assert len(index)==len(tokens)==361
 lookup={r['prompt']:i for i,r in enumerate(index)};assert len(lookup)==361
 for r,t in zip(index,tokens):
  assert r['prompt_id']==t['prompt_id'] and len(t['input_ids'])==len(t['attention_mask'])
  assert t['positions']['assistant_start']==len(t['input_ids'])-1
  assert 0<=t['positions']['context_end']<len(t['input_ids'])
  lo,hi=t['context_end_offset'];assert lo<=t['context_end_char']<hi
 design=pd.read_csv(root/'design.csv',keep_default_na=False).set_index('item_id');training=pd.read_csv(root/'training.csv',keep_default_na=False)
 scores=pd.read_csv(root/'scores.csv');assert len(scores)==2280 and not scores[['item_id','layer','position']].duplicated().any()
 expected={(i,l,p) for i in design.index for l in cfg['layers'] for p in cfg['positions']};assert set(zip(scores.item_id,scores.layer,scores.position))==expected
 weights=np.load(root/'probe_weights.npz');probes=pd.read_csv(root/'probes.csv')
 for layer in cfg['layers']:
  for position in cfg['positions']:
   F=np.load(root/f'features_L{layer}_{position}.npz')['features'].astype(np.float64);assert F.shape==(361,m['hidden_size']) and np.isfinite(F).all()
   for x,y in cfg['pairs'].items():
    key=f'{x}__L{layer}__{position}';g=scores[(scores.pair==x)&(scores.layer==layer)&(scores.position==position)]
    ids=[lookup[design.loc[i,'prompt']] for i in g.item_id]
    raw=((F[ids]-weights[key+'__mean'])/weights[key+'__scale'])@weights[key+'__coef']+weights[key+'__intercept'][0]
    assert np.allclose(raw,g.score,atol=1e-8,rtol=1e-8)
    assert np.allclose((raw-weights[key+'__center'][0])/weights[key+'__margin_scale'][0],g.z_score,atol=1e-8,rtol=1e-8)
    for r in g.itertuples():
     row=design.loc[r.item_id]
     for field in ['pair','comparison','cue_id','cue_kind','condition']:assert getattr(r,field)==row[field]
    tr=training[training.concept.isin([x,y])];tr_ids=[lookup[p] for p in tr.prompt]
    train_raw=((F[tr_ids]-weights[key+'__mean'])/weights[key+'__scale'])@weights[key+'__coef']+weights[key+'__intercept'][0]
    assert np.isclose(train_raw.mean(),weights[key+'__center'][0]) and np.isclose(train_raw.std(ddof=1),weights[key+'__margin_scale'][0])
 auc=pd.read_csv(root/'probe_auc.csv');assert len(auc)==120
 for r in auc.itertuples():
  g=scores[(scores.pair==r.pair)&(scores.layer==r.layer)&(scores.position==r.position)&(scores.condition==r.condition)&scores.cue_kind.isin(['x','y'])]
  assert len(g)==r.n==12 and np.isclose(roc_auc_score((g.cue_kind=='x').astype(int),g.score),r.auc)
 null=pd.read_csv(root/'shuffled.csv');assert len(null)==300 and not null[['pair','repeat']].duplicated().any()
 calibration=pd.read_csv(root/'calibration.csv');assert len(calibration)==3
 for r in calibration.itertuples():
  n=null[null.pair==r.pair].auc;true=auc[(auc.pair==r.pair)&(auc.condition=='neutral')&(auc.layer==cfg['primary_layer'])&(auc.position==cfg['primary_position'])].auc.iloc[0]
  assert len(n)==100 and np.isclose(n.quantile(.95),r.shuffled_p95) and np.isclose(true,r.primary_auc)
  assert r.calibration_ok==bool(true>=cfg['probe_auc_min'] and true>n.quantile(.95))
 assert m['all_primary_calibrated']==bool(calibration.calibration_ok.all())
 contrasts=pd.read_csv(root/'contrasts.csv');assert len(contrasts)==2280
 for (pair,layer,pos),g in scores.groupby(['pair','layer','position']):
  ng=g[g.condition=='neutral'].set_index('cue_id');ne=ng.loc['empty','z_score']
  for condition in cfg['conditions']:
   cg=g[g.condition==condition].set_index('cue_id');ce=cg.loc['empty','z_score']
   e=contrasts[(contrasts.pair==pair)&(contrasts.layer==layer)&(contrasts.position==pos)&(contrasts.condition==condition)].set_index('cue_id').loc[cg.index]
   delta=cg.z_score-ng.loc[cg.index,'z_score'];gain=cg.z_score-ce
   assert np.allclose(e.score_delta_vs_neutral,delta,atol=1e-8)
   assert np.allclose(e.cue_gain_vs_empty,gain,atol=1e-8)
   assert np.allclose(e.interaction_vs_neutral,gain-(ng.loc[cg.index,'z_score']-ne),atol=1e-8)
 means=pd.read_csv(root/'means.csv');assert len(means)==480
 # Recompute every aggregate rather than trusting a plot or summary.
 actual=scores.groupby(['pair','layer','position','cue_kind','condition'],as_index=False).agg(mean_z=('z_score','mean'),n=('z_score','size'))
 merged=actual.merge(means,on=['pair','layer','position','cue_kind','condition'],suffixes=('_a','_b'),validate='one_to_one')
 assert len(merged)==480 and np.allclose(merged.mean_z_a,merged.mean_z_b,atol=1e-8) and (merged.n_a==merged.n_b).all()
 print('Verification PASS: 361 inputs, 24 probes, 2280 scores/contrasts, 120 AUCs, 300 label shuffles and 480 aggregates.')
 return True
if __name__=='__main__':
 import sys
 verify(Path(sys.argv[1]))
