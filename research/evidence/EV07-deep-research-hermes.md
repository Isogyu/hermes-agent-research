
# Hermes Agent 公開情報調査：Claude Code / Codex を超える余地と「常駐する仕事仲間」が成立する条件

## 結論と調査範囲

2026年11月21日時点で公開情報から最も強く言える結論は、**Hermes Agent の優位性は「単発タスクの知能」よりも、「自分で所有・運用できる常駐型のエージェント基盤」にある**、ということです。Hermes Agent は、モデルを交換しながら同じローカルの記憶・Skills・メッセージング・cron・サブエージェント環境を維持できるため、Claude Code や Codex を「モデル付きの作業者」として内部から呼ぶメタエージェントにもなれます。一方で、**Skills、長期記憶、定期実行、クラウド実行、Slackからの呼び出し、複数エージェント並列実行そのものは、2026年には Claude Code / Claude Tag と Codex にもかなり吸収されており、もはや Hermes 固有の差ではありません**。Hermes に残る差は、OSS・自己ホスト・モデル非依存・複数メッセージ基盤・ユーザーが直接点検できる記憶と手順資産、という運用上の自由度です。

問い1については、**公開された第三者ベンチマークから「Hermes のほうが Claude Code / Codex よりタスク品質が高い」と言える領域は、現時点では見つかりませんでした**。特にコーディング品質について、同一モデル・同一課題・同一予算で Hermes と Claude Code / Codex を比較した独立評価は確認できませんでした。むしろ Claude Code と Codex は、2026年には Skills、サブエージェント、長時間タスク、クラウド実行、定期実行、メモリまで揃えており、コード中心の用途では専用ハーネスとレビューUI、worktree、PRワークフローを持つ両者に構造的な強みがあります。

問い2については、**「人が毎回プロンプトして結果を受け取る」働き方から、「常駐エージェントに継続的な役割を持たせる」働き方へ移れること自体は、数週間から数か月の実運用報告で実証されています。ただし、公開事例は『人を不要にした』というより、『人の仕事を指示・承認・例外処理・エージェント運用へ移した』ことを示しています**。最も情報量が多い Cloudvisor の5か月の運用では、複数 Hermes を常時稼働させ、学習した Skill が実務上のミスを恒久的に修正した例がある一方、役に立たないエージェント工程の撤去、自己再起動による障害、自己生成タスクの循環、監視・バックアップ・復旧・コスト制御に週数時間を使うことも報告されています。しかも同社自身、当初期待した「納期50%短縮」を測定できず、最終的な生産性効果は不明としています。

もう一つ重要な結論があります。**あなたの「Collective Wisdom は公開2リポジトリに実装がない」という実測は、現在は更新が必要です。** 2026年11月11日までに NousResearch は `hermes-collective-wisdom` という第3の公開リポジトリを公開しており、Hermes Agent 0.21.5+ 向けの公式プラグインとして、チームへの Skill の共有、バージョン管理、承認付きインストール、共有候補の提案を実装しています。ただし「自動的に社内全体へ知識が伝播する」という宣伝的表現とは異なり、公開コードの現行設計は**共有時に人間の明示承認を要求し、バックグラウンドで勝手に共有しない**仕組みです。

なお、基準版の Hermes Agent v0.23.3 は2026年11月19日付のリリースとして確認できました。以下では Hermes Agent OSS、Hermes Foundry、Hermes Enterprise を分離して扱います。Nous Research の Hermes 3/4 等の言語モデルは対象外です。

## 主張の一覧表

下表の「信頼度」は、その主張が事実として確認できる強さを示します。「公式の主張」であっても、性能効果が再現されていないものは高評価にしていません。

