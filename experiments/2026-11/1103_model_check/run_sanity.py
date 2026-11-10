"""Post-hoc positive controls; do not replace prespecified calibration scores."""
from pathlib import Path
import sys,json,re
import torch,pandas as pd
from transformers import AutoTokenizer,AutoModelForCausalLM
from run_check import build,WORDS
base=Path(sys.argv[1]);size=sys.argv[2];m=json.loads((base/size/'manifest.json').read_text())
qs={'banana':('What fruit is long, yellow, curved, and peeled before eating?','A long yellow curved fruit that is peeled before eating.'),'apple':('What round red or green fruit grows in orchards and is used to make cider?','A round red or green orchard fruit used to make cider.'),'elephant':('What very large animal has a long trunk, big ears, and ivory tusks?','A very large animal with a long trunk, big ears, and ivory tusks.'),'giraffe':('What spotted African animal has a very long neck and eats leaves from tall trees?','A spotted African animal with a very long neck that eats leaves from tall trees.'),'piano':('What musical instrument has 88 black and white keys and foot pedals?','A musical instrument with 88 black and white keys and foot pedals.'),'violin':('What small four-stringed instrument is held under the chin and played with a bow?','A small four-stringed instrument held under the chin and played with a bow.')}
torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.manual_seed(42)
tok=AutoTokenizer.from_pretrained(m['model'],revision=m['revision']);model=AutoModelForCausalLM.from_pretrained(m['model'],revision=m['revision'],dtype=torch.float32,attn_implementation='eager').cuda().eval();rows=[]
for word,(q,text) in qs.items():
 pair={'apple':'banana','giraffe':'elephant','violin':'piano'}.get(word,word)
 for mode in ['direct','context']:
  p=q+' Answer with the specific name only.' if mode=='direct' else build(pair,text,'naming')[0]
  rendered=tok.apply_chat_template([{'role':'user','content':p}],tokenize=False,add_generation_prompt=True);b=tok(rendered,return_tensors='pt',add_special_tokens=False).to('cuda')
  with torch.inference_mode():g=model.generate(**b,max_new_tokens=32,do_sample=False,pad_token_id=tok.eos_token_id)
  ans=tok.decode(g[0,b.input_ids.shape[1]:],skip_special_tokens=True);mentions=[w for w in WORDS if re.search(r'\b'+w+r's?\b',ans,re.I)]
  rows.append(dict(model=size,target=word,mode=mode,prompt=p,answer=ans,exact_name_correct=mentions==[word],post_hoc=True))
pd.DataFrame(rows).to_csv(base/size/'posthoc_sanity.csv',index=False);print(pd.DataFrame(rows).to_string(index=False),flush=True)
