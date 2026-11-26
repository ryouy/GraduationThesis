# v0.98 採用根拠・検証記録

[統合プロトコル v0.98](main_experiment_protocol_v0_98.md) ｜ [旧 v0.97（保存）](main_experiment_protocol_v0_97.md)

本資料は設計上の採用理由と探索的実測結果を結び付ける。予備実験の結果は本実験の抑制効果の証明ではない。数値上の成功、正式Probe採択、刺激品質承認を区別する。

## 1. 概念ペア：なぜYを遠めにするのか

Probe・Logit LensはX/Y相対指標である。XとYが近いと、説明文での識別が難しく、CueからXとYへの距離が共変動しやすい可能性がある。Xのカテゴリーを維持しつつ、Yは同一・異カテゴリー双方を許容し、固定定義・固定MPNet尺度のdXY≥0.60を優先する。必須閾値にはしない。

<details>
<summary>実験A〜Dの目的・方法・結果</summary>

| 実験 | 方法 | 結果と判断 |
|---|---|---|
| A | 既存50ペア・10カテゴリーの距離と旧Probe L24 AUCを比較 | Pearson +0.447、Spearman +0.454。距離を順位付けに取り入れる |
| B | 5 XとCueを固定、15 Y/X（75ペア） | dXYとCueの距離間絶対相関のX内順位相関中央値 −0.775、spreadでは−0.800 |
| C | Bの25ペア、16学習・8探索評価文/ラベルの新規Probe | dXYとL24 AUCのX内順位相関中央値+0.791。dXY≥0.6の9/9が探索基準通過 |
| D | Bの同一候補集合・最大採択数でY非考慮とjointを比較 | 数値統制3→44/75、完全成功0→9/75。dXY≥0.6で数値統制29/29、完全成功7/29 |

[ABCD統合報告書](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/INTEGRATED_REPORT_ABCD.md)（個別結果・グラフ・manifestへのリンクを含む）。

Aは定義集合によってdXYが最大約0.301変動。Bの部分意味監査標本では負の関連が3/5 Xまで減った。Cは正式64/32/32評価ではなく、Dは新Yへの全件監査が未実施。共有X・Cue・カテゴリーの影響が残り、0.6は探索的な優先値であり普遍的閾値ではない。遠いYが広範なカテゴリー差だけで識別される危険も残る。

</details>

## 2. Probe：64学習・32探索・32最終独立評価

<details>
<summary>なぜこの文数・学習器・採択規則なのか</summary>

- 5組の学習曲線（8/16/32/64学習文/ラベル）で平均L24 AUCは0.6921/0.7327/0.7527/0.7740。事前の32文推奨基準を満たさず64を採用。[学習曲線](../experiments/2026-11/1126_probe_learning_curve/results/20261126_probe_learning_curve_v1/analysis_summary.md)
- 32評価文を基準に、8/16/24評価文の平均AUC絶対誤差は0.0696/0.0391/0.0210、Z-score RMSEの95パーセンタイルの5組平均は0.3911/0.2215/0.1254。32文を採用するが、別の32文集合への安定性は未検証。[評価安定性集計](../experiments/2026-11/1126_probe_evaluation_stability/results/20261126_probe_evaluation_stability_v1/stability_summary.csv)
- 32評価文で499/999/4,999/9,999回の置換すべてで3/5通過。9,999回（plus-one）に統一する。[置換集計](../experiments/2026-11/1126_probe_evaluation_stability/results/20261126_probe_evaluation_stability_v1/permutation_summary.csv)
- 学習器は既存のStandardScaler＋LogisticRegression(C=0.1, liblinear, seed=42)を継承。評価ラベルのタイプ内置換、L24 AUC≥0.80かつBH q≤0.05を正式基準とし、探索とは独立した新規確認を行う。閾値そのものの最適性を実証したわけではない。
- L24採択のみとすることで中間層が識別しにくい概念を選抜で排除しない。全24層の情報を保存し、各層専用Probeを使う。高AUCは抑制入力への一般化や心理的「思考量」を保証しない。

[旧v0.97の確定節・実測メモ](main_experiment_protocol_v0_97.md) ／ [均衡版50ペアの検証](../experiments/2026-11/1124_probe_50pairs/results/20261124_probe50_balanced_v5/analysis_summary.md)

</details>

## 3. Cue：なぜ実測距離・140候補・追加生成なのか

<details>
<summary>初期生成、選定比較、Y距離の最適化、追加生成の経緯</summary>

| 検証 | 方法 | 実測結果・採用判断 |
|---|---|---|
| 初期候補・v3修正版 | 5ペア、各140候補（関連120＋無関係20）、別AI監査 | 700文中622文合格。設定CでY制限なし110/120、Y固定範囲方式93/120。想定距離と実測帯を区別 |
| v4 | 同一候補・最大採択数を保持し相関・spreadを最適化 | jointで110/120を維持し、平均絶対相関0.678→約0.459。固定Y距離幅より最大数を保つjointを優先 |
| v5 | 不足枠80文、Y距離改善240文を追加生成 | 320文中289品質合格、139がいずれかの帯、31が指定帯に適合。採択110→115。自然さだけでは距離を精密に操作できない |
| v6 | 1,020候補（911品質合格）、幅3×空白3×タイプ制約2の18条件 | 各帯均等のまま±0.06/0.01で120/120。±0.08/0.01も120/120。全体均等方式はタイプ偏りを生むため各帯均等を維持 |

