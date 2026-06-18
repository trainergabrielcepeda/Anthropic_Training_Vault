---
tags: [exercises, python, agentic-workflows]
module: "05 - Agentic Workflows"
language: Python
---

# Python Exercises — Agentic Workflows

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/05_Agentic_Workflows/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_simple_agent.py` — Simple Agent Loop

| Part | What it does |
|------|-------------|
| 1 | Implement the **observe → plan → act** loop using tool calls |
| 2 | Add a max-turn guard to prevent infinite loops (critical safety practice) |
| 3 | Register multiple tools in a single agent |
| 4 | Log each step (turn number, tool called, result) for observability |

> **Key concept:** An agent is just a `while` loop around `messages.create`. The loop exits when `stop_reason == "end_turn"` (no more tools) or the turn limit is hit.

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_simple_agent.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
