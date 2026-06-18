---
tags: [topic, production, evaluation]
topic: "06 - Production & Evaluation"
---

# Topic 6 — Production & Evaluation

Shipping Claude-powered applications requires more than correct prompts. This topic covers reducing cost and latency with caching and batching, designing evaluation pipelines, and monitoring production systems.

---

## Theory Notes

1. [[Theory/01_Caching_and_Batching|01 — Caching & Batching]] — Prompt caching mechanics, cache breakpoints, and the Batch API for high-volume workloads.
2. [[Theory/02_Cost_Optimization|02 — Cost Optimization]] — Token budgets, model routing, and architectural patterns that reduce spend.
3. [[Theory/03_Evaluation_and_Testing|03 — Evaluation & Testing]] — Designing evals, LLM-as-judge, automated test suites, and regression detection.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_prompt_caching.py` | Implementing and measuring cache hits |
| Python | `Exercises/python/02_batch_api.py` | Submitting and polling Batch API jobs |
| Python | `Exercises/python/03_llm_judge.py` | LLM-as-judge evaluation pattern |
| JavaScript | `Exercises/javascript/01_caching.js` | Caching in Node.js |
| TypeScript | `Exercises/typescript/01_eval_suite.ts` | Typed evaluation suite |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 15 questions on caching, batching, cost strategies, and eval design.

---

## Key Concepts Checklist

- [ ] Explain the minimum token threshold for prompt caching to activate
- [ ] Describe the correct position of `cache_control` breakpoints in a request
- [ ] Explain the tradeoff between Batch API latency and cost savings
- [ ] Design a basic LLM-as-judge eval for a summarization task
- [ ] Name two metrics to monitor in a production Claude deployment
