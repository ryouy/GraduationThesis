# 1019 v3 — matched X/Y semantic specificity controls

Run: 20261020T070234997011Z
Model: Qwen/Qwen2.5-0.5B-Instruct

## Main interpretation
Probe measures X-vs-Y decodability, not absolute target activation.
Both X and Y were independently selected as the named forbidden target.
Each cue set includes target-related, comparison-related and unrelated texts.
A positive specificity interaction means suppression increases target-vs-competitor cue discrimination compared with permissive instructions.
A negative specificity interaction means the cue discrimination is weaker under suppression.
Never interpret absolute target state or causal circuit from this alone.

## Key files
01_audited_XY_control_stimuli.csv — MiniLM sim-to-X/Y and cue length
02_embedding_and_length_audit.csv — matched stimulus quality
03_probe_validation_all_layers.csv — independent holdout AUC
04_probe_validation_flags.csv / 05_probe_validation_per_layer.csv
03_all_layer_target_aligned_pre_post.csv — all prompt-level pre/post readouts
04_precue_causal_invariance.csv — checks causal prefix invariance
05_prompt_and_cue_length_diagnostics.csv — prompt length controls
06_paired_instruction_contrasts.csv — same cue, different instruction
07_triplet_matched_specificity.csv — parallel target vs competitor vs unrelated triples
08_specificity_by_concept_target_layer.csv — target reversal retained
09_specificity_by_concept_layer.csv — unit-of-analysis summaries
10_layerwise_concept_bootstrap.csv — exploratory bootstrap and sign counts
11_prespecified_layers_22_23_by_concept.csv — follow-up focus outcomes
12_prespecified_22_23_bootstrap.csv — focus summary and exploratory CI
13_cue_length_balance_by_target_role.csv — token mismatch diagnostic
01..09_*.png — 9 diagnostic and exploratory plots
metadata.json — exact model, inputs and interpretation limits

This run does not change any saved v1/v2 result files.
