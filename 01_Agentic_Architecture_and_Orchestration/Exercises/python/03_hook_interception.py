"""
Exercise 3 — Hook-Style Tool Call Interception & Result Normalization
Domain: Agentic Architecture & Orchestration (Task 1.5, plus the
enforcement half of Task 1.4)

Covers:
  - A PreToolUse-style hook: inspects an outgoing tool call BEFORE it
    executes and can block it — used here to enforce "refunds over $500
    require human approval" as a deterministic guarantee, not a prompt
    suggestion the model might skip.
  - A PostToolUse-style hook: inspects a tool's RESULT after execution but
    before it re-enters the model's context — used here to normalize
    heterogeneous formats (a Unix timestamp, an ISO 8601 string, and a
    numeric HTTP-style status code) into one consistent shape.

IMPORTANT — how this maps to the Claude Agent SDK in production:
  This file implements both hooks as plain Python functions called from a
  manual agentic loop, because these exercises target the raw Anthropic
  SDK. In the Claude Agent SDK, this exact pattern is a first-class
  feature: a `PreToolUse` hook can return a "deny" decision to block a
  tool call before it runs, and a `PostToolUse` hook can rewrite the tool
  result before Claude ever sees it. The reason to reach for hooks (here
  or in the SDK) instead of a system-prompt instruction is the same in
  both cases: hooks give a DETERMINISTIC guarantee — the code runs every
  single time, unconditionally — while a prompt instruction is
  PROBABILISTIC and has a non-zero chance of being skipped.
"""

import json
from datetime import datetime, timezone
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5"

REFUND_APPROVAL_THRESHOLD = 500

TOOLS = [
    {
        "name": "process_refund",
        "description": "Issue a refund for an order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "amount": {"type": "number"},
            },
            "required": ["order_id", "amount"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": "Hand off to a human agent for cases exceeding autonomous authority.",
        "input_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
            "required": ["summary"],
        },
    },
    {
        "name": "lookup_order",
        "description": "Retrieve order details, including status and last-update time.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
]


# --- Mock backend: deliberately returns heterogeneous formats, as if it
# were fronting two different legacy systems behind one MCP tool. ---------

def _mock_lookup_order(order_id: str) -> dict:
    if order_id == "A1029":
        return {
            "order_id": "A1029",
            "status_code": 200,               # numeric status, not a label
            "last_updated": 1732492800,        # Unix timestamp, not ISO 8601
        }
    return {"order_id": order_id, "status_code": 404, "last_updated": None}


def _mock_process_refund(order_id: str, amount: float) -> dict:
    return {"refund_id": "rfd_9001", "order_id": order_id, "amount": amount, "status_code": 200}


# --- Hook 1 (PreToolUse-style): outgoing tool call interception ---------

def pre_tool_use_hook(tool_name: str, tool_input: dict) -> dict | None:
    """Runs BEFORE a tool executes. Returning a dict means "blocked" — the
    tool is never called, and the returned dict becomes the tool_result
    instead, redirecting the model toward an allowed alternative.

    This is a deterministic gate: no phrasing of "please don't approve
    refunds over $500" in the system prompt can be as reliable as code
    that runs unconditionally on every process_refund call.
    """
    if tool_name == "process_refund" and tool_input.get("amount", 0) > REFUND_APPROVAL_THRESHOLD:
        return {
            "is_error": True,
            # "message" here is the blocked-tool payload; it is separate from
            # the tool_result wrapper's own "content" field set in run_agent().
            "message": (
                f"BLOCKED by policy hook: refunds over ${REFUND_APPROVAL_THRESHOLD} "
                "require human approval. Call escalate_to_human with a "
                "structured summary (customer, order, amount, reason) instead."
            ),
        }
    return None  # not blocked


# --- Hook 2 (PostToolUse-style): result normalization --------------------

def post_tool_use_hook(tool_name: str, raw_result: dict) -> dict:
    """Runs AFTER a tool executes, BEFORE the result is appended to the
    conversation. Normalizes heterogeneous formats from the (mock)
    backend so the model always reasons over one consistent shape,
    regardless of which underlying system actually answered the call."""
    result = dict(raw_result)

    status_map = {200: "success", 404: "not_found", 409: "conflict", 500: "error"}
    if isinstance(result.get("status_code"), int):
        result["status"] = status_map.get(result["status_code"], "unknown")
        del result["status_code"]

    if isinstance(result.get("last_updated"), (int, float)):
        result["last_updated"] = datetime.fromtimestamp(
            result["last_updated"], tz=timezone.utc
        ).isoformat()

    return result


def execute_tool_with_hooks(name: str, tool_input: dict) -> dict:
    """The harness's single execution entry point: PreToolUse hook, then
    the real call (only if not blocked), then PostToolUse hook."""
    blocked = pre_tool_use_hook(name, tool_input)
    if blocked is not None:
        print(f"  [PreToolUse hook] blocked {name}({tool_input})")
        return blocked

    if name == "process_refund":
        raw = _mock_process_refund(**tool_input)
    elif name == "lookup_order":
        raw = _mock_lookup_order(**tool_input)
    elif name == "escalate_to_human":
        raw = {"escalation_id": "esc_2210", "status_code": 200}
    else:
        raw = {"error": f"Unknown tool: {name}"}

    normalized = post_tool_use_hook(name, raw)
    print(f"  [PostToolUse hook] {name} raw={raw} -> normalized={normalized}")
    return normalized


def run_agent(task: str) -> str:
    messages = [{"role": "user", "content": task}]
    print(f"Task: {task}\n{'-' * 60}")

    for _ in range(6):  # safety-net cap; primary stop is still stop_reason
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=(
                "You are a support agent. Look up orders before acting on "
                "them. If a refund is blocked by policy, escalate to a "
                "human with a structured summary instead of retrying."
            ),
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if b.type == "text"), "")

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n-> {block.name}({block.input})")
                    result = execute_tool_with_hooks(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                        "is_error": bool(result.get("is_error")),
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        return f"Unexpected stop_reason: {response.stop_reason}"

    return "[SAFETY NET TRIGGERED] exceeded max turns"


if __name__ == "__main__":
    print("=== Case 1: refund within policy ===")
    print(run_agent("Look up order A1029 and refund $50 for a late delivery."))

    print("\n\n=== Case 2: refund blocked by policy hook ===")
    print(run_agent("Look up order A1029 and refund $750 — customer wants a full refund."))
