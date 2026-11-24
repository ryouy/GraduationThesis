# 1124 Pre-main experiment

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1124_pre_main_experiment/pre_main_experiment.ipynb)

本実験v0.9の探索的縮小版。Probe50 balanced v5の33通過組から各カテゴリー1組（C01, C06, C12, C16, C25, C27, C35, C38, C42, C46）を固定。10概念・関連5帯×4＋無関係4、Cueなし、Avoid/Neutral、500入力。既存v5の保存特徴からProbeを復元してAUCを照合。新規CueをAPI生成、距離はall-mpnet-base-v2、Qwen固定revision。Probe L22–24・Logit Lens L1–24、生成1回。

GPU T4以上、Colab Secrets: OPENAI_API_KEY, GITHUB_RESULTS_TOKEN。上から実行。API生成と推論はGitHubにチェックポイント保存、既存結果は上書きしない。別run IDで設計変更。結果方向に依存した再選定禁止。

結果は results/20261124_pre_main_v1/ に保存。散布図、層別推移、ヒートマップ、条件差、集計、manifestを生成。未実行。AIによる刺激生成・表層監査であり、人手監査は未実施。
