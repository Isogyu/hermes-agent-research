# EV05 提出つき業務（暗黙知）と自動振り返りの結果（2026-11-21）

| 実行 | モデル | 条件 | 合格 | 提出回数 | 受付の応答 | 呼び出し | 入力 | 秒 |
|---|---|---|---|---|---|---|---|---|
| h1-c0-1 | gpt-6-luna | Skill なし | × | 3 | E11 → E23 → E31 | 12 | 194,182 | 57 |
| h1-c0-2 | gpt-6-luna | Skill なし | × | 3 | E11 → E23 → E31 | 10 | 158,928 | 49 |
| h1-c0-3 | gpt-6-luna | Skill なし | × | 3 | E11 → E23 → E31 | 13 | 257,592 | 54 |
| h4-explicit-1 | gpt-6-luna | 明示的に保存させた Skill | ○ | 2 | E42 → ACCEPTED | 9 | 135,869 | 59 |
| h4-explicit-2 | gpt-6-luna | 明示的に保存させた Skill | ○ | 2 | E42 → ACCEPTED | 7 | 111,936 | 44 |
| h4-explicit-3 | gpt-6-luna | 明示的に保存させた Skill | ○ | 1 | ACCEPTED | 6 | 92,361 | 29 |
| h4-auto-1 | gpt-6-luna | 自動振り返りの Skill | × | 3 | E11 → E23 → E31 | 11 | 181,509 | 54 |
| h4-auto-2 | gpt-6-luna | 自動振り返りの Skill | × | 3 | E11 → E23 → E31 | 11 | 178,050 | 54 |
| h4-auto-3 | gpt-6-luna | 自動振り返りの Skill | × | 3 | E11 → E23 → E31 | 11 | 180,627 | 69 |
| o2-orr-hard-c0 | nemotron-3-ultra:free | Skill なし | × | 4 | E11 → E23 → E31 → LOCKED | 14 | 216,428 | 91 |
| o2-orr-hard-explicit | nemotron-3-ultra:free | 明示的に保存させた Skill（luna 作） | ○ | 2 | E42 → ACCEPTED | 9 | 131,419 | 68 |

## 月次レポート業務の追加条件

| 実行 | モデル | 条件 | 得点 | 呼び出し | 入力 | 秒 |
|---|---|---|---|---|---|---|
| k6-c1auto-1 | gpt-6-luna | 自動振り返りの Skill（しきい値5） | 6/6 | 10 | 151,454 | 42 |
| k6-c1auto-2 | gpt-6-luna | 自動振り返りの Skill（しきい値5） | 6/6 | 7 | 101,682 | 33 |
| k6-c1auto-3 | gpt-6-luna | 自動振り返りの Skill（しきい値5） | 6/6 | 9 | 135,175 | 35 |
| o1-orr-c0 | nemotron-3-ultra:free | Skill なし | 6/6 | 6 | 84,787 | 50 |
| o1-orr-c1s | nemotron-3-ultra:free | スクリプトつき Skill（luna 作） | 6/6 | 7 | 80,560 | 31 |

## 訓練（試行上限20回）

- h2-train-explicit: 6回目の提出で受理。Skill に5つの慣習すべてが記載された（`research/evidence/skills/hard-explicit-skill`）。
- h3-train-auto、h5-train-auto2: どちらも6回目で受理。自動振り返りは Skill を書いたが、5つの慣習の記載は0件（`hard-auto-review-skill`、`hard-auto-review-skill-2`）。メモリへの書き込みもなし。
