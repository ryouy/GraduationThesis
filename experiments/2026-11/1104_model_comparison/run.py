from pathlib import Path
import sys,json,time,hashlib,gc,traceback,importlib.util,argparse
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_grade',ROOT/'experiments/2026-11/1103_fresh_check/run.py');grader=importlib.util.module_from_spec(spec);spec.loader.exec_module(grader)
SYSTEM='You are a helpful assistant.'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--resolve',action='store_true');ap.add_argument('--key');args=ap.parse_args();args.out.mkdir(exist_ok=True,parents=True)
 if args.resolve:
  from huggingface_hub import model_info
  entries=json.loads((HERE/'models.json').read_text())
  for e in entries:e['revision']=e.get('revision') or model_info(e['model']).sha
  (args.out/'resolved_models.json').write_text(json.dumps(entries,indent=2));print('REVISIONS FIXED',json.dumps(entries),flush=True);return
 import torch,transformers
 from transformers import AutoTokenizer,AutoModelForCausalLM,GenerationConfig
 entries=json.loads((args.out/'resolved_models.json').read_text());entry=next(e for e in entries if e['key']==args.key);out=args.out/args.key;out.mkdir(exist_ok=True)
 m=dict(status='RUNNING',**entry,system=SYSTEM,precision='float16',attention='sdpa',quantized=False,hashes={p.name:sha(p) for p in [Path(__file__),HERE/'PLAN.md',HERE/'models.json']},questions_sha256=sha(ROOT/'experiments/2026-11/1103_fresh_check/results/answers.csv'),rules_sha256=sha(ROOT/'experiments/2026-11/1103_fresh_check/rules.json'))
 def save(): (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 save()
 try:
  assert torch.cuda.is_available();torch.manual_seed(42);torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
  print('LOAD',entry['model'],entry['revision'],flush=True);t=time.perf_counter();tok=AutoTokenizer.from_pretrained(entry['model'],revision=entry['revision'],trust_remote_code=False)
  attempts=[];model=None
  for budget in ['14GiB','13GiB']:
   try:
    model=AutoModelForCausalLM.from_pretrained(entry['model'],revision=entry['revision'],dtype=torch.float16,attn_implementation='sdpa',device_map='auto',max_memory={0:budget,'cpu':'8GiB'},offload_state_dict=True,trust_remote_code=False).eval();attempts.append(dict(budget=budget,status='loaded'));break
   except torch.OutOfMemoryError as ex:
    attempts.append(dict(budget=budget,error=repr(ex)));gc.collect();torch.cuda.empty_cache()
  assert model is not None,'Model could not be loaded after memory retry.'
  m.update(load_seconds=time.perf_counter()-t,load_attempts=attempts,device_map={k:str(v) for k,v in model.hf_device_map.items()},actual_dtype=str(next(model.parameters()).dtype),actual_attention=model.config._attn_implementation,parameters=sum(p.numel() for p in model.parameters()))
  eos=model.generation_config.eos_token_id or tok.eos_token_id;pad=tok.pad_token_id
  if pad is None:pad=eos[0] if isinstance(eos,list) else eos
  config=GenerationConfig(do_sample=False,num_beams=1,max_new_tokens=32,repetition_penalty=1.0,eos_token_id=eos,pad_token_id=pad,bos_token_id=tok.bos_token_id,use_cache=True)
  m['generation_config']=config.to_dict();save()
  questions=pd.read_csv(ROOT/'experiments/2026-11/1103_fresh_check/results/answers.csv',keep_default_na=False);assert len(questions)==42 and questions.item_id.is_unique
  rows=[];tokenrows=[];torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
  for i,r in enumerate(questions.itertuples()):
   rendered=tok.apply_chat_template([{'role':'system','content':SYSTEM},{'role':'user','content':r.prompt}],tokenize=False,add_generation_prompt=True)
   batch=tok(rendered,return_tensors='pt',add_special_tokens=False).to(model.device)
   torch.cuda.synchronize();t=time.perf_counter()
   with torch.inference_mode():generated=model.generate(**batch,generation_config=config)
   torch.cuda.synchronize();elapsed=time.perf_counter()-t
   ids=generated[0,batch.input_ids.shape[1]:].tolist();answer=tok.decode(ids,skip_special_tokens=True);eoslist=eos if isinstance(eos,list) else [eos]
   rows.append(dict(model_key=entry['key'],item_id=r.item_id,target=r.target,text=r.text,prompt=r.prompt,rendered_prompt=rendered,answer=answer,output_tokens=len(ids),seconds=elapsed,truncated=bool(len(ids)==32 and ids[-1] not in eoslist),**grader.grade(answer,r.target)))
   tokenrows.append(dict(item_id=r.item_id,input_ids=batch.input_ids[0].tolist(),attention_mask=batch.attention_mask[0].tolist(),output_ids=ids))
   pd.DataFrame(rows).to_csv(out/'answers.csv',index=False)
   if i%6==0:print(entry['key'],i,'/42',r.target,repr(answer),flush=True)
  a=pd.DataFrame(rows);clear=a[a.target!='none'];none=a[a.target=='none'];per=clear.groupby('target').correct.sum();per.to_csv(out/'correct_per_concept.csv')
  m.update(status='COMPLETED',contexts=len(a),correct=int(clear.correct.sum()),clear_n=len(clear),min_per_concept=int(per.min()),none_correct=int(none.correct.sum()),behavior_pass=bool(clear.correct.sum()>=30 and per.min()>=4),none_pass=bool(none.correct.sum()>=5),all_pass=bool(clear.correct.sum()>=30 and per.min()>=4 and none.correct.sum()>=5),truncations=int(a.truncated.sum()),generation_seconds=time.perf_counter()-start,peak_vram_bytes=int(torch.cuda.max_memory_allocated()),torch=torch.__version__,transformers=transformers.__version__,gpu=torch.cuda.get_device_name(0))
  (out/'tokens.json').write_text(json.dumps(tokenrows));save();print('MODEL COMPLETED',entry['key'],json.dumps({k:m[k] for k in ['correct','clear_n','min_per_concept','none_correct','all_pass','truncations']}),flush=True)
 except Exception as e:
  m.update(status='ERROR',error=repr(e),traceback=traceback.format_exc());save();print('MODEL ERROR',entry['key'],m['traceback'],flush=True);sys.exit(1)
if __name__=='__main__':main()
