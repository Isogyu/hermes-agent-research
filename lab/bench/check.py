"""成果物を採点する。使い方: check.py <作業フォルダ> <YYYY-MM>  → JSON を出力"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_workspace import truth
ws, month = pathlib.Path(sys.argv[1]), sys.argv[2]
t = truth(month); p = ws / "out" / f"report_{month}.md"
res = {"file": p.is_file(), "header": False, "grand_total": False, "categories": False, "sorted": False, "findings3": False}
if p.is_file():
    s = p.read_text()
    res["header"] = s.splitlines()[0].strip() == f"# Sales report {month}" if s.strip() else False
    m = re.search(r"^GRAND_TOTAL_JPY=(\d+)\s*$", s, re.M)
    res["grand_total"] = bool(m) and int(m.group(1)) == t["grand_total"]
    cats = re.findall(r"^CATEGORY:([a-z]+)=(\d+)\s*$", s, re.M)
    got = {k: int(v) for k, v in cats}
    res["categories"] = got == t["categories"]
    vals = [int(v) for _, v in cats]
    res["sorted"] = bool(vals) and vals == sorted(vals, reverse=True)
    f = s.split("## Findings")[-1] if "## Findings" in s else ""
    res["findings3"] = len(re.findall(r"^\s*[-*] ", f, re.M)) == 3
res["score"] = sum(1 for k in ("file", "header", "grand_total", "categories", "sorted", "findings3") if res[k])
res["pass"] = res["score"] == 6
print(json.dumps(res))
