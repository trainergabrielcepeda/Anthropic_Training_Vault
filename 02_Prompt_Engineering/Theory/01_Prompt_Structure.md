---
tags: [theory, prompting, structure]
topic: "02 - Prompt Engineering"
---

# Prompt Structure

## The Three Roles

Every message in a conversation has a `role` field. Understanding each role is the foundation of prompt design.

| Role | Who sends it | Purpose |
| ---- | ------------ | ------- |
| `system` | Developer (operator) | Sets Claude's persona, constraints, and behavioral instructions. Processed before all user messages |
| `user` | End user or developer | The request, question, or input Claude should respond to |
| `assistant` | Claude (or prefilled by developer) | Claude's response. Can be prefilled to guide output format |

---

## The System Prompt

The system prompt is the most powerful lever in prompt engineering. It is set via the top-level `system` parameter, **not** as a message in the `messages` array.

```python
client.messages.create(
    model="claude-sonnet-4-6",
    system="You are a senior Python engineer. Answer concisely. Always include type hints.",
    messages=[{"role": "user", "content": "Write a function that reverses a string."}],
    max_tokens=512
)
```

### What to put in the system prompt

- **Persona** — who Claude is in this context
- **Task scope** — what topics are in/out of scope
- **Format instructions** — response length, structure, language
- **Behavioral constraints** — what Claude must never do
- **Background context** — domain knowledge Claude needs upfront

> [!tip] System prompt ordering matters
> Put your most important instructions at the beginning **and** at the end of a long system prompt. Claude attends most strongly to the beginning and end of its context.

---

## Conversation Structure

Messages must alternate strictly between `user` and `assistant`. You cannot have two consecutive `user` or `assistant` messages.

```json
"messages": [
  { "role": "user",      "content": "Translate 'hello' to French." },
  { "role": "assistant", "content": "Bonjour." },
  { "role": "user",      "content": "Now to Spanish." }
]
```

> [!warning] Invalid sequences
> Starting with `assistant`, or placing two `user` messages in a row, causes a 400 error.

---

## Assistant Prefilling

You can prefill the start of Claude's response by adding an `assistant` message as the last item in the array. Claude will continue from that exact text.

```python
messages=[
    {"role": "user", "content": "What is 2 + 2?"},
    {"role": "assistant", "content": "The answer is"}   # Claude continues here
]
```

This technique is powerful for:
- Forcing a specific output format (e.g., starting with `{` for JSON)
- Locking in a response style
- Skipping preamble ("Certainly! Here is…")

---

## Content Blocks

The `content` field in a message can be a plain string **or** an array of typed content blocks. Use blocks when mixing text with images or tool results.

```json
{
  "role": "user",
  "content": [
    { "type": "text", "text": "What is in this image?" },
    { "type": "image", "source": { "type": "base64", "media_type": "image/jpeg", "data": "..." } }
  ]
}
```

---

## Common Structural Mistakes

| Mistake | Effect | Fix |
| ------- | ------ | --- |
| Putting instructions in the first `user` message instead of `system` | Instructions can be overridden or ignored in multi-turn | Move to `system` parameter |
| Vague persona ("be helpful") | Inconsistent behavior | Use specific, behavioral descriptions |
| Omitting response format instructions | Verbose, unpredictable output | Specify length, format, and structure |
| Contradictory instructions | Unpredictable behavior | Review for conflicts before shipping |

---

## Related Notes

- [[02_Advanced_Techniques|Advanced Techniques]]
- [[03_Prompt_Patterns|Prompt Patterns]]
- [[../../01_Claude_Models_and_API/Theory/02_API_Fundamentals|API Fundamentals — request shape]]

---

[[../_Index|← Back to Prompt Engineering Index]]
