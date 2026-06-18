---
tags: [setup, exercises]
topic: "02 - Prompt Engineering"
---

# Exercises Setup — Prompt Engineering

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## Run

```bash
# Python
cd 02_Prompt_Engineering/Exercises/python
pip install -r requirements.txt
python 01_system_prompts.py
python 02_few_shot.py
python 03_chain_of_thought.py

# JavaScript
cd 02_Prompt_Engineering/Exercises/javascript
npm install && node 01_system_prompts.js

# TypeScript
cd 02_Prompt_Engineering/Exercises/typescript
npm install && npx ts-node 01_structured_output.ts
```

## What Each Exercise Covers

| File | Topic |
| ---- | ----- |
| `01_system_prompts` | Persona, scope, format instructions in system prompt |
| `02_few_shot` | Zero-shot vs few-shot classification |
| `03_chain_of_thought` | CoT prompting and measuring accuracy improvement |
| `01_structured_output.ts` | Forcing JSON output via prefilling and tool use |

---

[[../_Index|← Back to Prompt Engineering Index]]
