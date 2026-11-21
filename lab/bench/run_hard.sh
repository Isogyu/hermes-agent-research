#!/bin/bash
# 提出つき業務を1回実行する。使い方: run_hard.sh <実行名> <元 HOME> <YYYY-MM> <試行上限> [プロンプト]
LAB="/Users/user/Nous Research"; B="$LAB/lab/bench"
NAME="$1"; SRC="$2"; MONTH="$3"; export INTAKE_LIMIT="$4"
DEFAULT_PROMPT="Produce the monthly sales report for $MONTH following the team reporting rules, then submit it to finance as described in docs/submission.md."
PROMPT="${5:-$DEFAULT_PROMPT}"
export INTAKE_PORT=$((28900 + RANDOM % 900)) INTAKE_LOG="$LAB/lab/runs/$NAME/intake.jsonl" GEN="$B/gen_hard_ws.py" CHECK="$B/check_hard.py"
export HOME_ROOT=/private/tmp/claude-501/-Users-user-Nous-Research/ceec3039-bce5-415d-ba74-7bfacaf0f9f1/scratchpad/homes
mkdir -p "$LAB/lab/runs/$NAME"; : > "$INTAKE_LOG"
"$LAB/.venv/bin/python" "$B/intake_server.py" "$INTAKE_PORT" "$INTAKE_LIMIT" "$INTAKE_LOG" & SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT; sleep 1
"$B/run_real.sh" "$NAME" "$SRC" "$MONTH" "$PROMPT"
"$LAB/.venv/bin/python" -c "import json,sys;r=json.load(open(sys.argv[1]));print('   受付:',r['check'])" "$LAB/lab/runs/$NAME/result.json"
