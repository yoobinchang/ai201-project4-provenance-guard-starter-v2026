# Acceptance criteria — Provenance Guard

Five criteria for Unit 9 Shape B, written before the failure-hardening results
were collected. At least three criteria test the extension directly: malformed
input handling, detector failure recovery, and structured run instrumentation.

---
## 1.

For 10 malformed submissions, including missing text, null text, no
`creator_id`, a non-string `creator_id`, control characters, emoji-only text,
and text over 10,000 characters, at least 9 must return a JSON 400 response
with no 500 response.

**Why this target:** The extension is specifically about preventing bad input
from reaching model inference. A 90% rejection rate across malformed classes
is defendable for the first hardening pass while still requiring meaningful
coverage of all major bad paths.

---

## 2.

After 3 trials of a simulated detector timeout, each trial must return HTTP
503 within 31 seconds, retry exactly 2 times, and include `detector_unavailable`
in the JSON error.

**Why this target:** A timeout should fail quickly and predictably rather than
leaving a request waiting. Three trials catch slow or inconsistent retry
behavior, while the 31-second bound allows one 30-second call plus small retry
overhead.

---

## 3.

For 20 valid submissions, at least 18 must produce one structured `run` entry
with a non-negative `duration_ms`, `input_size`, `output_status`, and a
matching route in the audit log.

**Why this target:** Instrumentation is part of the extension, not a side
feature. Losing more than 2 run entries would make latency and cost evidence
unreliable.

---

## 4.

Across 3 trials, 15 rapid submissions from one `creator_id` must end in at
least 1 HTTP 429 and every 429 must produce a structured audit entry whose
reason is `rate_limited`.

**Why this target:** Rate limiting is already present, but hardening means a
rejected request must remain visible. The target verifies both the failure
control and its trace.

---

## 5.

For 5 valid appeals, the original decision remains in the audit log and exactly
1 additional `under_review` appeal entry is recorded for each `content_id`.

**Why this target:** A failure-hardening pass must not overwrite or erase an
original decision. Preserving append-only history lets reviewers diagnose the
state before and after an appeal.
