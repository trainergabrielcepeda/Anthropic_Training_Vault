"""
Exercise 3 — Chain-of-Thought Prompting
Topic: Prompt Engineering

Covers:
  - Zero-shot vs CoT accuracy on reasoning tasks
  - XML-tagged reasoning containers
  - Extracting the final answer from a CoT response
"""

import re
import anthropic

client = anthropic.Anthropic()

PROBLEMS = [
    {
        "question": "A bat and a ball cost $1.10 together. The bat costs $1.00 more than the ball. How much does the ball cost?",
        "answer": "0.05",
    },
    {
        "question": "If you have 3 apples and take away 2, how many apples do you have?",
        "answer": "2",
    },
    {
        "question": "A farmer has 17 sheep. All but 9 die. How many sheep are left?",
        "answer": "9",
    },
    {
        "question": "Tom is twice as old as his brother. In 5 years Tom will be 1.5 times as old. How old is Tom now?",
        "answer": "10",
    },
]


# ─────────────────────────────────────────────
# Part 1: Zero-Shot (No Reasoning)
# ─────────────────────────────────────────────
def solve_zero_shot(question: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        system="Answer with only a number. No explanation.",
        messages=[{"role": "user", "content": question}]
    )
    return r.content[0].text.strip()


# ─────────────────────────────────────────────
# Part 2: Chain-of-Thought with XML Tags
# ─────────────────────────────────────────────
def solve_with_cot(question: str) -> tuple[str, str]:
    """Returns (reasoning, final_answer)."""
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=(
            "Solve the problem step by step inside <thinking> tags. "
            "Then give ONLY the numeric answer inside <answer> tags."
        ),
        messages=[{"role": "user", "content": question}]
    )
    text = r.content[0].text

    thinking_match = re.search(r"<thinking>(.*?)</thinking>", text, re.DOTALL)
    answer_match   = re.search(r"<answer>(.*?)</answer>",   text, re.DOTALL)

    thinking = thinking_match.group(1).strip() if thinking_match else "Not found"
    answer   = answer_match.group(1).strip()   if answer_match   else text.strip()

    return thinking, answer


# ─────────────────────────────────────────────
# Part 3: Compare Accuracy
# ─────────────────────────────────────────────
def part3_compare():
    print("\n=== Zero-Shot vs Chain-of-Thought Accuracy ===\n")

    zero_shot_correct = 0
    cot_correct = 0

    for p in PROBLEMS:
        zs_answer = solve_zero_shot(p["question"])
        thinking, cot_answer = solve_with_cot(p["question"])

        zs_ok  = p["answer"] in zs_answer
        cot_ok = p["answer"] in cot_answer

        if zs_ok:  zero_shot_correct += 1
        if cot_ok: cot_correct += 1

        print(f"Q: {p['question'][:70]}...")
        print(f"   Expected : {p['answer']}")
        print(f"   Zero-shot: {zs_answer!r}  {'✓' if zs_ok else '✗'}")
        print(f"   CoT      : {cot_answer!r}  {'✓' if cot_ok else '✗'}")
        if not cot_ok:
            print(f"   Reasoning: {thinking[:120]}...")
        print()

    print(f"Zero-shot accuracy: {zero_shot_correct}/{len(PROBLEMS)}")
    print(f"CoT accuracy      : {cot_correct}/{len(PROBLEMS)}")


if __name__ == "__main__":
    part3_compare()
