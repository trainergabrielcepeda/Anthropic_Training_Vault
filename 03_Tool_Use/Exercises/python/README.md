---
tags: [exercises, python, tool-use]
module: "03 - Tool Use"
language: Python
---

# Python Exercises — Tool Use & Function Calling

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/03_Tool_Use/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_single_tool.py` — Single Tool

| Part | What it does |
|------|-------------|
| 1 | Define a tool schema (name, description, input_schema) |
| 2 | Detect `stop_reason == "tool_use"` in the response |
| 3 | Execute the tool locally and send back a `tool_result` message |
| 4 | Complete the full two-turn cycle inside a `while` loop |

> **Key concept:** Tool use is two API calls — Claude asks for the tool, you run it, then Claude generates the final answer.

### `02_multi_tool.py` — Multiple Tools

| Part | What it does |
|------|-------------|
| 1 | Pass multiple tool definitions in a single request |
| 2 | Handle parallel tool calls (Claude invokes two tools in one response) |
| 3 | Force a specific tool with `tool_choice` |
| 4 | Use a "fake" tool as a structured data extraction schema |

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_single_tool.py
python 02_multi_tool.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
