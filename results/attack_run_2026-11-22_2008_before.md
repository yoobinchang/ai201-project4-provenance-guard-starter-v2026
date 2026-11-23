# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-22 20:08
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `4587e736-d2ad-4289-b5e7-e8f2ac3d25df` | unsure | 0.371 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3c13196d-924f-468d-8d0e-be0357a7843b` | unsure | 0.518 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `3838f7cc-fe37-4cf8-aa46-6f83d6381330` | unsure | 0.580 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `3c2f05a5-5539-4f95-8540-3d6db743fb33` | unsure | 0.590 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `23df1931-581f-4447-a239-051aa6182264` | unsure | 0.387 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `4c3c6677-be06-42af-80e8-abe75a5c0c22` | unsure | 0.507 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `aabc94bc-1c9d-41ed-9bb1-786bdb109ed9` | unsure | 0.612 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `5c2a11d6-687f-43c8-a0bf-c9a8fd9ee348` | unsure | 0.375 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `bfd21f4f-b631-4f4b-9c6c-359e2e2b860a` | unsure | 0.596 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `34499245-9cfd-431a-ba07-d93b79a7ecd7` | ai | 0.845 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f7a1ee3c-ee51-4f9e-ae15-3670154d03e7` | unsure | 0.583 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `eaedbcfa-14af-414e-8f43-f66185a6a552` | ai | 0.677 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `1cc5c1ef-474e-4eaa-a5d6-b7541d581d89` | ai | 0.697 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `691fd3e0-f018-41ad-b89e-c6f7aa0b7f36` | ai | 0.687 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `a8f05cb6-a3ba-44fd-b08a-9741e88ef784` | ai | 0.719 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c3d938e1-13f7-46ee-85ab-c2a563c1368c` | ai | 0.706 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `56b41897-3a3b-46c7-9caf-4e5ad121b218` | ai | 0.733 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `d0e205ac-41ed-48fd-afdd-b2da2e96eafc` | unsure | 0.393 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `220b45f9-b438-4236-83d6-9ed6a0cf2667` | unsure | 0.454 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ae551528-8fd5-4936-947c-80d9e2276ee0` | human | 0.312 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c55b238a-fb13-423d-80a9-3aa8874c5936` | unsure | 0.544 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9e571431-9015-424e-9822-792167e0d894` | unsure | 0.488 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `e6adf836-5b81-4377-b2b9-189b65b291fc` | unsure | 0.510 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `5167d368-4a20-4474-9c55-1f5f91209d69` | unsure | 0.556 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `47c86bc6-18e2-49be-81ef-e453fa7b5a59` | human | 0.200 |  |
| MF04 | malformed | text is only punctuation | 200 | `f01e5822-3d18-4003-8618-d282ec3584b4` | unsure | 0.381 |  |
| MF05 | malformed | text is a very long single word | 200 | `36b7b5b8-6a30-4216-b7f6-15ebe89050a4` | ai | 0.824 |  |
| MF06 | malformed | text is emoji only | 200 | `b73b36ae-2b0c-4b7c-a488-4f1d4de82a9f` | ai | 0.999 |  |
| MF07 | malformed | text is right-to-left script | 200 | `27e8aa0f-a790-419f-978b-24990ed2da60` | ai | 0.953 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `969ba66f-9767-47da-a021-9e09326c6a40` | unsure | 0.445 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `5947cc74-d581-4cbc-bee9-49927fb8b1b1` | human | 0.350 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4ee04307-396d-4603-a514-2204884c8d10` | human | 0.339 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `249dd7c0-3561-4e81-9ab4-20b7299f74da` | human | 0.339 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c26a4093-2f22-4b23-a8ad-1870a835ebaf` | human | 0.339 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f62258bf-9f1e-416d-9f61-82b497677ed3` | human | 0.339 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3628c853-018b-49a0-859e-7b695e7c24be` | human | 0.339 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0bfe9f3d-2e0f-42ba-83d0-f93920d4df6d` | human | 0.339 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c1b28a3-9fd2-474f-90f6-9f2b4a6511da` | human | 0.339 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0d7ff27f-8bbc-4933-a31d-9b12a4fe5c68` | human | 0.339 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3a2e9d51-1f55-4e81-88a9-86cf5a263f01` | human | 0.339 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `26b21e42-5288-4323-b29b-edae079b8d7a` | human | 0.339 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "4587e736-d2ad-4289-b5e7-e8f2ac3d25df",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3712,
  "model_score": 0.1635,
  "style_score": 0.579,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "3c13196d-924f-468d-8d0e-be0357a7843b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5182,
  "model_score": 0.5943,
  "style_score": 0.4421,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "3838f7cc-fe37-4cf8-aa46-6f83d6381330",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.58,
  "model_score": 0.6662,
  "style_score": 0.4939,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "3c2f05a5-5539-4f95-8540-3d6db743fb33",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5896,
  "model_score": 0.6114,
  "style_score": 0.5677,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "23df1931-581f-4447-a239-051aa6182264",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3874,
  "model_score": 0.3212,
  "style_score": 0.4537,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "4c3c6677-be06-42af-80e8-abe75a5c0c22",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5071,
  "model_score": 0.5727,
  "style_score": 0.4415,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "aabc94bc-1c9d-41ed-9bb1-786bdb109ed9",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6119,
  "model_score": 0.5862,
  "style_score": 0.6376,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "5c2a11d6-687f-43c8-a0bf-c9a8fd9ee348",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3753,
  "model_score": 0.2452,
  "style_score": 0.5055,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "bfd21f4f-b631-4f4b-9c6c-359e2e2b860a",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5956,
  "model_score": 0.7042,
  "style_score": 0.487,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "34499245-9cfd-431a-ba07-d93b79a7ecd7",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8454,
  "model_score": 0.9792,
  "style_score": 0.7116,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f7a1ee3c-ee51-4f9e-ae15-3670154d03e7",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5832,
  "model_score": 0.6175,
  "style_score": 0.5489,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "eaedbcfa-14af-414e-8f43-f66185a6a552",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6768,
  "model_score": 0.7387,
  "style_score": 0.6149,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "1cc5c1ef-474e-4eaa-a5d6-b7541d581d89",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6968,
  "model_score": 0.8051,
  "style_score": 0.5885,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "691fd3e0-f018-41ad-b89e-c6f7aa0b7f36",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6867,
  "model_score": 0.8329,
  "style_score": 0.5406,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "a8f05cb6-a3ba-44fd-b08a-9741e88ef784",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7185,
  "model_score": 0.8005,
  "style_score": 0.6365,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c3d938e1-13f7-46ee-85ab-c2a563c1368c",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7059,
  "model_score": 0.8814,
  "style_score": 0.5304,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "56b41897-3a3b-46c7-9caf-4e5ad121b218",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7327,
  "model_score": 0.8816,
  "style_score": 0.5837,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "d0e205ac-41ed-48fd-afdd-b2da2e96eafc",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3933,
  "model_score": 0.3223,
  "style_score": 0.4644,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "220b45f9-b438-4236-83d6-9ed6a0cf2667",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.454,
  "model_score": 0.4625,
  "style_score": 0.4454,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ae551528-8fd5-4936-947c-80d9e2276ee0",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3121,
  "model_score": 0.2044,
  "style_score": 0.4198,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c55b238a-fb13-423d-80a9-3aa8874c5936",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5443,
  "model_score": 0.5943,
  "style_score": 0.4942,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "9e571431-9015-424e-9822-792167e0d894",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4877,
  "model_score": 0.4998,
  "style_score": 0.4756,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "e6adf836-5b81-4377-b2b9-189b65b291fc",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5098,
  "model_score": 0.6401,
  "style_score": 0.3795,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "5167d368-4a20-4474-9c55-1f5f91209d69",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5557,
  "model_score": 0.5583,
  "style_score": 0.5532,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "47c86bc6-18e2-49be-81ef-e453fa7b5a59",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.2,
  "model_score": 0.0,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "f01e5822-3d18-4003-8618-d282ec3584b4",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.3806,
  "model_score": 0.0112,
  "style_score": 0.75,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "36b7b5b8-6a30-4216-b7f6-15ebe89050a4",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8238,
  "model_score": 0.9976,
  "style_score": 0.65,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "b73b36ae-2b0c-4b7c-a488-4f1d4de82a9f",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "27e8aa0f-a790-419f-978b-24990ed2da60",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this was probably written with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "969ba66f-9767-47da-a021-9e09326c6a40",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.4447,
  "model_score": 0.2395,
  "style_score": 0.65,
  "label": "We cannot tell reliably whether this was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "5947cc74-d581-4cbc-bee9-49927fb8b1b1",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.3496,
  "model_score": 0.0492,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "4ee04307-396d-4603-a514-2204884c8d10",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "249dd7c0-3561-4e81-9ab4-20b7299f74da",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c26a4093-2f22-4b23-a8ad-1870a835ebaf",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "f62258bf-9f1e-416d-9f61-82b497677ed3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "3628c853-018b-49a0-859e-7b695e7c24be",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "0bfe9f3d-2e0f-42ba-83d0-f93920d4df6d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "1c1b28a3-9fd2-474f-90f6-9f2b4a6511da",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "0d7ff27f-8bbc-4933-a31d-9b12a4fe5c68",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "3a2e9d51-1f55-4e81-88a9-86cf5a263f01",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "26b21e42-5288-4323-b29b-edae079b8d7a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3393,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
