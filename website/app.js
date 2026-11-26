"use strict";
const REPO="ryouy/GraduationThesis", BRANCH="main", $=s=>document.querySelector(s), content=$("#content"), tree=$("#tree");
const encodePath=p=>p.split("/").map(encodeURIComponent).join("/");
const github=p=>"https://github.com/"+REPO+(p?"/"+(dirs.has(p)&&!files.has(p)?"tree":"blob")+"/"+BRANCH+"/"+encodePath(p):"");
const colab=p=>"https://colab.research.google.com/github/"+REPO+"/blob/"+BRANCH+"/"+encodePath(p);
const raw=p=>"https://raw.githubusercontent.com/"+REPO+"/"+BRANCH+"/"+encodePath(p);
const route=(p,h="")=>"?file="+encodeURIComponent(p)+h;
const ext=p=>p.split(".").pop().toLowerCase();
const allowed=new Set(["md","csv","ipynb","png","jpg","jpeg","gif","webp","svg","pdf","py","json","jsonl","txt","log","tsv","zip","npz","npy","parquet","xlsx","pptx","docx"]);
const localTypes=new Set(["md","csv","png","jpg","jpeg","gif","webp","svg","pdf","py","json","jsonl","txt","log","tsv"]);
const excluded=p=>p.split("/").some(s=>s.startsWith("."))||p.startsWith("website/")||p==="index.html"||p==="manifest.json";
let files=new Map(), dirs=new Set([""]), revision=BRANCH;
function node(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n}
function link(label,href,external=false){const a=node("a",label);a.href=href;if(external){a.target="_blank";a.rel="noopener noreferrer"}return a}
function source(p){return files.get(p)?.local?"data/"+encodePath(p):"https://raw.githubusercontent.com/"+REPO+"/"+revision+"/"+encodePath(p)}
function destination(p,h=""){if(ext(p)==="ipynb"&&files.has(p))return colab(p);if(files.has(p)||dirs.has(p))return route(p,h);return github(p)+h}
async function get(url){const r=await fetch(url);if(!r.ok)throw Error("HTTP "+r.status+" — "+url);return r}
async function loadIndex(){try{const r=await get("manifest.json");const m=await r.json();if(!Array.isArray(m.files))throw Error("Invalid manifest");revision=m.commit||BRANCH;return m.files}catch(e){const r=await get("https://api.github.com/repos/"+REPO+"/git/trees/"+BRANCH+"?recursive=1");const m=await r.json();if(m.truncated)throw Error("GitHub file index is truncated.");return m.tree.filter(f=>f.type==="blob"&&!excluded(f.path)&&allowed.has(ext(f.path))).map(f=>({path:f.path,size:f.size,local:false}))}}
function addIndex(list){for(const f of list){files.set(f.path,f);const parts=f.path.split("/");parts.pop();while(parts.length){dirs.add(parts.join("/"));parts.pop()}}}
const current=new URLSearchParams(location.search).get("file")??"README.md";
function fileLink(p,label=p.split("/").pop()){const a=link(label+(ext(p)==="ipynb"?" ↗":""),destination(p),ext(p)==="ipynb");a.title=p;a.dataset.ext=ext(p);a.classList.add("file-entry");if(p===current)a.classList.add("active");return a}
function buildTree(query=""){tree.replaceChildren();const needle=query.trim().toLowerCase();if(needle){let n=0;for(const p of [...files.keys()].sort())if(p.toLowerCase().includes(needle)){tree.append(fileLink(p,p));n++}if(!n)tree.append(node("p","該当するファイルはありません"));return}
const root={children:new Map(),files:[]};for(const p of files.keys()){let b=root;const parts=p.split("/");parts.pop();for(const part of parts){if(!b.children.has(part))b.children.set(part,{children:new Map(),files:[]});b=b.children.get(part)}b.files.push(p)}
function draw(branch,parent,prefix=""){const order=(a,b)=>a.localeCompare(b,"ja",{numeric:true});for(const p of branch.files.sort((a,b)=>(a.endsWith("/README.md")||a==="README.md"?-1:0)-(b.endsWith("/README.md")||b==="README.md"?-1:0)||order(a,b)))parent.append(fileLink(p));for(const [name,b] of [...branch.children].sort((a,b)=>order(a[0],b[0]))){const p=prefix+name;const d=node("details");d.open=current===p||current.startsWith(p+"/");const summary=node("summary",name);summary.title=p;summary.classList.add("folder-entry");d.append(summary);const folder=link("フォルダを表示",route(p));folder.classList.add("folder-view");d.append(folder);draw(b,d,p+"/");parent.append(d)}}draw(root,tree)}
function crumbs(p){const el=$("#crumb");el.replaceChildren(link("Home",route("README.md")));let base="";for(const s of p.split("/").filter(Boolean)){base+=(base?"/":"")+s;el.append(node("span","/"),link(s,destination(base)))}}
function updateGithubLink(p){const a=$(".github-link");a.href=github(p);a.title="GitHubで表示: "+(p||"リポジトリ");}
function resolveHref(h,p){if(!h)return null;if(h.startsWith("#"))return {anchor:h};try{const u=new URL(h,"https://repo.invalid/"+encodePath(p));if(u.origin==="https://repo.invalid"){return {path:decodeURIComponent(u.pathname).replace(/^\//,"").replace(/\/$/,""),hash:u.hash}}if(u.hostname==="github.com"||u.hostname==="raw.githubusercontent.com"){const prefixes=u.hostname==="github.com"?["/"+REPO+"/blob/"+BRANCH+"/","/"+REPO+"/tree/"+BRANCH+"/"]:["/"+REPO+"/"+BRANCH+"/"];for(const prefix of prefixes)if(u.pathname.startsWith(prefix))return {path:decodeURIComponent(u.pathname.slice(prefix.length)).replace(/\/$/,""),hash:u.hash}}return null}catch(e){return null}}
function wrapTable(t,cls=""){const w=node("div",undefined,"table-wrap "+cls);t.replaceWith(w);w.append(t)}
function headings(){const toc=$("#toc");toc.replaceChildren();const hs=[...content.querySelectorAll("h1,h2,h3,h4")];if(!hs.length)return;toc.append(node("strong","このページの目次"));const used=new Set();for(const h of hs){const base=h.textContent.toLowerCase().trim().replace(/[^\p{L}\p{N}\s_-]/gu,"").replace(/\s/g,"-")||"section";let id=base,i=1;while(used.has(id))id=base+"-"+i++;used.add(id);h.id=id;const a=link(h.textContent,"#"+encodeURIComponent(id));a.title=h.textContent;a.style.paddingLeft=(Number(h.tagName[1])-1)*8+"px";toc.append(a)}}
async function markdown(p){if(!window.marked||!window.DOMPurify)throw Error("Markdown renderer failed to load.");const md=await(await get(source(p))).text();content.innerHTML=DOMPurify.sanitize(marked.parse(md,{gfm:true,breaks:false}),{FORBID_TAGS:["style","form","input","button","iframe","object","embed","svg","math"],FORBID_ATTR:["style","id","name","srcset","target"]});for(const a of content.querySelectorAll("a[href]")){const r=resolveHref(a.getAttribute("href"),p);if(r?.path!==undefined)a.href=destination(r.path,r.hash);if(r?.anchor)a.href=r.anchor;if(a.hostname!==location.hostname){a.target="_blank";a.rel="noopener noreferrer"}}for(const img of content.querySelectorAll("img[src]")){const r=resolveHref(img.getAttribute("src"),p);if(r?.path!==undefined)img.src=source(r.path);img.loading="lazy"}for(const t of content.querySelectorAll("table"))wrapTable(t);headings();if(window.renderMathInElement)renderMathInElement(content,{delimiters:[{left:"$$",right:"$$",display:true},{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false},{left:"$",right:"$",display:false}],throwOnError:false});const mer=[...content.querySelectorAll("code.language-mermaid")];if(mer.length){try{const {default:m}=await import("https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.esm.min.mjs");m.initialize({startOnLoad:false,securityLevel:"strict",theme:document.documentElement.dataset.theme==="dark"?"dark":"default"});let i=0;for(const code of mer){try{const out=await m.render("diagram-"+i++,code.textContent);const box=node("div");box.innerHTML=DOMPurify.sanitize(out.svg,{USE_PROFILES:{svg:true,svgFilters:true},FORBID_TAGS:["foreignObject","script"]});code.parentElement.replaceWith(box)}catch(e){}}}catch(e){}}if(location.hash){try{document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView()}catch(e){}}}
async function csv(p){if(!window.Papa)throw Error("CSV renderer failed to load.");const text=await(await get(source(p))).text();const parsed=Papa.parse(text,{skipEmptyLines:"greedy",delimiter:ext(p)==="tsv"?"\t":""});const [header=[],...rows]=parsed.data;const width=rows.reduce((n,r)=>Math.max(n,r.length),header.length);while(header.length<width)header.push("Column "+(header.length+1));content.replaceChildren(node("h1",p.split("/").pop()));if(!header.length){content.append(node("p","空のファイルです。"));return}const bar=node("div",undefined,"toolbar"), search=node("input"), prev=node("button","前へ"), next=node("button","次へ"), status=node("span");search.type="search";search.placeholder="すべての列から検索";search.setAttribute("aria-label","表を検索");bar.append(search,prev,next,status);content.append(bar);const wrap=node("div",undefined,"table-wrap csv-wrap"),table=node("table"),thead=node("thead"),tbody=node("tbody"),tr=node("tr");table.append(thead,tbody);thead.append(tr);wrap.append(table);content.append(wrap);if(parsed.errors.length)content.append(node("p","CSV解析時の警告: "+parsed.errors.length+" 件。原本も確認してください。","error"));let page=0,sort=-1,asc=true,view=rows;const size=100;function draw(){tr.replaceChildren();header.forEach((v,i)=>{const th=node("th");const b=node("button",v+(sort===i?(asc?" ↑":" ↓"):""));b.onclick=()=>{asc=sort===i?!asc:true;sort=i;page=0;filter()};th.append(b);tr.append(th)});tbody.replaceChildren();const fragment=document.createDocumentFragment();for(const row of view.slice(page*size,(page+1)*size)){const r=node("tr");for(let i=0;i<header.length;i++)r.append(node("td",row[i]??""));fragment.append(r)}tbody.append(fragment);status.textContent=(view.length?page*size+1:0)+"–"+Math.min((page+1)*size,view.length)+" / "+view.length.toLocaleString()+" 行 · "+header.length+" 列";prev.disabled=page===0;next.disabled=(page+1)*size>=view.length}function filter(){const q=search.value.toLowerCase();view=rows.filter(r=>!q||r.some(v=>String(v).toLowerCase().includes(q)));if(sort>=0)view.sort((a,b)=>{const x=a[sort]??"",y=b[sort]??"",nx=Number(x),ny=Number(y);const c=x!==""&&y!==""&&Number.isFinite(nx)&&Number.isFinite(ny)?nx-ny:x.localeCompare(y,undefined,{numeric:true});return asc?c:-c});draw()}search.oninput=()=>{page=0;filter()};prev.onclick=()=>{if(page>0)page--;draw()};next.onclick=()=>{if((page+1)*size<view.length)page++;draw()};draw()}
function directory(p){content.replaceChildren(node("h1",p||"ファイル一覧"));const list=node("div",undefined,"file-list"),prefix=p?p+"/":"";for(const d of [...dirs].sort())if(d&&d.startsWith(prefix)&&!d.slice(prefix.length).includes("/")&&d!==p)list.append(link(d.slice(prefix.length)+"/",route(d)));for(const f of [...files.keys()].sort())if(f.startsWith(prefix)&&!f.slice(prefix.length).includes("/"))list.append(fileLink(f));content.append(list)}
async function show(p){crumbs(p);updateGithubLink(p);if(dirs.has(p)&&!files.has(p)){directory(p);return}if(!files.has(p))throw Error("ファイルが見つかりません: "+p);document.title=p.split("/").pop()+" | Graduation Thesis";const e=ext(p);if(e==="md")return markdown(p);if(e==="csv"||e==="tsv")return csv(p);content.replaceChildren(node("h1",p.split("/").pop()));if(e==="ipynb"){content.append(link("Google Colabで開く ↗",colab(p),true));return}if(["png","jpg","jpeg","gif","webp","svg"].includes(e)){const img=node("img");img.src=source(p);img.alt=p;content.append(img);return}if(e==="pdf"){const frame=node("iframe");frame.title=p;frame.src=source(p);content.append(frame);return}if(localTypes.has(e)){let txt=await(await get(source(p))).text();if(e==="json"){try{txt=JSON.stringify(JSON.parse(txt),null,2)}catch(e){}}const pre=node("pre");pre.append(node("code",txt));content.append(pre);return}content.append(link("GitHubでファイルを開く ↗",github(p),true))}
$("#search").oninput=e=>buildTree(e.target.value);
function setMenu(open){$("#sidebar").classList.toggle("open",open);$("#menu").setAttribute("aria-expanded",String(open))}
$("#menu").onclick=()=>setMenu(!$("#sidebar").classList.contains("open"));
$("#close-menu").onclick=()=>setMenu(false);
document.addEventListener("keydown",e=>{if(e.key==="Escape")setMenu(false)});
/* Persist pane widths between pages and visits; keep the article usable. */
const paneDefaults={left:270,right:205}, paneMin={left:150,right:130};
const paneWidths={...paneDefaults};
const rootStyle=document.documentElement.style;
function paneLimits(side){
  const viewport=document.documentElement.clientWidth;
  const other=side==="left"?(viewport>900?paneWidths.right:0):paneWidths.left;
  return Math.max(paneMin[side],Math.min(700,viewport-other-330-(viewport>900?10:5)));
}
function applyPane(side,value,save=false){
  const width=Math.round(Math.max(paneMin[side],Math.min(paneLimits(side),value)));
  paneWidths[side]=width;
  rootStyle.setProperty("--"+side+"-width",width+"px");
  const handle=$("#resize-"+side);
  handle.setAttribute("aria-valuemin",String(paneMin[side]));
  handle.setAttribute("aria-valuemax",String(paneLimits(side)));
  handle.setAttribute("aria-valuenow",String(width));
  if(save){try{localStorage.setItem("thesis-pane-"+side,String(width))}catch(e){}}
}
for(const side of ["left","right"]){
  try{const saved=Number(localStorage.getItem("thesis-pane-"+side));if(Number.isFinite(saved)&&saved>0)paneWidths[side]=Math.min(700,saved)}catch(e){}
}
function fitPanes(){applyPane("left",paneWidths.left);applyPane("right",paneWidths.right)}
fitPanes();
window.addEventListener("resize",fitPanes);
for(const side of ["left","right"]){
  const handle=$("#resize-"+side);
  let drag=null;
  handle.addEventListener("pointerdown",e=>{
    if(e.button!==0)return;
    e.preventDefault();handle.focus();drag={id:e.pointerId,x:e.clientX,width:paneWidths[side]};
    handle.setPointerCapture(e.pointerId);handle.classList.add("dragging");document.body.classList.add("resizing");
  });
  handle.addEventListener("pointermove",e=>{
    if(!drag||drag.id!==e.pointerId)return;
    applyPane(side,drag.width+(e.clientX-drag.x)*(side==="left"?1:-1));
  });
  const finish=e=>{
    if(!drag||drag.id!==e.pointerId)return;
    drag=null;applyPane(side,paneWidths[side],true);handle.classList.remove("dragging");document.body.classList.remove("resizing");
  };
  handle.addEventListener("pointerup",finish);handle.addEventListener("pointercancel",finish);handle.addEventListener("lostpointercapture",finish);
  handle.addEventListener("dblclick",()=>applyPane(side,paneDefaults[side],true));
  handle.addEventListener("keydown",e=>{
    if(!["ArrowLeft","ArrowRight","Home","End"].includes(e.key))return;
    e.preventDefault();const step=e.shiftKey?40:12;
    const delta=(e.key==="ArrowLeft"?-step:step)*(side==="left"?1:-1);
    applyPane(side,e.key==="Home"?paneMin[side]:e.key==="End"?paneLimits(side):paneWidths[side]+delta,true);
  });
}
$("#theme").onclick=()=>{const cur=document.documentElement.dataset.theme|| (matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");const next=cur==="dark"?"light":"dark";document.documentElement.dataset.theme=next;try{localStorage.setItem("thesis-theme",next)}catch(e){}};try{const t=localStorage.getItem("thesis-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}
(async()=>{try{addIndex(await loadIndex());buildTree();await show(current)}catch(e){content.replaceChildren(node("h1","読み込みエラー"),node("p",e.message,"error"),link("GitHubで確認する ↗",github(current),true))}})();