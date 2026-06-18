"""
Exercise 2 — Multiple Tools
Topic: Tool Use & Function Calling

Covers:
  - Multiple tools in one request
  - Parallel tool calls (Claude calls two tools in one response)
  - Forced tool use with tool_choice
  - Using a "fake" tool to extract structured data
"""

import json
import anthropic

client = anthropic.Anthropic()

# ─────────────────────────────────────────────
# Tool Definitions
# ─────────────────────────────────────────────
TOOLS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_exchange_rate",
        "description": "Get the current exchange rate between two currencies.",
        "input_schema": {
            "type": "object",
            "properties": {
                "from_currency": {"type": "string", "description": "e.g. USD"},
                "to_currency":   {"type": "string", "description": "e.g. EUR"}
            },
            "required": ["from_currency", "to_currency"]
        }
    },
    {
        "name": "search_flights",
        "description": "Search for available flights between two cities on a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin":      {"type": "string"},
                "destination": {"type": "string"},
                "date":        {"type": "string", "description": "YYYY-MM-DD"}
            },
            "required": ["origin", "destination", "date"]
        }
    }
]


def mock_execute(name: str, inputs: dict) -> str:
    if name == "get_weather":
        return json.dumps({"city": inputs["city"], "temp": "21°C", "condition": "sunny"})
    if name == "get_exchange_rate":
        return json.dumps({"rate": 0.92, "from": inputs["from_currency"], "to": inputs["to_currency"]})
    if name == "search_flights":
        return json.dumps({"flights": [
            {"airline": "AF", "departs": "08:30", "price": "$450"},
            {"airline": "BA", "departs": "14:00", "price": "$380"}
        ]})
    return "Unknown tool"


def run_agent(user_message: str, tools=TOOLS, tool_choice=None) -> str:
    messages = [{"role": "user", "content": user_message}]
    print(f"\nUser: {user_message}\n")
    kwargs = {"tools": tools}
    if tool_choice:
        kwargs["tool_choice"] = tool_choice

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=messages,
            **kwargs
        )
        print(f"[stop_reason: {response.stop_reason}]")

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"  → {block.name}({block.input})")
                    result = mock_execute(block.name, block.input)
                    print(f"  ← {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})


# ─────────────────────────────────────────────
# Part 1: Parallel Tool Calls
# ─────────────────────────────────────────────
def part1_parallel():
    print("\n=== Part 1: Parallel Tool Calls ===")
    answer = run_agent(
        "I'm planning a trip from New York to Paris on 2026-08-01. "
        "What's the weather in Paris and the USD to EUR exchange rate?"
    )
    print(f"\nClaude: {answer}")


# ─────────────────────────────────────────────
# Part 2: Tool Chaining (sequential)
# ─────────────────────────────────────────────
def part2_chaining():
    print("\n\n=== Part 2: Tool Chaining ===")
    answer = run_agent(
        "Find me flights from New York to Paris on 2026-08-01, "
        "then tell me what the weather will be like in Paris."
    )
    print(f"\nClaude: {answer}")


# ─────────────────────────────────────────────
# Part 3: Forced Tool Use for Structured Extraction
# ─────────────────────────────────────────────
EXTRACTION_TOOL = [{
    "name": "record_trip_details",
    "description": "Record the extracted trip details from the user message.",
    "input_schema": {
        "type": "object",
        "properties": {
            "origin":       {"type": "string"},
            "destination":  {"type": "string"},
            "date":         {"type": "string", "description": "YYYY-MM-DD if parseable"},
            "travelers":    {"type": "integer"},
            "budget_usd":   {"type": ["number", "null"]}
        },
        "required": ["origin", "destination"]
    }
}]

def part3_extraction():
    print("\n\n=== Part 3: Structured Extraction via Forced Tool Use ===")
    user_text = "We're a group of 4 flying from London to Tokyo sometime in March, budget around $2000 each."

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        tools=EXTRACTION_TOOL,
        tool_choice={"type": "tool", "name": "record_trip_details"},
        messages=[{"role": "user", "content": user_text}]
    )

    tool_block = response.content[0]
    print(f"Extracted data:\n{json.dumps(tool_block.input, indent=2)}")


if __name__ == "__main__":
    part1_parallel()
    part2_chaining()
    part3_extraction()
