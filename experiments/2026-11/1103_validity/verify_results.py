from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

def verify(folder):
    manifest=json.loads((folder/'manifest.json').read_text())
    assert manifest['status']=='COMPLETED'
    d=pd.read_csv(folder/'design.csv');a=pd.read_csv(folder/'answers.csv');r=pd.read_csv(folder/'readouts.csv')
    assert len(d)==216 and len(a)==216 and len(r)==1296
    assert not a.input_id.duplicated().any()
    assert not r.duplicated(['input_id','position','layer']).any()
    np.testing.assert_allclose(a.logp_X-a.logp_Y,a.candidate_margin,atol=1e-12)
    q=r.merge(d,on='input_id',validate='many_to_one')
    w=q.pivot(index=['concept','format','position','layer','cue','proposed_level','distance'],columns='condition',values='score').reset_index()
    old=pd.read_csv(folder/'paired_scores.csv')
    m=w.merge(old,on=['concept','format','position','layer','cue','proposed_level','distance'],validate='one_to_one',suffixes=('_new','_saved'))
    np.testing.assert_allclose(m.suppression_new-m.neutral_new,m.suppression_minus_neutral,atol=1e-12)
    ans=a.merge(d,on='input_id',validate='one_to_one')
    correlations=pd.read_csv(folder/'distance_correlations.csv')
    for keys,g in ans[ans.condition=='cue_only'].groupby(['concept','format']):
        expected=spearmanr(g.distance,g.candidate_margin).statistic
        saved=correlations[(correlations.concept==keys[0])&(correlations['format']==keys[1])&(correlations.metric=='candidate_margin')].rho.iloc[0]
        np.testing.assert_allclose(expected,saved,atol=1e-12)
    from sklearn.metrics import roc_auc_score
    validation=pd.read_csv(folder/'probe_validation.csv')
    held=pd.read_csv(folder/'holdout_scores.csv')
    for keys,g in held.groupby(['concept','format','position','layer']):
        item=validation[(validation.concept==keys[0])&(validation['format']==keys[1])&(validation.position==keys[2])&(validation.layer==keys[3])]
        np.testing.assert_allclose(roc_auc_score(g.label,g.score),item.auc.iloc[0],atol=1e-12)
    if (folder/'legacy_transfer_scores.csv').exists():
        held=pd.read_csv(folder/'legacy_transfer_scores.csv');validation=pd.read_csv(folder/'legacy_transfer_auc.csv')
        for keys,g in held.groupby(['concept','layer','split']):
            item=validation[(validation.concept==keys[0])&(validation.layer==keys[1])&(validation.split==keys[2])]
            np.testing.assert_allclose(roc_auc_score(g.label,g.score),item.auc.iloc[0],atol=1e-12)
    assert len(pd.read_csv(folder/'probe_validation.csv'))==36
    assert len(pd.read_csv(folder/'holdout_scores.csv'))==36*24
    assert len(pd.read_csv(folder/'shuffled_controls.csv'))==720
    report=dict(status='PASS',contexts=216,readouts=1296,probe_evaluations=36,shuffled_fits=720,checks=['candidate log probability arithmetic','paired effects recomputed','all six behavioral distance correlations recomputed','all primary and grammatical-control AUC values recomputed','unique measurement keys and counts'])
    (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);verify(p.parse_args().folder)
