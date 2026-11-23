# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

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

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
