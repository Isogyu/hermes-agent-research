---
name: monthly-sales-report
description: Use when producing monthly sales reports from salesops data.
---

# Monthly sales report

Run the bundled generator from a salesops workspace:

`python3 <skill-directory>/scripts/monthly_sales_report.py YYYY-MM`

It reads `data/sales_YYYY-MM.csv` and `config/rates.json` from the current workspace, writes `out/report_YYYY-MM.md`, and validates the report before exiting successfully.

## Team rules (current)

- Count only rows whose `status` is `completed`; skip `cancelled`, `refunded`, and `pending`.
- Convert USD amounts to JPY using `USD_JPY` from `config/rates.json`; JPY amounts remain unchanged.
- Sum by category, then round each category total to the nearest 1,000 JPY.
- The grand total is the sum of rounded category totals, not a rounding of the raw aggregate.
- Save to `out/report_<YYYY-MM>.md`.
- First line must be `# Sales report <YYYY-MM>`.
- Include one line per category as `CATEGORY:<name>=<integer JPY>`, sorted by amount descending, with no thousands separators; include `GRAND_TOTAL_JPY=<integer>`.
- End with `## Findings` and exactly three bullet points.
- `docs/rules-2024-archived.md` is explicitly superseded and must not be used.

The script validates month, input rows, currency, status, report layout, category values/order, grand-total calculation, and exactly three findings.