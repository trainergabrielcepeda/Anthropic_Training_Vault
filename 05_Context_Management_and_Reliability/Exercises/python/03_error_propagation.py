"""
Exercise 3 — Structured Error Propagation Across a Multi-Agent Call
Domain: Context Management & Reliability (Task 5.3)

Problem this demonstrates:
  A subagent's tool call times out. Two anti-patterns to avoid:
    1. Returning a generic string like "search unavailable" — hides
       whether this is retryable and discards any partial results.
    2. Silently catching the failure and returning an empty result
       marked as SUCCESS — the coordinator ends up believing a topic
       was researched when it never actually was.

  Instead, the "subagent" here returns a STRUCTURED error object:
    - failure_type       (what kind of failure — enables the right recovery)
    - attempted_query    (what it was trying to do)
    - partial_results    (whatever it already had before failing)
    - alternative_approaches (suggestions for the coordinator)

  A "coordinator" function then makes a decision USING that structure —
  something it could not do with a bare string or a silently-empty
  success. This file has no network dependency for the failure itself
  (it's simulated), but the final synthesis step is a real Claude call
  so you can see a coordinator actually reasoning over structured
  error context instead of just branching on it in Python.
"""

import json
import time
import anthropic

client = anthropic.Anthropic()

MODEL = "claude-haiku-4-5-20251001"


# ─────────────────────────────────────────────
# Simulated subagent: a web-research call that can time out
# ─────────────────────────────────────────────
class SubagentTimeout(Exception):
    pass


def subagent_search(query: str, simulate_timeout: bool) -> dict:
    """Stands in for a subagent's tool call (e.g. a real web-search MCP tool).
    Returns a STRUCTURED result on both success and failure — never a bare
    string, and never a silently-empty 'success' when something actually
    went wrong."""

    partial_results_gathered_so_far = [
        {"source": "trade-press-article-1", "excerpt": "Early coverage before the timeout hit."}
    ]

    if simulate_timeout:
        # This is where a real implementation would attempt LOCAL RECOVERY first
        # (e.g. one retry with backoff) before giving up and propagating upward.
        try:
            _attempt_with_local_retry(query)
        except SubagentTimeout:
            # Local recovery failed — propagate a STRUCTURED error, not a string.
            return {
                "status": "error",
                "failure_type": "timeout",
                "attempted_query": query,
                "partial_results": partial_results_gathered_so_far,
                "alternative_approaches": [
                    "retry with a narrower date range",
                    "fall back to a cached index if available",
                ],
            }

    # Success path: a genuine, successful result (possibly an empty one —
    # which must still be reported as status: "success", not conflated with error).
    return {
        "status": "success",
        "query": query,
        "results": [
            {"source": "industry-report-2026", "excerpt": "Full findings retrieved normally."}
        ],
    }


def _attempt_with_local_retry(query: str) -> None:
    """Simulates one local retry attempt that also fails — this is the
    'local recovery for transient failures' step a real subagent should
    try BEFORE propagating an error upward."""
    time.sleep(0.01)  # stand-in for a real retry-with-backoff delay
    raise SubagentTimeout(f"retry for '{query}' also timed out")


# ─────────────────────────────────────────────
# Anti-patterns shown for contrast (do not do this)
# ─────────────────────────────────────────────
def anti_pattern_generic_string(simulate_timeout: bool) -> str:
    """BAD: collapses everything into one opaque string. The coordinator can't
    tell a retryable timeout from a permanent failure, and any partial
    results are simply gone."""
    if simulate_timeout:
        return "search unavailable"
    return "search complete"


def anti_pattern_silent_empty_success(simulate_timeout: bool) -> dict:
    """BAD: swallows the failure and reports success with an empty result.
    A synthesis step built on this will look confident about a topic that
    was never actually researched."""
    if simulate_timeout:
        return {"status": "success", "results": []}
    return {"status": "success", "results": [{"source": "industry-report-2026", "excerpt": "..."}]}


# ─────────────────────────────────────────────
# Coordinator: makes a real decision from the structured error
# ─────────────────────────────────────────────
COORDINATOR_TOOL = [{
    "name": "record_recovery_decision",
    "description": "Record how the coordinator should recover from this subagent result.",
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["proceed_with_partial_results", "retry_with_alternative", "accept_success"]
            },
            "coverage_note": {
                "type": "string",
                "description": "A short annotation describing coverage/confidence for this sub-topic."
            }
        },
        "required": ["action", "coverage_note"]
    }
}]


def coordinator_recover(subagent_result: dict) -> dict:
    """A real Claude call reasoning over the STRUCTURED result — this is only
    possible because the subagent returned failure_type / partial_results /
    alternatives instead of a bare string or a fake success."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=250,
        system=(
            "You are a research coordinator. You receive a structured result from a "
            "search subagent — either a success payload or a structured error "
            "(failure_type, attempted_query, partial_results, alternative_approaches). "
            "Decide the best recovery action and write a short coverage note describing "
            "how much confidence the final report should place in this sub-topic."
        ),
        tools=COORDINATOR_TOOL,
        tool_choice={"type": "tool", "name": "record_recovery_decision"},
        messages=[{
            "role": "user",
            "content": f"Subagent result:\n{json.dumps(subagent_result, indent=2)}"
        }]
    )
    return response.content[0].input


# ─────────────────────────────────────────────
# Demonstration
# ─────────────────────────────────────────────
def main():
    print("=== Anti-pattern 1: generic string on timeout ===")
    print(repr(anti_pattern_generic_string(simulate_timeout=True)))
    print("-> coordinator has no idea if this is retryable, or if any partial data exists.\n")

    print("=== Anti-pattern 2: silently-empty 'success' on timeout ===")
    print(json.dumps(anti_pattern_silent_empty_success(simulate_timeout=True), indent=2))
    print("-> looks identical to a genuine zero-match query. The failure is invisible.\n")

    print("=== Correct pattern: structured error context ===")
    failing_result = subagent_search("AI adoption in independent film production, 2024-2026", simulate_timeout=True)
    print(json.dumps(failing_result, indent=2))

    print("\n=== Coordinator reasoning over the structured error ===")
    decision = coordinator_recover(failing_result)
    print(json.dumps(decision, indent=2))

    print("\n=== For comparison: a genuine success (not conflated with error) ===")
    success_result = subagent_search("AI adoption in music production, 2024-2026", simulate_timeout=False)
    print(json.dumps(success_result, indent=2))
    decision2 = coordinator_recover(success_result)
    print(json.dumps(decision2, indent=2))


if __name__ == "__main__":
    main()
