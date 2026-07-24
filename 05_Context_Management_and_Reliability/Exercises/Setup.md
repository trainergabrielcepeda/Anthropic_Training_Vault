---
tags: [setup, exercises]
topic: "05 - Context Management & Reliability"
---

# Exercises Setup — Context Management & Reliability

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set in your environment. See [[../../00_Setup/Environment_Setup|Environment Setup]] for per-language install steps and the current model-ID reference table.

## What These Exercises Build

All three languages implement the same three reliability patterns from this domain's theory notes:

1. **Case-facts extraction (Task 5.1)** — pull structured transactional facts (order ID, dates, amount) out of a verbose, 20+ field tool result the moment it's returned, and re-inject only that small block into subsequent prompts — never the raw payload, and never something that passes through a summarizer.
2. **Escalation decisions via explicit criteria (Task 5.2)** — a decision function driven by an explicit criteria list plus few-shot examples in the system prompt, not a self-reported confidence score. It correctly separates "customer explicitly asked for a human → escalate now," "policy gap → escalate," and "complex but policy-covered → resolve."
3. **Structured error propagation (Task 5.3)** — a simulated subagent call that times out and returns a structured error object (`failure_type`, `attempted_query`, `partial_results`, `alternative_approaches`) instead of a generic string or a silently-empty "success," plus a coordinator that reasons over that structure to decide how to recover.

## Run

```bash
# Python
cd 05_Context_Management_and_Reliability/Exercises/python
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python 01_case_facts.py
python 02_escalation_decision.py
python 03_error_propagation.py

# JavaScript
cd 05_Context_Management_and_Reliability/Exercises/javascript
npm install
node 01_case_facts.js
node 02_escalation_and_errors.js

# TypeScript
cd 05_Context_Management_and_Reliability/Exercises/typescript
npm install
npx ts-node --esm 01_context_reliability.ts
```

Or use the per-language `run.sh` (Linux/macOS) / `run.ps1` (Windows) scripts in each folder to install dependencies and run every exercise in sequence.

## What Each Exercise Covers

| File | Language | Topic |
| ---- | -------- | ----- |
| `01_case_facts.py` / `.js` / (Part A of `.ts`) | Python, JS, TS | Trimming verbose tool output into a persistent case-facts block |
| `02_escalation_decision.py` / (Part B of `02_escalation_and_errors.js`, `.ts`) | Python, JS, TS | Explicit-criteria + few-shot escalation, contrasted with unreliable self-reported confidence |
| `03_error_propagation.py` / (Part B of `02_escalation_and_errors.js`, Part C of `.ts`) | Python, JS, TS | Structured error context on a simulated subagent timeout vs. the generic-string and silent-empty-success anti-patterns |

> [!note] Deviation from a strict 1:1 file mapping
> Python keeps each pattern in its own file (3 files) to mirror the three task statements exactly. JavaScript combines escalation + error propagation into one file (2 files total) and TypeScript combines all three patterns into a single typed file (1 file), per the "2-3 well-commented files per language" scope in this domain's brief — the same three patterns are demonstrated in every language, just grouped differently for brevity.

---

[[../_Index|← Back to Context Management & Reliability Index]]
