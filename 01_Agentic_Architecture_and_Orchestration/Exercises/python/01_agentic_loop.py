"""
Exercise 1 — The Agentic Loop, Keyed Off stop_reason
Domain: Agentic Architecture & Orchestration (Task 1.1)

Covers:
  - The lifecycle: send request -> inspect stop_reason -> execute tools ->
    return results for the next iteration
  - Terminating on "end_turn", continuing on "tool_use" — stop_reason is the
    ONLY control-flow signal used here, never assistant text content
  - Appending the full assistant turn (including tool_use blocks) and a
    single user turn with all tool_result blocks, so the model can reason
    about results on the next iteration
  - A max-iteration circuit breaker used ONLY as a safety net, never as the
    primary stopping mechanism (see the anti-pattern callout below)

Scenario: a minimal version of the Customer Support Resolution Agent from
the exam guide (get_customer, lookup_order, process_refund, escalate_to_human).
"""

import json
import anthropic

client = anthropic.Anthropic()

MODEL = "claude-sonnet-5"

# Safety net only — NOT the primary stop condition. The primary stop
# condition is response.stop_reason == "end_turn". This cap exists purely
# to prevent a genuinely stuck loop from running forever and to give us
# something to alert on.
MAX_ITERATIONS = 12

TOOLS = [
    {
        "name": "get_customer",
        "description": (
            "Look up and verify a customer's identity by email or phone. "
            "Call this BEFORE lookup_order or process_refund — those tools "
            "require a verified customer_id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "identifier": {"type": "string", "description": "Customer email or phone number"},
            },
            "required": ["identifier"],
        },
    },
    {
        "name": "lookup_order",
        "description": "Retrieve order details by order ID for a verified customer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "customer_id": {"type": "string"},
            },
            "required": ["order_id", "customer_id"],
        },
    },
    {
        "name": "process_refund",
        "description": "Issue a refund for an order. Requires a verified customer_id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "customer_id": {"type": "string"},
                "amount": {"type": "number"},
                "reason": {"type": "string"},
            },
            "required": ["order_id", "customer_id", "amount", "reason"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": "Hand off to a human agent with a structured summary. Use for policy exceptions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Structured handoff: customer, root cause, recommendation"},
            },
            "required": ["summary"],
        },
    },
]

# --- Mock backend -----------------------------------------------------

_MOCK_CUSTOMERS = {"jane@example.com": "cust_4471"}
_MOCK_ORDERS = {"A1029": {"order_id": "A1029", "status": "delivered", "total": 42.50}}


def execute_tool(name: str, tool_input: dict) -> dict:
    """Runs a single tool call and returns a JSON-serializable result.
    This is the harness's execution step — Claude only ever REQUESTS a
    tool call via a tool_use block; your code decides how to fulfill it."""
    if name == "get_customer":
        customer_id = _MOCK_CUSTOMERS.get(tool_input["identifier"])
        if customer_id:
            return {"verified": True, "customer_id": customer_id}
        return {"verified": False, "error": "No matching customer found"}

    if name == "lookup_order":
        order = _MOCK_ORDERS.get(tool_input["order_id"])
        if order:
            return order
        return {"error": f"Order {tool_input['order_id']} not found"}

    if name == "process_refund":
        return {
            "refund_id": "rfd_9001",
            "status": "processed",
            "amount": tool_input["amount"],
        }

    if name == "escalate_to_human":
        return {"escalation_id": "esc_2210", "status": "queued_for_human_review"}

    return {"error": f"Unknown tool: {name}"}


def run_agent(task: str) -> str:
    messages = [{"role": "user", "content": task}]
    print(f"\nTask: {task}\n{'-' * 60}")

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n[iteration {iteration}]")

        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=(
                "You are a customer support resolution agent. Always verify "
                "identity with get_customer before calling lookup_order or "
                "process_refund. Escalate policy exceptions rather than "
                "guessing."
            ),
            tools=TOOLS,
            messages=messages,
        )

        print(f"stop_reason: {response.stop_reason}")

        # Append the FULL assistant turn — including tool_use blocks, not
        # just extracted text. Dropping tool_use blocks here breaks the
        # tool_use_id pairing the API expects on the next request.
        messages.append({"role": "assistant", "content": response.content})

        # --- PRIMARY termination signal ---
        # We branch on stop_reason, never on the presence/absence of
        # particular words in response text. That would be an anti-pattern:
        # phrasing varies, and a model discussing why it ISN'T done yet can
        # accidentally contain the same trigger words.
        if response.stop_reason == "end_turn":
            final_text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            print("-" * 60)
            return final_text

        if response.stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            tool_results = []

            for block in tool_use_blocks:
                print(f"  -> {block.name}({block.input})")
                result = execute_tool(block.name, block.input)
                print(f"  <- {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            # All tool_result blocks from this turn go back as ONE user
            # message — not one message per tool call. This is what feeds
            # the results into context so Claude can reason about them on
            # the next iteration.
            messages.append({"role": "user", "content": tool_results})
            continue

        # Any other stop_reason (max_tokens, pause_turn, refusal, ...) is
        # handled explicitly rather than silently looping.
        return f"Stopped with unexpected stop_reason: {response.stop_reason}"

    # We only get here if we exhausted MAX_ITERATIONS without an end_turn.
    # This is an anomaly to investigate, not a successful completion —
    # treating it as "the answer" is exactly the anti-pattern this
    # exercise is designed to avoid.
    return (
        f"[SAFETY NET TRIGGERED] Agent did not reach end_turn within "
        f"{MAX_ITERATIONS} iterations. Escalate for investigation."
    )


if __name__ == "__main__":
    result = run_agent(
        "Hi, this is jane@example.com. Can you check the status of order "
        "A1029 and refund me $42.50 since it never arrived?"
    )
    print(f"\nFinal Answer:\n{result}")
