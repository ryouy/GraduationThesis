from pathlib import Path
import sys,json
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(sys.argv[1]);a=pd.read_csv(p/'answers.csv',converters={'answer':str,'found':str});u=pd.read_csv(p/'probe_auc.csv');n=pd.read_csv(p/'shuffled.csv')
b=a.groupby('target').correct.agg(['sum','count']);print(b.to_string());print(a[['target','answer','correct']].to_string(index=False));print(u.query('position=="assistant_start" and layer==27').to_string(index=False))
q=u.query('position=="assistant_start" and layer==27').merge(n.groupby('pair').auc.quantile(.95).rename('shuffle_p95'),on='pair');q.to_csv(p/'primary_probe_summary.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained');order=['banana','apple','elephant','giraffe','piano','violin','none'];v=b.reindex(order);bars=axes[0].bar(order,v['sum'],color=['#19887b']*6+['#7e8795']);axes[0].bar_label(bars,labels=[f'{int(x)}/6' for x in v['sum']],padding=3);axes[0].set_ylim(0,7);axes[0].set_ylabel('Correct responses (aliases accepted)');axes[0].set_title('1.5B naming: new descriptions');axes[0].tick_params(axis='x',rotation=30)
bars=axes[1].bar(q.pair,q.auc,color='#19887b');axes[1].bar_label(bars,fmt='%.3f',padding=3);axes[1].scatter(q.pair,q.shuffle_p95,color='#9e644c',marker='D',label='Shuffled-label 95th percentile',zorder=3);axes[1].set_ylim(0,1.12);axes[1].set_ylabel('ROC AUC');axes[1].set_title('Probe: layer 27, before answer');axes[1].legend(frameon=False,fontsize=8,loc='lower left')
for ax in axes:ax.spines[['top','right']].set_visible(False)
fig.savefig(p/'fresh_check_summary.png',dpi=180);fig.savefig(p/'fresh_check_summary.pdf')
