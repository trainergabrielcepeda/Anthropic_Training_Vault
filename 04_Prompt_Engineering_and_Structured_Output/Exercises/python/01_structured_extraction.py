"""
Exercise 1 — Structured Extraction via tool_use (Task 4.3)
Domain: Prompt Engineering & Structured Output

Covers:
  - Defining an extraction tool with a JSON schema as its input_schema
  - required vs optional/nullable fields (don't force fabrication on
    fields the source document doesn't have)
  - enum field with an "other" + free-text detail escape hatch
  - forcing a specific tool via tool_choice so it's guaranteed to run
  - reading the extracted data straight from the tool_use response
    block (no string/JSON parsing needed)
"""

import json
import anthropic

client = anthropic.Anthropic()

# A receipt that has no listed due date and a vendor category that
# doesn't cleanly fit a fixed enum bucket — on purpose, to exercise
# the nullable field and the "other" + detail pattern.
RECEIPT_TEXT = """
RECEIPT — Riverside Print & Signage Co.
Date: 2026-06-02
Items:
  - Vinyl banner, 6ft x 3ft ......... $84.00
  - Rush production fee ............. $25.00
Total: $109.00
(No due date listed — paid in full at time of purchase.)
"""

EXTRACT_RECEIPT_TOOL = {
    "name": "extract_receipt",
    "description": "Record structured fields extracted from a purchase receipt.",
    "input_schema": {
        "type": "object",
        "properties": {
            "vendor_name": {
                "type": "string",
                "description": "The name of the business that issued the receipt."
            },
            "purchase_date": {
                "type": "string",
                "description": "ISO 8601 date (YYYY-MM-DD) the purchase was made."
            },
            "line_items": {
                "type": "array",
                "description": "Each individual charge on the receipt.",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"}
                    },
                    "required": ["description", "amount"]
                }
            },
            "stated_total": {
                "type": "number",
                "description": "The total amount printed on the receipt."
            },
            "due_date": {
                # Nullable: many receipts (paid-in-full, point-of-sale)
                # simply have no due date. Making this required would
                # pressure the model to invent one.
                "type": ["string", "null"],
                "description": "ISO 8601 date, or null if the receipt has no due date (e.g. paid in full)."
            },
            "category": {
                "type": "string",
                "enum": ["utilities", "software", "travel", "office_supplies", "other"],
                "description": "Best-fit spend category. Use 'other' if none of the fixed values fit."
            },
            "category_detail": {
                "type": ["string", "null"],
                "description": "Required when category is 'other': a short free-text description of the actual category. Null otherwise."
            }
        },
        "required": ["vendor_name", "purchase_date", "line_items", "stated_total", "category"]
    }
}


def extract_receipt(receipt_text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[EXTRACT_RECEIPT_TOOL],
        # Forced tool choice: we already know which schema applies
        # (a single receipt type), so we force the specific tool
        # rather than using "any" — see 4.3 notes on tool_choice modes.
        tool_choice={"type": "tool", "name": "extract_receipt"},
        messages=[{
            "role": "user",
            "content": f"Extract the receipt fields from this document:\n\n{receipt_text}"
        }],
    )

    # Structured output guarantee: the model MUST have called our tool.
    # No regex, no json.loads() on free text — the block's `.input` is
    # already a schema-shaped dict.
    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    return tool_use_block.input


def main():
    print("=== Structured Extraction via tool_use ===\n")
    result = extract_receipt(RECEIPT_TEXT)
    print(json.dumps(result, indent=2))

    print("\n--- What to notice ---")
    print(f"due_date came back as: {result.get('due_date')!r}  (nullable field — no fabrication)")
    print(f"category came back as: {result.get('category')!r}")
    if result.get("category") == "other":
        print(f"category_detail: {result.get('category_detail')!r}  ('other' + detail pattern)")

    # Schema compliance does NOT mean semantic correctness — tool_use
    # guarantees the shape, not that the numbers add up. See
    # 02_validation_retry_loop.py for the semantic-validation layer.
    line_item_sum = sum(item["amount"] for item in result["line_items"])
    stated = result["stated_total"]
    print(f"\nline items sum to {line_item_sum}, stated_total is {stated} "
          f"({'OK' if abs(line_item_sum - stated) < 0.01 else 'MISMATCH — see Exercise 2'})")


if __name__ == "__main__":
    main()
