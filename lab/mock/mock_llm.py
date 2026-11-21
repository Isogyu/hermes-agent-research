"""台本どおりに応答する OpenAI 互換の偽 LLM サーバー。

目的: モデルの賢さに左右されずに、Hermes が何をモデルへ送るかを記録し、
決めたとおりのツール呼び出しを返して仕組みを検証する。

使い方:
    python mock_llm.py --port 8765 --log requests.jsonl --script script.json

台本 (script.json) は手順の配列。メインのエージェントからのリクエスト
（tools に terminal か skill_view を含むもの）が来るたびに、先頭から1つずつ消費する。
    {"text": "最終回答"}
    {"tool_calls": [{"name": "terminal", "arguments": {"command": "ls"}}]}
台本が尽きたとき、またはメイン以外（補助タスク）のリクエストには既定の文を返す。
"""
import argparse
import json
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOCK = threading.Lock()
STATE = {"script": [], "pos": 0, "log": None, "n": 0, "aux_text": "OK", "main_tools": ("terminal", "skill_view")}


def est_tokens(obj) -> int:
    """文字数 / 4 の粗い見積もり。相対比較にだけ使う。"""
    return len(json.dumps(obj, ensure_ascii=False)) // 4


def classify(body) -> str:
    names = {t.get("function", {}).get("name") for t in body.get("tools") or []}
    if names & set(STATE["main_tools"]):
        return "main"
    return "aux"


def next_step(kind):
    with LOCK:
        if kind == "main" and STATE["pos"] < len(STATE["script"]):
            step = STATE["script"][STATE["pos"]]
            STATE["pos"] += 1
            return step, STATE["pos"] - 1
    return {"text": STATE["aux_text"] if kind == "aux" else "DONE (script exhausted)"}, None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _json(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.rstrip("/").endswith("/models"):
            return self._json(200, {"object": "list", "data": [
                {"id": "mock-model", "object": "model", "owned_by": "lab", "context_length": 200000}]})
        self._json(404, {"error": {"message": "not found"}})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        if not self.path.rstrip("/").endswith("/chat/completions"):
            return self._json(404, {"error": {"message": f"unsupported path {self.path}"}})
        kind = classify(body)
        step, idx = next_step(kind)
        msgs = body.get("messages") or []
        tools = body.get("tools") or []
        prompt_tokens = est_tokens(msgs) + est_tokens(tools)
        with LOCK:
            STATE["n"] += 1
            rec = {
                "n": STATE["n"], "ts": time.time(), "kind": kind, "step": idx,
                "model": body.get("model"), "stream": bool(body.get("stream")),
                "n_messages": len(msgs), "n_tools": len(tools),
                "tool_names": [t.get("function", {}).get("name") for t in tools],
                "chars_messages": len(json.dumps(msgs, ensure_ascii=False)),
                "chars_tools": len(json.dumps(tools, ensure_ascii=False)),
                "chars_system": sum(len(json.dumps(m.get("content"), ensure_ascii=False))
                                    for m in msgs if m.get("role") in ("system", "developer")),
                "est_prompt_tokens": prompt_tokens,
                "extra_keys": sorted(k for k in body if k not in ("messages", "tools")),
                "reply": step,
                "messages": msgs,
            }
            if STATE["log"]:
                with open(STATE["log"], "a") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        cid = "chatcmpl-" + uuid.uuid4().hex[:12]
        tool_calls = [{
            "id": "call_" + uuid.uuid4().hex[:10], "type": "function",
            "function": {"name": tc["name"], "arguments": json.dumps(tc.get("arguments", {}), ensure_ascii=False)},
        } for tc in step.get("tool_calls", [])]
        text = step.get("text")
        completion_tokens = est_tokens(step)
        usage = {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                 "total_tokens": prompt_tokens + completion_tokens}
        finish = "tool_calls" if tool_calls else "stop"
        if not body.get("stream"):
            msg = {"role": "assistant", "content": text}
            if tool_calls:
                msg["tool_calls"] = tool_calls
            return self._json(200, {"id": cid, "object": "chat.completion", "created": int(time.time()),
                                    "model": body.get("model"), "usage": usage,
                                    "choices": [{"index": 0, "message": msg, "finish_reason": finish}]})
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        def chunk(delta, fr=None, with_usage=False):
            obj = {"id": cid, "object": "chat.completion.chunk", "created": int(time.time()),
                   "model": body.get("model"),
                   "choices": [{"index": 0, "delta": delta, "finish_reason": fr}]}
            if with_usage:
                obj["choices"] = []
                obj["usage"] = usage
            self.wfile.write(f"data: {json.dumps(obj, ensure_ascii=False)}\n\n".encode())
            self.wfile.flush()

        chunk({"role": "assistant", "content": ""})
        if text:
            chunk({"content": text})
        for i, tc in enumerate(tool_calls):
            chunk({"tool_calls": [{"index": i, **tc}]})
        chunk({}, fr=finish)
        chunk({}, with_usage=True)
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()
        self.close_connection = True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--log", required=True)
    ap.add_argument("--script")
    ap.add_argument("--aux-text", default="OK")
    a = ap.parse_args()
    STATE["log"] = a.log
    STATE["aux_text"] = a.aux_text
    if a.script:
        with open(a.script) as f:
            STATE["script"] = json.load(f)
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
