from pathlib import Path
import sys,json
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);entries=json.loads((root/'resolved_models.json').read_text());summary=[];frames=[]
for e in entries:
 m=json.loads((root/e['key']/'manifest.json').read_text())
 if m['status']!='COMPLETED':continue
 a=pd.read_csv(root/e['key']/'answers.csv',converters={'answer':str,'found':str});a['model']=e['label'];frames.append(a)
 summary.append({k:m[k] for k in ['key','label','correct','clear_n','min_per_concept','none_correct','all_pass','truncations','load_seconds','generation_seconds','peak_vram_bytes']})
s=pd.DataFrame(summary);a=pd.concat(frames);s.to_csv(root/'comparison_summary.csv',index=False);a.to_csv(root/'all_answers.csv',index=False)
per=a.groupby(['model','target']).correct.sum().unstack().reindex(s.label);per.to_csv(root/'per_concept.csv');print(s.to_string(index=False));print(per.to_string());print('WRONG\n',a[a.correct==False][['model','target','answer']].to_string(index=False))
fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained');colors=['#748396','#3e9c90','#bd925a','#1c6964'][:len(s)]
bars=axes[0].bar(s.label,s.correct,color=colors);axes[0].bar_label(bars,labels=[f'{v}/36' for v in s.correct],padding=3);axes[0].set_ylim(0,41);axes[0].axhline(30,ls=':',color='gray',lw=1);axes[0].set_title('Same 36 descriptions: naming performance');axes[0].set_ylabel('Correct responses (aliases accepted)');axes[0].tick_params(axis='x',rotation=20)
order=['banana','apple','elephant','giraffe','piano','violin','none'];matrix=per.reindex(columns=order).to_numpy();axes[1].imshow(matrix,vmin=0,vmax=6,cmap='YlGnBu',aspect='auto');axes[1].set_xticks(range(7),order,rotation=30);axes[1].set_yticks(range(len(s)),s.label);axes[1].set_title('Correct per concept / 6; none uses STRICT format')
for i in range(len(s)):
 for j in range(7):axes[1].text(j,i,str(int(matrix[i,j])),ha='center',va='center',color='white' if matrix[i,j]>=4 else 'black')
axes[0].spines[['top','right']].set_visible(False)
fig.savefig(root/'four_model_comparison.png',dpi=180);fig.savefig(root/'four_model_comparison.pdf')

# Post-hoc diagnostic, separate from the frozen score and gate.
none=a[a.target=='none'].copy()
none['none_prefix_diagnostic']=none.answer.str.match(r'(?i)^\s*none(?:[.!]|$)')
none[['model','item_id','text','answer','correct','none_prefix_diagnostic']].to_csv(root/'none_format_diagnostic.csv',index=False)
print('POST-HOC none-prefix diagnostic (not the preregistered grade):')
print(none.groupby('model').none_prefix_diagnostic.sum().to_string())
