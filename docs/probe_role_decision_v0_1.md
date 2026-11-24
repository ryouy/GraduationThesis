# ④ Probeの位置づけ・検証打ち切り判断（2026-11-24）

> 状態：**位置づけ確定。探索的補助指標として使用。追加の妥当性実験は実施しない。** 既存の生成・Probe・Logit Lensデータは変更しない。

## 判断

本実験の主指標は**Explicit Mention Rate**、副指標は**Semantic Mention Rate**（①の判定規則の監査は未了）。Probeは**探索的な内部表現指標**として、Logit Lensも探索的補助指標として使う。

Probeの説明文X/Y分類のROC-AUCはX/Yの判別能力の指標であり、抑制指示下の「思考量」「概念の絶対活性量」「抑制成功率」の検証ではない。入力の末尾位置（assistant生成開始直前）のHidden Stateに対し、同一X/Yペア・同一層の符号付き判別値の**条件差**を測る。層間・概念ペア間で生スコアを直接合算しない。

## 根拠

- [独立した新説明文での確認](../experiments/2026-11/1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md)：学習に使わなかった文章184文、対象16概念の確認で、ROC-AUC等を評価。FDR補正の感度条件を通った比較ペアは一部に限られる。全概念で無条件にProbeが信頼できるとは言えない。
- [既存の抑制パイロット解釈](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)：同じX/Y Probeで抑制指示への応答差を観測。ただし訓練分布と異なる「指示＋Cue」に適用している。
- [Neutral X追加パイロットの第22・23・24層対応集計](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/paired_cue_probe_effects.csv)：関連12 Cue/概念のAvoid X − Neutral Xの平均符号は、bicycleが3層とも負、boatは3層とも正、busとmotorcycleは3層とも負。第24層ではbicycle−0.188、boat+0.211、bus−0.472、motorcycle−0.596。**層間の符号が概ね整合しても「思考量」の妥当性証明にはならない。**
- [Neutral X追加パイロットのLogit Lens対応集計](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261124_qwen_neutral_x_addon_v1/paired_cue_lens_effects.csv)：第24層のX/Y対数尤度マージンの平均条件差は4概念とも負。ただしこれは候補文字列のteacher-forcingによる結果であり、Probeと同じ構成概念を測るとは限らない。

## 本実験の事前規則

1. **出力分析はProbe採択に依存させない。** 本実験の全採用概念に対して出力の言及率を算出する。
2. 概念ペアごとに、出力の本実験結果を見る前に実施・記録された**独立した未学習文章によるX/Y識別評価**を使用し、Probeの採用可否を決める。既存のFDR感度評価結果等を参考に、具体的な採用閾値とペア数は⑤で事前固定。通過しないペアはProbeの本解析から除外し、出力分析には残す。
3. Probeは訓練時と同じ処理、同一の最終入力位置、固定したX/YとProbe係数を用いる。主に第24層、補助で第22・23層。条件に応じた再学習は禁止。
4. 同一X/Yペア・Cue・層における**Avoid X − Neutral X**を中心に記述し、その他の対照を補助的に扱う。概念間のdecision値の生平均はしない。
5. 言及率・Probe・Logit Lensの方向が異なっても結果をそのまま報告する。内部指標からモデルの心理的状態を断定しない。

## 終了条件

- [x] 未学習説明文での性能評価の範囲と限界を確認
- [x] 第22/23/24層の条件差を既存データで点検
- [x] Probeの位置づけを探索的補助指標として固定
- [x] 無制限なProbe改善・追加検証はしないと決定
- [ ] 本実験の概念数・ペア採択基準・具体的な解析仕様は⑤で確定

**④はここで区切り、⑤の本実験の分析・規模決定に移る。**

---

## 研究方針変更（2026-11-24、後続判断）

**この節が本研究の指標の優先順位について上記の旧判断に優先する。旧記録は意思決定の経緯として保存する。**

卒論の主眼は、最終出力の言及率ではなく、抑制指示とCue距離による**LLMの内部表現・語彙投影の変化**とする。

- **主解析① Concept Probe**：固定X/Y識別器の第24層decision scoreについて、同一X/Y・Cueの条件差（主にAvoid X−Neutral X）を分析する。層22・23は補助的な層別比較。X/Yの**相対判別情報**であり思考量・絶対概念活性量ではない。
- **主解析② Logit Lens**：各層の固定X/Y候補文字列のteacher-forced sequence log probability marginを、同一概念・Cue・層で条件比較する。層方向を生成時間と同一視しない。候補文字列の長さやトークン化を統制・記録する。
- **補助：Explicit Mention Rate**：生成回答に現れたX名・事前固定語形を測定し、内部指標との対応を確認する。
- **参考：Semantic Mention Rate**：strict X identificationの定義・API誤判定と人手監査の未完了を明記し、主結論の根拠とはしない。
- 出力にXが現れない場合でも、内部指標の条件差が残るかを調べる。ただし「無意識にXを考えている」とは主張しない。
- 独立評価を通らないProbeペアは主解析対象から外す。概念・ペアの採択基準と推定方法は⑤で凍結。Probeが適用できない場合もLogit Lensと出力の分析は分離して報告する。
- **④は追加検証を行わず終了**。検証打ち切りは「思考量の妥当性が証明された」ことを意味しない。

研究質問：RQ1＝抑制指示による生成前Hidden StateのX/Y判別スコア変化、RQ2＝距離・層によるProbe/Logit Lens差、RQ3＝内部指標相互および最終出力との対応。

この方針は旧パイロットを見た後の設計変更なので、**本実験の開始前に⑤として解析仕様を文書化・固定する**。
