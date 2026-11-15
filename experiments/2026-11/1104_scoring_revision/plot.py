from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent/'results'
rows=list(csv.DictReader((R/'summary.csv').open()))
paired={r['condition']:r for r in rows if r['condition'] in ['A_original','B_best_match']}
fig,axes=plt.subplots(1,2,figsize=(9,4),layout='constrained')
for ax,key,total,title in [(axes[0],'naming_correct_adjudicated',60,'Description naming /60'),(axes[1],'none_correct_v2',12,'Unrelated controls /12')]:
 values=[int(paired[c][key]) for c in ['A_original','B_best_match']];b=ax.bar(['A: original','B: best match'],values,color=['#75889d','#367c77']);ax.bar_label(b,labels=[f'{v}/{total}' for v in values],padding=3);ax.set_ylim(0,total*1.2);ax.set_title(title);ax.spines[['top','right']].set_visible(False)
fig.suptitle('Revised scoring + explicit review (post-hoc; same saved answers)',fontsize=11)
fig.savefig(R/'corrected_comparison.png',dpi=170)
