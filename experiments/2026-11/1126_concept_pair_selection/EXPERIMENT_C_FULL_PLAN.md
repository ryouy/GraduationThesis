# 実験C — X/Y意味的距離とProbe識別性能（探索的）
[Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1126_concept_pair_selection/experiment_C_distance_probe_full.ipynb)

Bの固定75ペア＋旧Yアンカー5、B commit ada2278f06f89a9adc32c4efe2eab083935cfd68。v0.97 (8fc35efe88604f2b47577958b7feb58efde0ba94) の64学習/32探索評価、4タイプ均衡、全24層、最後の入力トークン、X正例、学習のみScaler fit、LR C=.1 liblinear、seed42、max_iter2000、評価ラベルのタイプ内均衡置換9999回片側plus-one。最終独立評価32文は本実験採択用の別工程。L24 p<=.05かつAUC>=.8探索通過、探索的BHは固定75 L24と固定75×23を別族、アンカーは補助。正式採択なし。

- 同一X内の15Y＋アンカーでX説明文を共有（X5ユニット、Y80ユニット、計85×96=8160文）。Yの定義はBを固定、Xには全選定Y名・別名を禁止、YにはXと自身名・別名を禁止。この非対称性と共有Xの依存性は限界。別のXに同じYがあってもペア専用文。
- 学習と探索評価は別API生成、過去の文面/事実の近重複を機械・AI監査。全件AI監査、失敗は不足のみ追加生成。人手標本はpendingとして保存、正式採択に使わない。
- GPT-6 Luna medium、temperatureなし。1ユニット8生成＋8監査が理想下限、85ユニットで約1360成功呼出し。再試行で増える。6並列、GitHub通信直列・書込み間隔1.2秒以上。上限3500。APIごとのローカルジャーナル、GitHubは学習/評価split完了および例外時に不変スナップショットを保存（通常170件）。ランタイム消失時は最後のGitHubスナップショット以降の応答が失われ、再課金される場合あり。429/レート制限403はRetry-After/resetを尊重して待機。費用は実行者負担。GPU T4等、同時に同じrunを実行しない。
- Qwen float32 eager、各説明文の全24層Hidden Stateを一度抽出、48文単位の特徴量チェックポイント。約0.7GB生配列（圧縮サイズは変動）。Probe学習はCPU。全ペア×24層評価、予測スコア・p/q・タイプ別AUCを保存。
- Cの主分析はXごとの距離とL24 AUCの関係。全層、相対/絶対帯、カテゴリー、token差を補助分析。Bの共通旧品質Cue交絡指標との結合は記述的、最終Y距離最適化Dは別。75ペアを独立観測としない。抑制条件・最終出力は使わない。
- 既存結果・mainは変更しない。OPENAI_API_KEY/GITHUB_RESULTS_TOKEN。完了後は新run ID。v2 run ID: 20261126_concept_pair_distance_C_v2。未実行、実行時にエラーや品質不足なら停止して記録。
