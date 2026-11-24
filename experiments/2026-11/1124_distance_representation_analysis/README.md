# 意味的距離と内部表現の再分析 (2026-11-24)

[Open in Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1124_distance_representation_analysis/distance_representation_analysis.ipynb)

既存4概念のパイロットとNeutral X追加実験を使う探索的再分析。CPUで実行可能、OpenAI API不要。関連48 Cueを連続距離で分析し、無関係・Cueなしは別扱い。概念別のProbe／Logit Lens散布図、層別推移、相関ヒートマップ、傾き差、CSV、PDF、manifestを出力する。

Colabで上から実行。結果は /content/distance_analysis に保存。最後のセルで PUBLISH=True にすると GITHUB_RESULTS_TOKEN を使い新規結果ディレクトリへ保存する。既存結果は上書きしない。

未実行：ノートブック作成時点では分析結果は未生成。50組のProbe検証および後続の1124_pre_main_experimentとは独立。後者は50組の検証・概念選定後に実施する。

既存の刺激は4概念すべて乗り物で、人手監査未了。相関・傾きは記述的な探索結果であり、因果効果や思考量を示さない。
