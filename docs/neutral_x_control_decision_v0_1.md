# ② X名称提示の交絡対策：Neutral X追加パイロット設計 v0.1

> 2026-11-24。**追加条件の設計を固定するための計画。追加生成・人手監査・集計はまだ未実施。** 既存パイロットv1のデータ・分析結果・刺激は変更しない。

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
- [ ] 追加340回答の取得・監査
- [ ] 対応差を集計し、②の完了判断を記録

関連：[本実験プロトコル](main_experiment_protocol.md) / [出力評価①](output_evaluation_decision_v0_1.md) / [パイロット統合解釈](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)
