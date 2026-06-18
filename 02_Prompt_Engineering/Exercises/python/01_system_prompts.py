"""
Exercise 1 — System Prompts
Topic: Prompt Engineering

Covers:
  - Effect of system prompt on tone and behavior
  - Persona definition
  - Format constraints
  - Assistant prefilling
"""

import anthropic

client = anthropic.Anthropic()

QUESTION = "Can you help me understand compound interest?"


# ─────────────────────────────────────────────
# Part 1: No System Prompt vs With System Prompt
# ─────────────────────────────────────────────
def part1_system_prompt_effect():
    print("\n=== Part 1: No System Prompt vs With System Prompt ===\n")

    # Without system prompt
    r1 = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": QUESTION}]
    )
    print("WITHOUT system prompt:")
    print(r1.content[0].text)

    # With a specific persona system prompt
    r2 = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=(
            "You are a financial advisor speaking to a 10-year-old. "
            "Use simple words and a fun analogy. Answer in exactly 3 sentences."
        ),
        messages=[{"role": "user", "content": QUESTION}]
    )
    print("\nWITH persona system prompt:")
    print(r2.content[0].text)


# ─────────────────────────────────────────────
# Part 2: Format Constraints
# ─────────────────────────────────────────────
def part2_format_constraints():
    print("\n=== Part 2: Format Constraints ===\n")

    formats = {
        "Bullet list": "Respond with a markdown bullet list only. No intro, no conclusion.",
        "JSON":        'Respond with a JSON object only: {"definition": str, "formula": str, "example": str}',
        "One sentence":"Respond in exactly one sentence.",
    }

    for fmt_name, instruction in formats.items():
        r = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=instruction,
            messages=[{"role": "user", "content": QUESTION}]
        )
        print(f"Format [{fmt_name}]:")
        print(r.content[0].text)
        print()


# ─────────────────────────────────────────────
# Part 3: Assistant Prefilling
# ─────────────────────────────────────────────
def part3_prefilling():
    print("\n=== Part 3: Assistant Prefilling ===\n")

    # Prefill forces JSON without needing JSON instructions
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[
            {"role": "user", "content": "Explain compound interest."},
            {"role": "assistant", "content": "{"}  # prefill starts the JSON
        ]
    )
    # The response continues from the prefill — prepend it back
    full_response = "{" + r.content[0].text
    print("Prefilled JSON response:")
    print(full_response)


if __name__ == "__main__":
    part1_system_prompt_effect()
    part2_format_constraints()
    part3_prefilling()
