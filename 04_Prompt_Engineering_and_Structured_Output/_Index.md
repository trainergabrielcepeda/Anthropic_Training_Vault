---
tags: [topic, structured-output, prompting]
topic: "04 - Prompt Engineering & Structured Output"
---

# Domain 4 · Prompt Engineering & Structured Output

**20% of the exam.** The exam assumes you already know basic prompt mechanics (system/user roles, message structure). This domain tests a narrower, more specific set of skills: writing precision-focused review criteria, using few-shot examples deliberately, enforcing structured output via `tool_use`, building validation/retry loops, choosing between synchronous and batch APIs, and designing review architectures that catch what a single self-reviewing pass misses.

> [!note] Scope check
> See [[../00_Exam_Guide/Out_of_Scope_Topics|Out-of-Scope Topics]] — generic prompt-engineering trivia (basic role prompting, generic chain-of-thought, general persona design) is **not** what this domain tests. Everything below maps to an official task statement.

---

## Official Task Statements

1. **4.1 — Explicit criteria for precision.** Vague instructions ("be conservative," "high-confidence only") fail to improve precision; specific categorical criteria (what to report vs. skip, per category, with severity examples) do. False positives in one category erode trust in accurate categories too.
2. **4.2 — Few-shot for consistency.** 2-4 targeted examples with stated reasoning teach judgment that generalizes to novel cases — for ambiguous tool selection, output-format consistency, false-positive reduction via contrast, varied document structures, and empty/null extraction.
3. **4.3 — `tool_use` + JSON schemas.** The most reliable path to schema-compliant output. `tool_choice`: `auto` vs. `any` vs. a forced specific tool. Required vs. nullable fields to prevent fabrication; enum + `"other"`/detail for extensible categories.
4. **4.4 — Validation, retry, and feedback loops.** Retry-with-specific-error-feedback fixes format/structural errors; it cannot fix information that's genuinely absent from the source. `detected_pattern` fields and `conflict_detected` booleans support downstream analysis and self-correction.
5. **4.5 — Batch processing strategy.** The Message Batches API: 50% cheaper, up to 24h, no latency SLA — right for overnight/weekly non-blocking work, wrong for blocking checks. `custom_id` correlation, resubmitting only failures, sampling before scaling.
6. **4.6 — Multi-instance and multi-pass review.** Self-review is weaker than independent review because the generator retains its own reasoning context. Large multi-file reviews split into per-file + cross-file integration passes to avoid attention dilution.

---

## Theory Notes

1. [[Theory/01_Precision_and_Few_Shot_Prompting|01 — Precision & Few-Shot Prompting]] — Tasks 4.1 & 4.2
2. [[Theory/02_Structured_Output_and_Validation|02 — Structured Output & Validation]] — Tasks 4.3 & 4.4
3. [[Theory/03_Batch_Processing_and_Multi_Pass_Review|03 — Batch Processing & Multi-Pass Review]] — Tasks 4.5 & 4.6

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | Task(s) |
| -------- | ---- | ------- |
| Python | `Exercises/python/01_structured_extraction.py` | 4.3 |
| Python | `Exercises/python/02_validation_retry_loop.py` | 4.4 |
| Python | `Exercises/python/03_few_shot_consistency.py` | 4.2 |
| JavaScript | `Exercises/javascript/01_structured_extraction.js` | 4.3, 4.4 |
| JavaScript | `Exercises/javascript/02_few_shot_consistency.js` | 4.2 |
| TypeScript | `Exercises/typescript/01_structured_extraction.ts` | 4.3 |
| TypeScript | `Exercises/typescript/02_validation_retry_loop.ts` | 4.3, 4.4 |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 18 original scenario-based questions covering all six task statements.

---

## Related

- [[../00_Exam_Guide/_Index|Exam Guide]]
- [[../00_Exam_Guide/Exam_Scenarios|Exam Scenarios]] — Scenario 5 (Claude Code for CI/CD) and Scenario 6 (Structured Data Extraction) are this domain's primary anchors
- [[../Home|Home]]

---

## Key Concepts Checklist

- [ ] Explain why "be conservative" fails to improve precision and what to write instead
- [ ] Describe how a false-positive rate in one finding category damages trust in unrelated, accurate categories
- [ ] Write 2-4 few-shot examples for an ambiguous decision, each with stated reasoning
- [ ] Explain why few-shot examples generalize to novel cases rather than only matching memorized ones
- [ ] Define an extraction tool schema with required, nullable, and enum + `"other"` fields
- [ ] State the difference between `tool_choice: "auto"`, `"any"`, and a forced specific tool, and when to use each
- [ ] Explain why `tool_use` eliminates syntax errors but not semantic errors
- [ ] Design a retry-with-error-feedback loop and identify when retrying cannot help
- [ ] State the Message Batches API's cost/latency tradeoff and when it's (in)appropriate
- [ ] Calculate a batch submission cadence from an SLA constraint
- [ ] Explain why an independent review instance outperforms self-review on generated output
- [ ] Describe when to split a review into per-file and cross-file integration passes

---

[[../Home|← Home]]