原資料： [v3選定集計](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_selection_corrected_v3/selection_summary.csv) ｜ [v4 joint集計](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_y_optimization_v4/summary.csv) ｜ [v5追加生成](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_targeted_generation_v5/summary.csv) ｜ [v5第1追加候補](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_targeted_generation_v5/round1_measured.csv) ｜ [v5第2追加候補](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_targeted_generation_v5/round2_measured.csv) ｜ [v6条件比較](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_constraint_comparison_v6/aggregate.csv)

初期140文は実施済みの生成規模を継承した運用初期値であって、最小必要数・最適数を確立したものではない。GPT-6 Luna (medium) は実際に使用した生成・別呼出し監査モデルとして継承する。異なるモデルとの対照比較による最良性の証明はない。v5は通常追加生成と同数の対照を設けていないためプロンプト自体の優越性は未証明。

</details>

## 4. 統合実験E：なぜ最大±0.06、最小空白0.01なのか

同じ75ペア、700 Cue（旧品質合格622）、固定中心、同一品質フィルタ、同一探索予算（3 seed×1,200 step）のもとで旧条件と改良条件を比較した。旧アンカー5ペアは別集計。全体均等への変更は行わない。

| 主分析 joint | 旧 ±0.04 / 0.03 | 改良 ±0.06 / 0.01 |
|---|---:|---:|
| 平均採択数 | 21.99 | 23.57 |
| 24文確保 | 15/75 | 44/75 |
| 数値統制成功 | 44/75 | 54/75 |
| 完全成功 | 9/75 | 30/75 |
| 平均絶対Spearman | 0.2039 | 0.1269 |
| 平均spread | 0.0596 | 0.0368 |
| 平均dX span | 0.3368 | 0.3371 |
| 最小帯平均間距離（平均） | 0.0550 | 0.0511 |
| 実現最小帯間空白（平均） | 0.0384 | 0.0200 |

dXY≥0.6の29ペアは両条件とも数値統制29/29、完全成功7→16/29。既知監査不適格を除外した感度分析も完全成功9→30/75。新規生成なしで構造充足と統制が改善し、dXの全体幅はほぼ維持された。帯間の最小空白は縮小したため、距離帯の区別を絶対視せず実測dXを主解析とする。

<details>
<summary>原資料・図・限界</summary>

- [実験Eノートブック](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/experiment_E_integrated_cue_constraints.ipynb) ｜ [結果概要](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/analysis_summary.md) ｜ [全体集計](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/aggregate.csv) ｜ [dXY別集計](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/distance_group_summary.csv) ｜ [ペア別比較](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/paired_comparison.csv) ｜ [manifest](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/manifest.json)
- [達成率図](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/figures/success_rates.png) ｜ [距離全体の幅](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/figures/dx_span.png) ｜ [実現最小空白](https://github.com/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/results/20261126_concept_pair_integrated_E_v1/figures/min_realized_dx_gap.png)
- [v6の全条件比較](https://github.com/ryouy/GraduationThesis/blob/experiments/cue-selection-luna-v1/experiments/2026-11/1126_cue_selection_luna/results/20261126_cue_constraint_comparison_v6/aggregate.csv)：±0.06/0.01で各帯均等120/120、全体均等120/120。全体均等の平均Cramér's V=0.411、各帯均等0。±0.08へさらに緩める利益は限定的。
- Eの改良joint主分析で新Y未監査は平均21.4文/ペア。完全成功30組は正式採択ではない。5 Xに依存し、既存Cueは元のY向けに生成された。近似探索で未達を不可能と断定しない。±0.06と0.01の一般的最適性は未証明。

</details>

## 5. その他の採用判断と未確定事項

| 方針 | 理由・根拠 |
|---|---|
| Avoid X主解析・Neutral X対照 | 名称提示を共通にした比較対照を持ち、抑制指示下の距離関係を中心にする。[パイロット解釈](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)、[Neutral追加](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/analysis_summary.md) |
| dYも記録・調整 | 10概念Pre-mainでL24 Avoidの負相関概念数がProbe 5→8、Lens 3→7。因果効果の証明ではない。[距離感度分析](../experiments/2026-11/1125_pre_main_distance_sensitivity/README.md) |
| Probe decision score標準化・平均対数尤度Lens | 概念間の尺度差、候補トークン数の影響を意識した設計。[内部測定方針](internal_representation_measurement_policy_20261126.md) |
| 5回回答生成 | 予備実験との連続性・出力ばらつきの測定を重視。内部表現の独立観測数は増えない。[生成条件](answer_generation_policy_20261126.md) |
| 100 X・10カテゴリー | 対象の幅と概念単位の分析を拡大する研究設計上の目標。検出力・代表性を保証する標本数ではない。[規模方針](probe_learning_curve_and_scale_plan_20261126.md) |
| 出力評価4指標 | 明示的言及、厳密な意味的同定、Cue妥当性、形式遵守は別物。v4の500回答を評価済みだが正式判定・人手一致度は未完了。[評価メモ](output_evaluation_validation_memo_20261126.md) |
| dX連続値・dY調整・階層分析 | CueがX内にネストされるため。[統計方針](statistical_analysis_policy_20261126.md)。具体的推定器・検定族等は未凍結 |
| GitHub不変チャンク・工程分離 | 過去の生成失敗・中断への対応、再現性確保。[実行管理方針](main_experiment_execution_policy_20261126.md) |

## 6. 採用と正式確定の区別

v0.98では刺激設計の基本方針を採用する。Yの厳密な順位キー、トークン許容差、Cue追加生成の回数・費用上限、数値診断未達の扱い、人手抽出件数、意味重複規則、最終出力採点、統計・実装照合は凍結前に決める。新規Xでの一般化も未確認である。本実験の結果を見て基準を変更しない。旧資料は保存し、v0.98が優先する。
