# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## Unit 9 Extension

**Shape:** B — Harden against failure

This extension adds a bounded failure-handling layer to Provenance Guard. It
validates request fields and text before model inference, rejects malformed
inputs without a 500 response, bounds model calls with timeout and retry
settings, records structured run timing for each request, and preserves existing
rate-limit rejection logging.

**What is out of scope:** This unit does not deploy the service, add hosted
authentication, replace the local GPT-2 model, or change the scoring labels.
The run path is **Path B — local with logs** because loading GPT-2 and PyTorch
requires more memory than a typical free host. All failure and cost evidence is
recorded on the local machine.

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writer sends `POST /submit` a JSON body containing `text` and `creator_id`.
2. The route creates a new `content_id` and validates that the text is present
   and usable.
3. `detector.model_signal(text)` measures how predictable the text is to GPT-2.
   Lower perplexity produces a score closer to 1.0 (more AI-like).
4. `stylometry.style_signal(text)` measures sentence-length variation,
   vocabulary repetition, and punctuation density. It maps those shape features
   to the same 0.0–1.0 scale where higher is more AI-like.
5. `scoring.combine_signals(model_score, style_score)` combines the two signals
   into one combined score.
6. `scoring.score_to_label(combined_score)` maps the score to `human`, `unsure`,
   or `ai`, and produces plain-language text for the writer.
7. `audit.log_decision(...)` saves the content ID, creator ID, both signal
   scores, combined score, guess, label, and status. The route returns the
   same information to the writer.
8. The writer can challenge the result with `POST /appeal` and a `content_id`.
   The service verifies that the ID exists, appends an appeal to the audit log,
   and changes that item to `under_review`. It does not re-run the detector.
9. The hardened submission path validates `creator_id`, text length, meaningful
   words, and control characters before calling GPT-2.
10. `detector.model_signal` is wrapped by a bounded timeout and retry count.
    A timeout or unavailable model returns a JSON 503 instead of an unhandled
    500.
11. Every submit, appeal, and rejected request writes a structured `run` entry
    containing timestamp, route, input size/type, status, error, and duration.

**Run path:** Local with logs (`python app.py`). A hosted URL is not used
because the local GPT-2 model plus PyTorch exceeds a typical 512 MB free-host
limit. The exact environment and commands are in [RUNNING.md](/Users/yoobin/ai201-project4-provenance-guard-starter-v2026/RUNNING.md).

**Cost measurement:** I measured five warmed submissions against the running
local service. Their wall-clock durations were 12.767 s, 3.272 s, 1.978 s,
2.694 s, and 1.278 s, for an average of **4.398 seconds per run**. I worked
this out with a Python wall-clock timer around the HTTP request and divided
the five durations by five. The cost is local compute time, not API spend.

**Scaling the cost:** At 100 submissions, the measured average implies
`100 x 4.398 = 439.8 seconds`, or approximately **7 minutes 20 seconds** of
local compute time. This is a projection, not a measured 100-run result.
It assumes comparable warmed runs and does not include model download time,
which happened separately and was not included in the five-run average.

**Before/after criterion verdict**

| Criterion | Before | After | Verdict |
|---|---|---|---|
| 1. Malformed submissions return 400 | Several malformed inputs reached model/scoring stages | 10 of 10 malformed categories returned 400 | MET |
| 2. Model timeout and retry | No bounded timeout/retry contract | 3 of 3 simulated timeouts returned 503 within the bound | MET |
| 3. Structured run logging | No named run records for all requests | 20 of 20 valid samples had run entries | MET |
| 4. Rate-limit trace | 10 200 then 5 429, with rejection entries | Same 10/5 pattern in every relevant run | MET |
| 5. Appeal history | Original decision was preserved | 5 of 5 appeals kept the decision and added one under-review entry | MET |

**The improvement**

The measured improvement was validation before model inference: reject missing
or non-string `creator_id`, control characters, emoji-only or under-worded text,
oversized text, and malformed JSON before the detector is called. This failed
in the before state for malformed text such as control characters and emoji,
which could receive a 200 label. After the change, the bad-input run returned
400 for every malformed category tested.

