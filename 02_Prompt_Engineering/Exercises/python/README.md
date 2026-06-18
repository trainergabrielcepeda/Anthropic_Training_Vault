---
tags: [exercises, python, prompt-engineering]
module: "02 - Prompt Engineering"
language: Python
---

# Python Exercises — Prompt Engineering

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/02_Prompt_Engineering/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_system_prompts.py` — System Prompts

| Part | What it does |
|------|-------------|
| 1 | Compare no system prompt vs with system prompt on the same question |
| 2 | Define a persona via the system prompt and observe tone shift |
| 3 | Enforce output format constraints (e.g., bullet-only, JSON) through the system |
| 4 | Assistant prefilling — prepend text to the assistant turn to steer the response |

### `02_few_shot.py` — Few-Shot Prompting

| Part | What it does |
|------|-------------|
| 1 | Zero-shot classification vs few-shot with labeled examples |
| 2 | Measure output consistency by running the same prompt multiple times |
| 3 | Test how example quality affects classification accuracy |

### `03_chain_of_thought.py` — Chain-of-Thought Prompting

| Part | What it does |
|------|-------------|
| 1 | Zero-shot answer vs CoT answer on classic reasoning traps (bat-and-ball, etc.) |
| 2 | Use XML tags (`<thinking>`) as a structured reasoning container |
| 3 | Extract the final answer from a CoT response using regex |

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_system_prompts.py
python 02_few_shot.py
python 03_chain_of_thought.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
