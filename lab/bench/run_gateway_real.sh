#!/bin/bash
# 実モデルでゲートウェイの API サーバーに1依頼を流し、ターン後の自動振り返りの完了を待つ。
# 使い方: run_gateway_real.sh <実行名> <元の HERMES_HOME> <YYYY-MM> <プロンプト>   （環境変数 EXTRA_CFG で設定を追記）
set -u
LAB="/Users/user/Nous Research"; B="$LAB/lab/bench"
SP=/private/tmp/claude-501/-Users-user-Nous-Research/ceec3039-bce5-415d-ba74-7bfacaf0f9f1/scratchpad
NAME="$1"; SRC="$2"; MONTH="$3"; PROMPT="$4"
OUT="$LAB/lab/runs/$NAME"; H="$SP/homes/gw-$NAME"; ISO="$SP/iso/$NAME/salesops"
mkdir -p "$OUT" "$H" "$ISO"
rsync -a --exclude 'gateway.*' --exclude logs --exclude 'state.db*' --exclude sessions "$SRC/" "$H/"
"$LAB/.venv/bin/python" "${GEN:-$B/gen_workspace.py}" "$ISO" "$MONTH"
cat >> "$H/config.yaml" <<CFG
platforms:
  api_server:
    enabled: true
    extra:
      host: "127.0.0.1"
      port: 28642
${EXTRA_CFG:-}
CFG
sed -i '' "s|  cwd: \".\"|  cwd: \"$ISO\"|" "$H/config.yaml"
( cd "$ISO" && HERMES_HOME="$H" API_SERVER_KEY=labkey-local-only nohup "$LAB/.venv/bin/hermes" gateway run --quiet > "$OUT/gateway.out" 2>&1 ) &
for i in $(seq 1 90); do curl -s -o /dev/null -H "Authorization: Bearer labkey-local-only" http://127.0.0.1:28642/v1/health && break; sleep 1; done
"$LAB/.venv/bin/python" -c 'import json,sys;print(json.dumps({"model":"hermes-agent","messages":[{"role":"user","content":sys.argv[1]}]}))' "$PROMPT" > "$OUT/body.json"
S=$(date +%s)
curl -s -m 900 -H "Authorization: Bearer labkey-local-only" -H "Content-Type: application/json" http://127.0.0.1:28642/v1/chat/completions -d @"$OUT/body.json" > "$OUT/response.json"
echo "turn_seconds=$(( $(date +%s) - S ))" > "$OUT/time.txt"
# 振り返りの完了を最大 WAIT_REVIEW 秒待つ
for i in $(seq 1 "${WAIT_REVIEW:-240}"); do grep -q 'Background review complete' "$H/logs/agent.log" 2>/dev/null && break; sleep 1; done
echo "review_wait=$i" >> "$OUT/time.txt"
kill "$("$LAB/.venv/bin/python" -c "import json,sys;print(json.load(open(sys.argv[1]))['pid'])" "$H/gateway.pid" 2>/dev/null)" 2>/dev/null; sleep 2
mkdir -p "$OUT/ws"; rsync -a "$ISO/" "$OUT/ws/"
grep -E 'Background review complete|Turn ended' "$H/logs/agent.log" | sed -E 's/^([0-9-]+ [0-9:,]+).*(Background review complete.*|Turn ended: reason=[^ ]+ .*api_calls=[0-9/]+).*/\1 \2/' | cut -c1-220 > "$OUT/review.txt"
cat "$OUT/time.txt" "$OUT/review.txt"; "$LAB/.venv/bin/python" "${CHECK:-$B/check.py}" "$ISO" "$MONTH"
echo "HOME=$H"
