# Probe再解析・独立評価実験（2026-11-10）

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)

## 目的

11月4日に保存したPhi-3.5-mini-instructのHidden Stateを再利用し、Probeの校正問題と、学習時に使っていない説明ファミリーへの汎化性能を検証する。

## 実行内容

1. 20概念ペア×5つの重複する学習構成について、10学習ファミリーから5つをXラベルにする全252通りを列挙し、Probeを再学習する（合計25,200 fit）。
2. 固定した正解ラベルProbeについて、評価ファミリー10個のラベルを全252通り置換する検定。
3. X/Yそれぞれの評価ファミリーを1つずつ除く25通りの感度分析。
4. 40概念×5説明ファミリー×4プロンプト枠（800入力）について、同じモデル・同じHidden State位置から特徴を抽出し、既存Probeで評価する。

## 実行方法

1. 上の **Open in Colab** バッジを押す。
2. ColabのランタイムをGPU（T4以上）に設定する。
3. 「ランタイム」→「すべてのセルを実行」を選ぶ。
4. 最後にダウンロードされる `probe_recheck_results.zip` を保存する。

## データとモデル

- 元データ：[`1104_instruction_probe_20pairs`](../1104_instruction_probe_20pairs/)
- モデル：`microsoft/Phi-3.5-mini-instruct`
- Revision：`2fe192450127e6a83f7441aef6e3ca586c338b77`
- Hidden State：`hidden_states[31]`、`assistant_start`
- 元の特徴量・CSVはGitHub上の保存済み実験結果から取得し、SHA-256を照合する。

## 解釈上の注意

- 学習ラベル置換検定と評価ラベル置換検定は別の検定である。
- 5つの学習構成は学習ファミリーを共有するため、独立した5回の追試ではなく感度分析として扱う。
- 252通りの置換で得られる最小p値は1/252。20ペアの多重比較を考慮し、未補正p値を確証的な証拠として扱わない。
- 新しい説明文はAI作成の候補刺激であり、事実性・概念の一意性・難易度の人手確認が必要。
- AUCが高くても、概念一般への汎化や抑制条件の因果効果を証明するものではない。
- 回答生成は行わず、入力時点のHidden Stateのみを抽出する。

## 主な出力

- `exact_training_label_summary.csv`
- `exact_training_label_null_distribution.csv`
- `exact_evaluation_label_permutation.csv`
- `old_evaluation_family_swap.csv`
- `independent_eval_cues.csv`
- `independent_eval_probe_summary.csv`
- `independent_eval_family_scores.csv`
- `independent_eval_family_leaveout.csv`
- `training_label_shuffle_distributions.png`
