# Graduation Thesis｜LLMにおける抑制概念と意味的距離

LLMに対する「Xについて考えないで」という抑制指示の下で、手がかりの意味的距離が内部表現と最終出力に与える影響を分析する卒業研究のリポジトリ。

このREADMEは研究全体への入口です。研究の考え方・分析方法・実験設計・進捗は、以下のドキュメントに分けて管理しています。

## はじめに読む

| ページ | 内容 |
|---|---|
| **[研究概要](docs/research_overview.md)** | 背景、研究目的、Research Question、研究の意義 |
| **[分析手法と測定指標](docs/methods.md)** | Probe、Generation、Logit Lens、意味的距離の扱い |
| **[実験設計と分析計画](docs/experimental_design.md)** | 4条件、比較方法、実験規模案、分析の順序 |
| **[現在の進捗と次の課題](docs/current_status.md)** | 直近の検証結果、残っている課題、次の作業 |
| **[実験記録・資料一覧](docs/experiment_index.md)** | 日付別の実験、コード、データ、発表資料へのリンク |

## 研究の要点

**Research Question**

> 「Xについて考えないで」という抑制指示の下で、手がかりの意味的距離（近い・遠い）は、LLMの内部表現と最終出力にどのような影響を与えるのか？

| 観察対象 | 主な方法 | 確認すること |
|---|---|---|
| 内部表現 | Probe | Hidden StateからX/Yをどの程度識別できるか |
| 最終出力 | Generation分析 | 対象概念Xが生成文にどの程度出現するか |
| 層別予測 | Logit Lens | 各層でX関連トークンの予測がどう推移するか |

本研究では「禁止すると逆に考えてしまう」という結果を前提にしません。抑制・増幅・距離による違い・明確な変化なしのいずれも、測定の妥当性を確認したうえで研究結果として扱います。

## 現在の状況

<sub>2026年11月10日整理。最新の実験記録は2026年11月4日まで。</sub>

- モデル比較・質問形式・採点処理・Probeの予備検証を実施。
- Phi-3.5 miniは次の確認候補だが、固定評価の基準を満たしておらず、本実験への採用は保留。
- Probeでは高いAUCが得られた条件もある一方、指示文や説明文に由来する情報を分離できているか、汎化性能の確認が必要。
- **本実験に使うモデル・課題・測定方法は未確定。** まず課題と測定方法を検証し、採用基準を固定してから本実験へ進む。

詳細は **[現在の進捗と次の課題](docs/current_status.md)** を参照。

## リポジトリの構成

```text
GraduationThesis/
├── README.md                  # 研究全体への入口
├── docs/
│   ├── research_overview.md   # 研究目的・問い・意義
│   ├── methods.md             # 分析手法・測定指標
│   ├── experimental_design.md # 実験条件・分析計画
│   ├── current_status.md      # 進捗・課題・次の作業
│   └── experiment_index.md    # 過去の実験・資料への索引
├── 1015/ ... 1019/             # 初期の実験記録
├── 1103_*/                    # 11月3日の追加検証
├── 1104_*/                    # 11月4日のモデル・課題・Probe検証
├── Interim_Posters/           # 中間ポスター
└── lab_meeting_slides/        # 研究室ミーティング資料
```

## 記録の扱い

- 最新の研究方針は docs/ 配下の文書を参照してください。
- 各実験フォルダには、その時点の計画・コード・結果を保存します。
- 過去の実験記録は、後から都合よく書き換えず、実行時点の記録として保持します。
- 古いREADMEは [README_previous_20261103.md](README_previous_20261103.md) に保存しています。旧状況の参照用であり、現在の方針には最新のドキュメントを優先してください。


## 追加検証（2026-11-10）

- [Probe再解析・独立評価実験](1110_probe_reanalysis/README.md)：既存Hidden Stateを使った全252通りの学習ラベル置換検定と、新しい説明ファミリーによる汎化検証。
- [Google Colabで実行](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)
