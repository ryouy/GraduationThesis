"""Synthetic offline fixture only: tests pairing/verification; no model inference."""
from pathlib import Path
import json,hashlib,tempfile,unittest
import pandas as pd
import grade,analyze
H=Path(__file__).resolve().parent
class AnalysisTest(unittest.TestCase):
 def test_pairing_and_detect_tampering(self):
  q=pd.read_csv(H/'questions.csv',keep_default_na=False)
  old=pd.read_csv(H.parent/'1104_phi_validation/results/20261104T012418280152Z/phi3_5mini/answers.csv',keep_default_na=False).set_index('item_id')
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);out=root/'phi3_5mini';out.mkdir();rows=[];tokens=[]
   for r in q.itertuples():
    answer=old.loc[r.source_item_id,'answer']
    if r.source_item_id=='banana_00' and r.condition=='B_best_match':answer='Mango'
    rows.append(dict(item_id=r.item_id,source_item_id=r.source_item_id,condition=r.condition,target=r.target,text=r.text,prompt=r.prompt,answer=answer,output_tokens=1,truncated=False,**grade.grade(answer,r.target)))
    tokens.append(dict(item_id=r.item_id,input_ids=[1],attention_mask=[1],output_ids=[2]))
   a=pd.DataFrame(rows);a.to_csv(out/'answers.csv',index=False);(out/'tokens.json').write_text(json.dumps(tokens))
   manifest=dict(status='COMPLETED',revision='2fe192450127e6a83f7441aef6e3ca586c338b77',hashes={name:hashlib.sha256((H/name).read_bytes()).hexdigest() for name in ['run.py','PLAN.md','models.json','grade.py','rules.json','questions.csv','source.json']},actual_dtype='torch.float16',generation_config={'do_sample':False,'repetition_penalty':1},**grade.summarize(a))
   (out/'manifest.json').write_text(json.dumps(manifest));(root/'resolved_models.json').write_text((H/'models.json').read_text());a.groupby('target').correct.sum().to_csv(out/'correct_per_concept.csv')
   analyze.analyze(root)
   summary=pd.read_csv(root/'condition_summary.csv').set_index('condition');self.assertEqual(summary.loc['A_original','naming_correct']-summary.loc['B_best_match','naming_correct'],1)
   transitions=json.loads((root/'paired_transitions.json').read_text());self.assertEqual(transitions['naming']['correct -> wrong'],1)
   a.loc[0,'prompt']='tampered';a.to_csv(out/'answers.csv',index=False)
   with self.assertRaises(AssertionError):analyze.verify(root)
if __name__=='__main__':unittest.main()
