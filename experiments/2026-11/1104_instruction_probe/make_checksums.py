from pathlib import Path
import sys,json,hashlib
from verify import verify
from github_save import ALLOWED
root=Path(sys.argv[1]);verify(root)
checks={}
for name in ALLOWED:
 if name=='RESULT_SHA256.json':continue
 p=root/name;assert p.is_file() and not p.is_symlink(),name
 assert p.stat().st_size<10*1024*1024,name
 checks[name]=hashlib.sha256(p.read_bytes()).hexdigest()
(root/'RESULT_SHA256.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Result checksums ready:',len(checks),'files. Feature shards and weights are included.')
