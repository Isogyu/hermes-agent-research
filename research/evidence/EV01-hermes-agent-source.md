# EV01 Hermes Agent ソース解析（読み取りのみ）

- 対象: `repos/hermes-agent` commit 2de9f51（2026-11-20、v0.23.3+93）
- 方法: 読み取り専用のサブエージェントによる解析（2026-11-20）。パスはリポジトリルートからの相対。
- 区分: ここに書くのは、断りがない限りソースまたはテストで確認した事実。実行による確認は各実験記録を見ること。

## Skill
- 保存先は `HERMES_HOME/skills/[category/]<name>/SKILL.md`（YAML frontmatter と本文）。補助は `references/` `templates/` `scripts/` `assets/`。(`tools/skill_manager_tool.py:1-8`)
- 作成・更新ツールは `skill_manage`（create / patch / write_file / remove_file / delete）。(`tools/skill_manager_tool.py:840-949`)
- 作成の経路は2つ。
  - (a) メインのエージェントが裁量で呼ぶ。system prompt に `SKILLS_GUIDANCE` が入る。(`agent/prompt_builder.py:261`, `:1347-1366`)
  - (b) バックグラウンドレビュー。ターン終了後に会話をフォークし、`memory` と `skill_manage` だけを持つ別エージェントが振り返る。(`agent/background_review.py`)
- (b) の起動条件は回数カウンタで、複雑さは判定しない。Skill はツール呼び出し反復 10 回、メモリはユーザーターン 10 回。(`agent/review_signals.py:33-40`, `agent/turn_context.py:818-827`)
- レビュー用プロンプトは「Be ACTIVE — most sessions produce at least one skill update」と書き込みを促す。(`agent/background_review.py:532-603`)
- system prompt に入るのは名前と説明（60字で切り詰め）の一覧だけ。全文はモデルが `skill_view` を呼んで読む。最初から全文を入れるのは `skills.auto_load` と `--skills`。(`agent/skill_utils.py:846`)
- 安全スキャンは正規表現（`tools/skills_guard.py`）。Hub 導入は常にスキャン。エージェントが通常ターンで書いた Skill のスキャン `skills.guard_agent_created` は既定 False。人の承認 `skills.write_approval` も既定 False。
- 版管理は git ではなく `skills/.curator_ledger.jsonl` と blob。利用状況は `skills/.usage.json`。

## メモリ
- `HERMES_HOME/memories/MEMORY.md`（上限 2200字）と `USER.md`（1375字）。区切りは `\n§\n`。
- セッション開始時に一度だけ読み込んで固定。セッション中の書き込みはプロンプトに反映されない。
- セッション検索は `state.db` の FTS5。`session_search` は LLM を呼ばない。
- Honcho はコア外のカタログプラグインで、外部 API とキーが必要。

## 学習関連
- バックグラウンドレビューは既定で有効。cron（`cron/scheduler.py:2472`）と委譲された子エージェントでは無効。
- ワンショット（`-z`）は Skill 記録の促しをプロンプトから外す（`agent/oneshot_footprint.py`）。レビュー自体が止まるかは未確認。
- Curator は既定で有効。7日ごと・2時間アイドルで起動、14日で stale、30日で archive。LLM による統合は既定 False。
- 「Collective Wisdom」の実装はない（テスト用文字列に1度出るだけ）。
- Skill 再利用の効果を測る eval は `evals/` に見当たらない。

## 他エージェント・接続
- Claude Code / Codex は専用ツールではなく、同梱 Skill が `terminal()` で `claude -p` や `codex exec` を呼ぶ手順を教える方式。
- ACP サーバー（`hermes-acp`）、ACP クライアント（外部 CLI をモデルプロバイダにする）、`delegate_task`（同時3、深さ2）、MCP クライアントあり。MCP サーバーはプラグイン。
- プロバイダは約40種。ollama / vllm / llamacpp は `custom` の別名。

## 計測
- `hermes -z PROMPT --usage-file PATH`: トークン数・コスト・api_calls。ツール呼び出し回数は含まない。承認は自動で通る。
- `hermes chat -q … --format stream-json`: JSONL で tool_use などを出す。危険コマンドは既定で拒否。
- `state.db` の `sessions` 表に tool_call_count、トークン数、コスト。

## 安全性
- `approvals.mode` は manual / smart / off、既定 smart（補助 LLM が判定）。
- 実行バックエンドは local / docker / modal / daytona / vercel_sandbox / ssh。既定は local で隔離なし。

## gateway
- Teams アダプタはリポジトリ内にある（`plugins/platforms/teams/adapter.py`、Bot Framework、ポート 3978、TEAMS_CLIENT_ID / SECRET / TENANT_ID）。

## README・docs と実装の食い違い
1. README「FTS5 session search with LLM summarization」に対し、実装は LLM を呼ばない。
2. README は Honcho を学習ループの一部に挙げるが、実際は外部プラグイン。
3. 「Autonomous skill creation after complex tasks」は複雑さを判定せず回数で起動。cron と子エージェントでは無効。
4. `requires-python >=3.11` だが、依存は 3.14 でしか入らない（E001 で実機確認）。
