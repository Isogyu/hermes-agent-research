---
name: monthly-sales-report
description: Use when preparing monthly sales reports.
version: 1.0.0
metadata:
  hermes:
    tags: [sales, reporting, csv, finance]
    category: software-development
---

# Monthly Sales Report

## When to Use
A monthly sales report is requested in a sales-ops workspace, or a similar workspace whose current team rules and inputs are discoverable.

## Procedure
1. Confirm the workspace root and inspect `docs/` for current reporting rules. Read README/onboarding for context. Ignore explicitly archived or superseded rules.
2. Identify the exact month and matching input file under `data/`. Read relevant configuration, including currency rates.
3. Parse CSV data using its header; do not estimate rows visually. Apply current rules exactly for statuses, currency conversion, aggregation, rounding, ordering, output path/format, and findings. Do not carry forward assumptions from prior reports.
4. Calculate with a script or reliable decimal arithmetic. Check currency conversions and rounding boundaries. Compute the grand total in the prescribed aggregation order.
5. Write the report to the prescribed location and use exact required line formats. Satisfy required section counts and formatting constraints.
6. Validate the saved artifact programmatically: title/month, category lines and ordering, grand-total arithmetic, and required findings count/format. Reconcile included CSV row counts and totals against an independently computed result.
7. Report the exact output path, key totals, and validation status. Do not send or publish it unless explicitly requested.

## Reusable cautions
- Current team rules take precedence over archived documents.
- Make calculations reproducible from source data and current config; never fabricate missing rates or infer undocumented rules.
- Keep report-specific facts out of this skill; reread inputs and rules for every run.
