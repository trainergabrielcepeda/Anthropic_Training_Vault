"""
Exercise 2 — Streaming Responses
Topic: Claude Models & API

Covers:
  - Streaming with the context manager pattern
  - Measuring time-to-first-token (TTFT)
  - Accumulating the full text from a stream
  - Accessing usage stats after streaming
"""

import time
import anthropic

client = anthropic.Anthropic()


# ─────────────────────────────────────────────
# Part 1: Basic Streaming
# ─────────────────────────────────────────────
def part1_basic_stream():
    print("\n=== Part 1: Basic Streaming ===")
    print("Streaming response (text appears incrementally):\n")

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": "Explain how a rainbow forms. Be detailed."}]
    ) as stream:
        for text_chunk in stream.text_stream:
            print(text_chunk, end="", flush=True)

    print("\n\n[Stream complete]")


# ─────────────────────────────────────────────
# Part 2: Measuring Time-to-First-Token
# ─────────────────────────────────────────────
def part2_measure_ttft():
    print("\n=== Part 2: Time-to-First-Token (TTFT) ===")

    start = time.perf_counter()
    first_token_time = None
    full_text = []

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": "List 5 planets in our solar system."}]
    ) as stream:
        for text_chunk in stream.text_stream:
            if first_token_time is None:
                first_token_time = time.perf_counter()
            full_text.append(text_chunk)

    end = time.perf_counter()

    print(f"TTFT          : {(first_token_time - start) * 1000:.0f} ms")
    print(f"Total time    : {(end - start) * 1000:.0f} ms")
    print(f"Output        : {''.join(full_text)}")


# ─────────────────────────────────────────────
# Part 3: Accessing Final Message and Usage
# ─────────────────────────────────────────────
def part3_final_message():
    print("\n=== Part 3: Final Message and Usage After Streaming ===")

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=128,
        messages=[{"role": "user", "content": "What year did the Berlin Wall fall?"}]
    ) as stream:
        for _ in stream.text_stream:
            pass  # consume the stream
        final = stream.get_final_message()

    print(f"Stop reason   : {final.stop_reason}")
    print(f"Input tokens  : {final.usage.input_tokens}")
    print(f"Output tokens : {final.usage.output_tokens}")
    print(f"Full text     : {final.content[0].text}")


# ─────────────────────────────────────────────
# Part 4: Compare Streaming vs Non-Streaming Latency
# ─────────────────────────────────────────────
def part4_latency_comparison():
    print("\n=== Part 4: Streaming vs Non-Streaming Latency ===")

    prompt = "Write a haiku about the ocean."

    # Non-streaming: wait for full response
    t0 = time.perf_counter()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        messages=[{"role": "user", "content": prompt}]
    )
    non_stream_ms = (time.perf_counter() - t0) * 1000

    # Streaming: measure TTFT
    t0 = time.perf_counter()
    ttft_ms = None
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for _ in stream.text_stream:
            if ttft_ms is None:
                ttft_ms = (time.perf_counter() - t0) * 1000
            break

    print(f"Non-streaming total latency : {non_stream_ms:.0f} ms")
    print(f"Streaming TTFT              : {ttft_ms:.0f} ms")
    print("\nStreaming improves perceived performance even though total tokens are the same.")


if __name__ == "__main__":
    part1_basic_stream()
    part2_measure_ttft()
    part3_final_message()
    part4_latency_comparison()
