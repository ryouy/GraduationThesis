# 50概念X・比較Y候補の一次選定 v0.1

> 2026-11-24。**一次候補リスト作成済み、Probeの新規学習・独立評価は未実施。50ペアは本実験用に凍結していない。** 条件別Hidden State、Avoid/Neutralの効果、生成結果を用いた選抜は行っていない。

[候補50件CSV](concept_pair_candidates_50_v0_1.csv) · [現在の本実験プロトコルv0.9](main_experiment_protocol_v0_9.md)

## 1. 選定方針

- **10カテゴリー×5対象X＝50 X**を一次候補とする。明確な対象を指し、カテゴリーに偏りすぎず、英語で多様な関連Cueを作れそうな具体名詞を優先。
- **各Xに比較対象Yを1つ**指定。基本的に同カテゴリーで明確に区別できるものを選ぶが、既存の独立検証で確認済みの乗り物4組は既存Yを維持し、結果の継続性を優先。Yは50対象Xの集合外でもよい。
- XとYがあまりに同義なら問題になり、逆に遠すぎるとProbeは課題と関係ない分類になり得る。**近さ・語の曖昧さ・トークン化・名前非露出時の文章の識別性を次工程で確認**する。
- **X↔Yの反転だけの重複比較は避ける**。同一Yを複数Xで使うことは、異なるX/Yペアとして記録する（ただしカテゴリー別の依存やYによるバイアスは検討する）。
- 事前のProbe検証でペアを採択する。最終的に50ペアに達しない場合、AUC閾値を結果に合わせて緩和したり、都合のよいXのみを後から強調したりしない。

## 2. 一次候補（X → Y）

| カテゴリー | 5候補 |
|---|---|
| 乗り物 | bicycle → submarine / boat → bus / bus → helicopter / motorcycle → helicopter / submarine → motorcycle |
| 陸上哺乳類 | elephant → lion / lion → tiger / wolf → bear / giraffe → zebra / rabbit → hare |
| 海洋動物 | dolphin → jellyfish / jellyfish → octopus / octopus → squid / shark → dolphin / starfish → sea urchin |
| 昆虫 | ant → dragonfly / butterfly → dragonfly / dragonfly → moth / moth → butterfly / beetle → butterfly |
| 楽器 | piano → organ / violin → cello / trumpet → trombone / flute → clarinet / drum → tambourine |
| 果物 | apple → pear / banana → pineapple / strawberry → raspberry / lemon → lime / pineapple → coconut |
| 家具 | chair → stool / sofa → armchair / bed → sofa / desk → table / bookshelf → cabinet |
| 道具 | hammer → mallet / screwdriver → wrench / scissors → pliers / wrench → pliers / power drill → electric saw |
| 植物 | rose → tulip / cactus → aloe / sunflower → daisy / bamboo → reed / oak → maple |
| 自然現象 | rain → snow / snow → hail / fog → smoke / lightning → thunder / earthquake → volcanic eruption |

これは採択前の**語彙・意味の候補**。対称性や共通カテゴリーを揃えただけで、QwenのProbeで実際に識別できるという意味ではない。次工程で無理に採用させず変更履歴を保存する。

## 3. 既存Probe実験から直接引き継げる情報

参照した既存結果：
- [100概念v2の候補と傾向](../experiments/2026-11/1111_qwen_probe_100concepts_v2/results/20261112_qwen100_richer_dedup_v2/target_candidates.csv)
- [独立した新説明文による47方向比較のペア別結果](../experiments/2026-11/1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/frozen_pair_confirmation.csv)
- [独立確認の概要](../experiments/2026-11/1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md)

**候補50ペアに対する過去の検証状態**（CSVの`prior_evidence`列）：

- `FDR_CONFIRMED_PRIOR`：**6組**。bicycle/submarine、boat/bus、bus/helicopter、motorcycle/helicopter、elephant/lion、ant/dragonfly。**これは以前の小規模な新規説明文実験でのFDR感度条件通過を示すのみ**で、今回の名称非露出・新たな刺激に対する本実験品質保証ではない。
- `PRIOR_UNADJUSTED_ONLY`：**1組**（submarine/motorcycle）。
- `PRIOR_TESTED_NOT_CONFIRMED`：**5組**（wolf/bear、dolphin/jellyfish、jellyfish/octopus、butterfly/dragonfly、dragonfly/moth）。
- `NOT_TESTED_WITH_THIS_Y`：**38組**。過去にX単独が試された場合も、**この特定のX/Yの独立確認結果はない**。

過去のデータでは多くの楽器・果物ペアで安定条件を満たさなかった。**新規候補が多いのは研究上の最大の不確実性**であり、Probe採択数を安易に50と想定しない。

## 4. 特に点検が必要な候補

- **rabbit/hare, lemon/lime, violin/cello, chair/stool, fog/smoke**：近い概念の識別が必要。文に名称を出さずに特徴差を表現できるか。
- **apple/pear**：appleは会社名との多義性があるため、説明文とCueにおける果物の意味を固定する。
- **dolphin/jellyfish, jellyfish/octopus, butterfly/dragonfly**：既存の新文章確認では採択基準を通らず、さらに言い換えを増やすだけで信頼性が上がるとは限らない。
- **piano/organなど楽器群**：旧スクリーニングで概念ごとの安定性が不十分。Probe検証時に重点確認。
- **自然現象**：対象が「モノ」ではなく事象なので、既存の回答課題・Cue文章タイプが同じように成立するか点検。
- **power drill/electric saw, earthquake/volcanic eruption**：複数トークン候補と語彙長によるLogit Lensの偏りを記録する。

**実装準備（2026-11-24）：** [50組Probeの独立説明文評価Colab](../experiments/2026-11/1124_probe_50pairs/README.md) を作成。**GPU実行・OpenAI API生成・Probe採択結果はまだ未実施**。本実験で使う50ペアをここで正式確定したことにはならない。

## 5. 次工程（新しい条件効果を見ずに実施）

1. **名称を含まないX/Y学習用説明文と独立評価用説明文を生成**。OpenAI APIを利用する場合、別プロンプト・重複除去・事実品質の一次監査を実施。
2. 本実験用の固定Qwenモデルに対し、Probeをペアごとに学習し、新規説明文によるROC-AUC、シャッフルラベル感度、FDR調整を確認。**選抜基準は実行前にv1.0の追補規則として固定**。
3. 不適切なX/Y・多義性・Probe不採択は、候補→変更理由→再評価の履歴を残す。条件効果を見た後での比較相手Y選び直しは禁止。
4. X/Yペアが決まったら、**関連5距離帯×4 Cue＋無関係4 Cue**を生成・距離測定・監査し、本実験用刺激を凍結する。

**このファイルの`CANDIDATE_NOT_FROZEN`は全50行で維持。次工程の独立確認が完了するまで「正式採択」「信頼できるProbe 50組」とは記載しない。**
