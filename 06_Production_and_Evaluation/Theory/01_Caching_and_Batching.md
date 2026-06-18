---
tags: [theory, production, caching, batching]
topic: "06 - Production & Evaluation"
---

# Caching & Batching

## Prompt Caching

Prompt caching allows reusing the KV cache of a prompt prefix across multiple requests. If the cached portion is unchanged, Anthropic processes it at a significantly reduced cost and latency.

### How It Works

You mark a breakpoint in your request with `{"type": "ephemeral"}` in a `cache_control` block. Everything up to that point is eligible for caching.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert on the following legal document.",
        },
        {
            "type": "text",
            "text": very_long_legal_document,      # 50,000 tokens
            "cache_control": {"type": "ephemeral"} # ← cache up to here
        }
    ],
    messages=[{"role": "user", "content": "What are the termination clauses?"}]
)
```

On the second request with the same prefix (and same model/version), the cached portion is read from cache instead of being re-processed.

---

## Cache Rules

| Rule | Detail |
| ---- | ------ |
| Minimum cache size | 1,024 tokens (Haiku), 2,048 tokens (Sonnet/Opus) |
| Cache TTL | 5 minutes (ephemeral). Resets on each cache hit |
| Max cache breakpoints | Up to 4 per request |
| What is cached | Everything before the last `cache_control` breakpoint |
| Cache invalidation | Any change to the cached prefix invalidates the cache |

> [!warning] Cache ordering matters
> The cached prefix must be **identical** across requests. Even a single character difference misses the cache. Dynamic content (timestamps, user names) should go **after** the cache breakpoint.

---

## Cache Breakpoint Placement

Optimal placement: at the end of your longest stable prefix.

```python
system=[
    # STABLE — put cache_control here
    {"type": "text", "text": static_instructions, "cache_control": {"type": "ephemeral"}},
]
messages=[
    # DYNAMIC — changes per user, no cache_control needed
    {"role": "user", "content": user_question}
]
```

For multi-turn conversations, move the breakpoint to the end of the accumulated history:

```python
# Last message in the messages array gets the cache_control
messages[-1]["content"][-1]["cache_control"] = {"type": "ephemeral"}
```

---

## Cache Cost Impact

Typical caching savings for a 10,000-token system prompt reused 100 times:
- Without caching: 100 × 10,000 input tokens = 1M tokens billed
- With caching (after first request): 1 × 10,000 (write) + 99 × 10,000 × 0.1 (read) = 109,000 tokens equivalent

> [!tip] Best use cases for caching
> - Large static documents (legal, medical, technical)
> - Long system prompts shared across many users
> - Tool definitions for agents with many tools
> - Multi-turn conversations (cache the growing history)

---

## The Batch API

The Batch API allows submitting up to 100,000 requests in a single batch. Requests are processed asynchronously within 24 hours at a 50% cost discount.

### When to Use

| Scenario | Use Batch API | Use Real-Time API |
| -------- | ------------- | ----------------- |
| Classifying 50,000 documents overnight | Yes | No |
| Generating product descriptions for catalog | Yes | No |
| Real-time chat response | No | Yes |
| User waiting for response | No | Yes |

### Submitting a Batch

```python
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"req-{i}",
            "params": {
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 256,
                "messages": [{"role": "user", "content": texts[i]}]
            }
        }
        for i in range(len(texts))
    ]
)
print(batch.id)  # store this
```

### Polling and Retrieving Results

```python
import time

while True:
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status == "ended":
        break
    time.sleep(60)

for result in client.messages.batches.results(batch_id):
    if result.result.type == "succeeded":
        print(result.custom_id, result.result.message.content[0].text)
    else:
        print(result.custom_id, "FAILED:", result.result.error)
```

---

## Related Notes

- [[02_Cost_Optimization|Cost Optimization]]
- [[../../01_Claude_Models_and_API/Theory/03_Tokens_and_Context|Tokens & Context — token counting]]
- [[../../01_Claude_Models_and_API/Theory/01_Model_Overview|Model Overview — per-tier pricing]]

---

[[../_Index|← Back to Production & Evaluation Index]]
