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

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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
