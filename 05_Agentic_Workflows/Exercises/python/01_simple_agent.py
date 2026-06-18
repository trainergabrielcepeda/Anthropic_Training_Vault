"""
Exercise 1 — Simple Agent Loop
Topic: Agentic Workflows

Covers:
  - The observe → plan → act loop
  - Max-turn guard to prevent infinite loops
  - Multiple tools in an agent
  - Logging each step for observability
"""

import json
import anthropic

client = anthropic.Anthropic()

MAX_TURNS = 8

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a mathematical expression and return the numeric result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A Python-evaluable math expression, e.g. '(15 * 3) / 4 + 2'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "lookup_fact",
        "description": "Look up a factual piece of information from a knowledge base.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The fact to look up, e.g. 'population of France'"
                }
            },
            "required": ["query"]
        }
    }
]


def execute_tool(name: str, inputs: dict) -> str:
    if name == "calculator":
        try:
            result = eval(inputs["expression"], {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"Math error: {e}"

    if name == "lookup_fact":
        facts = {
            "population of france": "approximately 68 million (2024)",
            "capital of japan":     "Tokyo",
            "speed of light":       "299,792,458 metres per second",
            "gdp of germany":       "approximately $4.4 trillion USD (2023)",
        }
        return facts.get(inputs["query"].lower(), "Fact not found in knowledge base.")

    return f"Unknown tool: {name}"


def run_agent(task: str) -> str:
    """Run the agent loop until done or MAX_TURNS reached."""
    messages = [{"role": "user", "content": task}]
    print(f"\nTask: {task}\n{'─'*50}")

    for turn in range(1, MAX_TURNS + 1):
        print(f"\n[Turn {turn}]")

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=(
                "You are a research assistant. Use the available tools to answer "
                "the user's question. Show your work step by step."
            ),
            tools=TOOLS,
            messages=messages
        )

        print(f"stop_reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return "[No text in final response]"

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "text" and block.text:
                    print(f"Claude says: {block.text[:100]}...")
                if block.type == "tool_use":
                    print(f"  → {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"  ← {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})
            continue

        # Unexpected stop_reason
        return f"Unexpected stop_reason: {response.stop_reason}"

    return f"Agent hit max turns ({MAX_TURNS}). Task may be incomplete."


if __name__ == "__main__":
    result = run_agent(
        "What is 15% of the population of France? "
        "Also, what is the speed of light divided by 1000?"
    )
    print(f"\n{'─'*50}\nFinal Answer:\n{result}")
