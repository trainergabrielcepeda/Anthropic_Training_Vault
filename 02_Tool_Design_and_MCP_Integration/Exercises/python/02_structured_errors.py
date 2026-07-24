"""
Exercise 2 -- Structured MCP-Style Error Responses
Domain 2, Task 2.2: Implement structured error responses for MCP tools.

Demonstrates the MCP `isError` pattern: instead of returning a flat
"Operation failed" string, a tool returns structured metadata that the
CALLING CODE -- and, once relayed as a tool_result, Claude itself -- can use
to decide how to recover:

    {
      "isError": true,
      "errorCategory": "transient" | "validation" | "business" | "permission",
      "isRetryable": bool,
      "message": "human-readable explanation"
    }

Client-side logic then branches on errorCategory instead of treating every
failure identically, and transient failures are retried LOCALLY (inside this
function) rather than always bothering the caller/coordinator.

Note: the Anthropic Messages API also has its own top-level `is_error`
boolean on a `tool_result` content block (see Part 2 below). That is a
DIFFERENT, API-level signal ("this tool call failed, adjust your response")
from the `isError` field inside our own JSON payload ("here is structured
detail about why it failed"). MCP tools typically set both: `is_error: True`
on the tool_result block, with the structured payload as its content.
"""

import json
import random
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5"


def process_refund(order_id: str, amount: float) -> dict:
    """Simulated MCP tool. Returns a structured success OR a structured error."""

    # Validation error -- bad input; retrying with the same args will never work
    if amount <= 0:
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Refund amount must be positive; received {amount}.",
        }

    # Business error -- policy violation, not a system fault, not retryable
    if amount > 500:
        return {
            "isError": True,
            "errorCategory": "business",
            "isRetryable": False,
            "message": (
                "Refunds over $500 require manager approval and cannot be "
                "processed automatically. Escalate to a human agent."
            ),
        }

    # Permission error -- the caller isn't authorized for this action
    if order_id.startswith("LOCKED-"):
        return {
            "isError": True,
            "errorCategory": "permission",
            "isRetryable": False,
            "message": f"Order {order_id} is locked pending fraud review; refunds are disabled.",
        }

    # Transient error -- simulate a flaky downstream payment service
    if random.random() < 0.3:
        return {
            "isError": True,
            "errorCategory": "transient",
            "isRetryable": True,
            "message": "Payment service timed out after 10s. Safe to retry.",
        }

    # Success -- NOT an error. Distinguish this from a valid-but-empty result:
    # a refund of $0 line items found would still be isError: False, just
    # with an empty/zero payload -- never mark "no matches" as isError.
    return {
        "isError": False,
        "orderId": order_id,
        "refundedAmount": amount,
        "status": "completed",
    }


def handle_tool_result(result: dict) -> dict:
    """Client-side recovery logic branching on errorCategory."""
    if not result.get("isError"):
        return {"action": "return_to_caller", "content": result}

    category = result["errorCategory"]

    if category == "transient" and result["isRetryable"]:
        # Local recovery: retry once without bothering the coordinator/user
        print(f"    [recovery] transient -- retrying locally: {result['message']}")
        return {"action": "retry"}

    if category == "validation":
        # Non-retryable with the SAME input, but fixable if the caller
        # (Claude, or the coordinator) supplies corrected input
        print(f"    [recovery] validation -- needs corrected input: {result['message']}")
        return {"action": "return_to_caller", "content": result}

    if category == "business":
        # Non-retryable under any input; no amount of retrying helps
        print(f"    [recovery] business rule violation -- surface as-is: {result['message']}")
        return {"action": "return_to_caller", "content": result}

    if category == "permission":
        print(f"    [recovery] permission denied -- escalate, do not retry: {result['message']}")
        return {"action": "escalate", "content": result}

    return {"action": "return_to_caller", "content": result}


def run_refund_with_recovery(order_id: str, amount: float, max_local_retries: int = 2):
    """Wraps process_refund with LOCAL retry for transient failures only,
    propagating everything else with its full structured context."""
    attempts = 0
    while True:
        attempts += 1
        result = process_refund(order_id, amount)
        decision = handle_tool_result(result)

        if decision["action"] == "retry" and attempts <= max_local_retries:
            continue
        return decision, attempts


# ── Part 1: Pure client-side recovery logic (no API call needed) ─────
def part1_local_recovery_demo():
    print("\n=== Part 1: Client-side recovery branching on errorCategory ===")
    cases = [
        ("ORD-1001", 45.00),     # likely success (or transient retry along the way)
        ("ORD-1002", -10.00),    # validation error
        ("ORD-1003", 750.00),    # business error
        ("LOCKED-9001", 20.00),  # permission error
    ]
    for order_id, amount in cases:
        print(f"\nRefund request: order={order_id} amount={amount}")
        decision, attempts = run_refund_with_recovery(order_id, amount)
        print(f"  Final action: {decision['action']} (after {attempts} attempt(s))")
        print(f"  Payload: {json.dumps(decision.get('content'), indent=2)}")


# ── Part 2: Wiring the structured error into a real Claude conversation ──
REFUND_TOOL = [{
    "name": "process_refund",
    "description": (
        "Process a refund for a given order. Returns a structured error "
        "(with errorCategory and isRetryable) if the refund cannot be "
        "completed -- explain the reason to the user based on that "
        "structured detail rather than a generic failure message."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string"},
            "amount": {"type": "number"},
        },
        "required": ["order_id", "amount"],
    },
}]


def part2_claude_sees_structured_error():
    print("\n=== Part 2: Structured error surfaced through a real tool_result ===")
    messages = [{"role": "user", "content": "Please refund $750 on order ORD-2002."}]

    response = client.messages.create(
        model=MODEL, max_tokens=400, tools=REFUND_TOOL, messages=messages
    )
    tool_block = next(b for b in response.content if b.type == "tool_use")
    messages.append({"role": "assistant", "content": response.content})

    result = process_refund(tool_block.input["order_id"], tool_block.input["amount"])

    # Two distinct signals sent back:
    #  - is_error (API-level): tells Claude this call did not succeed
    #  - the JSON payload's isError/errorCategory/isRetryable: tells Claude WHY,
    #    so its final response to the user reflects the actual reason
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": json.dumps(result),
            "is_error": result["isError"],
        }],
    })

    final = client.messages.create(model=MODEL, max_tokens=400, tools=REFUND_TOOL, messages=messages)
    for block in final.content:
        if block.type == "text":
            print(f"  Claude's response to the user:\n  {block.text}")


if __name__ == "__main__":
    part1_local_recovery_demo()
    part2_claude_sees_structured_error()
