# Qwen2.5-0.5B：抑制指示 × 意味的距離のパイロット実験

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1112_qwen_suppression_pilot/qwen_suppression_pilot_4concepts.ipynb)

[Colabノートブック](qwen_suppression_pilot_4concepts.ipynb) · [本実験のプロトコル](../docs/main_experiment_protocol.md) · [固定した64 Cue](../1112_cue_semantic_distance/final_stimuli/20261112_frozen_ai_audit_v1/README.md) · [事前の独立Probe検証](../1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md)

> **状態：パイロット本実行・意味的言及API判定とも完了（2026-11-13確認）。** コア結果：272入力、1,360生成、固定Probe、全24層Logit Lens。API意味判定1,360件（保留17件）。**[結果の統合解釈](results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)**。人間による評価は未実施。

## 1. 目的

「Xについて考えないで」という指示の影響が、手がかり（Cue）とXの意味的距離によって、**生成出力・線形ProbeのX/Y判別スコア・Logit Lens**の間でどのように異なるかを調べる。

このパイロットは**研究手順・分析指標・指示追従性の診断**が目的であり、距離の因果効果や一般的なLLM心理現象の証明を目的としない。4つのX概念が全て乗り物である点も制約である。

## 2. 事前に固定した設定

| 項目 | 設定 | 理由 |
|---|---|---|
| LLM | `Qwen/Qwen2.5-0.5B-Instruct` | 同モデルの特徴量・学習用Probeデータが残っており、再現可能 |
| モデルrevision | `7ae557604adf67be50417f59c2c2f167def9a775` | 計測対象の内部表現を固定 |
| 実行環境 | Google Colab、GPU（T4可） | Hidden State抽出と生成をローカルAPIに依存せず実行 |
| 概念X | `boat`, `bus`, `bicycle`, `motorcycle` | 未学習の説明文によるProbe汎化検証で有望 |
| 比較Y | `boat→bus`, `bus→helicopter`, `bicycle→submarine`, `motorcycle→helicopter` | 既存の確認済みX/Yペアから選び、今回の生成結果を見て変更しない |
| Cue | 各Xにつき近4、中4、遠4、無関係4 | 選定済み240候補から実測距離とAI内容監査で固定した64文 |
| 指示条件 | `Base`, `Think X`, `Avoid X`, `Think Y` | 指示の有無、集中、抑制、代替への誘導を比較 |
| 生成 | 温度0.7、top-p 0.9、128新規トークン上限、5 seeds | 言及率のばらつきを記録しつつ再現可能にする |
| 生成前Hidden State | 最後の入力トークン（assistant先頭） | 応答の違いが入る前の同一位置で条件差を比較 |
| Probe | 既存の8学習例×X/Yで `StandardScaler + LogisticRegression(C=0.1)`、22・23・24層 | 過去の学習特徴のみで再構成。今回のCue・生成結果では再学習しない |
| Logit Lens | 全24層、Qwenの最終RMSNormとlm_headで投影 | Probeと独立の観点から層方向の語彙予測を追跡 |
| 出力の言及 | 事前固定辞書による明示的言及、任意のOpenAI APIによる意味的言及 | 語の出現と概念の同定を混同しない |

### 入力規模

- **関連Cue：** 4 X × 12 Cue × 4条件 = **192入力**
- **無関係Cue：** 4 X × 4 Cue × 4条件 = **64入力**
- **Cueなし：** 4 X × 4条件 = **16入力**
- **計272入力、各5回生成で1,360出力**。生成前のHidden Stateは272入力について各1回だけ測定。

Cueなしの`Base`は4つのXで同じプロンプトになるため、4つの独立した入力内容とはみなさない。反復生成数と異なるCueの数も区別する。

## 3. 計測指標と解釈

1. **Explicit Mention Rate**：生成文にXの名称・事前定義した別名が明示的に現れた割合。否定での言及も数える。生成結果を残し、判定辞書を固定。
2. **Semantic Mention Rate（任意）**：APIの判定器にX名と生成回答だけを渡し、Xそのものを答えているか`yes/no/uncertain`で判定。元の指示・Cueは渡さない。APIキーがない場合は未実施とし、明示的言及で代用しない。
3. **Probe decision score**：以前の学習用Hidden Stateだけから再構成した固定ProbeのX側判別値。**同じX/Y・層・Cueの `Avoid X − Think X` / `Avoid X − Base`** を比較する。旧ROC-AUCは測定器の評価であり、Xの絶対的な活性量ではない。
4. **Logit Lens**：各層のX/Yラベル文字列のteacher-forced log probability。複数トークン語は**全トークン**を評価。Qwen最終層のhidden stateは正規化済みで、二重Normをしない。各入力で最終層のlogitsが通常forward出力と一致することを自動テスト。
5. **品質補助指標**：応答長、空回答、128トークン上限到達、辞書とAPI判定の相違。**同じCueの5反復は5つの独立Cueではない**。

