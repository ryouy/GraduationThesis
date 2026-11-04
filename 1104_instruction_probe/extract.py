"""Extract fixed positions only; never generate or grade answers."""
from pathlib import Path
import argparse,json,time,hashlib,shutil,traceback
from check import check_design
H=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();train,design,cfg=check_design()
 frozen=json.loads((H/'FROZEN_SHA256.json').read_text())
 for name,digest in frozen.items():assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,name
 out=args.out;out.mkdir(exist_ok=False,parents=True)
 for name in ['training.csv','design.csv','config.json','sources.json','PLAN.md','FROZEN_SHA256.json']:shutil.copyfile(H/name,out/name)
 manifest=dict(status='EXTRACTING',config=cfg,fixed_hashes=frozen,forward_count=0,generated_answers=0)
 def save_manifest():(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 save_manifest()
 try:
  import numpy as np
  import torch,transformers
  from transformers import AutoTokenizer,AutoModelForCausalLM
  assert torch.cuda.is_available(),'T4 GPU is required.'
  torch.set_num_threads(4);torch.manual_seed(cfg['seed']);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
  tok=AutoTokenizer.from_pretrained(cfg['model'],revision=cfg['revision'],use_fast=True,trust_remote_code=False);assert tok.is_fast
  start=time.perf_counter();model=AutoModelForCausalLM.from_pretrained(cfg['model'],revision=cfg['revision'],dtype=torch.float16,attn_implementation='sdpa',device_map={'':'cuda:0'},trust_remote_code=False).eval()
  assert model.config.num_hidden_layers==cfg['expected_depth']
  assert str(next(model.parameters()).dtype)=='torch.float16'
  manifest.update(load_seconds=time.perf_counter()-start,gpu=torch.cuda.get_device_name(0),torch=torch.__version__,transformers=transformers.__version__,hidden_size=model.config.hidden_size,actual_attention=model.config._attn_implementation,actual_dtype=str(next(model.parameters()).dtype),actual_depth=model.config.num_hidden_layers)
  prompts=list(dict.fromkeys([r['prompt'] for r in train]+[r['prompt'] for r in design]));assert len(prompts)==361
  index=[];tokens=[];features={(l,p):[] for l in cfg['layers'] for p in cfg['positions']}
  def checkpoint():
   (out/'prompt_index.json').write_text(json.dumps(index,indent=2)+'\n');(out/'tokens.json').write_text(json.dumps(tokens)+'\n')
   for (layer,pos),rows in features.items():np.savez_compressed(out/f'features_L{layer}_{pos}.npz',features=np.stack(rows).astype(np.float16))
   save_manifest()
  torch.cuda.reset_peak_memory_stats();started=time.perf_counter()
  with torch.inference_mode():
   for i,prompt in enumerate(prompts):
    rendered=tok.apply_chat_template([{'role':'system','content':cfg['system']},{'role':'user','content':prompt}],tokenize=False,add_generation_prompt=True)
    assert rendered.count(prompt)==1
    text=prompt.split('\n\nContext:\n',1)[1].split('\n\nGive one short response',1)[0]
    char=rendered.index(prompt)+prompt.index('\n\nContext:\n')+len('\n\nContext:\n')+len(text)-1
    batch=tok(rendered,return_tensors='pt',return_offsets_mapping=True,add_special_tokens=False)
    offsets=batch.pop('offset_mapping')[0].tolist();hit=[j for j,(lo,hi) in enumerate(offsets) if lo<=char<hi];assert len(hit)==1
    positions={'context_end':hit[0],'assistant_start':batch.input_ids.shape[1]-1}
    result=model(**batch.to('cuda'),output_hidden_states=True,use_cache=False,return_dict=True)
    for layer in cfg['layers']:
     for pos in cfg['positions']:features[(layer,pos)].append(result.hidden_states[layer][0,positions[pos]].cpu().numpy().copy())
    del result
    prompt_id=f'p{i:04d}';index.append(dict(prompt_id=prompt_id,prompt=prompt,text=text,rendered_prompt=rendered))
    tokens.append(dict(prompt_id=prompt_id,input_ids=batch.input_ids[0].tolist(),attention_mask=batch.attention_mask[0].tolist(),context_end_char=char,context_end_offset=offsets[positions['context_end']],positions=positions))
    manifest['forward_count']=i+1
    if i%30==0 or i==len(prompts)-1:
     checkpoint();print('Hidden extraction',i+1,'/',len(prompts),flush=True)
  manifest.update(status='FEATURES_COMPLETED',extraction_seconds=time.perf_counter()-started,peak_vram_bytes=int(torch.cuda.max_memory_allocated()))
  checkpoint();print('Feature extraction complete. No answers generated.',flush=True)
 except Exception as exc:
  manifest.update(status='ERROR',error=type(exc).__name__,traceback=traceback.format_exc());save_manifest();raise
if __name__=='__main__':main()
