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
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "I usually start a project by writing down the path from an input to the final response. That makes the implementation easier to explain because every stage has a clear responsibility.",
            "I missed the bus this morning and had to wait in the rain. The driver saw me from across the street, but the bus kept moving before I reached the stop.",
            "When I review code, I first check whether the behavior is measurable. A vague statement may sound reasonable, but it does not tell me what changed or how I would test it.",
            "Yesterday I cooked rice, soup, and vegetables for dinner. I added too much salt, so I had to dilute the soup and serve it with plain rice.",
            "My first priority for this service is to protect a real writer from a wrong accusation. A missed AI text is less harmful than telling someone that their own work is not theirs.",
            "I walked to the library after class and found a quiet table near the window. I finished the assignment slowly because I kept checking the examples.",
            "A good audit trail should show what happened before the original decision. It should also leave the appeal separate instead of changing or deleting the old record.",
            "I prefer to test a small part before building on it. If the route works, I can add the detector, but I cannot diagnose the route and the model at the same time.",
            "The coffee in the kitchen was already cold, so I reheated it twice and eventually drank it while reviewing the documentation.",
            "I changed the limit to ten submissions per minute because repeated revisions should work, while a flood should be stopped quickly.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 2,
        "texts": [
            "The implementation of the proposed framework requires careful consideration of several important factors. The system provides consistent results across multiple scenarios while maintaining clarity, reliability, and a structured approach to decision making.",
            "I found a small white feather under the kitchen table this morning. It looked out of place beside my shoes, and I spent too long wondering whether the cat had brought it inside.",
            "This text is written carefully, but some of its sentences vary in rhythm. It may be difficult to determine whether the ideas came from a person or an automated writing system.",
        ],
    },
    {
        "name": "score spread",
        "criterion": 3,
        "texts": [
            "I bought groceries after work and carried the bags upstairs one at a time. The elevator was broken, but the stairs gave me more time to remember what I had forgotten.",
            "We took the train instead of driving because it was already late. I watched the stations pass while nobody said much.",
            "My neighbor left a note asking me to water the plants. I forgot once, so I set an alarm and checked both pots every morning.",
            "I wrote a paragraph three times before I was satisfied. The first version was too formal, and the second sounded like a manual.",
            "The dog found a tennis ball under the shed. He dropped it near my feet and waited for me to throw it again.",
            "The proposed system improves operational consistency by applying a structured framework to multiple input scenarios. It balances reliability, maintainability, and measurable performance outcomes.",
            "The framework provides an effective solution by integrating well-defined components with consistent processes. The resulting system supports clear evaluation across a range of use cases.",
            "Careful implementation requires a systematic approach that considers technical constraints, expected results, and potential risks. The process should remain clear and repeatable.",
            "The described method combines established principles with practical safeguards. Its structured design allows teams to review decisions, compare outcomes, and refine future processes.",
            "The service processes submitted text through a sequence of defined steps. Each stage produces a measurable output that contributes to the final decision.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 2500, "creator_id": "eval_bad_huge"},
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
