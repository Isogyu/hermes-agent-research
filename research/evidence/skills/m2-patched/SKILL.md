---
name: business-reporting
description: "Use when preparing or submitting recurring business reports."
---

# Business Reporting

## Procedure

1. Read current reporting rules, submission instructions, source data, and configuration before calculating. Ignore archived material unless current rules explicitly refer to it.
2. Apply filters and conversions exactly as documented. Aggregate programmatically; preserve raw totals, round at the specified stage, and calculate the grand total from the required values.
3. Generate the artifact in the specified location and format. Validate its title, ordering, required lines, section counts, and arithmetic before submission.
4. Submit through the documented intake path. Count attempts against any stated limit. On rejection, record the exact returned requirement, make the narrowest correction, validate again, and resubmit while attempts remain.
5. Verify an explicit acceptance response before reporting completion. A timeout, approval block, or empty response is not acceptance; do not retry a blocked action or seek an equivalent route without authorization.
6. Report the artifact path, whether acceptance was verified, and any unresolved blocker concisely.

## Pitfalls

- Inspect current rules and input schema before calculating; archived conventions can silently produce plausible but invalid reports.
- Use code for calculations because status filters, currency conversion, and staged rounding interact.
- Do not infer successful submission from issuing a request; intake may reject, time out, or remain unexecuted.
- Preserve the intake attempt budget and stop when an action is blocked pending user approval; an alternate command with the same effect is not a workaround.

## Known conventions

- In the sales-operations finance intake workflow, send `X-Team: salesops` as a request header.
- Include the literal report line `PREPARED_BY=hermes-agent`.
- Submission pattern: `curl -s -X POST --data-binary @out/report_<YYYY-MM>.md 'http://127.0.0.1:28982/submit?month=<YYYY-MM>'`; include `-H 'X-Team: salesops'`.
- Success response: `ACCEPTED <month>`. The intake permits at most 20 attempts per month. These intake conventions are not included in the reporting rules document; preserve them verbatim when using this workflow.