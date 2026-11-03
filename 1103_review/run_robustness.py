"""Unexecuted model-inference follow-up; use the accompanying Colab notebook.

4,608 experimental contexts, 20 probe training variants, all 24 layers.
No automatic publishing. Raw features retained for reanalysis and interrupted runs.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import platform
import re
import subprocess
import time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
LAYERS=list(range(1,25))
FOCUS=[22,23]
MODEL='Qwen/Qwen2.5-0.5B-Instruct'
ENCODER='sentence-transformers/all-MiniLM-L6-v2'
INSTRUCTIONS=[
    ('You may think about {target}. Continue reading.', 'Do not think about {target}. Continue reading.'),
    ('You may focus on {target}. Continue reading.', 'Do not focus on {target}. Continue reading.'),
    ('You may consider {target}. Continue reading.', 'Do not consider {target}. Continue reading.'),
]
CONTEXTS=['{cue}', 'Context: {cue}']


def prompt(target,condition,cue,instruction_frame,context_frame):
    instruction=INSTRUCTIONS[instruction_frame][int(condition=='suppression')].format(target=target)
    return instruction+'\nSTATE:\n'+CONTEXTS[context_frame].format(cue=cue)+'\nSTATE:\n'


def make_design():
    old=pd.read_csv(ROOT/'1019/specificity_cues_v3.csv').assign(cue_source='original')
    new=pd.read_csv(HERE/'additional_cues.csv').assign(cue_source='new_authored')
    cues=pd.concat([old,new],ignore_index=True)
    rows=[]
    for family,bank,comparison in [
        ('v2',pd.read_csv(ROOT/'1019/stimuli_v2.csv'),'replacement'),
        ('v3',cues,'comparison')]:
        for i,c in bank.iterrows():
            for role in (['X'] if family=='v2' else ['X','Y']):
                target=c.concept if role=='X' else c[comparison]
                for frame,context,cond in itertools.product(range(3),range(2),['neutral','suppression']):
                    text=prompt(target,cond,c.cue_text,frame,context)
                    row=dict(family=family,concept=c.concept,comparison=c[comparison],
                        target_role=role,condition=cond,cue_id=f'{family}_{i:03}',
                        cue_text=c.cue_text,instruction_frame=frame,context_frame=context,
                        prompt=text,feature_key=hashlib.sha256(text.encode()).hexdigest())
                    if family=='v3':
                        row.update(triplet=int(c.triplet),cue_type=c.cue_type,
                            cue_source=c.cue_source,
                            cue_role='target' if c.cue_type==role else
                                     'unrelated' if c.cue_type=='unrelated' else 'other')
                    else:
                        row.update(cue_source='original',proposed_level=c.proposed_level)
                    rows.append(row)
    design=pd.DataFrame(rows)
    assert len(design)==4608 and design.groupby('family').size().to_dict()=={'v2':1152,'v3':3456}
    assert not design.duplicated(['family','concept','target_role','condition','cue_id',
                                  'instruction_frame','context_frame']).any()
    for c in cues.itertuples():
        assert not any(re.search(r'\b'+re.escape(w)+r'\b',c.cue_text,re.I)
                       for w in [c.concept,c.comparison])
    return design


def probe_plan():
    # 1 original fit, 9 grouped leave-one-description-per-class-out fits,
    # 9 analogous fits excluding named examples, 1 full description-only fit.
    plan=[dict(name='original',omit_x=None,omit_y=None,names=True)]
    for names in [True,False]:
        for ix,iy in itertools.product(range(3),repeat=2):
            plan.append(dict(name=f'names_{int(names)}_omit_{ix}_{iy}',
                             omit_x=ix,omit_y=iy,names=names))
    plan.append(dict(name='description_only',omit_x=None,omit_y=None,names=False))
    assert len(plan)==20
    return plan


def analyze(measurements,design,out):
    from audit_saved_results import summarize as full_summary
    def summarize(values):
        return full_summary(values, n_boot=5000)
    data=measurements.merge(design.drop(columns=['prompt']),on='design_row',validate='many_to_one')
    validation=pd.read_csv(out/'probe_validation.csv')
    # v3 contrasts within each instruction/context/target role; no pseudoreplication.
    v=data[data.family=='v3']
    keys=['probe_variant','concept','target_role','triplet','cue_source',
          'instruction_frame','context_frame','layer']
    p=v.pivot(index=keys,columns=['condition','cue_role'],values='delta_target_std')
    contrast=p.index.to_frame(index=False)
    for c in ['neutral','suppression']:
        contrast[c+'_specificity']=(p[(c,'target')]-p[(c,'other')]).to_numpy()
    contrast['interaction']=contrast.suppression_specificity-contrast.neutral_specificity
    contrast.to_csv(out/'v3_all_contrasts.csv',index=False)
    # Each frame, target role, and original/new cue set is reported separately.
    results=[]
    for group,g in contrast[contrast.layer.isin(FOCUS)].groupby(
            ['probe_variant','target_role','cue_source','instruction_frame','context_frame']):
        bypair=g.groupby('concept').interaction.mean()
        results.append(dict(zip(['probe_variant','target_role','cue_source',
                                  'instruction_frame','context_frame'],group),
                            **summarize(bypair)))
    pd.DataFrame(results).to_csv(out/'v3_focus_sensitivity.csv',index=False)
    # v2 continuous-distance analyses using independently computed MiniLM distances.
    v=data[data.family=='v2']
    keys=['probe_variant','concept','cue_id','instruction_frame','context_frame','layer']
    p=v.pivot(index=keys,columns='condition',values='delta_target_std')
    p['interaction']=p.suppression-p.neutral
    contrasts=p[['interaction']].reset_index().merge(
        design[design.family=='v2'][['concept','cue_id','semantic_distance','cue_token_count']].drop_duplicates(),
        on=['concept','cue_id'],validate='many_to_one')
    trends=[]
    for keys,g in contrasts.groupby(['probe_variant','concept','instruction_frame','context_frame','layer']):
        d=g.semantic_distance.to_numpy();n=g.cue_token_count.to_numpy();y=g.interaction.to_numpy()
        d=d-d.mean();n=n-n.mean();y=y-y.mean()
        matrix=np.c_[d,n]
        trends.append(dict(zip(['probe_variant','concept','instruction_frame','context_frame','layer'],keys),
            slope_simple=float(d@y/(d@d)),
            slope_length_adjusted=float(np.linalg.lstsq(matrix,y,rcond=None)[0][0]),
            design_rank=int(np.linalg.matrix_rank(matrix))))
    trends=pd.DataFrame(trends)
    trends.to_csv(out/'v2_all_distance_slopes.csv',index=False)
    summaries=[]
    for keys,g in trends.groupby(['probe_variant','instruction_frame','context_frame','layer']):
        for metric in ['slope_simple','slope_length_adjusted']:
            summaries.append(dict(zip(['probe_variant','instruction_frame','context_frame','layer'],keys),
                                   metric=metric,**summarize(g[metric])))
    pd.DataFrame(summaries).to_csv(out/'v2_distance_sensitivity.csv',index=False)
    # No holdout-AUC-based pair exclusion in primary summaries. Report coverage separately.
    validation.groupby(['probe_variant','layer']).auc.agg(['mean','min']).to_csv(out/'probe_coverage.csv')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--out',type=Path,default=HERE/'robustness_run')
    parser.add_argument('--model-revision',default='main')
    parser.add_argument('--encoder-revision',default='main')
    args=parser.parse_args()
    design=make_design().reset_index(names='design_row')
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    manifest=dict(status='DESIGN_ONLY_NOT_EXECUTED',contexts=len(design),
        unique_prompts=int(design.feature_key.nunique()),probe_variants=len(probe_plan()),
        n_concept_pairs=8,focus_layers=FOCUS,
        limitation='Repeated frames/probe fits are sensitivity variants, not independent participants or concepts.',
        new_cues_note='72 newly authored sentences; not human validated or length matched yet.')
    if args.dry_run:
        design.to_csv(out/'planned_design.csv',index=False)
        (out/'planned_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(json.dumps(manifest,indent=2));return
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
    from huggingface_hub import HfApi
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    import transformers, sklearn
    device='cuda' if torch.cuda.is_available() else 'cpu'
    dtype=torch.float32  # avoid old fp16 readout sensitivity; report numerical differences
    torch.manual_seed(42);np.random.seed(42)
    torch.set_num_threads(min(4,torch.get_num_threads()))
    if device=='cuda':
        torch.backends.cuda.matmul.allow_tf32=False
        torch.backends.cudnn.allow_tf32=False
    api=HfApi()
    model_sha=api.model_info(MODEL,revision=args.model_revision).sha
    encoder_sha=api.model_info(ENCODER,revision=args.encoder_revision).sha
    identity=dict(model=MODEL,model_sha=model_sha,encoder=ENCODER,encoder_sha=encoder_sha,
        dtype=str(dtype),device=device,torch=torch.__version__,transformers=transformers.__version__,
        extraction_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    identity_file=out/'cache_identity.json'
    if identity_file.exists():
        assert json.loads(identity_file.read_text())==identity, 'Use a fresh --out for another runtime/model revision.'
    identity_file.write_text(json.dumps(identity,indent=2)+'\n')
    (out/'run_started.json').write_text(json.dumps({**manifest,**identity,'status':'STARTED_NOT_COMPLETED'},indent=2)+'\n')
    tok=AutoTokenizer.from_pretrained(MODEL,revision=model_sha,use_fast=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=model_sha,
        torch_dtype=dtype,attn_implementation='eager').to(device).eval()
    assert tok.is_fast and model.config.num_hidden_layers==24
    cache=out/'feature_cache';cache.mkdir(exist_ok=True)

    @torch.inference_mode()
    def read(text):
        key=hashlib.sha256(text.encode()).hexdigest();file=cache/(key+'.npz')
        if file.exists():
            with np.load(file) as z:
                return z['states'],z['positions'],int(z['tokens'])
        rendered=tok.apply_chat_template([{'role':'user','content':text}],tokenize=False,add_generation_prompt=False)
        spans=[m.span() for m in re.finditer('STATE:',rendered)]
        assert len(spans) in [1,2]
        b=tok(rendered,return_offsets_mapping=True,return_tensors='pt',add_special_tokens=False)
        offsets=b.pop('offset_mapping')[0].tolist();ids=b.input_ids[0].tolist()
        positions=[]
        for start,end in spans:
            hit=[i for i,(lo,hi) in enumerate(offsets) if lo<=end-1<hi]
            assert len(hit)==1;positions.append(hit[0])
        assert len({ids[i] for i in positions})==1
        result=model(**{k:v.to(device) for k,v in b.items()},output_hidden_states=True,use_cache=False)
        states=np.stack([np.stack([result.hidden_states[l][0,p].float().cpu().numpy()
                                 for l in LAYERS]) for p in positions])
        assert np.isfinite(states).all()
        temp=file.with_suffix('.tmp.npz')
        np.savez_compressed(temp,states=states,positions=positions,tokens=len(ids));temp.replace(file)
        return states,np.asarray(positions),len(ids)

    # Test causal masking with a fixed prefix and two different suffixes.
    a,_,_=read(prompt('banana','neutral','The room contained a wooden table.',0,0))
    b,_,_=read(prompt('banana','neutral','The room contained a curved yellow fruit.',0,0))
    assert np.max(np.abs(a[0]-b[0]))<1e-5
    # Audit equal instruction token counts and actual readout positions, not word counts.
    diagnostics=[]
    for target in sorted(set(design.apply(lambda r:r.concept if r.target_role=='X' else r.comparison,axis=1))):
        for f in range(3):
            sizes=[len(tok(INSTRUCTIONS[f][i].format(target=target),add_special_tokens=False).input_ids) for i in range(2)]
            diagnostics.append(dict(target=target,instruction_frame=f,neutral_tokens=sizes[0],
                                    suppression_tokens=sizes[1],length_matched=sizes[0]==sizes[1]))
    pd.DataFrame(diagnostics).to_csv(out/'instruction_length_audit.csv',index=False)
    # Independent semantic encoder audit. Never discard stimuli based on model outcomes.
    et=AutoTokenizer.from_pretrained(ENCODER,revision=encoder_sha)
    em=AutoModel.from_pretrained(ENCODER,revision=encoder_sha).cpu().eval()
    texts=sorted(set(design.cue_text)|{f'This text concerns {w}.' for w in set(design.concept)|set(design.comparison)})
    embeddings={}
    for start in range(0,len(texts),32):
        chunk=texts[start:start+32];batch=et(chunk,padding=True,truncation=True,max_length=128,return_tensors='pt')
        with torch.inference_mode():
            h=em(**batch).last_hidden_state;mask=batch.attention_mask.unsqueeze(-1)
            pooled=(h*mask).sum(1)/mask.sum(1).clamp(min=1)
            vec=torch.nn.functional.normalize(pooled.float(),dim=-1).numpy()
        embeddings.update(zip(chunk,vec))
    del em,et
    design['sim_X']=[float(embeddings[f'This text concerns {x}.']@embeddings[t])
                     for x,t in zip(design.concept,design.cue_text)]
    design['sim_Y']=[float(embeddings[f'This text concerns {y}.']@embeddings[t])
                     for y,t in zip(design.comparison,design.cue_text)]
    # Preserve exact v2 distance values for comparison with saved experiment;
    # the fresh encoder similarities above are a separate sensitivity audit.
    bank=pd.read_csv(ROOT/'1019/results_v2/20261019T133851060426Z/01_stimulus_distances_and_ranks.csv')
    distances={(r.concept,r.cue_text):r.semantic_distance for r in bank.itertuples()}
    design['semantic_distance']=[distances.get((r.concept,r.cue_text),np.nan) for r in design.itertuples()]
    design['cue_token_count']=[len(tok(t,add_special_tokens=False).input_ids) for t in design.cue_text]
    design.to_csv(out/'executed_design.csv',index=False)
    descriptions=json.loads((ROOT/'1019/probe_description_bank_v2.json').read_text())
    train_frames=['The concept is {}.\nSTATE:\n','Focus attention on {}.\nSTATE:\n']
    description_frames=['A short definition is {}.\nSTATE:\n','The subject is described as {}.\nSTATE:\n']
    test_frames=['A curator wrote about {}.\nSTATE:\n','An observer reported {}.\nSTATE:\n']
    all_validation=[];fragments=[];shuffle_controls=[]
    for x,g in design.groupby('concept',sort=True):
        print('Extracting and fitting',x,'contexts:',len(g),flush=True)
        y=g.comparison.iloc[0];examples=[]
        for label,word,prefix in [(1,x,'x'),(0,y,'y')]:
            for f in train_frames:
                feature,_,_=read(f.format(word));examples.append(dict(label=label,split='train',phrase=-1,feature=feature[0]))
            for split,frames in [('train',description_frames),('test',test_frames)]:
                for idx,phrase in enumerate(descriptions[x][prefix+'_'+split]):
                    for f in frames:
                        feature,_,_=read(f.format(phrase));examples.append(dict(label=label,split=split,phrase=idx,feature=feature[0]))
        # Group-wise shuffled-label controls: duplicated frames of one phrase
        # must share a shuffled label. Exploratory calibration, not extra n.
        base=[e for e in examples if e['split']=='train']
        held=[e for e in examples if e['split']=='test']
        groups=sorted({(e['label'],e['phrase']) for e in base})
        rng=np.random.default_rng(20261103+sum(map(ord,x)))
        for repeat in range(10):
            perm=rng.permutation([g[0] for g in groups])
            mapping=dict(zip(groups,perm))
            labels=[mapping[(e['label'],e['phrase'])] for e in base]
            for layer in [22,23,24]:
                X=np.stack([e['feature'][layer-1] for e in base])
                clf=make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',max_iter=2500,random_state=42))
                clf.fit(X,labels)
                ev=np.stack([e['feature'][layer-1] for e in held])
                auc=roc_auc_score([e['label'] for e in held],clf.decision_function(ev))
                shuffle_controls.append(dict(concept=x,repeat=repeat,layer=layer,auc=float(auc)))
        pd.DataFrame(shuffle_controls).to_csv(out/'probe_label_shuffle_controls.csv',index=False)
        states=[];metadata=[];references={}
        for r in g.itertuples():
            h,pos,n=read(r.prompt);assert h.shape[0]==2
            group=(r.target_role,r.condition,r.instruction_frame,r.context_frame)
            if group in references:
                assert np.max(np.abs(references[group]-h[0]))<1e-5
            else:references[group]=h[0].copy()
            states.append(h);metadata.append((r.design_row,r.target_role,pos,n))
        features=np.stack(states) # prompt x pre/post x layer x hidden
        records=[]
        for variant in probe_plan():
            train=[e for e in examples if e['split']=='train'
                and (variant['names'] or e['phrase']!=-1)
                and (e['phrase']==-1 or e['phrase']!=variant['omit_x' if e['label']==1 else 'omit_y'])]
            test=[e for e in examples if e['split']=='test']
            for l in LAYERS:
                X=np.stack([e['feature'][l-1] for e in train]);labels=np.array([e['label'] for e in train])
                clf=make_pipeline(StandardScaler(),LogisticRegression(C=.1,solver='liblinear',max_iter=2500,random_state=42))
                clf.fit(X,labels)
                sd=max(float(np.std(clf.decision_function(X),ddof=1)),1e-8)
                testx=np.stack([e['feature'][l-1] for e in test])
                auc=roc_auc_score([e['label'] for e in test],clf.decision_function(testx))
                all_validation.append(dict(concept=x,probe_variant=variant['name'],layer=l,auc=float(auc),
                                            n_train=len(train),n_holdout=12,n_holdout_phrases=6))
                raw=clf.decision_function(features[:,:,l-1,:].reshape(-1,features.shape[-1])).reshape(len(g),2)/sd
                for i,(design_row,role,pos,n) in enumerate(metadata):
                    sign=1 if role=='X' else -1
                    records.append(dict(design_row=design_row,probe_variant=variant['name'],layer=l,
                        pre_target_std=sign*raw[i,0],post_target_std=sign*raw[i,1],
                        delta_target_std=sign*(raw[i,1]-raw[i,0]),
                        pre_pos=int(pos[0]),post_pos=int(pos[1]),prompt_tokens=n))
        file=out/f'measurements_{x}.csv';pd.DataFrame(records).to_csv(file,index=False);fragments.append(file)
        pd.DataFrame(all_validation).to_csv(out/'probe_validation.csv',index=False)
        del features,states,records
    measurements=pd.concat([pd.read_csv(f) for f in fragments],ignore_index=True)
    assert len(measurements)==len(design)*20*24
    analyze(measurements,design,out)
    try:commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    except (OSError,subprocess.CalledProcessError):commit=None
    provenance={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        HERE/'run_robustness.py',HERE/'additional_cues.csv',ROOT/'1019/stimuli_v2.csv',
        ROOT/'1019/specificity_cues_v3.csv',ROOT/'1019/probe_description_bank_v2.json']}
    manifest.update(identity,status='COMPLETED',python=platform.python_version(),sklearn=sklearn.__version__,
        git_commit=commit,input_hashes=provenance,
        label_shuffle_control_fits=len(shuffle_controls),
        caution='Exploratory sensitivity analysis. 8 pairs only. 20 probes/6 frames do not increase independent n. No human cue validation.')
    (out/'completed_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Completed:',out,flush=True)


if __name__=="__main__":
    main()
