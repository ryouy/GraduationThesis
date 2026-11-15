# 1019 v2：意味的距離 × 抑制概念表現（全24層・手がかり前後）

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1019/semantic_distance_layer_probe_v2.ipynb)

## なぜ作り直したか

1019 v1では、最終層のProbeは8概念中7概念がAUC≥0.75でしたが、中間層は評価基準に満たないものが多く、元のnear/medium/far/unrelatedという手がかりの距離順序も8概念中4概念で崩れました。

今回の改善版は、**どの層で、手がかりを処理した前後に、抑制対象Xと比較概念Yの識別スコアがどう変わったか**を、全24層で可視化するための新実験です。結果はまだ出ていません。

## 改善した点

1. **同一プロンプト内の前後比較**：各入力に`STATE:`という固定測定位置を2箇所設定。最初は手がかり前、2番目は手がかり後。Transformerの因果マスクのもと、同一forward passで内部ベクトルを取得。
2. **全24層を測定**：埋め込み後のTransformer Layer 1〜24の全層を記録（Layer 0は含めない）。
3. **Probe学習を改善**：語形を含む例と、名称を直接出さない意味記述の両方で学習。学習に使わない説明文で各層のROC-AUCを測定。AUC≥0.75だけを主要な解釈対象とし、非通過も生CSVへ保存。
4. **意味的距離の定量化**：Cueは8概念×12文の96例。別モデルMiniLMで各文の距離を評価。暫定ラベルを盲信せず、概念内距離順位による4等分と連続距離の両方で分析。
5. **禁止条件と参照条件を統制**：`You may think about X` と `Do not think about X` を対比し、Xをどちらも1回だけ書く。残余の表現は同じ。完全な同長ではないため、トークン長も保存。
6. **モデル非依存の補助計測**：Probeによる概念識別スコアに加え、手がかり前後のHidden Stateコサイン距離・相対L2変化量を保存。
7. **比較対象Yの対照実験**：Xに近いCueだけでなく、Yに近いCueをそれぞれ2例ずつ別途提示し、Probeが概念XとYの方向を識別するかを全24層で点検。\n8. **統計**：Concept（8組）単位でBootstrap。Cueごとの変動と概念間の変動を混同しない。各概念内の距離対効果の傾き、およびCueトークン数を調整した感度分析を出力。

## 実験条件と主指標

- モデル：`Qwen/Qwen2.5-0.5B-Instruct`（前回と同一）
- 条件：`neutral`（思考を許す参照条件）、`suppression`（抑制条件）
- 概念：8組、Cue：12×8＝96文、総処理系列：192（Probe学習・評価用文は別）
- 前後差：`Δ = X/Y Probe(after cue) − X/Y Probe(before cue)`
- 指示による交互作用：`I = Δsuppression − Δneutral`
- 距離対照を引いた差：`DID = I(cue) − I(同概念の最遠距離Cue平均)`
- 層別主解析：独立データでProbe検証を満たした概念に限ってLayer 1〜24で効果を比較。Layer 24を事前指定の主な検証対象とする。

## Colabでの実行方法

1. 上の「Open in Colab」を押す。
2. **ランタイム → ランタイムのタイプを変更 → GPU（T4）** にする。
3. 実験結果をGitHubへ自動反映するには、Colab左側の「シークレット」に `GITHUB_RESULTS_TOKEN` を設定し、Notebookアクセスを有効にする。GitHub tokenには対象リポジトリの `Contents: Read and write` 権限が必要。
4. **すべてのセルを実行**。結果はまず `/content/GraduationThesis/1019/results_v2/<UTC実行ID>/` に保存。設定済みなら実行の終盤でGitHubの同名フォルダへCSV・PNGなどをアップロードする。
5. Secretがない場合も、最終セルで結果ZIPをダウンロード可能。

現時点では実験コードの追加のみで、**モデル実行と研究結果の検証はまだ行っていません**。

## 注意すべき解釈

- **ProbeはX対Yの相対識別情報**を測ります。X概念単独の活性量、意識的想起、忘却そのものではありません。
- 同一系列内の「前／後」は、モデルの内部処理における**異なるトークン位置**を意味します。長時間の思考や同一Hidden Stateの時間発展を直接追うものではありません。
- 層間でProbeの精度・通過概念が違うため、Layerごとの平均値をそのまま同じ母集団の変化とみなさないでください。
- Hidden Stateのコサイン距離は概念非依存の全体的な変化です。意味的な「再活性化」の証明にはなりません。
- 意味的距離はMiniLMの代理指標で、人間による事前評定や別エンコーダーでの再現性確認は今後の課題です。
- 統計区間は探索的で、n=8概念です。因果的な効果や一般性は主張できません。

## 関連ファイル

- [Colabノートブック](semantic_distance_layer_probe_v2.ipynb)
- [監査可能な96件の手がかり](stimuli_v2.csv)
- [Probe学習と評価の分離済み説明文](probe_description_bank_v2.json)
- [前回のノートブック](semantic_distance_layer_probe.ipynb)
- [前回の結果](results/20261019T130118Z/)
