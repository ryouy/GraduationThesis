"""CPU-only fit and analysis from saved FP16 features; no model calls."""
from pathlib import Path
import argparse,json,hashlib,csv,warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.exceptions import ConvergenceWarning
H=Path(__file__).resolve().parent

def analyze(out):
 import sklearn
 from threadpoolctl import threadpool_limits
 threadpool_limits(limits=4)
 cfg=json.loads((out/'config.json').read_text());m=json.loads((out/'manifest.json').read_text());assert m['status'] in ['FEATURES_COMPLETED','COMPLETED']
 train=pd.read_csv(out/'training.csv',keep_default_na=False);design=pd.read_csv(out/'design.csv',keep_default_na=False);index=json.loads((out/'prompt_index.json').read_text());lookup={r['prompt']:i for i,r in enumerate(index)}
 assert len(lookup)==len(index)==361
 train_indices=np.array([lookup[p] for p in train.prompt]);design_indices=np.array([lookup[p] for p in design.prompt])
 score_rows=[];auc_rows=[];null_rows=[];probe_rows=[];weights={}
 warnings.simplefilter('error',ConvergenceWarning)
 for layer in cfg['layers']:
  for position in cfg['positions']:
   F=np.load(out/f'features_L{layer}_{position}.npz')['features'].astype(np.float64)
   assert F.shape==(361,m['hidden_size']) and np.isfinite(F).all()
   for x,y in cfg['pairs'].items():
    training_mask=train.concept.isin([x,y]);X=F[train_indices[training_mask]];labels=(train.loc[training_mask,'concept']==x).astype(int).to_numpy();assert len(labels)==30 and labels.sum()==15
    scaler=StandardScaler().fit(X);Z=scaler.transform(X)
    def fit(target):return LogisticRegression(C=cfg['C'],solver='liblinear',max_iter=2000,random_state=cfg['seed']).fit(Z,target)
    clf=fit(labels);base=clf.decision_function(Z);center=float(base.mean());scale=float(base.std(ddof=1));assert scale>0
    probe_id=f'{x}__L{layer}__{position}'
    weights.update({probe_id+'__mean':scaler.mean_,probe_id+'__scale':scaler.scale_,probe_id+'__coef':clf.coef_[0],probe_id+'__intercept':clf.intercept_,probe_id+'__center':np.array([center]),probe_id+'__margin_scale':np.array([scale])})
    probe_rows.append(dict(probe_id=probe_id,pair=x,comparison=y,layer=layer,position=position,training_n=30,center=center,margin_scale=scale))
    mask=design.pair==x;D=design[mask];raw=clf.decision_function(scaler.transform(F[design_indices[mask]]))
    for r,score in zip(D.itertuples(),raw):score_rows.append(dict(item_id=r.item_id,pair=x,comparison=y,cue_id=r.cue_id,cue_kind=r.cue_kind,condition=r.condition,layer=layer,position=position,score=float(score),z_score=float((score-center)/scale)))
    for condition in cfg['conditions']:
     subset=D[(D.condition==condition)&D.cue_kind.isin(['x','y'])];ids=[lookup[p] for p in subset.prompt];target=(subset.cue_kind=='x').astype(int).to_numpy()
     pred=clf.decision_function(scaler.transform(F[ids]));auc_rows.append(dict(pair=x,condition=condition,layer=layer,position=position,n=12,auc=float(roc_auc_score(target,pred))))
     if condition=='neutral' and layer==cfg['primary_layer'] and position==cfg['primary_position']:
      rng=np.random.default_rng(cfg['seed']);T=scaler.transform(F[ids])
      for repeat in range(cfg['shuffle_repeats']):
       perm=rng.permutation(labels);pred_null=fit(perm).decision_function(T);null_rows.append(dict(pair=x,repeat=repeat,auc=float(roc_auc_score(target,pred_null))))
 scores=pd.DataFrame(score_rows);auc=pd.DataFrame(auc_rows);null=pd.DataFrame(null_rows);probes=pd.DataFrame(probe_rows)
 calibration=[]
 for x in cfg['pairs']:
  v=float(auc[(auc.pair==x)&(auc.condition=='neutral')&(auc.layer==cfg['primary_layer'])&(auc.position==cfg['primary_position'])].auc.iloc[0]);n=null[null.pair==x].auc;threshold=float(n.quantile(.95))
  calibration.append(dict(pair=x,primary_auc=v,shuffled_p95=threshold,shuffled_ge_true=int((n>=v).sum()),shuffles=len(n),calibration_ok=bool(v>=cfg['probe_auc_min'] and v>threshold)))
 cal=pd.DataFrame(calibration)
 effects=[]
 for (x,layer,pos),g in scores.groupby(['pair','layer','position']):
  neutral=g[g.condition=='neutral'].set_index('cue_id')
  for condition in cfg['conditions']:
   current=g[g.condition==condition].set_index('cue_id');empty=float(current.loc['empty','z_score']);neutral_empty=float(neutral.loc['empty','z_score'])
   for cue_id,r in current.iterrows():
    delta=float(r.z_score-neutral.loc[cue_id,'z_score']);gain=float(r.z_score-empty);neutral_gain=float(neutral.loc[cue_id,'z_score']-neutral_empty)
    effects.append(dict(item_id=r.item_id,pair=x,layer=layer,position=pos,cue_id=cue_id,cue_kind=r.cue_kind,condition=condition,score_delta_vs_neutral=delta,cue_gain_vs_empty=gain,interaction_vs_neutral=gain-neutral_gain))
 ef=pd.DataFrame(effects);means=scores.groupby(['pair','layer','position','cue_kind','condition'],as_index=False).agg(mean_z=('z_score','mean'),n=('z_score','size'))
 for name,frame in [('scores',scores),('probe_auc',auc),('shuffled',null),('probes',probes),('calibration',cal),('contrasts',ef),('means',means)]:frame.to_csv(out/(name+'.csv'),index=False)
 np.savez_compressed(out/'probe_weights.npz',**weights)
 primary=scores[(scores.layer==cfg['primary_layer'])&(scores.position==cfg['primary_position'])]
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,3,figsize=(13,4.5),layout='constrained');colors={'x':'#267c75','y':'#af7850','unrelated':'#8d98a4','empty':'#272c33'}
 for ax,(x,y) in zip(axes,cfg['pairs'].items()):
  for kind in ['x','y','unrelated','empty']:
   values=[]
   for i,c in enumerate(cfg['conditions']):
    group=primary[(primary.pair==x)&(primary.condition==c)&(primary.cue_kind==kind)];values.append(group.z_score.mean());ax.scatter(np.repeat(i,len(group)),group.z_score,color=colors[kind],s=13,alpha=.4)
   ax.plot(range(5),values,label=kind,color=colors[kind],marker='o',ms=3)
  flag=bool(cal[cal.pair==x].calibration_ok.iloc[0]);ax.set_title(f'{x} vs {y}\nProbe calibration: {"OK" if flag else "NOT OK"}');ax.set_xticks(range(5),['neutral','mention X','think X','avoid X','think Y'],rotation=35,ha='right');ax.spines[['top','right']].set_visible(False)
 axes[0].set_ylabel('Probe margin / training-score SD (not activation)');axes[-1].legend(frameon=False,fontsize=8)
 fig.suptitle('Primary: layer 31, assistant prefix; points are descriptions, not repeats',fontsize=11);fig.savefig(out/'comparison.png',dpi=160)
 lines=['# Instruction sensitivity diagnostic','', 'Exploratory. No answers were generated. Scores are relative X-vs-Y discriminability, not concept activation or suppression.','', '## Primary probe calibration','',cal.to_csv(index=False),'## Mean primary scores','',means[(means.layer==cfg['primary_layer'])&(means.position==cfg['primary_position'])].to_csv(index=False),'','If calibration is NOT OK, do not interpret instruction-score differences as concept changes. Empty is one fixed marker; no error bar or repeated-trial inference applies.','', '![Primary scores](comparison.png)']
 (out/'README.md').write_text('\n'.join(lines)+'\n')
 m.update(status='COMPLETED',sklearn=sklearn.__version__,training_descriptions=90,factorial_rows=285,unique_prompts=361,score_rows=len(scores),probes=len(probes),all_primary_calibrated=bool(cal.calibration_ok.all()),adoption_decision='NOT EVALUATED',generated_answers=0)
 (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(cal.to_string(index=False));print('Completed: 24 probes, 2280 score rows. Model adoption is not evaluated.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);analyze(ap.parse_args().out)
