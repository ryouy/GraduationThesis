# 1019 Semantic-distance × suppression run

Run ID: 20261019T130118Z
Model: Qwen/Qwen2.5-0.5B-Instruct

## Interpretation
X-vs-Y probe decision scores are not activation probabilities.
Positive DID means a larger related-cue vs unrelated-cue contrast under suppression than neutral.
The neutral and suppression prompts differ in the number of literal X mentions.
Semantic bins are hypotheses; use 01_cue_distances.csv and 02_distance_order_diagnostics.csv.
Only validated probes (description AUC >= 0.75) are used in the main figures.
Unfiltered raw scores are preserved. Concept count n=8; bootstrap intervals exploratory.

## Files
01_cue_distances.csv - cue text, lexical checks, independent distance
02_distance_order_diagnostics.csv - ordering of candidate distance groups
03_probe_validation.csv - all held-out probes
04_probe_validated_flags.csv - semantically validated probes
05_probe_scores_all_conditions.csv - all 4 conditions and baseline by layer
06_prompt_length_diagnostics.csv - remaining length confounds
07_cue_level_paired_contrasts.csv - within-cue suppression vs neutral
08_per_concept_layer_summary.csv - cluster-level aggregation
09_DID_concept_bootstrap.csv - exploratory 95% concept intervals
10_within_concept_distance_trends.csv - final-layer continuous-distance analysis
01-04_*.png - visualization; optional 05 behavior graphic
metadata.json - run configuration and all limitations

Original code: 1019/semantic_distance_layer_probe.ipynb
