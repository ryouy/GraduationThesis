# 本実験：実行・管理方針（2026-11-26）

[統合プロトコルv0.95](main_experiment_protocol_v0_95.md)第11・13節の更新メモ。4主要フェーズを20程度の独立したColabノートブックに分割し、中断再開と再実行範囲の最小化を優先する。構成・命名は実装時に調整可能。現時点では設計方針のみ採用し、実装・実験は未実施。

## 1. ノートブック構成（20本の基本案）

| Phase | ノートブック（拡張子 .ipynb） | 実行環境 | 処理 |
|---|---|---|---|
| 1 | 01_concept_candidates | CPU/API | X/Y候補生成、意味的距離・トークン数の測定 |
| 1 | 02_probe_text_generation | CPU/API | 学習・独立評価用説明文生成、品質検査 |
| 2 | 03_probe_hidden_states | GPU | 説明文の全24層Hidden State取得 |
| 2 | 04_probe_training | CPU | 層専用Probe学習、独立評価、置換検定、標準化パラメータ |
| 2 | 05_concept_selection | CPU | X/Y採択、不足候補の確認 |
| 2 | 06_cue_generation | CPU/API | 採択概念に対する本番用Cue候補生成 |
| 2 | 07_cue_selection | CPU/API | 距離測定、品質評価、Cue採択 |
| 3 | 08_main_hidden_states | GPU | 全入力の生成直前Hidden State取得 |
| 3 | 09_internal_measurement | GPU/CPU | Probe・Logit Lens測定 |
| 3 | 10_response_generation | GPU | Qwenによる回答生成 |
| 4 | 11_response_evaluation | CPU/API | 原回答の明示的言及・意味的同定・妥当性等の評価 |
| 4 | 12a_concept_analysis | CPU | 概念別相関・回帰・偏相関 |
| 4 | 12b_mixed_effects | CPU | 混合効果モデル・全体傾向 |
| 4 | 12c_condition_analysis | CPU | Avoid X/Neutral X比較 |
| 4 | 12d_layer_analysis | CPU | 全24層の分析 |
| 4 | 12e_category_analysis | CPU | 10カテゴリー比較 |
| 4 | 12f_metric_comparison | CPU | Probe/Logit Lens比較 |
| 4 | 12g_output_analysis | CPU | 最終出力と内部表現の対応 |
| 4 | 12h_sensitivity_analysis | CPU | 頑健性・感度分析 |
| 4 | 12i_visualization | CPU | 保存済み統計量から図表・統合レポート作成 |

Phase 1–2は必要な候補のみ反復する。Y変更やX入れ替え時は該当候補の説明文・特徴量・Probe等だけ追加処理し、既存成果物を上書きしない。Cue採択後にX/Yが変わる場合は依存データを再検証する。最終採択集合・Cue・Probe・プロンプト・解析計画・コード等をv1.0として凍結してからPhase 3へ進む。Phase 4の内部分析は必要な内部測定が揃えば回答評価と独立に実行可能。出力との対応分析は評価完了を要する。

## 2. チェックポイント・中断再開

| 処理 | 保存単位の基本案 |
|---|---|
| X/Y候補 | 概念単位 |
| 説明文生成 | 概念×学習/評価区分、部分合格文も保存 |
| Cue生成・選定 | 概念×距離帯等、部分合格文も保存 |
| Hidden State取得 | 概念または処理バッチ |
| Probe学習 | 概念ペア単位 |
| 置換検定 | ペア×層または検定バッチ |
| 内部測定・Qwen回答生成 | 概念または入力バッチ、回答ID/seed別に完了確認 |
| AI評価 | 25–50回答程度のバッチ（暫定） |
| 統計・可視化 | 分析手法・テーマ・図表単位 |

全ノートブックでGitHubを永続保存先とする。Google Driveは使用しない。処理単位とアップロード単位は分けてよいが、未保存の作業量を制限する。成果物を追記型の不変チャンクとして保存し、保存確認後に完了状態を記録する。途中の成功結果も可能な限り保持し、再開時に重複を避ける。保存前の突然の切断で失われた処理のみ再実行が必要となる可能性がある。