**Structured run log extract**

```json
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"eval_structured r_15","input_type":"text","input_size":58,"output_status":200,"output_error":null,"duration_ms":51.837}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"eval_structured r_16","input_type":"text","input_size":54,"output_status":200,"output_error":null,"duration_ms":45.945}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"eval_structured r_17","input_type":"text","input_size":56,"output_status":200,"output_error":null,"duration_ms":186.857}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"eval_structured r_18","input_type":"text","input_size":63,"output_status":200,"output_error":null,"duration_ms":113.986}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"eval_structured r_19","input_type":"text","input_size":57,"output_status":200,"output_error":null,"duration_ms":48.315}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"eval_structured r_20","input_type":"text","input_size":70,"output_status":200,"output_error":null,"duration_ms":70.020}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"bad","input_type":"text","input_size":18,"output_status":400,"output_error":"invalid_text_content","duration_ms":0.103}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"bad","input_type":"text","input_size":3,"output_status":400,"output_error":"invalid_text_content","duration_ms":0.262}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"bad","input_type":"text","input_size":12500,"output_status":400,"output_error":"text_too_long","duration_ms":0.800}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"test","input_type":"text","input_size":45,"output_status":503,"output_error":"detector_unavailable","duration_ms":507.879}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/submit","creator_id":"flood_tester","input_type":"json","input_size":0,"output_status":429,"output_error":"rate_limited","duration_ms":0.0}
{"timestamp":"2026-11-23T03:43:38+00:00","event":"run","route":"/appeal","creator_id":"normal_cost_test","input_type":"json","input_size":56,"output_status":200,"output_error":null,"duration_ms":1.200}
```

### Submission endpoint shape

**Request**

```json
{
  "text": "The text to judge.",
  "creator_id": "writer_123"
}
```

**Response**

```json
{
  "content_id": "a-generated-uuid",
  "guess": "human | unsure | ai",
  "confidence": 0.0,
  "label": "A plain-language explanation.",
  "model_score": 0.0,
  "style_score": 0.0
}
```

`combined_score` is also stored in the audit log. Invalid or unusable text
returns a 400 JSON error and is recorded as a rejection when it is a submission
attempt rather than a route parsing failure.

### Appeal endpoint shape

**Request**

```json
{
  "content_id": "a-generated-uuid",
  "reasoning": "This was written by me."
}
```

**Success response**

```json
{
  "ok": true,
  "content_id": "a-generated-uuid",
  "status": "under_review"
}
```

An unknown `content_id` returns 404 without creating an appeal entry.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** `detector.py::model_signal` measures text perplexity:
how surprising GPT-2 finds the text. The perplexity is converted with a logistic
function onto a 0.0–1.0 score where higher means more AI-like.

**Why that might differ between human and AI writing:** AI-generated text often
uses the likely patterns GPT-2 itself expects, so it can have lower perplexity.
Human writing can be more varied, unusual, or structurally surprising.

**What it can't see:** This signal confuses predictability with authorship.
Plain, conventional, or highly repetitive human writing can be very predictable
and may receive an AI-like score. Dense, unusual, or non-native-but-limited
vocabulary can also have a high perplexity and look human.

### Signal two — the style signal

**What it measures:** `stylometry.py::style_signal` measures shape without
reading meaning: the variation in sentence lengths, the type-token ratio
(unique words / total words), and punctuation density.

**Why that might differ between human and AI writing:** Generated prose may use
even, mid-length sentences and repeat vocabulary patterns. Human prose is often
less regular, with short sentences beside longer ones and more varied
punctuation.

**What it can't see:** The signal cannot understand what the text says or who
wrote it. Typos, sentence breaks, quotations, edits, or even formality changes
can move the score without changing authorship. It is therefore easy to evade
with superficial edits and should not be treated as proof.

