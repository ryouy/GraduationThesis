# 1019 v2 — Layer-wise semantic distance vs concept suppression

Run: 20261019T133851060426Z
LLM: Qwen/Qwen2.5-0.5B-Instruct
Encoder: sentence-transformers/all-MiniLM-L6-v2

## Main analysis
X vs Y probes at 24 layers; same-prompt pre- and post-cue STATE: markers.
For each cue: interaction = (after-before)_suppression - (after-before)_neutral.
DID_vs_unrelated subtracts each concept's three farthest measured cues.
Plots of semantic X/Y readouts require held-out description AUC≥0.75 and at least 5 valid concept probes.
Semantic bin labels are quartiles from an independent sentence encoder, not verified human ratings.

## CSV and PNG outputs
01_stimulus_distances_and_ranks.csv: independent continuous distances and both cue labels
02_proposed_distance_audit.csv: which original distance orders held
03_probe_validation_all_layers.csv: held-out AUC and accuracy
04_probe_validation_flags.csv / 05_probe_validation_per_layer.csv
06_layerwise_pre_post_measurements.csv: raw and standardized X/Y scores plus vector displacement
07_token_length_diagnostics.csv: prompt length differences
08_matched_cue_layer_contrasts.csv: delta, instruction interaction, DID
09_concept_layer_distance_bin_summary.csv: concept-level near/medium/far/unrelated
10_distance_slope_by_concept_layer.csv: concept-specific distance sensitivity
11_layerwise_distance_slopes_bootstrap.csv: concept bootstrap across layers
12_distance_bin_layerwise_DID_bootstrap.csv: measured-bin contrast intervals
13_near_vs_far_by_concept_layer.csv: validated mask and near-minus-far profile
01..08_*.png: 8 diagnostic and scientific figures
stimuli_v2.csv and probe_description_bank_v2.json: exact input copies
metadata.json: experiment and limitations

## Interpretation
Positive DID: suppression differs from neutral in cue-driven change relative to distant cues.
It does NOT mean that the suppressed concept is absolutely stronger than normal.
Do not claim causal reactivation, knowledge erasure, or reliable early-layer trends without probe validity.

