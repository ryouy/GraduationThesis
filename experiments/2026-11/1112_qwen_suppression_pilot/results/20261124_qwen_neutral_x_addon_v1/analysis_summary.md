# Neutral X追加パイロット：結果

- 状態：COMPLETED_NEUTRAL_X_CORE_PILOT
- 実行：68入力、340生成、204 Probe、3264 Logit Lens
- Cue SHA256: `f9c1c729e285853c84702fe50cdf0f8ab105787dd995e36b525d778a4098a74c`
- Prompts SHA256: `4cc4af71cea4106c0164f2b91419551652e87cdd8d60014670725633a631e014`
- native logits最大誤差: 3.3378601e-05
- 比較先：experiments/2026-11/1112_qwen_suppression_pilot/results/20261112_qwen_suppression_pilot_v1

## Cueごとの平均差（明示的言及）

|                          |   avoid_minus_neutral |   neutral_minus_base |   avoid_minus_thinkx |
|:-------------------------|----------------------:|---------------------:|---------------------:|
| ('bicycle', 'far')       |                 -0.7  |                 0.9  |                -0.5  |
| ('bicycle', 'medium')    |                 -0.35 |                 0.85 |                -0.25 |
| ('bicycle', 'near')      |                 -0.15 |                 0.55 |                -0.15 |
| ('boat', 'far')          |                 -0.15 |                 0.15 |                -0.25 |
| ('boat', 'medium')       |                 -0.35 |                 0.6  |                -0.3  |
| ('boat', 'near')         |                 -0.2  |                 0.45 |                 0.05 |
| ('bus', 'far')           |                 -0.25 |                 0.4  |                -0.4  |
| ('bus', 'medium')        |                 -0.1  |                 0.4  |                -0.25 |
| ('bus', 'near')          |                 -0.2  |                 0.6  |                -0.25 |
| ('motorcycle', 'far')    |                 -0.25 |                 0.5  |                -0.15 |
| ('motorcycle', 'medium') |                 -0.1  |                 0.1  |                -0.1  |
| ('motorcycle', 'near')   |                  0    |                 0.55 |                -0.05 |

## 解釈上の注意

これは既存v1パイロットを見た後に設計した追加の探索的対照である。
Neutral XはX名の提示を揃える一方、文法や入力位置を厳密には揃えない。
よって純粋な抑制効果の因果的証明とはしない。
結果方向によらず追加プロンプトの再選定を行わない。
人手による出力監査、Cue監査は別作業として未完了。
