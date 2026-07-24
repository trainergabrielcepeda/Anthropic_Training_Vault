"""
Exercise 1 — Case-Facts Extraction Pattern
Domain: Context Management & Reliability (Task 5.1)

Problem this demonstrates:
  A `lookup_order` tool returns 40+ fields (warehouse codes, carrier
  metadata, audit timestamps...) when only a handful matter for the
  conversation. If the full raw JSON is appended to conversation
  history on every turn, it accumulates tokens far out of proportion
  to its relevance, and numeric/date details risk being lost later if
  the history is ever summarized.

Pattern:
  1. Call the tool, get the verbose result.
  2. Immediately extract only the fields that matter into a small
     structured "case facts" block (via forced tool use, so the shape
     is guaranteed).
  3. Re-inject that small block into every subsequent prompt, kept
     OUTSIDE the (potentially summarized) conversation history — never
     let the case facts themselves pass through a summarizer.
  4. Discard the 40-field raw payload; it never needs to enter context
     again once the relevant facts are captured.
"""

import json
import anthropic

client = anthropic.Anthropic()

MODEL = "claude-haiku-4-5-20251001"  # cheap, fast — a pure extraction task


# ─────────────────────────────────────────────
# Simulated backend: a verbose order lookup
# ─────────────────────────────────────────────
def mock_lookup_order(order_id: str) -> dict:
    """Stands in for a real MCP tool call. Real order-lookup APIs commonly
    return this many fields — most of them irrelevant to a refund conversation."""
    return {
        "order_id": order_id,
        "order_date": "2026-07-02",
        "promised_delivery": "2026-07-09",
        "actual_delivery": "2026-07-14",
        "amount_charged": 214.50,
        "currency": "USD",
        "customer_id": "cust_88213",
        "customer_email": "j.rivera@example.com",
        "shipping_carrier": "FastFreight",
        "shipping_service_level": "ground-economy",
        "warehouse_code": "WH-EAST-04",
        "warehouse_zone": "B12",
        "picking_batch_id": "PB-2026-07-02-0091",
        "packing_station": "PS-7",
        "audit_created_ts": "2026-07-02T14:03:11Z",
        "audit_updated_ts": "2026-07-14T09:22:47Z",
        "payment_method": "visa_ending_4471",
        "payment_processor_ref": "txn_9f8a2b1c",
        "loyalty_points_earned": 21,
        "loyalty_points_redeemed": 0,
        "gift_wrap": False,
        "internal_routing_notes": "rerouted via hub 3 due to weather delay",
        "sku_list": ["SKU-1123", "SKU-1124", "SKU-1125"],
        "tax_amount": 17.16,
        "discount_code_applied": None,
        "fraud_score": 0.02,
        "return_window_days": 30,
        # ... a real payload would keep going for another 15-20 fields
    }


# ─────────────────────────────────────────────
# Structured extraction: only the fields that matter for THIS task
# ─────────────────────────────────────────────
CASE_FACTS_TOOL = [{
    "name": "record_case_facts",
    "description": (
        "Record only the order facts relevant to a delivery-delay refund "
        "conversation. Ignore all other fields in the source data."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id":           {"type": "string"},
            "order_date":         {"type": "string", "description": "YYYY-MM-DD"},
            "promised_delivery":  {"type": "string", "description": "YYYY-MM-DD"},
            "actual_delivery":    {"type": "string", "description": "YYYY-MM-DD"},
            "amount_charged":     {"type": "number"},
        },
        "required": ["order_id", "order_date", "promised_delivery", "actual_delivery", "amount_charged"]
    }
}]


def extract_case_facts(raw_order: dict) -> dict:
    """Force-extract a small, relevant subset of a verbose tool result."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        tools=CASE_FACTS_TOOL,
        tool_choice={"type": "tool", "name": "record_case_facts"},
        messages=[{
            "role": "user",
            "content": f"Extract the delivery-delay-relevant case facts from this order record:\n{json.dumps(raw_order)}"
        }]
    )
    tool_block = response.content[0]
    return tool_block.input


def render_case_facts_block(facts: dict, customer_ask: str, issue_status: str) -> str:
    """The small, persistent block that gets re-injected into every prompt —
    kept separate from (and never subjected to) summarized conversation history."""
    lines = ["CASE FACTS (persistent — do not summarize):"]
    for key, value in facts.items():
        lines.append(f"- {key}: {value}")
    lines.append(f"- customer_ask: {customer_ask}")
    lines.append(f"- issue_status: {issue_status}")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Demonstration
# ─────────────────────────────────────────────
def main():
    print("=== Step 1: Verbose raw tool result (what NOT to keep re-sending) ===")
    raw = mock_lookup_order("8841203")
    print(f"{len(raw)} fields returned by the tool call.\n")

    print("=== Step 2: Extract only the relevant fields into case facts ===")
    facts = extract_case_facts(raw)
    print(json.dumps(facts, indent=2))

    print("\n=== Step 3: Persistent case-facts block (re-injected every turn) ===")
    block = render_case_facts_block(
        facts,
        customer_ask="15% partial refund for the 5-day delivery delay",
        issue_status="open, awaiting policy check",
    )
    print(block)

    print("\n=== Step 4: Using the block in a follow-up turn ===")
    print("Instead of resending all 25 raw fields, only this ~7-line block")
    print("plus the current user message is needed to reason about the case:\n")
    follow_up = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=(
            "You are a support agent. Use ONLY the case facts below to answer. "
            "Do not invent details not present in the case facts.\n\n" + block
        ),
        messages=[{"role": "user", "content": "How many days late was this delivery?"}]
    )
    print(follow_up.content[0].text)


if __name__ == "__main__":
    main()
