# Graduation Thesis｜LLMにおける抑制概念と意味的距離

<!-- github-only:start -->
[![Web版](https://img.shields.io/badge/Web版-2563eb?style=flat)](https://ryouy.github.io/GraduationThesis/)
<!-- github-only:end -->

<a href="Interim_Posters/LLM%20Concept%20Probe%20Infographic.png"><img src="Interim_Posters/LLM%20Concept%20Probe%20Infographic.png" alt="LLM Concept Probe — 研究概要図" align="right" width="48%"></a>

LLMに対する「Xについて考えないで」という抑制指示の下で、対象概念Xと手がかり（Cue）の意味的距離が内部表現とどのように関係するかを調べる卒業研究のリポジトリです。

本実験では、抑制指示（Avoid X）と中立的な指示（Neutral X）を比較し、約50の対象概念について、意味的に近い手がかりから無関係な手がかりまでを段階的に提示する計画です。生成直前の内部表現をConcept Probe・Logit Lensで層ごとに分析し、最終出力における対象概念の言及は、内部解析との対応を見るための補助指標として扱います。

<br clear="right">

## 本実験の統合プロトコル（最初に読む）

**[本実験・統合プロトコル v0.95](docs/main_experiment_protocol_v0_95.md)** — 現行研究方針の唯一の正本。実験設計、測定、Cue準備、統計、未完了事項を統合。実行用v1.0は未凍結。

現在：初回50組中33組のProbeが暫定基準通過。**後日、採択可能な異なるXを合計約50にする追加探索と、本番用Cueの独立準備を行う。** Probeは今後全24層に拡張するが、概念採択は従来の第24層基準を維持する。追加実験・実装は未実施。過去の設計・実験データは保存する。

## はじめに読む

| ページ | 内容 |
|---|---|
| **[統合プロトコル v0.95（現行の正本）](docs/main_experiment_protocol_v0_95.md)** | **Probe採択可能な約50概念を目標・6区分・Avoid X中心／Neutral X対照・Probe／Logit Lens主解析**。追加探索・Cue準備を含む |
| [旧統合設計 v0.9](docs/main_experiment_protocol_v0_9.md) | 2026-11-24までの設計記録（保存） |
| [研究概要](docs/research_overview.md) | 研究動機・背景・当初の研究質問 |
| [分析手法と測定指標](docs/methods.md) | Probe・Logit Lens・出力解析・意味的距離の解説（過去の測定計画も含む） |
| [研究参考資料](docs/reference/README.md) | トークン・生成直前のHidden State・Concept Probe・Logit Lensのわかりやすい解説 |
| [旧プロトコル（歴史的記録）](docs/main_experiment_protocol.md) | 4概念・4条件を含む以前の設計。**内容を維持** |
| [本実験設計の検討記録 v0.7](docs/main_experiment_design_v0_5.md) | 新プロトコルへ統合する前の設計案と判断経緯 |
| [旧実験設計・分析計画](docs/experimental_design.md) | パイロット段階の4条件を中心とする記録 |
| [進捗と過去の検証](docs/current_status.md) | 2026年11月の予備実験と過去の課題を記録 |
| [月別の実験一覧](experiments/README.md) | 月別・日付別に実験を探す |
| [実験記録・資料一覧](docs/experiment_index.md) | 目的別に実験コードと結果へアクセス |

## 現在の本実験の概要（2026年11月24日）

> **研究質問：** 「Xについて考えないで」という指示を与えたLLMで、対象概念XとCueとの意味的距離は、内部表現に読み出されるX/Y相対情報とどのような関係を持つか？

| 項目 | 現在の設計案 |
|---|---|
| 主たる指示条件 | **Avoid X**（Neutral Xは比較対照） |
| 対象概念 | **Probe採択可能な異なるXを約50**（現在33組暫定通過・追加探索予定） |
| Cue | **関連5距離帯×各4文＋無関係4文＝24 Cue／概念** |
| 主説明変数 | 関連Cueの連続的な埋め込みコサイン距離 |
| 主解析① | 固定Concept Probe（第24層が主解析・全24層を学習／評価して層別分析）と距離の関連 |
| 主解析② | Logit Lens（第24層の要約・全24層の推移） |
| 副次解析 | Neutral Xでの距離傾向、距離×条件の違い |
| 補助解析 | 生成出力におけるXの明示的な言及 |
| 入力規模 | 最終50概念なら**2,500入力**（Cueあり2,400＋Cueなし100） |

これは**実施前の統合設計**です。追加Probe探索、正式採択、本番用Cueの作成・凍結、統計推定法、GPU本実験・CPU分析Colabの最終固定は未完了です。詳細は[統合プロトコルv0.95](docs/main_experiment_protocol_v0_95.md)を参照してください。

### これまでの予備実験

- **4条件パイロット（2026年11月）**：4概念・64 Cue、272入力・1,360生成を実行し、生成前Hidden State、Probe（22/23/24層）、全24層Logit Lens、出力判定を保存。[統合解釈](experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)
- **Neutral X追加検証（2026年11月24日）**：68入力・340生成、固定Probe・Logit Lensを取得。Xを名称提示する中立条件を追加した結果、出力の明示的X言及率は関連CueでNeutral X 57.9%、Avoid X 34.6%。この比較は探索的であり、禁止指示だけの因果効果の証明ではありません。[結果](experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/analysis_summary.md)
- **刺激品質の限界**：固定64 CueにAI一次評価はありますが独立人手評価は未実施です。本実験は対象概念を広げ、Cueの文章タイプの偏りも点検します。[Cue評価の記録](docs/cue_validation_decision_v0_1.md) ／ [独立した説明文によるProbe評価](experiments/2026-11/1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md)

**注意**：本実験は「抑制すると必ずXが強く表現される」という結果を前提にしません。ProbeとLogit Lensは思考そのものを直接測るものではなく、読み出し可能な相対情報・語彙投影を測る手法です。旧4条件や出力中心の説明は当時のパイロットの設計経緯として保持しています。

## 本実験の準備資料

- [Probe50均衡版v5：実行済み・33/50組暫定通過](experiments/2026-11/1124_probe_50pairs/results/20261124_probe50_balanced_v5/analysis_summary.md) · [Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1124_probe_50pairs/qwen_probe_50pairs_balanced_validation_v5.ipynb)
- [初回50組の候補と選定理由](docs/concept_pair_selection_v0_1.md) · [候補CSV](docs/concept_pair_candidates_50_v0_1.csv)（正式採択ではない）
- [既存4概念の距離再分析](experiments/2026-11/1124_distance_representation_analysis/results/20261124_distance_reanalysis_v1/analysis_summary.md)（完了・探索的）
- [10概念Pre-main](experiments/2026-11/1124_pre_main_experiment/README.md)（実装済み・探索的）
- **追加Probe探索・本番用Cue準備：後日実施。** 仕様・開始条件は[統合プロトコル](docs/main_experiment_protocol_v0_95.md)に記載。

## 実験へのアクセス

**[月別の実験一覧](experiments/README.md)** · [研究段階別の実験索引](docs/experiment_index.md) · [現在の進捗](docs/current_status.md)

実験の記録は月別一覧と研究段階別索引の両方から参照できます。日付別の実験ディレクトリは experiments/2026-10/ と experiments/2026-11/ に移動しました。

## リポジトリの構成

```text
GraduationThesis/
├── README.md                  # 研究全体への入口
├── docs/
│   ├── research_overview.md   # 研究目的・問い・意義
│   ├── methods.md             # 分析手法・測定指標
│   ├── reference/             # 研究理解のための参考資料
│   ├── experimental_design.md # 実験条件・分析計画
│   ├── main_experiment_protocol_v0_95.md # 現行の統合プロトコル（正本）
│   ├── main_experiment_protocol_v0_9.md # 旧統合設計（保存）
│   ├── main_experiment_protocol.md # 以前のプロトコル（保存）
│   ├── main_experiment_design_v0_5.md # 設計議論v0.7の記録
│   ├── current_status.md      # 進捗・課題・次の作業
│   └── experiment_index.md    # 過去の実験・資料への索引
├── experiments/
│   ├── README.md
│   ├── 2026-10/               # 10月の実験
│   └── 2026-11/               # 11月の実験
├── Interim_Posters/           # 中間ポスター
└── lab_meeting_slides/        # 研究室ミーティング資料
```

## 記録の扱い

- **本実験の最新方針は [統合プロトコル v0.95](docs/main_experiment_protocol_v0_95.md) を参照してください。**
- 各実験フォルダには、その時点の計画・コード・結果を保存します。
- 過去の実験記録は、後から都合よく書き換えず、実行時点の記録として保持します。
- 古いREADMEは [README_previous_20261103.md](README_previous_20261103.md) に保存しています。旧状況の参照用であり、現在の方針には最新のドキュメントを優先してください。


## 過去のProbe再解析結果（2026-11-11・Phi）

**[結果の要約・統計上の注意・全CSVリンク](experiments/2026-11/1110_probe_reanalysis/FINDINGS_20261111.md)** · [GitHub保存結果](experiments/2026-11/1110_probe_reanalysis/results/20261111_173427/) · [Colabで再現](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)

- 既存評価AUCの平均 **0.9996** → 未使用説明文の平均 **0.8436**。概念ペアによって汎化性能が異なる。
- 252通りの学習ラベル置換×100構成＝**25,200再学習**。ランダムなラベルでAUC 1.0が **1,742回（6.91%）**。
- **高いAUC＝概念の思考量ではない。** 新しい説明文の品質と汎化性能を検証してからProbeの採用を判断する。

[実験一覧](docs/experiment_index.md)・[現在の進捗](docs/current_status.md)・[分析手法](docs/methods.md)からも上記の結果にアクセスできる。

## 追加検証（2026-11-10）

- [Probe再解析・独立評価実験](experiments/2026-11/1110_probe_reanalysis/README.md)：既存Hidden Stateを使った全252通りの学習ラベル置換検定と、新しい説明ファミリーによる汎化検証。
- [Google Colabで実行](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)
