---
tags: [exercises, typescript, context-management, reliability]
module: "05 - Context Management & Reliability"
language: TypeScript
---

# TypeScript Exercises — Context Management & Reliability

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_context_reliability.ts` — Case Facts, Escalation Criteria & Structured Error Propagation (Tasks 5.1, 5.2, 5.3)

| Part | What it does |
|------|-------------|
| A — Case facts | Extracts a small, typed `CaseFacts` block from a verbose `RawOrder` tool result instead of letting the full payload accumulate in context |
| B — Escalation | `decideEscalation()` uses explicit criteria + few-shot examples in the system prompt, returning a typed `EscalationDecision` — distinguishing explicit human requests and policy gaps from ordinary complex-but-covered cases |
| C — Error propagation | `subagentSearch()` returns a typed `SubagentResult` union (`SubagentSuccess \| SubagentError`) on a simulated timeout, and `coordinatorRecover()` reasons over the structured error to pick a recovery action |

> **Key concept:** the `SubagentResult` discriminated union makes it a compile-time error to treat a structured error as if it were a success payload (or vice versa) — the pattern from the theory notes enforced by the type system, not just convention.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run
npx ts-node --esm 01_context_reliability.ts

# Or run via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
