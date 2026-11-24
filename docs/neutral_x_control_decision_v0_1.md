# ② X名称提示の交絡対策：Neutral X追加パイロット設計 v0.1

> 2026-11-24。**追加340生成・内部指標取得・比較集計を完了。②の限定パイロットは実施済み。** 独立人手監査は未実施。既存パイロットv1のデータ・分析結果・刺激は変更しない。

## 問題と目的

従来のBaseには対象Xの名前がない一方、Think X / Avoid X / Think YはX名がある。したがってAvoid XとBaseの差は「抑制指示」のみの効果ではない。追加するNeutral Xによって「名称を提示したが抑制・注意誘導していない」参照条件を設ける。

## 追加条件（他の部分は既存v1と同一）

- 条件名：`Neutral X`
- 指示文：`The word is {X}. Read the clue and briefly name the thing it brings to mind.`
- Cue部分：既存と同一の `Clue: {cue}\nAnswer with one short phrase.`。Cueなしもv1と同じ方法で構成する。
- Qwenモデル・revision・chat template・system instruction・生成設定・seed集合・Probe・Logit Lens・辞書はv1から変更しない。
- 対象：bicycle / boat / bus / motorcycle の4 X ×（16固定Cue＋Cueなし1）＝**68ユニーク入力、5反復で340回答**。新規Hidden State 68入力、Probe 68×3層＝204スコア、Logit Lens 68×24層×2＝3,264件が想定値。
- 既存4条件のデータは再生成せず、追加条件の結果を新しい結果ディレクトリに保存し、対応するID・Cue・seedで統合集計する。
- 追加条件で出力・内部状態を記録できれば十分。追加実験は**原則1回**とし、事後的に都合の良い文面・概念・Cueを選び直さない。

## 比較（確認前に宣言）

主たる観察比較は、**同一X・Cue内**の `Avoid X − Neutral X` のExplicit Mention Rate差（および距離帯による違い）。副次比較は `Neutral X − Base`、既存の `Avoid X − Think X`、Semantic Mention Rate（評価規則①の固定後）、Probeの同一ペア・同一層でのスコア差、Logit Lens。近・中・遠はCue単位で集計し、無関係とCueなしを別の対照として扱う。5生成を独立した5 Cueとみなさない。

## 解釈の限界

Neutral XはXの名称提示を合わせるが、命令の語数・文法・トークン位置・表現上のニュアンスは一致しない。ゆえに `Avoid X − Neutral X` を厳密に純粋な否定命令の因果効果とは呼ばない。`Neutral X − Base` も語提示と文の追加が交絡する。「逆説的抑制の証明」は主張せず、**名称提示を揃えた対照での指示条件差**として報告する。

## 最低限の実行品質・終了条件

1. 68入力・340生成がそろい、重複・欠損・形式逸脱・トークン切り詰めを記録。
2. v1と同じ条件を維持したことをmanifestで示す。Probe・Logit Lensの対応位置と最終層一致の整合性を検査する。
3. 同一Cue対応差の概要表と概念別の結果を作る。主指標は①の評価ルールの固定に従う。
4. Neutral Xの言及率がどちらへ動いても、結果を記述して②の追加パイロットを終了する。明らかなバグがなければ刺激や文面の最適化ループを行わない。
5. 本実験の確定は①監査と③Cue監査、④Probe判断、⑤分析仕様の凍結が済んでからとする。

## 現状

- [x] 対照条件の目的、文面、実験範囲、主要比較、停止規則を文書化
- [x] [Neutral X追加Colab](../experiments/2026-11/1112_qwen_suppression_pilot/qwen_neutral_x_addon_4concepts.ipynb)をGitHubに作成。既存v1から生成・Probe・Logit Lensを継承し、追加条件68入力・340回答だけを処理する構成（**GPUでの実測と実行時検証は未実施**）
- [x] 追加340回答・204 Probeスコア・3,264 Logit Lens行を取得し、GitHubに保存（**独立人手監査は未実施**）
- [x] 対応Cue単位の比較を集計。②の追加対照実験は終了し、結果を固定

関連：[本実験プロトコル](main_experiment_protocol.md) / [出力評価①](output_evaluation_decision_v0_1.md) / [パイロット統合解釈](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)

## 実測結果と②の終了判断（2026-11-24）

[追加パイロット結果](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/analysis_summary.md) · [manifest](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/manifest.json) · [Cue対応集計](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/paired_cue_explicit_effects.csv)

- manifestのstatusは`COMPLETED_NEUTRAL_X_CORE_PILOT`。68入力・340生成・204 Probe・3,264 Logit Lens・5チャンク。最終層logits最大整合誤差`3.3378601e-05`。
- 関連Cue（4概念×12Cue×5生成=各条件240回答）の明示的X言及率は、Base 7.5%、Neutral X 57.9%、Think X 56.3%、Avoid X 34.6%、Think Y 8.8%。
- **主要比較Avoid X − Neutral X = −23.3パーセントポイント**。距離帯別には近−13.75pt、中−22.5pt、遠−33.75pt。いずれも探索的な記述統計。
- 第24層ProbeのAvoid−Neutral平均差はbicycle−0.188、boat+0.211、bus−0.472、motorcycle−0.596（概念間で生のスコアを無条件に平均しない）。
- 第24層Logit LensのX/Y対数尤度差は4概念ともAvoid Xの方が低い。
- **②の判断：追加パイロットはここで終了。** Neutral Xを複数案作って効果の大きい条件を選ぶことはしない。主張は「X名称提示を含む中立参照条件よりAvoid Xで明示的言及が少なかった」に限定。厳密な純粋抑制効果・逆説的抑制の因果証明ではない。
- ①の監査・③Cue監査・④Probeの位置づけは引き続き別項目で扱う。
