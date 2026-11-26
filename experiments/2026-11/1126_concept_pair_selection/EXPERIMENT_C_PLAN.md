# 実験C-small — 軽量探索版（未実行）
フル版は experiment_C_distance_probe_full.ipynb と EXPERIMENT_C_FULL_PLAN.md に保存。今回の既定は軽量版。
- Bの75組からXごとの各距離五分位でBのband_centerに最も近い1組を選択。距離だけを使用、同値はconcept/idで固定。5 X×5 Y=25。旧Yアンカーなし。Bの原データとハッシュ固定。
- X 5、Y 25、計30ユニット。16学習/8探索評価文/label、各4/2文×4タイプ。720説明文。学習・評価は別生成と監査。1 splitをまとめて生成・監査し、不足分のみ再試行。最低120 API呼出し、上限300。6並列。料金は実測usageで記録。
- Qwen固定revision、全24層、600 Probe、StandardScaler/LRは従来通り。評価タイプ内均衡置換の全1296通りを列挙（正確片側p、観測割当も含む）。探索的BH、正式採択不可。8文評価のAUCは不安定、各Xにつき5点なので関連の推定は粗い。
- 同一Xの説明文/特徴を共有、AI品質監査は全件、人手監査はpending。最終独立確認なし。正式採択はv0.97の64/32/新規32文が必要。
- GitHubに原則splitごと60回＋特徴30回＋ペア結果25回＋集計。ローカルジャーナル、例外時保存。別run ID 20261126_concept_pair_distance_C_small_v1。ランタイム消失時は未同期分を再生成する可能性あり。mainは変更しない。Colab未実行。
