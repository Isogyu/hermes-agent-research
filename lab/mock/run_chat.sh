#!/bin/bash
# 偽 LLM を相手に Hermes を1回実行し、送られたリクエストを記録する。
# 使い方: run.sh <実行名> <HERMES_HOME> <台本.json または -> <プロンプト> [hermes の追加引数...]
# 出力:   lab/runs/<実行名>/{requests.jsonl,usage.json,stdout.txt,time.txt}
set -u
LAB="/Users/user/Nous Research"
NAME="$1"; HOME_DIR="$2"; SCRIPT="$3"; PROMPT="$4"; shift 4
OUT="$LAB/lab/runs/$NAME"; rm -rf "$OUT"; mkdir -p "$OUT/cwd" "$HOME_DIR"
PORT=$((20000 + RANDOM % 20000))
ARGS=(--port "$PORT" --log "$OUT/requests.jsonl" --aux-text "${AUX_TEXT:-OK}")
[ "$SCRIPT" != "-" ] && ARGS+=(--script "$SCRIPT")
"$LAB/.venv/bin/python" "$LAB/lab/mock/mock_llm.py" "${ARGS[@]}" &
MOCK=$!
trap 'kill $MOCK 2>/dev/null' EXIT
sleep 1
if [ ! -f "$HOME_DIR/config.yaml" ]; then
cat > "$HOME_DIR/config.yaml" <<EOF
model:
  default: "mock-model"
  provider: "custom"
  base_url: "http://127.0.0.1:$PORT/v1"
  api_key: "mock"
  context_length: 200000
EOF
else
  sed -i '' -E "s#http://127.0.0.1:[0-9]+/v1#http://127.0.0.1:$PORT/v1#" "$HOME_DIR/config.yaml"
fi
cd "$OUT/cwd"
START=$(date +%s)
HERMES_HOME="$HOME_DIR" "$LAB/.venv/bin/hermes" chat -Q -q "$PROMPT" --format stream-json "$@" > "$OUT/stdout.txt" 2>&1
echo "exit=$? seconds=$(( $(date +%s) - START ))" > "$OUT/time.txt"
# 後から来る補助リクエスト（バックグラウンドレビューなど）を待つ
sleep "${POST_WAIT:-5}"
# ゲートウェイを止めて、次の実行に状態を持ち越さない
if [ -f "$HOME_DIR/gateway.pid" ]; then
  PID=$("$LAB/.venv/bin/python" -c "import json,sys;print(json.load(open(sys.argv[1]))['pid'])" "$HOME_DIR/gateway.pid" 2>/dev/null)
  [ -n "${PID:-}" ] && kill "$PID" 2>/dev/null
fi
cat "$OUT/time.txt"; tail -3 "$OUT/stdout.txt"
