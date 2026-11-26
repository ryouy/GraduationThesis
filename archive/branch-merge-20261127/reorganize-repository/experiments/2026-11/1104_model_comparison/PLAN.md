# 固定42問題による4モデル比較（推論前固定）

目的：基本課題が安定して成立するモデルを選ぶための校正比較。Qwen2.5-1.5B/3B/7B-InstructとMicrosoft Phi-3.5-mini-instructの4種類。モデル名はmodels.jsonで事前固定し、開始時に全モデルのrevision SHAを解決して保存、以後そのSHAからロードする。1.5Bは既知のSHAを継承。

問題はexperiments/2026-11/1103_fresh_check/results/answers.csvの42件（6概念×6説明＋none対照6）。user promptを完全に同じにし、採点はexperiments/2026-11/1103_fresh_check/rules.jsonの事前固定ルールを継承する。問題・採点をモデルごとに変更しない。全モデルへ共通のsystem「You are a helpful assistant.」を明示し、各モデルのchat templateを用いるためtoken列自体はモデル間で異なる。

全モデルFP16/SDPA、量子化なし。greedy、最大32token、repetition_penalty=1.0、num_beams=1を明示したGenerationConfigを使用。各モデル固有のEOS/PADのみ保持。従来のQwen固有systemと継承ペナルティ1.1とは変更があるため、1.5Bも再実行し、過去25/36を比較表に混ぜない。全入力・出力token列と生成設定を保存する。

Colab T4でモデルを順に実行し、必要ならCPUへFP16のまま一部offloadする。GPU上限14GiB、CPU上限8GiB、OOM時のみGPU上限13GiBでロードを再試行。実際のdevice_map・VRAM・ロード時間・生成時間を記録する。offload時の実行時間はモデル固有の推論速度とは解釈しない。GPU課金や有料APIは使用しない。各モデルは別processで実行し、エラーも保存、成功モデルだけを明記する。remote custom codeは実行せずtransformers内蔵クラスを使う。

採用目安は既存基準：36件中30以上かつ各概念4/6以上、none対照5/6以上。総数だけでなく概念別・切り詰め・原回答も確認する。通過したモデルを次の確認候補とし、近い性能なら小さいモデルを優先。これまで繰り返した42問は校正用であり、最終評価や母集団性能推定ではない。順位のわずかな差に有意性を主張しない。選定後は未使用問題・残り概念、Probe、距離×指示条件への転移を別途確認する。

この比較ではProbeの再学習は行わず、命名課題のモデル比較を完了する。
