---
tags: [setup, exercises]
topic: "03 - Tool Use"
---

# Exercises Setup — Tool Use & Function Calling

## Prerequisites

Completed [[../../00_Setup/Getting_Started|Getting Started]] and `ANTHROPIC_API_KEY` is set.

## Run

```bash
# Python
cd 03_Tool_Use/Exercises/python
pip install -r requirements.txt
python 01_single_tool.py
python 02_multi_tool.py

# JavaScript
cd 03_Tool_Use/Exercises/javascript
npm install && node 01_single_tool.js

# TypeScript
cd 03_Tool_Use/Exercises/typescript
npm install && npx ts-node 01_typed_tools.ts
```

## What Each Exercise Covers

| File | Topic |
| ---- | ----- |
| `01_single_tool` | Define one tool, handle the two-turn call cycle |
| `02_multi_tool.py` | Multiple tools, parallel calls, chaining |
| `01_typed_tools.ts` | Strongly typed tool definitions and responses |

---

[[../_Index|← Back to Tool Use & Function Calling Index]]
