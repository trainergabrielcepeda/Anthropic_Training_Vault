#!/usr/bin/env python3
"""
Rebuild Assets/quiz.html from the Questions.json files in each topic folder.

Usage:
    python3 build_quiz.py

To add, edit, or remove questions, modify the Questions.json file in the
relevant topic folder, then run this script. The quiz.html is regenerated
automatically.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
QUIZ_HTML = ROOT / "Assets" / "quiz.html"

TOPIC_FOLDERS = [
    "01_Claude_Models_and_API",
    "02_Prompt_Engineering",
    "03_Tool_Use",
    "04_Responsible_AI",
    "05_Agentic_Workflows",
    "06_Production_and_Evaluation",
]

def load_banks():
    banks = []
    for folder in TOPIC_FOLDERS:
        path = ROOT / folder / "Questions.json"
        if not path.exists():
            print(f"  WARNING: {path} not found — skipping")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ERROR: {path} has invalid JSON — {e}")
            raise
        banks.append(data)
        print(f"  Loaded {len(data['questions']):>2} questions  ← {folder}/Questions.json")
    return banks

def rebuild_html(banks):
    html = QUIZ_HTML.read_text(encoding="utf-8")
    banks_js = json.dumps(banks, ensure_ascii=False, separators=(",", ":"))
    updated, n = re.subn(
        r"const BANKS = \[.*?\];",
        f"const BANKS = {banks_js};",
        html,
        flags=re.DOTALL,
    )
    if n == 0:
        raise RuntimeError("Could not find 'const BANKS = [...]' in quiz.html — was the file modified?")
    QUIZ_HTML.write_text(updated, encoding="utf-8")

def main():
    print("Building quiz.html from Questions.json files...\n")
    banks = load_banks()
    rebuild_html(banks)
    total = sum(len(b["questions"]) for b in banks)
    print(f"\nDone — {total} questions across {len(banks)} topics written to Assets/quiz.html")

if __name__ == "__main__":
    main()
