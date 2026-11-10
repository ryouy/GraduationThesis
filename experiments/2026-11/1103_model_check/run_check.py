from pathlib import Path
import argparse,json,re,hashlib,subprocess,gc,math,time
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
PAIRS={'banana':'apple','elephant':'giraffe','piano':'violin'}
CATS={'banana':'fruit','elephant':'animal','piano':'musical instrument'}
WORDS=list(PAIRS)+list(PAIRS.values())
def build(x,text,task):
    prefix='Context:\n';end=len(prefix)+len(text)
    q=(f'Name the specific {CATS[x]} described in the context. If no specific {CATS[x]} can be identified, answer none.' if task=='naming' else 'What single object, animal, or instrument comes to mind from this context?')
    return prefix+text+'\n\n'+q+' Answer with one name only.',end

def main():
    a=argparse.ArgumentParser();a.add_argument('--size',choices=['0.5B','1.5B'],required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();out=args.out/args.size;out.mkdir(parents=True,exist_ok=True)
    old=json.loads((ROOT/'experiments/2026-10/1019/probe_description_bank_v2.json').read_text());extra=json.loads((ROOT/'experiments/2026-11/1103_validity/heldout_descriptions.json').read_text());held=json.loads((ROOT/'experiments/2026-11/1103_revision/fresh_holdout.json').read_text())
    for x,y in PAIRS.items():
        for k in ['x','y']:
            assert not set(held[x][k]) & set(old[x][k+'_train']+extra[x][k])
            assert all(not re.search(r'\b('+x+'|'+y+r')s?\b',s,re.I) for s in held[x][k])
    import torch,transformers,sklearn
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from huggingface_hub import model_info
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    assert torch.cuda.is_available()
    torch.manual_seed(42);torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    mid=f'Qwen/Qwen2.5-{args.size}-Instruct';rev=model_info(mid).sha
    manifest=dict(status='RUNNING',model=mid,revision=rev,precision='float32',evaluation_reused=True,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),plan_sha256=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest(),source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print('LOAD',mid,rev,flush=True);start=time.time()
    tok=AutoTokenizer.from_pretrained(mid,revision=rev);model=AutoModelForCausalLM.from_pretrained(mid,revision=rev,dtype=torch.float32,attn_implementation='eager').cuda().eval()
    depth=model.config.num_hidden_layers;layers=sorted(set([math.ceil(depth*.5),math.ceil(depth*.75),depth-1,depth]));primary=depth-1;positions=['context_end','assistant_start'];cache={}
    @torch.inference_mode()
    def infer(content,end,generate=False):
        rendered=tok.apply_chat_template([{'role':'user','content':content}],tokenize=False,add_generation_prompt=True)
        b=tok(rendered,return_offsets_mapping=True,return_tensors='pt',add_special_tokens=False);offsets=b.pop('offset_mapping')[0].tolist();char=rendered.index(content)+end-1;pos=[i for i,(lo,hi) in enumerate(offsets) if lo<=char<hi];assert len(pos)==1;pos.append(b.input_ids.shape[1]-1);b=b.to('cuda')
        if content in cache:h=cache[content]
        else:
            r=model(**b,output_hidden_states=True,use_cache=False);h=np.stack([np.stack([r.hidden_states[l][0,p].float().cpu().numpy() for l in layers]) for p in pos]);del r;cache[content]=h
        if not generate:return h
        g=model.generate(**b,max_new_tokens=32,do_sample=False,pad_token_id=tok.eos_token_id)
        ids=g[0,b.input_ids.shape[1]:];return h,tok.decode(ids,skip_special_tokens=True),len(ids),bool(len(ids)==32 and int(ids[-1])!=tok.eos_token_id)
    answers=[];scores=[];aucs=[];null=[];design=[]
    cues=pd.read_csv(ROOT/'experiments/2026-10/1019/results_v2/20261019T133851060426Z/01_stimulus_distances_and_ranks.csv');cues=cues[cues.concept.isin(PAIRS)]
    for x,y in PAIRS.items():
        for task in ['naming','association']:
            print('CHECK',args.size,x,task,flush=True);tr=[];te=[]
            for label,k,word in [(1,'x',x),(0,'y',y)]:
                for i,text in enumerate([word]+old[x][k+'_train']+extra[x][k]):
                    for frame in ['{}','A note says: "{}".']:
                        p,end=build(x,frame.format(text),task);tr.append((infer(p,end),label,f'{label}_{i}'));design.append(dict(concept=x,task=task,label=label,group=f'{label}_{i}',prompt=p))
                for i,text in enumerate(held[x][k]):
                    p,end=build(x,text,task);h,ans,nt,cut=infer(p,end,True);te.append((h,label,text,'phrase' if i<3 else 'sentence'))
                    mentions=[w for w in WORDS if re.search(r'\b'+w+r's?\b',ans,re.I)]
                    answers.append(dict(model=args.size,concept=x,target=word,task=task,split='clear',level='clear',text=text,prompt=p,answer=ans,mentions='|'.join(mentions),correct=mentions==[word],tokens=nt,truncated=cut))
            groups=sorted({r[2] for r in tr});rng=np.random.default_rng(42);maps=[dict(zip(groups,rng.permutation([int(g[0]) for g in groups]))) for _ in range(20)]
            for pi,pos in enumerate(positions):
                for li,layer in enumerate(layers):
                    X=np.stack([r[0][pi,li] for r in tr]);T=np.stack([r[0][pi,li] for r in te]);gt=np.array([r[1] for r in te])
                    def fit(labels):return make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',max_iter=2500,random_state=42)).fit(X,labels)
                    clf=fit([r[1] for r in tr]);pred=clf.decision_function(T);v=float(roc_auc_score(gt,pred));aucs.append(dict(model=args.size,concept=x,task=task,position=pos,layer=layer,primary=pos=='assistant_start' and layer==primary,auc=v))
                    for r,s in zip(te,pred):scores.append(dict(model=args.size,concept=x,task=task,position=pos,layer=layer,description=r[2],label=r[1],style=r[3],score=float(s)))
                    if pos=='assistant_start' and layer==primary:
                        for rep,m in enumerate(maps):null.append(dict(model=args.size,concept=x,task=task,repeat=rep,auc=float(roc_auc_score(gt,fit([m[r[2]] for r in tr]).decision_function(T)))))
            for r in cues[cues.concept==x].itertuples():
                p,end=build(x,r.cue_text,task);_,ans,nt,cut=infer(p,end,True);mentions=[w for w in WORDS if re.search(r'\b'+w+r's?\b',ans,re.I)]
                answers.append(dict(model=args.size,concept=x,target='',task=task,split='cue',level=r.proposed_level,text=r.cue_text,prompt=p,answer=ans,mentions='|'.join(mentions),correct=None,tokens=nt,truncated=cut))
            for name,rows in [('answers',answers),('holdout_scores',scores),('probe_auc',aucs),('shuffled',null),('training_design',design)]:pd.DataFrame(rows).to_csv(out/(name+'.csv'),index=False)
    ans=pd.DataFrame(answers);u=pd.DataFrame(aucs);nu=pd.DataFrame(null);summary=[]
    for task,g in ans[ans.split=='clear'].groupby('task'):
        per=g.groupby('target').correct.sum();pg=u[(u.task==task)&u.primary];thresholds=nu[nu.task==task].groupby('concept').auc.quantile(.95);probe_ok=bool(all(r.auc>=.8 and r.auc>thresholds[r.concept] for r in pg.itertuples()))
        summary.append(dict(model=args.size,task=task,n=len(g),correct=int(g.correct.sum()),min_correct_per_concept=int(per.min()),behavior_pass=bool(g.correct.sum()>=30 and per.min()>=4),min_primary_auc=float(pg.auc.min()),probe_pass=probe_ok))
    pd.DataFrame(summary).to_csv(out/'summary.csv',index=False)
    manifest.update(status='COMPLETED',layers=layers,primary_layer=primary,positions=positions,behavior_contexts=len(ans),seconds=time.time()-start,torch=torch.__version__,transformers=transformers.__version__,sklearn=sklearn.__version__,gpu=torch.cuda.get_device_name(0))
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(pd.DataFrame(summary).to_string(index=False),flush=True);print('CHECK COMPLETED',args.size,flush=True)
if __name__=='__main__':main()
