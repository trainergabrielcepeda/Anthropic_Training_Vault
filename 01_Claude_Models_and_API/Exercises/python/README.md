---
tags: [exercises, python, claude-api]
module: "01 - Claude Models & API"
language: Python
---

# Python Exercises — Claude Models & API

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/01_Claude_Models_and_API/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_basic_messages.py` — Messages API Fundamentals

| Part | What it does |
|------|-------------|
| 1 | Single-turn message — send a question and inspect the full response object (`id`, `model`, `stop_reason`, `usage`) |
| 2 | Multi-turn conversation — stateless chat loop; you maintain message history manually |
| 3 | Model comparison — run the same prompt on Haiku and Sonnet, compare output and token cost |
| 4 | Stop reasons — observe `max_tokens` truncation vs natural `end_turn` |

### `02_streaming.py` — Streaming Responses

| Part | What it does |
|------|-------------|
| 1 | Basic streaming with the `with client.messages.stream(...)` context manager |
| 2 | Measure time-to-first-token (TTFT) vs total response time |
| 3 | Access usage stats and the final `Message` object after stream ends |
| 4 | Latency comparison — streaming TTFT vs non-streaming total latency |

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_basic_messages.py
python 02_streaming.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
