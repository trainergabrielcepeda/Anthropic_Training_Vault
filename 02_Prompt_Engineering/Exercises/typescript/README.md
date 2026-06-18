---
tags: [exercises, typescript, prompt-engineering]
module: "02 - Prompt Engineering"
language: TypeScript
---

# TypeScript Exercises — Prompt Engineering

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/02_Prompt_Engineering/Exercises/typescript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_structured_output.ts` — Structured Output

| Part | What it does |
|------|-------------|
| 1 | Force JSON output via assistant prefilling (`{` starter) and parse into a typed interface |
| 2 | Use a tool definition as a structured extraction schema — cleaner than regex parsing |
| 3 | Compare both approaches: prefilling vs tool-based extraction |

> **Key concept:** TypeScript interfaces (`ArticleSummary`) let you validate that Claude's JSON matches your expected shape at compile time.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
npx ts-node --esm 01_structured_output.ts

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
