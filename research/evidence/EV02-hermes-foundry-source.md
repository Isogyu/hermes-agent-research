# EV02 Hermes Foundry ソース解析（読み取りのみ）

- 対象: `repos/hermes-foundry` commit 8367c97（2026-11-13）
- 方法: 読み取り専用のサブエージェントによる解析（2026-11-20）。テストは実行していない。
- 区分: ［コード］コードで確認、［文書］ドキュメントの記述のみ、［推定］推論。

## 正体
- ［コード］Hermes Agent を Microsoft Foundry の hosted agent として1コンテナで動かすためのパッケージ。Hermes 本体のソースは含まない。
- ［コード］`src/` は edge（.NET 9、Microsoft Agents SDK、:8088）、gateway（Python 標準ライブラリの中継、:8080）、sidecar（FastMCP の M365 ツール約40個、:8010）、hermes-patches（ビルド時に Hermes へ当てるパッチ）。
- ［コード］ベースイメージは `nousresearch/hermes-agent` を digest 固定。Hermes の認証・api_server 周りを AST で確認しながら書き換える。
- ［コード］起動時の config で `disabled_toolsets: file, terminal, code_execution, browser, project` を指定。つまり Foundry 版の Hermes は端末もファイルも使えず、M365 の MCP ツールが主な手段になる。
- ［コード］リポジトリ内に「Hermes Enterprise」という語はない。テナントごとに手作業で入れる POC という位置づけ（README.md:7-11）。

## Azure のリソース
- ［コード］Bicep が作るもの: AIServices（S0、public）、Foundry project、ACR Basic（public）、モデル配置 `gpt-6.1-sol`（GlobalStandard、5K TPM）、RBAC、ユーザー割り当て MI（リソースグループの Contributor）、deploymentScript（Agent Identity Blueprint を preview API で作成）、Azure Bot F0（SingleTenant、Teams チャネル）。
- ［コード］Bicep の外: hosted agent 本体（2 CPU / 4Gi）、Logic App、Graph の delegated scope 宣言、Teams セットアップアプリ。
- ［コード］作られないもの: Container Apps、Key Vault、Storage Account、App Insights。
- 課金: トークン、ACR、Logic App、hosted agent の compute、Bing grounding。［文書］M365 側に Copilot 1席と Frontier for AI Teammates 席が要る。

## Teams / M365
- ［コード］受信は Bot Framework。M365 操作は sidecar から Graph v1.0。
- ［コード］人間ユーザーの OBO は使わない。エージェントは専用の Agent User として動く。
- ［コード］呼び出し元は owner / colleague / outsider の3段階。colleague への権限は HMAC 署名付き grant として OneDrive に保存。
- ［コード］マルチテナント非対応。
- ［コード］要求する Graph scope: Chat.ReadWrite, Mail.ReadWrite, Mail.Send, Calendars.ReadWrite, Files.ReadWrite.All, Sites.ReadWrite.All, User.Read.All, User.ReadBasic.All。

## モデル
- ［コード］Foundry の OpenAI 形式モデルのみ。既定 `gpt-6.1-sol`。Hermes 系モデルを既定にしている箇所はない。
- ［コード］Nous を選ぶ場合はユーザーが各自 OAuth し、課金は個人の portal アカウント。

## 状態と共有
- ［コード］owner のターンのときだけ `memories, skills, SOUL.md, skill-bundles, pending/*` を Agent User の OneDrive に tar.gz で同期（ETag の 3-way merge）。
- ［コード］Skill とメモリは Agent User（インスタンス）単位。インスタンス間・ユーザー間・テナント間で共有されない。
- ［コード］「Collective Wisdom」や組織内 Skill 共有の実装は見つからない。

## README と ROADMAP の食い違い
- README は「loopback only」と書くが、gateway・sidecar・Hermes は `0.0.0.0` で bind。
- README「installer も IaC も無い」に対し、`setup.sh`・Bicep は実在。
- README「完全な CI が無い」に対し `.github/workflows/ci.yml` がある。
- ROADMAP の未実装: ユーザーごとのモデル利用権、quota を考慮した failover、routine の即時失効と鍵ローテーション、相関ログ、統合テスト、完全な uninstall、ライセンスとサポート条件。

## セキュリティ上の懸念
- ［コード］署名鍵 `IdentitySignKey` `RoutineBindingSignKey` が hosted agent version の平文環境変数。
- ［コード］sidecar の MCP（:8010）は認証なし。gateway の鍵比較は定数時間でない。
- ［コード］edge に受信 JWT の検証がなく、Foundry の `BotServiceTenant` に任せている。
- ［コード］deploymentScript 用 MI がリソースグループの Contributor を持ち続ける。`Files.ReadWrite.All` と `Sites.ReadWrite.All` は広い。

## ローカルで動かせる範囲
- ［コード］Python unittest 約372件と .NET xunit 24件は Azure なしで動く設計（未実行）。
- ［推定］コンテナはヘルスチェックまでは応答するが、Foundry の MI と Graph トークンがないとターンは成立しない。
- ［コード］docker-compose や Graph / Foundry のモックは含まれない。
