"""
Exercise 1 — Basic Messages API
Topic: Claude Models & API

Covers:
  - Single-turn message
  - Inspecting the response object (id, model, stop_reason, usage)
  - Multi-turn conversation (stateless — you manage history)
  - Comparing model tiers on the same prompt
"""

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment


# ─────────────────────────────────────────────
# Part 1: Single-Turn Message
# ─────────────────────────────────────────────
def part1_single_turn():
    print("\n=== Part 1: Single-Turn Message ===")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[
            {"role": "user", "content": "What is the speed of light in metres per second?"}
        ]
    )

    print(f"Response ID : {response.id}")
    print(f"Model       : {response.model}")
    print(f"Stop reason : {response.stop_reason}")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens:{response.usage.output_tokens}")
    print(f"\nContent:\n{response.content[0].text}")


# ─────────────────────────────────────────────
# Part 2: Multi-Turn Conversation
# ─────────────────────────────────────────────
def part2_multi_turn():
    print("\n=== Part 2: Multi-Turn Conversation ===")

    messages = []

    def chat(user_input: str) -> str:
        messages.append({"role": "user", "content": user_input})
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            system="You are a concise science tutor. Keep answers to two sentences.",
            messages=messages
        )
        reply = response.content[0].text
        messages.append({"role": "assistant", "content": reply})
        return reply

    print("User: What is a black hole?")
    print(f"Claude: {chat('What is a black hole?')}")

    print("\nUser: How does Hawking radiation escape it?")
    print(f"Claude: {chat('How does Hawking radiation escape it?')}")

    print("\nUser: Who predicted it?")
    print(f"Claude: {chat('Who predicted it?')}")


# ─────────────────────────────────────────────
# Part 3: Compare Model Tiers
# ─────────────────────────────────────────────
def part3_model_comparison():
    print("\n=== Part 3: Model Comparison ===")

    prompt = "In one paragraph, explain the difference between machine learning and deep learning."
    models = [
        "claude-haiku-4-5-20251001",
        "claude-sonnet-4-6",
    ]

    for model_id in models:
        response = client.messages.create(
            model=model_id,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        tokens = response.usage.input_tokens + response.usage.output_tokens
        print(f"\n--- {model_id} ({tokens} tokens total) ---")
        print(response.content[0].text)


# ─────────────────────────────────────────────
# Part 4: Stop Reasons
# ─────────────────────────────────────────────
def part4_stop_reasons():
    print("\n=== Part 4: Stop Reasons ===")

    # Trigger max_tokens truncation
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,  # deliberately tiny
        messages=[{"role": "user", "content": "Write a 500 word essay about the ocean."}]
    )
    print(f"stop_reason with max_tokens=10: {response.stop_reason}")
    print(f"Truncated output: {response.content[0].text!r}")

    # Normal end_turn
    response2 = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        messages=[{"role": "user", "content": "What is 2 + 2?"}]
    )
    print(f"\nstop_reason for short answer: {response2.stop_reason}")


if __name__ == "__main__":
    part1_single_turn()
    part2_multi_turn()
    part3_model_comparison()
    part4_stop_reasons()
