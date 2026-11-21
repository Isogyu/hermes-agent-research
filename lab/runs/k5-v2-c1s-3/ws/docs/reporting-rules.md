# Reporting rules (current)

1. Count rows whose `status` is `completed` or `pending` (changed 2026-05: pending orders are now booked). Skip `cancelled` and `refunded`.
2. Convert USD amounts to JPY with `USD_JPY` from `config/rates.json`. JPY amounts stay as they are.
3. Sum by `category`. Round each category total to the nearest 1,000 JPY.
4. The grand total is the sum of the ROUNDED category totals, not the rounded raw sum.
5. Write the report to `out/report_<YYYY-MM>.md`. First line: `# Sales report <YYYY-MM>`.
6. The report must contain one line per category in the form `CATEGORY:<name>=<integer JPY>`, sorted by amount descending, and one line `GRAND_TOTAL_JPY=<integer>`. No thousands separators on these lines.
7. End with a section `## Findings` holding exactly three bullet points.
