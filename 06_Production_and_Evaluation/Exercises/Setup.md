---
tags: [setup, exercises]
topic: "06 - Production & Evaluation"
---

# Exercises Setup — Production & Evaluation

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## Run

```bash
# Python
cd 06_Production_and_Evaluation/Exercises/python
pip install -r requirements.txt
python 01_prompt_caching.py
python 02_batch_api.py
python 03_llm_judge.py

# JavaScript
cd 06_Production_and_Evaluation/Exercises/javascript
npm install && node 01_caching.js

# TypeScript
cd 06_Production_and_Evaluation/Exercises/typescript
npm install && npx ts-node 01_eval_suite.ts
```

## What Each Exercise Covers

| File | Topic |
| ---- | ----- |
| `01_prompt_caching.py` | Cache breakpoints, measuring cache hit vs miss |
| `02_batch_api.py` | Submit a batch, poll for completion, retrieve results |
| `03_llm_judge.py` | LLM-as-judge eval pattern with scoring rubric |
| `01_eval_suite.ts` | Typed eval suite with regression detection |

---

[[../_Index|← Back to Production & Evaluation Index]]
