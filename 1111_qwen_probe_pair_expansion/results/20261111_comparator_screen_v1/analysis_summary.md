# Comparator-pair screening of 40 concepts

- **69 directed candidate contrasts** / **61 unique unordered contrasts**
- **21 unique contrasts** met exploratory stability criterion.
- **4 distinct targets** have at least two stable alternative Ys.
- Input: previously generated 5200 Qwen hidden-state records (no new model inference).
- Exact family-label permutations completed: 68,040 fits.

## Candidate targets by number of stable comparators

| target       |   stable_distinct_comparators | comparators    | two_comparators_stable   |
|:-------------|------------------------------:|:---------------|:-------------------------|
| apple        |                             2 | carrot, potato | True                     |
| butterfly    |                             2 | spider, shark  | True                     |
| dog          |                             2 | lion, tiger    | True                     |
| spider       |                             2 | shark, eagle   | True                     |
| banana       |                             1 | carrot         | False                    |
| boat         |                             1 | submarine      | False                    |
| bread        |                             1 | rice           | False                    |
| calendar     |                             1 | clock          | False                    |
| cat          |                             1 | lion           | False                    |
| clock        |                             1 | calendar       | False                    |
| elephant     |                             1 | cat            | False                    |
| lemon        |                             1 | banana         | False                    |
| lion         |                             1 | dolphin        | False                    |
| motorcycle   |                             1 | train          | False                    |
| potato       |                             1 | orange         | False                    |
| rice         |                             1 | bread          | False                    |
| rose         |                             1 | sunflower      | False                    |
| sunflower    |                             1 | rose           | False                    |
| tiger        |                             1 | elephant       | False                    |
| train        |                             1 | airplane       | False                    |
| airplane     |                             0 |                | False                    |
| bicycle      |                             0 |                | False                    |
| camera       |                             0 |                | False                    |
| carrot       |                             0 |                | False                    |
| dolphin      |                             0 |                | False                    |
| eagle        |                             0 |                | False                    |
| giraffe      |                             0 |                | False                    |
| hammer       |                             0 |                | False                    |
| knife        |                             0 |                | False                    |
| orange       |                             0 |                | False                    |
| oven         |                             0 |                | False                    |
| penguin      |                             0 |                | False                    |
| piano        |                             0 |                | False                    |
| refrigerator |                             0 |                | False                    |
| scissors     |                             0 |                | False                    |
| screwdriver  |                             0 |                | False                    |
| shark        |                             0 |                | False                    |
| submarine    |                             0 |                | False                    |
| telescope    |                             0 |                | False                    |
| violin       |                             0 |                | False                    |

## Pair-level screening results

