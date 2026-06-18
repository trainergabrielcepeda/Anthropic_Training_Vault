---
tags: [topic, tools, function-calling]
topic: "03 - Tool Use & Function Calling"
---

# Topic 3 — Tool Use & Function Calling

Tool use lets Claude take actions and retrieve information beyond its training data. This topic covers how to define tools, handle the two-turn tool call flow, chain multiple tools, and deal with errors gracefully.

---

## Theory Notes

1. [[Theory/01_Tool_Definition|01 — Tool Definition]] — JSON schema for tools: `name`, `description`, `input_schema`, and best practices.
2. [[Theory/02_Tool_Call_Flow|02 — Tool Call Flow]] — The two-turn cycle: `tool_use` content blocks, `tool_result` responses.
3. [[Theory/03_Advanced_Tool_Patterns|03 — Advanced Tool Patterns]] — Parallel tools, forced tool use, error propagation, and tool chaining.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_single_tool.py` | Define one tool and handle its call |
| Python | `Exercises/python/02_multi_tool.py` | Multiple tools in one conversation |
| JavaScript | `Exercises/javascript/01_single_tool.js` | Tool use in Node.js |
| TypeScript | `Exercises/typescript/01_typed_tools.ts` | Strongly typed tool definitions |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 15 questions on tool schemas, call flow, and error handling.

---

## Key Concepts Checklist

- [ ] Write a valid tool definition JSON schema from scratch
- [ ] Describe exactly what Claude returns when it decides to use a tool
- [ ] Explain how to send a `tool_result` back correctly (success and error cases)
- [ ] Identify the `stop_reason` that signals a tool call
- [ ] Explain when to use `tool_choice: { type: "tool" }` vs `"auto"`
