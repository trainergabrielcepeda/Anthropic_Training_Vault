---
tags: [theory, tools, schema]
topic: "03 - Tool Use & Function Calling"
---

# Tool Definition

## What Is a Tool?

A tool is a function you expose to Claude via a JSON schema. Claude decides when to call it, constructs the arguments, and waits for you to execute it and return the result.

Claude cannot execute tools itself — it only requests them. Your code is always the executor.

---

## Tool Schema Structure

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city. Returns temperature in Celsius and a short condition description.",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The city name, e.g. 'Paris' or 'New York'"
      },
      "country_code": {
        "type": "string",
        "description": "ISO 3166-1 alpha-2 country code, e.g. 'FR' or 'US'",
        "default": "US"
      }
    },
    "required": ["city"]
  }
}
```

### Schema Fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `name` | Yes | Snake_case identifier. Must be unique within the tools array |
| `description` | Yes | Natural language explanation of what the tool does and when to use it. **This is the most important field** |
| `input_schema` | Yes | JSON Schema object defining the tool's parameters |

---

## The Description Is Critical

Claude uses the `description` field to decide **whether** to call a tool and **which** tool to call when multiple are available.

**Bad description:**

```json
"description": "Weather tool"
```

**Good description:**

```json
"description": "Get current weather conditions for a specific city. Use this when the user asks about current weather, temperature, or conditions in any location. Do not use for forecasts or historical data."
```

The good description tells Claude:
- What it returns
- When to use it
- When **not** to use it

---

## Input Schema Best Practices

Use JSON Schema constraints to help Claude produce valid arguments:

```json
{
  "type": "object",
  "properties": {
    "temperature": {
      "type": "number",
      "minimum": -273.15,
      "description": "Temperature in Celsius"
    },
    "unit": {
      "type": "string",
      "enum": ["celsius", "fahrenheit", "kelvin"],
      "description": "Temperature unit"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 5
    }
  },
  "required": ["temperature", "unit"]
}
```

Supported JSON Schema constraints: `type`, `enum`, `minimum`, `maximum`, `minLength`, `maxLength`, `pattern`, `items`, `required`, `description`.

---

## Attaching Tools to a Request

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current temperature and conditions for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

---

## `tool_choice` Parameter

Control whether Claude uses tools automatically or is forced to use one.

| Value | Behavior |
| ----- | -------- |
| `{"type": "auto"}` | Default. Claude decides whether to use a tool |
| `{"type": "any"}` | Claude must use at least one tool |
| `{"type": "tool", "name": "tool_name"}` | Claude must use this specific tool |
| `{"type": "none"}` | Claude cannot use any tools in this turn |

---

## Related Notes

- [[02_Tool_Call_Flow|Tool Call Flow — handling the response]]
- [[03_Advanced_Tool_Patterns|Advanced Tool Patterns]]
- [[../../02_Prompt_Engineering/Theory/02_Advanced_Techniques|Advanced Techniques — structured output]]

---

[[../_Index|← Back to Tool Use & Function Calling Index]]