| unordered_pair        | a            | b           | group                |   mean_auc |   min_auc |   median_auc |   folds_auc_ge_075 |   folds_auc_ge_080 |   median_worst_family_drop_auc | screen_pass   |   folds_shuffle_p_le_005 |   median_shuffle_p | exploratory_stable_pair   |
|:----------------------|:-------------|:------------|:---------------------|-----------:|----------:|-------------:|-------------------:|-------------------:|-------------------------------:|:--------------|-------------------------:|-------------------:|:--------------------------|
| bicycle__boat         | boat         | bicycle     | vehicles             |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        0 |         0.0753968  | False                     |
| bicycle__submarine    | submarine    | bicycle     | vehicles             |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        0 |         0.0992063  | False                     |
| boat__submarine       | boat         | submarine   | vehicles             |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        5 |         0.0436508  | True                      |
| boat__train           | train        | boat        | vehicles             |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        2 |         0.0535714  | False                     |
| butterfly__shark      | butterfly    | shark       | other_animals        |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.0297619  | True                      |
| calendar__clock       | clock        | calendar    | time_instruments     |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        5 |         0.0416667  | True                      |
| camera__telescope     | camera       | telescope   | optical_instruments  |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        4 |         0.0456349  | False                     |
| dog__lion             | dog          | lion        | mammals              |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.00595238 | True                      |
| dolphin__tiger        | tiger        | dolphin     | mammals              |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        4 |         0.0436508  | False                     |
| eagle__shark          | shark        | eagle       | other_animals        |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        1 |         0.0694444  | False                     |
| eagle__spider         | spider       | eagle       | other_animals        |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.0257937  | True                      |
| hammer__knife         | knife        | hammer      | tools                |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        4 |         0.0396825  | False                     |
| knife__screwdriver    | screwdriver  | knife       | tools                |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        0 |         0.0972222  | False                     |
| motorcycle__submarine | submarine    | motorcycle  | vehicles             |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        1 |         0.0793651  | False                     |
| oven__refrigerator    | refrigerator | oven        | household_appliances |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        0 |         0.0734127  | False                     |
| rose__sunflower       | rose         | sunflower   | flowers              |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.015873   | True                      |
| scissors__screwdriver | screwdriver  | scissors    | tools                |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        3 |         0.0496032  | False                     |
| shark__spider         | spider       | shark       | other_animals        |   1        |      1    |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.0198413  | True                      |
| hammer__screwdriver   | hammer       | screwdriver | tools                |   0.993333 |      0.96 |         1    |                  6 |                  6 |                        1       | True          |                        0 |         0.0595238  | False                     |
| motorcycle__train     | motorcycle   | train       | vehicles             |   0.993333 |      0.96 |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.0396825  | True                      |
| cat__lion             | cat          | lion        | mammals              |   0.986667 |      0.92 |         1    |                  6 |                  6 |                        1       | True          |                        6 |         0.0138889  | True                      |
| hammer__scissors      | hammer       | scissors    | tools                |   0.986667 |      0.92 |         1    |                  6 |                  6 |                        1       | True          |                        2 |         0.0535714  | False                     |
| airplane__motorcycle  | motorcycle   | airplane    | vehicles             |   0.98     |      0.96 |         0.98 |                  6 |                  6 |                        0.96875 | True          |                        2 |         0.0595238  | False                     |
| airplane__boat        | airplane     | boat        | vehicles             |   0.966667 |      0.92 |         0.98 |                  6 |                  6 |                        0.96875 | True          |                        4 |         0.031746   | False                     |
| orange__potato        | potato       | orange      | produce              |   0.966667 |      0.92 |         0.98 |                  6 |                  6 |                        0.96875 | True          |                        6 |         0.00992063 | True                      |
| airplane__submarine   | airplane     | submarine   | vehicles             |   0.96     |      0.96 |         0.96 |                  6 |                  6 |                        0.9375  | True          |                        0 |         0.126984   | False                     |
| dog__tiger            | dog          | tiger       | mammals              |   0.96     |      0.92 |         0.96 |                  6 |                  6 |                        0.9375  | True          |                        6 |         0.0257937  | True                      |
| banana__carrot        | banana       | carrot      | produce              |   0.96     |      0.76 |         1    |                  6 |                  5 |                        1       | True          |                        6 |         0.00992063 | True                      |
| apple__carrot         | apple        | carrot      | produce              |   0.953333 |      0.88 |         0.96 |                  6 |                  6 |                        0.9375  | True          |                        6 |         0.0119048  | True                      |
| bread__rice           | bread        | rice        | staple_foods         |   0.946667 |      0.92 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        6 |         0.0218254  | True                      |
| dolphin__lion         | lion         | dolphin     | mammals              |   0.94     |      0.88 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        5 |         0.0198413  | True                      |
| airplane__train       | train        | airplane    | vehicles             |   0.933333 |      0.92 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        5 |         0.0416667  | True                      |
| apple__potato         | apple        | potato      | produce              |   0.92     |      0.88 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        6 |         0.0198413  | True                      |
| butterfly__spider     | butterfly    | spider      | other_animals        |   0.92     |      0.88 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        5 |         0.0337302  | True                      |
| banana__lemon         | lemon        | banana      | produce              |   0.913333 |      0.84 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        6 |         0.0119048  | True                      |
| elephant__tiger       | tiger        | elephant    | mammals              |   0.913333 |      0.88 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        6 |         0.0218254  | True                      |
| knife__scissors       | scissors     | knife       | tools                |   0.913333 |      0.84 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        1 |         0.0853175  | False                     |
| dolphin__elephant     | dolphin      | elephant    | mammals              |   0.906667 |      0.84 |         0.92 |                  6 |                  6 |                        0.875   | True          |                        4 |         0.0416667  | False                     |
| penguin__shark        | shark        | penguin     | other_animals        |   0.9      |      0.76 |         0.92 |                  6 |                  5 |                        0.875   | True          |                        1 |         0.0992063  | False                     |
| cat__dog              | cat          | dog         | mammals              |   0.893333 |      0.8  |         0.92 |                  6 |                  6 |                        0.875   | True          |                        3 |         0.0456349  | False                     |
| butterfly__eagle      | eagle        | butterfly   | other_animals        |   0.886667 |      0.84 |         0.88 |                  6 |                  6 |                        0.8125  | True          |                        1 |         0.0615079  | False                     |
| cat__elephant         | elephant     | cat         | mammals              |   0.846667 |      0.76 |         0.86 |                  6 |                  5 |                        0.78125 | True          |                        5 |         0.0357143  | True                      |
| lemon__orange         | lemon        | orange      | produce              |   0.826667 |      0.8  |         0.84 |                  6 |                  6 |                        0.75    | True          |                        1 |         0.0833333  | False                     |
| dolphin__giraffe      | dolphin      | giraffe     | mammals              |   0.82     |      0.76 |         0.84 |                  6 |                  5 |                        0.75    | True          |                        2 |         0.0753968  | False                     |
| lemon__potato         | potato       | lemon       | produce              |   0.793333 |      0.6  |         0.82 |                  5 |                  4 |                        0.71875 | True          |                        1 |         0.115079   | False                     |
| dolphin__shark        | dolphin      | shark       | mammals              |   0.82     |      0.68 |         0.82 |                  4 |                  4 |                        0.71875 | False         |                      nan |       nan          | False                     |
| bicycle__train        | bicycle      | train       | vehicles             |   0.793333 |      0.76 |         0.78 |                  6 |                  3 |                        0.65625 | False         |                      nan |       nan          | False                     |
| dog__giraffe          | giraffe      | dog         | mammals              |   0.786667 |      0.68 |         0.8  |                  5 |                  3 |                        0.6875  | False         |                      nan |       nan          | False                     |
| apple__banana         | banana       | apple       | produce              |   0.786667 |      0.64 |         0.8  |                  4 |                  4 |                        0.71875 | False         |                      nan |       nan          | False                     |
| carrot__lemon         | carrot       | lemon       | produce              |   0.773333 |      0.72 |         0.78 |                  4 |                  3 |                        0.71875 | False         |                      nan |       nan          | False                     |
| lion__tiger           | lion         | tiger       | mammals              |   0.746667 |      0.68 |         0.74 |                  3 |                  1 |                        0.65625 | False         |                      nan |       nan          | False                     |
| butterfly__penguin    | penguin      | butterfly   | other_animals        |   0.74     |      0.68 |         0.74 |                  3 |                  1 |                        0.65625 | False         |                      nan |       nan          | False                     |
| elephant__giraffe     | elephant     | giraffe     | mammals              |   0.72     |      0.56 |         0.72 |                  2 |                  1 |                        0.5625  | False         |                      nan |       nan          | False                     |
| penguin__spider       | penguin      | spider      | other_animals        |   0.72     |      0.64 |         0.7  |                  2 |                  2 |                        0.59375 | False         |                      nan |       nan          | False                     |
| carrot__potato        | carrot       | potato      | produce              |   0.7      |      0.6  |         0.68 |                  2 |                  1 |                        0.5     | False         |                      nan |       nan          | False                     |
| apple__orange         | orange       | apple       | produce              |   0.693333 |      0.6  |         0.7  |                  1 |                  0 |                        0.5625  | False         |                      nan |       nan          | False                     |
| cat__giraffe          | giraffe      | cat         | mammals              |   0.686667 |      0.64 |         0.68 |                  1 |                  0 |                        0.625   | False         |                      nan |       nan          | False                     |
| bicycle__motorcycle   | bicycle      | motorcycle  | vehicles             |   0.68     |      0.64 |         0.68 |                  0 |                  0 |                        0.625   | False         |                      nan |       nan          | False                     |
| eagle__penguin        | eagle        | penguin     | other_animals        |   0.646667 |      0.6  |         0.64 |                  0 |                  0 |                        0.53125 | False         |                      nan |       nan          | False                     |
| piano__violin         | piano        | violin      | musical_instruments  |   0.626667 |      0.56 |         0.62 |                  0 |                  0 |                        0.40625 | False         |                      nan |       nan          | False                     |
| banana__orange        | orange       | banana      | produce              |   0.586667 |      0.48 |         0.56 |                  1 |                  0 |                        0.4375  | False         |                      nan |       nan          | False                     |

**Interpretation:** screening only. The selected 20 concept targets require new independently authored descriptions and matched semantic-distance cues to confirm out-of-sample performance.
