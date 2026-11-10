# Qwen Concept Probe Robustness — Run Summary

- Model: `Qwen/Qwen2.5-0.5B-Instruct`
- Revision: `7ae557604adf67be50417f59c2c2f167def9a775`
- Pairs: 20
- Unique prompts: 5200
- Exact shuffled fits: 30,240

## Pair summary

| pair         | comparison   |   folds |   mean_neutral_auc |   median_neutral_auc |   min_neutral_auc |   max_neutral_auc |   folds_auc_ge_075 |   folds_auc_ge_080 |   median_shuffle_upper_tail_proportion |   folds_shuffle_p_le_005 |   median_worst_family_drop_auc | exploratory_stable_candidate   |
|:-------------|:-------------|--------:|-------------------:|---------------------:|------------------:|------------------:|-------------------:|-------------------:|---------------------------------------:|-------------------------:|-------------------------------:|:-------------------------------|
| banana       | apple        |       6 |           0.786667 |                 0.8  |              0.64 |              0.88 |                  4 |                  4 |                              0.0615079 |                        3 |                        0.71875 | False                          |
| bicycle      | motorcycle   |       6 |           0.68     |                 0.68 |              0.64 |              0.72 |                  0 |                  0 |                              0.142857  |                        0 |                        0.625   | False                          |
| boat         | submarine    |       6 |           1        |                 1    |              1    |              1    |                  6 |                  6 |                              0.0436508 |                        5 |                        1       | True                           |
| bread        | rice         |       6 |           0.946667 |                 0.92 |              0.92 |              1    |                  6 |                  6 |                              0.0218254 |                        6 |                        0.875   | True                           |
| butterfly    | spider       |       6 |           0.92     |                 0.92 |              0.88 |              0.96 |                  6 |                  6 |                              0.0337302 |                        5 |                        0.875   | True                           |
| camera       | telescope    |       6 |           1        |                 1    |              1    |              1    |                  6 |                  6 |                              0.0456349 |                        4 |                        1       | False                          |
| carrot       | potato       |       6 |           0.7      |                 0.68 |              0.6  |              0.84 |                  2 |                  1 |                              0.144841  |                        1 |                        0.5     | False                          |
| cat          | dog          |       6 |           0.893333 |                 0.92 |              0.8  |              0.96 |                  6 |                  6 |                              0.0456349 |                        3 |                        0.875   | False                          |
| clock        | calendar     |       6 |           1        |                 1    |              1    |              1    |                  6 |                  6 |                              0.0416667 |                        5 |                        1       | True                           |
| dolphin      | shark        |       6 |           0.82     |                 0.82 |              0.68 |              1    |                  4 |                  4 |                              0.103175  |                        1 |                        0.71875 | False                          |
| eagle        | penguin      |       6 |           0.646667 |                 0.64 |              0.6  |              0.72 |                  0 |                  0 |                              0.384921  |                        0 |                        0.53125 | False                          |
| elephant     | giraffe      |       6 |           0.72     |                 0.72 |              0.56 |              0.84 |                  2 |                  1 |                              0.18254   |                        0 |                        0.5625  | False                          |
| hammer       | screwdriver  |       6 |           0.993333 |                 1    |              0.96 |              1    |                  6 |                  6 |                              0.0595238 |                        0 |                        1       | False                          |
| lemon        | orange       |       6 |           0.826667 |                 0.84 |              0.8  |              0.84 |                  6 |                  6 |                              0.0833333 |                        1 |                        0.75    | False                          |
| lion         | tiger        |       6 |           0.746667 |                 0.74 |              0.68 |              0.88 |                  3 |                  1 |                              0.160714  |                        1 |                        0.65625 | False                          |
| piano        | violin       |       6 |           0.626667 |                 0.62 |              0.56 |              0.68 |                  0 |                  0 |                              0.212302  |                        0 |                        0.40625 | False                          |
| refrigerator | oven         |       6 |           1        |                 1    |              1    |              1    |                  6 |                  6 |                              0.0734127 |                        0 |                        1       | False                          |
| rose         | sunflower    |       6 |           1        |                 1    |              1    |              1    |                  6 |                  6 |                              0.015873  |                        6 |                        1       | True                           |
| scissors     | knife        |       6 |           0.913333 |                 0.92 |              0.84 |              0.96 |                  6 |                  6 |                              0.0853175 |                        1 |                        0.875   | False                          |
| train        | airplane     |       6 |           0.933333 |                 0.92 |              0.92 |              0.96 |                  6 |                  6 |                              0.0416667 |                        5 |                        0.875   | True                           |

