# White Bear / Zhou v3 — exploratory run

Model: `Qwen/Qwen2.5-0.5B-Instruct`; seed: `42`; generation samples: `5` per unique prompt.

## Behavioral performance (Zhou-inspired)

| Polarity | Word answers | Word answers (calibrated) | Letter answers (raw) | Letter answers (calibrated) |
|---|---:|---:|---:|---:|
| negative | 18.5% | 11.1% | 29.6% | 29.6% |
| positive | 100.0% | 100.0% | 66.7% | 88.9% |

## Interpretive limits
- Mann: forbidden words counted as singular or explicitly listed plural forms; semantic paraphrases not counted.
- Zhou: answer-word scores can still reflect lexical and token-length biases; only 6 word sets.
- Concept probe: X-versus-Y discrimination; use semantic-description held-out AUC before interpreting.
- This run is NOT an exact replication of either paper. No causal suppression/construction mechanism is identified.
- Exploratory paired uncertainty intervals resample independent concepts / word sets, not repeated draws.
- Every CSV and graph is preserved, including unexpected outcomes.
