# Cue distance selection / pilot stimuli

- **Status:** PROVISIONAL, awaiting human review. Not a final experimental stimulus set.
- Model: `sentence-transformers/all-mpnet-base-v2`, revision `e8c3b32edf5434bc2275fc9bab85f82640a19130`.
- Candidate cues: **240** (60 per X; 48 related and 12 unrelated controls).
- Selected provisional cues: **64** (4 near + 4 medium + 4 far + 4 unrelated per X).
- No Qwen output, instruction-condition outcomes, or Probe scores were consulted.
- Definitions and Y concepts were frozen before distance measurement.

## Distance separation by target (lower = semantically closer by this embedding)

| target_x   |   mean_near |   mean_medium |   mean_far |   near_to_medium_gap |   medium_to_far_gap | low_gap_warning   |
|:-----------|------------:|--------------:|-----------:|---------------------:|--------------------:|:------------------|
| boat       |       0.592 |         0.764 |      0.895 |                0.078 |               0.040 | False             |
| bus        |       0.559 |         0.719 |      0.847 |                0.064 |               0.050 | False             |
| bicycle    |       0.591 |         0.822 |      0.998 |                0.046 |               0.061 | False             |
| motorcycle |       0.653 |         0.799 |      0.971 |                0.059 |               0.055 | False             |

## Related candidate distance distribution

| target_x   |   min |   median |   max |
|:-----------|------:|---------:|------:|
| bicycle    | 0.42  |    0.866 | 1.063 |
| boat       | 0.473 |    0.775 | 0.971 |
| bus        | 0.436 |    0.723 | 0.925 |
| motorcycle | 0.545 |    0.8   | 1.084 |

## Required human review

Check factuality, naturalness, semantic diversity, relevance of far cues, and Y association in `cue_review_template.csv`.
**Never replace rejected cues after viewing the main experiment outcomes.**

## Files

- `cue_candidates.csv`: full candidate pool, measured X/Y distances and quality flags.
- `cue_selected_PROVISIONAL.csv`: selected 64 texts and distances.
- `cue_review_template.csv`: review sheet. The selection is not FINAL.
- `distance_separation_audit.csv`: separation flags.
- `cue_distance_distributions.png`: distance histograms and selected texts.
- `config.json`: reproducibility configuration and embedding revision.
- `manifest.json`: hashes and run completion status.
