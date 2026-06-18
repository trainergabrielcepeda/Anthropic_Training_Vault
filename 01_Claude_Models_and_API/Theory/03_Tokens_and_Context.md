---
tags: [theory, tokens, context]
topic: "01 - Claude Models & API"
---

# Tokens & Context Windows

## What Is a Token?

Claude processes text as **tokens**, not characters or words. A token is roughly 3–4 characters of English text, but the exact count depends on the tokenizer.

| Content | Approximate Tokens |
| ------- | ------------------ |
| 1 word (English) | ~1.3 tokens |
| 1 paragraph (100 words) | ~130 tokens |
| 1 page (500 words) | ~650 tokens |
| 1,000 tokens | ~750 words |
| Full novel (100k words) | ~130,000 tokens |

> [!note] Non-English text uses more tokens
> CJK characters (Chinese, Japanese, Korean) and many other scripts consume more tokens per character than English. Code is typically token-efficient.

---

## Context Window

The **context window** is the total number of tokens Claude can process in a single request — inputs **plus** outputs combined.

```
context_window = input_tokens + output_tokens
```

All current Claude models support a **200,000 token** context window (~150,000 words or ~500 pages).

> [!warning] Context ≠ memory
> Claude does not remember previous API calls. The context window only covers the current request. To give Claude history, you must include prior messages in the `messages` array.

---

## Counting Tokens Before Sending

Use the token counting endpoint to estimate cost and check you are within limits:

```python
import anthropic
client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Explain quantum entanglement."}]
)
print(response.input_tokens)  # e.g. 23
```

> [!tip] Count before large requests
> Always count tokens before sending very large documents (legal contracts, codebases, etc.) to avoid hitting context limits mid-processing.

---

## How Tokens Affect Cost

Pricing is per million tokens (MTok), charged separately for input and output.

```
cost = (input_tokens / 1_000_000 × input_price)
     + (output_tokens / 1_000_000 × output_price)
```

Output tokens are typically 3–5× more expensive than input tokens. To minimize cost:
- Write concise system prompts.
- Ask for concise responses when verbosity is not needed.
- Use `max_tokens` to cap runaway generation.
- Use Haiku for tasks that do not require Sonnet/Opus quality.

---

## Managing Long Contexts

When inputs approach the context window:

1. **Summarize** earlier conversation turns and replace them with a summary block.
2. **Chunk** large documents and process them in parallel with separate requests.
3. **Retrieve** only relevant sections via RAG rather than sending the full document (covered in [[../../06_Production_and_Evaluation/_Index|Production & Evaluation]]).
4. **Use prompt caching** to avoid re-tokenizing repeated prefixes across requests (see [[../../06_Production_and_Evaluation/Theory/01_Caching_and_Batching|Caching & Batching]]).

---

## Token Distribution Patterns

| Pattern | Input Tokens | Output Tokens | When to Use |
| ------- | ------------ | ------------- | ----------- |
| Classification | High | Very low (~10) | Sentiment, routing |
| Summarization | High | Medium (~500) | Document processing |
| Generation | Low | High (~2000) | Creative writing, reports |
| Q&A | Medium | Medium | Chat, support |

---

## Related Notes

- [[01_Model_Overview|Model Overview — context window limits per tier]]
- [[02_API_Fundamentals|API Fundamentals — `max_tokens` parameter]]
- [[../../06_Production_and_Evaluation/Theory/01_Caching_and_Batching|Caching & Batching]]

---

[[../_Index|← Back to Claude Models & API Index]]
