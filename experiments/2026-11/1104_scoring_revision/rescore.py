"""Regrade saved answers only; no model or network access in this script."""
from pathlib import Path
import csv,json,hashlib,argparse,subprocess
from grade_v2 import grade
H=Path(__file__).resolve().parent
DEFAULT_COMMIT='ee04dcc06375799bff953d5cc9ff7ad3d852bf30'
def read_rows(p):return list(csv.DictReader(p.open()))
def boolean(v):
 if str(v).lower()=='true':return True
 if str(v).lower()=='false':return False
 raise ValueError('Unknown boolean '+str(v))
def write_csv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path);ap.add_argument('--out',type=Path,default=H/'results');ap.add_argument('--commit',default=DEFAULT_COMMIT);args=ap.parse_args()
 repo=H.parent
 if args.inputs:
  src=args.inputs;info=json.loads((src/'sources.json').read_text());assert info['commit']==args.commit
 else:
  import tempfile
  temp=tempfile.TemporaryDirectory();src=Path(temp.name)
  # Read locally available git objects from this exact commit, never current main.
  paths=subprocess.check_output(['git','ls-tree','-r','--name-only',args.commit],cwd=repo,text=True).splitlines()
  answers=[p for p in paths if p.endswith('/answers.csv') and p.startswith(('1104_model_comparison/results/','1104_phi_validation/results/','1104_phi_prompt_diagnostic/results/'))]
  info={'commit':args.commit,'answer_paths':answers}
  for p in paths:
   if p in answers or (p.endswith('/raw_answer_review.csv') and p.startswith(('1104_phi_validation/','1104_phi_prompt_diagnostic/'))):
    dst=src/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(subprocess.check_output(['git','show',args.commit+':'+p],cwd=repo))
 refs={}
 for path in src.rglob('raw_answer_review.csv'):
  rows=read_rows(path)
  parent=path.parent
  answer_path=next(p for p in info['answer_paths'] if Path(p).parent.parent==parent.relative_to(src))
  for r in rows:
   value=r.get('review_correct',r.get('review_content_correct'))
   refs[(answer_path,r['item_id'])]=boolean(value)
 adjudications={(r['source_path'],r['item_id']):r for r in read_rows(H/'adjudications.csv')}
 output=[];hashes={}
 for path in info['answer_paths']:
  rawpath=src/path;hashes[path]=hashlib.sha256(rawpath.read_bytes()).hexdigest()
  for r in read_rows(rawpath):
   result=grade(r['answer'],r['target'],boolean(r['truncated']))
   prior=refs.get((path,r['item_id']))
   decision=adjudications.get((path,r['item_id']))
   adjudicated=prior if result['correct'] is None and prior is not None else result['correct']
   if decision is not None:
    assert result['correct'] is None, 'Manual review must not silently override decidable v2 scores'
    adjudicated=boolean(decision['correct'])
    if prior is not None:assert prior==adjudicated
   if prior is not None and result['correct'] is not None:assert prior==result['correct'],(path,r['item_id'],result)
   output.append(dict(source_path=path,item_id=r['item_id'],model_key=r['model_key'],condition=r.get('condition','single'),target=r['target'],text=r['text'],answer=r['answer'],frozen_correct=boolean(r['correct']),v2_correct=result['correct'],v2_status=result['status'],parsed_label=result['parsed_label'],reason=result['reason'],format_ok=result['format_ok'],truncated=result['truncated'],needs_review=result['needs_review'],prior_content_review=prior,adjudicated_correct=adjudicated,adjudication_reason=decision['reason'] if decision else '',adjudicator='assistant raw-answer review, 2026-11-04' if decision else ''))
 assert len(output)==384
 assert len({(r['source_path'],r['item_id']) for r in output})==384
 args.out.mkdir(exist_ok=True,parents=True)
 write_csv(args.out/'rescored_answers.csv',output)
 review=[r for r in output if r['needs_review']];write_csv(args.out/'review_queue.csv',review)
 changed=[r for r in output if r['v2_correct'] is not None and r['frozen_correct']!=r['v2_correct']];write_csv(args.out/'changed_scores.csv',changed)
 from collections import defaultdict
 groups=defaultdict(list)
 for r in output:groups[(r['source_path'],r['condition'])].append(r)
 summary=[]
 for (source,condition),rows in groups.items():
  c=[r for r in rows if r['target']!='none'];n=[r for r in rows if r['target']=='none']
  summary.append(dict(source_path=source,condition=condition,naming_n=len(c),naming_correct_v2=sum(r['v2_correct'] is True for r in c),naming_unresolved_v2=sum(r['v2_correct'] is None for r in c),naming_correct_adjudicated=sum(r['adjudicated_correct'] is True for r in c),none_n=len(n),none_correct_v2=sum(r['v2_correct'] is True for r in n),none_unresolved_v2=sum(r['v2_correct'] is None for r in n),format_conforms=sum(r['format_ok'] is True for r in rows),format_unknown=sum(r['format_ok'] is None for r in rows),truncations=sum(r['truncated'] for r in rows)))
 write_csv(args.out/'summary.csv',summary)
 refchecks=sum((r['source_path'],r['item_id']) in refs for r in output)
 meta={'source_commit':args.commit,'source_sha256':hashes,'code_sha256':{n:hashlib.sha256((H/n).read_bytes()).hexdigest() for n in ['grade_v2.py','rules_v2.json','rescore.py','test_grade_v2.py','adjudications.csv']},'answers':len(output),'changed_decidable_scores':len(changed),'review_queue':len(review),'unresolved_content':sum(r['v2_correct'] is None for r in output),'existing_manual_labels':refchecks,'decidable_matches_prior_review':sum(r['prior_content_review'] is not None and r['v2_correct'] is not None and r['prior_content_review']==r['v2_correct'] for r in output),'manual_queue_adjudications':len(adjudications),'unresolved_after_adjudication':sum(r['adjudicated_correct'] is None for r in output),'new_model_inference':False}
 (args.out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(json.dumps(meta,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
