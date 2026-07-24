---
tags: [exercises, typescript, tool-design, mcp]
module: "02 - Tool Design & MCP Integration"
language: TypeScript
---

# TypeScript Exercises — Tool Design & MCP Integration

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/vaults/Anthropic_Training_Vault/02_Tool_Design_and_MCP_Integration/Exercises/typescript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

| File | Task | What it does |
|---|---|---|
| `01_tool_description_design.ts` | 2.1 | Ambiguous, overlapping tool descriptions vs. differentiated, purpose-specific tools, using the typed `Tool` schema |
| `02_structured_errors.ts` | 2.2 | MCP-style structured errors as a discriminated union (`ToolError \| RefundSuccess`) with exhaustive `errorCategory` branching |
| `03_tool_choice_modes.ts` | 2.3 | `tool_choice` in all three modes: forced, `"auto"`, and `"any"`, with typed `ToolUseBlock` narrowing |

See [[../python/README|Python exercises]] for the same three exercises with more detailed inline commentary.

## How to Run

```bash
npm install
npx ts-node --esm 01_tool_description_design.ts
npx ts-node --esm 02_structured_errors.ts
npx ts-node --esm 03_tool_choice_modes.ts

# Or via script
./run.sh
.\run.ps1
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
