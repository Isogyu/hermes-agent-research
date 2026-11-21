"""受付ログから採点する。合格 = ACCEPTED が出たこと。"""
import json, os, sys
month = sys.argv[2]; recs = []
try: recs = [r for r in map(json.loads, open(os.environ["INTAKE_LOG"])) if r["month"] == month]
except Exception: pass
acc = any(r["result"] == "ACCEPTED" for r in recs)
print(json.dumps({"score": int(acc), "pass": acc, "attempts": len(recs), "codes": [r.get("code") or r["result"] for r in recs]}))
