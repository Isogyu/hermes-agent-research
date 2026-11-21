
# 仕事のあり方を変える可能性のある AI の道具と使い方 — 2026年11月21日時点

## 全体の地図

2026年時点の証拠を先に要約すると、**「AIが人間の作業を丸ごと引き受け、人は例外だけを見る」という世界は、一部の限定された業務では既に成立しているが、汎用的な知的労働ではまだ成立していない**。最も強い実証があるのは、①ソフトウェア開発、②顧客サポート、③定型的な文書作成・専門職支援である。一方、長時間にわたるGUI操作、完全自律型の個人秘書、自己改善する長期記憶、複雑なマルチエージェントは、製品機能の進歩に比べて「仕事が本当に変わった」という独立証拠がかなり遅れている。

### 常駐型の個人エージェント

Hermes Agent と OpenClaw は、2026年に「チャットで一回頼む道具」から最も遠くまで進んだオープン系の実装に入る。Hermes は永続メモリ、経験からのSkill生成・改善、cron、Webhook、メッセージング、隔離サブエージェント、クラウド／SSH／ローカル実行を一つのハーネスに統合し、OpenClaw は会話記録、段階的な記憶統合、prospective memoryをcronや構造化intentに変換する設計まで持っている。

ただし、**Hermes/OpenClawを数週間〜数か月使った結果、委任範囲が継続的に拡大し、人間の役割が実際に変わったことを第三者が測定した研究は見つからなかった**。特に長期記憶については、2026年のMemoraベンチマークで、複数のmemory agentが古くなった記憶を再利用し、更新情報との整合に失敗する例が多く、既存memory layerの改善も限定的だった。したがって現段階では「非常に試す価値の高い研究対象」だが、「実証済みの働き方」とは分けるべきである。

### コーディングエージェントから汎用ワークエージェントへ

Claude Code、Codex系、Qwen Codeなどは、もはやコード生成器ではなく、**shell＋ファイル＋ブラウザ＋MCP＋Skills＋subagentsという汎用的な“コンピュータ上で仕事をするハーネス”**になりつつある。Anthropic自身もClaude CodeのSkill例としてSlack、Drive、Asana、GitHubの同期や分析業務を挙げており、OpenAIも2026年には同じagent harnessの原語彙としてSkills、AGENTS.md、shell、patch、MCP、sandboxをまとめている。

ここは重要で、**2026年に起きた変化は「最高の専用エージェントを探す」より、「汎用ハーネスに手順・ツール・検証器を与える」方向への収束**である。Anthropicは専用agentを多数作る方針からSkill中心へ移行したと説明し、Agent Skills自体もオープン形式となった。

コーディングの独立測定は強いが一様ではない。Microsoft、Accenture、Fortune 100企業の計4,867人を対象とするRCTを統合した2026年のManagement Science論文では、AI coding assistant利用群で完了タスクが26.1%増えた。一方METRの2025年前半の熟練OSS開発者RCTでは19%程度遅くなり、2025年後半の追試データでは改善方向に転じたものの、参加者選択バイアスが強く、METR自身が確定的な速度向上の推定を撤回している。

### 企業エージェント基盤と業務自動化

Microsoft Agent 365、Google Gemini Enterprise Agent Platform、ServiceNow、Salesforce Agentforce、OpenAI、Anthropicはいずれも、2026年には「agentを作る」より**identity、permissions、audit、runtime、memory、approval、governanceをどう管理するか**へ競争軸を移した。MicrosoftはAgent 365をagentの中央control planeとしてEntra identityと統合し、GoogleはAgent PlatformでADK、A2A、MCP、長期Memory Bankを統合、ServiceNowもagentの権限を実行時に制御するAI Passportを発表している。

これは宣伝だけではない変化の兆候もある。McKinseyの2026年調査では、年商10億ドル超の企業の40%がAI agentsをscaleしていると回答し、32%の回答者がagentic codingによって購入予定だったソフトウェア／機能を内製に切り替えた経験を報告した。ただしDeloitteの501人の経営層調査では、agent向けに業務プロセスが「高度に準備済み」と答えた企業は5%、部門横断multi-agentをscaleしたのは15%にすぎない。これは**モデル能力より業務設計・権限・データ・監督の不足がボトルネック**であることと整合する。

