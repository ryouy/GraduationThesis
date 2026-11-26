# 本実験：回答生成時の実験条件（2026-11-26）

[統合プロトコルv0.95](main_experiment_protocol_v0_95.md)第2・5・6節の更新メモ。2026-11-26の合意に基づく採用方針。実装・本実験は未実施、v1.0は未凍結。

## 指示条件

既存パイロットとの連続性を重視し、現行プロトコルの英語指示を維持する。

| 条件 | 指示 |
|---|---|
| Avoid X（主対象） | `Do not think about {X}. Read the clue and briefly name the thing it brings to mind.` |
| Neutral X（比較対照） | `The word is {X}. Read the clue and briefly name the thing it brings to mind.` |

共通Cue入力：`Clue: {cue}\nAnswer with one short phrase.`

Cueなし：`No clue is provided.\nAnswer with one short phrase.`

既存Qwen chat templateを維持し、改行・メッセージ構成を既存コードと照合して凍結する。両条件はXの名称を提示するが、指示文の長さ・意味・トークン化の違いは残る。条件差を純粋な抑制の因果効果と断定しない。

## 回答生成設定

| 項目 | 採用値 |
|---|---|
| モデル | Qwen2.5-0.5B-Instruct（既存プロトコルの固定revision） |
| do_sample | True |
| temperature | 0.7 |
| top_p | 0.9 |
| max_new_tokens | 128 |
| 反復回数 | 各ユニーク入力につき5回 |
| seed | 101, 211, 307, 401, 503 |

設定は両指示条件・全概念・全Cueで共通とする。反復ごとにseedを対応付け、入力ID・反復ID・seed・実際の生成設定・モデル/Tokenizer revision・ライブラリ版を記録する。設定値は最適性を実証したものではなく、予備実験との連続性を優先した採用値。追加のtemperature等の比較実験は予定しない。

## 規模と測定単位

100概念×（関連20 Cue＋無関係4 Cue＋Cueなし1）×2条件＝5,000ユニーク入力。各5回生成するため25,000回答を予定する。最終採択数Nなら50N入力、250N回答。

生成直前のHidden Stateは原則として同一入力につき1回測定し、Probe・Logit Lensに使用する。生成反復は最終出力のばらつきを測るためのものであり、内部表現の独立サンプル数を5倍にしない。出力分析でも同一入力内の反復を考慮する。

## 残る確認事項

GPU計算時間・AI評価費用・生成設定の実装整合性・再現性は実行前に確認する。最終出力の評価規則は別途確定する。過去のノートブックと結果は変更せず、実装時は新しいversionとrun_idを使用する。
