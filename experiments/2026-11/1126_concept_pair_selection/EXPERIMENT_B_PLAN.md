# 実験B — X/Y間距離とCue距離の交絡（探索的・未実行）
[Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/experiments/concept-pair-selection-v1/experiments/2026-11/1126_concept_pair_selection/experiment_B_y_distance_confound.ipynb)

Aの完了commit 25856eaaf00c2aa10ea104093d5b47466674d3bb。Cue v1の固定commit c9f8d3d563f51d6bead9a3221dfa81554d23102d、700文、622旧品質通過、既存定義・埋め込みrevision・setting Cの境界を継承。既存結果を上書きしない。

- 5 X × 新規40 Y、5群各8件。独立API候補監査、除外理由保存。旧Yを独立アンカーとし、新規適格候補を実測距離で順位五分位に分けて中央値に近い3件ずつ採用。最大75＋5アンカー。欠員補充や基準緩和なし。全適格候補も補助分析。距離の同値・範囲を確認する。
- GPT-6 Luna medium、既存のChat Completions設定、temperature未指定。Qwen tokenizerのみCPUで使用。トークン差は除外ではなく記録、±1感度分析。X/Yカテゴリー内外の分析と共通距離範囲での記述比較。
- 関連Cueの共通旧品質通過集合を主分析。全700文・新Y名称露出除外後・無関係Cueを分離。元Yを避けて生成・監査した偏りに注意。
- 既存dXを固定、再計算で一致確認。dYを全適格Yで再測定。固定5帯別平均/SD、最大差、Pearson/Spearman、X内の距離と交絡の関係。75を独立観測としない。
- 新Yの意味的品質監査は既定で旧品質通過CueをXごとに元意図帯別2文（最大12）同じIDで抽出し、各選定Y・元Yを評価。標本内前後を比較。全監査はconfig内 semantic_audit_mode='full' に変更し別run ID、API費用増。機械的名称/別名監査は全候補×Cue。
- Cueの固定帯×4タイプ・近重複制約による構造的最大採択数をMILPで算出。Y距離joint最適化は実験Dで実施。構造的完全率とY統制成功率を混同しない。
- API checkpoint は開始記録・応答・失敗・usageを保存。途中再開は同一run ID、完了後設定変更は別run ID。Colab Secrets OPENAI_API_KEY / GITHUB_RESULTS_TOKEN。新規Cue生成・Probe学習なし。
- 人手監査なし、定義依存、カテゴリー交絡、5 Xの限界。正式基準未確定。

通常の成功API回数は生成5＋候補監査10＋標本Cue監査最大80＝最大95。失敗や全監査で増える。上限900試行、1タスク最大2試行。初期候補不足時は実数を報告。API利用料は実行アカウントに発生。
