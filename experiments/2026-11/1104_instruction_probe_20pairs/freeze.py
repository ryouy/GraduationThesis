from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
names=['prepare.py','check.py','extract.py','analyze.py','verify.py','github_save.py','make_checksums.py','test_pipeline.py','test_github_save.py','training.csv','design.csv','config.json','sources.json','PLAN.md','requirements.txt']
(H/'FROZEN_SHA256.json').write_text(json.dumps({n:hashlib.sha256((H/n).read_bytes()).hexdigest() for n in names},indent=2)+'\n')
print('Frozen',len(names),'files before model extraction.')
