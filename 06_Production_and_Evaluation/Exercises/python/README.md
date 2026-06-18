---
tags: [exercises, python, production, evaluation]
module: "06 - Production & Evaluation"
language: Python
---

# Python Exercises — Production & Evaluation

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/06_Production_and_Evaluation/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_prompt_caching.py` — Prompt Caching

| Part | What it does |
|------|-------------|
| 1 | Add `cache_control` breakpoints to a large system prompt |
| 2 | Compare `usage.cache_creation_input_tokens` vs `usage.cache_read_input_tokens` across calls |
| 3 | Verify cache hits on repeated identical requests |
| 4 | Demonstrate correct breakpoint placement (at the end of stable content) |

> **Key concept:** Prompt caching can cut costs by up to 90% when you have a large, repeated system prompt. Cache write is more expensive than a read, so the benefit compounds over multiple calls.

### `03_llm_judge.py` — LLM-as-Judge Evaluation

| Part | What it does |
|------|-------------|
| 1 | Design a judge prompt with an explicit scoring rubric (1–5 per criterion) |
| 2 | Run an eval suite — score multiple model outputs against the rubric |
| 3 | Detect regressions by comparing two system prompt variants |

> **Key concept:** Using a Claude judge is more scalable than human review and more nuanced than exact-match metrics.

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_prompt_caching.py
python 03_llm_judge.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
