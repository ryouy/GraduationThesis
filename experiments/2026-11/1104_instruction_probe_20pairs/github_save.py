"""Save only validated result files, atomically, without putting secrets in git."""
from pathlib import Path
import base64,hashlib,json,re
import requests
REPOSITORY='ryouy/GraduationThesis'
BRANCH='main'
PREFIX='1104_instruction_probe_20pairs/results'
# Edit this name only if the existing Colab Secret uses another name.
SECRET_NAME='GITHUB_TOKEN'
SECRET_CANDIDATES=['GITHUB_TOKEN','GH_TOKEN','github_token','github_pat']
ALLOWED=['training.csv', 'design.csv', 'config.json', 'sources.json', 'PLAN.md', 'FROZEN_SHA256.json', 'manifest.json', 'prompt_index.json', 'tokens.json', 'features_L31_context_end.npz', 'features_L31_assistant_start.npz', 'scores.csv', 'probe_auc.csv', 'shuffled.csv', 'probes.csv', 'calibration.csv', 'pair_summary.csv', 'family_scores.csv', 'contrasts.csv', 'means.csv', 'probe_weights.npz', 'README.md', 'comparison.png', 'RESULT_SHA256.json']
class GitHubSaveError(RuntimeError):pass

def read_secret(secret_name=SECRET_NAME):
 from google.colab import userdata
 for name in dict.fromkeys([secret_name]+SECRET_CANDIDATES):
  try:token=userdata.get(name)
  except userdata.SecretNotFoundError:continue
  except Exception:raise GitHubSaveError('Colabシークレットへのアクセスを許可してください。秘密値は表示していません。') from None
  if token and token.strip():return token.strip()
 raise GitHubSaveError('GitHubトークンのシークレットが見つかりません。SECRET_NAMEを既存のキー名に合わせてください。値をコードに貼る必要はありません。')

def session_for(token):
 s=requests.Session();s.headers.update({'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'});return s

def api(session,method,path,body=None,allow=()):
 # The authenticated client has one fixed origin and repository. Never follow redirects.
 url='https://api.github.com/repos/'+REPOSITORY+path
 try:r=session.request(method,url,json=body,timeout=45,allow_redirects=False)
 except requests.RequestException:raise GitHubSaveError('GitHubへの通信に失敗しました。結果はColabに残っています。保存セルだけ再実行できます。') from None
 if r.status_code in allow:return None
 if not 200<=r.status_code<300:
  hint='トークンの対象リポジトリとContents書込み権限を確認してください。' if r.status_code in (401,403,404) else '結果はColabに残っています。'
  raise GitHubSaveError(f'GitHub保存停止（HTTP {r.status_code}）。{hint}')
 return r.json()

def check_access(secret_name=SECRET_NAME):
 token=read_secret(secret_name);s=session_for(token)
 try:
  api(s,'GET','/git/ref/heads/'+BRANCH)
  print('GitHub接続確認済み（書込みは実験後の保存時に確認）。トークンは表示しません。')
 finally:s.headers.pop('Authorization',None);s.close();del token

def save_results(root,secret_name=SECRET_NAME):
 root=Path(root).resolve();run_id=root.name
 if json.loads((root/'manifest.json').read_text()).get('synthetic_test'):raise GitHubSaveError('Synthetic test results cannot be uploaded as experiments.')
 if not re.fullmatch(r'instruction-probe20-\d{8}T\d{12}Z',run_id):raise GitHubSaveError('Unexpected run directory name.')
 # Reverify immediately before collecting the explicit allowlist.
 from verify import verify
 verify(root)
 checks=json.loads((root/'RESULT_SHA256.json').read_text())
 if set(checks)!=set(ALLOWED)-{'RESULT_SHA256.json'}:raise GitHubSaveError('Result checksum list mismatch.')
 data={}
 for name in ALLOWED:
  p=root/name
  if p.is_symlink() or not p.is_file():raise GitHubSaveError('Result file missing or symlink: '+name)
  raw=p.read_bytes()
  if name in checks and hashlib.sha256(raw).hexdigest()!=checks[name]:raise GitHubSaveError('Result changed after verification: '+name)
  if len(raw)>64*1024*1024:raise GitHubSaveError('Unexpectedly large result file: '+name)
  data[name]=raw
 destination=PREFIX+'/'+run_id
 token=read_secret(secret_name);s=session_for(token)
 try:
  # Fail before creating blobs if a secret somehow entered the allowlisted files.
  for raw in data.values():
   if token.encode() in raw:raise GitHubSaveError('Secret detected in a result file; upload cancelled.')
  blobs={}
  for name,raw in data.items():
   blob=api(s,'POST','/git/blobs',{'content':base64.b64encode(raw).decode(),'encoding':'base64'})
   expected=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
   if blob['sha']!=expected:raise GitHubSaveError('Uploaded blob checksum mismatch.')
   blobs[name]=blob['sha']
  for attempt in range(3):
   head=api(s,'GET','/git/ref/heads/'+BRANCH)['object']['sha']
   parent=api(s,'GET','/git/commits/'+head)
   existing=api(s,'GET','/contents/'+destination,allow=(404,))
   if existing is not None:
    # Idempotent save-cell retry: never overwrite a result directory.
    tree=api(s,'GET','/git/trees/'+parent['tree']['sha']+'?recursive=1')
    actual={e['path']:e['sha'] for e in tree['tree'] if e['type']=='blob'}
    if not tree.get('truncated') and all(actual.get(destination+'/'+n)==sha for n,sha in blobs.items()):
     print('同じ結果は既にGitHubに保存されています。')
     return {'commit':head,'url':'https://github.com/'+REPOSITORY+'/tree/'+head+'/'+destination,'already_saved':True}
    raise GitHubSaveError('Destination exists with different content; overwrite cancelled.')
   tree=api(s,'POST','/git/trees',{'base_tree':parent['tree']['sha'],'tree':[{'path':destination+'/'+n,'mode':'100644','type':'blob','sha':sha} for n,sha in blobs.items()]})
   commit=api(s,'POST','/git/commits',{'message':'Record instruction Probe diagnostic '+run_id,'tree':tree['sha'],'parents':[head]})
   # force=False protects concurrent commits. A race is retried on the new head.
   try:
    api(s,'PATCH','/git/refs/heads/'+BRANCH,{'sha':commit['sha'],'force':False})
   except GitHubSaveError:
    new_head=api(s,'GET','/git/ref/heads/'+BRANCH)['object']['sha']
    if new_head!=head and attempt<2:continue
    raise
   verify_tree=api(s,'GET','/git/trees/'+tree['sha']+'?recursive=1')
   actual={e['path']:e['sha'] for e in verify_tree['tree'] if e['type']=='blob'}
   if verify_tree.get('truncated') or not all(actual.get(destination+'/'+n)==sha for n,sha in blobs.items()):raise GitHubSaveError('Commit created; tree verification incomplete. Keep the local ZIP.')
   receipt={'commit':commit['sha'],'url':'https://github.com/'+REPOSITORY+'/tree/'+commit['sha']+'/'+destination,'files':len(data),'already_saved':False}
   (root/'github_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
   return receipt
  raise GitHubSaveError('Concurrent updates prevented save. Retry this save cell only.')
 finally:s.headers.pop('Authorization',None);s.close();del token
