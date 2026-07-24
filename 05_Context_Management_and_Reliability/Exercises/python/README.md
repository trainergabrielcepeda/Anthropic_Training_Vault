---
tags: [exercises, python, context-management, reliability]
module: "05 - Context Management & Reliability"
language: Python
---

# Python Exercises — Context Management & Reliability

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_case_facts.py` — Case-Facts Extraction Pattern (Task 5.1)

| Part | What it does |
|------|-------------|
| Verbose tool result | Simulates a `lookup_order` call returning 25+ fields |
| Forced extraction | Uses `tool_choice` to pull only the 5 fields relevant to a delivery-delay conversation |
| Persistent block | Renders a small "CASE FACTS" block kept outside summarized history and re-injected on the next turn |

### `02_escalation_decision.py` — Escalation via Explicit Criteria (Task 5.2)

| Part | What it does |
|------|-------------|
| Explicit criteria + few-shot | System prompt defines exactly when to escalate (explicit human request, policy gap, no progress possible) with worked examples |
| Forced decision tool | Returns a typed `ESCALATE`/`RESOLVE` decision with the matched criterion and reasoning |
| Anti-pattern shown | A self-reported-confidence function included for contrast — **not used** to drive the real decision |

### `03_error_propagation.py` — Structured Error Propagation (Task 5.3)

| Part | What it does |
|------|-------------|
| Simulated subagent timeout | Returns a structured error object: `failure_type`, `attempted_query`, `partial_results`, `alternative_approaches` |
| Anti-patterns shown | A generic string ("search unavailable") and a silently-empty "success" — both included only for contrast |
| Coordinator | A real Claude call reasons over the structured result to decide a recovery action and write a coverage note |

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_case_facts.py
python 02_escalation_decision.py
python 03_error_propagation.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