## Condition / layer / position summary

|   layer | position        | condition   |   mean_family_auc |   median_family_auc |   proportion_auc_ge_075 |   proportion_auc_ge_080 |   n_pair_fold_fits |
|--------:|:----------------|:------------|------------------:|--------------------:|------------------------:|------------------------:|-------------------:|
|      22 | assistant_start | avoid_x     |          0.851333 |                0.88 |                0.741667 |                0.658333 |                120 |
|      22 | assistant_start | mention_x   |          0.861    |                0.88 |                0.725    |                0.683333 |                120 |
|      22 | assistant_start | neutral     |          0.846667 |                0.88 |                0.708333 |                0.658333 |                120 |
|      22 | assistant_start | think_x     |          0.861    |                0.88 |                0.783333 |                0.708333 |                120 |
|      22 | assistant_start | think_y     |          0.859333 |                0.88 |                0.808333 |                0.716667 |                120 |
|      22 | context_end     | avoid_x     |          0.613667 |                0.6  |                0.258333 |                0.208333 |                120 |
|      22 | context_end     | mention_x   |          0.604667 |                0.6  |                0.291667 |                0.216667 |                120 |
|      22 | context_end     | neutral     |          0.690333 |                0.72 |                0.45     |                0.408333 |                120 |
|      22 | context_end     | think_x     |          0.62     |                0.6  |                0.241667 |                0.183333 |                120 |
|      22 | context_end     | think_y     |          0.59     |                0.6  |                0.233333 |                0.141667 |                120 |
|      23 | assistant_start | avoid_x     |          0.859667 |                0.9  |                0.758333 |                0.658333 |                120 |
|      23 | assistant_start | mention_x   |          0.867667 |                0.92 |                0.766667 |                0.675    |                120 |
|      23 | assistant_start | neutral     |          0.860667 |                0.92 |                0.766667 |                0.675    |                120 |
|      23 | assistant_start | think_x     |          0.871    |                0.92 |                0.783333 |                0.708333 |                120 |
|      23 | assistant_start | think_y     |          0.867667 |                0.92 |                0.783333 |                0.716667 |                120 |
|      23 | context_end     | avoid_x     |          0.608333 |                0.6  |                0.283333 |                0.241667 |                120 |
|      23 | context_end     | mention_x   |          0.588    |                0.6  |                0.275    |                0.2      |                120 |
|      23 | context_end     | neutral     |          0.712    |                0.72 |                0.483333 |                0.416667 |                120 |
|      23 | context_end     | think_x     |          0.602667 |                0.6  |                0.225    |                0.183333 |                120 |
|      23 | context_end     | think_y     |          0.583    |                0.6  |                0.241667 |                0.166667 |                120 |
|      24 | assistant_start | avoid_x     |          0.867333 |                0.92 |                0.766667 |                0.7      |                120 |
|      24 | assistant_start | mention_x   |          0.87     |                0.92 |                0.758333 |                0.7      |                120 |
|      24 | assistant_start | neutral     |          0.857667 |                0.92 |                0.725    |                0.691667 |                120 |
|      24 | assistant_start | think_x     |          0.873667 |                0.92 |                0.808333 |                0.716667 |                120 |
|      24 | assistant_start | think_y     |          0.866333 |                0.92 |                0.791667 |                0.725    |                120 |
|      24 | context_end     | avoid_x     |          0.608333 |                0.6  |                0.333333 |                0.225    |                120 |
|      24 | context_end     | mention_x   |          0.61     |                0.6  |                0.308333 |                0.283333 |                120 |
|      24 | context_end     | neutral     |          0.722333 |                0.72 |                0.483333 |                0.416667 |                120 |
|      24 | context_end     | think_x     |          0.613333 |                0.64 |                0.275    |                0.216667 |                120 |
|      24 | context_end     | think_y     |          0.582333 |                0.6  |                0.208333 |                0.15     |                120 |

## Interpretation

This is an exploratory validation of an X-vs-Y Concept Probe. It does not establish absolute concept activation, thought, or causality.