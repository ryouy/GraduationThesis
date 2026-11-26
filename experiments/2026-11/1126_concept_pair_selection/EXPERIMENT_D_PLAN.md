# 実験D：概念ペア間距離とCue選定可能性（探索的、未実行）

[Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/experiments/2026-11/1126_concept_pair_selection/experiment_D_cue_joint_selection.ipynb)

## 固定入力
- Bの75主分析ペア＋旧Yアンカー5（別集計）、既存700 Cue（旧品質通過622）、固定実測dX/dY・X/Y距離。B commit ada2278f06f89a9adc32c4efe2eab083935cfd68、C-small commit 6eb730f8dcaf48bfce9d98825b13e41d2a4dbd25。入力ハッシュを検証する。新規生成API・埋め込み推論・GPU不要。
- Bの固定setting C（最大±.04、帯間隔≥.03）を変えない。関連5帯×4タイプ＋無関係4タイプ＝24スロット。各1文、名称・明白な別名露出除外、近重複SequenceMatcher≥.80禁止。
- 主分析: 旧品質通過かつ新Y名称露出なし。感度分析: 既存部分意味監査で判明した不適格・不確実Cueも除外。未監査分は未監査として記録。Bの構造的最大採択数との一致を確認。

## 比較
- MILPで最大採択数を厳密計算。ベースラインは同数でdX帯中心からの絶対誤差を最小化（dY不使用）。
- jointは同じ最大数を維持し、欠落帯を優先回避し、|Spearman rho(dX,dY)|≤.30かつ5帯のdY平均最大差≤.05を優先。次いでv4と同様 max(|rho|/.30,spread/.05)+.1*sum(normalized)＋微小中心誤差。3 seed (11,23,37)×1200 step、v4より軽量。近似探索なので基準未達は不可能の証明ではない。
- 24文の構造的完全・両数値基準達成・双方達成を分ける。関連のみの相関・最大差、欠損帯、候補不足、文面監査状況、選定前後の差を保存。無関係Cueは主距離相関に含めない。
- 5 X内の距離関連、距離五分位、絶対距離帯、カテゴリー、24文完全集合のみの分析。C-small 25ペアのL24 AUCを選定後のみ結合、欠測を不通過扱いしない。
- 75ペアは独立観測ではない。Bの旧Yに依存した生成・監査、未監査Cue、カテゴリ/トークン交絡、少数X、Cの軽量学習を限界とする。正式採択や固定閾値の確定を主張しない。

## 実行
CPU Colab、GITHUB_RESULTS_TOKENのみ。OpenAI APIキー不要。5つのX単位で圧縮チェックポイント、例外時は未完了Xを再計算。GitHub書込み約25件。入力設定変更時は新run ID。成果物はPROVISIONAL、mainと既存結果は変更しない。ノートブックに小規模合成データのself-testを含める。
