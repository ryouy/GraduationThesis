import unittest
from grade_v2 import grade
class ContentTests(unittest.TestCase):
 def test_none_punctuation(self):
  for s in ['None','None.','None, as the context does not describe an animal.','None: no animal is described.','None (the context is not about an animal)','None - the context does not describe an animal.']:
   with self.subTest(s=s):self.assertTrue(grade(s,'none')['correct'])
 def test_negative_coordination_is_not_choice(self):
  self.assertTrue(grade('None. The context is about a cyclist and does not describe or relate to any animal.','none')['correct'])
 def test_subtypes_and_aliases(self):
  for s,t in [('Green apple','apple'),('red apples','apple'),('Grand Piano','piano'),('Upright piano','piano'),('Fiddles','violin'),('**Banana**','banana'),('An apple.','apple')]:
   with self.subTest(s=s):self.assertTrue(grade(s,t)['correct'])
 def test_wrong_names(self):
  for s,t in [('Mango','banana'),('Giraffe','elephant'),('Harp','piano'),('Viola','violin'),('None','banana'),('Apple','none'),('Keyboard','piano'),('Plantain','banana')]:
   with self.subTest(s=s):self.assertFalse(grade(s,t)['correct'])
 def test_unknown_needs_review(self):
  for s in ['Apple juice','African elephant','Bananaland','It is a banana.','None of these','', 'Persimmon']:
   with self.subTest(s=s):self.assertIsNone(grade(s,'banana')['correct'])
 def test_contradictions_alternatives_hedges(self):
  for s in ['None, but it is a banana.','None. Actually a pear.','None. A dragon is described.','Banana or apple','Banana or something else','Banana. It is not a banana.','Maybe banana','Banana. It could be an apple.','None. It is not fruit or it is a vegetable.']:
   with self.subTest(s=s):self.assertIsNone(grade(s,'banana' if not s.startswith('None') else 'none')['correct'])
 def test_format_is_independent_of_content(self):
  x=grade('Mango','banana');self.assertFalse(x['correct']);self.assertTrue(x['format_ok'])
  x=grade('None, as no fruit is described.','none');self.assertTrue(x['correct']);self.assertFalse(x['format_ok'])
 def test_truncation_is_flagged(self):
  x=grade('Banana','banana',True);self.assertTrue(x['correct']);self.assertTrue(x['needs_review'])
 def test_incidental_negation_does_not_validate_none(self):
  for s in ['None. No doubt it is a dragon.','None. The context is not short; it describes a dragon.','None. There is no wind.']:
   with self.subTest(s=s):self.assertIsNone(grade(s,'none')['correct'])
 def test_positive_restatement_is_reviewed(self):
  self.assertIsNone(grade('None. It is not an animal; it is a persimmon.','none')['correct'])
 def test_harmless_or_in_description(self):
  self.assertTrue(grade('Banana. The skin is yellow or green.','banana')['correct'])
if __name__=='__main__':unittest.main()
