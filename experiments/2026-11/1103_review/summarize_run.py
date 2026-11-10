"""Describe a COMPLETED follow-up without treating variants as independent n."""
from pathlib import Path
import argparse,json
import pandas as pd


def summarize_run(folder):
    manifest=json.loads((folder/'completed_manifest.json').read_text())
    assert manifest['status']=='COMPLETED'
    v3=pd.read_csv(folder/'v3_focus_sensitivity.csv')
    v2=pd.read_csv(folder/'v2_distance_sensitivity.csv')
    validation=pd.read_csv(folder/'probe_validation.csv')
    assert v3.n_pairs.eq(8).all() and v2.n_pairs.eq(8).all()
    baseline=v3.query('probe_variant=="original" and instruction_frame==0 and context_frame==0')
    # Summaries below count sensitivity configurations, NOT statistical replicates.
    group=v3.groupby(['cue_source','target_role']).estimate.agg(
        configurations='size',negative_configurations=lambda x:int((x<0).sum()),
        minimum='min',maximum='max',median='median').reset_index()
    auc=validation[validation.layer.isin([22,23])].groupby('probe_variant').auc.agg(
        mean_auc='mean',min_auc='min',below_075=lambda x:int((x<.75).sum())).reset_index()
    original_v2=v2.query('probe_variant=="original" and instruction_frame==0 and context_frame==0 and layer in [22,23,24]')
    prefix=[]
    for p in sorted(folder.glob('prefix_invariance_*.csv')):
        d=pd.read_csv(p)
        assert d.token_prefix_identical.all()
        prefix.append(dict(file=p.name,n=len(d),max_absolute=float(d.absolute.max()),max_relative=float(d.relative.max())))
    assert len(prefix)==8 and sum(x['n'] for x in prefix)==4608
    result=dict(manifest=manifest,baseline_v3=baseline.to_dict('records'),
        v3_sensitivity_ranges=group.to_dict('records'),
        probe_auc=auc.to_dict('records'),baseline_v2=original_v2.to_dict('records'),
        prefix_checks=prefix,
        interpretation='Exploratory robustness of eight selected pairs; configurations are not independent replications.')
    (folder/'review_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Baseline v3:\n'+baseline.to_string(index=False))
    print('\nV3 sensitivity ranges:\n'+group.to_string(index=False))
    print('\nProbe holdout AUC (22/23):\n'+auc.to_string(index=False))
    print('\nBaseline v2:\n'+original_v2.to_string(index=False))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path)
    summarize_run(p.parse_args().folder)