再開手順：manifest取得 → version・入力/設定/コードのSHA照合 → 保存済み成果物と処理ID・件数・ハッシュ検証 → 完了済み処理をスキップ → 未完了の処理だけ実行 → チェックポイント保存。前工程の必須データが欠ける場合は不足を明示して停止する。完了フラグだけを信用せず実データを検証する。

API一時障害は上限付き再試行・バックオフ。恒久的エラーや認証エラーは停止。GitHub保存失敗は再試行後に停止し、未保存のまま長時間の処理を続けない。秘密情報はColab Secrets（GITHUB_RESULTS_TOKEN等）で管理し、ログ・リポジトリに含めない。

## 3. 保存・競合対策・構成

```text
main_experiment/
├── README.md
├── config/
├── common/
│   ├── github_storage.py
│   ├── checkpoint.py
│   ├── api_client.py
│   ├── validation.py
│   └── logging_utils.py
├── notebooks/
│   ├── phase_01_preparation/
│   ├── phase_02_training/
│   ├── phase_03_inference/
│   └── phase_04_analysis/
└── runs/{run_id}/
    ├── manifest.json
    ├── concepts/
    ├── probe_texts/
    ├── probe_hidden_states/
    ├── probes/
    ├── cues/
    ├── main_hidden_states/
    ├── internal_scores/
    ├── responses/
    ├── evaluations/
    ├── analysis/
    ├── figures/
    ├── checkpoints/
    └── logs/
```

配置先・名称は既存experiments構造との整合性を確認して実装時に決定する。共通config JSON・共通Pythonモジュールを使用し、読み込むコードのcommit/versionも固定する。run_id・phase・処理ID・versionで出力先を分離し、同一パスへの並列書き込みを避ける。GitHub競合時は最新版・SHAを再取得し、既存チャンクを照合してから上限付きで再試行。共有manifestの更新は直列化または競合検出付き更新とし、他工程の成果を消さない。過去のノートブック・実験結果の上書きは禁止。修正時は新しいversion、再実験は独立したrun_idを使用する。

| データ | 形式候補 |
|---|---|
| 概念、説明文、Cue、距離、評価、統計量 | CSV/JSONL（大規模表はParquetも可） |
| Hidden State | 概念・バッチ別の圧縮NPZ |
| Probe係数・scaler・標準化パラメータ | NPZ/JSON |
| 原回答・ログ | JSONL |
| 設定・manifest・進捗 | JSON |
| 図・レポート | PNG/SVG/Markdown |

GitHub Pagesで閲覧しやすいCSV・Markdownの主要結果を残す。大容量データはファイル上限・API転送制約・リポジトリ総容量を考慮して分割する。各成果物には入力ID・候補ID・層・条件・seed等の結合キー、件数、型、SHA-256を付与する。

## 4. 計算資源・分離の原則

100 Xなら2,400 Cue、5,000ユニーク入力、25,000回答、最大2,400採択ペア別・層別Probe。本実験の生成直前Hidden Stateだけで5,000×24×896×4 byte＝430,080,000 byte（約430 MB、圧縮前）。学習評価用特徴量、候補探索、teacher forcing、その他の成果物は別途見積もる。

- 全24層を1回のforward passで取得し、生成反復ごとに内部測定を繰り返さない。
- Hidden State取得とProbe学習・置換検定を分け、保存済み特徴量からCPUで学習可能にする。
- 08/09間で必要なGPU計算を分担し、単一トークン投影と複数トークンteacher forcingを区別する。不要な再forwardを避け、計算効率に応じてGPU工程内の共通処理をまとめてよい。
- 原回答生成とAPI評価を分離し、評価方法の変更で原回答を再生成しない。
- 統計量と図の生成を分離し、可視化の変更だけならモデル実行・統計再計算を不要にする。
- 統計の詳細は[統計分析方針](statistical_analysis_policy_20261126.md)に従う。

## 5. 実装前の未確定事項

実測GPU時間・API費用・GitHub総容量およびアップロード方式、最適チャンクサイズ、再試行上限・費用上限、依存関係とデータスキーマ、共通モジュール、チェックポイント復元テスト・競合テストを確定する。20本の構成は採用する基本案であり、必要に応じて追加・統合してよい。今回ノートブック作成や追加実験は実施しない。
