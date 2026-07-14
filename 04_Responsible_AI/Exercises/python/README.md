---
tags: [exercises, python, responsible-ai]
module: "04 - Responsible AI"
language: Python
---

# Python Exercises — Responsible AI & Safety

> [📂 Open folder in file manager](file:///home/gabrielcepeda/Documentos/obsidian/Anthropic_Training_Vault/04_Responsible_AI/Exercises/python)

## Prerequisites

- Python 3.9+
- `ANTHROPIC_API_KEY` set in your environment
- Install dependencies: `pip install -r requirements.txt`

## Exercises

### `01_operator_system_prompts.py` — Operator System Prompts

| Part | What it does |
|------|-------------|
| 1 | Restrict a default-ON behavior via system prompt (debate practice, one-sided argumentation) |
| 2 | Enable a default-OFF behavior via system prompt (harm-reduction platform, controlled-substance detail) |
| 3 | Confirm a hardcoded absolute limit resists override even when the system prompt claims full authority |

> **Key concept:** operators sit above users but below Anthropic in the trust hierarchy — they can toggle softcoded defaults but never unlock hardcoded limits.

### `02_harm_testing.py` — Harm Testing

| Part | What it does |
|------|-------------|
| 1 | Compare responses to freely-available vs. genuinely uplifting requests (counterfactual impact) |
| 2 | Show how legitimate professional context shifts the cost-benefit balance |
| 3 | Run a small batch of probes through a classifier and summarize decline rate |

> **Key concept:** Claude weighs probability, severity, breadth, and counterfactual impact of harm against the legitimacy of the stated context — it's a balance, not a keyword blocklist.

## How to Run

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run individually
python 01_operator_system_prompts.py
python 02_harm_testing.py

# Or run all via script
./run.sh          # Linux / macOS
.\run.ps1         # Windows PowerShell
```

---
[[../Setup|← Setup]] | [[../../_Index|← Module Index]]
