"""Frozen lexical content proxy, separate from whole-answer format adherence."""
from pathlib import Path
import json,re,unicodedata
RULES=json.loads((Path(__file__).parent/'rules.json').read_text())
def norm(s):
 return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s).casefold()).strip().strip(' .!?:;\"\'`*_')
def grade(answer,target):
 # Strip common markdown delimiters, not words; never search only for a mention.
 clean=unicodedata.normalize('NFKC',answer).strip().strip('`*_')
 first=re.split(r'[.!?\n]',clean,maxsplit=1)[0]
 prefix=norm(first);whole=norm(clean)
 if target!='none':
  prefix=re.sub(r'^(?:a|an|the) ','',prefix)
  whole=re.sub(r'^(?:a|an|the) ','',whole)
 found=[k for k,vs in RULES['aliases'].items() if any(re.search(r'\b'+re.escape(v)+r'\b',clean,re.I) for v in vs)]
 alternative=bool(re.search(r'\b(or|however|actually|instead|but|maybe|perhaps|possibly)\b',clean,re.I))
 neg=bool(re.search(r'\b(not|neither|isn.t|aren.t|cannot|can.t)\b',clean,re.I))
 if target=='none':
  correct=prefix in RULES['none_answers'] and not found and not alternative
  format_ok=whole in RULES['none_answers']
 else:
  correct=prefix in RULES['aliases'][target] and found==[target] and not alternative and not neg
  format_ok=whole in RULES['aliases'][target]
 return dict(correct=bool(correct),format_ok=bool(format_ok),prefix=prefix,found='|'.join(found),conflict=bool(alternative or (neg and target!='none')))
def summarize(a):
 return dict(contexts=len(a),correct=int(a.correct.sum()),truncations=int(a.truncated.sum()))
