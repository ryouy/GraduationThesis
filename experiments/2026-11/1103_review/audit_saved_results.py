"""Recompute v2/v3 aggregates from saved prompt-level scores; no model access.

Run from any directory: python 1103_review/audit_saved_results.py
Bootstrap resamples concept pairs, never individual layer/cue rows.
"""
from pathlib import Path
import itertools
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / 'results'


def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adjusted = np.empty(len(p))
    adjusted[order] = np.minimum(1, np.maximum.accumulate(
        p[order] * np.arange(len(p), 0, -1)))
    return adjusted


def summarize(values, seed=20261103, n_boot=100000):
    x = np.asarray(values, float)
    assert len(x) >= 3 and np.isfinite(x).all()
    rng = np.random.default_rng(seed)
    boots = rng.choice(x, size=(n_boot, len(x)), replace=True).mean(1)
    signs = np.array(list(itertools.product([-1, 1], repeat=len(x))))
    # Exact under a symmetric sign-flip null, not a randomized-trial p value.
    p = np.mean(np.abs((signs*x).mean(1)) >= abs(x.mean()) - 1e-12)
    loo = (x.sum()-x)/(len(x)-1)
    return dict(n_pairs=len(x), estimate=float(x.mean()),
                ci_low=float(np.quantile(boots, .025)),
                ci_high=float(np.quantile(boots, .975)),
                signflip_p=float(p), n_negative=int((x < 0).sum()),
                leave_one_pair_out_min=float(loo.min()),
                leave_one_pair_out_max=float(loo.max()))


def rebuild_v3(m):
    keys = ['concept', 'target_role', 'triplet', 'layer']
    q = m.pivot(index=keys, columns=['condition', 'cue_role'],
                values='delta_target_std')
    out = q.index.to_frame(index=False)
    for cond in ['neutral', 'suppression']:
        out[cond+'_specificity'] = (
            q[(cond, 'target')]-q[(cond, 'other')]).to_numpy()
    out['interaction'] = out.suppression_specificity-out.neutral_specificity
    return out


