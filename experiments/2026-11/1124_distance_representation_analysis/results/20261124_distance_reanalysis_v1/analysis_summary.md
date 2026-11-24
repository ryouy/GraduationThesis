# Exploratory distance–representation reanalysis
Source commit: 97a9c30fb836a1bf6b16af6e31e0611293ea8f0e

4 vehicle concepts; 12 related cues per concept and condition. No new model inference.
Unrelated and no-cue controls are excluded from distance regression.

## Layer 24: descriptive results

| metric     | target_x   | condition   |   layer |   n |   slope |   intercept |   pearson_r |   spearman_rho |
|:-----------|:-----------|:------------|--------:|----:|--------:|------------:|------------:|---------------:|
| Logit Lens | bicycle    | Avoid X     |      24 |  12 |  -4.116 |      13.964 |      -0.254 |         -0.42  |
| Logit Lens | bicycle    | Neutral X   |      24 |  12 |  -2.208 |      13.921 |      -0.168 |         -0.182 |
| Logit Lens | boat       | Avoid X     |      24 |  12 |  -8.371 |      13.12  |      -0.581 |         -0.559 |
| Logit Lens | boat       | Neutral X   |      24 |  12 |  -6.621 |      12.424 |      -0.517 |         -0.434 |
| Logit Lens | bus        | Avoid X     |      24 |  12 |  -5.815 |      12.66  |      -0.433 |         -0.266 |
| Logit Lens | bus        | Neutral X   |      24 |  12 |  -5.072 |      13.005 |      -0.483 |         -0.385 |
| Logit Lens | motorcycle | Avoid X     |      24 |  12 |   8.306 |       0.976 |       0.569 |          0.399 |
| Logit Lens | motorcycle | Neutral X   |      24 |  12 |   6.404 |       3.104 |       0.574 |          0.357 |
| Probe      | bicycle    | Avoid X     |      24 |  12 |  -1.433 |       0.705 |      -0.251 |         -0.126 |
| Probe      | bicycle    | Neutral X   |      24 |  12 |  -1.52  |       0.961 |      -0.303 |         -0.252 |
| Probe      | boat       | Avoid X     |      24 |  12 |   2.816 |       1.872 |       0.337 |          0.203 |
| Probe      | boat       | Neutral X   |      24 |  12 |   3.24  |       1.346 |       0.413 |          0.252 |
| Probe      | bus        | Avoid X     |      24 |  12 |  -5.133 |       7.246 |      -0.598 |         -0.385 |
| Probe      | bus        | Neutral X   |      24 |  12 |  -5.291 |       7.831 |      -0.64  |         -0.434 |
| Probe      | motorcycle | Avoid X     |      24 |  12 |   1.327 |       1.604 |       0.241 |          0.182 |
| Probe      | motorcycle | Neutral X   |      24 |  12 |   1.177 |       2.316 |       0.252 |          0.168 |

## Paired slope differences (Avoid minus Neutral)

| metric     | target_x   |   layer |   n |   slope |   intercept |   pearson_r |   spearman_rho |
|:-----------|:-----------|--------:|----:|--------:|------------:|------------:|---------------:|
| Logit Lens | bicycle    |      24 |  12 |  -1.908 |       0.044 |      -0.497 |         -0.671 |
| Logit Lens | boat       |      24 |  12 |  -1.751 |       0.695 |      -0.586 |         -0.643 |
| Logit Lens | bus        |      24 |  12 |  -0.742 |      -0.344 |      -0.124 |         -0.105 |
| Logit Lens | motorcycle |      24 |  12 |   1.902 |      -2.128 |       0.329 |          0.217 |
| Probe      | bicycle    |      24 |  12 |   0.087 |      -0.256 |       0.081 |          0.105 |
| Probe      | boat       |      24 |  12 |  -0.424 |       0.526 |      -0.337 |         -0.336 |
| Probe      | bus        |      24 |  12 |   0.158 |      -0.585 |       0.089 |          0.168 |
| Probe      | motorcycle |      24 |  12 |   0.15  |      -0.712 |       0.066 |          0.035 |

## Limitations
- Exploratory reuse of pilot data; no confirmatory hypothesis test.
- All four concepts are vehicles; stimulus distance and content may covary.
- AI-audited cues lack independent human validation.
- Probe is relative X/Y discrimination, not absolute concept activation.
- Logit Lens uses teacher-forced fixed candidate sequence log-probability margins.
- Neutral and Avoid instructions differ in wording; contrasts are not pure causal suppression effects.
- Layers are not generation time; generation repetitions are not independent hidden states.