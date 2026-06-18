---
tags: [setup, exercises]
topic: "04 - Responsible AI & Safety"
---

# Exercises Setup — Responsible AI & Safety

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## Run

```bash
# Python
cd 04_Responsible_AI/Exercises/python
pip install -r requirements.txt
python 01_operator_system_prompts.py
python 02_harm_testing.py

# JavaScript
cd 04_Responsible_AI/Exercises/javascript
npm install && node 01_content_moderation.js

# TypeScript
cd 04_Responsible_AI/Exercises/typescript
npm install && npx ts-node 01_guardrails.ts
```

## What Each Exercise Covers

| File | Topic |
| ---- | ----- |
| `01_operator_system_prompts` | Restricting and expanding behaviors via system prompt |
| `02_harm_testing.py` | Probing refusals and understanding the policy boundary |
| `01_content_moderation.js` | Building a basic content moderation layer |
| `01_guardrails.ts` | Typed guardrail patterns |

---

[[../_Index|← Back to Responsible AI & Safety Index]]
