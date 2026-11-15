# Cue semantic-distance selection — 4-concept pilot

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1112_cue_semantic_distance/cue_semantic_distance_selection.ipynb)

[Open notebook](cue_semantic_distance_selection.ipynb) · [Full experimental protocol](../docs/main_experiment_protocol.md)

## Research purpose

Prepare stimuli *before running* the main suppression experiment. This notebook does not run Qwen generation, instruction comparisons, Probe decoding, or Logit Lens. It cannot be used to select cues based on an interesting downstream effect.

### Fixed design

| Dimension | Selection |
|---|---|
| X concepts | boat, bus, bicycle, motorcycle |
| Fixed Y comparisons | boat→bus; bus→helicopter; bicycle→submarine; motorcycle→helicopter |
| Candidate cues | 60 per target: 48 weakly/strongly related, 12 unrelated |
| Total candidates | **240** |
| Embedding model | `sentence-transformers/all-mpnet-base-v2` |
| Main distance | `1 − cos(embedding(frozen target definition), embedding(cue))` |
| Additional measures | target-name distance, Y definition distance, X−Y distance gap |
| Related selection | 4 each: near (bottom 30% of relevant candidates), medium (35–65% ranks), far (top 30%); evenly sampled within region |
| Negative control | 4 unrelated cues per target, separate from far |
| Provisional selected set | **64 cues** (subsequently AI-audited: 17 replaced, 47 retained) |
| Final eligibility | Manual review of naturalness, correctness, weak relevance for far cues, lexical diversity, cross-concept ambiguity, and X/Y influence |

The candidate pool consists of 240 newly authored English sentences, embedded inside the notebook, with deliberately different direct, contextual, peripheral and unrelated formulations. The initial candidate validation verifies no concept-name leakage, duplicate text or extremely short/long sentences.

**Important:** Seed type is an authoring intention, **not an empirical distance label**. Near/medium/far are based on actual cosine distances measured *after running the notebook*. The labels are relative to this candidate pool, not universal values. A far cue must retain a semantically plausible relationship with X; truly unrelated cues are a different control group.

## Execution

Open the Colab badge. CPU execution is sufficient; running `sentence-transformers` may download the embedding model. To save files automatically to GitHub, enable Colab Secret `GITHUB_RESULTS_TOKEN` scoped to this repository with Contents read/write permissions.

The immutable output directory is:

`1112_cue_semantic_distance/results/20261112_cue_distance_pilot_v1/`

Outputs include `cue_candidates.csv`, `cue_selected_PROVISIONAL.csv`, `cue_review_template.csv`, `distance_separation_audit.csv`, `cue_distance_distributions.png`, `analysis_summary.md`, `config.json`, `manifest.json`, and an archive.

**Updated status (2026-11-12):** The Colab notebook has been **executed**; 240 real `all-mpnet-base-v2` distances and 64 provisional cues are saved under [results/20261112_cue_distance_pilot_v1](results/20261112_cue_distance_pilot_v1/analysis_summary.md). A subsequent **AI-only** review checked all 64 provisional cues and replaced 17 with previously unused measured candidates. The final **pilot-frozen, AI-audited** 64-cue set is [here](final_stimuli/20261112_frozen_ai_audit_v1/README.md), with the [CSV for the pilot](final_stimuli/20261112_frozen_ai_audit_v1/cue_final_FROZEN_AI_AUDITED.csv). Human validation remains **PENDING**. The original notebook's automatic selection is **not** the final frozen selection, and should not be rerun to overwrite the audited set.

## Prior evidence

- [Latest independent concept Probe confirmation](../1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md): the four vehicle concepts retained stronger pairwise decodability under new descriptions.
- [100-concept v2 screening](../1111_qwen_probe_100concepts_v2/results/20261112_qwen100_richer_dedup_v2/analysis_summary.md): pair and concept dependence motivates concept-specific auditing.

All four concepts are vehicles, so this stage is an **engineering pilot**, not evidence that the experimental effects generalize to other semantic categories.
