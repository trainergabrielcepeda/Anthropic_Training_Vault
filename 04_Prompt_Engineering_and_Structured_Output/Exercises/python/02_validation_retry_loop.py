"""
Exercise 2 — Validation, Retry, and Feedback Loops (Task 4.4)
Domain: Prompt Engineering & Structured Output

Covers:
  - A semantic validation check that tool_use / JSON-schema compliance
    CANNOT catch on its own (line items not summing to the stated total)
  - Retry-with-error-feedback: appending the SPECIFIC validation error
    to the next request so the model can self-correct
  - Recognizing the case where retrying will NOT help, because the
    required information is genuinely absent from the source document
    (not a format problem — an absence problem)
"""

import anthropic

client = anthropic.Anthropic()

EXTRACT_INVOICE_TOOL = {
    "name": "extract_invoice",
    "description": "Record structured fields extracted from an invoice.",
    "input_schema": {
        "type": "object",
        "properties": {
            "vendor_name": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"}
                    },
                    "required": ["description", "amount"]
                }
            },
            "stated_total": {"type": "number"},
            "purchase_order_number": {
                "type": ["string", "null"],
                "description": "PO number, or null if not present in the document."
            }
        },
        "required": ["vendor_name", "line_items", "stated_total"]
    }
}

# This invoice is deliberately malformed in a way a model can plausibly
# mis-extract on the first pass (the "Rush fee" line is easy to miss
# because it's on its own line without a clear "Item:" label) — a
# FORMAT/STRUCTURAL issue, which retry-with-feedback CAN fix.
INVOICE_WITH_FIXABLE_ISSUE = """
INVOICE #4471 — Sunrise Logistics LLC
  Freight handling ................. $310.00
  Fuel surcharge .................... $45.00
  Rush fee
    (applied for same-day dispatch)... $60.00
TOTAL DUE: $415.00
"""

# This invoice genuinely never states a PO number anywhere. No amount
# of retrying will produce one — the correct behavior is to accept
# purchase_order_number = null, not keep re-asking.
INVOICE_WITHOUT_PO_NUMBER = """
INVOICE — Cedar Grove Office Supply
  Paper (10 reams) .................. $65.00
  Toner cartridges (x2) ............. $140.00
TOTAL DUE: $205.00
"""


def validate_semantics(extraction: dict) -> str | None:
    """Returns a specific error string, or None if the extraction is valid.

    This is exactly the layer tool_use/JSON-schema enforcement does NOT
    provide: the schema is satisfied (right types, right shape) but the
    values may still be semantically wrong.
    """
    computed = sum(item["amount"] for item in extraction["line_items"])
    stated = extraction["stated_total"]
    if abs(computed - stated) > 0.01:
        return (
            f"Line items sum to {computed:.2f}, but stated_total is {stated:.2f}. "
            f"Re-read the document for a line item you may have missed or misread."
        )
    return None


def extract_with_retry(document_text: str, max_retries: int = 2) -> dict:
    messages = [{
        "role": "user",
        "content": f"Extract the invoice fields from this document:\n\n{document_text}"
    }]

    for attempt in range(max_retries + 1):
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=[EXTRACT_INVOICE_TOOL],
            tool_choice={"type": "tool", "name": "extract_invoice"},
            messages=messages,
        )
        tool_block = next(b for b in response.content if b.type == "tool_use")
        result = tool_block.input

        error = validate_semantics(result)
        if error is None:
            print(f"  [attempt {attempt + 1}] validation passed")
            return result

        print(f"  [attempt {attempt + 1}] validation FAILED: {error}")
        if attempt == max_retries:
            print("  [giving up] max retries exhausted")
            return result

        # Retry-with-error-feedback: send back the assistant's own tool
        # call, then a tool_result containing the SPECIFIC error — not
        # a generic "please try again." The model can now re-read the
        # same source with a concrete thing to check.
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": f"Validation failed: {error}",
                "is_error": True,
            }],
        })

    return result


def demonstrate_retry_that_helps():
    print("=== Case A: format/structural error — retry CAN help ===\n")
    result = extract_with_retry(INVOICE_WITH_FIXABLE_ISSUE)
    print(f"\nFinal extraction: {result}\n")


def demonstrate_retry_that_cannot_help():
    print("=== Case B: info genuinely absent from source — retry CANNOT help ===\n")
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[EXTRACT_INVOICE_TOOL],
        tool_choice={"type": "tool", "name": "extract_invoice"},
        messages=[{
            "role": "user",
            "content": f"Extract the invoice fields from this document:\n\n{INVOICE_WITHOUT_PO_NUMBER}"
        }],
    )
    tool_block = next(b for b in response.content if b.type == "tool_use")
    result = tool_block.input
    po = result.get("purchase_order_number")
    print(f"purchase_order_number extracted as: {po!r}")
    print(
        "Correct outcome is null/None here — the document never states a PO number.\n"
        "Retrying with 'the PO number field is empty, please try again' would NOT\n"
        "produce a real PO number; it would just pressure the model to fabricate one.\n"
        "The nullable field (Task 4.3) plus accepting null (Task 4.4) is the fix,\n"
        "not a retry loop."
    )


if __name__ == "__main__":
    demonstrate_retry_that_helps()
    print()
    demonstrate_retry_that_cannot_help()
