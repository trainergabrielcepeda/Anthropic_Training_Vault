---
tags: [topic, safety, responsible-ai]
topic: "04 - Responsible AI & Safety"
---

# Topic 4 — Responsible AI & Safety

Anthropic's mission is the responsible development of AI for the long-term benefit of humanity. This topic covers the principles behind Claude's behavior, the training techniques that shape it, content policies, and how developers implement guardrails in applications.

---

## Theory Notes

1. [[Theory/01_Safety_Philosophy|01 — Safety Philosophy]] — Anthropic's mission, the RSP, and the priority ordering: safe → ethical → principled → helpful.
2. [[Theory/02_Constitutional_AI|02 — Constitutional AI & RLHF]] — How Constitutional AI and RLHF shape Claude's values and behavior.
3. [[Theory/03_Content_Policies|03 — Content Policies & Harm Categories]] — Hardcoded vs softcoded behaviors, harm categories, and operator/user trust levels.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_operator_system_prompts.py` | Restricting and expanding behaviors via system prompt |
| Python | `Exercises/python/02_harm_testing.py` | Probing refusals and understanding the policy boundary |
| JavaScript | `Exercises/javascript/01_content_moderation.js` | Building a basic content moderation layer |
| TypeScript | `Exercises/typescript/01_guardrails.ts` | Typed guardrail patterns |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 15 questions on Anthropic's safety principles, CAI, and policy application.

---

## Key Concepts Checklist

- [ ] State Anthropic's four-level priority ordering for Claude's behavior
- [ ] Explain the difference between hardcoded and softcoded behaviors
- [ ] Describe the three principals in Claude's trust hierarchy (Anthropic, operator, user)
- [ ] Explain what the Responsible Scaling Policy (RSP) governs
- [ ] Give an example of a behavior an operator can enable that is off by default
