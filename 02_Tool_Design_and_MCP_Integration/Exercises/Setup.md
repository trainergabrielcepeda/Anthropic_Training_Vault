---
tags: [setup, exercises]
topic: "02 - Tool Design & MCP Integration"
---

# Exercises Setup — Tool Design & MCP Integration

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## What These Exercises Cover

Three exercises, implemented in Python, JavaScript, and TypeScript, mapped directly to exam tasks 2.1-2.3:

| # | File | Task | Covers |
| - | ---- | ---- | ------ |
| 1 | `01_tool_description_design.*` | 2.1 | Before/after: ambiguous, overlapping tool descriptions vs. differentiated, purpose-specific tools |
| 2 | `02_structured_errors.*` | 2.2 | MCP-style structured error objects (`isError`, `errorCategory`, `isRetryable`) and client-side recovery branching |
| 3 | `03_tool_choice_modes.*` | 2.3 | `tool_choice` in all three modes — forced, `"auto"`, `"any"` |

Tasks 2.4 (MCP server configuration in `.mcp.json` / `~/.claude.json`) and 2.5 (built-in tool selection) are configuration and workflow skills exercised directly inside Claude Code itself, rather than through API scripts — see [[../Theory/03_MCP_Servers_and_Builtin_Tools|MCP Servers & Built-in Tools]] for the worked examples and patterns to practice hands-on in your own Claude Code sessions.

## Run

```bash
# Python
cd 02_Tool_Design_and_MCP_Integration/Exercises/python
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python 01_tool_description_design.py
python 02_structured_errors.py
python 03_tool_choice_modes.py

# JavaScript
cd 02_Tool_Design_and_MCP_Integration/Exercises/javascript
npm install
node 01_tool_description_design.js
node 02_structured_errors.js
node 03_tool_choice_modes.js

# TypeScript
cd 02_Tool_Design_and_MCP_Integration/Exercises/typescript
npm install
npx ts-node --esm 01_tool_description_design.ts
npx ts-node --esm 02_structured_errors.ts
npx ts-node --esm 03_tool_choice_modes.ts
```

Or, per language, run everything at once via the bundled scripts: `./run.sh` (Linux/macOS) or `.\run.ps1` (Windows).

---

[[../_Index|← Back to Domain 2 Index]]
