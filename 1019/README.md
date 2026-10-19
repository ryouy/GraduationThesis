## 改善版（推奨：全24層・同一系列の前後測定）

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1019/semantic_distance_layer_probe_v2.ipynb)

新しいノートブック：[`semantic_distance_layer_probe_v2.ipynb`](semantic_distance_layer_probe_v2.ipynb) ／ [改善内容・実行方法](README_v2.md)。結果は `1019/results_v2/<UTC実行ID>/` に保存されます。旧版と旧結果は以下に残しています。

---

# 1019 — Semantic distance × Suppression（層別 Concept Probe 実験）

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1019/semantic_distance_layer_probe.ipynb)


## 何を調べるか

LLMに概念Xを考えるなと指示したあと、意味的距離の異なる手がかりを与えると、モデル内部のX/Y識別スコアが各層でどう変化するか。通常指示（neutral）と抑制指示（suppression）の相違を中心に検証する。

- モデル：Qwen/Qwen2.5-0.5B-Instruct（1015 v3と同じ）
- 概念：既存の8組の X / Y
- 条件：neutral、affirm、suppression、replacement（4種類）、および手がかりなしの基準
- 手がかり：near / medium / far / unrelated（暫定4群）×各2例／概念、計64例
- 独立の意味的距離指標：MiniLM埋め込みによる1 − cosine類似度（人手評定ではない）
- Hidden State：指定した6層（4、8、12、16、20、24）で共通のassistant開始境界から読み出す
- Probe：X/Y二値の正則化ロジスティック回帰。学習16例／ペアと、語形なし説明文12例／ペアの評価を分離
- 主要比較：SuppressionとNeutralの手がかり効果の差の差（DID）。Concept単位の探索的Bootstrap
- 出力：CSV 10件以上、図4件以上、設定JSON、結果README。オプションの自由生成が有効なら追加CSVと図

## 使い方

1. 上のリンクをColabで開く。
2. 「ランタイムのタイプを変更」→ GPU（T4）を選ぶ。
3. 結果をGitHubへ反映させる場合、Colabの「シークレット」に `GITHUB_RESULTS_TOKEN` を設定し、ノートブックのアクセスを許可する。トークンには対象リポジトリの **Contents: Read and write** 権限が必要。
4. 「すべてのセルを実行」する。
5. Colab内の `/content/GraduationThesis/1019/results/<UTC実行ID>/` にCSV・PNG・JSON等を生成する。
6. トークンが有効なら最後のセルで `main/1019/results/<UTC実行ID>/` にファイルごとにアップロードする。トークンがない場合も、`1019/results/<UTC実行ID>_results.zip` をダウンロードできる。

各実行はUTCタイムスタンプ別ディレクトリを使用。既存の1015/1016のファイルは書き換えない。

**注意：このノートブックはGitHubに配置した実験コードであり、Colab上の実測はまだ実施していない。結果フォルダはノートブック実行時に生成される。**

## 研究上の解釈と限界

- Probeが読むのは**X対Yの相対的識別可能性**であって、絶対的な概念活性や「忘却」を直接測定するわけではない。
- 禁止概念Xは指示文に明示されており、neutralとsuppressionではX出現回数と入力長も異なる。文面の交絡を認めたうえで結果を読む。
- 距離帯4群の順序は暫定的。MiniLM距離で順序が崩れれば診断CSVに残し、連続的な測定距離で分析する。将来的に人手関連度評定が必要。
- 層別Probeは held-out description AUC≥0.75 を主図の探索的基準にするが、全層の生スコアは保存する。
- 比較は別プロンプトの読み出しであり、単一推論過程における時系列の「再活性化」は証明できない。
- 自由生成の同一プロンプト読み出しは、Probe学習時の `Topic:` 終端とは分布が違うため**補助的**に扱う。
- 母集団への一般化や因果効果は、この探索的8概念の実験のみから断定できない。

背景：[1015 v3](../1015/white_bear_and_zhou_pilot_v3.ipynb) ／ [1016 研究の流れ](../1016/00_一ページでわかる研究の流れと予備実験.md)
