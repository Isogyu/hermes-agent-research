---
name: sales-reporting
description: Use when producing and submitting recurring sales reports.
---

# Sales reporting

Use this for recurring reports built from local sales data and submitted to a finance intake service.

1. Discover the governing materials before calculating: inspect repository instructions, current reporting rules, submission instructions, data files, and configuration values. Prefer current rules over archived notes; consult other docs for relevant context. Treat intake instructions as potentially incomplete when they say finance conventions may be discovered through rejection responses.
2. Parse source data programmatically. Apply documented inclusion filters first, convert currencies using configured rates, and aggregate by the required grouping. Use decimal arithmetic for currency conversion and the specified rounding mode; round at the required stage (for example, each group before computing the grand total). Independently verify counts and totals from the parsed source.
3. Write the artifact at the exact path and format. Validate title, ordering, required lines, totals, rounding, and exact bullet/section counts against the rules before submission. Keep machine-parsed data lines free of separators or extra prose when required.
4. Submit exactly as specified. Read each response. If rejected, treat its reason as actionable intake-validation guidance: make the smallest correction satisfying the finance convention without changing computed amounts, then resubmit. Track the reported attempt count and never exceed the stated limit; avoid speculative retries.
5. After any report change, re-check that the original reporting requirements still hold alongside newly discovered intake requirements. Continue until the service returns the explicit success response, then report the artifact path and verified acceptance briefly.

Pitfalls:
- Do not infer that undocumented intake conventions are optional; rejection messages can specify required headers, metadata, category aliases, or checksums.
- Do not alter source totals to satisfy a formatting rejection; change presentation metadata or labels only as instructed, because intake conventions should not corrupt the accounting basis.
- Do not claim submission succeeded from an HTTP/tool success alone; only the finance service's explicit acceptance response completes the task.
- Preserve the required report structure when appending intake metadata; a machine-required trailing line may coexist with a final findings section only if that section still contains exactly the required number of bullets.