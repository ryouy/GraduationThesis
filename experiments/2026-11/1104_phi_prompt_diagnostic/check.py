from pathlib import Path
from collections import Counter
import csv,json,hashlib,re
import grade
H=Path(__file__).resolve().parent
q=list(csv.DictReader((H/'questions.csv').open()));assert len(q)==144 and len({r['item_id'] for r in q})==144
old={r['item_id']:r for r in csv.DictReader((H.parent/'experiments/2026-11/1104_phi_validation/questions.csv').open())}
src=json.loads((H/'source.json').read_text());assert hashlib.sha256((H.parent/src['path']).read_bytes()).hexdigest()==src['sha256']
for condition in ['A_original','B_best_match']:
 rows=[r for r in q if r['condition']==condition];assert len(rows)==72 and len({r['source_item_id'] for r in rows})==72
 assert Counter(r['target'] for r in rows)==Counter({**{t:10 for t in grade.RULES['aliases']},'none':12})
 for r in rows:
  base=old[r['source_item_id']];assert r['text']==base['text'] and r['target']==base['target']
  if condition=='A_original':assert r['prompt']==base['prompt']
  instruction=r['prompt'].split('\n\n',1)[1]
  assert not any(re.search(r'\b'+re.escape(v)+r'\b',instruction,re.I) for vs in grade.RULES['aliases'].values() for v in vs)
assert grade.grade('Grand Piano','piano')['correct']
assert grade.grade('Upright piano. It has keys.','piano')['correct']
assert not grade.grade('Violin or viola','violin')['correct']
assert grade.grade('None. The context is about a worker.','none')['correct']
assert not grade.grade('None. Banana.','none')['correct']
print('Preflight PASS: all 72 texts paired, A prompts identical, no answer-name instruction leak; scoring cases passed.')
