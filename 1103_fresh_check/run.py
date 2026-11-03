from pathlib import Path
import sys,json,re,argparse,hashlib,subprocess
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'1103_model_check'))
from run_check import build,PAIRS
RULES=json.loads((HERE/'rules.json').read_text())
def grade(answer,target):
    found=[w for w,aliases in RULES['aliases'].items() if any(re.search(r'\b'+re.escape(a)+r'\b',answer,re.I) for a in aliases)]
    negated=bool(re.search(r'\b(not|neither|isn.t|aren.t)\b',answer,re.I))
    none=answer.strip().lower().strip('.! "\'') in RULES['none_answers']
    return dict(found='|'.join(found),negated=negated,correct=(none if target=='none' else found==[target] and not negated))
def validate():
    items=json.loads((HERE/'items.json').read_text());previous=[]
    for p in [ROOT/'1103_validity/heldout_descriptions.json',ROOT/'1103_revision/fresh_holdout.json',ROOT/'1019/probe_description_bank_v2.json']:
        def walk(o):
            if isinstance(o,str):previous.append(o.strip().lower())
            elif isinstance(o,dict):
                for v in o.values():walk(v)
            elif isinstance(o,list):
                for v in o:walk(v)
        walk(json.loads(p.read_text()))
    for p in [ROOT/'1103_model_check/results/1.5B/answers.csv',ROOT/'1103_model_check/results/1.5B/posthoc_sanity.csv']:
        d=pd.read_csv(p,keep_default_na=False)
        previous+=d['text' if 'text' in d else 'prompt'].str.lower().tolist()
    alltexts=[]
    for word in RULES['aliases']:
        assert len(items[word])==6
    for key,texts in items.items():
        for text in texts:
            assert text.lower().strip() not in previous
            assert not any(re.search(r'\b'+re.escape(alias)+r'\b',text,re.I) for vs in RULES['aliases'].values() for alias in vs)
            alltexts.append(text)
    assert len(alltexts)==42 and len(set(alltexts))==42
    return items

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--dry-run',action='store_true');args=ap.parse_args();items=validate()
    if args.dry_run:print('PASS: 36 new descriptions + 6 none controls; no exact reuse or direct concept/alias leakage.');return
    out=args.out;out.mkdir(exist_ok=True,parents=True)
    import torch,transformers,sklearn
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    mid='Qwen/Qwen2.5-1.5B-Instruct';rev='989aa7980e4cf806f80c7fef2b1adb7bc71aa306';layers=[14,21,27,28];positions=['context_end','assistant_start']
    assert torch.cuda.is_available();torch.set_num_threads(4);torch.manual_seed(42);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    tok=AutoTokenizer.from_pretrained(mid,revision=rev);model=AutoModelForCausalLM.from_pretrained(mid,revision=rev,dtype=torch.float32,attn_implementation='eager').cuda().eval()
    @torch.inference_mode()
    def infer(p,end,generate=False):
        rendered=tok.apply_chat_template([{'role':'user','content':p}],tokenize=False,add_generation_prompt=True);b=tok(rendered,return_tensors='pt',return_offsets_mapping=True,add_special_tokens=False);offset=b.pop('offset_mapping')[0].tolist();char=rendered.index(p)+end-1;pos=[i for i,(lo,hi) in enumerate(offset) if lo<=char<hi];assert len(pos)==1;pos.append(b.input_ids.shape[1]-1);b=b.to('cuda')
        r=model(**b,output_hidden_states=True,use_cache=False);h=np.stack([np.stack([r.hidden_states[l][0,j].float().cpu().numpy() for l in layers]) for j in pos]);del r
        if not generate:return h
        g=model.generate(**b,do_sample=False,max_new_tokens=32,pad_token_id=tok.eos_token_id);ids=g[0,b.input_ids.shape[1]:];return h,tok.decode(ids,skip_special_tokens=True),len(ids),len(ids)==32 and int(ids[-1])!=tok.eos_token_id
    train=pd.read_csv(ROOT/'1103_model_check/results/1.5B/training_design.csv');train=train[train.task=='naming'].copy();assert len(train)==192
    train.to_csv(out/'training_design.csv',index=False)
    answers=[];scores=[];aucs=[];null=[]
    for x,y in PAIRS.items():
        print('PAIR',x,y,flush=True);tr=[];te=[]
        for r in train[train.concept==x].itertuples():
            # End of context precedes the unchanged question, including quoted frame.
            end=r.prompt.index('\n\nName the specific')
            tr.append((infer(r.prompt,end),r.label,r.group))
        for label,word in [(1,x),(0,y)]:
            for i,text in enumerate(items[word]):
                p,end=build(x,text,'naming');h,answer,nt,cut=infer(p,end,True);te.append((h,label,text));answers.append(dict(item_id=f'{word}_{i}',pair=x,target=word,text=text,prompt=p,answer=answer,tokens=nt,truncated=cut,**grade(answer,word)))
        groups=sorted({r[2] for r in tr});rng=np.random.default_rng(42);maps=[dict(zip(groups,rng.permutation([int(g[0]) for g in groups]))) for _ in range(20)]
        for pi,pos in enumerate(positions):
            for li,layer in enumerate(layers):
                X=np.stack([r[0][pi,li] for r in tr]);T=np.stack([r[0][pi,li] for r in te]);gt=[r[1] for r in te]
                def fit(labels):return make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',max_iter=2500,random_state=42)).fit(X,labels)
                pred=fit([r[1] for r in tr]).decision_function(T);aucs.append(dict(pair=x,position=pos,layer=layer,auc=float(roc_auc_score(gt,pred))))
                for r,s in zip(te,pred):scores.append(dict(pair=x,position=pos,layer=layer,label=r[1],text=r[2],score=float(s)))
                if pos=='assistant_start' and layer==27:
                    for rep,m in enumerate(maps):null.append(dict(pair=x,repeat=rep,auc=float(roc_auc_score(gt,fit([m[r[2]] for r in tr]).decision_function(T)))))
        pd.DataFrame(answers).to_csv(out/'answers.csv',index=False)
    for key,x in [('none_fruit','banana'),('none_animal','elephant'),('none_instrument','piano')]:
        for i,text in enumerate(items[key]):
            p,end=build(x,text,'naming');_,answer,nt,cut=infer(p,end,True);answers.append(dict(item_id=f'{key}_{i}',pair=x,target='none',text=text,prompt=p,answer=answer,tokens=nt,truncated=cut,**grade(answer,'none')))
    for name,rows in [('answers',answers),('holdout_scores',scores),('probe_auc',aucs),('shuffled',null)]:pd.DataFrame(rows).to_csv(out/(name+'.csv'),index=False)
    a=pd.DataFrame(answers);summary=a.groupby('target',as_index=False).correct.agg(['sum','count']).reset_index();summary.to_csv(out/'behavior_summary.csv',index=False)
    clear=a[a.target!='none'];none=a[a.target=='none'];primary=pd.DataFrame(aucs).query('position=="assistant_start" and layer==27');thresholds=pd.DataFrame(null).groupby('pair').auc.quantile(.95)
    manifest=dict(status='COMPLETED',model=mid,revision=rev,layers=layers,position=positions,contexts=len(a),behavior_correct=int(clear.correct.sum()),behavior_n=36,behavior_pass=bool(clear.correct.sum()>=30 and clear.groupby('target').correct.sum().min()>=4),none_correct=int(none.correct.sum()),none_pass=bool(none.correct.sum()>=5),probe_pass=bool(all(r.auc>=.8 and r.auc>thresholds[r.pair] for r in primary.itertuples())),source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'PLAN.md',HERE/'items.json',HERE/'rules.json']},training_hash=hashlib.sha256((ROOT/'1103_model_check/results/1.5B/training_design.csv').read_bytes()).hexdigest(),torch=torch.__version__,transformers=transformers.__version__,sklearn=sklearn.__version__,gpu=torch.cuda.get_device_name(0))
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(summary.to_string(index=False),flush=True);print(primary.to_string(index=False),flush=True);print(json.dumps(manifest),flush=True);print('FRESH CHECK COMPLETED',flush=True)
if __name__=='__main__':main()
