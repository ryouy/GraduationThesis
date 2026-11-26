# Experiment E — integrated exploratory comparison

Same D pool, fixed centers, identical optimization budget, old vs relaxed bounds. No API generation.
- old / <0.6: 46 pairs, complete 8, diagnostics 15, full 2, mean |rho| 0.3215, spread 0.0902, min realized gap 0.0382
- old / >=0.6: 29 pairs, complete 7, diagnostics 29, full 7, mean |rho| 0.0173, spread 0.0112, min realized gap 0.0387
- relaxed / <0.6: 46 pairs, complete 28, diagnostics 25, full 14, mean |rho| 0.2012, spread 0.0577, min realized gap 0.0193
- relaxed / >=0.6: 29 pairs, complete 16, diagnostics 29, full 16, mean |rho| 0.0091, spread 0.0036, min realized gap 0.0211

Limits: shared five X, old-Y cue generation, partial semantic audit, heuristic joint search; threshold 0.6 is exploratory. Smaller gap can reduce actual distance separation. No formal adoption.
