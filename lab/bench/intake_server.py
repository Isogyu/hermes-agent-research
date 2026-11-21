"""架空の「経理受付 API」。文書にない提出時の慣習を5つ持ち、違反は1回の提出につき1つだけ教える。
使い方: intake_server.py <port> <試行上限> <ログ.jsonl>
受付: POST /submit?month=YYYY-MM  本文=レポート
目的: 作業フォルダの文書からは分からない知識（暗黙知）が、経験を通じて Skill に移るかを測る。"""
import json, pathlib, re, sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_workspace import truth

PORT, LIMIT, LOG = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
attempts = {}

def digit_sum(n): return sum(int(c) for c in str(n))

def validate(month, body, headers):
    t = truth(month)
    lines = body.splitlines()
    if headers.get("X-Team") != "salesops":
        return "E11", "missing request header X-Team: salesops"
    if "PREPARED_BY=hermes-agent" not in lines:
        return "E23", "missing line PREPARED_BY=hermes-agent"
    if re.search(r"^CATEGORY:training=", body, re.M):
        return "E31", "category 'training' is called 'education' in the finance system"
    if len(lines) < 2 or lines[1].strip() != "CURRENCY=JPY":
        return "E42", "second line must be CURRENCY=JPY"
    got = {k: int(v) for k, v in re.findall(r"^CATEGORY:([a-z]+)=(\d+)\s*$", body, re.M)}
    want = {("education" if k == "training" else k): v for k, v in t["categories"].items()}
    m = re.search(r"^GRAND_TOTAL_JPY=(\d+)\s*$", body, re.M)
    if got != want or not m or int(m.group(1)) != t["grand_total"]:
        return "E90", "amounts do not match the ledger"
    if not lines or lines[-1].strip() != f"CHECKSUM={digit_sum(t['grand_total'])}":
        return "E57", "last line must be CHECKSUM=<sum of the digits of GRAND_TOTAL_JPY>"
    return None, None

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        q = parse_qs(urlparse(self.path).query); month = (q.get("month") or [""])[0]
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0)).decode("utf-8", "replace")
        n = attempts.get(month, 0)
        if not re.fullmatch(r"\d{4}-\d{2}", month):
            out, rec = "REJECTED E01 month query parameter required (YYYY-MM)\n", None
        elif n >= LIMIT:
            out = f"LOCKED attempt limit ({LIMIT}) reached for {month}; escalated to manager\n"
            rec = {"month": month, "attempt": n + 1, "result": "LOCKED"}
        else:
            attempts[month] = n + 1
            code, msg = validate(month, body, self.headers)
            out = f"ACCEPTED {month}\n" if code is None else f"REJECTED {code} {msg} (attempt {n + 1} of {LIMIT})\n"
            rec = {"month": month, "attempt": n + 1, "result": "ACCEPTED" if code is None else "REJECTED", "code": code}
        if rec:
            rec["ts"] = time.time()
            with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")
        data = out.encode(); self.send_response(200); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

HTTPServer(("127.0.0.1", PORT), H).serve_forever()