The style signal uses coefficient of variation for sentence length, exact
unique-word ratio for vocabulary variation, and meaningful punctuation per
character. Lower sentence variation and lower vocabulary variation increase
the AI-like score. The three normalized components have weights of 40%, 35%, and
25%, respectively.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Start with a weighted average of the model and style scores.
When the signals agree, the combined score moves toward their shared conclusion.
When they disagree, the average produces a middle score. That outcome is
explicitly uncertain rather than letting either signal win on its own.

**The numbers:** Model signal weight: `0.35`. Style signal weight: `0.65`.
Human threshold: `0.35`. AI threshold: `0.65`. These numbers live in
`config.py`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** Suppose
a plainly written human paragraph has `model_score = 0.90` but
`style_score = 0.10`. The model mistakes predictable prose for AI, while the
style signal sees a varied human-like shape. The 0.5/0.5 rule produces
`combined_score = 0.50`, which falls in the unsure band instead of calling the
writer confidently human or AI. This does not prove authorship; it records
disagreement and limits the consequence of a split verdict.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | We think this was probably written by a person. |
| unsure | 0.35 - 0.65 | We cannot tell reliably whether this was written by a person or AI. |
| high-confidence AI | 0.65 - 1.00 | We think this was probably written with AI assistance. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The unsure label does not accuse the writer or assign intent. It says the
service does not have enough evidence to decide. That keeps the label in terms
of the service's uncertainty rather than the person's authorship.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I first thought through the submission flow, signals,
  thresholds, and expected behavior myself. I then asked AI to follow the
  project walkthrough and turn those requirements into repository changes.
- *What came back:* AI produced candidate documentation and implementation
  structures, including the submission trace, endpoint shapes, signal scoring,
  labels, and acceptance criteria.
- *What I changed:* I reviewed each change and kept the parts that matched my
  own design decisions, while requesting English comments and corrections where
  the project instructions or code needed adjustment.

**Moment 2**

- *What I asked for:* I asked AI to continue through Unit 8 with the
  walkthrough, including the rate limiter, attack-set run, criteria trials,
  failure diagnoses, one measured improvement, and Unit 9 failure hardening.
- *What came back:* AI produced candidate implementations and run summaries,
  including a 35% model and 65% style weight change. It also drafted which
  attacks and criteria were held, missed, or still broken. For Unit 9, AI
  drafted timeout/retry handling, validation, structured run logging, and the
  local evidence documentation.
- *What I changed:* I reviewed the actual before-and-after evidence, kept only
  the one-change improvement, and checked the response fields and audit-log
  behavior. I ran the bad-input and timeout simulations, measured five local
  request durations, and used the resulting evidence in this write-up. I did
  not treat every candidate diagnosis as final; I verified the score changes
  and service responses before writing the conclusions.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
The limits allow a real writer to submit several revisions and appeal while
remaining fast enough to stop a script from mapping thresholds in a burst.
Ten requests per minute is high enough for ordinary use, but low enough that
15 rapid submissions trigger 429 responses. The 200-per-day limit gives a
writer room to use the service repeatedly without allowing sustained automated
probing.

**What a caller counts as:** Per `creator_id`, with the IP address as fallback
for requests that do not provide a valid creator ID. <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

The full 56-row table is in
`results/attack_run_2026-11-22_2008_before.md`.

| Family | Attacks | HELD | BROKE / concerning |
|---|---:|---:|---:|
| evasion | 10 | 9 | 1 |
| false_positive | 8 | 2 | 6 |
| prompt_injection | 6 | 6 | 0 |
| malformed / bad request | 20 | 10 | 10 |
| flood_same_creator | 12 | 12 | 0 |

- EV10 returned `ai` and is marked BROKE for the repeated-stanza evasion.
- FP02-FP07 are genuine human writing but received `ai`; all are marked
  BROKE from a false-positive perspective.
- MF03-MF07 and RQ02/RQ06 allowed malformed inputs to receive a 200 decision;
  the malformed/bad-request cases are marked BROKE where 400 was expected.
