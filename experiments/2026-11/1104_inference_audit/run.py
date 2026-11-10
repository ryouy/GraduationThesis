from pathlib import Path
import sys,json,hashlib,gc,time,traceback,importlib.util
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fresh_grading',ROOT/'experiments/2026-11/1103_fresh_check/run.py');fresh=importlib.util.module_from_spec(spec);spec.loader.exec_module(fresh)
MODEL='Qwen/Qwen2.5-1.5B-Instruct';REV='989aa7980e4cf806f80c7fef2b1adb7bc71aa306'
SYSTEM='You are Qwen, created by Alibaba Cloud. You are a helpful assistant.'
def main():
 import argparse,torch,transformers
 from transformers import AutoTokenizer,AutoModelForCausalLM
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
 torch.manual_seed(42);torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 assert torch.cuda.is_available()
 old=pd.read_csv(ROOT/'experiments/2026-11/1103_fresh_check/results/answers.csv',keep_default_na=False);assert len(old)==42
 tok=AutoTokenizer.from_pretrained(MODEL,revision=REV)
 rows=[];tokens=[];meta=[];errors=[];checks=[];gpu_logits=None
 def inputs(p,official):
  messages=([{'role':'system','content':SYSTEM}] if official else [])+[{'role':'user','content':p}]
  text=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
  b=tok([text],return_tensors='pt') if official else tok(text,return_tensors='pt',return_offsets_mapping=True,add_special_tokens=False)
  b.pop('offset_mapping',None)
  return text,b
 for r in old.itertuples():
  t1,b1=inputs(r.prompt,False);t2,b2=inputs(r.prompt,True)
  checks.append(dict(item_id=r.item_id,text_equal=t1==t2,ids_equal=torch.equal(b1.input_ids,b2.input_ids),mask_equal=torch.equal(b1.attention_mask,b2.attention_mask),legacy_text=t1,official_text=t2))
 pd.DataFrame(checks).to_csv(out/'input_comparison.csv',index=False)
 modes=[('legacy_fp32_eager',torch.float32,'eager',False),('official_input_only_fp32_eager',torch.float32,'eager',False),('official_fp32_eager',torch.float32,'eager',True),('official_fp32_sdpa',torch.float32,'sdpa',True),('official_auto_sdpa','auto','sdpa',True),('official_fp16_sdpa',torch.float16,'sdpa',True)]
 for name,dtype,attn,official in modes:
  print('MODE',name,flush=True);model=None;start=time.time()
  try:
   model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REV,torch_dtype=dtype,device_map='auto',attn_implementation=attn).eval()
   meta.append(dict(mode=name,dtype=str(next(model.parameters()).dtype),attention=model.config._attn_implementation,device=str(model.device),generation_config=model.generation_config.to_dict()))
   for i,r in enumerate(old.itertuples()):
    text,b=inputs(r.prompt,official)
    if name=='official_input_only_fp32_eager':b=tok([text],return_tensors='pt')
    b=b.to(model.device)
    with torch.inference_mode():
     if i==0:
      logits=model(**b,use_cache=False).logits[0,-1].float().cpu();vals,ids=logits.topk(10)
      entry=dict(mode=name,top10=[dict(id=int(j),token=tok.decode([int(j)]),logit=float(v)) for j,v in zip(ids,vals)])
      if name=='legacy_fp32_eager':gpu_logits=logits.clone()
      (out/(name+'_first_token.json')).write_text(json.dumps(entry,indent=2))
     result=model.generate(**b,do_sample=False,max_new_tokens=32,pad_token_id=tok.eos_token_id)
     seq=result[0,b.input_ids.shape[1]:].tolist();answer=tok.decode(seq,skip_special_tokens=True)
     if i==0 and name=='legacy_fp32_eager':
      z=model(**b,output_hidden_states=True,use_cache=False);del z
      after=model.generate(**b,do_sample=False,max_new_tokens=32,pad_token_id=tok.eos_token_id)[0,b.input_ids.shape[1]:].tolist()
      (out/'hidden_extraction_control.json').write_text(json.dumps(dict(tokens_equal=seq==after,before=seq,after=after)))
    rows.append(dict(mode=name,item_id=r.item_id,target=r.target,prompt=r.prompt,answer=answer,old_answer=r.answer,matches_old=answer==r.answer,tokens=len(seq),**fresh.grade(answer,r.target)))
    tokens.append(dict(mode=name,item_id=r.item_id,input_ids=b.input_ids[0].tolist(),attention_mask=b.attention_mask[0].tolist(),output_ids=seq))
    if i%12==0:print(name,i,'/42',answer,flush=True)
    pd.DataFrame(rows).to_csv(out/'answers.csv',index=False)
   # Supplemental official default sampling, with fixed seed and unchanged questions.
   if name=='official_auto_sdpa':
    samples=[]
    for tag,p in [('banana_context',old.iloc[0].prompt),('banana_direct','What fruit is long, yellow, curved, and peeled before eating? Answer with the specific name only.'),('official_example','Give me a short introduction to large language model.')]:
     _,b=inputs(p,True);b=b.to(model.device);torch.manual_seed(42)
     with torch.inference_mode():g=model.generate(**b,max_new_tokens=512)
     seq=g[0,b.input_ids.shape[1]:].tolist();samples.append(dict(item_id=tag,prompt=p,answer=tok.decode(seq,skip_special_tokens=True),output_ids=seq,tokens=len(seq)))
    (out/'official_default_samples.json').write_text(json.dumps(samples,indent=2))
  except Exception as e:
   errors.append(dict(mode=name,error=repr(e),traceback=traceback.format_exc()));print('MODE ERROR',name,repr(e),flush=True)
  finally:
   del model;gc.collect();torch.cuda.empty_cache()
  print('MODE DONE',name,round(time.time()-start,1),'s',flush=True)
 # CPU check compares same weights, precision, backend, input and greedy decoding.
 print('CPU CHECK',flush=True)
 try:
  model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REV,torch_dtype=torch.float32,attn_implementation='eager').cpu().eval();r=old.iloc[0];_,b=inputs(r.prompt,False)
  with torch.inference_mode():
   cpu=model(**b,use_cache=False).logits[0,-1].float().cpu();g=model.generate(**b,max_new_tokens=32,do_sample=False,pad_token_id=tok.eos_token_id)
  seq=g[0,b.input_ids.shape[1]:].tolist();vals,ids=cpu.topk(10)
  check=dict(item_id=r.item_id,answer=tok.decode(seq,skip_special_tokens=True),output_ids=seq,max_absolute_logit_difference=float((cpu-gpu_logits).abs().max()) if gpu_logits is not None else None,top1_cpu=int(cpu.argmax()),top1_gpu=int(gpu_logits.argmax()) if gpu_logits is not None else None,top10=[dict(id=int(j),token=tok.decode([int(j)]),logit=float(v)) for j,v in zip(ids,vals)])
  (out/'cpu_check.json').write_text(json.dumps(check,indent=2));print('CPU ANSWER',check['answer'],flush=True)
 except Exception as e:errors.append(dict(mode='cpu',error=repr(e),traceback=traceback.format_exc()));print('CPU ERROR',repr(e),flush=True)
 pd.DataFrame(rows).to_csv(out/'answers.csv',index=False)
 (out/'tokens.json').write_text(json.dumps(tokens));(out/'mode_metadata.json').write_text(json.dumps(meta,indent=2));(out/'errors.json').write_text(json.dumps(errors,indent=2))
 a=pd.DataFrame(rows);summary=[]
 for name,g in a.groupby('mode'):
  clear=g[g.target!='none'];none=g[g.target=='none'];summary.append(dict(mode=name,n=len(g),correct=int(clear.correct.sum()),clear_n=len(clear),banana_correct=int(clear[clear.target=='banana'].correct.sum()),none_correct=int(none.correct.sum()),matches_old=int(g.matches_old.sum())))
 pd.DataFrame(summary).to_csv(out/'summary.csv',index=False)
 manifest=dict(status='COMPLETED' if not errors else 'COMPLETED_WITH_ERRORS',model=MODEL,revision=REV,torch=torch.__version__,cuda=torch.version.cuda,transformers=transformers.__version__,gpu=torch.cuda.get_device_name(0),hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'PLAN.md']},previous_answers_hash=hashlib.sha256((ROOT/'experiments/2026-11/1103_fresh_check/results/answers.csv').read_bytes()).hexdigest(),purpose='Implementation diagnostic on reused data; not a new validation set.',errors=len(errors))
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(pd.DataFrame(summary).to_string(index=False),flush=True);print('INPUT IDS EQUAL',sum(x['ids_equal'] for x in checks),'/42',flush=True);print('INFERENCE AUDIT COMPLETED',flush=True)
if __name__=='__main__':main()
