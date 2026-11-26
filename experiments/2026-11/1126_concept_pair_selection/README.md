# 概念ペア生成・選定の方法論検証 — 実験A
2026-11-26 / 探索的 / 未実行。既存ファイル・mainは変更しない。
[Colabで開く](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/experiment_A_distance_probe.ipynb)

## A
固定50組、82概念。v5の既存成績（8学習・8評価、L22–24、L24の499置換p・BH q）を再利用。L1–21と層別p/qは欠測。v0.97の正式採択（64/32/新規32、9,999置換）とは区別。入力commit・埋め込みrevisionを固定。CPUのみ、生成API不使用。
既存の定義はCue v1の5組、pre-mainの10組に限られるため、全50組を同一形式で比較するための新規定義案を明示的に作成。人手未監査。既存定義の二つの集合で個別に感度分析し、混合しない。定義案の監査後は別runで実行する。正式採択はしない。
GitHub secret GITHUB_RESULTS_TOKEN（任意、なければZIP）で距離チェックポイントと成果物を専用ブランチに保存。既存出力は上書き不可。完了済みの再実行は新run IDを推奨。
## B（計画のみ）
5 X固定、既存Yをアンカー、各Xに新規30–40 Y候補を同カテゴリー/異カテゴリーの双方から生成（GPT-6 Luna、medium）。定義統一・同義/上下位/曖昧概念除外、トークン数記録、実測距離五分位から3件ずつ距離中央値への近さで選ぶ。カテゴリー・トークン差の偏りを別集計。既存Yが選外なら別アンカーとして追加、75+最大5組。既存Cue全候補700（品質通過622）を固定、元のYを意識して生成・監査した選択偏りあり。全候補と旧品質通過のみを分け、関連・無関係を別集計。Y特有の関連や名称露出を監査し、共通Cue集合とY別監査後集合を別分析。X内相関と効果方向の一貫性を確認し、75組を独立観測としない。BはAPI未実行。
Dは既存v4 jointのsetting C（±.04、空白.03）を継承候補とする。元の五分位中心・候補集合をX内固定、同じ探索予算/seed、欠損スロット・完全成功と診断的達成を区別。正式基準ではない。

## 実験B — 実装済み・未実行（2026-11-26）
- [実験B Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/experiment_B_y_distance_confound.ipynb)
- [実験Bの設計・実行手順](EXPERIMENT_B_PLAN.md)
- [実験Aの結果](results/20261126_concept_pair_distance_A_v1/analysis_summary.md)

## 実験C — 実装済み・未実行
- [実験C Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/experiment_C_distance_probe.ipynb)
- [実験C仕様](EXPERIMENT_C_PLAN.md)
- [実験B結果](results/20261126_concept_pair_distance_B_v1/analysis_summary.md)

## 実験D — 実装済み・未実行
- [実験D Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/experiment_D_cue_joint_selection.ipynb)
- [実験D仕様](EXPERIMENT_D_PLAN.md)
- [実験C軽量版結果](results/20261126_concept_pair_distance_C_small_v1/analysis_summary.md)
