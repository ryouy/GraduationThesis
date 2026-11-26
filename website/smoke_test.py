"""Browser regression test for the generated layout, with deterministic local data."""
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "_site" / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "_site" / "data" / "README.md").read_text(encoding="utf-8")
assert "github-only:start" not in readme and "[Web ver.]" not in readme and "img.shields.io/badge/Web版" not in readme

# No network dependencies in the smoke test: replace third-party renderers
# with a small fixture while retaining the actual generated CSS and viewer JS.
assert '<style>' in HTML and "DOMContentLoaded" in HTML
assert 'href="website/style.css"' not in HTML
assert 'src="website/app.js"' not in HTML
fixture = re.sub(r'<script defer src="https://[^"]+"></script>', '', HTML)
fixture = re.sub(r'<link rel="stylesheet" href="https://[^"]+">', '', fixture)
stubs = """
<script>
window.marked={parse:()=>'<h1>Layout regression test</h1><details><summary>実験全体のフロー図</summary><p>図の内容</p></details><h2>Section</h2><p>Content</p>'};
window.DOMPurify={sanitize:x=>x};
window.fetch=async url=>({ok:true,json:async()=>({commit:'main',files:[{path:'README.md',local:true},{path:'docs/very_long_research_document_name_to_test_fading.md',local:true},{path:'docs/sample.ipynb',local:false},{path:'docs/sample.csv',local:true},{path:'docs/nested/example.md',local:true}]}),text:async()=> '# Layout regression test'});
</script>
"""
fixture = fixture.replace('</head>', stubs + '</head>')
checks = """
<script>
document.addEventListener('DOMContentLoaded',async()=>{
  const checks=[];
  const verify=(name,ok)=>checks.push([name,Boolean(ok)]);
  try {
    for(let i=0;i<50&&!document.querySelector('#content h1');i++) await new Promise(r=>setTimeout(r,20));
    const get=id=>document.getElementById(id), rect=id=>get(id).getBoundingClientRect(), style=id=>getComputedStyle(get(id));
    const main=document.querySelector('main').getBoundingClientRect();
    const desktop=innerWidth>900, mobile=innerWidth<=650;
    verify('article rendered',!!document.querySelector('#content h1'));
    const detail=document.querySelector('#content details');
    verify('protocol figure initially closed',!!detail&&!detail.open);
    if(detail){detail.querySelector('summary').click();verify('protocol figure expands',detail.open);detail.querySelector('summary').click();verify('protocol figure collapses',!detail.open);}
    verify('article width',main.width>= (mobile?innerWidth-2:325));
    verify('article within viewport',main.left>=0&&main.right<=innerWidth+1);
    verify('no horizontal overflow',document.documentElement.scrollWidth<=innerWidth+1);
    verify('no global header',!document.querySelector('header'));
    verify('search has no placeholder',!get('search').hasAttribute('placeholder'));
    verify('no source action bar',!get('actions'));
    verify('GitHub targets current document',document.querySelector('.github-link').href.endsWith('/blob/main/README.md'));
    const home=document.querySelector('.sidebar-tools .home-link');
    verify('Home icon precedes theme',!!home&&home.nextElementSibling===get('theme')&&!!home.querySelector('svg')&&home.getAttribute('href')==='?file=README.md');
    verify('root README absent from file tree',!document.querySelector('#tree a[title="README.md"]'));
    verify('home breadcrumb contains only Home',get('crumb').textContent.trim()==='Home'&&get('crumb').querySelectorAll('a').length===1);
    const file=document.querySelector('#tree a');
    verify('file names do not wrap',getComputedStyle(file).whiteSpace==='nowrap');
    verify('file names fade',getComputedStyle(file).maskImage!=='none');
    const notebook=document.querySelector('#tree [data-ext="ipynb"]'), csv=document.querySelector('#tree [data-ext="csv"]'), folder=document.querySelector('#tree .folder-entry');
    verify('file types and folder distinct',!!notebook&&!!csv&&!!folder&&getComputedStyle(notebook).color!==getComputedStyle(csv).color&&getComputedStyle(folder).color!==getComputedStyle(notebook).color);
    verify('notebook orange',getComputedStyle(notebook).getPropertyValue('--file-color').trim()===getComputedStyle(notebook).getPropertyValue('--file-notebook').trim());
    verify('folder icon',getComputedStyle(folder,'::before').maskImage!=='none');
    const branch=folder.parentElement, children=branch.querySelector(':scope > .tree-children');
    verify('collapsed folder hides child guides',!!children&&getComputedStyle(children).display==='none');
    folder.click();
    verify('expanded folder shows guide',branch.open&&getComputedStyle(children).display==='block'&&getComputedStyle(children).borderLeftWidth==='1px'&&getComputedStyle(children).borderLeftStyle==='solid');
    const nested=children.querySelector('details'), nestedChildren=nested?.querySelector(':scope > .tree-children');
    if(nested){nested.querySelector('summary').click();verify('nested guide',nested.open&&getComputedStyle(nestedChildren).display==='block'&&parseFloat(getComputedStyle(nestedChildren).marginLeft)>0&&getComputedStyle(nestedChildren).borderLeftWidth==='1px');}
    else verify('nested folder exists',false);
    folder.click();
    verify('guide hidden on collapse',!branch.open&&getComputedStyle(children).display==='none');
    if(mobile){
      verify('mobile sidebar initially hidden',style('sidebar').display==='none');
      get('menu').click();
      verify('mobile sidebar opens',style('sidebar').display!=='none');
      get('close-menu').click();
      verify('mobile sidebar closes',style('sidebar').display==='none');
    }else{
      verify('left pane before article',rect('sidebar').right<=main.left);
      verify('desktop close button hidden',style('close-menu').display==='none');
      const left=rect('sidebar').width;
      get('resize-left').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true}));
      verify('left pane resizes',rect('sidebar').width>left);
      if(desktop){
        verify('right pane after article',rect('toc').left>=main.right);
        const right=rect('toc').width;
        get('resize-right').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true,cancelable:true}));
        verify('right pane resizes',rect('toc').width>right);
      }else verify('tablet toc hidden',style('toc').display==='none');
    }
    // A long file list must scroll independently of the toolbar and search.
    if(mobile)get('menu').click();
    const sidebar=get('sidebar'), tree=get('tree'), tools=sidebar.querySelector('.sidebar-tools'), search=sidebar.querySelector('.search-row');
    const extra=document.createElement('div');extra.style.height='2000px';tree.append(extra);
    const toolsTop=tools.getBoundingClientRect().top, searchTop=search.getBoundingClientRect().top;
    tree.scrollTop=300;
    verify('file tree scrolls independently',tree.scrollTop>0&&sidebar.scrollTop===0);
    verify('sidebar controls stay fixed',tools.getBoundingClientRect().top===toolsTop&&search.getBoundingClientRect().top===searchTop);
    extra.remove();tree.scrollTop=0;
    if(mobile)get('close-menu').click();
  }catch(e){checks.push([String(e),false])}
  const output=document.createElement('pre');output.id='smoke-result';
  output.textContent=checks.every(x=>x[1])?'PASS':JSON.stringify(checks);
  document.body.append(output);
});
</script>
"""
fixture = fixture.replace('</body>', checks + '</body>')
browser = next((p for n in ('google-chrome','chromium','chromium-browser') if (p:=shutil.which(n))), None)
if browser is None:
    raise RuntimeError("Chrome/Chromium is required")
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "layout.html"
    path.write_text(fixture, encoding="utf-8")
    for width in (1440, 800, 500):
        result = subprocess.run([browser,"--headless","--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--disable-background-networking","--no-first-run",f"--user-data-dir={tmp}/profile-{width}",f"--window-size={width},900","--virtual-time-budget=4000","--dump-dom",path.as_uri()],capture_output=True,text=True,timeout=30)
        match = re.search(r'<pre id="smoke-result">(.*?)</pre>', result.stdout, re.S)
        if result.returncode or not match or match.group(1) != "PASS":
            raise RuntimeError(f"Layout test at {width}px failed: {match.group(1) if match else result.stderr[-1500:]}")
        print(f"PASS: {width}px")
