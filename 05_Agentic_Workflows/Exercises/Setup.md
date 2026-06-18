---
tags: [setup, exercises]
topic: "05 - Agentic Workflows"
---

# Exercises Setup — Agentic Workflows

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## Run

```bash
# Python
cd 05_Agentic_Workflows/Exercises/python
pip install -r requirements.txt
python 01_simple_agent.py
python 02_orchestrator.py

# JavaScript
cd 05_Agentic_Workflows/Exercises/javascript
npm install && node 01_simple_agent.js

# TypeScript
cd 05_Agentic_Workflows/Exercises/typescript
npm install && npx ts-node 01_typed_agent.ts
```

## What Each Exercise Covers

| File | Topic |
| ---- | ----- |
| `01_simple_agent` | Agent loop with tool use, max-turn guard |
| `02_orchestrator.py` | Orchestrator dispatching tasks to specialized subagents |
| `01_typed_agent.ts` | Typed agent with explicit state object |

---

[[../_Index|← Back to Agentic Workflows Index]]
