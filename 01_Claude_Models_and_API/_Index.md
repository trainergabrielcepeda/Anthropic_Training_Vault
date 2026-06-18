---
tags: [topic, models, api]
topic: "01 - Claude Models & API"
---

# Topic 1 — Claude Models & API

Understanding the Claude model family and the core Messages API is the foundation for every other topic in this vault. This section covers model selection, the request/response lifecycle, and token economics.

---

## Theory Notes

1. [[Theory/01_Model_Overview|01 — Model Overview]] — Haiku, Sonnet, Opus: capabilities, tradeoffs, and when to use each.
2. [[Theory/02_API_Fundamentals|02 — API Fundamentals]] — The Messages endpoint, request parameters, and response structure.
3. [[Theory/03_Tokens_and_Context|03 — Tokens & Context Windows]] — Tokenization, counting tokens, and managing long contexts.

---

## Exercises

[[Exercises/Setup|Setup instructions]] — install dependencies before running.

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_basic_messages.py` | Basic messages call, roles, stop reasons |
| Python | `Exercises/python/02_streaming.py` | Streaming responses with event iteration |
| JavaScript | `Exercises/javascript/01_basic_messages.js` | Same flow in Node.js |
| TypeScript | `Exercises/typescript/01_basic_messages.ts` | Typed SDK usage |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 15 questions covering model selection, API parameters, and token handling.

---

## Key Concepts Checklist

- [ ] Name the three current Claude model tiers and one key use-case per tier
- [ ] Explain the difference between `max_tokens` and the model's context window
- [ ] Describe the `role` field values and when each is used
- [ ] Explain what a `stop_reason` of `end_turn` vs `max_tokens` means
- [ ] Calculate approximate token cost for a given prompt/completion pair