| **主張** | **対象（Agent / Foundry / Enterprise）** | **根拠の種類** | **出典 URL** | **日付と版** | **信頼度** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Hermes は Skills、会話横断メモリ、ユーザーモデル、cron、複数メッセージ基盤、並列サブエージェントを持つ | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 2026-11、v0.23.x | 高 |
| Nous は Hermes を「built-in learning loop」を持つ self-improving agent と位置付けている | Agent | 公式の主張（根拠なし） | [https://github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 2026-11 | 高〔主張の存在〕／低〔効果〕 |
| Skills は必要時に本文をロードする progressive disclosure 方式だが、Skill 一覧・説明は system prompt に入る | Agent | ソースコードや Issue の一次情報 | [https://hermes-agent.nousresearch.com/docs/user-guide/features/skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | 2026-11 | 高 |
| 約200 Skills の実環境で Skill index が約11.5K tokens/turn を消費し、線形増加すると報告された | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent/issues/89844](https://github.com/NousResearch/hermes-agent/issues/89844) | 2026-08頃 | 中〜高 |
| 約200 Skills、400K+ token の長期会話で Skill / memory recall が低下するという実利用報告がある | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent/issues/76307](https://github.com/NousResearch/hermes-agent/issues/76307) | v0.19.1、2026-08頃 | 中 |
| 「20+ self-created Skills で類似research taskが約40%高速化」という数字が流通している | Agent | 公式の主張（根拠なし） | [https://hermes-agent.nousresearch.com/](https://hermes-agent.nousresearch.com/) および二次引用 | 2026 | 低〜中 |
| 上記40%について、公開された課題セット、N、モデル、分散、raw trajectories を伴う一次ベンチマークは確認できなかった | Agent | 推測〔公開探索結果に基づく〕 | 公式docs・GitHub・引用元群 | 2026-11-21まで | 中〜高 |
| 一部記事は40%を「TokenMix検証済み」と呼ぶが、公開された独立再現手順は確認できない | Agent | 報道 | [https://tokenmix.ai/blog/hermes-agent-review-self-improving-open-source-2026](https://tokenmix.ai/blog/hermes-agent-review-self-improving-open-source-2026) | 2026 | 低 |
| SkillsBenchでは curated Skills が平均+16.2pp、一方 self-generated Skills は平均的な改善なし | Agentに直接ではない一般研究 | 第三者の測定 | [https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670) | 2026-02、7,308 trajectories | 高 |
| SkillsBenchでは86 tasks/11 domains中、Skill が逆効果になる課題も存在する | Agentに直接ではない一般研究 | 第三者の測定 | [https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670) | 2026-02 | 高 |
| 反復的にSkillを自己書換えさせ、外部フィードバックを与えないと30 rounds後にSkillsBenchで平均約15pt悪化した | Agentに直接ではない一般研究 | 第三者の測定 | [https://arxiv.org/abs/2611.25534](https://arxiv.org/abs/2611.25534) | 2026-11-19 | 高 |
| Skill poolを5→100に増やすと実際の利用 precision が29.6%→3.3%へ低下するとの測定がある | Agentに直接ではない一般研究 | 第三者の測定 | [https://arxiv.org/abs/2608.14036](https://arxiv.org/abs/2608.14036) | 2026-08 | 高 |
| Voyager の成功は「自己生成Skill」だけでなく、環境feedback、execution errors、self-verificationを使った改善ループに依存する | Agentに直接ではない一般研究 | 第三者の測定 | [https://ut-austin-rpl.github.io/publications/2024/03/14/wang-tmlr24-voyager/](https://ut-austin-rpl.github.io/publications/2024/03/14/wang-tmlr24-voyager/) | TMLR 2024 | 高 |
| `hermes-agent-self-evolution` は DSPy + GEPA でSkillを最適化する実験repoで、README上は当初Phase 1中心、API費用目安$2–10/run | Agent関連実験 | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) | 2026 | 高 |
| self-evolution repoにはreleaseがなく、「GEPAが実Skillを書き換えない」「出力がdeployされない」等の重大Issue/PRが多数ある | Agent関連実験 | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent-self-evolution/issues/33](https://github.com/NousResearch/hermes-agent-self-evolution/issues/33) | 2026-04〜11 | 高 |
| self-evolutionを「Hermesの実証済み自己改善機構」とみなす根拠はない | Agent関連実験 | 推測 | 上記repo/Issues | 2026-11 | 高 |
| Background Review が bundled/hub skill を無人で書換え得たというIssueがある | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent/issues/20273](https://github.com/NousResearch/hermes-agent/issues/20273) | 2026、当時の実装 | 高 |
| Background Review が5日間で不完全なfrontmatterを持つSkillを複数生成した実環境報告がある | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent/issues/101402](https://github.com/NousResearch/hermes-agent/issues/101402) | 2026-09頃 | 中〜高 |
| 24 profile共有環境の30日auditでBackground Review由来340 writes、重複編集等が観測され、運用者が自動writeを無効化した | Agent | ソースコードや Issue の一次情報 | GitHub issue #156124 | v0.23.1付近、2026-11 | 高 |
| cronはBackground Reviewを明示的にskipするコードパスが報告されている | Agent | ソースコードや Issue の一次情報 | GitHub issue #137339 | v0.21.6–0.21.7/main、2026-10 | 高 |
| Background Reviewのforkが古いmessage snapshotから共有memory/skillを書換える競合リスクが報告された | Agent | ソースコードや Issue の一次情報 | GitHub issue #9055 | 2026 | 高 |
| Cloudvisorは2026年3月頃から5か月、最大8体程度のHermesを実運用したと報告 | Agent | 第三者の体験談 | LinkedIn / Rimas Lukaszewicz | 2026-08、約5か月の履歴 | 中〜高 |
| CloudvisorではSkill追記により特定の図面ミスが以後再発しなくなった例がある | Agent | 第三者の体験談 | LinkedIn / Cloudvisor series | 2026-08〜09 | 中 |
| ただし同じ図面エージェント全体は品質不足で3週間後に停止され、人間確認型ワークフローへ変更された | Agent | 第三者の体験談 | 同上 | 2026 | 中 |
| Cloudvisorではself-repair agentが自分で作ったrepair cardを消費する循環に入り、役割そのものを廃止した | Agent | 第三者の体験談 | LinkedIn / Cloudvisor series | 2026-09 | 中〜高 |
| agentが自分をcronから再起動し、cron自身を殺したため障害を4日間見逃した事例がある | Agent | 第三者の体験談 | LinkedIn / Cloudvisor series | 2026-09 | 中〜高 |
| Cloudvisorは一部の二重レビュー工程を「品質低下＋token浪費」のため撤去した | Agent | 第三者の体験談 | LinkedIn / Cloudvisor series | 2026-08 | 中 |
| Cloudvisor自身、期待した「delivery time半減」を測定できず、総生産性改善率は不明とした | Agent | 第三者の体験談 | LinkedIn / Cloudvisor series | 2026-09 | 高 |
| 別ユーザーが4週間、cronでニュース収集→選別→要約→メール配信パイプラインを継続運用した | Agent | 第三者の体験談 | [https://www.foundry81.com/posts/four-weeks-hermes-agent/](https://www.foundry81.com/posts/four-weeks-hermes-agent/) | 4週間、2026 | 中 |
| Hermes Foundry repoは公式にWIP/PoCであり、production-readyなEnterprise distributionではない | Foundry | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-foundry](https://github.com/NousResearch/hermes-foundry) | 2026-11 | 高 |
| Foundry版はHermesに独自Entra identity、M365 mailbox/calendar/OneDrive等を与える | Foundry | 公式の主張（方法つき） | [https://nousresearch.com/hermes-enterprise-on-microsoft-foundry](https://nousresearch.com/hermes-enterprise-on-microsoft-foundry) | 2026-11 | 高 |
| Foundry Autopilotは2026-11時点でFrontier preview enrollment等が必要で、instanceごとにAgent365 license seatを消費する | Foundry | ソースコードや Issue の一次情報 | [https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-365](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-365) | 2026-11 | 高 |
| MicrosoftとNousの関係は単なる個人実装ではなく、Nous公式・Microsoft側双方で公表された協業 | Foundry / Enterprise | 公式の主張（方法つき） | [https://nousresearch.com/hermes-enterprise-in-microsoft-teams](https://nousresearch.com/hermes-enterprise-in-microsoft-teams) | 2026-11-18 | 高 |
| Hermes Enterpriseはcustomer Azure tenantでの提供も案内されている | Enterprise | 公式の主張（根拠なし） | [https://nousresearch.com/hermes-enterprise-in-microsoft-teams](https://nousresearch.com/hermes-enterprise-in-microsoft-teams) | 2026-11-18 | 高〔提供方針〕 |
| Enterpriseの公開定価は確認できず、business portalはcontact-sales型 | Enterprise | 公式の主張（根拠なし） | Nous Business portal | 2026-11 | 高 |
| Collective Wisdomは現在、独立した公式OSS plugin repoとして公開されている | Agent / Enterprise関連 | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-collective-wisdom](https://github.com/NousResearch/hermes-collective-wisdom) | Agent 0.21.5+、repo更新2026-11-11 | 高 |
| 現行Collective Wisdom pluginは共有を完全自動化せず、共有・install/updateに人のreview/approvalを置く | Agent / Enterprise関連 | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-collective-wisdom](https://github.com/NousResearch/hermes-collective-wisdom) | 2026-11 | 高 |
| Agent repo本体に一度Collective Wisdom V1が入り即日revertされた痕跡があり、その残骸がAPI 500を起こしたIssueがある | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent/issues/108967](https://github.com/NousResearch/hermes-agent/issues/108967) | 2026-09 | 高 |
| Hermes公式Security Policyは「敵対的LLMに対する真正のsecurity boundaryはOS-level isolation」と明記している | Agent | ソースコードや Issue の一次情報 | [https://github.com/NousResearch/hermes-agent/security](https://github.com/NousResearch/hermes-agent/security) | 2026-11 | 高 |
| Approval gate、redaction、pattern scanner、tool allowlistは公式にcontainment boundaryとはされていない | Agent | ソースコードや Issue の一次情報 | 同上 | 2026-11 | 高 |
| Skill DESCRIPTION等を経由した永続prompt injectionの実証Issueが存在する | Agent | ソースコードや Issue の一次情報 | GitHub issue #8884 | 2026-04以降 | 高〔攻撃の存在〕／中〔現行版での残存〕 |
| 2026年中にSkill Guard、memory scanning、env sanitization、sandbox等に複数CVEが付与され、一部は0.15.0/0.18.0等で修正済み | Agent | ソースコードや Issue の一次情報 | GitHub advisories / NVD | 2026 | 高 |
| Claude Codeは2026年現在Skills、CLAUDE.md memory、subagents、hooksを備える | 比較対象 | 公式の主張（方法つき） | Anthropic docs/news | 2026 | 高 |
| Claude CodeのCloud Routinesはschedule/API/GitHub eventsで無人実行できる | 比較対象 | 公式の主張（方法つき） | Anthropic docs/news | 2026-04以降 | 高 |
| Claude TagはSlack常駐、channel横断context、memory、ambient/proactive動作、hours/daysのscheduled workを備える | 比較対象 | 公式の主張（方法つき） | [https://www.anthropic.com/news/introducing-claude-tag](https://www.anthropic.com/news/introducing-claude-tag) | 2026-06-23、beta | 高 |
| CodexはSkills、parallel agents、worktrees、Automationsを備える | 比較対象 | 公式の主張（方法つき） | [https://openai.com/index/introducing-the-codex-app/](https://openai.com/index/introducing-the-codex-app/) | 2026-03以降 | 高 |
| Codex Automationsは同じthreadを再利用し、days/weeksにまたがり自ら起床して仕事を継続できる | 比較対象 | 公式の主張（方法つき） | [https://openai.com/index/codex-for-almost-everything/](https://openai.com/index/codex-for-almost-everything/) | 2026-04 | 高 |
| Codexは2026年、memory、scheduled tasks、browser、Computer Use、Record & Replayによるworkflow→Skill化を提供する | 比較対象 | 公式の主張（方法つき） | OpenAI Help Center | 2026-11現在 | 高 |
| OpenClawやLettaにも常駐、memory、cron/background worker、skillsに相当する構造があり、「常駐型」自体はHermes固有ではない | 比較対象 | 公式の主張（方法つき） | 各公式docs | 2026 | 高 |

「20+ Skills / 40% faster」については特に注意が必要です。Nous関連の紹介ページや TokenMix 記事では数字が引用されていますが、**同じ課題を何回実行したのか、20個がどのように作られたのか、fresh agentとのprompt/model/token budgetをどう揃えたか、統計誤差がどれだけかを示す公開一次資料を確認できませんでした**。したがって、これは現時点で「自己改善の効果量」として実験を省略できるレベルの根拠ではありません。

むしろ2026年の独立研究は、より限定的な結論を支持します。SkillsBenchでは**人間がよく作ったSkillは大きく効くが、モデル自身が作ったSkillは平均では効かなかった**うえ、Skill効果には負のケースもありました。また11月19日のself-evolution研究では、feedbackなしにSkillを何度も自己書換えすると、モデルがもともと知っている一般論へ文書が引き寄せられ、専門家が書いた「モデルのprior外の情報」が失われることが確認されています。これは、あなたが観測した「background reviewが具体値を落として一般的手順書にする」という現象とかなり近い機序です。ただし、これはHermesのreview promptそのものを測った論文ではありません。

`hermes-agent-self-evolution` についても、現状は「自己改善の追加証拠」ではなく、むしろ**未成熟な研究用パイプライン**として扱うべきです。READMEはDSPy/GEPAによるSkill最適化を掲げますが、公開Issueには「fitnessが実質的なsemantic task successを見ていない」「GEPAの変更が実際のSkillへ書き戻されない」「evolved outputがdeploymentへ到達しない」といった根本的な不具合が継続的に指摘されています。releaseも確認できません。

## 私の実測との照合

| **あなたの実測** | **公開情報との照合** | **判定** |
| :--- | :--- | :--- |
| 明示保存Skillで0/3→3/3 | Hermesで全く同じ3/3の独立再現は見つからない。ただしCloudvisorでは、利用者からの訂正をSkillに1文追加した後、図のreturn legミスが以後毎回直ったと報告。一般研究でもcurated Skillsは平均+16.2pp。 | **方向は強く一致、数値再現なし** |
| Background Review Skillは具体値を失い0/3、再試行やprompt変更でも改善せず | 「具体値が消える」というHermes固有の同一報告は見つからない。一方、24-profile環境で340 autonomous writesと重複・不適切変更、background-created Skillのprovenance欠落、stale snapshot writeが報告されている。独立研究でもself-generated Skillsは平均無改善、feedback-free rewriteは専門知識を失う。 | **機序・危険性は一致、あなたの具体的failure modeは未再現** |
| Background Reviewは`-z`、`chat -q`、cron、子agentでは発火しない | cronについてはIssue #137339がコード上 `skip_background_review=True` と明示しており一致。一方、short-lived Kanban/group bot runtimeでreviewがlostするIssueもある。one-shot docsも通常sessionとは異なる軽量経路を記載するが、`-z`/`chat -q`/子agentの4条件すべてを一括確認した公開検証は見つからない。 | **cronは公開一次情報で一致。他3条件は公開証拠不足** |
| script付きSkillで手数/token約1/3。ただしルール変更で0/3なのに成功報告 | Hermesで同じ比率やfalse-successを測った報告は見つからない。一般研究ではSkillsはbrittle assumptions / incompatible contextsで失敗するとされ、Cloudvisorでは自動チェックを通しながら実際の成果物が不十分だった工程が廃止された。 | **定性的には一致、定量再現なし** |
| 最小request約1万tokens、2000 Skillsで約5.8万tokens | exactな10K/58K再現は見つからない。しかし約200 Skillsでavailable-skills blockだけ約11.5K tokensというIssueがあり、線形増加を実測している。また200 Skills利用者はrecall低下も報告。 | **強い部分一致。あなたの2000件データは独自価値が高い** |
| 通常turnでagentが書くSkillは既定安全検査を通らない | Skill scanner/write approval/security guardの実装・問題は公開されているが、「通常turnで生成したSkillがdefault設定では恒常的にfailする」という独立実測は見つからない。 | **見当たらない** |
| Collective Wisdomは公開2repoに実装なし | **2026-11-21現在は反対。** `NousResearch/hermes-collective-wisdom` が別repoとして公開済み。Agent本体では一度V1を入れてrevertした痕跡もある。 | **現在は反証された** |
| Claude Code/Codexへの委任は動くが遅く脆い | HermesからClaude Code/Codex CLIをworkerとして使う利用者報告はある。一方で公開の比較計測はない。ある利用談ではClaude workerは比較的smooth、Codex側のcoordinationを「nightmare」と評しており、別利用者はClaude CLI呼び出しを問題なく使っている。 | **委任可能性は一致。速度・脆さは混在し定量証拠なし** |

「見つからない」とした項目について、主要検索語は以下でした：`"Hermes Agent" background review loses details values`, `"background review" skill generic concrete values`, `"Hermes" skill stale rule false success`, `"skill script" outdated rule Hermes`, `"Hermes" 10000 tokens minimum prompt`, `"Hermes" 2000 skills 58000 tokens`, `"guard_agent_created" skill scanner`, `"skill_manage" default safety rejected`, `"skip_background_review" oneshot`, `"background review" child agent`, `"chat -q" background review`。検索範囲は NousResearch GitHub organization、Hermes docs、GitHub Issues/PRs、一般Web検索、Reddit/Hacker News/公開ブログ、論文検索です。見つからなかったこと自体から「存在しない」とは断定していません。

ここであなたの実験の価値がかなりはっきりします。**「手で正しく作ったSkillは効くが、自動振り返りは知識を一般化しすぎる」という大筋は2026年の独立研究と整合しています。しかし、Hermes Background Reviewそのものを同一業務・複数試行で評価した公開ベンチマークは見つかりません。** あなたの0/3→3/3→0/3という対照実験は、単なる機能確認よりも公開知識の空白を直接突いています。

## 実運用・企業利用・セキュリティから見える境界

Bの「数週間以上使った人」を探した結果、最も価値が高いのは Cloudvisor の連続レポートでした。これは短時間のレビューではなく、2026年春から少なくとも5か月、複数エージェントを常時稼働させた運用記録です。同社が Hermes を選んだ理由は、自己ホストでき、モデルを変えてもmemory / skills / historyを維持できることでした。これは「モデルを交換できる常駐作業者」という Hermes の構造的差を、実際の組織が評価した数少ない一次体験です。

しかし、その事例は自己改善の成功談だけではありません。ある図面生成フローでは、利用者の訂正をSkillへ保存すると同じ局所ミスが再発しなくなった一方、成果物全体の品質不足から3週間後に自動生成そのものを止め、Hermesは「人が最終成果物を作るためのprompt生成」に後退しました。別の二重レビュー工程では、二人目のagentを追加すると文書が悪化しtokenも増えたため、その工程を撤去しています。つまり、**Skill学習は局所的な再発防止には成功しても、業務全体を自律化できるとは限らない**という実例です。

常駐化には別種の失敗も生じました。自己修復用agentが自分で作ったrepair cardを自分で処理し続けるself-feeding loopに入り廃止された例、orchestratorが自身をcronから再起動してcronを途中で殺し、外形上processが生きていたため4日間障害を見逃した例があります。運用者は、最終的にplain scriptや外部supervisorのような**agentの外側の決定論的な監視・制御**が必要だとしています。

これは問い2への重要な答えです。仕事の形は変わっていますが、**「人→AIへ仕事が移る」だけではなく、「手作業→AIの監督・権限設計・失敗検知・Skill管理へ仕事が移る」**のが実態です。Cloudvisorは更新、backup、monitoring、recovery、access policy、cost limit、quality checkを自前で設計し、運用工数を週4時間程度と記述しています。それでも最終報告では納期短縮率を測れていません。したがって、現段階の公開情報は「常駐agentで仕事の分担は変わる」を支持しますが、「総労働時間やコストが確実に減る」までは支持しません。

より小規模な例では、Foundry81が4週間、Hermesを定時起床させ、ニュース源確認→候補選別→要約分析→メール・archiveというループを運用し、情報収集に使っていた時間を編集・戦略へ回せるようになったと述べています。ただし比較実験や時系列工数はなく、体験談の域を出ません。Hacker NewsやRedditにも数週間〜数か月、研究、Obsidian、home automation、life admin、server managementに使ったという利用者がいますが、逆に「使うより設定に時間を費やすようになった」と離脱・不満を述べる長期利用者も見つかりました。

長期運用の技術的問題も一次情報が増えています。約200 Skillsの利用者は、長期会話で関連Skillを選ばなくなりmemoryも効かなくなると報告しています。別Issueでは200 Skillsの説明一覧だけで約11.5K tokens/turnを使うと実測されました。Background Reviewについては、24 profilesの共有環境で30日間に340 writesが発生し、短期間に同じ共有Skillへ複数agentが編集を重ねたため、運用者が自動writeを止めています。これは「使うほどSkillが蓄積して良くなる」という単純な正のフィードバックではなく、**量が増えるほどretrieval、token cost、conflict、stalenessという負の効果が増える**ことを示しています。

この挙動はHermes固有の偶然とも言い切れません。2026年のSkill研究では、candidate poolを5から100に増やすだけでactual-use precisionが29.6%から3.3%へ落ち、brittle assumptionsやcontext mismatchが典型的failure modeとして観測されています。つまり、「Skillライブラリが増えるほど能力が単調増加する」という前提自体が、現在の研究では支持されていません。

EnterpriseとFoundryは分ける必要があります。`hermes-foundry` **は Microsoft と共同で公開された技術PoCですが、README自身が production-ready / supported enterprise distribution ではないと明記しています。** 一方、Hermes Enterprise はNousの商用提供で、Microsoft/Nous双方の2026年11月発表によれば、Azure/Foundry、Teams、Microsoft 365 identityを利用する方向で展開されています。両者は同じアーキテクチャを共有し得ますが、OSS Foundry repoをdeployしたものをそのまま「Hermes Enterprise」と呼ぶのは誤りです。

Foundryの現行PoCにはかなりの企業導入上の宿題があります。READMEでは一括deployや完全IaC、権限revocation、dedup、signing-key rotation、telemetry、load/chaos test、SLO、rollback、mature alerting、support、SBOM、DR/state migration等が未完成とされています。またMicrosoft側のAutopilotもFrontier preview enrollment、Agent365 terms、適格なM365/Copilot系license、instanceごとのagent license seatを要求します。したがって2026年11月21日時点では、**Microsoftとの関係は公式な協業だが、Foundry repoそのものはGA済み完成製品ではない**という整理が適切です。

Hermes Enterpriseの固定価格は公開されておらず、contact-sales型です。Nousはcustomer Azure tenant内で動かせる形も説明しており、Collective Wisdomを商用価値の一つとして挙げています。公開されている導入企業一覧、seat単価、SLA値、サポート応答時間、SOC 2 / ISO 27001等の具体的な第三者認証については、今回確認した公式ページからは十分な情報を得られませんでした。したがって、これらを「Enterpriseにはある」と仮定してはいけません。

Collective Wisdomについては状況が調査期間直前に変化しています。現在の独立repoは、Skillをteam libraryへpublishし、version指定でinstall/updateする仕組みを実装しています。重要なのは、**Nousのマーケティング文にある「what one person learns spreads to the organization」というイメージに対し、実装は共有時のexact-file review、明示的Share、install/update approvalを要求する**ことです。つまり、現行の「Collective Wisdom」は無人の集合知自己進化というより、**agentが候補を推薦する、人間承認付き組織Skill Registry**に近いものです。

セキュリティでは、公式方針がかなり明確です。Nous自身が、敵対的入力を扱うLLMに対する本当の隔離境界はOS-level isolationであり、approval gate、pattern scanner、redaction、tool allowlistをcontainment boundaryとはみなしていません。terminal backendをsandbox化しても、agent process内のMCP、plugin、hook、skill loading等の全てが自動的に隔離されるわけではないと説明しています。untrusted web/email/multiuser入力を扱うなら、whole-process sandboxingが公式の安全姿勢です。

2026年にはSkill Guard injection、memory content scanning、environment sanitization、sandbox pathなど複数のCVEが公表・修正されています。またSkill metadata/description等を経由して将来の会話へ命令を残すpersistent prompt injectionのIssueもあります。したがって、**「Skillやmemoryを学習資産として永続化する」こと自体が、攻撃者にとっても永続化経路になり得る**のは理論上の話ではありません。現行v0.23.3ですべての過去PoCがそのまま成立するとは確認できないため、古い脆弱性と現行挙動は分けるべきですが、「永続記憶を持つほどtrust boundary設計が重要になる」という結論は変わりません。

## 空白の一覧と Hermes が優位になりうる領域

公開情報を調べた結果、**今から機能を順番に試す価値は低く、下表の空白を狙う方が問い1・問い2に直接答えます。**

| **公開情報で答えが出ていない問い** | **なぜ未解決と判断したか** | **問い1 / 問い2への影響** | **1台PC＋低額APIで検証** |
| :--- | :--- | :--- | :--- |
| Human-curated SkillとBackground Review Skillは、同じ実業務でどれだけ差が出るか | 一般Skill benchmarkはあるが、Hermes background reviewをA/Bした公開benchmarkがない | **Q1/Q2両方に最大級**。自動学習が手動管理より劣るなら「使うほど任せられる」は成立しにくい | **容易** |
| Skillが増えたとき、何件からtask successが下がるか | 200 Skills token/recall Issueはあるが、5/20/100/500/2000件で同一課題を反復したHermes測定なし | Q2。「経験蓄積」が能力向上から能力劣化へ反転する点が決まる | **容易** |
| Skill内の手順が古くなった際、Hermesは矛盾を検出して停止できるか | 研究ではstale/brittle Skill問題が示されるが、Hermesのfalse-positive success率は未測定 | **Q1/Q2両方**。自律運用の安全上の核心 | **容易** |
| Background Reviewが知識を一般化しすぎる原因はmodelかpromptかreview architectureか | 同様の一般研究はあるがHermesのfactorial ablationなし | Q2。review model/promptを変えれば実用化できるのか、それとも構造的問題かを決める | **可能** |
| Claude Code/Codex/Hermesで同一の非coding recurring workflowを30日回したとき、人間介入回数はどれが少ないか | 公開事例は各製品単独で、controlled longitudinal head-to-headがない | **Q1/Q2の中心** | **可能** |
| 同じモデルをHermesとCodex/Claude harnessで動かしたとき、harness差だけで品質・token・時間がどう変わるか | モデルが違う比較ばかりでharness effectを分離した公開評価がない | Q1。Hermesの価値がagent architectureなのかmodel freedomなのかを分離 | 一部可能。Claudeは同一model条件を作りにくい |
| 常駐Hermesの「削減人時 − agent運用人時」は正か | Cloudvisorも測定できていない | **Q2の最終指標** | **可能だが数週間必要** |
| cron/gatewayの無人失敗で、silent failure率はどの程度か | failure例は豊富だが母数・rateがない | Q2。「人が見なくても任せられる」の成立条件 | **可能** |
| Background Reviewが正しいSkillを誤って変更するrate | 多数writeや競合Issueはあるがtask-grounded quality measurementがない | Q2 | **容易** |
| Skillのretrieval問題を人間による小さなSkill集合、BM25/plugin、model searchのどれが最も改善するか | Issue #89844にworkaroundはあるがcontrolled outcome evalなし | Q1/Q2 | **容易** |
| Hermes→Claude Code/Codex delegationは、直接Claude Code/Codex使用より総token/latencyに見合うか | 利用談はあるがbenchmarkなし | Q1 | **容易** |
| Collective WisdomでチームのSkill qualityが時間とともに上がるか、それとも悪いSkillも伝播するか | pluginが公開されたばかりでlongitudinal事例なし | Q2、Enterprise価値の核心 | 個人環境では完全再現困難、擬似チームなら可能 |
| Hermes Enterpriseが実際に何社で本番運用され、何をSLA化しているか | 商用契約・導入企業・SLA値が非公開 | Q2のenterprise版 | **不可** |
| Foundry版の1 agent/月の実費と、同じ業務のself-hosted HermesとのTCO差 | Azure課金要素は公開されるがHermes workloadの実測値なし | Q1/Q2 | Azure preview環境があれば可能、低額とは限らない |
| Persistent prompt injectionが現行v0.23.3でSkill→memory→将来turnまでどこまで残るか | 過去PoC/CVEはあるがv0.23.3 targeted retestなし | Q2の無人運用安全性 | **可能** |

これを踏まえると、HermesがClaude Code/Codexより優位になりうる候補は、根拠の強い順に次のようになります。

**第一候補は、「モデルを固定しない、自己ホスト可能な常駐業務エージェント」です。** Hermesは同じmemory / skills / profile / gatewayを保ったまま、複数providerやローカルモデルを使える構造を持ちます。Cloudvisorが数か月の運用で実際にこの点を選定理由に挙げています。Claude CodeはClaudeモデル、CodexはOpenAI/Codex環境に強く結びついており、同じユーザー所有のagent stateを保ったまま安価なモデル・ローカルモデル・高性能モデルを仕事ごとに自由に差し替えることは両者の中心設計ではありません。

Claude Codeで近づけるには、Claude Code Skills/CLAUDE.md + Cloud Routines + Claude Tagを組み合わせます。CodexならSkills + Memories + Automations + connected appsを使います。機能の表面はかなり近づきますが、**残る差は「agent runtimeと状態を自分で所有し、vendor/modelを交換できること」**です。逆に言えば、モデル非依存性が不要なら、この差は大きな価値になりません。

**第二候補は、個人・小組織が自分のサーバーで持つ「複数チャネル共通の常駐agent」です。** HermesはTelegram、Slack、Discord、WhatsApp、Signal等を同じagent stateへ接続できます。Claude Tagは2026年11月時点ではSlack betaが中心で、CodexもSlackやcloud integrationsを持ちますが、個人が同じOSS gatewayを自分のVPSに置き、TelegramからでもDiscordからでも同じ記憶へアクセスする形はHermesのほうが自然です。

ただし、これは「Hermesだけに可能」ではありません。OpenClawにもgateway、cron、heartbeat、memory、skillsがあり、Lettaにもalways-on agentsとbackground memory processingがあります。したがって、Hermesの比較優位をClaude/Codexに対して主張できても、「常駐型agent市場全体で固有」とは言えません。

**第三候補は、長期の非coding業務で、人間が明示的に良いSkillを育てるケースです。** Cloudvisorの局所修正事例、SkillsBenchのcurated Skill効果、あなたの実測は同じ方向を向いています。規則が文章化されていない事務処理、個人の判断慣習、研究手順、定型連絡などで、正しいprocedural knowledgeを明示保存できるなら、Hermesの透明なローカルSkill資産は強い可能性があります。

ただしClaude Code/Codexにも今やSkillsがあります。Codexはinstructions/resources/scriptsをSkillとして持ち、Record & Replayで実演からSkillを作れます。Claude Codeもproject skillsとCLAUDE.md、hooksがあります。従って残る差は「Skillの存在」ではなく、**Hermesではそれを常駐agentの全チャネル・全modelで共通の長期資産として持ちやすい**ことです。

**第四候補は、安価なモデルをroutine workに使い、高価なClaude/Codexを必要時だけworkerとして呼ぶmeta-agent構成です。** 構造上は合理的で、実際にHermesからClaude Code/Codexをworkerとして使う利用例があります。しかし、この構成が直接Claude/Codexを使うより安い・速い・成功率が高いという公開測定は見つかりません。あなたの「遅くて脆い」という結果を考えると、これは現時点では優位候補というより重要な未検証仮説です。

**第五候補は、コード以外の「定刻に起きて状況を見て、必要なら処理する」仕事です。** ニュース監視・要約、サーバー管理、life adminなどの長期利用例があります。しかし2026年にはCodex AutomationsがCI failure、daily release briefs、issue triage等を定期実行し、長期threadをdays/weeks継続できます。Claude Tagもhours/daysのscheduled workとproactive follow-upを持ちます。従って、「定期実行できる」こと自体はHermesの優位ではなく、**self-hostできる、modelを選べる、メッセージ基盤を選べる**場合だけ差が残ります。

反対に、**現在の公開情報からはコーディング中心の作業でHermesがClaude Code/Codexより優れる根拠はありません**。Claude Codeは専用のcoding agent環境、subagents、hooks、cloud routinesを持ち、Codexはworktrees、parallel agents、review queue、Automations、GitHub/CI系の実運用事例を持ちます。Hermesからそれらを呼ぶことはできますが、その場合Hermesは追加のorchestration layerであり、品質上の上積みを証明しない限りlatency/token/failure surfaceを増やします。

また「Hermesだけが使うほど賢くなる」という表現も、2026年11月時点では成立しません。Claude Tagはchannel contextから継続学習的に文脈を蓄え、Codexはmemoryでpreferences/correctionsを再利用し、長期Automationsも同一threadを再開します。違うのは、Hermesが**Skillファイルそのものをagentの明示的なprocedural memoryとして自分で編集することを設計の中心にしている**点です。そして、まさにその自動編集品質が現在もっとも不確かな部分です。

## 検証する価値が高い仮説

以下の5件は、機能チェックではなく、問い1・問い2を直接反証できるように設計できます。

| **仮説** | **共通作業と評価指標** | **反証方法** | **捨てる条件** |
| :--- | :--- | :--- | :--- |
| **H1：人間が明示保存したprocedural Skillを使う反復業務では、HermesはClaude Code/Codexより「再説明なし成功率」が高くなる** | 文書にない10〜20個の慣習を必要とする同一業務を、Hermes Skill / Claude Skill・CLAUDE.md / Codex Skillで各10〜20回。成功率、再説明回数、token、wall timeを測る | 各ツールに同量・同内容のSkillを与え、model能力差をできるだけ揃える。複数sessionに分ける | Hermesの成功率がClaude/Codex以下、または差が5–10pp以内でtoken/時間が多いなら、「Hermesのprocedural memory優位」は捨てる |
| **H2：自動Background Reviewは、明示保存Skillより長期的にtask successを悪化させる** | 同じ業務を「固定Skill」「human-reviewed更新」「Hermes auto review」の3群で20〜30 iterations。具体値保持率、成功率、false-success率、Skill diff entropyを測る | 正解ruleを途中で2回変更し、どの群が最速で適応するか比較する | auto-review群がhuman-reviewed群と同等以上の成功率・具体値保持・rule-change追随を示すなら仮説を捨てる |
| **H3：Skillライブラリは一定規模を超えるとHermesの長期能力を下げ、Claude/Codexのretrieval方式より劣る** | 同じ20 taskでSkill数5/20/100/500/2000を用意。正しいSkill invocation率、pass rate、prompt tokens、latencyを各製品で測る | distractor Skillを意味的に近いもの／無関係なものに分けて原因を切り分ける | 500〜2000 SkillsでもHermesのpass rate低下がなく、cost増もClaude/Codex以下なら捨てる |
| **H4：常駐・定期業務ではHermesはClaude/Codexより安価に済むが、人間介入率は高い** | 30日相当を圧縮した定期監視タスク。入力更新→判定→必要時action→報告。API費、成功率、silent failure、人間介入回数、MTTRを比較 | 同じtrigger frequency、同じexternal data、同じacceptance criteriaを使う | Hermesがcostでも介入率でも優位なら後半を棄却。cost差が小さい/逆転するなら「安価」という前半も棄却 |
| **H5：Hermes→Claude Code/Codexのmeta-agent化は、直接Claude Code/Codexを使うより複雑なmulti-step業務でのみ価値が出る** | ①単一coding task、②非coding調査＋coding＋通知の複合taskをそれぞれ直接実行とHermes coordinator経由で比較。end-to-end success、tokens、wall time、再試行、human interventions | workerへのprompt、repo、budgetを固定し、Hermes追加layerだけを変数にする | 複合taskでも成功率向上がなく、latency/tokenが20%以上増えるなら「meta-agentとしてのHermes優位」を捨てる |

このうち最優先は **H2、H3、H4** です。H2は、Hermesの売りである「使うほど学ぶ」が実際には人間curationなしで成立するかを直接測ります。SkillsBenchと11月19日のself-evolution論文は、「curated skillは強いが、自動生成・feedbackなしrewriteは弱い」というかなり強い事前仮説を与えています。もしHermesのBackground Reviewがそれを克服しているなら、それは公開研究に対する重要な正例です。逆に克服していなければ、Hermesの「self-improving」は**自動学習というより、人がSkillを育てるための便利な永続メモリ基盤**と再定義すべきです。

H3も重要です。あなたの2000 Skills / 約5.8万tokensという測定、公開Issueの200 Skills / 約11.5K skill-index tokens、200 Skillsでのrecall低下、研究上の5→100でactual-use precision 29.6%→3.3%という結果は、すべて同じ方向を示しています。もし規模を増やすほど検索・token・選択精度が悪化するなら、Hermesの長期学習には**知識の追加ではなく、削除・統合・versioning・retrieval architectureが必要**になります。これは問い2の成立条件そのものです。

H4は「仕事のあり方が本当に変わるか」を最も直接測ります。Cloudvisorの事例が示すように、agentが仕事を肩代わりしても、その代わりに監視、recovery、approval、quality check、Skill cleanupが発生します。よって成功率だけでなく、**人間の総介入分数**を主指標にすべきです。「自律agentが100件処理した」ではなく、「その100件のために人間が何分使ったか」「何件がsilentに間違ったか」を測れば、常駐化が仕事を減らしたのか、単に別の仕事へ変えただけなのかが判定できます。

公開情報だけで現時点の問い1に答えるなら、**HermesがClaude Code/Codexを超える最有力領域は、コーディング能力ではなく、「ユーザー所有・モデル非依存・複数チャネル・長期状態を持つ常駐オーケストレーター」としての運用です。** ただしClaude TagとCodex Automations/Memoryの進化により、2026年前半に比べてこの差はかなり縮小しています。性能差として残っているかは未証明です。

公開情報だけで問い2に答えるなら、**「常駐agentに仕事を持たせる」働き方はすでに成立しているが、「自動で学び続けるほど人の確認が減る」とまでは証明されていません。** むしろ現時点の最も長いHermes運用事例、Hermes自身のIssues、2026年の独立Skill研究を合わせると、成功している形は「人が良い手順を明示・承認し、agentは反復実行する」「agentの外側に決定論的なsupervisorを置く」「自動学習は無制限に信用しない」です。完全な放置型より、**人が例外・学習・権限変更を承認する半自律型**のほうが公開証拠に合っています。

したがって、あなたが再実験すべきなのは「Hermesに何ができるか」ではありません。公開情報ですでに答えがかなり出ているのは、常駐、cron、messaging、memory、skills、subagents、model swapping、Foundry integrationといった**機能の有無**です。未解決で、かつ問い1・問い2を本当に左右するのは、**時間と経験が増えたときに、Hermesの任せられる範囲が実際に広がるのか、それともSkill肥大・staleness・自動reviewの一般化・運用負荷によって一定点から縮むのか**です。現在の公開証拠は後者のリスクをかなり強く示していますが、Hermes v0.23.3上で業務レベルのcontrolled longitudinal experimentを行った公開データはまだありません。
