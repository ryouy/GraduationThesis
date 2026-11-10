# Graduation Thesis｜LLMにおける抑制概念と意味的距離

LLMに対する「Xについて考えないで」という抑制指示の下で、手がかりの意味的距離が内部表現と最終出力に与える影響を分析する卒業研究のリポジトリ。

研究の考え方・分析方法・実験設計・進捗・実験記録を分けて管理しています。

## Research guide

| ページ | 内容 |
|---|---|
| [研究概要](docs/research_overview.md) | 背景、研究目的、Research Question |
| [分析手法と測定指標](docs/methods.md) | Probe、Generation、Logit Lens、意味的距離 |
| [実験設計と分析計画](docs/experimental_design.md) | 条件、比較方法、分析手順 |
| [現在の進捗と次の課題](docs/current_status.md) | 最新の検証結果と次の作業 |
| [実験記録・資料一覧](docs/experiment_index.md) | 個々の実験・データ・資料への索引 |

## Research question

> 「Xについて考えないで」という抑制指示の下で、手がかりの意味的距離（近い・遠い）は、LLMの内部表現と最終出力にどのような影響を与えるのか？

| 観察対象 | 主な方法 | 確認すること |
|---|---|---|
| 内部表現 | Probe | Hidden StateからX/Yをどの程度識別できるか |
| 最終出力 | Generation分析 | 対象概念Xが生成文にどの程度出現するか |
| 層別予測 | Logit Lens | 各層でX関連トークンの予測がどう推移するか |

特定の結果を前提にせず、測定の妥当性と再現性を重視します。

## Current status

<sub>2026年11月10日整理。実験結果の記録は2026年11月4日まで。</sub>

- モデル比較、質問形式、採点処理、Probeの予備検証を実施。
- Phi-3.5 miniは次の確認候補だが、本実験への採用は保留。
- Probeの識別性能と汎化性能、指示文・説明文に由来する情報の分離に追加検証が必要。
- **本実験に使うモデル・課題・測定方法は未確定。**

詳細：[現在の進捗と次の課題](docs/current_status.md)

## Repository structure

```text
GraduationThesis/
├── README.md
├── docs/                 # 研究方針・手法・進捗・資料索引
│   ├── research_notes/   # テーマに関する補助的な研究ノート
│   └── archive/          # 過去のREADMEなど
├── experiments/          # 実験コード・Notebook・設定・結果
│   ├── 2026-10/           # 10月の初期実験
│   └── 2026-11/           # 11月の追加検証
├── presentations/        # ポスター・研究室発表資料
└── archive/              # 初期の探索的テストなど
```

### Main folders

- [Experiments](experiments/README.md) — 日付別の実験
- [Presentations](presentations/README.md) — 中間ポスター・研究室ミーティング資料
- [Research documentation](docs/README.md) — 研究方針・方法・進捗
- [Archive](archive/README.md) — 過去の探索的資料

## Record policy

- 最新の研究方針は `docs/` 配下で管理します。
- 各実験フォルダには、その時点の計画・コード・結果を保存します。
- 過去の実験結果は上書きせず、実行時点の記録として保持します。
- 旧READMEは [docs/archive/README_previous_20261103.md](docs/archive/README_previous_20261103.md) に保存しています。
