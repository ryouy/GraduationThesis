# Experiment D — exploratory results

Primary pairs: 75; original anchors: 5. No generation API or embedding inference.
Fixed setting C, 24 slots, exact maximum cardinality, approximate joint search (3 seeds × 1200 steps). No missing slot hidden; diagnostic success on partial sets is not full success.

- known_audit_fail_excluded / baseline_no_y: n=75, complete=15, diagnostic=3, full=0, mean |rho|=0.4836, mean spread=0.1447
- known_audit_fail_excluded / joint: n=75, complete=15, diagnostic=44, full=9, mean |rho|=0.2041, mean spread=0.0596
- old_quality_no_y_name / baseline_no_y: n=75, complete=15, diagnostic=3, full=0, mean |rho|=0.4839, mean spread=0.1447
- old_quality_no_y_name / joint: n=75, complete=15, diagnostic=44, full=9, mean |rho|=0.2039, mean spread=0.0596

Among the 25 pairs measured in C, 4 meet D full and C exploratory screen.

## Limitations
B cues were generated/audited relative to original Y; new-Y semantic audit covers only a sample, and unaudited cues are not certified. Full success is a numeric/structural diagnostic, not formal stimulus adoption. Only five X families; shared cue pools and category/token confounding. Approximate search failure is not proof of infeasibility. Structural shortage is exact for the frozen candidate pool only. C uses 16 train/8 eval texts, not formal confirmation. No suppression outcomes were used. No distance cutoff is established by these exploratory results.