n8n、Zapier、Make系は、LLMに全手順を考えさせるより、**決定論的workflowを骨格にして、曖昧な判断だけLLMへ渡す**用途で実務性が高い。n8nの事例ではFlow AIが数時間の不動産アウトリーチを60秒未満へ縮めているが、これは提供元事例なので「導入組織の主張」であり独立証拠とは数えない。一方、Salesforce Agentforceでも確率的agentだけでは不安定だったため、Agent Scriptという決定論的層を追加したという報道があり、この方向性は複数製品に共通している。

### コンピュータ操作、マルチエージェント、記憶

GUI／ブラウザ操作は、「APIがない仕事をAIに任せる」という意味で潜在的インパクトは巨大だが、**現在の自律性を最も過大評価しやすい領域**でもある。OSWorld 2.0は人間なら中央値約1.6時間の108業務を評価し、最良構成でも完全成功率20.6%。Odysseysの200件の長時間web taskでも最強agentの成功率は44.5%だった。

さらに2026年9月のTraverse研究は2,518件の長時間agent trajectoryから6,967件の誤りを人手分類し、最初のミスをagent自身が発見・回復できないケースが多く、最終的に成功判定されたrunでもデータ削除、システム破損、成功の捏造があったと報告した。したがって現時点の実務パターンは「agentに任せて忘れる」ではなく、**sandbox＋権限制限＋checkpoint＋機械的な検証器＋例外時の人間handoff**である。

マルチエージェントも同様で、OpenAI、Google、Claude、Hermesなどに実装は揃ったが、「1 agentより組織的に良い」という独立した長期業務測定はまだ薄い。多数のagentを走らせることそのものより、独立した検証、context分離、並列探索に意味がある場合に有効、という位置づけが2026年時点では妥当である。

### 標準化、ローカルモデル、そして「道具ではない変化」

MCPは2026年には単なるAnthropicの規格ではなくなった。Linux Foundation傘下のAgentic AI Foundationへ寄贈され、OpenAI、Google、Microsoft、AWS等が支援し、2026-07-28仕様ではstateless core、長時間Task extension、enterprise authなどが追加された。A2AもLinux Foundation管理下でv1.0となり、150超の組織が参加している。

これらは直接生産性を高める道具ではないが、**agentとモデルを入れ替えてもtool/Skillを再利用できること**が長期的には大きい。Agent SkillsもAnthropic起源からvendor-neutralな仕様へ動いているため、2026年末時点で最も過小評価されている変化の一つは「モデル」ではなく、AGENTS.md／SKILL.md／MCP／A2Aといった**業務手順と接続面の可搬化**である。

ローカルモデルも「最高性能の代替」より、**大量に回す安価なworker tier**として意味が出ている。Qwen CodeはローカルOllama/vLLM、subagents、memory、skills、MCPをサポートし、Qwen3.6-27Bは提供元評価ながらagentic codingで大規模モデルにかなり接近している。一方、個人の実測では公称benchmarkと実agent loop性能が大きく乖離するケースも報告されており、ローカルモデルは自分のworkflowで実測すべきである。

## 候補の評価表

以下の「証拠」は**提供元ページだけの場合は明示的に主張扱い**とした。

