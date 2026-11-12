# 実験記録・資料一覧

[← リポジトリのトップへ戻る](../README.md) · [現在の進捗](current_status.md)

各実験の詳細・コード・データは、それぞれのフォルダに保存する。このページでは、主な記録へアクセスしやすいように分類している。

## 1. 11月12日：Qwen Probe検証とCue設計（直近）

| 実験 | 位置づけ・結果 |
|---|---|
| [1110_qwen_probe_20pairs](../1110_qwen_probe_20pairs/qwen_concept_probe_robustness_20pairs.ipynb) | Qwenによる20概念ペアの識別可能性・学習分割とラベル置換の検証（[結果](../1110_qwen_probe_20pairs/results/20261110_qwen20pairs_v1/)） |
| [1111_qwen_probe_pair_expansion](../1111_qwen_probe_pair_expansion/qwen_probe_pair_expansion_cpu.ipynb) | 既存特徴を利用したY候補の探索（[結果](../1111_qwen_probe_pair_expansion/results/20261111_comparator_screen_v1/)） |
| [1111_qwen_probe_100concepts](../1111_qwen_probe_100concepts/qwen_probe_100concepts_semantic_distance.ipynb) | 少数説明文を用いた100概念試験。評価データ数の不足が判明（[結果](../1111_qwen_probe_100concepts/results/20261111_qwen100_v1/)） |
| **[1111_qwen_probe_100concepts_v2](../1111_qwen_probe_100concepts_v2/README.md)** | **説明文を各8+8に増量。69概念を評価し、探索的に12ターゲットが複数距離帯で条件を満たした。** [レポート](../1111_qwen_probe_100concepts_v2/results/20261112_qwen100_richer_dedup_v2/analysis_summary.md) |
| **[1112_qwen_probe_independent_confirmation](../1112_qwen_probe_independent_confirmation/README.md)** | **新たな184文（23概念）で確認。16ターゲット中、FDR感度分析後に4ターゲットが複数距離帯で再現。** [レポート](../1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md) |
| **[1112_cue_semantic_distance](../1112_cue_semantic_distance/README.md)** | **240候補の実測、64文の暫定選択、17文交換を含むAI内容監査。** [距離結果](../1112_cue_semantic_distance/results/20261112_cue_distance_pilot_v1/analysis_summary.md)・[監査と固定刺激64文](../1112_cue_semantic_distance/final_stimuli/20261112_frozen_ai_audit_v1/README.md) |
| **[1112_qwen_suppression_pilot](../1112_qwen_suppression_pilot/README.md)** | **抑制指示×実測Cueのパイロット：272入力、5反復、固定Probe、全24層Logit Lens、別工程の意味的言及API判定。** [Colabで開く](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1112_qwen_suppression_pilot/qwen_suppression_pilot_4concepts.ipynb)。**コード作成済み・GPU未実行。** |
| [本実験プロトコル](main_experiment_protocol.md) | 環境、指示条件、Cue・Probe・Logit Lens、出力採点、統計解析と再現性。**Qwen抑制パイロットは未実行** |

**状態の区別：** Probe探索は本実験の抑制効果の検証ではない。CueはAI監査によるパイロット用固定版で、人間の独立評定は未実施。

## 2. 11月4日〜11日：モデル・課題・Probeの初期検証


| 実験 | 内容 |
|---|---|
| [1104_model_comparison](../1104_model_comparison/README.md) | 4モデル比較 |
| [1104_phi_validation](../1104_phi_validation/results/20261104T012418280152Z/README.md) | Phiの固定評価72問 |
| [1104_phi_prompt_diagnostic](../1104_phi_prompt_diagnostic/results/phi-prompt-20261104T015128731641Z/REVIEW.md) | 質問形式の対比較と原回答点検 |
| [1104_scoring_revision](../1104_scoring_revision/README.md) | 既存384回答の採点処理修正 |
| [1104_inference_audit](../1104_inference_audit/README.md) | 推論コード照合 |
| [1104_instruction_probe](../1104_instruction_probe/results/instruction-probe-20261104T024551489146Z/REVIEW.md) | 指示×手がかりProbe診断 |
| [1104_instruction_probe_20pairs](../1104_instruction_probe_20pairs/README.md) | 11月4日の20組のProbe診断（元データ・コード） |
| **[1110_probe_reanalysis](../1110_probe_reanalysis/README.md)** | **11月11日のProbe再解析：完全ラベル置換25,200 fit／新説明文による汎化検証。[結果と考察](../1110_probe_reanalysis/FINDINGS_20261111.md)・[結果データ](../1110_probe_reanalysis/results/20261111_173427/)・[Colab](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1110_probe_reanalysis/probe_reanalysis_and_independent_generalization.ipynb)** |

## 3. 11月3日の追加検証

| 実験 | 内容 |
|---|---|
| [1103_fresh_check](../1103_fresh_check/README.md) | 未使用問題による確認 |
| [1103_model_check](../1103_model_check/README.md) | モデル・質問・Probeの追加確認 |
| [1103_review](../1103_review/README.md) | 内部表現実験のコード監査・追加検証 |
| [1103_revision](../1103_revision/README.md) | 質問・学習例拡張・X/Y距離の追加診断 |
| [1103_validity](../1103_validity/README.md) | 測定妥当性パイロット |

## 4. 初期の実験・研究資料

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

## 5. アーカイブ

- [README_previous_20261103.md](../README_previous_20261103.md)：README再構成前の記録。旧状況の参照用。
- 各実験フォルダ内のPLAN.md、README.md、結果ファイル：実行時点の計画と記録。現在の研究方針と異なる場合は、[研究概要](research_overview.md)と[現在の進捗](current_status.md)を優先する。

---

**記録の原則：** 過去の実験結果や計画は、後から都合よく書き換えず、その時点の記録として保持する。最新の研究方針・進捗は、このdocs配下の文書とトップREADMEで管理する。
