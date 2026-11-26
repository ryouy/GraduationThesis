# Experiment C — exploratory results

Primary pairs: 25; anchors: 0; independent exploratory evaluation (16 train/8 eval per label, reduced pilot only).
L24 screen pass: 18/25; exploratory BH pass: 18/25.
Joint B diagnostics plus C screen pass: 2/25 (not formal adoption).

## Within-X distance vs L24 AUC
- bicycle: Spearman 0.3536, n=5
- trumpet: Spearman 0.6000, n=5
- banana: Spearman 0.7906, n=5
- bookshelf: Spearman 0.9000, n=5
- screwdriver: Spearman 0.8721, n=5

## Limitations
Five X families; shared X training and evaluation, correlated observations. AI quality review only; human review pending. No fresh final confirmation, no formal adoption. No original Y anchors evaluated. X descriptions exclude all selected Y terms while Y descriptions exclude X and own terms; this asymmetry can affect results. High AUC does not establish validity on suppression prompts. No suppression output or effect used for selection.
