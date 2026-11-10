# Phi prompt diagnostic: exploratory results

Raw answers require review; no model adoption decision is automatic.

condition,naming_correct,naming_n,none_correct,none_n,format_correct,truncations,clear_none_answers
A_original,44,60,12,12,44,1,5
B_best_match,46,60,5,12,47,0,0

Paired transitions:
```json
{
  "naming": {
    "correct -> correct": 42,
    "wrong -> correct": 4,
    "correct -> wrong": 2,
    "wrong -> wrong": 12
  },
  "none": {
    "correct -> correct": 5,
    "wrong -> correct": 0,
    "correct -> wrong": 7,
    "wrong -> wrong": 0
  }
}
```
