"""Three-pair, prespecified measurement-validity pilot. No hypothesis fishing."""
from pathlib import Path
import argparse,json,re,hashlib,sys,itertools
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
PAIRS={'banana':'apple','elephant':'giraffe','piano':'violin'}
LAYERS=[22,23,24]
FORMATS=['markers','natural']
POSITIONS=['context_end','assistant_start']
CONDITIONS=['cue_only','neutral','suppression']
MODEL='Qwen/Qwen2.5-0.5B-Instruct'
REVISION='7ae557604adf67be50417f59c2c2f167def9a775'
QUESTION='What single object, animal, or instrument is most associated with this context? Answer with one lowercase English noun.'

def build(fmt,condition,target,text):
    intro={'cue_only':'Read the following context.',
           'neutral':f'You may think about {target}. Read the following context.',
           'suppression':f'Do not think about {target}. Read the following context.'}[condition]
    prefix=intro+ ('\nSTATE:\n' if fmt=='markers' else '\nContext:\n')
    content=prefix+text+ ('\nSTATE:\n' if fmt=='markers' else '\n')+QUESTION
    end=len(prefix)+len(text)
    if fmt=='markers':end=content.rindex('STATE:')+len('STATE:')
    return content,end

def inputs():
    cues=pd.read_csv(ROOT/'1019/results_v2/20261019T133851060426Z/01_stimulus_distances_and_ranks.csv')
    cues=cues[cues.concept.isin(PAIRS)].copy()
    rows=[]
    for c in cues.itertuples():
        for fmt,cond in itertools.product(FORMATS,CONDITIONS):
            content,end=build(fmt,cond,c.concept,c.cue_text)
            rows.append(dict(concept=c.concept,comparison=PAIRS[c.concept],cue=c.cue_text,
                             proposed_level=c.proposed_level,distance=c.semantic_distance,
                             format=fmt,condition=cond,content=content,context_end_char=end))
    d=pd.DataFrame(rows).reset_index(names='input_id')
    assert len(d)==216 and not d.duplicated(['concept','cue','format','condition']).any()
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--dry-run',action='store_true');args=ap.parse_args()
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    design=inputs();design.to_csv(out/'design.csv',index=False)
    bank=json.loads((ROOT/'1019/probe_description_bank_v2.json').read_text())
    held=json.loads((HERE/'heldout_descriptions.json').read_text())
    for x,y in PAIRS.items():
        for label in ['x','y']:
            assert len(held[x][label])==12
            for text in held[x][label]:
                assert not any(re.search(r'\b'+word+r'\b',text,re.I) for word in [x,y])
                assert text not in bank[x][label+'_train']
    manifest={'status':'PLANNED','contexts':216,'concept_pairs':PAIRS,'layers':LAYERS,
              'model':MODEL,'revision':REVISION,'heldout_descriptions_per_class':12,
              'decision_rules':'See PLAN.md. Diagnostic pilot, not confirmatory inference.'}
    if args.dry_run:
        print(json.dumps(manifest));return
    import torch,transformers,sklearn
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from scipy.stats import spearmanr
    assert torch.cuda.is_available(),'T4 GPU is required for this run.'
    torch.manual_seed(42);np.random.seed(42);torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    tok=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,use_fast=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,dtype=torch.float32,attn_implementation='eager').cuda().eval()
    cache=out/'features';cache.mkdir(exist_ok=True)
    @torch.inference_mode()
    def features(content,end):
        rendered=tok.apply_chat_template([{'role':'user','content':content}],tokenize=False,add_generation_prompt=True)
        start=rendered.index(content);char=start+end-1
        batch=tok(rendered,return_tensors='pt',return_offsets_mapping=True,add_special_tokens=False)
        offsets=batch.pop('offset_mapping')[0].tolist()
        matches=[i for i,(lo,hi) in enumerate(offsets) if lo<=char<hi]
        assert len(matches)==1
        positions=[matches[0],batch.input_ids.shape[1]-1]
        key=hashlib.sha256((rendered+str(positions)).encode()).hexdigest();file=cache/(key+'.npz')
        if file.exists():
            with np.load(file) as z:states=z['states']
        else:
            result=model(**{k:v.cuda() for k,v in batch.items()},output_hidden_states=True,use_cache=False)
            states=np.stack([np.stack([result.hidden_states[l][0,p].float().cpu().numpy() for l in LAYERS]) for p in positions])
            assert np.isfinite(states).all();np.savez_compressed(file,states=states)
        return states,batch,positions
    @torch.inference_mode()
    def word_score(batch,word):
        # Probability of the entire fixed lowercase candidate token sequence.
        ids=tok(word,add_special_tokens=False).input_ids
        prefix=batch.input_ids.cuda();full=torch.cat([prefix,torch.tensor([ids],device='cuda')],dim=1)
        logits=model(input_ids=full,use_cache=False).logits[0]
        logp=torch.log_softmax(logits[prefix.shape[1]-1:-1].float(),dim=-1)
        return float(logp[torch.arange(len(ids),device='cuda'),torch.tensor(ids,device='cuda')].sum()),len(ids)
    probes={};validation=[];shuffles=[];holdout_scores=[]
    for x,y in PAIRS.items():
        for fmt in FORMATS:
            print('Probe:',x,fmt,flush=True)
            train=[];test=[]
            for label,word,k in [(1,x,'x'),(0,y,'y')]:
                phrases=[word]+bank[x][k+'_train']
                for group,phrase in enumerate(phrases):
                    for frame in ['The subject is {}.','A description is {}.']:
                        content,end=build(fmt,'cue_only',x,frame.format(phrase));h,_,_=features(content,end)
                        train.append((h,label,f'{label}_{group}'))
                for idx,phrase in enumerate(held[x][k]):
                    content,end=build(fmt,'cue_only',x,phrase);h,_,_=features(content,end)
                    test.append((h,label,idx,phrase))
            assert len(train)==16 and len(test)==24
            groups=sorted({e[2] for e in train});rng=np.random.default_rng(20261103)
            permutations=[dict(zip(groups,rng.permutation([int(g[0]) for g in groups]))) for _ in range(20)]
            for pi,pos in enumerate(POSITIONS):
                for li,layer in enumerate(LAYERS):
                    X=np.stack([e[0][pi,li] for e in train]);labels=np.array([e[1] for e in train])
                    T=np.stack([e[0][pi,li] for e in test]);gt=np.array([e[1] for e in test])
                    def fit(labels):
                        return make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',max_iter=2500,random_state=42)).fit(X,labels)
                    clf=fit(labels);sd=max(float(np.std(clf.decision_function(X),ddof=1)),1e-8)
                    scores=clf.decision_function(T);auc=float(roc_auc_score(gt,scores))
                    probes[x,fmt,pos,layer]=(clf,sd)
                    validation.append(dict(concept=x,format=fmt,position=pos,layer=layer,n_unique_descriptions=24,auc=auc,pass_080=auc>=.8))
                    for item,score in zip(test,scores):
                        holdout_scores.append(dict(concept=x,format=fmt,position=pos,layer=layer,label=item[1],description=item[3],score=float(score)))
                    for repeat,mapping in enumerate(permutations):
                        shuffled=fit(np.array([mapping[e[2]] for e in train]))
                        shuffles.append(dict(concept=x,format=fmt,position=pos,layer=layer,repeat=repeat,auc=float(roc_auc_score(gt,shuffled.decision_function(T)))))
    pd.DataFrame(validation).to_csv(out/'probe_validation.csv',index=False)
    pd.DataFrame(holdout_scores).to_csv(out/'holdout_scores.csv',index=False)
    pd.DataFrame(shuffles).to_csv(out/'shuffled_controls.csv',index=False)
    rows=[];answers=[]
    for i,r in enumerate(design.itertuples()):
        if i%24==0:print('Contexts:',i,'/',len(design),flush=True)
        h,batch,positions=features(r.content,r.context_end_char)
        sx,nx=word_score(batch,r.concept);sy,ny=word_score(batch,r.comparison)
        with torch.inference_mode():
            generated=model.generate(**{k:v.cuda() for k,v in batch.items()},max_new_tokens=12,do_sample=False,pad_token_id=tok.eos_token_id)
        answer=tok.decode(generated[0,batch.input_ids.shape[1]:],skip_special_tokens=True)
        mention=bool(re.search(r'\b'+r.concept+r's?\b',answer,re.I))
        answers.append(dict(input_id=r.input_id,answer=answer,target_mention=mention,logp_X=sx,logp_Y=sy,candidate_margin=sx-sy,X_tokens=nx,Y_tokens=ny))
        for pi,pos in enumerate(POSITIONS):
            for li,layer in enumerate(LAYERS):
                clf,sd=probes[r.concept,r.format,pos,layer]
                rows.append(dict(input_id=r.input_id,position=pos,layer=layer,score=float(clf.decision_function(h[pi,li][None])[0]/sd),token_position=int(positions[pi])))
        if i%24==0:
            pd.DataFrame(answers).to_csv(out/'answers.csv',index=False)
            pd.DataFrame(rows).to_csv(out/'readouts.csv',index=False)
    answers=pd.DataFrame(answers);rows=pd.DataFrame(rows)
    assert len(answers)==216 and len(rows)==216*2*3
    answers.to_csv(out/'answers.csv',index=False);rows.to_csv(out/'readouts.csv',index=False)
    a=answers.merge(design,on='input_id',validate='one_to_one')
    corr=[]
    for (x,fmt),g in a[a.condition=='cue_only'].groupby(['concept','format']):
        corr.append(dict(concept=x,format=fmt,metric='candidate_margin',layer=0,n_cues=len(g),rho=float(spearmanr(g.distance,g.candidate_margin).statistic)))
    q=rows.merge(design,on='input_id',validate='many_to_one')
    for keys,g in q[q.condition=='cue_only'].groupby(['concept','format','position','layer']):
        corr.append(dict(concept=keys[0],format=keys[1],metric=keys[2],layer=int(keys[3]),n_cues=len(g),rho=float(spearmanr(g.distance,g.score).statistic)))
    pd.DataFrame(corr).to_csv(out/'distance_correlations.csv',index=False)
    w=q.pivot(index=['concept','format','position','layer','cue','proposed_level','distance'],columns='condition',values='score').reset_index()
    w['suppression_minus_neutral']=w.suppression-w.neutral
    w.to_csv(out/'paired_scores.csv',index=False)
    summary=w.groupby(['concept','format','position','layer'],as_index=False).suppression_minus_neutral.mean()
    summary.to_csv(out/'position_effects.csv',index=False)
    a.groupby(['concept','format','condition','proposed_level'],as_index=False).agg(n=('target_mention','size'),target_mentions=('target_mention','sum'),mean_margin=('candidate_margin','mean')).to_csv(out/'behavior_summary.csv',index=False)
    manifest.update(status='COMPLETED',torch=torch.__version__,transformers=transformers.__version__,sklearn=sklearn.__version__,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),plan_sha256=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest(),
        heldout_sha256=hashlib.sha256((HERE/'heldout_descriptions.json').read_bytes()).hexdigest(),
        caveats=['Three purposively chosen concept pairs; no population-level significance claim.','Probe score differences across positions use separate fitted probes.','Lowercase candidate token-sequence log probabilities are not concept-activation probabilities.','Greedy output counts summarize different cues, not repeated random trials.'])
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETED',out,flush=True)

if __name__=='__main__':main()
