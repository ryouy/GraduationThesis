"""Conservative content parser. correct=None means human review is required."""
from pathlib import Path
import json,re,unicodedata
RULES=json.loads(Path(__file__).with_name('rules_v2.json').read_text())
NAMES={alias:label for label,aliases in RULES['aliases'].items() for alias in aliases}
NAMES.update({name:'other:'+name for name in RULES['other_names']})
NAMES.update({name:'none' for name in RULES['none_answers']})
def normalize(s):
 s=unicodedata.normalize('NFKC',s).casefold().replace('’',"'")
 s=re.sub(r'[*`_]','',s)  # Only formatting delimiters, never meaning-bearing words.
 return re.sub(r'\s+',' ',s).strip().strip('"\'')
def name_pattern(name):return r'(?<!\w)'+re.escape(name)+r'(?!\w)'
def parse(answer):
 text=normalize(answer)
 if not text:return dict(label=None,status='review',reason='empty_answer',format_ok=False)
 # A correction or hedge anywhere is conservatively reviewed rather than guessed.
 if re.search(r"\b(maybe|perhaps|possibly|probably|might|could|unsure|uncertain|however|actually|instead|but)\b|\bnot sure\b",text):
  return dict(label=None,status='review',reason='hedge_or_correction',format_ok=False)
 head=re.sub(r'^(?:a|an|the)\s+','',text)
 matched=None
 for name in sorted(NAMES,key=len,reverse=True):
  if head.startswith(name):
   suffix=head[len(name):]
   # Name ends at punctuation/end, never at a longer name such as apple juice.
   if not suffix or re.match(r'^\s*[.,!?;:\n()\[\]]',suffix) or re.match(r'^\s+(?:[-–—]|or\b)',suffix):
    matched=(name,NAMES[name],suffix);break
 if matched is None:
  return dict(label=None,status='review',reason='unrecognized_or_noncanonical_answer',format_ok=None)
 name,label,suffix=matched
 format_ok=not suffix.strip(' .!?:;')
 if re.match(r'^\s+or\b',suffix):return dict(label=None,status='review',reason='answer_alternatives',format_ok=False)
 # Extra concept mentions can be alternatives or comparisons. Both require review.
 mentioned=set()
 for alias,other in NAMES.items():
  if other!='none' and re.search(name_pattern(alias),suffix):mentioned.add(other)
 if any(other!=label for other in mentioned):
  return dict(label=None,status='review',reason='other_name_in_explanation',format_ok=False)
 if label=='none':
  if not suffix.strip(' .!?:;'):
   return dict(label=label,status='parsed',reason='explicit_none',format_ok=True)
  if re.search(r'\bor\b',suffix) and not re.search(r'\bdoes not (?:describe|mention) or (?:relate|refer)\b',suffix):
   return dict(label=None,status='review',reason='unresolved_or_in_none_explanation',format_ok=False)
  # Accept explanations explicitly stating absence or irrelevance; never ignore
  # arbitrary text after None. Unknown positive explanations remain ungraded.
  domain=r'(?:fruits?|animals?|(?:musical )?instruments?)'
  absence=re.search(r"\b(?:does not|doesn't|cannot|can't) (?:describe|provide|mention|relate|refer|correspond|match|pertain|identify)\b[^.!?;]{0,140}\b"+domain+r'\b',suffix)
  absence=absence or re.search(r'\b(?:not|no|unrelated to)\s+(?:(?:a|an|any|specific|about|to|the)\s+){0,4}'+domain+r'\b',suffix)
  positive_restatement=re.search(r'[.;]\s*(?:it|this) (?:is|describes|depicts) (?:a|an)\b',suffix)
  if not absence or positive_restatement:
   return dict(label=None,status='review',reason='unverified_none_explanation',format_ok=False)
  return dict(label=label,status='parsed',reason='none_with_negative_explanation',format_ok=False)
 if re.search(r"\b(not|neither|isn't|aren't|cannot|can't)\b",suffix):
  return dict(label=None,status='review',reason='negation_in_name_explanation',format_ok=False)
 return dict(label=label,status='parsed',reason='recognized_answer_name',format_ok=format_ok)
def grade(answer,target,truncated=False):
 if target not in RULES['aliases'] and target!='none':raise ValueError('Unsupported target')
 result=parse(answer)
 correct=None if result['status']=='review' else result['label']==target
 return dict(correct=correct,status='review' if correct is None else 'correct' if correct else 'incorrect',parsed_label=result['label'],reason=result['reason'],format_ok=result['format_ok'],truncated=bool(truncated),needs_review=bool(correct is None or truncated))