def main():
    OUT.mkdir(exist_ok=True)
    v2 = ROOT/'experiments/2026-10/1019/results_v2/20261019T133851060426Z'
    v3 = ROOT/'experiments/2026-10/1019/results_v3/20261020T070234997011Z'
    m2 = pd.read_csv(v2/'06_layerwise_pre_post_measurements.csv')
    m3 = pd.read_csv(v3/'03_all_layer_target_aligned_pre_post.csv')
    checks = {}
    for name, frame, keys, expected, pre, post, delta in [
        ('v2', m2, ['concept', 'condition', 'cue_id', 'cue_text', 'layer'], 4608,
         'pre_probe_std', 'post_probe_std', 'delta_probe_std'),
        ('v3', m3, ['concept', 'target_role', 'condition', 'triplet', 'cue_role', 'layer'],
         6912, 'pre_target_std', 'post_target_std', 'delta_target_std')]:
        assert len(frame) == expected and not frame.duplicated(keys).any()
        np.testing.assert_allclose(frame[post]-frame[pre], frame[delta], atol=1e-12)
        assert np.isfinite(frame[[pre, post, delta]].to_numpy()).all()
        prefixkeys = ['concept', 'condition', 'layer'] + (['target_role'] if name=='v3' else [])
        assert frame.groupby(prefixkeys)[pre].nunique().max() == 1
        checks[name] = {'rows': len(frame), 'unique_inputs': len(frame)//24,
                        'score_arithmetic_and_unique_keys': 'pass',
                        'precue_score_invariance': 'pass'}
    # v2 independent reconstruction, including continuous-distance regression.
    p2 = m2.pivot(index=['concept', 'cue_id', 'cue_text', 'layer'], columns='condition',
                  values='delta_probe_std')
    p2['interaction'] = p2.suppression-p2.neutral
    p2 = p2[['interaction']].reset_index().merge(
        m2[m2.condition=='neutral'][['concept', 'cue_id', 'cue_text', 'layer',
           'semantic_distance', 'cue_token_count', 'measured_bin', 'proposed_level']],
        on=['concept', 'cue_id', 'cue_text', 'layer'], validate='one_to_one')
    slopes = []
    for (concept, layer), g in p2.groupby(['concept', 'layer']):
        d = g.semantic_distance.to_numpy(); n = g.cue_token_count.to_numpy()
        y = g.interaction.to_numpy(); d=d-d.mean(); n=n-n.mean(); y=y-y.mean()
        slopes.append(dict(concept=concept, layer=layer,
            simple=float(d@y/(d@d)),
            adjusted=float(np.linalg.lstsq(np.c_[d,n], y, rcond=None)[0][0])))
    slopes = pd.DataFrame(slopes)
    saved = pd.read_csv(v2/'10_distance_slope_by_concept_layer.csv')
    merged=slopes.merge(saved, on=['concept','layer'], validate='one_to_one')
    np.testing.assert_allclose(merged.simple, merged.slope_distance_simple, atol=1e-10)
    np.testing.assert_allclose(merged.adjusted, merged.slope_distance_length_adjusted, atol=1e-10)
    stats=[]
    for metric in ['simple', 'adjusted']:
        sub=[]
        for layer,g in slopes.groupby('layer'):
            sub.append(dict(layer=int(layer), metric=metric, **summarize(g[metric])))
        sub=pd.DataFrame(sub); sub['holm_24']=holm(sub.signflip_p)
        stats.append(sub)
    pd.concat(stats).to_csv(OUT/'v2_distance_reanalysis.csv', index=False)
    # Distinguish most-distant quartile from authored unrelated cues.
    bins=m2.query('layer==24 and condition=="neutral"')
    pd.crosstab(bins.proposed_level,bins.measured_bin).to_csv(OUT/'v2_bin_label_audit.csv')
    # v3 reconstruct from per-prompt data, not from precomputed interactions.
    r3=rebuild_v3(m3)
    bypair=r3.groupby(['concept','layer']).interaction.mean().reset_index()
    old=pd.read_csv(v3/'09_specificity_by_concept_layer.csv')
    j=bypair.merge(old,on=['concept','layer'],validate='one_to_one')
    np.testing.assert_allclose(j.interaction,j.specificity_interaction,atol=1e-12)
    focus=r3[r3.layer.isin([22,23])]
    tests=[]
    tests.append(dict(analysis='focus_both_roles', **summarize(focus.groupby('concept').interaction.mean())))
    for role in ['X','Y']:
        tests.append(dict(analysis='focus_role_'+role,
            **summarize(focus[focus.target_role==role].groupby('concept').interaction.mean())))
    for triplet in [1,2,3]:
        tests.append(dict(analysis='omit_triplet_'+str(triplet),
            **summarize(focus[focus.triplet!=triplet].groupby('concept').interaction.mean())))
    # Exact target/other token-length matching; selection uses input metadata only.
    length=m3.query('condition=="neutral"').pivot(
        index=['concept','target_role','triplet','layer'],columns='cue_role', values='cue_token_count')
    match=length[length.target==length.other].reset_index()[['concept','target_role','triplet','layer']]
    matched=focus.merge(match,on=['concept','target_role','triplet','layer'],validate='one_to_one')
    tests.append(dict(analysis='exact_target_other_length_match',
        **summarize(matched.groupby('concept').interaction.mean())))
    # Secondary input-based semantic audit: retain triplets with BOTH cue directions passing.
    c=pd.read_csv(v3/'01_audited_XY_control_stimuli.csv')
    passed=c[c.cue_type.isin(['X','Y'])].groupby(['concept','triplet']).independent_expected_direction.all()
    ids=passed[passed].reset_index()[['concept','triplet']]
    sem=focus.merge(ids,on=['concept','triplet'],validate='many_to_one')
    tests.append(dict(analysis='embedding_both_directions_pass',
        **summarize(sem.groupby('concept').interaction.mean())))
    pd.DataFrame(tests).to_csv(OUT/'v3_sensitivity.csv',index=False)
    layerstats=pd.DataFrame([dict(layer=int(l),**summarize(g.interaction))
        for l,g in bypair.groupby('layer')])
    layerstats['holm_24']=holm(layerstats.signflip_p)
    layerstats.to_csv(OUT/'v3_layerwise_reanalysis.csv',index=False)
    focus.groupby(['concept','target_role']).interaction.mean().unstack().to_csv(OUT/'v3_target_reversal.csv')
    # Shared descriptions imply shared probe training/evaluation features across v2/v3.
    assert (v2/'probe_description_bank_v2.json').read_bytes()==(v3/'probe_description_bank_v2.json').read_bytes()
    checks['shared_probe_bank']='identical: v3 is a follow-up, not independent probe replication'
    checks['new_model_inference']='NOT RUN: no GPU/model dependencies or model endpoint access'
    checks['bootstrap_draws']=100000
    checks['signflip_null']='symmetric independent concept-pair effect distribution; exploratory'
    (OUT/'audit_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(pd.DataFrame(tests).round(6).to_string(index=False))
    print('\nv2 layers 22/23/24:')
    print(pd.concat(stats).query('layer>=22').round(6).to_string(index=False))
    print('\nv3 layers 22/23/24:')
    print(layerstats.query('layer>=22').round(6).to_string(index=False))


if __name__=='__main__':
    main()
