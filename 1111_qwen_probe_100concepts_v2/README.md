# Qwen Concept Probe: richer 100-concept validation (v2)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1111_qwen_probe_100concepts_v2/qwen_probe_100concepts_v2.ipynb)

[Notebook on GitHub](qwen_probe_100concepts_v2.ipynb)

## Why this experiment?

The previous 100-concept pilot used only **3 training facts and 2 held-out facts** per concept; its per-pair ROC-AUC was too coarse and zero targets met the two-distance-band stable criterion. The follow-up focuses on semantic sample diversity rather than increasing concept count.

## Protocol

- Fixed inventory of **100 concepts** across 10 groups; data coverage may cause exclusions.
- Collect **8 different training statements** from English Wikipedia and **8 evaluation statements** per concept. Prefer Simple English Wikipedia for evaluation; when insufficient, draw from later non-overlapping English Wikipedia sentences and explicitly tag that weaker same-article holdout. Require all 16 without duplicate wrappers. Record article URLs, revisions and per-sentence source tier.
- Evaluate **six Ys per X** (two close, two middle, two distant) within its group by pretrained `all-mpnet-base-v2` embedding distance based on training-only data.
- Qwen2.5-0.5B-Instruct hidden state at assistant start, layers **22/23/24**.
- Compare X-vs-Y linear probes via ROC-AUC and eight leave-one-training-fact-out fits.
- A label-shuffle null of **100** class-balanced permutations for first-pass qualifying pairs; flag exploratory pairs with shuffle upper-tail proportion at most **0.05**.
- Count *distinct target concepts* with >= 2 passing Ys in >= 2 distance bands.
- Save original sourced statements, data coverage, frozen comparison selections, reproducibility settings, intermediate GPU checkpoints, summaries, full CSV and archive on GitHub under `results/20261111_qwen100_richer_v1/`.

## Run

Open the Colab badge. Select a T4 GPU and enable notebook access to Colab Secrets `GITHUB_RESULTS_TOKEN`. Set the token to a fine-grained PAT scoped only to `ryouy/GraduationThesis` with Contents read/write. Run from the first cell.

**Important availability condition:** article sourcing depends on English and Simple English Wikipedia API access and enough usable sentences. If fewer than 20 concepts qualify, the notebook deliberately stops and writes `data_coverage.csv` locally rather than fabricating a dataset. The coverage report also distinguishes Simple-English evaluation sentences from English-Wikipedia same-article fallback. It may require a revised sourcing strategy and a new run ID.

## Methodological caveats

- Train/evaluation articles originate from different language-edition websites, but may share facts and prose. They are **not guaranteed independent semantic samples**.
- Many sentences can be anaphoric, tangential to the target, historically dated, or misleading; manual semantic validity review is necessary.
- Source reuse must comply with Wikipedia attribution and CC BY-SA licensing requirements. Links and revision IDs are retained.
- This is an **exploratory candidate screen**, not confirmatory evidence. Selected pairs require additional independently reviewed, freshly collected evaluation facts, ideally preregistered.
- No multiple-testing correction; do not interpret exploratory shuffled-tail proportions as confirmatory p-values.
- A high Probe AUC measures relative X/Y discrimination, *not absolute X activation* or suppression success.

**Status:** Code created and committed; data coverage, GPU extraction and experimental results have **not** been executed and verified in Colab.
