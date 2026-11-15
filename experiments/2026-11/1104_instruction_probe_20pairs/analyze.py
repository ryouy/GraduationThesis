"""CPU analysis. Five overlapping fits are sensitivity checks, not replications."""
from pathlib import Path
import argparse,json,warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.exceptions import ConvergenceWarning
def fit_model(X,y,cfg):
 scaler=StandardScaler().fit(X)
 clf=LogisticRegression(C=cfg['C'],solver='liblinear',max_iter=2000,random_state=cfg['seed']).fit(scaler.transform(X),y)
 return scaler,clf
def family_auc(frame,column='score'):
 g=frame.groupby(['family','cue_kind'],as_index=False)[column].mean()
 return float(roc_auc_score((g.cue_kind=='x').astype(int),g[column]))
def analyze(out):
 import sklearn
 from threadpoolctl import threadpool_limits
 threadpool_limits(limits=4);warnings.simplefilter('error',ConvergenceWarning)
 cfg=json.loads((out/'config.json').read_text());m=json.loads((out/'manifest.json').read_text());assert m['status'] in ['FEATURES_COMPLETED','COMPLETED']
 train=pd.read_csv(out/'training.csv');design=pd.read_csv(out/'design.csv');index=json.loads((out/'prompt_index.json').read_text());lookup={r['prompt']:i for i,r in enumerate(index)}
 assert len(lookup)==cfg['unique_n'];ti=np.array([lookup[p] for p in train.prompt]);di=np.array([lookup[p] for p in design.prompt])
 scores=[];aucs=[];nulls=[];probes=[];weights={}
 for layer in cfg['layers']:
  for pos in cfg['positions']:
   F=np.load(out/f'features_L{layer}_{pos}.npz')['features'].astype(np.float64);assert F.shape==(cfg['unique_n'],m['hidden_size']) and np.isfinite(F).all()
   for x,y in cfg['pairs'].items():
    D=design[design.pair==x];df=F[di[design.pair==x]]
    for repeat in range(cfg['fit_repeats']):
     # Leave out one complete five-wrapper family from EACH class.
     mask=train.concept.isin([x,y]) & (train.family_index!=repeat)
     tr=train[mask];X=F[ti[mask]];labels=(tr.concept==x).astype(int).to_numpy()
     assert len(labels)==50 and labels.sum()==25
     scaler,clf=fit_model(X,labels,cfg);Z=scaler.transform(X);raw=clf.decision_function(scaler.transform(df))
     base=clf.decision_function(Z);center=base.mean();scale=base.std(ddof=1);assert scale>0
     key=f'{x}__R{repeat}__L{layer}__{pos}'
     for name,value in dict(mean=scaler.mean_,scale=scaler.scale_,coef=clf.coef_[0],intercept=clf.intercept_,center=np.array([center]),margin_scale=np.array([scale]),train_indices=ti[mask]).items():weights[key+'__'+name]=value
     probes.append(dict(probe_id=key,pair=x,repeat=repeat,omitted_family=repeat,layer=layer,position=pos,training_n=len(tr)))
     current=[]
     for r,score in zip(D.itertuples(),raw):
      current.append(dict(item_id=r.item_id,pair=x,comparison=y,repeat=repeat,layer=layer,position=pos,cue_id=r.cue_id,family=r.family,cue_kind=r.cue_kind,condition=r.condition,score=score,z_score=(score-center)/scale))
     scores.extend(current);cur=pd.DataFrame(current)
     for condition in cfg['conditions']:
      g=cur[(cur.condition==condition)&cur.cue_kind.isin(['x','y'])]
      aucs.append(dict(pair=x,repeat=repeat,layer=layer,position=pos,condition=condition,n_rows=len(g),n_families=10,auc_rows=float(roc_auc_score((g.cue_kind=='x').astype(int),g.score)),auc_families=family_auc(g)))
     if layer==cfg['primary_layer'] and pos==cfg['primary_position']:
      ev=D[(D.condition=='neutral')&D.cue_kind.isin(['x','y'])];T=scaler.transform(F[[lookup[p] for p in ev.prompt]])
      families=sorted(tr.family.unique());assert len(families)==10
      rng=np.random.default_rng(cfg['seed']+repeat)
      for j in range(cfg['shuffle_repeats']):
       positive=set(rng.choice(families,5,replace=False));perm=tr.family.isin(positive).astype(int).to_numpy()
       nullclf=LogisticRegression(C=cfg['C'],solver='liblinear',max_iter=2000,random_state=cfg['seed']).fit(Z,perm)
       e=ev[['family','cue_kind']].copy();e['score']=nullclf.decision_function(T)
       nulls.append(dict(pair=x,repeat=repeat,shuffle=j,positive_families=json.dumps(sorted(positive)),auc=family_auc(e)))
    print(f'Analysis L{layer} {pos}: {x}/{y}',flush=True)
 scores=pd.DataFrame(scores);auc=pd.DataFrame(aucs);null=pd.DataFrame(nulls)
 primary_auc=auc[(auc.layer==cfg['primary_layer'])&(auc.position==cfg['primary_position'])&(auc.condition=='neutral')]
 calibration=[]
 for r in primary_auc.itertuples():
  n=null[(null.pair==r.pair)&(null.repeat==r.repeat)].auc;q=n.quantile(.95)
  calibration.append(dict(pair=r.pair,repeat=r.repeat,primary_auc=r.auc_families,shuffled_p95=q,shuffles=len(n),shuffled_ge_true=int((n>=r.auc_families).sum()),calibration_ok=bool(r.auc_families>=cfg['probe_auc_min'] and r.auc_families>q)))
 cal=pd.DataFrame(calibration)
 summary=cal.groupby('pair',as_index=False).agg(fits_passed=('calibration_ok','sum'),min_auc=('primary_auc','min'),max_auc=('primary_auc','max'))
 summary['all_fits_pass']=summary.fits_passed==cfg['fit_repeats']
 # Each family contributes equally, regardless of its number of wrappers.
 family=scores.groupby(['pair','repeat','layer','position','cue_kind','condition','family'],as_index=False).agg(mean_z=('z_score','mean'),n_wrappers=('z_score','size'))
 means=family.groupby(['pair','repeat','layer','position','cue_kind','condition'],as_index=False).agg(mean_z=('mean_z','mean'),n_families=('family','size'))
 effects=[]
 for (x,repeat,layer,pos),g in scores.groupby(['pair','repeat','layer','position']):
  neutral=g[g.condition=='neutral'].set_index('cue_id');ne=neutral.loc['empty','z_score']
  for condition in cfg['conditions']:
   cur=g[g.condition==condition].set_index('cue_id');ce=cur.loc['empty','z_score']
   for cue,r in cur.iterrows():effects.append(dict(item_id=r.item_id,pair=x,repeat=repeat,layer=layer,position=pos,cue_id=cue,family=r.family,cue_kind=r.cue_kind,condition=condition,score_delta_vs_neutral=r.z_score-neutral.loc[cue,'z_score'],cue_gain_vs_empty=r.z_score-ce,interaction_vs_neutral=(r.z_score-ce)-(neutral.loc[cue,'z_score']-ne)))
 for name,frame in dict(scores=scores,probe_auc=auc,shuffled=null,probes=pd.DataFrame(probes),calibration=cal,pair_summary=summary,family_scores=family,means=means,contrasts=pd.DataFrame(effects)).items():frame.to_csv(out/(name+'.csv'),index=False)
 np.savez_compressed(out/'probe_weights.npz',**weights)
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(5,4,figsize=(16,18),layout='constrained');colors=dict(x='#267c75',y='#af7850',unrelated='#8d98a4',empty='#272c33')
 primary=means[(means.layer==cfg['primary_layer'])&(means.position==cfg['primary_position'])]
 for ax,(x,y) in zip(axes.flat,cfg['pairs'].items()):
  for kind,color in colors.items():
   g=primary[(primary.pair==x)&(primary.cue_kind==kind)].pivot(index='repeat',columns='condition',values='mean_z')[cfg['conditions']]
   for _,row in g.iterrows():ax.plot(range(5),row,color=color,alpha=.2,lw=.6)
   ax.plot(range(5),g.mean(),color=color,label=kind,marker='o',ms=2)
  passed=int(summary[summary.pair==x].fits_passed.iloc[0]);ax.set_title(f'{x} / {y} | checks {passed}/5',fontsize=10);ax.set_xticks(range(5),['base','name X','think X','avoid X','think Y'],rotation=40,ha='right',fontsize=8);ax.spines[['top','right']].set_visible(False)
 axes.flat[0].legend(fontsize=7,frameon=False);fig.suptitle('L31 assistant prefix: descriptive means; faint lines are overlapping training fits\nScores are relative X-vs-Y margins, not amounts of thought. No error bars or population inference.');fig.savefig(out/'comparison.png',dpi=140);plt.close(fig)
 (out/'README.md').write_text('# 20-pair instruction-probe diagnostic\n\nExploratory. Five evaluation families per concept, four sentence wrappers each. Five overlapping training fits are not independent replications. Scores are relative discriminability, not thought or activation.\n\n'+summary.to_csv(index=False)+'\nOnly pairs passing all five primary checks are candidates for interpretation; failure is not evidence that concept information is absent. No model adoption or causal suppression claim.\n\n![Scores](comparison.png)\n')
 m.update(status='COMPLETED',sklearn=sklearn.__version__,training_descriptions=len(train),factorial_rows=len(design),unique_prompts=len(index),score_rows=len(scores),probes=len(probes),all_primary_calibrated=bool(summary.all_fits_pass.all()),adoption_decision='NOT EVALUATED',generated_answers=0)
 (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(summary.to_string(index=False))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);analyze(ap.parse_args().out)
