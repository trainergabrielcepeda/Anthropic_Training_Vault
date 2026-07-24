---
tags: [exercises, python, agentic-architecture]
module: "01 - Agentic Architecture & Orchestration"
language: Python
---

# Python Exercises — Agentic Architecture & Orchestration

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_agentic_loop.py` — The Agentic Loop, Keyed Off `stop_reason` (Task 1.1)

| Part | What it does |
|------|-------------|
| 1 | Loop control keyed off `response.stop_reason` — continue on `"tool_use"`, terminate on `"end_turn"` |
| 2 | Append the full assistant turn (including `tool_use` blocks) plus one `user` turn with all `tool_result` blocks |
| 3 | A `MAX_ITERATIONS` cap used only as a safety-net circuit breaker, never as the primary stop condition |
| 4 | A minimal Customer Support Resolution Agent (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`) |

> **Key concept:** `stop_reason`, not assistant text content, is the only thing your control flow should branch on.

### `02_coordinator_subagents.py` — Coordinator Dispatching to Parallel Subagents (Tasks 1.2, 1.3)

| Part | What it does |
|------|-------------|
| 1 | A coordinator decomposes a goal and dispatches to 2+ "subagents" — separate, isolated `messages.create()` calls with distinct system prompts and self-contained prompts |
| 2 | Parallel dispatch via a thread pool, standing in for the Agent SDK's "multiple `Task` calls in one coordinator turn" pattern |
| 3 | Coordinator synthesis, followed by a coverage-gap check that re-delegates a targeted follow-up if the synthesis looks incomplete |

> **Key concept:** subagents never automatically inherit the coordinator's history — every fact they need is written directly into their prompt. See the file's module docstring for exactly how this maps to the Agent SDK's `Task` tool and `AgentDefinition`.

### `03_hook_interception.py` — Hook-Style Interception & Normalization (Task 1.5)

| Part | What it does |
|------|-------------|
| 1 | A `PreToolUse`-style hook that blocks `process_refund` calls over $500 and redirects toward `escalate_to_human` |
| 2 | A `PostToolUse`-style hook that normalizes a Unix timestamp and a numeric status code into consistent formats before the model sees them |
| 3 | Two runs of the same agent showing the allowed case and the blocked case |

> **Key concept:** hooks are a deterministic guarantee (the code always runs); a system-prompt instruction is a probabilistic guideline (the model might skip it).

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_agentic_loop.py
python 02_coordinator_subagents.py
python 03_hook_interception.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