| **候補** | **分類** | **変わると主張されていること** | **実際に変わった証拠** | **うまくいかなかった証拠** | **成熟度** | **個人で試せるか** | **出典URL** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Claude Code / 汎用coding harness | コーディング→全業務 | 実行作業から仕様・レビューへ人を移す | **独立した測定**: coding assistant RCT 4,867人で完了タスク+26.1%。製品そのものと完全同一ではないがagentic codingの基礎証拠は強い。 | **独立した測定**: 熟練OSS開発者では2025年前半に約19% slowdown。 | 広く実用 | ◎。既に利用中なら非コードworkflowを試す価値大 | [Management Science](https://doi.org/10.1287/mnsc.2025.00535), [METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) |
| Codex / ChatGPT Work型 | 汎用work agent | files/apps/webを跨ぐ仕事を完遂、定期実行 | **提供元の主張**: Workはconnected apps、files、browser、scheduled tasksを扱い、OpenAIは100万超がcoding外でCodex系を使用と説明。 | 独立した長期測定は未発見 | GA/展開中 | ○〜◎、プラン依存 | [OpenAI release notes](https://help.openai.com/en/articles/11391654-chatgpt-team-release-notes) |
| Hermes Agent | 常駐個人agent | memory、skills、cron、chat gatewayで使うほど任せられる | **提供元の主張**: memory→Skill化→再利用のclosed loop、cron、subagents。 | **独立した測定**: Hermes固有の長期効果は未発見。一般的memory agentは古い記憶処理に弱い。 | 活発なOSS、実験〜実用 | ◎ | [GitHub](https://github.com/NousResearch/hermes-agent) |
| OpenClaw | 常駐個人agent | 会話・意図・記憶を継続管理 | **提供元の主張**: memory flush、dreaming、cron、structured intents。 | 長期独立測定なし。memory benchmark一般では更新失敗。 | OSS、実験〜実用 | ◎ | [GitHub docs](https://github.com/openclaw/openclaw) |
| n8n + LLM | automation＋agent | AI判断を既存workflowの中に埋める | **導入組織の報告（数字つき）**: Flow AIで3–5時間→60秒未満。ただしn8n掲載事例。 | 汎用agent部分はidentity/reliability等に追加実装が必要という実運用報告もある。 | 広く実用 | ◎、self-host可能 | [n8n case](https://n8n.io/case-studies/flow-ai/) |
| Zapier + MCP/agents | automation＋agent | agentを多数SaaSの実行層につなぐ | **導入組織の報告（数字つき）**: Mach 1は25社を小規模チームで支え、内部Gmail接続9,552 tasks/90日。提供元掲載。 | 独立比較研究なし | 実用 | ○、無料/低額枠から可能 | [Zapier case](https://zapier.com/blog/Mach-1-MCP/) |
| Salesforce Agentforce | enterprise agents | support/salesの一次処理をagentへ | **導入組織の報告（数字つき）**: Salesforce自身では2.6M会話、63%解決、support人員再配置。ただし自社主張。ReutersはCEOによるsupport headcount削減発言を報道。 | **独立報道**: 非決定的agentがproductionで同じ状況に異なる経路を選ぶ問題が報告され、deterministic Script導入へ。 | 広く提供 | △ | [Reuters](https://www.reuters.com/business/world-at-work/salesforce-cuts-less-than-1000-jobs-business-insider-reports-2026-02-10/) |
| Microsoft Agent 365 + Copilot Studio/Foundry | enterprise基盤 | agentを人と同じidentity/governance対象にする | **提供元の主張**: Entra Agent ID、Conditional Access、central governance、自律trigger。 | 独立したproductivity測定は未発見 | control planeは実用、機能ごとにpreview混在 | △ | [Microsoft Learn](https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-agent-365/microsoft-agent-365) |
| Google Gemini Enterprise Agent Platform | enterprise基盤 | persistent agents、memory、A2A/MCPを企業全体へ | **提供元の主張**: long-running agents、Memory Bank、ADK、A2A/MCP。 | 独立した働き方変化の測定は未発見 | GA/preview混在 | △ | [Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/the-new-gemini-enterprise-one-platform-for-agent-development) |
| ServiceNow Arc / Autonomous Workforce | enterprise基盤 | 長時間agentにend-to-end process ownership | **提供元の主張**: Arcは2026-10 GA、minutes-to-daysの仕事を自律継続。 | 独立的な長期間測定は未発見 | GAだが新しい | ×〜△ | [ServiceNow](https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-delivers-industry-first-personal-enterprise-agent-and-policy-enforcement-with-NVIDIA-extending-AI-governance-across-software-and-silicon/default.aspx) |
| Computer/browser-use agents | GUI操作 | APIなしシステムもagentに任せる | **独立した測定**: real-world long-horizon benchmarkで一定の能力。 | **独立した測定**: OSWorld2完全成功20.6%、Odysseys 44.5%。長時間ではhidden failure多発。 | 実用初期 | ◎、sandbox推奨 | [OSWorld2](https://arxiv.org/abs/2606.29537) |
| Customer-support AI | 業務agent/assistant | L1処理をAI、人は例外対応 | **独立した測定**: 5,172人でissues/hour +15%。Alibaba field experimentでも速度・主観品質改善。 | 熟練者では改善小、品質悪化例。Klarnaも複雑案件でhumanへ戻す運用。 | 最も成熟 | 個人検証○ | [QJE](https://doi.org/10.1093/qje/qjae044) |
| 法務drafting AI | 専門業務 | juniorの作業からreview中心へ | **独立した測定**: 3か月RCT、11法律事務所133人でdraft品質+0.38SD。 | juniorではAI無しでの後続能力向上が平均的に確認されず、trainingの有無で逆効果例もある。 | 実用 | ○ | [NBER](https://www.nber.org/papers/w35720) |
| AI medical scribes | 文書/事務 | 医師を記録作業から診療へ戻す | **独立した測定**: 5医療機関でdocumentation時間-10%、visit volume +1.7%。別RCTでも時間削減。 | **独立した測定**: 一RCTでmedical errors 19件対従来9件。 | 実用 | △、個人用途ではない | [JAMA](https://jamanetwork.com/journals/jama/fullarticle/2847319) |
| MCP | 接続標準 | model/agentを変えてもtoolsを再利用 | 実利用規模は非常に大きく、2026-07-28に長時間Tasks等が標準化。 | 生産性そのもののRCTなし。security/permission設計は別途必要 | 標準として成熟中 | ◎ | [MCP](https://blog.modelcontextprotocol.io/posts/2026-07-28/) |
| A2A | agent間標準 | 異なるagent/vendor間で委任 | **提供組織の報告**: v1.0、150超の組織、cloud統合。 | 「multi-agentにしたから生産性向上」の独立証拠は薄い | 標準成熟初期 | ○ | [A2A](https://a2a-protocol.org/v1.0.0/) |
| Agent Skills / SKILL.md | 手順の標準化 | 組織知をモデルから切り離してportableにする | Google、Anthropic、OpenAI等が共通仕様へ参加。 | packaging/discovery/versioningはまだ未標準化。 | 急速に成熟中 | ◎ | [Agent Skills](https://github.com/agentskills/agentskills) |
| ローカル小型/中型モデル | 低コスト・機密 | always-on workerを低コストで大量実行 | **提供元の測定**: Qwen3.6-27B等でagentic benchmarkが大幅改善。 | **個人の実測**では公開benchmarkと実agent-loop結果が大きく乖離した例。 | 実用だがhardware依存 | ◎ | [Qwen](https://qwen.ai/blog?id=qwen3.6-27b) |

## 証拠の強さによる順位

ここでは「将来性」ではなく、**既に働き方が変わったことを裏付ける証拠 × 今後さらに広がる可能性**で順位を付けた。

| **順位** | **領域 / 仕組み** | **評価理由** | **この評価が外れる条件** |
| :--- | :--- | :--- | :--- |
| **1** | 顧客サポートのAI＋human escalation | 数千人規模の独立field studyで+15%、2026年Alibaba RCTでも速度・品質改善。新人ほど効果大で、人が複雑案件へ移るという**役割変更**まで最も明確。 | 長期運用で品質低下・顧客離反・監督コストが利益を消す場合 |
| **2** | coding agent＋human review | 4,867人RCTで+26.1%。企業がsoftware購入をやめ内製する例まで出ており、「できる範囲」の変化が始まっている。 | review bottleneck、technical debt、熟練者 slowdownが支配的になる場合 |
| **3** | 専門文書の「AI first draft → expert review」 | 特許弁護士3か月RCTで品質向上が90日後も継続。短時間toy experimentではない点が強い。 | AI依存でjuniorの技能形成が阻害される場合 |
| **4** | 決定論workflow＋LLM判断 | n8n/Zapier等の実運用で既に小規模チームが大量処理。agent単体より失敗箇所を限定できる。提供元事例中心なので順位は抑えた。 | 維持管理・例外処理コストが人力と変わらなくなる場合 |
| **5** | AI scribe / ambient documentation | 独立した多施設研究とRCTがあり、専門家を記録作業から本来業務へ戻す証拠がある。 | 誤記録の検証コストや責任問題が時間削減を相殺する場合 |
| **6** | Skills＋agent harness | 「モデルへ毎回説明」から「業務手順をversion-controlして委任」への役割変更を可能にする。直接RCTはないため6位。 | Skill transferabilityがモデルごとに崩れる場合 |
| **7** | MCP | 仕事そのものではなくagent化のtransaction costを下げる。主要vendor横断で標準化が進んでいる。 | permission/security問題でenterprise adoptionが止まる場合 |
| **8** | 常駐agent＋scheduler＋memory | Hermes/OpenClaw等に必要部品はほぼ揃った。**ユーザーが求める「任せ続ける働き方」に最も近いが、長期独立証拠がないため順位を下げた。** | 記憶・誤作動・維持管理が改善せず、人間が毎回監視する必要が残る場合 |
| **9** | computer-use agents | API非対応softwareを横断できるため潜在市場は大きいが、長時間成功率20〜45%程度という現状ではhuman-in-the-loopが必須。 | 次世代agentでlong-horizon成功率が80〜90%へ急上昇すれば順位は一気に上がる |
| **10** | A2A / multi-agent | 異なる組織・vendorのagentを組み合わせる基盤としては急速に成熟。だが「複数にした方が仕事が良くなる」証拠が未成熟。 | production dataでsingle-agentより費用対効果が明確になれば上昇 |

この順位から見える最大のポイントは、**最も強い証拠は「agentが完全自律化した領域」ではなく、「AIが一次処理を行い、人間が難しいものだけ見るようになった領域」**に集中していることである。これはcustomer support、coding、法務、医療記録で共通している。

生産性研究全体も「平均的にはプラス、しかしtask/userごとの分散が非常に大きい」という結論に近い。BCGの758人実験ではAI適合タスクで25.1%高速化・12.2%多くのタスクを完了した一方、能力境界外の課題では正答率が19%低下した。法律学生の2026年RCTでも、LLMを渡すだけの群はむしろ悪化傾向だったが短いtrainingを入れると成績が有意に改善した。つまり**tool accessより「いつ、どう使うか」の設計が効く**という独立証拠がある。

マクロではまだ「AIで生産性革命が統計に明確に出た」とは言えない。OECDは2026年時点でもmicro-levelの効果に比べ、公式統計からeconomy-wideなAI productivity gainを識別するのは難しいとしている。米国の全国代表調査では2026年8月に就業者の40.5%が仕事でGenAIを使っていたが、GenAIによる自己申告の時間節約は全労働時間の約2.1%だった。

一方で「影響なし」とも言えない。ADPの数百万人規模給与データではeconomy-wideの大規模な雇用消失はまだ見えないが、AI exposureの高い職種の22〜25歳雇用は低exposure職種との比較で19%下振れしている。別の2026年行政データ研究はAI exposure増加とoutput増加を関連付けているが、因果識別にはなお議論の余地がある。

## 働き方の型

**「AIに全部やらせる」より、「AIが作業面を占有し、人間が境界条件を占有する」型が強い。** 2026年までの実証から、再現性が高い型は次のように整理できる。

| **働き方の型** | **実例** | **成り立つ条件** |
| :--- | :--- | :--- |
| **AI一次処理 → 人間は例外だけ扱う** | customer supportでAIがroutine queryを処理、新人のissues/hourが特に改善。 | high-volume、正解パターンがある、human escalationが明確 |
| **夜間/定期実行 → 朝に人間が検収** | Hermes/OpenClaw/Workのcron・scheduled taskがこの構造を直接サポート。実証はまだproduct-level。 | input取得が自動、outputに明確なchecklist、失敗しても可逆 |
| **手順をSkill化してから委任** | Claude Code / Agent Skills。個人のprompt memoryではなくrepositoryに手順を置く。 | SOPが文章化可能、acceptance criteriaがある、version control |
| **probabilistic判断をdeterministic workflowで囲む** | Agentforce Script、n8n、Zapier型。 | 分岐・権限・書込みはコード側、LLMは分類・生成・例外判断 |
| **生成と検証を分離する** | codingならtests/CI、研究ならsource verification、長時間agentなら別verifier。Traverseは自己検証だけでは弱いことを示す。 | verifierが生成agentから独立、pass/failが機械的に判定可能 |
| **juniorの実行量をAIで引き上げ、seniorをreviewerにする** | coding、customer support、特許draftingで低経験者の効果が大きい。 | senior review capacity、教育設計、AI出力を鵜呑みにしないtraining |
| **小型modelをworker、大型modelをjudge/escalationにする** | 2026年のcost managementではsmaller/distilled modelやroutingの採用が広がっている。 | task分類、fallback、cost/quality logging |
| **接続面と手順をmodelから独立させる** | MCP＋Agent Skills＋A2A。 | provider固有機能に依存しすぎない設計 |

この中で特に重要なのは**仕様化→委任→機械検証→例外対応**という四段構成である。AIの性能差そのものより、問題をこの形へ変換できるかが成果を左右しているという証拠は複数ある。BCG実験では同じAIでもtask frontierの内外で効果が正負逆転し、法律学生実験では短いtrainingが成績差を反転させ、Agentforceのproduction報告でも確率的自然言語指示だけでは足りずdeterministic controlが追加された。

「使うほど任せられる範囲が広がる」については、**部分的には成立しているが、一般形ではまだ実証されていない**。成立している最も近い例は、人間が失敗を見てSOP/Skill/workflowを更新し、その結果次回からそのパターンを自動処理できるという意味での「組織的学習」である。モデル自身が経験から安全に能力を自己拡張するというHermes的な強い意味でのself-improvementについて、数か月単位の独立実証は確認できなかった。

## 個人が次に試す価値のあるもの

あなたは既にClaude Code、Codex CLI、Hermesを使っているので、「別のチャットAIを触る」より、**委任の仕方そのものを比較する実験**の方が得られる情報量が大きい。

| **実験** | **確かめること** | **実施方法** | **「使える」の基準** | **「使えない」の基準** | **Claude Code / Codexだけで代替可能か** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hermesを7〜14日常駐させる** | memory＋cron＋self-created skillsが本当に委任範囲を広げるか | 毎朝「AI/ITニュース5件→根拠確認→Markdown報告」、週次で過去報告から重複排除。人が修正したルールをmemory/Skillへ残す | 2週目の人間修正時間が1週目比50%以上減り、重大誤り0〜1件 | 修正量が減らない、古いmemoryを繰り返す、scheduler管理が作業になる | **部分代替可**。cron＋Skill＋scriptを組めば可能。ただし「memory→自律Skill化」の比較こそHermesを試す意味 |
| **“AI社員の受信箱”を作る** | push型仕事がpull型chatより働き方を変えるか | Telegram/Slack→Hermesまたはdaemon→task queue。URL、メモ、調査依頼を投げ、夜間に処理 | 自分がPCを開かずに投入した仕事の70%以上が翌朝review-ready | 依頼ごとに追加指示が必要なら単なるremote chat | Claude Code/Codex単体ではやや弱い。scheduler/webhookを外付けすれば再現可能 |
| **Skill-first vs prompt-first A/B test** | toolより業務設計の方が重要か | 同一10タスクを①毎回自然言語、②SKILL.md＋checklist＋verification scriptで実行 | Skill群で再作業時間または失敗率が30%以上低下 | 差がほぼない | **完全に可能**。むしろClaude Code/Codexで行う価値が高い |
| **n8nをagentの“外骨格”にする** | LLM単体よりdeterministic workflow＋LLMの方が放置できるか | RSS/mail→filter→LLM分類→source fetch→report→通知。LLMには判断部分だけ担当させる | 30回以上連続運転し、手動介入率<10%、誤書込み0 | workflow保守時間が節約時間を超える | **機能上は可能**だが、daemon/retries/state/auditを自作する必要があり、そこが比較点 |
| **local worker＋frontier reviewer** | 月額を増やさずalways-on化できるか | Ollama等＋Qwen系を分類・要約・整形workerにし、曖昧なものだけClaude/Codexへescape | frontier API callを50%以上削減しつつ品質低下<5% | localの誤り検査・待ち時間がコスト削減以上 | Claude Code/Codexだけでは「低コスト常時worker」という目的は代替しにくい |

この5件で最優先なのは**Skill-first A/B test**である。2026年の研究とproduction事例を横断すると、「どのモデルか」より「正しいinput、明示的手順、機械的検証、human escalation」が成果を左右する事例が非常に多いからである。

次点は**Hermesの長期実験**である。理由は逆で、これは現在最も大きな「未検証領域」だからだ。単発タスクの品質ではなく、毎日の訂正が1週間後の自律性を本当に上げるかを測れば、HermesとClaude Code/Codexとの差を直接検証できる。Hermes自身はclosed learning loopを主張しているが、その主張を独立に裏付ける長期研究は現状見つからない。

なお「月数千円」の条件では、企業向けAgent 365、ServiceNow、Salesforceを直接試す優先度は低い。個人が学ぶべき本質部分――Skill、MCP、scheduler、state、approval、audit、workflow、local routing――は、Hermes/OpenClaw/n8n/Claude Code/Codex/Qwen等の組み合わせでかなり再現できる。

## 分からなかったこと

調査した範囲では、以下は**2026年11月21日時点でも十分な独立証拠が見つからなかった**。

- **Hermes AgentやOpenClawを数か月以上使った利用者について、「memoryが蓄積した結果、最初より何%多くの仕事を無監督で任せられるようになった」と測定した研究。** 製品機能は確認できるが、longitudinal evidenceがない。
- **汎用personal agentがメール・カレンダー・browser・filesを継続的に管理し、人間が本当に例外だけを見る状態を、第三者が長期間測定した例。** 近いvendor case studyはあるが、独立検証ではない。
- **multi-agentが同じtoken budgetのsingle-agentより実際の企業業務で高ROIになるという長期間の独立比較。** A2Aや各種frameworkのproduction readinessは進んだが、経済的優位の証拠は不足している。
- **agent memoryが人間の組織知のように安全に自己更新すること。** 2026年の長期memory benchmarkはむしろobsolete memoryの再利用や更新不整合を示している。
- **GUI agentを完全無監督で数時間走らせても、企業業務として許容できる信頼性になること。** 最新long-horizon benchmarkではまだ成功率が低く、hidden failureも多い。
- **特定のenterprise agent platformが他社製品より組織変革を生むという独立比較。** Microsoft、Google、Salesforce、ServiceNow、OpenAI、Anthropicはいずれも高度な基盤を持つが、横並びの独立production studyは確認できなかった。
- **AI agentsによるeconomy-wide productivity revolutionが既に公式統計に明確に現れていること。** micro-levelでは多くのプラス効果があるが、OECDは2026年にもaggregate statisticsで明確に識別することは難しいとしている。

したがって、2026年11月時点の最も支持しやすい結論は、**「AI社員」が既に完成した、ではない。仕事を“AIが実行し、人間が仕様・検証・例外処理を担当できる形”に再設計した組織・個人から、働き方が先に変わっている**、である。独立実証が強いcustomer support、coding、法務、医療文書はいずれもこの構造を共有しており、反対に完全自律agent、長期memory、GUI操作、multi-agentほど製品能力に対して実証が追いついていない。

今後1〜2年で最も重要なのは、単にモデルが賢くなることより、**①Skillsで手順を形式知化する、②MCPで実行面を標準化する、③scheduler/event triggerで人間の呼び出しを不要にする、④機械的verifierとhuman escalationを標準装備する、⑤cheap/local workerとfrontier modelをroutingする**という5つの層が一体化することだと考える。これは一部が推測だが、2026年の標準化・製品設計・独立研究が同じ方向を示している。
