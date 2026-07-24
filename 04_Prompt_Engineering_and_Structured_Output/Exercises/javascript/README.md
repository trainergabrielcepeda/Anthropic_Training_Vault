---
tags: [exercises, javascript, structured-output]
module: "04 - Prompt Engineering & Structured Output"
language: JavaScript
---

# JavaScript Exercises — Prompt Engineering & Structured Output

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_structured_extraction.js` — Structured Extraction + Validation Retry (Tasks 4.3 & 4.4)

| Part | What it does |
|------|-------------|
| Schema | `extract_invoice` tool with required fields, nullable `purchase_order_number`, and an enum + `"other"`/detail category |
| Extraction | Forces the tool via `tool_choice` and reads the result from the `tool_use` block |
| Validation | Checks line items against `stated_total` — a semantic check schema compliance alone can't catch |
| Retry loop | On mismatch, sends back a `tool_result` with the specific error and retries, demonstrating self-correction |

### `02_few_shot_consistency.js` — Few-Shot for Consistency (Task 4.2)

| Part | What it does |
|------|-------------|
| Before | Detailed instructions alone, zero-shot, on ambiguous escalation cases |
| After | Same cases with 3 targeted few-shot examples (with reasoning) added |
| Generalization | A 4th novel case checks whether the model learned the decision principle, not just the examples |

> The JavaScript version uses ES Modules (`"type": "module"`). All functions are `async`.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
node 01_structured_extraction.js
node 02_few_shot_consistency.js

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
