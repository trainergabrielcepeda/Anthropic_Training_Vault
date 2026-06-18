---
tags: [theory, agents, memory]
topic: "05 - Agentic Workflows"
---

# Memory & State

## Why Memory Matters

Claude has no persistent memory between API calls. Every agent conversation starts with a blank slate. For agents to be useful across tasks and sessions, you must design explicit memory systems.

---

## Memory Types

| Type | Where Stored | Persistence | Best For |
| ---- | ------------ | ----------- | -------- |
| **In-context** | `messages` array | Current session only | Recent conversation, working state |
| **External (key-value)** | Database / file | Permanent | User preferences, facts, entity data |
| **External (semantic)** | Vector database | Permanent | Fuzzy search over large knowledge bases |
| **External (structured)** | SQL / structured DB | Permanent | Relational data, complex queries |

---

## In-Context Memory

The simplest form: everything you include in the `messages` array.

```python
messages = [
    {"role": "system", "content": "You are a research assistant."},
    {"role": "user", "content": "What is quantum entanglement?"},
    {"role": "assistant", "content": "Quantum entanglement is..."},
    {"role": "user", "content": "How does it relate to teleportation?"}
]
```

**Limitation:** The context window is finite (200k tokens). Long conversations must be managed:

```python
def summarize_and_compress(messages: list, client) -> list:
    """Replace old messages with a summary when context grows large."""
    if count_tokens(messages) < 150_000:
        return messages
    
    # Summarize everything except the last 4 messages
    to_summarize = messages[:-4]
    summary = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Summarize this conversation concisely:\n{to_summarize}"
        }]
    ).content[0].text
    
    return [
        {"role": "user", "content": f"[Previous context summary: {summary}]"},
        {"role": "assistant", "content": "Understood."}
    ] + messages[-4:]
```

---

## External Key-Value Memory

Store and retrieve facts about entities (users, tasks, projects):

```python
# Writing to memory
memory_store = {}

def save_memory(key: str, value: str):
    memory_store[key] = value

# Reading memory into context
def load_relevant_memory(user_id: str) -> str:
    facts = memory_store.get(f"user:{user_id}", {})
    if not facts:
        return ""
    return "Known facts about this user:\n" + "\n".join(
        f"- {k}: {v}" for k, v in facts.items()
    )

# Inject into system prompt
system = f"""You are a personal assistant.
{load_relevant_memory(user_id)}
"""
```

In production, replace `memory_store` with Redis, DynamoDB, or any key-value store.

---

## Semantic Memory (Vector Search)

Store text as embeddings and retrieve the most relevant pieces for any query:

```
Document → chunk → embed → store in vector DB
Query → embed → similarity search → top-k chunks → inject into context
```

This is the basis of RAG (Retrieval-Augmented Generation). See [[../../06_Production_and_Evaluation/_Index|Production & Evaluation]] for implementation patterns.

---

## State Management in Agent Loops

For multi-step tasks, maintain a state object alongside the messages:

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    task: str
    steps_completed: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    turn_count: int = 0

state = AgentState(task="Analyze the Q3 report and write a summary")

# After each tool call, update state
state.steps_completed.append("Retrieved Q3 report")
state.artifacts["report"] = report_content
state.turn_count += 1

# Inject state summary into system prompt if needed
system = f"""
Current task: {state.task}
Steps completed: {', '.join(state.steps_completed)}
Turn: {state.turn_count}
"""
```

---

## Scratchpad Pattern

Give Claude an explicit scratchpad tool to record intermediate thinking, plans, and partial results:

```json
{
  "name": "update_scratchpad",
  "description": "Record your current plan, observations, and intermediate results. Use this to track your thinking across steps.",
  "input_schema": {
    "type": "object",
    "properties": {
      "content": {"type": "string", "description": "Your notes, plan, or observations"}
    },
    "required": ["content"]
  }
}
```

The scratchpad tool handler simply saves the content and returns an acknowledgment. This externalizes Claude's working memory and makes agent behavior more inspectable.

---

## Related Notes

- [[01_Agent_Design|Agent Design Patterns]]
- [[03_Multi_Agent_Systems|Multi-Agent Systems]]
- [[../../01_Claude_Models_and_API/Theory/03_Tokens_and_Context|Tokens & Context — managing long context]]

---

[[../_Index|← Back to Agentic Workflows Index]]
