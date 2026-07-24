"""
Exercise 1 -- Tool Description Quality & Selection Reliability
Domain 2, Task 2.1: Design effective tool interfaces with clear descriptions
and boundaries.

Demonstrates:
  Part A: Two tools with vague, overlapping descriptions ("analyze_content" vs
          "analyze_document") give Claude nothing to disambiguate between them,
          so routing across similar queries is unreliable.
  Part B: The same capability, redesigned as three purpose-specific tools with
          differentiated names and descriptions (input format, example
          queries, explicit exclusions), routes consistently.

This mirrors the official CCAR-F exam guide's sample question about
`get_customer` vs `lookup_order`: the fix for misrouting is almost always a
description rewrite -- not a routing classifier, not few-shot examples, and
not immediately merging the tools.
"""

import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5"

SAMPLE_DOC = (
    "Q3 2026 Financial Summary. Revenue grew 12% quarter over quarter to "
    "$4.2M. The board concluded that international expansion drove the "
    "majority of new growth, though the underlying regional breakdown shows "
    "growth was concentrated almost entirely in the APAC region."
)

# ── Part A: Ambiguous, overlapping tools ─────────────────────────────
AMBIGUOUS_TOOLS = [
    {
        "name": "analyze_content",
        "description": "Analyzes content and provides insights.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "analyze_document",
        "description": "Analyzes a document and returns information.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
]

# ── Part B: Purpose-specific tools with differentiated descriptions ──
DIFFERENTIATED_TOOLS = [
    {
        "name": "summarize_content",
        "description": (
            "Condense a long text into a short summary of its main points. "
            "Use when the user asks to summarize, give an overview of, or "
            "list key takeaways from a document. Input: raw text. Output: a "
            "3-5 bullet summary. Do NOT use this to pull out a single "
            "specific figure (use extract_data_points) or to check whether a "
            "claim is supported by the text (use verify_claim_against_source)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The full document text to summarize."}
            },
            "required": ["text"],
        },
    },
    {
        "name": "extract_data_points",
        "description": (
            "Pull one or more specific, named data points (numbers, dates, "
            "names, figures) out of a document. Use when the user asks for a "
            "precise value such as 'total revenue', 'filing date', or 'CEO "
            "name'. Input: raw text plus the field to extract, e.g. "
            "field='total revenue'. Output: the exact value found, or null "
            "if not present. Do NOT use this for open-ended summarization or "
            "claim verification."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The full document text to search."},
                "field": {"type": "string", "description": "The specific data point to extract, e.g. 'total revenue'."},
            },
            "required": ["text", "field"],
        },
    },
    {
        "name": "verify_claim_against_source",
        "description": (
            "Check whether a specific claim or conclusion is actually "
            "supported by the evidence in a document. Use when the user asks "
            "'does X follow from this', 'is this claim accurate', or "
            "'fact-check this against the source'. Input: raw text plus the "
            "claim to check. Output: supported / contradicted / not "
            "addressed, with the supporting excerpt. Do NOT use this for "
            "general summarization or simple data extraction."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The full document text to check against."},
                "claim": {"type": "string", "description": "The specific claim or conclusion to verify."},
            },
            "required": ["text", "claim"],
        },
    },
]

TEST_QUERIES = [
    "Summarize the three main points of this quarterly report.",
    "Pull out the exact total revenue figure stated in this report.",
    "Does the conclusion about international expansion actually follow from the regional breakdown described?",
]


def show_routing(tools, label):
    print(f"\n=== {label} ===")
    for query in TEST_QUERIES:
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            tools=tools,
            tool_choice={"type": "any"},  # force a tool call so routing is always visible
            messages=[{"role": "user", "content": f"{query}\n\nDocument:\n{SAMPLE_DOC}"}],
        )
        chosen = next((b.name for b in response.content if b.type == "tool_use"), "NONE")
        print(f"  Query: {query}")
        print(f"    -> routed to: {chosen}")


if __name__ == "__main__":
    show_routing(AMBIGUOUS_TOOLS, "Part A: Ambiguous tools (analyze_content vs analyze_document)")
    show_routing(DIFFERENTIATED_TOOLS, "Part B: Differentiated, purpose-specific tools")
    print(
        "\nNote: Part A's routing may be inconsistent or arbitrary from run to "
        "run -- that unpredictability IS the bug the description rewrite in "
        "Part B is meant to fix. Part B's tools each state their input "
        "format, a trigger example, and an explicit exclusion, which is what "
        "gives Claude a reliable basis for choosing between them."
    )
