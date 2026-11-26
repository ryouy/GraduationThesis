# 2026-11-27 ブランチ統合記録

現在のmainを保持し、実験2ブランチの追加分を元のパスへ統合。旧整理ブランチは46箇所の競合があるため現行構成を優先し、固有変更版を原文のまま保存。既存同一blobは重複コピーしない。旧削除指示は適用しない。旧Workflowは移動前パス参照のため非実行アーカイブに保存。全履歴をマージコミットの親として保持する。

## 元commit

- main: `cc03dd3af86792d26bd64e7a40014f6cd7975f86`
- concept-pair-selection: `ffed58248f17e87c5803f54e7c600927f0716b94`
- cue-selection-luna: `3268eea2a7b96fc25ca904bf915b74849c467c72`
- reorganize-repository: `431edca9e44de2755e794d65b460a26b2c4d4f7f`
- exact-probe-permutations: `605bfcdf2f23e2d263299da396785c5a7ade084e`
- group-experiments-by-month: `c20fd0ffb81c97281628c3dfd802dec5bc07aed6`

## 保存した旧版

- `README.md` → `archive/branch-merge-20261127/reorganize-repository/README.md`
- `archive/README.md` → `archive/branch-merge-20261127/reorganize-repository/archive/README.md`
- `archive/legacy_tests/GT03.ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/GT03.ipynb`
- `archive/legacy_tests/GT04.ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/GT04.ipynb`
- `archive/legacy_tests/GrammarConfidenceExperiment copy 2.ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/GrammarConfidenceExperiment copy 2.ipynb`
- `archive/legacy_tests/GrammarConfidenceExperiment copy.ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/GrammarConfidenceExperiment copy.ipynb`
- `archive/legacy_tests/GrammarConfidenceExperiment_StrongConditions (1).ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/GrammarConfidenceExperiment_StrongConditions (1).ipynb`
- `archive/legacy_tests/GrammarConfidenceExperiment_StrongConditions (2).ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/GrammarConfidenceExperiment_StrongConditions (2).ipynb`
- `archive/legacy_tests/grammar_prompt_experiment_bundle_ready_fixed.ipynb` → `archive/branch-merge-20261127/reorganize-repository/archive/legacy_tests/grammar_prompt_experiment_bundle_ready_fixed.ipynb`
- `docs/README.md` → `archive/branch-merge-20261127/reorganize-repository/docs/README.md`
- `docs/archive/README.md` → `archive/branch-merge-20261127/reorganize-repository/docs/archive/README.md`
- `docs/archive/README_previous_20261103.md` → `archive/branch-merge-20261127/reorganize-repository/docs/archive/README_previous_20261103.md`
- `docs/current_status.md` → `archive/branch-merge-20261127/reorganize-repository/docs/current_status.md`
- `docs/experiment_index.md` → `archive/branch-merge-20261127/reorganize-repository/docs/experiment_index.md`
- `docs/research_notes/README.md` → `archive/branch-merge-20261127/reorganize-repository/docs/research_notes/README.md`
- `experiments/2026-10/1015/white_bear_and_zhou_pilot.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1015/white_bear_and_zhou_pilot.ipynb`
- `experiments/2026-10/1015/white_bear_and_zhou_pilot_v2.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1015/white_bear_and_zhou_pilot_v2.ipynb`
- `experiments/2026-10/1015/white_bear_and_zhou_pilot_v2_fixed.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1015/white_bear_and_zhou_pilot_v2_fixed.ipynb`
- `experiments/2026-10/1015/white_bear_and_zhou_pilot_v3.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1015/white_bear_and_zhou_pilot_v3.ipynb`
- `experiments/2026-10/1015/white_bear_colab_pilot.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1015/white_bear_colab_pilot.ipynb`
- `experiments/2026-10/1016/06_再現手順と解釈上の注意.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1016/06_再現手順と解釈上の注意.md`
- `experiments/2026-10/1017/MidPoster_Fig2.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1017/MidPoster_Fig2.ipynb`
- `experiments/2026-10/1019/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1019/README.md`
- `experiments/2026-10/1019/concept_specificity_control_v3.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1019/concept_specificity_control_v3.ipynb`
- `experiments/2026-10/1019/results/20261019T130118Z/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1019/results/20261019T130118Z/README.md`
- `experiments/2026-10/1019/semantic_distance_layer_probe.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1019/semantic_distance_layer_probe.ipynb`
- `experiments/2026-10/1019/semantic_distance_layer_probe_v2.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/1019/semantic_distance_layer_probe_v2.ipynb`
- `experiments/2026-10/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-10/README.md`
- `experiments/2026-11/1103_fresh_check/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_fresh_check/README.md`
- `experiments/2026-11/1103_model_check/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_model_check/PLAN.md`
- `experiments/2026-11/1103_model_check/run_check.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_model_check/run_check.py`
- `experiments/2026-11/1103_review/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_review/README.md`
- `experiments/2026-11/1103_review/audit_saved_results.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_review/audit_saved_results.py`
- `experiments/2026-11/1103_revision/run_revision.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_revision/run_revision.py`
- `experiments/2026-11/1103_validity/measurement_validity_pilot.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1103_validity/measurement_validity_pilot.ipynb`
- `experiments/2026-11/1104_inference_audit/verify.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_inference_audit/verify.py`
- `experiments/2026-11/1104_instruction_probe/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_instruction_probe/PLAN.md`
- `experiments/2026-11/1104_instruction_probe/instruction_probe_diagnostic.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_instruction_probe/instruction_probe_diagnostic.ipynb`
- `experiments/2026-11/1104_instruction_probe/results/instruction-probe-20261104T024551489146Z/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_instruction_probe/results/instruction-probe-20261104T024551489146Z/PLAN.md`
- `experiments/2026-11/1104_instruction_probe_20pairs/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_instruction_probe_20pairs/PLAN.md`
- `experiments/2026-11/1104_instruction_probe_20pairs/instruction_probe_20pairs.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_instruction_probe_20pairs/instruction_probe_20pairs.ipynb`
- `experiments/2026-11/1104_instruction_probe_20pairs/results/instruction-probe20-20261104T034343105831Z/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_instruction_probe_20pairs/results/instruction-probe20-20261104T034343105831Z/PLAN.md`
- `experiments/2026-11/1104_model_comparison/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_model_comparison/PLAN.md`
- `experiments/2026-11/1104_model_comparison/verify.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_model_comparison/verify.py`
- `experiments/2026-11/1104_phi_prompt_diagnostic/PLAN.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_phi_prompt_diagnostic/PLAN.md`
- `experiments/2026-11/1104_phi_prompt_diagnostic/check.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_phi_prompt_diagnostic/check.py`
- `experiments/2026-11/1104_phi_prompt_diagnostic/phi_prompt_diagnostic.ipynb` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_phi_prompt_diagnostic/phi_prompt_diagnostic.ipynb`
- `experiments/2026-11/1104_phi_prompt_diagnostic/prepare.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_phi_prompt_diagnostic/prepare.py`
- `experiments/2026-11/1104_phi_prompt_diagnostic/test_analysis.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_phi_prompt_diagnostic/test_analysis.py`
- `experiments/2026-11/1104_phi_validation/check.py` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/1104_phi_validation/check.py`
- `experiments/2026-11/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/2026-11/README.md`
- `experiments/README.md` → `archive/branch-merge-20261127/reorganize-repository/experiments/README.md`
- `presentations/README.md` → `archive/branch-merge-20261127/reorganize-repository/presentations/README.md`

旧版の相対リンク・実行パスは当時の配置を前提とする。ノートブック・CIは再実行していない。マージ前mainは backup/main-before-merge-20261127 に保存。
