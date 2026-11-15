# 20組の指示・説明文Probe診断

状態：コードと人工特徴テストを準備。実モデルの結果はまだない。

[Colabで開く](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1104_instruction_probe_20pairs/instruction_probe_20pairs.ipynb)

T4 GPUを選び、すべてのセルを実行。最後にGitHub mainへ検算済み結果を保存する。既存の結果を上書きしない。

- 20組・40概念、学習1,200行、評価説明800行、5指示条件。
- 評価は各概念5説明×4表現。20独立文ではなく、5説明ファミリーとして集計。
- 6,901 unique forward、5学習構成、200 Probe、61,000スコア。
- 主測定は層31・assistant_start、補助は同層context_end。
- 100主Probe×100回のファミリー単位ラベルシャッフル。
- 100入力ごとにチェックポイント。同じOUT・同じランタイム環境なら抽出セルを再実行して再開可。
- トークンはColabシークレットからのみ取得。保存失敗時は保存セルのみ再実行。

CSVはprepare.pyで決定的に生成する。FROZEN_SHA256.jsonと照合してから抽出し、実行時にfreeze.pyを実行しない。

詳細・限界は[PLAN.md](PLAN.md)。元の3組は含むが文章は新規の作成規則。AI作成の文章で、人による独立した一意性確認は未実施。概念の意味情報・単語の影響・構文の影響を完全には分離しない。
