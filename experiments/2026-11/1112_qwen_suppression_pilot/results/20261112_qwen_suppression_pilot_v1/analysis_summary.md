# Qwen抑制指示パイロット — コア測定結果

- **状態：** COMPLETED_CORE_PILOT_SEMANTIC_GRADING_SEPARATE
- **モデル：** Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775
- **入力：** 272（4X×16Cue×4条件＋Cueなし16）
- **生成：** 1360（5反復/入力）
- **Cue原本のSHA256：** `f9c1c729e285853c84702fe50cdf0f8ab105787dd995e36b525d778a4098a74c`
- **プロンプト設計のSHA256：** `4bec772934863e389c5495bad482a5e0e05db4cbeb71bab682cd4693ecf7a19f`
- **Logit Lens最終層のnative logits一致（最大誤差）：** 4.9591064e-05
- **明示的X言及：** 辞書判定。否定文中の語も言及と数える。
- **意味的X言及：** このファイルでは**未実施**。APIによる独立の後続判定は別出力に保存。

## 距離帯×指示条件：明示的X言及率

|                          |   Avoid X |   Base |   Think X |   Think Y |
|:-------------------------|----------:|-------:|----------:|----------:|
| ('bicycle', 'far')       |      0.2  |   0    |      0.7  |      0    |
| ('bicycle', 'medium')    |      0.5  |   0    |      0.75 |      0    |
| ('bicycle', 'near')      |      0.55 |   0.15 |      0.7  |      0    |
| ('boat', 'far')          |      0    |   0    |      0.25 |      0    |
| ('boat', 'medium')       |      0.25 |   0    |      0.55 |      0.1  |
| ('boat', 'near')         |      0.65 |   0.4  |      0.6  |      0.6  |
| ('bus', 'far')           |      0.15 |   0    |      0.55 |      0    |
| ('bus', 'medium')        |      0.3  |   0    |      0.55 |      0    |
| ('bus', 'near')          |      0.65 |   0.25 |      0.9  |      0.2  |
| ('motorcycle', 'far')    |      0.25 |   0    |      0.4  |      0.1  |
| ('motorcycle', 'medium') |      0    |   0    |      0.1  |      0    |
| ('motorcycle', 'near')   |      0.65 |   0.1  |      0.7  |      0.05 |

## Cue単位で平均した指示効果（Avoid X − Think X / Base）

| target_x   |   n_cues |   avoid_minus_thinkx |   avoid_minus_base |
|:-----------|---------:|---------------------:|-------------------:|
| bicycle    |       12 |               -0.3   |              0.367 |
| boat       |       12 |               -0.167 |              0.167 |
| bus        |       12 |               -0.3   |              0.283 |
| motorcycle |       12 |               -0.1   |              0.267 |

## 第24層Probeの条件差（各概念内でのみ解釈）

| target_x   |   n_cues |   avoid_minus_thinkx |   avoid_minus_base |
|:-----------|---------:|---------------------:|-------------------:|
| bicycle    |       12 |               -0.125 |              0.742 |
| boat       |       12 |                0.116 |              0.13  |
| bus        |       12 |               -0.806 |              0.313 |
| motorcycle |       12 |               -0.236 |              0.407 |

## 分析上の注意

- 結果は4つの乗り物概念に限る。CueはAI監査後の固定64文であり、独立人手検証は未了。
- 出力はCueごとの5生成をまとめて分析。Cue数は関連Cue48、無関係Cue16であり、1,360件を独立Cue扱いしない。
- Probeの出力はX/Yの**相対判別スコア**。異なる概念で生スコアを平均して「活性化量」とは呼ばない。
- 近い/中/遠Cueは内容や具体性も異なるため、観測された差を意味的距離だけの因果効果とみなさない。
- 無関係CueとCueなしを距離回帰に混ぜない。BaseのCueなしは全Xで同じ文字列。
- [プロトコル](https://github.com/ryouy/GraduationThesis/blob/main/docs/main_experiment_protocol.md)の事前検討事項を踏まえた探索的なパイロット。
