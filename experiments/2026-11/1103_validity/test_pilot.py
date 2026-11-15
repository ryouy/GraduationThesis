import unittest
from run_pilot import inputs,build,PAIRS

class PilotTests(unittest.TestCase):
    def test_crossed_design_and_no_target_in_cue_only(self):
        d=inputs()
        self.assertEqual(len(d),216)
        self.assertTrue(d.groupby(['concept','format','condition']).size().eq(12).all())
        for r in d[d.condition=='cue_only'].itertuples():
            # Target names are absent from both stimulus cues and instructions.
            self.assertNotIn(r.concept,r.content.lower())
            self.assertNotIn(r.comparison,r.content.lower())
    def test_readout_character_anchor(self):
        for fmt in ['markers','natural']:
            s,end=build(fmt,'neutral','banana','A yellow fruit lay on the table.')
            self.assertEqual(s[end-1], ':' if fmt=='markers' else '.')
            self.assertEqual(s.count('STATE:'),2 if fmt=='markers' else 0)
    def test_instruction_contrast_keeps_cue_and_question(self):
        a,_=build('natural','neutral','banana','A yellow fruit lay on the table.')
        b,_=build('natural','suppression','banana','A yellow fruit lay on the table.')
        self.assertEqual(a.split('Context:')[1],b.split('Context:')[1])

if __name__=='__main__':unittest.main()
