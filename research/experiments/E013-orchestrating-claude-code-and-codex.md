# E013 Hermes から Claude Code と Codex を動かす（2026-11-21）

- **目的**: Hermes が既存エージェントの上位制御層になれるかを実行で確かめる（H6）。
- **背景**: Hermes に専用の連携ツールはなく、同梱 Skill（`claude-code`、`codex`）が `terminal` での呼び出し方を教えるだけ（EV01）。仮説: 委任は動くが、直接実行より遅く、Skill の記述と実際の CLI のずれで失敗しやすい。
- **課題**: `textkit.py` に `slugify` と `wrap_title` を実装し、テスト9件を通す（`lab/bench/gen_code_ws.py`）。採点はテストファイルを原本に差し替えて実行（`check_code.py`）。Hermes のモデルは `gpt-6-luna`。各条件1回。
- **結果**:

| 実行 | 経路 | 所要 | 結果 | 備考 |
|---|---|---|---|---|
| d1-direct-claude | `claude -p` を直接 | 61秒 | 9/9 | 7ターン、`--permission-mode acceptEdits` と Bash 許可を指定 |
| d1-direct-codex | `codex exec` を直接 | 33秒 | 9/9 | 9,721 トークン |
| d2-hermes-alone | Hermes 単独 | 34秒 | 9/9 | 7回の呼び出し、入力 99,757 |
| d2-hermes-codex | Hermes → Codex | 61秒 | 9/9 | 11回、入力 184,563（Hermes 側のみ） |
| d2-hermes-claude | Hermes → Claude Code | 53秒 | **0/9** | 古い `claude` を掴んで失敗 |
| d3-hermes-claude-fixedpath | Hermes → Claude Code（場所を指定） | 307秒 | 9/9 | 回り道をして成功 |

- **Claude Code 委任で起きたこと**:
  1. この PC には `claude` が2つある（`/opt/homebrew/bin` の 2.1.316 と `/usr/local/bin` の 2.1.31）。通常のシェルは新しい方を使うが、Hermes の端末は古い方を先に解決した。古い版は現在のモデル名を知らず `404 model: fable`。Hermes は失敗を正直に報告し、成果物を捏造しなかった。
  2. 場所を指定した再実行では、Hermes は権限の指定なしで `claude -p … --max-turns 8` を呼んだ。1回目は上限ターンに到達。2回目は Claude Code 側の権限層がファイル書き込みをすべて拒否し、Claude Code は実装を自分の一時フォルダに書いた。
  3. Hermes はその一時フォルダのファイルを見つけ、自分で `cp` して作業フォルダへ入れ、テストを通した。
- **Codex 委任で起きたこと**: 同梱 Skill は `terminal(…, pty=true)` と教えるが、ツールは `pty requires background=true` で拒否。Hermes はエラーを読んで `background=true` を足し、`process_manage` で完了を待った。Skill の記述がツールの現状と合っていない。
- **解釈**:
  - 委任は「動かせる」が、上位制御層としての付加価値はこの課題では見えない。Hermes 単独（34秒）が最速で、委任は直接実行の約2倍〜5倍かかった。
  - 連携は「Skill という文章」と「実際の CLI」の一致に依存する。版のずれ、権限の既定値、PATH の違いがそのまま失敗になる。専用の連携機構（Claude Code のサブエージェントや SDK）と比べて脆い。
  - 下位のエージェントが権限で止められた作業を、上位の Hermes が代わりに実行した。今回は依頼の範囲内だが、下位の権限設定が上位の層で意味を失うという統制上の論点になる。
  - 良い点: 失敗時に捏造せず報告した。エラーから自力で呼び出し方を直した。
- **限界**: 各条件1回。課題が小さく、単独で解けるものを委任させている。委任が意味を持つのは、長時間・並列・別モデルの強みが要る作業のはずで、それは測っていない。Hermes のモデルは軽量の luna。
- **この PC についての注意**: `/usr/local/bin/claude`（2.1.31）は古い導入の残りと思われる。Hermes に限らず、PATH の順序次第で古い版が使われる。
- **次の行動**: 委任が意味を持つ課題（複数ファイルの並列作業、Codex に実装させ Claude Code にレビューさせる分業）で再評価する。`delegate_task`（Hermes 自身の子エージェント）との比較。
