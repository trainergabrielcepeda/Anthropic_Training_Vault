---
tags: [exercises, javascript, context-management, reliability]
module: "05 - Context Management & Reliability"
language: JavaScript
---

# JavaScript Exercises — Context Management & Reliability

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_case_facts.js` — Case-Facts Extraction Pattern (Task 5.1)

| Part | What it does |
|------|-------------|
| Verbose tool result | Simulates a `lookup_order` call returning 20+ fields |
| Forced extraction | Uses `tool_choice` to pull only the fields relevant to a delivery-delay conversation |
| Persistent block | Renders a small "CASE FACTS" block re-injected on the next turn, outside summarized history |

### `02_escalation_and_errors.js` — Escalation Criteria + Structured Error Propagation (Tasks 5.2 & 5.3)

| Part | What it does |
|------|-------------|
| Explicit criteria + few-shot | System prompt defines exactly when to escalate, with worked examples |
| Forced decision tool | Returns a typed `ESCALATE`/`RESOLVE` decision with matched criterion and reasoning |
| Structured error | Simulated subagent timeout returns `failure_type`, `attempted_query`, `partial_results`, `alternative_approaches` |
| Anti-patterns shown | A generic string and a silently-empty "success" — included only for contrast |
| Coordinator | A real Claude call reasons over the structured result to decide a recovery action |

> The JavaScript version uses ES Modules (`"type": "module"`). All functions are `async`.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
node 01_case_facts.js
node 02_escalation_and_errors.js

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
