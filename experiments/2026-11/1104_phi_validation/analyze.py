"""Analyze frozen scores and record a separate post-hoc raw-answer audit."""
from pathlib import Path
import sys,json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(sys.argv[1]);a=pd.read_csv(r/'phi3_5mini/answers.csv',keep_default_na=False)
# All 72 raw answers were reviewed. One exact subtype is semantically correct.
a['review_content_correct']=a.correct
mask=(a.item_id=='piano_07')&(a.answer=='Grand Piano')
assert mask.sum()==1
a.loc[mask,'review_content_correct']=True
a['review_note']='Fixed grade agrees with intended-target content judgment; stimulus ambiguity not independently adjudicated.'
a.loc[mask,'review_note']='Post-hoc discrepancy: Grand Piano is a subtype of piano. Keep frozen grade false; report separately.'
a.loc[a.truncated,'review_note']='Truncated after an initial None; incorrect target identification before truncation. No continuation generated.'
a[['item_id','target','text','answer','correct','format_ok','truncated','review_content_correct','review_note']].to_csv(r/'raw_answer_review.csv',index=False)
order=['banana','apple','elephant','giraffe','piano','violin']
clear=a[a.target!='none'];per=clear.groupby('target')[['correct','review_content_correct']].sum().reindex(order);per['n']=10;per.to_csv(r/'concept_summary.csv')
a[~a.correct].to_csv(r/'frozen_errors.csv',index=False)
summary={'clear_frozen':int(clear.correct.sum()),'clear_n':60,'clear_review':int(clear.review_content_correct.sum()),'none_correct':int(a[a.target=='none'].correct.sum()),'none_n':12,'format_clear':int(clear.format_ok.sum()),'format_none':int(a[a.target=='none'].format_ok.sum()),'truncations':int(a.truncated.sum()),'frozen_pass':False,'review_is_posthoc':True}
(r/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4),layout='constrained');x=range(6);bars=ax.bar(x,per.correct,color='#347c78')
ax.bar_label(bars,labels=[f'{v}/10' for v in per.correct],padding=3)
ax.bar(4,1,bottom=7,color='#d7a96b',label='Post-hoc: Grand Piano (+1)')
ax.axhline(8,color='#777777',ls='--',lw=1,label='Required per concept: 8/10')
ax.set(xticks=list(x),xticklabels=['Banana','Apple','Elephant','Giraffe','Piano','Violin'],ylim=(0,11.7),ylabel='Correct / 10',title='Phi: new descriptions — frozen 43/60; content review 44/60')
ax.spines[['top','right']].set_visible(False);ax.legend(loc='upper left',fontsize=8)
fig.savefig(r/'phi_validation_results.png',dpi=180)
print(per.to_string());print(json.dumps(summary))
