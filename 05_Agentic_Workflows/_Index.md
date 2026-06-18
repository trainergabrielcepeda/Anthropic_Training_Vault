---
tags: [topic, agents, agentic]
topic: "05 - Agentic Workflows"
---

# Topic 5 — Agentic Workflows

Agentic systems give Claude the ability to take sequences of actions, use tools, and make decisions over extended interactions. This topic covers agent architecture, memory strategies, orchestration patterns, and multi-agent coordination.

---

## Theory Notes

1. [[Theory/01_Agent_Design|01 — Agent Design Patterns]] — The agent loop, when to use agents, and architectural patterns (router, orchestrator, subagent).
2. [[Theory/02_Memory_and_State|02 — Memory & State]] — In-context, external, and semantic memory; state management across turns.
3. [[Theory/03_Multi_Agent_Systems|03 — Multi-Agent Systems]] — Orchestrator/subagent patterns, trust between agents, and parallelization.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_simple_agent.py` | Basic agent loop with tool use |
| Python | `Exercises/python/02_orchestrator.py` | Orchestrator dispatching to subagents |
| JavaScript | `Exercises/javascript/01_simple_agent.js` | Agent loop in Node.js |
| TypeScript | `Exercises/typescript/01_typed_agent.ts` | Typed agent with state management |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 15 questions on agent design, memory types, and multi-agent coordination.

---

## Key Concepts Checklist

- [ ] Describe the basic agent loop (observe → plan → act → observe)
- [ ] Explain the difference between in-context and external memory
- [ ] Identify when to use an orchestrator vs a single agent
- [ ] Explain why subagents should receive only necessary permissions (minimal footprint)
- [ ] Describe one strategy for detecting and breaking agent loops
