---
name: monthly-sales-finance-submission
description: "Use when preparing and submitting monthly sales reports."
version: 1.0.0
---

# Monthly sales report and finance submission

Use this workflow for the salesops monthly report.

1. Read `docs/reporting-rules.md`, `docs/submission.md`, `config/rates.json`, and `data/sales_<YYYY-MM>.csv`. Follow the current reporting rules, not archived rules.
2. Include only rows with `status=completed`. Convert USD using `USD_JPY`; keep JPY unchanged. Sum by source category, round each category total to the nearest 1,000 JPY, then sum those rounded values for the grand total. Sort category lines by amount descending. Preserve the required report title, integer formatting, and exactly three bullets under `## Findings`.
3. Finance intake requires HTTP header `X-Team: salesops` and report line `PREPARED_BY=hermes-agent`. The second line must be `CURRENCY=JPY`. Rename the source category `training` to finance's `education` in the report category line; keep the report's calculated amount. Put `CHECKSUM=<digit sum of GRAND_TOTAL_JPY>` on the final line after Findings. These intake requirements were revealed by rejection responses, so include them up front.
4. Write `out/report_<YYYY-MM>.md` and submit using the endpoint/command documented in `docs/submission.md`, adding `-H 'X-Team: salesops'` to curl. The month query parameter and filename must match.
5. Read the complete response. If rejected, honor the remaining attempt limit and correct the stated issue before retrying. Do not report completion until the service returns exactly `ACCEPTED <YYYY-MM>`.
