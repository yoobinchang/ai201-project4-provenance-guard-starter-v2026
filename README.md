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

**The numbers:** Model signal weight: `0.5`. Style signal weight: `0.5`.
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

- *What I asked for:* I asked AI to continue the walkthrough for the remaining
  milestones, including the endpoint implementation, second signal, combined
  score, labels, and appeal path.
- *What came back:* AI generated code drafts for `submit`, `appeal`, the
  stylometry measures, signal combination, label mapping, and audit-log updates.
- *What I changed:* I verified the behavior with smoke tests and reviewed the
  response fields and validation logic. I kept the final implementation only
  after checking that it followed the starter's contracts.

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
| 1. my own writing | No more than 1 of 10 labeled AI | 1 AI | 1 AI | 1 AI | PASS |
| 2. label coverage | All three labels reachable | only unsure | only unsure | only unsure | MISS |
| 3. score spread | Human below AI by at least 0.20 | gap -0.13 | gap -0.13 | gap -0.13 | MISS |
| 4. appeal path | 5 of 5 under review with an appeal entry | 5/5 | 5/5 | 5/5 | PASS |
| 5. bad input | 4 malformed cases return 400 | 4/4 | 4/4 | 4/4 | PASS |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json
{
  "source": "scoring.py::combine_signals",
  "scenario": "label coverage",
  "trial": 1,
  "results": [
    {"guess": "unsure", "confidence": 0.5366, "model_score": 0.5534, "style_score": 0.5198},
    {"guess": "unsure", "confidence": 0.5342, "model_score": 0.5783, "style_score": 0.49},
    {"guess": "unsure", "confidence": 0.5393, "model_score": 0.5719, "style_score": 0.5068}
  ]
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

- **Criterion 1 — MET.** In each trial, one of the 10 own-writing pieces was
  labeled AI, so the result met the target of at most one false positive.
- **Criterion 2 — MISSED.** All three label-coverage submissions landed in the
  unsure band: 0.5366, 0.5342, and 0.5393 in trial 1, and the same pattern
  occurred in the other two trials. The stage was signal combination and label
  mapping: the inputs did not cover enough of the combined-score range, and
  the 0.35/0.65 thresholds left this test batch without a human or AI result.
- **Criterion 3 — MISSED.** The 5 human-like pieces averaged 0.52152 while the
  5 AI-like pieces averaged 0.38872 across all three trials. This is a
  -0.1328 average gap in the wrong direction. The stage is the style signal:
  its normalization and AI-direction calculations assign higher scores to the
  human-like batch and lower scores to the AI-like batch, so the same weighting
  does not recover a meaningful separation.
- **Criterion 4 — MET.** All five valid submissions were appealed successfully.
  Each appeal returned `under_review`, and the append-only log received exactly
  one appeal entry beside the original decision.
- **Criterion 5 — MET.** Empty text, missing text, null text, and text over
  10,000 characters returned 400 in all three trials. The route rejected the
  input before model inference, and the rejection was logged.

### Attack diagnoses

- **EV10 — BROKE.** The repeated-stanza text targeted the style signal and
  returned AI with a combined score of 0.8454. The mechanism is the style
  signal's spread/punctuation normalization: the repeated structure reduced
  its human-like variation reading, and the high model score increased the
  combined result.
- **FP02-FP07 — BROKE.** Six genuine human texts were labeled AI or were
  pushed above the human threshold. The signal-one model finds predictable
  formal, careful, rubric-style, and repeated text easy to predict, while the
  style signal also rewards regular shape as AI-like. This is a
  false-positive mechanism at stages 1 and 2, before the combining rule
  amplifies the agreement.
- **MF03 — BROKE.** Control characters reached the model and returned human
  instead of being rejected. The route validation only checked text length,
  not control-character content, so malformed bytes reached the signal stage.
- **MF04 — BROKE.** A punctuation-only submission received a 200 decision.
  It has no meaningful words, but the style signal produced a shape score that
  was combined into a decision instead of being rejected by the route.
- **MF05-MF07 — BROKE.** A very long word, emoji-only text, and right-to-left
  text received AI or high-AI decisions. Their shapes or lack of normal English
  words do not belong in the model/style assumptions, so they reached the
  combining rule as ordinary text and were overconfidently labeled.
- **RQ02 and RQ06 — BROKE.** Missing or non-string creator IDs fell back to
  `unknown` or were accepted rather than rejected. The route accepted malformed
  metadata instead of validating the creator field as a non-empty string.
- **FL01_11-FL01_12 — HELD.** The flood reached 429 after ten 200 responses,
  so the per-creator limiter stopped the same-caller burst. The mechanism was
  the Flask-Limiter decorator, and the rejection entries appeared in the log.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
