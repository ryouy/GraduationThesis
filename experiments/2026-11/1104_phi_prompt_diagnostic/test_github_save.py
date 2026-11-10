"""Offline tests of real upload logic; never use a real secret or repository."""
import base64,hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import github_save as g

class Response:
 def __init__(self,status,data):self.status_code=status;self.data=data
 def json(self):return self.data
class FakeSession:
 def __init__(self,race=False,unauthorized=False):self.headers={};self.calls=[];self.files={};self.head='parent';self.tree={};self.saved=False;self.race=race;self.unauthorized=unauthorized
 def close(self):pass
 def request(self,method,url,json=None,**kwargs):
  self.calls.append((method,url,json,kwargs))
  assert url.startswith('https://api.github.com/repos/ryouy/GraduationThesis/')
  assert kwargs['allow_redirects']==False
  path=url.split('/GraduationThesis',1)[1]
  if self.unauthorized:return Response(403,{'message':'Do not expose server body'})
  if path=='/git/blobs':
   raw=base64.b64decode(json['content']);sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();return Response(201,{'sha':sha})
  if path=='/git/ref/heads/main':return Response(200,{'object':{'sha':self.head}})
  if path.startswith('/git/commits/') and method=='GET':return Response(200,{'tree':{'sha':'base'}})
  if path.startswith('/contents/'):return Response(200,[]) if self.saved else Response(404,{})
  if path=='/git/trees' and method=='POST':self.tree={e['path']:e['sha'] for e in json['tree']};assert json['base_tree']=='base';return Response(201,{'sha':'newtree'})
  if path=='/git/commits' and method=='POST':assert json['parents']==[self.head];return Response(201,{'sha':'newcommit'})
  if path=='/git/refs/heads/main':
   assert json['force']==False
   if self.race:self.race=False;self.head='concurrent';return Response(422,{})
   self.saved=True;self.head='newcommit';return Response(200,{'object':{'sha':'newcommit'}})
  if path.startswith('/git/trees/'):
   return Response(200,{'tree':[{'path':p,'sha':s,'type':'blob'} for p,s in self.tree.items()],'truncated':False})
  raise AssertionError((method,path))

class SaveTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'phi-prompt-20261104T000000000000Z';self.root.mkdir()
  for name in g.ALLOWED:
   p=self.root/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text('{}\n')
  self.checks()
 def tearDown(self):self.temp.cleanup()
 def checks(self):
  (self.root/'RESULT_SHA256.json').write_text(json.dumps({n:hashlib.sha256((self.root/n).read_bytes()).hexdigest() for n in g.ALLOWED if n!='RESULT_SHA256.json'}))
 def save(self,session):
  with patch('analyze.verify') as verify,patch.object(g,'read_secret',return_value='mock_secret_for_offline_test'),patch.object(g,'session_for',return_value=session):
   result=g.save_results(self.root);verify.assert_called_once_with(self.root.resolve());return result
 def test_atomic_save_and_receipt(self):
  s=FakeSession();r=self.save(s);self.assertEqual(r['files'],12);self.assertEqual(sum(c[0]=='PATCH' for c in s.calls),1);self.assertTrue((self.root/'github_receipt.json').exists())
 def test_repeat_is_idempotent(self):
  s=FakeSession();self.save(s);r=self.save(s);self.assertTrue(r['already_saved']);self.assertEqual(sum(c[0]=='PATCH' for c in s.calls),1)
 def test_concurrent_ref_retry(self):
  s=FakeSession(race=True);self.save(s);self.assertEqual(sum(c[0]=='PATCH' for c in s.calls),2)
 def test_changed_result_stops_before_network(self):
  (self.root/'README.md').write_text('changed');s=FakeSession()
  with self.assertRaises(g.GitHubSaveError):self.save(s)
  self.assertEqual(len(s.calls),0)
 def test_secret_in_result_not_transmitted(self):
  (self.root/'README.md').write_text('mock_secret_for_offline_test');self.checks();s=FakeSession()
  with self.assertRaises(g.GitHubSaveError):self.save(s)
  self.assertEqual(len(s.calls),0)
 def test_auth_error_has_no_body_or_secret(self):
  with self.assertRaises(g.GitHubSaveError) as cm:self.save(FakeSession(unauthorized=True))
  self.assertNotIn('mock_secret',str(cm.exception));self.assertNotIn('server body',str(cm.exception))
if __name__=='__main__':unittest.main()
