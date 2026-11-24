# Pre-main experiment — exploratory
- Run: 20261124_pre_main_v1
- Source: a9095b153ff869556bcf3fbba4dddee6a43b305a
- 10 fixed X/Y pairs, 10 categories; 240 cues; 500 prompts; 500 single generations.
- 20 related cues per concept and condition; unrelated and no-cue excluded from distance regression.
- Probe L22/23/24 restored from v5 cached training features, AUC matched on its independent text set.
- Cue distance bands are within-concept empirical quintiles; not common numerical cutoffs.
- AI-generated cues and prewritten definitions, no independent human audit. Style imbalance is logged in cue_quality.csv.
- Probe scores are relative X/Y information; Lens margins are teacher-forced candidate sequence log probabilities.
- No claim of thought quantity, causal suppression, or confirmatory significance.

## Final-layer results

| metric     | target_x   | condition   |   layer |   n |   slope |   intercept |   pearson_r |   spearman_rho |
|:-----------|:-----------|:------------|--------:|----:|--------:|------------:|------------:|---------------:|
| Logit Lens | ant        | Avoid X     |      24 |  20 |  17.383 |      -7.871 |       0.708 |          0.672 |
| Logit Lens | ant        | Neutral X   |      24 |  20 |  16.226 |      -7.602 |       0.641 |          0.677 |
| Logit Lens | banana     | Avoid X     |      24 |  20 |   2.331 |       2.252 |       0.066 |          0.126 |
| Logit Lens | banana     | Neutral X   |      24 |  20 |   1.327 |       4.45  |       0.045 |          0.021 |
| Logit Lens | bicycle    | Avoid X     |      24 |  20 | -28.932 |      29.146 |      -0.704 |         -0.741 |
| Logit Lens | bicycle    | Neutral X   |      24 |  20 | -25.984 |      28.943 |      -0.685 |         -0.705 |
| Logit Lens | bookshelf  | Avoid X     |      24 |  20 |  -0.393 |       6.38  |      -0.018 |          0.08  |
| Logit Lens | bookshelf  | Neutral X   |      24 |  20 |  -4.222 |       8.284 |      -0.188 |         -0.008 |
| Logit Lens | cactus     | Avoid X     |      24 |  20 |   1.752 |      10.027 |       0.076 |          0.009 |
| Logit Lens | cactus     | Neutral X   |      24 |  20 |   0.497 |      12.761 |       0.028 |         -0.021 |
| Logit Lens | drum       | Avoid X     |      24 |  20 |   1.698 |       6.829 |       0.141 |          0.141 |
| Logit Lens | drum       | Neutral X   |      24 |  20 |   2.239 |       7.176 |       0.197 |          0.192 |
| Logit Lens | elephant   | Avoid X     |      24 |  20 |   5.749 |      -0.465 |       0.153 |          0.179 |
| Logit Lens | elephant   | Neutral X   |      24 |  20 |   5.845 |       0.165 |       0.162 |          0.156 |
| Logit Lens | jellyfish  | Avoid X     |      24 |  20 |   3.617 |      -0.121 |       0.228 |          0.281 |
| Logit Lens | jellyfish  | Neutral X   |      24 |  20 |   4.134 |       1.817 |       0.277 |          0.287 |
| Logit Lens | rain       | Avoid X     |      24 |  20 | -14.042 |      10.547 |      -0.477 |         -0.543 |
| Logit Lens | rain       | Neutral X   |      24 |  20 | -12.74  |      10.751 |      -0.493 |         -0.549 |
| Logit Lens | scissors   | Avoid X     |      24 |  20 |  -1.281 |       3.031 |      -0.146 |         -0.096 |
| Logit Lens | scissors   | Neutral X   |      24 |  20 |  -2.514 |       5.508 |      -0.283 |         -0.198 |
| Probe      | ant        | Avoid X     |      24 |  20 |   7.929 |      -0.56  |       0.414 |          0.302 |
| Probe      | ant        | Neutral X   |      24 |  20 |   8.771 |      -0.886 |       0.427 |          0.337 |
| Probe      | banana     | Avoid X     |      24 |  20 |  -5.972 |       2.898 |      -0.188 |         -0.167 |
| Probe      | banana     | Neutral X   |      24 |  20 |  -7.647 |       4.022 |      -0.242 |         -0.205 |
| Probe      | bicycle    | Avoid X     |      24 |  20 | -18.5   |      16.228 |      -0.741 |         -0.802 |
| Probe      | bicycle    | Neutral X   |      24 |  20 | -16.307 |      15.443 |      -0.726 |         -0.818 |
| Probe      | bookshelf  | Avoid X     |      24 |  20 |  14.806 |     -11.543 |       0.655 |          0.605 |
| Probe      | bookshelf  | Neutral X   |      24 |  20 |  11.461 |      -8.55  |       0.646 |          0.651 |
| Probe      | cactus     | Avoid X     |      24 |  20 |  12.773 |      -7.325 |       0.606 |          0.568 |
| Probe      | cactus     | Neutral X   |      24 |  20 |   9.451 |      -6.357 |       0.633 |          0.62  |
| Probe      | drum       | Avoid X     |      24 |  20 |  -0.576 |      -4.927 |      -0.022 |         -0.063 |
| Probe      | drum       | Neutral X   |      24 |  20 |   0.343 |      -5.333 |       0.014 |         -0.066 |
| Probe      | elephant   | Avoid X     |      24 |  20 |   2.592 |      -2.305 |       0.105 |          0.177 |
| Probe      | elephant   | Neutral X   |      24 |  20 |  -0.033 |      -0.854 |      -0.002 |          0.045 |
| Probe      | jellyfish  | Avoid X     |      24 |  20 |   7.386 |      -4.104 |       0.275 |          0.269 |
| Probe      | jellyfish  | Neutral X   |      24 |  20 |   8.525 |      -4.843 |       0.362 |          0.314 |
| Probe      | rain       | Avoid X     |      24 |  20 | -11.711 |       6.723 |      -0.521 |         -0.57  |
| Probe      | rain       | Neutral X   |      24 |  20 | -10.523 |       6.198 |      -0.514 |         -0.532 |
| Probe      | scissors   | Avoid X     |      24 |  20 | -14.349 |       8.681 |      -0.896 |         -0.544 |
| Probe      | scissors   | Neutral X   |      24 |  20 | -14.92  |       9.913 |      -0.905 |         -0.611 |

