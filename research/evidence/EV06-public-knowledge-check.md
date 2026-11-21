# EV06 公開情報との照合（2026-11-21、Web 検索2件・標準モード）

目的: この研究の発見のうち、どれが既に公開されていて、どれが新しいかを見積もる。検索は2件だけで、網羅的ではない。

## 既に公開されていると見られるもの
- Skill が永続的な指示の置き場所になり、インジェクションの経路になるという指摘（セキュリティ系の解説記事、v0.8.0 の独立監査への言及）。
- Skill の検査器が文字列一致で回避されうるという GitHub の勧告（特定コミットに対するもの。現状は未確認）。
- Hermes の方針として、承認機構などはヒューリスティックで、OS レベルの隔離に頼るという整理。
→ E004・E009 は「既知の懸念を、現行版の既定設定で実行して確認した」という位置づけ。

## 公開情報に見当たらなかったもの
- Skill 学習の効果を独立に測った評価。流通している「自作 Skill が20個以上あると調査タスクが40%速い」は Nous の社内ベンチマーク由来で、方法が公開されていない。レビュー記事は再実行していないと明記している。
- 自動の振り返りが何を保存するか、その中身が役に立つかの検証。
- 自動の振り返りが1回実行・cron・子エージェントで無効という実装上の事実と、その実測。
- 前提が変わったときに Skill が誤答する度合いの実測。

## 出典
- https://dev.to/tokenmixai/hermes-agent-review-956k-stars-self-improving-ai-agent-april-2026-11le
- https://ssojet.com/blog/hermes-agent-self-evolving-skills.md
- https://dev.to/crushforce/how-hermes-agents-self-improving-skills-actually-work-notes-from-building-a-real-agent-on-it-4dcn
- https://docsearch.algolia.com/mcp/docs/repo/nousresearch/hermes-agent-self-evolution
- https://neuraltrust.ai/blog/hermes-agent-security
- https://medium.com/@ishayvilroel/hermes-agent-what-security-teams-should-understand-before-they-run-it-e413de65fcd4
- https://gist.github.com/YLChen-007/9dd399c6f75b31fa741a613dfd41de08
- https://arxiv.org/pdf/2604.02837

## 注意
検索結果は要約経由で、各ページの原文は読んでいない。「見当たらなかった」は「存在しない」の証明ではない。記事化の前に、GitHub の Issue と公式ドキュメントを含めて調べ直す。別リポジトリ hermes-agent-self-evolution（DSPy と GEPA で Skill を最適化する仕組み）は未調査で、今回の「製品内の自動振り返り」とは別物。
