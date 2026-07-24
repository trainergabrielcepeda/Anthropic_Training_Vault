---
tags: [exercises, python, structured-output]
module: "04 - Prompt Engineering & Structured Output"
language: Python
---

# Python Exercises — Prompt Engineering & Structured Output

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_structured_extraction.py` — Structured Extraction via `tool_use` (Task 4.3)

| Part | What it does |
|------|-------------|
| Schema | Defines `extract_receipt` with required fields, a nullable `due_date`, and an `enum` + `"other"`/`category_detail` escape hatch |
| Call | Forces the tool via `tool_choice: {"type": "tool", "name": ...}` and reads the result straight from the `tool_use` block |
| Check | Prints whether line items sum to the stated total — demonstrating that schema compliance alone doesn't guarantee semantic correctness |

### `02_validation_retry_loop.py` — Validation, Retry & Feedback (Task 4.4)

| Part | What it does |
|------|-------------|
| Case A | A format/structural extraction error (an easy-to-miss line item) — retry-with-specific-error-feedback fixes it |
| Case B | A field that's genuinely absent from the source document — demonstrates why retrying is ineffective here and a nullable field is the correct design instead |

### `03_few_shot_consistency.py` — Few-Shot for Consistency (Task 4.2)

| Part | What it does |
|------|-------------|
| Before | Detailed written instructions alone, zero-shot, on ambiguous escalation-decision cases |
| After | The same cases with 3 targeted few-shot examples (each with stated reasoning) added |
| Generalization check | A 4th, novel case not modeled directly on any example, to test whether the model learned the underlying decision principle |

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_structured_extraction.py
python 02_validation_retry_loop.py
python 03_few_shot_consistency.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Domain Index]]
