---
tags: [theory, tools, advanced]
topic: "03 - Tool Use & Function Calling"
---

# Advanced Tool Patterns

## Parallel Tool Calls

Claude can call multiple tools in a single response when the tasks are independent. The `content` array will contain multiple `tool_use` blocks.

```json
"content": [
  {
    "type": "tool_use",
    "id": "toolu_001",
    "name": "get_weather",
    "input": {"city": "Tokyo"}
  },
  {
    "type": "tool_use",
    "id": "toolu_002",
    "name": "get_weather",
    "input": {"city": "Paris"}
  }
]
```

You must return a `tool_result` for **every** `tool_use` block in the same user message:

```python
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = execute_tool(block.name, block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result
        })

messages.append({"role": "user", "content": tool_results})
```

> [!tip] Run parallel calls concurrently
> Since parallel tool calls are independent, you can execute them in parallel using `asyncio.gather` (Python) or `Promise.all` (JavaScript) to reduce total latency.

---

## Tool Chaining

Claude can call tools sequentially when the output of one is needed as input to another. This happens naturally over multiple turns.

```
Turn 1: User: "What restaurants near the Eiffel Tower have outdoor seating?"
Turn 2: Claude calls get_location("Eiffel Tower") → coordinates
Turn 3: Claude calls search_restaurants(lat=48.858, lon=2.294, features=["outdoor"])
Turn 4: Claude returns the list
```

Your agent loop handles this automatically if you continue until `stop_reason == "end_turn"`.

---

## Forcing a Specific Tool

Use `tool_choice: {"type": "tool", "name": "..."}` when you want Claude to always call a particular tool, regardless of whether it thinks it needs to.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_entities"},
    messages=[{"role": "user", "content": document_text}]
)
```

**Use case:** Extracting structured data on every call, where calling the tool is mandatory, not optional.

---

## Extracting Structured Data via Tools

A common pattern is to define a "fake" tool whose only purpose is to force structured output. Claude will always call it, giving you a typed JSON object without needing to parse free text.

```python
tools = [{
    "name": "record_summary",
    "description": "Record the extracted summary. Always call this tool.",
    "input_schema": {
        "type": "object",
        "properties": {
            "title":    {"type": "string"},
            "topics":   {"type": "array", "items": {"type": "string"}},
            "sentiment":{"type": "string", "enum": ["positive","neutral","negative"]},
            "word_count":{"type": "integer"}
        },
        "required": ["title", "topics", "sentiment", "word_count"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    tools=tools,
    tool_choice={"type": "tool", "name": "record_summary"},
    messages=[{"role": "user", "content": f"Analyze: {article_text}"}]
)

data = response.content[0].input  # already a Python dict
```

---

## Error Handling Strategy

```python
for block in response.content:
    if block.type == "tool_use":
        try:
            result = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result)
            })
        except Exception as e:
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Error: {str(e)}",
                "is_error": True
            })
```

With `is_error: True`, Claude will acknowledge the failure in its response and may suggest alternatives or retry with different arguments.

---

## Tool Design Checklist

- [ ] Description explains **when to use** and **when not to use** the tool
- [ ] All required parameters are in `required`
- [ ] Parameters have `enum` constraints where the set of values is finite
- [ ] Parameter descriptions include example values
- [ ] Tool names are unique within the array
- [ ] Each tool does exactly one thing (single responsibility)

---

## Related Notes

- [[01_Tool_Definition|Tool Definition]]
- [[02_Tool_Call_Flow|Tool Call Flow]]
- [[../../05_Agentic_Workflows/Theory/01_Agent_Design|Agent Design — tools in agent loops]]

---

[[../_Index|← Back to Tool Use & Function Calling Index]]
