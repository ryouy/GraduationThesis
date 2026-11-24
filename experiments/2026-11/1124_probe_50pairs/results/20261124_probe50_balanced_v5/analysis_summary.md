# Probe50 — balanced text-type follow-up v2

- Run ID: \`20261124_probe50_balanced_v5\`
- Fixed 50 X/Y candidate pairs; unique concepts: 82
- Inputs: 1312 sentences (8 train + 8 held-out per concept)
- Balanced 4 styles per split: structure, action, situation, function (2 per style).
- L24 AUC>=0.80: **35/50** (v1: **17/50**)
- L24 AUC>=0.80 and uncorrected p<=0.05: **33/50**
- L24 AUC>=0.80 and BH q<=0.05: **33/50**
- Median L24 AUC, v1: **0.742**; v2: **0.906**
- Mean delta (v2-v1): **+0.162**; median delta: **+0.164**
- Pairs changing AUC>=0.80 classification: **20**

## Scientific interpretation

- v1-v2 differences are descriptive: new facts and API stochasticity also changed.
- Surface checks do not guarantee semantic fact independence or unbiased category/stylistic coverage.
- AI-generated statements have not been human fact-checked; Probe AUC is X/Y decodability, not suppression or absolute concept activation.
- Treat permutation p and BH q as exploratory diagnostics and report ALL 50 candidates.

## By category

| Category | v1 AUC≥0.8 | v2 AUC≥0.8 | v1 median AUC | v2 median AUC |
|---|---:|---:|---:|---:|
| fruits | 1 | 3 | 0.531 | 0.844 |
| furniture | 2 | 3 | 0.609 | 0.812 |
| insects | 2 | 5 | 0.797 | 1.000 |
| land_mammals | 1 | 3 | 0.609 | 0.906 |
| marine_animals | 1 | 3 | 0.547 | 0.844 |
| musical_instruments | 0 | 2 | 0.688 | 0.797 |
| natural_phenomena | 4 | 5 | 0.891 | 1.000 |
| plants | 0 | 4 | 0.688 | 0.906 |
| tools | 1 | 2 | 0.766 | 0.781 |
| vehicles | 5 | 5 | 1.000 | 1.000 |
