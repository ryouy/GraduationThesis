# Qwen Concept Probe: richer 100-concept study

- Eligible concepts (8 train + 8 evaluation sentences): **69 / 100**
- Sources: English Wikipedia (train); Simple English Wikipedia preferred for evaluation, with explicitly tagged same-article fallback. See per-sentence provenance in sourced_facts.csv.
- Model: Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775
- Unique prompts: 1104
- Unique unordered pairs: **158**
- Screen-passing pairs: **40**
- Screen + shuffle-passing pairs: **32**
- Distinct targets passing across 2 distance bands: **12** (target ~20)

## Distance-banded performance

| band   |   n |   mean_auc |   median_auc |   mean_distance |   stable |
|:-------|----:|-----------:|-------------:|----------------:|---------:|
| far    |  94 |   0.726895 |     0.734375 |        0.717082 |       18 |
| medium |  94 |   0.738032 |     0.765625 |        0.62097  |       26 |
| near   |  94 |   0.69498  |     0.6875   |        0.515556 |       10 |

## Best targets

| target     | group                     |   comparisons_tested |   stable_comparators |   stable_bands | comparators                                      |   near_mean_auc |   medium_mean_auc |   far_mean_auc | two_bands_stable   |
|:-----------|:--------------------------|---------------------:|---------------------:|---------------:|:-------------------------------------------------|----------------:|------------------:|---------------:|:-------------------|
| bus        | vehicles                  |                    6 |                    5 |              3 | boat, motorcycle, bicycle, submarine, helicopter |        0.929688 |          1        |       0.984375 | True               |
| motorcycle | vehicles                  |                    6 |                    5 |              3 | car, bus, train, helicopter, submarine           |        0.867188 |          1        |       0.976562 | True               |
| bicycle    | vehicles                  |                    6 |                    4 |              3 | boat, train, car, submarine                      |        0.835938 |          1        |       0.765625 | True               |
| boat       | vehicles                  |                    6 |                    4 |              3 | train, bicycle, bus, motorcycle                  |        0.875    |          0.945312 |       0.75     | True               |
| butterfly  | insects_and_small_animals |                    6 |                    4 |              3 | dragonfly, spider, ant, scorpion                 |        0.804688 |          0.9375   |       0.984375 | True               |
| dragonfly  | insects_and_small_animals |                    6 |                    3 |              2 | butterfly, moth, ant                             |        0.890625 |          0.960938 |       0.703125 | True               |
| jellyfish  | marine_animals            |                    6 |                    3 |              3 | octopus, dolphin, whale                          |        0.898438 |          0.820312 |       0.859375 | True               |
| submarine  | vehicles                  |                    6 |                    3 |              2 | car, bus, motorcycle                             |        0.828125 |          0.890625 |       0.992188 | True               |
| ant        | insects_and_small_animals |                    6 |                    2 |              2 | butterfly, dragonfly                             |        0.71875  |          0.734375 |       0.921875 | True               |
| moth       | insects_and_small_animals |                    6 |                    2 |              2 | dragonfly, scorpion                              |        0.789062 |          0.929688 |       0.898438 | True               |
| starfish   | marine_animals            |                    6 |                    2 |              2 | jellyfish, whale                                 |        0.585938 |          0.953125 |       0.726562 | True               |
| wolf       | land_mammals              |                    6 |                    2 |              2 | bear, elephant                                   |        0.828125 |          0.835938 |       0.820312 | True               |
| car        | vehicles                  |                    6 |                    2 |              1 | motorcycle, bicycle                              |        0.585938 |          0.976562 |       0.648438 | False              |
| elephant   | land_mammals              |                    6 |                    2 |              1 | lion, wolf                                       |        0.734375 |          0.796875 |       0.90625  | False              |
| scorpion   | insects_and_small_animals |                    6 |                    2 |              1 | moth, butterfly                                  |        0.757812 |          0.96875  |       0.703125 | False              |
| train      | vehicles                  |                    6 |                    2 |              1 | boat, bicycle                                    |        0.578125 |          1        |       0.898438 | False              |
| dolphin    | marine_animals            |                    6 |                    1 |              1 | jellyfish                                        |        0.773438 |          0.84375  |       0.890625 | False              |
| giraffe    | land_mammals              |                    6 |                    1 |              1 | wolf                                             |        0.492188 |          0.648438 |       0.742188 | False              |
| helicopter | vehicles                  |                    6 |                    1 |              1 | motorcycle                                       |        0.679688 |          0.726562 |       0.664062 | False              |
| lion       | land_mammals              |                    6 |                    1 |              1 | elephant                                         |        0.695312 |          0.84375  |       0.835938 | False              |
| octopus    | marine_animals            |                    6 |                    1 |              1 | jellyfish                                        |        0.796875 |          0.851562 |       0.726562 | False              |
| spider     | insects_and_small_animals |                    6 |                    1 |              1 | butterfly                                        |        0.78125  |          0.757812 |       0.632812 | False              |
| whale      | marine_animals            |                    6 |                    1 |              1 | starfish                                         |        0.765625 |          0.664062 |       0.851562 | False              |
| apple      | fruits                    |                    6 |                    0 |              0 |                                                  |        0.546875 |          0.601562 |       0.726562 | False              |
| banana     | fruits                    |                    6 |                    0 |              0 |                                                  |        0.796875 |          0.757812 |       0.59375  | False              |
| bear       | land_mammals              |                    6 |                    0 |              0 |                                                  |        0.695312 |          0.757812 |       0.609375 | False              |
| beetle     | insects_and_small_animals |                    6 |                    0 |              0 |                                                  |        0.882812 |          0.71875  |       0.554688 | False              |
| clarinet   | musical_instruments       |                    6 |                    0 |              0 |                                                  |        0.601562 |          0.625    |       0.609375 | False              |
| crab       | marine_animals            |                    6 |                    0 |              0 |                                                  |        0.679688 |          0.625    |       0.695312 | False              |
| deer       | land_mammals              |                    6 |                    0 |              0 |                                                  |        0.8125   |          0.59375  |       0.6875   | False              |

**Interpretation:** Exploratory *pair-relative decodability*, not absolute concept activation. Manually review texts and run a preregistered additional held-out confirmation before thesis claims.
