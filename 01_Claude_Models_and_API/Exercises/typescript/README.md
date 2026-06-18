---
tags: [exercises, typescript, claude-api]
module: "01 - Claude Models & API"
language: TypeScript
---

# TypeScript Exercises — Claude Models & API

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/01_Claude_Models_and_API/Exercises/typescript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_basic_messages.ts` — Typed Messages API

| Part | What it does |
|------|-------------|
| 1 | Typed single-turn message — use `Message` and content block type guards (`block.type === 'text'`) |
| 2 | Typed multi-turn conversation — `MessageParam[]` history array with full type safety |
| 3 | Model comparison — parallel requests with `Promise.all`, typed `ModelResult` interface |

> **Key concept:** TypeScript's union types on `ContentBlock` require narrowing (`if (block.type === 'text')`) before accessing `.text`.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
npx ts-node --esm 01_basic_messages.ts

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
