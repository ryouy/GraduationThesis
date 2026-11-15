# 04｜Concept Probe：禁止概念は内部で読み出せるか？

[← 目次](README.md) ｜ [前：Zhou型](03_Zhou型_否定理解とLogitLens.md) ｜ [次：研究展望](05_研究展望_意味的距離と再活性化.md)

## 一言でいうと

**最終層のHidden Stateには、XとYのどちらを表すか区別できる情報が含まれていた。** また、関連/無関連の手がかりに対するProbeスコアの変化は、NeutralとSuppressionで異なった。

これは卒論案Bへつながる有望な予備結果。ただし、**「Xが忘却され、後から再活性化した」と証明したわけではない**。

## そもそもConcept Probeとは？

例えばX=`banana`、Y=`apple`に対し、モデルに次の文章を入力する。

| ラベル | 学習例（イメージ） |
|---|---|
| X | `The note concerns banana. Topic:` |
| Y | `The note concerns apple. Topic:` |

文章末尾 `Topic:` のHidden Stateから、**X寄りかY寄りか**を分類する小さな線形モデル（ロジスティック回帰）を学習する。

```mermaid
flowchart LR
  A["文を入力"] --> B["LLMのHidden State
Layer 8 / 16 / 24"]
  B --> C["線形Probe"]
  C --> D["X寄りかY寄りか
(連続スコア)"]
```

ここで測るのは**二概念の相対的な識別スコア**。人間の意識における「想起」、概念の絶対活性量、あるいはモデルパラメータからの知識削除ではない。

### 学習と検証を分離

| 段階 | 入力例 | 件数（1概念ペア当たり） |
|---|---|---:|
| Train | `Think of banana. Topic:` / `Think of apple. Topic:` など、概念名を直接含む8種の文型 | 16 |
| Held-out named | 学習していない別の3文型（概念名あり）×2 | 6 |
| **Held-out description** | `A writer described a curved yellow fruit. Topic:` など、概念名なしの3文型×2 | **6** |

**重要**：概念名を含まない説明文に一般化するかを別に測り、AUC **0.75以上**を探索的な判定基準とした。説明文自体の内容が学習語や後の関連刺激と意味的に近いため、**独立した多数の刺激に対する頑健性は未検証**。

## 結果①：Probeは概念名なしでも区別できたか？

![Concept Probeの検証AUC](figures/03_probe_auc.svg)

| 層 | 説明文での平均ROC-AUC | AUC≥0.75の概念数 |
|---|---:|---:|
| Layer 8 | 0.431 | 1/8 |
| Layer 16 | 0.681 | 3/8 |
| **Layer 24（最終）** | **0.972** | **8/8** |

ROC-AUCは、Xの例をYの例より高いスコアに並べる能力を表す指標。**1.0に近いほど順序づけが良く、0.5前後は偶然に近い**。

### 最終層の概念別AUC

| X（Y） | Layer 24 AUC | 同じ6例での固定閾値によるAccuracy |
|---|---:|---:|
| banana（apple） | 1.000 | 100.0% |
| elephant（giraffe） | 1.000 | 100.0% |
| tiger（lion） | **0.778** | **50.0%** |
| piano（violin） | 1.000 | 100.0% |
| coffee（tea） | 1.000 | 100.0% |
| ocean（river） | 1.000 | 83.3% |
| castle（palace） | 1.000 | 100.0% |
| bicycle（scooter） | 1.000 | 83.3% |

**注意**：tigerではAUCが0.778でもAccuracyは50.0%。AUCは順位づけ、Accuracyは分類閾値（この場合スコア0）での判定であり、同じ性能指標ではない。評価例が各概念6件しかないことも忘れない。

## 結果②：関連刺激に対する内部スコア変化

次に、次のような入力を比べる。

- **Neutral + 関連**：`The topic word is banana.` → 黄色い果物を示唆する文 → `Topic:`
- **Suppression + 関連**：`Do not think of banana. Do not write the word banana.` → 同じ関連文 → `Topic:`
- 上の2条件それぞれで、関連文を電車の話題（無関連文）に置き換えた条件も測定。

