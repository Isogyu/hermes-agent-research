---
name: sales-reporting
description: Use for sales reports; follow rules and verify output.
---

# Sales reporting

Use this workflow for recurring sales reports governed by local team documentation.

1. Inspect the workspace instructions, current reporting rules, input data, and configuration before calculating. Treat explicitly archived or superseded rules as historical only; follow the current rule document.
2. Translate each rule literally into a deterministic calculation: filter eligible rows first, convert currencies using the configured rate, aggregate at the specified grouping level, and apply rounding at the specified stage. Do not assume a conventional rounding method or reporting format if the rules specify otherwise; use the standard implied by the data/tooling and make the result reproducible.
3. Generate the report with a small script using decimal arithmetic for currency, rather than mental arithmetic or binary floating-point. Keep the implementation simple and calculate directly from source files.
4. Write to the exact required path and preserve exact headers, line formats, sort order, and section constraints, including an exact count of required findings/bullets.
5. Verify the written artifact by reading it back or printing its exact contents, and check totals/ordering/format against the rules before reporting completion. Report the path and key total concisely.

Pitfalls: filter statuses before aggregation because excluded rows must not affect category amounts. Round each group before computing a grand total whenever rules say the grand total is based on rounded groups; rounding the raw grand sum can differ. Use a decimal rounding mode explicitly because default language behavior may not match the intended nearest-unit convention. Keep findings factual and supported by the calculated results; do not invent business interpretations.