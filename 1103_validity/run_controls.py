"""Post-pilot diagnostics, added after observing low AUC and copied-noun answers.
Not preregistered confirmation; no stimulus selection by result.
"""
from pathlib import Path
import argparse,json,re
import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from run_pilot import PAIRS,LAYERS,MODEL,REVISION,QUESTION,ROOT,HERE

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);out=p.parse_args().out
out.mkdir(exist_ok=True);torch.set_num_threads(4);torch.manual_seed(42)
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
assert torch.cuda.is_available()
tok=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,use_fast=True)
model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,dtype=torch.float32,attn_implementation='eager').cuda().eval()
@torch.inference_mode()
def read(text):
    rendered=tok.apply_chat_template([{'role':'user','content':text}],tokenize=False,add_generation_prompt=False)
    end=rendered.index('STATE:')+5
    b=tok(rendered,return_tensors='pt',return_offsets_mapping=True,add_special_tokens=False)
    offsets=b.pop('offset_mapping')[0].tolist();ix=[i for i,(lo,hi) in enumerate(offsets) if lo<=end<hi]
    assert len(ix)==1
    h=model(**{k:v.cuda() for k,v in b.items()},output_hidden_states=True,use_cache=False).hidden_states
    return np.stack([h[l][0,ix[0]].float().cpu().numpy() for l in LAYERS])
bank=json.loads((ROOT/'1019/probe_description_bank_v2.json').read_text());held=json.loads((HERE/'heldout_descriptions.json').read_text())
results=[];raw=[]
for x,y in PAIRS.items():
    print('Legacy controlled check:',x,flush=True)
    training=[];tests=[]
    for label,word,k in [(1,x,'x'),(0,y,'y')]:
        for frame in ['The concept is {}.\nSTATE:\n','Focus attention on {}.\nSTATE:\n']:
            training.append((read(frame.format(word)),label))
        for phrase in bank[x][k+'_train']:
            for frame in ['A short definition is {}.\nSTATE:\n','The subject is described as {}.\nSTATE:\n']:
                training.append((read(frame.format(phrase)),label))
        for split,phrases in [('old_holdout',bank[x][k+'_test']),('new_holdout',held[x][k])]:
            for phrase in phrases:
                for fi,frame in enumerate(['A curator wrote about {}.\nSTATE:\n','An observer reported {}.\nSTATE:\n']):
                    tests.append((read(frame.format(phrase)),label,split,phrase,fi))
    assert len(training)==16
    for li,layer in enumerate(LAYERS):
        X=np.stack([e[0][li] for e in training]);labels=[e[1] for e in training]
        clf=make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',random_state=42,max_iter=2500)).fit(X,labels)
        for split in ['old_holdout','new_holdout']:
            q=[e for e in tests if e[2]==split];scores=clf.decision_function(np.stack([e[0][li] for e in q]))
            results.append(dict(concept=x,layer=layer,split=split,n_prompts=len(q),n_unique_descriptions=len(q)//2,auc=float(roc_auc_score([e[1] for e in q],scores))))
            for e,s in zip(q,scores):raw.append(dict(concept=x,layer=layer,split=split,label=e[1],description=e[3],frame=e[4],score=float(s)))
pd.DataFrame(results).to_csv(out/'legacy_transfer_auc.csv',index=False)
pd.DataFrame(raw).to_csv(out/'legacy_transfer_scores.csv',index=False)
# Keep ALL three originally near-labelled cues per concept, both questions.
cues=pd.read_csv(ROOT/'1019/stimuli_v2.csv');cues=cues[cues.concept.isin(PAIRS)&(cues.proposed_level=='near')]
answers=[];category={'banana':'fruit','elephant':'animal','piano':'musical instrument'}
for r in cues.itertuples():
    for mode,q in [('original',QUESTION),('specific_naming',f'Which specific {category[r.concept]} is described? Answer with its specific name, not a part or a broad category.')]:
        content='Read the following context.\nContext:\n'+r.cue_text+'\n'+q
        b=tok.apply_chat_template([{'role':'user','content':content}],add_generation_prompt=True,return_tensors='pt').cuda()
        with torch.inference_mode():g=model.generate(input_ids=b,max_new_tokens=12,do_sample=False,pad_token_id=tok.eos_token_id)
        answer=tok.decode(g[0,b.shape[1]:],skip_special_tokens=True)
        answers.append(dict(concept=r.concept,cue=r.cue_text,question_mode=mode,question=q,answer=answer,target_mention=bool(re.search(r'\b'+r.concept+r's?\b',answer,re.I))))
pd.DataFrame(answers).to_csv(out/'question_controls.csv',index=False)
(out/'controls_manifest.json').write_text(json.dumps({'status':'COMPLETED','post_hoc':True,'purpose':'Disentangle changed probe scaffolding from new holdout text; diagnose ambiguous answer task.','question_contexts':18,'revision':REVISION},indent=2)+'\n')
print(pd.DataFrame(results).to_string(index=False));print(pd.DataFrame(answers).groupby('question_mode').target_mention.agg(['sum','count']).to_string());print('CONTROLS COMPLETED',flush=True)
