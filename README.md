# Graduation Thesis｜LLMにおける抑制概念と意味的距離

LLMに対する「Xについて考えないで」という抑制指示の下で、手がかりの意味的距離が内部表現と最終出力に与える影響を分析する卒業研究のリポジトリ。

このREADMEは研究全体への入口です。研究の考え方・分析方法・実験設計・進捗は、以下のドキュメントに分けて管理しています。

## はじめに読む

| ページ | 内容 |
|---|---|
| **[研究概要](docs/research_overview.md)** | 背景、研究目的、Research Question、研究の意義 |
| **[分析手法と測定指標](docs/methods.md)** | Probe、Generation、Logit Lens、意味的距離の扱い |
| **[実験設計と分析計画](docs/experimental_design.md)** | 4条件、比較方法、実験規模案、分析の順序 |
| **[本実験プロトコル案（2026-11-12）](docs/main_experiment_protocol.md)** | 使用環境・モデル選定理由・Cue設計・4条件・Probe・Logit Lens・分析計画・再現性 |
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

## 現在の状況（2026年11月12日）

**本実験に向けた準備から、4概念のパイロット実験へ移る段階。** Qwen2.5-0.5B-Instructをパイロット用LLM、all-mpnet-base-v2を意味的距離の測定モデルとして採用する。

| 段階 | 実施内容 | 現在の到達点 |
|---|---|---|
| 従来のProbe測定検証 | [Phiの再解析](1110_probe_reanalysis/FINDINGS_20261111.md) | 既存文平均AUC 0.9996に対し新規文0.8436。汎化・ラベル置換の検証が必要と判明 |
| Qwenでの候補探索 | [100概念v2の結果](1111_qwen_probe_100concepts_v2/results/20261112_qwen100_richer_dedup_v2/analysis_summary.md) | 100候補中69概念が評価可能、32ペア・12ターゲットが探索的基準を通過 |
| 新規説明文による再確認 | [独立文検証結果](1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md) | 16ターゲット中、FDR感度分析後も4概念（boat / bus / bicycle / motorcycle）が複数距離帯で再現 |
| Cueの作成・距離測定 | [240候補の測定](1112_cue_semantic_distance/results/20261112_cue_distance_pilot_v1/analysis_summary.md) | 4概念×60文の距離計測完了。64文を暫定選定 |
| Cueの内容監査・固定 | [固定刺激と17文差し替え記録](1112_cue_semantic_distance/final_stimuli/20261112_frozen_ai_audit_v1/README.md) | 64文中17文を元の候補から差し替え。各概念で近・中・遠の範囲は重複なし。**AI監査済み、人手評価は未実施** |

**次の作業：** [パイロット実験プロトコル](docs/main_experiment_protocol.md)に従い、凍結したCueを使って4条件（Base / Think X / Avoid X / Think Y）の生成・Probe・Logit Lens測定を行う。モデルの回答形式・Probeの適用可能性・判定方法はパイロットで診断する。**抑制指示の効果については、まだ結果が出ていない。**

詳細は[最新の進捗](docs/current_status.md)と[実験一覧](docs/experiment_index.md)を参照。

## リポジトリの構成

```text
GraduationThesis/
├── README.md                  # 研究全体への入口
├── docs/
│   ├── research_overview.md   # 研究目的・問い・意義
│   ├── methods.md             # 分析手法・測定指標
│   ├── experimental_design.md # 実験条件・分析計画
│   ├── main_experiment_protocol.md # パイロット・本実験の方法と評価
│   ├── current_status.md      # 進捗・課題・次の作業
│   └── experiment_index.md    # 過去の実験・資料への索引
├── 1015/ ... 1019/             # 初期の実験記録
├── 1103_*/                    # 11月3日の追加検証
├── 1104_*/                    # 11月4日のモデル・課題・Probe検証
├── 1110_probe_reanalysis/      # Phi Probe再解析
├── 1111_qwen_probe_100concepts_v2/ # Qwen概念候補の探索
├── 1112_qwen_probe_independent_confirmation/ # 未使用説明文での独立検証
├── 1112_cue_semantic_distance/ # Cue距離実測・監査・固定
├── Interim_Posters/           # 中間ポスター
└── lab_meeting_slides/        # 研究室ミーティング資料
```

## 記録の扱い

- 最新の研究方針は docs/ 配下の文書を参照してください。
- 各実験フォルダには、その時点の計画・コード・結果を保存します。
- 過去の実験記録は、後から都合よく書き換えず、実行時点の記録として保持します。
- 古いREADMEは [README_previous_20261103.md](README_previous_20261103.md) に保存しています。旧状況の参照用であり、現在の方針には最新のドキュメントを優先してください。


## 過去のProbe再解析結果（2026-11-11・Phi）

**[結果の要約・統計上の注意・全CSVリンク](1110_probe_reanalysis/FINDINGS_20261111.md)** · [GitHub保存結果](1110_probe_reanalysis/results/20261111_173427/) · [Colabで再現](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)

- 既存評価AUCの平均 **0.9996** → 未使用説明文の平均 **0.8436**。概念ペアによって汎化性能が異なる。
- 252通りの学習ラベル置換×100構成＝**25,200再学習**。ランダムなラベルでAUC 1.0が **1,742回（6.91%）**。
- **高いAUC＝概念の思考量ではない。** 新しい説明文の品質と汎化性能を検証してからProbeの採用を判断する。

[実験一覧](docs/experiment_index.md)・[現在の進捗](docs/current_status.md)・[分析手法](docs/methods.md)からも上記の結果にアクセスできる。

## 追加検証（2026-11-10）

- [Probe再解析・独立評価実験](1110_probe_reanalysis/README.md)：既存Hidden Stateを使った全252通りの学習ラベル置換検定と、新しい説明ファミリーによる汎化検証。
- [Google Colabで実行](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)
