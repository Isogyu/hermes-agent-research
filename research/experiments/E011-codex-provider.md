# E011 Codex の契約を Hermes の推論元にする（2026-11-20）

- **目的**: 追加費用なしで実モデルを使えるようにする（利用者の承認済み）。
- **方法**: `lab/homes/real` に `provider: openai-codex` を設定。
- **経過**:
  1. `--provider openai-codex` だけでは「No provider configured」。設定ファイルに書く必要があった。
  2. 「No Codex credentials stored」。`auth.adopt_external_logins` は既定 True だが、自動取り込みは既存の認証を修復するときだけ働く（`hermes_cli/auth_codex.py:236-`）。
  3. `hermes auth add openai-codex --type oauth` は取り込みを聞かず、ブラウザのデバイス認証へ進む。30秒で中断した。
  4. Hermes の内部関数 `_import_codex_cli_tokens()` と `_save_codex_tokens()` を直接呼び、`~/.codex/auth.json` のトークンを実験用フォルダへ写した。元のファイルは書き換えない。
  5. `gpt-5.4-mini` は「ChatGPT アカウントでは非対応」で 400。`gpt-6-luna` で成功（3秒、入力 13,767、キャッシュ読み 3,712）。
- **確認できた事実**:
  - Codex と Claude の OAuth 更新トークンは使い捨てで、取り込むと Hermes と CLI が同じトークン系列を共有し、先に更新したほうが他方をログアウトさせる（`agent/credential_sources.py:32-38` のコメント）。Hermes 自身は別ログインを推奨している。
  - 取り込み時点でアクセストークンの残りは約73時間。Hermes が更新するのは期限の120秒前。短期の実験なら Codex CLI のログインは壊れない見込み。
  - 実トークナイザでの最小リクエストは 13,767 トークン。偽 LLM の見積もり（10,452）より3割多い。Responses API 向けのツール定義の違いと推定（未確認）。
- **注意**: 認証情報は `lab/homes/real/` とその複製（`lab/homes/run-*`、`trained*`）に入っている。これらは git の追跡から外した。**73時間を超えて使い続けると Codex CLI 側のログインが切れる恐れがある。** 長期に使うなら Hermes 用に別ログインをする。
- **次の行動**: このモデルで Skill 再利用実験を行う（E012）。
