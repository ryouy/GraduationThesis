import unittest
from run import grade,validate
class RulesTest(unittest.TestCase):
 def test_synonyms(self):
  self.assertTrue(grade('A fiddle.','violin')['correct'])
  self.assertTrue(grade('African elephants','elephant')['correct'])
 def test_no_substring_or_broad_label(self):
  self.assertFalse(grade('Pineapple','apple')['correct'])
  self.assertFalse(grade('Keyboard','piano')['correct'])
 def test_reject_ambiguous_or_negative(self):
  self.assertFalse(grade('A violin or piano','violin')['correct'])
  self.assertFalse(grade('Not a banana','banana')['correct'])
 def test_none(self):
  self.assertTrue(grade('None.','none')['correct'])
  self.assertFalse(grade('Apple','none')['correct'])
 def test_data_integrity(self):validate()
if __name__=='__main__':unittest.main()
