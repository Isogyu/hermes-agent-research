"""架空の月次売上レポート業務の作業フォルダを作る。
使い方: gen_workspace.py <出力先> <YYYY-MM>
社内ルールは docs/reporting-rules.md にあり、古い矛盾したルール文書も混ぜてある。"""
import csv, json, os, pathlib, random, sys

# RULESET=v2 でルール改定版を作る: pending も計上する（Skill が古くなる状況の再現）
V2 = os.environ.get("RULESET") == "v2"
COUNTED = ("completed", "pending") if V2 else ("completed",)

def rows(month):
    rnd = random.Random("sales-" + month)
    cats = ["hardware", "software", "services", "training"]
    regions = ["tokyo", "osaka", "nagoya", "fukuoka"]
    out = []
    for i in range(60):
        cur = "USD" if rnd.random() < 0.3 else "JPY"
        amt = rnd.randint(200, 9000) if cur == "USD" else rnd.randint(30000, 1500000)
        st = rnd.choices(["completed", "cancelled", "refunded", "pending"], [70, 10, 8, 12])[0]
        out.append({"date": f"{month}-{rnd.randint(1, 28):02d}", "region": rnd.choice(regions),
                    "category": rnd.choice(cats), "amount": amt, "currency": cur, "status": st})
    return out

RATE = 152.4

def truth(month):
    tot = {}
    for r in rows(month):
        if r["status"] not in COUNTED:
            continue
        v = r["amount"] * RATE if r["currency"] == "USD" else r["amount"]
        tot[r["category"]] = tot.get(r["category"], 0) + v
    cat = {k: int(round(v / 1000.0)) * 1000 for k, v in tot.items()}
    return {"categories": cat, "grand_total": sum(cat.values())}

def main():
    ws, month = pathlib.Path(sys.argv[1]), sys.argv[2]
    for d in ("data", "config", "docs", "out"):
        (ws / d).mkdir(parents=True, exist_ok=True)
    with open(ws / "data" / f"sales_{month}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "region", "category", "amount", "currency", "status"])
        w.writeheader(); w.writerows(rows(month))
    (ws / "config" / "rates.json").write_text(json.dumps({"USD_JPY": RATE, "EUR_JPY": 165.1}, indent=1))
    (ws / "README.md").write_text("# Sales ops workspace\n\nData lives in `data/`. Team conventions are under `docs/`.\n")
    (ws / "docs" / "onboarding.md").write_text("# Onboarding\n\nWelcome. Ask your lead for system access. Reports go to the finance channel on the 3rd business day.\n")
    (ws / "docs" / "rules-2024-archived.md").write_text(
        "# Reporting rules (2024, ARCHIVED - superseded by reporting-rules.md)\n\n"
        "- Include every row regardless of status.\n- Use a fixed rate of 140 JPY per USD.\n"
        "- Write the report to `report.txt` in the workspace root.\n")
    (ws / "docs" / "reporting-rules.md").write_text(
        "# Reporting rules (current)\n\n"
        ""
        + ("1. Count rows whose `status` is `completed` or `pending` (changed 2026-05: pending orders are now booked). Skip `cancelled` and `refunded`.\n" if V2 else
           "1. Count only rows whose `status` is `completed`. Skip `cancelled`, `refunded` and `pending`.\n") +
        "2. Convert USD amounts to JPY with `USD_JPY` from `config/rates.json`. JPY amounts stay as they are.\n"
        "3. Sum by `category`. Round each category total to the nearest 1,000 JPY.\n"
        "4. The grand total is the sum of the ROUNDED category totals, not the rounded raw sum.\n"
        "5. Write the report to `out/report_<YYYY-MM>.md`. First line: `# Sales report <YYYY-MM>`.\n"
        "6. The report must contain one line per category in the form `CATEGORY:<name>=<integer JPY>`, "
        "sorted by amount descending, and one line `GRAND_TOTAL_JPY=<integer>`. No thousands separators on these lines.\n"
        "7. End with a section `## Findings` holding exactly three bullet points.\n")

if __name__ == "__main__":
    main()
