# 公式最小コードと従来推論の照合

目的：バナナ命名0/6を、モデルの能力不足と決める前に入力・推論設定の影響を切り分ける。新規の性能検証ではなく、既に評価済みの42問題を用いる実装診断。

参照：https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct のQuickstart（2026-11-04確認）。公式例はsystemメッセージ、apply_chat_template(tokenize=False, add_generation_prompt=True)、tokenizer([text])、dtype auto、device_map auto、model.generateを使用する。

モデルrevision、問題文、採点は前回のまま固定。transformers4.57.6を維持し、GPU・PyTorch・実際のdtype/attention backend・generation_config・入力/出力token列を記録。

比較：legacy_fp32_eager（前回同様のtokenizer処理）、official_input_only_fp32_eager（userのみのままtokenizer([text])へ変更）、official_fp32_eager（公式のsystemを含む入力処理、precision/backendは固定）、official_fp32_sdpa（attentionのみ変更）、official_auto_sdpa（公式のauto dtype）、official_fp16_sdpa（T4でのFP16対照）。全42問をgreedy/max32で比較し、公式例のデフォルトsamplingとは区別する。公式デフォルト生成はバナナ先頭・直接バナナ質問・公式のLLM紹介例のみ最大512tokenで補助確認する。samplingのseedは42に固定、反復性能の推定はしない。

入力token列とattention maskの同一性を明示的に検査。FP32/eagerで最初のバナナ問題について、hidden抽出前後の生成token列も比較。最後にFP32/eagerの同じ先頭token logitsをCPUとGPUで比較し、CPU上のgreedy回答も1件取得する。CPU検証は低速のため1件のみ。計算誤差や設定差の観測だけでライブラリ一般のバグとは断定しない。

各モードの不対応・OOM等はエラーとして保存し、別モードの成功と混同しない。過去の原回答は上書きせず、再現一致件数と変更箇所を記録する。結果に応じて必要な小規模追試を別記する。