全体の分析では、近・中・遠の帯を比較するほか、**実測コサイン距離の連続値**を保存する。`unrelated`と`none`は距離解析から外し、別の対照として表示する。異なるX/Y Probeの**判別生スコアを無条件に平均しない**。

## 4. 実行手順

1. [Colabを開く](https://colab.research.google.com/github/ryouy/GraduationThesis/blob/main/1112_qwen_suppression_pilot/qwen_suppression_pilot_4concepts.ipynb)。ランタイムを**GPU**に設定。
2. Colab左側のSecretsに`GITHUB_RESULTS_TOKEN`を登録し、このノートブックに使用を許可。GitHubの対象リポジトリの**Contents read/write**だけを与える。
3. 上から全セルを実行。以前の学習用特徴ベクトルはGitHubから読み込む。**本パイロットのためにProbeを再選定したり、Cueを変更したりしない**。
4. 入力16件ごと、計**17チェックポイント**をGitHubへ保存。中断したら同じノートブックを上から再実行すると既存の検証済みチャンクを復元する。
5. コア測定の結果は下記`results/...`へ自動保存。`manifest.json`が完了状態となったら、出力、Probe、Logit LensのCSV・図を確認。
6. **意味的言及も計測する場合のみ**Colab Secret`OPENAI_API_KEY`を設定し、最後の判定セルを実行（別途API課金、モデル利用権限が必要）。API判定は**別のチェックポイント・結果フォルダ**に保存。

APIキー・GitHub PATはノートブックやGitHub上のCSVに書き込まない。

### 想定する保存場所

`1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1/`

| ファイル | 内容 |
|---|---|
| `config.json` / `prompts.csv` / `cue_selected.csv` | 事前固定したモデル・生成設定、272入力、64 Cue |
| `probe_fit_validation.csv` | 過去データから再構成した12個の層別Probeの方向と指紋 |
| `checkpoints/chunk_000.zip` など | 中断再開用の生成・Hidden State・Probe・Lensを含む17分割 |
| `generations.csv` | 1,360件の生応答、seed、生成トークン数、明示的言及 |
| `probe_scores.csv` | 272入力×3層のX/Y判別スコア |
| `logit_lens.csv` | 272入力×24層×2候補のトークン列評価 |
| `cue_level_explicit_effects.csv` | Cue単位に集計した条件差 |
| `cue_level_probe_effects.csv` | Probeの対応する条件差 |
| `logit_lens_cue_level_effects.csv` | Logit Lensの条件差 |
| `pilot_overview.png` など | 出力の言及、Probe、Lensのグラフ |
| `analysis_summary.md` / `manifest.json` | 実測の要約、完了状態、限界 |
| `semantic_grading/.../` | **任意・別保存**のAPI意味的言及判定と監査記録 |

## 5. 予備実験に基づく注意点

- [100概念v2](../1111_qwen_probe_100concepts_v2/results/20261112_qwen100_richer_dedup_v2/analysis_summary.md)：69/100概念の評価が可能で、探索的に12Xが複数Y・距離帯で安定した。
- [新規184文によるProbe再評価](../1112_qwen_probe_independent_confirmation/results/20261112_newfacts_16targets_v1/analysis_summary.md)：16Xから4XがFDR感度分析後にも複数Y・帯で再現。本パイロットの4Xをここから選定。
- [Cueの距離測定](../1112_cue_semantic_distance/results/20261112_cue_distance_pilot_v1/analysis_summary.md)：240文の実測後、64文を暫定採択。
- [64文のAI監査・17文差し替え](../1112_cue_semantic_distance/final_stimuli/20261112_frozen_ai_audit_v1/README.md)：パイロット用の刺激を固定。**独立した人間による妥当性評価は未実施**。
- [最新の実験プロトコル](../docs/main_experiment_protocol.md)：出力と内部表現の比較で注意する交絡や評価規則。

**実施済み**：GPU生成・Logit Lens実測・API判定。**未実施**：独立した人間のCue・応答ラベル評定、より広い概念カテゴリでの確認。結果は探索的で、語提示の交絡を分離していないため抑制の逆説的効果は断定しない。

[コア結果](results/20261112_qwen_suppression_pilot_v1/analysis_summary.md) · [API判定](results/20261112_qwen_suppression_pilot_v1/semantic_grading/20261112_semantic_grader_gpt6luna_v1/analysis_semantic.md) · [統合解釈](results/20261112_qwen_suppression_pilot_v1/INTERPRETATION_20261113.md)