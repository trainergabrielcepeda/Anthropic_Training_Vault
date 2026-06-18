---
tags: [exercises, javascript, claude-api]
module: "01 - Claude Models & API"
language: JavaScript
---

# JavaScript Exercises — Claude Models & API

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/01_Claude_Models_and_API/Exercises/javascript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_basic_messages.js` — Messages API Fundamentals

| Part | What it does |
|------|-------------|
| 1 | Single-turn message — send a question and log the full response object (`id`, `model`, `stop_reason`, `usage`) |
| 2 | Multi-turn conversation — async chat loop with manually managed message history |
| 3 | Streaming — iterate over the stream using `for await...of`, print chunks, get final usage |

> **Note:** JavaScript uses ES Modules (`"type": "module"` in package.json). Run with `node`, not `require`.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
node 01_basic_messages.js

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
