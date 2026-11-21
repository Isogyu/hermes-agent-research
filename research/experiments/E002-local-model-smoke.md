# E002 ローカル小型モデルでの疎通確認（2026-11-20）

- **目的**: 課金なしで Hermes を実際に動かせるか確かめる。
- **背景・仮説**: Ollama の `qwen3:4b-instruct`（tools 対応、2.5GB）を `provider: custom` でつなげば、遅くても動くはず。
- **実施内容**: `HERMES_HOME=lab/home`、`config.yaml` に `provider: custom`、`base_url: http://127.0.0.1:11434/v1`、`context_length: 64000`、`ollama_num_ctx: 64000`。`hermes -z "Reply with exactly: OK" --usage-file …`。
- **結果**:
  - 1回目（81秒、失敗）: Ollama が `request (10019 tokens) exceeds the available context size (4096 tokens)` を返した。Hermes は圧縮を試み、「会話が長すぎる」と表示してセッションを自動リセットした。
  - 2回目（Modelfile で `num_ctx 24576` にした別名 `hermes-lab-qwen3`、173秒、失敗）: `Error: Gateway disconnected; turn outcome is unknown`。Ollama のモデルは 4.6GB を占め、スワップ使用量は 7.5GB / 8GB。エージェントのログはモデルへのリクエスト開始で止まっている。
- **確認できた事実**:
  - 一言だけの依頼でも、最初のリクエストは約 10,019 トークン（system prompt とツール定義）。ログでは「14 core/visible tools kept, 7 deferred (~5518 tokens)」。
  - `ollama_num_ctx` は OpenAI 互換口（`/v1`）では効かず、Ollama は 4096 で読み込んだ。
  - 最小コンテキスト長は 64,000（`agent/model_metadata.py:281`）。
  - `hermes -z` は `gateway run --quiet --idle-exit` という常駐プロセスを osascript 経由で切り離して起動する。1回実行でも裏にゲートウェイが残る。
  - 1回目の失敗メッセージは原因（サーバー側のコンテキスト設定）を指しておらず、利用者には「会話が長い」としか伝わらない。
- **解釈**: この PC（8GB）では、Hermes が要求する規模のコンテキストを持つローカルモデルは実用にならない。Hermes の固定費（約1万トークン）は、小型モデルや低メモリ環境を事実上の対象外にする。
- **限界・反証**: 2回目の切断の原因は特定していない（メモリ逼迫によるタイムアウトと推定）。メモリに余裕のある機械なら動く可能性が高い。`num_ctx 16384` は試していない。
- **次の行動**: 台本どおりに応答する偽の OpenAI 互換サーバーを作り、モデルの賢さに依存しない仕組みの検証（Skill の読み込み、トークン固定費、承認、学習の起動条件）へ進む。実モデルでの検証は、API キーの利用について承認を得てから。
