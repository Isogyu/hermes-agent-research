#!/bin/bash
# ゲートウェイの API サーバー経由で1依頼を流す。
# 使い方: run_gateway.sh <実行名> <HERMES_HOME> <台本> <プロンプト>   （環境変数 AUX_TEXT, POST_WAIT）
set -u
LAB="/Users/user/Nous Research"
NAME="$1"; H="$2"; SCRIPT="$3"; PROMPT="$4"
OUT="$LAB/lab/runs/$NAME"; rm -rf "$OUT"; mkdir -p "$OUT/cwd" "$H"
[ -f "$H/config.yaml" ] || cp "$LAB/lab/homes/hgw/config.yaml" "$H/"
"$LAB/.venv/bin/python" "$LAB/lab/mock/mock_llm.py" --port 28765 --log "$OUT/requests.jsonl" --script "$SCRIPT" --aux-text "${AUX_TEXT:-OK}" & MOCK=$!
( cd "$OUT/cwd" && HERMES_HOME="$H" API_SERVER_KEY=labkey-local-only nohup "$LAB/.venv/bin/hermes" gateway run --quiet > "$OUT/gateway.out" 2>&1 ) &
for i in $(seq 1 90); do curl -s -o /dev/null -H "Authorization: Bearer labkey-local-only" http://127.0.0.1:28642/v1/health && break; sleep 1; done
"$LAB/.venv/bin/python" -c 'import json,sys;print(json.dumps({"model":"hermes-agent","messages":[{"role":"user","content":sys.argv[1]}]}))' "$PROMPT" > "$OUT/body.json"
curl -s -m 180 -H "Authorization: Bearer labkey-local-only" -H "Content-Type: application/json" http://127.0.0.1:28642/v1/chat/completions -d @"$OUT/body.json" > "$OUT/response.json"
sleep "${POST_WAIT:-5}"
pkill -f 'hermes_cli.*gateway run|hermes gateway run'; kill $MOCK 2>/dev/null; sleep 1
