# 50 X/Y Concept Probe — Colab独立説明文検証

> **最新版（2026-11-24）：[v4 Colabを開く](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1124_probe_50pairs/qwen_probe_50pairs_balanced_validation_v4.ipynb)**。文章をタイプ別に2文ずつ生成・検査する別ファイルです。旧v1/v2/v3ノートブックは変更せず残しています。v4はまだ実行検証していません。


## 追加検証 v2：文章タイプ均衡版（2026-11-24）

**[Google Colabで開く](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1124_probe_50pairs/qwen_probe_50pairs_balanced_validation.ipynb)** · [ノートブック](qwen_probe_50pairs_balanced_validation.ipynb)

前回の50組を**全組そのまま**使い、学習文・評価文の双方に以下の文章タイプを**各2文ずつ**入れる追加スクリーニング。

- 構造・特徴（structure）
- 動作・行為（action）
- 場面・環境（situation）
- 用途・役割（function）

**82概念×（8学習＋8評価）＝1,312入力**。Qwen revision、Hidden Stateの取得位置（assistant-start）、第22/23/24層、Logistic Regression（C=0.1）、学習・評価文数、乱数seedはv1と同様。新しい文章はOpenAI APIで生成し、名称漏れ、近似重複、型の数を検査する。

結果には、**v1とv2のAUCを50組すべてについて並記**し、AUC≥0.80、補正前ラベル置換p≤0.05、BH-FDR q≤0.05を**別々**に集計。文章タイプ別AUCは評価文2件/ラベルなので探索的な診断のみ。文章内容やAPI生成も変わるので、AUC差を「文章タイプだけの純粋な因果効果」とは断定しない。

出力先：`experiments/2026-11/1124_probe_50pairs/results/20261124_probe50_balanced_v2/`。旧v1の結果には一切上書きしない。

**実行状況：ノートブック作成済み、Colab未実行。** 既存の`OPENAI_API_KEY`と`GITHUB_RESULTS_TOKEN`を利用できる。実行時間・費用の実測は未確認。

---


[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1124_probe_50pairs/qwen_probe_50pairs_validation.ipynb)

[ノートブック](qwen_probe_50pairs_validation.ipynb) · [候補50組](../../../docs/concept_pair_candidates_50_v0_1.csv) · [選定方針](../../../docs/concept_pair_selection_v0_1.md) · [現行プロトコルv0.9](../../../docs/main_experiment_protocol_v0_9.md)

## 目的

本実験開始前に、50 X/Y候補ペアの**概念識別Probeの学習・未使用説明文での評価**を行う。Avoid X/Neutral Xの内部状態・応答はこのノートブックで取得・利用しない。

## 準備と実行

1. 上記「Open in Colab」から開き、**GPU（T4以上）**を選択。
2. Colab Secretsに`OPENAI_API_KEY`と`GITHUB_RESULTS_TOKEN`を登録し、ノートブックへのアクセスを有効化。GitHub PATは`ryouy/GraduationThesis`の**Contents: read/write**のみ付与する。どちらのキーもセルやGitHubへ貼らない。
3. 最初からセルを実行。OpenAI APIを使って各概念8学習文・8独立評価文を作成。名称混入・重複の自動点検に失敗したら、原因を確認し、**文章生成条件を改変する場合は新RUN_ID**で実行する。
4. Qwen2.5-0.5B-Instructの生成開始直前Hidden Stateを第22/23/24層で抽出。50ペア各々の線形Probeを学習し、未学習説明文でROC-AUCを測定する。
5. 499回のラベル置換、Benjamini–Hochberg FDR感度分析、leave-one-training-family-outを実施し、**全50ペアの合否と限界**を記録する。レポートと元データはGitHubへimmutable保存する。

## データと結果

実行先：`experiments/2026-11/1124_probe_50pairs/results/20261124_probe50_independent_v1/`

- `candidate_pairs.csv`、`config.json`：候補・設定の凍結。
- `texts/concept_*.json`：概念単位で学習・評価文を中断再開しながら保存。
- `all_descriptions.csv`、`pair_lexical_audit.csv`、`train_eval_overlap_flags.csv`：元の入力と自動監査。
- `features/chunk_*.npz`：再現用のQwenのHidden State。
- `pair_probe_scores.csv`、`analysis_summary.md`、`manifest.json`：全50ペアの独立評価結果。

**未実行**：GitHubへ保存したのはノートブック・READMEであり、Colab GPU実行、OpenAI APIによる刺激生成、50ペアのROC-AUC結果はまだ得ていない。

## 研究上の注意

- OpenAI APIが作成した説明文の「未学習評価」は、文章文字列として学習データと分離されているという意味。**人間の独立した正解付けではない**。同一モデルに由来する文章の言い換えやテンプレートの癖が分類を容易にする可能性がある。抜き取り人手点検・異なる出典による再確認を推奨する。
- 暫定スクリーニングは**L24 AUC≥0.80かつ499置換のBH-FDR q≤0.05**。これはv1.0の最終採択基準の確定を意味しない。L24のLOO最低値とL23/L22のAUCも保存する。
- この判定はX/Y相対判別性能のみ。抑制下での絶対概念活性量・思考量・因果的抑制効果を証明しない。結果を見てからYを再選定する場合は、今回の探索結果を報告し、**新たな独立評価データで再検証する**。
- GPU実行には時間とAPI料金が必要。途中中断は保存済み刺激・GPUチャンクを再利用する。同じRUN_IDで内容が変化したファイルを上書きしない。
