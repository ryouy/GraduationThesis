# Independent new-description confirmation: Qwen Concept Probe

- **Frozen primary targets:** 12; secondary near-misses: 4.
- **Newly authored evaluation statements:** 184 (8 per concept, 23 unique concepts).
- **Source:** previous frozen training vectors only; no old evaluation vectors in classifier fit.
- **Frozen directed comparisons:** 47; unique unordered pairs: 31.
- **New-text threshold-only pairs:** 16.
- **New-text threshold + shuffle-passing pairs:** 16.
- **New-text threshold + FDR-adjusted shuffle pairs:** 11.
- **Distinct targets replicating across >=2 Ys and >=2 semantic bands:** 5/16 (unadjusted), 4/16 (FDR-sensitivity).

## Target-by-target confirmation

| target     | tier      |   frozen_comparisons |   n_confirmed_unadjusted |   n_confirmed_bands_unadjusted | replicated_two_bands_unadjusted   |   n_confirmed_fdr |   n_confirmed_bands_fdr | replicated_two_bands_fdr   | confirmed_ys_unadjusted                          |   mean_L24_new_auc |   near_auc |   medium_auc |    far_auc |
|:-----------|:----------|---------------------:|-------------------------:|-------------------------------:|:----------------------------------|------------------:|------------------------:|:---------------------------|:-------------------------------------------------|-------------------:|-----------:|-------------:|-----------:|
| bus        | primary   |                    5 |                        5 |                              3 | True                              |                 4 |                       3 | True                       | boat, motorcycle, bicycle, submarine, helicopter |           0.965625 |   1        |     0.914062 |   1        |
| boat       | primary   |                    4 |                        4 |                              3 | True                              |                 3 |                       2 | True                       | train, bicycle, bus, motorcycle                  |           1        |   1        |     1        |   1        |
| motorcycle | primary   |                    5 |                        4 |                              2 | True                              |                 2 |                       2 | True                       | bus, train, helicopter, submarine                |           0.915625 |   0.765625 |     0.914062 |   0.992188 |
| bicycle    | primary   |                    4 |                        3 |                              3 | True                              |                 3 |                       3 | True                       | boat, train, submarine                           |           0.945312 |   1        |     0.890625 |   1        |
| submarine  | primary   |                    3 |                        3 |                              2 | True                              |                 0 |                       0 | False                      | car, bus, motorcycle                             |           0.984375 | nan        |     0.953125 |   1        |
| train      | secondary |                    2 |                        2 |                              1 | False                             |                 1 |                       1 | False                      | boat, bicycle                                    |           0.976562 | nan        |     0.976562 | nan        |
| ant        | primary   |                    2 |                        1 |                              1 | False                             |                 1 |                       1 | False                      | dragonfly                                        |           0.90625  | nan        |     0.828125 |   0.984375 |
| dragonfly  | primary   |                    3 |                        1 |                              1 | False                             |                 1 |                       1 | False                      | ant                                              |           0.869792 |   0.84375  |     0.882812 | nan        |
| elephant   | secondary |                    2 |                        1 |                              1 | False                             |                 1 |                       1 | False                      | lion                                             |           0.882812 | nan        |   nan        |   0.882812 |
| butterfly  | primary   |                    4 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.847656 |   0.84375  |     0.828125 |   0.859375 |
| car        | secondary |                    2 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.796875 | nan        |     0.796875 | nan        |
| jellyfish  | primary   |                    3 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.697917 |   0.625    |     0.859375 |   0.609375 |
| moth       | primary   |                    2 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.789062 | nan        |     0.78125  |   0.796875 |
| scorpion   | secondary |                    2 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.84375  | nan        |     0.84375  | nan        |
| starfish   | primary   |                    2 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.640625 | nan        |     0.625    |   0.65625  |
| wolf       | primary   |                    2 |                        0 |                              0 | False                             |                 0 |                       0 | False                      |                                                  |           0.757812 |   0.6875   |     0.828125 | nan        |

## Distance bands

| band   |   n |   mean_auc |   median_auc |   confirm_unadjusted |   confirm_fdr |   mean_distance |
|:-------|----:|-----------:|-------------:|---------------------:|--------------:|----------------:|
| far    |  16 |   0.907227 |     0.984375 |                   10 |             6 |        0.75007  |
| medium |  23 |   0.875679 |     0.890625 |                   11 |             8 |        0.652129 |
| near   |   8 |   0.845703 |     0.84375  |                    3 |             2 |        0.563248 |

**Interpretation:** AUC measures relative concept identity discrimination, not absolute activation or suppression. The newly written statements must be independently reviewed for factual validity, lack of duplicate semantic content, and target-label ambiguity. This is *not* a claim of independently human-verified confirmation.
