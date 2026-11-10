"""Independent recomputation from saved individual rows."""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
p=Path(sys.argv[1]);a=pd.read_csv(p/'answers.csv');s=pd.read_csv(p/'holdout_scores.csv');u=pd.read_csv(p/'probe_auc.csv');d=pd.read_csv(p/'distances_XY.csv');c=pd.read_csv(p/'distance_correlations.csv')
assert len(a)==108 and not a.duplicated(['concept','cue','mode']).any()
assert len(s)==216 and not s.duplicated(['concept','training','layer','description']).any()
assert len(u)==54 and len(d)==36 and len(c)==15
np.testing.assert_allclose(a.margin,a.logp_X-a.logp_Y,atol=1e-12)
np.testing.assert_allclose(d.sim_margin,d.simX-d.simY,atol=1e-7)
for r in u.itertuples():
 g=s[(s.concept==r.concept)&(s.training==r.training)&(s.layer==r.layer)]
 if r.style!='all':g=g[g['style']==r.style]
 assert len(g)==r.n
 assert abs(roc_auc_score(g.label,g.score)-r.auc)<1e-12
j=a[a['mode']=='free'].merge(d,on=['concept','cue'],validate='one_to_one')
for r in c.itertuples():
 g=j[j.concept==r.concept]
 assert abs(spearmanr(g[r.predictor],g[r.outcome]).statistic-r.rho)<1e-12
assert json.loads((p/'manifest.json').read_text())['status']=='COMPLETED'
print('PASS: 108 behavior inputs, 216 heldout scores, 54 AUCs and 15 correlations independently verified.')
