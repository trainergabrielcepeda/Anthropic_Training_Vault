---
tags: [theory, agents, design]
topic: "05 - Agentic Workflows"
---

# Agent Design Patterns

## What Is an Agent?

An agent is a system that uses an LLM to make decisions and take actions in a loop — observing results, planning the next step, acting, and repeating — until a goal is achieved.

The key property of an agent is **autonomy**: it takes multiple sequential actions without a human approving each one.

---

## The Agent Loop

```
┌─────────────────────────────────────────┐
│  OBSERVE: Receive task + context        │
│       ↓                                 │
│  PLAN:  Decide next action              │
│       ↓                                 │
│  ACT:   Call a tool or produce output   │
│       ↓                                 │
│  OBSERVE: Receive tool result           │
│       ↓                                 │
│  Done? → Yes → Return final output      │
│       ↓ No                              │
│  Back to PLAN                           │
└─────────────────────────────────────────┘
```

In code this is typically a `while` loop that breaks when `stop_reason == "end_turn"` and no tool call occurred.

---

## Agent Architectural Patterns

### Single Agent

One Claude instance with a set of tools. Suitable for most tasks.

```
User → Claude (with tools) → Output
```

### Orchestrator + Subagents

One orchestrator Claude routes tasks to specialized subagents. Use when:
- Tasks require different skill sets or system prompts
- You want to parallelize independent subtasks
- You want to isolate tool access (subagent A has read-only tools, subagent B has write tools)

```
User → Orchestrator Claude
          ├── Subagent A (research)
          ├── Subagent B (writing)
          └── Subagent C (review)
       → Final output
```

### Router

A lightweight classifier Claude routes requests to the right agent or pipeline without doing the work itself.

```
User → Router (classify intent)
          ├── If BILLING → Billing Agent
          ├── If TECHNICAL → Tech Support Agent
          └── If GENERAL → General Agent
```

---

## When to Use Agents (and When Not To)

**Use agents when:**
- The task requires multiple sequential steps where each step depends on the previous result
- The number of steps is not known in advance
- The task requires real-world actions (web search, file writes, API calls)

**Do NOT use agents when:**
- A single well-crafted prompt handles the task
- The task is purely text generation with no external dependencies
- You need strict determinism (agents are inherently non-deterministic)
- Latency is critical (agent loops add turns = latency)

> [!warning] Agents are harder to test and debug
> Each additional turn multiplies the state space. Test agents with narrow, well-defined tasks before expanding scope.

---

## Minimal Footprint Principle

Agents should:
- Request only the permissions they need for the current task
- Avoid storing sensitive information beyond immediate needs
- Prefer reversible actions over irreversible ones
- Err on the side of doing less and confirming with users when uncertain about scope

> [!example] Reversible vs irreversible
> Drafting an email is reversible. Sending it is not. An agent should draft, show the user, and send only on explicit confirmation.

---

## Stopping Conditions

Always define when your agent stops. Without a termination condition, agents can loop indefinitely.

```python
MAX_TURNS = 10
turn = 0

while turn < MAX_TURNS:
    response = client.messages.create(...)
    turn += 1

    if response.stop_reason == "end_turn":
        # No tool call — agent is done
        break

    if response.stop_reason == "tool_use":
        # Execute tools and continue
        ...
else:
    # Hit MAX_TURNS — handle gracefully
    raise AgentLoopError("Max turns exceeded")
```

---

## Related Notes

- [[02_Memory_and_State|Memory & State]]
- [[03_Multi_Agent_Systems|Multi-Agent Systems]]
- [[../../03_Tool_Use/Theory/02_Tool_Call_Flow|Tool Call Flow — the mechanism agents use]]

---

[[../_Index|← Back to Agentic Workflows Index]]
