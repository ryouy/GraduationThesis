# 実験記録・資料一覧

[← リポジトリのトップへ戻る](../README.md) · [現在の進捗](current_status.md)

各実験の詳細・コード・データは、それぞれのフォルダに保存する。このページでは、主な記録へアクセスしやすいように分類している。

## 1. 直近のモデル・課題・Probe検証

| 実験 | 内容 |
|---|---|
| [1104_model_comparison](../1104_model_comparison/README.md) | 4モデル比較 |
| [1104_phi_validation](../1104_phi_validation/results/20261104T012418280152Z/README.md) | Phiの固定評価72問 |
| [1104_phi_prompt_diagnostic](../1104_phi_prompt_diagnostic/results/phi-prompt-20261104T015128731641Z/REVIEW.md) | 質問形式の対比較と原回答点検 |
| [1104_scoring_revision](../1104_scoring_revision/README.md) | 既存384回答の採点処理修正 |
| [1104_inference_audit](../1104_inference_audit/README.md) | 推論コード照合 |
| [1104_instruction_probe](../1104_instruction_probe/results/instruction-probe-20261104T024551489146Z/REVIEW.md) | 指示×手がかりProbe診断 |
| [1104_instruction_probe_20pairs](../1104_instruction_probe_20pairs/README.md) | 20組のProbe診断。実モデル結果の状態はREADMEを参照 |

## 2. 11月3日の追加検証

| 実験 | 内容 |
|---|---|
| [1103_fresh_check](../1103_fresh_check/README.md) | 未使用問題による確認 |
| [1103_model_check](../1103_model_check/README.md) | モデル・質問・Probeの追加確認 |
| [1103_review](../1103_review/README.md) | 内部表現実験のコード監査・追加検証 |
| [1103_revision](../1103_revision/README.md) | 質問・学習例拡張・X/Y距離の追加診断 |
| [1103_validity](../1103_validity/README.md) | 測定妥当性パイロット |

## 3. 初期の実験・研究資料

| 資料 | 内容 |
|---|---|
| [1015](../1015/) | 初期の予備実験 |
| [1016](../1016/) | 10月16日の実験記録 |
| [1017](../1017/) | 10月17日の実験記録 |
| [1019](../1019/README.md) | 意味的距離・層別実験の記録 |
| [Interim_Posters](../Interim_Posters/) | 中間ポスター |
| [lab_meeting_slides](../lab_meeting_slides/) | 研究室ミーティング資料 |
| [concept_persistence_and_reactivation.md](../concept_persistence_and_reactivation.md) | 概念の持続・再活性化に関する整理 |
| [semantic_distance_and_reactivation.md](../semantic_distance_and_reactivation.md) | 意味的距離と再活性化に関する整理 |

## 4. アーカイブ

- [README_previous_20261103.md](../README_previous_20261103.md)：README再構成前の記録。旧状況の参照用。
- 各実験フォルダ内のPLAN.md、README.md、結果ファイル：実行時点の計画と記録。現在の研究方針と異なる場合は、[研究概要](research_overview.md)と[現在の進捗](current_status.md)を優先する。

---

**記録の原則：** 過去の実験結果や計画は、後から都合よく書き換えず、その時点の記録として保持する。最新の研究方針・進捗は、このdocs配下の文書とトップREADMEで管理する。
