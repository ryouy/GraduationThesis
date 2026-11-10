"""Recalculate saved scores, AUCs, contrasts and family aggregates on CPU."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from analyze import family_auc
H=Path(__file__).resolve().parent
def verify(root):
 from threadpoolctl import threadpool_limits
 threadpool_limits(limits=4)
 root=Path(root);cfg=json.loads((root/'config.json').read_text());m=json.loads((root/'manifest.json').read_text())
 assert m['config']==cfg and m['status']=='COMPLETED' and m['actual_depth']==cfg['expected_depth'] and m['actual_dtype']=='torch.float16'
 assert m['generated_answers']==0 and m['forward_count']==m['unique_prompts']==cfg['unique_n']
 assert m['fixed_hashes']==json.loads((root/'FROZEN_SHA256.json').read_text())
 for name,digest in m['fixed_hashes'].items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,name
 for name in ['training.csv','design.csv','config.json','sources.json','PLAN.md']:assert hashlib.sha256((root/name).read_bytes()).hexdigest()==m['fixed_hashes'][name]
 index=json.loads((root/'prompt_index.json').read_text());tokens=json.loads((root/'tokens.json').read_text());assert len(index)==len(tokens)==cfg['unique_n']
 lookup={r['prompt']:i for i,r in enumerate(index)};assert len(lookup)==len(index)
 for r,t in zip(index,tokens):
  assert r['prompt_id']==t['prompt_id'] and len(t['input_ids'])==len(t['attention_mask'])
  assert t['positions']['assistant_start']==len(t['input_ids'])-1
  assert 0<=t['positions']['context_end']<len(t['input_ids'])
  lo,hi=t['context_end_offset'];assert lo<=t['context_end_char']<hi
 design=pd.read_csv(root/'design.csv').set_index('item_id');tr=pd.read_csv(root/'training.csv');scores=pd.read_csv(root/'scores.csv');w=np.load(root/'probe_weights.npz')
 expected={(i,r,l,p) for i in design.index for r in range(cfg['fit_repeats']) for l in cfg['layers'] for p in cfg['positions']}
 assert len(scores)==m['score_rows']==len(expected) and set(zip(scores.item_id,scores.repeat,scores.layer,scores.position))==expected
 for (layer,pos),blocks in scores.groupby(['layer','position']):
  F=np.load(root/f'features_L{layer}_{pos}.npz')['features'].astype(np.float64);assert F.shape==(cfg['unique_n'],m['hidden_size']) and np.isfinite(F).all()
  for (pair,repeat),g in blocks.groupby(['pair','repeat']):
   key=f'{pair}__R{repeat}__L{layer}__{pos}';ids=[lookup[design.loc[i,'prompt']] for i in g.item_id]
   raw=((F[ids]-w[key+'__mean'])/w[key+'__scale'])@w[key+'__coef']+w[key+'__intercept'][0]
   assert np.allclose(raw,g.score,atol=1e-8,rtol=1e-8)
   assert np.allclose((raw-w[key+'__center'][0])/w[key+'__margin_scale'][0],g.z_score,atol=1e-8,rtol=1e-8)
   y=cfg['pairs'][pair];t=tr[tr.concept.isin([pair,y])&(tr.family_index!=repeat)];ti=np.array([lookup[p] for p in t.prompt]);assert np.array_equal(ti,w[key+'__train_indices']) and len(ti)==50
   X=F[ti];assert np.allclose(X.mean(axis=0),w[key+'__mean'])
   sd=X.std(axis=0);sd[sd==0]=1;assert np.allclose(sd,w[key+'__scale'])
   base=((X-w[key+'__mean'])/w[key+'__scale'])@w[key+'__coef']+w[key+'__intercept'][0]
   assert np.isclose(base.mean(),w[key+'__center'][0]) and np.isclose(base.std(ddof=1),w[key+'__margin_scale'][0])
   fields=['pair','comparison','cue_id','family','cue_kind','condition'];actual=design.loc[g.item_id,fields].reset_index(drop=True);assert actual.equals(g[fields].reset_index(drop=True))
   # Refit a fixed subset of nulls, with whole families permuted together.
   if layer==cfg['primary_layer'] and pos==cfg['primary_position']:
    null=pd.read_csv(root/'shuffled.csv');n=null[(null.pair==pair)&(null.repeat==repeat)];assert len(n)==cfg['shuffle_repeats']
    for nr in n[n.shuffle.isin([0,1,2])].itertuples():
     positive=set(json.loads(nr.positive_families));assert len(positive)==5 and positive<=set(t.family)
     labels=t.family.isin(positive).astype(int).to_numpy();Z=(X-w[key+'__mean'])/w[key+'__scale']
     clf=LogisticRegression(C=cfg['C'],solver='liblinear',max_iter=2000,random_state=cfg['seed']).fit(Z,labels)
     ev=design[(design.pair==pair)&(design.condition=='neutral')&design.cue_kind.isin(['x','y'])].copy()
     ev['score']=clf.decision_function((F[[lookup[p] for p in ev.prompt]]-w[key+'__mean'])/w[key+'__scale'])
     assert np.isclose(family_auc(ev),nr.auc)
 auc=pd.read_csv(root/'probe_auc.csv');assert len(auc)==len(cfg['pairs'])*cfg['fit_repeats']*len(cfg['layers'])*len(cfg['positions'])*5
 for r in auc.itertuples():
  g=scores[(scores.pair==r.pair)&(scores.repeat==r.repeat)&(scores.layer==r.layer)&(scores.position==r.position)&(scores.condition==r.condition)&scores.cue_kind.isin(['x','y'])]
  assert len(g)==r.n_rows==40 and r.n_families==10 and np.isclose(family_auc(g),r.auc_families) and np.isclose(roc_auc_score((g.cue_kind=='x').astype(int),g.score),r.auc_rows)
 null=pd.read_csv(root/'shuffled.csv');assert len(null)==len(cfg['pairs'])*cfg['fit_repeats']*cfg['shuffle_repeats'] and not null[['pair','repeat','shuffle']].duplicated().any()
 cal=pd.read_csv(root/'calibration.csv');assert len(cal)==100
 for r in cal.itertuples():
  n=null[(null.pair==r.pair)&(null.repeat==r.repeat)].auc;a=auc[(auc.pair==r.pair)&(auc.repeat==r.repeat)&(auc.layer==cfg['primary_layer'])&(auc.position==cfg['primary_position'])&(auc.condition=='neutral')].auc_families.iloc[0]
  assert np.isclose(a,r.primary_auc) and np.isclose(n.quantile(.95),r.shuffled_p95) and r.shuffled_ge_true==int((n>=a).sum())
  assert r.calibration_ok==bool(a>=cfg['probe_auc_min'] and a>n.quantile(.95))
 summary=pd.read_csv(root/'pair_summary.csv');assert len(summary)==20
 for r in summary.itertuples():
  g=cal[cal.pair==r.pair];assert r.fits_passed==int(g.calibration_ok.sum()) and r.all_fits_pass==bool(g.calibration_ok.all()) and np.isclose(r.min_auc,g.primary_auc.min()) and np.isclose(r.max_auc,g.primary_auc.max())
 assert m['all_primary_calibrated']==bool(summary.all_fits_pass.all())
 contrasts=pd.read_csv(root/'contrasts.csv');assert len(contrasts)==len(scores)
 for (pair,repeat,layer,pos),g in scores.groupby(['pair','repeat','layer','position']):
  n=g[g.condition=='neutral'].set_index('cue_id');ne=n.loc['empty','z_score']
  for condition in cfg['conditions']:
   c=g[g.condition==condition].set_index('cue_id');ce=c.loc['empty','z_score']
   e=contrasts[(contrasts.pair==pair)&(contrasts.repeat==repeat)&(contrasts.layer==layer)&(contrasts.position==pos)&(contrasts.condition==condition)].set_index('cue_id').loc[c.index]
   assert np.allclose(e.score_delta_vs_neutral,c.z_score-n.loc[c.index,'z_score'])
   assert np.allclose(e.cue_gain_vs_empty,c.z_score-ce)
   assert np.allclose(e.interaction_vs_neutral,(c.z_score-ce)-(n.loc[c.index,'z_score']-ne))
 groups=['pair','repeat','layer','position','cue_kind','condition','family'];f=scores.groupby(groups,as_index=False).agg(mean_z=('z_score','mean'),n_wrappers=('z_score','size'))
 saved=pd.read_csv(root/'family_scores.csv');merged=f.merge(saved,on=groups,suffixes=('_a','_b'),validate='one_to_one');assert len(merged)==len(f)==len(saved) and np.allclose(merged.mean_z_a,merged.mean_z_b) and (merged.n_wrappers_a==merged.n_wrappers_b).all()
 groups=groups[:-1];means=f.groupby(groups,as_index=False).agg(mean_z=('mean_z','mean'),n_families=('family','size'));saved=pd.read_csv(root/'means.csv');merged=means.merge(saved,on=groups,suffixes=('_a','_b'),validate='one_to_one');assert len(merged)==len(means)==len(saved) and np.allclose(merged.mean_z_a,merged.mean_z_b) and (merged.n_families_a==merged.n_families_b).all()
 assert len(pd.read_csv(root/'probes.csv'))==m['probes']==200
 print(f'PASS: {len(index)} inputs, {m["probes"]} probes, {len(scores)} scores; AUCs, 300 null refits, contrasts and family aggregates verified.');return True
if __name__=='__main__':
 import sys
 verify(sys.argv[1])
