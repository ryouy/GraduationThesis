# Qwen Concept Probe: 100 concepts, controlled comparator distance

**[Open in Google Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1111_qwen_probe_100concepts/qwen_probe_100concepts_semantic_distance.ipynb)**

[Notebook on GitHub](qwen_probe_100concepts_semantic_distance.ipynb)

## Goal

Expand beyond the prior 40-concept pool and identify approximately 20 **distinct target concepts X** that can be discriminated from **multiple comparison concepts Y** at different semantic distances.

This is a new GPU experiment, not a reanalysis of the earlier 5,200 prompts.

## Protocol

- **100 target concepts in 10 semantic groups** (10 concepts per group).
- Five author-created semantic description facts per concept: **3 training** and **2 held-out evaluation**; 2 independent surface wrappers per fact = **1,000 prompts**.
- Embeddings: `sentence-transformers/all-mpnet-base-v2`, cosine distance on **concept name + first training description**.
- Comparator Ys are selected before training using **near/medium/far within-category distance ranks** (3 per target, **300 directed comparisons**, fewer unique unordered contrasts).
- Base model: `Qwen/Qwen2.5-0.5B-Instruct` revision `7ae557604adf67be50417f59c2c2f167def9a775`.
- Hidden-state readout: `assistant_start`, layers **22, 23, 24**, primary layer 24.
- Linear X/Y probes using L2 logistic regression and description-family-averaged features.
- Explore AUC and leave-one-training-family-out sensitivity; coarse exact family-label-shuffle controls for promising pairs.
- Count distinct targets with successful comparisons in at least 2 different semantic-distance bands.
- Record raw distances and AUCs for all comparisons, not only winners.

## How to execute

1. Open the Colab link above and select a **T4 GPU**.
2. In Colab **Secrets**, provide the `GITHUB_RESULTS_TOKEN` with Contents read/write permissions restricted to `ryouy/GraduationThesis`; enable notebook access.
3. Run all cells in order. Checkpoints automatically appear in `results/20261111_qwen100_v1/checkpoints/` in bundles of 240 prompts, allowing restart of an identical run.
4. On completion, CSV/manifest/plot/ZIP files appear under `results/20261111_qwen100_v1/`. Do **not** reuse the same run ID for changed experimental inputs.

## Interpretation cautions

- This dataset uses **only two novel semantic evaluation facts per concept**, so family-level AUC is coarse. The two wrappers for each fact are *not* independent samples.
- Comparing different concepts can change AUC through task difficulty. **Distance band is ranked within a semantic group**, and does not guarantee comparable absolute distances across concepts.
- Pre-selected near/medium/far distances come from embedding **labels plus training-only descriptions**, not from evaluation data. Semantic distance is thus operationally defined, not a direct conceptual ground truth.
- The exact balanced shuffle with 3 training families per class has only 20 possible assignments. It is a coarse negative control, not strong statistical evidence.
- All findings are **exploratory**. Selection of passing contrasts on held-out text introduces selection bias. A separate confirmation study with **fresh, independently reviewed held-out descriptions** and greater family counts is required.
- Concept Probe AUC means **X-vs-Y relative identity decodability**, not direct measurement of absolute concept activation or effectiveness of thought suppression.

**Status:** Experiment notebook published. No GPU execution or new empirical result has been confirmed yet.
