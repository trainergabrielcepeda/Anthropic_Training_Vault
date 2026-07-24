---
tags: [exercises, python, tool-design, mcp]
module: "02 - Tool Design & MCP Integration"
language: Python
---

# Python Exercises — Tool Design & MCP Integration

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/vaults/Anthropic_Training_Vault/02_Tool_Design_and_MCP_Integration/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_tool_description_design.py` — Task 2.1

| Part | What it does |
|------|-------------|
| A | Two tools with vague, overlapping descriptions (`analyze_content` vs `analyze_document`) and unreliable routing across similar queries |
| B | The same capability split into three purpose-specific tools (`summarize_content`, `extract_data_points`, `verify_claim_against_source`) with differentiated, boundaried descriptions — routes consistently |

> **Key concept:** Tool descriptions are the primary signal Claude uses for tool selection. Vague or overlapping descriptions — not tool count, not ordering — are the usual root cause of misrouting.

### `02_structured_errors.py` — Task 2.2

| Part | What it does |
|------|-------------|
| 1 | A `process_refund` tool returns structured MCP-style errors (`isError`, `errorCategory`, `isRetryable`, `message`) for transient/validation/business/permission failures |
| 2 | Client-side logic branches on `errorCategory` — retrying transient failures locally, propagating everything else with full context |
| 3 | The structured error is wired into a real Claude conversation via `tool_result`, so Claude's final answer reflects the actual failure reason instead of a generic message |

### `03_tool_choice_modes.py` — Task 2.3

| Part | What it does |
|------|-------------|
| 1 | `tool_choice={"type": "tool", "name": "extract_metadata"}` — forces a specific tool to run first |
| 2 | `tool_choice={"type": "auto"}` — Claude freely chooses the next step once the forced step is done |
| 3 | `tool_choice={"type": "any"}` — guarantees a tool call happens, without dictating which tool |

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_tool_description_design.py
python 02_structured_errors.py
python 03_tool_choice_modes.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
