# 最終出力の評価方針：判定規則と限定監査（案 v0.1）

> 状態：**方針採用・人手監査待ち**（2026-11-24）。本実験の指標をまだ最終凍結していない。既存1,360生成とAPI採点は変更しない。

## 目的・検証の上限

パイロットの判定方法を無制限に改訂せず、あらかじめ決めた範囲で評価して本実験へ進む。

- **主指標候補：Explicit Mention Rate**。回答中にXの名称または事前に固定した別名・語形が明示的にあるか。施設、活動、否定文、複合語の中でも名称が現れればYes。単なる関連語は含めない。辞書・表記揺れの一覧と境界処理を本実験前に固定する。既存辞書の自動ラベルと新たな人手評価を区別する。
- **副指標候補：Semantic Mention Rate（strict identification）**。回答がXそのものを名称・明瞭な言い換え・下位種で同定すればYes。Xに関わる場所・活動・部品だけならNo。曖昧な場合はuncertain（単純にNoにしない）。
- **探索的**：「Xに関連する内容」の広い言及。定義の拡張によって結果が変わりやすいため、今回の主解析には採用しない。
- 判定時は原則 **Xと回答本文** を使い、条件・距離帯・Cueを見せて判断を誘導しない。監査用シートには後から層化・傾向確認できるよう全メタデータを保存する。

## 実データに基づく監査範囲

既存の `graded_responses.csv`（1,360回答）の分類は以下。

| 判定 | 件数 |
|---|---:|
| 辞書Yes、API No | 100 |
| 辞書No、API Yes | 40 |
| 辞書Yes、API uncertain | 6 |
| API uncertain全体 | 17 |
| 辞書とAPIの不一致合計（uncertainを非Yesとして比較） | 146 |
| 不一致・保留の和集合 | **157** |

不一致と保留の双方に属する6件を重複計上しない。これに **一致例から40件** を概念・条件・距離帯の層を巡回して再現可能な決定的並びで抽出した計 **197件** の監査表を作成済み：

[output_label_audit_v1.csv](../experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/output_label_audit_v1.csv)

監査表の `human_explicit_label`、`human_identity_label`、`reviewer_notes` は意図的に空欄、`review_status=PENDING_HUMAN_REVIEW` とした。**AIによる一次整理と、人間による独立評価は異なる**。実施済みと記載しない。

## 最初に注目する事例

- `Bicycle Route`、`Bus Station`、`Motorcycle Licensing School`：名称は含むためExplicit Yes、対象そのものの同定はNo。
- `Island Ferry`、`Oar-powered vessel`：X名なしでも、boatの同定に該当しうる。
- `Transit Vehicle`、`Scheduled Transit Vehicle`：bus以外も指し得る。APIのYesが広すぎる可能性がある。
- `Rider balances on narrow wheels while pedaling.`：自転車を強く示唆するが行為の記述であり、strict identificationの定義を統一して判断する。
- `Quiet Cornering Bike`、`Rally bike`：bikeはbicycle/motorcycleで曖昧。未確定時はuncertain。

## 完了判定（事前に固定）

1. 監査表197件に判定と短い根拠を記録し、APIと辞書の系統的誤りを整理する。
2. 明示的言及の辞書・境界条件と、strict identificationの曖昧例の扱いを1回固定する。
3. 元の結果は不変のまま、採用規則による集計を別ファイルで実行する。条件×距離帯と概念別の主要傾向が変更されたか示す。
4. 主指標の機械的判定に重大な欠陥が残らず、副指標の限界が説明可能なら **①完了** とし②へ進む。恣意的な正答率目標や改善ループを設けない。重大な欠陥があれば理由と範囲を記録し、一度だけ規則を見直す。

## 注意

旧パイロットの結果から、逆説的抑制が確認されたと主張しない。Baseでは指示文にXがない一方、Avoid XにはX名がある。これは次項②で扱う。説明文分類のProbe AUCを「思考量の測定妥当性」とは解釈しない。

---

## 本実験での役割変更（2026-11-24）

**この記録は出力判定の定義・監査に関するものとして維持するが、本文冒頭の「主指標候補」は研究全体の主解析という意味ではなくなった。** 本実験の主解析はProbeとLogit Lensによる内部表現解析。Explicit Mention Rateは**出力側の主要な補助指標**、Semantic Mention Rateは**参考指標**とする。197件の人手監査は未完了であり、AIの一次整理を人間による正解判定としない。詳しくは[④内部表現指標の方針](probe_role_decision_v0_1.md)。
