"""Prespecified diagnostic revision. See PLAN.md before interpreting results."""
from pathlib import Path
import json,re,argparse,hashlib,subprocess
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
PAIRS={'banana':'apple','elephant':'giraffe','piano':'violin'}
CATS={'banana':'fruit','elephant':'animal','piano':'musical instrument'}
MODEL='Qwen/Qwen2.5-0.5B-Instruct';REV='7ae557604adf67be50417f59c2c2f167def9a775'
EMB='sentence-transformers/all-MiniLM-L6-v2';EREV='1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
def prompt(x,text,mode='free'):
    head=f'Identify the specific {CATS[x]} from this description.'
    if mode!='free':
        words=[x,PAIRS[x]] if mode=='xy' else [PAIRS[x],x]
        head+=' Choose one of: '+', '.join(words)+'.'
    return head+'\nDescription: '+text+'\nAnswer with the specific name only.'
def banks():
    old=json.loads((ROOT/'1019/probe_description_bank_v2.json').read_text())
    extra=json.loads((ROOT/'1103_validity/heldout_descriptions.json').read_text())
    fresh=json.loads((HERE/'fresh_holdout.json').read_text())
    for x,y in PAIRS.items():
        for k,word in [('x',x),('y',y)]:
            assert len(fresh[x][k])==6
            assert not set(fresh[x][k]) & set(old[x][k+'_train']+old[x][k+'_test']+extra[x][k])
            assert all(not re.search(r'\b('+x+'|'+y+r')s?\b',s,re.I) for s in fresh[x][k])
    return old,extra,fresh
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out;out.mkdir(parents=True,exist_ok=True)
    old,extra,fresh=banks()
    import torch,transformers,sklearn
    from transformers import AutoTokenizer,AutoModelForCausalLM,AutoModel
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from scipy.stats import spearmanr
    assert torch.cuda.is_available()
    torch.manual_seed(42);np.random.seed(42);torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    tok=AutoTokenizer.from_pretrained(MODEL,revision=REV)
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REV,dtype=torch.float32,attn_implementation='eager').cuda().eval()
    layers=[22,23,24]
    @torch.inference_mode()
    def infer(content,generate=False,x=None):
        rendered=tok.apply_chat_template([{'role':'user','content':content}],tokenize=False,add_generation_prompt=True)
        batch=tok(rendered,return_tensors='pt',add_special_tokens=False).to('cuda')
        r=model(**batch,output_hidden_states=True,use_cache=False)
        h=np.stack([r.hidden_states[l][0,-1].float().cpu().numpy() for l in layers])
        if not generate:return h
        del r
        scores=[]
        for word in [x,PAIRS[x]]:
            ids=tok(word,add_special_tokens=False).input_ids;n=batch.input_ids.shape[1]
            full=torch.cat([batch.input_ids,torch.tensor([ids],device='cuda')],1)
            logits=model(input_ids=full,attention_mask=torch.ones_like(full),use_cache=False).logits[0,n-1:-1].float().log_softmax(-1)
            scores.append(float(logits[torch.arange(len(ids),device='cuda'),torch.tensor(ids,device='cuda')].sum()))
        g=model.generate(**batch,do_sample=False,max_new_tokens=24,pad_token_id=tok.eos_token_id)
        answer=tok.decode(g[0,batch.input_ids.shape[1]:],skip_special_tokens=True)
        return h,answer,scores
    scores=[];aucs=[];training=[]
    for x,y in PAIRS.items():
        print('PROBE',x,flush=True)
        train=[];test=[]
        for label,k,word in [(1,'x',x),(0,'y',y)]:
            for i,text in enumerate([word]+old[x][k+'_train']+extra[x][k]):
                for frame in ['{}','A note says: "{}".']:
                    p=prompt(x,frame.format(text));train.append((infer(p),label,i<4))
                    training.append(dict(concept=x,label=label,description=text,frame=frame,in_baseline=i<4,prompt=p))
            for i,text in enumerate(fresh[x][k]):
                test.append((infer(prompt(x,text)),label,text,'phrase' if i<3 else 'sentence'))
        for mode in ['baseline','expanded']:
            tr=[r for r in train if mode=='expanded' or r[2]]
            for li,layer in enumerate(layers):
                clf=make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',max_iter=2500,random_state=42))
                clf.fit(np.stack([r[0][li] for r in tr]),[r[1] for r in tr])
                pred=clf.decision_function(np.stack([r[0][li] for r in test]))
                for r,s in zip(test,pred):scores.append(dict(concept=x,training=mode,layer=layer,label=r[1],description=r[2],style=r[3],score=float(s)))
                for style in ['all','phrase','sentence']:
                    ids=[i for i,r in enumerate(test) if style=='all' or r[3]==style]
                    aucs.append(dict(concept=x,training=mode,layer=layer,style=style,n=len(ids),auc=float(roc_auc_score([test[i][1] for i in ids],pred[ids]))))
    pd.DataFrame(scores).to_csv(out/'holdout_scores.csv',index=False);pd.DataFrame(aucs).to_csv(out/'probe_auc.csv',index=False);pd.DataFrame(training).to_csv(out/'training_design.csv',index=False)
    cues=pd.read_csv(ROOT/'1019/results_v2/20261019T133851060426Z/01_stimulus_distances_and_ranks.csv');cues=cues[cues.concept.isin(PAIRS)].copy()
    answers=[]
    for r in cues.itertuples():
        print('BEHAVIOR',r.concept,r.proposed_level,flush=True)
        for mode in ['free','xy','yx']:
            p=prompt(r.concept,r.cue_text,mode);_,answer,lp=infer(p,True,r.concept)
            mx=bool(re.search(r'\b'+r.concept+r's?\b',answer,re.I));my=bool(re.search(r'\b'+PAIRS[r.concept]+r's?\b',answer,re.I))
            choice='X' if mx and not my else 'Y' if my and not mx else 'ambiguous' if mx and my else 'other'
            answers.append(dict(concept=r.concept,comparison=PAIRS[r.concept],cue=r.cue_text,level=r.proposed_level,mode=mode,prompt=p,answer=answer,target_mention=mx,choice=choice,logp_X=lp[0],logp_Y=lp[1],margin=lp[0]-lp[1]))
        pd.DataFrame(answers).to_csv(out/'answers.csv',index=False)
    del model;torch.cuda.empty_cache()
    etok=AutoTokenizer.from_pretrained(EMB,revision=EREV);emodel=AutoModel.from_pretrained(EMB,revision=EREV).cuda().eval()
    @torch.inference_mode()
    def embed(texts):
        b=etok(texts,padding=True,truncation=True,max_length=256,return_tensors='pt').to('cuda');h=emodel(**b).last_hidden_state;m=b.attention_mask.unsqueeze(-1)
        z=(h*m).sum(1)/m.sum(1);return torch.nn.functional.normalize(z,p=2,dim=1).cpu().numpy()
    distances=[];corr=[]
    for x,y in PAIRS.items():
        sub=cues[cues.concept==x];texts=sub.cue_text.tolist();z=embed([x,y]+texts);sx=z[2:]@z[0];sy=z[2:]@z[1]
        for text,vx,vy in zip(texts,sx,sy):distances.append(dict(concept=x,cue=text,simX=float(vx),simY=float(vy),dX=float(1-vx),dY=float(1-vy),sim_margin=float(vx-vy)))
    d=pd.DataFrame(distances);d.to_csv(out/'distances_XY.csv',index=False)
    ans=pd.DataFrame(answers);joined=ans[ans['mode']=='free'].merge(d,on=['concept','cue'],validate='one_to_one')
    for x,g in joined.groupby('concept'):
        for v,w in [('simX','margin'),('sim_margin','margin'),('simX','simY'),('simX','logp_X'),('simY','logp_Y')]:
            corr.append(dict(concept=x,predictor=v,outcome=w,n=len(g),rho=float(spearmanr(g[v],g[w]).statistic)))
    pd.DataFrame(corr).to_csv(out/'distance_correlations.csv',index=False)
    manifest=dict(status='COMPLETED',model=MODEL,revision=REV,embedding=EMB,embedding_revision=EREV,behavior_contexts=len(ans),fresh_descriptions=36,layers=layers,torch=torch.__version__,transformers=transformers.__version__,sklearn=sklearn.__version__,source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'PLAN.md',HERE/'fresh_holdout.json']})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('REVISION COMPLETED',flush=True)
    print(pd.DataFrame(aucs).query('style=="all" and layer<24').groupby(['concept','training']).auc.mean().unstack().round(3).to_string(),flush=True)
    print(ans[ans.level=='near'].groupby('mode').target_mention.agg(['sum','count']).to_string(),flush=True)
    print(pd.DataFrame(corr).to_string(index=False),flush=True)
if __name__=='__main__':main()
