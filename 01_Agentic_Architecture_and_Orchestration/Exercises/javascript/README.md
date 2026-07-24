---
tags: [exercises, javascript, agentic-architecture]
module: "01 - Agentic Architecture & Orchestration"
language: JavaScript
---

# JavaScript Exercises — Agentic Architecture & Orchestration

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

| File | Topic |
|---|---|
| `01_agentic_loop.js` | Agentic loop keyed off `stop_reason` (`"tool_use"` vs `"end_turn"`), with a safety-net iteration cap that is never the primary stop condition (Task 1.1) |
| `02_coordinator_subagents.js` | Coordinator dispatching to 2+ isolated "subagents" in parallel via `Promise.all`, with explicit context passing and a coverage-gap re-delegation pass (Tasks 1.2, 1.3) |
| `03_hook_interception.js` | `PreToolUse`-style blocking of refunds over $500 and a `PostToolUse`-style hook normalizing heterogeneous tool-result formats (Task 1.5) |

Each file's header comment explains how the pattern maps to the Claude Agent SDK (`Task` tool, `AgentDefinition`, `PreToolUse`/`PostToolUse` hooks) — these exercises use the raw `@anthropic-ai/sdk` so the underlying mechanics are visible.

## How to Run

```bash
npm install
node 01_agentic_loop.js
node 02_coordinator_subagents.js
node 03_hook_interception.js

# Or via script
./run.sh
.\run.ps1
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
