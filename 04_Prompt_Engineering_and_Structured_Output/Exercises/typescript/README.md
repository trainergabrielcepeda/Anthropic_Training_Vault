---
tags: [exercises, typescript, structured-output]
module: "04 - Prompt Engineering & Structured Output"
language: TypeScript
---

# TypeScript Exercises — Prompt Engineering & Structured Output

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_structured_extraction.ts` — `tool_choice: "any"` with Multiple Schemas (Task 4.3)

| Part | What it does |
|------|-------------|
| Two schemas | `extract_receipt` and `extract_contract`, each mapped to a TypeScript interface with required, nullable, and enum (`"other"` / `"unclear"`) fields |
| `tool_choice: { type: "any" }` | Used because the document type is unknown ahead of time — guarantees a tool call without forcing a possibly-wrong schema |

### `02_validation_retry_loop.ts` — Forced Tool Ordering + Self-Correction (Tasks 4.3 & 4.4)

| Part | What it does |
|------|-------------|
| Forced tool | `{"type": "tool", "name": "extract_metadata"}` guarantees a metadata step runs before the invoice-extraction (enrichment) step depends on it |
| Self-correction schema | Extracts `stated_total` and an independently computed `calculated_total` side by side |
| `conflict_detected` | Boolean flag for genuinely inconsistent source data (not an extraction bug) — routed to human review instead of retried |

> **Key concept:** TypeScript interfaces (`ReceiptExtraction`, `InvoiceExtraction`, etc.) let you validate that Claude's `tool_use.input` matches your expected shape at compile time — the schema and the interface should be kept in sync by hand.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
npx ts-node --esm 01_structured_extraction.ts
npx ts-node --esm 02_validation_retry_loop.ts

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
