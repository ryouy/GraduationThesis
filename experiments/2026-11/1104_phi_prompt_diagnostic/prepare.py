from pathlib import Path
import csv,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
source=ROOT/'1104_phi_validation/questions.csv'
rows=[]
for r in csv.DictReader(source.open()):
 category={'banana':'fruit','apple':'fruit','elephant':'animal','giraffe':'animal','piano':'musical instrument','violin':'musical instrument'}.get(r['target'])
 if category is None:category=['fruit','animal','musical instrument'][int(r['item_id'].split('_')[-1])//4]
 prompts={'A_original':r['prompt'],'B_best_match':f"Context:\n{r['text']}\n\nWhich {category} best matches the description in the context? Answer with the most likely name. If the context is unrelated to {category}s, answer none. Answer with one name only."}
 for condition,prompt in prompts.items():rows.append(dict(item_id=r['item_id']+'__'+condition,source_item_id=r['item_id'],condition=condition,target=r['target'],text=r['text'],prompt=prompt))
with (HERE/'questions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
(HERE/'source.json').write_text(json.dumps({'path':'1104_phi_validation/questions.csv','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'set':'previously evaluated; exploratory paired diagnostic'},indent=2)+'\n')
