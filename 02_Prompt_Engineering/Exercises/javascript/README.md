---
tags: [exercises, javascript, prompt-engineering]
module: "02 - Prompt Engineering"
language: JavaScript
---

# JavaScript Exercises — Prompt Engineering

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/02_Prompt_Engineering/Exercises/javascript)

## Prerequisites

- Node.js 18+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `npm install`

## Exercises

### `01_system_prompts.js` — System Prompts

| Part | What it does |
|------|-------------|
| 1 | Compare responses with and without a system prompt on the same question |
| 2 | Define a persona via system prompt and observe tone/format shift |
| 3 | Enforce output constraints (e.g., JSON-only) through the system turn |

> The JavaScript version uses ES Modules (`"type": "module"`). All functions are `async`.

## How to Run

```bash
# Install dependencies (once)
npm install

# Run individually
node 01_system_prompts.js

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
