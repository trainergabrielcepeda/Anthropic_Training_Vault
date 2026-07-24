---
tags: [exercises, javascript, tool-design, mcp]
module: "02 - Tool Design & MCP Integration"
language: JavaScript
---

# JavaScript Exercises — Tool Design & MCP Integration

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/vaults/Anthropic_Training_Vault/02_Tool_Design_and_MCP_Integration/Exercises/javascript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

| File | Task | What it does |
|---|---|---|
| `01_tool_description_design.js` | 2.1 | Ambiguous, overlapping tool descriptions vs. differentiated, purpose-specific tools — before/after routing comparison |
| `02_structured_errors.js` | 2.2 | MCP-style structured error objects (`isError`, `errorCategory`, `isRetryable`) and client-side recovery logic that branches on category |
| `03_tool_choice_modes.js` | 2.3 | `tool_choice` in all three modes: forced, `"auto"`, and `"any"` |

See [[../python/README|Python exercises]] for the same three exercises with more detailed inline commentary.

## How to Run

```bash
npm install
node 01_tool_description_design.js
node 02_structured_errors.js
node 03_tool_choice_modes.js

# Or via script
./run.sh
.\run.ps1
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
