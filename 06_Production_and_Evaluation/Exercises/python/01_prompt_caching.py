"""
Exercise 1 — Prompt Caching
Topic: Production & Evaluation

Covers:
  - Adding cache_control breakpoints to system prompts
  - Measuring cache write vs cache read in usage stats
  - Verifying cache hits on repeated requests
  - Correct cache breakpoint placement
"""

import anthropic

client = anthropic.Anthropic()

# A large, static document to cache (simulated)
LARGE_DOCUMENT = """
ACME Corporation Employee Handbook — Version 12.3

Chapter 1: Company Values
ACME Corporation was founded in 1985 with a mission to deliver reliable products
to customers worldwide. Our core values are: Integrity, Innovation, and Impact.
Employees are expected to embody these values in every interaction.

Chapter 2: Code of Conduct
All employees must comply with applicable laws and regulations. Conflicts of
interest must be disclosed to HR within 10 business days of identification.
Company resources are for business use only. Personal use must be minimal and
must not interfere with work responsibilities.

Chapter 3: Benefits
Health insurance is provided from day one of employment. The company matches
401(k) contributions up to 4% of salary. Employees accrue 15 vacation days per
year for the first 5 years, then 20 days per year thereafter.

Chapter 4: Performance Reviews
Performance reviews are conducted annually in December. Employees set goals in
January and mid-year check-ins occur in June. Ratings range from 1 (below
expectations) to 5 (exceptional). Raises are effective the following February.

Chapter 5: Remote Work Policy
Employees may work remotely up to 3 days per week with manager approval.
Remote workers must be available during core hours of 10am-3pm local time.
All remote work must comply with the company's information security policy.
""" * 10  # Repeat to create a large document (~2500 tokens)


# ─────────────────────────────────────────────
# Part 1: Request WITHOUT caching
# ─────────────────────────────────────────────
def part1_without_cache(question: str):
    print("\n=== Part 1: Without Prompt Caching ===")
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=f"You are an HR assistant. Answer questions about this handbook:\n\n{LARGE_DOCUMENT}",
        messages=[{"role": "user", "content": question}]
    )
    usage = response.usage
    print(f"Input tokens  : {usage.input_tokens}")
    print(f"Output tokens : {usage.output_tokens}")
    print(f"Cache write   : {getattr(usage, 'cache_creation_input_tokens', 0)}")
    print(f"Cache read    : {getattr(usage, 'cache_read_input_tokens', 0)}")
    print(f"Answer        : {response.content[0].text[:120]}...")


# ─────────────────────────────────────────────
# Part 2: Request WITH caching (first call — cache write)
# ─────────────────────────────────────────────
def part2_with_cache_write(question: str):
    print("\n=== Part 2: With Prompt Caching (First Call — Cache Write) ===")
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": "You are an HR assistant. Answer questions about this handbook:",
            },
            {
                "type": "text",
                "text": LARGE_DOCUMENT,
                "cache_control": {"type": "ephemeral"}  # ← cache breakpoint
            }
        ],
        messages=[{"role": "user", "content": question}]
    )
    usage = response.usage
    print(f"Input tokens  : {usage.input_tokens}")
    print(f"Output tokens : {usage.output_tokens}")
    print(f"Cache write   : {getattr(usage, 'cache_creation_input_tokens', 0)}")
    print(f"Cache read    : {getattr(usage, 'cache_read_input_tokens', 0)}")
    print(f"Answer        : {response.content[0].text[:120]}...")
    return response


# ─────────────────────────────────────────────
# Part 3: Second request — should be a cache HIT
# ─────────────────────────────────────────────
def part3_cache_hit(question: str):
    print("\n=== Part 3: With Prompt Caching (Second Call — Cache Read) ===")
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": "You are an HR assistant. Answer questions about this handbook:",
            },
            {
                "type": "text",
                "text": LARGE_DOCUMENT,
                "cache_control": {"type": "ephemeral"}  # same prefix = cache hit
            }
        ],
        messages=[{"role": "user", "content": question}]
    )
    usage = response.usage
    print(f"Input tokens  : {usage.input_tokens}")
    print(f"Output tokens : {usage.output_tokens}")
    print(f"Cache write   : {getattr(usage, 'cache_creation_input_tokens', 0)}")
    print(f"Cache read    : {getattr(usage, 'cache_read_input_tokens', 0)}")
    cache_read = getattr(usage, 'cache_read_input_tokens', 0)
    print(f"\n{'✓ Cache HIT' if cache_read > 0 else '✗ Cache MISS — wait and retry'}")
    print(f"Answer        : {response.content[0].text[:120]}...")


if __name__ == "__main__":
    q1 = "How many vacation days do employees get after 5 years?"
    q2 = "What is the 401k match percentage?"

    part1_without_cache(q1)
    part2_with_cache_write(q1)
    part3_cache_hit(q2)  # different question, same cached prefix → cache hit
