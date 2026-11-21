"""ゲートウェイの Responses API に、同じ会話で複数月の提出つき業務を順に依頼し、自動振り返りの結果を調べる。
使い方: run_gw_multi.py <実行名> <月,月,...> [--patched]
出力: lab/runs/<実行名>/{summary.json, intake.jsonl, ...}、訓練後の HOME は lab/homes/<実行名>"""
import json, os, pathlib, re, shutil, subprocess, sys, time, urllib.request
LAB = pathlib.Path("/Users/user/Nous Research"); B = LAB / "lab/bench"
SP = pathlib.Path("/private/tmp/claude-501/-Users-user-Nous-Research/ceec3039-bce5-415d-ba74-7bfacaf0f9f1/scratchpad")
name, months, patched = sys.argv[1], sys.argv[2].split(","), "--patched" in sys.argv
out = LAB / "lab/runs" / name; H = SP / "homes" / f"gw-{name}"; iso = SP / "iso" / name / "salesops"
for d in (out, iso): d.mkdir(parents=True, exist_ok=True)
if H.exists(): shutil.rmtree(H)
subprocess.run(["rsync", "-a", "--exclude", "gateway.*", "--exclude", "logs", "--exclude", "state.db*", "--exclude", "sessions", f"{LAB}/lab/homes/real/", f"{H}/"], check=True)
port, iport = 28642, 28960 + int(time.time()) % 30
env = {**os.environ, "HERMES_HOME": str(H), "API_SERVER_KEY": "labkey-local-only", "INTAKE_PORT": str(iport), "INTAKE_LIMIT": "20"}
cfg = (H / "config.yaml").read_text().replace('cwd: "."', f'cwd: "{iso}"')
(H / "config.yaml").write_text(cfg + f'platforms:\n  api_server:\n    enabled: true\n    extra:\n      host: "127.0.0.1"\n      port: {port}\n')
log = out / "intake.jsonl"; log.write_text("")
srv = subprocess.Popen([sys.executable, str(B / "intake_server.py"), str(iport), "20", str(log)])
cmd = [str(LAB / ".venv/bin/python"), str(B / "gateway_patched.py")] if patched else [str(LAB / ".venv/bin/hermes"), "gateway", "run", "--quiet"]
gw = subprocess.Popen(cmd, cwd=iso, env=env, stdout=open(out / "gateway.out", "w"), stderr=subprocess.STDOUT)
def call(path, body=None, timeout=900):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Bearer labkey-local-only", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))
try:
    for _ in range(90):
        try: call("/v1/health", timeout=3); break
        except Exception: time.sleep(1)
    alog = H / "logs/agent.log"; turns = []
    for m in months:
        subprocess.run([sys.executable, str(B / "gen_hard_ws.py"), str(iso), m], env=env, check=True)
        n_before = alog.read_text().count("Background review complete") if alog.exists() else 0
        t = time.time()
        r = call("/v1/responses", {"model": "hermes-agent", "conversation": f"salesops-{name}",
                 "input": f"Produce the monthly sales report for {m} following the team reporting rules, then submit it to finance as described in docs/submission.md."})
        sec = int(time.time() - t)
        # このターンで振り返りが起動したなら完了を待つ（起動しない場合は60秒で諦める）
        waited = 0
        while waited < 240:
            txt = alog.read_text()
            if txt.count("Background review complete") > n_before: break
            if waited >= 60 and "bg-review" not in txt.split("Turn ended")[-1]: break
            time.sleep(2); waited += 2
        recs = [json.loads(l) for l in log.read_text().splitlines() if json.loads(l)["month"] == m]
        turns.append({"month": m, "seconds": sec, "usage": r.get("usage"), "attempts": len(recs),
                      "codes": [x.get("code") or x["result"] for x in recs], "review_wait": waited})
        print(json.dumps(turns[-1], ensure_ascii=False), flush=True)
finally:
    gw.terminate(); srv.terminate(); time.sleep(3)
reviews = re.findall(r"Background review complete: (.*)", (H / "logs/agent.log").read_text())
since = (out / "intake.jsonl").stat().st_ctime
new = [p for p in list((H / "skills").rglob("*")) + list((H / "memories").rglob("*")) if p.is_file() and ".curator" not in str(p) and "/." not in str(p.relative_to(H)) and p.stat().st_mtime > since - 5]
keys = ["X-Team", "PREPARED_BY", "education", "CURRENCY=JPY", "CHECKSUM"]
text = "\n".join(p.read_text(errors="replace") for p in new)
summary = {"name": name, "patched": patched, "turns": turns, "reviews": reviews, "new_files": [str(p.relative_to(H)) for p in new],
           "conventions_found": {k: text.count(k) for k in keys}, "n_found": sum(1 for k in keys if k in text)}
(out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
ev = LAB / "research/evidence/skills" / name; ev.mkdir(parents=True, exist_ok=True)
for p in new: shutil.copy(p, ev / p.name)
dst = LAB / "lab/homes" / name
if dst.exists(): shutil.rmtree(dst)
subprocess.run(["rsync", "-a", "--exclude", "gateway.*", "--exclude", "logs", "--exclude", "state.db*", "--exclude", "sessions", f"{H}/", f"{dst}/"], check=True)
shutil.copy(LAB / "lab/homes/real/config.yaml", dst / "config.yaml")
print(json.dumps({k: summary[k] for k in ("reviews", "new_files", "conventions_found", "n_found")}, ensure_ascii=False, indent=1))
