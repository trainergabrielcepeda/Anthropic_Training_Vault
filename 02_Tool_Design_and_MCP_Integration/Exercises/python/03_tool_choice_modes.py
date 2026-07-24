"""
Exercise 3 -- tool_choice Modes & Tool Distribution
Domain 2, Task 2.3: Distribute tools appropriately across agents and
configure tool choice.

Demonstrates the three tool_choice modes:
  {"type": "auto"}                    -- Claude decides whether/which tool to call (default)
  {"type": "any"}                     -- Claude must call SOME tool, but picks which one
  {"type": "tool", "name": "..."}     -- Claude must call this EXACT tool

Scenario: a small document-processing pipeline with three SCOPED tools
(not eighteen -- see Theory/02_Error_Handling_and_Tool_Distribution.md on why
tool count matters). extract_metadata must always run first (forced), the
next step is chosen freely in a follow-up turn ("auto"), and a final
classification step must produce a tool call rather than prose ("any").
"""

import json
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5"

TOOLS = [
    {
        "name": "extract_metadata",
        "description": "Extract title, author, and date from a raw document. Always run this first on any new document, before translation or classification.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "translate_text",
        "description": "Translate document text into another language. Use only after metadata has already been extracted.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "target_language": {"type": "string"},
            },
            "required": ["text", "target_language"],
        },
    },
    {
        "name": "classify_topic",
        "description": "Classify a document's primary topic into one of a fixed set of categories.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "category": {
                    "type": "string",
                    "enum": ["finance", "legal", "engineering", "marketing", "other"],
                },
            },
            "required": ["text", "category"],
        },
    },
]

DOCUMENT = (
    "Q3 2026 Financial Summary\nBy J. Alvarez, Finance Dept, 2026-10-01\n\n"
    "Revenue grew 12% quarter over quarter to $4.2M, driven primarily by "
    "international expansion in the APAC region."
)


def mock_execute(name: str, tool_input: dict) -> str:
    """Mock execution -- would dispatch to real tool implementations."""
    return json.dumps({"tool": name, "received": tool_input})


def step_1_forced_tool_choice():
    """FORCED: guarantee extract_metadata runs first, regardless of what
    Claude might otherwise pick, even with other tools in scope."""
    print("\n=== Step 1: forced tool_choice ({'type': 'tool', 'name': 'extract_metadata'}) ===")
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        tools=TOOLS,
        tool_choice={"type": "tool", "name": "extract_metadata"},
        messages=[{"role": "user", "content": DOCUMENT}],
    )
    block = next(b for b in response.content if b.type == "tool_use")
    print(f"  Forced call: {block.name}({block.input})")
    return response, block


def step_2_auto_followup(first_response, metadata_block):
    """AUTO: once metadata is extracted, let Claude freely decide the next
    step -- translate_text, classify_topic, or plain text -- in a follow-up
    turn. This is where forced tool_choice hands control back to the model."""
    print("\n=== Step 2: tool_choice 'auto' for the follow-up turn ===")
    messages = [
        {"role": "user", "content": DOCUMENT},
        {"role": "assistant", "content": first_response.content},
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": metadata_block.id,
            "content": mock_execute(metadata_block.name, metadata_block.input),
        }]},
    ]
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        tools=TOOLS,
        tool_choice={"type": "auto"},
        messages=messages,
    )
    print(f"  stop_reason: {response.stop_reason}")
    for b in response.content:
        if b.type == "tool_use":
            print(f"  Claude chose: {b.name}({b.input})")
        elif b.type == "text":
            print(f"  Claude said: {b.text[:150]}")


def step_3_any_guarantees_tool_call():
    """ANY: guarantee a tool call happens (vs. a conversational text reply),
    without dictating which of the available tools it must be."""
    print("\n=== Step 3: tool_choice 'any' ===")
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        tools=TOOLS,
        tool_choice={"type": "any"},
        messages=[{
            "role": "user",
            "content": f"This document is clearly about finance. Classify it.\n\n{DOCUMENT}",
        }],
    )
    block = next((b for b in response.content if b.type == "tool_use"), None)
    if block:
        print(f"  Guaranteed tool call: {block.name}({block.input})")
    else:
        print("  Unexpected: no tool_use block returned despite tool_choice='any'")


if __name__ == "__main__":
    first_response, metadata_block = step_1_forced_tool_choice()
    step_2_auto_followup(first_response, metadata_block)
    step_3_any_guarantees_tool_call()
