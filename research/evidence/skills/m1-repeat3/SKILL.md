---
name: operational-reporting
description: "Use when preparing and submitting recurring reports."
---

# Operational reporting

Use this for recurring reports built from local or connected source data and delivered to an intake service.

## Workflow

1. Read the submission instructions, current reporting rules, source data, and configuration inputs before calculating. Distinguish current guidance from archived or superseded rules. Identify exact output path, required structure, delivery command, and any explicit retry/attempt limit.
2. Parse source data programmatically. Apply inclusion/exclusion rules first, then conversions using configured rates, then aggregate at the specified level. Keep intermediate unrounded sums and apply rounding exactly where directed; compute any grand total from the values the rules specify.
3. Draft the report to the required path. Check the required first/last lines, category naming, ordering, exact line formats, number formatting, and requested number of findings. Ensure narrative claims agree with computed totals and ranking. Check derived metadata (such as a checksum) against the exact final required total; calculate it programmatically rather than by inspection.

4. Submit only through the documented channel/command, preserving the intended period and payload. A direct request to submit the report authorizes that submission.
5. Treat the intake response as authoritative. If rejected, use the returned code/reason to correct the report or required request metadata, check the attempt budget before retrying, and resubmit. Do not stop at a successful HTTP command; finish only on an explicit acceptance response.
6. Report completion briefly with the output path and exact acceptance status; mention unresolved blockers plainly.

## Pitfalls

- Read all relevant current instructions before calculating; archived examples can conflict with the active rules.
- Validate each finding against the computed totals and sort order; plausible prose can contradict the actual numbers.
- Do not infer undocumented intake conventions from the submission guide alone; a rejection may specify additional required headers or report fields, and each retry consumes the stated attempt budget.
- Preserve the requested report structure while adding required intake metadata; do not silently alter the underlying calculation rules to satisfy a naming or format convention.
- After each correction, resend the exact on-disk report and verify the response, because locally changing a file does not complete submission.
