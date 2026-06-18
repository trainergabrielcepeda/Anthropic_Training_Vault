---
tags: [topic, prompting]
topic: "02 - Prompt Engineering"
---

# Topic 2 — Prompt Engineering

Prompt engineering is the highest-leverage skill for working with Claude. Small changes in phrasing, structure, and context can dramatically alter output quality. This topic covers the full toolkit — from basic structure to advanced reasoning techniques.

---

## Theory Notes

1. [[Theory/01_Prompt_Structure|01 — Prompt Structure]] — System prompts, conversation turns, roles, and how Claude processes context.
2. [[Theory/02_Advanced_Techniques|02 — Advanced Techniques]] — Few-shot examples, chain-of-thought, XML structuring, and output formatting.
3. [[Theory/03_Prompt_Patterns|03 — Prompt Patterns]] — Reusable patterns: classification, extraction, summarization, transformation.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_system_prompts.py` | Authoring effective system prompts |
| Python | `Exercises/python/02_few_shot.py` | Few-shot prompting patterns |
| Python | `Exercises/python/03_chain_of_thought.py` | CoT and step-by-step reasoning |
| JavaScript | `Exercises/javascript/01_system_prompts.js` | System prompt patterns in Node |
| TypeScript | `Exercises/typescript/01_structured_output.ts` | Structured JSON output via prompting |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 15 questions on prompt design principles and techniques.

---

## Key Concepts Checklist

- [ ] Explain the purpose of the `system` parameter vs the first `user` message
- [ ] Describe when few-shot examples improve over zero-shot prompting
- [ ] Write a chain-of-thought prompt that forces step-by-step reasoning
- [ ] Explain why XML tags help structure complex prompts
- [ ] Identify at least two prompt anti-patterns and how to fix them
