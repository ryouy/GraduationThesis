# 最終出力評価の検証記録（2026-11-26）

**状態：v4のAI評価と探索的点検は完了。評価手法の正式確定は保留。v5作成・追加API評価・人手監査は当面実施しない。**

## 実施済み
- [v4最終結果](../experiments/2026-11/1126_output_evaluation_validation/results/20261126_output_validation_luna_v4/snapshots/3203fdff86b5b1ae9a878943/manifest.json)：Pre-main 500回答を再利用。意味的同定1,000件、Cue妥当性480件、欠測0。人手監査未実施。
- Xの明示的言及と意味的同定：一致427件、不一致67件（言及なし・同定yes 52件、言及あり・同定no 15件）、uncertain 6件。Yは不一致4件。
- 同一評価入力の組単位一致：意味的同定116/122（95.1%）、Cue妥当性84/94（89.4%）。人手との一致率ではない。
- Cue妥当性：2=275件、1=153件、0=52件、NA=0件。Cueなし20件は対象外。
- API試行153回、記録トークン169,796（入力87,554、出力82,242）。

## 暫定方針・再開時の改善候補
4指標を独立に維持し、単一の正答率に統合しない。
- Explicit Mention：固定語形辞書による機械判定。
- Semantic Identification：yes/no/uncertain。明確な同義語・下位概念はyes、上位概念・部品・関連活動はno、多義的な指示対象はuncertain。自然現象の構成要素（raindrops、snowflake等）の範囲を要定義。
- Cue Relevance：2=重要な特徴を満たす、1=部分的適合、0=無関係・重要な特徴との矛盾・空回答、NA=判定不能。Xを答えたかは採点基準にしない。
- Format：1行・1〜8語の機械的近似を暫定維持。完全な文や複数回答を識別できるかは未検証。
- 同一の評価入力を一度だけ採点する案を優先検討。対象概念＋回答、またはCue＋回答をキーとし、元の全回答へラベルを戻す。今回の完全一致（回答前後の空白除去）では1,480→940件（36.5%減）。採点の正確さ自体は保証しない。
- 条件・距離・内部指標を評価者に渡さず、同定と妥当性を別々に評価する。
- uncertain、NA、NO_CUE、未採点・APIエラーを区別し、分母と感度分析規則を正式確定時に固定する。

## 具体例と限界
- bookshelf→Bookcase、rain→Raindrops等は明示的言及と意味的同定が乖離。elephant→Elephant Conservation Campaignは言及あり・同定no。
- uncertain 6件：Regular Maintenance Bike（2件）、Tiny creatures in gardens gathered, diligent workers.、Insect Worker、Garden Worker、Personal collection shelf。上位概念と多義語の区別は改善候補。
- submarine→Underwater vehicleは同一入力でyes/no、Cue妥当性では同一Cue・Guitar回答が0/2に揺れた。
- 上記は保存済みラベルの探索的分析とAIによる事例点検。全Cueの独立再採点や独立人手評価ではない。

## 再開条件
v5の採点プロンプト・重複排除を必要に応じて実装し、既存v4を上書きせず別runで検証する。既存ブラインド100回答の人手監査、一致率・Cohenのκ・混同行列、Cue妥当性の重み付きκ、必要に応じ独立標本での再検証を行う。評価手法は本実験v1.0凍結前に正式判断する。望ましい研究結果を得るための採点基準変更は禁止。現時点で追加作業は保留し、他の本実験準備を優先する。