## Paired slope difference

| metric     | target_x   |   layer |   n |   slope |   intercept |   pearson_r |   spearman_rho |
|:-----------|:-----------|--------:|----:|--------:|------------:|------------:|---------------:|
| Logit Lens | ant        |      24 |  20 |   1.157 |      -0.269 |       0.189 |          0.069 |
| Logit Lens | banana     |      24 |  20 |   1.004 |      -2.199 |       0.099 |          0.259 |
| Logit Lens | bicycle    |      24 |  20 |  -2.947 |       0.203 |      -0.57  |         -0.544 |
| Logit Lens | bookshelf  |      24 |  20 |   3.829 |      -1.904 |       0.396 |          0.269 |
| Logit Lens | cactus     |      24 |  20 |   1.254 |      -2.734 |       0.163 |          0.242 |
| Logit Lens | drum       |      24 |  20 |  -0.541 |      -0.347 |      -0.156 |         -0.18  |
| Logit Lens | elephant   |      24 |  20 |  -0.096 |      -0.63  |      -0.013 |          0     |
| Logit Lens | jellyfish  |      24 |  20 |  -0.517 |      -1.938 |      -0.047 |         -0.036 |
| Logit Lens | rain       |      24 |  20 |  -1.303 |      -0.204 |      -0.267 |         -0.117 |
| Logit Lens | scissors   |      24 |  20 |   1.233 |      -2.477 |       0.243 |          0.101 |
| Probe      | ant        |      24 |  20 |  -0.842 |       0.326 |      -0.262 |         -0.254 |
| Probe      | banana     |      24 |  20 |   1.675 |      -1.124 |       0.271 |          0.329 |
| Probe      | bicycle    |      24 |  20 |  -2.193 |       0.785 |      -0.551 |         -0.552 |
| Probe      | bookshelf  |      24 |  20 |   3.345 |      -2.993 |       0.45  |          0.214 |
| Probe      | cactus     |      24 |  20 |   3.322 |      -0.968 |       0.49  |          0.493 |
| Probe      | drum       |      24 |  20 |  -0.919 |       0.406 |      -0.263 |         -0.389 |
| Probe      | elephant   |      24 |  20 |   2.625 |      -1.451 |       0.365 |          0.331 |
| Probe      | jellyfish  |      24 |  20 |  -1.139 |       0.739 |      -0.205 |         -0.239 |
| Probe      | rain       |      24 |  20 |  -1.188 |       0.525 |      -0.404 |         -0.334 |
| Probe      | scissors   |      24 |  20 |   0.571 |      -1.232 |       0.258 |          0.253 |

