"""Analysis regression tests use real saved readouts; no new inference is claimed."""
from pathlib import Path
import tempfile
import unittest
import numpy as np
import pandas as pd
from audit_saved_results import holm, summarize, rebuild_v3, ROOT
from run_robustness import make_design, probe_plan, analyze


class AuditTests(unittest.TestCase):
    def test_holm_known_values(self):
        np.testing.assert_allclose(holm([.01,.04,.03]),[.03,.06,.06])

    def test_summary_uses_pair_count(self):
        r=summarize([-1]*8,n_boot=1000)
        self.assertEqual(r['n_pairs'],8)
        self.assertEqual(r['signflip_p'],2/256)
        self.assertEqual(r['estimate'],-1)

    def test_expanded_design(self):
        d=make_design()
        self.assertEqual(len(d),4608)
        self.assertEqual(d.feature_key.nunique(),4608)
        self.assertEqual(d.query('family=="v3"').cue_text.nunique(),144)
        self.assertEqual(d.query('family=="v2"').cue_text.nunique(),96)
        self.assertEqual(d.query('family=="v3" and cue_source=="new_authored"').cue_text.nunique(),72)
        self.assertEqual(len(probe_plan()),20)
        self.assertEqual(len({str(p) for p in probe_plan()}),20)

    def test_v3_precue_offsets_cancel_from_specificity(self):
        p=ROOT/'1019/results_v3/20261020T070234997011Z'
        m=pd.read_csv(p/'03_all_layer_target_aligned_pre_post.csv')
        original=rebuild_v3(m).interaction.to_numpy()
        # Any cue-independent condition-specific pre-score offset must cancel.
        m['delta_target_std']+=np.where(m.condition=='suppression',30.,-20.)
        np.testing.assert_allclose(rebuild_v3(m).interaction,original,atol=1e-12)

    def test_new_analysis_reproduces_old_readouts(self):
        # Exercise the new follow-up aggregation on ORIGINAL observations.
        d=make_design().query('instruction_frame==0 and context_frame==0 and cue_source=="original"').copy()
        d=d.reset_index(drop=True).reset_index(names='design_row')
        self.assertEqual(len(d),480)
        v2=ROOT/'1019/results_v2/20261019T133851060426Z'
        v3=ROOT/'1019/results_v3/20261020T070234997011Z'
        a=pd.read_csv(v2/'06_layerwise_pre_post_measurements.csv').rename(columns={'delta_probe_std':'delta_target_std'})
        a['target_role']='X'
        b=pd.read_csv(v3/'03_all_layer_target_aligned_pre_post.csv')
        pieces=[]
        for family,old in [('v2',a),('v3',b)]:
            records=d[d.family==family][['design_row','concept','target_role','condition','cue_text']].merge(
                old[['concept','target_role','condition','cue_text','layer','delta_target_std']],
                on=['concept','target_role','condition','cue_text'],validate='one_to_many')
            records['probe_variant']='original';pieces.append(records[['design_row','probe_variant','layer','delta_target_std']])
        bank=pd.read_csv(v2/'01_stimulus_distances_and_ranks.csv')
        d=d.merge(bank[['concept','cue_text','semantic_distance']],on=['concept','cue_text'],how='left',validate='many_to_one')
        oldcounts=a[a.condition=='neutral'][['concept','cue_text','cue_token_count']].drop_duplicates()
        d=d.merge(oldcounts,on=['concept','cue_text'],how='left',validate='many_to_one')
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)
            validation=pd.read_csv(v3/'03_probe_validation_all_layers.csv').query('split=="holdout_description"')
            validation['probe_variant']='original';validation.to_csv(out/'probe_validation.csv',index=False)
            analyze(pd.concat(pieces,ignore_index=True),d,out)
            result=pd.read_csv(out/'v3_focus_sensitivity.csv')
            self.assertEqual(result.n_pairs.unique().tolist(),[8])
            self.assertAlmostEqual(result.estimate.mean(),-.11015731854666672,12)
            slopes=pd.read_csv(out/'v2_all_distance_slopes.csv')
            old=pd.read_csv(v2/'10_distance_slope_by_concept_layer.csv')
            j=slopes.merge(old,on=['concept','layer'],validate='one_to_one')
            np.testing.assert_allclose(j.slope_simple,j.slope_distance_simple,atol=1e-10)
            np.testing.assert_allclose(j.slope_length_adjusted,j.slope_distance_length_adjusted,atol=1e-10)


if __name__=='__main__':
    unittest.main()
