# Experiment B — exploratory results

Generated 200 Y candidates; eligible new 198; primary selected 75/75; original anchors 5.
700 original cues, 622 historical quality pass; X definitions and dX fixed; related and unrelated separated.
Primary: old-quality common related cues, selected new Y, within-X correlations. All-cue and all-eligible analyses are sensitivity analyses.
Semantic audit mode: sample; audited rows: 960. Sample mode does not certify full cue-set quality.
No new Cue generation, Qwen forward passes, Probe learning or joint optimization. Slot feasibility is structural (distance, style, surface deduplication), NOT success at Y-distance control.

## Within-X Spearman association between X/Y distance and each outcome
- C01 / spearman: rho=-0.5750, n=15
- C01 / abs_spearman: rho=-0.5750, n=15
- C01 / band_mean_spread: rho=-0.6179, n=15
- C23 / spearman: rho=-0.9679, n=15
- C23 / abs_spearman: rho=-0.9679, n=15
- C23 / band_mean_spread: rho=-0.8964, n=15
- C27 / spearman: rho=-0.8071, n=15
- C27 / abs_spearman: rho=-0.8071, n=15
- C27 / band_mean_spread: rho=-0.8929, n=15
- C35 / spearman: rho=-0.7893, n=15
- C35 / abs_spearman: rho=-0.7750, n=15
- C35 / band_mean_spread: rho=-0.8000, n=15
- C37 / spearman: rho=-0.7571, n=15
- C37 / abs_spearman: rho=-0.7571, n=15
- C37 / band_mean_spread: rho=-0.8000, n=15

## Limitations
Candidates share X and Cue sets, so 75 pairs are not 75 independent replicates. Category and token length may confound distance; overlap and restricted analyses are descriptive. Old cues were generated/audited with original Y, which can favor anchors. Candidate definitions and semantic judgments are AI-produced and not human-verified. No causal or formal threshold claim. No suppression results used.
