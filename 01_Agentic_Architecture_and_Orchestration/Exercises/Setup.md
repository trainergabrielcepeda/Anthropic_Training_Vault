---
tags: [setup, exercises]
topic: "01 - Agentic Architecture & Orchestration"
---

# Exercises Setup — Agentic Architecture & Orchestration

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## Run

```bash
# Python
cd 01_Agentic_Architecture_and_Orchestration/Exercises/python
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python 01_agentic_loop.py
python 02_coordinator_subagents.py
python 03_hook_interception.py

# JavaScript
cd 01_Agentic_Architecture_and_Orchestration/Exercises/javascript
npm install
node 01_agentic_loop.js
node 02_coordinator_subagents.js
node 03_hook_interception.js

# TypeScript
cd 01_Agentic_Architecture_and_Orchestration/Exercises/typescript
npm install
npx ts-node --esm 01_agentic_loop.ts
npx ts-node --esm 02_coordinator_subagents.ts
npx ts-node --esm 03_hook_interception.ts
```

Or use the per-language `run.sh` (Linux/macOS) / `run.ps1` (Windows) scripts, which install dependencies and run every exercise in order.

## What Each Exercise Covers

| File | Topic | Task statement(s) |
| ---- | ----- | ------------------ |
| `01_agentic_loop.{py,js,ts}` | Agentic loop keyed off `stop_reason` — continue on `"tool_use"`, terminate on `"end_turn"`; a max-iteration cap used only as a safety net, never the primary stop condition | 1.1 |
| `02_coordinator_subagents.{py,js,ts}` | Coordinator dispatching to 2+ isolated "subagents" in parallel, explicit context passing (no shared memory), synthesis + coverage-gap re-delegation | 1.2, 1.3 |
| `03_hook_interception.{py,js,ts}` | `PreToolUse`-style blocking of a policy-violating tool call (refund > $500) and a `PostToolUse`-style hook normalizing heterogeneous tool-result formats | 1.4, 1.5 |

Every exercise uses the raw `anthropic` / `@anthropic-ai/sdk` client directly — there is no Claude Agent SDK dependency here. Each file's header comment explains exactly how the pattern maps onto Agent SDK concepts (`Task` tool, `AgentDefinition`, `allowedTools`, `PreToolUse`/`PostToolUse` hooks) referenced in [[../Theory/02_Multi_Agent_Orchestration|Multi-Agent Orchestration]] and [[../Theory/03_Workflow_Control_and_Session_Management|Workflow Control & Session Management]].

---

[[../_Index|← Back to Domain 1 Index]]
