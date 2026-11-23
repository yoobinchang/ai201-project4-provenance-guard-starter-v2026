#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import re
import time
import uuid
import queue
import threading

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)


def _call_model_with_timeout(text: str) -> float:
    """Call the detector with a bounded wait and retry transient failures."""
    last_error = None
    for attempt in range(config.DETECTOR_RETRY_COUNT + 1):
        result_queue = queue.Queue(maxsize=1)

        def call_detector():
            try:
                result_queue.put(("ok", detector.model_signal(text)))
            except Exception as exc:  # noqa: BLE001
                result_queue.put(("error", exc))

        worker = threading.Thread(target=call_detector, daemon=True)
        worker.start()
        try:
            status, value = result_queue.get(
                timeout=config.DETECTOR_TIMEOUT_SECONDS,
            )
        except queue.Empty:
            last_error = TimeoutError(
                f"model call timed out after {config.DETECTOR_TIMEOUT_SECONDS:.1f}s"
            )
        else:
            if status == "ok":
                if not isinstance(value, (int, float)):
                    last_error = RuntimeError("model returned no numeric score")
                elif not 0.0 <= float(value) <= 1.0:
                    last_error = RuntimeError("model returned an out-of-range score")
                else:
                    return float(value)
            else:
                last_error = value

        if attempt < config.DETECTOR_RETRY_COUNT:
            time.sleep(config.DETECTOR_RETRY_DELAY_SECONDS)

    if isinstance(last_error, detector.DetectorUnavailable):
        raise last_error
    raise detector.DetectorUnavailable(
        f"Model signal unavailable after retries: {last_error}"
    )


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        audit.log_run(
            route="/submit",
            creator_id=payload.get("creator_id", "unknown"),
            input_type="json",
            input_size=0,
            output_status=429,
            output_error="rate_limited",
            duration_ms=0.0,
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "detector_timeout_seconds": config.DETECTOR_TIMEOUT_SECONDS,
        "detector_retry_count": config.DETECTOR_RETRY_COUNT,
        "max_text_chars": config.MAX_TEXT_CHARS,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """
    started = time.perf_counter()
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        audit.log_rejection(
            creator_id="unknown",
            reason="invalid_json",
            detail="Request body must be a JSON object.",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        response = jsonify({
            "error": "invalid_json",
            "message": "Request body must be a JSON object.",
        })
        audit.log_run(
            route="/submit",
            creator_id="unknown",
            input_type="invalid_json",
            input_size=0,
            output_status=400,
            output_error="invalid_json",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return response, 400

    text = payload.get("text")
    creator_id = payload.get("creator_id")
    if not isinstance(creator_id, str) or not creator_id.strip():
        creator_id = "unknown"
        audit.log_rejection(
            creator_id=creator_id,
            reason="invalid_creator_id",
            detail="creator_id must be a non-empty string.",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        audit.log_run(
            route="/submit",
            creator_id=creator_id,
            input_type="json",
            input_size=len(text) if isinstance(text, str) else 0,
            output_status=400,
            output_error="invalid_creator_id",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "invalid_creator_id",
            "message": "creator_id must be a non-empty string.",
        }), 400
    creator_id = creator_id.strip()

    if not isinstance(text, str) or not text.strip():
        audit.log_rejection(
            creator_id=creator_id,
            reason="invalid_text",
            detail="text must be a non-empty string.",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        audit.log_run(
            route="/submit",
            creator_id=creator_id,
            input_type="json",
            input_size=0,
            output_status=400,
            output_error="invalid_text",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "invalid_text",
            "message": "text must be a non-empty string.",
        }), 400

    if len(text) > config.MAX_TEXT_CHARS:
        audit.log_rejection(
            creator_id=creator_id,
            reason="text_too_long",
            detail=f"text exceeds {config.MAX_TEXT_CHARS} characters.",
            text_length=len(text),
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        audit.log_run(
            route="/submit",
            creator_id=creator_id,
            input_type="text",
            input_size=len(text),
            output_status=400,
            output_error="text_too_long",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "text_too_long",
            "message": f"text must not exceed {config.MAX_TEXT_CHARS} characters.",
        }), 400

    control_characters = any(ord(character) < 32 and character not in "\n\r\t" for character in text)
    words = re.findall(r"[a-z0-9']+", text.lower())
    if control_characters or len(words) < config.MIN_TEXT_WORDS:
        reason = "invalid_text_content"
        audit.log_rejection(
            creator_id=creator_id,
            reason=reason,
            detail="text must contain meaningful words and no control characters.",
            word_count=len(words),
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        audit.log_run(
            route="/submit",
            creator_id=creator_id,
            input_type="text",
            input_size=len(text),
            output_status=400,
            output_error=reason,
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": reason,
            "message": "text must contain at least 3 meaningful words and no control characters.",
        }), 400

    content_id = str(uuid.uuid4())
    try:
        model_score = _call_model_with_timeout(text)
    except ValueError as exc:
        audit.log_rejection(
            creator_id=creator_id,
            reason="text_too_short",
            detail=str(exc),
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        audit.log_run(
            route="/submit",
            creator_id=creator_id,
            input_type="text",
            input_size=len(text),
            output_status=400,
            output_error="text_too_short",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "text_too_short",
            "message": str(exc),
        }), 400
    except detector.DetectorUnavailable as exc:
        audit.log_rejection(
            creator_id=creator_id,
            reason="detector_unavailable",
            detail=str(exc),
            retry_count=config.DETECTOR_RETRY_COUNT,
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        audit.log_run(
            route="/submit",
            creator_id=creator_id,
            input_type="text",
            input_size=len(text),
            output_status=503,
            output_error="detector_unavailable",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "detector_unavailable",
            "message": str(exc),
        }), 503

    style_score = stylometry.style_signal(text)
    combined_score = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(combined_score)
    confidence = combined_score

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
        status="decided",
        duration_ms=(time.perf_counter() - started) * 1000,
    )
    audit.log_run(
        route="/submit",
        creator_id=creator_id,
        input_type="text",
        input_size=len(text),
        output_status=200,
        output_error=None,
        duration_ms=(time.perf_counter() - started) * 1000,
        content_id=content_id,
        guess=guess,
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score,
    })


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    started = time.perf_counter()
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        audit.log_run(
            route="/appeal",
            creator_id="unknown",
            input_type="invalid_json",
            input_size=0,
            output_status=400,
            output_error="invalid_json",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "invalid_json",
            "message": "Request body must be a JSON object.",
        }), 400

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")
    if not isinstance(content_id, str) or not content_id.strip():
        audit.log_run(
            route="/appeal",
            creator_id="unknown",
            input_type="json",
            input_size=len(str(payload)),
            output_status=400,
            output_error="invalid_content_id",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "invalid_content_id",
            "message": "content_id must be a non-empty string.",
        }), 400
    if not isinstance(reasoning, str) or not reasoning.strip():
        audit.log_run(
            route="/appeal",
            creator_id="unknown",
            input_type="json",
            input_size=len(str(payload)),
            output_status=400,
            output_error="invalid_reasoning",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "invalid_reasoning",
            "message": "reasoning must be a non-empty string.",
        }), 400

    content_id = content_id.strip()
    entries = audit.entries_for(content_id)
    if not entries:
        audit.log_run(
            route="/appeal",
            creator_id="unknown",
            input_type="json",
            input_size=len(str(payload)),
            output_status=404,
            output_error="content_not_found",
            duration_ms=(time.perf_counter() - started) * 1000,
        )
        return jsonify({
            "error": "content_not_found",
            "message": "No submission exists for this content_id.",
        }), 404

    decision = next(
        (entry for entry in entries if entry.get("event") != "appeal"),
        entries[0],
    )
    creator_id = decision.get("creator_id", "unknown")
    audit.log_appeal(
        content_id=content_id,
        creator_id=creator_id,
        reasoning=reasoning.strip(),
    )
    audit.log_run(
        route="/appeal",
        creator_id=creator_id,
        input_type="json",
        input_size=len(str(payload)),
        output_status=200,
        output_error=None,
        duration_ms=(time.perf_counter() - started) * 1000,
        content_id=content_id,
    )

    return jsonify({
        "ok": True,
        "content_id": content_id,
        "status": "under_review",
        "message": "Your appeal was recorded and the submission is under review.",
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