## L22 exploratory follow-up

| metric     | target_x   | condition   |   layer |   n |   slope |   intercept |   pearson_r |   spearman_rho |
|:-----------|:-----------|:------------|--------:|----:|--------:|------------:|------------:|---------------:|
| Logit Lens | ant        | Avoid X     |      22 |  20 |  26.853 |     -12.285 |       0.856 |          0.743 |
| Logit Lens | banana     | Avoid X     |      22 |  20 |   0.399 |       3.899 |       0.014 |          0.062 |
| Logit Lens | bicycle    | Avoid X     |      22 |  20 | -20.862 |      15.731 |      -0.619 |         -0.726 |
| Logit Lens | bookshelf  | Avoid X     |      22 |  20 |   6.649 |       4.045 |       0.333 |          0.316 |
| Logit Lens | cactus     | Avoid X     |      22 |  20 |  -5.088 |      13.616 |      -0.311 |         -0.361 |
| Logit Lens | drum       | Avoid X     |      22 |  20 |  -2.691 |      24.81  |      -0.197 |         -0.281 |
| Logit Lens | elephant   | Avoid X     |      22 |  20 |   2.176 |      -0.317 |       0.081 |          0     |
| Logit Lens | jellyfish  | Avoid X     |      22 |  20 |   3.905 |      -8.253 |       0.189 |          0.143 |
| Logit Lens | rain       | Avoid X     |      22 |  20 | -11.603 |       8.752 |      -0.393 |         -0.371 |
| Logit Lens | scissors   | Avoid X     |      22 |  20 |  -5.402 |      -0.462 |      -0.41  |         -0.343 |
| Probe      | ant        | Avoid X     |      22 |  20 |  27.109 |     -12.096 |       0.665 |          0.579 |
| Probe      | banana     | Avoid X     |      22 |  20 | -18.575 |       3.237 |      -0.282 |         -0.242 |
| Probe      | bicycle    | Avoid X     |      22 |  20 | -29.219 |      24.865 |      -0.757 |         -0.836 |
| Probe      | bookshelf  | Avoid X     |      22 |  20 |  23.131 |     -16.281 |       0.706 |          0.716 |
| Probe      | cactus     | Avoid X     |      22 |  20 |  21.166 |     -10.911 |       0.582 |          0.582 |
| Probe      | drum       | Avoid X     |      22 |  20 |  -1.025 |      -1.572 |      -0.029 |         -0.114 |
| Probe      | elephant   | Avoid X     |      22 |  20 |  10.459 |     -12.271 |       0.198 |          0.167 |
| Probe      | jellyfish  | Avoid X     |      22 |  20 |  12.555 |      -9.953 |       0.346 |          0.359 |
| Probe      | rain       | Avoid X     |      22 |  20 | -17.58  |       7.089 |      -0.392 |         -0.341 |
| Probe      | scissors   | Avoid X     |      22 |  20 | -26.086 |      12.265 |      -0.869 |         -0.454 |

## Generation quality
- Empty: 0; truncation: 0
- Explicit mention is surface matching only; one generation per input is a supplemental outcome.
