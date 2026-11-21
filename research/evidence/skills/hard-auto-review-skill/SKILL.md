---
name: monthly-sales-reporting
description: "Use when preparing and submitting monthly sales reports."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Sales, Finance, Reporting, CSV, Reconciliation]
---

# Monthly sales reporting

Use this workflow when generating a monthly sales report from source transaction data and submitting it to a finance intake service.

## When to Use

Use for recurring monthly sales reports computed from transaction data and submitted to finance. Do not use for general narrative sales analysis without a finance submission workflow.

## Procedure

1. Read the submission instructions, current reporting rules, data file, and referenced rate/config files before calculating. Check for archived rules, but follow the current rules explicitly identified as authoritative.
2. Parse source data programmatically. Apply inclusion criteria first; convert currencies using the configured rate; aggregate by source category; round each category exactly as specified; calculate the grand total from the rounded category values when required. Verify counts, category sums, ordering, and arithmetic independently before writing.
3. Write the report at the required path and match its required structure literally, including exact line formats, sort order, and any fixed-count findings. Keep findings consistent with the data and report labels.
4. Before submitting, validate required formatting and totals with a small deterministic check. Submit using the documented endpoint and payload format.
5. Treat each rejection as both a consumed attempt and new intake convention evidence. Read the full rejection, make only the indicated correction, re-validate, and resubmit with a conservative attempt budget. Do not guess additional conventions when the service provides a precise error.
6. Preserve the accounting calculation while applying finance-system presentation aliases when explicitly required. Keep the underlying amount and grand total unchanged, and update narrative references to match the displayed label.
7. Stop only after receiving the documented success response; report the accepted period and output path.

## Pitfalls

- Apply status filtering before aggregation; otherwise excluded transactions contaminate category totals.
- Round category totals before calculating the grand total when the rules say the grand total is the sum of rounded categories; rounding the raw grand sum can differ.
- Keep source category names for calculations and only map display labels when finance explicitly requires an alias, so relabeling does not create or lose sales.
- Treat intake rejections as charged attempts, not harmless validation probes; each retry consumes the finite monthly budget.
- Include the exact required intake header and report metadata once discovered; the POST body alone may not satisfy service conventions.
- Ensure terminal checksum/control lines are outside required findings bullets when the format requires exactly a fixed number of bullets, and ensure any requirement that a line be last is literally satisfied.
