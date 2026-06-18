"""
Exercise 2 — Few-Shot Prompting
Topic: Prompt Engineering

Covers:
  - Zero-shot vs few-shot classification
  - Measuring consistency across repeated calls
  - Effect of example quality on output
"""

import anthropic

client = anthropic.Anthropic()

TEST_MESSAGES = [
    "I've been waiting for 3 days and still no response!",
    "How do I change my billing address?",
    "Your team was incredibly helpful, thank you!",
    "The app crashed and I lost all my data.",
    "Is there a student discount available?",
]


# ─────────────────────────────────────────────
# Part 1: Zero-Shot Classification
# ─────────────────────────────────────────────
def classify_zero_shot(message: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        system=(
            "Classify the customer message as exactly one of: "
            "COMPLAINT, QUESTION, COMPLIMENT. "
            "Respond with only the category. Nothing else."
        ),
        messages=[{"role": "user", "content": message}]
    )
    return r.content[0].text.strip()


# ─────────────────────────────────────────────
# Part 2: Few-Shot Classification
# ─────────────────────────────────────────────
FEW_SHOT_SYSTEM = """Classify customer messages as COMPLAINT, QUESTION, or COMPLIMENT.

Examples:
Message: "Your app keeps crashing!"
Classification: COMPLAINT

Message: "What are your business hours?"
Classification: QUESTION

Message: "The new design is beautiful!"
Classification: COMPLIMENT

Message: "I've been charged twice this month."
Classification: COMPLAINT

Message: "Can I transfer my account to another email?"
Classification: QUESTION

Respond with only the classification. Nothing else."""


def classify_few_shot(message: str) -> str:
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        system=FEW_SHOT_SYSTEM,
        messages=[{"role": "user", "content": f"Message: {message}\nClassification:"}]
    )
    return r.content[0].text.strip()


# ─────────────────────────────────────────────
# Part 3: Compare and Measure
# ─────────────────────────────────────────────
def part3_compare():
    print("\n=== Comparing Zero-Shot vs Few-Shot Classification ===\n")
    print(f"{'Message':<50} {'Zero-Shot':<15} {'Few-Shot':<15}")
    print("-" * 80)

    for msg in TEST_MESSAGES:
        zs = classify_zero_shot(msg)
        fs = classify_few_shot(msg)
        match = "✓" if zs == fs else "✗ DIFFER"
        display = msg[:47] + "..." if len(msg) > 47 else msg
        print(f"{display:<50} {zs:<15} {fs:<15} {match}")


if __name__ == "__main__":
    part3_compare()
