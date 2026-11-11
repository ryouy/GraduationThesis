# Concept Probe — Expanded comparison-pair screening

**[Open in Google Colab (CPU)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1111_qwen_probe_pair_expansion/qwen_probe_pair_expansion_cpu.ipynb)**

[Notebook source](qwen_probe_pair_expansion_cpu.ipynb)

## Goal

Identify ~20 **distinct target concepts X** with reproducible relative X-versus-Y discrimination. This is exploratory screening using an existing concept bank, **not proof of absolute concept activation or suppression**.

The first 20-pair experiment returned 6 pairs meeting the exploratory stability criteria. To expand efficiently, this notebook **reuses the stored hidden-state vectors for all 40 concepts from the completed run**, then trains new probes using alternative comparison concepts Y.

**No new Qwen inference or GPU is required in this notebook.** Changing the comparison concept requires training a new linear Probe but not rerunning the 5,200 source prompts.

## Procedure

1. Rebuild and verify the exact old prompt order, source SHA, and manifest.
2. Download and independently verify each of 11 archived feature checkpoint ZIPs in the original run (read-only).
3. Preregister new within-topic candidate X/Y contrasts for all 40 available concepts. Original pairs are retained. Reversed pairs are not counted as independent.
4. Run 6 leave-one-family-out training fits per **unique unordered contrast** and score the five independent held-out description families.
5. Apply the AUC/family-deletion stability screen, then 252 balanced family-label permutation assignments for each passed contrast.
6. Report **how many distinct target concepts** have at least **two distinct stable comparators Y**.
7. Save CSVs, manifest, summary, chart, and full ZIP under `results/20261111_comparator_screen_v1/`.

## How to run

Use standard Colab **CPU** runtime, and grant access to the `GITHUB_RESULTS_TOKEN` Secret (a fine-grained GitHub PAT with Contents read/write access restricted to `ryouy/GraduationThesis`). Run all cells in order. The notebook will write only under its new experiment results directory. It will not modify previous experiments.

## Scientific limits

- The same 40 concepts and the same held-out descriptions are reused: this **does not independently establish generalization**, and candidate comparisons are correlated.
- Contrasts are screened on evaluation AUC, so the winning combinations need **fresh held-out descriptions, prepared independently after selection**, before publication or the thesis's main semantic-distance experiment.
- It is easy to obtain artificially high AUC using unrelated comparisons. The design restricts comparators to predefined broad categories, and each candidate target must pass two distinct comparisons, but this does **not** entirely eliminate that issue.
- AUC is relative pair discrimination. It cannot be interpreted as whether the model was thinking of X or successfully suppressed X.
- The label-shuffle proportions are exploratory and no multiple-testing adjustment is applied.
- The 20-concept target is **not guaranteed**; the notebook reports the observed count rather than changing the threshold to force a desired result.

## Status

Notebook and code authored. **The additional screening has not yet been executed in Colab**. Results will appear in this folder when the run finishes.
