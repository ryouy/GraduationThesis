from pathlib import Path
import csv,json,hashlib
H=Path(__file__).resolve().parent;R=H/'results'
def read(name):return list(csv.DictReader((R/name).open()))
a=read('rescored_answers.csv');m=json.loads((R/'manifest.json').read_text());assert len(a)==m['answers']==384
assert m['new_model_inference']==False and m['unresolved_after_adjudication']==0
for name,sha in m['code_sha256'].items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==sha
assert len(read('changed_scores.csv'))==15 and len(read('review_queue.csv'))==4
for r in a:
 if r['prior_content_review']!='':assert r['prior_content_review']==r['adjudicated_correct'],r['item_id']
assert sum(r['prior_content_review']!='' for r in a)==216
s=read('summary.csv')
expected={'phi3_5mini':(34,6),'qwen1_5b':(27,3),'qwen3b':(26,6),'qwen7b':(28,6)}
for r in s:
 if r['source_path'].startswith('experiments/2026-11/1104_model_comparison/'):
  key=r['source_path'].split('/')[-2];assert (int(r['naming_correct_adjudicated']),int(r['none_correct_v2']))==expected[key]
 elif r['condition']=='B_best_match':assert (r['naming_correct_adjudicated'],r['none_correct_v2'])==('47','12')
 else:assert (r['naming_correct_adjudicated'],r['none_correct_v2'])==('44','12')
print('PASS: 384 answers, 216 prior content labels agree, 15 corrected scores, 4 explicit adjudications; all aggregates verified.')
