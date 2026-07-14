---
tags: [setup, exercises]
topic: "01 - Claude Models & API"
---

# Exercises Setup — Claude Models & API

## Prerequisites

- Completed [[../../00_Setup/Getting_Started|Getting Started]]
- `ANTHROPIC_API_KEY` set in your environment

## Python

```bash
cd 01_Claude_Models_and_API/Exercises/python
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python 01_basic_messages.py
python 02_streaming.py
```

## JavaScript

```bash
cd 01_Claude_Models_and_API/Exercises/javascript
npm install
node 01_basic_messages.js
```

## TypeScript

```bash
cd 01_Claude_Models_and_API/Exercises/typescript
npm install
npx ts-node 01_basic_messages.ts
```

## What Each Exercise Covers

| File | Topic |
| ---- | ----- |
| `01_basic_messages.py/js/ts` | Messages API: single turn, multi-turn, stop reasons |
| `02_streaming.py` | Streaming responses, TTFT measurement |

---

[[../_Index|← Back to Claude Models & API Index]]