- MF01, MF02, MF08, RQ01, RQ03-RQ05, RQ07-RQ12 correctly returned 400.
- FL01_11 and FL01_12 received 429 after ten 200 responses.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"creator_id":"attacker_FP02","content_id":"eaedbcfa-14af-414e-8f43-f66185a6a552","guess":"ai","model_score":0.7387,"style_score":0.6149,"combined_score":0.6768,"label":"We think this was probably written with AI assistance.","status":"decided"}
{"creator_id":"attacker_FP03","content_id":"1cc5c1ef-474e-4eaa-a5d6-b7541d581d89","guess":"ai","model_score":0.8051,"style_score":0.5885,"combined_score":0.6968,"label":"We think this was probably written with AI assistance.","status":"decided"}
{"creator_id":"attacker_FP04","content_id":"691fd3e0-f018-41ad-b89e-c6f7aa0b7f36","guess":"ai","model_score":0.8329,"style_score":0.5406,"combined_score":0.6867,"label":"We think this was probably written with AI assistance.","status":"decided"}
{"creator_id":"attacker_EV10","content_id":"34499245-9cfd-431a-ba07-d93b79a7ecd7","guess":"ai","model_score":0.9792,"style_score":0.7116,"combined_score":0.8454,"label":"We think this was probably written with AI assistance.","status":"decided"}
{"creator_id":"attacker_MF03","content_id":"47c86bc6-18e2-49be-81ef-e453fa7b5a59","guess":"human","model_score":0.0,"style_score":0.4,"combined_score":0.2,"label":"We think this was probably written by a person.","status":"decided"}
{"creator_id":"attacker_MF07","content_id":"27e8aa0f-a790-419f-978b-24990ed2da60","guess":"ai","model_score":0.9064,"style_score":1.0,"combined_score":0.9532,"label":"We think this was probably written with AI assistance.","status":"decided"}
{"creator_id":"attacker_RQ02","content_id":"969ba66f-9767-47da-a021-9e09326c6a40","guess":"unsure","model_score":0.2395,"style_score":0.65,"combined_score":0.4447,"label":"We cannot tell reliably whether this was written by a person or AI.","status":"decided"}
{"creator_id":"attacker_MF01","event":"rejected","reason":"invalid_text","detail":"text must be a non-empty string.","status":"rejected"}
{"creator_id":"attacker_MF02","event":"rejected","reason":"text_too_short","detail":"Text is too short to score — a few sentences at least.","status":"rejected"}
{"creator_id":"attacker_MF08","event":"rejected","reason":"text_too_long","detail":"text exceeds 10000 characters.","text_length":57640,"status":"rejected"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP02-FP07 were genuinely human pieces that received `ai` or `unsure` in ways
that could wrongly accuse a writer. The worst pattern was FP03: non-native
English writing that was carefully written received a 0.6968 combined score,
with a 0.8051 model score and 0.5885 style score. The model signal dominated
the result even though predictability and careful vocabulary are poor evidence
of AI authorship.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. malformed submissions | At least 9 of 10 return JSON 400 | 10/10 | 10/10 | 10/10 | MET |
| 2. detector timeout | 503 within 31 s, 2 retries | 503 | 503 | 503 | MET |
| 3. structured run entries | At least 18 of 20 produce run entries | 20/20 | 20/20 | 20/20 | MET |
| 4. rate-limit trace | 15 rapid requests end with 429 and rejection logs | 5 429 | 5 429 | 5 429 | MET |
| 5. appeal history | 5 appeals preserve decision and add one entry | 5/5 | 5/5 | 5/5 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json
{
  "source": "app.py::_call_model_with_timeout",
  "scenario": "simulated detector timeout",
  "trial": 1,
  "status": 503,
  "model_calls": 3,
  "retry_count": 2,
  "elapsed_ms": 507.879,
  "body": {
    "error": "detector_unavailable",
    "message": "simulated unavailable model"
  }
}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

### Criterion diagnoses

- **Criterion 1 — MET.** The route validation stage rejected missing text,
  null/number/list text, missing or non-string creator IDs, control characters,
  emoji-only text, and oversized text with JSON 400 responses. This prevented
  malformed inputs from reaching model inference.
- **Criterion 2 — MET.** The `_call_model_with_timeout` stage made one initial
  model call and two retries, then returned 503 with `detector_unavailable` in
  all three timeout trials. The 31-second bound was not exceeded.
- **Criterion 3 — MET.** The structured logging stage wrote matching
  `/submit` run entries for 20 of 20 valid requests in each trial. Each entry
  included `timestamp`, `input_type`, `input_size`, `output_status`,
  `output_error`, and `duration_ms`.
- **Criterion 4 — MET.** In all three trials, the limiter allowed 10 requests
  and returned 429 for the final 5. The 429 handler wrote `reason=rate_limited`
  run records in the audit log.
- **Criterion 5 — MET.** In all three trials, 5 of 5 appeals returned
  `under_review`. The original decisions remained and each appeal appended one
  under-review entry beside it.

---

## The Improvement

**What I changed:** I added validation before model inference and bounded the
detector call with a 30-second timeout and two retries. I also added structured
run records with timestamp, route, input size/type, status, error, and duration.

**Which diagnosis pointed at it:** The failure evidence showed that malformed
text could reach the model, timeout failures could become uncaught exceptions,
and successful/error requests were not consistently instrumented. The route
and detector stages were the two mechanisms addressed by this improvement.

**Before:** Malformed control-character and emoji-only text could be scored,
and no bounded timeout/retry contract existed. Runs did not include named
duration and output fields consistently.

**After:** Three timeout trials returned 503 with two retries, malformed
categories returned 400, and 20 of 20 valid submissions wrote structured run
entries in the same audit log.

**Did it help, and how do I know:** It helped because criterion 1 changed from
malformed values reaching scoring to 10 of 10 JSON 400 responses. Criterion 2
changed from an unbounded model call to a simulated 503 with exactly two
retries, and criterion 3 recorded 20 of 20 run entries.

---

## What's Still Broken

- All five acceptance criteria met in the three-trial evidence runs.
- A real timeout still needs load testing against actual model-cache pressure,
  because the timeout trials used a deliberately slowed detector rather than an
  external network failure.
- Log growth is not rotated or archived. I would add size-based rotation and
  backup/diagnostics export before production use.
- The service has no process-level readiness check for partial model loading.
  I would add a circuit breaker and health-state transition tests.

I stopped after implementing and measuring one failure-hardening improvement:
input validation, bounded timeout/retry behavior, and structured logging. Each
item is complete enough for a local, instrumented run. Full production
deployment, authentication, log rotation, and external monitoring are out of
scope for this extension.

**The next unit I would build:** I would add size-based rotation and a
diagnostics export for `logs/audit.jsonl`, because the local run record grows
linearly and a larger workload could make retrieval slow or consume disk
space. This is the one next piece I would build first; it would preserve the
append-only log while making it safe to archive and inspect after rotation.

### Unit 9 failure-hardening review

- **Model timeout:** The bounded timeout and two retries were verified with
  simulated delays, but real network or disk failures may behave differently.
  I would add process-level health checks and a circuit breaker for repeated
  detector failures. I stopped because local GPT-2 has no hosted-network retry
  dependency and the required timeout simulation was sufficient.
- **Retry cost:** Retrying may multiply local compute time when the model is
  merely slow instead of unavailable. I would expose retry attempt count and
  total model duration in the response only after load testing. I stopped
  before that implementation because the milestone asks for evidence, not every
  operational dashboard.
- **Log persistence:** The local JSONL log survives process restarts but has no
  rotation or external backup. I would add size-based rotation and a
  diagnostics export. I stopped because Path B is intentionally local and
  persistent storage is outside the extension scope.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 9

       [x] One system extended: Provenance Guard
       [x] Shape B named and out-of-scope items documented
       [x] Path B local run path documented in RUNNING.md
       [x] Five acceptance criteria written before results
       [x] Three trials completed for every criterion
       [x] Before and after evidence recorded
       [x] At least ten structured run entries pasted as text
       [x] One cost number measured from local runs
       [x] One improvement implemented and measured
       [x] Every criterion verdict and diagnosis completed
       [x] What's Still Broken and stopping reason written
       [x] Repository URL unchanged from the previous unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
