---
tags: [exercises, typescript, tool-use]
module: "03 - Tool Use"
language: TypeScript
---

# TypeScript Exercises — Tool Use & Function Calling

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/03_Tool_Use/Exercises/typescript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

> **Coming soon.** TypeScript exercises will add strong typing to the tool-use patterns already shown in Python:

| Planned file | Topic |
|---|---|
| `01_single_tool.ts` | Typed tool schema (`Tool` type), discriminated union on `ContentBlock` |
| `02_multi_tool.ts` | `ToolResultBlockParam`, typed parallel tool responses |

In the meantime, see the [[../python/README|Python exercises]] for the full implementation.

## How to Run (once files exist)

```bash
npm install
npx ts-node --esm 01_single_tool.ts
npx ts-node --esm 02_multi_tool.ts

# Or via script
./run.sh
.\run.ps1
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
