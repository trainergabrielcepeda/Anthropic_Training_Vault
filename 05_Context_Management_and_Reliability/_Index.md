---
tags: [topic, context-management, reliability, escalation, provenance]
topic: "05 - Context Management & Reliability"
---

# Domain 5 — Context Management & Reliability

**Domain 5 · 15% of the exam.**

This is the domain that turns a working demo into a system that survives production: preserving what matters across long conversations, calibrating when to escalate to a human instead of guessing, propagating errors across multi-agent systems without either hiding or overreacting to them, holding onto orientation during long codebase-exploration sessions, calibrating confidence for human review routing, and preserving source provenance when synthesizing findings from multiple places.

---

## Task Statements

- **5.1 — Manage conversation context to preserve critical information across long interactions.** Progressive-summarization risk, the "lost in the middle" effect, tool-result bloat, case-facts persistence.
- **5.2 — Design effective escalation and ambiguity resolution patterns.** Explicit escalation triggers, honoring explicit human requests immediately, why sentiment/self-reported confidence are unreliable, clarification over heuristic selection on multiple matches.
- **5.3 — Implement error propagation strategies across multi-agent systems.** Structured error context, access failures vs. valid empty results, avoiding silent suppression and total-workflow termination, coverage annotations.
- **5.4 — Manage context effectively in large codebase exploration.** Context degradation in extended sessions, scratchpad files, subagent delegation for isolating verbose output, `/compact`, crash-recovery manifests.
- **5.5 — Design human review workflows and confidence calibration.** Aggregate-metric masking, stratified random sampling, field-level confidence calibration, routing low-confidence extractions to review.
- **5.6 — Preserve information provenance and handle uncertainty in multi-source synthesis.** Claim-source mappings, annotating conflicting statistics instead of arbitrarily picking one, temporal data / publication dates, content-type-appropriate rendering.

---

## Theory Notes

1. [[Theory/01_Context_Preservation_and_Escalation|01 — Context Preservation & Escalation]] — Tasks 5.1 & 5.2.
2. [[Theory/02_Error_Propagation_and_Codebase_Context|02 — Error Propagation & Codebase Context]] — Tasks 5.3 & 5.4.
3. [[Theory/03_Human_Review_and_Provenance|03 — Human Review & Provenance]] — Tasks 5.5 & 5.6.

---

## Exercises

[[Exercises/Setup|Setup instructions]]

| Language | File | What it covers |
| -------- | ---- | -------------- |
| Python | `Exercises/python/01_case_facts.py` | Extracting a persistent case-facts block from verbose tool-result JSON |
| Python | `Exercises/python/02_escalation_decision.py` | Criteria + few-shot escalation decisions vs. self-reported confidence |
| Python | `Exercises/python/03_error_propagation.py` | Structured error context on a simulated subagent timeout |
| JavaScript | `Exercises/javascript/01_case_facts.js` | Case-facts extraction pattern in Node.js |
| JavaScript | `Exercises/javascript/02_escalation_and_errors.js` | Escalation decision function + structured error propagation in Node.js |
| TypeScript | `Exercises/typescript/01_context_reliability.ts` | Typed case-facts, escalation, and structured-error-propagation patterns together |

---

## Practice Exam

[[Practice_Exam|Take the practice exam]] — 18 questions spanning all six task statements.

---

## Related

- [[../00_Exam_Guide/_Index|Exam Guide]]
- [[../Home|Home]]

---

## Key Concepts Checklist

- [ ] Explain why progressive summarization is risky for numbers, dates, and stated expectations — and describe the case-facts pattern that avoids it
- [ ] Describe the "lost in the middle" effect and the mitigation (key findings at the start, with headers)
- [ ] Write escalation criteria that distinguish "explicit human request" and "policy gap" from "merely complex but resolvable"
- [ ] Explain why sentiment and self-reported confidence scores are unreliable escalation triggers
- [ ] Describe the difference between an access failure and a valid empty result, and why collapsing them is a bug
- [ ] Name the two anti-patterns in error propagation (silent suppression, total-workflow termination) and the local-recovery alternative
- [ ] Describe how a scratchpad file and subagent delegation counteract context degradation in long codebase exploration
- [ ] Explain why aggregate accuracy metrics can mask poor performance on a specific document type or field
- [ ] Describe stratified random sampling and what it's meant to catch that a one-time validation pass would miss
- [ ] Explain claim-source mapping preservation and why conflicting statistics should be annotated, not arbitrarily resolved
