# 公式最小コードと従来推論の照合

バナナの命名失敗をモデルの能力だけで説明できるか、実行方法の差を確認する。[公式Quickstart](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct#quickstart)を参照し、同じrevision・42問題・採点を固定して入力・計算精度・attention実装を比較する。

[実行前計画](PLAN.md) / [Colab](official_inference_audit.ipynb) / [比較コード](run.py)

比較のgreedy生成は全モード共通の32token上限。公式例のデフォルト生成は別枠の補助確認とする。公式のauto dtypeが実際に何を選んだか、各モードのbackend、入力token列・出力token列、旧回答との一致を保存する。CPU比較は先頭のバナナ1問のみ。

この実験は既に評価した問題での実装診断であり、新規集合での性能評価ではない。実行環境内での差の再現を確認し、ライブラリやGPU一般への結論は出さない。

保存結果の検証：`python 1104_inference_audit/verify.py 1104_inference_audit/results`。

## 結果：公式手順でも課題の失敗が再現

Colab T4、PyTorch 2.11.0+cu130、transformers 4.57.6、固定revisionで全6設定・各42問（252回答）を完了。エラー0件。CPU補助1回答、公式のデフォルトsamplingによる補助3回答も保存した。

| 設定 | 説明36件の正答 | バナナ6件の正答 | none対照6件 | 旧回答との完全一致 / 42 |
|---|---:|---:|---:|---:|
| 従来FP32・eager | 25/36 | 0/6 | 5/6 | 42/42 |
| tokenizer([text])のみ公式形式 | 25/36 | 0/6 | 5/6 | 42/42 |
| 公式system・入力処理、FP32・eager | 25/36 | 0/6 | 5/6 | 42/42 |
| 公式system・入力処理、FP32・SDPA | 25/36 | 0/6 | 5/6 | 42/42 |
| 公式auto dtype（実際はBF16）・SDPA | 25/36 | 1/6 | 5/6 | 40/42 |
| 公式入力、FP16・SDPA | 25/36 | 0/6 | 5/6 | 41/42 |

FP16/BF16では一部の回答が変わるが、合計正答は25/36で同じだった。BF16のバナナ1件の成功を、採用基準を満たす改善とはみなさない。

### 入力と内部状態抽出

- 公式例のsystemメッセージを明示してもしなくても、renderされたテキスト、input_ids、attention_maskは42/42件すべて同一だった。使用Tokenizerのchat templateが同じsystem文を補っていたため、system文の欠落が今回の原因という証拠はない。
- 最初のバナナ問題は、内部状態を抽出する前後とも出力token列が同一。内部抽出による生成の汚染はこの1件では見られない。全問題での因果検証ではない。
- 全設定で入力・出力token列を保存した。旧回答、採点、token列の長さ、集計を個別行から再計算して検証した。

### CPU補助確認

最初のバナナ問題はCPUでも **Mango**。GPU/CPUの先頭tokenの最大logitはいずれもtoken ID 44（M）。全語彙にわたる先頭token logitsの最大絶対差は約 **7.44×10^-5**。同じFP32/eagerのCPU計算でも誤答が再現したため、この1問の失敗をGPUだけの数値異常で説明する根拠は見つからなかった。

CPUは1問のみであり、すべてのGPU結果の一致や、あらゆる環境不具合がないことを証明するものではない。

### 公式デフォルト生成の補助確認

公式例のauto dtype・system・デフォルトgeneration_config（seed42、上限512token）でも、最初の文脈バナナ問題はMangosteen、直接のバナナ質問はPeachだった。公式のLLM紹介例には長文で回答した。samplingは各1回の補助診断で、正答率の推定ではない。

モデル配布時のgeneration_configにはdo_sample=true、temperature=.7、top_k=20、top_p=.8、repetition_penalty=1.1があった。本比較の主6設定はdo_sample=false/max_new_tokens=32を上書きする一方、repetition_penalty=1.1等は継承する。したがって無加工logitsだけによる純粋なargmaxではなく、同じ配布設定を用いた決定的生成の比較である。このペナルティ単独の効果は今回未検証。

## 判断

**入力形式・attention実装・精度・CPU/GPUの今回の確認では、従来処理に特有の失敗は見つからなかった。公式手順でもこの命名課題の不安定さが再現した。** ただし、同じtransformers/PyTorch環境を使っており、全ライブラリ版や別実装での一致までは検証していない。

今回のモデル・問題・生成設定では基本課題の採用基準を満たさない、という判断を維持する。公開ベンチマークと別の課題なので、そのスコアだけから今回の正答を保証できない。モデルが概念を一切持たない、あるいはQwen一般が低性能、という結論にはしない。

次にモデルを変更するなら、同じ固定問題・採点で大きいモデルを比較し、課題成立で選ぶ。繰り返し使用した42問題は校正集合として扱い、採用後の評価には未使用集合が必要。

## 保存データ

- `results/answers.csv`：252回答、旧回答、一致、事前採点。
- `results/input_comparison.csv` / `tokens.json`：公式/従来の入力テキストとtoken列、attention_mask、出力token列。
- `mode_metadata.json` / `manifest.json`：dtype、backend、generation_config、model revision、環境・hash。
- `*_first_token.json` / `cpu_check.json`：先頭token logitsの上位候補とCPU/GPU差。
- `hidden_extraction_control.json`：内部状態抽出前後の生成一致。
- `official_default_samples.json`：公式デフォルト生成の補助3回答。
- `summary.csv` / `errors.json` / `run.log`：集計・エラー（0件）・実行ログ。
