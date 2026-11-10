# Qwen2.5-0.5B-Instruct — Concept Probe robustness, 20 pairs

[**Open this notebook in Google Colab**](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1110_qwen_probe_20pairs/qwen_concept_probe_robustness_20pairs.ipynb)

[View the notebook on GitHub](qwen_concept_probe_robustness_20pairs.ipynb)

## Purpose

Explore whether a linear X-vs-Y Concept Probe generalizes to different descriptions, readout locations, and instruction conditions. This is a measurement-validation experiment **not** a direct test of semantic distance, absolute concept activation, or causal suppression.

- Model: `Qwen/Qwen2.5-0.5B-Instruct`, revision `7ae557604adf67be50417f59c2c2f167def9a775`.
- 20 X/Y pairs (40 concepts); 6 training description families and 5 separately authored evaluation families per concept.
- 6 leave-one-family-out training configurations; layers 22/23/24; context-end and assistant-start positions.
- Neutral, mention X, think X, avoid X, think Y evaluation conditions.
- Exact family-level negative control: 252 balanced label assignments per primary Probe.
- Results are exploratory: training configurations and text wrappers are not independent repetitions.

## Run in Colab

1. Open the Colab link above; choose **Runtime → Change runtime type → T4 GPU**.
2. Create a GitHub fine-grained Personal Access Token restricted to `ryouy/GraduationThesis`, with **Contents: Read and write**.
3. In **Colab Secrets**, add `GITHUB_RESULTS_TOKEN` and enable notebook access.
4. Run the cells from top to bottom. Never commit the token or paste it into a notebook cell.

The run ID is fixed to `20261110_qwen20pairs_v1`. Keep this ID to recover the same interrupted run; change it for a fresh run with different experimental data.

## GitHub persistence

The notebook saves 64-prompt feature batches to Colab storage and commits a bundle of 8 batches (512 prompts) as soon as it is complete. Checkpoints are stored under:

```
1110_qwen_probe_20pairs/
  qwen_concept_probe_robustness_20pairs.ipynb
  README.md
  results/
    20261110_qwen20pairs_v1/
      checkpoint_chunks/
        chunk_000.zip
        chunk_001.zip
        ...
      README.md
      manifest.json
      pair_summary.csv
      condition_layer_position_summary.csv
      analysis_summary.md
      qwen_concept_probe_20pairs_results.zip
```

Only files that have actually been produced by the Colab run appear under `results/`. An incomplete extraction contains checkpoint chunks but **not** a completed result archive.

Remote checkpoints are validated using the stored prompt/configuration hash before reuse. Existing GitHub files are never silently overwritten. If a file exists with different bytes, execution stops and a new run ID is required.

The feature checkpoints are intentionally not included in the final analysis ZIP to avoid duplicating large data. The ZIP contains detailed per-pair and per-layer CSVs, shuffled AUC distributions, plots and a reproducibility manifest.

## Limits and reproducibility

- The evaluation descriptions were authored for this pilot; automatic lexical checks cannot establish human-judged semantic validity.
- AUC measures relative X/Y discrimination, not whether the LLM literally thinks about a concept.
- Repeated wrappers are not independent semantic samples.
- An exploratory stable-candidate flag is a diagnostic, not confirmatory evidence.

**Status:** Notebook committed. GPU extraction and experimental results are not yet run or verified in this commit.
