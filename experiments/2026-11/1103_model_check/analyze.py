from pathlib import Path
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);aa=[];uu=[];ss=[];nn=[]
for size in ['0.5B','1.5B']:
 for name,rows in [('answers',aa),('probe_auc',uu),('summary',ss),('shuffled',nn)]:rows.append(pd.read_csv(root/size/(name+'.csv'),converters={'answer':str} if name=='answers' else None))
a=pd.concat(aa);u=pd.concat(uu);s=pd.concat(ss);n=pd.concat(nn)
a[a.split=='clear'].groupby(['model','task','target']).correct.agg(['sum','count']).to_csv(root/'accuracy_per_concept.csv')
u[u.primary].merge(n.groupby(['model','concept','task']).auc.quantile(.95).rename('shuffle_p95').reset_index(),on=['model','concept','task']).to_csv(root/'primary_probe_summary.csv',index=False)
s.to_csv(root/'combined_summary.csv',index=False)
print(s.to_string(index=False));print('\nACCURACY BY CONCEPT\n',pd.read_csv(root/'accuracy_per_concept.csv').to_string(index=False));print('\nPRIMARY PROBES\n',pd.read_csv(root/'primary_probe_summary.csv').to_string(index=False));print('\nTRUNCATIONS',int(a.truncated.sum()));print('\nWRONG ANSWERS\n',a[(a.split=='clear') & (a.correct==False)][['model','task','target','text','answer']].to_string(index=False))
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained');colors=['#63758a','#19887b'];models=['0.5B','1.5B'];tasks=['naming','association'];x=np.arange(2)
for i,size in enumerate(models):
 v=s[s.model==size].set_index('task').reindex(tasks)
 bars=axes[0].bar(x+(i-.5)*.34,v.correct,width=.34,label=size,color=colors[i]);axes[0].bar_label(bars,labels=[f'{int(z)}/36' for z in v.correct],padding=3)
axes[0].set_xticks(x,['Naming','Association']);axes[0].set_ylim(0,40);axes[0].axhline(30,color='gray',linestyle=':',lw=1);axes[0].set_title('Calibration descriptions: target-name matches');axes[0].set_ylabel('Number of strict target-name matches');axes[0].legend(frameon=False,loc='lower right')
pairs=['banana','elephant','piano'];xx=np.arange(3);width=.18
for i,(size,task) in enumerate([(m,t) for m in models for t in tasks]):
 v=u[(u.model==size)&(u.task==task)&u.primary].set_index('concept').reindex(pairs)
 bars=axes[1].bar(xx+(i-1.5)*width,v.auc,width=width,label=f'{size} {task}',color=colors[models.index(size)],alpha=1 if task=='naming' else .55);axes[1].bar_label(bars,fmt='%.2f',fontsize=8,padding=2)
axes[1].set_xticks(xx,pairs);axes[1].set_ylim(0,1.12);axes[1].axhline(.8,color='gray',linestyle=':',lw=1);axes[1].set_title('Probe AUC: penultimate layer, before answer');axes[1].set_ylabel('ROC AUC');axes[1].legend(frameon=False,fontsize=8,loc='lower right')
for ax in axes:ax.spines[['top','right']].set_visible(False)
fig.savefig(root/'model_check_summary.png',dpi=180);fig.savefig(root/'model_check_summary.pdf')
