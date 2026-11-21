#!/bin/bash
# 実モデルで1回実行して採点する。
# 使い方: run_real.sh <実行名> <元になる HERMES_HOME> <YYYY-MM> <プロンプト>
# 元の HOME は毎回複製するので、実行どうしは互いに影響しない。
set -u
LAB="/Users/user/Nous Research"; B="$LAB/lab/bench"
NAME="$1"; SRC="$2"; MONTH="$3"; PROMPT="$4"
OUT="$LAB/lab/runs/$NAME"; H="${HOME_ROOT:-$LAB/lab/homes}/run-$NAME"
mkdir -p "$OUT"; [ -e "$OUT/usage.json" ] && { echo "既に存在: $OUT"; exit 1; }
[ "${KEEP_HOME:-0}" = 1 ] && H="$SRC" || { mkdir -p "$H"; rsync -a --exclude 'gateway.*' --exclude 'logs' --exclude 'state.db*' --exclude 'sessions' "$SRC/" "$H/"; }
# 作業フォルダは研究フォルダの外（git 管理外）に置く。エージェントが親フォルダを検索して
# ほかの実行や証跡を読むのを防ぐため（k2 の比較はこれで無効になった）。
ISO="${ISO_ROOT:-/private/tmp/claude-501/-Users-user-Nous-Research/ceec3039-bce5-415d-ba74-7bfacaf0f9f1/scratchpad/iso}/$NAME/salesops"
mkdir -p "$ISO"
"$LAB/.venv/bin/python" "${GEN:-$B/gen_workspace.py}" "$ISO" "$MONTH"
cd "$ISO"; S=$(date +%s)
HERMES_HOME="$H" "$LAB/.venv/bin/hermes" ${MODE:--z} "$PROMPT" --usage-file "$OUT/usage.json" > "$OUT/stdout.txt" 2>&1
SEC=$(( $(date +%s) - S ))
mkdir -p "$OUT/ws"; rsync -a "$ISO/" "$OUT/ws/"
PIDF="$H/gateway.pid"; [ -f "$PIDF" ] && kill "$("$LAB/.venv/bin/python" -c "import json,sys;print(json.load(open(sys.argv[1]))['pid'])" "$PIDF" 2>/dev/null)" 2>/dev/null
"$LAB/.venv/bin/python" - "$OUT" "$H" "$MONTH" "$SEC" "$NAME" <<'PY'
import json, sqlite3, subprocess, sys, os
out, home, month, sec, name = sys.argv[1:6]
u = json.load(open(f"{out}/usage.json")) if os.path.exists(f"{out}/usage.json") else {}
chk = json.loads(subprocess.check_output([sys.executable, os.environ.get("CHECK") or (os.path.dirname(out.rstrip('/')) + "/../bench/check.py"), f"{out}/ws", month]))
tools, calls = None, []
try:
    db = sqlite3.connect(f"{home}/state.db")
    tools = db.execute("select sum(tool_call_count) from sessions").fetchone()[0]
    for (tc,) in db.execute("select tool_calls from messages where tool_calls is not null"):
        try: calls += [c.get("function", {}).get("name") for c in json.loads(tc)]
        except Exception: pass
except Exception as e:
    calls = [f"db-error:{e}"]
import re
outside = 0
try:
    for (tc,) in db.execute("select tool_calls from messages where tool_calls is not null"):
        for c in json.loads(tc):
            a = c.get("function", {}).get("arguments", "")
            if "Nous Research" in a or "/Users/" in a or "../.." in a:
                outside += 1
except Exception:
    outside = -1
rec = {"name": name, "outside_refs": outside, "month": month, "seconds": int(sec), "api_calls": u.get("api_calls"), "input": u.get("input_tokens"),
       "cache_read": u.get("cache_read_tokens"), "output": u.get("output_tokens"), "tool_calls": tools,
       "skill_view": sum(1 for c in calls if c == "skill_view"), "skill_manage": sum(1 for c in calls if c == "skill_manage"),
       "delegated": [c for c in ("claude", "codex") if any(('"command"' in (tc or "")) and ((c + " -p") in tc or (c + " exec") in tc) for (tc,) in db.execute("select tool_calls from messages where tool_calls is not null"))],
       "score": chk["score"], "pass": chk["pass"], "check": chk, "completed": u.get("completed")}
json.dump(rec, open(f"{out}/result.json", "w"))
print(json.dumps({k: rec[k] for k in ("name", "seconds", "api_calls", "input", "cache_read", "output", "tool_calls", "skill_view", "skill_manage", "outside_refs", "delegated", "score", "pass")}))
PY
