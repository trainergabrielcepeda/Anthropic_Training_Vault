---
tags: [setup, exercises]
topic: "04 - Prompt Engineering & Structured Output"
---

# Exercises Setup — Prompt Engineering & Structured Output

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set. See [[../../00_Setup/Environment_Setup|Environment Setup]] for per-language SDK install steps and model IDs.

## Run

```bash
# Python
cd 04_Prompt_Engineering_and_Structured_Output/Exercises/python
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python 01_structured_extraction.py
python 02_validation_retry_loop.py
python 03_few_shot_consistency.py

# JavaScript
cd 04_Prompt_Engineering_and_Structured_Output/Exercises/javascript
npm install
node 01_structured_extraction.js
node 02_few_shot_consistency.js

# TypeScript
cd 04_Prompt_Engineering_and_Structured_Output/Exercises/typescript
npm install
npx ts-node --esm 01_structured_extraction.ts
npx ts-node --esm 02_validation_retry_loop.ts
```

Or use the bundled runner scripts (`./run.sh` / `.\run.ps1`) in each language folder to run everything in sequence.

## What Each Exercise Covers

| File | Domain task | What it does |
| ---- | ----------- | ------------- |
| `01_structured_extraction.*` | 4.3 | `tool_use` + JSON schema extraction with required, nullable, and enum-with-"other" fields; reads the result straight from the `tool_use` block |
| `02_validation_retry_loop.*` | 4.4 | Semantic validation (line items vs. stated total) with a retry-with-error-feedback loop, plus a case where retry can't help because the info isn't in the source |
| `03_few_shot_consistency.py` / `02_few_shot_consistency.js` | 4.2 | Before/after comparison: inconsistent zero-shot classification of an ambiguous escalation decision vs. consistent output after adding 3 targeted few-shot examples with reasoning |

> [!note] Why fewer TypeScript files
> The TypeScript folder covers 4.3 and 4.4 (the two most type-relevant tasks — schemas map naturally to interfaces). Python and JavaScript additionally cover the 4.2 few-shot exercise. All three languages hit every task statement in this domain across the vault as a whole once you also read the Theory notes.

---

[[../_Index|← Back to Domain 4 Index]]