### 差の差（Difference-in-Differences、DID）

```text
D = [Suppression(関連) − Suppression(無関連)]
  − [Neutral(関連)     − Neutral(無関連)]
```

**Dが正**とは、NeutralよりSuppressionのほうが、「関連刺激と無関連刺激の間のX寄りスコア差」が大きいこと。**Suppressionの絶対スコアがNeutralより高いという意味ではない**。

![Concept Probe DID](figures/04_probe_did.svg)

| 概念X | Layer 24 DID |
|---|---:|
| banana | +0.388 |
| elephant | **+1.077** |
| tiger | +0.469 |
| piano | +0.860 |
| coffee | +0.255 |
| ocean | +0.749 |
| castle | +0.169 |
| bicycle | +0.182 |
| **平均** | **+0.519** |

- **Layer 24では8/8概念が正**。すべての概念が説明文AUC≥0.75の基準を通過している。
- Layer 8の平均Dは−0.564、Layer 16は−0.236。ただし両層ではProbeの検証性能が低い概念が多く、その差を同等に解釈しない。
- 参考値として、8概念を再標本化する探索的Bootstrap 5,000回（seed 42）で平均Dの95%区間を計算すると、約 **+0.307〜+0.748**。異なるペアごとに学習されたProbeスコアを平均している点にも注意。

### 誤解しやすい重要ポイント

Layer 24の8概念平均Probeスコアは次のとおり。

| 条件 | 関連刺激 | 無関連刺激 | 関連 − 無関連 |
|---|---:|---:|---:|
| Neutral | +4.575 | +3.962 | +0.613 |
| Suppression | +2.760 | +1.628 | +1.132 |
| **Suppression − Neutral** | **−1.815** | **−2.334** | **D = +0.519** |

つまり、**関連刺激のときでもSuppressionはNeutralよりX寄りスコアが低い**。それでも「関連−無関連の差」を引き算すると、Suppressionの方が大きくなる。

この点を取り違えると、「抑制すると通常より概念が強くなる」という過大な結論になってしまう。

## 結果③：単純な置換は内部表現にも影響するか？

Layer 24の関連刺激条件における平均X-vs-Y Probeスコアは、Neutral **+4.575**、Suppression **+2.760**、Replacement **−1.563**。

これは、同じXとYの識別器で見たとき、Replacement条件が比較的**Y寄り**になる傾向を示す。ただし、置換のプロンプトにはYの語形自体が明示されているので、実装上は当然起こりうる効果でもある。

## 研究としての解釈

**観測したこと**

1. 最終層のHidden Stateでは、概念名を含まない少数の説明文からでもX/Yを高い順位づけ性能で区別できた。
2. 禁止対象Xの語形が指示文に含まれる条件で、関連・無関連刺激に伴うX/Yスコア変化が条件依存的に異なった。
3. 最終層の関連刺激DIDは、今回の8概念では一貫して正だった。

**まだ言えないこと**

- Xが一度消えたり減衰した後、*同一の推論過程*で再び活性化したという時系列は見ていない。
- プロンプト中に書いたXを取り除いても情報が残るか、という厳密な残存の検証ではない。
- X/Y相対スコアの上昇が、独立したX概念の絶対活性を意味するわけではない。
- 関連刺激の意味的距離を実際に数値化・操作していない。
- Probeで読めることと、その情報が生成を因果的に決めることは別。

**生データ**：`concept_probe_validation_v3.csv`、`concept_probe_measurements_v3.csv`、`concept_probe_DID_v3.csv`、`concept_probe_paired_contrasts_v3.csv`（[v3結果ZIP](../1015/results_v3/20261016T054754Z/)）。

**次の一歩**：関連・無関連という二分法を、意味的距離の**複数水準**へ拡張し、語長・語頻度・文型を統制して検証する。
