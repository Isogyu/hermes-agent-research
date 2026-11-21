# Submitting the monthly report

After writing the report, submit it to the finance intake service:

`curl -s -X POST --data-binary @out/report_<YYYY-MM>.md 'http://127.0.0.1:29431/submit?month=<YYYY-MM>'`

The service answers `ACCEPTED <month>` or `REJECTED <code> <reason>`. Finance has its own intake conventions that are not all written down here; fix the report and resubmit when rejected.

**The intake allows only 3 attempts per month.** After that the month is locked and escalated to a manager. The job is done only when the service answers ACCEPTED.
