"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "malformed submissions",
        "criterion": 1,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "Valid words should fail because creator ID is absent."},
            {"text": "Valid text but the creator is invalid.", "creator_id": []},
            {"text": "hello\x00world this still has text", "creator_id": "eval_control"},
            {"text": "😀😀😀", "creator_id": "eval_emoji"},
            {"text": "word " * 2500, "creator_id": "eval_bad_huge"},
            {"text": 12345, "creator_id": "eval_number"},
            {"text": ["not", "a", "string"], "creator_id": "eval_list"},
        ],
    },
    {
        "name": "structured run entries",
        "criterion": 3,
        "texts": [
            "The local service received a complete and meaningful submission.",
            "I checked the route, validation logic, audit log, and response.",
            "A structured run entry should include timing and output status.",
            "The text contains enough ordinary words to pass the minimum validation.",
            "This request measures how the service behaves under normal operation.",
            "The audit trail keeps each route outcome separate and readable.",
            "I am testing duration fields during a repeated local run.",
            "One submission should create one matching run entry.",
            "The response status and input size make failures diagnosable.",
            "A local model call can take longer than simple route validation.",
            "The service should return useful JSON after successful scoring.",
            "This sample provides a stable normal-path request.",
            "Every run should report whether it succeeded or returned an error.",
            "The instrumented route writes the elapsed duration in milliseconds.",
            "The model signal and style signal use separate code paths.",
            "The combined score should remain available in the log.",
            "This is a valid sentence for a repeated measurement run.",
            "Structured evidence makes a failure easier to find and explain.",
            "A normal submission should not produce a rejection entry.",
            "The final sample completes the twenty-request structured logging test.",
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
