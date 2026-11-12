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
| Provisional selected set | **64 cues** |
| Final eligibility | Manual review of naturalness, correctness, weak relevance for far cues, lexical diversity, cross-concept ambiguity, and X/Y influence |

The candidate pool consists of 240 newly authored English sentences, embedded inside the notebook, with deliberately different direct, contextual, peripheral and unrelated formulations. The initial candidate validation verifies no concept-name leakage, duplicate text or extremely short/long sentences.

**Important:** Seed type is an authoring intention, **not an empirical distance label**. Near/medium/far are based on actual cosine distances measured *after running the notebook*. The labels are relative to this candidate pool, not universal values. A far cue must retain a semantically plausible relationship with X; truly unrelated cues are a different control group.

## Execution

Open the Colab badge. CPU execution is sufficient; running `sentence-transformers` may download the embedding model. To save files automatically to GitHub, enable Colab Secret `GITHUB_RESULTS_TOKEN` scoped to this repository with Contents read/write permissions.

The immutable output directory is:

`1112_cue_semantic_distance/results/20261112_cue_distance_pilot_v1/`

Outputs include `cue_candidates.csv`, `cue_selected_PROVISIONAL.csv`, `cue_review_template.csv`, `distance_separation_audit.csv`, `cue_distance_distributions.png`, `analysis_summary.md`, `config.json`, `manifest.json`, and an archive.

**State:** Source code created, 240-candidate input validation performed, and selection logic tested with clearly labeled mock distances. **Actual all-mpnet-base-v2 distances have not yet been measured; selected stimuli are not final.** Do not cite unrun results as numerical findings. Any human-rejected cue must be replaced in a new version before the suppression experiment.

## Prior evidence

- [Latest independent concept Probe confirmation](../1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md): the four vehicle concepts retained stronger pairwise decodability under new descriptions.
- [100-concept v2 screening](../1111_qwen_probe_100concepts_v2/results/20261112_qwen100_richer_dedup_v2/analysis_summary.md): pair and concept dependence motivates concept-specific auditing.

All four concepts are vehicles, so this stage is an **engineering pilot**, not evidence that the experimental effects generalize to other semantic categories.
