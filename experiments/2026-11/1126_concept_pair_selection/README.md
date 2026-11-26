# 概念ペア生成・選定の方法論検証 — 実験A〜D

2026-11-26 / 4実験とも実施済み・探索的 / 正式採択・プロトコル凍結前。

**[A〜D統合報告書](INTEGRATED_REPORT_ABCD.md)** — 背景、実験方法、実測結果、図、総合考察、限界、本実験の選定方針案。

| 実験 | 内容 | 状態 | 実行・結果 |
|---|---|---|---|
| A | 既存50ペアの距離とProbe識別性能 | 完了 | [Notebook](experiment_A_distance_probe.ipynb) · [結果](results/20261126_concept_pair_distance_A_v1/analysis_summary.md) · [manifest](results/20261126_concept_pair_distance_A_v1/manifest.json) |
| B | 固定Xの75ペアとCue距離の共変動 | 完了 | [Notebook](experiment_B_y_distance_confound.ipynb) · [仕様](EXPERIMENT_B_PLAN.md) · [結果](results/20261126_concept_pair_distance_B_v1/analysis_summary.md) · [manifest](results/20261126_concept_pair_distance_B_v1/manifest.json) |
| C | 固定Xの25ペアとProbe識別性能（軽量版） | 完了 | [Notebook](experiment_C_distance_probe.ipynb) · [仕様](EXPERIMENT_C_PLAN.md) · [結果](results/20261126_concept_pair_distance_C_small_v1/analysis_summary.md) · [manifest](results/20261126_concept_pair_distance_C_small_v1/manifest.json) |
| D | 75ペアのCue joint最適化 | 完了 | [Notebook](experiment_D_cue_joint_selection.ipynb) · [仕様](EXPERIMENT_D_PLAN.md) · [結果](results/20261126_concept_pair_distance_D_v1/analysis_summary.md) · [manifest](results/20261126_concept_pair_distance_D_v1/manifest.json) |

Cのフル版は[Notebook](experiment_C_distance_probe_full.ipynb)・[仕様](EXPERIMENT_C_FULL_PLAN.md)として保存（未実行）。A〜Dは正式採択ではない。既存データ・mainは変更しない。

過去の計画と作業経緯は[旧README](README_PLANNING_HISTORY.md)に保存。
