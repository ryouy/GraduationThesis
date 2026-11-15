# Qwen Concept Probe 100 concepts — exploratory screen

- Concepts: 100 in 10 categories
- Source model: Qwen/Qwen2.5-0.5B-Instruct at 7ae557604adf67be50417f59c2c2f167def9a775
- Independent authored train/evaluation facts: 3 + 2 per concept
- Prompts: 1000
- Pair selection: 3 within-category cosine-distance ranks × 100 target concepts
- Unique unordered Probe contrasts: 241
- Screen-passing unordered contrasts: 50
- With exact label-shuffle tail <= 0.10: 4
- Distinct X targets with two or more distance-band-stable Ys: 0 (goal: ~20)

## Most promising targets

| target      | group                     |   stable_comparators | stable_bands   | comparators   |   near_auc |   medium_auc |   far_auc | two_bands_stable   |
|:------------|:--------------------------|---------------------:|:---------------|:--------------|-----------:|-------------:|----------:|:-------------------|
| moth        | insects_and_small_animals |                    1 | medium         | mosquito      |       0.5  |         1    |      0.25 | False              |
| motorcycle  | vehicles                  |                    1 | medium         | boat          |       0.75 |         1    |      1    | False              |
| screwdriver | tools                     |                    1 | far            | saw           |       0    |         0.75 |      1    | False              |
| washer      | home_appliances           |                    1 | medium         | fan           |       0.75 |         1    |      1    | False              |
| airplane    | vehicles                  |                    0 |                |               |       0.5  |         1    |      1    | False              |
| albatross   | birds                     |                    0 |                |               |       0    |         1    |      1    | False              |
| ant         | insects_and_small_animals |                    0 |                |               |       0.5  |         0.75 |      1    | False              |
| apple       | fruits                    |                    0 |                |               |       0.5  |         0.5  |      0.5  | False              |
| banana      | fruits                    |                    0 |                |               |       0.25 |         0    |      0.5  | False              |
| bear        | land_mammals              |                    0 |                |               |       0.5  |         0.75 |      1    | False              |
| bee         | insects_and_small_animals |                    0 |                |               |       0.5  |         1    |      1    | False              |
| beetle      | insects_and_small_animals |                    0 |                |               |       0.25 |         0.5  |      0.5  | False              |
| bicycle     | vehicles                  |                    0 |                |               |       0.75 |         1    |      1    | False              |
| blender     | home_appliances           |                    0 |                |               |       0.75 |         0.75 |      1    | False              |
| boat        | vehicles                  |                    0 |                |               |       1    |         1    |      1    | False              |
| broccoli    | vegetables                |                    0 |                |               |       0    |         0.5  |      0.5  | False              |
| bus         | vehicles                  |                    0 |                |               |       1    |         1    |      1    | False              |
| butterfly   | insects_and_small_animals |                    0 |                |               |       0.25 |         0.75 |      1    | False              |
| cabbage     | vegetables                |                    0 |                |               |       0    |         0.25 |      0.5  | False              |
| car         | vehicles                  |                    0 |                |               |       1    |         1    |      1    | False              |
| carrot      | vegetables                |                    0 |                |               |       0.5  |         0    |      0.25 | False              |
| chisel      | tools                     |                    0 |                |               |       0.5  |         0.75 |      0.75 | False              |
| clarinet    | musical_instruments       |                    0 |                |               |       0.5  |         0.5  |      0.75 | False              |
| crab        | marine_animals            |                    0 |                |               |       0    |         0.5  |      0.25 | False              |
| cricket     | insects_and_small_animals |                    0 |                |               |       0.75 |         0.5  |      1    | False              |
| cucumber    | vegetables                |                    0 |                |               |       0    |         0.25 |      0.25 | False              |
| deer        | land_mammals              |                    0 |                |               |       0.75 |         1    |      0.75 | False              |
| dishwasher  | home_appliances           |                    0 |                |               |       0.5  |         1    |      1    | False              |
| dolphin     | marine_animals            |                    0 |                |               |       0.5  |         1    |      1    | False              |
| dragonfly   | insects_and_small_animals |                    0 |                |               |       0.25 |         0.5  |      0.75 | False              |
| drill       | tools                     |                    0 |                |               |       0.25 |         1    |      1    | False              |
| drum        | musical_instruments       |                    0 |                |               |       0.75 |         0.75 |      1    | False              |
| dryer       | home_appliances           |                    0 |                |               |       0.75 |         1    |      1    | False              |
| eagle       | birds                     |                    0 |                |               |       0.75 |         0.25 |      0.75 | False              |
| eggplant    | vegetables                |                    0 |                |               |       0.5  |         0.25 |      0    | False              |

## Distance-band AUC (exploratory)

| band   |   n |   mean_auc |   median_auc |   passing |   mean_distance |
|:-------|----:|-----------:|-------------:|----------:|----------------:|
| far    | 100 |     0.725  |         0.75 |         1 |        0.587257 |
| medium | 100 |     0.67   |         0.75 |         3 |        0.471076 |
| near   | 100 |     0.5075 |         0.5  |         0 |        0.321812 |

**Interpretation:** This is pair-relative Probe identity classification only, not suppression or absolute activation. Two evaluation fact families per concept are insufficient for confirmatory measurement claims. All candidates require fresh, independently authored evaluation texts before thesis main experiments.
