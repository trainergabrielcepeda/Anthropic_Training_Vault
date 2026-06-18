"""
Exercise 1 — Single Tool
Topic: Tool Use & Function Calling

Covers:
  - Defining a tool schema
  - Detecting stop_reason == "tool_use"
  - Executing the tool and sending tool_result
  - The full two-turn cycle in a while loop
"""

import json
import anthropic

client = anthropic.Anthropic()

# ─────────────────────────────────────────────
# Tool Definition
# ─────────────────────────────────────────────
TOOLS = [
    {
        "name": "get_weather",
        "description": (
            "Get the current temperature and weather conditions for a city. "
            "Use this when the user asks about current weather in any location. "
            "Do NOT use for forecasts."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'Tokyo' or 'New York'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["city"]
        }
    }
]


# ─────────────────────────────────────────────
# Mock Tool Implementation
# ─────────────────────────────────────────────
def get_weather(city: str, unit: str = "celsius") -> dict:
    """Simulated weather data — replace with a real API call in production."""
    mock_data = {
        "tokyo":    {"celsius": 22, "fahrenheit": 72, "condition": "partly cloudy"},
        "paris":    {"celsius": 18, "fahrenheit": 64, "condition": "sunny"},
        "new york": {"celsius": 15, "fahrenheit": 59, "condition": "overcast"},
    }
    city_lower = city.lower()
    data = mock_data.get(city_lower, {"celsius": 20, "fahrenheit": 68, "condition": "clear"})
    temp = data[unit]
    symbol = "°C" if unit == "celsius" else "°F"
    return {"city": city, "temperature": f"{temp}{symbol}", "condition": data["condition"]}


def execute_tool(name: str, tool_input: dict) -> str:
    if name == "get_weather":
        result = get_weather(**tool_input)
        return json.dumps(result)
    raise ValueError(f"Unknown tool: {name}")


# ─────────────────────────────────────────────
# Agent Loop
# ─────────────────────────────────────────────
def run(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    print(f"\nUser: {user_message}")

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            tools=TOOLS,
            messages=messages
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
                    print(f"  → Calling {block.name}({block.input})")
                    try:
                        result = execute_tool(block.name, block.input)
                        print(f"  ← Result: {result}")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {e}",
                            "is_error": True
                        })

            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    answer = run("What is the weather like in Tokyo right now?")
    print(f"\nClaude: {answer}")

    answer2 = run("Compare the weather in Paris and New York for me.")
    print(f"\nClaude: {answer2}")
